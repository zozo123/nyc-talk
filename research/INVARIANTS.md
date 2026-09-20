# Acceptance invariants and trusted roots

1. **Exact bytes.** The one supported candidate is a bounded `handler.py` payload. Frozen identity is derived from those immutable bytes. Publication stores the bytes it checked, not a mutable workspace reference or a caller-supplied digest alone.
2. **Independent criteria.** The trusted controller owns the task, policy and expected values. A worker-supplied PASS is never release authority. Protect the checker's transitive inputs, not only its source file.
3. **Context-bound approval.** Authenticate schema, task, run, artifact manifest, verifier/source bundle, expected results, policy, acceptance-environment manifest, decision, nonce and expiry. A rejected, stale, malformed, forged or context-mismatched receipt cannot authorize publication.
4. **Atomic one-use publication.** Store payload plus manifest and consume `(run, nonce)` together. The SQLite primary key prevents two concurrent successful publications for the same receipt. Expiry is rechecked after acquiring the transaction lock.
5. **Incomplete is not approved.** Missing, malformed, non-integer or timed-out status evidence does not produce an acceptance decision. This is a fail-closed logic property, not evidence that a workload was contained.
6. **Every denial has a counterfactual control.** Test an unwanted action and the allowed work that should survive. In particular, test substitution with an unconsumed approval, then use the same approval for its original bytes.
7. **Evidence has an explicit boundary.** All expected source files must match the recorded hashes. All expected check names must appear exactly once and pass. Stage evidence must come from isolated mode. These checks do not authenticate a malicious maintainer or prove exhaustive coverage.

Trusted: controller process and code, expected values, signing key, environment description, store directory, SQLite implementation and host kernel. `Gate.issue()` is a trusted internal API, never a worker endpoint. An environment-manifest hash binds a declared configuration; it is not hardware-backed remote attestation.

Only committed fixtures may run locally. Bubblewrap isolation is configuration-dependent. Arbitrary hostile-output DoS, kernel escape resistance, global information-flow security, production IAM integration and durable distributed release transactions are outside this implementation's demonstrated scope.
