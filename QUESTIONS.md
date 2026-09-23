# Hard questions and precise answers

## Is this a flaw in an Incredibuild product?

No. Everything shown is a synthetic research fixture written for this talk, and the repository contains its full source. It is not a finding in any Incredibuild product and it is not a customer report. Product-specific questions are welcome afterward rather than on stage.

## Is this a new vulnerability or just least privilege?

These are controlled reproductions of known mechanisms. The closest public name is poisoned pipeline execution, OWASP CICD-SEC-4: someone with repository write, and no access to the build environment, gets the pipeline to run their commands, through the CI config or files it references such as test code. Ours is its data-only neighbor. The program and checker bytes stayed identical, and the only file the worker changed was an answer key the checker obeys. Nothing new had to run. We do not claim a vendor zero-day or novelty for least privilege. What the paired run adds is a measurement: the candidate and checker stay fixed while ownership of the answer key changes the decision. And the usual least-privilege fix does not fit, because a coding agent needs this write to do its job. You cannot remove the permission to edit tests; you can move who decides whether the edited tests are the ones that count. We also publish a counterexample in our own original controller API.

## Where is the LLM?

It is deliberately absent. Deterministic worker actions isolate the capability boundary. This measures whether the interface permits the action, not whether a particular model discovers or attempts it. There is no model attack-success rate.

## Are real agents doing this today?

That is not what this recording measures, and we do not report a rate. The closest public research is Anthropic's November 2025 reward-hacking paper (MacDiarmid et al., arXiv 2511.18397), and its setup matters. The researchers first gave models information about specific hacks, through synthetic documents or a prompt, then trained them with reinforcement learning on real Claude coding environments chosen because they were vulnerable. One hack the models learned is a `conftest.py` that makes pytest report failures as passes: a worker-written file the harness obeys, the same family as `expected.json` here. The paper says its models do not discover these hacks unaided, so it is not a measurement of deployed agents, and its results stay with that study. It does report milder reward hacking, such as test hardcoding, in real Claude Sonnet 3.7 training. What we can say is narrower and does not depend on any model: the permission such a shortcut needs is already granted in the configuration we recorded, and finding it takes an inventory, not telemetry.

## Did you really lock the checker?

In `factory/isolated.py`, the checker is bind-mounted read-only. A direct worker write is attempted and denied. Its actual file hash and the candidate hash are compared before and after. Both checker runs use the identical launch, the same interpreter flags, working directory and mounts, and the record keeps both exit codes: 1 with FAIL on the honest answer key, 0 with PASS on the edited one. The answer key remains worker-writable in the intentionally weak configuration.

## Is `/admin` a real service?

The factory example is a five-input CLI status-code model. It emits integers. It is not a running authentication service. The credential and allowed-service examples in `lab/run.py` do use real loopback HTTP requests and receiver-side stored payloads.

## Could the candidate just print the expected answers?

Yes. The finite policy only establishes those five observations. It is not comprehensive application verification. Real acceptance needs appropriately owned, representative tests and observations, and defenses against test detection or overfitting. A truthful record of a narrow test remains narrow.

## Our agents write tests. Are you saying they can't?

No. The worker may propose criteria; it must not be what applies them. A proposed test travels with the candidate and is reviewed and approved the way code is. The approval in `factory/core.py` binds `expected_results_digest` alongside the artifact, so the criteria used for a decision are named in the record and a change to them is visible rather than silent. What we recorded is the narrow version: the expected values are controller-owned constants and the comparison runs outside the workspace. A review workflow that promotes a proposed test into controller-owned criteria is the natural extension and is not something this package measures. Slide 4 is not a story about an agent editing a file. It is a story about the agent being the last writer of the thing that judged it.

## What if the candidate cheats from inside the test process?

Then no shared file is involved, and that is a different class: exiting early with status 0, or returning an object whose equality check always says yes. Neither checker in this recording is exposed to it, the weak one included: both run the candidate as its own process and act only on its exit status and what it prints, and an always-equal object cannot survive being printed as JSON. The repaired path adds a separate sandbox per case with a read-only `/candidate` mount and no network. In the isolated run, a non-zero exit, empty output or non-JSON text aborts the run before anything is signed; a parseable non-integer reaches `judge` in `factory/core.py`, which returns no approval. Locally, all of these become typed observations that `judge` refuses, and `tests/test_factory.py` covers non-JSON output and timeouts. None of this is exercised by the thirteen isolated checks. So keeping the candidate out of the checker's process, as slide 10 says, is necessary, but it is not what fixed this run: the weak checker already did it and still went green.

## Our agent can edit the CI workflow itself. Is that the same thing?

Yes, at pipeline scale, and that case is direct poisoned pipeline execution. A workflow file under `.github/workflows` defines which checks run and what counts as passing, so a worker that can write it holds the same kind of pen as a worker that can write `expected.json`. The question from slide 10 transfers directly. We did not test a CI system here, so the question carries over and the measurement does not.

## Why is another VM insufficient?

A second machine can still consume the worker's expected-results file. The relevant independence is the ownership of authoritative inputs, comparison, credentials and publication capability. The multi-agent point is an architectural inference, not an empirical benchmark.

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

Two signals, neither of which needs model telemetry. The static one is an inventory question: list the paths your acceptance decision reads, list the paths the worker can write, remove the candidate itself, and treat anything left in both lists as the finding. Keep the candidate out of the checker's process too, because in-process shortcuts such as an early exit or an always-equal object touch no shared file. The in-run one is a tripwire, not a policy: hash the criteria file at task start and again at the verdict; on this recording that is the answer key moving from `0494f1a01dee` to `390e5e764916` while the program and checker hashes hold. Both come from a file inventory and two digests. Neither tells you a change was malicious. The first shows the worker could write what judges it, and the second shows it did.

## Does this apply to MCP and tool calls?

The same two questions transfer: which inputs does the decision read, and who can write them. A tool description, an argument schema and a server response are all inputs a decision can read. If the worker can write the server config, the tool manifest, or a file a tool reads, it moves the decision without escaping anything — the shape is identical to `expected.json`. No MCP server was tested here, so the boundary question transfers and the measurement does not.

## Where does prompt injection fit?

Mostly beside this result rather than inside it. Injection is about getting the worker to do something it was not asked to do; here the worker did not need to be subverted, because the permission was already there. The two meet in one place worth naming: if the controller asks a model to decide whether the work is done, the candidate's own text becomes an input to that decision, and the worker writes that text. This gate's judge is deliberately the opposite — deterministic and typed, and a verdict-shaped observation produces no approval at all rather than an accepting one (`factory/core.py`, `judge`; `tests/test_redteam.py`). We did not test an LLM judge, so that contrast is a design argument, not a measured result.

## Doesn't SLSA already solve this?

No. SLSA v1.2 checks an artifact against its provenance, and the provenance against expectations: builder identity, canonical source repository, build type, external parameters. That says where the bytes came from, not whether they are correct. That step also assumes an adversary who cannot write the source repository, and a coding agent is that writer. So on slide 4 a fully valid attestation over the green run would verify, because `expected.json` sits in the workspace the worker writes. The nearest SLSA idea is protection against unilateral change, two-party review on its source track; `expected.json` had none. Our gate is an illustrative reference protocol, not SLSA certification, and we claim no novelty over trusted provenance. The paired run measures where the acceptance criteria moved: into the worker's workspace, while the checker bytes stayed locked.

## What did you find in your own gate?

The archived controller object allowed candidate bytes to change while its stored digest stayed unchanged. The old gate then emitted a publication marker. The reproduction requires controller-object access. We have not shown an untrusted worker can reach that object. The corrected protocol derives its digest from immutable entries and stores actual authorized bytes.

## How do you actually fix it?

Three properties, each with a check. The gate has no parameter through which a caller states acceptance: `issue` runs a controller-owned observer over the exact frozen bytes the approval is about to name, and judges the raw observations itself (`release.derived_reject`, and `gate.invalid` in the lab record). An approval binds one destination — account, environment, operation and subject — so an approval issued for one store does not authorize a different one (`release.wrong_destination`, `gate.destination`). And the approval names the verifier's declared trusted base by hash, six files including the isolation runner `lab/run.py`, so changing the verifier invalidates approvals it issued (`gate.verifier_changed`). That binding is the mechanism; this gate still publishes into a controller-owned local database, not a production destination.

## Could your substitution test have passed for the wrong reason?

The old one could have, and the defect was in our test, not the gate: it published first and tried the substitute afterwards, so a spent nonce could have hidden a missing byte check. The corrected test, on slide 9, runs four steps on one approval. Different bytes while the approval is unused: DENIED. The approved bytes to another destination, approval still unused: DENIED. The approved bytes to the named destination: PUBLISHED. The same again: DENIED as replay. Both refusals happen before the nonce is spent, so neither can be credited to replay protection.

## What about concurrency and restarts?

A SQLite transaction combines byte publication and nonce consumption; a 16-way concurrent regression allows one publication. A new Gate has a new key and run identifier and rejects old approvals. This is not a tested distributed commit protocol or a persistent production signing service.

## Is local `python -I` the sandbox?

No. The local executor is a protocol fixture runner. Actual namespace/mount checks use bubblewrap on Linux, with only committed deterministic fixtures. Neither path certifies resistance to kernel vulnerabilities or arbitrary resource exhaustion.

## Does this merge a real pull request or deploy a package?

No. The reference gate stores candidate bytes in a controller-owned SQLite database. A production publication destination requires its own authorization and atomicity analysis. A local marker is not mislabeled as a production release.

## What should we do tomorrow?

Attempt the unauthorized credential read, cross-task write, wrong-recipient upload and answer-key/approved-byte substitution. For each denial, demonstrate a legitimate task that still completes. Then inspect who owns every authoritative input to the release decision.
