# Invariants and trusted boundary

**Acceptance integrity:** for the five fixed task cases, worker-authored expectations and reports cannot cause the intended controller to accept a candidate that fails the controller-owned reference criteria.

**Release identity:** a publication contains the exact payload whose manifest digest was authorized for the same task, run, verifier source, expected results, policy and declared acceptance environment.

**Single use:** the publication bytes and approval nonce commit in one transaction. Concurrent attempts using the same approval produce at most one publication.

**Positive controls:** the correct candidate must publish. A rejected fresh swap must not consume the original valid approval. Replay is tested only after a successful original publication.

**Uncertainty:** missing, malformed or incomplete results produce no approval. An infrastructure failure is inconclusive, not a successful security defense.

The controller process, keys, policy, reference cases, filesystem and database are trusted. Worker code is untrusted. The local executor runs committed deterministic fixtures and provides no OS containment for arbitrary programs. The separate Linux lab exercises actual namespaces and bind mounts. For hostile submissions, place the candidate behind a separately enforced execution boundary and transport only bounded results to the controller.

A second machine is independent only with respect to the state and capabilities actually separated. Shared worker-writable criteria remain a decision dependency. A declared environment digest is not hardware attestation or a complete dependency pin. Finite passing cases do not prove universal application correctness.
