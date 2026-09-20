# Invariants and assumptions

**Acceptance integrity:** within the reference's fixed five-case policy, a worker report or proposed expected-results file cannot cause the controller to approve a failing candidate.

**Release integrity:** the artifact manifest of the actual released file must match the manifest bound into an authenticated unused approval for the same task, run, verifier bundle, expected results, policy and execution-environment manifest.

**Useful work:** every restriction has a positive control. The correct candidate must still be released and behave correctly under the stated cases.

**Evidence completeness:** malformed, timed-out, missing, skipped or source-mismatched evidence does not authorize release. Testing this fail-closed behavior is distinct from claiming an attack was successfully defended.

The reference assumes one trusted controller, a protected store, and committed deterministic fixture programs. Local Python isolated mode is not an operating-system sandbox. A production implementation needs strong executor/controller isolation, protected keys and storage, transactional nonce consumption, crash recovery and more comprehensive policy coverage.

A second VM alone does not establish independent criteria. A digest label alone does not establish byte identity. Hash-chain detection requires a trusted anchor outside worker control. Five cases establish those five observations, not complete security.
