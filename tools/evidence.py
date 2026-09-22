#!/usr/bin/env python3
"""Fail closed on missing, skipped, stale or incomplete recorded experiments.

These hashes link records to source; they are not an independent attestation
against a malicious repository owner who can rewrite both source and evidence.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAB = set("""isolation.namespaces credentials.before credentials.after credentials.positive
credentials.fixture-expired credentials.fixture-wrong-audience mount.before mount.after
mount.positive egress.before egress.recipient egress.payload egress.url egress.no_delivery
egress.bypass egress.positive verifier.before verifier.after verifier.positive gate.invalid
gate.substitution gate.destination gate.cross_run gate.stale_run gate.verifier_changed
gate.forgery gate.positive gate.replay history.rewrite final.task""".split())
LOCAL = set("""intended.good intended.bad intended.derived intended.swap
intended.destination intended.replay weakened.report weakened.deps""".split())
ISOLATED = set("""answer_key.honest_key_fails answer_key.checker_write_denied
answer_key.checker_unchanged answer_key.candidate_unchanged answer_key.expected_changed
answer_key.weak_pass answer_key.independent_reject answer_key.positive
release.derived_reject release.fresh_swap release.wrong_destination
release.exact_bytes release.replay""".split())


def validate_sources(record, required, root=ROOT):
    hashes = record.get('source_sha256')
    if type(hashes) is not dict or set(hashes) != set(required) or not hashes:
        raise ValueError('Recorded source set is incomplete or unexpected')
    for name, expected in hashes.items():
        actual = hashlib.sha256((root / name).read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError('Stale evidence: ' + name)


def validate_checks(record, required, mode):
    checks = record.get('checks')
    if record.get('status') != 'PASS' or record.get('mode') != mode or type(checks) is not list:
        raise ValueError('A complete successful ' + mode + ' record is required')
    if any(type(c) is not dict or c.get('status') != 'PASS' for c in checks):
        raise ValueError('A recorded check failed, skipped, or is malformed')
    names = [c.get('check') for c in checks]
    if len(names) != len(set(names)) or set(names) != required:
        raise ValueError('Missing, duplicate, or unexpected check')


def verify_all(root=ROOT):
    read = lambda name: json.loads((root / 'evidence' / name).read_text())
    lab, factory, isolated = read('results.json'), read('factory-results.json'), read('isolated-factory.json')
    lab_sources = {str(p.relative_to(root)) for p in (root / 'lab').glob('*.py')}
    factory_sources = {str(p.relative_to(root)) for p in (root / 'factory').glob('*.py')}
    validate_sources(lab, lab_sources, root)
    validate_sources(factory, factory_sources, root)
    validate_sources(factory['local'], factory_sources, root)
    validate_sources(isolated, factory_sources | {'lab/run.py'}, root)
    validate_checks(lab, LAB, 'isolated')
    validate_checks(factory['local'], LOCAL, 'local')
    validate_checks(isolated, ISOLATED, 'isolated')
    if isolated['checker_sha256_before'] != isolated['checker_sha256_after']:
        raise ValueError('The checker changed')
    if isolated['weak_before'] != {'exit': 1, 'stdout': 'FAIL'} or isolated['weak_stdout'] != 'PASS':
        raise ValueError('Missing paired checker observation')
    if isolated['bad_verdict'].get('accepted') is not False or isolated['good_verdict'].get('accepted') is not True:
        raise ValueError('Independent negative and positive controls are required')
    if [o.get('value') for o in isolated['bad_outputs']] != [200] * 5:
        raise ValueError('Unexpected bad fixture observations')
    if [o.get('value') for o in isolated['good_outputs']] != [401, 200, 403, 200, 401]:
        raise ValueError('Unexpected good fixture observations')
    return lab, factory, isolated


def main():
    verify_all()
    text = (r'\newcommand{\evidencecount}{30 isolation-lab checks; '
            r'13 isolated checker/gate checks; 8 local factory checks}' + '\n')
    (ROOT / 'slides/evidence.tex').write_text(text)
    print('Evidence verified: 30 lab + 13 isolated checker/gate + 8 local checks. No skips. Source sets match.')


if __name__ == '__main__':
    try:
        main()
    except (OSError, KeyError, TypeError, ValueError) as error:
        raise SystemExit('Evidence verification failed: ' + str(error))
