/* Native editable PPTX plus a shared geometry model for the Beamer PDF. */
const fs = require('fs');
const path = require('path');
const pptxgen = require('pptxgenjs');
let helpers;
try { helpers = require('/home/oai/skills/slides/pptxgenjs_helpers'); } catch (_) { helpers = null; }
const root = path.resolve(__dirname, '..');
const data = JSON.parse(fs.readFileSync(path.join(__dirname, 'content.json'), 'utf8'));
const pptx = new pptxgen();
pptx.layout = 'LAYOUT_WIDE'; pptx.author = data.author; pptx.subject = 'Reproducible agent authority-boundary experiments';
pptx.title = data.title; pptx.company = 'Incredibuild'; pptx.lang = 'en-US';
pptx.theme = {headFontFace:'Arial',bodyFontFace:'Arial',lang:'en-US'};
const C = {bg:'101214',text:'F0F0E8',accent:'C7FF48',red:'FF756B',muted:'A7ADB3',panel:'1A1F25',border:'3C434B'};
let s, E; const layouts=[];
function text(t,x,y,w,h,size=22,color=C.text,bold=false,mono=false,align='left') {
  const e={kind:'text',text:t,x,y,w,h,size,color,bold,mono,align}; E.push(e);
  s.addText(t,{x,y,w,h,fontFace:mono?'Courier New':'Arial',fontSize:size,color,bold,margin:0,
    breakLine:false,valign:'top',align,paraSpaceAfter:0,fit:'resize',lineSpacingMultiple:1.12});
}
function rect(x,y,w,h,color=C.panel,lineColor=null){
  E.push({kind:'rect',x,y,w,h,color,lineColor});
  s.addShape(pptx.ShapeType.rect,{x,y,w,h,fill:{color},line:{color:lineColor||color,width:lineColor?0.7:0}});
}
function line(x,y,w,color=C.border){E.push({kind:'line',x,y,w,color});s.addShape(pptx.ShapeType.line,{x,y,w,h:0,line:{color,width:0.75}});}
function panel(x,y,w,h,label){rect(x,y,w,h);text(label,x+.22,y+.22,w-.44,.30,12.5,C.accent,true);}
function code(lines,x,y,w,h,size=20,color=C.text){
  const max=Math.max(...lines.map(z=>z.length)); const fit=Math.min(size,(w*72)/(max*.61));
  text(lines.join('\n'),x,y,w,h,Math.max(14,fit),color,false,true);
}
function rowTable(rows,x,y,w,widths,size=19){
  const rh=rows.length>6?.46:.66;
  rows.forEach((row,i)=>{
    rect(x,y+i*rh,w,rh-.035,i===0?'2D363F':i%2?C.panel:'15191D');
    let xx=x;
    row.forEach((v,j)=>{const ww=w*widths[j];text(v,xx+.16,y+i*rh+.09,ww-.29,rh-.14,i===0?13.5:size,i===0?C.accent:C.text,i===0||j===0);xx+=ww;});
  });
}
for(let i=0;i<data.slides.length;i++){
  const d=data.slides[i]; s=pptx.addSlide();s.background={color:C.bg};E=[];
  text(d.kicker,.62,.37,12.05,.32,12,C.accent,true);
  if(d.kind!=='cover'&&d.kind!=='close'){
    const titleSize=d.title.length>68?28:32;
    text(d.title,.62,.91,12.0,1.0,titleSize,C.text,true);
  }
  if(d.kind==='cover'){
    text(d.title,.62,1.50,12.05,2.52,44,C.text,true);
    line(.62,4.55,12.05,C.accent);
    text(d.subtitle,.65,4.97,10.6,1.52,22);
    text('REPRODUCIBLE AUTHORITY-BOUNDARY EXPERIMENTS',.65,6.69,11.9,.27,11.5,C.muted,true);
  } else if(d.kind==='cold'){
    panel(.62,2.06,5.38,3.96,d.leftlabel);
    code(d.left,.9,2.76,4.83,1,20);
    text('The hash stays unchanged.',.9,4.64,4.8,.75,24,C.text,true);
    panel(6.30,2.06,6.41,3.96,d.rightlabel);
    text('PASS',6.59,2.66,2.72,.85,48,C.accent,true,true);
    text('checker result',9.62,2.99,2.72,.42,18,C.muted);
    text('200',6.59,3.84,2.72,.85,48,C.red,true,true);
    text('candidate result',9.62,4.18,2.72,.45,18,C.muted);
    text(d.required,6.6,5.22,5.78,.48,18,C.text);
  } else if(d.kind==='model'){
    panel(.62,2.0,3.75,3.9,d.leftlabel);
    d.left.forEach((t,k)=>text(t,.89,2.8+k*.72,3.1,.5,22));
    panel(8.40,2.0,4.31,3.9,d.rightlabel);
    d.right.forEach((t,k)=>text(t,8.67,2.8+k*.72,3.75,.56,20));
    d.routes.forEach((t,k)=>{const yy=2.30+k*.84;line(4.58,yy+.36,3.58,C.accent);rect(4.90,yy,2.95,.55,C.bg);text(t,4.98,yy+.07,2.79,.4,18,C.text,false,false,'center');});
    text('Commands and data may cross. Authority must be checked.',.7,6.13,11.9,.35,17,C.muted);
  } else if(d.kind==='compare'){
    panel(.62,2.06,6.0,3.92,d.leftlabel);panel(6.86,2.06,5.85,3.92,d.rightlabel);
    code(d.left,.88,2.94,5.5,2.56,21);
    code(d.right,7.12,2.88,5.34,2.65,20);
  } else if(d.kind==='reveal'){
    panel(.62,2.06,6.55,3.92,d.leftlabel);panel(7.40,2.06,5.31,3.92,d.rightlabel);
    code(d.left,.88,2.95,6.04,2.65,19);
    code(d.right,7.66,2.93,4.77,1.3,21);
    text(d.verdict,7.66,4.34,4.77,.9,45,C.accent,true,true);
    text('Independent policy: REJECT',7.67,5.40,4.64,.4,17,C.red,true);
  } else if(d.kind==='flow'){
    text('TRUSTED CONTROLLER / WORKER CANNOT CHANGE THE CRITERIA',.72,2.15,12,.4,13,C.accent,true);
    d.steps.forEach((t,k)=>{const x=.63+k*2.46;rect(x,2.97,2.17,1.25,C.panel,C.border);text(String(k+1).padStart(2,'0'),x+.16,3.12,1,.27,12,C.accent,true,true);text(t,x+.16,3.48,1.91,.68,20,C.text,true);if(k<4)text('>',x+2.19,3.36,.27,.4,18,C.accent,false,true);});
    panel(.63,4.77,12.07,1.25,'RECEIPT BINDS');
    text(d.binding,.90,5.37,11.49,.37,17,C.text,false,true);
  } else if(d.kind==='results'){
    rowTable(d.rows,.62,2.06,12.09,[.49,.21,.30],18);
    text('Fresh receipt -> bad bytes DENIED -> original good bytes PUBLISHED',.77,5.75,11.7,.48,18,C.accent,false,true);
  } else if(d.kind==='agents'){
    d.workers.forEach((t,k)=>{rect(.63+k*2.49,2.27,2.22,.78);text(t,.77+k*2.49,2.51,1.94,.36,18,C.text,true,false,'center');});
    rect(.63,3.46,7.20,1.02,'2D363F');text(d.shared,.9,3.80,6.66,.38,20,C.red,true,false,'center');
    text('Candidates + reviewer reports',.98,5.1,6.5,.4,21,C.muted,false,false,'center');
    text('>',8.15,3.51,.43,.65,32,C.accent,true);
    panel(9.02,2.27,3.68,3.30,'RELEASE AUTHORITY');
    text(d.controller,9.28,3.35,3.15,1.62,22,C.text,true);
  } else if(d.kind==='checks'){
    rowTable(d.rows,.62,2.13,12.09,[.18,.45,.37],18);
  } else if(d.kind==='close'){
    text(d.title,.62,1.58,12.1,2.73,36,C.text,true);
    line(.62,4.92,12.1,C.accent);
    text(d.link,.65,5.42,11.95,.57,28,C.accent,true,true);
    text('Source / recorded evidence / reproduction / limitations',.67,6.14,11.9,.43,18,C.muted);
  } else {
    d.body.forEach((t,k)=>{
      const y=2.15+k*.62;
      text(String(k+1).padStart(2,'0'),.68,y,.49,.35,12,C.accent,true,true);
      text(t,1.24,y-.035,11.16,.53,17.5,C.text,false,d.kind==='appendix'&&d.title.startsWith('Reproduce'));
    });
  }
  if(d.takeaway){line(.62,6.53,12.08);text(d.takeaway,.64,6.72,12.04,.46,18,C.accent,true);}
  const footer=i<data.main_slides?'YOSSI ELIAZ / OCT 21, 2026':'APPENDIX / NOT IN THE 14-MINUTE DELIVERY';
  text(footer,.64,7.24,10,.18,8.5,C.muted);
  text(i>=data.main_slides?`A${i-data.main_slides+1} / A${data.slides.length-data.main_slides}`:`${String(i+1).padStart(2,'0')} / ${String(data.main_slides).padStart(2,'0')}`,11.8,7.20,.9,.23,10,C.muted,false,true,'right');
  s.addNotes(`${d.time}\n\n${d.notes}\n\n${d.refs?'Evidence: '+d.refs+'\n\n':''}[Sources]\n${d.sources.join('\n')}\n[/Sources]`);
  if(helpers){helpers.warnIfSlideHasOverlaps(s,pptx);helpers.warnIfSlideElementsOutOfBounds(s,pptx);}
  layouts.push({slide:i+1,...d,elements:E});
}
fs.mkdirSync(path.join(root,'build'),{recursive:true});
fs.writeFileSync(path.join(root,'build/layout.json'),JSON.stringify(layouts,null,2)+'\n');
pptx.writeFile({fileName:path.join(root,'build/talk.pptx')});
