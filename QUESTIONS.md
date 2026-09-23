# Hard questions and precise answers

## Is this a flaw in an Incredibuild product?

No. Everything shown is a synthetic research fixture written for this talk, and the repository contains its full source. It is not a finding in any Incredibuild product and it is not a customer report. Product-specific questions are welcome afterward rather than on stage. Give this answer the same way every time it is asked, including in the hallway.

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

## Our agents write tests. Are you saying they can't?

No. The worker may propose criteria; it must not be what applies them. A proposed test travels with the candidate and is reviewed and approved the way code is. The approval in `factory/core.py` binds `expected_results_digest` alongside the artifact, so the criteria used for a decision are named in the record and a change to them is visible rather than silent. What we recorded is the narrow version: the expected values are controller-owned constants and the comparison runs outside the workspace. A review workflow that promotes a proposed test into controller-owned criteria is the natural extension and is not something this package measures. Slide 4 is not a story about an agent editing a file. It is a story about the agent being the last writer of the thing that judged it.

## Why is another VM insufficient?

A second machine can still consume the worker's expected-results file. The relevant independence is the ownership of authoritative inputs, comparison, credentials and publication capability. Our multi-agent slide is an architectural inference, not an empirical benchmark.

## What stops the worker editing the controller's criteria?

In the repaired path there is no controller copy inside the worker's world to edit. The expected values and the comparison are `CASES` and `POLICY` in `factory/core.py`, evaluated in the controller process. The sandboxed invocation receives a read-only `/candidate` mount and no network; no controller path is mounted at all, and `expected.json` is never consulted. That is a configuration fact of this experiment, not a demonstrated denial. None of the thirteen isolated checks tests controller unreachability. An agent with controller filesystem or process access defeats this model, and we record that as a trust assumption in `research/INVARIANTS.md`, not as a boundary we defended.

## Do snapshots make it safe?

Snapshots preserve bytes. They do not establish whether a copied test file should be authoritative or whether a token should be available in the next task. Reproducibility and authorization are different properties.

## Does the broker stop every leak?

No. This broker accepts one fixed operation with no arbitrary destination or payload fields, and the worker loses its direct network route. Allowing arbitrary report text, additional tools, uncontrolled metadata or other channels changes the threat model. We demonstrate this one operation, not universal data-loss prevention.

## Does short token lifetime fix excessive permissions?

No. The service must enforce task scope and audience. Expiration limits the exposure window; it does not narrow what an otherwise broad token can access while valid.

## Is a hash chain proof the work is correct?

No. The history check detects a rewrite relative to a separately retained controller anchor. Rewriting both history and an unprotected head would defeat that comparison. Correctness comes from an independently owned policy and its evidence, not from an internally consistent log.

## How would we see this in our own pipeline?

Two signals, neither of which needs model telemetry. The static one is an inventory question: take the set of paths your acceptance decision reads, intersect it with the set of paths the worker can write, and treat a non-empty intersection as the finding. The in-run one is a criteria file whose bytes change between task start and verdict inside the same run; on this recording that is the answer key moving from `0494f1a01dee` to `390e5e764916` while the program and checker hashes hold. Both are computable from a file inventory and two digests. Neither tells you the change was malicious, only that the thing which defined success was written by the thing being judged.

## Does this apply to MCP and tool calls?

The same two questions transfer: which inputs does the decision read, and who can write them. A tool description, an argument schema and a server response are all inputs a decision can read. If the worker can write the server config, the tool manifest, or a file a tool reads, it moves the decision without escaping anything — the shape is identical to `expected.json`. No MCP server was tested here, so the boundary question transfers and the measurement does not.

## Where does prompt injection fit?

Mostly beside this result rather than inside it. Injection is about getting the worker to do something it was not asked to do; here the worker did not need to be subverted, because the permission was already there. The two meet in one place worth naming: if the controller asks a model to decide whether the work is done, the candidate's own text becomes an input to that decision, and the worker writes that text. This gate's judge is deliberately the opposite — deterministic and typed, and a verdict-shaped observation produces no approval at all rather than an accepting one (`factory/core.py`, `judge`; `tests/test_redteam.py`). We did not test an LLM judge, so that contrast is a design argument, not a measured result.

## Doesn't SLSA already solve this?

SLSA v1.2 names the right requirement, and this run is what skipping it looks like. Provenance binds a producer to bytes; whether those bytes are good is decided by expectations the verifier supplies, not by the attestation. On slide 4 a fully valid attestation over the green run would verify, because the same side that produced the program also authored `expected.json`. Our context-bound gate is an illustrative reference protocol, not SLSA certification, and we claim no novelty over trusted provenance. What the paired run adds is the measurement of where the expectations migrated: into the worker's workspace, while the checker bytes stayed locked.

## What did you find in your own gate?

The archived controller object allowed candidate bytes to change while its stored digest stayed unchanged. The old gate then emitted a publication marker. The reproduction requires controller-object access. We have not shown an untrusted worker can reach that object. The corrected protocol derives its digest from immutable entries and stores actual authorized bytes.

## How do you actually fix it?

Three properties, each with a check. The gate has no parameter through which a caller states acceptance: `issue` runs a controller-owned observer over the exact frozen bytes the approval is about to name, and judges the raw observations itself (`release.derived_reject`, and `gate.invalid` in the lab record). An approval binds one destination — account, environment, operation and subject — so an approval issued for one store does not authorize a different one (`release.wrong_destination`, `gate.destination`). And the approval names the verifier's declared trusted base by hash, six files including the isolation runner `lab/run.py`, so changing the verifier invalidates approvals it issued (`gate.verifier_changed`). That binding is the mechanism; this gate still publishes into a controller-owned local database, not a production destination.

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
