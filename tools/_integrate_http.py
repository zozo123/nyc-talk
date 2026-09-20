"""One-shot integration of two pinned, already reviewed repository revisions.

Retain main's SQLite publication, concurrency tests and offline replay. Add the
HTTP demonstration, expanded checks and stage narrative without a force push.
The migration removes itself; the resulting sources are committed and retested.
"""
from pathlib import Path
import hashlib
import io
import json
import shutil
import subprocess
import tarfile
import tempfile

MAIN = '43af18958fabcb1faf0bd8383587b638b8719b57'
DONOR = '1c2a6e73a62b8b948dc8b2467eac9722e70d5a03'
out = Path.cwd()
work = tempfile.TemporaryDirectory(prefix='talk-integration-')

def archive(revision, name):
    data = subprocess.check_output(['git', 'archive', revision])
    target = Path(work.name) / name
    target.mkdir()
    with tarfile.open(fileobj=io.BytesIO(data)) as handle:
        for member in handle.getmembers():
            path = Path(member.name)
            if path.is_absolute() or '..' in path.parts or member.issym() or member.islnk():
                raise ValueError('unsafe source archive path')
        handle.extractall(target)
    return target

base = archive(MAIN, 'main')
ours = archive(DONOR, 'donor')
validator = (out / 'tools/_integrated_evidence.py').read_bytes()
shutil.copytree(base, out, dirs_exist_ok=True)
for name in ['.github/workflows/verify.yml','.gitignore','Makefile','QUESTIONS.md','README.md','RUNBOOK.md','package.json','research/BASELINE.md','research/DOSSIER.md','research/INVARIANTS.md','research/RESULTS.md','slides/content.json','tools/build_deck.py','tools/build_deck.js','tools/notes.py','tools/package.py','factory/http_demo.py']:
    p=out/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ours/name,p)
shutil.copytree(ours/'evidence/archive',out/'evidence/archive',dirs_exist_ok=True)
shutil.copyfile(ours/'tests/test_factory.py',out/'tests/test_factory_extended.py')
shutil.copyfile(ours/'tests/test_evidence.py',out/'tests/test_evidence.py')

p=out/'factory/core.py';s=p.read_text()
s=s.replace('source = Path(__file__).read_bytes()\n    return digest(canonical({"source": digest(source), "launch": launch}))','sources = {p.name: digest(p.read_bytes())\n               for p in sorted(Path(__file__).parent.glob("*.py"))}\n    return digest(canonical({"sources": sources, "launch": launch}))')
s=s.replace('or type(item.get("value")) is not int for item in outputs):','or type(item.get("value")) is not int\n           or set(item) != {"status", "value"} for item in outputs):')
s=s.replace('def issue(self, *, artifact: Frozen, accepted: bool, launch: dict, env_manifest: dict) -> dict:\n        value = {','def issue(self, *, artifact: Frozen, accepted: bool, launch: dict, env_manifest: dict) -> dict:\n        if not validate_frozen(artifact) or type(accepted) is not bool:\n            raise ValueError("invalid controller decision or artifact")\n        value = {')
mark='    def replay_or_swap(self, approval: dict, artifact: Frozen, launch: dict, env_manifest: dict) -> str:\n'
export='''    def export_release(self, nonce: str) -> Path:
        """Materialize bytes already committed with the single-use approval.

        Publication and nonce consumption are atomic in SQLite. File export is
        a separate, repeatable step; this is not crash-atomic deployment.
        """
        if len(nonce) != 16 or any(c not in "0123456789abcdef" for c in nonce):
            raise ValueError("invalid publication nonce")
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT artifact,payload FROM publications WHERE nonce=? AND run=?",
                (nonce, self.run),
            ).fetchone()
        if row is None:
            raise ValueError("no committed publication for this run")
        artifact_digest, payload = row
        if freeze({SUBJECT: payload}).digest != artifact_digest:
            raise ValueError("committed publication digest mismatch")
        parent = self.store / "releases"
        root = parent / (self.run + "-" + nonce)
        path = root / SUBJECT
        if any(p.is_symlink() for p in (self.store, parent, root, path)):
            raise ValueError("symlink in release export")
        root.mkdir(parents=True, mode=0o700, exist_ok=True)
        try:
            with path.open("xb") as handle:
                handle.write(payload)
        except FileExistsError:
            if path.read_bytes() != payload:
                raise ValueError("existing export differs from committed publication")
        if freeze({SUBJECT: path.read_bytes()}).digest != artifact_digest:
            raise ValueError("exported file digest mismatch")
        return path

'''
assert mark in s;s=s.replace(mark,export+mark);p.write_text(s)

p=out/'factory/run.py';s=p.read_text();a=s.index('ACCEPT_ENV = {');b=s.index('\n\n\ndef classify',a)
ourenv=(ours/'factory/run.py').read_text();a2=ourenv.index('ACCEPT_ENV = {');b2=ourenv.index('\n\n\ndef classify',a2)
s=s[:a]+ourenv[a2:b2]+s[b:]
s=s.replace('result.get("boat", {}).get("status") == "FAIL":\n        raise SystemExit(1)','result.get("boat", {}).get("status") != "PASS":\n        raise SystemExit(2)')
p.write_text(s)

p=out/'factory/http_demo.py';s=p.read_text()
s=s.replace("record = json.loads(gate.pub_path.read_text().splitlines()[-1])\n        released = Path(record['released_file'])", "released = gate.export_release(approval['value']['nonce'])\n        released_digest = freeze({SUBJECT: released.read_bytes()}).digest")
s=s.replace("(before['checker_sha256_before'] == before['checker_sha256']\n                                       == after['checker_sha256_before'] == after['checker_sha256'])", "(before['checker_sha256'] == before['checker_after_sha256']\n                                       == after['checker_sha256'] == after['checker_after_sha256'])")
s=s.replace("'released_artifact': record['artifact']", "'released_artifact': released_digest")
s=s.replace("'Single trusted controller; no concurrent or crash-consistency claim.'", "'SQLite commits nonce and payload together; file export is a separate non-atomic deployment step.'")
p.write_text(s)

p=out/'tests/test_factory_extended.py';s=p.read_text()
s=s.replace('import json\n', 'import json\nimport sqlite3\n')
s=s.replace("self.assertEqual(self.publish(self.approval()), 'PUBLISHED')\n        record = json.loads(self.gate.pub_path.read_text().splitlines()[-1])\n        data = Path(record['released_file']).read_bytes()\n        self.assertEqual(data, GOOD.encode())\n        self.assertEqual(freeze({SUBJECT: data}).digest, record['artifact'])", "approval = self.approval()\n        self.assertEqual(self.publish(approval), 'PUBLISHED')\n        released = self.gate.export_release(approval['value']['nonce'])\n        data = released.read_bytes()\n        self.assertEqual(data, GOOD.encode())\n        self.assertEqual(freeze({SUBJECT: data}).digest, self.good.digest)")
s=s.replace('self.assertFalse(self.gate.pub_path.exists())', 'with sqlite3.connect(self.gate.db_path) as conn:\n            self.assertEqual(conn.execute("SELECT COUNT(*) FROM publications").fetchone()[0], 0)')
s=s.replace("observed['checker_sha256_before'], observed['checker_sha256']", "observed['checker_sha256'], observed['checker_after_sha256']")
p.write_text(s)
for rel in ['README.md','RUNBOOK.md','research/DOSSIER.md','research/RESULTS.md','slides/content.json']:
    p=out/rel;s=p.read_text().replace('25 unit tests','51 unit tests').replace('25 tests','51 tests').replace('25 regression tests','51 regression tests').replace('| 25 tests |','| 51 tests |').replace('twenty-five unit tests','fifty-one unit tests')
    if rel=='slides/content.json':
        s=s.replace('atomic nonce consumption, crash recovery, and protected storage', 'protected storage, crash recovery, and a deployment protocol beyond the reference SQLite publication transaction')
        s=s.replace('Write the released file from that validated object. Then measure the released artifact as well.', 'Commit the exact publication bytes and nonce together in SQLite. Export that committed publication to a file, then measure and request that file as well.')
        s=s.replace('production crash consistency', 'crash-atomic deployment')
    p.write_text(s)
p=out/'research/DOSSIER.md';s=p.read_text().replace('write a real released file and verifies it', 'writes a real released file and verifies it')
s=s.replace('The fix makes attached bytes immutable, checks the manifest against the bytes, loads and rehashes the controller-owned store, writes a real released file and verifies it.', 'The integrated fix preserves main commit `43af18958fabcb1faf0bd8383587b638b8719b57`: attached bytes are immutable, publication payload and nonce are committed together in SQLite, and concurrent publication is tested. The added export path materializes the committed payload as a real file and rechecks it. File export is a separate step, not crash-atomic deployment.')
s=s.replace('parallel publication atomicity; crash consistency;', 'crash-atomic deployment and export;')
s=s.replace('The reference has a single trusted controller and ephemeral keys.', 'The reference has a trusted controller and ephemeral keys. Main\'s eight-contender SQLite publication test is retained: exactly one nonce/payload insert succeeds. That observation does not establish crash-atomic deployment of the exported file.')
s=s.replace('transactional release semantics.', 'a complete transactional deployment protocol beyond the publication database.')
s=s.replace('Unit regression suite | 25', 'Unit regression suite | 51')
s += '\n## Integration with concurrent main work\n\nMain `43af18958fabcb1faf0bd8383587b638b8719b57` landed during finalization. Its SQLite nonce/payload transaction, all 26 regression tests, and offline replay are retained. This revision adds 21 extended factory tests and four evidence-validator tests (51 total), real HTTP observations of exported publication bytes, stricter decision evidence, full factory-source binding and the final stage narrative. The predecessor deck specification and audit remain available in history and `research/archive/`.\n'
p.write_text(s)
p=out/'README.md';s=p.read_text().replace('atomic concurrent publication, crash consistency, durable keys and strong executor isolation remain deployment requirements.', 'SQLite commits publication bytes and nonce consumption together, including a retained concurrency test. Crash-atomic file deployment, durable keys and strong executor isolation remain deployment requirements.')
s += '\nThe integration preserves the 26 regression tests and transactional publication from main `43af1895`, adds 25 tests, and retains `demo/replay.html` as an offline recorded demonstration. The real HTTP fixture is separately rerunnable with `make http`.\n'
p.write_text(s)
p=out/'QUESTIONS.md';s=p.read_text().replace('Concurrent atomic nonce consumption, crash recovery, durable key management, access control and strong candidate isolation are deployment requirements.', 'SQLite commits nonce consumption and exact publication bytes together, with an eight-contender regression requiring exactly one success. Exporting the committed payload to a file is a separate step. Crash-atomic deployment, durable key management, access control and strong candidate isolation remain deployment requirements.')
s=s.replace('Unit tests establish specific behavior, not a proof of a concurrent protocol.', 'The concurrency regression establishes that observed transaction behavior, not a proof of a full crash-consistent deployment protocol.')
p.write_text(s)
p=out/'research/INVARIANTS.md';s=p.read_text().replace('transactional nonce consumption, crash recovery', 'a deployment transaction beyond the atomic SQLite nonce/payload insert, crash recovery');p.write_text(s)
(out/'research/archive').mkdir(exist_ok=True)
for old,new in [('slides/deck.json','research/archive/deck-before-http.json'),('research/AUDIT.md','research/archive/audit-before-http.md')]:
    if (out/old).exists(): shutil.move(out/old,out/new)
(out/'research/AUDIT.md').write_text('# Integrated audit\n\nThe active claim ledger is [DOSSIER.md](DOSSIER.md). The predecessor audit from main `43af1895` is preserved as [archive/audit-before-http.md](archive/audit-before-http.md). Its SQLite publication, concurrency protections, tests and offline replay are retained; the integrated revision adds HTTP observation of actual exported publication bytes and extended regression coverage.\n')
p=out/'Makefile';s=p.read_text().replace('\tcp build/talk.pptx slides/talk.pptx\n', '\tcp build/talk.pptx slides/talk.pptx\n\tpython3 tools/replay.py verifier --html demo/replay.html\n');p.write_text(s)
p=out/'tools/package.py';s=p.read_text().replace("'tests','tools','.github'", "'tests','tools','demo','.github'").replace("'.yml','.yaml'", "'.yml','.yaml','.html'");p.write_text(s)
p=out/'.github/workflows/verify.yml';s=p.read_text().replace('cp --parents slides/talk.pdf', 'cp --parents demo/replay.html slides/talk.pdf').replace('git add slides/talk.pdf', 'git add demo/replay.html slides/talk.pdf');p.write_text(s)
(out/'tools/evidence.py').write_bytes(validator)
content=json.loads((out/'slides/content.json').read_text())
words=sum(len(slide['notes'].split()) for slide in content['slides'][:11])
assert words == 1667, words
for name in ['README.md','RUNBOOK.md']:
    p=out/name;p.write_text(p.read_text().replace('1,651',f'{words:,}'))
expected = {
    'factory/core.py':'eabf1af93669c672666113129dd9b514212a8ef65898c33a3cc520566c30bf60',
    'factory/run.py':'d909722fe92f3731e96c447c42b74a1273d160339f9b866cc3c1ef8940e70fb8',
    'factory/http_demo.py':'1e54fcebe1bdd81d2d2b46d5f2ba4696da88400956128b60040e116d30402447',
    'tests/test_factory.py':'33cb19db4a05c4615adf934cd6125fd83b3c5a01a25870a3adfc5f78c1931871',
    'tests/test_factory_extended.py':'6377617dbc35da38b3cf6f126b8f3e0d95abef85382e6f98262d9a5cd7b84e00',
    'tests/test_evidence.py':'8eb611524e969b96ae1912f5b3505753ddf6b68180f0ff571decb5cb8a8ae406',
    'tools/evidence.py':'58863957ea5d663812d6aad29a3a9d6f818210f39533e3f3a5809b4e616a10ed',
    'tools/build_deck.py':'ba1a80fd3f7635934b00be819d730c16f5b4450b8dce9fd97339a1dedf94af4d',
    'tools/build_deck.js':'756d7b3f4961492b7196fcb0bcbaf5025a1a742754f0652ecdaf1609cbca1013',
}
for name, wanted in expected.items():
    actual=hashlib.sha256((out/name).read_bytes()).hexdigest()
    if actual != wanted:
        raise ValueError('integration differs from tested source: ' + name)
for name in ['tools/_integrate_http.py','tools/_integrated_evidence.py','.github/workflows/integrate-http.yml']:
    (out/name).unlink()
print('Integrated pinned sources; preserved all 26 main tests; 51 total tests to rerun.')
work.cleanup()
