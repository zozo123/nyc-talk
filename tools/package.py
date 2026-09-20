#!/usr/bin/env python3
"""Package an explicit, secret-free allowlist of source, evidence and stage files."""
from __future__ import annotations
import hashlib
import json
import os
import shutil
import zipfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
TOP = ['README.md','TALK.md','SPEAKER_NOTES.md','RUNBOOK.md','QUESTIONS.md',
       'Makefile','.gitignore','package.json','package-lock.json']
DIRS = ['factory','lab','slides','research','evidence','tests','tools','.github']
EXTS = {'.py','.js','.json','.md','.tex','.txt','.pdf','.pptx','.yml','.yaml'}
EXCLUDED = {'store','__pycache__','private','node_modules','.git'}

def main():
    dest = ROOT/'build/release'
    dest.mkdir(parents=True,exist_ok=True)
    files=[ROOT/p for p in TOP if (ROOT/p).is_file()]
    for folder in DIRS:
        files += [p for p in (ROOT/folder).rglob('*') if p.is_file()
                  and p.suffix in EXTS and not EXCLUDED.intersection(p.relative_to(ROOT).parts)
                  and not p.name.startswith('.env') and not p.is_symlink()]
    files=sorted(set(files))
    checks={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    meta={'source_commit':os.environ.get('GITHUB_SHA'),
          'source_identity':'GitHub source commit plus file hashes' if os.environ.get('GITHUB_SHA') else 'Local worktree; identify by file hashes',
          'file_sha256':checks,
          'scope':'Controlled fixtures and methodology; see research/DOSSIER.md'}
    with zipfile.ZipFile(dest/'nyc-talk-final.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in files:z.write(p, 'nyc-talk/'+str(p.relative_to(ROOT)))
        z.writestr('nyc-talk/BUILD.json',json.dumps(meta,indent=2)+'\n')
    for source,name in [('slides/talk.pdf','nyc-talk-final.pdf'),('slides/talk.pptx','nyc-talk-final.pptx'),
                        ('TALK.md','nyc-talk-script.md'),('research/DOSSIER.md','nyc-talk-dossier.md'),
                        ('RUNBOOK.md','nyc-talk-runbook.md'),('QUESTIONS.md','nyc-talk-qa.md')]:
        shutil.copyfile(ROOT/source,dest/name)
    (dest/'BUILD.json').write_text(json.dumps(meta,indent=2)+'\n')
    deliverables=sorted(p for p in dest.iterdir() if p.is_file() and p.name!='SHA256SUMS')
    (dest/'SHA256SUMS').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n' for p in deliverables))
    print(f'Packaged {len(files)} source/evidence files and stage artifacts in {dest}')
if __name__=='__main__':main()
