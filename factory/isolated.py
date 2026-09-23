#!/usr/bin/env python3
"""Read-only checker / mutable answer-key experiment on disposable Linux.

Only the committed deterministic fixtures run here. The policy is a five-case
HTTP-status *model*, not a network server. No LLM and no external service.
"""
from __future__ import annotations

import argparse
import json
import platform
import shutil
import tempfile
from pathlib import Path

from factory.core import (BAD, CASES, GOOD, POLICY, SUBJECT, WEAK_CHECKER,
                          WORKER_EXPECTED, Gate, acceptance_environment,
                          canonical, digest, freeze, judge)
from lab.run import Runner

ROOT = Path(__file__).resolve().parents[1]
# The approval names one destination. The staging store is a different target
# for the same bytes, and the same approval must not reach it.
RELEASE_TARGET = {
    "operation": "publish_release",
    "environment": "isolated-lab-release-store",
    "account": "controller-owned",
    "subject": SUBJECT,
}
OTHER_TARGET = dict(RELEASE_TARGET, environment="isolated-lab-staging-store")


def run() -> dict:
    if not shutil.which("bwrap"):
        raise RuntimeError("bubblewrap is required; there is no unisolated fallback")
    checks = []

    def check(name, passed, detail):
        checks.append({"check": name, "status": "PASS" if passed else "FAIL", "detail": detail})
        if not passed:
            raise AssertionError(name)

    with tempfile.TemporaryDirectory(prefix="nyc-checker-") as tmp:
        root = Path(tmp)
        work, verifier = root / "work", root / "verifier"
        work.mkdir(); verifier.mkdir()
        (work / SUBJECT).write_text(BAD)
        original_expected = [{"input": value, "output": expected} for value, expected in CASES]
        (work / "expected.json").write_bytes(canonical(original_expected))
        checker = verifier / "checker.py"
        checker.write_text(WEAK_CHECKER)
        checker_before = digest(checker.read_bytes())
        candidate_before = digest((work / SUBJECT).read_bytes())
        expected_before = digest((work / "expected.json").read_bytes())
        runner = Runner("isolated", root)
        invoke_checker = 'import json, subprocess\np = subprocess.run(["/usr/bin/python3", "-I", "-B", "/verifier/checker.py"], cwd="/work", text=True, capture_output=True)\nprint(json.dumps({"exit": p.returncode, "stdout": p.stdout.strip()}))'
        weak_before = json.loads(runner.run(invoke_checker,
                                 mounts=[(work, "/work", False), (verifier, "/verifier", False)], network=False))
        check("answer_key.honest_key_fails", weak_before == {"exit": 1, "stdout": "FAIL"},
              "The unchanged checker rejects the same candidate with the honest answer key.")
        mutate = '''from pathlib import Path
try:
    Path("/verifier/checker.py").write_text("print('PASS')")
    checker_write = "SUCCEEDED"
except OSError:
    checker_write = "DENIED"
Path("/work/expected.json").write_text(PAYLOAD)
print(checker_write)
'''.replace("PAYLOAD", repr(canonical(WORKER_EXPECTED).decode()))
        result = runner.run(mutate, mounts=[(work, "/work", True),
                                            (verifier, "/verifier", False)], network=False)
        check("answer_key.checker_write_denied", result == "DENIED", "Read-only checker mount rejects the direct write.")
        check("answer_key.checker_unchanged", digest(checker.read_bytes()) == checker_before,
              "Checker SHA-256 is identical before and after the worker step.")
        check("answer_key.candidate_unchanged", digest((work / SUBJECT).read_bytes()) == candidate_before,
              "The always-200 candidate bytes are also unchanged.")
        check("answer_key.expected_changed", json.loads((work / "expected.json").read_text()) == WORKER_EXPECTED,
              "Worker changed only the answer key to expect 200 for every case.")
        weak_stdout = runner.run('import os, runpy\nos.chdir("/work")\nrunpy.run_path("/verifier/checker.py", run_name="__main__")',
                                 mounts=[(work, "/work", False), (verifier, "/verifier", False)], network=False)
        check("answer_key.weak_pass", weak_stdout == "PASS", "Unchanged, read-only checker accepts the open-admin fixture.")

        def observe(data: bytes) -> list:
            """Controller-owned observer: bytes in, raw observations out.

            It has no way to return a decision, and the gate hands it the exact
            frozen bytes the approval will name."""
            candidate = freeze({SUBJECT: data})
            path = root / candidate.digest
            path.mkdir(exist_ok=True)
            (path / SUBJECT).write_bytes(candidate.files[SUBJECT])
            outputs = []
            for value, _ in CASES:
                out = runner.run('import runpy\nrunpy.run_path("/candidate/handler.py", run_name="__main__")',
                                 mounts=[(path, "/candidate", False)], network=False, args=[value])
                outputs.append({"status": "ok", "value": json.loads(out)})
            return outputs

        def evaluate(source):
            candidate = freeze({SUBJECT: source.encode()})
            outputs = observe(candidate.files[SUBJECT])
            return candidate, outputs, judge(outputs, POLICY)

        bad, bad_outputs, bad_verdict = evaluate(BAD)
        good, good_outputs, good_verdict = evaluate(GOOD)
        check("answer_key.independent_reject", bad_verdict.get("accepted") is False,
              "Controller-owned cases reject the same always-200 bytes.")
        check("answer_key.positive", good_verdict.get("accepted") is True,
              "Fixed handler satisfies all five controller-owned cases.")
        launch = {"executor": "bubblewrap", "compare": "controller", "cases": len(CASES)}
        environment = acceptance_environment(
            "accept", worker_network=False, candidate_mount="read-only",
            expected_results_in_child=False)
        gate = Gate(root / "release", policy=POLICY)
        refused = gate.issue(artifact=bad, observe=observe, launch=launch,
                             env_manifest=environment, destination=RELEASE_TARGET)
        check("release.derived_reject",
              refused.approval["value"]["decision"] == "reject"
              and gate.publish(refused.approval, bad, launch, environment, RELEASE_TARGET) == "DENIED",
              "The gate re-ran the always-200 bytes itself and signed reject. No caller states the decision.")
        auth = gate.issue(artifact=good, observe=observe, launch=launch,
                          env_manifest=environment, destination=RELEASE_TARGET)
        approval = auth.approval
        check("release.fresh_swap", gate.publish(approval, bad, launch, environment, RELEASE_TARGET) == "DENIED",
              "Substitution is tested BEFORE the approval nonce is consumed.")
        check("release.wrong_destination",
              gate.publish(approval, good, launch, environment, OTHER_TARGET) == "DENIED",
              "The still-unused approval names one destination and does not authorize the staging store.")
        check("release.exact_bytes", gate.publish(approval, good, launch, environment, RELEASE_TARGET) == "PUBLISHED"
              and gate.published_bytes(approval["value"]["nonce"]) == GOOD.encode(),
              "The same unused approval still publishes the exact accepted bytes into the local database.")
        check("release.replay", gate.publish(approval, good, launch, environment, RELEASE_TARGET) == "DENIED",
              "A second publication with the consumed approval is rejected.")
        return {"mode": "isolated", "status": "PASS", "host": platform.platform(),
                "checker_sha256_before": checker_before, "checker_sha256_after": digest(checker.read_bytes()),
                # File-byte digests of exactly what the deck shows. "subject_file"
                # and "expected_file" are digests of the bytes on disk; the
                # "artifact_digest" pair are freeze() manifest digests of the same
                # program, which is why the two differ for identical bytes.
                "subject_file_sha256_before": candidate_before,
                "subject_file_sha256_after": digest((work / SUBJECT).read_bytes()),
                "expected_file_sha256_before": expected_before,
                "expected_file_sha256_after": digest((work / "expected.json").read_bytes()),
                "good_subject_file_sha256": digest(good.files[SUBJECT]),
                "bad_artifact_digest": bad.digest, "good_artifact_digest": good.digest,
                "weak_before": weak_before, "weak_stdout": weak_stdout, "bad_outputs": bad_outputs, "bad_verdict": bad_verdict,
                "good_outputs": good_outputs, "good_verdict": good_verdict,
                "checks": checks, "invocations": runner.invocations}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "build/isolated-factory")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    try:
        result = run()
    except Exception as error:
        result = {"mode": "isolated", "status": "INFRA_OR_FAILURE", "error": str(error), "checks": []}
    sources = sorted((ROOT / "factory").glob("*.py")) + [ROOT / "lab/run.py"]
    result["source_sha256"] = {str(p.relative_to(ROOT)): digest(p.read_bytes()) for p in sources}
    (args.output / "results.json").write_text(json.dumps(result, indent=2) + "\n")
    transcript = ["MODE isolated-factory / STATUS " + result["status"]]
    transcript += [c["status"] + " " + c["check"] + ": " + c["detail"] for c in result["checks"]]
    (args.output / "transcript.txt").write_text("\n".join(transcript) + "\n")
    print("\n".join(transcript))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
