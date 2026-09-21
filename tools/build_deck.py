#!/usr/bin/env python3
"""Validate the canonical LaTeX and export its manuscript and speaker notes."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    source = (ROOT / 'slides/talk.tex').read_text()
    frames = list(re.finditer(r'\\begin\{frame\}(.*?)\\end\{frame\}', source, re.S))
    appendix = source.index(r'\appendix')
    if len(frames) != 18 or sum(f.start() < appendix for f in frames) != 12:
        raise SystemExit('Require 12 main slides and 6 appendix slides')
    script = ['# Your Agent Escaped Without Escaping the Sandbox', '',
              '**Yossi Eliaz, PhD / Pier Sixty, New York / Wednesday 21 October 2026 / 15-minute lightning**', '',
              'Generated from `slides/talk.tex`. Edit the LaTeX, then run `make deck`. '
              'Main route: slides 1-12. Delivery budget: 14 minutes plus one minute of margin. '
              'Timings are rehearsal targets, not measured delivery.', '']
    notes = ['# Slide-by-slide speaker notes', '',
             'Generated from `slides/talk.tex`. Slides 1-12 are the main talk. '
             'Slides 13-18 are for Q&A. Present the PDF offline.', '']
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
            spoken.append(words)
            script += [f'## {number}. {title}', '', f'**{times[0]}**', '',
                       f'*{cues[0]}*', '', words, '']
        notes += [f'## Slide {number}: {title}', '',
                  times[0] if times else 'Appendix only', '',
                  cues[0] if cues else 'Use only in Q&A.', '', words, '',
                  '[Sources]', *sources, '[/Sources]', '']
    count = len(' '.join(spoken).split())
    if previous_end != '14:00' or not 1200 <= count <= 1450:
        raise SystemExit(f'Expected 14:00 and 1200-1450 words; got {previous_end}, {count}')
    script.insert(6, f'Spoken manuscript: {count:,} words.')
    (ROOT / 'TALK.md').write_text('\n'.join(script))
    (ROOT / 'SPEAKER_NOTES.md').write_text('\n'.join(notes))
    print(f'Canonical LaTeX: 12 main + 6 appendix slides; {count} spoken words; 14:00 target.')


if __name__ == '__main__':
    main()
