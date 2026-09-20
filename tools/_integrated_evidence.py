#!/usr/bin/env python3
"""Validate exact source inventories, observations and acceptance controls.

Hashes bind records to source, not to their author. Fresh CI execution and a
trusted distribution channel remain separate provenance requirements.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAB_REQUIRED = {
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
FACTORY_REQUIRED = {'intended.good', 'intended.bad', 'intended.swap',
                    'intended.replay', 'weakened.report', 'weakened.deps'}
HTTP_REQUIRED = {'original_checker_rejects_bad', 'worker_cases_make_same_checker_pass',
                 'checker_hash_unchanged', 'open_admin_really_http_200',
                 'controller_rejects_open_admin', 'fresh_approval_rejects_swap',
                 'same_approval_publishes_good', 'released_bytes_match_verified',
                 'released_admin_really_http_401', 'authorized_admin_still_http_200',
                 'used_approval_denied'}


def check_sources(record, directory, root=ROOT):
    expected = {str(p.relative_to(root)) for p in (root / directory).glob('*.py')}
    sources = record.get('source_sha256', {})
    if not expected or set(sources) != expected:
        raise ValueError(directory + ': incomplete or unexpected source inventory')
    for name, recorded in sources.items():
        if hashlib.sha256((root / name).read_bytes()).hexdigest() != recorded:
            raise ValueError('stale evidence for ' + name)


def check_rows(record, required):
    rows = record.get('checks', [])
    if record.get('status') != 'PASS' or not rows:
        raise ValueError('missing or unsuccessful evidence')
    names = [row.get('check') for row in rows]
    if len(set(names)) != len(names) or set(names) != required:
        raise ValueError('duplicate, unexpected or missing observations')
    if any(row.get('status') != 'PASS' for row in rows):
        raise ValueError('failed, skipped, or unknown observation')
    return len(rows)


def validate():
    """Keep the two-record API used by the preserved offline replay."""
    lab = json.loads((ROOT / 'evidence/results.json').read_text())
    factory = json.loads((ROOT / 'evidence/factory-results.json').read_text())
    http = json.loads((ROOT / 'evidence/http-results.json').read_text())
    check_sources(lab, 'lab')
    check_sources(factory, 'factory')
    check_sources(http, 'factory')
    if lab.get('mode') != 'isolated':
        raise ValueError('stage deck requires recorded Linux isolation evidence')
    check_rows(lab, LAB_REQUIRED)
    local = factory['local']
    if local.get('mode') != 'local':
        raise ValueError('stage deck requires local factory evidence')
    check_rows(local, FACTORY_REQUIRED)
    deps = local['weakened_deps']
    if (deps['checker_stdout'] != 'PASS' or deps['checker_file_changed']
            or deps['checker_sha256'] != deps['checker_after_sha256']
            or deps['independent_verdict'].get('accepted') is not False):
        raise ValueError('unchanged-checker reveal is unsupported')
    good = local['good']
    if (good['swap_after_freeze'] != 'DENIED' or good['published'] != 'PUBLISHED'
            or good['replay'] != 'DENIED'):
        raise ValueError('fresh-swap / positive / replay sequence is unsupported')
    if (http.get('status') != 'PASS' or set(http.get('checks', {})) != HTTP_REQUIRED
            or not all(value is True for value in http['checks'].values())):
        raise ValueError('HTTP observations missing or unsuccessful')
    return lab, factory


def main():
    lab, factory = validate()
    count, factory_count = len(lab['checks']), len(factory['local']['checks'])
    text = '\n'.join([
        r'\newcommand{\evidencescope}{Recorded Linux isolation + local fixture protocols}',
        r'\newcommand{\mountscope}{Observed with real bind mounts}',
        r'\newcommand{\networkscope}{Host-loopback probe unreachable from the worker net namespace}',
        r'\newcommand{\evidencecount}{' + str(count) + ' Linux assertions; '
        + str(factory_count) + ' factory assertions; ' + str(len(HTTP_REQUIRED)) + ' HTTP assertions}',
    ]) + '\n'
    (ROOT / 'slides/evidence.tex').write_text(text)
    print(f'Evidence valid: {count} Linux / {factory_count} factory / {len(HTTP_REQUIRED)} HTTP')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError) as error:
        raise SystemExit('Evidence refused: ' + str(error))
