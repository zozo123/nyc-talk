# October 21 stage runbook

**Zenity AI Agent Security Summit. Pier Sixty, New York. Wednesday 21 October 2026.**

**15-minute lightning.** Present `slides/talk.pdf` offline. The leave-behind is `paper/paper.pdf`. Main route: slides 1-12. Slides 13-20 are backup slides for questions. The PDF has one page per slide and no overlay clicks. Keep a second local copy of both PDFs.

Do not invent a stage time on the day. Private logistics are kept in `research/private/`, which is not published. The final stage clock is still to be confirmed with the organizer.

## Timing

The slide windows total 12:15. With 1:00 of shared reserve for transitions, pointing and pauses, the rehearsal target is 13:15, which leaves 1:45 of the 15-minute slot for the host.

The spoken script is 1,005 words: about 82 words per minute across the 12:15 of windows, with no slide above 99. These are allowances, not a measured delivery. At a conversational pace the words alone take roughly eight to nine minutes; the rest is looking at the slide with the room. Do not pad the script to fill the windows. After the first timed run-through, record the measured time here, move the reserve to the slides that actually need it, and update the `% time:` lines in `slides/talk.tex` to match.

Measured rehearsal: **not yet recorded.**

## The talk in one line

A read-only checker passed a broken program because the worker could change the expected answers the checker read. Before you trust a green check, find out whether the agent can change what makes it green.

| Window | Slide | Stage action |
|---|---:|---|
| 00:00-00:45 | 1 | Start with the ticket. No preamble. |
| 00:45-01:30 | 2 | Let the room compare PASS and 200 before you speak. |
| 01:30-02:30 | 3 | Point to the writable directory, then to DENIED. |
| 02:30-03:45 | 4 | Point at 401, then at 200. Pause after "match it." |
| 03:45-04:45 | 5 | Point at the line of code, then trace the two arrows. |
| 04:45-05:45 | 6 | Say METR as "meter". One example. No rates. |
| 05:45-07:00 | 7 | One breath per row. |
| 07:00-08:00 | 8 | Read across each row: the change, then the result. |
| 08:00-09:00 | 9 | Read the rows top to bottom. Pause on REJECT. |
| 09:00-10:30 | 10 | Slow down for the first test. Then read the four rows in order. |
| 10:30-11:30 | 11 | Read the four questions. Pause after the fourth. |
| 11:30-12:15 | 12 | Point at the four lines. Say the last sentence, then stop. |
| 12:15-13:15 | - | Shared reserve, spent across the slides above. |
| 13:15-15:00 | - | Margin for the host. |

## Rehearsal

Rehearse with an audible timer and record the result above. Checkpoints: the passing result on screen by 01:00, the changed expected answer by 03:00, the corrected result by 09:00, and the closing slide by 12:00.

Pauses of two or three seconds: after the ticket (1), before speaking on slide 2, after "We'd changed the expected result to match it." (4), after "It's rejected." (9), after "But the approval was already spent." (10), and after the fourth question (11).

Read the whole script aloud at least once before the day. Rewrite any sentence that is awkward to say or needs a second reading, in `slides/talk.tex`, then run `python3 tools/build_deck.py` and commit. GitHub Actions rebuilds and commits the PDFs on `main`; download them from the workflow run or pull again before presenting.

Say "admin" plainly; the only case read aloud is no login. Do not read hashes aloud: the slides carry them. Say METR as "meter". Name METR, the date and o3 as written on slide 6, and add no rates on stage; if asked, the numbers and METR's own caveats are in `research/DOSSIER.md`.

If behind, cut words, never the disclosures. Keep these lines on every run: the worker is a script (3), we stopped at the passing result (2), METR's example is a separate evaluation (6), the three other cases are separate experiments and the services run locally (7), we did not implement a review workflow for proposed tests (8), five cases do not prove an application secure (9), and publication is a local database (10). Slide 5 may drop its middle paragraph. Slide 7 may drop its last paragraph. Slide 11 may drop its second paragraph.

## Evidence on stage

The slide outputs summarize recorded executions. Do not present them as a live session. The central example is a command-line model that prints status codes. The supporting credential and upload cases use loopback HTTP. The earlier-gate audit belongs in Q&A (backup slide A5) and required controller-object access.

The talk describes a controlled experiment around a familiar mechanism. Do not improvise a production incident, customer, vendor flaw, surprised reaction or model attack-success rate. Five cases establish their tested behavior only.

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
