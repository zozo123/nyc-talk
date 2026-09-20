# Your Agent Escaped Without Escaping the Sandbox

**Yossi Eliaz | Incredibuild**  
AI Agent Security Summit, New York | **October 21, 2026**

**15-minute lightning talk: 12 main slides, 4 appendix slides.** The manuscript targets 14 minutes including pauses; rehearse against the clock.

[Stage PDF](slides/talk.pdf) | [Editable PowerPoint](slides/talk.pptx) | [Beamer source](slides/talk.tex) | [Manuscript](TALK.md) | [Speaker notes](SPEAKER_NOTES.md) | [Runbook](RUNBOOK.md) | [Skeptical Q&A](QUESTIONS.md) | [Research dossier](research/DOSSIER.md)

## The finding on screen

The worker cannot write `checker.py`. Its SHA-256 stays unchanged. The worker can write `expected.json`, which the checker reads. The unchanged checker prints **PASS** for a candidate that the controller's original policy rejects.

**Before accepting an agent's work, identify every input that can change the verdict.** Protecting the checker file alone does not protect the criteria it consumes.

The talk connects four reproducible cases: a runner credential reads another project; a writable mount changes another job's file; an allowed service accepts an unintended recipient; and worker-controlled expectations change acceptance. Every corrected case retains a legitimate-operation control.

These are deterministic, deliberately vulnerable reference configurations, not discovered vendor zero-days or a model attack-success-rate study. The credential and outbound cases use loopback HTTP. The admin example is a **status-code model**, not a deployed HTTP service. The release sink stores approved bytes in controller-owned SQLite, not a production registry or Git merge.

## Run the experiments

Python 3.10+ and its standard library run the logic and regression tests:

```sh
make test
make factory
```

`make factory` is **local fixture execution, not a sandbox**. Run only the committed fixtures through it.

On disposable Linux with bubblewrap and unprivileged user namespaces enabled:

```sh
make isolated        # both fresh experiment suites; no cloud or credentials
make record          # explicitly refresh checked-in evidence from isolated runs
```

The suite contains **29 isolation-lab assertions, 15 factory assertions and 15 unit tests**. Passing a detector means the deliberately weak configuration failed as expected. These counts are not counts of vulnerabilities or independent attacks. Machine-readable records and full transcripts live in [evidence/](evidence/).

## Build the talk

```sh
# TeX Live: beamer, tikz, helvet/courier (fonts-recommended).
make deck            # fail closed on stale, incomplete or non-isolated evidence
make snapshot        # copy the verified PDF to slides/talk.pdf

# Only needed when authoring slides or rebuilding the editable PowerPoint:
npm install --ignore-scripts --no-audit --no-fund
make author          # one content model -> native PPTX + native Beamer + manuscript
make deck
```

`slides/content.json` is the shared content source; `slides/build.js` creates editable PptxGenJS shapes/text and exports the geometry used by `tools/author.py` for Beamer. Neither format is a flattened screenshot deck. Node is unnecessary for recompiling the checked-in Beamer source. No stage command provisions a VM or calls a model.

`factory/boat.py` remains an optional, historical provider adapter; the final evidence path does not use it. Earlier cloud-run records are not treated as verification of the revised factory. See [baseline](research/BASELINE.md).

## Release boundary

The trusted controller owns policy, expected results, signing key and publication. It freezes exact candidate bytes, executes the frozen candidate, compares outputs outside the candidate, and authenticates a receipt bound to artifact, verifier, policy, expectations, run, environment, expiry and nonce. Publication atomically stores those **same bytes** and consumes the nonce.

An audit also reproduced a defect in our earlier reference API: a mutable file map could change payload bytes without changing its stored digest. This was a direct in-process harness result, not evidence that a sandboxed worker could reach controller memory. The repaired API derives identity from immutable bytes and includes fresh-nonce substitution controls and a concurrent replay regression.

## Accepted abstract

> Every namespace and cgroup can work exactly as designed and an agent can still cause a real breach. This talk demonstrates four non-escape escapes: inherited credentials, dangerous mounts, exfiltration through an allowed endpoint, and verifier tampering. Then we close each one at the layer that can actually enforce it: real process isolation, capability-scoped filesystems, short-lived credential projection, and tamper-evident execution history. You leave with four boundaries you can check against your own agent deployment.

The title uses "escaped" for a policy/authority violation while a process remains confined. It does not assert a kernel escape. History detects changes relative to a trusted head; the gate enforces release. See [scope and limitations](research/DOSSIER.md#scope-and-limitations).

[Official event page](https://zenity.io/resources/events/ai-agent-security-summit-2026)
