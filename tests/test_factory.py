"""Controller protocol regressions; OS boundary checks are a separate CI job."""
import copy
import sqlite3
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from dataclasses import FrozenInstanceError
from pathlib import Path
from unittest.mock import patch

from factory.core import (BAD, CASES, GOOD, SUBJECT, Gate, execute_frozen,
                          execute_weak_checker, freeze, judge, WORKER_EXPECTED)

LAUNCH = {"executor": "fixture", "compare": "controller"}
ENV = {"role": "accept", "worker_write_access": False}


class FactoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = Path(self.tmp.name)
        self.now = [1000.0]
        self.gate = Gate(self.store, clock=lambda: self.now[0])
        self.good = freeze({SUBJECT: GOOD.encode()})
        self.bad = freeze({SUBJECT: BAD.encode()})

    def approval(self, **kw):
        return self.gate.issue(artifact=kw.get("artifact", self.good),
                               accepted=kw.get("accepted", True), launch=LAUNCH,
                               env_manifest=ENV, ttl=kw.get("ttl", 300))

    def publish(self, approval, artifact=None, launch=None, env=None):
        return self.gate.publish(approval, artifact or self.good, launch or LAUNCH, env or ENV)

    def test_good_passes_five_cases(self):
        self.assertTrue(judge(execute_frozen(GOOD.encode()))["accepted"])

    def test_bad_fails_independent_cases(self):
        self.assertEqual(judge(execute_frozen(BAD.encode()))["matches"], [False, True, False, True, False])

    def test_unchanged_checker_false_positive(self):
        out = execute_weak_checker(BAD.encode(), WORKER_EXPECTED)
        self.assertEqual((out["exit"], out["stdout"]), (0, "PASS"))
        self.assertFalse(judge(execute_frozen(BAD.encode()))["accepted"])

    def test_files_are_not_mutable(self):
        with self.assertRaises(TypeError):
            self.good.files[SUBJECT] = BAD.encode()

    def test_dataclass_is_not_mutable(self):
        with self.assertRaises(FrozenInstanceError):
            self.good._entries = self.bad._entries

    def test_manifest_is_a_copy(self):
        before = self.good.digest
        self.good.manifest["files"][0]["sha256"] = "0" * 64
        self.assertEqual(self.good.digest, before)

    def test_input_dict_mutation_does_not_change_frozen_bytes(self):
        inputs = {SUBJECT: GOOD.encode()}
        frozen = freeze(inputs)
        inputs[SUBJECT] = BAD.encode()
        self.assertEqual(frozen.files[SUBJECT], GOOD.encode())

    def test_disallowed_artifact_shapes(self):
        for value in ({}, {"../handler.py": b"x"}, {SUBJECT: bytearray(b"x")},
                      {SUBJECT: b""}, {SUBJECT: b"x" * 64001}, {SUBJECT: b"x", "extra": b"x"}):
            with self.subTest(value_type=str(type(value))):
                with self.assertRaises(ValueError):
                    freeze(value)

    def test_fresh_swap_then_positive(self):
        approval = self.approval()
        self.assertEqual(self.publish(approval, self.bad), "DENIED")
        self.assertEqual(self.publish(approval), "PUBLISHED")
        self.assertEqual(self.gate.published_bytes(approval["value"]["nonce"]), GOOD.encode())

    def test_publication_is_actual_bytes(self):
        approval = self.approval()
        self.assertEqual(self.publish(approval), "PUBLISHED")
        published = self.gate.published_bytes(approval["value"]["nonce"])
        self.assertEqual(published, GOOD.encode())
        self.assertTrue(judge(execute_frozen(published))["accepted"])

    def test_replay(self):
        approval = self.approval()
        self.assertEqual(self.publish(approval), "PUBLISHED")
        self.assertEqual(self.publish(approval), "DENIED")

    def test_concurrent_replay_exactly_one_commit(self):
        approval = self.approval()
        with ThreadPoolExecutor(max_workers=8) as pool:
            outcomes = list(pool.map(lambda _: self.publish(approval), range(16)))
        self.assertEqual(outcomes.count("PUBLISHED"), 1)
        self.assertEqual(outcomes.count("DENIED"), 15)

    def test_rejected_decision(self):
        self.assertEqual(self.publish(self.approval(accepted=False)), "DENIED")

    def test_tampered_mac(self):
        approval = self.approval(); approval["mac"] = "0" * 64
        self.assertEqual(self.publish(approval), "DENIED")

    def test_tampered_artifact_digest(self):
        approval = self.approval(); approval["value"]["artifact_manifest_digest"] = self.bad.digest
        self.assertEqual(self.publish(approval, self.bad), "DENIED")

    def test_wrong_run_even_with_same_key(self):
        approval = self.approval(); self.gate.run = "new-run"
        self.assertEqual(self.publish(approval), "DENIED")

    def test_controller_restart_fails_closed(self):
        approval = self.approval()
        replacement = Gate(self.store, clock=lambda: self.now[0])
        self.assertEqual(replacement.publish(approval, self.good, LAUNCH, ENV), "DENIED")

    def test_changed_launch(self):
        self.assertEqual(self.publish(self.approval(), launch={"executor": "other"}), "DENIED")

    def test_changed_environment(self):
        self.assertEqual(self.publish(self.approval(), env={"role": "worker"}), "DENIED")

    def test_changed_verifier(self):
        approval = self.approval()
        with patch("factory.core.verifier_bundle_digest", return_value="other"):
            self.assertEqual(self.publish(approval), "DENIED")

    def test_changed_policy(self):
        approval = self.approval()
        with patch("factory.core.policy_digest", return_value="other"):
            self.assertEqual(self.publish(approval), "DENIED")

    def test_changed_expected_results(self):
        approval = self.approval()
        with patch("factory.core.expected_digest", return_value="other"):
            self.assertEqual(self.publish(approval), "DENIED")

    def test_expiration(self):
        approval = self.approval(ttl=1); self.now[0] += 1
        self.assertEqual(self.publish(approval), "DENIED")

    def test_malformed_approval(self):
        for value in (None, [], {}, {"value": {}}, {"value": [], "mac": "x"},
                      {"value": {}, "mac": 1}):
            with self.subTest(value=value):
                self.assertEqual(self.publish(value), "DENIED")

    def test_unknown_approval_fields(self):
        approval = self.approval(); approval["ignored"] = "not allowed"
        self.assertEqual(self.publish(approval), "DENIED")

    def test_authorize_is_not_consumption(self):
        approval = self.approval()
        self.assertTrue(self.gate.authorize(approval, self.good, LAUNCH, ENV))
        self.assertEqual(self.publish(approval), "PUBLISHED")
        self.assertFalse(self.gate.authorize(approval, self.good, LAUNCH, ENV))

    def test_missing_observations_no_approval(self):
        self.assertEqual(judge([])["kind"], "no_approval")

    def test_malformed_observations_no_approval(self):
        for value in (None, [], {}, {"status": "timeout"}, {"status": "ok", "value": 200.0},
                      {"status": "ok", "value": True}, {"status": "ok", "value": 200, "extra": 1}):
            with self.subTest(value=value):
                self.assertEqual(judge([value] * len(CASES))["kind"], "no_approval")

    def test_malformed_process_output_no_approval(self):
        self.assertEqual(judge(execute_frozen(b"print('not-json')"))["kind"], "no_approval")

    def test_timeout_no_approval(self):
        out = execute_frozen(b"import time; time.sleep(60)", timeout=0.01)
        self.assertEqual(judge(out)["kind"], "no_approval")

    def test_publication_tampering_detected(self):
        approval = self.approval(); self.publish(approval)
        with sqlite3.connect(self.gate.db_path) as db:
            db.execute("UPDATE publications SET candidate = ?", (BAD.encode(),))
        with self.assertRaises(ValueError):
            self.gate.published_bytes(approval["value"]["nonce"])


if __name__ == "__main__":
    unittest.main()
