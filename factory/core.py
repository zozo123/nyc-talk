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
from types import MappingProxyType
from typing import Mapping

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
    sources = {p.name: digest(p.read_bytes())
               for p in sorted(Path(__file__).parent.glob("*.py"))}
    return digest(canonical({"sources": sources, "launch": launch}))


@dataclass(frozen=True)
class Frozen:
    digest: str
    manifest: dict
    files: Mapping[str, bytes]


def freeze(files: dict[str, bytes]) -> Frozen:
    """Collect, bound, store as an immutable object, then hash the manifest."""
    if set(files) != ALLOWED:
        raise ValueError("artifact must contain exactly handler.py")
    entries = []
    stored = {}
    for name in sorted(files):
        if name not in ALLOWED:
            raise ValueError(f"path not permitted: {name}")
        if "/" in name or name.startswith(".") or ".." in name:
            raise ValueError(f"illegal path: {name}")
        data = files[name]
        if not isinstance(data, bytes):
            raise ValueError("artifact content must be immutable bytes")
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


def validate_frozen(frozen: Frozen) -> bool:
    """A digest label is not evidence about the bytes currently attached to it."""
    try:
        rebuilt = freeze(dict(frozen.files))
        return (rebuilt.digest == frozen.digest
                and canonical(rebuilt.manifest) == canonical(frozen.manifest))
    except (AttributeError, KeyError, TypeError, ValueError):
        return False


def load_frozen(store: Path, artifact_digest: str) -> Frozen:
    """Read and rehash the controller-owned object; reject corruption or symlinks."""
    if (len(artifact_digest) != 64
            or any(c not in "0123456789abcdef" for c in artifact_digest)):
        raise ValueError("invalid object digest")
    root = store / artifact_digest
    paths = [root, root / "manifest.json", root / "files", root / "files" / SUBJECT]
    if any(path.is_symlink() for path in paths):
        raise ValueError("object contains a symlink")
    if set(p.name for p in (root / "files").iterdir()) != ALLOWED:
        raise ValueError("object file set changed")
    source = root / "files" / SUBJECT
    if source.stat().st_size > MAX_FILE:
        raise ValueError("stored object is too large")
    frozen = freeze({SUBJECT: source.read_bytes()})
    if (frozen.digest != artifact_digest
            or canonical(frozen.manifest) != (root / "manifest.json").read_bytes()):
        raise ValueError("stored object digest mismatch")
    return frozen


def persist(frozen: Frozen, store: Path) -> Path:
    """The store belongs to the controller, never a producer-writable mount."""
    if not validate_frozen(frozen):
        raise ValueError("invalid frozen object")
    store.mkdir(parents=True, exist_ok=True)
    dest = store / frozen.digest
    if dest.exists() or dest.is_symlink():
        load_frozen(store, frozen.digest)
        return dest
    # A single controller owns this reference store. There is no claim of a
    # concurrent, crash-consistent production publication protocol here.
    dest.mkdir(mode=0o700)
    (dest / "manifest.json").write_bytes(canonical(frozen.manifest))
    files = dest / "files"
    files.mkdir(mode=0o700)
    for name, data in frozen.files.items():
        (files / name).write_bytes(data)
    load_frozen(store, frozen.digest)
    return dest


def execute_frozen(candidate: bytes, timeout: float = 5.0) -> list[dict]:
    """Execute committed fixtures locally. Python -I is NOT an OS sandbox.

    Do not pass arbitrary hostile code here. The isolated Linux lab supplies
    kernel boundaries separately. Timeout/malformed output yields no approval.
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
    """Measure the checker bytes before and after using worker-owned criteria."""
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
            "checker_sha256_before": checker_before,
            "checker_sha256": digest((root / "checker.py").read_bytes()),
            "expected_sha256": digest(canonical(expected_doc)),
        }


def judge(outputs: list[dict]) -> dict:
    """Controller-owned comparison. Incomplete evidence yields no approval."""
    if len(outputs) != len(CASES):
        return {"kind": "no_approval", "reason": "incomplete"}
    if any(not isinstance(item, dict) or item.get("status") != "ok" for item in outputs):
        return {"kind": "no_approval", "reason": "timeout_or_malformed"}
    if any(set(item) != {"status", "value"} or type(item["value"]) is not int
           for item in outputs):
        return {"kind": "no_approval", "reason": "malformed_value"}
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
        if not validate_frozen(artifact) or type(accepted) is not bool:
            raise ValueError("invalid controller decision or artifact")
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
        """Validate an unconsumed approval. Only publish consumes the nonce."""
        if not validate_frozen(artifact):
            return False
        try:
            value = approval["value"]
            expected_mac = hmac.new(self.key, canonical(value), "sha256").hexdigest()
            return bool(
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
        except (KeyError, TypeError, ValueError):
            return False

    def publish(self, approval: dict, artifact: Frozen, launch: dict, env_manifest: dict) -> str:
        """Release rehashed stored bytes, not a caller's label or live workspace.

        Single-controller educational protocol. Keys are ephemeral; restarting
        fails closed. A production service also needs atomic consumption,
        crash recovery, access control and a strongly isolated executor.
        """
        if not self.authorize(approval, artifact, launch, env_manifest):
            return "DENIED"
        try:
            stored = load_frozen(self.store, artifact.digest)
        except (OSError, ValueError):
            return "DENIED"
        nonce = approval["value"]["nonce"]
        release = self.store / "releases" / (self.run + "-" + nonce)
        release.mkdir(parents=True, exist_ok=False)
        (release / SUBJECT).write_bytes(stored.files[SUBJECT])
        # The actual released file, not merely an entry in a publication log.
        released = freeze({SUBJECT: (release / SUBJECT).read_bytes()})
        if released.digest != artifact.digest:
            return "DENIED"
        self._remember(nonce)
        record = {
            "artifact": released.digest,
            "run": self.run,
            "nonce": nonce,
            "released_file": str(release / SUBJECT),
        }
        with self.pub_path.open("a") as handle:
            handle.write(json.dumps(record) + "\n")
        return "PUBLISHED"

    def replay_or_swap(self, approval: dict, artifact: Frozen, launch: dict, env_manifest: dict) -> str:
        return self.publish(approval, artifact, launch, env_manifest)
