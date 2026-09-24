# October 21 stage runbook

**Zenity AI Agent Security Summit. Pier Sixty, New York. Wednesday 21 October 2026.**

**15-minute lightning.** Present `slides/talk.pdf` offline. The leave-behind is `paper/paper.pdf`. Main route: slides 1-12. Slides 13-21 are backup slides for questions; slide 21 lists every reference. The PDF has one page per slide and no overlay clicks. Keep a second local copy of both PDFs.

Do not invent a stage time on the day. Private logistics are kept in `research/private/`, which is not published. The final stage clock is still to be confirmed with the organizer.

## The story

**Unit tests are dead. Not because agents stopped writing them. Because agents write them.** A test used to be a second opinion; with an agent holding both pens, a green check is a self-report. The turn: tests are not dead, trusting a test written by the thing it tests is. The fix: separate the pens. The close pays off the title: *your agent didn't escape the sandbox, it escaped the test.*

The arc: a Tuesday scene (1), the recorded result and the one honest line about the scripted agent (2), why tests ever worked (3), the history, 2018 to 2025 (4), our locked pipeline (5), the whodunit (6), the flaw in four lines (7), the fix (8), our own test that lied (9), every yes outside the sandbox (10), the 2026 benchmark audit (11), the close (12).

Lines to know by heart:

1. "Unit tests are dead. Not because agents stopped writing them. Because agents write them."
2. "A test written by the thing it tests is a self-report."
3. "It didn't make the code pass the test. It made the test pass the code."
4. "A no only counts when a matching yes works."
5. "Your agent didn't escape the sandbox. It escaped the test."

## Timing

The slide windows total 12:15. With 1:00 of shared reserve for transitions, pointing and pauses, the rehearsal target is 13:15, which leaves 1:45 of the 15-minute slot for the host.

The spoken script is 1,011 words: about 83 words per minute across the 12:15 of windows, with no slide above 96. These are allowances, not a measured delivery. Do not pad the script to fill the windows. After the first timed run-through, record the measured time here, move the reserve to the slides that need it, and update the `% time:` lines in `slides/talk.tex` to match.

Measured rehearsal: **not yet recorded.**

| Window | Slide | Stage action |
|---|---:|---|
| 00:00-00:50 | 1 | Tell Tuesday as a scene. Pause before the last two sentences. |
| 00:50-01:35 | 2 | Let the room compare PASS and 200. Say the scripted-agent line plainly, once. |
| 01:35-02:45 | 3 | Left panel, then right panel. Land the self-report line slowly. |
| 02:45-03:55 | 4 | One breath per year. None of them broke out of anything. |
| 03:55-04:45 | 5 | Point to the writable directory, then to DENIED. |
| 04:45-06:00 | 6 | One suspect at a time. Point at 401, then 200. Pause before the last line. |
| 06:00-07:10 | 7 | Count the four lines. Stress line four. |
| 07:10-08:20 | 8 | Read the three rows top to bottom. Pause on REJECT. |
| 08:20-09:30 | 9 | Slow down for the first test. Then read the four rows in order. |
| 09:30-10:45 | 10 | One breath per row: the yes, our lab, the real case. |
| 10:45-11:30 | 11 | Point at the two numbers. Read the quote exactly. |
| 11:30-12:15 | 12 | Callback to Tuesday. Say the title line, pause, then the question. Stop. |
| 12:15-13:15 | - | Shared reserve, spent across the slides above. |
| 13:15-15:00 | - | Margin for the host. |

## Rehearsal

Rehearse with an audible timer and record the result above. Checkpoints: "Unit tests are dead" by 00:50, the self-report line by 02:45, the whodunit by 05:00, the fix by 08:00, and the closing slide by 12:00.

Pauses of two or three seconds: before "Unit tests are dead" (1), after "a self-report" (3), before "It made the test pass the code" (6), after "you can't take that permission away" (7), after "rejected" (8), after "A no only counts" (9), and between the title line and the question (12).

Read the whole script aloud at least once before the day. Rewrite any sentence that is awkward to say or needs a second reading, in `slides/talk.tex`, then run `python3 tools/build_deck.py` and commit. GitHub Actions rebuilds and commits the PDFs on `main`; download them from the workflow run or pull again before presenting.

Say "admin" plainly; the only case read aloud is no login. Do not read hashes aloud: the slides carry them. Read the SWE-Bench Pro quote exactly as written, and name GLM-5.2 only if asked; the slide credits it. Add no rates beyond the two numbers on slide 11.

Disclosures that stay on every run, even if behind: the agent is a script and Opus 5.5 is an assumption (1, 2), the historical cases are other people's reports (4), the AI-reviewer point is an argument (8), publication is a local database (9), and the 2026 numbers are their measurement (11). If behind, slide 3 may drop its last paragraph, slide 7 its middle paragraph, and slide 10 the CamoLeak sentence.

## Evidence on stage

The slide outputs summarize recorded executions. Do not present them as a live session. The central example is a command-line model that prints status codes. The supporting credential and upload cases use loopback HTTP. The earlier-gate audit belongs in Q&A (backup slide A5) and required controller-object access. Every real-world case is someone else's report; the sources are on backup slide A9 and in the README.

The talk describes a controlled experiment around a familiar mechanism. Do not improvise a production incident, customer, vendor flaw, surprised reaction or model attack-success rate, and do not say Opus 5.5 did anything: it was not run. Five cases establish their tested behavior only.

## Local preparation

```sh
make test
make evidence
python3 tools/build_deck.py
```

GitHub Actions builds the PDFs ([Build LaTeX PDFs](.github/workflows/pdfs.yml)). `make snapshot` builds them locally if TeX Live is installed. Before the talk, pull `main` so `slides/talk.pdf` is the version the workflow built.

After changing experiment source, first run `make record-all` on disposable Linux with bubblewrap. Ubuntu 24.04 restricts unprivileged user namespaces, and bubblewrap then fails while bringing up a network namespace. On that release:

```sh
sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0
```

The current records come from a privileged Ubuntu 22.04 container on kernel 6.8.0-64, where that sysctl is not needed; on a stock Ubuntu 24.04 host it is. Inspect the compiled PDF and keep it offline. `make replay` is an optional, explicitly labeled recording. No cloud login or live terminal is part of the delivery.

## Organizer and AV

Use the accepted title. The 15-minute duration comes from the session brief. Exact stage time and AV arrangements still require organizer confirmation. This package does not imply that logistical confirmation has happened.
