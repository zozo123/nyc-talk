# October 21 stage runbook

**Zenity AI Agent Security Summit. Pier Sixty, New York. Wednesday 21 October 2026.**

**15-minute lightning. Target delivery: 14:00.** The final stage clock is still to be confirmed. Present `slides/talk.pdf` offline. The leave-behind is `paper/paper.pdf`. Main route: slides 1-12. Slides 13-18 are for questions. Keep a second local copy of both PDFs.

Attendance is confirmed. Slides are due 9 October. Speaker dinner follows the happy hour. A logistics note to Ian, Anna, Kayla, and Neil is still awaiting reply. Do not invent a stage time on the day.

The spoken script contains 1,200 words. The timings are budgets for speech, pauses and pointing at evidence. They are not a measured human rehearsal.

| Clock | Slide | Stage action |
|---|---:|---|
| 00:00-01:00 | 1 | FAIL, then PASS. Ask what changed. |
| 01:00-02:30 | 2 | No login must be 401. The program prints 200. |
| 02:30-04:00 | 3 | Checker write denied. It reads expected.json. |
| 04:00-06:00 | 4 | Same program, same checker, new answer file, PASS. |
| 06:00-07:00 | 5 | Say what each hash rules out. |
| 07:00-08:00 | 6 | The workspace write included the acceptance criteria. |
| 08:00-09:15 | 7 | Controller-owned cases reject the same program. |
| 09:15-10:30 | 8 | The corrected program is accepted. |
| 10:30-12:00 | 9 | Unused approval: denied, published, denied. |
| 12:00-13:15 | 10 | Three questions for another system. |
| 13:15-13:40 | 11 | Read the next experiment. Label it unfinished. |
| 13:40-14:00 | 12 | PASS beside the unchanged program. Stop. |
| 14:00-15:00 | - | Margin for transitions or the host. |

## Rehearsal

Rehearse with an audible timer. FAIL and PASS are up in the first minute. The hash row is on screen by minute five. The unused approval is on screen by minute eleven. The next-experiment question is up by minute thirteen.

If behind, keep slides 4, 7, 8, and 9. Say the token, mount, and host only if asked. Do not read full hashes aloud. The prefixes on the slide are enough. The payload is a CLI fixture and the worker is a script. State that once.

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

The recorded run used that setting on kernel 6.8.0-117. Inspect the compiled PDF and keep it offline. `make replay` is an optional explicitly labeled recording. No cloud login or live terminal is part of the delivery.

## Organizer and AV

Use the accepted title. The 15-minute duration comes from the session brief. Exact stage time and AV arrangements still require organizer confirmation. This package does not imply that logistical confirmation has happened.
