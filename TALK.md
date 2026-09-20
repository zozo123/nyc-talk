# Your Agent Escaped Without Escaping the Sandbox

Yossi Eliaz, PhD | AI Agent Security Summit | New York | October 21, 2026

12 main slides. Target 14 minutes plus one minute of margin. Timing is a delivery plan, not a measured rehearsal.

## 1. Your Agent Escaped Without Escaping the Sandbox | 00:00-00:30

I am Yossi Eliaz. Here is the result I want you to remember: the checker prints PASS, its file hash has not changed, and the candidate still allows the unauthenticated admin request.

We will walk through four small, reproducible boundary failures. The final one explains how a worker can influence the evidence used to approve its own work. Everything on screen comes from synthetic fixtures in this repository. The examples use deterministic scripts so the mechanism is repeatable.

## 2. The sandbox gives a worker useful permissions. | 00:30-01:20

Assume the worker can execute the code we allow inside its sandbox. It can use its injected token, write its mounted output and submit a publish request. In the weakened verifier configuration, it can also write the expected-results file.

The controller, its keys, its reference cases and its storage are trusted. We are not trying to compromise that controller or exploit the kernel.

There are four interfaces to inspect: credentials, mounted files, network operations and the inputs to the release decision. Each connects a contained process to something valuable outside its task.

Our Linux lab exercises real namespaces, real bind mounts and a loopback HTTP service. The final admin example is a five-case command-line policy model. Keeping those scopes distinct matters when we interpret the results.

## 3. The injected token can read another project. | 01:20-02:35

The job needs an input file. We give the worker the token that the runner already has. The request on the left uses that token to read another project's private fixture. The service returns 200.

The worker used the credential through its intended interface. The permission was broader than the job.

On the right we replace it with a task-scoped credential. The other-project read returns 403. The input for the actual task still returns 200. The service also rejects the expired and wrong-audience fixtures.

That positive control is important. We did not obtain a safe-looking result by disabling the job. For a real deployment, ask the issuer for the task's audience and minimum scope, then bound its lifetime. A short lifetime alone still permits an over-scoped request while the token is valid.

## 4. A permitted write changes the next job. | 02:35-03:40

The next example uses an ordinary file write. We bind another job's directory into the worker and leave it writable. Writing the file changes the host fixture exactly as the mount configuration permits.

Then we run the same write with a read-only bind. The write is denied and the host fixture is unchanged. The worker can still write its legitimate patch to the output directory.

In a deployment I would usually remove the next job's directory entirely. The read-only experiment is a controlled comparison, not a reason to expose unnecessary data.

Also inspect the state you snapshot. A file carried into a later worker can become that worker's input. Our lab demonstrates the shared mount; snapshot propagation is an architectural consequence to check separately, not an extra experiment we claim to have run.

## 5. An allowed service can receive the wrong upload. | 03:40-05:00

The worker needs to publish a report. The allowed service accepts uploads for more than one account. The worker posts our private fixture to the other account's path, and the receiving service records it.

Checking a service name does not answer who selected the account, the operation or the body. Our lab models that service boundary on loopback; it does not claim to test a particular firewall or SaaS product.

The restricted worker can request one fixed report operation. The controller-side broker rejects extra recipient, payload and URL fields. It constructs the team destination and the report body itself. The worker's separate network namespace cannot reach the host service directly.

The team report still arrives. For this operation the body has no worker-selected free text. That restriction is why this fixture cannot carry arbitrary bytes through the report. A general-purpose text publishing tool needs a separate information-flow decision. Process isolation and the broker's semantic policy have different jobs here.

## 6. The checker stays unchanged throughout the test. | 05:00-06:20

Now the interface is the answer to a more consequential question: may this work be accepted?

The policy says an unauthenticated admin request must return 401. Our small handler represents that request as the command-line input admin colon none. The bad candidate returns 200. We are modeling the authorization decision rather than deploying a web application.

The checker executes the candidate and compares its outputs against expected.json. We measure the checker's bytes before and after execution. They are identical.

There is one fact I have not shown yet: the expected-results file comes from the worker's workspace. Before looking at the next slide, decide what the unchanged hash actually tells us about the decision this checker will make.

## 7. The worker changes the expected result. | 06:20-07:40

The worker writes expectations that allow every request. The bad handler returns 200 for every case. The checker therefore prints PASS.

The checker has done exactly what its code says. Its own integrity check tells us nothing about whether the worker was allowed to redefine the expected answers.

Our independent comparison still requires 401 for an unauthenticated or expired request and 403 for an ordinary user accessing admin. It rejects the same candidate. The legitimate admin and public cases still pass.

We also include the simpler worker-written PASS-file configuration as a detector. It confirms that the experiment can recognize a false accept. The dependency case is the useful reveal: changing the trusted input is enough while the checker code remains unchanged.

Both weak configurations were constructed deliberately. We are reproducing an authority failure, not reporting a vendor zero-day or measuring how often a model discovers it.

## 8. More reviewers can inherit the same bad rulebook. | 07:40-08:40

This is where the result connects to multi-agent systems. Imagine a writer, a reviewer and a tester. They have different prompts, different models, or different sampling temperatures. They all load the same worker-writable expected-results file.

Each can reach agreement using the altered criterion. Agreement does not remove the writer's ability to set that criterion.

The same applies to a second machine that consumes the same contaminated dependency. Moving execution changes the process boundary; the trust dependency still needs inspection.

I would draw a write-authority graph. Starting at every worker-controlled object, follow what reads it and what ultimately influences release. The property we need is that a worker cannot modify the authoritative cases, policy or approval state. This slide is an architectural inference from the demonstrated dependency, not a measured claim about any particular multi-agent framework.

## 9. Approve fixed bytes under controller-owned criteria. | 08:40-10:15

The corrected path has four steps. First, collect the candidate into controller-owned storage and compute a manifest over the actual bytes. Second, execute those bytes and compare the results against controller-owned cases. Third, bind the decision to the artifact, task, run, verifier, expected results, policy, environment description and a one-use nonce. Finally, publish the exact bytes that were authorized.

In this repository publication means writing the bytes and consumed nonce in one SQLite transaction. It is a reference gate, not a production deployment service. A real publisher needs the equivalent guarantee at its own release boundary.

The gate recomputes the payload identity. A cached digest label is insufficient. It also checks the stored bytes before committing publication. The worker never holds the gate key.

We retain a controller-held history anchor in the isolation lab to detect a rewritten event history. That detects disagreement with the retained record. The acceptance comparison and publication gate are what enforce this release decision. Missing or malformed results produce no approval and must be investigated, rather than celebrated as proof of a successful defense.

## 10. A rejected swap preserves the original approval. | 10:15-11:30

These are the distinctions I want in a convincing demo. The correct candidate publishes. The incorrect candidate fails the fixed criteria. A fresh approval for the correct candidate rejects a different artifact. The original bytes can still publish with that approval. Only after that publication do we test replay.

The order matters. During this audit, the previous swap test ran after the approval had already been consumed. That result could not tell us whether the digest check or replay check rejected it. We changed the order and added a regression test.

We also hardened the reference artifact object and checked mutation of the stored bytes. Those are robustness tests at the trusted controller API; they are not evidence that a sandboxed worker can write controller memory.

The suite exercises eight concurrent publication attempts and expects exactly one recorded publication. A timeout or missing result gets no approval. It remains incomplete evidence, not a demonstrated attack rejection.

## 11. Inspect four concrete decisions outside the worker. | 11:30-13:00

For your own deployment, start with one real task and record four answers.

Which identity does the worker receive, and which resources will accept it? Look at scope, audience and lifetime together.

Which state can it write? Include shared workspaces, snapshots, caches and files that another worker later treats as instructions or truth.

For each outbound action, who selects the destination and content? Check whether the worker can bypass the component that is supposed to make that decision.

Finally, who owns the acceptance criteria and the release capability? Trace configuration, imports, expected outputs and other dependencies, not just the top-level checker file. Verify that the bytes released are the ones evaluated.

For each control, run the unwanted action and then the legitimate task. Keep both observations. That is how we distinguish an enforcing boundary from a broken workflow that happens to return an error.

## 12. The release decision needs its own boundary. | 13:00-14:00

We have seen a token read another project, a mounted file change another job, an allowed service receive the wrong upload, and an unchanged checker accept worker-edited expectations.

Each result follows an interface the system provided. The release case is especially important because the worker's output can become the evidence used to authorize the next action.

The repository contains the fixtures, recorded observations, corrected gate and limitations. You can reproduce the cases without a model account or a cloud key.

When you review an agent system, ask: what can this worker make the rest of your system believe?

Then keep the release decision outside its write authority. Thank you.

