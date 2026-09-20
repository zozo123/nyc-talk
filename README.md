# Your Agent Escaped Without Escaping the Sandbox

**Yossi Eliaz**  
Principal Engineer and Head of DevRel / Incredibuild  
**AI Agent Security Summit, New York / 21 October 2026 / 15 minutes**

> The checker passed. An unauthenticated HTTP request to `/admin` still returned `200`.
> The checker bytes had not changed. The worker changed the expected-results file it loaded.

**11 main slides + 5 Q&A appendices.** A 1,651-word spoken script targets 14 minutes including pauses, with one minute of margin. Timings are rehearsal targets, not an already measured performance.

[Stage PDF](slides/talk.pdf) | [Editable PowerPoint](slides/talk.pptx) | [Beamer source](slides/talk.tex) | [Spoken script](TALK.md) | [Speaker notes and sources](SPEAKER_NOTES.md) | [Runbook](RUNBOOK.md) | [Skeptical Q&A](QUESTIONS.md) | [Research dossier](research/DOSSIER.md)

## What the talk demonstrates

| Interface | Unwanted observation | Restriction and positive control |
|---|---|---|
| Inherited credential | Fixture runner token reads another project: `200` | Task-scoped token: `403` there, `200` on its own input |
| Writable mount | Ordinary write changes a host-side next-job file | Read-only bind denies it; legitimate patch output still works |
| Allowed endpoint | Same service accepts the private canary for another account | Direct route removed; narrow broker owns recipient/body; team report still arrives |
| Verifier dependency | Same checker and handler change from `FAIL` to `PASS` after worker expectations change | Controller-owned five-case policy rejects the open handler and releases the correct file |

The final sequence follows actual bytes: freeze, compare under controller-owned criteria, authenticate approval, rehash the stored object, release that file, and request it over HTTP. An **unused** approval rejects a swapped artifact and then accepts the correct artifact; replay is tested separately.

## Reproduce

```sh
make verify       # 25 unit tests, 6 factory assertions, 11 HTTP assertions, evidence check
make demo         # 29 isolated Linux assertions; requires bubblewrap
make deck         # validate source-bound records; compile Beamer PDF
npm install --ignore-scripts
make pptx         # native editable presentation, same content and notes
```

Python 3.10+ standard library. `make verify` uses only committed deterministic fixtures and loopback HTTP. It requires permission to bind a local port. It does **not** require cloud credentials or a model API. `make demo` needs disposable Linux with user namespaces and bubblewrap. See [RUNBOOK.md](RUNBOOK.md) for packages, commands, recording, and stage fallback.

`slides/content.json` is the shared content source. `tools/build_deck.py` generates Beamer, `TALK.md` and `SPEAKER_NOTES.md`; `tools/build_deck.js` generates editable PowerPoint. The workflow reruns experiments and generates release artifacts. After successful verification on `main`, a separate narrowly permitted job commits only the generated PDF and PPTX; experiment sources are not rewritten by that job.

## Evidence and limits

The [stage-16 decision](research/DOSSIER.md#16-decision-finalize-a-methodology-talk) approves an evidence-backed methodology talk, not a vendor zero-day claim. There are 29 Linux assertions, six local-factory assertions, eleven HTTP assertions and 25 regression tests. These are **not vulnerability counts** or a model attack-success rate.

The Linux lab and the local acceptance fixture are separate demonstrations. Python isolated mode is not an operating-system sandbox; never feed arbitrary hostile source to `factory/`. The HTTP wrapper uses synthetic authorization credentials, not a production identity provider. Five cases do not establish complete application security. The reference assumes one trusted controller; atomic concurrent publication, crash consistency, durable keys and strong executor isolation remain deployment requirements.

This review also found and fixed a defect in **our own** baseline reference API: mutable payload bytes could retain an old digest label, and publication logged a digest without releasing a file. The prerequisite was access to a controller-side object; no remote-worker exploit path was established. The [dossier](research/DOSSIER.md#11-a-defect-found-in-our-own-reference-api) and regression tests preserve that distinction.

Active results are in `evidence/`; earlier factory/Boat observations are clearly archived under `evidence/archive/`. The optional cloud adapter is not part of the final fresh evidence. Source hashes detect stale source/record combinations; they do not authenticate a record's author. Keep the workflow's commit ID, source archive and evidence together.

## Speaker framing

The accepted title and four interfaces are preserved. The final delivery describes synthetic policy violations, actual namespace/mount observations and real loopback HTTP. It makes no cgroup or kernel-escape-resistance claim. History detects a rewrite against a trusted anchor; the gate separately enforces release.

[Event page](https://zenity.io/resources/events/ai-agent-security-summit-2026)
