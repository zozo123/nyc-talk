# October 21 stage runbook

**Zenity AI Agent Security Summit. Pier Sixty, New York. Wednesday 21 October 2026.**

**15-minute lightning.** Present `slides/talk.pdf` offline. The leave-behind is `paper/paper.pdf`. Main route: slides 1-10. Slides 11-19 are backup slides for questions; slide 19 lists every source. The PDF has one page per slide and no overlay clicks. Keep a second local copy of both PDFs.

Do not invent a stage time on the day. Private logistics are kept in `research/private/`, which is not published. The final stage clock is still to be confirmed with the organizer.

## The story

```
 1 Title: no internet, checker locked, every check green, admin allowed
   "Those aren't holes. They're doors. You opened them on purpose."
 2 Door 1, the key      broad token read another project; fix: one key per task
 3 Door 2, the folder   rewrote the next job's input on the host; fix: read-only
 4 Door 3, the wire     posted to another account, 201; fix: no route, a broker
 5 Door 4, the verdict  FAIL, DENIED, PASS. "Which file did it?"
 6 The fingerprints     same, same, CHANGED. "It made the test pass the code."
 7 This move has a record   2010, Replit 2025, SWE-bench 2025, SWE-Bench Pro 2026
 8 The answer key lives outside   three doors: take the permission away; the
                         fourth you can't; a second copy. REJECTED, ACCEPTED.
 9 How to check a door  our test lied; refused/refused/released/refused
10 Escaped without escaping   pick one door; what does it trust, can the agent write it
```

Lines to know by heart:

1. "Those aren't holes. They're doors. You opened them on purpose."
2. "Same code. Same checker. Which file did it?"
3. "It didn't make the code pass the test. It made the test pass the code."
4. "Lock the answer file, and the agent can't write tests. Writing tests is the job. You just fired it."
5. "Not a bigger lock. A second copy."
6. "A no only counts if the yes still works. Green checks lie. So do red ones."
7. "Your agent escaped without escaping the sandbox."

## Timing

The slide windows total 10:15. With 1:00 of shared reserve, the rehearsal target is 11:15, which leaves about 3:45 of the 15-minute slot for questions and the host.

The spoken script is 1,153 words of short sentences: about 113 words per minute across the windows, with no slide above 118. That is a brisk conversational pace; do not rush past the three pauses below. These are allowances, not a measured delivery. After the first timed run-through, record the measured time here and update the `% time:` lines in `slides/talk.tex`.

Measured rehearsal: **not yet recorded.**

| Window | Slide | Stage action |
|---|---:|---|
| 00:00-01:10 | 1 | Pause after "walks straight in". Say the honest note flat and fast. No pause before "Four doors". |
| 01:10-02:10 | 2 | Say "Why not? The key was valid." with a shrug. Point at 403, then at 200. |
| 02:10-02:55 | 3 | Say "On the host." as its own beat and let it sit. |
| 02:55-03:55 | 4 | Say "201, created" and stop for a beat before "front door". |
| 03:55-04:55 | 5 | Point at each line in turn. End on "Which file did it?", count three seconds, and welcome the shout. |
| 04:55-06:00 | 6 | Point at each row. Hold on CHANGED. Say the last line, then let it sit. |
| 06:00-07:15 | 7 | One year per breath. Slow down on the four controls. Say the last line to the back of the room. |
| 07:15-08:15 | 8 | Pause after "A second copy." before you explain it. Point at REJECTED, then ACCEPTED. |
| 08:15-09:25 | 9 | Point at the four rows one at a time. Say the rule only after the fourth. |
| 09:25-10:15 | 10 | Say the title line, stop, then the two questions. Add nothing after "Thank you". |
| 10:15-11:15 | - | Shared reserve. |
| 11:15-15:00 | - | Questions and the host. |

## Rehearsal

Rehearse with an audible timer and record the result above. Checkpoints: "Four doors" by 01:10, "Which file did it?" by 05:00, "A second copy" by 07:30, the close by 09:30.

The three pauses that matter: three seconds after "Which file did it?" (5), two after "A second copy." (8), two after "Your agent escaped without escaping the sandbox." (10).

Read the whole script aloud at least once before the day. Rewrite any sentence that is awkward to say, in `slides/talk.tex`, then run `python3 tools/build_deck.py` and commit. GitHub Actions rebuilds and commits the PDFs on `main`.

Say "admin" plainly. Do not read hashes aloud. Name GLM-5.2 and DeepSeek-V4-Pro only if asked; the sources slide credits them. Add no rates beyond 79 and 57.

Lines that stay on every run, even if behind: "Say your agent is Opus 5.5. Pick any model." and "with no model in it. Our agent is a script." (1); "Not an agent. Same door." for tj-actions (2); "a researcher showed" and "GitHub fixed it" for CamoLeak (4); "Another barely moved." (7); "We didn't build the step that reviews those proposals." (8); "In our lab that place is a local database." (9). Never say Opus 5.5 did anything; it was not run. If behind, slide 2 may drop the tj-actions sentence, slide 4 the CamoLeak sentence, and slide 7 the four controls.

## Evidence on stage

The slide outputs summarize recorded executions. Do not present them as a live session. The central example is a command-line model that prints status codes. The supporting credential and upload cases use loopback HTTP. The earlier-gate audit belongs in Q&A (backup slide A5) and required controller-object access. Slide 9's release step stores a build in a local database; say so if anyone hears "released" as deployed. Every real-world case is someone else's report; the sources are on backup slide A9 and in the README.

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
