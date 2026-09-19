# Speaker notes

The slides use one fictional deployment with four alternate failure paths. Do not present the opening as a real incident, or the proof obligations as measured results.

## Slide 1

The accepted title and tagline are exact. This is a fictional lab walkthrough, not an observed customer incident. No DEF CON affiliation is implied by the visual style.

## Slide 2

Pause while the audience reads. The runtime dashboard looks reassuring. Now look at the three lines underneath. Which outcome required the process to escape its sandbox? These are illustrative story facts, not captured telemetry.

## Slide 3

The operator authorized one repair and a report upload. Establish this narrow task before revealing the larger privileges. We follow one deployment through four alternate failure paths, not a mandatory four-step exploit chain.

## Slide 4

Each extra permission was easy to justify during development. The security design has to survive arbitrary code execution within the intended sandbox. Ask which grant is truly required by the operator's request.

## Slide 5

A malicious repository, tool output, or model behavior can lead to adversarial actions. This talk starts after that point. We do not claim complete protection against kernel vulnerabilities, covert channels, malicious trusted services, or a compromised broker.

## Slide 6

Use a synthetic token recognized by a local mock service. Show the child performing a mock administrative action the task never required. Namespaces do not narrow a bearer token's service-side permissions. Inspect inherited descriptors and mounted credential files too.

## Slide 7

Keep broad upstream credentials in a trusted broker. Where direct token projection is necessary, scope audience, resource, operation and lifetime. Sender constraint can reduce replay exposure where available. An environment allowlist alone is not a sandbox.

## Slide 8

These are acceptance criteria, not experiment results. Keep the legitimate read as a positive control. Record token identifiers and authorization decisions, never real credentials.

## Slide 9

Change a harmless release-policy fixture. Do not use host system paths or the Docker socket as demonstration targets. The point is a granted write, not a filesystem escape. The verifier file sets up the final act.

## Slide 10

Use kernel-enforced mounts and permissions. Broker file operations must account for symlinks and rename races. A read-only checkout requires explicit patch output or a separate writable copy. Read-only prevents modification, not disclosure.

## Slide 11

Check the fixture on the host and capture the syscall failure or inaccessible path. A mocked filesystem cannot prove a real mount boundary. Run the eventual container lab on controlled Linux.

## Slide 12

Use a local multi-tenant service fixture, with no real outbound exfiltration. This is our threat-model analysis, not a claim about a vendor. Recipient checks must use authenticated service semantics, not trust a caller-supplied label.

## Slide 13

Scanning is not a universal solution. Encoding and allowed free-text fields can carry data. Prevent secret access or constrain output construction and channels at the trusted boundary. For this lab, use broker-owned report values with no arbitrary agent strings. Later tests must include redirects and alternative routes.

## Slide 14

Check the broker decision and receiving service state. A denied request log alone does not establish absence of alternative routes. Verify network policy separately from application authorization.

## Slide 15

Keep the invalid artifact identical across runs. Show the mutable acceptance mechanism accepting it, then the external checker rejecting the same bytes. Editable unit tests remain useful feedback but cannot be the sole publication authority.

## Slide 16

SLSA motivates artifact identity and trusted provenance checks. This architecture applies those ideas without claiming SLSA conformance. Separate acceptance enforcement from audit. Provenance alone does not establish semantic correctness.

## Slide 17

Hash linkage detects change relative to a trusted reference. External keys, independently retained checkpoints or independently controlled append-only storage provide that reference. Signed logs still require identity, freshness and completeness checks.

## Slide 18

Exercise the time-of-check/time-of-use gap by swapping output after verification. The gate should fetch or validate the exact digest-bound object. Bind approvals to task identity and freshness to prevent replay.

## Slide 19

Process isolation establishes enforceable separation. Each capability still needs a boundary. A microVM does not repair broad injected credentials or unsafe network permissions. Four attacks do not map automatically onto four independent products.

## Slide 20

Return to the original operator request. The agent still does useful work. The system makes explicit grants and keeps acceptance authority outside the agent.

## Slide 21

Ask the audience to apply these to one deployment. Product names are insufficient. We need concrete paths, identities, resources, operations and owners for the enforcing controls.

## Slide 22

Close the loop with the opening dashboard. Isolation may hold while granted authority allows a breach. Invite questions about the trusted computing base and the evidence required to validate each control.

## Slide 23

Primary-source references checked during preparation. No production incident attribution or conference affiliation beyond the speaker-provided NYC acceptance.

## Slide 24

Explain the residual trusted computing base, semantic limits and output-channel risks without diluting the concrete controls in the main talk.
