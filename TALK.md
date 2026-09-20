# Your Agent Escaped Without Escaping the Sandbox

**Yossi Eliaz**  
Principal Engineer and Head of DevRel at Incredibuild.com

**15-minute lightning talk.** Nine main slides, three appendix slides. Target 14 minutes, one minute of margin. Blockquotes are stage directions. Recorded results are on the slides. Keep the terminal closed.

## 1. The question — 00:00–00:40

You give an agent a small job: fix a parser, publish the report.

It has a sandbox. The sandbox does not break.

A little later, the check is green.

Would you ship it?

The title does not mean a VM escape. It means the agent exceeded the task **through interfaces we granted**, and we treated that as success.

The question that matters:

**What made this work eligible for release — and how much of that decision could the agent influence?**

> Advance.

## 2. The factory — 00:40–02:00

Here is the path we actually built.

The **dev VM** is untrusted. Files, harness, tests, reports.

The **controller collects**. It chooses the paths. It stores a bounded artifact in storage the worker cannot write. It hashes a manifest. After that, the live VM is not a publication source.

A **fresh accept VM** runs those frozen bytes as untrusted code under test. It does not hold the expected results. It does not get an API key that can rewrite the checker.

The **controller compares** the outputs to criteria it owns.

A **gate** binds the digest, the run, the verifier bundle, the expected results, the policy and a nonce. Publication reads **that** frozen object.

Two invariants. Acceptance integrity: the worker cannot force us to accept bytes that fail our criteria. Release integrity: we only publish the digest we approved.

Five cases prove those five cases. They do not prove the parser is correct for every input.

> Do not call a second VM “independence.” Judgment still has to live off worker-controlled inputs.

## 3. The miss — 02:00–05:00

We protected the checker file. Its hash did not change.

The buggy parser still got PASS.

The checker reads `expected.json` from the working directory. The worker wrote that file. The expected results now match the bug: empty fields are allowed.

The executable we “protected” still took its truth from the worker.

> Pause on: checker hash unchanged, verdict PASS, independent cases fail.

A second VM does not save you if the comparison still imports worker state.

That is the finding. Not a kernel escape. Not a model jailbreak. The controller trusted worker-shaped evidence.

We also ran a detector: if the controller simply believes a worker `PASS` file, the same buggy parser ships. That variant is **deliberate**. It proves the experiment can see a failure. It is not a surprise.

## 4. The other swap — 05:00–06:30

Same factory. This time the comparison is honest. The worker changes the file after we look.

If we publish from the live path, verification was correct and we still released something else.

Hashing the path before and after is not enough. The path can change between the two observations.

Freeze is an operation: collect, store, digest, evaluate **that object**, publish **that object**.

An approval for digest A does not authorize digest B. A used nonce does not come back after a controller restart.

## 5. Three surrounding grants — 06:30–08:30

The acceptance path is the spine. The abstract promised three other non-escape escapes. They are independent synthetic checks, not one exploit chain.

**Identity.** A broad runner token reads another project. A task-scoped token gets 403. Task input still works.

**Files.** A writable bind changes another job’s host fixture. Read-only blocks the write. Task output stays writable.

**Release.** The same allowed upload service receives synthetic private data under another account. A broker that fixes recipient and body, with no direct route, sends only the permitted report.

Each time the namespace held. The grant did the damage.

> One slide, three rows. Do not rebuild the parser mystery here.

## 6. Repair — 08:30–11:00

Move every input to the decision off the worker.

Expected results live on the controller. The accept VM only runs frozen candidate bytes. No in-sandbox key on that VM that can change the checker through the control plane.

Harness success, logs, preview URLs, worker reports: logged, never an approval.

Timeout, malformed output, missing evidence: **no approval**. That is not a successful defense. That is refuse-to-ship.

The authenticated decision names the artifact, the run, the verifier bundle **and its launch config**, the expected-results digest, the policy, the accept-environment manifest, the decision and a nonce. An authentic statement can still name the wrong artifact. Check identity, not only the MAC.

History: if someone rewrites the log and recomputes the chain, the controller’s retained head disagrees. That **detects** a rewrite. It does not make a bad acceptance good.

> Gate enforces. History detects. Different jobs.

## 7. Same job, restricted path — 11:00–12:20

Good parser: frozen, judged, approved, published. `1,,3` is REJECT.

Buggy parser: rejected. Not published.

Worker PASS file: ignored.

Worker `expected.json`: ignored.

Swap after freeze: denied.

The useful job completes.

## 8. Four questions — 12:20–13:20

When you go back to your agent host, write down four answers.

Whose identity can the worker use?

Which files can it read or change — including the next job’s disk, snapshots and templates?

Who can receive its output, and what can that output contain?

Who can approve **these bytes** — and does that decision depend on imports, expected results, collection path or a harness green check?

Name the component that can refuse the unwanted action **outside** the worker. Then test that the legitimate operation still works.

## 9. Closing — 13:20–14:00

We built this workflow. We believed a green check meant the controller had independently accepted the artifact.

The sandbox held. The decision still depended on the worker.

The repair is not a stronger jail. It is moving judgment, expected results and publication onto objects the worker cannot write.

When your next agent starts a job, ask:

**Who gave this process the authority?**

> Stop. Leave the repository URL visible. The remaining minute is margin.

---

This is a reference factory plus an educational Linux lab. Deterministic scripts, synthetic data, finite cases. Not a named-product zero-day, not a customer incident, not a model success-rate. Prior art: process-exit reward hacking and in-sandbox graders are known; the claim here is that **our** acceptance path still trusted worker-controlled inputs after we “protected the checker.” Boat, when used, is an accept-VM substrate with `noEnv`, not the vulnerability.
