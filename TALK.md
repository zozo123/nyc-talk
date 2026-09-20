# Your Agent Escaped Without Escaping the Sandbox

Yossi Eliaz  
Principal Engineer and Head of DevRel at Incredibuild.com

Final spoken manuscript for slides 1–17. Blockquotes are stage directions, not spoken text. Slides 18–20 support questions. The [runbook](RUNBOOK.md) provides a 45-minute rehearsal plan and shorter cuts. The speaking and Q&A allocation still needs organizer confirmation.

**Story:** an ordinary parser repair acquires authority over another project, another job, another recipient, and its own acceptance decision. Act four explains the opening's false success. The ending completes the original task under narrower grants.

The demonstrations use deterministic scripts and synthetic fixtures. The [recorded Linux run](https://github.com/zozo123/nyc-talk/actions/runs/35461381644) passed all 29 checks. The presentation commands below display selected recorded observations. They do not execute attacks or generate new results.

## 1. A small request

You give an agent a small job.

Fix a parser. Publish the report.

It has a sandbox, a copy of the source, and a way to run the tests.

A little later, the check turns green.

Would you accept the patch?

> Advance to slide 2. Pause before explaining the output.

## 2. Something is wrong

Here is the input: 1, comma, comma, 3.

An empty field. The parser should reject it.

It returns the list 1, 3.

The check says PASS. The parser still has the original bug.

Keep that contradiction in mind. We will come back to exactly how it happened.

This is a result from our synthetic lab. We built a small job so we could inspect every permission around it.

The title says the agent escaped without escaping the sandbox. Here, “escaped” means it exceeded the intended task. The process used interfaces the deployment had made available.

We will follow those interfaces from the task to another project's data, another job's state, another account's inbox, and finally the decision that tells us the work succeeded.

## 3. How a small job gets large permissions

Think about the conveniences that make an agent useful.

It needs to fetch source, so we pass it a credential.

It needs files, so we mount a directory.

It needs to publish a report, so we allow an upload service.

It needs feedback, so we run the checker in its workspace.

Each choice makes the next step easier. Each choice also gives the worker authority.

Now compare the two descriptions of the job.

The request says: fix this parser and publish this report.

The infrastructure decides which identity the process can use, which files it can modify, where it can send bytes, and which evidence we will accept.

Those decisions can authorize much more than the request describes.

We will reset the lab four times around the same job. Each time, one of those grants reaches beyond the task.

## 4. The question for every experiment

Assume the agent's code tries an unwanted action. Which component can actually stop it?

For repeatability, our demos use fixed scripts to perform those actions. Credentials and data are synthetic. The service runs locally.

The isolated workers have separate Linux user, PID and mount namespaces. The controller stays outside. We add a separate network namespace where direct service access should be unavailable.

We are testing whether the action is permitted once the code runs. The controller and host remain trusted.

Process isolation separates the worker from the controller's own files and memory under this model. We then have to decide which interfaces to expose across that separation.

For each experiment, watch three things: the unwanted action succeeds, the enforcing component refuses the same action after the repair, and a legitimate operation still succeeds.

The transcript's PASS labels mean the lab observed the expected result. In a “before” check, that expected result can be the security failure we deliberately configured.

> Show only the current act. Do not scroll through later acts and reveal the checker early.

## 5. First grant: the runner's identity

The worker's job is parser-fix.

The credential it inherited belongs to a runner with access to several projects.

We ask for another project's private fixture.

The service returns it.

> On slide 5, run `python3 tools/present.py credentials`. Point to `credentials.before`, then compare `credentials.after` and `credentials.positive`.

Look at the service's decision: it recognized a valid credential with permission to read that resource. It honored the grant.

The sandbox did not need to break. The process already held the identity the service would accept.

The label parser-fix was descriptive. The credential carried the authority.

Now repeat the request with a task-scoped credential. The service refuses it.

Reading the actual task input still works.

The worker's useful job has survived. Its access to the other project has disappeared.

## 6. What the service needs to know

The service needs an enforceable grant: this operation, on this resource, for this audience, until this expiry.

In our lab, a small grant table supplies that policy. An expired credential and one intended for the wrong audience both fail. The service makes those decisions outside the worker.

A short lifetime limits how long a token works. Its scope determines what it can do during that time. A broad credential can authorize an unwanted request immediately.

We also control what reaches the worker in the first place: an explicit environment, only the required descriptors, and no broad upstream credential.

> Ask: “If I give the same token to a process in a stronger sandbox, which service permission changes?” Allow a brief answer. The service still evaluates the same grant.

The question at this handoff is simple: whose authority did we just give to this process?

## 7. Second grant: a directory that reaches another job

Reset the lab.

This time, the excessive grant is a writable mount.

The worker sees a file representing the next job's queue setting. It performs an ordinary write.

Outside the sandbox, the host fixture changes.

> On slide 7, run `python3 tools/present.py mounts`. Explain that the controller checks the host bytes, rather than trusting the worker's claim that it wrote them.

The path looks like a file inside the sandbox. The mount connects it to state outside this task. Its address inside the worker does not tell us who else depends on the underlying bytes.

The mount worked exactly as configured. That is the problem: our configuration let this task alter state belonging to another task.

We reset the file and mount it read-only. The same write fails.

We remove the earlier output before retrying. The restricted worker creates a fresh patch in its own output directory.

That last check matters. We need evidence that useful output still works after the restriction.

## 8. The filesystem is a list of permissions

The worker needs source input and somewhere to put its result.

That gives us a concrete mount policy: read this input, write this output.

In our comparison, the shared job fixture remains visible but read-only. A task that does not need to read it can lose that mount entirely.

Also, read-only means the data can still be read. Keep that in mind for the next experiment.

The host constructs the mount set. The worker does not get to decide which host paths it should receive.

Think of each mount as a grant attached to a resource. A broad directory can include resources with different owners and different consequences.

> Ask: “Who else uses the files under your agent's writable directory?” Leave room for the audience to name caches, later jobs or shared configuration. These are review prompts, not additional tested attacks.

We have limited the worker's identity and the state it can change. It still needs to publish a report. That creates the next boundary.

## 9. Third grant: permission to send a report

Reset again. We allow the report service.

The intended upload goes to the team's report endpoint.

Our worker sends the synthetic private fixture to another account on that same service.

We inspect the receiving service. The data is there, under the other account.

> On slide 9, run `python3 tools/present.py egress`. Start with `egress.before`. Return to the remaining observations on slide 10.

The hostname stayed the same. The recipient changed.

Our fixture deliberately accepts uploads to both account paths. Think of an available upload URL for each account. We are showing the distinction between permission to reach a service and permission to release particular data to a recipient.

Our network decision answered the first question. The task needed an answer to both.

Now remember the read-only mount. If the worker can read a private value and choose arbitrary upload contents, making the source read-only has not settled the release decision.

## 10. A report operation with a known recipient

For this job, we can make that decision precise.

The worker asks for one report operation. An external broker selects the team account and constructs the fixed report from its own fields.

The request is a proposal. The broker owns the decision.

Try adding another recipient. Denied.

Try adding an arbitrary payload. Denied.

Try supplying a different URL. Denied.

The receiving service records no new deliveries for those requests.

There must also be a reason the worker cannot bypass this broker. In the repaired experiment, its separate network namespace has no direct route to the host-loopback fixture service. We test that route explicitly.

Then we request the permitted report. It arrives at the team account.

If we let the worker insert arbitrary text into that report, it could put private data in that text. The permitted contents matter as much as the recipient.

For this fixed report, we can keep destination and contents under controller control. More expressive outputs require their own release policy.

We have now examined who the worker can act as, what it can change, and where it can send data.

One more grant remains: the authority to declare the job finished.

## 11. Fourth grant: control over the green check

Return to the opening.

The parser is broken. The checker says PASS.

Here is what happened.

The launcher ran a checker from the worker's writable workspace. The worker replaced it with two lines: print PASS, then exit zero.

It left the parser unchanged.

> Pause on the two-line checker on slide 11. Run `python3 tools/present.py verifier` and point first to `verifier.before`.

The recorded result is success output and a zero exit code while the buggy parser bytes remain unchanged. A controller using that result as its acceptance decision would accept the broken work.

The agent could change a file that defined success. We had made its own workspace the source of evidence for accepting its work.

The worker needs permission to edit the proposed solution. We also gave it permission to edit the program we relied on to judge the solution.

Running the altered checker in a fresh process cannot restore the test we overwrote. The acceptance criteria need an owner outside the worker's authority.

That is why the green check was misleading.

## 12. The original bug meets an independent check

Now keep the same broken parser bytes and change who owns the decision.

The producer exits. The controller freezes its output. Candidate code runs in a separate worker, while the expected results and final comparison stay outside.

Candidate code still executes behind a process boundary. The verifier does not import it into its own trusted process.

The empty-field case fails. So does the empty-input case.

> Compare the two failing rows on slide 12. Return to `verifier.after` and `verifier.positive` in the recorded output.

The fixed parser passes all five cases.

That is what we wanted the green check to mean: the candidate satisfied checks the worker could not rewrite.

Five cases establish this demonstrated repair. They leave other possible inputs outside the evidence.

Isolation protects who can change the decision. Good tests determine what that decision actually establishes.

## 13. A passing result belongs to one artifact

There is another question before we accept the result.

Are these the same bytes we checked?

If someone swaps the artifact after verification, an earlier PASS should not authorize the replacement.

Our gate ties approval to the exact artifact, the current run, and the verifier and policy that produced the decision.

A single-use nonce prevents reusing that approval. The authentication key stays outside the worker.

> On slide 13, run `python3 tools/present.py acceptance`. Walk through substitution and stale approval. Leave the full field list for questions.

The lab rejects substituted bytes, stale approvals, a changed verifier and replay.

The verified artifact for the current run is accepted.

In this lab, acceptance is a publication decision. We are not deploying software to an external system.

We can now say what passed and what that decision authorizes. Every later step must preserve the relationship between the approved bytes and the current task.

## 14. The record needs an independent reference

We also want to know whether somebody rewrote the history.

A worker that controls an entire hash chain can change an event and recompute the links.

In the lab, we turn a failed verification event into a success. We rebuild the chain.

The controller retained the original head. The new history disagrees with it.

> On slide 14, run `python3 tools/present.py history`. Point out where the original reference lives.

That external reference is what exposes the rewrite.

Our reference lives in controller memory. Production retention needs a durable design.

Keep the responsibilities clear. The verifier evaluates the candidate. The gate enforces acceptance. The retained reference lets us detect a changed record.

A record can preserve a bad decision faithfully. It cannot make that decision correct. That is why the acceptance boundary and the evidence boundary must both be designed.

## 15. Back to the original job

Now give the restricted worker the original task.

It receives the source as read-only input. It writes the fixed parser into its output directory.

The controller freezes those bytes. Independent checks pass. The gate accepts that artifact. The broker sends the report to the team.

> On slide 15, run `python3 tools/present.py final`. Return to the input from slide 2.

One, comma, comma, three.

This time the parser rejects it.

The useful job is complete.

We changed the permissions around the work while preserving the path to a correct result.

## 16. Four boundaries to check

For your deployment, make the answers concrete.

Whose identity can the worker use? Name the resource and operation the service will authorize.

Which files can it read or change? Inspect the mounts and permissions supplied at launch.

Who can receive its output, and what can that output contain? Include direct network paths and mediated operations.

Who can approve the result? Follow the candidate bytes through verification, acceptance and the retained evidence.

Process isolation supports these boundaries by separating the worker from the components that enforce them.

At each boundary, name the component that can refuse the action outside the worker's control.

Then repeat the legitimate operation to check that it still works. Those answers define the task the infrastructure actually permits.

## 17. Closing

Our request was small: fix a parser and publish a report.

The deployment also offered a broader identity, shared state, another recipient, and a checker the worker could rewrite.

Each experiment followed a permission we had supplied.

The task was defined in our request. Its authority was defined in our infrastructure.

When your next agent starts a job, ask:

**Who gave this process the authority?**

> Stop. Leave the repository URL on screen. Invite questions.

---

Mechanism references for preparation: [Linux environment inheritance](https://man7.org/linux/man-pages/man7/environ.7.html), [bind-mount effects](https://docs.docker.com/engine/storage/bind-mounts/), [token privilege restrictions](https://www.rfc-editor.org/rfc/rfc9700.html#section-2.3), [artifact verification](https://slsa.dev/spec/v1.2/verifying-artifacts), and [bubblewrap's security model](https://github.com/containers/bubblewrap#sandbox-security). The recorded experiments support the demonstration-specific results.
