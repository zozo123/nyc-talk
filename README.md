# Your Agent Escaped Without Escaping the Sandbox

**Yossi Eliaz**  
**Principal Engineer and Head of DevRel at Incredibuild.com**

NYC · AI Agent Security Summit · October 21, 2026

## Deck

[Read the PDF](slides/talk.pdf) · [LaTeX source](slides/talk.tex) · [Speaker notes](SPEAKER_NOTES.md)

28 slides (26 main + 2 appendix), in a dark security-conference style. A single fictional parser-fix task connects four failure paths. The terminal snippets are illustrative; runnable demos remain planned. No affiliation with DEF CON is implied.

Build with TeX Live (Beamer, Latin Modern, listings):

```sh
make
```

The PDF is written to `build/talk.pdf`. The checked-in `slides/talk.pdf` is the reviewed snapshot. Speaker notes also live in the LaTeX `\\note{}` commands.

## Accepted Sessionize abstract

> Every namespace and cgroup can work exactly as designed and an agent can still cause a real breach. This talk demonstrates four non-escape escapes: inherited credentials, dangerous mounts, exfiltration through an allowed endpoint, and verifier tampering. Then we close each one at the layer that can actually enforce it: real process isolation, capability-scoped filesystems, short-lived credential projection, and tamper-evident execution history. You leave with four boundaries you can check against your own agent deployment.

Accepted title, abstract, tagline, and status supplied by the speaker from Sessionize.

## Schedule: confirmation needed

The speaker reports a public schedule entry for **October 21, 15:45–16:45, Room 1**. That is a 60-minute calendar block; the actual speaking time and Q&A allocation still need confirmation from Zenity. Do not assume either a 15-minute talk or 60 minutes of speaking time. This modular draft proceeds at the speaker's request. Final pacing remains pending that confirmation.

## Core argument

A process can stay inside its sandbox while using authority that should never have been available to it. For every demo, ask: **which authority crossed which boundary, and which component can refuse it?**

## Four demos to build

These are demo specifications, not implemented or validated demonstrations. Use synthetic data and local fixtures throughout.

| Scenario | Deliberately weak setup | Enforcing control | Evidence to show |
|---|---|---|---|
| Inherited credentials | Child process receives a synthetic parent credential | Clean environment and closed inherited descriptors; brokered, audience- and action-scoped credentials with expiry | Forbidden action succeeds before; denied after; intended action still works |
| Dangerous mounts | Agent can write a fixture outside its intended workspace through an overbroad bind mount | Minimal mount set, read-only inputs, bounded writable outputs, no runtime control socket | Out-of-scope fixture changes before; remains unchanged after |
| Allowed-endpoint exfiltration | Mock allowed service accepts synthetic private data in an upload | External broker validates operation, destination account, and data scope; isolate workloads with secrets from unrestricted egress | Mock unauthorized recipient receives data before; denied after; permitted upload succeeds |
| Verifier tampering | Agent can edit the checker or expected result used for acceptance | Verifier and policy outside agent write authority; immutable input/artifact digests; externally anchored execution history | Invalid artifact passes mutable checker before; external verifier rejects it after |

Process isolation provides a foundation; it cannot revoke credentials or mounts deliberately granted to a process. Short-lived credentials still require narrow authority. A hostname allowlist alone does not establish a safe recipient. Tamper-evident history supports detection and audit; trusted verification and publication gates enforce acceptance.

## Talk structure

1. **Opening:** “The sandbox reports success. The breach already happened.”
2. **Threat model:** the agent controls its code and writable workspace; the host, broker, and external verifier are trusted.
3. **Four acts:** show a failing boundary, identify the granted authority, enforce a control outside the agent, rerun the same action.
4. **Synthesis:** connect execution, filesystem, authority/egress, and evidence boundaries.
5. **Audience takeaway:** four questions to use in a deployment review.
6. **Q&A:** time allocation pending organizer confirmation.

For each act, preserve the same sequence: intended task → adversarial action → observed outcome → enforcing control → negative and positive controls.

## Four boundaries to check

- **Execution:** Which processes, descriptors, identities, and host interfaces can agent code reach?
- **Filesystem:** Which exact inputs, outputs, mounts, and control sockets are accessible?
- **Authority and egress:** Which actions, recipients, accounts, payloads, and credential lifetimes are permitted?
- **Evidence:** Can the agent rewrite its verifier, policy, expected results, or the history used to approve publication?

## Build plan

- [ ] Confirm speaking time, Q&A, room setup, and live-demo connectivity with Zenity.
- [ ] Implement four local, synthetic before/after demos.
- [ ] Assert both blocked attacks and successful legitimate operations.
- [ ] Record deterministic fallback transcripts and videos.
- [x] Build a modular LaTeX draft and compiled PDF.
- [ ] Adjust pacing after the duration is confirmed.
- [ ] Rehearse to the confirmed time budget.
- [ ] Publish audience checklist and reproducible demo instructions.

## Demo acceptance criteria

Each demo must have a one-command reset, synthetic fixtures, explicit expected outcomes, recorded exit status, and a repeatable before/after run. No real credentials, external exfiltration targets, privileged host mounts, or production services are needed. Clearly distinguish simulations from isolation mechanisms actually exercised.

## Organizer question

“Could you confirm the speaking time and Q&A allocation for ‘Your Agent Escaped Without Escaping the Sandbox’? The public schedule shows October 21, 15:45–16:45 in Room 1. Is that a full session or a shared block, and what time budget should I prepare for?”

This question is prepared here; it has not been sent.
