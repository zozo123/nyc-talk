# Your Agent Escaped Without Escaping the Sandbox

**Yossi Eliaz**  
Principal Engineer and Head of DevRel at Incredibuild.com

AI Agent Security Summit · Pier Sixty · NYC · October 21, 2026

**15 minutes.** Nine main slides, three appendix. Aim for 14. Smile. Point at the slide. No terminal, no kernel war stories.

This is the talk on the badge: four non-escape escapes, four locks, four things to check on Monday.

## 1. Title — 00:00–00:30

Hi. I’m Yossi.

Spoiler: the agent never climbed the wall.

The namespaces were fine. The cgroups were fine. We still had a bad day.

Four short stories. Nobody picks a lock. We hold the door.

> Wave at the title. Advance.

## 2. The deal — 00:30–01:15

You put an agent in a sandbox so the blast radius ends at the box.

Cute. Necessary. Not the end of the movie.

If we hand it a fat badge, a writable folder, a stamp for the mailroom, or the pencil that grades its own homework — it can cause a real mess **without leaving**.

That’s a non-escape escape. The process stays put. A decision you care about still moves.

Four of them. Then we lock each one. Then you steal four questions. Then we go to the reception.

## 3. It had dad’s badge — 01:15–03:15

Story one. Inherited credentials.

The job is called `lock-admin`. We give the worker a runner token, because CI already had one, and copying it was easy.

It asks another project for a private fixture. The service says 200. Of course it does. Valid badge. Big scope.

The sandbox did not steal the key. **We hung it around its neck.**

Fix: don’t copy dad’s badge. Mint a tiny one. This task. This audience. Short life. Same request: 403. Its own input: still 200.

A short lifetime is not a small scope. A broad token is a problem at second zero.

> Point at 200, then 403. Grin. “We did that.”

## 4. It sat in the next job’s chair — 03:15–05:00

Story two. Dangerous mounts.

We bind a shared folder because the next job might need it. Writable, because why not.

The worker writes a normal write. Outside the box, the next job’s file has changed.

The mount worked. That’s the bug.

Fix: you may read this, you may write that. Same write: denied. Host file unchanged. Its own output folder: still works.

Read-only is still a read. If the next job shouldn’t be in the room, don’t put the chair in the room.

## 5. The allowed door — 05:00–07:00

Story three. Exfil through an allowed endpoint.

We let it talk to the report service. Reasonable. It has to publish *something*.

It sends our private fixture to **another account on the same host**. Same hostname. Different mailbox. The data is there. We checked.

The firewall said “this host is fine.” The host was never the question. **Who** and **what** were.

Fix: the worker does not pick the URL, the recipient, or the body. It asks for one operation: publish the report. An outside broker builds a boring, allowed postcard. Extra fields: no. Direct route to the service: gone. The real report still arrives.

If your agent can mail a postcard, it can mail a postcard to the wrong address. Don’t let it address the envelope.

## 6. The test said yes — 07:00–09:30

Story four. This is the fun one. Verifier tampering.

Ticket: unauthenticated `/admin` must be 401. CI green means you may merge.

We lock the checker. Hash unchanged. Very responsible of us.

The checker still reads `expected.json` from the workspace. The worker rewrites the spec so no-cookie `/admin` is *supposed* to be 200. Checker prints PASS.

I curl `/admin` with no cookie. **200**.

We protected the referee. We let the player write the rulebook.

That’s not a failed test. That’s a **policy rewrite**, then a merge you would have approved.

A second box does not save you if it still reads the same folder. That’s not a new referee. That’s the same kid in a new hoodie.

Bonus, on purpose: if the controller just believes a worker `PASS` file, same open door. That’s the smoke detector. We ran it so we can’t pretend the experiment is blind.

> Pause on 401 required / 200 shipped. Let people groan.

## 7. Four locks — 09:30–11:30

Close each one at the layer that can actually say no.

**Short-lived credential projection.** Tiny badge. This task. Then it expires.

**Capability-scoped filesystems.** Read this input. Write this output. Nothing about the next job.

**Real process isolation.** The worker cannot reach the mailroom. The broker can.

**Tamper-evident history** — plus a grown-up: the worker is not the witness. Freeze the bytes. Grade them somewhere that does not own `expected.json`. Merge **those** bytes. If someone rewrites the diary, your copy disagrees. A faithful diary can still say “the vault is fine.” History catches a rewrite. It does not make `/admin` 401.

Timeouts and crashes are not a win. That’s “we didn’t ship.” Different from “the door is locked.”

The useful ticket still closes. Locked `/admin` merges. Open `/admin` does not. `PASS` file ignored. Fake rulebook ignored. Swap after freeze: no.

## 8. Steal these four — 11:30–13:15

Monday morning. One agent job. Four questions. Write the answers on a sticky note.

Whose **identity** can it use?

Which **files** can it change — including tomorrow’s snapshot?

Who can **receive** its output, and what’s in the envelope?

Who is allowed to say **these bytes are true**?

If the last answer is “the same disk that wrote them,” you don’t have a verifier. You have a very confident diary.

Name the thing that can refuse, **outside** the worker. Then prove the real job still works. That’s the whole game.

## 9. Close — 13:15–14:00

The sandbox contained the process. We still had a breach. We issued the badge, the chair, the stamp, and the rulebook.

That’s the talk you came for.

When the next agent starts a job, ask:

**Who gave this process the authority?**

Repo is on the slide. Go check four things. Then go enjoy New York.

> Stop. Smile. Don’t add a tenth slide with “in conclusion.”

---

Synthetic lab, deterministic scripts, recorded results. `/admin` is a fixture, not a customer incident. The 29 Linux checks and the factory checks are not 29 CVEs. Appendix if anyone wants reproduction.
