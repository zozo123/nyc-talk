# Final result summary

| Scenario | Observed result | Classification |
|---|---|---|
| Overbroad fixture credential | Other project 200; scoped token 403; own input 200 | Controlled authority violation and successful restriction |
| Writable host bind | Host file changed; read-only bind denies; output still written | Controlled authority violation and successful restriction |
| Allowed host, other account | Private canary uploaded; direct route/broker restriction prevents delivery; team report delivered | Narrow, controlled disclosure channel |
| Unchanged checker, worker expectations | FAIL becomes PASS; unauthenticated HTTP `/admin` remains 200 | Deliberately weakened verifier dependency |
| Independent five-case policy | Open handler denied; good handler actually released | Reference protocol behavior |
| Fresh approval and wrong digest | Wrong artifact denied, same approval accepts correct artifact | Artifact binding tested independently of nonce consumption |
| Reuse after publication | Denied | Sequential replay protection |
| Mutated baseline Frozen payload | Baseline gate accepted unchanged label | Our reference-API defect; no remote exploit path established |
| Actual final released file | HTTP vector `[401, 200, 403, 200, 401]` | Observed release bytes and finite policy |

Active records: 29 isolated-Linux assertions, six local-factory assertions, eleven HTTP assertions. Regression suite: 25 unit tests. These are not vulnerability counts or statistical samples. See [DOSSIER.md](DOSSIER.md) for pins, prerequisites, sources, limitations and the stage-16 decision.

The final talk does not claim a vendor zero-day, customer incident, model attack-success rate, kernel-escape resistance, general DLP or production-grade concurrent publication. Historical cloud observations are archived, not represented as fresh runs.
