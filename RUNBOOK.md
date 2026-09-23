# October 21 stage runbook

**Zenity AI Agent Security Summit. Pier Sixty, New York. Wednesday 21 October 2026.**

**15-minute lightning. Target delivery: 14:00.** The final stage clock is still to be confirmed. Present `slides/talk.pdf` offline. The leave-behind is `paper/paper.pdf`. Main route: slides 1-12. Slides 13-18 are for questions. Keep a second local copy of both PDFs.

Do not invent a stage time on the day. Private logistics are kept in `research/private/`, which is not published.

The spoken script contains 1,405 words. The timings are budgets for speech, pauses and pointing at evidence. They are not a measured human rehearsal.

| Clock | Slide | Stage action |
|---|---:|---|
| 00:00-01:15 | 1 | FAIL, then PASS. Ask what changed. |
| 01:15-02:00 | 2 | No login must be 401. The program prints 200, so it is wrong on three cases. Its bytes never change. |
| 02:00-03:00 | 3 | Honest answer key, FAIL. Overwrite DENIED. Same hash. Same launch, PASS. Pause. |
| 03:00-04:30 | 4 | Read across the row: same program, same checker, new answer key, PASS. The worker did not change the checker. |
| 04:30-05:30 | 5 | Say what each hash rules out. Then the trap: a hash does not say who wrote it. |
| 05:30-07:00 | 6 | Point at the load. The worker's write permission included the criteria. |
| 07:00-08:00 | 7 | Say REJECT first. Then: who owns the answers. The failing checker was sandboxed too. |
| 08:00-08:45 | 8 | The corrected program is ACCEPTED. |
| 08:45-10:15 | 9 | Unused approval: denied, denied, published, denied. All four are correct. |
| 10:15-11:45 | 10 | Three questions. Then the inventory, the candidate out of process, the tripwire. |
| 11:45-13:15 | 11 | Isolation and acceptance are different boundaries. Name the title's escape: it escaped the check. End on the last-writer rule. |
| 13:15-14:00 | 12 | Repository first. Then “Not the program. Not the checker. The answer key.” Thank you. Leave PASS up. |
| 14:00-15:00 | - | Margin for transitions or the host. |

## Rehearsal

Rehearse with an audible timer. FAIL and PASS are up in the first minute. The hash row is on screen by minute four. The unused approval is on screen by minute nine. The title payoff is up by minute twelve.

No slide is budgeted above about 116 spoken words per minute, and the build refuses any slide above 150. The spare seconds are deliberate: the beat after “It prints PASS and exits 0” on slide 3, the silence while the room reads the row on slide 4, the beat after REJECT on slide 7, a breath after each of the three questions on slide 10, and the pauses between the three short lines near the end of slide 12. Do not pad to fill the clock and do not speed up the close.

Say “admin none”, not “admin colon none”. Read the two answer-key landmarks on slide 4 digit by digit and pick one reading for 0. Point at the Answer key column as you say them. The printed script says “for the rest of this talk” rather than a minute count, because the stage clock is still unconfirmed.

If behind, keep slides 4, 7, 8, 9, 11, and 12. Say the token, mount, and host only if asked. Do not read full hashes aloud. The prefixes on the slide are enough. The payload is a command-line fixture and the worker is a script. Slide 1 states it once.

## Evidence on stage

The slide outputs summarize recorded executions. Do not present them as a live session. The centerpiece uses a CLI status-code model. The supporting credential and upload cases use loopback HTTP. The archived API audit belongs in Q&A and requires controller-object access.

The talk claims a controlled reproduction of a known mechanism. Do not improvise a customer incident, vendor flaw or model attack-success rate. Five policy cases establish their tested behavior only.

## Local preparation

```sh
make test
make evidence
make snapshot
```

After changing experiment source, first run `make record-all` on disposable Linux with bubblewrap. Ubuntu 24.04 restricts unprivileged user namespaces, and bubblewrap then fails while bringing up a network namespace. On that release:

```sh
sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0
```

The current records come from a privileged Ubuntu 22.04 container on kernel 6.8.0-64, where that sysctl is not needed; on a stock Ubuntu 24.04 host it is. Inspect the compiled PDF and keep it offline. `make replay` is an optional explicitly labeled recording. No cloud login or live terminal is part of the delivery.

## Organizer and AV

Use the accepted title. The 15-minute duration comes from the session brief. Exact stage time and AV arrangements still require organizer confirmation. This package does not imply that logistical confirmation has happened.
