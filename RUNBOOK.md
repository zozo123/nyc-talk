# Stage and reproduction runbook

## Stage delivery

Use `slides/talk.pdf` in full-screen mode. Main talk: slides 1-11. Stop at slide 11; appendices are for Q&A. Keep the PPTX as an editable alternative, not the stage dependency. Carry the PDF and `TALK.md` offline. No terminal, cloud API, model call or live login is required for the main talk.

| Clock | Slide | Beat |
|---|---:|---|
| 00:00-00:20 | 1 | Title and execution-infrastructure context |
| 00:20-01:10 | 2 | PASS versus actual HTTP 200 |
| 01:10-02:15 | 3 | Attacker capabilities and trusted controller |
| 02:15-03:30 | 4 | Credential authority, denial, positive control |
| 03:30-04:45 | 5 | Host-side write through an allowed mount |
| 04:45-06:15 | 6 | Same host, unauthorized account, narrow broker |
| 06:15-08:20 | 7 | Byte-identical checker, worker-owned expectations |
| 08:20-10:20 | 8 | Frozen object through actual release bytes |
| 10:20-11:30 | 9 | Working-task controls and unused-approval swap |
| 11:30-12:30 | 10 | History, enforcement, scope |
| 12:30-14:00 | 11 | Four audit questions and close |
| 14:00-15:00 | - | Margin, host transition or one question |

The 1,651-word script is a target, not a measured rehearsal. Rehearse with the actual projector PDF. At minute 6, be on the verifier-dependency sequence. At minute 10, reach the control matrix. When late, omit the deployment-audit examples on slide 5 and the prior-art paragraph on slide 10. Preserve the threat model, slide 7, unused-approval control, actual release check and close. Never recover lost time by claiming the local executor is a security sandbox.

## Local reproduction

```sh
# Python 3.10+; no third-party Python package required.
make verify
# Inspect fresh, separate outputs:
cat build/http/transcript.txt
cat build/factory/local.json
```

`make verify` runs the 25 unit tests, six factory checks, eleven HTTP checks, and validates source-bound checked-in evidence. HTTP runs on `127.0.0.1` with an ephemeral port. The candidates are committed fixtures. Do not replace them with arbitrary hostile code: local Python `-I` is not OS isolation.

For the actual namespace and bind-mount experiments, use a disposable Linux host with user namespaces enabled:

```sh
sudo apt-get update
sudo apt-get install -y bubblewrap
make demo
```

A denied user namespace or unavailable runtime is an infrastructure limitation, not a successful defense. Do not present `--mode reference` results as isolated-Linux observations. The GitHub Actions job uses Ubuntu 22.04 and installs bubblewrap to reproduce these checks.

## Build the deck

```sh
sudo apt-get install -y texlive-latex-recommended texlive-pictures lmodern
make deck
# Output: build/talk.pdf
npm install --ignore-scripts
make pptx
# Output: build/talk.pptx
make snapshot
# Copies verified outputs into slides/ for distribution.
```

`make deck` first refuses stale or incomplete active evidence, then regenerates Beamer/script/notes from `slides/content.json` and runs LaTeX twice. PptxGenJS 4.0.0 is pinned. Text, panels and tables in the PowerPoint are editable; no font files are distributed. Rendering can vary by installed fonts, so present the PDF.

## Re-record after experiment changes

```sh
make record          # isolated Linux only; copies the actual new record
make record-factory  # reruns and records the local reference protocol
make record-http     # reruns and records HTTP behavior and released bytes
make verify
make deck
```

Update the content only after classifying the new observations. Do not edit hashes to make old results appear current. Keep source maps, result files and the exact source commit together. The build validator checks consistency and completeness; it is not a signature on the evidence.

## Recorded fallback / Q&A

```sh
cat evidence/http-transcript.txt
python3 tools/present.py credentials
python3 tools/present.py mounts
python3 tools/present.py egress
```

These commands display recorded observations. Say "recorded"; they do not launch fresh experiments. If a fresh terminal run fails, show the already-rendered slide and recorded transcript, label the run failure, and continue. Never repair infrastructure or expose environment variables on the projector.

## Optional historical cloud adapter

`make factory-boat` needs a separately supplied `BOAT_API_KEY`. It provisions a short-lived sandbox and attempts cleanup. This is optional, is not needed on stage, and was not rerun for the final active evidence. Infrastructure outcomes exit nonzero rather than appearing as successful defenses. Do not print keys or share shell history.

## Last-mile checklist

Open the PDF offline, check both 200/401 observations and all code lines from the back of the room, hide notifications, and keep the close on screen. Confirm the actual slot and AV arrangements with the organizer separately; the public event page confirms the New York date, not this speaker's exact clock time. Use `QUESTIONS.md` for adversarial rehearsal. Keep any later policy or source change paired with freshly recorded evidence before presenting it.
