# Your Agent Escaped Without Escaping the Sandbox

**Yossi Eliaz, PhD**  
Principal Engineer and Head of DevRel, Incredibuild  
**AI Agent Security Summit / New York / October 21, 2026 / 15 minutes**

[Presentation PDF](slides/talk.pdf) | [Spoken script](TALK.md) | [Speaker notes](SPEAKER_NOTES.md) | [Stage runbook](RUNBOOK.md) | [Research dossier](research/DOSSIER.md) | [Hard questions](QUESTIONS.md)

## The talk

The worker may propose the artifact. **It must not define why that artifact is eligible for release.**

Twelve main slides, six technical appendices, approximately 1,700 spoken words. The delivery target is 14 minutes with a one-minute margin. The accepted title and four cases remain intact. These are reproducible, deliberately scoped experiments, not a claimed vendor zero-day.

The centerpiece holds the candidate and checker constant: an always-200 handler fails with the honest answer key; the worker cannot write the read-only checker, but can edit `expected.json`; the unchanged checker then prints `PASS`. Controller-owned cases still reject those same candidate bytes. The repaired handler still passes. This is a five-case **CLI status-code model**, not an HTTP deployment or an LLM trial.

The opening three cases use real loopback HTTP requests and Linux bind mounts: an inherited credential reaches another project, a writable mount reaches another job, and a permitted service accepts an upload for the wrong account. Each denial is paired with a legitimate operation that remains possible.

## Reproduce

Python 3.10+ standard library; isolated experiments require disposable Linux with bubblewrap. Never feed arbitrary untrusted code into the local factory executor.

```sh
make test              # 37 protocol / evidence regression tests
make factory           # six local fixture checks; NO OS isolation
make demo              # 29 Linux isolation / loopback HTTP checks
make factory-isolated  # 11 read-only checker / gate checks
make record-all        # refresh source-bound records after source edits
make snapshot          # compile Beamer PDF and update slides/talk.pdf
make replay            # show recorded observations; no new experiment
```

Deck dependencies on Ubuntu: `texlive-latex-recommended texlive-pictures lmodern`. The PDF build rejects stale, incomplete, skipped, or reference-mode evidence and overfull TeX layouts. `make deck` never provisions a machine.

### Editable PowerPoint companion

```sh
npm install --prefix slides
make pptx              # build/nyc-talk.pptx
```

The Beamer PDF, native editable PowerPoint, spoken script, and speaker notes share one reviewed content source: [`slides/deck.json`](slides/deck.json). Edit that file and regenerate; do not edit generated talk text independently. PowerPoint dependencies are separate from the standard-library experiments.

## Evidence and boundaries

[`research/RESULTS.md`](research/RESULTS.md) maps every result class to its raw record. The 29 + 11 + 6 checks are assertions, **not vulnerability counts**. Protocol unit tests are a separate class. Multi-agent and snapshot implications are explicitly architectural inferences, not measured attack trials.

We also [audited our own previous reference gate](research/AUDIT.md): mutable bytes could retain a stale digest and receive a publication marker. The archived reproduction requires controller API access; no sandbox-to-controller exploit path was shown. The corrected local gate derives its digest from immutable bytes, tests substitution before nonce consumption, and atomically records the approved bytes with the nonce. It is a local protocol model, not a production release service.

No vendor zero-day, customer incident, model attack-success rate, kernel-escape claim, or general security certification. Five cases establish this policy only. A hash chain detects a rewrite against a separately retained anchor; it does not establish semantic correctness.

## Event and prior work

[Official event series](https://zenity.io/resources/events/ai-agent-security-summit-2026) lists New York on October 21, 2026. The 15-minute format is the session brief in this repository; the public event page is not a confirmation of a speaker's exact stage time.

Primary references and claim limits are in [the dossier](research/DOSSIER.md) and the `[Sources]` blocks in every slide's notes. Existing mechanisms are credited rather than relabeled as discoveries.

## Optional historical substrate

`make factory-boat` remains an optional credentialed execution example. It is not required or used for this final evidence path. No cloud key, environment name, or historical cloud run is needed to reproduce the talk. The local executor is not an arbitrary-code sandbox.
