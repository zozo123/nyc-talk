# Result summary

**Real Linux lab:** 29 completed assertions, no skipped integration groups, in the retained CI record. The original `lab/run.py` is unchanged. Cases use synthetic fixtures and actual namespaces, mounts and host-loopback HTTP.

**Local factory:** six completed checks. The incorrect candidate false-passes both deliberately weak configurations. Fixed controller criteria reject it. The correct candidate publishes. An unconsumed approval rejects different bytes, still publishes the original bytes, and rejects subsequent replay.

**Regression suite:** 26 tests covering exact-byte publication, malformed approvals/results, fresh swap, same-key cross-run mismatch, verifier/environment/policy mismatch, object and stored-byte changes, single-use consumption, concurrent publication and missing evidence.

The local before/after audit is in `AUDIT.md`. Changes to controller memory in those robustness probes are outside the worker threat model. The local candidate executor is not a sandbox.

The exact source commit, fresh experiment outputs, test results and compiled slides are retained together by CI. Do not describe infrastructure errors as successful defenses. No live model or current cloud-VM run is part of this revision. Boat remains optional and was not rerun.
