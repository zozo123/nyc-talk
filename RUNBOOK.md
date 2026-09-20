# Talk runbook

## Narrative in 90 seconds

An agent gets a small job: fix a parser and publish its report.

The checker turns green, yet the parser still accepts an invalid input. We rewind and inspect four independent grants: the identity the worker inherits, the files it can change, the recipients it can send data to, and the evidence the controller trusts.

Each experiment uses fresh synthetic fixtures. Each repair blocks the unwanted action while preserving the intended operation. At the end, a restricted worker produces the correct parser. An external verifier checks frozen bytes. A separate gate accepts those bytes. The broker sends the fixed report.

The audience leaves with a concrete question for every interface: **who can refuse this action outside the worker's control?**

## Delivery arc

- **Opening:** show PASS alongside the broken parser output. Ask whether the audience would accept the patch. Hold the explanation until slide 11.
- **Setup:** make the engineering choices recognizable: pass a credential, mount files, allow a report service, run a workspace checker.
- **Escalation:** another project's data, another job's state, another account's inbox, then the operator's confidence in success.
- **Reveal:** the worker rewrote the checker. Connect this explicitly to the opening.
- **Resolution:** the restricted worker completes the original task; the same invalid input now gets rejected.
- **Close:** the request defined the task; infrastructure defined the authority. Ask the final question and pause.

Keep the 29-check count and detailed cryptographic fields in the appendix or Q&A. Use the main narrative to connect each permission to its consequence. Say once that the cases reset independently; avoid implying a cumulative intrusion or an observed customer incident. Use TALK.md for the spoken wording.

## Before presenting

1. Read the current `evidence/transcript.txt`. Confirm its mode is isolated before describing kernel-enforced results.
2. On the rehearsal Linux machine, run `make demo`. Do not weaken machine security settings to make the demo run. Use a suitable disposable Linux VM if namespaces are unavailable.
3. Run `make record snapshot` to bind the deck labels to the new evidence.
4. Keep `evidence/transcript.txt` open as an offline fallback. It is a recorded run, not a live demonstration.
5. Confirm actual speaking time and Q&A with Zenity. The public hour-long block does not establish either allocation. The 45+15 plan below is a preparation assumption.
6. Rehearse with a timer. The manuscript alone is approximately 17 minutes at 125 spoken words per minute; the expanded delivery includes narrated evidence/code walkthroughs, audience exercises and pauses. These are estimates, not a measured rehearsal.
7. Keep the PDF, this runbook and the recorded JSON available offline. Test the presentation commands before entering the room.

## On-stage commands

Use the checked-in, recorded Linux observations for a reliable offline delivery. Say “this recorded run” when showing them. The reader verifies lab source hashes and refuses reference-mode, stale or incomplete evidence. It displays only the selected act and labels observations as CONFIRMED, because an expected observation may be an unwanted action succeeding.

```sh
python3 tools/present.py credentials
python3 tools/present.py mounts
python3 tools/present.py egress
python3 tools/present.py verifier
python3 tools/present.py acceptance
python3 tools/present.py history
python3 tools/present.py final
```

Show these at slides 5, 7, 9, 11, 13, 14 and 15 respectively. Keep later acts off-screen until their reveal.

For a live run on a rehearsed Linux machine, run `make demo` once before the opening. Use `--record build/evidence/results.json` with each command to show observations from that invocation. The reader itself never executes the lab. Avoid displaying the full suite output during the opening because it reveals the verifier mechanism early.

If the live run fails, stop that attempt and use the checked-in record, identifying the switch aloud. Never present the recorded output as the result of a failed live attempt.

Each lab invocation creates a fresh temporary directory, loopback service and in-memory approval keys. The acts use independent fixtures. Temporary state is removed on normal completion and exceptions. A hard process termination may leave its temporary directory.

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

## Timing: 45-minute delivery plus 15 minutes of questions

This is the working plan for the reported 60-minute calendar block, pending organizer confirmation. The 17 main slides carry the story. The three appendix slides support questions.

| Clock | Slides | Delivery and demonstration |
|---|---|---|
| 00:00–03:00 | 1–2 | Small request, green check, broken input. Pause for the audience's acceptance decision. |
| 03:00–07:00 | 3–4 | Convenient grants, threat model, independent resets and the meaning of recorded observations. |
| 07:00–14:00 | 5–6 | Credential comparison. Trace the request and service grant table. Ask what a stronger runtime would change about the token. |
| 14:00–21:00 | 7–8 | Host bytes before and after the mount repair. Explain the fresh output control. Let the audience inventory another user of a shared directory. |
| 21:00–28:00 | 9–10 | Same service, different recipient. Inspect rejected request fields, receiving-service observations and the direct-route probe. Explain arbitrary text as a remaining release decision. |
| 28:00–35:00 | 11–12 | Reveal the checker replacement. Revisit the exact original bug. Walk through the five external cases and the producer/controller separation. |
| 35:00–40:00 | 13–14 | Follow one approval from verified bytes to the gate. Show substitution and replay. Explain the separately retained history reference. |
| 40:00–43:00 | 15 | Final restricted task and callback to `1,,3`. Show the report reaching the team. |
| 43:00–45:00 | 16–17 | Four boundary questions and the closing line. |
| 45:00–60:00 | 18–20 as needed | Questions. Use QUESTIONS.md for precise answers and evidence limits. |

The walkthrough time is for explaining observations and ownership, not waiting for commands. Before rehearsal, bookmark these code locations in `lab/run.py`: `Service.Handler.do_GET`, the mount block in `experiments`, `broker`, `verify`, `Gate`, and `chain`. Keep the checker replacement hidden until act four. Never read the entire file aloud.

### 25-minute speaking cut

Use slides 1–17. Allow 4 minutes for setup, 4 each for credentials, mounts and egress, 6 for verifier/acceptance/history, and 3 for resolution and close. Display the recorded observations. Drop the source-code walkthroughs and audience exercises. Move approval field details to questions.

### 15-minute speaking cut

Use slides 1–5, 7, 9–12, and 15–17. Allow 3 minutes for setup, 2 each for credentials, mounts and egress, 3 for the verifier reveal and independent check, and 3 for the final task and close. Compress the skipped credential and mount repair slides into the narrated before/after comparisons. On slide 12, state that approval binds the verified bytes and the controller retains an independent history reference; keep slides 13–14 for questions. No terminal switching.

### If running late

Finish the current before/after comparison. Remove the remaining audience exercises and detailed code walkthroughs. Preserve the checker reveal, the independent rejection of the broken parser, the successful restricted task, and the closing question.

## Source references

- [Linux environ(7)](https://man7.org/linux/man-pages/man7/environ.7.html)
- [Docker bind mounts](https://docs.docker.com/engine/storage/bind-mounts/)
- [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700.html)
- [SLSA artifact verification](https://slsa.dev/spec/v1.2/verifying-artifacts)
- [Bubblewrap security model](https://github.com/containers/bubblewrap)
