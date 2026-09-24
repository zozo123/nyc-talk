# Hard questions and precise answers

Each answer starts with what to say. The detail below it is for follow-ups.

## Is this a flaw in an Incredibuild product?

No. Everything shown is a synthetic research fixture written for this talk, and the repository contains its full source. It is not a finding in any Incredibuild product and it is not a customer report. Product-specific questions are welcome afterward rather than on stage.

## How is this different from the other talks here today?

The contribution here is a reproducible comparison. The program and checker stay fixed while a worker-edited answer file changes the result. The repository also shows the corrected configuration and the intended operation succeeding.

The same package records three neighboring cases (a broad token, a writable shared mount, an upload to another account), each with its change and a paired check that the intended operation still works. If someone names the confused deputy, agree: the checker acted on expected answers the worker wrote.

## Is this new?

No. The mechanism is familiar. This experiment makes the dependency visible and tests a specific correction.

The closest public name is poisoned pipeline execution, OWASP CICD-SEC-4: someone with repository write, and no access to the build environment, gets the pipeline to run their commands through the CI config or files it references, such as test code. Ours is its data-only neighbor. The program and checker bytes stayed identical, and the only file the worker changed was the expected-results file the checker reads. Nothing new had to run. What the paired run adds is a measurement: the candidate and checker stay fixed while ownership of the expected answers changes the decision. We also publish a bug we found in our own earlier release gate.

## Where is the LLM?

The worker is a script so the experiment repeats the same actions. We measure what the setup permits, not how likely a model is to try it.

There is no model attack-success rate. For a model example, the slide "What METR observed" cites METR's report; its results stay with that report.

## Are real agents doing this today?

In published evaluations, models have changed how their work was measured. The example on the slide "What METR observed" is METR's: o3, asked to make code faster, changed the timing function used to measure it. None of those results are measurements from this experiment, and we report no rate.

If pressed for numbers, the rates, task names and METR's own caveats (a crude monitor, possible underestimates, contrived harmful scenarios) are in [research/DOSSIER.md](research/DOSSIER.md), section 9. Quote them from there, with the caveats, or not at all.

A related study: Anthropic's November 2025 paper (MacDiarmid et al., arXiv 2511.18397) includes a worker-written `conftest.py` that makes pytest report failures as passes. Its models were first given information about the hacks, then trained on environments chosen because they were hackable, and the paper says they do not discover the hacks unaided. That is motivation, not a measurement we transfer.

## Would process separation fix it?

It avoids the in-process route in METR's example, where the candidate's code changed the scorer from inside its own process. It does not fix this one: our weak checker already ran the candidate as a separate process and still read the writable answer file.

Both o3 moves METR describes were code the scorer imported: o3's solution replaced the `time.time` that `score.py` used to time it, and on a contest task its code rebound `evaluate_rust_code`, which `score.py` then awaited. Neither changed a file anyone had protected, so a read-only mount would not have stopped them. Both checkers in this recording run the program as its own process and act only on its exit status and what it prints, so those moves had nothing to patch here, by construction rather than by measurement. Process separation is one necessary property, not a complete security guarantee.

## What if the candidate cheats from inside the test process?

Then no shared file is involved, and that is a different class: exiting early with status 0, or returning an object whose equality check always says yes.

Neither checker in this recording is exposed to it: both run the candidate as its own process, and an always-equal object cannot survive being printed as JSON. The repaired path adds a separate sandbox per case with a read-only `/candidate` mount and no network. In the isolated run, a non-zero exit, empty output or non-JSON text aborts the run before anything is signed; a parseable non-integer reaches `judge` in `factory/core.py`, which returns no approval. Locally, these become typed observations that `judge` refuses, and `tests/test_factory.py` covers non-JSON output and timeouts. None of this is exercised by the thirteen isolated checks.

## Did you really lock the checker?

Yes. In `factory/isolated.py` the checker is bind-mounted read-only, a direct worker write is attempted and denied, and its file hash is compared before and after.

The candidate hash is compared too. Both checker runs use the identical launch (same interpreter flags, working directory and mounts), and the record keeps both exit codes: 1 with FAIL on the original expected answers, 0 with PASS on the edited ones. The expected-results file remains worker-writable in the intentionally weak configuration.

## Is `/admin` a real service?

No. The checker example is a five-input command-line model that prints status integers. It is not a running authentication service.

The credential and upload examples in `lab/run.py` do use real loopback HTTP requests and receiver-side stored payloads.

## Could the candidate just print the expected answers?

Yes. The five cases only establish those five observations. They are not comprehensive application verification.

Real acceptance needs representative tests with a separate owner, and defenses against test detection or overfitting. A truthful record of a narrow test remains narrow.

## Our agents write tests. Are you saying they can't?

They can. The distinction is between proposing a test and approving it as a release requirement. Our controller uses its own expected values; this repository does not implement a review process for agent-proposed tests.

The approval in `factory/core.py` binds `expected_results_digest` alongside the artifact, so the criteria used for a decision are named in the record and a change to them is visible rather than silent. A workflow that reviews a proposed test and promotes it into the controller's criteria is the natural extension; it is not something this package measures.

## Our agent can edit the CI workflow itself. Is that the same thing?

Yes, at pipeline scale, and that case is direct poisoned pipeline execution. A workflow file under `.github/workflows` defines which checks run and what counts as passing, so a worker that can write it can change the rules behind the check.

The four questions on "Where to look in your pipeline" transfer directly. We did not test a CI system here, so the questions carry over; the measurement does not.

## Why is another VM insufficient?

Because a second machine can still read the worker's expected-results file. What matters is who controls the authoritative inputs, the comparison, the credentials and the publication step, not how many machines are involved.

The multi-agent point is an implication of shared writable inputs, not a measured benchmark.

## What stops the worker editing the controller's criteria?

In the repaired path there is no controller copy inside the worker's sandbox to edit. That is a configuration fact of this experiment, not a demonstrated denial.

The expected values and the comparison are `CASES` and `POLICY` in `factory/core.py`, evaluated in the controller process. The sandboxed invocation receives a read-only `/candidate` mount and no network; no controller path is mounted, and `expected.json` is never consulted. None of the thirteen isolated checks tests controller unreachability. An agent with controller filesystem or process access defeats this model; `research/INVARIANTS.md` records that as a trust assumption.

## Do snapshots make it safe?

No. Snapshots preserve bytes. They do not decide whether a copied test file should be authoritative or whether a token should be available in the next task.

Reproducibility and authorization are different properties.

## Does the broker stop every leak?

No. This broker accepts one fixed operation with no arbitrary destination or payload fields, and the worker loses its direct network route. We demonstrate that one operation, not universal data-loss prevention.

Allowing arbitrary report text, additional tools, uncontrolled metadata or other channels changes the threat model.

## Does short token lifetime fix excessive permissions?

No. The service must enforce task scope and audience. Expiration limits the exposure window; it does not narrow what a broad token can reach while it is valid.

## Is a hash chain proof the work is correct?

No. The history check detects a rewrite relative to a separately retained controller anchor.

Rewriting both history and an unprotected head would defeat that comparison. Correctness comes from criteria the worker cannot change and the evidence checked against them, not from an internally consistent log.

## How would we see this in our own pipeline?

Take one release check. List the expected answers, configuration and helper code it reads, list what the agent can write, remove the candidate itself, and treat anything left in both lists as the finding.

Keep the candidate out of the checker's process too, because in-process shortcuts such as an early exit or an always-equal object touch no shared file. For an in-run signal, hash the criteria file at task start and again at the verdict; on this recording that is `expected.json` moving from `0494f1a01dee` to `390e5e764916` while the program and checker hashes hold. Neither signal tells you a change was malicious. The first shows the worker could change the rules behind the check, and the second shows it did.

## Does this apply to MCP and tool calls?

The same two questions transfer: which inputs does the decision read, and who can write them. No MCP server was tested here.

A tool description, an argument schema and a server response are all inputs a decision can read. If the worker can write the server config, the tool manifest, or a file a tool reads, it can move the decision without escaping anything, just as with `expected.json`.

## Where does prompt injection fit?

Mostly beside this result. Injection is about getting the worker to do something it was not asked to do; here the worker did not need to be subverted, because the permission was already there.

The two meet in one place: if the controller asks a model to decide whether the work is done, the candidate's own text becomes an input to that decision, and the worker writes that text. This gate's decision is deterministic and typed, and a verdict-shaped observation produces no approval at all (`factory/core.py`, `judge`; `tests/test_redteam.py`). We did not test an LLM judge, so that contrast is a design argument, not a measured result.

## Doesn't SLSA already address this?

A valid signature alone would not show that our expected answers had independent approval. SLSA verification also checks expectations, and its guidance discusses protection against unilateral changes to them. We did not run a signed-attestation verification experiment.

[SLSA v1.2 artifact verification](https://slsa.dev/spec/v1.2/verifying-artifacts) checks an artifact against its provenance, and the provenance against expectations such as builder identity, source repository, build type and external parameters. Whether a verifier would have flagged this run depends on what it was configured to expect. Our gate is an illustrative reference protocol, not a SLSA implementation or certification, and we claim no novelty over trusted provenance.

## What did you find in your own gate?

The earlier gate trusted a stored digest after the candidate bytes changed, and emitted a publication marker. This required access to the controller object; we did not show a worker-to-controller exploit.

The current gate derives its digest from the bytes it publishes and stores those bytes. Details and the reproduction are in [research/AUDIT.md](research/AUDIT.md).

## How do you actually fix it?

Keep the rules behind the check under a separate owner, and make the gate decide for itself.

In this repository that means three properties, each with a check. The gate has no parameter through which a caller states acceptance: `issue` runs a controller-owned observer over the exact frozen bytes the approval will name and judges the raw observations itself (`release.derived_reject`, and `gate.invalid` in the lab record). An approval binds one destination (account, environment, operation and subject), so an approval issued for one store does not authorize another (`release.wrong_destination`, `gate.destination`). And the approval names the verifier's declared source files by hash, six files including the isolation runner `lab/run.py`, so changing the verifier invalidates approvals it issued (`gate.verifier_changed`). This gate still publishes into a controller-owned local database, not a production destination.

## Could your substitution test have passed for the wrong reason?

The first version could have. The defect was in our test, not the gate: it published first and tried the substitute afterwards, so a spent approval could have hidden a missing byte check.

The corrected test, on "What our first test missed", runs four steps on one approval. Different bytes while the approval is unused: DENIED. The approved bytes to another destination, approval still unused: DENIED. The approved bytes to the intended destination: PUBLISHED. The same again: DENIED as reuse. Both refusals happen before the approval is spent, so neither can be credited to replay protection.

## What about concurrency and restarts?

A SQLite transaction combines byte publication and nonce consumption; a 16-way concurrent regression allows one publication. A new Gate has a new key and run identifier and rejects old approvals.

This is not a tested distributed commit protocol or a persistent production signing service.

## Is local `python -I` the sandbox?

No. The local executor is a protocol fixture runner. Actual namespace and mount checks use bubblewrap on Linux, with only committed deterministic fixtures.

Neither path certifies resistance to kernel vulnerabilities or arbitrary resource exhaustion.

## Does this deploy a real package?

No. The reference gate stores the bytes in a controller-owned SQLite database.

A production publication destination needs its own authorization and atomicity analysis. A local database row is not presented as a production release.

## What should we do tomorrow?

Pick one release check and run the four questions from "Where to look in your pipeline" against it.

Then attempt the unauthorized credential read, cross-task write, wrong-recipient upload, expected-results edit and approved-byte substitution in your own setup. For each denial, show that the intended operation still completes under the same conditions.
