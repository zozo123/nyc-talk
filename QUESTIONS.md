# Hard questions and precise answers

## Is this a new vulnerability or just least privilege?

These are controlled reproductions of known mechanisms. The useful result is a paired experiment: the candidate and checker stay fixed while ownership of the answer key changes the decision. We also publish a counterexample in our own original controller API. We do not claim a vendor zero-day or novelty for least privilege.

## Where is the LLM?

It is deliberately absent. Deterministic worker actions isolate the capability boundary. This measures whether the interface permits the action, not whether a particular model discovers or attempts it. There is no model attack-success rate.

## Did you really lock the checker?

In `factory/isolated.py`, the checker is bind-mounted read-only. A direct worker write is attempted and denied. Its actual file hash and the candidate hash are compared before and after. The answer key remains worker-writable in the intentionally weak configuration.

## Is `/admin` a real service?

The factory example is a five-input CLI status-code model. It emits integers. It is not a running authentication service. The credential and allowed-service examples in `lab/run.py` do use real loopback HTTP requests and receiver-side stored payloads.

## Could the candidate just print the expected answers?

Yes. The finite policy only establishes those five observations. It is not comprehensive application verification. Real acceptance needs appropriately owned, representative tests and observations, and defenses against test detection or overfitting. A truthful record of a narrow test remains narrow.

## Why is another VM insufficient?

A second machine can still consume the worker's expected-results file. The relevant independence is the ownership of authoritative inputs, comparison, credentials and publication capability. Our multi-agent slide is an architectural inference, not an empirical benchmark.

## Do snapshots make it safe?

Snapshots preserve bytes. They do not establish whether a copied test file should be authoritative or whether a token should be available in the next task. Reproducibility and authorization are different properties.

## Does the broker stop every leak?

No. This broker accepts one fixed operation with no arbitrary destination or payload fields, and the worker loses its direct network route. Allowing arbitrary report text, additional tools, uncontrolled metadata or other channels changes the threat model. We demonstrate this one operation, not universal data-loss prevention.

## Does short token lifetime fix excessive permissions?

No. The service must enforce task scope and audience. Expiration limits the exposure window; it does not narrow what an otherwise broad token can access while valid.

## Is a hash chain proof the work is correct?

No. The history check detects a rewrite relative to a separately retained controller anchor. Rewriting both history and an unprotected head would defeat that comparison. Correctness comes from an independently owned policy and its evidence, not from an internally consistent log.

## What did you find in your own gate?

The archived controller object allowed candidate bytes to change while its stored digest stayed unchanged. The old gate then emitted a publication marker. The reproduction requires controller-object access. We have not shown an untrusted worker can reach that object. The corrected protocol derives its digest from immutable entries and stores actual authorized bytes.

## Could your substitution test have passed for the wrong reason?

That was an important audit question. The corrected test presents different bytes with an unused approval first, then publishes the intended bytes with that same approval, then attempts replay. A consumed nonce cannot mask a missing artifact check in the first step.

## What about concurrency and restarts?

A SQLite transaction combines byte publication and nonce consumption; a 16-way concurrent regression allows one publication. A new Gate has a new key and run identifier and rejects old approvals. This is not a tested distributed commit protocol or a persistent production signing service.

## Is local `python -I` the sandbox?

No. The local executor is a protocol fixture runner. Actual namespace/mount checks use bubblewrap on Linux, with only committed deterministic fixtures. Neither path certifies resistance to kernel vulnerabilities or arbitrary resource exhaustion.

## Does this merge a real pull request or deploy a package?

No. The reference gate stores candidate bytes in a controller-owned SQLite database. A production publication destination requires its own authorization and atomicity analysis. A local marker is not mislabeled as a production release.

## What should we do tomorrow?

Attempt the unauthorized credential read, cross-task write, wrong-recipient upload and answer-key/approved-byte substitution. For each denial, demonstrate a legitimate task that still completes. Then inspect who owns every authoritative input to the release decision.
