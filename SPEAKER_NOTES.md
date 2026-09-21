# Slide-by-slide speaker notes

Generated from `slides/talk.tex`. Slides 1-12 are the main talk. Slides 13-18 are for Q&A. Present the PDF offline.

## Slide 1: Your Agent Escaped Without Escaping the Sandbox

00:00-00:40

Say the sentence. Stop.

The agent changes the answers. The check goes green.

A pull request is open to fix admin login. The program prints 200 for every request. No login on the admin page must return 401. The test answers live in the checkout, next to the program.

I am Yossi Eliaz. One GitHub Actions job. The file that matters is the answer file sitting in the checkout. The program stays wrong. The test starts agreeing with it. That agreement is the whole fifteen minutes. Everything else on stage is how the job is wired.

[Sources]
https://github.com/zozo123/nyc-talk/blob/main/research/DOSSIER.md
[/Sources]

## Slide 2: One GitHub Actions job

00:40-01:40

Workflow on the left. Checkout on the right.

A GitHub Actions job splits in two. The workflow file comes from the default branch. That file is the check. The checkout is the pull request. The program and the answer file are in the checkout.

A pull request from a fork gets a read-only job token. The privileged trigger runs the default-branch workflow and can hold a write token. Since June 2026 the checkout action refuses a fork head in that job. A same-repo change still lands in a checkout the job runs.

We recorded that shape on a Boat Ubuntu machine. The calls are loopback. The mounts are real. There are five cases. The deck reads those recordings. It does not call GitHub. The point of the job picture is small: the check and the answers are not in the same place. The check is the workflow. The answers are in the pull request.

[Sources]
https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target
https://github.com/zozo123/nyc-talk/blob/main/research/DOSSIER.md
[/Sources]

## Slide 3: No login must be 401

01:40-02:50

Point at 200. Say what a correct program prints.

admin:none is one request. The route is admin. The login is none. A correct program prints 401. This program prints 200 for every request. The admin page is open.

The checker that grades it sits with the workflow and is read-only. It loads expected.json from the checkout. When the printed number matches the file, it prints PASS. The agent is allowed to edit files in the checkout, so it can edit the answers. Replacing the checker is denied. That is the whole opening: the grade and the program can be brought into agreement while the admin page stays open.

[Sources]
https://github.com/zozo123/nyc-talk/blob/main/factory/core.py
[/Sources]

## Slide 4: The answer file

02:50-04:30

Read the two JSON lines. Pause.

Honest file: admin:none expects 401. The program prints 200. The checker prints FAIL and exits 1.

The agent writes 200 into the expected rows. admin:none now expects 200. The program still prints 200. The attempt to overwrite checker.py is denied. The hash before matches the hash after. The same checker prints PASS and exits 0.

The check is green. The program you would merge still lets anyone into admin. Remember the filename: expected.json. It is an ordinary JSON file in the pull request, and the checker trusts it. Anyone who can edit the pull request can edit the grade, and the workflow will report success.

[Sources]
https://github.com/zozo123/nyc-talk/blob/main/evidence/isolated-factory.json
https://github.com/zozo123/nyc-talk/blob/main/factory/core.py
[/Sources]

## Slide 5: Same program. Four results.

04:30-06:10

FAIL, PASS, REJECT, ACCEPT.

Same program. Four results.

Honest answers in the checkout: FAIL. Answers the agent wrote: PASS. Cases stored on the runner: REJECT. The fixed program returns 401 for no login, 200 for a real admin, 403 for an ordinary user, 200 for the public page, and 401 for an expired login. The runner accepts it.

The real fix can merge. What changed between FAIL and PASS was the answer file, not the program. Put that file on the runner, with the workflow, and the checkout can still hold the code. Five numbers cover this policy: 401, 200, 403, 200, 401. They are the policy we ran.

[Sources]
https://github.com/zozo123/nyc-talk/blob/main/evidence/isolated-factory.json
[/Sources]

## Slide 6: Then the merge

06:10-07:40

Denied. Published. Denied.

Green is the check. Merge is the next step. Freeze the program. Run those exact bytes. Compare them with the cases on the runner. Then one fresh approval.

The bad program: DENIED. The judged program: PUBLISHED. Those bytes again: DENIED.

This recording publishes the corrected handler and refuses the program that always prints 200. Compare first, then spend the approval. An earlier version of this gate spent the approval first, and a bad swap could hide behind an already-used approval. The order on this slide is the whole demonstration: the bad program is offered while the approval is still live.

[Sources]
https://github.com/zozo123/nyc-talk/blob/main/evidence/isolated-factory.json
https://github.com/zozo123/nyc-talk/blob/main/factory/core.py
[/Sources]

## Slide 7: Three more files in the job

07:40-09:20

Token, disk, host. One result each.

Three more things in the same kind of job. Each one is its own recording.

The job token reads another project's private fixture and gets 200. A token for this task gets 403 there and 200 on this job's own input. Expired and wrong-audience tokens get 403.

The next job's file is mounted writable. The write changes the host file. A read-only mount denies it. This job's own patch still writes.

The job may call one host. A post of the private fixture to another account is stored, 201, and the receiver log has the bytes. The repair sends one fixed team report from the runner. Extra fields are denied, and the checkout has no route of its own. The team report still arrives. These three rows are separate runs. They sit in one job because a real workflow has a token, a disk, and a host.

[Sources]
https://github.com/zozo123/nyc-talk/blob/main/evidence/results.json
[/Sources]

## Slide 8: The next run keeps the file

09:20-10:20

One sentence. Move on.

Copy this checkout into the next run and expected.json still expects 200. The next job grades against the edited answers. A cache, a reusable workspace, or a forked machine does the same thing if it copies the tree.

This follows from the file the agent changed. We did not run a separate trial across several jobs. A copied workspace keeps whatever the last job wrote, including a grade of 200 for no login. The next run will go green on the same open admin page.

[Sources]
https://github.com/zozo123/nyc-talk/blob/main/research/DOSSIER.md
[/Sources]

## Slide 9: Keep the answers on the runner

10:20-11:30

Left file moves to the right.

Move the answer file to the runner, beside the workflow. Leave the program in the checkout.

The agent can change the code. The agent cannot change the grade. The honest cases fail the open admin page. The runner rejects that program. The fixed program is accepted and can be published. The checkout remains the place where the agent writes handler.py. The answers move to the side that merges.

[Sources]
https://github.com/zozo123/nyc-talk/blob/main/factory/isolated.py
[/Sources]

## Slide 10: On your job

11:30-12:40

Four rows. Then stop.

On your own job, check four places. The token may read this job's input and is refused on another project. The disk may take this job's output and refuses a write to the next job. The host delivers the team report and refuses another account. The check publishes the real fix and refuses an edited answer file.

Do that on the runner. Then run the real ticket again, so the job can still ship. A check that can only refuse will also refuse the fix. Each row needs both columns.

[Sources]
https://github.com/zozo123/nyc-talk/blob/main/evidence/results.json
https://github.com/zozo123/nyc-talk/blob/main/evidence/isolated-factory.json
[/Sources]

## Slide 11: Compare, then approve

12:40-13:20

Three words. Denied, published, denied.

Say the order once more. Denied. Published. Denied. One fresh approval. The bad program first, while the approval is still live. Then the program that was judged. Then a replay, which is refused. If the replay is refused before the bad program is tried, the demonstration hides the swap.

The publication stores those exact bytes and spends the approval in the same write. What leaves the job is the program that was compared, and it leaves once.

[Sources]
https://github.com/zozo123/nyc-talk/blob/main/factory/core.py
[/Sources]

## Slide 12: Who merged it?

13:20-14:00

Leave the question up.

The agent changed the answers. The check went green.

Who merged it?

Keep the answers with the workflow. Freeze the program. Publish those bytes. Run the open-admin case again, and run the real fix again.

The repository has the source and the Linux recordings from the Boat machine: the token, the mounts, the upload, the answer file, and the merge. Open expected.json in the job you run tomorrow. If that file is in the checkout, the grade belongs to whoever edits the pull request. Thank you.

[Sources]
https://github.com/zozo123/nyc-talk/blob/main/research/DOSSIER.md
[/Sources]

## Slide 13: The five policy cases

Appendix only

Use only in Q&A.

The handler takes a route and an authentication label and prints an integer. The runner checks these five. The repaired handler matches all five. This is the model of the check that promotes into the prod sandbox.

[Sources]
https://github.com/zozo123/nyc-talk/blob/main/factory/core.py
[/Sources]

## Slide 14: Runner token and the dev disk

Appendix only

Use only in Q&A.

The token case is loopback HTTP. The broad fixture stands in for the runner secret. The task fixture stands in for a job-scoped token. The mount case watches the host file after an ordinary write from the dev sandbox. This job's output stays writable.

[Sources]
https://github.com/zozo123/nyc-talk/blob/main/evidence/results.json
[/Sources]

## Slide 15: Allowed host, wrong account

Appendix only

Use only in Q&A.

The fixture service permits both account paths, the way one allowed deploy host holds more than one operation. The delivery record shows the bytes arrived. The repair moves the POST onto the runner and removes the dev sandbox's direct route.

[Sources]
https://github.com/zozo123/nyc-talk/blob/main/lab/run.py
https://github.com/zozo123/nyc-talk/blob/main/evidence/results.json
[/Sources]

## Slide 16: An earlier promote stored a marker

Appendix only

Use only in Q&A.

The archived case mutates a controller-side object, keeps a stale digest, and the old gate records a publication marker. The current promote derives the digest from immutable bytes and stores those bytes. Reaching the old flaw takes access to the controller object.

[Sources]
https://github.com/zozo123/nyc-talk/blob/main/research/AUDIT.md
https://github.com/zozo123/nyc-talk/blob/main/evidence/baseline-audit.json
[/Sources]

## Slide 17: What was recorded

Appendix only

Use only in Q&A.

The records bind their source. The dev sandbox recordings use bubblewrap on a Boat Ubuntu machine. The harness under test is a script. The prod step in the recording is the runner's publication of exact bytes, the shape of what a prod sandbox is allowed to execute. The forked-disk slide follows from that workspace file. The timings are a delivery budget.

[Sources]
https://github.com/zozo123/nyc-talk/blob/main/research/RESULTS.md
[/Sources]

## Slide 18: Reproduce the factory

Appendix only

Use only in Q&A.

Run the fixtures on disposable Linux with bubblewrap. The deck reads those recordings. Poisoned pipeline execution is the public name for a CI job that runs an attacker-influenced file. Anthropic's reward-hacking study is prior motivation and its measurements stay with that study. Reproducing the talk needs no GitHub token.

[Sources]
https://github.com/zozo123/nyc-talk
https://tessl.io/
https://github.com/containers/bubblewrap#sandbox-security
https://slsa.dev/spec/v1.2/verifying-artifacts
https://www.anthropic.com/research/emergent-misalignment-reward-hacking
[/Sources]
