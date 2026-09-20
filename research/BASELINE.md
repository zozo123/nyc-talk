# Baseline and change boundary

The audited original talk/factory source is commit `4b06c519cff2ffcc69a8471f4f861a03f08f93a0` in `zozo123/nyc-talk` (September 20, 2026). The acquisition snapshot was commit `418805e2a65cdcb4e9ed9991a18a9278b6c3cbe8`, which changed the evidence-upload workflow but retained that factory implementation.

Original `factory/core.py` Git blob: `a1405216ae5329f1ea0140cc9d16884dbfd00da3`.

A direct local in-process harness reproduced an old API defect: mutate the exported `Frozen.files` mapping after issuance, preserve its stored digest, and call `publish`. The old gate returned `PUBLISHED`. The old publication operation recorded identity metadata; it did not copy bytes into a release sink. No worker-to-controller-memory path was established.

The revised factory uses immutable payload bytes, a derived manifest/digest, strict authenticated context, expiry, and an atomic SQLite payload/nonce transaction. Its regression test attempts substitution before consuming the approval, then exercises the legitimate publication with the same receipt. A file-view mutation can no longer change the frozen payload.

The original `lab/run.py` is retained as the isolated four-boundary teaching harness. It includes a parser example; the final factory's acceptance demonstration uses the admin status-code model. Do not confuse these subjects or their check counts.

Prior cloud-adapter experiments belong to the earlier implementation and are not evidence for the revised factory. The final suite uses bubblewrap on Linux and does not require or record any API key. `factory/boat.py` is retained as historical optional adapter source only.

The release source hashes, runtime mode and observed outputs are in `evidence/*.json`. CI artifacts additionally contain a source archive and commit identifier. Evidence hashes prevent accidental code/result mismatch; they are not independent provenance from an untrusted maintainer.
