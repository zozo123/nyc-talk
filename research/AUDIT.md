# Audit of our own reference gate

## Finding

The archived `Frozen` object stored three independent mutable representations: files, manifest, and digest. `Gate.authorize` compared approval metadata with the stored digest field. It did not derive that field from the candidate bytes at the point of publication.

At baseline `4b06c519cff2ffcc69a8471f4f861a03f08f93a0`, a controller-side caller can create an approval for the good candidate, replace `frozen.files['handler.py']` with bad bytes, leave `frozen.digest` unchanged, and obtain `PUBLISHED`. The recorded manifest no longer matches the candidate. The old publication function writes a marker, not deployed application bytes.

```sh
python3 tools/audit_baseline.py
```

The script imports only the checked-in archival module and uses a temporary store. Raw output and the archived source hash live in `evidence/baseline-audit.json`.

## Reachability and classification

This is an **internal API integrity flaw in our reference implementation**. The reproduction manipulates the controller's Python object directly. We have not shown an untrusted worker can obtain that object or mutate the controller filesystem. It is not a demonstrated sandbox escape, remote exploit, vendor zero-day, or evidence that a real release was compromised.

## Corrections

The current object contains immutable byte entries. Its manifest and digest are derived properties. The gate normalizes the accepted artifact again, validates a strict approval envelope and all decision-context digests, and records the actual byte copy with nonce consumption in one SQLite transaction. Readback verifies the stored bytes and manifest. The regression suite includes stale context, modified MAC, incorrect digest, timeout/malformed observations, expired approval, restart, byte substitution and concurrent replay.

Two audit improvements matter independently of the code fix. First, substitution is tested with an **unused approval**, then the legitimate candidate must still publish. Testing substitution after consuming an approval cannot isolate which condition blocked it. Second, publication now stores and rereads actual fixture bytes rather than equating a log marker with delivery.

## Remaining limits

Python immutability is not a security boundary against a hostile controller; code with controller-process access can replace functions or keys. SQLite ownership and the host remain trusted. The demonstration does not implement a distributed registry transaction, a hardware-backed signing system, multi-process crash recovery tests, attested execution, adversarial resource bounds, or comprehensive verification of arbitrary programs. Those properties must not be inferred from these tests.
