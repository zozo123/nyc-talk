"""Controller protocol regressions; OS boundary checks are a separate CI job."""
import sqlite3
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from dataclasses import FrozenInstanceError
from pathlib import Path
from unittest.mock import patch

from factory.core import (BAD, CASES, GOOD, SUBJECT, VERIFIER_TCB, Gate,
                          execute_frozen, execute_weak_checker, freeze, judge,
                          verifier_bundle_digest, WORKER_EXPECTED)

LAUNCH = {"executor": "fixture", "compare": "controller"}
ENV = {"role": "accept", "worker_write_access": False}
DEST = {"operation": "publish_release", "environment": "test-release-store",
        "account": "controller-owned", "subject": SUBJECT}
OTHER_DEST = dict(DEST, environment="test-staging-store")


class FactoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = Path(self.tmp.name)
        self.now = [1000.0]
        self.gate = Gate(self.store, clock=lambda: self.now[0])
        self.good = freeze({SUBJECT: GOOD.encode()})
        self.bad = freeze({SUBJECT: BAD.encode()})

    def issue(self, **kw):
        return self.gate.issue(artifact=kw.get("artifact", self.good),
                               launch=LAUNCH, env_manifest=ENV,
                               destination=kw.get("destination", DEST),
                               ttl=kw.get("ttl", 300))

    def approval(self, **kw):
        return self.issue(**kw).approval

    def publish(self, approval, artifact=None, launch=None, env=None, destination=None):
        return self.gate.publish(approval, artifact or self.good, launch or LAUNCH,
                                 env or ENV, destination or DEST)

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

    def test_gate_derives_accept_from_good_bytes(self):
        auth = self.issue()
        self.assertEqual(auth.approval["value"]["decision"], "accept")
        self.assertTrue(auth.verdict["accepted"])
        self.assertEqual(len(auth.observations), len(CASES))

    def test_gate_derives_reject_from_bad_bytes(self):
        auth = self.issue(artifact=self.bad)
        self.assertEqual(auth.approval["value"]["decision"], "reject")
        self.assertFalse(auth.verdict["accepted"])
        self.assertEqual(self.publish(auth.approval, self.bad), "DENIED")

    def test_no_approval_on_malformed_observations(self):
        auth = self.gate.issue(artifact=self.good, observe=lambda data: ["garbage"],
                               launch=LAUNCH, env_manifest=ENV, destination=DEST)
        self.assertIsNone(auth.approval)
        self.assertEqual(auth.verdict["kind"], "no_approval")

    def test_observer_receives_the_named_bytes(self):
        seen = []
        auth = self.gate.issue(artifact=self.good,
                               observe=lambda data: seen.append(data) or execute_frozen(data),
                               launch=LAUNCH, env_manifest=ENV, destination=DEST)
        self.assertEqual(seen, [GOOD.encode()])
        self.assertEqual(auth.approval["value"]["decision"], "accept")

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

    def test_tampered_mac(self):
        approval = self.approval(); approval["mac"] = "0" * 64
        self.assertEqual(self.publish(approval), "DENIED")

    def test_tampered_artifact_digest(self):
        approval = self.approval(); approval["value"]["artifact_manifest_digest"] = self.bad.digest
        self.assertEqual(self.publish(approval, self.bad), "DENIED")

    def test_tampered_decision(self):
        approval = self.approval(artifact=self.bad)
        approval["value"]["decision"] = "accept"
        self.assertEqual(self.publish(approval, self.bad), "DENIED")

    def test_wrong_run_even_with_same_key(self):
        approval = self.approval(); self.gate.run = "new-run"
        self.assertEqual(self.publish(approval), "DENIED")

    def test_controller_restart_fails_closed(self):
        approval = self.approval()
        replacement = Gate(self.store, clock=lambda: self.now[0])
        self.assertEqual(replacement.publish(approval, self.good, LAUNCH, ENV, DEST), "DENIED")

    def test_changed_launch(self):
        self.assertEqual(self.publish(self.approval(), launch={"executor": "other"}), "DENIED")

    def test_changed_environment(self):
        self.assertEqual(self.publish(self.approval(), env={"role": "worker"}), "DENIED")

    def test_changed_destination(self):
        approval = self.approval()
        self.assertEqual(self.publish(approval, destination=OTHER_DEST), "DENIED")
        self.assertEqual(self.publish(approval), "PUBLISHED")

    def test_malformed_destination_refused_at_issue(self):
        for value in (None, [], {}, {"operation": "publish_release"},
                      dict(DEST, subject="other.py"), dict(DEST, account=""),
                      dict(DEST, extra="field"), dict(DEST, account=7)):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    self.issue(destination=value)

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
        self.assertTrue(self.gate.authorize(approval, self.good, LAUNCH, ENV, DEST))
        self.assertEqual(self.publish(approval), "PUBLISHED")
        self.assertFalse(self.gate.authorize(approval, self.good, LAUNCH, ENV, DEST))

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

    def test_verifier_tcb_covers_imported_modules(self):
        import factory.boat  # noqa: F401
        import factory.isolated  # noqa: F401
        import factory.run  # noqa: F401
        import lab.run  # noqa: F401
        root = Path(__file__).resolve().parents[1]
        for module in list(sys.modules.values()):
            path = getattr(module, "__file__", None)
            if not path:
                continue
            try:
                rel = Path(path).resolve().relative_to(root)
            except ValueError:
                continue
            if rel.parts[0] in ("factory", "lab"):
                self.assertIn(str(rel), VERIFIER_TCB,
                              f"{rel} shapes controller observations but is outside VERIFIER_TCB")

    def test_verifier_digest_fails_closed_on_missing_member(self):
        with self.assertRaises(OSError):
            verifier_bundle_digest(LAUNCH, tcb=VERIFIER_TCB + ("factory/absent.py",))


if __name__ == "__main__":
    unittest.main()
