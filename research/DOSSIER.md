# Research dossier and claim ledger

**Question:** what makes an agent's work eligible for release, and which inputs to that decision can the worker influence?

**Written promise:** a worker can submit candidate bytes, but cannot change the controller's criteria or use an approval for different bytes or another run. The exact invariants and trusted base are in `INVARIANTS.md`; the baseline revision is in `BASELINE.md`.

## Configurations

| Configuration | Worker-controlled object | Independent observation | Classification |
|---|---|---|---|
| Broad inherited credential | Injected runner credential and requested path | Another-project fixture returns 200 | Deliberately broad authority |
| Task credential | Task-scoped token | Other project 403; intended input 200 | Successful scoped control in this service |
| Writable shared mount | Next-job path | Host fixture changes | Deliberately broad filesystem authority |
| Read-only shared mount | Attempted same write | Host fixture unchanged; output still writable | Successful configured mount control |
| Broad allowed service | Account path and payload | Wrong-account fixture stored | Deliberately broad operation authority |
| Fixed report broker | Exact request operation/task only | Extra fields denied; direct route unreachable; report delivered | Successful bounded-operation control |
| Worker PASS report | PASS file | Weak controller accepts independently rejected candidate | Deliberate false-accept detector |
| Worker expectations | `expected.json` | Unchanged checker PASS; fixed criteria reject | Deliberate dependency-boundary reproduction |
| Intended factory | Candidate only | Good accepted; bad rejected; fresh swap/replay denied | Finite-case acceptance and publication controls |

## Evidence discipline

`lab/run.py` is the real Linux namespace/mount and synthetic loopback-service experiment. `factory/` is a local reference protocol using committed deterministic candidate fixtures. An admin case is a command-line input/output pair; it is not a deployed HTTP application. Publication stores bytes in SQLite; it is not a production release.

The transcript says PASS when an expected observation occurs, including an unwanted success in a deliberately weak configuration. PASS is not synonymous with a secure configuration. Counts must always say assertions, checks or tests, never vulnerabilities.

The scripts run without an LLM to isolate the mechanism. We did not evaluate discovery probability, prompting, model rates, agent collusion or model-to-model transfer. The multi-agent slide is a dependency inference: shared writable criteria can influence all consumers. Snapshot propagation is likewise a deployment implication rather than a measured experiment here.

Every restricted configuration preserves a positive task path. Infrastructure failures, timeouts and malformed results produce no approval and are not classified as successful defenses. Source hashes bind records to files but do not themselves authenticate execution; the trusted CI run and retained artifact supply the execution context.

## Contribution and limits

The delivered contribution is a reproducible four-boundary audit and a corrected reference release gate, with a staged unchanged-checker reveal and explicit classification. This builds on least authority, trusted verification and subject-bound provenance; it does not claim to invent them.

Primary related work: Bubblewrap's documented policy-dependent guarantees; SLSA v1.2 artifact/provenance verification; Anthropic's November 2025 programming-task reward-hacking research. These motivate the framing without supplying attack-rate estimates for our fixtures.

Remaining deployment work includes an isolated executor for hostile candidates, bounded transport/output handling, complete runtime/environment identity, a real release authority integration and stronger task coverage. A correct result on five cases can still be wrong on an untested input. The reference's trusted controller APIs are not intended to be exposed to workers.
