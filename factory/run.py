#!/usr/bin/env python3
"""Reproduce the acceptance-boundary cases with explicit runtime labels."""
from __future__ import annotations
import argparse
import json
import os
import platform
import tempfile
from pathlib import Path
from factory.core import (BAD, CASES, GOOD, SUBJECT, WORKER_EXPECTED, Gate, digest,
                          execute_frozen, execute_weak_checker, freeze, judge, source_hashes)

LAUNCH = {"executor": "python3 -I -B", "subject": SUBJECT, "compare": "controller", "cases": len(CASES)}
ACCEPT_ENV = {"role": "accept", "inherits_producer_disk": False, "expected_results_in_worker": False,
              "api_credential": "none", "runtime": "local-committed-fixtures-only"}


def run_local(store: Path, *, isolated: bool = False) -> dict:
    environment = {**ACCEPT_ENV, "runtime": "bubblewrap-readonly-candidate-no-network" if isolated
                   else "local-committed-fixtures-only"}
    gate = Gate(store)
    good, bad = freeze({SUBJECT: GOOD.encode()}), freeze({SUBJECT: BAD.encode()})
    good_out = execute_frozen(good.payload, isolated=isolated)
    bad_out = execute_frozen(bad.payload, isolated=isolated)
    good_v, bad_v = judge(good_out), judge(bad_out)
    checks = []

    def check(name: str, ok: bool, detail: str, observed: str = "successful_defense",
              config: str = "reference-intended"):
        checks.append({"check": name, "status": "PASS" if ok else "FAIL", "detail": detail,
                       "classification": {"execution_status": "completed", "observed_result": observed,
                                          "configuration": config, "attribution": "our_reference_factory",
                                          "prior_work": "known_mechanism"}})

    approve = lambda obj, accepted: gate.issue(artifact=obj, accepted=accepted, launch=LAUNCH, env_manifest=environment)
    publish = lambda receipt, obj: gate.publish(receipt, obj, LAUNCH, environment)
    approval = approve(good, good_v.get("accepted") is True)
    # Test substitution BEFORE consuming this nonce. Then positive control SAME approval.
    swap = publish(approval, bad)
    positive = publish(approval, good)
    check("intended.swap", swap == "DENIED" and positive == "PUBLISHED",
          "Fresh good approval denies bad bytes; the SAME unconsumed approval then publishes good bytes.")
    check("intended.good", good_v.get("accepted") is True and positive == "PUBLISHED"
          and gate.released_bytes(approval) == GOOD.encode(), "Five expected results match; exact approved bytes stored in release sink.")
    rejected = approve(bad, bad_v.get("accepted") is True)
    check("intended.bad", bad_v.get("accepted") is False and publish(rejected, bad) == "DENIED",
          "Open-admin status model fails three cases; rejected bytes are not released.")
    check("intended.replay", publish(approval, good) == "DENIED", "Consumed run/nonce cannot publish twice.")
    check("intended.malformed", publish({}, good) == "DENIED", "Malformed approval yields denial, not an exception.")
    fresh = approve(good, True)
    changed = {**LAUNCH, "compare": "worker"}
    check("intended.verifier", gate.publish(fresh, good, changed, environment) == "DENIED",
          "Unconsumed authentic approval denies a changed verifier launch contract.")
    check("intended.environment", gate.publish(fresh, good, LAUNCH, {**environment, "api_credential": "present"}) == "DENIED",
          "Unconsumed authentic approval denies a different acceptance environment manifest.")
    saved = gate.run; gate.run = "other-run"
    stale = publish(fresh, good); gate.run = saved
    check("intended.run", stale == "DENIED", "Same signing key, different run: approval denied.")
    forged = json.loads(json.dumps(fresh)); forged["value"]["artifact_manifest_digest"] = bad.digest
    check("intended.forgery", publish(forged, bad) == "DENIED", "Edited receipt fails authentication.")
    check("intended.positive_after_negatives", publish(fresh, good) == "PUBLISHED",
          "Denied verifier/environment/run/forgery probes did not consume the legitimate approval.")
    now = [1000.0]; timed = Gate(store / "timed", clock=lambda: now[0])
    expiring = timed.issue(artifact=good, accepted=True, launch=LAUNCH, env_manifest=environment, ttl=1)
    now[0] = 1002.0
    check("intended.expired", timed.publish(expiring, good, LAUNCH, environment) == "DENIED", "Expired approval cannot publish.")
    partial = judge([{"status": "timeout"}] * len(CASES))
    check("intended.incomplete", partial["kind"] == "no_approval", "Timeout evidence creates no approval; no attack-resistance inference.", "fail_closed_logic")
    view = good.files; view[SUBJECT] = BAD.encode()
    check("intended.immutable", good.payload == GOOD.encode() and freeze(good.files).digest == good.digest,
          "Editing an exported file view cannot alter frozen bytes or their identity.", "regression_guard")

    weak = execute_weak_checker(BAD.encode(), WORKER_EXPECTED, isolated=isolated)
    deps_ok = weak["stdout"] == "PASS" and weak["checker_sha256_before"] == weak["checker_sha256_after"]
    deps_ok = deps_ok and bad_v.get("accepted") is False
    if isolated:
        deps_ok = deps_ok and weak["checker_write_denied"] is True
    check("weakened.deps", deps_ok, "Unchanged checker accepts worker-written expected.json; controller-owned cases reject SAME bad candidate.",
          "boundary_violation", "deliberately-weakened-untrusted-dependencies")
    check("weakened.report", b"PASS\n".strip() == b"PASS" and bad_v.get("accepted") is False,
          "Detector control: a worker PASS claim accompanies a candidate the independent judge rejects.",
          "boundary_violation", "deliberately-weakened-worker-report")
    return {"mode": "isolated" if isolated else "local", "host": platform.platform(), "task": "lock-admin",
            "status": "PASS" if all(c["status"] == "PASS" for c in checks) else "FAIL",
            "good": {"artifact": good.digest, "outputs": good_out, "verdict": good_v, "published": positive},
            "bad": {"artifact": bad.digest, "outputs": bad_out, "verdict": bad_v}, "weakened_deps": weak,
            "checks": checks, "limitations": ["Deterministic fixtures; no model-driven attack or attack success rate.",
                "handler.py prints modeled status codes; it is not a deployed HTTP application.",
                "Release sink is a controller-owned SQLite record containing actual bytes, not a registry or Git merge.",
                "Local mode has no OS isolation. Isolated mode uses bubblewrap and assumes the host kernel is trusted.",
                "Controller, key, policy and store are trusted. Finite cases do not prove general correctness."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--isolated", action="store_true")
    parser.add_argument("--output", type=Path, default=Path("build/factory"))
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="nyc-factory-") as tmp:
        result = run_local(Path(tmp), isolated=args.isolated)
    record = {"local": result, "source_sha256": source_hashes(), "commit": os.environ.get("GITHUB_SHA"), "python": platform.python_version()}
    (args.output / "results.json").write_text(json.dumps(record, indent=2) + "\n")
    (args.output / "local.json").write_text(json.dumps(result, indent=2) + "\n")
    text = [f"MODE {result['mode']} / STATUS {result['status']}"]
    text += [f"{c['status']} {c['check']}: {c['detail']}" for c in result["checks"]]
    text += ["OBSERVED weak checker: " + result["weakened_deps"]["stdout"],
             "OBSERVED checker SHA before: " + result["weakened_deps"]["checker_sha256_before"],
             "OBSERVED checker SHA after:  " + result["weakened_deps"]["checker_sha256_after"],
             "OBSERVED bad candidate values: " + json.dumps([x.get("value") for x in result["bad"]["outputs"]]),
             "CONTROLLER expected values:   " + json.dumps([v for _, v in CASES])]
    (args.output / "transcript.txt").write_text("\n".join(text) + "\n")
    print("\n".join(text))
    raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
