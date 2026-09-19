# Talk runbook

## Narrative in 90 seconds

An agent gets a small job: fix a parser and publish its report.

The checker turns green, yet the parser still accepts an invalid input. We rewind and inspect four independent grants: the identity the worker inherits, the files it can change, the recipients it can send data to, and the evidence the controller trusts.

Each experiment uses fresh synthetic fixtures. Each repair blocks the unwanted action while preserving the intended operation. At the end, a restricted worker produces the correct parser. An external verifier checks frozen bytes. A separate gate accepts those bytes. The broker sends the fixed report.

The audience leaves with a concrete question for every interface: **who can refuse this action outside the worker's control?**

## Before presenting

1. Read the current `evidence/transcript.txt`. Confirm its mode is isolated before describing kernel-enforced results.
2. On the rehearsal Linux machine, run `make demo`. Do not weaken machine security settings to make the demo run. Use a suitable disposable Linux VM if namespaces are unavailable.
3. Run `make record snapshot` to bind the deck labels to the new evidence.
4. Keep `evidence/transcript.txt` open as an offline fallback. It is a recorded run, not a live demonstration.
5. Confirm actual speaking time and Q&A with Zenity. The public hour-long block does not establish either allocation.

## Live commands

```sh
make demo
cat build/evidence/transcript.txt
```

The complete suite runs the four cases in order and ends with the legitimate task. Use the named check groups to narrate the output. Each invocation records its exit code, stdout, stderr, mount grants and network-namespace choice.

No reset command is necessary: each invocation creates a fresh temporary directory, a fresh loopback service and new in-memory approval keys. Temporary state is removed on normal completion and exceptions. A hard machine/process termination may leave its temporary directory.

## Demo beats

| Act | Reveal | Repair | Positive control |
|---|---|---|---|
| Credentials | Runner token reads another project | Task scope, audience and expiry checked by service | Task input still readable |
| Mounts | Ordinary write alters a host fixture | Same fixture mounted read-only | Fresh patch output still created |
| Egress | Same host, other account receives canary | No direct fixture-service route; exact broker operation | Controller-built report reaches team account |
| Verifier | Workspace checker exits zero on broken parser | External expected results and isolated candidate execution | Fixed parser passes five cases |

Then show the gate rejecting substitution, changed verifier identity, a stale run, a forged approval and replay. Show the changed history chain disagreeing with the controller's retained head. Finish with `final.task`.

## Technical distinctions to preserve

- This is a deterministic enforcement lab. The worker scripts represent selected actions an agent could generate. There is no live LLM, prompt-injection success rate or customer incident.
- The four cases are independent. Act 1's fixture credential is not needed for act 3's fixture upload capabilities.
- The credential and weak-egress cases intentionally share host networking to reach the loopback service. All isolated workers still receive separate user, PID and mount namespaces.
- The repaired egress worker uses a separate network namespace and has no inherited network descriptors. The probe establishes that the host-loopback fixture service is unreachable. It does not enumerate every possible covert channel.
- The mount demo changes a next-job fixture, not the verifier. The verifier demo tests ownership of the acceptance decision.
- The verifier executes candidate code in a separate worker and compares results in the controller. It never imports candidate code into its own process.
- The snapshot happens after the producing worker exits. Approval binds the frozen bytes, current run, verifier source digest, policy and a single-use nonce.
- The gate's result represents publication authorization. No external deployment occurs.
- A controller-held MAC authenticates lab approvals. A controller-held chain head detects lab history rewriting. Neither is a distributed transparency or key-management service.
- History detects rewriting. The independent verifier and gate enforce acceptance.
- Runtime isolation is necessary for the demonstrated separation. Granted credentials, files and service operations still need their own policies.

## Timing

Until Zenity confirms the slot, rehearse the 17-slide main narrative as a compact talk and keep slides 18–20 for questions. For a shorter slot, show recorded outputs instead of running the entire suite. For a longer slot, expand the four before/after demonstrations and audience questions.

## Source references

- [Linux environ(7)](https://man7.org/linux/man-pages/man7/environ.7.html)
- [Docker bind mounts](https://docs.docker.com/engine/storage/bind-mounts/)
- [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700.html)
- [SLSA artifact verification](https://slsa.dev/spec/v1.2/verifying-artifacts)
- [Bubblewrap security model](https://github.com/containers/bubblewrap)
