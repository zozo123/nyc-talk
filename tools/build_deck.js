#!/usr/bin/env node
// Editable PowerPoint counterpart to the canonical Beamer deck.
// Text, tables and panels are native elements; no screenshots of slides.
// All text and speaker notes come from slides/content.json.
const fs = require('fs');
const path = require('path');
const pptxgen = require('pptxgenjs');
const root = path.resolve(__dirname, '..');
const content = JSON.parse(fs.readFileSync(path.join(root, 'slides/content.json'), 'utf8'));
let helpers;
try { helpers = require('/home/oai/skills/slides/pptxgenjs_helpers'); }
catch (_) { helpers = null; } // Authoring-environment QA helper, not a runtime dependency.
const pptx = new pptxgen();
pptx.layout = 'LAYOUT_WIDE';
pptx.author = 'Yossi Eliaz';
pptx.subject = 'AI Agent Security Summit, New York, October 21, 2026';
pptx.title = content.title;
pptx.company = 'Incredibuild';
pptx.lang = 'en-US';
pptx.theme = {headFontFace:'Aptos Display',bodyFontFace:'Aptos',lang:'en-US'};
const C = {void:'101214',panel:'1A1F23',paper:'F0F0E8',acid:'C7FF48',alarm:'FF756B',muted:'A7ADB3'};
const u = 5/6; // 16 x 9 design grid -> native 13 1/3 x 7.5 inches.
function text(s,x,y,w,h,value,size=11,color='paper',bold=false,extra={}) {
  s.addText(value, {x:x*u,y:y*u,w:w*u,h:h*u,fontFace:'Aptos',fontSize:size*2.0,
    color:C[color],bold,margin:0,breakLine:false,vertAnchor:'top',valign:'top',
    paraSpaceAfterPt:0,transparency:0,...extra});
}
function rect(s,x,y,w,h,color='panel'){
  // Deliberate background panel, with its content fully contained.
  s.addShape(pptx.ShapeType.rect,{x:x*u,y:y*u,w:w*u,h:h*u,line:{color:C[color],transparency:100},fill:{color:C[color]}});
}
for(let idx=0;idx<content.slides.length;idx++){
  const v=content.slides[idx], i=idx+1, s=pptx.addSlide(); s.background={color:C.void};
  text(s,1,.48,14,.32,v.eyebrow,8.5,'acid',true,{charSpacing:1.2});
  if(v.kind==='title'){
    text(s,1,1.85,14,3.7,v.title,30,'paper',true,{fontFace:'Aptos Display',breakLine:false});
    text(s,1,6.0,14,.55,v.subtitle,16,'paper',true);
    text(s,1,6.8,14,.45,v.affiliation,10,'muted');
    text(s,1,7.55,14,.45,v.date,11,'acid');
  } else {
    text(s,1,1.12,14,1.5,v.title,22,'paper',true,{fontFace:'Aptos Display'});
    if(v.kind==='reveal'){
      [[1,v.left_label,v.left_value,'acid'],[8.2,v.right_label,v.right_value,'alarm']].forEach(([x,label,value,col])=>{
        rect(s,x,3.4,6.8,2.75);text(s,x+.35,3.73,6.1,.35,label,9,'muted',true);
        text(s,x+.35,4.25,6.1,1.5,value,38,col,true);
      });
    } else if(['case','checker'].includes(v.kind)){
      rect(s,1,3,9.3,3.85);
      text(s,1.28,3.27,8.75,3.34,v.code,9,'paper',false,{fontFace:'DejaVu Sans Mono',lineSpacingMultiple:1.05});
      [[3.14,'outcome','alarm'],[5.23,'control','acid']].forEach(([y,key,col])=>{
        let [label,value]=v[key].split('\n');
        if(value.length>19)value=value.replace(' -> ',' ->\n');
        text(s,10.8,y,4.15,.55,label,9.3,'muted',true);
        text(s,10.8,y+.68,4.15,1.22,value,value.length<19?15:12,col,true);
      });
    } else if(['boundary','close','history'].includes(v.kind)){
      const start=v.kind==='history'?3.25:3.04, rh=v.kind==='history'?1.08:.87;
      v.rows.forEach(([label,value],j)=>{
        const y=start+j*rh;rect(s,1,y,.05,rh-.15,'acid');
        text(s,1.3,y+.02,3.6,rh-.16,label,10,'acid',true);
        text(s,5.0,y+.02,9.9,rh-.16,value,11.2);
      });
      if(v.trust)text(s,1,6.95,14,.6,v.trust,9.3,'muted');
      if(v.kind==='close')text(s,1,7.95,14,.4,v.url,10,'acid',true,{hyperlink:{url:'https://'+v.url}});
    } else if(v.kind==='pipeline'){
      v.steps.forEach(([num,label,description],j)=>{
        const x=1+j*3.57;rect(s,x,3.25,3.3,2.12);text(s,x+.23,3.5,2.85,.32,num,9,'acid',true);
        text(s,x+.23,3.98,2.85,.5,label,15,'paper',true);text(s,x+.23,4.65,2.85,.6,description,8.8,'muted');
      });
      text(s,1,6.0,14,.72,v.equation,18,'acid',true);
    } else if(v.kind==='matrix'){
      const xs=[1,4,7.6,11.05], ws=[3,3.6,3.45,3.95];rect(s,1,3.06,14,.58);
      v.headers.forEach((h,j)=>text(s,xs[j]+.12,3.19,ws[j]-.2,.35,h,8.4,'acid',true));
      v.rows.forEach((row,j)=>{
        const y=3.75+j*.68;if(j%2===0)rect(s,1,y-.04,14,.68);
        row.forEach((value,k)=>text(s,xs[k]+.12,y+.10,ws[k]-.23,.47,value,9.1));
      });
    } else if(v.kind==='code'){
      rect(s,1,3,14,3.85);text(s,1.3,3.25,13.4,3.35,v.code,9,'paper',false,{fontFace:'DejaVu Sans Mono'});
    } else if(v.kind==='sources'){
      v.rows.forEach(([label,url],j)=>{const y=3.04+j*.9;
        text(s,1,y,14,.36,label,10.6,'paper',true);
        text(s,1,y+.39,14,.34,url,7.5,'acid',false,{hyperlink:{url}});
      });
    }
    if(v.bottom)text(s,1,v.kind==='close'?7.0:7.23,14,.7,v.bottom,['matrix','sources'].includes(v.kind)?10.4:11,'paper',true);
    if(v.foot)text(s,1,8.13,13.25,.38,v.foot,6.8,'muted');
  }
  text(s,14.0,8.52,1.0,.25,i<=11?String(i).padStart(2,'0')+'/11':'APP '+String.fromCharCode(65+i-12),7,'muted');
  s.addNotes(`${v.time}. ${v.cue}\n\n${v.notes}\n\n[Sources]\n${v.sources.join('\n')}\n[/Sources]`);
  if(helpers){helpers.warnIfSlideHasOverlaps(s,pptx);helpers.warnIfSlideElementsOutOfBounds(s,pptx);}
}
fs.mkdirSync(path.join(root,'build'),{recursive:true});
pptx.writeFile({fileName:path.join(root,'build/talk.pptx')});
