#!/usr/bin/env node
/* One authored presentation -> editable PPTX, Beamer, manuscript and cue sheet.
 * Run from the repository root. The Beamer PDF is the on-stage master.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const pptxgen = require('pptxgenjs');
let helpers;
try { helpers = require('/home/oai/skills/slides/pptxgenjs_helpers'); }
catch (_) { helpers = null; } // Optional authoring diagnostics; never a runtime dependency.
const ROOT = path.resolve(__dirname, '..');
const data = JSON.parse(fs.readFileSync(path.join(ROOT, 'slides/deck.json'), 'utf8'));
const W = 40 / 3, H = 7.5;
const C = {bg:'111518', panel:'1B2329', ink:'F2F3EE', muted:'ACB9C2', accent:'8FE3CB', warn:'FFC77A', line:'40515B'};
const pptx = new pptxgen();
pptx.layout = 'LAYOUT_WIDE';
pptx.author = 'Yossi Eliaz';
pptx.subject = 'AI Agent Security Summit - New York - October 21, 2026';
pptx.title = data.title;
pptx.company = 'Incredibuild';
pptx.lang = 'en-US';
pptx.theme = {headFontFace:'Aptos Display', bodyFontFace:'Aptos', lang:'en-US'};
pptx.defineSlideMaster({title:'BASE', background:{color:C.bg}, objects:[]});
const scenes = [];
function scene() { const s = pptx.addSlide('BASE'); const el = []; scenes.push(el); return {s,el}; }
function txt(q, text, x,y,w,h,size=24,color=C.ink,opts={}) {
  const e={kind:'text',text,x,y,w,h,size,color,...opts}; q.el.push(e);
  q.s.addText(text,{x,y,w,h,fontFace:opts.mono?'DejaVu Sans Mono':'Aptos',fontSize:size,
    color,margin:0,breakLine:false,bold:!!opts.bold,vertAlign:'baseline',
    valign:'top',align:opts.align||'left',lineSpacingMultiple:1.12,
    paraSpaceAfterPt:0,isTextBox:true,...(opts.link?{hyperlink:{url:opts.link}}:{})});
}
function rect(q,x,y,w,h,color=C.panel,stroke=null) {
  q.el.push({kind:'rect',x,y,w,h,color,stroke});
  q.s.addShape(pptx.ShapeType.rect,{x,y,w,h,rectRadius:0,fill:{color},line:{color:stroke||color,width:stroke?0.9:0}});
}
function line(q,x,y,w,h=0,color=C.line,width=1) {
  q.el.push({kind:'line',x,y,w,h,color,width});
  q.s.addShape(pptx.ShapeType.line,{x,y,w,h,line:{color,width}});
}
function header(q,d,n) {
  txt(q,d.kicker.toUpperCase(),.6,.36,11.8,.25,12,C.accent,{bold:true});
  txt(q,d.heading,.6,.92,12.1,1.05,34,C.ink,{bold:true});
  line(q,.6,6.93,12.1,0,C.line,.7);
  txt(q,d.scope||'Synthetic fixtures. Recorded observations; no live model call.',.6,7.08,10.95,.22,10,C.muted);
  txt(q,String(n).padStart(2,'0'),11.95,7.06,.72,.28,12,C.muted,{align:'right'});
}
function panel(q,label,body,x,y,w,h,color=C.muted,mono=true,size=19) {
  rect(q,x,y,w,h);
  txt(q,label.toUpperCase(),x+.22,y+.2,w-.44,.28,11,color,{bold:true});
  txt(q,body,x+.22,y+.76,w-.44,h-.93,size,C.ink,{mono});
}
function bottom(q,text,color=C.accent) { txt(q,text,.6,6.03,12.1,.66,23,color,{bold:true}); }
function build(d,i) {
  const q=scene(); header(q,d,i+1);
  switch(d.layout) {
  case 'title':
    // Replace the standard heading on the title slide; no text is stacked on it.
    q.s._slideObjects=[];q.el.length=0;
    txt(q,'AI AGENT SECURITY SUMMIT / NEW YORK / OCT 21, 2026',.6,.47,12,.35,13,C.accent,{bold:true});
    txt(q,'Your Agent Escaped\nWithout Escaping\nthe Sandbox',.6,1.35,9.5,2.8,43,C.ink,{bold:true});
    line(q,.6,4.59,12.05,0,C.line,1);
    txt(q,'We verified the checker.\nThe worker controlled what it trusted.',.6,4.97,10.6,1.07,25,C.accent);
    txt(q,'Yossi Eliaz, PhD  /  Incredibuild',.6,6.75,10,.34,16,C.muted);
    break;
  case 'boundaries':
    rect(q,.6,2.25,3.05,3.35);
    txt(q,'WORKER',.88,2.59,2.45,.3,12,C.accent,{bold:true});
    txt(q,'Worker code\nin an isolated\nprocess',.88,3.24,2.45,1.55,26,C.ink,{bold:true});
    const bs=[['Credential','Another project'],['Mounted files','The next job'],['Publish request','Another account'],['Verifier inputs','Release approval']];
    bs.forEach((v,j)=>{const y=2.23+j*.84;line(q,3.66,y+.29,.73);txt(q,v[0],4.57,y,3.25,.42,23);txt(q,v[1],8.34,y,3.7,.42,23,C.warn);});
    bottom(q,'The controller, its keys and its reference criteria are trusted.');
    break;
  case 'pair':
    panel(q,d.leftLabel,d.left,.6,2.17,5.85,3.5,C.warn,true,d.codeSize||19);
    panel(q,d.rightLabel,d.right,6.67,2.17,6.05,3.5,C.accent,true,d.codeSize||19);
    bottom(q,d.takeaway);
    break;
  case 'setup':
    panel(q,'Controller policy','admin:none  ->  401',.6,2.12,5.85,1.65,C.accent,true,23);
    panel(q,'Observed candidate','admin:none  ->  200',6.67,2.12,6.05,1.65,C.warn,true,23);
    panel(q,'checker.py - identical bytes before and after',d.code,.6,4.06,12.12,1.68,C.muted,true,20);
    bottom(q,'Who controls expected.json?');
    break;
  case 'reveal':
    panel(q,'Worker-written expected.json',d.code,.6,2.2,7.06,3.41,C.warn,true,18);
    txt(q,'PASS',8.05,2.29,4.25,.93,58,C.accent,{bold:true});
    txt(q,'checker output',8.07,3.3,4.17,.44,21,C.muted);
    txt(q,'200',8.07,4.11,4.17,.82,49,C.warn,{bold:true});
    txt(q,'candidate / required: 401',8.07,5.05,4.3,.4,18,C.muted);
    bottom(q,'The checker faithfully compared against the altered expectations.');
    break;
  case 'multi':
    [['WRITER',.6],['REVIEWER',4.74],['TESTER',8.88]].forEach(([t,x])=>{
      rect(q,x,2.2,3.84,1.04);txt(q,t,x+.22,2.5,3.4,.37,22,C.ink,{bold:true});line(q,x+1.92,3.28,0,.62,C.warn,1.2);
    });
    rect(q,2.08,3.9,9.18,1.08);txt(q,'shared expected.json',2.33,4.24,8.68,.4,23,C.warn,{mono:true});
    txt(q,'All three agents trust the same worker-writable expectations.',.6,5.3,12.12,.55,23,C.ink);
    bottom(q,'Trace every write path into the release decision.');
    break;
  case 'pipeline':
    [['FREEZE','Copy candidate bytes'],['JUDGE','Controller-owned cases'],['GATE','Bind one approval'],['PUBLISH','Store those bytes']].forEach(([t,b],j)=>{
      const x=.6+j*3.09;rect(q,x,2.25,2.84,1.65);txt(q,t,x+.19,2.49,2.46,.38,20,C.accent,{bold:true});txt(q,b,x+.19,3.13,2.46,.56,17,C.ink);
    });
    panel(q,'Approval context',d.code,.6,4.28,12.12,1.37,C.muted,true,17);
    bottom(q,'The untrusted worker never receives the gate key or release authority.');
    break;
  case 'matrix':
    const widths=[6.8,3.82];
    txt(q,'OBSERVATION',.84,2.06,widths[0],.3,12,C.muted,{bold:true});
    txt(q,'RESULT',8.18,2.06,widths[1],.3,12,C.muted,{bold:true});
    d.rows.forEach((r,j)=>{const y=2.55+j*.57;if(j%2===0)rect(q,.6,y-.06,12.12,.54);txt(q,r[0],.84,y,7.1,.41,20);txt(q,r[1],8.18,y,4.28,.41,18,j<2?C.accent:C.warn,{mono:true});});
    bottom(q,d.takeaway);
    break;
  case 'checklist':
    d.rows.forEach((r,j)=>{const y=2.19+j*.89;txt(q,String(j+1).padStart(2,'0'),.6,y,.78,.43,23,C.accent,{mono:true});txt(q,r[0],1.65,y,3.0,.5,24,C.ink,{bold:true});txt(q,r[1],4.89,y,7.83,.67,22,C.ink);line(q,1.65,y+.68,11.07,0,C.line,.6);});
    bottom(q,'After every denial, prove that the legitimate task still completes.');
    break;
  case 'close':
    txt(q,'What can this worker\nmake the rest of\nyour system believe?',.6,2.0,12.1,2.77,42,C.ink,{bold:true});
    txt(q,'Keep the release decision outside its write authority.',.6,5.35,12,.6,25,C.accent,{bold:true});
    txt(q,'github.com/zozo123/nyc-talk',.6,6.29,11.9,.4,20,C.muted,{mono:true,link:'https://github.com/zozo123/nyc-talk'});
    break;
  case 'appendix':
    d.blocks.forEach((b,j)=>{const y=2.09+j*1.26;txt(q,b[0],.6,y,3.08,.65,19,C.accent,{bold:true});txt(q,b[1],3.91,y,8.82,1.02,18,C.ink);});
    break;
  case 'sources':
    d.blocks.forEach((b,j)=>{const y=2.11+j*1.13;txt(q,b[0],.6,y,12,.41,20,C.accent,{bold:true});txt(q,b[1],.6,y+.47,12.1,.5,14,C.muted,{link:b[1]});});
    break;
  default:throw new Error('Unknown layout '+d.layout);
  }
  const sources=(d.sources||[]).map(x=>x.startsWith('http')?x:'Repository: '+x).join('\n');
  q.s.addNotes(`${d.timing||'Appendix - not in the 15-minute delivery'}\n\n${d.notes}\n\n[Sources]\n${sources}\n[/Sources]`);
  // Native panels deliberately contain their text. Diagnose content boxes independently.
  if(helpers){
    helpers.warnIfSlideElementsOutOfBounds(q.s,pptx);
    helpers.warnIfSlideHasOverlaps(q.s,pptx,{muteContainment:true,ignoreLines:true});
  }
  for(const e of q.el) if(e.x<0||e.y<0||e.x+e.w>W+.005||e.y+e.h>H+.005) throw Error('Out of bounds: '+d.heading);
}
data.slides.forEach(build);
function escapeTex(s){return s.replace(/[\\{}#$%&_~^]/g,m=>({'\\':'\\textbackslash{}','{':'\\{','}':'\\}','#':'\\#','$':'\\$','%':'\\%','&':'\\&','_':'\\_','~':'\\textasciitilde{}','^':'\\textasciicircum{}'}[m]));}
function texText(s){return s.split('\n').map(x=>'\\strut '+escapeTex(x)).join('\\\\ ');}
const scale=160/338.6666667;
let tex=String.raw`\documentclass[aspectratio=169,10pt]{beamer}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{tikz}
\usepackage{hyperref}
\hyphenpenalty=10000
\exhyphenpenalty=10000
\setbeamertemplate{navigation symbols}{}
\setbeamertemplate{footline}{}
\setbeamersize{text margin left=0pt,text margin right=0pt}
\definecolor{pagebg}{HTML}{111518}
\setbeamercolor{background canvas}{bg=pagebg}
\hypersetup{pdftitle={Your Agent Escaped Without Escaping the Sandbox},pdfauthor={Yossi Eliaz},colorlinks=false}
\begin{document}
`;
scenes.forEach((els,i)=>{
 tex+='\\begin{frame}[plain]\n\\begin{tikzpicture}[remember picture,overlay,x=1.2cm,y=-1.2cm]\n\\begin{scope}[shift={(current page.north west)}]\n';
 els.forEach(e=>{
  const col='{rgb,255:red,'+parseInt(e.color.slice(0,2),16)+';green,'+parseInt(e.color.slice(2,4),16)+';blue,'+parseInt(e.color.slice(4,6),16)+'}';
  if(e.kind==='rect')tex+=`\\fill[fill=${col}] (${e.x},${e.y}) rectangle (${e.x+e.w},${e.y+e.h});\n`;
  if(e.kind==='line')tex+=`\\draw[draw=${col},line width=${e.width*scale}pt] (${e.x},${e.y}) -- (${e.x+e.w},${e.y+e.h});\n`;
  if(e.kind==='text'){
   const font=e.mono?'\\ttfamily':'\\sffamily';const size=e.size*scale;
   let content=texText(e.text);
   if(e.link)content=`\\href{${e.link.replace(/%/g,'\\%')}}{${content}}`;
   tex+=`\\node[anchor=north west,inner sep=0pt,outer sep=0pt,text=${col},text width=${e.w*1.2}cm,align=${e.align==='right'?'right':'left'},font=${font}${e.bold?'\\bfseries':''}\\fontsize{${size.toFixed(3)}}{${(size*1.17).toFixed(3)}}\\selectfont] at (${e.x},${e.y}) {${content}};\n`;
  }
 });
 tex+='\\end{scope}\n\\end{tikzpicture}\n\\note{'+escapeTex(data.slides[i].notes)+'}\n\\end{frame}\n';
});
tex+='\\end{document}\n';
fs.writeFileSync(path.join(ROOT,'slides/talk.tex'),tex);
const main=data.slides.filter(s=>s.timing);
let script=`# ${data.title}\n\nYossi Eliaz, PhD | AI Agent Security Summit | New York | October 21, 2026\n\n12 main slides. Target 14 minutes plus one minute of margin. Timing is a delivery plan, not a measured rehearsal.\n\n`;
main.forEach((d,i)=>{script+=`## ${i+1}. ${d.heading} | ${d.timing}\n\n${d.notes}\n\n`;});
fs.writeFileSync(path.join(ROOT,'TALK.md'),script);
fs.writeFileSync(path.join(ROOT,'SPEAKER_NOTES.md'),'# Stage cues\n\n'+main.map((d,i)=>`## ${i+1}. ${d.heading} | ${d.timing}\n\n${d.cue}\n`).join('\n'));
fs.mkdirSync(path.join(ROOT,'build'),{recursive:true});
fs.writeFileSync(path.join(ROOT,'build/deck-layout.json'),JSON.stringify(scenes,null,2));
pptx.writeFile({fileName:path.join(ROOT,'build/talk.pptx')}).then(()=>{
 const words=main.reduce((n,d)=>n+d.notes.split(/\s+/).length,0);
 console.log(`${data.slides.length} slides; ${main.length} main; ${words} spoken-script words. Beamer and PPTX generated.`);
}).catch(e=>{console.error(e);process.exit(1);});
