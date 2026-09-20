#!/usr/bin/env python3
"""Fail closed on stale, incomplete, skipped, or source-mismatched evidence.

These hashes bind records to source; they do not authenticate the record author.
Fresh CI reruns are a separate check. No credentials or cloud calls are needed.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAB_REQUIRED = {'isolation.namespaces', 'credentials.before', 'credentials.after',
                'credentials.positive', 'mount.before', 'mount.after', 'mount.positive',
                'egress.before', 'egress.bypass', 'egress.positive', 'verifier.after',
                'gate.substitution', 'gate.stale_run', 'gate.verifier_changed', 'final.task'}
FACTORY_REQUIRED = {'intended.good', 'intended.bad', 'intended.swap', 'intended.replay',
                    'weakened.report', 'weakened.deps'}
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
        raise ValueError(directory + ': source set mismatch (including empty maps)')
    for name, recorded in sources.items():
        if hashlib.sha256((root / name).read_bytes()).hexdigest() != recorded:
            raise ValueError('stale evidence for ' + name)


def check_rows(record, required):
    rows = record.get('checks', [])
    if record.get('status') != 'PASS' or not rows:
        raise ValueError('missing or unsuccessful evidence')
    names = [row['check'] for row in rows]
    if len(set(names)) != len(names) or not required.issubset(set(names)):
        raise ValueError('duplicate or missing observations')
    if any(row.get('status') != 'PASS' for row in rows):
        raise ValueError('failed, skipped, or unknown observation')
    return len(rows)


def main():
    lab = json.loads((ROOT / 'evidence/results.json').read_text())
    factory = json.loads((ROOT / 'evidence/factory-results.json').read_text())
    http = json.loads((ROOT / 'evidence/http-results.json').read_text())
    check_sources(lab, 'lab')
    check_sources(factory, 'factory')
    check_sources(http, 'factory')
    if lab.get('mode') != 'isolated':
        raise ValueError('stage deck requires recorded Linux isolation evidence')
    count = check_rows(lab, LAB_REQUIRED)
    factory_count = check_rows(factory['local'], FACTORY_REQUIRED)
    if (http.get('status') != 'PASS' or set(http.get('checks', {})) != HTTP_REQUIRED
            or not all(value is True for value in http['checks'].values())):
        raise ValueError('HTTP observations missing or unsuccessful')
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
    except (ValueError, KeyError, TypeError) as error:
        raise SystemExit('Evidence refused: ' + str(error))
