"""Controller-owned freeze, comparison and gate.

Independence is not a second VM. The accept environment executes the frozen
candidate. The controller owns expected results and the comparison. Publication
reads the frozen object, never the live producer path.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import secrets
import sqlite3
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Mapping

SCHEMA = 1
TASK = "lock-admin"
POLICY = "admin-requires-auth-v1"
SUBJECT = "handler.py"
MAX_FILE = 64_000
ALLOWED = {SUBJECT}

# CLI authorization-policy model. argv is "route:auth". Prints a status code.
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
# Deliberately faulty policy: every fixture request returns 200.
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


@dataclass(frozen=True)
class Frozen:
    digest: str
    manifest: dict
    files: Mapping[str, bytes]


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
        if type(data) is not bytes:
            raise ValueError("artifact values must be immutable bytes")
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
    return Frozen(digest=digest(canonical(manifest)), manifest=manifest, files=MappingProxyType(stored))


def validate_frozen(artifact: Frozen) -> bool:
    """Recompute both payload and manifest. Never trust a cached digest label."""
    try:
        actual = freeze(dict(artifact.files))
        return (actual.digest == artifact.digest
                and canonical(actual.manifest) == canonical(artifact.manifest))
    except (ValueError, TypeError, AttributeError, KeyError):
        return False


def persist(frozen: Frozen, store: Path) -> Path:
    """Controller-owned teaching CAS. Existing objects must match exactly."""
    if not validate_frozen(frozen):
        raise ValueError("artifact does not match its digest")
    dest = store / frozen.digest
    if dest.is_symlink():
        raise ValueError("symlink in controller store")
    dest.mkdir(parents=True, exist_ok=True)
    payloads = {"manifest.json": canonical(frozen.manifest)}
    payloads.update({"files/" + name: data for name, data in frozen.files.items()})
    for relative, data in payloads.items():
        path = dest / relative
        if path.parent.is_symlink() or path.is_symlink():
            raise ValueError("symlink in controller store")
        path.parent.mkdir(exist_ok=True)
        try:
            with path.open("xb") as handle:
                handle.write(data)
        except FileExistsError:
            if path.read_bytes() != data:
                raise ValueError("stored object was changed")
    return dest


def execute_frozen(candidate: bytes, timeout: float = 5.0) -> list[dict]:
    """Run committed fixtures locally; this function is NOT an OS sandbox.

    A disposable isolated executor is required for arbitrary submissions.
    Timeout/malformed output cannot yield an approval.
    """
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
    """Unchanged checker file, worker-controlled expected.json in the same cwd."""
    with tempfile.TemporaryDirectory(prefix="factory-weak-") as tmp:
        root = Path(tmp)
        (root / SUBJECT).write_bytes(candidate)
        (root / "expected.json").write_bytes(canonical(expected_doc))
        (root / "checker.py").write_text(WEAK_CHECKER)
        checker_before = digest((root / "checker.py").read_bytes())
        proc = subprocess.run(
            [sys.executable, "-I", "-B", str(root / "checker.py")],
            capture_output=True, text=True, timeout=10, cwd=root,
            env={"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"},
        )
        return {
            "exit": proc.returncode,
            "stdout": proc.stdout.strip(),
            "checker_sha256": checker_before,
            "checker_after_sha256": digest((root / "checker.py").read_bytes()),
            "expected_sha256": digest(canonical(expected_doc)),
        }


def judge(outputs: list[dict]) -> dict:
    """Controller-owned comparison. Incomplete evidence yields no approval."""
    if len(outputs) != len(CASES):
        return {"kind": "no_approval", "reason": "incomplete"}
    if any(not isinstance(item, dict) or item.get("status") != "ok"
           or type(item.get("value")) is not int for item in outputs):
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
        self.db_path = store / "publications.sqlite3"
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS publications ("
                         "nonce TEXT PRIMARY KEY, run TEXT NOT NULL, "
                         "artifact TEXT NOT NULL, payload BLOB NOT NULL)")

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
        """Validate without consuming. publish() commits consumption and bytes together."""
        try:
            if not validate_frozen(artifact):
                return False
            value = approval["value"]
            expected_mac = hmac.new(self.key, canonical(value), "sha256").hexdigest()
            expected_fields = {
                "schema_version": SCHEMA, "task_id": TASK, "run_id": self.run,
                "artifact_manifest_digest": artifact.digest,
                "verifier_bundle_digest": verifier_bundle_digest(launch),
                "expected_results_digest": expected_digest(),
                "policy_digest": policy_digest(),
                "acceptance_environment_manifest_digest": digest(canonical(env_manifest)),
                "decision": "accept",
            }
            return (set(value) == set(expected_fields) | {"nonce"}
                    and isinstance(value["nonce"], str) and len(value["nonce"]) == 16
                    and hmac.compare_digest(expected_mac, approval["mac"])
                    and all(value[k] == v for k, v in expected_fields.items()))
        except (TypeError, KeyError, ValueError, AttributeError):
            return False

    def publish(self, approval: dict, artifact: Frozen, launch: dict, env_manifest: dict) -> str:
        if not self.authorize(approval, artifact, launch, env_manifest):
            return "DENIED"
        # Read the controller's copy, rehash those exact bytes, publish those bytes.
        # The controller store and Python process are trusted in this reference model.
        try:
            root = self.store / artifact.digest
            paths = [root, root / "files", root / "manifest.json", root / "files" / SUBJECT]
            if any(path.is_symlink() for path in paths):
                return "DENIED"
            payload = (root / "files" / SUBJECT).read_bytes()
            stored = freeze({SUBJECT: payload})
            if (stored.digest != artifact.digest
                    or (root / "manifest.json").read_bytes() != canonical(stored.manifest)):
                return "DENIED"
            # One transaction binds exact publication bytes to single-use approval.
            # A competing call can only lose the UNIQUE nonce insert.
            with sqlite3.connect(self.db_path, timeout=5) as conn:
                conn.execute("INSERT INTO publications VALUES (?, ?, ?, ?)",
                             (approval["value"]["nonce"], self.run, stored.digest, payload))
        except (OSError, ValueError, sqlite3.Error):
            return "DENIED"
        return "PUBLISHED"

    def replay_or_swap(self, approval: dict, artifact: Frozen, launch: dict, env_manifest: dict) -> str:
        return self.publish(approval, artifact, launch, env_manifest)
