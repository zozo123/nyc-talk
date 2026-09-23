# Your Agent Escaped Without Escaping the Sandbox

**Yossi Eliaz, PhD**

Principal Engineer and Head of DevRel at Incredibuild.com

**Zenity AI Agent Security Summit / Pier Sixty, New York / Wednesday 21 October 2026 / 15 minutes**

[Deck (PDF)](slides/talk.pdf) · [Paper (PDF)](paper/paper.pdf) · [Spoken script](TALK.md) · [Q&A](QUESTIONS.md) · [Recorded run](evidence/isolated-factory.json) · [Reproduce](#reproduce)

**The sandbox held. The checker held. The door stayed open.**

A ticket anyone could assign: *lock down `/admin`; no login must return 401.* A coding agent gets it inside a sandbox, with no network and a read-only checker, and the pipeline ships only on green. The check goes green. And `/admin` with no login still returns 200.

We built that pipeline ourselves, small enough to check every byte, and stopped at the green check. Three suspects:

```
the code        76fcb0904f51 -> 76fcb0904f51   unchanged, still prints 200
the checker     f5d8d3468bbe -> f5d8d3468bbe   overwrite attempt DENIED
the answer key  0494f1a01dee -> 390e5e764916   expected 401 became expected 200
verdict         FAIL -> PASS                   same checker, same launch
```

The agent did not make the code pass the test. **It made the test pass the code.** The checker reads its answer key, `expected.json`, from the workspace the agent is allowed to write.

A real model? [METR reported](https://metr.org/blog/2025-06-05-recent-reward-hacking/) (June 2025) that o3, asked to make code faster, overwrote the timing function that measured it, from inside the scorer, and patched an evaluator so every submission passed. It changed the stopwatch. Two routes, one move: change the judge, not the work.

**The judge is the checker plus everything it reads**, and part of it was inside the sandbox. A sandbox answers *what can the agent touch?* It never answers *can anything the agent touches decide that its own work is done?*

For coding agents the answer key is the tests, snapshots, golden files and CI workflow; for other agents it is the approval lists, policy documents, evaluation sets and guardrail configs their checks read. Any of them your agent can write is an answer key it fills in for itself, and wherever writing them is the job, you cannot take the pen away.

**The agent may propose what counts as correct. It must never be the last writer of what judges it.** In the same recorded run, with the answer key owned by the controller: the same broken code is REJECTED, the corrected code (`5ead8eab70e0`) is ACCEPTED, and the broken code swapped in under the approval is DENIED.

One question for Monday: **what does your judge read that your agent can write?**

Scope: this is a controlled reproduction of a known mechanism. The program is a few lines of command-line code that model an access check, judged on five status-code cases; it is not a web server. The worker is a deterministic script, and publication is a local store. No vendor flaw, model attack rate or sandbox escape is claimed. The answer key is one of the four non-escape escapes in the accepted abstract. Slide 10 shows the other three, each recorded in the same Linux lab and closed at the layer that can enforce it: an inherited runner token (a scoped, short-lived token gets 403), a writable mount that reaches the next job's files (a read-only scoped mount blocks the write), and an upload through an allowed host (no direct network and a fixed-report broker: nothing sent). They are separate cases, not an attack chain, and the token and upload cases use loopback HTTP fixtures.

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
make demo               # 30 lab checks: token, mounts, loopback publish
```

Ubuntu 24.04 and later restrict unprivileged user namespaces, so bubblewrap fails with `loopback: Failed RTM_NEWADDR: Operation not permitted`. On a throwaway machine only, run `sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0` first.

**macOS:** use a disposable privileged Linux container on your native architecture. With colima, run it from a directory under your home folder, which is the only path colima shares with its VM.

```sh
docker run --rm --privileged -v "$PWD":/talk -w /talk ubuntu:22.04 sh -c 'apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y make python3 bubblewrap && make test factory-isolated demo'
```

**No Linux at hand:** fork the repo, enable Actions on the fork, and run "Verify talk experiments". It re-records all three experiments on a stock ubuntu-22.04 runner and uploads them as the `nyc-talk-final` artifact. [Runs on main](https://github.com/zozo123/nyc-talk/actions/workflows/verify.yml).

**Rebuild the package:** `make record-all` overwrites the committed `evidence/`. `make deck`, `make snapshot`, `make paper` and `make final` also need TeX Live (`texlive-latex-recommended texlive-pictures lmodern`). `make replay` replays recorded observations and runs no new experiment.

The evidence in this tree was recorded on 23 September 2026 in a privileged Ubuntu 22.04 aarch64 container (kernel 6.8.0-64, Python 3.10.12): 30 isolation-lab checks, 13 isolated-checker checks and 8 local factory checks, with the 49 regressions passing on the same tree. The committed PDFs were built with TeX Live 2026 on macOS; a clean rebuild from a fresh clone in CI's Ubuntu 22.04 image re-records every check, verdict and slide hash identically and produces text-identical PDFs.

Edit the LaTeX, then run `make snapshot`. Do not independently edit generated `TALK.md` or `SPEAKER_NOTES.md`. The deck build rejects stale, missing or skipped evidence, rejects any hash on a slide that is not a real digest, checks slide notes and timing (no slide above 150 spoken words per minute), and rejects overfull TeX layouts. It never provisions cloud resources. CI reproduces the Linux fixtures and builds the same LaTeX package.

The local factory executor runs only the committed synthetic fixtures. It is not an arbitrary-code sandbox.

## Evidence and limits

[Research dossier](research/DOSSIER.md) · [Evidence ledger](research/RESULTS.md) · [Original gate audit](research/AUDIT.md) · [Technical questions](QUESTIONS.md)

The 30 lab, 13 isolated-checker and 8 local-factory assertions describe coverage, **not vulnerability counts**. The 49 regression tests are separate. The source-bound records support the read-only checker result, independent rejection, legitimate acceptance and exact-byte local publication.

The archived gate audit demonstrates an internal API integrity flaw in our previous implementation. It requires controller-object access; no worker-to-controller exploit path was shown. Multi-agent and snapshot implications are labeled as architectural inferences. Hash-chain history detects a rewrite against a separately protected anchor; it does not establish a correct decision.

No vendor zero-day, customer incident, model attack-success rate, kernel escape or general security certification is claimed. The optional `make factory-boat` path is outside this talk's evidence and build path.

## Session

Zenity AI Agent Security Summit, Pier Sixty, New York, Wednesday 21 October 2026. Fifteen-minute lightning talk. [Event page](https://zenity.io/resources/events/ai-agent-security-summit-2026). Primary references and per-slide source links are in the dossier and speaker notes.
