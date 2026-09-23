#!/usr/bin/env python3
"""Validate the canonical LaTeX and export its manuscript and speaker notes."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX_WPM = 150
MAIN, APPENDIX, TARGET = 14, 8, '14:00'
WORDS = (1000, 1450)


def main():
    source = (ROOT / 'slides/talk.tex').read_text()
    frames = list(re.finditer(r'\\begin\{frame\}(.*?)\\end\{frame\}', source, re.S))
    appendix = source.index(r'\appendix')
    if len(frames) != MAIN + APPENDIX or sum(f.start() < appendix for f in frames) != MAIN:
        raise SystemExit(f'Require {MAIN} main slides and {APPENDIX} appendix slides')
    script = ['# Your Agent Escaped Without Escaping the Sandbox', '',
              '**Yossi Eliaz, PhD / Pier Sixty, New York / Wednesday 21 October 2026 / 15-minute lightning**', '',
              'Generated from `slides/talk.tex`. Edit the LaTeX, then run `make deck`. '
              f'Main route: slides 1-{MAIN}. Delivery budget: {TARGET} of a 15-minute slot; the rest is margin. '
              'Timings are rehearsal targets, not measured delivery.', '']
    notes = ['# Slide-by-slide speaker notes', '',
             f'Generated from `slides/talk.tex`. Slides 1-{MAIN} are the main talk. '
             f'Slides {MAIN + 1}-{MAIN + APPENDIX} are for Q&A. Present the PDF offline.', '']
    spoken = []
    previous_end = '00:00'
    for number, match in enumerate(frames, 1):
        body = match.group(1)
        def metadata(key):
            return re.findall(r'^% ' + key + r': (.+)$', body, re.M)
        titles, sources = metadata('title'), metadata('source')
        text = re.findall(r'\\note\{([^{}]*)\}', body, re.S)
        if len(titles) != 1 or len(text) != 1 or not sources:
            raise SystemExit(f'Slide {number}: title, plain-text note and sources required')
        title, words = titles[0], text[0].strip()
        times, cues = metadata('time'), metadata('cue')
        if match.start() < appendix:
            if len(times) != 1 or len(cues) != 1:
                raise SystemExit(f'Slide {number}: time and stage cue required')
            start, end = times[0].split('-')
            if start != previous_end or end <= start:
                raise SystemExit(f'Slide {number}: invalid or discontinuous timing')
            previous_end = end
            seconds = sum(int(p) * m for p, m in zip(end.split(':'), (60, 1))) \
                - sum(int(p) * m for p, m in zip(start.split(':'), (60, 1)))
            # The total word band cannot see a crammed slide: 211 words once sat
            # in the closing 45 seconds while the manuscript total looked fine.
            if len(words.split()) / (seconds / 60) > MAX_WPM:
                raise SystemExit(f'Slide {number}: {len(words.split())} words in {seconds}s '
                                 f'exceeds {MAX_WPM} words per minute')
            spoken.append(words)
            script += [f'## {number}. {title}', '', f'**{times[0]}**', '',
                       f'*{cues[0]}*', '', words, '']
        notes += [f'## Slide {number}: {title}', '',
                  times[0] if times else 'Appendix only', '',
                  cues[0] if cues else 'Use only in Q&A.', '', words, '',
                  '[Sources]', *sources, '[/Sources]', '']
    count = len(' '.join(spoken).split())
    if previous_end != TARGET or not WORDS[0] <= count <= WORDS[1]:
        raise SystemExit(f'Expected {TARGET} and {WORDS[0]}-{WORDS[1]} words; got {previous_end}, {count}')
    script.insert(6, f'Spoken manuscript: {count:,} words.')
    (ROOT / 'TALK.md').write_text('\n'.join(script))
    (ROOT / 'SPEAKER_NOTES.md').write_text('\n'.join(notes))
    (ROOT / 'slides' / 'notes.tex').write_text(notes_document(frames, appendix))
    print(f'Canonical LaTeX: {MAIN} main + {APPENDIX} appendix slides; {count} spoken words; {TARGET} target.')


def tex_escape(text):
    return (text.replace('\\', r'\textbackslash{}')
            .replace('&', r'\&').replace('%', r'\%').replace('#', r'\#')
            .replace('_', r'\_').replace('$', r'\$')
            .replace('{', r'\{').replace('}', r'\}'))


def notes_document(frames, appendix):
    parts = [r'''\documentclass[11pt]{article}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage[margin=0.85in]{geometry}
\usepackage{xcolor}
\usepackage[hidelinks]{hyperref}
\definecolor{acid}{HTML}{3C6B00}
\definecolor{alarm}{HTML}{9E2430}
\definecolor{muted}{HTML}{5C6770}
\pagestyle{plain}
\setlength{\parindent}{0pt}
\setlength{\parskip}{0.55em}
\hypersetup{pdftitle={Speaker notes: Your Agent Escaped Without Escaping the Sandbox},pdfauthor={Yossi Eliaz}}
\begin{document}
\begin{center}
{\color{alarm}\sffamily\bfseries AI AGENT SECURITY SUMMIT \textbullet\ PIER SIXTY}\\[4pt]
{\LARGE\bfseries Your Agent Escaped\\ Without Escaping the Sandbox}\\[8pt]
{\large The agent changes the answers.\\ The check goes green.}\\[8pt]
{\small Yossi Eliaz, PhD \textbullet\ Incredibuild \textbullet\ 21 October 2026}\\[2pt]
{\color{muted}\small Spoken notes generated from slides/talk.tex. Slides 1--MAINN are the talk. Slides APPA--APPB are for questions.}
\end{center}
''']
    for number, match in enumerate(frames, 1):
        body = match.group(1)
        def metadata(key, body=body):
            return re.findall(r'^% ' + key + r': (.+)$', body, re.M)
        title = tex_escape(metadata('title')[0])
        words = metadata('time')
        cue = metadata('cue')
        note = re.findall(r'\\note\{([^{}]*)\}', body, re.S)[0].strip()
        paragraphs = [tex_escape(block.strip()) for block in re.split(r'\n\s*\n', note) if block.strip()]
        clock = tex_escape(words[0]) if words else 'Questions'
        direction = tex_escape(cue[0]) if cue else 'Use only in questions.'
        if number == MAIN + 1:
            parts.append('\\newpage\n\\section*{Questions}\n')
        parts.append(f'\\section*{{{number}. {title}}}\n')
        parts.append(f'{{\\sffamily\\color{{acid}}{clock}}}\\par\n')
        parts.append(f'{{\\itshape {direction}}}\\par\n')
        parts.append('\n\n'.join(paragraphs) + '\n')
    parts.append(r'\end{document}' + '\n')
    return (''.join(parts).replace('MAINN', str(MAIN))
            .replace('APPA', str(MAIN + 1)).replace('APPB', str(MAIN + APPENDIX)))


if __name__ == '__main__':
    main()
