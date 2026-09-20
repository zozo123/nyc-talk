# Your Agent Escaped Without Escaping the Sandbox

**Yossi Eliaz, PhD | AI Agent Security Summit | October 21, 2026**

12 main slides. Target: 14 minutes, with one minute of margin. The script is generated from `slides/deck.json`; edit that file, not this one.

## 1. Your Agent Escaped Without Escaping the Sandbox | 00:00-00:35

*Stage cue: Start on the title. Do not introduce the company or sell a product.*

You ask a coding agent to fix authorization. Its checker reports PASS. The checker file has exactly the same hash as before. The unauthenticated admin case still returns two hundred.

I am Yossi Eliaz. I will show how that happens, alongside three other failures that use capabilities we deliberately give a worker. Every demonstration uses synthetic fixtures. The worker scripts are deterministic, so we can inspect the mechanism without debating what a model intended.

## 2. The worker can act. Who can authorize? | 00:35-01:25

*Stage cue: Point to the boundary. State assumptions before showing attacks.*

Here is the threat model. Treat the worker as an arbitrary task program. It can edit its code and writable files, invoke its tools, and ask for its output to be published. We trust the controller and the operating-system boundary. We do not give the worker the controller's key or storage.

In the isolated runs, Linux user, PID, and mount namespaces really are different. Network access is disabled where the experiment requires it. The question is what authority remains through the interfaces we intentionally leave open.

I will use four concrete interfaces: a credential, a shared mount, an upload operation, and the inputs to a checker. For each fix, the legitimate task must still work.

## 3. 1. The inherited token reaches another project. | 01:25-02:35

*Stage cue: Read 200, then 403, then the legitimate 200. The tokens are public fixtures.*

The task needs one input. We start the worker with a synthetic runner token inherited through its environment. That token is broader than the task. The worker asks the service for another project's private fixture. The service returns two hundred and the fixture bytes.

The process has not escaped. The service has accepted a credential we placed inside it.

Now use the task token. The same request returns four-oh-three. The authorized task input still returns two hundred. The service also rejects an expired token and a token for the wrong audience.

The important control is enforced scope. A short expiry reduces the exposure window, but a broad token can still do damage before it expires. Project only the grant this task needs, and validate that grant at the resource. These token strings and the private data on this slide are fixtures, not live credentials.

## 4. 2. The mount grants a write into the next job. | 02:35-03:40

*Stage cue: Do not call this a filesystem escape. The write follows the mount policy.*

The second interface is a shared directory. In the first configuration it is writable. The worker performs an ordinary file write, and the next-job fixture on the host changes. The mount is doing exactly what we configured it to do.

We repeat the same operation with a read-only bind. The write is denied and the host fixture remains unchanged. A separate output mount still accepts the legitimate patch.

That positive control matters. We did not fix the system by making the agent unable to work.

For a system that forks snapshots or reuses workspaces, ask which writable state crosses into the next task. That is an architectural implication of sharing those bytes; we did not measure a snapshot attack here. In this experiment, the demonstrated boundary is the bind mount.

## 5. 3. The allowed service accepts the wrong upload. | 03:40-05:00

*Stage cue: Explain that the service permits both account paths by design. This is a capability mistake.*

Here the task needs to publish a completion report. Our synthetic upload service supports a team report path and another account's upload path. Both live on the same service. The worker sends the private fixture to the other path. The service returns created, and we inspect its receiving-side delivery record to confirm the bytes arrived.

A hostname decision cannot express which account should receive which data. This fixture models that distinction; it is not a test of an enterprise firewall or a SaaS vendor.

In the corrected configuration the worker has no direct route to the service. It can request one operation from a broker. The broker constructs the destination and a fixed body itself. Recipient, payload, and URL overrides are rejected. The legitimate report still arrives.

Both parts matter: the broker must constrain the operation, and the worker must not bypass it. This deliberately narrow reporting interface does not prove that every free-form output channel is free of exfiltration.

## 6. 4. The checker is read-only. Its answer key is not. | 05:00-06:25

*Stage cue: Pause after "Its answer key is not." This is the central reveal.*

Now the fourth interface: the meaning of done. The policy says the unauthenticated admin case must return four-oh-one. The candidate is an intentionally broken handler that always returns two hundred. It is a small status-code model, invoked as a Python program, not a deployed web server.

We put the checker on a read-only mount. With the honest answer key, it reports FAIL. The worker attempts to overwrite the checker and the operating system denies the write.

But the checker reads expected dot json from the workspace. The worker changes that file to expect two hundred. The checker now reports PASS. Its SHA-256 is unchanged. The broken handler's bytes are unchanged too.

The failure is in what the checker trusts. Hashing its source does not bind the specification it loads. A separate machine would not repair this dependency if we copied the same worker-controlled answer key into it. The isolation experiment is recorded; the second-machine statement is the consequence of that dependency, not a separate measured trial.

## 7. Keep the candidate fixed. Change who owns the cases. | 06:25-08:00

*Stage cue: Walk one row at a time. PASS here means the weak checker was fooled, not that the app is safe.*

This comparison is the evidence. Follow the first three rows: the candidate does not change. With the honest workspace key, the weak checker fails it. After the worker changes the key, the same checker passes it. With controller-owned expectations, those same candidate bytes are rejected.

Then the positive control: the corrected handler is accepted. We test five cases. An anonymous admin request is four-oh-one. An administrator receives two hundred. An ordinary user receives four-oh-three. The public route returns two hundred. An expired credential receives four-oh-one.

The always-two-hundred candidate fails three of those expectations. The corrected candidate meets all five.

This is a deterministic reproduction of a known trust-boundary failure. It does not tell us how often a language model discovers the trick, and five cases do not establish universal application security. What it establishes is narrower and useful: moving the answer key outside worker control changes the decision while we hold the bad artifact fixed. That is the experiment to repeat against your own acceptance pipeline.

## 8. Make the release decision outside the worker. | 08:00-09:20

*Stage cue: Point to the worker/controller split, not just the left-to-right arrows.*

The repair has a sequence. Copy the candidate into a narrow frozen representation. Execute those bytes with a read-only candidate mount. The controller compares observed outputs against expectations the worker cannot rewrite.

Only that controller can issue the approval. The approval binds the artifact manifest, verifier, expected results, policy, environment description, task, run, a fresh nonce, and an expiry. Publication rechecks that context and stores the exact approved bytes.

In this repository, publication is a local SQLite transaction. It is a runnable model of the release boundary, not a claim that we integrated with a production deployment system. Consuming the nonce and storing the bytes happen together.

The trust assumption remains important: the worker cannot access the controller key, database, or comparison code. A local Python subprocess with isolated-import flags is not an operating-system sandbox. That is why the local protocol tests and the Linux isolation experiments are separate evidence classes. A hash chain supports integrity checking; it does not decide whether the application behavior meets policy.

## 9. Challenge the gate before you trust the green check. | 09:20-10:35

*Stage cue: Emphasize FRESH. Keep the controller-API audit in the appendix unless asked.*

Now attack the approval protocol itself. Take a fresh, unused approval for the good candidate and offer different bytes. The gate must deny it. Immediately offer the original good bytes with that same approval. They must still publish. Only then test replay.

That ordering prevents a misleading test: if you consume the nonce first, a substitution test can pass because the nonce is already used, even when artifact binding is broken. We corrected that ordering in this repository.

We also hardened our frozen representation and made publication store bytes instead of only a success marker. The appendix records the baseline flaw as controller API misuse. We have not demonstrated a worker crossing the OS boundary to reach those objects.

Finally, distinguish rejection from missing evidence. A timed-out or malformed execution produces no approval. That is a fail-closed outcome, but it is not proof that the candidate met the policy. Keep that distinction in the dashboard and in the release logic.

## 10. More agents do not create an independent judge. | 10:35-11:40

*Stage cue: Connect to software factories without adding untested phase/temperature claims.*

This matters when one worker becomes a software factory. You may have a builder, a reviewer, and a judge. They may run different models or use different prompts. But if all three read a writable answer key produced by the builder, you have replicated the dependency.

Trace who can write the specification, fixtures, dependencies, evidence, and final approval. A second role or a second machine is not automatically a second authority boundary.

You can still let many workers explore, generate competing patches, and propose tests. Keep those proposals distinct from the criteria authorized to promote a release. The final publication path should accept only an approval bound to the selected artifact and decision context.

That is an architectural inference from the dependency we just measured. We are not presenting a multi-agent benchmark or claiming that changing model temperature is a security control.

## 11. Four tests to run on your own deployment. | 11:40-13:10

*Stage cue: This is the audience photo slide. Give it a pause.*

These are the four tests I would take back to a deployment review.

Use the worker's credential to ask for another project's data. The resource should deny it while the real task input remains available.

Attempt a write outside the task's output area. Confirm the shared input stays unchanged and the legitimate patch still appears.

Try to change the recipient or body of the permitted report. Verify both that the broker refuses the request and that the worker cannot bypass the broker. Inspect the receiving system rather than trusting a worker log.

Finally, change an input that determines success. Then try to substitute bytes under a fresh approval. The acceptance decision must use criteria outside worker write authority, and publication must bind to the bytes that were evaluated.

Each denial should come from a component the worker cannot rewrite. Each test needs a positive control. Otherwise a completely broken system can look perfectly secure because nothing ever completes. The repository contains the fixtures, raw observations, source hashes, and reproduction commands so you can inspect exactly what each test means.

## 12. The worker may propose the artifact. It must not define why that artifact is eligible for release. | 13:10-14:00

*Stage cue: Stop at the repository address. Leave the closing slide visible. One minute remains.*

The four failures used interfaces we intentionally gave the worker: a token, a mount, a permitted service, and an answer key. The useful question is not only whether the process can leave its sandbox. It is which decisions the process can cause while it remains inside.

Let the worker propose code, tests, and explanations. Keep the authority that defines acceptance outside its write boundary, and bind the release to the exact artifact that authority evaluated.

The source and recorded evidence are at github dot com, zozo one two three, nyc dash talk. Thank you.
