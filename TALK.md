# Your Agent Escaped Without Escaping the Sandbox

**Yossi Eliaz**  
Principal Engineer and Head of DevRel at Incredibuild.com

**15-minute lightning talk.** Nine main slides, three appendix. 14 minutes plus one minute of margin. Stage directions in blockquotes. Results are already on the slides. No terminal.

## 1. Cold open — 00:00–00:45

I am going to show you a breach where every namespace and cgroup did exactly what they were designed to do.

An agent gets a small job. Fix a parser. Publish the report. It runs in a sandbox. The sandbox does not break.

The check turns green.

The parser still silently drops an empty field. One, comma, comma, three. Spec says reject. It returns one, three.

Would you ship it?

Most of this room spent two years putting agents in boxes. That was the right instinct. It is the wrong finish line.

> Advance. Let the contradiction sit.

## 2. The property you bought is not the property you needed — 00:45–02:15

Isolation answers one question: can this process touch the host?

Release answers a different question: should we believe these bytes?

Those got collapsed. The platform treats “the agent finished” as “the artifact is true.”

That is happening for a boring reason. The harness already lives in the box. Claude Code, Codex, Harbor, a `PASS` file, a prompt that returns idle. The same disk that produced the candidate is the only witness that the candidate worked.

You did not need a kernel bug. You asked the prisoner if the trial was fair. Then you signed the pardon.

> Do not say “zero-day.” Say: this is becoming the default shape of an agent factory.

## 3. The control is green. You still lost. — 02:15–05:15

Here is the part that should bother a verifier person.

We locked the checker. `checker.py` — hash unchanged. The worker never touched it.

The checker still reads `expected.json` from the workspace. The worker wrote that file so the bug is now the spec. Empty fields are allowed. The checker prints PASS.

Independent cases, owned by the controller, still fail.

The file-integrity control you would put in the audit still passes. The release is still wrong.

A second VM does not save you. If you fork the producer to “verify,” you are verifying the crime scene. If the accept machine imports the workspace, you moved the jail and brought the witness with you.

We also ran a stupid version on purpose: the controller believes a worker `PASS` file. Same bug ships. That is not the finding. That is the smoke detector. It exists so we cannot pretend the experiment cannot see a failure.

The finding is the first one. You protected the program that judges. You did not protect what that program believes.

> Pause on hash unchanged / PASS / `1,,3` still wrong.

## 4. You can be right and still ship the wrong bytes — 05:15–06:45

Same factory. This time the comparison is honest. The worker loses on the merits.

Then it changes the file.

If publication reads the live path, verification was correct and the thing you released is not the thing you judged.

Two hashes of a mutable path are not a freeze. The path can change between them.

Freeze is an operation. Collect. Store somewhere the worker cannot write. Digest that object. Evaluate that object. Publish that object.

An approval for digest A does not authorize digest B. A used nonce does not come back because the controller restarted.

Authenticity of a statement is not identity of an artifact. SLSA already says this about provenance. Agent factories are about to relearn it with a green check.

## 5. The process never left — 06:45–08:15

Three other ways the same sentence is true. Independent checks. Not a chain.

A broad runner token reads another project. The sandbox did not steal it. We handed the identity over.

A writable bind changes the next job’s file. The mount worked. That was the bug.

An allowed upload service receives private data under another account. The network policy said this host is fine. The host was never the question. Recipient and contents were.

Every time, containment held. The grant did the work of an escape.

That is what the title means. Not a breakout. A process that stayed put and still moved a decision we cared about.

## 6. Stop taking testimony from the box — 08:15–11:00

The repair is not a thicker jail.

The producer writes a candidate. That is all it is allowed to mean.

The controller chooses the paths, copies a bounded artifact into storage the worker cannot touch, and never publishes from the live VM again.

A fresh machine runs those frozen bytes as the *subject of the test*, not as the author of the verdict. It does not get expected results. It does not get an API key that can rewrite the checker through the control plane.

The controller compares the outputs to criteria it already had.

Harness success, logs, preview URLs, worker reports: log them. They do not authorize.

Timeout, malformed output, missing evidence: no approval. That is not a defense. That is refuse to ship.

The gate names the bytes, the run, the verifier, the expected results, the policy, and a nonce. Check those fields against what you meant. A valid MAC on the wrong digest is still the wrong digest.

If someone rewrites the log and recomputes the hash chain, the copy you kept will disagree. That detects a rewrite. It does not turn a bad PASS into a good one.

> Gate enforces. History detects. Do not let them swap jobs.

## 7. The same job, after we stopped asking — 11:00–12:15

Good parser: frozen, judged, approved, published. One, comma, comma, three is REJECT.

Buggy parser: rejected. Not published.

Worker `PASS` file: ignored.

Worker `expected.json`: ignored.

Swap after freeze: denied.

The useful job still completes. That is the whole point. We did not have to choose between shipping software and having a real verdict.

## 8. Four questions — 12:15–13:20

When you go back to whatever you use — Boat, E2B, a cluster, a laptop with bubblewrap — do not start with the kernel.

Whose identity can this process use?

Which files can it change, including the next job, the snapshot, the template you will fork tomorrow?

Who can receive its output, and what is that output allowed to contain?

And the one this talk is for: **who is allowed to say these bytes are true?** If the answer is the same disk that wrote them, you do not have acceptance. You have a diary.

Name the component that can refuse, outside the worker. Then prove the legitimate job still works.

## 9. Close — 13:20–14:00

We built this path. We believed a green check meant an independent controller had accepted the artifact.

The sandbox contained the process.

It did not attest the bytes.

Containment is not attestation.

When the next agent starts a job, ask:

**Who gave this process the authority?**

> Stop. Repository on screen. Margin is silence, not another slide.

---

Spoken claim is a class, not a vendor bug. Reference factory plus synthetic lab. Deterministic scripts. Five cases prove five cases. In-sandbox grading and process-exit reward hacking are known; the sting is that file-integrity of the checker can pass and the release is still a lie. Boat, when used, is an accept-VM with `noEnv`, not the target.
