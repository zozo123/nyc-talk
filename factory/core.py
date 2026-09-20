"""Small reference acceptance gate, not a production execution sandbox.

Only the committed deterministic fixtures may run through the local executor.
Controller memory, policy, signing key and store are trusted. Isolated mode uses
bubblewrap; it does not claim resistance to kernel attacks or hostile output DoS.
The release operation atomically stores the actual approved bytes in SQLite.
"""
from __future__ import annotations

from contextlib import closing
import hashlib
import hmac
import json
import secrets
import sqlite3
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

SCHEMA = 2
TASK = "lock-admin"
POLICY = "admin-requires-auth-v1"
SUBJECT = "handler.py"
MAX_FILE = 64_000
ROOT = Path(__file__).resolve().parents[1]

# Status-code model, not a web server. No HTTP /admin traffic is claimed here.
GOOD = '''import json, sys
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
'''
BAD = '''import json, sys
sys.argv[1].split(":", 1)
print(json.dumps(200))
'''
CASES = (("admin:none", 401), ("admin:admin", 200), ("admin:user", 403),
         ("public:none", 200), ("admin:expired", 401))
WORKER_EXPECTED = [{"input": value, "output": 200} for value, _ in CASES]
WEAK_CHECKER = '''import json, subprocess, sys
from pathlib import Path
expected = json.loads(Path("expected.json").read_text())
ok = True
for case in expected:
    out = subprocess.check_output([sys.executable, "handler.py", case["input"]], text=True)
    if json.loads(out) != case["output"]:
        ok = False
print("PASS" if ok else "FAIL")
raise SystemExit(0 if ok else 1)
'''


def canonical(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def source_hashes() -> dict[str, str]:
    paths = [*sorted((ROOT / "factory").glob("*.py")), ROOT / "lab/run.py"]
    return {str(p.relative_to(ROOT)): digest(p.read_bytes()) for p in paths}


def policy_digest() -> str:
    return digest(canonical({"id": POLICY, "task": TASK, "cases": CASES}))


def expected_digest() -> str:
    return digest(canonical(CASES))


def verifier_bundle_digest(launch: dict) -> str:
    return digest(canonical({"source": source_hashes(), "launch": launch}))


@dataclass(frozen=True)
class Frozen:
    """One bounded immutable payload. Manifests and identities are derived."""
    payload: bytes

    def __post_init__(self):
        if type(self.payload) is not bytes or len(self.payload) > MAX_FILE:
            raise ValueError("candidate must be bounded bytes")

    @property
    def files(self) -> dict[str, bytes]:
        return {SUBJECT: self.payload}  # A fresh view cannot mutate this object.

    @property
    def manifest(self) -> dict:
        return {"schema": SCHEMA, "files": [{"path": SUBJECT, "type": "file",
                "mode": "0644", "size": len(self.payload), "sha256": digest(self.payload)}]}

    @property
    def digest(self) -> str:
        return digest(canonical(self.manifest))


def freeze(files: dict[str, bytes]) -> Frozen:
    if type(files) is not dict or set(files) != {SUBJECT}:
        raise ValueError("exactly handler.py is required")
    return Frozen(files[SUBJECT])


def persist(frozen: Frozen, store: Path) -> Path:
    """Controller-owned inspection copy; publication independently binds bytes."""
    frozen = freeze(frozen.files)
    dest = store / frozen.digest
    dest.mkdir(parents=True, exist_ok=True)
    for path, data in ((dest / "manifest.json", canonical(frozen.manifest)),
                       (dest / SUBJECT, frozen.payload)):
        try:
            with path.open("xb") as handle:
                handle.write(data)
        except FileExistsError:
            if path.is_symlink() or path.read_bytes() != data:
                raise ValueError("stored artifact disagrees with its digest")
    return dest


def execute_frozen(candidate: bytes, timeout: float = 5.0, *, isolated: bool = False) -> list[dict]:
    """Evaluate committed fixtures. Local mode is explicitly NOT containment."""
    outputs = []
    with tempfile.TemporaryDirectory(prefix="factory-accept-") as tmp:
        root = Path(tmp)
        subject = root / "candidate"
        subject.mkdir()
        path = subject / SUBJECT
        path.write_bytes(candidate)
        env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"}
        if isolated:
            from lab.run import Runner
            runner = Runner("isolated", root)
        for value, _ in CASES:
            try:
                if isolated:
                    out = runner.run('import runpy\nrunpy.run_path("/candidate/handler.py", run_name="__main__")',
                                     mounts=[(subject, "/candidate", False)], network=False, args=[value])
                else:
                    proc = subprocess.run([sys.executable, "-I", "-B", str(path), value],
                                          capture_output=True, text=True, timeout=timeout, cwd=tmp, env=env)
                    if proc.returncode != 0:
                        outputs.append({"status": "error", "code": proc.returncode})
                        continue
                    out = proc.stdout
                if len(out) > 256:
                    raise ValueError("oversized fixture result")
                result = json.loads(out)
                if type(result) is not int:
                    raise ValueError("status must be an integer")
                outputs.append({"status": "ok", "value": result})
            except subprocess.TimeoutExpired:
                outputs.append({"status": "timeout"})
            except (ValueError, RuntimeError):
                outputs.append({"status": "malformed_or_execution_error"})
    return outputs


def execute_weak_checker(candidate: bytes, expected_doc, *, isolated: bool = False) -> dict:
    """Keep checker bytes unchanged; worker controls expected.json. No model."""
    with tempfile.TemporaryDirectory(prefix="factory-weak-") as tmp:
        root = Path(tmp)
        work, verifier = root / "work", root / "verifier"
        work.mkdir(); verifier.mkdir()
        (work / SUBJECT).write_bytes(candidate)
        checker = verifier / "checker.py"
        checker.write_text(WEAK_CHECKER)
        before = digest(checker.read_bytes())
        denied = None
        if isolated:
            from lab.run import Runner
            runner = Runner("isolated", root)
            mounts = [(work, "/work", True), (verifier, "/verifier", False)]
            edit = 'from pathlib import Path\n' + (
                'try:\n    Path("/verifier/checker.py").write_text("print(42)")\n'
                '    print("WRITABLE")\nexcept OSError:\n    print("DENIED")\n')
            edit += 'Path("/work/expected.json").write_text(' + repr(canonical(expected_doc).decode()) + ')\n'
            denied = runner.run(edit, mounts=mounts, network=False) == "DENIED"
            out = runner.run('import os, runpy\nos.chdir("/work")\nrunpy.run_path("/verifier/checker.py", run_name="__main__")',
                             mounts=mounts, network=False)
            exit_code = 0
        else:
            (work / "expected.json").write_bytes(canonical(expected_doc))
            proc = subprocess.run([sys.executable, "-I", "-B", str(checker)], capture_output=True,
                                  text=True, timeout=10, cwd=work,
                                  env={"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8"})
            out, exit_code = proc.stdout.strip(), proc.returncode
        return {"exit": exit_code, "stdout": out, "checker_sha256_before": before,
                "checker_sha256_after": digest(checker.read_bytes()), "checker_write_denied": denied,
                "expected_sha256": digest((work / "expected.json").read_bytes())}


def judge(outputs: list[dict]) -> dict:
    if type(outputs) is not list or len(outputs) != len(CASES):
        return {"kind": "no_approval", "reason": "incomplete"}
    if any(type(x) is not dict or x.get("status") != "ok" or type(x.get("value")) is not int for x in outputs):
        return {"kind": "no_approval", "reason": "invalid_evidence"}
    matches = [x["value"] == expected for x, (_, expected) in zip(outputs, CASES)]
    return {"kind": "verdict", "accepted": all(matches), "matches": matches}


class Gate:
    """Trusted controller API. Never expose issue() or the store to a worker.

    SQLite publication is the local reference release sink, not a deployed app.
    The UNIQUE(run, nonce) insertion atomically stores bytes and consumes approval.
    """
    def __init__(self, store: Path, *, clock: Callable[[], float] = time.time):
        self.key, self.run = secrets.token_bytes(32), secrets.token_hex(16)
        self.clock = clock
        self.store = store
        store.mkdir(parents=True, exist_ok=True)
        self.database = store / "releases.sqlite3"
        with closing(sqlite3.connect(self.database)) as conn, conn:
            conn.execute('CREATE TABLE IF NOT EXISTS releases (run TEXT, nonce TEXT, artifact TEXT, '
                         'manifest BLOB, payload BLOB, PRIMARY KEY(run, nonce))')

    def issue(self, *, artifact: Frozen, accepted: bool, launch: dict, env_manifest: dict, ttl: int = 300) -> dict:
        if type(accepted) is not bool or type(ttl) is not int or ttl <= 0:
            raise ValueError("invalid decision or TTL")
        artifact = freeze(artifact.files)
        value = {"schema_version": SCHEMA, "task_id": TASK, "run_id": self.run,
                 "artifact_manifest_digest": artifact.digest, "verifier_bundle_digest": verifier_bundle_digest(launch),
                 "expected_results_digest": expected_digest(), "policy_digest": policy_digest(),
                 "acceptance_environment_manifest_digest": digest(canonical(env_manifest)),
                 "decision": "accept" if accepted else "reject", "nonce": secrets.token_hex(16),
                 "expires_at": int(self.clock()) + ttl}
        return {"value": value, "mac": hmac.new(self.key, canonical(value), "sha256").hexdigest()}

    def authorize(self, approval: dict, artifact: Frozen, launch: dict, env_manifest: dict) -> bool:
        """Pure validation; consumption occurs in the publication transaction."""
        try:
            actual = freeze(artifact.files)
            if type(approval) is not dict or set(approval) != {"value", "mac"}:
                return False
            value = approval["value"]
            fields = {"schema_version", "task_id", "run_id", "artifact_manifest_digest", "verifier_bundle_digest",
                      "expected_results_digest", "policy_digest", "acceptance_environment_manifest_digest",
                      "decision", "nonce", "expires_at"}
            return (type(value) is dict and set(value) == fields
                    and type(approval["mac"]) is str
                    and hmac.compare_digest(hmac.new(self.key, canonical(value), "sha256").hexdigest(), approval["mac"])
                    and value["schema_version"] == SCHEMA and value["task_id"] == TASK and value["run_id"] == self.run
                    and value["artifact_manifest_digest"] == actual.digest
                    and value["verifier_bundle_digest"] == verifier_bundle_digest(launch)
                    and value["expected_results_digest"] == expected_digest() and value["policy_digest"] == policy_digest()
                    and value["acceptance_environment_manifest_digest"] == digest(canonical(env_manifest))
                    and value["decision"] == "accept" and type(value["expires_at"]) is int
                    and self.clock() < value["expires_at"] and type(value["nonce"]) is str and len(value["nonce"]) == 32)
        except (KeyError, TypeError, ValueError, AttributeError):
            return False

    def publish(self, approval: dict, artifact: Frozen, launch: dict, env_manifest: dict) -> str:
        try:
            actual = freeze(artifact.files)  # Exact immutable bytes checked AND stored.
            if not self.authorize(approval, actual, launch, env_manifest):
                return "DENIED"
            with closing(sqlite3.connect(self.database, timeout=10)) as conn, conn:
                conn.execute("BEGIN IMMEDIATE")
                if self.clock() >= approval["value"]["expires_at"]:
                    return "DENIED"
                conn.execute('INSERT INTO releases VALUES (?, ?, ?, ?, ?)',
                             (self.run, approval["value"]["nonce"], actual.digest,
                              canonical(actual.manifest), actual.payload))
            return "PUBLISHED"
        except (sqlite3.Error, KeyError, TypeError, ValueError, AttributeError):
            return "DENIED"

    def released_bytes(self, approval: dict) -> bytes | None:
        with closing(sqlite3.connect(self.database)) as conn, conn:
            row = conn.execute('SELECT artifact, manifest, payload FROM releases WHERE run=? AND nonce=?',
                               (self.run, approval["value"]["nonce"])).fetchone()
        if row is None:
            return None
        actual = freeze({SUBJECT: bytes(row[2])})
        if actual.digest != row[0] or canonical(actual.manifest) != bytes(row[1]):
            raise ValueError("corrupt release record")
        return actual.payload

    replay_or_swap = publish
