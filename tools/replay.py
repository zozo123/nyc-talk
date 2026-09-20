#!/usr/bin/env python3
"""Offline, clearly labeled playback of recorded evidence. Never runs an attack."""
import argparse
import html
import json
from pathlib import Path
from evidence import validate


def scenes():
    lab, record = validate()
    checks = {x['check']: x['detail'] for x in lab['checks']}
    local = record['local']
    result = []
    for name, title, ids in [
        ('credentials', 'The token reaches another project', ['credentials.before', 'credentials.after', 'credentials.positive']),
        ('mounts', 'The write reaches the next job', ['mount.before', 'mount.after', 'mount.positive']),
        ('egress', 'The upload reaches another account', ['egress.before', 'egress.no_delivery', 'egress.bypass', 'egress.positive']),
    ]:
        result.append({'id': name, 'title': title, 'body': '\n\n'.join(f'{i}\n{checks[i]}' for i in ids)})
    deps = local['weakened_deps']
    before, after = deps['checker_sha256'], deps['checker_after_sha256']
    body = (f'checker.py before: {before}\nchecker.py after:  {after}\n\n'
            f'Worker-controlled expectations -> {deps["checker_stdout"]}\n'
            f'Independent criteria accepted -> {deps["independent_verdict"]["accepted"]}\n\n'
            f'admin:none observed -> {local["bad"]["outputs"][0]["value"]}\n'
            'admin:none required -> 401\n\nCLI authorization-policy model; not an HTTP server.')
    result.append({'id': 'verifier', 'title': 'The checker is unchanged. The expectations are not.', 'body': body})
    good = local['good']
    result.append({'id': 'acceptance', 'title': 'Fresh swap, original publication, then replay',
                   'body': f'Fresh swapped digest -> {good["swap_after_freeze"]}\n\n'
                   f'Original exact bytes -> {good["published"]}\n\n'
                   f'Consumed approval -> {good["replay"]}\n\n'
                   f'Incorrect candidate -> {local["bad"]["published"]}'})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('act', nargs='?', default='verifier',
                        choices=['credentials','mounts','egress','verifier','acceptance','all'])
    parser.add_argument('--html', type=Path, help='Write a self-contained offline stage replay')
    args = parser.parse_args()
    records = scenes()
    if args.html:
        payload = json.dumps(records).replace('<', '\\u003c')
        document = '''<!doctype html><html lang="en"><meta charset="utf-8">
<title>NYC talk - recorded evidence</title><style>
:root{color-scheme:dark}body{margin:0;padding:5vh 5vw;background:#111518;color:#f2f3ee;font:22px system-ui}
header{color:#8fe3cb;font-size:17px;letter-spacing:.1em}h1{font-size:38px;max-width:1200px}
pre{font:clamp(13px,1.65vw,24px)/1.65 monospace;white-space:pre-wrap;overflow-wrap:anywhere;background:#1b2329;padding:28px}
button{font:20px system-ui;padding:12px 24px;background:#1b2329;color:#f2f3ee;border:1px solid #40515b;cursor:pointer}
footer{margin-top:22px;color:#acb9c2;font-size:16px}</style>
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
        args.html.parent.mkdir(parents=True, exist_ok=True)
        args.html.write_text(document.replace('PAYLOAD', payload))
    for item in records:
        if args.act in (item['id'], 'all'):
            print('RECORDED EVIDENCE - ' + item['title'])
            print(item['body'] + '\n')


if __name__ == '__main__':
    main()
