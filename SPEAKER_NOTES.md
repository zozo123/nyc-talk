# Speaker notes

One job, four independent experiments, then a successful restricted run.
The workers are deterministic scripts. No claim of model-driven exploitation.

## Slide 1

Start with the audience's small request: fix a parser and publish its report. Let the green check invite trust before slide 2 exposes the contradiction. TALK.md contains the spoken opening. Pause after asking whether the audience would accept the patch.

## Slide 2

Let the audience notice the contradiction between PASS and the invalid parser output. Withhold the mechanism until slide 11. This is a measured synthetic result, not a customer incident. Read the opening from TALK.md and move to the convenient grants that made the task executable.

## Slide 3

The parser should accept comma-separated integers and reject empty fields. The agent needs task input, somewhere to write a patch, and a narrow report operation. Each experiment starts with its own fixtures. They are independent failure paths, not a four-step intrusion and not a customer incident.

## Slide 4

We begin after an adversarial action has been chosen. This makes enforcement reproducible. Isolated mode uses Linux user, PID and mount namespaces through bubblewrap, with a separate network namespace where specified. The service and controller remain outside the worker. Reference mode does not establish those boundaries. Read the evidence label honestly.

## Slide 5

The weak launcher passes a synthetic broad runner token into the child. It reads another project even though its task ID says parser-fix. The repaired launcher projects a task-scoped token. Repeat the identical forbidden request and the service refuses it. Then read task input successfully. Expiry and wrong-audience checks also run. Our local service uses an in-memory grant table rather than implementing OAuth.

## Slide 6

Ask what the child inherits before asking what the model intends. A short-lived token retains all its permissions until expiry. Keep broad upstream credentials outside the worker and project only the required capability. This finite lab demonstrates service-side scope, audience and expiry decisions. References: Linux environ(7) and RFC 9700.

## Slide 7

Display the mounts act with tools/present.py. Use a next-job queue fixture, separate from the verifier. This keeps filesystem and acceptance failures distinct. The attack is an ordinary write to a deliberately mounted path. In isolated mode the controller checks host bytes, resets the fixture, removes the prior output, and reruns with a read-only bind. Reference mode skips this entire integration experiment.

## Slide 8

The host constructs the mount set. A path check in code the worker can edit cannot enforce it. Our repaired demonstration keeps the same fixture visible but read-only for a direct comparison. Omit it when the task does not need to read it. Read-only access still permits disclosure. Reference: Docker bind-mount documentation.

## Slide 9

Both paths are on the same loopback endpoint. The fixture models a multi-tenant service with an available upload capability for each account. We verify that the receiving service stores the synthetic canary under the other account. A network destination and a data recipient are different policy choices. This is a local example, not a claim about a vendor.

## Slide 10

The worker emits a request on stdout. The controller treats it as untrusted input, accepts one exact schema, and constructs the report from controller-owned fields. Isolated mode gives the worker a new network namespace and tests reachability of the host loopback service. Arbitrary report strings would reopen a data channel. This operation does not establish universal freedom from covert channels.

## Slide 11

Display the verifier act with tools/present.py. This is the reveal. Return explicitly to slide 2: the parser stayed broken because the worker changed the checker. File mutation is the mechanism. Trusting that file to define acceptance is the failure. Pause before showing the independent check.

## Slide 12

The controller snapshots exact parser bytes after the producer exits. It runs those bytes in a separate worker per case and compares output with controller-held expected results. The buggy parser fails two cases. The fixed parser passes five. Candidate code never executes inside the controller process. Five cases show this defect and repair; they do not prove complete parser correctness.

## Slide 13

The controller authenticates an approval binding artifact digest, run, verifier source digest, policy and a single-use nonce. Its MAC key remains outside worker mounts and environment. We separately test a stale run with the same key, changed verifier identity, forged approval, substituted artifact and replay. The lab gate returns a publication decision; it does not deploy software externally.

## Slide 14

Change a failed verification event to success and recompute every subsequent link. The chain differs from the controller-held head. This demonstrates the need for a reference outside attacker control. The lab reference lives in controller memory, not durable transparency infrastructure. History provides evidence of rewriting. The verifier and gate enforce acceptance.

## Slide 15

This is the positive end-to-end control. In isolated mode the worker has read-only input, writable task output, no projected service credential and a separate network namespace. Publication and reporting happen only after external verification. The parser fix is deterministic fixture code, not live model output. Reference mode runs the sequence without isolation and must be described that way.

## Slide 16

Return to the four acts in order: identity, files, data release and acceptance. For each, name the component that can refuse the action outside worker control. Then test a legitimate operation. Process isolation supports the separation. The retained history reference exposes rewriting; it does not replace the verifier's decision.

## Slide 17

Return to the small original request. The task was defined in the request; its authority was defined in infrastructure. Ask the final question once and pause. The lab count and implementation details belong in the appendix and repository.

## Slide 18

Run isolated mode on a disposable Linux host that permits user namespaces. It fails when isolation is unavailable and never silently falls back. Reference mode tests policy logic but skips mount and network integration. The deck build checks recorded lab source digests and refuses stale evidence. Use tools/present.py for act-by-act recorded observations without revealing subsequent acts. RUNBOOK.md gives timeboxes and shorter cuts. QUESTIONS.md covers likely objections.

## Slide 19

Do not imply we measured model susceptibility to prompt injection or proved the absence of all sandbox escapes. The controls address named failure paths. The network probe targets the fixture endpoint. The history anchor is ephemeral. Production hardening and broader adversarial analysis remain separate engineering work.

## Slide 20

Additional implementation reference: github.com/containers/bubblewrap. These primary sources support the mechanisms discussed. The experiments are synthetic examples and do not claim OAuth or SLSA conformance. See QUESTIONS.md for the distinction between enforcement, acceptance and tamper detection.
