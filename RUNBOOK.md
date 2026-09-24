# October 21 stage runbook

**Zenity AI Agent Security Summit. Pier Sixty, New York. Wednesday 21 October 2026.**

**15-minute lightning.** Present `slides/talk.pdf` offline. The leave-behind is `paper/paper.pdf`. Main route: slides 1-8. Slides 9-17 are backup slides for questions; slide 17 lists every source. The PDF has one page per slide and no overlay clicks. Keep a second local copy of both PDFs.

Do not invent a stage time on the day. Private logistics are kept in `research/private/`, which is not published. The final stage clock is still to be confirmed with the organizer.

## The story

```
1 Tuesday: tests pass, door open        "Unit tests are dead."
2 A test was a second opinion           student writes the answer key (2010 experiment, Replit)
3 We locked the checker. It passed.     our lab: FAIL, BLOCKED, PASS
4 Who made it pass?                     the answer file changed
5 Separate the pens                     REJECTED, ACCEPTED
6 Real models go find the answers       SWE-bench; SWE-Bench Pro 78.8% -> 57.3%
7 Four places to check                  key, folder, upload, answers
8 It escaped the test                   Monday checklist
```

Lines to know by heart:

1. "Unit tests are dead. Not because agents stopped writing them. Because agents write them."
2. "It's like letting the student write the answer key."
3. "A passing test is just the agent's own opinion."
4. "It didn't make the code pass the test. It made the test pass the code."
5. "Separate the pens. The teacher keeps the answer key."
6. "Your agent didn't escape the sandbox. It escaped the test."

## Timing

The slide windows total 10:00. With 1:00 of shared reserve, the rehearsal target is 11:00, which leaves 4:00 of the 15-minute slot for questions and the host.

The spoken script is 717 words of short, plain sentences: about 72 words per minute across the windows, with no slide above 92. At a normal pace the words take five to six minutes; with pauses, pointing and the room reading the slides, expect roughly eight to nine. These are allowances, not a measured delivery. After the first timed run-through, record the measured time here and update the `% time:` lines in `slides/talk.tex`.

Measured rehearsal: **not yet recorded.**

| Window | Slide | Stage action |
|---|---:|---|
| 00:00-01:00 | 1 | Tell Tuesday as a scene. Pause before "Unit tests are dead." |
| 01:00-02:15 | 2 | Before, then now. Say the student line, then the two examples, then land the last line. |
| 02:15-03:15 | 3 | Say the script line once, before any result. Point to FAIL, then BLOCKED, then PASS. |
| 03:15-04:30 | 4 | One suspect at a time. Pause before the last line. |
| 04:30-05:45 | 5 | Say the turn first. Read the three rows. Pause on REJECTED. |
| 05:45-06:45 | 6 | Ask the question. Point at the two numbers. Say "another barely moved." |
| 06:45-08:45 | 7 | Say the rule first. One breath per row. Number them out loud. |
| 08:45-10:00 | 8 | Back to Tuesday. Say the title line, pause, then the checklist. Stop. |
| 10:00-11:00 | - | Shared reserve. |
| 11:00-15:00 | - | Questions and the host. |

## Rehearsal

Rehearse with an audible timer and record the result above. Checkpoints: "Unit tests are dead" by 01:00, the whodunit by 03:30, the fix by 05:00, the four places by 07:00, the close by 09:00.

Pauses of two or three seconds: before "Unit tests are dead" (1), after "the student write the answer key" (2), before "It made the test pass the code" (4), after "rejected" (5), after "another barely moved" (6), and between the title line and the checklist (8).

Read the whole script aloud at least once before the day. Rewrite any sentence that is awkward to say, in `slides/talk.tex`, then run `python3 tools/build_deck.py` and commit. GitHub Actions rebuilds and commits the PDFs on `main`.

Say "admin" plainly. Do not read hashes aloud. Name GLM-5.2 and DeepSeek-V4-Pro only if asked; the slide credits them. Add no rates beyond the two numbers on slide 6.

Lines that stay on every run, even if behind: "Say your agent is Opus 5.5. The model doesn't matter here." (1), "our agent is a script" (3), "another barely moved" (6), and "a researcher showed" for CamoLeak (7). Never say Opus 5.5 did anything; it was not run. The 2010 example is a bug-fixing experiment, not GenProg in 2018. Backup slide A1 covers the rest: five cases, local database, what is not claimed. If behind, slide 2 may drop the Replit sentence and slide 7 the tj-actions and CamoLeak sentences.

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
