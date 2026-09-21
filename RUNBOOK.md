# October 21 stage runbook

**Zenity AI Agent Security Summit. Pier Sixty, New York. Wednesday 21 October 2026.**

**15-minute lightning. Target delivery: 14:00.** The final stage clock is still to be confirmed. Present `slides/talk.pdf` offline. The leave-behind is `paper/paper.pdf`. Main route: slides 1-12. Slides 13-18 are for questions. Keep a second local copy of both PDFs.

Attendance is confirmed. Slides are due 9 October. Speaker dinner follows the happy hour. A logistics note to Ian, Anna, Kayla, and Neil is still awaiting reply. Do not invent a stage time on the day.

The spoken script contains 1,200 words. The timings are budgets for speech, pauses and pointing at evidence. They are not a measured human rehearsal.

| Clock | Slide | Stage action |
|---|---:|---|
| 00:00-00:40 | 1 | The agent changes the answers. The check goes green. |
| 00:40-01:40 | 2 | Workflow on the default branch. Answers in the checkout. |
| 01:40-02:50 | 3 | No login must be 401. This program prints 200. |
| 02:50-04:30 | 4 | Honest file FAIL. Edited file PASS. Pause. |
| 04:30-06:10 | 5 | FAIL, PASS, REJECT, ACCEPT. |
| 06:10-07:40 | 6 | Denied, published, denied. |
| 07:40-09:20 | 7 | Token, disk, host. One result each. |
| 09:20-10:20 | 8 | The next run keeps the answer file. |
| 10:20-11:30 | 9 | Answers move to the runner. Code stays in the checkout. |
| 11:30-12:40 | 10 | Four rows. Refuse, and still allow. |
| 12:40-13:20 | 11 | Compare, then approve. |
| 13:20-14:00 | 12 | Who merged it? Leave it up. |
| 14:00-15:00 | - | Margin for transitions or the host. |

## Rehearsal

Rehearse with an audible timer. The sentence is up in the first minute. The answer file is on screen by minute three. The merge order is on screen by minute seven. The question is up by minute thirteen.

If behind, read slide 7 as the table only and slide 8 in one sentence. Keep the edited-file PASS, the runner REJECT, the real fix ACCEPT, and denied, published, denied. Do not read hashes aloud. The fixtures have the shape of a GitHub Actions job and were recorded on a Boat Ubuntu machine. State that once.

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
