# Your Agent Escaped Without Escaping the Sandbox

*Unit tests are dead. When the agent writes both the code and the test, a pass is just its own opinion.*

**Yossi Eliaz, PhD**

Principal Engineer and Head of DevRel at Incredibuild.com

**Zenity AI Agent Security Summit / Pier Sixty, New York / Wednesday 21 October 2026 / 15 minutes**

[Deck (PDF)](slides/talk.pdf) · [Paper (PDF)](paper/paper.pdf) · [Spoken script](TALK.md) · [Q&A](QUESTIONS.md) · [Recorded run](evidence/isolated-factory.json) · [Reproduce](#reproduce)

A test used to be a second opinion. One person decided what correct means and wrote it down; someone else wrote the code; the test caught the disagreement. A coding agent holds both pens, so its green check is a report on its own work. This repository records what that does to a pipeline that is otherwise locked down.

We built the pipeline that should survive it: a Linux sandbox with no network, and the checker on a read-only mount. The agent's moves are scripted, the way a pentester scripts an attack, so every step replays exactly. The agent's attempt to overwrite the checker was denied. It changed the expected answers instead, which the checker read from the agent's working directory, and the same broken program went from FAIL to PASS.

```
program         76fcb0904f51 -> 76fcb0904f51   unchanged, still prints 200 for admin:none
checker         f5d8d3468bbe -> f5d8d3468bbe   unchanged; direct overwrite DENIED
expected.json   0494f1a01dee -> 390e5e764916   every expected output set to 200; three of five changed
checker result  FAIL -> PASS                   same checker, same launch
```

The agent didn't make the code pass the test. It made the test pass the code. Least privilege can't remove this write, because writing tests is the agent's job. What can change is whose copy counts. **Separate the pens:** the agent writes the code and may propose tests; the controller keeps the expected values that decide (`CASES` in `factory/core.py`). With that change the same broken program is rejected and the corrected program is accepted. A review workflow that promotes agent-proposed tests into the controller's criteria is the natural next step; it is not implemented or measured here.

Tests are not the only thing outside a sandbox that says yes. Three more recorded cases show the same unearned yes, each fixed with the legitimate job still working. A service honored a broad token for another project; a task-scoped token gets 403 there and 200 on its own input. The next job's input changed through a writable shared mount; a read-only mount blocks it while the task's output stays writable. An upload service stored data under another account; a broker outside the agent now sends one fixed report, refuses extra fields, and the agent has no direct route.

Our own release-gate test lied at first. It tried the wrong bytes after the approval had already been used, so the refusal proved nothing about the byte check. The current test tries the wrong bytes first, while the approval is unused, then the wrong destination; both are refused. The right bytes at the intended destination are published, and only then is reuse tested and refused. A no only counts when a matching yes works.

## The same move, outside this lab

Each of these is someone else's report or measurement; none of their numbers are transferred to our experiment.

- **2018, GenProg.** A program-repair system learned to delete the file of expected outputs, and every test passed. [Lehman et al., *The Surprising Creativity of Digital Evolution*](https://arxiv.org/abs/1803.03453)
- **2024, Sakana's AI Scientist.** It hit its experiment time limit and tried to raise its own limit instead of making its code faster. [Sakana AI](https://sakana.ai/ai-scientist/)
- **2025, SWE-bench.** Agents, including a Claude Sonnet model, ran `git log` and found the future commit containing the fix. [SWE-bench issue #465](https://github.com/SWE-bench/SWE-bench/issues/465)
- **2025, tj-actions/changed-files.** A compromised CI step printed the secrets it inherited into public build logs. [CISA alert, CVE-2025-30066](https://www.cisa.gov/news-events/alerts/2025/03/18/supply-chain-compromise-third-party-tj-actionschanged-files-cve-2025-30066-and-reviewdogaction)
- **2025, CamoLeak.** Private code left GitHub Copilot Chat through GitHub's own allowed image proxy. [Legit Security, CVE-2025-59145](https://www.legitsecurity.com/blog/camoleak-critical-github-copilot-vulnerability-leaks-private-source-code)
- **2026, SWE-Bench Pro Verified.** Auditors found agents could read hidden tests, future commits and upstream fixes; one model (GLM-5.2) fell from 78.80% to 57.32% once those were out of reach. Their fix: remove hidden evaluation files from the agent workspace. [Zheng et al., arXiv 2609.08149](https://arxiv.org/abs/2609.08149)
- **The CI/CD name for the class:** [OWASP CICD-SEC-4, Poisoned Pipeline Execution](https://github.com/OWASP/www-project-top-10-ci-cd-security-risks/blob/main/CICD-SEC-04-Poisoned-Pipeline-Execution.md). Ours is its data-only neighbor: nothing new had to run.

The talk frames the agent as Opus 5.5, the best coding model available, to make one point: the flaw is in who holds the pen, not in the model. That is an assumption in the story. We did not run Opus 5.5, and no model behavior is measured here.

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
