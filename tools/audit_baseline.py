#!/usr/bin/env python3
"""Reproduce the archived controller-API bug, never exposed to arbitrary input."""
import importlib.util
import json
import sys
import tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('archived_core', ROOT / 'research/baseline/core.py')
old = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = old
spec.loader.exec_module(old)
with tempfile.TemporaryDirectory() as tmp:
    gate = old.Gate(Path(tmp))
    frozen = old.freeze({old.SUBJECT: old.GOOD.encode()})
    launch, env = {'executor':'fixture'}, {'role':'accept'}
    approval = gate.issue(artifact=frozen, accepted=True, launch=launch, env_manifest=env)
    before = frozen.digest
    frozen.files[old.SUBJECT] = old.BAD.encode()
    actual_hash = old.digest(frozen.files[old.SUBJECT])
    result = {'baseline_commit':'4b06c519cff2ffcc69a8471f4f861a03f08f93a0',
              'archived_core_sha256':old.digest((ROOT/'research/baseline/core.py').read_bytes()),
              'digest_field_unchanged':frozen.digest == before,
              'candidate_matches_manifest':actual_hash == frozen.manifest['files'][0]['sha256'],
              'gate_result':gate.publish(approval, frozen, launch, env),
              'reachability':'Controller API misuse; no demonstrated worker-to-controller exploit path',
              'publication_scope':'The archived gate records a marker, not deployed bytes'}
    assert result['digest_field_unchanged'] and not result['candidate_matches_manifest']
    assert result['gate_result'] == 'PUBLISHED'
(ROOT/'evidence/baseline-audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
