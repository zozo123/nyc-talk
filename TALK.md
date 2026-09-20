# Your Agent Escaped Without Escaping the Sandbox

**Yossi Eliaz**  
Principal Engineer and Head of DevRel at Incredibuild.com

**15-minute lightning talk.** Twelve main slides, followed by three appendix slides. Target a 14-minute delivery with one minute of margin. Times below are rehearsal targets, not measured delivery times. Blockquotes are stage directions. The slides show recorded results; keep the terminal closed during the talk.

## 1. A small request — 00:00–00:30

You give an agent a small job.

Fix a parser. Publish the report.

It has a sandbox, a copy of the source, and a way to run the tests.

A little later, the check turns green.

Would you accept the patch?

> Advance. Let the audience read the contradiction.

## 2. Something is wrong — 00:30–01:30

Here is the input: one, comma, comma, three.

There is an empty field in the middle. Our specification says to reject it.

The parser returns the list one, three. It silently drops the empty field.

The check says PASS. The original bug is still there.

Keep that contradiction in mind. We will come back to exactly how it happened.

The title says the agent escaped without escaping the sandbox. Here, “escaped” means it exceeded the intended task. Each example uses an interface the deployment made available.

We will follow those grants to another project's data, another job's state, another account's inbox, and finally the decision that tells us the work succeeded.

## 3. The job and the grants — 01:30–02:30

Every grant begins with a reasonable request.

The agent needs source, so we pass it a credential. It needs files, so we mount a directory. It needs to publish a report, so we allow a service. It needs feedback, so we run the workspace checker.

Each choice gives the worker authority.

These are four independent experiments with synthetic data and fixed worker scripts. They test enforcement after an unwanted action has been chosen. They do not measure a model's likelihood of choosing it.

The workers use Linux namespaces. The controller and host remain trusted. We add network separation where the worker should lose direct service access.

For each experiment, watch the unwanted action succeed, the same action fail after the repair, and a legitimate operation still succeed.

## 4. Another project's data — 02:30–04:00

The worker's task is called parser-fix.

The credential it inherited belongs to a runner with access to several projects.

We request another project's private fixture. The service returns it.

> Point to the 200 response, then the 403 below it.

The service recognized a valid credential with permission to read that resource. It honored the grant.

The sandbox did not need to break. The process already held the identity the service would accept.

The label parser-fix was descriptive. The credential carried the authority.

Now repeat the same request with a task-scoped credential. The service returns 403. Request the task's own input, and it returns 200.

The service also rejects expired credentials and the wrong audience.

A short lifetime limits how long a token works. Scope limits what it can do while it works. A broad token can authorize an unwanted request immediately.

At launch, build the environment explicitly. Keep broad credentials outside the worker. Supply the grant this task actually needs.

## 5. Another job's state — 04:00–05:30

Reset the lab.

The excessive grant is now a writable mount.

The worker sees next-job.json, a fixture representing another job's queue setting. It performs an ordinary write.

Outside the sandbox, the host bytes change. The controller checks those bytes directly.

The mount worked exactly as configured. Our configuration let this task alter another task's state.

We reset the file and expose the same path read-only. The same write fails. The host fixture stays unchanged.

We also remove the earlier output before retrying. The restricted worker creates a fresh patch in its output directory.

The policy is concrete: read this input, write this output. The host owns the mount set.

A task that does not need the shared state can lose that mount entirely. Read-only still authorizes reading. Keep that distinction in mind for the next experiment.

## 6. Another account's inbox — 05:30–07:30

Reset again. We allow the reporting service.

The intended destination is the team's report endpoint.

The worker sends our synthetic private fixture to another account on that same service. We inspect the receiving service. The data is there.

The hostname stayed the same. The recipient changed.

Our fixture deliberately accepts uploads to both account paths. It models a service where an upload capability is available for another recipient.

The network decision answered which service the worker could reach. The task also needed a decision about who should receive which data.

For this report, we can make that decision precise.

The worker requests one report operation. An external broker chooses the team account and constructs the body from controller-owned fields. Extra recipient, URL or payload fields are rejected.

The worker also loses its direct route to the fixture service. The permitted report still arrives through the broker.

If the report accepted arbitrary worker-written text, that text could carry private data. The permitted contents matter as much as the recipient.

We have examined identity, files and data release. One grant remains: the authority to declare the job finished.

## 7. The green check — 07:30–08:30

Return to the opening.

The parser is broken. The checker says PASS.

Here is what happened.

The launcher ran a checker from the worker's writable workspace. The worker replaced it with two lines: print PASS, then exit zero.

It left the parser unchanged.

> Pause on the two-line checker.

That is the recorded result: success output and a zero exit code, with the original bug still present. A controller using that result as its acceptance decision would accept the broken work.

We gave the worker permission to edit the solution and the program we relied on to judge it.

Running that altered checker in a fresh process cannot restore the test we overwrote.

## 8. An independent decision — 08:30–10:00

Keep the same broken parser bytes. Change who owns the decision.

The producing worker exits. The controller freezes its output. It runs the candidate in a separate worker for each case. Expected results and the final comparison stay outside.

The empty-field case fails. So does the empty-input case.

The fixed parser passes all five cases.

> Point to the two changed rows. Let the audience compare them.

We have restored the meaning we wanted from PASS: these candidate bytes satisfied checks the producer could not rewrite.

Candidate code still executes behind a process boundary. The verifier does not import it into its own trusted process.

Five cases establish this demonstrated repair. They do not prove complete correctness. Isolation protects who can change the decision. The specification and tests determine what that decision establishes.

## 9. Which bytes passed? — 10:00–11:30

Before accepting the work, ask: are these the same bytes we checked?

Our gate binds approval to the exact artifact, the current run, the verifier and the policy. Its authentication key stays outside the worker. A single-use nonce prevents replay.

Substituted bytes are denied. A reused approval is denied. The verified artifact for the current run is accepted.

Now suppose someone rewrites the history to say the broken parser passed.

A writer controlling an entire hash chain can change an event and recompute the links. In our experiment, the controller retained the original head. The rewritten chain disagrees with it.

That reference exposes the rewrite. It lives in controller memory here; durable retention needs a further design.

The verifier evaluates the candidate. The gate enforces acceptance. The retained reference reveals changed history. A faithful record alone cannot make a bad decision correct.

## 10. Back to the original job — 11:30–12:30

Now give the restricted worker the original task.

It receives read-only source input and a writable output directory. It writes the fixed parser.

The producer exits. The controller freezes those bytes. Independent checks pass. The gate accepts that artifact. Only then does the broker send the fixed report to the team.

One, comma, comma, three.

This time the parser rejects it.

The useful job is complete.

We narrowed the grants around the work and preserved the path to a correct result. The worker could propose the repair. The controller retained authority over acceptance and release.

## 11. Four boundaries to check — 12:30–13:30

For your deployment, write down four answers.

Whose identity can the worker use?

Which files can it read or change?

Who can receive its output, and what can that output contain?

Who can approve these bytes?

Process isolation supports these boundaries by separating the worker from the components that enforce them.

At each boundary, name the component that can refuse the unwanted action outside the worker's control. Then test that the legitimate operation still works.

That gives you something concrete to check in your own system.

## 12. Closing — 13:30–14:00

Our request was small: fix a parser and publish a report.

The deployment also offered a broader identity, shared state, another recipient, and a checker the worker could rewrite.

Each experiment followed a permission we supplied.

The task was defined in our request. Its authority was defined in our infrastructure.

When your next agent starts a job, ask:

**Who gave this process the authority?**

> Stop. Leave the repository URL visible. The remaining minute is delivery margin, not another section.

---

The [recorded Linux run](https://github.com/zozo123/nyc-talk/actions/runs/35461381644) supports the demonstrated results. Primary mechanism references: [Linux environment inheritance](https://man7.org/linux/man-pages/man7/environ.7.html), [bind mounts](https://docs.docker.com/engine/storage/bind-mounts/), [token privilege restrictions](https://www.rfc-editor.org/rfc/rfc9700.html#section-2.3), [artifact verification](https://slsa.dev/spec/v1.2/verifying-artifacts), and [bubblewrap's security model](https://github.com/containers/bubblewrap#sandbox-security).
