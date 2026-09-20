# Your Agent Escaped Without Escaping the Sandbox

**Yossi Eliaz**  
**Principal Engineer and Head of DevRel at Incredibuild.com**

NYC · AI Agent Security Summit · October 21, 2026

**15-minute lightning talk.** Twelve main slides, three appendix slides. The manuscript targets 14 minutes with one minute of margin. Recorded demonstrations are shown directly on slides.

[Deck PDF](slides/talk.pdf) · [LaTeX](slides/talk.tex) · [Spoken script](TALK.md) · [Speaker notes](SPEAKER_NOTES.md) · [Runbook](RUNBOOK.md) · [Q&A](QUESTIONS.md) · [Recorded results](evidence/transcript.txt)

**Verified:** all 29 checks passed in the [recorded Linux isolation run](https://github.com/zozo123/nyc-talk/actions/runs/35461381644), including real namespace, mount and network checks. The same CI run compiled the deck. Recorded lab source hashes match this repository.

## The story

One task: **fix a parser and publish its report**.

The talk opens on a green check and a parser that still fails its original case. It holds the explanation until act four. Between those moments, each experiment shows how a convenient grant lets the worker affect something beyond its task. The ending returns to the same input and shows the repaired system completing the job.

Four independent experiments reveal excess authority:

1. **Identity:** an inherited runner credential reads another project.
2. **Files:** a writable bind mount changes the next job's host fixture.
3. **Data release:** an allowed upload service receives private data in the wrong account.
4. **Acceptance:** a rewritten checker reports success while the parser stays broken.

Each experiment tests the repair and a legitimate operation. The final run fixes the parser, checks its frozen bytes independently, obtains a publication decision and sends the permitted report.

**The question: who gave this process the authority?**

## Run it

Python 3.10+ standard library. For actual isolation, use a disposable Linux host with bubblewrap and working unprivileged user namespaces.

```sh
make demo       # strict namespace/mount/network experiments
make reference  # policy logic only; integration checks explicitly skipped
make deck       # verify recorded source hashes, export notes, compile PDF
python3 tools/present.py credentials  # show one recorded act
```

Install bubblewrap through your Linux distribution. The deck needs TeX Live with Beamer, listings and Latin Modern. Example on Ubuntu:

```sh
sudo apt-get install bubblewrap texlive-latex-recommended texlive-pictures lmodern
```

A missing isolation capability causes **failure**, never automatic fallback. Fresh temporary fixtures are removed after each run. No real credentials, external targets or model API are used. Reference mode executes only this repo's deterministic fixtures and provides no sandbox.

## What's here

| File | Purpose |
|---|---|
| [slides/talk.tex](slides/talk.tex) | 15 editable Beamer slides: 12 main + 3 appendix |
| [lab/run.py](lab/run.py) | Four experiments, positive controls and final task |
| [evidence/results.json](evidence/results.json) | Recorded mode, source hashes, checks and subprocess output |
| [evidence/transcript.txt](evidence/transcript.txt) | Offline demo fallback |
| [TALK.md](TALK.md) | Final 15-minute manuscript with per-slide timeboxes |
| [RUNBOOK.md](RUNBOOK.md) | 15-minute delivery, rehearsal checkpoints and overrun cuts |
| [QUESTIONS.md](QUESTIONS.md) | Answers to security objections and scope questions |
| [tools/present.py](tools/present.py) | Display one recorded act without revealing the next |
| [tools/evidence.py](tools/evidence.py) | Refuses stale evidence before building the deck |
| [.github/workflows/verify.yml](.github/workflows/verify.yml) | Linux integration and deck build |

The PDF labels its evidence mode. The source digest in the record must match the lab. Use `make record` after an isolated run to refresh the record, then `make snapshot` to refresh the checked-in PDF.

The lab uses deterministic worker scripts, a local fixture service and controller-held trust anchors. It demonstrates specific authority failures. It does not measure live-model prompt-injection susceptibility, cgroup enforcement, kernel exploit resistance or all possible data channels. The history anchor is ephemeral. Five parser cases establish the demonstrated defect and fix, not complete correctness.

## Accepted Sessionize abstract

> Every namespace and cgroup can work exactly as designed and an agent can still cause a real breach. This talk demonstrates four non-escape escapes: inherited credentials, dangerous mounts, exfiltration through an allowed endpoint, and verifier tampering. Then we close each one at the layer that can actually enforce it: real process isolation, capability-scoped filesystems, short-lived credential projection, and tamper-evident execution history. You leave with four boundaries you can check against your own agent deployment.

Title, abstract, tagline and accepted status supplied by the speaker from Sessionize. The technical treatment distinguishes process isolation, authorization, independent verification and tamper detection.

## Scheduling

The speaker confirmed a **15-minute lightning talk**. That instruction supersedes the earlier hour-long calendar-block assumption. The deck and script target 14 minutes with one minute of margin. Do not reserve an additional Q&A segment inside the 15 minutes. The previously reported public feed listed Oct 21, 15:45–16:45, Room 1; that block does not define this talk's duration.
