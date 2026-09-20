# Technical Q&A

**Is this a sandbox escape?**  
The title refers to consequences beyond the worker's task while using granted interfaces. The demos do not establish a kernel/container breakout. Their concrete subjects are credential scope, mounted state, operation scope and trusted decision inputs.

**Is this new research or a vendor zero-day?**  
It is a reproducible audit method and reference implementation. The weak configurations deliberately reproduce known authority failures. The audit additionally corrected our own gate and a confounded swap test. None of that is a vendor incident or product-level vulnerability claim.

**Did the agent discover the attack?**  
The worker is a deterministic script. That establishes a repeatable mechanism. Model discovery, prompt sensitivity, attack frequency and transfer need separate experiments.

**Was checker.py actually read-only?**  
The local factory measures that its bytes remain unchanged. It does not establish a separate OS-protected checker identity. The actual namespace/bind-mount checks are in the separate Linux lab. The talk no longer conflates these guarantees.

**Did you send an HTTP request to /admin?**  
The admin example uses a five-case command-line policy model. Cases are named `admin:none`, `admin:user` and so on. The credential and upload examples use real HTTP on loopback. No production application is deployed.

**Why does a second VM not solve it automatically?**  
A second VM can still read the same worker-written expected file. Inspect both execution isolation and ownership of the trusted comparison inputs. Several agents can share one contaminated criterion.

**Do you need secret tests?**  
The relevant property here is controller ownership of authoritative criteria. Hidden cases can improve coverage but secrecy alone does not prevent mutable dependencies or weak publication binding. Passing finite tests remains weaker than universal correctness.

**Does a hash chain prevent the false accept?**  
A controller-retained head can reveal disagreement after history changes. The judge determines acceptance and the release gate enforces it. A self-contained chain that a worker can replace is not an independent anchor.

**Are the approval and publication production-ready?**  
The gate records exact bytes and consumes a nonce in one SQLite transaction. It is a small local reference. Production needs a real release boundary, isolated hostile-candidate execution, bounded result handling, key lifecycle, durable storage and complete environment identity.

**Why is the fresh-swap test important?**  
A denial after nonce consumption cannot distinguish replay enforcement from digest enforcement. Try the swap before consumption, show the original still publishes, then test replay.

**Can the worker mutate the Frozen object?**  
Not under the stated trusted-controller boundary. The stale-label probe was a trusted-caller/API robustness test. It does not prove worker reachability. The gate now revalidates reconstructed objects and actual stored bytes as defense in depth.

**Can arbitrary report text still leak data?**  
Yes. Our broker's fixed report operation has no worker-chosen destination or free-text body. That bounded result does not establish safe general-purpose messaging, timing-channel resistance or universal noninterference.
