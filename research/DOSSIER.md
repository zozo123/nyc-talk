# Research dossier and stage-16 decision

**Yossi Eliaz | 20 September 2026 | AI Agent Security Summit, New York, 21 October 2026**

## 1. Research question

What makes an agent's work eligible for release, and how much of that decision can the worker influence? The concrete task is `lock-admin`: an unauthenticated admin request must return 401. We investigate authority provided to a worker, rather than claiming a kernel escape.

## 2. Pinned baseline

The reviewed repository baseline is `4b06c519cff2ffcc69a8471f4f861a03f08f93a0`. Its factory implemented a five-case status-code model and a digest-bound approval gate. The source was captured by GitHub Actions run `35506381406`, at packaging commit `418805e2a65cdcb4e9ed9991a18a9278b6c3cbe8`. The workflow change did not alter the baseline experiment code. The run produced a fresh 29/29 isolated Linux record and a 6/6 local factory record.

Final code identity is the exact source-hash map in `evidence/factory-results.json` and `evidence/http-results.json`. The final workflow packages its own commit ID and source archive. Do not treat a branch name as an immutable scientific pin. Preserve the commit, source archive and result files together.

## 3. Written promises

**Acceptance integrity:** a candidate that fails the controller-owned five-case policy cannot gain approval by changing a worker report or its proposed expectations.

**Release integrity:** the actual released file must match the artifact manifest authorized for the same task, run, verifier bundle, expected results, policy and execution-environment manifest, under an unused authenticated approval.

These are finite, conditional reference-implementation promises. They do not establish complete application security or resistance to code with controller privileges.

## 4. Assets and trusted parties

Assets are a synthetic private fixture, a host-side next-job file, a synthetic report recipient, the authoritative five-case policy, the approval key, and the released `handler.py`. The intended design trusts the host kernel, fixture-service authorization, controller, its object store and its approval key. Policy changes require authority outside the candidate workspace.

The worker is adversarial and may use all interfaces deliberately exposed to it. The experiments use deterministic scripted actions, not a sampled model. No commercial customer, production identity system, private dataset or third-party target is involved.

## 5. Execution substrates

`lab/run.py --mode isolated` uses real Linux namespaces and bind mounts. Its service is a controlled fixture. The fixed outbound-call case probes host-loopback reachability from a separate network namespace and invokes a narrow controller broker.

`factory/` runs committed local fixtures. Python `-I`, an empty-ish environment and a temporary working directory are **not operating-system isolation**. The candidate shares its host with the controller. Never run arbitrary hostile source through this executor. The HTTP wrapper adds real loopback requests and response status codes; it does not add a security sandbox or production authentication.

The historical optional Boat record is archived separately. It is not a newly reproduced cloud result and is not evidence of a Boat vulnerability.

## 6. Trial protocol

Change one relevant authority at a time, observe the external effect, apply a specific restriction, then prove the required operation still succeeds. Preserve exact source hashes, all observations and failures. A timeout, malformed result, skip or infrastructure error cannot count as an accepted candidate or as a demonstrated defense. Unit tests of fail-closed behavior are labeled as such.

The source-hash validator refuses empty or mismatched source maps, missing/duplicate observations, failed/skipped rows and incomplete HTTP evidence. These checks detect stale or structurally incomplete records. They do not authenticate the person who wrote a result file. Fresh CI execution and trusted distribution remain separate provenance concerns.

## 7. Credentials experiment

**Precondition:** worker receives the overbroad fixture runner token. **Action:** `GET /projects/other/private`. **Observation:** 200 and the synthetic private fixture. **Restriction:** use the task-scoped fixture token. **Negative control:** the other project returns 403. **Positive control:** the task's own input returns 200. Expired and wrong-audience fixture tokens also return 403.

Evidence: `evidence/results.json`, checks `credentials.before`, `credentials.after`, `credentials.positive`, `credentials.fixture-expired`, `credentials.fixture-wrong-audience`. This establishes fixture-service decisions. It is not a real identity-provider evaluation or proof that lifetime alone limits resource authority.

## 8. Mount experiment

**Precondition:** a host fixture directory is bind-mounted writable at `/shared`. **Action:** ordinary `Path.write_text` to `next-job.json`. **Observation:** host-side file changes. **Restriction:** read-only bind for that directory. **Negative control:** identical write is denied and host file remains unchanged. **Positive control:** legitimate output under `/output` is written.

Evidence: `mount.before`, `mount.after`, `mount.positive` in `evidence/results.json`. Persistence via snapshots and other mounted dependencies are deployment audit questions, not additional measured incidents.

## 9. Allowed-endpoint experiment

**Precondition:** worker can reach a fixture service whose routes include another account's uploads. **Action:** post the private canary to `/accounts/other/uploads`. **Observation:** 201 and stored fixture. **Restriction:** remove direct host-loopback reachability from the worker; accept only the assigned task and the `publish_report` operation at the controller broker. The broker fixes the recipient and payload.

**Negative controls:** recipient, URL and payload additions are denied; no unauthorized delivery appears; direct service probe is unreachable. **Positive control:** the legitimate team report is delivered. Evidence: `egress.*` checks. This proves one narrow channel, not complete network isolation, arbitrary text sanitization, timing-channel resistance or general data-loss prevention.

## 10. Verifier-dependency experiment

The baseline checker reads worker-writable `expected.json`. With the honest five-case expectations, the open handler fails. Set all expected outputs to 200 and the same handler passes. The checker file is read and SHA-256 measured before and after each execution; it remains `f5d8d3468bbeeee014580159053a10a4af758a11a22af3045b03abcf94922e99`.

The final HTTP wrapper requests the actual handler over loopback. Unauthenticated `/admin` returns 200. The controller-owned policy remains 401. The independent judge rejects the candidate and the gate denies publication. A byte-identical checker is insufficient when its authoritative dependencies are worker-controlled. The demonstration does not establish OS-enforced checker immutability; the narrow claim is that no checker edit was needed.

Evidence: `evidence/http-results.json` and `evidence/http-transcript.txt`; code: `factory/core.py`, `factory/http_demo.py`. A regression test deliberately changes the checker file to prove the measurement reads the file rather than returning a constant source hash.

## 11. A defect found in our own reference API

The baseline `Frozen` dataclass contained a mutable payload dictionary. Code with access to this controller-side object could change its bytes while preserving its digest field. Our recorded baseline probe obtained `PUBLISHED` for the altered object, although an independent judge rejected its actual payload. The original publication operation wrote a digest record rather than releasing a file.

Classification: **our reference implementation defect, under controller-object mutation**. We did not establish a path by which a sandboxed remote worker obtains this access. Calling this a vendor vulnerability or worker-to-controller escape would exceed the evidence.

The fix makes attached bytes immutable, checks the manifest against the bytes, loads and rehashes the controller-owned store, writes a real released file and verifies it. Unit tests reject forged digest labels, mutated manifests, corrupted or missing stored objects and symlinks. Baseline probe: `evidence/archive/baseline-probes.txt`.

## 12. Controls that isolate the mechanism

The old swap test ran after successful publication. Its denial could therefore be explained by a consumed nonce. The final order is: submit the wrong digest with an **unused** approval; observe DENIED; submit the correct artifact with **that same** approval; observe PUBLISHED; retry; observe DENIED. This separates artifact binding from replay protection.

The actual released good file returns 401 to unauthenticated admin and 200 to the authorized administrator. Its full five-case response vector is `[401, 200, 403, 200, 401]`. The open handler's vector is `[200, 200, 200, 200, 200]`. We test the released file, not merely the live workspace path or a successful publication message.

## 13. Evidence ledger

| Evidence set | Scope | Observations | Interpretation |
|---|---|---:|---|
| `evidence/results.json` | Isolated Linux fixture lab | 29 assertions | Includes unwanted successes, restrictions and positive controls |
| `evidence/factory-results.json` | Local reference protocol | 6 assertions | Intended and deliberately weakened configurations |
| `evidence/http-results.json` | Real loopback HTTP around committed fixtures | 11 assertions | Same checker, observed status codes, actual release bytes, unused swap, replay |
| `tests/` | Unit regression suite | 25 tests | Evidence refusal, actual hash measurement, mutations, bindings, store checks, fail-closed outcomes |
| `evidence/archive/` | Pinned historical material | Baseline probes + earlier factory/Boat record | Context only; not fresh final-source validation |

These are assertions and tests, not independent vulnerabilities or statistical samples. The checked-in source hashes bind each active record to the current experiment sources. The workflow independently reruns Linux, factory, HTTP and regression checks and packages the result with the exact source commit.

## 14. Prior work and contribution boundary

[Bubblewrap's own security guidance](https://github.com/containers/bubblewrap#sandbox-security) makes the caller's configuration part of the boundary. We demonstrate consequences of particular mounts and network choices rather than alleging a defect in bubblewrap.

[Anthropic's November 21, 2025 research](https://www.anthropic.com/research/emergent-misalignment-reward-hacking) studies reward hacking in deliberately selected training environments. It is an antecedent for grader manipulation, not evidence about our worker or a transferable attack rate.

[SLSA v1.2 artifact verification](https://slsa.dev/spec/v1.2/verifying-artifacts) describes checking artifact subjects and trusted provenance. Our small HMAC reference gate borrows the general requirement to bind assertions to artifacts; it does not implement or claim a SLSA level.

The contribution is a reproducible boundary-testing method, a concrete verifier-dependency counterexample, an audited release path and paired positive/negative controls. Neither test tampering nor digest binding is claimed as a novel invention.

## 15. Limits and falsifiers

The result is falsified for a claimed configuration if the forbidden operation succeeds after restriction, the required operation fails, the checker actually changes in the dependency-only case, the approved/released manifests differ, or an unused approval fails to distinguish correct from substituted artifacts. The build must refuse missing or unsuccessful evidence rather than quietly keep a slide green.

Unestablished: a remote exploit against a named factory; model discovery probability or attack-success rate; kernel-escape resistance; cgroups or seccomp; arbitrary hostile-code isolation in `factory/`; production identity validation; general DLP; exhaustive correctness; parallel publication atomicity; crash consistency; durable key management. The reference has a single trusted controller and ephemeral keys. A restart invalidates earlier approvals. Real deployment must supply strong candidate/controller isolation, protected storage and transactional release semantics.

## 16. Decision: finalize a methodology talk

**Proceed with the 15-minute accepted talk as a controlled, evidence-backed security-engineering demonstration. Do not market it as a discovered vendor zero-day or a model benchmark.**

The accepted four cases stay intact. The final narrative opens with the actual HTTP mismatch, explains its verifier-dependency cause, and closes with independent criteria plus rehashed release bytes. Claims on slides map to this ledger. Main content is 11 slides; five appendix slides carry full criteria, reproduction, the reference-API defect, limits and primary sources.

This decision records the classification earned by the experiments. It is not an external conference review or a guarantee of acceptance at another event.
