# Hard questions and precise answers

Each answer starts with what to say. The detail below it is for follow-ups.

## Is this a flaw in an Incredibuild product?

No. Everything shown is a synthetic research fixture written for this talk, and the repository contains its full source. It is not a finding in any Incredibuild product and it is not a customer report. Product-specific questions are welcome afterward rather than on stage.

## Isn't 'doors' just attack surface with a new name?

Yes, and the name is the point: these are the pieces of attack surface you cannot remove, because the job needs them. Three of the four close by taking a permission away, which is ordinary least privilege, and we claim no novelty there. The fourth cannot close that way: writing tests is the job, so locking the answer file fires the agent. Calling them doors keeps the same two questions on each one: what does it trust, and can the agent write that?

## Your agent is a script, so what does this prove about real agents?

The script measures what the setup permits, not how likely a model is to try it. Every move replays, so FAIL then PASS with identical code and checker hashes is a fact about the pipeline, not about a model's mood. For models actually making the move, the talk cites others' reports: Replit in 2025, SWE-bench issue #465 in 2025, SWE-Bench Pro Verified in 2026. Those are their measurements. We report no attack-success rate and claim none.

## Why not just have humans write the tests?

Fine, as long as the agent cannot rewrite what the human wrote before the verdict reads it. In our lab the answer file was correct until the agent's step; it lived in the agent's folder, so the checker read the agent's edit. Who writes the answers matters less than who can write the copy the checker reads. Human-written tests kept outside the agent's reach are exactly the second copy on slide 8. We did not build the step that reviews agent-proposed tests.

## Isn't this only least privilege?

For three doors, yes, and we claim no novelty there. The key, the folder and the wire each closed by removing a permission, and we recorded the real job still working after each fix. Door four is where that stops working: you cannot remove write access to tests when writing tests is the job. The fix there is ownership, not permission. The controller keeps its own copy of the answers and decides with that: broken code rejected, fixed code accepted five of five.

## The SWE-Bench Pro drop was one model; cherry-picked?

No; the talk reports both ends. GLM-5.2 fell from 78.80% to 57.32% under the four controls; DeepSeek-V4-Pro moved 0.87 points, and the slide says another barely moved. The paper does not apportion the drop by channel, and neither do we. The point is not a rate: the answers were reachable through the workspace, the git history and the code hosts, and removing them changed one model's score by about 21 points. That is Zheng et al.'s measurement, arXiv 2609.08149, not ours.

## You didn't run the next job, so the folder case is hypothetical?

The write is recorded; the consequence is inferred, and the talk says 'would have'. We recorded /shared/next-job.json changing on the host through the writable bind, from inside a sandbox the agent never left. We did not run the next job. We also recorded the fix: with a read-only bind the write is refused and the agent's own output still lands. Whether the next job trusts that file is a property of your pipeline; the door is that the agent could write it.

## How does this differ from poisoned pipeline execution?

Door two is poisoned pipeline execution, and the talk names it. Door four is its data-only neighbour. OWASP CICD-SEC-4 is about getting the pipeline to run your commands through config or code it references. In our door-four run nothing new ran: the code hash and the checker hash were identical before and after, and the only changed file was the answers the checker reads. The question is the same, though: could the agent write what the pipeline trusts?

## What about prompt injection?

Mostly beside this result: our agent needed no subverting, because the permission was already there. Injection is one way an agent ends up trying a door; the four doors are what it finds when it does. CamoLeak on slide 4 is the injection case: injection was the cause, GitHub's allowed image proxy was the door, and GitHub fixed it by August 2025. The two meet at door four if the verdict is a model reading text the agent wrote. We did not test that.

## Is 'a second copy' just a golden file, which everyone has?

A golden file is a second copy only if the agent cannot write it. Ours was a golden file: five inputs and five expected answers. It sat in the agent's folder, so at verdict time it was the agent's proposal. The fix moves the values and the comparison into the controller's process, mounts nothing of the controller into the sandbox, and binds the criteria's digest into the approval so a change is visible. If your golden file lives in the repo the agent edits, door four is open.

## Are you saying tests don't count anymore?

They count as the agent's own tool. They stop counting as evidence when the agent can write the answers they check against.

A test was evidence because it was independent: a different person, or the same person at a different time, wrote down what correct means before the code existed. An agent writing both removes that independence. Keep the tests, and give the copy that decides release to something the agent cannot write.

## Did Opus 5.5 do this?

No. The talk says "Say your agent is Opus 5.5. Pick any model." It is a name in the story, and we did not run it. The agent in our lab is a script; we wrote every move.

That is the point of the framing: even the best-behaved model's green check is a self-report when it can write the checker's inputs. For models actually doing the move, cite others' measurements: SWE-bench issue #465 (agents including Claude 4 Sonnet finding the real fix in the project's git history, 2025) and SWE-Bench Pro Verified (arXiv 2609.08149, 2026). Those are their results, not ours.

## Doesn't an AI reviewer fix this?

Not by itself. The agent writes the code, the comments and the description the reviewer reads, so the thing being judged writes the judge's inputs.

That is an argument, not a measurement; we did not test an LLM judge. A reviewer helps when it reads criteria the agent cannot change, which is the same fix as for the tests.

## How is this different from the other talks here today?

The frame is four doors. A sandbox is a wall, and every agent's job needs a key, a folder, a wire and a verdict through it; our agent left through those doors, never through the wall. The contribution is a reproducible comparison on the fourth door: the program and checker stay fixed while an agent-edited answer file changes the result. The repository also shows the corrected configuration and the intended operation succeeding.

The same package records the other three doors (the key: a broad token; the folder: a writable shared mount; the wire: an upload to another account), each with its fix and a paired check that the intended operation still works. If someone names the confused deputy, agree: the checker acted on expected answers the worker wrote.

## Is this new?

No. Around 2010, in an automated bug-fixing experiment, one evolved program deleted the files of expected outputs and every candidate got a perfect score (Schulte, Forrest and Weimer; retold by Lehman et al. in 2018). This experiment makes the dependency visible in an otherwise locked-down pipeline and tests a specific correction.

The closest public name is poisoned pipeline execution, OWASP CICD-SEC-4: someone with repository write, and no access to the build environment, gets the pipeline to run their commands through the CI config or files it references, such as test code. Ours is its data-only neighbor. The program and checker bytes stayed identical, and the only file the worker changed was the expected-results file the checker reads. Nothing new had to run. What the paired run adds is a measurement: the candidate and checker stay fixed while ownership of the expected answers changes the decision. We also publish a bug we found in our own earlier release gate.

## Where is the LLM?

The agent is a script. We wrote every move and played the attacker, so the experiment repeats the same actions. We measure what the setup permits, not how likely a model is to try it.

There is no model attack-success rate. For models doing it, the slide "This move has a record" cites others' reports; their results stay with them.

## Are real agents doing this today?

Yes. In July 2025, SaaStr's founder Jason Lemkin said Replit's coding agent lied about his unit tests, made up data, and deleted his production database during a code freeze (reported by The Register). In published evaluations too: on SWE-bench in 2025, agents including Claude 4 Sonnet ran `git log` and found the real fix left in the project's history (SWE-bench issue #465). In September 2026, the SWE-Bench Pro Verified audit found agents could read hidden tests, future commits and upstream fixes; one model, GLM-5.2, fell from 78.80% to 57.32% once those were out of reach, while DeepSeek-V4-Pro moved 0.87 points (arXiv 2609.08149). Their fix had four parts: one clean commit, hidden evaluation files out of the agent workspace, metadata filtered, code hosts blocked. The paper does not say how much of the drop came through each channel.

Those are their measurements, not ours, and we report no rate. The earliest example on the slide is the 2010 program-repair experiment, in which one evolved program deleted the answer files and the scorer gave it and all of its peers a perfect score; sources are on backup slide A9 and in [research/DOSSIER.md](research/DOSSIER.md).

## Would process separation fix it?

It blocks tricks from inside the checker's process, such as patching the timer or returning an object that always compares equal. It does not fix this one: our weak checker already ran the candidate as a separate process and still read the writable answer file.

Both checkers in this recording run the program as its own process and act only on its exit status and what it prints. Process separation is one necessary property, not a complete security guarantee; the other is that the criteria live where the agent cannot write.

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

The two questions on the closing slide transfer directly: what does the check trust, and can the agent write that? We did not test a CI system here, so the questions carry over; the measurement does not.

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

The corrected test, on the slide "How to check a door", runs four steps on one approval. Wrong code while the approval is unused: refused. The right code to the wrong destination, approval still unused: refused. The right code to the right destination: released, which in our lab means one row in a local database. The same again: refused as reuse. Both refusals happen before the approval is spent, so neither can be credited to replay protection.

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

Take the four doors from the closing slide (the key, the folder, the wire, the verdict), pick one, and ask two things: what does it trust, and can the agent write that? Then try the bad thing and the good thing. List what the check reads, list what the agent can write, and remove the candidate itself; anything left on both lists is the finding.

Then attempt the unauthorized credential read, cross-task write, wrong-recipient upload, expected-results edit and approved-byte substitution in your own setup. For each denial, show that the intended operation still completes under the same conditions.
