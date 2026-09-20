# Slide-by-slide speaker notes

Main delivery: slides 1-12. Slides 13-16 are Q&A only.

## 1. Your Agent Escaped Without Escaping the Sandbox | 00:00-00:25

I am Yossi Eliaz. I build execution infrastructure for agents.

I want to show you four ways a worker can cross an authority boundary using the interfaces we deliberately gave it. Every case is reproducible. The worker scripts are deterministic, so we can examine the mechanism without depending on what a model happens to do on stage.

[Sources]
https://zenity.io/resources/events/ai-agent-security-summit-2026
https://github.com/zozo123/nyc-talk
[/Sources]

## 2. The checker passed an open-admin candidate. | 00:25-01:20

Here is the result we will come back to. The checker file has exactly the same hash before and after. It prints PASS. The candidate returns two hundred for an unauthenticated admin request, where the controller's policy requires four-oh-one.

This particular candidate is a tiny status-code model: it prints the number. I am not showing a live production website or a customer breach. The acceptance error is real inside this reference experiment.

Keep one question in mind: which bytes were allowed to decide what passing meant? We will answer that after following the three other interfaces into the worker.

[Sources]
https://github.com/zozo123/nyc-talk
[/Sources]

## 3. The worker has four routes to authority. | 01:20-02:15

Assume the worker is adversarial. It can run commands and write its workspace. It can emit requests and candidate code. It cannot rewrite the trusted controller, steal its signing key, or exploit the host kernel in this model.

The interfaces are a credential, mounted files, a permitted service, and the inputs to an acceptance decision. Each interface has a different enforcing component. A namespace can separate processes while a token still authorizes another project. A read-only checker can still read expectations from a writable directory.

The first three cases use a loopback HTTP fixture and real Linux namespace and mount experiments. The fourth isolates the acceptance mechanism. We deliberately keep those scopes separate.

[Sources]
https://github.com/zozo123/nyc-talk
[/Sources]

## 4. The inherited token authorizes another project. | 02:15-03:20

The job needs its own input. We start it with the runner's broader token in the environment. The worker sends an ordinary GET to another project's private path. The service returns two hundred and the synthetic private fixture.

That is an authorized request according to the credential we supplied. No process escape is required.

Now the service receives a task-scoped fixture token. The other project returns four-oh-three. The task's own input still returns two hundred. The expired and wrong-audience fixtures are denied as well.

The enforcing component is the service that checks the credential. Short lifetime limits exposure, while resource scope and audience determine what the token may do during that lifetime. The positive control matters: the worker still obtains the input it needs.

[Sources]
https://github.com/zozo123/nyc-talk
[/Sources]

## 5. The writable mount changes the next job. | 03:20-04:25

Next, the worker needs files. We bind a shared directory into its filesystem and leave it writable. The payload is a normal file write to next-job dot json. The host observes the changed content.

We rerun the same operation against a read-only bind. The write is denied and the host file remains unchanged. A separate output directory remains writable, so the worker can still deliver its patch.

That gives us a concrete filesystem policy: read the required inputs, write the intended outputs, and do not mount another job's writable state. Snapshots deserve the same review because they carry filesystem state into later runs. Snapshot inheritance is a deployment implication here; this experiment tests the bind mount itself.

[Sources]
https://github.com/zozo123/nyc-talk
[/Sources]

## 6. The allowed service accepts an unintended destination. | 04:25-05:45

The worker must publish a report. We allow it to reach a service. That service also accepts uploads addressed to another account. The worker sends the private fixture to that path, and the receiving fixture records the delivery.

A hostname allowlist has not specified the recipient or the payload.

In the restricted case, the worker's network namespace cannot directly reach the host-loopback service. It can request one broker operation. The broker fixes the destination and constructs the report body from controller-owned values. Requests with extra recipient, URL or payload fields are denied, and the receiving service records no delivery for those attempts. The legitimate team report still arrives.

This tests one direct route and one fixed-schema operation. It does not prove the absence of every timing channel or every possible network bypass. The practical question is who controls the complete outbound envelope.

[Sources]
https://github.com/zozo123/nyc-talk
[/Sources]

## 7. The worker changed the answers the checker trusted. | 05:45-07:35

Now return to the green checker. The ticket says unauthenticated admin access must produce four-oh-one. The checker file is mounted read-only in the isolated run. An attempted write to it is denied. Its hash remains unchanged.

But look at what the checker reads. It loads expected dot json from the worker's workspace. The worker writes a case saying that admin without authentication should return two hundred. The buggy candidate returns two hundred. The checker compares those two numbers and prints PASS.

The file that expresses the expected behavior has crossed the acceptance boundary. Protecting the checker's source did not protect the meaning of its decision.

We evaluate exactly the same bad candidate against controller-owned cases. Three of five comparisons fail: no authentication, ordinary-user authentication, and expired authentication. The legitimate admin and public cases still pass. The independent decision is reject.

The deliberately weakened configuration is labeled as such. It is a detector we built, not a newly discovered vendor vulnerability. Its value is that you can reproduce both the false acceptance and the correction, including an unchanged checker hash. Moving that same checker and the same writable expectations to another machine would preserve the dependency error.

[Sources]
https://github.com/zozo123/nyc-talk
[/Sources]

## 8. Bind the decision to the bytes that are released. | 07:35-09:05

The corrected path starts by copying the candidate into a bounded immutable representation. The controller derives the manifest and digest from those bytes. It evaluates the candidate in an acceptance environment and compares observations against criteria the worker does not own.

An approval binds the artifact, task, run, policy, verifier bundle, acceptance-environment manifest, expiry and a one-use nonce. The release operation validates that approval and stores the exact approved payload. In this reference implementation, release means a controller-owned database object, not a production deployment or a Git merge.

A missing result or a timeout produces no approval. That is fail-closed behavior, not evidence that an attack was defeated. A correct candidate must still pass.

The history chain has a separate job. A rewritten history can be detected against a head retained outside worker control. History does not establish that the expected answers were correct. The controller's policy and comparison remain trusted inputs.

[Sources]
https://github.com/zozo123/nyc-talk
https://slsa.dev/spec/v1.2/verifying-artifacts
[/Sources]

## 9. Every denial needs its matching positive control. | 09:05-10:35

These rows are the evidence I would want to see before trusting the demo.

The correct candidate is accepted and its exact bytes are stored. The open-admin candidate is rejected. Worker-written expectations can still fool the deliberately weakened checker, while the independent comparison rejects the same candidate.

For substitution, we use a fresh approval for good bytes and first try bad bytes. That is denied. We then submit the original good bytes with the same approval, and publication succeeds. Only after that do we test replay and get a denial.

The ordering matters. If you consume the nonce first and then try a substitution, the denial could be explained entirely by replay protection. It would not isolate byte binding.

Our audit also found a mutable-object problem in the earlier reference implementation. The appendix contains the reproduction and the limited threat scope. The current gate derives identity from immutable bytes and atomically stores the payload with nonce consumption. The regression suite also checks concurrent publication.

[Sources]
https://github.com/zozo123/nyc-talk
[/Sources]

## 10. A second reviewer can inherit the same bad criteria. | 10:35-11:35

This applies when there are many agents, too. A builder, a reviewer and a repair agent can all share the same mutable workspace. They can therefore agree because they read the same worker-edited expectations.

Different models, temperatures or roles may improve exploration. They do not by themselves establish an independent acceptance policy.

I would let those workers generate candidates and evidence in parallel, then promote one immutable candidate through the controller-owned decision. A reviewer can recommend acceptance. The release credential and the trusted criteria remain outside that worker pool.

We have not measured a multi-agent attack success rate here. This is the trust-boundary implication of the dependency case we just reproduced.

[Sources]
https://github.com/zozo123/nyc-talk
[/Sources]

## 11. Run four paired tests against your deployment. | 11:35-13:10

Here are the four paired tests I would take back to an agent platform.

Give the worker its normal task credential. Attempt access to another project's fixture, then confirm its own task input still works.

Attempt a write to a protected or cross-job path, then confirm an intended output can still be written. Include the state that will be inherited through snapshots or caches in your review.

Try to change the recipient and payload of a permitted publication request. Confirm those changes create no delivery, confirm the worker cannot use a direct bypass, and then send the legitimate report.

Finally, modify the worker-visible expectations and claim PASS for a bad candidate. The independent acceptance path should reject it. Try substituting different bytes under a fresh approval, then use that same approval with the original good bytes. Publish once and test replay.

For every result, record the enforcing component, the observed side effect and the positive control. That turns a diagram of your security boundaries into a repeatable experiment.

[Sources]
https://github.com/zozo123/nyc-talk
[/Sources]

## 12. Before accepting an agent's work, identify every input that can change the verdict. | 13:10-14:00

The four cases used authority we supplied: a broad credential, a writable shared path, a permitted endpoint and an acceptance dependency the worker could edit.

The Linux isolation checks can succeed while these higher-level decisions are still wrong. Each needs an enforcing component that owns the relevant policy.

Before accepting an agent's work, identify every input that can change the verdict. Freeze the candidate, own the criteria, and release those bytes.

The repository includes the source, transcripts, negative and positive controls, and the exact limitations of the experiment. Thank you.

[Sources]
https://github.com/zozo123/nyc-talk
[/Sources]

## 13. What these experiments establish | APPENDIX A

Use this slide when asked what was actually tested. The recorded mode and exact source hashes are checked before deck generation. Do not promote the local mode into an isolation result. The controller and its storage are trusted in both modes. The loopback fixture is not an Internet-wide egress assessment.

[Sources]
https://github.com/zozo123/nyc-talk
https://github.com/containers/bubblewrap
[/Sources]

## 14. We found a defect in our own earlier gate. | APPENDIX B

This is an audit result about our own reference implementation, not a product exploit. The baseline gate wrote metadata rather than a deployed artifact. The same-process harness exercises an API invariant; worker reachability was not established. That is why the main talk leads with the reproducible dependency-boundary case rather than calling this a sandbox escape.

[Sources]
https://github.com/zozo123/nyc-talk
[/Sources]

## 15. Reproduce without a live stage dependency. | APPENDIX C

Present the PDF and its recorded observations. Do not log into a cloud provider on stage. Build the deck before travel. For a technical follow-up, run the local factory or the Linux isolated suite and compare the new record with the checked-in evidence. A hash is an integrity identifier, not an independent attestation.

[Sources]
https://github.com/zozo123/nyc-talk
[/Sources]

## 16. Sources and prior work | APPENDIX D

SLSA is prior work for binding and checking artifact provenance. Anthropic is context that test and reward manipulation is a documented concern; their measured rates do not apply to these deterministic fixtures. Bubblewrap documents that policy depends on its arguments. The event page confirms the date and audience, not this experiment's conclusions.

[Sources]
https://github.com/zozo123/nyc-talk
https://github.com/containers/bubblewrap
https://slsa.dev/spec/v1.2/verifying-artifacts
https://www.anthropic.com/research/emergent-misalignment-reward-hacking
https://zenity.io/resources/events/ai-agent-security-summit-2026
[/Sources]

