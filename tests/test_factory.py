"""Adversarial regressions for the controller-owned reference gate.

These test the Python protocol and committed fixtures, not host containment.
"""
import copy
import sqlite3
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from factory.core import (BAD, GOOD, SUBJECT, CASES, Frozen, Gate, canonical,
                          execute_frozen, execute_weak_checker, freeze, judge,
                          persist, WORKER_EXPECTED, validate_frozen)
from factory.run import ACCEPT_ENV, LAUNCH, intended


class GateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.gate = Gate(self.root)
        self.good = freeze({SUBJECT: GOOD.encode()})
        self.bad = freeze({SUBJECT: BAD.encode()})
        persist(self.good, self.root)
        persist(self.bad, self.root)
        self.approval = self.gate.issue(artifact=self.good, accepted=True,
                                       launch=LAUNCH, env_manifest=ACCEPT_ENV)

    def publish(self, approval=None, artifact=None, launch=None, env=None):
        return self.gate.publish(self.approval if approval is None else approval,
                                 self.good if artifact is None else artifact,
                                 LAUNCH if launch is None else launch,
                                 ACCEPT_ENV if env is None else env)

    def test_good_publishes_exact_bytes(self):
        self.assertEqual(self.publish(), 'PUBLISHED')
        with sqlite3.connect(self.gate.db_path) as conn:
            digest, payload = conn.execute('SELECT artifact,payload FROM publications').fetchone()
        self.assertEqual(digest, self.good.digest)
        self.assertEqual(payload, GOOD.encode())

    def test_fresh_swap_rejected_without_consuming_original(self):
        self.assertEqual(self.publish(artifact=self.bad), 'DENIED')
        self.assertEqual(self.publish(), 'PUBLISHED')

    def test_replay(self):
        self.assertEqual(self.publish(), 'PUBLISHED')
        self.assertEqual(self.publish(), 'DENIED')

    def test_concurrent_publish_exactly_once(self):
        with ThreadPoolExecutor(max_workers=8) as pool:
            outcomes = list(pool.map(lambda _: self.publish(), range(8)))
        self.assertEqual(outcomes.count('PUBLISHED'), 1)
        self.assertEqual(outcomes.count('DENIED'), 7)

    def test_restart_with_same_key_and_run_remembers_consumption(self):
        self.assertEqual(self.publish(), 'PUBLISHED')
        resumed = Gate(self.root)
        resumed.key, resumed.run = self.gate.key, self.gate.run
        self.assertEqual(resumed.publish(self.approval, self.good, LAUNCH, ACCEPT_ENV), 'DENIED')

    def test_cross_run_with_same_key(self):
        self.gate.run = 'another-run'
        self.assertEqual(self.publish(), 'DENIED')

    def test_changed_verifier_launch(self):
        self.assertEqual(self.publish(launch={**LAUNCH, 'executor': 'different'}), 'DENIED')
        self.assertEqual(self.publish(), 'PUBLISHED')

    def test_changed_environment(self):
        self.assertEqual(self.publish(env={**ACCEPT_ENV, 'inherits_producer_disk': True}), 'DENIED')

    def test_authenticated_policy_mismatch(self):
        import hmac
        forged = copy.deepcopy(self.approval)
        forged['value']['policy_digest'] = 'different-policy'
        forged['mac'] = hmac.new(self.gate.key, canonical(forged['value']), 'sha256').hexdigest()
        self.assertEqual(self.publish(approval=forged), 'DENIED')

    def test_forged_approval(self):
        forged = copy.deepcopy(self.approval)
        forged['value']['artifact_manifest_digest'] = self.bad.digest
        self.assertEqual(self.publish(approval=forged, artifact=self.bad), 'DENIED')

    def test_reject_decision_cannot_publish(self):
        rejected = self.gate.issue(artifact=self.good, accepted=False, launch=LAUNCH, env_manifest=ACCEPT_ENV)
        self.assertEqual(self.publish(approval=rejected), 'DENIED')

    def test_malformed_approvals_fail_closed(self):
        for value in ({}, [], {'value': {}}, {'value': None, 'mac': 1}, {'value': [], 'mac': None}):
            with self.subTest(value=value):
                self.assertEqual(self.publish(approval=value), 'DENIED')

    def test_frozen_payload_is_immutable(self):
        with self.assertRaises(TypeError):
            self.good.files[SUBJECT] = BAD.encode()

    def test_stale_digest_on_reconstructed_object(self):
        spoof = Frozen(self.good.digest, self.good.manifest, {SUBJECT: BAD.encode()})
        self.assertFalse(validate_frozen(spoof))
        self.assertEqual(self.publish(artifact=spoof), 'DENIED')
        self.assertEqual(self.publish(), 'PUBLISHED')

    def test_manifest_mutation_rejected(self):
        self.good.manifest['files'][0]['mode'] = '0777'
        self.assertEqual(self.publish(), 'DENIED')

    def test_stored_payload_mutation_rejected(self):
        (self.root / self.good.digest / 'files' / SUBJECT).write_text(BAD)
        self.assertEqual(self.publish(), 'DENIED')

    def test_stored_manifest_mutation_rejected(self):
        (self.root / self.good.digest / 'manifest.json').write_text('{}')
        self.assertEqual(self.publish(), 'DENIED')

    def test_missing_object_rejected(self):
        (self.root / self.good.digest / 'files' / SUBJECT).unlink()
        self.assertEqual(self.publish(), 'DENIED')

    def test_store_symlink_rejected(self):
        payload = self.root / self.good.digest / 'files' / SUBJECT
        payload.unlink()
        target = self.root / 'elsewhere.py'
        target.write_text(GOOD)
        payload.symlink_to(target)
        self.assertEqual(self.publish(), 'DENIED')

    def test_existing_store_cannot_be_rewritten(self):
        (self.root / self.good.digest / 'files' / SUBJECT).write_text(BAD)
        with self.assertRaises(ValueError):
            persist(self.good, self.root)

    def test_illegal_or_mutable_artifacts_rejected(self):
        for files in ({}, {'../handler.py': b'x'}, {SUBJECT: bytearray(b'x')}, {SUBJECT: b'x' * 64001}):
            with self.subTest(files=list(files)):
                with self.assertRaises(ValueError):
                    freeze(files)


class CriteriaTests(unittest.TestCase):
    def test_good_and_bad_control(self):
        self.assertTrue(judge(execute_frozen(GOOD.encode()))['accepted'])
        self.assertFalse(judge(execute_frozen(BAD.encode()))['accepted'])

    def test_unchanged_checker_bad_candidate_false_pass(self):
        result = execute_weak_checker(BAD.encode(), WORKER_EXPECTED)
        self.assertEqual(result['stdout'], 'PASS')
        self.assertEqual(result['checker_sha256'], result['checker_after_sha256'])
        self.assertFalse(judge(execute_frozen(BAD.encode()))['accepted'])

    def test_missing_malformed_timeout_and_error_no_approval(self):
        records = [[], [{'status': 'timeout'}] * 5, [{'status': 'error'}] * 5,
                   [{'status': 'ok', 'value': True}] * 5, [{}] * 5,
                   [{'status': 'ok', 'value': str(v)} for _, v in CASES]]
        for outputs in records:
            with self.subTest(outputs=outputs):
                self.assertEqual(judge(outputs)['kind'], 'no_approval')

    def test_candidate_exit_zero_without_output_no_approval(self):
        self.assertEqual(judge(execute_frozen(b'raise SystemExit(0)\n'))['kind'], 'no_approval')

    def test_recorded_swap_precedes_legitimate_publish(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = intended(Path(tmp), GOOD.encode())
        self.assertEqual(result['swap_after_freeze'], 'DENIED')
        self.assertEqual(result['published'], 'PUBLISHED')
        self.assertEqual(result['replay'], 'DENIED')


if __name__ == '__main__':
    unittest.main()
