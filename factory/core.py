"""Controller-owned freeze, comparison and gate.

Independence is not a second VM. The accept environment executes the frozen
candidate. The controller owns expected results and the comparison. Publication
reads the frozen object, never the live producer path.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
import secrets
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

SCHEMA = 1
TASK = "lock-admin"
POLICY = "admin-requires-auth-v1"
SUBJECT = "handler.py"
MAX_FILE = 64_000
ALLOWED = {SUBJECT}

# Synthetic HTTP front door. argv is "route:auth". Prints a status code.
GOOD = """import json, sys
route, auth = sys.argv[1].split(":", 1)
if route == "public":
    print(json.dumps(200))
elif route == "admin":
    if auth == "admin":
        print(json.dumps(200))
    elif auth == "user":
        print(json.dumps(403))
    else:
        print(json.dumps(401))
else:
    print(json.dumps(404))
"""
# Always 200: unauthenticated /admin is open. This is the shipped bug.
BAD = """import json, sys
sys.argv[1].split(":", 1)
print(json.dumps(200))
"""
CASES = [
    ("admin:none", 401),
    ("admin:admin", 200),
    ("admin:user", 403),
    ("public:none", 200),
    ("admin:expired", 401),
]
# Worker-written spec: every request is allowed. Matches BAD.
WORKER_EXPECTED = [{"input": value, "output": 200} for value, _ in CASES]
WEAK_CHECKER = """import json, subprocess, sys
from pathlib import Path
expected = json.loads(Path("expected.json").read_text())
ok = True
for case in expected:
    out = subprocess.check_output([sys.executable, "handler.py", case["input"]], text=True)
    if json.loads(out) != case["output"]:
        ok = False
print("PASS" if ok else "FAIL")
raise SystemExit(0 if ok else 1)
"""


def canonical(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def policy_digest() -> str:
    return digest(canonical({"id": POLICY, "task": TASK, "cases": CASES}))


def expected_digest(cases=CASES) -> str:
    return digest(canonical(cases))


def verifier_bundle_digest(launch: dict) -> str:
    source = Path(__file__).read_bytes()
    return digest(canonical({"source": digest(source), "launch": launch}))


@dataclass
class Frozen:
    digest: str
    manifest: dict
    files: dict


def freeze(files: dict[str, bytes]) -> Frozen:
    """Collect, bound, store as an immutable object, then hash the manifest."""
    if not files:
        raise ValueError("empty artifact")
    entries = []
    stored = {}
    for name in sorted(files):
        if name not in ALLOWED:
            raise ValueError(f"path not permitted: {name}")
        if "/" in name or name.startswith(".") or ".." in name:
            raise ValueError(f"illegal path: {name}")
        data = files[name]
        if len(data) > MAX_FILE:
            raise ValueError(f"file too large: {name}")
        stored[name] = data
        entries.append({
            "path": name,
            "type": "file",
            "mode": "0644",
            "size": len(data),
            "sha256": digest(data),
        })
    manifest = {"schema": SCHEMA, "files": entries}
    return Frozen(digest=digest(canonical(manifest)), manifest=manifest, files=stored)


def persist(frozen: Frozen, store: Path) -> Path:
    dest = store / frozen.digest
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "manifest.json").write_bytes(canonical(frozen.manifest))
    files = dest / "files"
    files.mkdir(exist_ok=True)
    for name, data in frozen.files.items():
        (files / name).write_bytes(data)
    return dest


def execute_frozen(candidate: bytes, timeout: float = 5.0) -> list[dict]:
    """Run frozen bytes as untrusted code. Timeout/malformed is not a verdict."""
    outputs = []
    with tempfile.TemporaryDirectory(prefix="factory-accept-") as tmp:
        path = Path(tmp) / SUBJECT
        path.write_bytes(candidate)
        env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"}
        for value, _expected in CASES:
            try:
                proc = subprocess.run(
                    [sys.executable, "-I", "-B", str(path), value],
                    capture_output=True, text=True, timeout=timeout,
                    cwd=tmp, env=env,
                )
            except subprocess.TimeoutExpired:
                outputs.append({"status": "timeout"})
                continue
            if proc.returncode != 0:
                outputs.append({"status": "error", "code": proc.returncode})
                continue
            try:
                outputs.append({"status": "ok", "value": json.loads(proc.stdout)})
            except json.JSONDecodeError:
                outputs.append({"status": "malformed"})
    return outputs


def execute_weak_checker(candidate: bytes, expected_doc) -> dict:
    """Protected checker file, worker-controlled expected.json in the same cwd."""
    with tempfile.TemporaryDirectory(prefix="factory-weak-") as tmp:
        root = Path(tmp)
        (root / SUBJECT).write_bytes(candidate)
        (root / "expected.json").write_bytes(canonical(expected_doc))
        (root / "checker.py").write_text(WEAK_CHECKER)
        proc = subprocess.run(
            [sys.executable, "-I", "-B", str(root / "checker.py")],
            capture_output=True, text=True, timeout=10, cwd=root,
            env={"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"},
        )
        return {
            "exit": proc.returncode,
            "stdout": proc.stdout.strip(),
            "checker_sha256": digest(WEAK_CHECKER.encode()),
            "expected_sha256": digest(canonical(expected_doc)),
        }


def judge(outputs: list[dict]) -> dict:
    """Controller-owned comparison. Incomplete evidence yields no approval."""
    if len(outputs) != len(CASES):
        return {"kind": "no_approval", "reason": "incomplete"}
    if any(item["status"] != "ok" for item in outputs):
        return {"kind": "no_approval", "reason": "timeout_or_malformed"}
    matches = [item["value"] == expected for item, (_, expected) in zip(outputs, CASES)]
    return {
        "kind": "verdict",
        "accepted": all(matches),
        "matches": matches,
    }


class Gate:
    def __init__(self, store: Path):
        self.key = secrets.token_bytes(32)
        self.run = secrets.token_hex(16)
        self.store = store
        self.store.mkdir(parents=True, exist_ok=True)
        self.used_path = store / "used-nonces.json"
        self.pub_path = store / "publication.jsonl"
        if not self.used_path.exists():
            self.used_path.write_text("[]\n")

    def _used(self) -> set[str]:
        return set(json.loads(self.used_path.read_text()))

    def _remember(self, nonce: str) -> None:
        used = self._used()
        used.add(nonce)
        self.used_path.write_text(json.dumps(sorted(used)) + "\n")

    def issue(self, *, artifact: Frozen, accepted: bool, launch: dict, env_manifest: dict) -> dict:
        value = {
            "schema_version": SCHEMA,
            "task_id": TASK,
            "run_id": self.run,
            "artifact_manifest_digest": artifact.digest,
            "verifier_bundle_digest": verifier_bundle_digest(launch),
            "expected_results_digest": expected_digest(),
            "policy_digest": policy_digest(),
            "acceptance_environment_manifest_digest": digest(canonical(env_manifest)),
            "decision": "accept" if accepted else "reject",
            "nonce": secrets.token_hex(8),
        }
        return {"value": value, "mac": hmac.new(self.key, canonical(value), "sha256").hexdigest()}

    def authorize(self, approval: dict, artifact: Frozen, launch: dict, env_manifest: dict) -> bool:
        value = approval["value"]
        expected_mac = hmac.new(self.key, canonical(value), "sha256").hexdigest()
        ok = (
            hmac.compare_digest(expected_mac, approval["mac"])
            and value["schema_version"] == SCHEMA
            and value["task_id"] == TASK
            and value["run_id"] == self.run
            and value["artifact_manifest_digest"] == artifact.digest
            and value["verifier_bundle_digest"] == verifier_bundle_digest(launch)
            and value["expected_results_digest"] == expected_digest()
            and value["policy_digest"] == policy_digest()
            and value["acceptance_environment_manifest_digest"] == digest(canonical(env_manifest))
            and value["decision"] == "accept"
            and value["nonce"] not in self._used()
        )
        if ok:
            self._remember(value["nonce"])
        return ok

    def publish(self, approval: dict, artifact: Frozen, launch: dict, env_manifest: dict) -> str:
        if not self.authorize(approval, artifact, launch, env_manifest):
            return "DENIED"
        record = {
            "artifact": artifact.digest,
            "run": self.run,
            "nonce": approval["value"]["nonce"],
        }
        with self.pub_path.open("a") as handle:
            handle.write(json.dumps(record) + "\n")
        return "PUBLISHED"

    def replay_or_swap(self, approval: dict, artifact: Frozen, launch: dict, env_manifest: dict) -> str:
        return self.publish(approval, artifact, launch, env_manifest)
