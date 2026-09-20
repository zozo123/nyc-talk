# Your Agent Escaped Without Escaping the Sandbox

**Yossi Eliaz**  
Principal Engineer and Head of DevRel at Incredibuild.com

**15-minute lightning talk.** Nine main slides, three appendix. 14 minutes plus one minute of margin. Stage directions in blockquotes. Results are already on the slides. No terminal.

## 1. Cold open — 00:00–00:50

I am going to show you a merge you would have approved.

A coding agent is allowed to land a patch when CI is green. The ticket is not “parse a list.” The ticket is: **unauthenticated requests to `/admin` must return 401.**

It runs in a sandbox. The sandbox does not break.

CI is green.

I hit `/admin` with no cookie. I get **200**.

The admin door is open. The check that gates merge says PASS.

Would you have merged this?

Most of this room spent two years putting agents in boxes so this could not happen. The box worked. That was the wrong finish line.

> Advance. Let `/admin` `200` sit.

## 2. The property you bought is not the property you needed — 00:50–02:20

Isolation answers: can this process touch the host?

Release answers: should we believe these bytes enough to merge them?

Those got collapsed. The platform treats “the agent finished” as “the patch is true.”

That is happening for a boring reason. The harness already lives in the box. Claude Code, Codex, Harbor, a `PASS` file, a prompt that returns idle. The same disk that wrote the handler is the only witness that `/admin` is locked.

You did not need a kernel bug. You asked the prisoner if the vault was sealed. Then you opened the floor.

> Do not say “zero-day.” Say: this is becoming how agent CI works.

## 3. The control is green. You still lost. — 02:20–05:20

Here is the part that should bother anyone who has ever signed off a GitHub check.

We locked the checker. `checker.py` — hash unchanged. The worker never touched it.

The checker still reads `expected.json` from the workspace. The worker rewrote the spec. Unauthenticated `/admin` is now supposed to be 200. The checker prints PASS.

Independent cases, owned by the controller, still require 401. They fail.

The file-integrity control you would put in the audit still passes. **Merge is still a 200 on `/admin` with no cookie.**

You did not accept a sloppy parser. You accepted a **policy rewrite**. The agent was asked to make the tests pass. The tests *are* the security policy. Whoever controls `expected.json` controls the door.

A second VM does not save you. If you fork the producer to “verify,” you are verifying the crime scene. If the accept machine imports the workspace, you moved the jail and brought the witness with you.

We also ran a stupid version on purpose: the controller believes a worker `PASS` file. Same open admin ships. That is not the finding. That is the smoke detector.

The finding is the first one. You protected the program that judges. You did not protect what “locked down” is allowed to mean.

> Pause on: checker hash unchanged / CI PASS / `/admin` no cookie / 200.

## 4. You can be right and still ship the wrong door — 05:20–06:45

Same factory. This time the comparison is honest. Unauthenticated `/admin` fails. The worker loses on the merits.

Then it changes the file.

If publication — merge, deploy, `kubectl apply` — reads the live path, you verified a locked door and released an open one.

Two hashes of a mutable path are not a freeze. The path can change between them.

Freeze is an operation. Collect. Store somewhere the worker cannot write. Digest that object. Evaluate that object. Merge **that** object.

An approval for digest A does not authorize digest B. A used nonce does not come back because the controller restarted.

A valid GitHub check on the wrong bytes is still an open admin endpoint. Authenticity of a statement is not identity of an artifact.

## 5. The process never left — 06:45–08:15

Three other ways the same sentence is true. Independent checks. Not a chain.

A broad runner token reads another project. The sandbox did not steal it. We handed the identity over. Tomorrow that is a deploy key.

A writable bind changes the next job’s file. The mount worked. Tomorrow that is the shared cache your other agent will fork.

An allowed upload host receives private data under another account. The network policy said this hostname is fine. The hostname was never the question. Recipient and contents were. Tomorrow that is your logging endpoint.

Every time, containment held. The grant did the work of an escape.

That is the title. Not a breakout. A process that stayed put and still moved a decision you would bet production on.

## 6. Stop taking testimony from the box — 08:15–11:00

The repair is not a thicker jail.

The producer writes a candidate. That is all it is allowed to mean.

The controller chooses the paths, copies a bounded artifact into storage the worker cannot touch, and never merges from the live workspace again.

A fresh machine runs those frozen bytes as the *subject of the test*, not as the author of “`/admin` is locked.” It does not get expected results. It does not get an API key that can rewrite the checker through the control plane.

The controller compares the outputs to the policy it already had: no cookie, 401.

Harness success, logs, preview URLs, worker reports: log them. They do not authorize a merge.

Timeout, malformed output, missing evidence: no approval. That is not a defense. That is refuse to ship.

The gate names the bytes, the run, the verifier, the expected results, the policy, and a nonce. Check those fields against what you meant. A valid MAC on the wrong digest is still an open door.

If someone rewrites the log and recomputes the hash chain, the copy you kept will disagree. That detects a rewrite. It does not turn a bad PASS into a locked `/admin`.

> Gate enforces. History detects. Do not let them swap jobs.

## 7. The same ticket, after we stopped asking — 11:00–12:15

Locked handler: frozen, judged, approved, merged. `/admin` with no cookie is 401.

Open handler: rejected. Not merged.

Worker `PASS` file: ignored.

Worker `expected.json` that legalizes 200: ignored.

Swap after freeze: denied.

The ticket still closes. You can ship a locked door. You just cannot let the worker define what “locked” means.

## 8. Four questions — 12:15–13:20

When you go back to Boat, E2B, Actions, a laptop — do not start with the kernel.

Whose identity can this process use?

Which files can it change, including the snapshot you will fork tomorrow?

Who can receive its output, and what is that output allowed to contain?

And the one this talk is for: **who is allowed to say `/admin` is locked?** If the answer is the same disk that wrote the handler, you do not have acceptance. You have a diary that says the vault is fine.

Name the component that can refuse, outside the worker. Then prove a legitimate lock still merges.

## 9. Close — 13:20–14:00

We built this path. We believed a green check meant an independent controller had accepted a locked admin door.

The sandbox contained the process.

It did not attest the bytes.

Containment is not attestation.

When the next agent gets merge rights, ask:

**Who gave this process the authority?**

> Stop. Repository on screen. Margin is silence.

---

Spoken claim is a class, not a vendor bug. The payload is a synthetic `/admin` gate, not a parser quiz. Deterministic scripts. Five cases prove this policy, not that the app is secure. In-sandbox grading is known; the sting is a green checker hash and a 200 on `/admin` with no cookie. Boat, when used, is an accept-VM with `noEnv`, not the target.
