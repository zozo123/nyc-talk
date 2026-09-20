# Stage runbook - October 21, 2026

**Yossi Eliaz | 15-minute lightning slot | target 14:00 plus 1:00 margin.**
Use `slides/talk.pdf` full screen. The editable PPTX is an alternate presentation format, not a dependency. Keep a second copy of the PDF locally. Disconnect notifications. Test the projector, aspect ratio, clicker and font rendering during the venue check.

## Delivery map

| Clock | Slide | Deliver |
|---|---:|---|
| 00:00-00:25 | 1 | Title, name and the narrowly defined claim. |
| 00:25-01:20 | 2 | Unchanged checker, PASS, candidate 200, policy 401. Pause. |
| 01:20-02:15 | 3 | Worker-controlled inputs versus trusted authority. |
| 02:15-03:20 | 4 | Credential before/after and legitimate task input. |
| 03:20-04:25 | 5 | Host file changed; read-only denies; output remains usable. |
| 04:25-05:45 | 6 | Same service, wrong account; broker scopes destination and payload. |
| 05:45-07:35 | 7 | Reveal `expected.json`. Same checker, same candidate, different authority. |
| 07:35-09:05 | 8 | Freeze, run, compare, bind receipt, publish exact bytes. |
| 09:05-10:35 | 9 | Fresh-nonce substitution with the matching positive control. |
| 10:35-11:35 | 10 | More reviewers do not make shared criteria independent. |
| 11:35-13:10 | 11 | Four negative tests, each paired with useful work still succeeding. |
| 13:10-14:00 | 12 | Close on acceptance inputs and leave the repository visible. |
| 14:00-15:00 | - | Margin, transition or one question if the organizer permits. |

Slides 13-16 are appendix only. Do not read the bibliography or appendices during the lightning slot. [TALK.md](TALK.md) contains the complete spoken manuscript. Timing is a rehearsal target, not a measured human delivery time.

## Evidence and demo policy

The PDF contains recorded results. Say "in this recorded fixture" rather than pretending to type a live command. The credential and allowed-endpoint cases use actual loopback HTTP; the `/admin` case prints modeled status codes. Do not call it a live web breach.

No API keys, customer data, cloud boot, model response or venue Wi-Fi are needed. `evidence/` contains the underlying records. Optional `build/replay.html` is visibly labeled recorded evidence, not a live execution; use only if already rehearsed. A failed live reproduction is not evidence of a successful defense.

Before freezing a distribution, run `make test`, `make record` on suitable Linux, `make author`, `make snapshot`, and visually inspect every PDF page. Keep the source archive and its SHA256 manifest alongside the PDF. The source-hash check detects accidental mismatch, not a malicious maintainer rewriting both code and evidence.

## Overrun recovery

At minute 5:45 you should be revealing `expected.json`. If late, shorten the mount and endpoint explanation to their observed before/after and positive control; retain all four cases. If still late at minute 10:35, say the multiagent implication in one sentence and advance. Never cut the unchanged-checker reveal, the fresh-nonce positive control or the final acceptance question.

## Hard questions

Use appendix 13 for scope, 14 for the earlier in-process gate defect, 15 for reproduction, 16 for prior work. There is no vendor zero-day or measured model attack rate. Five admin cases check one small policy. Controller compromise is outside this experiment's trust model. The phrase "DEF CON level" is a quality goal, not an affiliation, acceptance or certification.
