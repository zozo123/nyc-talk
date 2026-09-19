#!/usr/bin/env python3
"""Four synthetic authority-boundary experiments. No LLM or external services."""
from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import platform
import secrets
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASK = "parser-fix"
CANARY = "SYNTHETIC-PRIVATE-FIXTURE"
POLICY = "comma-separated-integers-v1"
GOOD = """import json, sys
try:
    fields = sys.argv[1].split(",")
    if any(not field.strip() for field in fields):
        raise ValueError("empty field")
    print(json.dumps([int(field) for field in fields]))
except ValueError:
    print(json.dumps("REJECT"))
"""
BAD = GOOD.replace('    if any(not field.strip() for field in fields):\n        raise ValueError("empty field")\n', '').replace('for field in fields]', 'for field in fields if field.strip()]')
CASES = [("1,2,3", [1, 2, 3]), ("1,,3", "REJECT"), ("", "REJECT"),
         ("-2, 3", [-2, 3]), ("x", "REJECT")]


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(data):
    return hashlib.sha256(data).hexdigest()


class Service:
    """Loopback-only synthetic API. Policy lives outside the agent process."""

    def __init__(self):
        now = time.time()
        self.tokens = {
            "fixture-runner": {"scope": "all", "aud": "lab", "exp": now + 600},
            "fixture-task": {"scope": TASK, "aud": "lab", "exp": now + 60},
            "fixture-expired": {"scope": TASK, "aud": "lab", "exp": now - 1},
            "fixture-wrong-audience": {"scope": TASK, "aud": "other", "exp": now + 60},
        }
        self.events = []
        self.deliveries = []
        service = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *_args):
                pass

            def reply(self, status, body):
                data = canonical(body)
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def do_GET(self):
                token = self.headers.get("Authorization", "").removeprefix("Bearer ")
                grant = service.tokens.get(token)
                allowed = bool(grant and grant["aud"] == "lab" and grant["exp"] > time.time()
                               and (grant["scope"] == "all" or self.path == "/input/parser-fix"))
                service.events.append({"path": self.path, "allowed": allowed})
                if not allowed:
                    return self.reply(403, {"decision": "DENIED"})
                if self.path == "/projects/other/private":
                    return self.reply(200, {"fixture": CANARY})
                if self.path == "/input/parser-fix":
                    return self.reply(200, {"task": TASK})
                self.reply(404, {"decision": "UNKNOWN"})

            def do_POST(self):
                # Model an allowed upload service with different account upload URLs.
                # These synthetic upload capabilities intentionally allow both paths.
                length = int(self.headers.get("Content-Length", "0"))
                if length > 4096:
                    return self.reply(413, {"decision": "TOO_LARGE"})
                body = json.loads(self.rfile.read(length))
                if self.path not in ("/accounts/team/reports", "/accounts/other/uploads"):
                    return self.reply(404, {"decision": "UNKNOWN"})
                service.deliveries.append({"path": self.path, "body": body})
                self.reply(201, {"decision": "STORED"})

        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.url = f"http://127.0.0.1:{self.httpd.server_port}"
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)

    def __enter__(self):
        self.thread.start()
        return self

    def __exit__(self, *_):
        self.httpd.shutdown()
        self.thread.join(timeout=3)
        self.httpd.server_close()


class Runner:
    def __init__(self, mode, directory):
        self.mode = mode
        self.directory = directory
        self.count = 0
        self.invocations = []

    def run(self, code, *, mounts=(), env=None, network=True, args=()):
        """Launch only committed lab fixtures. Reference mode provides no sandbox."""
        self.count += 1
        agent = self.directory / f"agent-{self.count}.py"
        agent.write_text(code)
        clean_env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8"}
        clean_env.update(env or {})
        if self.mode == "isolated":
            command = [
                "bwrap", "--unshare-user", "--unshare-pid", "--unshare-ipc",
                "--unshare-uts", "--die-with-parent", "--new-session",
                "--cap-drop", "ALL", "--ro-bind", "/usr", "/usr",
            ]
            for directory in ("/lib", "/lib64"):
                if Path(directory).exists():
                    command.extend(["--ro-bind", directory, directory])
            command.extend(["--proc", "/proc", "--dev", "/dev",
                            "--tmpfs", "/tmp", "--dir", "/app",
                            "--ro-bind", str(agent), "/app/agent.py"])
            if not network:
                command.append("--unshare-net")
            for host, guest, writable in mounts:
                command.extend(["--bind" if writable else "--ro-bind", str(host), guest])
            command.extend(["--chdir", "/tmp", "/usr/bin/python3", "-I", "-B",
                            "/app/agent.py", *args])
        else:
            # Only our deterministic fixtures run here. No security claim.
            for host, guest, _writable in mounts:
                code = code.replace(guest, str(host))
            agent.write_text(code)
            command = [sys.executable, "-I", "-B", str(agent), *args]
        proc = subprocess.run(command, env=clean_env, capture_output=True, text=True,
                              timeout=15, close_fds=True)
        self.invocations.append({
            "agent_sha256": digest(agent.read_bytes()),
            "network_namespace": self.mode == "isolated" and not network,
            "mode": self.mode, "exit_code": proc.returncode,
            "stdout": proc.stdout.strip(), "stderr": proc.stderr.strip(),
            "mounts": [{"guest": g, "writable": w} for _, g, w in mounts],
        })
        if proc.returncode != 0:
            raise RuntimeError(f"agent {self.count} failed ({proc.returncode}): {proc.stderr}")
        return proc.stdout.strip()


def read_api(path):
    return f"""import json, os, urllib.request, urllib.error
req = urllib.request.Request(os.environ["LAB_URL"] + {path!r},
    headers={{"Authorization": "Bearer " + os.environ.get("LAB_TOKEN", "")}})
try:
    with urllib.request.urlopen(req, timeout=2) as response:
        print(json.dumps({{"status": response.status, "body": json.load(response)}}))
except urllib.error.HTTPError as error:
    print(json.dumps({{"status": error.code}}))
"""


def post_api(path, body):
    return f"""import json, os, urllib.request
request = urllib.request.Request(os.environ["LAB_URL"] + {path!r},
    data=json.dumps({body!r}).encode(), headers={{"Content-Type": "application/json"}})
with urllib.request.urlopen(request, timeout=2) as response:
    print(response.status)
"""


def broker(service, request):
    # Untrusted agent output is a request only. Exact keys, fixed destination and
    # broker-owned payload remove arbitrary strings from this one report operation.
    if request != {"operation": "publish_report", "task": TASK}:
        return "DENIED"
    import urllib.request
    body = {"task": TASK, "status": "completed"}
    req = urllib.request.Request(service.url + "/accounts/team/reports",
                                 data=canonical(body),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=2) as response:
        return "ACCEPTED" if response.status == 201 else "DENIED"


def verify(runner, artifact, directory):
    # Snapshot after the producer exits. The agent never gets this host path.
    snapshot = directory / ("snapshot-" + secrets.token_hex(4))
    snapshot.mkdir()
    (snapshot / "parser.py").write_bytes(artifact)
    outcomes = []
    for value, expected in CASES:
        result = runner.run(
            'import runpy\nrunpy.run_path("/candidate/parser.py", run_name="__main__")',
            mounts=[(snapshot, "/candidate", False)], network=False, args=[value])
        outcomes.append(json.loads(result) == expected)
    return all(outcomes), outcomes


class Gate:
    def __init__(self):
        self.key = secrets.token_bytes(32)
        self.run = secrets.token_hex(16)
        self.used = set()
        self.verifier = digest(Path(__file__).read_bytes())

    def issue(self, artifact, accepted):
        value = {"run": self.run, "artifact": digest(artifact), "accepted": accepted,
                 "verifier": self.verifier, "policy": POLICY, "nonce": secrets.token_hex(8)}
        return {"value": value, "mac": hmac.new(self.key, canonical(value), "sha256").hexdigest()}

    def publish(self, approval, artifact):
        value = approval["value"]
        expected = hmac.new(self.key, canonical(value), "sha256").hexdigest()
        valid = (hmac.compare_digest(expected, approval["mac"])
                 and value["run"] == self.run and value["artifact"] == digest(artifact)
                 and value["accepted"] is True and value["verifier"] == self.verifier
                 and value["policy"] == POLICY and value["nonce"] not in self.used)
        if valid:
            self.used.add(value["nonce"])
        return valid


def chain(events):
    head = "0" * 64
    for event in events:
        head = digest(head.encode() + canonical(event))
    return head


def experiments(mode):
    results = []

    def check(name, passed, detail):
        results.append({"check": name, "status": "PASS" if passed else "FAIL", "detail": detail})
        if not passed:
            raise AssertionError(f"{name}: {detail}")

    def skip(name, detail):
        results.append({"check": name, "status": "SKIP", "detail": detail})

    with tempfile.TemporaryDirectory(prefix="nyc-talk-") as tmp, Service() as service:
        directory = Path(tmp)
        runner = Runner(mode, directory)
        if mode == "isolated":
            state = json.loads(runner.run(
                'import json, os\nprint(json.dumps({n: os.readlink("/proc/self/ns/"+n) for n in ("user","pid","mnt")}))'))
            check("isolation.namespaces", all(v != os.readlink("/proc/self/ns/" + k)
                                             for k, v in state.items()),
                  "Child user, PID and mount namespace IDs differ from controller.")
        else:
            skip("isolation.namespaces", "Reference mode has no process or filesystem sandbox.")

        # Act 1: only a synthetic parent credential is intentionally inherited.
        parent_env = {"LAB_URL": service.url, "LAB_TOKEN": "fixture-runner"}
        before = json.loads(runner.run(read_api("/projects/other/private"), env=parent_env))
        check("credentials.before", before["status"] == 200 and before["body"]["fixture"] == CANARY,
              "Broad inherited fixture token reads unrelated project.")
        projected = {"LAB_URL": service.url, "LAB_TOKEN": "fixture-task"}
        after = json.loads(runner.run(read_api("/projects/other/private"), env=projected))
        check("credentials.after", after["status"] == 403, "Scoped token receives HTTP 403.")
        legitimate = json.loads(runner.run(read_api("/input/parser-fix"), env=projected))
        check("credentials.positive", legitimate["status"] == 200, "Task input remains readable.")
        for token in ("fixture-expired", "fixture-wrong-audience"):
            result = json.loads(runner.run(read_api("/input/parser-fix"),
                                env={"LAB_URL": service.url, "LAB_TOKEN": token}))
            check("credentials." + token, result["status"] == 403, "Service rejects token.")

        # Act 2: a separate host fixture, unrelated to verification.
        shared = directory / "shared"; shared.mkdir()
        output = directory / "output"; output.mkdir()
        target = shared / "next-job.json"
        original = b'{"queue":"normal"}\n'
        attack = """import json
from pathlib import Path
try:
    Path("/shared/next-job.json").write_text('{"queue":"attacker"}\\n')
    status = "WRITE_SUCCEEDED"
except OSError:
    status = "WRITE_DENIED"
Path("/output/patch.txt").write_text("legitimate patch output")
print(json.dumps({"write":status}))
"""
        if mode == "isolated":
            target.write_bytes(original)
            before = json.loads(runner.run(attack, mounts=[
                (shared, "/shared", True), (output, "/output", True)], network=False))
            check("mount.before", before["write"] == "WRITE_SUCCEEDED" and target.read_bytes() != original,
                  "Writable bind changes the next-job fixture on the host.")
            target.write_bytes(original)
            (output / "patch.txt").unlink()
            after = json.loads(runner.run(attack, mounts=[
                (shared, "/shared", False), (output, "/output", True)], network=False))
            check("mount.after", after["write"] == "WRITE_DENIED" and target.read_bytes() == original,
                  "Read-only bind blocks the same write; host fixture unchanged.")
            check("mount.positive", (output / "patch.txt").read_text() == "legitimate patch output",
                  "Task output remains writable.")
        else:
            skip("mount.integration", "Requires real bind mounts. No chmod or mocked substitute.")

        # Act 3: permitted upload service, wrong account and arbitrary bytes.
        runner.run(post_api("/accounts/other/uploads", {"data": CANARY}),
                   env={"LAB_URL": service.url})
        check("egress.before", service.deliveries[-1] == {
            "path": "/accounts/other/uploads", "body": {"data": CANARY}},
            "Loopback service stores synthetic private bytes under the other account.")
        delivery_count = len(service.deliveries)
        for suffix, extra in (("recipient", {"recipient": "other"}),
                              ("payload", {"data": CANARY}),
                              ("url", {"url": service.url + "/accounts/other/uploads"})):
            request = {"operation": "publish_report", "task": TASK, **extra}
            # Request is emitted by an actual child, then validated outside it.
            emitted = runner.run("print(" + repr(json.dumps(request)) + ")", network=False)
            check("egress." + suffix, broker(service, json.loads(emitted)) == "DENIED",
                  "Broker rejects unapproved request fields.")
        check("egress.no_delivery", len(service.deliveries) == delivery_count,
              "Rejected requests create no receiving-service deliveries.")
        if mode == "isolated":
            unreachable = runner.run("""import os, urllib.request, urllib.error
try:
    urllib.request.urlopen(os.environ["LAB_URL"], timeout=1)
    print("REACHABLE")
except (urllib.error.URLError, TimeoutError, OSError):
    print("UNREACHABLE")
""", network=False, env={"LAB_URL": service.url})
            check("egress.bypass", unreachable == "UNREACHABLE",
                  "New network namespace cannot reach host loopback fixture service.")
        else:
            skip("egress.bypass", "Reference mode cannot prove network isolation.")
        emitted = runner.run('print(\'{"operation":"publish_report","task":"parser-fix"}\')', network=False)
        check("egress.positive", broker(service, json.loads(emitted)) == "ACCEPTED"
              and service.deliveries[-1]["path"] == "/accounts/team/reports"
              and CANARY not in json.dumps(service.deliveries[-1]),
              "Broker constructs a fixed report for the team account.")

        # Act 4: mutable success criteria, then external verification of exact bytes.
        work = directory / "work"; work.mkdir()
        (work / "parser.py").write_text(BAD)
        (work / "check.py").write_text('raise SystemExit(1)\n')
        tamper = """from pathlib import Path
Path("/work/check.py").write_text('print("PASS")\\nraise SystemExit(0)\\n')
"""
        runner.run(tamper, mounts=[(work, "/work", True)], network=False)
        result = runner.run('import runpy\nrunpy.run_path("/work/check.py", run_name="__main__")',
                            mounts=[(work, "/work", False)], network=False)
        check("verifier.before", result == "PASS" and (work / "parser.py").read_text() == BAD,
              "Changed checker returns success while buggy parser bytes remain unchanged.")
        invalid = (work / "parser.py").read_bytes()
        accepted, outcomes = verify(runner, invalid, directory)
        check("verifier.after", not accepted and outcomes == [True, False, False, True, True],
              "External cases reject the same buggy parser on empty fields and empty input.")
        accepted, outcomes = verify(runner, GOOD.encode(), directory)
        check("verifier.positive", accepted, "Fixed parser passes all five external cases.")
        gate = Gate()
        rejected = gate.issue(invalid, False)
        check("gate.invalid", not gate.publish(rejected, invalid), "Rejected artifact cannot publish.")
        approval = gate.issue(GOOD.encode(), True)
        check("gate.substitution", not gate.publish(approval, invalid),
              "Approval does not authorize substituted bytes.")
        check("gate.cross_run", not Gate().publish(approval, GOOD.encode()), "Other run rejects approval.")
        saved_run = gate.run
        gate.run = "different-task-run"
        check("gate.stale_run", not gate.publish(approval, GOOD.encode()),
              "Authentic approval with the same MAC key cannot authorize a different run.")
        gate.run = saved_run
        saved_verifier = gate.verifier
        gate.verifier = "changed-verifier"
        check("gate.verifier_changed", not gate.publish(approval, GOOD.encode()),
              "Authentic approval cannot authorize a changed verifier identity.")
        gate.verifier = saved_verifier
        forged = json.loads(json.dumps(approval)); forged["value"]["artifact"] = digest(invalid)
        check("gate.forgery", not gate.publish(forged, invalid), "Modified approval fails authentication.")
        check("gate.positive", gate.publish(approval, GOOD.encode()), "Verified bytes publish.")
        check("gate.replay", not gate.publish(approval, GOOD.encode()), "Consumed approval cannot replay.")
        events = [{"artifact": digest(invalid), "accepted": False},
                  {"artifact": digest(GOOD.encode()), "accepted": True}]
        anchor = chain(events)
        rewritten = [{"artifact": digest(invalid), "accepted": True}, events[1]]
        check("history.rewrite", chain(rewritten) != anchor,
              "Recomputed attacker chain disagrees with independently retained controller head.")

        # Final run: same task, restricted worker, independent check and publication.
        final_output = directory / "final-output"; final_output.mkdir()
        source = directory / "source"; source.mkdir()
        (source / "parser.py").write_text(BAD)
        agent = f"""from pathlib import Path
import json
assert Path("/input/parser.py").exists()
Path("/output/parser.py").write_text({GOOD!r})
print(json.dumps({{"operation":"publish_report","task":"parser-fix"}}))
"""
        emitted = runner.run(agent, mounts=[(source, "/input", False),
                            (final_output, "/output", True)], network=False)
        artifact = (final_output / "parser.py").read_bytes()
        accepted, _ = verify(runner, artifact, directory)
        final_gate = Gate()
        publication = final_gate.publish(final_gate.issue(artifact, accepted), artifact)
        # Publication succeeds first; only then is the fixed report operation allowed.
        report = broker(service, json.loads(emitted)) if publication else "DENIED"
        check("final.task", publication and report == "ACCEPTED",
              "Worker emits fixed parser; external verifier accepts; exact bytes publish; report delivered.")
        return {"mode": mode, "checks": results, "invocations": runner.invocations,
                "service_events": service.events, "deliveries": service.deliveries}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("isolated", "reference"), default="isolated")
    parser.add_argument("--output", type=Path, default=ROOT / "build/evidence")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    try:
        result = experiments(args.mode)
    except Exception as error:
        failure = {"mode": args.mode, "status": "FAILED", "error": str(error)}
        (args.output / "failure.json").write_text(json.dumps(failure, indent=2) + "\n")
        print(json.dumps(failure))
        return 1
    sources = {str(p.relative_to(ROOT)): digest(p.read_bytes())
               for p in sorted((ROOT / "lab").glob("*.py"))}
    result["source_sha256"] = sources
    result["platform"] = {"system": platform.system(), "machine": platform.machine(),
                          "python": platform.python_version()}
    result["commit"] = os.environ.get("GITHUB_SHA")
    result["status"] = "PASS" if args.mode == "isolated" else "REFERENCE_ONLY"
    result["limitations"] = [
        "Synthetic, deterministic worker scripts; no model-driven prompt injection claim.",
        "Shared host network in credential and weak-egress cases is deliberate.",
        "No cgroup, seccomp, kernel-exploit, side-channel or universal noninterference claim.",
        "Finite parser cases do not prove correctness for every possible input.",
        "Controller-held MAC key and history head are the trusted lab anchors.",
    ]
    (args.output / "results.json").write_text(json.dumps(result, indent=2) + "\n")
    transcript = [f"MODE {args.mode} / STATUS {result['status']}"]
    transcript += [f"{r['status']:4} {r['check']}: {r['detail']}" for r in result["checks"]]
    (args.output / "transcript.txt").write_text("\n".join(transcript) + "\n")
    print("\n".join(transcript))
    print("EVIDENCE_JSON " + json.dumps(result, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
