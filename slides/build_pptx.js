// Editable PowerPoint companion generated from the same source as the Beamer PDF.
// npm install --prefix slides; node slides/build_pptx.js
const fs = require('fs');
const path = require('path');
const pptxgen = require('pptxgenjs');
const root = path.resolve(__dirname, '..');
const deck = JSON.parse(fs.readFileSync(path.join(__dirname, 'deck.json')));
const pptx = new pptxgen();
pptx.layout = 'LAYOUT_WIDE';
pptx.author = deck.author;
pptx.subject = 'Evidence-backed agent security; October 21, 2026';
pptx.title = deck.title;
pptx.company = 'Incredibuild';
pptx.lang = 'en-US';
pptx.theme = { headFontFace: 'Aptos Display', bodyFontFace: 'Aptos', lang: 'en-US' };
// Use the authoring environment's layout diagnostics when available. They are
// optional for a portable build and are not copied into the repository.
let helpers = null;
const hp = process.env.SLIDE_HELPERS_PATH || '/home/oai/skills/slides/pptxgenjs_helpers';
if (fs.existsSync(hp)) helpers = require(hp);
const C = { bg: '101214', panel: '1B2026', fg: 'F0F0E8', accent: 'C7FF48', dim: 'A7ADB3', rule: '35404B' };
const W = 40/3, H = 7.5;
function text(s, str, x, y, w, h, size=24, opts={}) {
  const config = {x,y,w,h,fontFace:'Aptos',fontSize:size,color:C.fg,margin:0,
    breakLine:false,vertAnchor:'top',paraSpaceAfterPt:0,...opts};
  // autoFontSize is diagnostic/fit assistance, while the deliberate minimum
  // keeps small body text out of the presentation.
  if (helpers && opts.fitBox) Object.assign(config, helpers.autoFontSize(str, config.fontFace,
    {x,y,w,h,fontSize:size,minFontSize:size-1,maxFontSize:size,mode:'shrink'}));
  delete config.fitBox;
  s.addText(str, config);
}
function box(s,x,y,w,h) {s.addShape(pptx.ShapeType.rect,{x,y,w,h,fill:{color:C.panel},line:{color:C.panel}});}
function mono(s,str,x,y,w,h,size=21) {text(s,str,x,y,w,h,size,{fontFace:'DejaVu Sans Mono',breakLine:false});}
function footer(s,d,n) {
  if(d.conclusion) {
    s.addShape(pptx.ShapeType.line,{x:.58,y:5.98,w:.66,h:0,line:{color:C.accent,width:2.2}});
    text(s,d.conclusion,.58,6.13,12.05,.58,23,{fitBox:true});
  }
  if(d.evidence) text(s,d.evidence,.58,6.84,11.85,.28,11.2,{color:C.dim});
  text(s,'YOSSI ELIAZ / AI AGENT SECURITY SUMMIT / OCT 21, 2026',.58,7.21,10.9,.17,9.2,{color:C.dim});
  text(s,String(n),12.1,7.17,.6,.24,11,{align:'right',color:C.dim});
}
for (const [i,d] of deck.slides.entries()) {
  const s = pptx.addSlide(); s.background = {color:C.bg};
  if(d.kind==='title') {
    text(s,d.kicker,.60,.48,12.1,.30,13.2,{color:C.accent,fontFace:'DejaVu Sans Mono'});
    text(s,d.title,.60,1.35,12.0,2.93,46,{bold:true,fontFace:'Aptos Display',breakLine:false});
    text(s,d.subtitle,.64,4.75,12.0,.80,22);
  } else if(d.kind==='close') {
    text(s,d.kicker,.60,.50,12.0,.38,13.2,{color:C.accent});
    text(s,d.title,.60,1.42,12.0,2.0,35,{bold:true});
    text(s,d.subtitle,.60,3.85,12.0,.6,28,{fontFace:'DejaVu Sans Mono',color:C.accent});
    mono(s,d.code,.60,4.66,12.0,1.08,19);
  } else {
    text(s,d.kicker||'TECHNICAL APPENDIX',.58,.34,12.1,.27,12.8,{fontFace:'DejaVu Sans Mono',color:C.accent});
    text(s,d.title,.58,.85,12.1,.92,30,{bold:true,fitBox:true});
    if(['split','boundary'].includes(d.kind)) {
      d.panels.forEach((p,j)=>{
        const x=.58+j*6.21;
        box(s,x,2.01,5.96,3.57);
        text(s,p.label,x+.24,2.27,5.47,.53,14.6,{bold:true,color:C.accent});
        mono(s,p.code,x+.24,3.04,5.47,2.23,18.8);
      });
    } else if(d.kind==='table') {
      const widths=[3.00,4.20,4.77];
      let x=.62;
      d.columns.forEach((h,j)=>{text(s,h,x,2.10,widths[j]-.22,.58,18.6,{color:C.accent,bold:true});x+=widths[j];});
      const rh = d.rows.length>4 ? .53 : .67;
      d.rows.forEach((row,r)=>{
        const y=2.83+r*rh; let x=.62;
        s.addShape(pptx.ShapeType.line,{x,y:y-.07,w:11.94,h:0,line:{color:C.rule,width:.5}});
        row.forEach((cell,c)=>{text(s,cell,x,y,widths[c]-.25,rh-.06,18.5,{fitBox:true}); x+=widths[c];});
      });
    } else if(d.kind==='pipeline') {
      d.steps.forEach((st,j)=>{
        const x=.58+j*2.49;
        box(s,x,2.26,2.25,.76);
        text(s,st,x,2.46,2.25,.32,18.5,{bold:true,color:C.accent,align:'center'});
        text(s,d.descriptions[j],x,3.30,2.25,.70,17,{color:C.dim,align:'center'});
        if(j<4) s.addShape(pptx.ShapeType.chevron,{x:x+2.30,y:2.51,w:.14,h:.24,line:{color:C.accent},fill:{color:C.accent}});
      });
      mono(s,d.code,.64,4.55,12.0,.9,22);
    } else if(d.kind==='code') {
      box(s,.58,2.07,12.1,3.50);
      mono(s,d.code,.86,2.53,11.55,2.55,20);
    } else if(d.kind==='sources') {
      d.items.forEach((item,j)=>{
        const y=1.98+j*.71;
        text(s,item[0],.62,y,12.0,.24,14.2,{color:C.accent,bold:true});
        text(s,item[1],.62,y+.27,12.0,.30,18.0);
      });
    } else throw new Error('Unknown slide kind: '+d.kind);
  }
  footer(s,d,i+1);
  s.addNotes([`${d.time||'Appendix only'}\n${d.cue||''}\n\n${d.notes}\n\n[Sources]\n${d.sources.join('\n')}\n[/Sources]`]);
  if(helpers) {
    helpers.warnIfSlideHasOverlaps(s,pptx);
    helpers.warnIfSlideElementsOutOfBounds(s,pptx);
  }
}
const out=process.argv[2]||path.join(root,'build','nyc-talk.pptx');
fs.mkdirSync(path.dirname(out),{recursive:true});
pptx.writeFile({fileName:out});
