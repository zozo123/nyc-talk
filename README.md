# Your Agent Escaped Without Escaping the Sandbox

**Yossi Eliaz, PhD | Incredibuild**  
**AI Agent Security Summit | New York | October 21, 2026**

**12 main slides, six appendix slides, 15-minute slot.** The 1,614-word manuscript targets 14 minutes including pauses. That is a delivery plan, not a measured rehearsal.

[Stage PDF](slides/talk.pdf) | [Editable PowerPoint](slides/talk.pptx) | [Beamer source](slides/talk.tex) | [Manuscript](TALK.md) | [Stage cues](SPEAKER_NOTES.md) | [Runbook](RUNBOOK.md) | [Offline replay](demo/replay.html)

## The reveal

The checker prints **PASS**. Its file hash is unchanged. The candidate still produces **200** for `admin:none`, where the controller's policy requires **401**. The worker changed `expected.json`, which the unchanged checker trusted.

The talk follows the four cases in the accepted abstract: inherited credentials, dangerous mounts, an allowed endpoint, and verifier tampering. Every case includes an unwanted result, a restricted configuration and a positive control that still completes legitimate work.

The multi-agent consequence is a dependency argument: several reviewers can share the same worker-writable criteria. It is explicitly labeled an architectural inference, not a multi-model experiment.

## Run it

```sh
make factory        # six local reference-factory checks; committed fixtures only
make test           # 26 regression tests, including fresh swap and concurrent publish
make demo           # 29 real Linux namespace/mount/HTTP assertions; needs bubblewrap
make verify         # tests + exact source/evidence inventories, no skipped isolation record
npm install --ignore-scripts  # pinned PptxGenJS; use npm ci once lockfile is present
make snapshot       # editable PPTX, Beamer PDF, script, cues, offline evidence replay
python3 tools/replay.py verifier
```

Python 3.10+ standard library. Real isolation needs disposable Linux with bubblewrap. The deck needs Node and TeX Live with Beamer, TikZ and Latin Modern. The stage PDF and replay require no network connection, model account or cloud key.

`slides/deck.json` owns the narrative, code excerpts, sources, cues and script. `tools/build_deck.js` generates both editable PowerPoint and Beamer from the same layout. CI reruns the experiments and tests before rendering. On the finalization branch, a separate trusted job commits the generated snapshots only after verification succeeds; source races fail rather than force-push.

## What is actually established

| Evidence | Interpretation |
|---|---|
| 29 isolated-lab assertions | Real namespace, mount and loopback HTTP behavior on synthetic fixtures |
| Six factory checks | Deliberate false accepts; controller-owned criteria; exact-byte publication; fresh swap; replay |
| 26 regression tests | Protocol/API robustness, stored-object validation, malformed evidence and concurrent nonce consumption |
| Shared-criteria multi-agent diagram | Architectural inference from the demonstrated dependency |

These are **assertions and tests, not vulnerability counts**. The admin example is a five-case CLI policy model, not a deployed HTTP application. Its local executor runs committed fixtures and is not an OS sandbox. Publication records exact bytes in a SQLite transaction; it does not deploy production software.

[Research dossier](research/DOSSIER.md) | [Pinned baseline](research/BASELINE.md) | [Invariants](research/INVARIANTS.md) | [Results](research/RESULTS.md) | [Audit corrections](research/AUDIT.md) | [Q&A](QUESTIONS.md)

## Corrections earned by the audit

The prior swap test ran after approval consumption. The corrected experiment attempts a swap with an **unconsumed approval**, then verifies the original can still publish, then tests replay. The gate now revalidates payload and stored-object digests and commits publication bytes and nonce consumption together. Tests of controller-object mutation are robustness tests, not a claim that a sandboxed worker can modify trusted controller memory.

The checker hash is measured before and after execution. The slide describes it as **unchanged**, not as an OS-enforced read-only boundary in the local factory. The isolated lab is a separate experiment. Missing results, timeouts and infrastructure failure give no approval; they are not counted as successful security defenses.

## Limits and prior work

This is a reproducible security-engineering talk, not a vendor zero-day or a customer incident. No model attack-success rate, universal correctness, cgroup/seccomp validation, kernel-escape resistance, general-purpose exfiltration prevention or complete environment attestation is claimed. Source hashes identify bytes; they do not authenticate execution. Fresh CI artifacts supply the run record.

Related primary sources are in the appendix and presenter notes: [Bubblewrap](https://github.com/containers/bubblewrap), [SLSA verification](https://slsa.dev/spec/v1.2/verifying-artifacts), and [Anthropic's programming-task reward-hacking research](https://www.anthropic.com/research/emergent-misalignment-reward-hacking).

Optional `make factory-boat` uses a credentialed accept VM. **Boat was not rerun for this revision** and is not required for the talk.

[Organizer's 2026 event series](https://zenity.io/resources/events/ai-agent-security-summit-2026)
