# Your Agent Escaped Without Escaping the Sandbox

**Yossi Eliaz, PhD**

Principal Engineer and Head of DevRel at Incredibuild.com

**AI Agent Security Summit / New York / October 21, 2026 / 15 minutes**

[Final deck (PDF)](slides/talk.pdf) · [Paper (PDF)](paper/paper.pdf) · [LaTeX source](slides/talk.tex) · [Spoken script](TALK.md) · [Speaker notes](SPEAKER_NOTES.md) · [Stage runbook](RUNBOOK.md) · [Offline replay](demo/replay.html)

## The story

**One line.** What changed when the test went green? The worker changed what counted as correct.

The accepted abstract is four failures on that factory: an inherited runner token, a dangerous mount in the dev sandbox, a publish through a host the runner already allows, and a green check whose answer key the harness can edit. The checker reports **PASS**. Unauthenticated admin still returns **200**, where policy requires **401**. The checker and the candidate have the same bytes as before.

The worker changed the answer key.

The central experiment keeps the bad candidate fixed, denies a write to the read-only checker, and lets the worker edit `expected.json`. The unchanged checker changes from FAIL to PASS. Controller-owned criteria reject those same bad bytes. A corrected handler passes. The release gate then denies substituted bytes under a fresh approval, publishes the original bytes, and rejects replay.

The question for the audience: **Who pressed promote?**

This is a controlled reproduction of a known trust-boundary failure, with a repair and positive controls. The centerpiece is a five-case **CLI status-code model**, not a deployed HTTP application, an LLM trial or a vendor zero-day. Publication is an exact-byte record in a controller-owned local database.

## Final stage package

- **12 main slides + 6 Q&A appendices.** One central experiment occupies the main story.
- **1,200 spoken words.** A 14-minute delivery budget leaves one minute of margin. Rehearse aloud to verify your own pace.
- **LaTeX only.** `slides/talk.tex` is the editable source for the PDF, manuscript and speaker notes.
- **Offline presentation.** Recorded observations are on the slides. No live terminal, cloud key or conference network is required.
- The four abstract categories remain the deployment checklist: identity, files, outbound operations and acceptance. Supporting experiments are independent cases, not an attack chain.

The latest standalone LaTeX draft has been consolidated into the canonical source. `slides/latex-only/finish-line.tex` forwards to it for compatibility. Earlier JSON/PowerPoint generators and snapshots remain available in git history.

## Build and reproduce

Python 3.10+ standard library and TeX Live for the deck. Ubuntu packages: `texlive-latex-recommended texlive-pictures lmodern`. The isolated experiments also require bubblewrap on disposable Linux.

```sh
make deck              # validate evidence, export notes, compile build/talk.pdf
make paper             # compile the leave-behind paper
make final             # snapshot the deck, then the paper
make snapshot          # update slides/talk.pdf and the offline replay
make test              # 37 controller / evidence regression tests
make factory           # six local fixture checks; NO OS isolation
make demo              # 29 Linux isolation / loopback HTTP checks
make factory-isolated  # 11 checker / release checks with real read-only mounts
make record-all        # refresh source-bound evidence after experiment changes
make replay            # replay recorded observations; no new experiment
```

The evidence in this tree was reproduced on 21 September 2026 on Ubuntu 24.04 x86_64 (kernel 6.8.0-117, Python 3.12.3). That run passed 37 regressions, 29 isolation-lab checks, 11 isolated-checker checks, and 6 local factory checks. `slides/talk.pdf` is the build from that machine.

Edit the LaTeX, then run `make snapshot`. Do not independently edit generated `TALK.md` or `SPEAKER_NOTES.md`. The deck build rejects stale, missing or skipped evidence, checks slide notes and timing, and rejects overfull TeX layouts. It never provisions cloud resources. CI reproduces the Linux fixtures and builds the same LaTeX package.

The local factory executor runs only the committed synthetic fixtures. It is not an arbitrary-code sandbox.

## Evidence and limits

[Research dossier](research/DOSSIER.md) · [Evidence ledger](research/RESULTS.md) · [Original gate audit](research/AUDIT.md) · [Technical questions](QUESTIONS.md)

The 29 lab, 11 isolated-checker and 6 local-factory assertions describe coverage, **not vulnerability counts**. The 37 regression tests are separate. The source-bound records support the read-only checker result, independent rejection, legitimate acceptance and exact-byte local publication.

The archived gate audit demonstrates an internal API integrity flaw in our previous implementation. It requires controller-object access; no worker-to-controller exploit path was shown. Multi-agent and snapshot implications are labeled as architectural inferences. Hash-chain history detects a rewrite against a separately protected anchor; it does not establish a correct decision.

No vendor zero-day, customer incident, model attack-success rate, kernel escape or general security certification is claimed. The optional `make factory-boat` path is outside this talk's evidence and build path.

## Session

Zenity AI Agent Security Summit. Wednesday 21 October 2026. Pier Sixty, New York. Fifteen-minute lightning. Attendance is confirmed. Slides are due 9 October. Speaker dinner follows the happy hour.

The exact stage clock, and a logistics reply to Ian, Anna, Kayla, and Neil, were still open when this package was prepared. The [official series page](https://zenity.io/resources/events/ai-agent-security-summit-2026) lists New York on October 21 at Pier Sixty. Primary references and per-slide source links are in the dossier and speaker notes.
