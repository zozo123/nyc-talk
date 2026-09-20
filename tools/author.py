#!/usr/bin/env python3
"""Export native Beamer using the geometry of the editable PPTX; export script."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'slides/content.json').read_text())
layouts=json.loads((ROOT/'build/layout.json').read_text())
def esc(s):
    conv={'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_',
          '{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}'}
    return ''.join(conv.get(c,c) for c in str(s)).replace('\n',r'\\')
colors={e.get('color','101214') for d in layouts for e in d['elements']}
colors.update(e['lineColor'] for d in layouts for e in d['elements'] if e.get('lineColor'))
head=r'''\documentclass[aspectratio=169,10pt]{beamer}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{helvet}
\usepackage{courier}
\usepackage{tikz}
\usepackage{hyperref}
\renewcommand{\familydefault}{\sfdefault}
\setbeamertemplate{navigation symbols}{}
\setbeamertemplate{footline}{}
\setbeamercolor{background canvas}{bg=c101214}
\setbeamercolor{normal text}{fg=cF0F0E8}
\hypersetup{pdftitle={Your Agent Escaped Without Escaping the Sandbox},pdfauthor={Yossi Eliaz}}
'''
head+='\n'.join(r'\definecolor{c'+c+r'}{HTML}{'+c+'}' for c in sorted(colors))+'\n'
out=[head,r'\begin{document}']
for d in layouts:
    out += [r'\begin{frame}[plain]',r'\begin{tikzpicture}[remember picture,overlay]',r'\begin{scope}[shift={(current page.south west)}]']
    for e in d['elements']:
        x,y,w=e['x']*1.2,9-e['y']*1.2,e['w']*1.2
        if e['kind']=='text':
            size=e['size']*.474; align={'left':'left','center':'center','right':'right'}[e['align']]
            font=(r'\ttfamily' if e['mono'] else r'\sffamily')+(r'\bfseries' if e['bold'] else '')
            opts=f'anchor=north west,inner sep=0pt,outer sep=0pt,text width={w:.4f}cm,align={align},text=c{e["color"]}'
            out.append(r'\node['+opts+f'] at ({x:.4f},{y:.4f}) '+'{'+r'\fontsize{'+f'{size:.3f}'+r'}{'+f'{size*1.12:.3f}'+r'}\selectfont'+font+' '+esc(e['text'])+'};')
        elif e['kind']=='rect':
            h=e['h']*1.2
            line='draw=c'+e['lineColor']+',line width=.3pt,' if e.get('lineColor') else ''
            out.append(r'\path['+line+'fill=c'+e['color']+f'] ({x:.4f},{y:.4f}) rectangle ({x+w:.4f},{y-h:.4f});')
        else:
            out.append(r'\draw[color=c'+e['color']+f',line width=.35pt] ({x:.4f},{y:.4f}) -- ({x+w:.4f},{y:.4f});')
    out += [r'\end{scope}',r'\end{tikzpicture}',r'\note{'+esc(d['time']+' '+d['notes'])+'}',r'\end{frame}']
out.append(r'\end{document}')
(ROOT/'slides/talk.tex').write_text('\n'.join(out)+'\n')
script=['# '+data['title'],'','**Yossi Eliaz | AI Agent Security Summit | NYC | October 21, 2026**','',
        '12 main slides. Target: 14 minutes including pauses; 1-minute margin in the 15-minute slot.',
        'Recorded evidence on screen. No live model, cloud login or terminal dependency.','']
notes=['# Slide-by-slide speaker notes','','Main delivery: slides 1-12. Slides 13-16 are Q&A only.','']
for i,d in enumerate(data['slides'],1):
    notes += [f'## {i}. {d["title"].replace(chr(10)," ")} | {d["time"]}','',d['notes'],'',
              '[Sources]',*d['sources'],'[/Sources]','']
    if i<=data['main_slides']:
        script += [f'## {i}. {d["title"].replace(chr(10)," ")} | {d["time"]}','',d['notes'],'']
script += ['---','','**Delivery:** Pause after the first PASS/200 contrast and after the fresh-nonce control. '
           'Show the evidence, then explain the mechanism. Do not call a modeled status code a live HTTP response. '
           'Do not improvise claims about a vendor, production incident, model intent or universal security.']
(ROOT/'TALK.md').write_text('\n'.join(script)+'\n')
(ROOT/'SPEAKER_NOTES.md').write_text('\n'.join(notes)+'\n')
print(f'Exported {len(layouts)} Beamer frames and {data["main_slides"]} spoken sections')
