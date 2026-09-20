# Finalization audit

Base: `4b06c519cff2ffcc69a8471f4f861a03f08f93a0`. Scope: our reference harness and claims, not a vendor system.

## 1. Swap/replay confound

The baseline `intended()` published the good candidate before attempting a swapped artifact. The nonce was already consumed. A denial therefore did not isolate digest enforcement from replay enforcement.

The corrected sequence is: issue fresh approval; attempt different artifact (DENIED); publish the original artifact (PUBLISHED); replay (DENIED). A dedicated regression verifies all three observations.

## 2. Cached artifact identity

The baseline `Frozen` dataclass exposed a writable `files` dictionary. The gate compared the cached digest label but did not recompute it from those bytes. In a local trusted-caller probe, replacing the good object's payload with BAD caused baseline `Gate.publish()` to return `PUBLISHED`, while independent evaluation of the mutated bytes rejected them.

**Reachability limit:** this probe modifies controller memory. The stated worker threat model does not grant that capability. It is a reference-API robustness defect, not evidence of a sandboxed-worker exploit. The baseline publication function only appended metadata, so the probe also does not establish that bad bytes were deployed anywhere.

The corrected object exposes an immutable payload mapping. The gate also validates reconstructed objects, recomputes manifest identity, reads and checks stored bytes, and records the actual payload in the publication transaction. Tests cover object-label substitution, manifest changes, stored-payload changes, missing files and symlinks.

## 3. Non-atomic replay/publication state

The baseline consumed a nonce in one file and appended a publication record separately. The corrected reference gate uses a SQLite transaction with a unique nonce and the actual payload in the same row. Eight concurrent attempts produce one successful publication in the regression test. This is bounded reference-gate evidence, not a distributed publisher durability proof.

## 4. Claims beyond the implementation

The baseline language called the local checker read-only, but the factory did not enforce a distinct filesystem protection domain. The revised claim is measured byte identity: hash before equals hash after. The slide labels the admin example as a command-line policy model instead of implying actual HTTP deployment. The lab's isolated HTTP/mount experiments remain separately identified.

The checker-result record now includes measured before/after hashes. The deck validator rejects missing source inventories, missing/duplicate checks, skipped isolation evidence, stale sources and a reveal unsupported by the factory record.

## Classification

The primary verifier-dependency case is a **deliberately weakened known-mechanism reproduction**. The corrections above are implementation and evidence-quality improvements to our own reference harness. No vendor disclosure, CVE, model attack-success rate or cross-product transfer claim follows from these observations.
