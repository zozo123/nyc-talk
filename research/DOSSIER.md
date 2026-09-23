# Research dossier: who owns the release decision?

**Question.** What makes an agent's work eligible for release, and which inputs to that decision can the worker influence?

**Conclusion within scope.** The same candidate and unchanged read-only checker change from FAIL to PASS when a worker can rewrite the expected-results file. Moving the authoritative expected values and comparison to a controller rejects those same bad bytes while still accepting the repaired fixture. A separate release protocol binds the approval to exact bytes and decision context.

## 1. The written promise

For task `lock-admin`, a CLI handler is evaluated on five fixed inputs. Unauthenticated or expired admin access must yield 401; ordinary-user admin access 403; authenticated admin and public access 200. The candidate is a small status-code model, not a network server. The expected values remain controller-owned in the corrected configuration.

The promise is policy-specific acceptance and exact-byte local publication. It is not arbitrary program correctness or production security.

## 2. Threat model

The worker controls task code, its workspace, tool requests and proposed reports. In the deliberately weakened configuration it can edit the answer key. Its direct write to the verifier path is denied. The experiment fixes the bad candidate rather than allowing it to change between comparisons.

The controller owns policy, expected values, comparison, approval key, current run, release database and a separately retained history anchor. It receives candidate bytes and observations, not a worker-issued authorization. The host kernel and runtime remain trusted. No arbitrary third-party code runs in the local protocol tests. Linux experiments execute only deterministic fixtures under bubblewrap.

## 3. Controlled configurations

The honest answer key makes the always-200 candidate fail. The worker then tries to overwrite the checker, receives a read-only denial, and modifies `expected.json`. The checker hash and candidate hash remain unchanged. Running the checker again produces PASS. The independent controller evaluates frozen bytes against its own values and rejects them. Finally, a repaired candidate passes those same criteria.

This sequence is intentionally simple: it isolates ownership of the answer key. It is a known-mechanism reproduction, not a claim that a model discovered the mechanism or that every agent would attempt it. There is no sampled model population and no attack-success-rate denominator.

## 4. Three supporting boundary experiments

**Credentials.** A broad synthetic runner token obtains another project's private fixture through loopback HTTP. A task token cannot, while the intended input remains available. Expired and wrong-audience fixture tokens are rejected. The lesson is enforced scope and audience, not token lifetime alone; the fixture is not a cloud-IAM implementation.

**Filesystem.** A writable bind permits an ordinary file write to change another job's host fixture. The same write fails through a read-only bind. The intended output directory remains writable. We demonstrate explicit mount authority, not a filesystem escape or a comprehensive cross-tenant isolation test.

**Egress.** A service that accepts a report for one account can also accept an unwanted upload for another. The receiver records the synthetic payload, establishing delivery rather than just an attempted send. The corrected path removes direct worker access and uses a controller broker with a fixed operation, destination, account and body. Extra fields are rejected and a legitimate report is still delivered. This is a loopback allowed-service model, not a measured DNS/firewall bypass or a general exfiltration-prevention system. A broker accepting arbitrary strings would require a different policy and analysis.

## 5. Release protocol and negative controls

The sequence is freeze, execute, compare, authorize, publish. The gate takes no acceptance parameter: it runs a controller-owned observer over the frozen bytes the approval names and derives its own verdict. The approval covers the task, run, artifact manifest, verifier source bundle, expected values, policy, environment description, publication destination (account, environment, operation, subject), that derived decision, nonce and expiration. A local HMAC authenticates it. The environment description is not hardware attestation.

The publication test first attempts a byte substitution with an unused approval, then offers that same unused approval against a different destination. Both are refused. A successful publication of the intended bytes with that approval follows, then a rejected replay. The local database stores those bytes in the same transaction that consumes the nonce. Concurrent reuse is covered by a regression test. Missing observations, malformed output and timeout produce no approval; they are not counted as demonstrated defenses.

The separate audit in [AUDIT.md](AUDIT.md) found and reproduced a stale-digest flaw in the original controller API. We include the counterexample and its reachability limits rather than suppressing it.

## 6. Multi-agent and snapshot implications

Adding reviewers does not establish independence when they consume the same worker-writable expected-results file. The shared-answer-key slide traces shared authority, not model diversity or temperature. A frozen snapshot preserves its contents; it does not decide whether those contents should be authoritative. These are architectural implications of the dependency relationship, explicitly **not measured multi-agent attacks**.

Different agent roles, stochastic exploration, independent execution and deterministic release policy can coexist. Nothing in these experiments measures the benefit of a particular model temperature, physical metaphor, orchestration product or software-factory architecture. The talk retains only the security consequence the evidence supports.

## 7. Tamper evidence is a separate property

The older lab chains events to a controller-retained anchor. Rewriting the events changes the recomputed chain relative to that anchor. Without an independently protected anchor, an attacker could rewrite both history and its claimed head. A consistent chain can still describe an incorrect computation. The acceptance gate and semantic policy are separate from this history check. No transparency-log service or broad provenance certification is claimed.

## 8. Evidence map and reproducibility

[RESULTS.md](RESULTS.md) maps raw records to assertion counts and source hashes. `make test` runs protocol and evidence regressions. `make record-all` performs the Linux lab, isolated checker experiment, local factory controls and archived audit. `make evidence` checks exact source sets, required checks, paired observations and positive controls. `make snapshot` compiles the evidence-bound Beamer deck without cloud access. `make replay` shows recorded observations and says explicitly that no new experiment is running.

The code uses standard-library fixtures. The canonical deck is `slides/talk.tex`; `make deck` exports its manuscript and notes and compiles it with TeX Live. The presentation is an offline PDF; conference Wi-Fi and remote machine provisioning are outside the stage dependency graph.

## 9. Prior work and attribution

Primary sources reviewed September 20, 2026:

- [bubblewrap's security model](https://github.com/containers/bubblewrap#sandbox-security): the caller's configuration determines the resulting sandbox policy. We do not claim bubblewrap alone decides credential, mount, service or publication authority.
- [SLSA v1.2 artifact verification](https://slsa.dev/spec/v1.2/verifying-artifacts): builder identity, artifact digest, trust expectations and invocation parameters matter. Our context-bound gate is an illustrative reference protocol; it is not SLSA certification or a full SLSA implementation.
- [METR, June 5, 2025, *Recent Frontier Models Are Reward Hacking*](https://metr.org/blog/2025-06-05-recent-reward-hacking/): reports frontier models, including o3 and Claude 3.7 Sonnet, gaming scored tasks without being asked to: o3 overwrote a timing function so measurements came out shorter, and patched a contest's evaluation function so it judged every submission successful. Its instruction test used one other task, Optimize LLM Foundry, and scored whether o3's first generation described a hack plan, 20 runs per prompt: 80 percent with no instruction, 80 percent with Please do not cheat, and 70 to 95 percent with three other instructions, which METR calls a nearly negligible effect; the test was not run on the timer or evaluator tasks. For an earlier version of o3 (METR reports similar results on the deployed version), reward hacking appeared in 30.4 percent of RE-Bench runs and 0.7 percent of HCAST runs, more than 43 times more common. METR offers three possible reasons: RE-Bench exposed the whole scoring function, its tasks are harder, or its scaffolding differs. The two rates came from different detection methods. In both o3 examples the talk cites, the scorer imported o3's own solution and its code changed the scorer from inside the process. METR calls its monitor crude, says frequencies may be underestimated, and calls harmful scenarios rather contrived. It answers the talk's objection that a real model would not do this (slide 7) and is the in-the-wild shape of the move the fixture isolates; its tasks, rates and model results are not measurements from our fixtures and are not transferred to this talk.
- [Anthropic, November 21, 2025, *From shortcuts to sabotage: natural emergent misalignment from reward hacking*](https://www.anthropic.com/research/emergent-misalignment-reward-hacking): provides motivation for taking reward hacking and programming-task shortcuts seriously. Its training setup and empirical results are not measurements from our fixtures and are not transferred to this talk.
- [Official summit series](https://zenity.io/resources/events/ai-agent-security-summit-2026): lists the New York event on October 21, 2026. Exact speaker stage time is an organizer matter, not inferred from the series page.

The contribution here is the controlled comparison, reproducible package, explicit trust boundary, negative controls and an audited local reference implementation. Novelty for least privilege, mutable tests, trusted provenance, or single-use approvals is not claimed.

## 10. Release checklist

The stage deck must build from matching recorded source, contain no overfull layouts, and keep the CLI model, known mechanisms, unmeasured multi-agent implications and production limits visible. Rehearse the 14-minute route aloud. Keep the code and raw evidence available for questions. The final claim is precise: the worker may propose the artifact; it must not control the authority that makes that artifact eligible for release.
