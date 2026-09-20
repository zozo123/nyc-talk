# October 21 stage runbook

## Stage master

Open `slides/talk.pdf` full-screen. Present slides **1-12 only**. Slides 13-18 are Q&A. Editable `slides/talk.pptx` contains presenter notes and source blocks. Beamer and PowerPoint share the narrative and layout source in `slides/deck.json`.

Bring local copies on the laptop and a USB drive. Disable notifications, sleep and automatic updates. Test the venue display ratio and contrast. The PDF requires no Wi-Fi, login or video codec.

## Timing

| Clock | Slides | Beat |
|---|---|---|
| 00:00-01:20 | 1-2 | Result first, then precise threat model |
| 01:20-05:00 | 3-5 | Credential, mount, allowed endpoint; preserve positive controls |
| 05:00-07:40 | 6-7 | Ask who owns expectations, pause, reveal unchanged-checker PASS |
| 07:40-08:40 | 8 | Shared rulebook in a multi-agent system; clearly an inference |
| 08:40-11:30 | 9-10 | Freeze/judge/gate, fresh swap, legitimate publication, replay |
| 11:30-14:00 | 11-12 | Four deployment questions and close |
| 14:00-15:00 | - | Margin; do not add new material |

The manuscript has 1,614 words. At about 130 words/minute plus 90 seconds of pauses and slide handling it approaches 14 minutes. Do a timed human rehearsal; this arithmetic does not confirm delivery duration.

## Exact reveal

At slide 6, ask **"Who controls expected.json?"** Wait three seconds. Advance once. On slide 7 read **PASS**, then **200**, then **required 401**. Say the checker faithfully used the altered expectations. Keep the CLI-policy-model label visible; do not pretend to curl a production service.

## Cut plan

At 05:00, be on slide 6. If behind, give slide 8 one sentence: "Several reviewers can all trust the same worker-writable expectations." On slide 9 omit the approval-field enumeration. Preserve the slide-10 fresh-swap order, all four controls and the closing question. Do not shorten by omitting limitations that change the interpretation of the result.

## Backup demo

Open `demo/replay.html` locally and use arrow keys. It is visibly labeled recorded evidence and makes no network calls. Or use `python3 tools/replay.py verifier`. Never present playback as a live attack. Do not execute arbitrary audience-supplied code through the local factory executor.

## Reproduction and final checks

On disposable Linux, run `make record`, `make record-factory`, `make verify`, then `make snapshot`. CI retains the exact source archive, commit, fresh evidence and rendered deck. A namespace-creation failure is an infrastructure failure, not a passing containment test.

Before delivery, confirm the organizer's precise slot and AV instructions. This repository plans a 15-minute slot; no new organizer correspondence was sent during finalization.
