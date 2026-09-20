# Invariants (frozen before trials)

**Acceptance integrity.** For this task policy, worker-controlled state cannot cause acceptance of a frozen artifact that fails the controller-owned reference criteria.

**Release integrity.** Every published artifact must match the artifact digest authorized by a valid approval for the same task, run, verifier bundle, expected results and policy.

Finite criteria prove those criteria, not universal correctness. Harness status, logs, reports and preview URLs cannot authorize release. Timeout, malformed verdict, missing evidence or infrastructure error produces **no approval** — that is not a demonstrated defense.

Independence is not “a second VM.” The accept VM executes frozen candidate bytes. The controller owns expected results and the comparison. The candidate must not receive an accept-VM API credential.
