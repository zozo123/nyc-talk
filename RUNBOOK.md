# October 21 stage runbook

**Zenity AI Agent Security Summit. Pier Sixty, New York. Wednesday 21 October 2026.**

**15-minute lightning. Target delivery: 14:00.** The final stage clock is still to be confirmed. Present `slides/talk.pdf` offline. The leave-behind is `paper/paper.pdf`. Main route: slides 1-12. Slides 13-18 are for questions. Keep a second local copy of both PDFs.

Attendance is confirmed. Slides are due 9 October. Speaker dinner follows the happy hour. A logistics note to Ian, Anna, Kayla, and Neil is still awaiting reply. Do not invent a stage time on the day.

The spoken script contains 1,396 words. The timings are budgets for speech, pauses and pointing at evidence. They are not a measured human rehearsal.

| Clock | Slide | Stage action |
|---|---:|---|
| 00:00-00:35 | 1 | Dev sandbox held. CI runner green. Prod sandbox got the bug. |
| 00:35-01:30 | 2 | Read spec, harness, verifier, runner, prod. Then the line. |
| 01:30-02:20 | 3 | Two files. handler.py prints 200. The checker trusts expected.json. |
| 02:20-03:30 | 4 | Runner token 200, task token 403, this job's input still 200. |
| 03:30-04:40 | 5 | Next-job file changes, then the same write is denied. |
| 04:40-05:50 | 6 | 201 on the wrong account, then the runner's own report. |
| 05:50-07:50 | 7 | Overwrite denied. 401 becomes 200. PASS. Pause. |
| 07:50-09:05 | 8 | FAIL, PASS, REJECT, then ACCEPT on the real fix. |
| 09:05-10:25 | 9 | Denied, published, denied. In that order. |
| 10:25-11:15 | 10 | The next dev sandbox inherits the key. Say it is a consequence. |
| 11:15-12:50 | 11 | Four lines. The abuse fails. The real ticket still ships. |
| 12:50-14:00 | 12 | Who pressed promote? Leave it up. |
| 14:00-15:00 | - | Margin for transitions or the host. |

## Rehearsal

Rehearse with an audible timer. The five stations are on screen by minute one. The answer key is on screen by minute six. The promote step is on screen by minute nine. The question is up by minute thirteen.

If behind, say slide 10 in one sentence and read only the left column of slide 11. Keep the four doors, the PASS from the edited answer key, the rejection outside the dev sandbox, the fix that still ships, and the fresh-approval order. Do not read hashes aloud. The fixtures have the shape of a GitHub Actions runner and a Boat dev sandbox. State that once.

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
