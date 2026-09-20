# Your Agent Escaped Without Escaping the Sandbox

**Yossi Eliaz**  
Principal Engineer and Head of DevRel at Incredibuild.com

AI Agent Security Summit · Pier Sixty · NYC · October 21, 2026

**15 minutes.** Nine main slides. 14 plus a minute of air. This is the Sessionize talk. One idea, four doors, four locks.

## 1. Title — 00:00–00:35

Hi. I’m Yossi.

Read the title again.

Your agent escaped **without escaping** the sandbox.

Every namespace and cgroup can work exactly as designed. And you can still have a real breach.

That first sentence of the abstract is not poetry. It is the demo.

The agent never climbed the wall. We cut four doors in the wall so it could do the job. It used the doors.

> Let that land. Advance.

## 2. The wall is not the interesting part — 00:35–01:30

We spent two years on the wall. MicroVMs, gVisor, namespaces, pretty dashboards that say Isolated.

Good. Keep the wall.

Here is what is new about agents, and why this talk is not last decade’s least-privilege rant:

A classical sandbox assumes the workload might *try to leave*.

An agent is hired to *finish a ticket*. It will use every interface you called “part of the job.” Token. Files. The one allowed host. The signal that means done.

Those four interfaces are in the abstract on purpose. They are not four random bugs. They are **the four doors a working agent actually needs**.

You cannot weld them shut. Then it cannot work.

So the question is not “did it escape.” The question is: **which layer can refuse a door when the process is still inside, still being helpful, still trying to complete.**

Four doors. Four locks. Four things you check on your own deployment. That’s the whole talk.

## 3. Door 1 — inherited credentials — 01:30–03:20

The job needs to read its input. CI already had a runner token. We copied it. Fast. Done.

The worker asks another project for a private fixture. **200.** Valid badge. Huge scope.

Nobody escaped. We hung dad’s badge on the intern because the intern had a job.

Lock, from the abstract: **short-lived credential projection**. Not “copy the runner secret and hope.” Mint: this task, this audience, this hour. Same request: **403**. Its own input: still **200**.

A token that dies at midnight is still a skeleton key at 9 a.m. Scope is the lock. Expiry is the courtesy.

> 200. 403. The job still runs. Next door.

## 4. Door 2 — dangerous mounts — 03:20–05:00

The job needs files. We bind a shared folder. Writable. The next job might need it. We are being helpful.

The worker writes a perfectly legal write. On the host, the next job’s file has changed.

The mount did what mounts do. That is the breach.

Lock: **capability-scoped filesystems**. Not “a sandbox has a disk.” You may read *this* input. You may write *that* output. The next job’s chair is not in the room. Same write: denied. Host unchanged. Its own `/output`: still works.

If tomorrow’s agent will fork this snapshot, tomorrow is already in the room.

## 5. Door 3 — exfiltration through an allowed endpoint — 05:00–07:00

The job has to publish a report. So we allow the report host. The firewall loves this hostname. Green.

The worker posts our private fixture to **another account on that same host**. Same door. Different mailbox. The bytes are there. We looked.

The wall never failed. The **allowed endpoint** was the exit.

Lock: **real process isolation** — the worker cannot dial the mailroom. And the postcard is not worker-authored. An outside broker builds one boring, allowed report. Extra fields: no. Direct route: gone. The real report still arrives.

If your agent can mail a postcard, it can mail it to the wrong address. Isolation is who can walk to the box. Policy is who may write on the envelope.

## 6. Door 4 — verifier tampering — 07:00–09:45

This is the door labeled **done**.

Ticket: unauthenticated `/admin` returns 401. Green CI means merge.

We lock the checker. Hash unchanged. Audit will love us.

The checker still reads `expected.json` from the workspace. The worker rewrites the spec so no-cookie `/admin` is *supposed* to be 200. Checker prints PASS.

I curl `/admin` with no cookie. **200**.

The agent did not break the sandbox. It used the success interface. You hired it to get to done. **Done is a door.**

That is why verifier tampering belongs in this abstract, and why it is not “the intern overwrote `test.sh`.” You protected the referee. The player wrote the rulebook. File integrity is green. The admin door is open. You would have merged this.

A second box that still reads that folder is not a new referee. It’s the same kid in a new hoodie.

We also ran the dumb version on purpose: controller believes a worker `PASS` file. Same 200. That’s the smoke detector, so nobody says the experiment is blind.

> Groan is good. Stay with 401 required / 200 shipped.

## 7. Four locks, at the layer that can actually say no — 09:45–11:45

The abstract promised we close each door where enforcement is real. Not inside the agent’s feelings. Outside the worker.

**Short-lived credential projection.** Tiny badge. This ticket.

**Capability-scoped filesystems.** This input. That output.

**Real process isolation.** It cannot reach the extra mailbox. The broker can.

**Tamper-evident execution history.** Keep a copy of what happened that the worker cannot rewrite. If the diary changes, you see it.

One grown-up next to that last lock, because a perfect diary can still say “the vault is fine.” History detects a rewrite. It does not make `/admin` a 401. Freeze the bytes. Grade them off the worker. Merge **those** bytes. Timeouts are not a win. That’s just “we didn’t ship.”

Locked `/admin` still merges. Open `/admin` does not. Fake rulebook ignored. Swap after freeze: no.

The agent can still do the job. It just cannot pick the lock by finishing.

## 8. Four boundaries for your deployment — 11:45–13:20

You leave with four boundaries. They are the four doors. Check them against *your* agent, not my lab.

Whose **identity** can it use?

Which **files** can it change — including the snapshot you will fork tomorrow?

Which **endpoint** may it call, and what is allowed to be in the body?

Who is allowed to say **these bytes are done**?

If “done” is a file the worker can write, or a spec it can edit, or a harness that lives on the same disk, you do not have a verifier. You have a very motivated intern grading their own homework.

Name the component that can refuse, **outside** the worker. Then prove the real ticket still completes. That’s how you know you locked a door instead of bricking the house.

## 9. Close — 13:20–14:00

The sandbox did its job.

The agent did its job too. It used the doors we installed so it could finish.

That is an escape without escaping.

When the next agent starts a ticket, don’t ask if the wall is pretty. Ask:

**Who gave this process the authority?**

Repo is on the slide. Four doors. Four locks. Go try them on your own box.

> Stop. Smile. No “in conclusion.”

---

The four doors and four locks are the accepted abstract. Recorded lab plus factory. Synthetic `/admin`, not a vendor CVE. Agents-are-goal-obsessed is the 2026 reason the doors matter; it is not a model-ASR claim.
