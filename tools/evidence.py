#!/usr/bin/env python3
"""Validate recorded claims and exact source inventories before a deck/replay build.

Hashes identify source bytes; they do not authenticate an experiment's execution.
Fresh CI runs and their retained artifacts are the execution record.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_LAB = {
    'isolation.namespaces', 'credentials.before', 'credentials.after',
    'credentials.positive', 'credentials.fixture-expired',
    'credentials.fixture-wrong-audience', 'mount.before', 'mount.after',
    'mount.positive', 'egress.before', 'egress.recipient', 'egress.payload',
    'egress.url', 'egress.no_delivery', 'egress.bypass', 'egress.positive',
    'verifier.before', 'verifier.after', 'verifier.positive', 'gate.invalid',
    'gate.substitution', 'gate.cross_run', 'gate.stale_run',
    'gate.verifier_changed', 'gate.forgery', 'gate.positive', 'gate.replay',
    'history.rewrite', 'final.task',
}
REQUIRED_FACTORY = {'intended.good', 'intended.bad', 'intended.swap',
                    'intended.replay', 'weakened.report', 'weakened.deps'}


def verify_sources(record, directory):
    paths = {str(p.relative_to(ROOT)) for p in (ROOT / directory).glob('*.py')}
    source = record.get('source_sha256', {})
    if set(source) != paths:
        raise ValueError(f'{directory}: incomplete or unexpected source inventory')
    for name, expected in source.items():
        actual = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError(f'Stale evidence for {name}; rerun and record the experiment')


def verify_checks(record, required):
    checks = record.get('checks', [])
    names = [c.get('check') for c in checks]
    if len(names) != len(set(names)) or set(names) != required:
        raise ValueError('Missing, duplicate or unexpected experiment checks')
    if any(c.get('status') != 'PASS' for c in checks):
        raise ValueError('Recorded experiment contains failed or skipped checks')


def validate():
    lab = json.loads((ROOT / 'evidence/results.json').read_text())
    factory = json.loads((ROOT / 'evidence/factory-results.json').read_text())
    verify_sources(lab, 'lab')
    verify_sources(factory, 'factory')
    if lab.get('mode') != 'isolated' or lab.get('status') != 'PASS':
        raise ValueError('Stage deck requires a completed isolated lab record')
    local = factory['local']
    if local.get('mode') != 'local' or local.get('status') != 'PASS':
        raise ValueError('Stage deck requires completed local factory evidence')
    verify_checks(lab, REQUIRED_LAB)
    verify_checks(local, REQUIRED_FACTORY)
    deps = local['weakened_deps']
    if (deps['checker_stdout'] != 'PASS' or deps['checker_file_changed']
            or deps['checker_sha256'] != deps['checker_after_sha256']
            or deps['independent_verdict'].get('accepted') is not False):
        raise ValueError('Unchanged-checker reveal is not supported by the record')
    good = local['good']
    if (good['swap_after_freeze'] != 'DENIED' or good['published'] != 'PUBLISHED'
            or good['replay'] != 'DENIED'):
        raise ValueError('Fresh-swap / positive / replay sequence is unsupported')
    return lab, factory


if __name__ == '__main__':
    try:
        lab, factory = validate()
    except (ValueError, KeyError, TypeError, OSError) as error:
        raise SystemExit(str(error))
    print(f"Verified sources and records: {len(lab['checks'])} isolated assertions; "
          f"{len(factory['local']['checks'])} factory checks. No cloud run implied.")
