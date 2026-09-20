# Research dossier: which inputs decide that an agent is done?

**Yossi Eliaz | October 21, 2026 talk | evidence-backed reference experiments**

## Question and scope of contribution

What makes a coding agent's work eligible for release, and how much of that decision can the worker influence?

The contribution is a reproducible explanation and a tested reference acceptance boundary. The experiment does not claim a new vendor vulnerability. Its centerpiece is a protected checker whose transitive input remains worker-controlled: the checker reads `expected.json` from the writable workspace. Keeping `checker.py` unchanged does not keep its decision independent.

The earlier source is pinned in [BASELINE.md](BASELINE.md). The release records bind the revised source files by SHA-256. The case inventory and observations are in [RESULTS.md](RESULTS.md), with raw records under `evidence/`. The source archive included with the final bundle permits cold reproduction without relying on a moving branch name.

## Threat model

The attacker is represented by a deterministic worker program able to run code, write its workspace and candidate artifact, and use the interfaces granted to that worker. The program substitutes for arbitrary commands an agent could issue; it is not an LLM sampled under a malicious prompt. The trusted controller owns the task, original policy, expected values, receipt key and release sink. In isolated mode, bubblewrap supplies the specified namespaces and read-only/writable mounts. The host kernel remains trusted.

The deliberately weak variants grant one excessive authority: a broad runner token, another job's writable directory, a generic outbound upload, or control of a dependency used to decide acceptance. Each corrected variant removes that authority while preserving intended task functionality. This is a controlled configuration comparison, not a before/after incident report.

## Four experiments

### 1. Identity

The worker receives a fixture runner credential in its environment and retrieves a different project's private fixture through a loopback HTTP API. Replacing it with a task-scoped credential denies that request while permitting the task's own input. Separate expired and wrong-audience tokens are denied. This demonstrates the configured scope, audience and lifetime checks, not a production OAuth implementation. Short duration does not erase excessive privilege while a token is valid.

### 2. Filesystem

A writable bind mount exposes another job's `next-job.json`. An ordinary file write changes the host-side fixture. The identical attempt through a read-only bind fails, while the permitted output path remains writable. No namespace breakout is required for the excessive mount grant. Snapshot inheritance is an architectural implication: if a system snapshots such state, it must account for which later tasks inherit it. Snapshot contamination is not a separately measured experiment here.

### 3. Outbound request

The loopback upload service accepts two account paths. Restricting a worker to that service alone still permits the private fixture to reach the unintended account. The corrected path denies the direct network route and uses a controller-side broker with a closed request schema, fixed recipient and controller-constructed report body. Extra recipient, payload and URL fields are rejected without delivery. The legitimate fixed report is delivered. This establishes the tested destination and payload controls, not the elimination of every covert channel.

### 4. Acceptance dependency

The task policy is modeled by a small program that prints status codes. The original expected results require unauthenticated or expired admin access to yield 401, a normal user's admin access to yield 403, and permitted requests to yield 200. The bad candidate prints 200 for all five cases.

In isolated mode the worker tries to rewrite the checker and the read-only bind denies it. The worker instead writes expected answers of 200 to `expected.json`. The unchanged checker loads those answers and prints PASS. The controller-owned expected values reject the same candidate on three of five cases. A correct candidate passes all five and is published. The weak configuration explicitly trusts the workspace dependency; no real product's default configuration is implied.

## Corrected gate and counterfactuals

The controller freezes one bounded candidate payload, derives its manifest and identity, executes those bytes, and compares observations with controller-owned criteria. An authenticated receipt binds artifact, verifier/source bundle, policy, expected results, task, run, environment description, decision, nonce and expiry. The release operation validates against the actual immutable bytes and atomically stores those bytes with nonce consumption. The local release sink is SQLite.

The substitution test matters: first use a valid, fresh approval with different bytes and observe denial; then use that same still-unconsumed approval with the original bytes and observe publication. Without that ordering, a denial could merely be replay rejection. Additional controls change verifier launch, environment or run, tamper with a receipt, expire it, replay it and submit malformed or incomplete evidence. Rejected probes are followed by their valid counterpart where appropriate. The unit suite also makes 24 concurrent publication attempts and asserts exactly one successful insertion.

The environment manifest is an authenticated declaration of the controller's chosen configuration, not independently measured remote attestation. The verifier bundle includes the factory Python sources and its reused isolation runner. These boundaries must be supplied by a real deployment, not inferred from the presence of a signature.

## A defect found while auditing our own baseline

The previous `Frozen` object exposed a mutable file mapping and stored its digest separately. A local harness changed the payload after approval while retaining that digest; the old gate returned PUBLISHED. This is evidence of a direct in-process API-invariant defect, not evidence of a confined worker reaching controller memory. The original publication method only recorded metadata, so the result must not be described as deployment of a malicious payload.

The corrected implementation derives identity from immutable payload bytes and stores the approved bytes at publication. The old substitution experiment also attempted its swap after the good receipt was consumed, confounding identity and replay checks; the revised ordering separates them. This finding and test repair are part of the contribution, with their reachability limit stated on the appendix slide.

## Scope and limitations

All workers are deterministic fixtures. There is no measured model attack-success rate, prompt-injection success claim, customer compromise or vendor zero-day. The admin case is a status-code model rather than a web server; the credential and outbound cases do use real loopback HTTP. The release sink is a reference SQLite transaction rather than a registry, deployment or merge.

Local factory mode has no OS containment and is only for committed fixtures. Isolated mode tests specific bubblewrap boundaries and assumes a trusted host kernel. These tests do not establish kernel-escape resistance, hostile-output resource isolation, comprehensive noninterference or general production safety. Five input cases do not establish program correctness; a candidate could special-case them. Controller, criteria, key and store compromise are outside the experiment's trust model.

A hash chain detects alterations only relative to a head retained independently of the worker. Source hashes detect accidental mismatch between recordings and the source being presented, not an adversarial maintainer rewriting both. Infrastructure errors and absent evidence must remain inconclusive, not be counted as defenses. The multiagent discussion follows from shared dependencies; no ensemble or temperature experiment is reported.

## Prior work and precise relationship

[Bubblewrap's security model](https://github.com/containers/bubblewrap) explicitly makes security depend on the arguments and grants supplied by its caller. We test a small selection of those grants; we do not assess the implementation for new vulnerabilities.

[SLSA v1.2 artifact verification](https://slsa.dev/spec/v1.2/verifying-artifacts) describes checking provenance against trusted identities, expected policy and the actual artifact digest. Our receipt demonstrates local byte/context binding, not SLSA compliance or an implementation of its full provenance model.

[Anthropic, November 21, 2025](https://www.anthropic.com/research/emergent-misalignment-reward-hacking) studies reward hacking in deliberately vulnerable coding training settings. It is prior work on the broader evaluation problem. Its model observations and measured rates are not results of this deterministic experiment.

[The official event](https://zenity.io/resources/events/ai-agent-security-summit-2026) lists New York on October 21, 2026. The 15-minute delivery follows this repository's accepted lightning-talk brief.

## Reproduction and disposition

Run `make test` for regression logic. Run `make isolated` on suitable disposable Linux for both suites. Use `make record` only when deliberately replacing evidence; inspect the mode, source hashes, check identities and observations. `make deck` refuses incomplete, stale or local-only stage evidence. The CI artifact includes the source, recorded results, PDF and editable deck with checksums.

Disposition: **reproducible authority-boundary failures in deliberately weak reference configurations; corrected paired controls; one narrowly scoped defect in our earlier controller API.** This supports the talk's acceptance-boundary lesson without inventing a product exploit.
