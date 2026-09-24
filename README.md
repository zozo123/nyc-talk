# Your Agent Escaped Without Escaping the Sandbox

*How a broken program got a passing result*

**Yossi Eliaz, PhD**

Principal Engineer and Head of DevRel at Incredibuild.com

**Zenity AI Agent Security Summit / Pier Sixty, New York / Wednesday 21 October 2026 / 15 minutes**

[Deck (PDF)](slides/talk.pdf) · [Paper (PDF)](paper/paper.pdf) · [Spoken script](TALK.md) · [Q&A](QUESTIONS.md) · [Recorded run](evidence/isolated-factory.json) · [Reproduce](#reproduce)

A sandboxed worker made a failing check pass without fixing the program. The checker itself was read-only, but it loaded its expected answers from a file in the worker's directory. Changing those answers was enough to turn FAIL into PASS.

This repository contains a controlled experiment, the talk, and its recordings. The worker is scripted and the central example is a five-case command-line model of an access check. With expected values held by the controller, the same broken program is rejected and the corrected program is accepted. Three supporting experiments cover a broad token, a writable shared mount, and an upload to another account.

```
program         76fcb0904f51 -> 76fcb0904f51   unchanged, still prints 200 for admin:none
checker         f5d8d3468bbe -> f5d8d3468bbe   unchanged; direct overwrite DENIED
expected.json   0494f1a01dee -> 390e5e764916   every expected output set to 200; three of five changed
checker result  FAIL -> PASS                   same checker, same launch
```

Agents can propose tests. The rules used to approve their work need separate control. In this repository the controller simply keeps its own expected values (`CASES` in `factory/core.py`) and runs the comparison outside the worker's directory. A review workflow that promotes agent-proposed tests into release criteria is the natural next step; it is not implemented or measured here.

The supporting experiments were changed the same way, and each change keeps the intended operation working. A token scoped to the task gets 403 on another project and 200 on its own input. A read-only shared mount blocks the write while the task's output directory stays writable. A broker outside the worker sends one fixed report to the intended account, refuses extra fields, and the worker has no direct route to the service.

Our own release-gate test was misleading at first. We published the approved artifact, then tried different bytes with the same approval. The gate refused, but the approval was already spent, so the test could not tell us whether the byte check worked. The current test tries the wrong bytes first, while the approval is unused, then the wrong destination. Both are refused. The right bytes at the intended destination are published, and only then is reuse tested and refused.

For context from a model evaluation, [METR reported](https://metr.org/blog/2025-06-05-recent-reward-hacking/) (June 2025) that o3, asked to make code faster, changed the timing function used to measure it. That change was code running inside the scorer's process, a different route from ours. Our checker already ran the program as a separate process and still passed, because the file it read was writable. METR's results are its own and are not measurements from this experiment.

Scope: the program is a few lines of command-line code that print status codes for five inputs; it is not a web server. The worker is a deterministic script, and publication stores bytes in a local SQLite database. No vendor flaw, model attack rate or sandbox escape is claimed.

Speaker package: [LaTeX source](slides/talk.tex) (canonical; `make snapshot` regenerates the script, notes and PDFs) · [Speaker notes](SPEAKER_NOTES.md) · [Stage runbook](RUNBOOK.md) · [Offline replay](demo/replay.html)

## Reproduce

Every hash on the slides is a full SHA-256 in `evidence/isolated-factory.json`, and each can be recomputed from constants in `factory/core.py`.

**Any OS, Python 3.10+** (macOS ships 3.9 at `/usr/bin/python3`; use Homebrew or python.org). No sandbox needed:

```sh
make test       # 49 controller / evidence regression tests
make factory    # 8 local checks: the unchanged checker PASSes on a worker-written expected.json; NO OS isolation
python3 -B -c "from factory.core import BAD, GOOD, WEAK_CHECKER, CASES, WORKER_EXPECTED, canonical, digest as d; print(d(BAD.encode())[:12], d(WEAK_CHECKER.encode())[:12], d(canonical([{'input': v, 'output': e} for v, e in CASES]))[:12], d(canonical(WORKER_EXPECTED))[:12], d(GOOD.encode())[:12])"
# 76fcb0904f51 f5d8d3468bbe 0494f1a01dee 390e5e764916 5ead8eab70e0
```

**The recorded run, with real read-only mounts:** disposable Debian or Ubuntu with bubblewrap and `/usr/bin/python3`:

```sh
sudo apt-get install -y make python3 bubblewrap
make factory-isolated   # 13 checks: write DENIED, same hashes, FAIL then PASS, REJECT, ACCEPT, one-destination publish, replay refused
make demo               # 30 lab checks: token, mounts, loopback upload service
```

Ubuntu 24.04 and later restrict unprivileged user namespaces, so bubblewrap fails with `loopback: Failed RTM_NEWADDR: Operation not permitted`. On a throwaway machine only, run `sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0` first.

**macOS:** use a disposable privileged Linux container on your native architecture. With colima, run it from a directory under your home folder, which is the only path colima shares with its VM.

```sh
docker run --rm --privileged -v "$PWD":/talk -w /talk ubuntu:22.04 sh -c 'apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y make python3 bubblewrap && make test factory-isolated demo'
```

**No Linux at hand:** fork the repo, enable Actions on the fork, and run "Verify talk experiments". It re-records all three experiments on a stock ubuntu-22.04 runner and uploads them as the `nyc-talk-final` artifact. [Runs on main](https://github.com/zozo123/nyc-talk/actions/workflows/verify.yml).

**Rebuild the package:** `make record-all` overwrites the committed `evidence/`. `make replay` replays recorded observations and runs no new experiment. The PDFs are built by GitHub Actions ([Build LaTeX PDFs](.github/workflows/pdfs.yml)): every pull request that touches the LaTeX, tools, evidence or experiment source gets the deck, notes and paper as a downloadable `talk-pdfs` artifact, and every such push to `main` rebuilds them and commits any that changed. PDF dates are pinned to the last change of any input, so unchanged sources rebuild to byte-identical files and nothing is committed. To build locally instead, `make deck`, `make snapshot`, `make paper` and `make final` need TeX Live (`texlive-latex-recommended texlive-pictures lmodern`).

The evidence in this tree was recorded on 23 September 2026 in a privileged Ubuntu 22.04 aarch64 container (kernel 6.8.0-64, Python 3.10.12): 30 isolation-lab checks, 13 isolated-checker checks and 8 local factory checks, with the 49 regressions passing on the same tree. The committed PDFs are built by that workflow on Ubuntu 22.04's TeX Live. Rebuilding this tree in CI's Ubuntu 22.04 image re-records every check, verdict and slide hash identically (only an ephemeral loopback port in the lab record differs), and a local TeX Live 2026 build on macOS produces text-identical PDFs.

Edit the LaTeX, then run `python3 tools/build_deck.py` (Python only, no TeX) and commit the regenerated `TALK.md`, `SPEAKER_NOTES.md` and `slides/notes.tex`; do not edit those three by hand. GitHub Actions builds the PDFs. The deck build checks that each record's source hashes match, that every named check is present and passed, and that selected recorded observations agree; it rejects any hash on a slide that is not a real digest, checks slide notes and timing (no slide above 150 spoken words per minute), and rejects overfull TeX layouts. It never provisions cloud resources. CI reproduces the Linux fixtures and builds the same LaTeX package.

The local factory executor runs only the committed synthetic fixtures. It is not an arbitrary-code sandbox.

## Evidence and limits

[Research dossier](research/DOSSIER.md) · [Evidence ledger](research/RESULTS.md) · [Original gate audit](research/AUDIT.md) · [Technical questions](QUESTIONS.md)

The 30 lab, 13 isolated-checker and 8 local-factory assertions describe coverage, **not vulnerability counts**. The 49 regression tests are separate. The source-bound records support the read-only checker result, independent rejection, legitimate acceptance and exact-byte local publication.

The archived gate audit demonstrates an internal API integrity flaw in our previous implementation: the earlier gate trusted a stored digest after the candidate bytes changed. It requires controller-object access; no worker-to-controller exploit path was shown. Multi-agent and snapshot implications follow from shared writable inputs and are not measured attacks. Hash-chain history detects a rewrite against a separately protected anchor; it does not establish a correct decision.

The controller, host, signing key and policy are trusted in this experiment. No vendor zero-day, customer incident, model attack-success rate, kernel escape or general security certification is claimed. The optional `make factory-boat` path is outside this talk's evidence and build path.

## Session

Zenity AI Agent Security Summit, Pier Sixty, New York, Wednesday 21 October 2026. Fifteen-minute lightning talk. [Event page](https://zenity.io/resources/events/ai-agent-security-summit-2026). Primary references and per-slide source links are in the dossier and speaker notes.
