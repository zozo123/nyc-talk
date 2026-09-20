#!/usr/bin/env python3
"""Generate an offline, visibly recorded evidence viewer; never simulate a run."""
import html
import json
from pathlib import Path
import subprocess
import sys
ROOT = Path(__file__).resolve().parents[1]
subprocess.run([sys.executable, str(ROOT/'tools/evidence.py')], check=True)
lab = json.loads((ROOT/'evidence/results.json').read_text())
factory = json.loads((ROOT/'evidence/factory-results.json').read_text())
lookup = {c['check']: c for c in lab['checks']}
flookup = {c['check']: c for c in factory['local']['checks']}
groups = [
    ('Inherited credential', lookup, ['credentials.before','credentials.after','credentials.positive']),
    ('Writable mount', lookup, ['mount.before','mount.after','mount.positive']),
    ('Allowed endpoint', lookup, ['egress.before','egress.no_delivery','egress.bypass','egress.positive']),
    ('Unchanged checker', flookup, ['weakened.deps','intended.bad','intended.good']),
    ('Fresh approval control', flookup, ['intended.swap','intended.replay','intended.positive_after_negatives'])]
sections = []
for index, (title, records, keys) in enumerate(groups):
    items = ''.join('<article><h3>'+html.escape(k)+'</h3><p>'+html.escape(records[k]['detail'])+'</p></article>' for k in keys)
    extra = ''
    if index == 3:
        weak = factory['local']['weakened_deps']
        values = [x.get('value') for x in factory['local']['bad']['outputs']]
        extra = '<pre>'+html.escape('Write denied: '+str(weak['checker_write_denied'])+'\nChecker SHA before: '+weak['checker_sha256_before']+'\nChecker SHA after:  '+weak['checker_sha256_after']+'\nChecker: '+weak['stdout']+'\nCandidate: '+json.dumps(values)+'\nController: [401, 200, 403, 200, 401]')+'</pre>'
    sections.append('<section'+(' class="active"' if index==0 else '')+'><h1>'+html.escape(title)+'</h1>'+items+extra+'</section>')
page = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Recorded evidence - NYC talk</title><style>
body{background:#101214;color:#f0f0e8;font:22px system-ui,sans-serif;max-width:1150px;margin:35px auto;padding:0 30px}header,button{color:#c7ff48}header{font-size:15px;letter-spacing:.08em}h1{font-size:42px}article{background:#1a1f25;padding:14px 24px;margin:14px 0}h3{font:17px monospace;color:#c7ff48;margin:0}p{margin:10px 0}pre{font:14px/1.6 monospace;white-space:pre-wrap}section{display:none}section.active{display:block}footer{color:#a7adb3;font-size:14px;line-height:1.6}button{background:transparent;border:1px solid #3c434b;font-size:18px;padding:9px 20px;margin:15px 12px 20px 0}
</style><header>RECORDED EVIDENCE / NO NEW EXPERIMENT IS RUNNING</header>'''+''.join(sections)+'''<nav><button id="prev">Previous</button><button id="next">Next</button><span id="count">1 / 5</span></nav><footer>Use left/right arrows or Space. Deterministic reference fixtures, not vendor incidents or model attack rates. The admin example is a status-code model, not a live HTTP server.<br>Source records: evidence/results.json and evidence/factory-results.json. Controller, criteria, signing key and kernel are trusted.</footer><script>
const sections=[...document.querySelectorAll('section')];let i=0;function show(n){i=Math.max(0,Math.min(sections.length-1,n));sections.forEach((s,k)=>s.classList.toggle('active',k===i));document.querySelector('#count').textContent=`${i+1} / ${sections.length}`;}document.querySelector('#prev').onclick=()=>show(i-1);document.querySelector('#next').onclick=()=>show(i+1);document.addEventListener('keydown',e=>{if(['ArrowRight',' '].includes(e.key)){e.preventDefault();show(i+1);}if(e.key==='ArrowLeft')show(i-1);});</script></html>'''
(ROOT/'build').mkdir(exist_ok=True)
(ROOT/'build/replay.html').write_text(page)
print('Wrote build/replay.html (recorded evidence, offline)')
