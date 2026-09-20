# Result ledger

The authoritative observations are `evidence/results.json` and `evidence/factory-results.json`, with adjacent transcripts. The build validates exact source-hash sets, isolated runtime labels and complete expected check-name sets before compiling the stage PDF. A stale or local-only record cannot satisfy that gate.

| Experiment | Deliberately weak observation | Corrected negative control | Legitimate-operation control |
|---|---|---|---|
| Inherited credential | Other project's private fixture: HTTP 200 | Task scope, expired token and wrong audience denied | Task's own input: HTTP 200 |
| Writable mount | Host-side next-job fixture is changed | Same write denied by read-only bind | Explicit output write succeeds |
| Allowed service | Private fixture delivered to another account | Extra destination/payload/URL fields denied; no delivery; direct route unavailable | Broker delivers the fixed team report |
| Verifier dependency | Read-only, unchanged checker prints PASS after worker writes expected answers | Controller-owned cases reject the same bad candidate | Good candidate matches all five cases and its exact bytes are stored |

The bad admin status model outputs `[200, 200, 200, 200, 200]`; the controller expects `[401, 200, 403, 200, 401]`. These are subprocess status-model values, not captured HTTP `/admin` responses. The unchanged checker SHA-256 is `f5d8d3468bbeeee014580159053a10a4af758a11a22af3045b03abcf94922e99`.

## Coverage counts

- Isolation lab: 29 assertions, including deliberately weak detectors and successful controls.
- Revised factory: 15 assertions, including byte substitution, positive release, rejection, replay, malformed/context/run/forgery/expiry failures and dependency tampering.
- Unit suite: 15 tests, including 24 parallel publish attempts against one receipt and evidence-manifest failure cases.

These counts are not independent vulnerabilities, statistical trials or model success rates. The input cases are small and deterministic. Infrastructure failure is never reported as successful defense. Read the classification attached to each assertion rather than treating every PASS as a defended attack.

The source revision containing these records and its CI run identify the execution. The main-slide timing is a planned 14-minute delivery, not a measured speaker rehearsal.
