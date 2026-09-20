"""Controlled fixtures only. This suite does not claim OS isolation."""
import copy
import json
import tempfile
import unittest
from dataclasses import FrozenInstanceError
from pathlib import Path

from factory.core import (BAD, CASES, GOOD, SUBJECT, Frozen, Gate, digest,
                          execute_frozen, freeze, judge, persist)
from factory.run import ACCEPT_ENV, LAUNCH


class FactoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = Path(self.tmp.name)
        self.gate = Gate(self.store)
        self.good = freeze({SUBJECT: GOOD.encode()})
        self.bad = freeze({SUBJECT: BAD.encode()})
        persist(self.good, self.store)
        persist(self.bad, self.store)

    def approval(self, **kw):
        return self.gate.issue(artifact=self.good, accepted=kw.get('accepted', True),
                               launch=LAUNCH, env_manifest=ACCEPT_ENV)

    def publish(self, approval, artifact=None, launch=None, env=None):
        return self.gate.publish(approval, artifact or self.good,
                                 launch or LAUNCH, env or ACCEPT_ENV)

    def test_positive_releases_actual_verified_bytes(self):
        self.assertEqual(self.publish(self.approval()), 'PUBLISHED')
        record = json.loads(self.gate.pub_path.read_text().splitlines()[-1])
        data = Path(record['released_file']).read_bytes()
        self.assertEqual(data, GOOD.encode())
        self.assertEqual(freeze({SUBJECT: data}).digest, record['artifact'])

    def test_wrong_digest_before_consumption_then_good(self):
        approval = self.approval()
        self.assertEqual(self.publish(approval, self.bad), 'DENIED')
        self.assertEqual(self.publish(approval), 'PUBLISHED')

    def test_replay_after_consumption(self):
        approval = self.approval()
        self.assertEqual(self.publish(approval), 'PUBLISHED')
        self.assertEqual(self.publish(approval), 'DENIED')

    def test_rejection_cannot_publish(self):
        self.assertEqual(self.publish(self.approval(accepted=False)), 'DENIED')

    def test_frozen_payload_is_immutable(self):
        with self.assertRaises(TypeError):
            self.good.files[SUBJECT] = BAD.encode()
        with self.assertRaises(FrozenInstanceError):
            self.good.digest = self.bad.digest

    def test_forged_label_is_rehashed(self):
        forged = Frozen(self.good.digest, self.good.manifest, {SUBJECT: BAD.encode()})
        self.assertEqual(self.publish(self.approval(), forged), 'DENIED')

    def test_mutated_manifest_is_rejected(self):
        approval = self.approval()
        self.good.manifest['files'][0]['size'] += 1
        self.assertEqual(self.publish(approval), 'DENIED')

    def test_stored_bytes_are_rehashed_at_release(self):
        approval = self.approval()
        (self.store / self.good.digest / 'files' / SUBJECT).write_text(BAD)
        self.assertEqual(self.publish(approval), 'DENIED')
        self.assertFalse(self.gate.pub_path.exists())

    def test_missing_stored_object_cannot_publish(self):
        (self.store / self.good.digest / 'files' / SUBJECT).unlink()
        self.assertEqual(self.publish(self.approval()), 'DENIED')

    def test_symlink_object_cannot_publish(self):
        path = self.store / self.good.digest / 'files' / SUBJECT
        path.unlink()
        other = self.store / 'other.py'
        other.write_text(GOOD)
        path.symlink_to(other)
        self.assertEqual(self.publish(self.approval()), 'DENIED')

    def test_tampered_approval_denied(self):
        approval = self.approval()
        approval['value']['decision'] = 'other'
        self.assertEqual(self.publish(approval), 'DENIED')

    def test_launch_binding_before_consumption(self):
        approval = self.approval()
        self.assertEqual(self.publish(approval, launch={**LAUNCH, 'executor': 'other'}), 'DENIED')
        self.assertEqual(self.publish(approval), 'PUBLISHED')

    def test_environment_binding_before_consumption(self):
        approval = self.approval()
        self.assertEqual(self.publish(approval, env={**ACCEPT_ENV, 'role': 'other'}), 'DENIED')
        self.assertEqual(self.publish(approval), 'PUBLISHED')

    def test_process_restart_fails_closed(self):
        approval = self.approval()
        self.gate = Gate(self.store)
        self.assertEqual(self.publish(approval), 'DENIED')

    def test_malformed_approval_fails_closed(self):
        for approval in ({}, {'value': {}}, {'value': None, 'mac': None}):
            with self.subTest(approval=approval):
                self.assertEqual(self.publish(approval), 'DENIED')

    def test_finite_policy_good_and_bad(self):
        self.assertTrue(judge(execute_frozen(GOOD.encode()))['accepted'])
        self.assertFalse(judge(execute_frozen(BAD.encode()))['accepted'])

    def test_incomplete_evidence_is_no_approval(self):
        self.assertEqual(judge([])['kind'], 'no_approval')

    def test_bad_evidence_is_no_approval(self):
        for item in ({}, {'status': 'timeout'}, {'status': 'malformed'},
                     {'status': 'ok', 'value': True},
                     {'status': 'ok', 'value': 401, 'extra': 'PASS'}):
            with self.subTest(item=item):
                self.assertEqual(judge([item] * len(CASES))['kind'], 'no_approval')

    def test_unexpected_artifact_paths_rejected(self):
        for files in ({}, {'../handler.py': GOOD.encode()}, {SUBJECT: bytearray(b'x')},
                      {SUBJECT: GOOD.encode(), 'expected.json': b'[]'}):
            with self.subTest(files=files):
                with self.assertRaises(ValueError):
                    freeze(files)

    def test_timeout_is_no_approval(self):
        out = execute_frozen(b'import time; time.sleep(0.2)', timeout=0.02)
        self.assertEqual(judge(out)['kind'], 'no_approval')



class CheckerMeasurementTests(unittest.TestCase):
    def test_hash_is_measured_from_the_file_not_constant(self):
        from factory.core import execute_weak_checker, WORKER_EXPECTED
        candidate = b"from pathlib import Path\nPath('checker.py').write_text('changed')\nprint(200)\n"
        observed = execute_weak_checker(candidate, WORKER_EXPECTED)
        self.assertNotEqual(observed['checker_sha256_before'], observed['checker_sha256'])

if __name__ == '__main__':
    unittest.main()
