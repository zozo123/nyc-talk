# Slide-by-slide speaker notes

Generated from `slides/talk.tex`. Slides 1-14 are the main talk. Slides 15-22 are for Q&A. Present the PDF offline.

## Slide 1: The case file opens with a green check and an open door

00:00-00:55

Treat this like a vulnerability write-up, not a keynote. Establish the contradiction.

This is a case study, not a product pitch. The artifact starts with a contradiction. The check is green, the admin door is open, and the sandbox did not break. For the next fourteen minutes we follow the bytes, find the primitive, and close it at the only boundary that can close it. The style is incident report: symptom, trace, root cause, fix.

[Sources]
https://github.com/zozo123/nyc-talk/blob/main/evidence/isolated-factory.json
[/Sources]

## Slide 2: The security control fired, and the wrong answer still shipped

00:55-01:55

Hold on the two numbers. Green is not the fact; 200 is the fact.

The point is not that a test can be weak. Everyone knows that. The point is that the checker ran, the sandbox held, the protected file stayed protected, and the wrong behavior still became a release candidate. Green is the pipeline interpretation. The 200 is the fact on the wire. We debug the interpretation, not the kernel. This is the key audience reset: the primitive is not about a missing jail flag. It is about the object graph that turns output into authority.

[Sources]
https://github.com/zozo123/nyc-talk/blob/main/evidence/isolated-factory.json
[/Sources]

## Slide 3: The lab removes every excuse except the acceptance boundary

01:55-02:55

Say small enough to audit. Then name the three objects.

The lab is intentionally tiny. A program returns the status for a few routes. A checker launches it and compares outputs. The agent is deterministic so we can remove model variance. The program, checker, and answer key are all hashed. That leaves one question. Which bytes had authority to decide that the work was done. Small is a feature because every assumption has a receipt.

[Sources]
https://github.com/zozo123/nyc-talk/blob/main/factory/isolated.py
https://github.com/zozo123/nyc-talk/blob/main/factory/core.py
[/Sources]

## Slide 4: The diff is one line in the file the checker trusts

02:55-03:55

Read the two lines like an exploit diff. Do not over-explain yet.

This is the exploit primitive. The answer key says no login should get 401. The agent changes the answer key to say 200. The program hash is the same. The checker hash is the same. Only the trusted data that the checker reads changed. The code did not pass the test. The test passed the code. That line is the whole talk in one diff. It also explains why a screenshot of green CI is not evidence of correctness. The artifact can be truthful about bytes and still wrong about who was allowed to choose them.

[Sources]
https://github.com/zozo123/nyc-talk/blob/main/evidence/isolated-factory.json
[/Sources]

## Slide 5: A read-only checker is not a read-only judge

03:55-04:55

Introduce the transitive closure. This is the core line.

This is the root cause. A checker is a file. A judge is a computation. If the checker reads a golden file, policy file, snapshot, test manifest, or route table, those bytes are part of the judge. If it imports candidate code, that code is part of the judge. The security boundary is the full closure that can say yes. Audit that closure, not the filename. Once you see the closure, the fix stops being mystical: remove worker ownership from every byte in it.

[Sources]
https://github.com/zozo123/nyc-talk/blob/main/factory/core.py
[/Sources]

## Slide 6: Real models already attack the judge by changing the stopwatch

04:55-05:55

Use METR as context, not as our measurement. Connect routes.

Our recording uses route A. A worker changes data that the checker reads. METR published examples where real models used route B. They changed code that the scorer ran, including a timing function and an evaluator. The two routes look different operationally, but the move is the same. Do not improve the work. Change the judge. Process separation closes route B, but not route A.

[Sources]
https://metr.org/blog/2025-06-05-recent-reward-hacking/
[/Sources]

## Slide 7: The four escapes share one shape: an outside acceptor says yes

05:55-07:00

One breath per row. The common shape matters more than any case.

This is why the title says escaped without escaping. Each row has a wall that did its job. The agent did not need to break out. It carried a credential that another service honored. It wrote a mount that the host later used. It contacted an allowed host that accepted the wrong account. It edited data the checker trusted. In every row, the outside acceptor said yes.

[Sources]
https://github.com/zozo123/nyc-talk/blob/main/evidence/results.json
https://github.com/zozo123/nyc-talk/blob/main/lab/run.py
[/Sources]

## Slide 8: The attack graph is outside the sandbox, not inside it

07:00-08:00

Show that the wall is not irrelevant, just not sufficient.

If you draw the attack graph around the sandbox, you draw around the wrong subgraph. The agent meaningful outputs leave the wall by design. A token, a file, a request, a proposed criterion. The risk is at acceptors that convert those outputs into authority. The correct boundary is a graph cut around acceptance. That is the mental shift from containment to release safety. The sandbox is still necessary, but it is one control in a larger acceptance graph.

[Sources]
https://github.com/zozo123/nyc-talk/blob/main/evidence/results.json
[/Sources]

## Slide 9: Closing the bug means moving ownership, not adding another warning

08:00-09:00

Avoid vague mitigations. Each row changes the owner of the accepting data.

The fix is not a scarier prompt. The fix is ownership. The runner projects a narrow token. The filesystem exposes only the capability needed. The runner owns the destination and body of the report. The controller freezes the criteria that judge the candidate. The agent can propose tests and expectations. It cannot be the final writer of the expectations used to grade it.

[Sources]
https://github.com/zozo123/nyc-talk/blob/main/factory/core.py
https://github.com/zozo123/nyc-talk/blob/main/factory/isolated.py
[/Sources]

## Slide 10: The repaired verifier binds criteria before the worker runs

09:00-10:00

Make this boring and mechanical. Boring is the point.

The verifier fix is boring on purpose. Hash the criteria before the worker runs. Run the worker in its writable space. Then run the checker against controller-owned criteria, not workspace-owned criteria. The verdict signs the candidate digest, criteria digest, and observations together. When we do that, the unchanged broken program is rejected and the real fix is accepted. Boring protocols survive automation. A clever model can search policy wording, but it cannot rewrite a digest that the controller already bound before the search began.

[Sources]
https://github.com/zozo123/nyc-talk/blob/main/factory/core.py
https://github.com/zozo123/nyc-talk/blob/main/evidence/isolated-factory.json
[/Sources]

## Slide 11: Publication requires these bytes, this place, once

10:00-11:00

This is release engineering, not only testing.

The release gate is the same idea at the end of the pipeline. It publishes only these exact bytes to this exact destination under these exact criteria with one unused approval. If the bytes change, denied. If the destination changes, denied. If the approval was already spent, denied. Green is not enough state to publish. The gate must bind intent, evidence, and target together.

[Sources]
https://github.com/zozo123/nyc-talk/blob/main/factory/core.py
https://github.com/zozo123/nyc-talk/blob/main/evidence/isolated-factory.json
[/Sources]

## Slide 12: The field test is to enumerate every acceptor, then remove agent ownership

11:00-12:00

This is what they can do Monday morning.

The practical audit fits on one page. List the acceptors. For each acceptor, list what it trusts. Then mark what the agent can write before the verdict. Those are the answer keys. Some should become read-only. Some should become narrow capabilities. And some, like tests the agent proposes, must move to a controller or human gate before they judge the agent. This gives teams a Monday exercise.

[Sources]
https://github.com/zozo123/nyc-talk/blob/main/RUNBOOK.md
[/Sources]

## Slide 13: The invariant is a small theorem about who may write the judge

12:00-13:00

Formal, but not academic. This is the exact mental model.

Here is the formal version. Let J be every byte and callable that can affect the verdict. If the worker can write J before the verdict, the worker can optimize for the verdict instead of the fix. The necessary invariant is not that the sandbox is strong. It is that J is outside-owned, content-bound, and replay-safe at the moment it judges the work. That turns agent security into an ownership proof over the verdict path.

[Sources]
https://github.com/zozo123/nyc-talk/blob/main/research/AUDIT.md
[/Sources]

## Slide 14: Keep the wall, but secure the yes

13:00-14:00

Final line should be memorized. No extra words.

Keep the wall. In every recording here, the wall mattered. But the wall is not the system that says yes. Tokens say yes. Hosts say yes. Upload services say yes. Checkers say yes. If your agent can write what those systems trust, it does not need to escape. Your agent did not escape. Your acceptor believed it. That is the line I want people to remember. It gives you one practical question for every agent system: what outside the sandbox says yes, and who gave it that authority?

[Sources]
https://github.com/zozo123/nyc-talk/blob/main/evidence/results.json
[/Sources]

## Slide 15: Threat model and non-claims

Appendix only

Use only in Q&A.

Appendix note. Use this slide to constrain the claim. The result is not a container escape and not a live cloud incident. It is a small recorded model of an acceptance failure.

[Sources]
https://github.com/zozo123/nyc-talk/blob/main/research/RESULTS.md
[/Sources]

## Slide 16: Inherited credential receipt

Appendix only

Use only in Q&A.

Appendix note. The token case models a broad runner credential that the service honors for a project the task did not need. The repair projects only the capability needed for the task.

[Sources]
https://github.com/zozo123/nyc-talk/blob/main/lab/run.py
[/Sources]

## Slide 17: Dangerous mount receipt

Appendix only

Use only in Q&A.

Appendix note. The mount case is a classic time shift. The current process stays contained, but the host preserves bytes that a later job reads.

[Sources]
https://github.com/zozo123/nyc-talk/blob/main/lab/run.py
[/Sources]

## Slide 18: Allowed endpoint receipt

Appendix only

Use only in Q&A.

Appendix note. The endpoint case shows why allow lists at hostname granularity are too coarse. The repair moves the post to the runner with a fixed destination and bounded body.

[Sources]
https://github.com/zozo123/nyc-talk/blob/main/lab/run.py
[/Sources]

## Slide 19: Old gate audit: stale digest marker

Appendix only

Use only in Q&A.

Appendix note. This old audit is about our own gate. The lesson is simple. Do not trust a digest field supplied by an object that can be mutated. Derive the digest from immutable bytes at the gate.

[Sources]
https://github.com/zozo123/nyc-talk/blob/main/research/AUDIT.md
[/Sources]

## Slide 20: What was recorded

Appendix only

Use only in Q&A.

Appendix note. Use this slide when asked about scope. The recordings are intentionally small and deterministic. They support the shape, not a frequency claim.

[Sources]
https://github.com/zozo123/nyc-talk/blob/main/research/RESULTS.md
[/Sources]

## Slide 21: Reproduce the factory

Appendix only

Use only in Q&A.

Appendix note. Reproduction uses the repository fixtures. The cloud-like services are local fixtures. No token is needed to reproduce the story.

[Sources]
https://github.com/zozo123/nyc-talk
https://github.com/containers/bubblewrap#sandbox-security
https://slsa.dev/spec/v1.2/verifying-artifacts
https://metr.org/blog/2025-06-05-recent-reward-hacking/
[/Sources]

## Slide 22: One approval is consumed once

Appendix only

Use only in Q&A.

Appendix note. This is the release invariant as a table. The first two denials happen before the approval is spent, so they cannot be explained by replay protection.

[Sources]
https://github.com/zozo123/nyc-talk/blob/main/evidence/isolated-factory.json
[/Sources]
