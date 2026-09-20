"""Regression tests for exact-byte binding, nonce atomicity and negative controls."""
import concurrent.futures
import dataclasses
import json
import tempfile
import unittest
from pathlib import Path
from factory.core import BAD, CASES, GOOD, SUBJECT, Frozen, Gate, freeze, judge, persist
from factory.run import ACCEPT_ENV, LAUNCH


class GateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.gate = Gate(Path(self.tmp.name))
        self.good = freeze({SUBJECT: GOOD.encode()})
        self.bad = freeze({SUBJECT: BAD.encode()})
        self.receipt = self.gate.issue(artifact=self.good, accepted=True, launch=LAUNCH, env_manifest=ACCEPT_ENV)

    def publish(self, receipt=None, artifact=None):
        return self.gate.publish(self.receipt if receipt is None else receipt,
                                 self.good if artifact is None else artifact, LAUNCH, ACCEPT_ENV)

    def test_mutation_cannot_keep_old_identity(self):
        initial = self.good.digest
        self.good.files[SUBJECT] = BAD.encode()
        self.good.manifest["files"][0]["sha256"] = "forged"
        self.assertEqual(self.good.digest, initial)
        self.assertEqual(self.good.payload, GOOD.encode())
        with self.assertRaises(dataclasses.FrozenInstanceError):
            self.good.payload = BAD.encode()

    def test_swap_uses_unconsumed_nonce_and_positive_control(self):
        self.assertEqual(self.publish(artifact=self.bad), "DENIED")
        self.assertEqual(self.publish(), "PUBLISHED")
        self.assertEqual(self.gate.released_bytes(self.receipt), GOOD.encode())

    def test_replay_is_denied(self):
        self.assertEqual(self.publish(), "PUBLISHED")
        self.assertEqual(self.publish(), "DENIED")

    def test_concurrent_publication_exactly_once(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
            results = list(pool.map(lambda _: self.publish(), range(24)))
        self.assertEqual(results.count("PUBLISHED"), 1)
        self.assertEqual(results.count("DENIED"), 23)
        self.assertEqual(self.gate.released_bytes(self.receipt), GOOD.encode())

    def test_tampered_mac(self):
        receipt = json.loads(json.dumps(self.receipt))
        receipt["value"]["artifact_manifest_digest"] = self.bad.digest
        self.assertEqual(self.publish(receipt, self.bad), "DENIED")
        self.assertEqual(self.publish(), "PUBLISHED")

    def test_malformed_receipts_fail_closed(self):
        for obj in ({}, [], None, {"value": []}, {"value": {}, "mac": 123}, {"value": None, "mac": "x"}):
            self.assertEqual(self.gate.publish(obj, self.good, LAUNCH, ACCEPT_ENV), "DENIED")

    def test_wrong_run_with_same_key(self):
        run = self.gate.run
        self.gate.run = "different"
        self.assertEqual(self.publish(), "DENIED")
        self.gate.run = run
        self.assertEqual(self.publish(), "PUBLISHED")

    def test_changed_launch_and_environment_do_not_consume(self):
        self.assertEqual(self.gate.publish(self.receipt, self.good, {**LAUNCH, "compare": "worker"}, ACCEPT_ENV), "DENIED")
        self.assertEqual(self.gate.publish(self.receipt, self.good, LAUNCH, {**ACCEPT_ENV, "api_credential": "worker"}), "DENIED")
        self.assertEqual(self.publish(), "PUBLISHED")

    def test_expired_receipt(self):
        self.gate.clock = lambda: 0.0
        receipt = self.gate.issue(artifact=self.good, accepted=True, launch=LAUNCH, env_manifest=ACCEPT_ENV, ttl=1)
        self.gate.clock = lambda: 1.0
        self.assertEqual(self.publish(receipt), "DENIED")

    def test_reject_cannot_publish(self):
        receipt = self.gate.issue(artifact=self.bad, accepted=False, launch=LAUNCH, env_manifest=ACCEPT_ENV)
        self.assertEqual(self.publish(receipt, self.bad), "DENIED")

    def test_frozen_inputs_are_bounded_and_exact(self):
        for files in ({}, {"../handler.py": b"x"}, {SUBJECT: bytearray(b"x")}, {SUBJECT: b"x" * 64001}, {SUBJECT: b"x", "extra": b"y"}):
            with self.assertRaises(ValueError):
                freeze(files)
        with self.assertRaises(ValueError):
            Frozen("not bytes")

    def test_persist_checks_existing_bytes(self):
        path = persist(self.good, Path(self.tmp.name) / "objects")
        self.assertEqual(persist(self.good, Path(self.tmp.name) / "objects"), path)
        (path / SUBJECT).write_bytes(BAD.encode())
        with self.assertRaises(ValueError):
            persist(self.good, Path(self.tmp.name) / "objects")

    def test_incomplete_malformed_bool_no_approval(self):
        for outputs in ([], None, [{}] * 5, [{"status": "timeout"}] * 5,
                        [{"status": "ok", "value": True}] * 5, [{"status": "ok", "value": "401"}] * 5):
            self.assertEqual(judge(outputs)["kind"], "no_approval")
        verdict = judge([{"status": "ok", "value": v} for _, v in CASES])
        self.assertTrue(verdict["accepted"])


if __name__ == "__main__":
    unittest.main()
