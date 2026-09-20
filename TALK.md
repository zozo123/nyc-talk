# Your Agent Escaped Without Escaping the Sandbox

Yossi Eliaz  
Principal Engineer and Head of DevRel at Incredibuild.com

Spoken manuscript for slides 1–17. Slides 18–20 are appendix material.

**Story:** a small request becomes a larger grant of authority at each interface. The opening's false success gets its explanation in act four. The ending completes the original task under narrower grants.

The demonstrations use deterministic scripts and synthetic fixtures. The [recorded Linux run](https://github.com/zozo123/nyc-talk/actions/runs/35461381644) passed all 29 checks.

## 1. A small request

You give an agent a small job.

Fix a parser. Publish the report.

It has a sandbox, a copy of the source, and a way to run the tests.

A little later, the check turns green.

Would you accept the patch?

## 2. Something is wrong

Here is the input: 1, comma, comma, 3.

An empty field. The parser should reject it.

It returns the list 1, 3.

The check says PASS. The parser still has the original bug.

Keep that contradiction in mind. We will come back to exactly how it happened.

This is a result from our synthetic lab. To explain it, we need to look at what we gave the worker.

## 3. How a small job gets large permissions

Think about the conveniences that make an agent useful.

It needs to fetch source, so we pass it a credential.

It needs files, so we mount a directory.

It needs to publish a report, so we allow an upload service.

It needs feedback, so we run the checker in its workspace.

Each choice creates an interface through which the worker can affect something we care about.

We will reset the lab four times around the same job. Each time, one of those grants reaches beyond the task.

## 4. The question for every experiment

Assume the agent's code tries an unwanted action. Which component can actually stop it?

For repeatability, our demos use fixed scripts to perform those actions. Credentials and data are synthetic. The service runs locally.

The isolated workers have separate Linux user, PID and mount namespaces. The controller stays outside. We add a separate network namespace where direct service access should be unavailable.

We are testing whether the action is permitted once the code runs. The controller and host remain trusted.

## 5. First grant: the runner's identity

The worker's job is parser-fix.

The credential it inherited belongs to a runner with access to several projects.

We ask for another project's private fixture.

The service returns it.

Look at the service's decision: it recognized a valid credential with permission to read that resource. The label parser-fix did not narrow the grant.

Now repeat the request with a task-scoped credential. The service refuses it.

Reading the actual task input still works.

The worker's useful job has survived. Its access to the other project has disappeared.

## 6. What the service needs to know

The service needs an enforceable grant: this operation, on this resource, for this audience, until this expiry.

A short lifetime limits how long a token works. Its scope determines what it can do during that time.

We also control what reaches the worker in the first place: an explicit environment, only the required descriptors, and no broad upstream credential.

The question at this handoff is simple: whose authority did we just give to this process?

## 7. Second grant: a directory that reaches another job

Reset the lab.

This time, the excessive grant is a writable mount.

The worker sees a file representing the next job's queue setting. It performs an ordinary write.

Outside the sandbox, the host fixture changes.

The mount worked exactly as configured. That is the problem: our configuration let this task alter state belonging to another task.

We reset the file and mount it read-only. The same write fails.

The worker still creates a fresh patch in its own output directory.

## 8. The filesystem is a list of permissions

The worker needs source input and somewhere to put its result.

That gives us a concrete mount policy: read this input, write this output.

In our comparison, the shared job fixture remains visible but read-only. A task that does not need to read it can lose that mount entirely.

Also, read-only means the data can still be read. Keep that in mind for the next experiment.

The host owns this policy. The worker cannot be responsible for enforcing restrictions on its own file access.

## 9. Third grant: permission to send a report

Reset again. We allow the report service.

The intended upload goes to the team's report endpoint.

Our worker sends the synthetic private fixture to another account on that same service.

We check the receiving account. The data is there.

The hostname stayed the same. The recipient changed.

Our network decision answered which service the worker could reach. The task also needed a decision about who should receive which data.

## 10. A report operation with a known recipient

For this job, we can make that decision precise.

The worker asks for one report operation. An external broker selects the team account and constructs the fixed report from its own fields.

Extra recipient, URL or payload fields are rejected.

The worker also loses its direct route to the fixture service. The legitimate report still arrives through the broker.

If we let the worker insert arbitrary text into that report, it could put private data in that text. The permitted contents matter as much as the recipient.

We have now examined who the worker can act as, what it can change, and where it can send data.

One more grant remains: the authority to declare the job finished.

## 11. Fourth grant: control over the green check

Return to the opening.

The parser is broken. The checker says PASS.

Here is what happened.

The controller ran a checker from the worker's writable workspace. The worker replaced it with two lines: print PASS, then exit zero.

It left the parser unchanged.

And the controller accepted the result.

The agent could change a file that defined success. We had made its own workspace the source of evidence for accepting its work.

That is why the green check was misleading.

## 12. The original bug meets an independent check

Now keep the same broken parser bytes and change who owns the decision.

The producer exits. The controller freezes its output. Candidate code runs in a separate worker, while the expected results and final comparison stay outside.

The empty-field case fails. So does the empty-input case.

The fixed parser passes all five cases.

That is what we wanted the green check to mean: the candidate satisfied checks the worker could not rewrite.

Five cases establish this demonstrated repair. A better verifier still needs a good specification.

## 13. A passing result belongs to one artifact

There is another question before we accept the result.

Are these the same bytes we checked?

If someone swaps the artifact after verification, an earlier PASS should not authorize the replacement.

Our gate ties approval to the exact artifact, the current run, and the verifier and policy that produced the decision.

The lab rejects substituted bytes, stale approvals, a changed verifier and replay.

The verified artifact for the current run is accepted.

We can now say what passed and what that decision authorizes.

## 14. The record needs an independent reference

We also want to know whether somebody rewrote the history.

A worker that controls an entire hash chain can change an event and recompute the links.

In the lab, we turn a failed verification event into a success. We rebuild the chain.

The controller retained the original head. The new history disagrees with it.

That external reference is what exposes the rewrite.

Our reference lives in controller memory. Production retention needs a durable design. The principle is the same: keep the evidence used to judge the worker outside its authority to rewrite.

## 15. Back to the original job

Now give the restricted worker the original task.

It reads the source. It writes the fixed parser into its output directory.

The controller freezes those bytes. Independent checks pass. The gate accepts that artifact. The broker sends the report to the team.

This time, when we return to the empty-field input, the parser rejects it.

The useful job is complete.

We changed the permissions around the work while preserving the path to a correct result.

## 16. What did we give it?

For your deployment, make the answers concrete.

Which host interfaces can the process reach?

Which files can it read or change?

Whose authority can it use, and who can receive its output?

Who decides whether the work is acceptable?

At each boundary, name the component that can refuse the action outside the worker's control.

Those answers define the task the infrastructure actually permits.

## 17. Closing

Our request was small: fix a parser and publish a report.

The deployment also offered a broader identity, shared state, another recipient, and a checker the worker could rewrite.

Each experiment followed a permission we had supplied.

The task was defined in our request. Its authority was defined in our infrastructure.

When your next agent starts a job, ask:

**Who gave this process the authority?**
