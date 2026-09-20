# Questions after the talk

Keep it light. Then the facts.

## Isn’t this just least privilege?

Yes. The contribution is an executable path from candidate to release, and a check for worker-controlled inputs on that path.

## Why no LLM in the demo?

We hold the action fixed and test enforcement. That is a different question from whether a model would choose the action.

## Would a microVM fix it?

It changes the host attack surface. It does not move expected results or publication off the worker. A second VM that still imports `expected.json` from the workspace is not independent.

## Isn’t a read-only checker enough?

Only if every input to the verdict is controller-owned: expected results, imports, collection path, launch config. Protecting the entrypoint while it reads worker files is the demonstrated miss.

## Did you find a zero-day in Boat / a vendor?

No. Boat, when used, is an accept-VM substrate with `noEnv`. The defect we discuss is in **our** factory’s trust in worker-shaped evidence. The PASS-file and writable-checker variants are deliberate detectors.

## Isn’t in-sandbox grading already known?

Yes. Process-exit reward hacking is documented. We do not claim that as novelty. The talk is that **after** we stopped the worker editing the checker file, the decision still depended on worker-controlled expected results and on whether we published the frozen object.

## Why five test cases? Why `/admin`?

They establish this finite policy: unauthenticated admin is 401. A candidate can overfit them. Strength of the spec is separate from who owns the spec. The payload is a merge-gated security property, not a parser quiz. It is still synthetic.

## What is the difference between the gate and the history?

The gate refuses bytes that lack a valid approval for this artifact, run, verifier, expected results and policy. History detects a rewritten log. A faithful log can still record a bad decision.

## Timeouts as a defense?

No. Timeout, malformed output and crashes produce **no approval**. That is refuse-to-ship, not evidence the boundary held.

## What should I do Monday?

Pick one agent job. Write the four questions. For acceptance, list every file the checker opens. Confirm publication reads the frozen digest, not the live workspace.
