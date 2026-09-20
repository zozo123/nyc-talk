#!/usr/bin/env python3
"""Real loopback HTTP around the five-case status-code fixture.

Only committed deterministic candidates run. Authentication is represented by
fixture credentials; this is not an identity provider or an arbitrary-code
sandbox. The wrapper executes the exact handler.py bytes later published.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import threading
import urllib.error
import urllib.request
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from factory.core import (BAD, CASES, GOOD, SUBJECT, WEAK_CHECKER, WORKER_EXPECTED,
                          Gate, canonical, digest, execute_weak_checker, freeze,
                          judge, persist)
from factory.run import ACCEPT_ENV, LAUNCH

ROOT = Path(__file__).resolve().parents[1]
AUTH = {'none': None, 'admin': 'fixture-admin', 'user': 'fixture-user',
        'expired': 'fixture-expired'}


@contextmanager
def serve(candidate: Path):
    """Expose a fixture as HTTP; never accept candidate paths from requests."""
    source = candidate.resolve()

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass

        def do_GET(self):
            header = self.headers.get('Authorization')
            auth = next((key for key, value in AUTH.items()
                         if value and header == 'Bearer ' + value), 'none')
            route = self.path.removeprefix('/')
            proc = subprocess.run(
                [sys.executable, '-I', '-B', str(source), route + ':' + auth],
                capture_output=True, text=True, timeout=2,
                cwd=source.parent,
                env={'PATH': '/usr/bin:/bin', 'LANG': 'C.UTF-8'},
            )
            try:
                status = json.loads(proc.stdout)
                if proc.returncode or type(status) is not int or status not in (200, 401, 403, 404):
                    raise ValueError('malformed status')
            except (json.JSONDecodeError, ValueError):
                status = 500
            body = canonical({'fixture': True, 'status': status})
            self.send_response(status)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f'http://127.0.0.1:{server.server_port}'
    finally:
        server.shutdown()
        thread.join(timeout=3)
        server.server_close()


def observe_http(candidate: Path) -> list[dict]:
    observations = []
    with serve(candidate) as url:
        for value, expected in CASES:
            route, auth = value.split(':', 1)
            headers = {} if AUTH[auth] is None else {'Authorization': 'Bearer ' + AUTH[auth]}
            req = urllib.request.Request(url + '/' + route, headers=headers)
            try:
                with urllib.request.urlopen(req, timeout=5) as response:
                    status = response.status
            except urllib.error.HTTPError as error:
                status = error.code
                error.close()
            observations.append({'request': 'GET /' + route, 'auth': auth,
                                 'expected': expected, 'observed': status})
    return observations


def run() -> dict:
    with tempfile.TemporaryDirectory(prefix='nyc-http-proof-') as tmp:
        root = Path(tmp)
        candidate = root / SUBJECT
        candidate.write_text(BAD)
        honest_cases = [{'input': value, 'output': output} for value, output in CASES]
        before = execute_weak_checker(BAD.encode(), honest_cases)
        after = execute_weak_checker(BAD.encode(), WORKER_EXPECTED)
        weak_http = observe_http(candidate)
        store = root / 'controller-store'
        gate = Gate(store)
        frozen_bad = freeze({SUBJECT: candidate.read_bytes()})
        persist(frozen_bad, store)
        bad_judgment = judge([{'status': 'ok', 'value': row['observed']} for row in weak_http])
        bad_approval = gate.issue(artifact=frozen_bad, accepted=bad_judgment['accepted'],
                                  launch=LAUNCH, env_manifest=ACCEPT_ENV)
        bad_publish = gate.publish(bad_approval, frozen_bad, LAUNCH, ACCEPT_ENV)
        candidate.write_text(GOOD)
        frozen_good = freeze({SUBJECT: candidate.read_bytes()})
        persist(frozen_good, store)
        good_http = observe_http(store / frozen_good.digest / 'files' / SUBJECT)
        good_judgment = judge([{'status': 'ok', 'value': row['observed']} for row in good_http])
        approval = gate.issue(artifact=frozen_good, accepted=good_judgment['accepted'],
                             launch=LAUNCH, env_manifest=ACCEPT_ENV)
        # This denial must precede a positive publication using the SAME nonce.
        swap = gate.publish(approval, frozen_bad, LAUNCH, ACCEPT_ENV)
        published = gate.publish(approval, frozen_good, LAUNCH, ACCEPT_ENV)
        record = json.loads(gate.pub_path.read_text().splitlines()[-1])
        released = Path(record['released_file'])
        released_http = observe_http(released)
        replay = gate.publish(approval, frozen_good, LAUNCH, ACCEPT_ENV)
        checks = {
            'original_checker_rejects_bad': before['stdout'] == 'FAIL',
            'worker_cases_make_same_checker_pass': after['stdout'] == 'PASS',
            'checker_hash_unchanged': (before['checker_sha256_before'] == before['checker_sha256']
                                       == after['checker_sha256_before'] == after['checker_sha256']),
            'open_admin_really_http_200': weak_http[0]['observed'] == 200,
            'controller_rejects_open_admin': bad_publish == 'DENIED',
            'fresh_approval_rejects_swap': swap == 'DENIED',
            'same_approval_publishes_good': published == 'PUBLISHED',
            'released_bytes_match_verified': released.read_bytes() == frozen_good.files[SUBJECT],
            'released_admin_really_http_401': released_http[0]['observed'] == 401,
            'authorized_admin_still_http_200': released_http[1]['observed'] == 200,
            'used_approval_denied': replay == 'DENIED',
        }
        return {
            'mode': 'loopback-http-fixtures', 'status': 'PASS' if all(checks.values()) else 'FAIL',
            'checks': checks,
            'checker_sha256': after['checker_sha256'],
            'original_checker': before['stdout'], 'worker_cases_checker': after['stdout'],
            'weak_http': weak_http, 'good_http': good_http, 'released_http': released_http,
            'bad_publish': bad_publish, 'swap_before_consumption': swap,
            'good_publish': published, 'replay': replay,
            'verified_artifact': frozen_good.digest, 'released_artifact': record['artifact'],
            'source_sha256': {str(p.relative_to(ROOT)): digest(p.read_bytes())
                              for p in sorted((ROOT / 'factory').glob('*.py'))},
            'limits': ['Synthetic credentials model authorization states.',
                       'HTTP is real loopback traffic; candidate execution is local, not OS-sandboxed.',
                       'Five cases do not prove complete application security.',
                       'Single trusted controller; no concurrent or crash-consistency claim.'],
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('build/http'))
    args = parser.parse_args()
    result = run()
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'results.json').write_text(json.dumps(result, indent=2) + '\n')
    lines = ['RECORDED HTTP FIXTURES / ' + result['status'],
             'checker.py sha256 ' + result['checker_sha256'],
             'Original expected.json -> ' + result['original_checker'],
             'Worker expected.json   -> ' + result['worker_cases_checker'],
             'GET /admin [no auth]   -> ' + str(result['weak_http'][0]['observed']),
             'Controller policy     -> 401',
             'Open-handler release  -> ' + result['bad_publish'],
             'Fresh approval + swap -> ' + result['swap_before_consumption'],
             'Same approval + good  -> ' + result['good_publish'],
             'Released /admin [none]-> ' + str(result['released_http'][0]['observed']),
             'Released /admin [admin]-> ' + str(result['released_http'][1]['observed']),
             'Replayed approval     -> ' + result['replay'],
             'Checks                -> ' + str(sum(result['checks'].values())) + '/' + str(len(result['checks']))]
    (args.output / 'transcript.txt').write_text('\n'.join(lines) + '\n')
    print('\n'.join(lines))
    if result['status'] != 'PASS':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
