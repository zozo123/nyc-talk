# Acceptance and release invariants

**Acceptance integrity.** For these five committed cases, the worker cannot redefine the expected values used by the independent controller. An unchanged verifier file is insufficient if its authoritative inputs remain worker-writable.

**Decision integrity.** The gate derives its own decision. No caller parameter states acceptance: `issue` runs a controller-owned observer over the frozen bytes it names and judges the raw observations against the policy object bound into the approval. A verdict-shaped observation is malformed and produces no approval. The declared verifier trusted base includes every file whose bytes shape what the controller observes, including the isolation runner.

**Release integrity.** Publication records exactly the candidate bytes authorized for this task, run, verifier source bundle, expected results, policy, environment manifest, destination and unexpired nonce. An approval names one destination (account, environment, operation, subject) and does not authorize a different store. Substitution and the wrong destination are challenged before the nonce is consumed; the legitimate publication must still succeed afterward.

**Single use.** Checking and consuming a nonce and recording candidate bytes occur in one SQLite transaction. Parallel use of the same approval produces one publication. A fresh controller has a new key and run ID and rejects previous-session approvals.

**Evidence integrity.** All required sources and all named checks must be present. Missing, skipped, stale, malformed, duplicate or failed evidence blocks the deck build. Missing or malformed candidate observations produce no approval, not a claimed successful defense.

**Trust assumptions.** The controller, its key, policy, interpreter, SQLite store, and host remain trusted. The worker receives neither those writable paths nor those capabilities in the isolated experiment. Local `python -I` is not process isolation. The diagnostic content-addressed store is not a hostile multi-tenant filesystem.

**Finite scope.** A correct answer to five inputs is not proof of application security. The status-code fixture is a CLI model. Production readiness, network-server correctness, resource-exhaustion resistance, cryptographic key management, disaster recovery, package deployment and GitHub merge integration are not established here.
