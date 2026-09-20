#!/usr/bin/env python3
"""Three labeled configurations. Local by default. Boat is optional substrate."""
from __future__ import annotations

import argparse
import json
import os
import platform
import tempfile
import traceback
import uuid
from pathlib import Path

from factory.core import (
    BAD,
    CASES,
    GOOD,
    SUBJECT,
    TASK,
    WEAK_CHECKER,
    WORKER_EXPECTED,
    Frozen,
    Gate,
    digest,
    execute_frozen,
    execute_weak_checker,
    freeze,
    judge,
    persist,
)

ROOT = Path(__file__).resolve().parents[1]
LAUNCH = {
    "executor": "python3 -I -B",
    "subject": SUBJECT,
    "compare": "controller",
    "cases": len(CASES),
}
ACCEPT_ENV = {
    "role": "accept",
    "inherits_producer_disk": False,
    "checker_in_vm": False,
    "expected_results_in_vm": False,
    "api_credential": "none",
}


def classify(execution, observed, configuration, attribution, prior):
    return {
        "execution_status": execution,
        "observed_result": observed,
        "configuration": configuration,
        "attribution": attribution,
        "prior_work": prior,
    }


def intended(store: Path, candidate: bytes) -> dict:
    frozen = freeze({SUBJECT: candidate})
    persist(frozen, store)
    outputs = execute_frozen(frozen.files[SUBJECT])
    verdict = judge(outputs)
    gate = Gate(store)
    published = "NO_APPROVAL"
    if verdict["kind"] == "verdict":
        approval = gate.issue(
            artifact=frozen, accepted=verdict["accepted"],
            launch=LAUNCH, env_manifest=ACCEPT_ENV,
        )
        if verdict["accepted"]:
            swapped = freeze({SUBJECT: BAD.encode() if candidate != BAD.encode() else GOOD.encode()})
            swap = gate.replay_or_swap(approval, swapped, LAUNCH, ACCEPT_ENV)
            published = gate.publish(approval, frozen, LAUNCH, ACCEPT_ENV)
            if gate.published_bytes(approval["value"]["nonce"]) != candidate:
                raise AssertionError("published bytes differ from evaluated bytes")
            replay = gate.replay_or_swap(approval, frozen, LAUNCH, ACCEPT_ENV)
        else:
            published = "NOT_PUBLISHED"
            swap = "n/a"
            replay = "n/a"
    else:
        swap = "n/a"
        replay = "n/a"
    return {
        "config": "reference-intended",
        "artifact": frozen.digest,
        "outputs": outputs,
        "verdict": verdict,
        "published": published,
        "swap_after_freeze": swap,
        "replay": replay,
        "worker_pass_file_consulted": False,
    }


def weakened_report(candidate: bytes) -> dict:
    """Deliberate defect: controller treats a worker PASS file as acceptance."""
    workspace = {SUBJECT: candidate, "PASS.txt": b"PASS\n"}
    trusted_report = workspace["PASS.txt"].strip() == b"PASS"
    real = judge(execute_frozen(candidate))
    return {
        "config": "deliberately-weakened-worker-report",
        "controller_used_worker_report": True,
        "worker_report": "PASS",
        "controller_decision": "accept" if trusted_report else "reject",
        "independent_verdict": real,
        "checker_edited": False,
    }


def weakened_deps(candidate: bytes) -> dict:
    """Protected checker file. Worker-controlled expected.json in the same cwd."""
    result = execute_weak_checker(candidate, WORKER_EXPECTED)
    independent = judge(execute_frozen(candidate))
    return {
        "config": "deliberately-weakened-untrusted-deps",
        "checker_sha256": digest(WEAK_CHECKER.encode()),
        "checker_stdout": result["stdout"],
        "checker_exit": result["exit"],
        "worker_expected_sha256": result["expected_sha256"],
        "independent_verdict": independent,
        "checker_file_changed": result["checker_sha256"] != digest(WEAK_CHECKER.encode()),
    }


def run_local(store: Path) -> dict:
    good = intended(store, GOOD.encode())
    bad = intended(store, BAD.encode())
    report = weakened_report(BAD.encode())
    deps = weakened_deps(BAD.encode())
    checks = []

    def check(name, passed, detail, classification):
        checks.append({
            "check": name,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "classification": classification,
        })

    check(
        "intended.good",
        good["verdict"].get("accepted") is True and good["published"] == "PUBLISHED",
        "Frozen locked-admin fixture is accepted; exact bytes are stored in the publication database.",
        classify("completed", "successful_defense", "reference-intended",
                 "our_factory", "known_mechanism"),
    )
    check(
        "intended.bad",
        good["verdict"].get("accepted") is True and bad["verdict"].get("accepted") is False
        and bad["published"] == "NOT_PUBLISHED",
        "Frozen open-admin handler is rejected. No publication.",
        classify("completed", "successful_defense", "reference-intended",
                 "our_factory", "known_mechanism"),
    )
    check(
        "intended.swap",
        good.get("swap_after_freeze") == "DENIED",
        "Fresh, unused approval rejects substituted bytes, then still publishes the intended bytes.",
        classify("completed", "successful_defense", "reference-intended",
                 "our_factory", "known_mechanism"),
    )
    check(
        "intended.replay",
        good.get("replay") == "DENIED",
        "Consumed approval cannot publish twice; nonce and published bytes commit in one SQLite transaction.",
        classify("completed", "successful_defense", "reference-intended",
                 "our_factory", "known_mechanism"),
    )
    check(
        "weakened.report",
        report["controller_decision"] == "accept"
        and report["independent_verdict"].get("accepted") is False
        and report["checker_edited"] is False,
        "Detector: worker PASS file accepted an open /admin the independent judge rejects.",
        classify("completed", "boundary_violation", "deliberately-weakened-worker-report",
                 "our_factory", "known_mechanism"),
    )
    check(
        "weakened.deps",
        deps["checker_stdout"] == "PASS"
        and deps["checker_file_changed"] is False
        and deps["independent_verdict"].get("accepted") is False,
        "Detector: unchanged checker still PASSed via worker expected.json (local logic run).",
        classify("completed", "boundary_violation", "deliberately-weakened-untrusted-deps",
                 "our_factory", "known_reproduction"),
    )
    failed = [c for c in checks if c["status"] == "FAIL"]
    return {
        "mode": "local",
        "host": platform.platform(),
        "task": TASK,
        "status": "PASS" if not failed else "FAIL",
        "good": good,
        "bad": bad,
        "weakened_report": report,
        "weakened_deps": deps,
        "checks": checks,
    }


def run_boat(store: Path) -> dict:
    from factory.boat import Boat, BoatError

    boat = Boat()
    sandbox_id = None
    ledger = {
        "execution_status": "not_run",
        "sandbox_id": None,
        "commands": 0,
        "stopped": False,
    }
    try:
        created = boat.create(
            name="nyc-talk-accept",
            ttl=480,
            no_env=True,
            idempotency=str(uuid.uuid4()),
        )
        sandbox = created.get("sandbox") or created
        sandbox_id = sandbox["id"]
        ledger["sandbox_id"] = sandbox_id
        boat.wait_ready(sandbox_id)
        ledger["execution_status"] = "running"

        def eval_on_boat(source: str) -> list[dict]:
            boat.write_file(sandbox_id, f"/tmp/candidate/{SUBJECT}", source)
            ledger["commands"] += 1
            outputs = []
            for value, _expected in CASES:
                quoted = json.dumps(value)
                result = boat.command(
                    sandbox_id,
                    f"python3 -I -B /tmp/candidate/{SUBJECT} {quoted}",
                    timeout_seconds=20,
                )
                ledger["commands"] += 1
                if result.get("timedOut"):
                    outputs.append({"status": "timeout"})
                    continue
                if not result.get("success"):
                    outputs.append({"status": "error", "code": result.get("exitCode")})
                    continue
                try:
                    outputs.append({"status": "ok", "value": json.loads(result.get("stdout") or "")})
                except json.JSONDecodeError:
                    outputs.append({"status": "malformed"})
            return outputs

        good_out = eval_on_boat(GOOD)
        bad_out = eval_on_boat(BAD)
        good_v = judge(good_out)
        bad_v = judge(bad_out)
        boat.stop(sandbox_id)
        ledger["stopped"] = True
        ledger["execution_status"] = "completed"
        ok = (
            good_v.get("kind") == "verdict" and good_v.get("accepted") is True
            and bad_v.get("kind") == "verdict" and bad_v.get("accepted") is False
        )
        return {
            "mode": "boat",
            "status": "PASS" if ok else "FAIL",
            "ledger": ledger,
            "good": good_v,
            "bad": bad_v,
            "no_env": True,
            "idle_not_used_as_quiescence": True,
            "classification": classify(
                "completed" if ok else "completed",
                "successful_defense" if ok else "inconclusive",
                "reference-intended",
                "our_factory",
                "known_mechanism",
            ),
        }
    except (BoatError, TimeoutError, KeyError, OSError) as error:
        if sandbox_id:
            try:
                boat.stop(sandbox_id)
                ledger["stopped"] = True
            except Exception:
                pass
        ledger["execution_status"] = "infrastructure_error"
        ledger["error_type"] = type(error).__name__
        return {
            "mode": "boat",
            "status": "INFRA",
            "ledger": ledger,
            "classification": classify(
                "infrastructure_error", "inconclusive",
                "reference-intended", "our_factory", "known_mechanism",
            ),
            "error": str(error)[:400],
        }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--boat", action="store_true")
    parser.add_argument("--output", default="build/factory")
    args = parser.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    store = ROOT / "factory" / "store"
    local = run_local(store)
    sources = {
        str(path.relative_to(ROOT)): digest(path.read_bytes())
        for path in sorted((ROOT / "factory").glob("*.py"))
    }
    local["source_sha256"] = sources
    (out / "local.json").write_text(json.dumps(local, indent=2) + "\n")
    print(f"local {local['status']} {sum(c['status']=='PASS' for c in local['checks'])}/{len(local['checks'])}")
    result = {"local": local, "source_sha256": sources}
    if args.boat:
        boat = run_boat(store)
        (out / "boat.json").write_text(json.dumps(boat, indent=2) + "\n")
        result["boat"] = boat
        print(f"boat {boat['status']}")
    (out / "results.json").write_text(json.dumps(result, indent=2) + "\n")
    if local["status"] != "PASS":
        raise SystemExit(1)
    if args.boat and result.get("boat", {}).get("status") != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
