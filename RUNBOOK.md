# October 21 stage runbook

**15-minute slot. Target delivery: 14:00.** Present `slides/talk.pdf` offline. Main route: slides 1-12. Slides 13-18 are for questions. Keep a second local copy.

The spoken script contains 1,307 words. The timings are budgets for speech, pauses and pointing at evidence. They are not a measured human rehearsal.

| Clock | Slide | Stage action |
|---|---:|---|
| 00:00-00:30 | 1 | Ask whether a protected checker's PASS is enough to release. |
| 00:30-01:20 | 2 | Show PASS beside the policy-violating 200. Pause. |
| 01:20-02:15 | 3 | State worker control and trusted components. |
| 02:15-03:10 | 4 | Honest key yields FAIL. Direct checker write is denied. |
| 03:10-04:45 | 5 | Reveal the workspace answer key. Same checker now passes. |
| 04:45-06:15 | 6 | Walk the paired comparison. Bad bytes rejected; valid fix accepted. |
| 06:15-07:40 | 7 | Follow frozen bytes and observations across the trust boundary. |
| 07:40-09:00 | 8 | Fresh substitution denied, original published, replay denied. |
| 09:00-10:00 | 9 | Explain shared criteria across agents and snapshots as an inference. |
| 10:00-12:00 | 10 | Give the four deployment checks and their positive controls. |
| 12:00-13:00 | 11 | Distinguish verification, the gate and protected history. |
| 13:00-14:00 | 12 | Close on who controls release eligibility. Leave the slide visible. |
| 14:00-15:00 | - | Margin for transitions or the host. |

## Rehearsal

Rehearse with an audible timer. Reach the answer-key reveal by minute four, the gate controls by minute eight, and the close by minute thirteen. The paired comparison and release controls are the story.

If behind, shorten slide 9 to one sentence and slide 10 to the table's four rows. Preserve the answer-key mechanism, independent rejection, legitimate success and fresh-approval substitution test. Do not read hashes or source URLs aloud.

## Evidence on stage

The slide outputs summarize recorded executions. Do not present them as a live session. The centerpiece uses a CLI status-code model. The supporting credential and upload cases use loopback HTTP. The archived API audit belongs in Q&A and requires controller-object access.

The talk claims a controlled reproduction of a known mechanism. Do not improvise a customer incident, vendor flaw or model attack-success rate. Five policy cases establish their tested behavior only.

## Local preparation

```sh
make test
make evidence
make snapshot
```

After changing experiment source, first run `make record-all` on disposable Linux with bubblewrap. Inspect the compiled PDF and keep it offline. `make replay` is an optional explicitly labeled recording. No cloud login or live terminal is part of the delivery.

## Organizer and AV

Use the accepted title. The 15-minute duration comes from the session brief. Exact stage time and AV arrangements still require organizer confirmation. This package does not imply that logistical confirmation has happened.
