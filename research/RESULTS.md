# Evidence ledger

Run `make record-all` on disposable Linux, then `make evidence`. Each record binds its exact experiment source set. CI fails rather than labeling an unavailable isolation run a success.

| Evidence class | Record | Checks | What the passing record establishes |
|---|---|---:|---|
| Linux lab | `evidence/results.json` | 30 | Actual namespace/mount observations, fixture-token HTTP access, stored loopback uploads, broker denials, positive controls, original parser/gate/history cases, destination-bound approvals |
| Read-only checker experiment | `evidence/isolated-factory.json` | 13 | Direct checker write denied; unchanged checker and candidate; mutable answer key changes FAIL to PASS; independent rejection and positive control; gate-derived reject; fresh substitution, wrong-destination refusal, exact-byte local publication, replay |
| Local factory protocol | `evidence/factory-results.json` | 8 | Local acceptance/rejection, gate-derived decision, fresh substitution, wrong-destination refusal and replay, two deliberately weakened detectors; no OS-isolation claim |
| Regression suite | `tests/test_factory.py`, `tests/test_evidence.py`, `tests/test_redteam.py`; CI test log | 48 | Controller protocol, fail-closed evidence and red-team decision-integrity regressions, including concurrent nonce use |
| Archived gate audit | `evidence/baseline-audit.json` | one reproduction | Internal API can retain stale digest after bytes mutate; requires controller-object access |

These are assertion counts, not vulnerability or attack-success counts. A passing deliberately weakened check means the unwanted acceptance was successfully reproduced.

## Paired checker result

| Candidate bytes | Answer-key owner | Decision |
|---|---|---|
| Always 200 | Honest workspace key | FAIL |
| Same bytes | Worker-edited workspace key | PASS |
| Same bytes | Controller-owned policy | REJECT |
| Corrected handler | Controller-owned policy | ACCEPT |

The checker SHA-256 before and after is recorded, not merely asserted by a constant. The worker's direct write attempt is denied by a read-only mount. The candidate digest is also unchanged. The independent expected values are `[401, 200, 403, 200, 401]`; the bad candidate emits five 200s.

## Publication controls

A fresh unused approval is first offered with bad bytes: denied. The same approval then publishes the correct bytes: accepted and read back from SQLite. Reuse is denied. This ordering distinguishes digest enforcement from a test that passes only because an earlier operation already consumed the nonce.

## Explicit non-results

There is no measured LLM behavior, prompt-injection campaign, model attack-success rate, commercial-product vulnerability, real customer exposure, kernel escape evaluation, or multi-agent benchmark. CLI status values are not packets from a deployed `/admin` server. No production package or GitHub merge is performed by the reference gate. The optional cloud path was not needed for this evidence bundle.
