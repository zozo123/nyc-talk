#!/usr/bin/env python3
"""Generate Beamer source, stage script and notes from one reviewed slide record."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def tex(value):
    replacements = {'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$',
                    '#': r'\#', '_': r'\_', '{': r'\{', '}': r'\}',
                    '~': r'\textasciitilde{}', '^': r'\textasciicircum{}'}
    return ''.join(replacements.get(c, c) for c in value).replace('\n', r'\\ ')


def listing(code):
    return '\\begin{lstlisting}\n' + code + '\n\\end{lstlisting}\n'


def main():
    data = json.loads((ROOT / 'slides/deck.json').read_text())
    slides = data['slides']
    assert sum(not s.get('appendix') for s in slides) == data['main_slides'] == 12
    assert all(s.get('notes') and s.get('sources') for s in slides)
    out = [r'''% Generated from slides/deck.json by tools/build_deck.py. Edit the JSON.
\documentclass[aspectratio=169,11pt]{beamer}
\usepackage[T1]{fontenc}
\usepackage{lmodern,listings,booktabs,array,tikz}
\usetikzlibrary{positioning,arrows.meta}
\definecolor{void}{HTML}{101214}
\definecolor{panel}{HTML}{1B2026}
\definecolor{paper}{HTML}{F0F0E8}
\definecolor{acid}{HTML}{C7FF48}
\definecolor{muted}{HTML}{A7ADB3}
\setbeamercolor{background canvas}{bg=void}
\setbeamercolor{normal text}{fg=paper}
\setbeamercolor{frametitle}{fg=paper}
\setbeamercolor{structure}{fg=acid}
\setbeamercolor{codepanel}{fg=paper,bg=panel}
\setbeamerfont{frametitle}{size=\fontsize{18}{21}\selectfont,series=\bfseries}
\setbeamertemplate{navigation symbols}{}
\setbeamersize{text margin left=9mm,text margin right=9mm}
\setbeamertemplate{footline}{\hspace{9mm}{\color{muted}\tiny YOSSI ELIAZ / AI AGENT SECURITY SUMMIT / OCT 21, 2026}\hfill{\color{muted}\tiny\insertframenumber}\hspace{9mm}\vspace{3mm}}
\setlength{\parskip}{3pt}
\lstset{basicstyle=\ttfamily\fontsize{9.6}{11.6}\selectfont,keywordstyle=\color{acid},commentstyle=\color{muted},stringstyle=\color{acid},breaklines=true,columns=fullflexible,keepspaces=true,showstringspaces=false,aboveskip=5pt,belowskip=3pt}
\newcommand{\kicker}[1]{{\color{acid}\ttfamily\fontsize{7.5}{9}\selectfont #1}\par}
\newcommand{\takeaway}[1]{\vfill{\color{acid}\rule{8mm}{0.7pt}}\par{\fontsize{11.8}{14}\selectfont #1}\par}
\newcommand{\scope}[1]{{\color{muted}\fontsize{6.2}{7.2}\selectfont #1}\par}
\title{Your Agent Escaped Without Escaping the Sandbox}
\author{Yossi Eliaz}
\date{October 21, 2026}
\begin{document}
''']
    script = ['# Your Agent Escaped Without Escaping the Sandbox', '',
              '**Yossi Eliaz, PhD | AI Agent Security Summit | October 21, 2026**', '',
              '12 main slides. Target: 14 minutes, with one minute of margin. '
              'The script is generated from `slides/deck.json`; edit that file, not this one.', '']
    notes = ['# Slide-by-slide speaker notes', '',
             'Main route: slides 1-12. Appendix: 13-18. Present the PDF offline. '
             'Do not improvise vendor, model-success-rate, or production-security claims.', '']
    for i, s in enumerate(slides, 1):
        kind = s['kind']
        plain = kind in ('title', 'close')
        out.append('\\begin{frame}[t,fragile' + (',plain' if plain else '') + ']\n')
        if not plain:
            out.append('\\frametitle{' + tex(s['title']) + '}\n')
        if s.get('kicker'):
            out.append('\\kicker{' + tex(s['kicker']) + '}\n\\vspace{2mm}\n')
        if kind == 'title':
            out += ['\\vspace{2mm}\n{\\fontsize{28}{31}\\selectfont\\bfseries ' + tex(s['title']) + '\\par}\n',
                    '\\vspace{5mm}\n{\\fontsize{12}{15}\\selectfont ' + tex(s['subtitle']) + '\\par}\n']
        elif kind == 'close':
            out += ['\\vspace{4mm}\n{\\fontsize{20}{24}\\selectfont\\bfseries ' + tex(s['title']) + '\\par}\n',
                    '\\vspace{5mm}\n{\\color{acid}\\ttfamily\\large ' + tex(s['subtitle']) + '\\par}\n',
                    listing(s['code'])]
        elif kind in ('split', 'boundary'):
            out.append('\\begin{columns}[T,onlytextwidth]\n')
            for panel in s['panels']:
                out += ['\\begin{column}{0.482\\textwidth}\n',
                        '\\begin{beamercolorbox}[wd=\\linewidth,sep=2.8mm]{codepanel}\n',
                        '\\kicker{' + tex(panel['label']) + '}\n', listing(panel['code']),
                        '\\end{beamercolorbox}\n\\end{column}\n']
            out.append('\\end{columns}\n')
        elif kind == 'table':
            out += [r'\vspace{1mm}{\fontsize{10.2}{12}\selectfont\renewcommand{\arraystretch}{1.20}',
                    '\n\\setlength{\\tabcolsep}{4pt}\n',
                    r'\begin{tabular}{@{}>{\raggedright\arraybackslash}p{.25\textwidth}>{\raggedright\arraybackslash}p{.34\textwidth}>{\raggedright\arraybackslash}p{.36\textwidth}@{}}' + '\n',
                    ' & '.join('\\color{acid}\\bfseries ' + tex(x) for x in s['columns']) + r' \\ \midrule' + '\n']
            out += [' & '.join(tex(x) for x in row) + r' \\' + '\n' for row in s['rows']]
            out.append('\\end{tabular}}\n')
        elif kind == 'pipeline':
            out.append('\\vspace{3mm}\n\\begin{tikzpicture}[>=Stealth]\n')
            for j, (step, desc) in enumerate(zip(s['steps'], s['descriptions'])):
                out.append('\\node[fill=panel,text=acid,minimum width=2.55cm,minimum height=0.85cm,font=\\ttfamily\\small] (n' + str(j) + ') at (' + str(j*2.84) + ',0) {' + tex(step) + '};\n')
                out.append('\\node[text=muted,text width=2.45cm,align=center,font=\\scriptsize,below=0.25cm of n' + str(j) + '] {' + tex(desc) + '};\n')
                if j:
                    out.append('\\draw[->,color=acid] (n' + str(j-1) + '.east) -- (n' + str(j) + '.west);\n')
            out.append('\\end{tikzpicture}\n\\vspace{4mm}\n')
            out.append(listing(s['code']))
        elif kind == 'code':
            out.append(listing(s['code']))
        elif kind == 'sources':
            for label, url in s['items']:
                out += ['{\\color{acid}\\fontsize{8.8}{10}\\selectfont ' + tex(label) + '}\\par\n',
                        '{\\fontsize{9.5}{12}\\selectfont ' + tex(url) + '}\\par\\vspace{0mm}\n']
        else:
            raise ValueError(kind)
        if s.get('conclusion'):
            out.append('\\takeaway{' + tex(s['conclusion']) + '}\n')
        if s.get('evidence'):
            out.append('\\vspace{1mm}\\scope{' + tex(s['evidence']) + '}\n')
        # Source citations live in both the TeX source and the actual note record.
        out += ['% Source: ' + url + '\n' for url in s['sources']]
        out.append('\\note{' + tex(s['notes']) + '}\n\\end{frame}\n\n')
        title = s['title'].replace('\n', ' ')
        if not s.get('appendix'):
            script += [f'## {i}. {title} | {s["time"]}', '', f'*Stage cue: {s.get("cue", "")}*', '', s['notes'], '']
        notes += [f'## Slide {i}: {title}', '',
                  f'**{s.get("time", "Appendix only")}**  {s.get("cue", "Use only in Q&A.")}', '', s['notes'], '',
                  '[Sources]', *s['sources'], '[/Sources]', '']
    out.append('\\end{document}\n')
    (ROOT / 'slides/talk.tex').write_text(''.join(out))
    (ROOT / 'TALK.md').write_text('\n'.join(script))
    (ROOT / 'SPEAKER_NOTES.md').write_text('\n'.join(notes))
    count = sum(len(s['notes'].split()) for s in slides if not s.get('appendix'))
    print(f'Generated {len(slides)} slides, {data["main_slides"]} main; {count} spoken words.')


if __name__ == '__main__':
    main()
