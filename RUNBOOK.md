# Fifteen-minute lightning talk

The speaker confirmed **15 minutes**. Deliver the 12 main slides in 14 minutes and retain one minute of margin. Slides 13–15 are appendix material. The primary script is TALK.md. QUESTIONS.md supports conversations afterward.

## Delivery

Keep the PDF on screen. The recorded before/after results are already on the slides. There is no terminal switching, live suite execution, code walkthrough or scheduled audience exercise in this delivery.

Open with the green check and broken parser. Hold the checker-replacement explanation until slide 7. The four independent cases escalate through another project's data, another job's state, another recipient and the acceptance decision. Each repair preserves a legitimate operation. Close by returning to the same invalid input, which the fixed parser now rejects.

## Timing

| Clock | Slide | Beat |
|---|---|---|
| 00:00–00:30 | 1 | Small job and green check |
| 00:30–01:30 | 2 | Broken parser despite PASS |
| 01:30–02:30 | 3 | Four grants, independent fixtures and threat model |
| 02:30–04:00 | 4 | Inherited identity, task scope and positive control |
| 04:00–05:30 | 5 | Writable host fixture, read-only repair and fresh output |
| 05:30–07:30 | 6 | Same service, wrong account; fixed broker operation |
| 07:30–08:30 | 7 | Checker-replacement reveal |
| 08:30–10:00 | 8 | Independent checks reject the original bug |
| 10:00–11:30 | 9 | Approval binds bytes; external reference exposes history rewrite |
| 11:30–12:30 | 10 | Restricted job succeeds; original input now rejects |
| 12:30–13:30 | 11 | Four boundary questions |
| 13:30–14:00 | 12 | Closing question, then stop |
| 14:00–15:00 | — | Delivery margin |

These are rehearsal targets, not a claim of a measured rehearsal. Time the spoken manuscript aloud, including pauses to read the output. Do not fill the margin with another section.

## Rehearsal checkpoints

- At 05:30, start egress on slide 6.
- At 07:30, reveal the checker on slide 7.
- At 11:30, return to the successful task on slide 10.
- At 13:30, start the closing on slide 12.

If behind, remove the launch-environment explanation from slide 4, the upload-capability explanation from slide 6, and the list of approval fields from slide 9. Preserve each before/after result and positive control. Say once that the examples are synthetic independent experiments. Keep the original-bug callback and closing intact.

For slide 9 under time pressure: “The gate accepts only the verified bytes for this run. The controller retains an independent history reference, so rewriting the record is detectable. Acceptance and tamper detection have separate jobs.” Then advance.

## Before presenting

1. Open `slides/talk.pdf` offline. Verify 15 pages and that slide 12 is the closing.
2. Read `evidence/transcript.txt`: it labels the recorded run as isolated. Describe these as recorded results, not an experiment executed in the room.
3. Rehearse the script with a timer. Keep the appendix out of the timed run.
4. Keep the local PDF and repository link available. The talk needs no network connection.

## Optional reproduction outside the lightning talk

```sh
make demo       # strict Linux namespace, mount and network experiments
make reference  # policy logic only; integration checks explicitly skipped
make deck       # verify evidence, export notes, compile the PDF
```

Actual isolation needs a disposable Linux host with bubblewrap and working unprivileged user namespaces. An unavailable isolation capability fails rather than falling back. Do not weaken machine security settings to make a demo work. Each invocation creates fresh temporary fixtures and keys, with cleanup on normal completion and exceptions. Hard termination can leave temporary state.

Display one recorded act for a later technical walkthrough:

```sh
python3 tools/present.py credentials
python3 tools/present.py mounts
python3 tools/present.py egress
python3 tools/present.py verifier
python3 tools/present.py acceptance
python3 tools/present.py history
python3 tools/present.py final
```

The reader checks source hashes and refuses stale, reference-mode or incomplete observations. CONFIRMED means the stated observation occurred; that can include an unwanted action succeeding. It never executes a new experiment. To inspect a fresh successful run, add `--record build/evidence/results.json`. Identify the record being shown accurately.

## Technical distinctions

- Worker scripts choose deterministic actions. There is no live LLM, prompt-injection success rate or customer incident.
- The four cases are independent. Act 1's credential is not a prerequisite for act 3's upload capability.
- Credential and weak-egress workers share host networking deliberately. Isolated workers receive separate user, PID and mount namespaces.
- Repaired egress uses a separate network namespace and tests the direct route to the host-loopback fixture. This does not enumerate every data channel.
- The mount experiment changes a next-job fixture. The verifier experiment changes the workspace checker. Keep the two consequences distinct.
- Candidate execution happens in a separate worker. Expected outputs and comparison remain in the controller. Five cases demonstrate this repair, not complete correctness.
- The deterministic producer exits before the controller snapshots bytes. Robust collection from arbitrary malicious processes and filesystems needs further engineering.
- The gate returns a publication decision; it performs no external deployment. Its approval binds artifact, current run, verifier source digest, policy and single-use nonce.
- The controller-held MAC key authenticates approvals. The controller-held original chain head detects rewriting. The history reference is ephemeral.
- The verifier and gate enforce acceptance. History supplies evidence of rewriting. Process isolation separates the worker from these trusted components.

Primary mechanism sources are linked in TALK.md and on slide 15. The accepted abstract remains verbatim in README.md.
