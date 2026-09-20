import hashlib
import tempfile
import unittest
from pathlib import Path
from tools.evidence import validate_checks, validate_sources

class EvidenceTests(unittest.TestCase):
    def test_complete_source_set(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'a.py').write_bytes(b'x')
            record={'source_sha256':{'a.py':hashlib.sha256(b'x').hexdigest()}}
            validate_sources(record,{'a.py'},root)
            for invalid in ({},{'source_sha256':{}},{'source_sha256':{'a.py':'old'}},
                            {'source_sha256':{'a.py':record['source_sha256']['a.py'],'other.py':'x'}}):
                with self.assertRaises(ValueError): validate_sources(invalid,{'a.py'},root)
    def test_modes_skips_and_duplicate_checks(self):
        good={'status':'PASS','mode':'isolated','checks':[{'check':'a','status':'PASS'}]}
        validate_checks(good,{'a'})
        for invalid in ({**good,'mode':'local'},{**good,'status':'FAIL'},
                        {**good,'checks':[]},{**good,'checks':good['checks']*2},
                        {**good,'checks':[{'check':'a','status':'SKIP'}]}):
            with self.assertRaises(ValueError): validate_checks(invalid,{'a'})
if __name__=='__main__': unittest.main()
