# Your Agent Escaped Without Escaping the Sandbox

Yossi Eliaz  
Principal Engineer and Head of DevRel at Incredibuild.com

Speaker manuscript for the 17-slide main talk. Slides 18–20 are appendix material. The accompanying lab uses synthetic data and deterministic worker scripts. All 29 isolated-mode checks passed in the [recorded Linux run](https://github.com/zozo123/nyc-talk/actions/runs/35461381644).

## 1. Title

I want to start with a result that looks reassuring.

A worker finishes its task. The checker prints PASS. The controller sees exit code zero.

The parser is still broken.

## 2. The check passed

The input is `1,,3`. Our parser should reject the empty field. Instead, it returns `[1, 3]`.

The worker did not fix the parser. It changed the checker.

That result comes from the synthetic lab in this repository. The broken artifact stays byte-for-byte unchanged while the workspace checker reports success. An independent check still catches the bug.

We will return to that result. First, we need to ask what authority the worker received.

## 3. One job

The operator's request is simple: fix the parser and publish the task report.

That implies some necessary permissions. Read the source. Write a candidate patch. Request a report upload.

It does not imply permission to read another project's private data, alter another job, choose arbitrary recipients, or decide its own acceptance criteria.

We will examine four independent experiments around this same task. Each starts with fresh fixtures. They are four ways to misuse granted authority, not four required steps in one intrusion.

## 4. The experiment

The workers are deterministic scripts representing actions an agent could generate. We are testing what the execution system permits after adversarial code runs. We are not measuring how reliably a prompt causes an LLM to generate that code.

The credentials are synthetic. The service runs on loopback. The data is a canary we created for this purpose.

In the isolated run, workers receive separate Linux user, PID and mount namespaces. The controller and fixture service remain outside them. Where the worker should have no direct service access, it also receives a separate network namespace.

The controller is trusted. Its code, keys and decisions are part of the trusted computing base.

## 5. Borrowed identity

The first worker receives a broad credential from its launcher.

Its task is parser-fix. Its token permits access to other projects.

We ask it to read the unrelated project's private fixture. The service returns HTTP 200 and the canary. The process did not need a kernel exploit. It presented a credential the launcher gave it.

Now we launch the same request with a task-scoped credential. The service returns 403.

We also run the legitimate request. Reading parser-fix's input still returns 200. Expired and wrong-audience credentials receive 403.

The important observation is the service's decision, made outside the worker.

## 6. The identity boundary

A task ID describes what we want. A credential determines what a service will allow.

We should construct the worker environment explicitly and close unnecessary inherited descriptors. We should keep broad upstream credentials outside the worker.

Any projected grant needs a specific resource, operation, audience and lifetime.

A short lifetime helps limit exposure. It does not narrow a token's permissions while that token remains valid.

Process isolation and credential authorization have separate jobs. Both need an enforcing owner.

## 7. The mount

The second experiment uses a different resource: a harmless file representing the next job's queue setting.

We deliberately bind-mount it into the worker's filesystem with write access.

The worker writes to its visible path. The controller observes changed bytes in the host fixture.

This is the configured behavior of a writable bind mount.

We reset the fixture and rerun the same action with a read-only bind. The write fails. The host bytes stay unchanged.

We remove the earlier patch output before the repaired run. The worker still creates a fresh patch in its permitted output directory.

## 8. The filesystem boundary

The mount set is part of the task contract.

Source input can be read-only. Task output can be writable. Controller files should stay outside the worker's mount set.

In this lab, keeping the shared fixture visible but read-only gives us a direct before-and-after comparison. A production task that does not need that fixture can omit it entirely.

Also remember what read-only means. It prevents modification. It still permits reading.

The host must enforce these grants. A path check inside editable worker code cannot carry that responsibility.

## 9. The allowed service

Our third worker can reach an upload service.

The intended destination is the team's report endpoint. The same service also exposes another account's upload endpoint.

The worker sends the synthetic private fixture to that second account. We inspect the receiving service and confirm that it stored the canary there.

The network destination stayed the same. The recipient changed.

This is why a hostname alone says too little about an authorized data flow.

## 10. The data-release boundary

For this task, we replace arbitrary upload access with one narrow operation: publish this task's fixed report.

The worker emits an untrusted request. The broker accepts one exact schema, constructs the report body from its own fields and selects the team account.

Requests containing extra recipient, payload or URL fields are rejected. The receiving service records no delivery for those requests.

The repaired worker also receives a separate network namespace. Its direct probe cannot reach the host's loopback service. The broker remains able to perform the legitimate report operation.

This is a specific data-release policy. If we allowed arbitrary worker-selected strings in the report, those strings could carry private data. A schema helps only when its permitted content matches the intended release.

## 11. Manufactured success

Now return to the green checker and broken parser.

The vulnerable controller runs a checker from the worker's writable workspace and accepts its exit code.

The worker replaces that checker with two lines: print PASS and exit zero.

The parser stays broken. The controller still accepts it.

The filesystem write is familiar from the previous experiment. The consequence here is different: the worker controls evidence used to declare its own success.

## 12. Independent verification

The repaired controller waits for the producer to exit, then snapshots the candidate bytes.

It runs that candidate in a separate worker and compares its output with expectations held outside the worker.

The buggy parser fails two of our five cases: an empty field and an empty input.

The fixed parser passes all five.

Candidate code never executes inside the controller process. The controller owns the comparisons and the decision.

These five cases establish this particular defect and repair. They do not prove correctness for every input. Independence protects the decision process; the quality of the specification still matters.

## 13. Exact-byte acceptance

A passing result must identify the artifact it authorizes.

Our lab approval binds the artifact digest, task run, verifier source digest, policy and a single-use nonce. A controller-held MAC authenticates that approval.

We test several ways to misuse it.

Swap the artifact after verification: denied.

Use an authentic approval for a stale run: denied.

Change the verifier identity: denied.

Modify the approval or replay one already consumed: denied.

Present the verified bytes for the current run: accepted.

The gate in this lab returns a publication decision. It does not deploy anything externally.

## 14. The history anchor

We also record verification events in a hash chain.

Suppose an attacker changes a failed result to success and recomputes all the links. The new chain is internally consistent.

Our controller retained the original head. The rewritten chain disagrees with that independent reference.

That is the trust requirement: the reference must stay outside the attacker's control.

In this lab, the reference lives in controller memory. A production system needs an appropriate durable anchor and retention design.

History provides evidence of rewriting. The verifier and gate enforce acceptance.

## 15. The original task succeeds

Now run the intended task with the restrictions in place.

The worker reads the input and writes the fixed parser to its output directory. It receives no service credential and has no direct route to the fixture service.

The controller snapshots the output. The independent verifier checks it. The gate accepts those exact bytes. Only then does the broker publish the fixed task report.

The complete isolated suite passes 29 checks, including this positive end-to-end case.

Useful work still happens under the narrower grants.

## 16. Four deployment questions

For any agent deployment, ask four concrete questions.

What can execute and reach the host?

What can read and change files?

What can act on services and send data?

What can declare the task successful?

For each answer, identify the component that can refuse the action outside the worker's control.

A product name is not enough. We need the actual identities, paths, recipients, operations and acceptance rules.

## 17. Closing

The worker in our experiments used interfaces the deployment supplied.

A credential. A mount. An upload endpoint. A checker.

Each one carried authority beyond the intended task.

The practical work is to make those grants explicit, enforce them outside the worker, and test that the legitimate task still succeeds.

When you inspect your next agent deployment, ask:

**Who gave this process the authority?**

