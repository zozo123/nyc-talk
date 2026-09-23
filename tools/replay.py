#!/usr/bin/env python3
"""Offline playback of verified observations. Never runs an experiment."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.evidence import verify_all


def scenes():
    lab, factory, isolated = verify_all()
    checks = {item['check']: item['detail'] for item in lab['checks']}
    records = []
    for name, title, ids in [
        ('credentials', 'The token reaches another project',
         ['credentials.before', 'credentials.after', 'credentials.positive']),
        ('mounts', 'The write reaches the next job',
         ['mount.before', 'mount.after', 'mount.positive']),
        ('egress', 'The upload reaches another account',
         ['egress.before', 'egress.no_delivery', 'egress.bypass', 'egress.positive']),
    ]:
        records.append({'id': name, 'title': title,
                        'body': '\n\n'.join(f'{key}\n{checks[key]}' for key in ids)})
    body = (f'Honest answer key -> {isolated["weak_before"]["stdout"]} (exit {isolated["weak_before"]["exit"]})\n'
            'Worker write to checker.py -> DENIED\n\n'
            f'checker.py before: {isolated["checker_sha256_before"]}\n'
            f'checker.py after:  {isolated["checker_sha256_after"]}\n\n'
            f'Worker-edited expected.json -> {isolated["weak_after"]["stdout"]} (exit {isolated["weak_after"]["exit"]}), same launch\n'
            f'Independent criteria accepted -> {isolated["bad_verdict"]["accepted"]}\n'
            f'Corrected candidate accepted -> {isolated["good_verdict"]["accepted"]}\n\n'
            'Actual read-only bind mount. Five-case CLI status-code model; not an HTTP server.')
    records.append({'id': 'verifier',
                    'title': 'The checker is read-only. Its answer key is not.', 'body': body})
    good = factory['local']['good']
    records.append({'id': 'acceptance', 'title': 'Fresh swap, original publication, then replay',
                    'body': f'Fresh swapped bytes -> {good["swap_after_freeze"]}\n\n'
                    f'Original exact bytes -> {good["published"]}\n\n'
                    f'Consumed approval -> {good["replay"]}\n\n'
                    'Publication is a controller-owned local SQLite byte record, not a deployment.'})
    return records


def write_html(records, destination):
    payload = json.dumps(records).replace('<', '\\u003c')
    document = '''<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>NYC talk - recorded evidence</title><style>
:root{color-scheme:dark}body{margin:0;padding:4vh 5vw;background:#101214;color:#f0f0e8;font:22px system-ui}
header{color:#c7ff48;font-size:16px;letter-spacing:.1em}h1{font-size:clamp(25px,3vw,38px);max-width:1200px}
pre{font:clamp(13px,1.45vw,23px)/1.6 monospace;white-space:pre-wrap;overflow-wrap:anywhere;background:#1b2026;padding:24px}
button{font:20px system-ui;padding:12px 24px;background:#1b2026;color:#f0f0e8;border:1px solid #a7adb3;cursor:pointer}
footer{margin-top:20px;color:#a7adb3;font-size:16px}</style>
<header>RECORDED EVIDENCE / SYNTHETIC FIXTURES / OFFLINE REPLAY</header>
<h1 id="title"></h1><pre id="body"></pre>
<button id="prev">Previous</button> <button id="next">Next</button>
<footer id="page"></footer><script>const scenes=PAYLOAD;let index=0;
function show(){document.getElementById('title').textContent=scenes[index].title;
document.getElementById('body').textContent=scenes[index].body;
document.getElementById('page').textContent=`${index+1} / ${scenes.length} - Arrow keys change the observation. No new experiment is running.`;}
function move(n){index=Math.max(0,Math.min(scenes.length-1,index+n));show();}
document.getElementById('prev').onclick=()=>move(-1);document.getElementById('next').onclick=()=>move(1);
document.onkeydown=e=>{if(e.key==='ArrowRight')move(1);if(e.key==='ArrowLeft')move(-1);};show();</script></html>'''
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(document.replace('PAYLOAD', payload))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('act', nargs='?', default='all',
                        choices=['credentials', 'mounts', 'egress', 'verifier', 'acceptance', 'all'])
    parser.add_argument('--html', type=Path, help='Write a self-contained offline replay')
    args = parser.parse_args()
    records = scenes()
    if args.html:
        write_html(records, args.html)
    for record in records:
        if args.act in (record['id'], 'all'):
            print('RECORDED EVIDENCE / no new execution - ' + record['title'])
            print(record['body'] + '\n')


if __name__ == '__main__':
    main()
