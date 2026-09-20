# Skeptical Q&A

**What is the actual contribution?**
A small, reproducible set of authority-boundary experiments and a corrected acceptance gate, with explicit negative and legitimate-operation controls. The central demonstration traces acceptance through an unchanged checker into worker-controlled expectations. These underlying security mechanisms are known; this talk does not claim to have invented test tampering or capability security.

**Did an LLM discover or execute these attacks?**
No. Deterministic fixture programs exercise the authority that a code-running agent would receive. They isolate an enforcement mechanism without confounding it with sampling, prompt quality or model compliance. They establish reachability in these fixtures, not frequency in deployed agents or a model attack-success rate.

**Is this a container or VM escape?**
No kernel escape is asserted. The selected interfaces authorize a cross-project read, another job's write, delivery to an unintended account, or an incorrect acceptance decision while the workload remains within the configured process boundaries. The deliberately permissive configurations are labeled in the records.

**Was the checker actually protected?**
In isolated factory mode its directory is a read-only bind mount. The worker attempts a write and the operation is denied. Its SHA-256 is checked before and after. Its dependency, `expected.json`, is in the writable workspace. Local mode only reproduces the logic and does not claim that operating-system protection.

**Why not give a second agent or machine the checker?**
If it loads the same worker-controlled expected answers, location or model identity does not make those criteria independent. The talk's multiagent slide is an architectural implication of that dependency, not a new experiment measuring ensembles or temperature effects.

**Could the candidate just special-case the five tests?**
Yes. Finite deterministic cases establish this specified policy for the tested inputs. They do not prove general application security, hidden-input correctness or an ungameable evaluation. Coverage and secure execution are separate requirements.

**Does a signed receipt prove the decision is correct?**
No. Authentication identifies which trusted authority approved which bytes under which context. That authority and its criteria must be sound. A receipt over a bad policy remains a bad decision. The comparison is controller-owned; worker stdout is a candidate observation, never an authorization to publish.

**What does "publish" do here?**
It inserts the actual frozen payload and manifest into a controller-owned SQLite release record while consuming its run/nonce in the same transaction. That is a reference release sink, not a registry upload, deployed web application or Git merge. The tests read back and compare the released bytes.

**Was the earlier mutable-map defect a sandbox vulnerability?**
The old API allowed a direct in-process caller to change `Frozen.files` while its stored digest remained unchanged; the gate returned `PUBLISHED`. That proves an API-invariant defect in our own code. It does not show a confined worker could mutate controller memory, and the old release path stored only metadata. The appendix makes this distinction explicit.

**How do you know substitution was really checked?**
The new experiment attempts a different candidate with a fresh, otherwise valid, unconsumed approval, then publishes the original candidate with that same approval. This separates identity checking from a denial caused merely by already-used approval. Parallel calls are also tested: 24 attempts against one receipt yield one publication in the regression test.

**Is this safe for arbitrary hostile programs?**
No such production claim is made. Local mode is for committed fixtures only. Isolated mode relies on bubblewrap's configured namespaces and mounts and a trusted host kernel. Hostile-output denial of service, kernel bugs, all covert channels, remote attestation and production deployment integration are not established here.

**Are short-lived credentials sufficient?**
Lifetime limits duration, not the authority available during that duration. This fixture separately checks task scope, audience and expiry. It also checks that the legitimate task input remains accessible. Do not hand the worker the runner credential merely because it expires soon.

**Does an allowed hostname prevent exfiltration?**
The fixture demonstrates why it need not: the same service accepts uploads under different account paths. The corrected broker owns the recipient and body, rejects extra request fields, and the worker lacks a direct network route. This proves those controls in this setup, not complete information-flow security for every protocol.

**Does a hash chain prevent tampering?**
A chain can reveal alteration relative to a head retained outside the worker. A worker able to rewrite both the history and its trusted head could construct another consistent chain. Logging does not authorize publication and does not establish the semantic correctness of a result.

**What happens if the controller is compromised?**
The trust model fails. The controller, policy, key, run identity and publication store are explicitly trusted. A real deployment must keep those outside the worker's capabilities and protect their administrative path. This reference does not claim a second VM alone establishes that property.

**How should someone reproduce and extend it?**
Use the pinned source and `make isolated` on disposable Linux, inspect both JSON records and matching transcripts, then `make test`. Add an independently owned policy and a negative/positive pair for each new authority. Keep infrastructure errors, rejection, successful exploitation and absent evidence distinct.
