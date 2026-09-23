"""The slide build must not turn incomplete or stale evidence green."""
import hashlib
import tempfile
import unittest
from pathlib import Path
from tools.evidence import validate_checks, validate_rendered_digests, validate_sources

class EvidenceTests(unittest.TestCase):
    def test_empty_sources_rejected(self):
        with self.assertRaises(ValueError): validate_sources({'source_sha256': {}}, {'x.py'})

    def test_missing_source_rejected(self):
        with self.assertRaises(ValueError): validate_sources({'source_sha256': {'x.py':'x'}}, {'x.py','y.py'})

    def test_stale_source_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'x.py').write_bytes(b'changed')
            with self.assertRaises(ValueError):
                validate_sources({'source_sha256': {'x.py':hashlib.sha256(b'old').hexdigest()}}, {'x.py'}, root)

    def test_duplicate_check_rejected(self):
        d={'status':'PASS','mode':'isolated','checks':[{'check':'x','status':'PASS'}]*2}
        with self.assertRaises(ValueError): validate_checks(d, {'x'}, 'isolated')

    def test_skip_and_reference_rejected(self):
        for mode,status in [('isolated','SKIP'),('reference','PASS')]:
            d={'status':'PASS','mode':mode,'checks':[{'check':'x','status':status}]}
            with self.assertRaises(ValueError): validate_checks(d, {'x'}, 'isolated')

    def test_complete_sources_and_checks_accepted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'x.py').write_bytes(b'content')
            validate_sources({'source_sha256':{'x.py':hashlib.sha256(b'content').hexdigest()}},{'x.py'},root)
        validate_checks({'mode':'isolated','status':'PASS','checks':[{'check':'x','status':'PASS'}]}, {'x'}, 'isolated')

    def test_rendered_digests_must_be_real(self):
        cases = {
            "real prefix": ("Program \\texttt{76fcb0904f51} stayed.", None),
            "invented prefix": ("Program \\texttt{0123456789ab} stayed.", ValueError),
            "hex run inside a link": ("\\href{https://web.archive.org/web/20230127205249/x}{a}", None),
        }
        for label, (body, error) in cases.items():
            with self.subTest(label), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                for name in ("slides/talk.tex", "paper/paper.tex"):
                    (root / name).parent.mkdir(parents=True, exist_ok=True)
                    (root / name).write_text(body)
                if error:
                    with self.assertRaises(error):
                        validate_rendered_digests((), root)
                else:
                    validate_rendered_digests((), root)
