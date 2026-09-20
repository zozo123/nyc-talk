import hashlib
import tempfile
import unittest
from pathlib import Path
from tools.evidence import check_rows, check_sources


class EvidenceTests(unittest.TestCase):
    def test_accepts_complete_passing_rows(self):
        self.assertEqual(check_rows({'status': 'PASS', 'checks': [
            {'check': 'x', 'status': 'PASS'}]}, {'x'}), 1)

    def test_missing_duplicate_and_skipped_rows_refused(self):
        for rows in ([], [{'check': 'y', 'status': 'PASS'}],
                     [{'check': 'x', 'status': 'SKIP'}],
                     [{'check': 'x', 'status': 'PASS'}] * 2):
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                check_rows({'status': 'PASS', 'checks': rows}, {'x'})

    def test_failure_status_refused(self):
        with self.assertRaises(ValueError):
            check_rows({'status': 'FAIL', 'checks': [{'check': 'x', 'status': 'PASS'}]}, {'x'})

    def test_exact_source_set_and_digest_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'lab').mkdir()
            (root / 'lab/run.py').write_bytes(b'print(1)\n')
            good = {'lab/run.py': hashlib.sha256(b'print(1)\n').hexdigest()}
            check_sources({'source_sha256': good}, 'lab', root)
            for sources in ({}, {'../outside.py': 'x'}, {'lab/run.py': 'wrong'}):
                with self.subTest(sources=sources), self.assertRaises(ValueError):
                    check_sources({'source_sha256': sources}, 'lab', root)


if __name__ == '__main__':
    unittest.main()
