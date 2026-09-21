# Your Agent Escaped Without Escaping the Sandbox

**Yossi Eliaz, PhD / NYC / October 21, 2026 / 15 minutes**

Generated from `slides/talk.tex`. Edit the LaTeX, then run `make deck`. Main route: slides 1-12. Delivery budget: 14 minutes plus one minute of margin. Timings are rehearsal targets, not measured delivery.

Spoken manuscript: 1,307 words.
## 1. Your Agent Escaped Without Escaping the Sandbox

**00:00-00:30**

*Start immediately. The contradiction is on the next slide.*

You ask an agent to fix authorization. It finishes. The checker says PASS. The checker itself is protected. Would you release the result?

I am Yossi Eliaz. Let me show you a small experiment where every one of those statements is true, and the authorization bug is still there.

## 2. The checker passes. The policy fails.

**00:30-01:20**

*Pause between PASS and 200. These are recorded observations.*

On the left, the checker reports PASS. On the right, the unauthenticated admin case returns two hundred. Our policy requires four-oh-one.

This is a deliberately small command-line model of authorization. Those numbers are program outputs. We are not showing packets from a production server.

The surprising part is what stayed constant. The broken candidate has the same bytes. The checker has the same bytes. The operating system refuses the worker's attempt to overwrite the checker.

Something else changed. To see it, follow the inputs to the decision.

## 3. The task and the trust boundary

**01:20-02:15**

*State the worker's actual control. Keep the setup brief.*

The worker can edit task code and its workspace. It can propose tests and write reports. That is ordinary coding-agent authority.

We protect the checker with a read-only bind mount. The controller process, approval key and release store remain outside worker control. We trust the kernel and the controller.

The promise is narrow: the worker should not be able to approve an artifact that fails the controller's acceptance policy.

Our worker is a deterministic script. That lets us test whether an action is permitted. It does not measure whether a particular model would discover or choose that action.

## 4. The original check catches the bug

**02:15-03:10**

*Establish the negative control before revealing the edit.*

First, establish that the check can catch the bug. The candidate always returns two hundred. With the honest expectations, the checker reports FAIL and exits with status one.

Next, the worker tries to write the checker. The operating system denies that write. We also hash the checker before and after the worker step.

So this is not the simple demonstration where someone replaces a grader with a program that exits zero. The check works, and the protected file stays protected.

Now look at the file the checker opens to learn what the answers should be.

## 5. The worker changes the answer key

**03:10-04:45**

*Point at expected.json, then PASS. Pause before the takeaway.*

The checker reads expected dot json from its working directory. That file lives in the workspace the worker can edit.

The worker changes the expected outputs to two hundred. For the anonymous admin case, the expected value changes from four-oh-one to two hundred. The candidate still returns two hundred. Now those values match, and the unchanged checker prints PASS.

Protecting the executable protected only one dependency of the decision. The answer key still belonged to the producer.

The consequence is precise. A controller that promotes this PASS to release eligibility accepts the worker's definition of success. This experiment demonstrates the false PASS. It does not claim a production deployment occurred.

You can replace this file with a workspace plugin, imported helper, test configuration or worker-written report. Those are audit leads, not additional attacks we measured here. The concrete dependency we reproduced is the answer key.

## 6. Independent checks reject the bad bytes

**04:45-06:15**

*Read the first three rows slowly. The fourth row proves the job still works.*

Here is the controlled comparison. The first three rows use the same bad candidate bytes.

The honest workspace key makes the checker fail. The worker-edited key makes it pass. Controller-owned expectations reject that same candidate.

Then we run a corrected handler. It passes all five controller-owned cases. Anonymous admin and expired credentials produce four-oh-one. An ordinary user produces four-oh-three. The authorized administrator and public route produce two hundred.

The repair preserves the legitimate job. We have not simply disconnected everything until the attack stops.

Five cases establish this policy's tested behavior. They do not prove all possible application behavior. The useful result is the paired change: move the criteria outside producer control, reject the bad artifact, and still accept the valid one.

## 7. Production and acceptance

**06:15-07:40**

*Explain the two arrows across the boundary: bytes and observations.*

The controller first freezes the candidate bytes. A separate isolated run executes those bytes with a read-only candidate mount. The run returns observations. The controller compares them with criteria the worker cannot rewrite.

The controller also owns the approval key and publication store. A harness saying finished has no authority to issue that approval.

A fresh acceptance machine can help implement this separation. But copying the producer's answer key into it preserves the bad dependency. A fork of the producer's disk also carries whatever expectations, configuration and caches the producer left there.

Our recorded repair uses Linux isolation and a controller-side comparison. The design requirement is ownership of the decision's dependencies. Count those dependencies before you count machines.

## 8. The gate binds approval to bytes

**07:40-09:00**

*Stress fresh approval. A consumed nonce would confound the substitution test.*

Independent checking still leaves a second question: do we release the bytes we checked?

Take a fresh approval for the good candidate. Offer bad bytes under that approval. The gate denies them. Offer the original bytes with the same approval. They publish. Offer them again. The gate rejects the replay.

The order matters. If you consume the approval first, a broken digest check can hide behind the already-used nonce. We corrected that misleading test order in this repository.

Here, publication means storing the approved bytes in a controller-owned SQLite database. It is a local release model. The same transaction stores the bytes and consumes the nonce. A real deployment needs to preserve that binding all the way to the consumer.

## 9. Three agents share one writable answer key

**09:00-10:00**

*Explicitly label this as an architectural implication.*

This is why the experiment matters to an agent factory. Add a builder, a reviewer and a judge. Give them different prompts, or different models. If they all trust the builder's writable answer key, they still share the same compromised criterion.

Freezing that workspace in a snapshot preserves the criterion. It does not establish who was authorized to choose it.

This slide is an architectural implication of our dependency, not a measured multi-agent attack. Agents can propose tests and explore solutions. Promotion criteria need a separate owner, and proposals need an explicit route to become authorized policy.

## 10. Four deployment boundaries

**10:00-12:00**

*The surrounding abstract categories. Spend most time on the positive controls.*

The answer-key failure sits inside a wider map of authority. Our repository includes three supporting boundary demonstrations.

First, identity. A broad fixture token reads another project's private data. A task-scoped token gets denied there, while still reading its own input. The service must enforce the resource grant. Short lifetime alone cannot narrow a broad token.

Second, files. A writable mount lets the worker change the next job's fixture. A read-only input mount blocks that write, while a separate output remains writable.

Third, outbound operations. One service accepts both the legitimate report and an upload to another account. The corrected broker fixes the destination and body, and the worker has no direct route around it. We inspect the receiver to confirm delivery or its absence.

Finally, acceptance. The worker must not change the governing criteria or substitute the released bytes.

For each boundary, require both a denied unauthorized effect and a successful legitimate job. Otherwise a system that cannot do any work looks secure. These are separate boundary experiments, not steps in one attack chain.

## 11. A release decision needs more than PASS

**12:00-13:00**

*Explain the three responsibilities. Do not turn history into the gate.*

A useful approval names the artifact, verifier, expected results, policy and run. Our reference gate also binds the environment description, task, decision, nonce, expiry and schema.

Keep verification, authorization and history distinct. A consistent history can faithfully record a bad decision. Our hash-chain check detects a rewrite only relative to a separately protected anchor.

Likewise, a green worker test or a successful harness exit cannot substitute for independent acceptance. Missing or malformed observations produce no approval.

For a release review, ask for evidence that the published artifact is the artifact evaluated under the intended criteria. A PASS without that context leaves the important question unanswered.

## 12. Who controls what makes the work releasable?

**13:00-14:00**

*Leave this slide on screen. Stop by 14:00 and retain one minute of margin.*

The checker was protected. The candidate never improved. The worker changed the answer key, and PASS changed meaning.

That is the question I want you to take home: who controls what makes the work releasable?

Trace the authority through every input to that decision. Keep the criteria outside producer control. Freeze the candidate, evaluate it independently, and publish those exact bytes. Then rerun the unauthorized attempt and the legitimate task.

The repository has the source, recorded observations and limits. This is a controlled reproduction of a known failure mechanism, with a repair you can inspect. Thank you.
