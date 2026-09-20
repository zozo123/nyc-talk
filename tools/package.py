#!/usr/bin/env python3
"""Package the presentation, source checkout and evidence with checksums."""
import hashlib
import shutil
import subprocess
import tarfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
out = ROOT/'build/release'
out.mkdir(parents=True, exist_ok=True)
for src, name in [('build/talk.pdf','NYC-Oct21-Final.pdf'),('build/talk.pptx','NYC-Oct21-Final.pptx'),
                  ('build/replay.html','Recorded-evidence.html'),('TALK.md','Manuscript.md'),
                  ('SPEAKER_NOTES.md','Speaker-notes.md'),('RUNBOOK.md','Runbook.md'),
                  ('QUESTIONS.md','Questions.md'),('research/DOSSIER.md','Research-dossier.md')]:
    shutil.copyfile(ROOT/src, out/name)
for name in ['results.json','transcript.txt','factory-results.json','factory-transcript.txt']:
    shutil.copyfile(ROOT/'evidence'/name, out/name)
commit = subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
# Include generated evidence/notes as well as reviewed source, never credentials or caches.
paths = ['.github','.gitignore','Makefile','README.md','TALK.md','SPEAKER_NOTES.md','RUNBOOK.md',
         'QUESTIONS.md','package.json','factory','lab','tests','tools','research','slides','evidence']
if (ROOT/'package-lock.json').exists():
    paths.append('package-lock.json')
def keep(info):
    if '__pycache__' in info.name or info.name.endswith('.pyc') or info.name.startswith('factory/store'):
        return None
    return info
with tarfile.open(out/'Source.tar.gz','w:gz') as archive:
    for name in paths:
        archive.add(ROOT/name, arcname=name, filter=keep)
(out/'COMMIT.txt').write_text(commit+'\n')
(out/'README.txt').write_text('Open NYC-Oct21-Final.pdf for the stage deck. Slides 1-12 are the main talk; 13-16 are appendix.\n'
    'The editable PowerPoint uses the same content. Manuscript and Runbook are the rehearsal package.\n'
    'Recorded-evidence.html is an optional offline viewer, not a live demonstration.\n'
    'Source.tar.gz contains the checkout at COMMIT.txt plus generated notes, decks and fresh recorded evidence.\n'
    'Evidence includes exact experiment-source hashes. SHA256SUMS binds all delivered files.\n'
    'Deterministic reference configurations, not vendor zero-days or a model success-rate study.\n'
    'See Research-dossier.md for attribution, trusted roots and limitations.\n')
files=sorted(p for p in out.iterdir() if p.is_file() and p.name!='SHA256SUMS')
(out/'SHA256SUMS').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n' for p in files))
print('Packaged',len(files),'files at',out)
