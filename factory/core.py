"""Controller-owned acceptance protocol for the committed synthetic fixtures.

Three properties this module tries to hold, and one it deliberately does not:

* The gate derives its own decision. No caller can assert acceptance; `issue`
  takes an observer over the frozen bytes and judges the observations against
  the policy object it also binds into the approval.
* The approval names the verifier trusted base (`VERIFIER_TCB`), the policy,
  the acceptance environment description and the publication destination.
* Publication commits the exact evaluated bytes and spends the nonce in one
  transaction, and the audit readback revalidates the whole stored record.

It does NOT make the policy hidden, unpredictable or complete. Five committed
cases are evaluation integrity, not evaluation quality. See research/INVARIANTS.md.

Local subprocess execution is NOT an OS sandbox. Use factory.isolated for the
Linux namespace/mount experiment. SQLite publication is a local release model,
not an integration with a package registry, production deployment or Git merge.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
import platform
import secrets
import sqlite3
import time
from types import MappingProxyType
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = 3
TASK = "lock-admin"
POLICY_ID = "admin-requires-auth-v1"
SUBJECT = "handler.py"
MAX_FILE = 64_000
ALLOWED = frozenset({SUBJECT})

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
# Always 200: violates the admin policy in this CLI fixture.
BAD = """import json, sys
sys.argv[1].split(":", 1)
print(json.dumps(200))
"""
# Immutable. Rebinding this name cannot make evaluation and the approved
# expected-results digest disagree: both read the policy passed to the gate.
CASES = (("admin:none", 401), ("admin:admin", 200), ("admin:user", 403),
         ("public:none", 200), ("admin:expired", 401))
POLICY = MappingProxyType({"id": POLICY_ID, "task": TASK, "cases": CASES})
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

# Every repository file whose bytes can change what the controller observes or
# how it decides. lab/run.py is listed because factory.isolated takes every
# observation through its Runner: changing that file changes the verifier.
# tests/test_factory.py asserts this list still covers the imported modules.
VERIFIER_TCB = ("factory/__init__.py", "factory/boat.py", "factory/core.py",
                "factory/isolated.py", "factory/run.py", "lab/run.py")

# An approval authorizes one operation against one destination. Without this
# binding an approval for a staging store also authorizes a production store.
DESTINATION_KEYS = ("account", "environment", "operation", "subject")


def canonical(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def cases_of(policy) -> tuple:
    return tuple(tuple(case) for case in policy["cases"])


def policy_digest(policy=POLICY) -> str:
    return digest(canonical({"id": policy["id"], "task": policy["task"],
                             "cases": [list(case) for case in cases_of(policy)]}))


def expected_digest(policy=POLICY) -> str:
    return digest(canonical([list(case) for case in cases_of(policy)]))


def verifier_bundle_digest(launch: dict, tcb=VERIFIER_TCB, root=ROOT) -> str:
    """Hash the declared verifier trusted base, not whatever happens to sit in
    one directory. A missing member raises rather than silently shrinking."""
    sources = {name: digest((root / name).read_bytes()) for name in sorted(tcb)}
    return digest(canonical({"tcb": sources, "launch": launch}))


def destination_digest(destination) -> str:
    if type(destination) is not dict or tuple(sorted(destination)) != DESTINATION_KEYS:
        raise ValueError("destination must name account, environment, operation and subject")
    if any(type(destination[key]) is not str or not destination[key] for key in destination):
        raise ValueError("destination fields must be non-empty strings")
    if destination["subject"] != SUBJECT:
        raise ValueError("destination subject is not the released subject")
    return digest(canonical(destination))


def acceptance_environment(role: str, **facts) -> dict:
    """A DESCRIPTION of the acceptance environment, measured where this process
    can measure it. It is not a platform attestation: nothing below is signed by
    hardware or by a runner, and a compromised controller can describe anything.
    It is bound so that a later approval from a different toolchain is refused."""
    described = {
        "role": role,
        "python": platform.python_version(),
        "system": platform.system(),
        "machine": platform.machine(),
        "runner_image": os.environ.get("ImageOS", "unmeasured"),
        "runner_image_version": os.environ.get("ImageVersion", "unmeasured"),
    }
    described.update(facts)
    return described


@dataclass(frozen=True)
class Frozen:
    """Bytes are immutable; the manifest and digest are derived, never caller labels."""
    _entries: tuple[tuple[str, bytes], ...]

    @property
    def files(self):
        return MappingProxyType(dict(self._entries))

    @property
    def manifest(self) -> dict:
        return {"schema": SCHEMA, "files": [
            {"path": name, "type": "file", "mode": "0644", "size": len(data),
             "sha256": digest(data)} for name, data in self._entries
        ]}

    @property
    def digest(self) -> str:
        return digest(canonical(self.manifest))


@dataclass(frozen=True)
class Authorization:
    """What the gate decided, what it saw, and the approval it signed (or None)."""
    approval: dict | None
    verdict: dict
    observations: list


def freeze(files: dict[str, bytes]) -> Frozen:
    """Narrow one-file fixture format. No paths, symlinks or mutable byte arrays."""
    if type(files) is not dict or set(files) != set(ALLOWED):
        raise ValueError("artifact must contain exactly handler.py")
    entries = []
    for name, data in sorted(files.items()):
        if type(data) is not bytes or not data or len(data) > MAX_FILE:
            raise ValueError(f"invalid file bytes: {name}")
        entries.append((name, data))
    return Frozen(tuple(entries))


def persist(frozen: Frozen, store: Path) -> Path:
    """Diagnostic CAS copy. The gate publishes its validated in-memory byte copy."""
    checked = freeze(dict(frozen.files))
    if checked.digest != frozen.digest:
        raise ValueError("inconsistent frozen object")
    dest = store / checked.digest
    dest.mkdir(parents=True, exist_ok=True)
    files = dest / "files"
    files.mkdir(exist_ok=True)
    contents = {dest / "manifest.json": canonical(checked.manifest)}
    contents.update({files / name: data for name, data in checked.files.items()})
    for path, data in contents.items():
        if path.is_symlink():
            raise ValueError("symlink in controller store")
        if path.exists():
            if path.read_bytes() != data:
                raise ValueError("controller store content mismatch")
        else:
            with path.open("xb") as handle:
                handle.write(data)
    return dest


def execute_frozen(candidate: bytes, policy=POLICY, timeout: float = 5.0) -> list[dict]:
    """Execute committed fixtures locally. This function provides NO OS isolation."""
    outputs = []
    with tempfile.TemporaryDirectory(prefix="factory-accept-") as tmp:
        path = Path(tmp) / SUBJECT
        path.write_bytes(candidate)
        env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"}
        for value, _expected in cases_of(policy):
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
    """Unchanged checker, workspace-owned expectations. Local logic reproduction."""
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
            "checker_sha256": digest((root / "checker.py").read_bytes()),
            "expected_sha256": digest(canonical(expected_doc)),
        }


def judge(outputs: list[dict], policy=POLICY) -> dict:
    """Only a complete, typed observation can become a policy verdict."""
    cases = cases_of(policy)
    if type(outputs) is not list or len(outputs) != len(cases):
        return {"kind": "no_approval", "reason": "incomplete"}
    if any(type(item) is not dict or set(item) != {"status", "value"}
           or item.get("status") != "ok" or type(item.get("value")) is not int
           for item in outputs):
        return {"kind": "no_approval", "reason": "timeout_or_malformed"}
    matches = [item["value"] == expected for item, (_, expected) in zip(outputs, cases)]
    return {"kind": "verdict", "accepted": all(matches), "matches": matches}


COLUMNS = ("nonce", "artifact", "run", "manifest", "candidate", "approval", "destination")
FIELDS = ("schema_version", "task_id", "run_id", "artifact_manifest_digest",
          "verifier_bundle_digest", "expected_results_digest", "policy_digest",
          "acceptance_environment_manifest_digest", "destination_digest",
          "decision", "nonce", "expires_at")


class Gate:
    """Ephemeral controller identity; atomic local byte publication and nonce use.

    The database, the signing key and the policy object are controller-owned
    trust assumptions. An agent with controller filesystem/process access defeats
    this model. A new Gate gets a new key and run ID and rejects approvals from
    the old controller session.

    There is no parameter through which a caller states a decision. `issue` runs
    a controller-owned observer over the frozen bytes it is about to name and
    judges the result against `self.policy`, the same object whose digests go
    into the approval.
    """
    def __init__(self, store: Path, *, clock=time.time, policy=POLICY,
                 tcb=VERIFIER_TCB, root=ROOT):
        self.key = secrets.token_bytes(32)
        self.run = secrets.token_hex(16)
        self.clock = clock
        self.policy = policy
        self.tcb = tuple(tcb)
        self.root = root
        self.store = store
        store.mkdir(parents=True, exist_ok=True)
        self.db_path = store / "publication.sqlite3"
        with sqlite3.connect(self.db_path, timeout=10) as db:
            db.execute("CREATE TABLE IF NOT EXISTS publications ("
                       "nonce TEXT PRIMARY KEY, artifact TEXT NOT NULL, "
                       "run TEXT NOT NULL, manifest TEXT NOT NULL, "
                       "candidate BLOB NOT NULL, approval TEXT NOT NULL, "
                       "destination TEXT NOT NULL)")
            columns = tuple(row[1] for row in db.execute("PRAGMA table_info(publications)"))
        if columns != COLUMNS:
            raise ValueError("publication store schema does not match this controller")

    def _bindings(self, checked: Frozen, launch, env_manifest, destination) -> dict:
        return {
            "schema_version": SCHEMA, "task_id": TASK, "run_id": self.run,
            "artifact_manifest_digest": checked.digest,
            "verifier_bundle_digest": verifier_bundle_digest(launch, self.tcb, self.root),
            "expected_results_digest": expected_digest(self.policy),
            "policy_digest": policy_digest(self.policy),
            "acceptance_environment_manifest_digest": digest(canonical(env_manifest)),
            "destination_digest": destination_digest(destination),
        }

    def issue(self, *, artifact: Frozen, observe=None, launch: dict,
              env_manifest: dict, destination: dict, ttl: int = 300) -> Authorization:
        """Observe the frozen bytes, judge them, then sign what was decided.

        `observe` is a controller-owned callable from candidate bytes to raw
        observations; it defaults to this module's local executor. It never sees
        a decision to return, and the bytes it receives are the bytes the
        approval names."""
        if type(ttl) is not int or not 0 < ttl <= 300:
            raise ValueError("invalid approval lifetime")
        checked = freeze(dict(artifact.files))
        observer = observe if observe is not None else (
            lambda data: execute_frozen(data, self.policy))
        observations = observer(checked.files[SUBJECT])
        verdict = judge(observations, self.policy)
        if verdict["kind"] != "verdict":
            return Authorization(None, verdict, observations)
        value = self._bindings(checked, launch, env_manifest, destination)
        value.update({
            "decision": "accept" if verdict["accepted"] else "reject",
            "nonce": secrets.token_hex(16),
            "expires_at": int(self.clock()) + ttl,
        })
        approval = {"value": value,
                    "mac": hmac.new(self.key, canonical(value), "sha256").hexdigest()}
        return Authorization(approval, verdict, observations)

    def _valid(self, approval, artifact, launch, env_manifest, destination) -> bool:
        try:
            if type(approval) is not dict or set(approval) != {"value", "mac"}:
                return False
            value, mac = approval["value"], approval["mac"]
            if type(value) is not dict or set(value) != set(FIELDS) or type(mac) is not str:
                return False
            if any(type(value[k]) is not str for k in set(FIELDS) - {"schema_version", "expires_at"}):
                return False
            if type(value["schema_version"]) is not int or type(value["expires_at"]) is not int:
                return False
            expected_mac = hmac.new(self.key, canonical(value), "sha256").hexdigest()
            checked = freeze(dict(artifact.files))
            bindings = self._bindings(checked, launch, env_manifest, destination)
            return (
                hmac.compare_digest(expected_mac, mac)
                and value["schema_version"] == SCHEMA
                and value["task_id"] == TASK
                and all(value[key] == bindings[key] for key in bindings)
                and checked.digest == artifact.digest
                and value["decision"] == "accept"
                and len(value["nonce"]) == 32
                and self.clock() < value["expires_at"]
            )
        except (KeyError, TypeError, ValueError, AttributeError, OSError):
            return False

    def authorize(self, approval, artifact: Frozen, launch: dict,
                  env_manifest: dict, destination: dict) -> bool:
        """Advisory check only. Publication rechecks and consumes atomically."""
        if not self._valid(approval, artifact, launch, env_manifest, destination):
            return False
        with sqlite3.connect(self.db_path, timeout=10) as db:
            return db.execute("SELECT 1 FROM publications WHERE nonce = ?",
                              (approval["value"]["nonce"],)).fetchone() is None

    def publish(self, approval, artifact: Frozen, launch: dict,
                env_manifest: dict, destination: dict) -> str:
        if not self._valid(approval, artifact, launch, env_manifest, destination):
            return "DENIED"
        checked = freeze(dict(artifact.files))
        with sqlite3.connect(self.db_path, timeout=10) as db:
            db.execute("BEGIN IMMEDIATE")
            if not self._valid(approval, checked, launch, env_manifest, destination):
                return "DENIED"
            try:
                db.execute("INSERT INTO publications VALUES (?, ?, ?, ?, ?, ?, ?)", (
                    approval["value"]["nonce"], checked.digest, self.run,
                    canonical(checked.manifest).decode(), checked.files[SUBJECT],
                    canonical(approval).decode(), canonical(destination).decode(),
                ))
            except sqlite3.IntegrityError:
                return "DENIED"
        return "PUBLISHED"

    def published_bytes(self, nonce: str) -> bytes | None:
        """Revalidate the whole stored authorization record, not just the bytes.

        The stored approval is re-authenticated under this controller's key, so
        any edit to the recorded decision, artifact, run, policy, verifier,
        environment, destination or nonce is a readback failure."""
        with sqlite3.connect(self.db_path, timeout=10) as db:
            row = db.execute("SELECT candidate, artifact, run, manifest, approval, destination "
                             "FROM publications WHERE nonce = ?", (nonce,)).fetchone()
        if row is None:
            return None
        candidate, artifact, run, manifest, stored_approval, stored_destination = row
        try:
            frozen = freeze({SUBJECT: candidate})
            approval = json.loads(stored_approval)
            destination = json.loads(stored_destination)
            value = approval["value"]
            mac = hmac.new(self.key, canonical(value), "sha256").hexdigest()
            consistent = (
                type(approval) is dict and set(approval) == {"value", "mac"}
                and type(value) is dict and set(value) == set(FIELDS)
                and hmac.compare_digest(mac, approval["mac"])
                and run == self.run == value["run_id"]
                and frozen.digest == artifact == value["artifact_manifest_digest"]
                and canonical(frozen.manifest).decode() == manifest
                and canonical(approval).decode() == stored_approval
                and canonical(destination).decode() == stored_destination
                and value["destination_digest"] == destination_digest(destination)
                and value["policy_digest"] == policy_digest(self.policy)
                and value["expected_results_digest"] == expected_digest(self.policy)
                and value["decision"] == "accept"
                and value["nonce"] == nonce
                and value["schema_version"] == SCHEMA
                and value["task_id"] == TASK
            )
        except (KeyError, TypeError, ValueError, AttributeError, json.JSONDecodeError):
            raise ValueError("publication integrity failure")
        if not consistent:
            raise ValueError("publication integrity failure")
        return candidate

    def replay_or_swap(self, approval, artifact: Frozen, launch: dict,
                       env_manifest: dict, destination: dict) -> str:
        return self.publish(approval, artifact, launch, env_manifest, destination)
