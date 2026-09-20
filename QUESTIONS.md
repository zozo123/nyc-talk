# Questions after the talk

These are speaker answers, not additional experimental claims. The examples and limits below refer to the committed lab.

## Isn't this least privilege?

Yes. The contribution is an executable way to inspect where authority enters an agent deployment. Each demonstration pairs an unwanted action with a repair and a positive control. The audience can apply that pattern to its own worker, filesystem, service and acceptance interfaces.

## What makes this about agents if there is no LLM in the demo?

An agent can generate code and requests that exercise these grants. We hold the chosen action fixed to test whether the surrounding system permits it. That isolates enforcement from the probability that a model chooses a particular action. The lab measures no model's prompt-injection susceptibility.

## Would a microVM fix these failures?

A different execution boundary can change the host attack surface. It still needs a policy for the credentials, files and service operations deliberately supplied to the guest. A valid broad token retains its service permissions. A writable checker still needs independent acceptance criteria. This lab uses Linux namespaces and makes no comparative runtime-security measurement.

## Can a short-lived token still leak data?

Yes. An unwanted read can occur before expiry. The demonstrated repair restricts the resource scope and checks audience and expiry at the service. The fixture uses opaque token strings backed by an in-memory grant table. It is not an OAuth implementation or a claim of OAuth conformance.

## Does the service really accept uploads to another account?

Our loopback fixture deliberately accepts both account paths. It represents a service where the worker has an available upload capability for another recipient. We verify receipt of synthetic data under that account. We make no claim that an arbitrary real service permits cross-account writes without authorization.

## Why not just allowlist the team URL?

That addresses the demonstrated recipient change if every route enforces the rule correctly. Contents still need a policy: an arbitrary allowed body can carry sensitive bytes. Our narrow operation fixes the recipient and constructs the body from controller-owned fields. The worker's direct route to the fixture is also unavailable.

## What about a useful report that contains agent-written text?

That is a richer release decision than this fixture implements. Decide which data the worker may read and which recipients may receive its output. A fixed schema alone cannot make an arbitrary string safe. The talk claims a repair for one controller-built report, not general data-loss prevention.

## Isn't making the checker read-only enough?

Only if the full acceptance path has the intended trust properties. Inspect the checker, its dependencies, configuration, expected values and the final comparison. Our verifier keeps expected results in the controller, executes candidate bytes in a separate worker, and compares the output externally. A protected entrypoint that imports worker-controlled logic would need further analysis.

## Can the candidate just recognize the five test inputs?

Yes. Five visible cases establish this finite acceptance test. They do not prove complete correctness. A production verifier needs a specification and evaluation strategy appropriate to the task. The demonstration separates who owns the check from how strong the check is.

## Could the producer keep changing files during verification?

The deterministic producer exits before the controller reads its bytes and creates a private snapshot. Production systems must also account for descendants, other writers, links and races in artifact collection. This fixture does not establish robust snapshotting for every adversarial filesystem behavior.

## Does the gate actually deploy anything?

No. It returns a publication decision. The controller authenticates the artifact digest, current run, verifier source digest, policy, acceptance result and a single-use nonce. A production consumer would have to preserve the binding when publishing or deploying the artifact. Our final fixture invokes the broker only after acceptance.

## Who verifies the verifier?

The controller, verifier and host are trusted in this threat model. Their implementation and updates need their own review and protection. The experiment tests the separation between a worker's proposed output and the authority that accepts it. It does not remove the trusted computing base.

## Does a hash chain make the history trustworthy?

A writer can rewrite an entire chain and recompute its links. Our controller keeps the original head outside the worker, which exposes the changed chain. The anchor is in memory. Durable retention, crash recovery, event completeness and external transparency are outside this demonstration.

## What is the difference between the gate and the history?

The gate refuses an artifact that lacks a valid approval for the current bytes and run. The retained history reference reveals a rewrite. A faithful record can still contain a bad decision, so tamper detection does not replace independent verification.

## What should I do first on Monday?

Choose one agent job. Inventory its inherited identity, mount set, possible recipients and acceptance path. Pick one unwanted action at each interface, name the component that should refuse it, and test the legitimate operation immediately afterward. Start with a disposable environment and synthetic fixtures, as this lab does.

## What remains untested here?

Live-model behavior, kernel escape resistance, cgroup limits, seccomp coverage, alternate descriptor channels, broad network noninterference, verifier resource exhaustion, complete parser correctness, durable evidence retention and a production deployment consumer. The evidence supports the specific committed fixtures and observations.

Primary mechanism references are linked in [the manuscript](TALK.md) and on slide 20. The recorded observations and their lab source digests are in [evidence/results.json](evidence/results.json).
