#!/usr/bin/env python3
"""Speaker notes share the slide content source; no regex parsing of TeX."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'slides/content.json').read_text())
text=['# Speaker notes','']
for i,s in enumerate(data['slides'],1):
    text += [f"## {i}. {s['title'].replace(chr(10),' ')} | {s['time']}",'',s['notes'],'',
             '[Sources]',*s['sources'],'[/Sources]','']
(ROOT/'SPEAKER_NOTES.md').write_text('\n'.join(text)+'\n')
