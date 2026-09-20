#!/usr/bin/env python3
"""Fail closed on missing, stale or non-isolated stage evidence."""
import argparse
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
LAB_CHECKS = {'isolation.namespaces','credentials.before','credentials.after','credentials.positive',
 'credentials.fixture-expired','credentials.fixture-wrong-audience','mount.before','mount.after','mount.positive',
 'egress.before','egress.recipient','egress.payload','egress.url','egress.no_delivery','egress.bypass','egress.positive',
 'verifier.before','verifier.after','verifier.positive','gate.invalid','gate.substitution','gate.cross_run',
 'gate.stale_run','gate.verifier_changed','gate.forgery','gate.positive','gate.replay','history.rewrite','final.task'}
FACTORY_CHECKS = {'intended.swap','intended.good','intended.bad','intended.replay','intended.malformed',
 'intended.verifier','intended.environment','intended.run','intended.forgery','intended.positive_after_negatives',
 'intended.expired','intended.incomplete','intended.immutable','weakened.deps','weakened.report'}

def source_paths(root: Path, group: str) -> set[str]:
    paths = set(str(p.relative_to(root)) for p in (root/group).glob('*.py'))
    if group == 'factory':
        paths.add('lab/run.py')
    return paths

def validate_sources(record: dict, expected: set[str], root: Path = ROOT) -> None:
    found=record.get('source_sha256')
    if not isinstance(found,dict) or not expected or set(found)!=expected:
        raise ValueError('Source set is missing, added, or incomplete; rerecord the full suite.')
    for name, expected_hash in found.items():
        if hashlib.sha256((root/name).read_bytes()).hexdigest()!=expected_hash:
            raise ValueError('Evidence is stale for '+name)

def validate_checks(result: dict, required: set[str]) -> None:
    checks=result.get('checks',[])
    names=[c.get('check') for c in checks]
    if len(names)!=len(set(names)) or set(names)!=required:
        raise ValueError('Evidence check set is incomplete, duplicated, or unexpected.')
    if result.get('status')!='PASS' or any(c.get('status')!='PASS' for c in checks):
        raise ValueError('Stage evidence contains a failure or skip.')
    if result.get('mode')!='isolated':
        raise ValueError('Stage claims require recorded isolated execution, not local fixtures.')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lab',type=Path,default=ROOT/'evidence/results.json')
    parser.add_argument('--factory',type=Path,default=ROOT/'evidence/factory-results.json')
    args=parser.parse_args()
    lab=json.loads(args.lab.read_text())
    factory=json.loads(args.factory.read_text())
    validate_sources(lab,source_paths(ROOT,'lab'))
    validate_sources(factory,source_paths(ROOT,'factory'))
    validate_checks(lab,LAB_CHECKS)
    validate_checks(factory['local'],FACTORY_CHECKS)
    weak=factory['local']['weakened_deps']
    if weak.get('checker_write_denied') is not True or weak.get('checker_sha256_before')!=weak.get('checker_sha256_after'):
        raise ValueError('Protected-checker demonstration lacks the required observed evidence.')
    count=f'{len(LAB_CHECKS)} lab assertions; {len(FACTORY_CHECKS)} factory assertions'
    (ROOT/'slides/evidence.tex').write_text('\\newcommand{\\evidencecount}{'+count+'}\n')
    print('VERIFIED exact source sets, isolated modes and required observations: '+count)
if __name__=='__main__':
    main()
