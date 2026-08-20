const UNIT=window.UNIT_DATA;
const STATE_KEY='samed-unit-state-'+UNIT.id,PROGRESS_KEY='samed-offline-progress-v1';
let state=load(STATE_KEY,{q:0,steps:{},done:{},hints:{}}),pane='';
const $=s=>document.querySelector(s);
function load(k,d){try{return JSON.parse(localStorage.getItem(k))||d}catch(e){return d}}
function save(){localStorage.setItem(STATE_KEY,JSON.stringify(state));metrics()}
function esc(v){return String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function attr(v){return esc(v).replace(/`/g,'&#96;')}
function arabicDigits(v){return String(v).replace(/[٠-٩]/g,d=>'٠١٢٣٤٥٦٧٨٩'.indexOf(d))}
function norm(v){return arabicDigits(v).toLowerCase().replace(/[\sـ_{}()]/g,'').replace(/[−–—]/g,'-').replace(/×/g,'*').replace(/⅔/g,'2/3').replace(/½/g,'1/2')}
function num(v){v=arabicDigits(v).trim().replace(/[−–—]/g,'-').replace(/×10\^?/g,'e').replace(/÷/g,'/').replace(',','.');const f=v.match(/^(-?\d+(?:\.\d+)?)\/(-?\d+(?:\.\d+)?)$/);if(f&&Number(f[2])!==0)return Number(f[1])/Number(f[2]);const n=Number(v);return Number.isFinite(n)?n:null}
function close(a,b,t=.01){return Math.abs(a-b)<=Math.max(t,Math.abs(b)*1e-4)}
function toast(m){const t=$('#toast');t.textContent=m;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2200)}

/* مصغّر معادلات محلي: لا CDN ولا نص LaTeX خام. */
function mathHtml(value){
 let s=esc(value??'');
 s=s.replace(/\\(?:mathbf|mathrm|text)\{([^{}]*)\}/g,'<strong>$1</strong>');
 for(let i=0;i<8;i++){
  const before=s;
  s=s.replace(/\\sqrt\{([^{}]*)\}/g,'<span class="root"><span class="radicand">$1</span></span>');
  s=s.replace(/\\frac\{([^{}]*)\}\{([^{}]*)\}/g,'<span class="frac"><span class="num">$1</span><span class="den">$2</span></span>');
  if(s===before)break;
 }
 s=s.replace(/\\(?:left|right)/g,'').replace(/\\cdot/g,'·').replace(/\\times/g,'×').replace(/\\div/g,'÷').replace(/\\pm/g,'±').replace(/\\infty/g,'∞');
 s=s.replace(/\^\{([^{}]+)\}/g,'<sup>$1</sup>').replace(/\^([A-Za-z0-9+\-])/g,'<sup>$1</sup>');
 s=s.replace(/_\{([^{}]+)\}/g,'<sub>$1</sub>').replace(/_([A-Za-z0-9])/g,'<sub>$1</sub>');
 s=s.replace(/\\[;,!]/g,' ').replace(/\\([A-Za-z]+)/g,'$1');
 return '<span class="math-expr" dir="ltr">'+s+'</span>';
}
function proseHtml(v){
 let s=esc(v??'');
 s=s.replace(/_([A-Za-z0-9])/g,'<sub>$1</sub>').replace(/\^([A-Za-z0-9+\-])/g,'<sup>$1</sup>');
 return '<span class="mixed-text">'+s+'</span>';
}
function equationOrText(v){return /\\(?:frac|sqrt|mathbf|text|times|cdot)|[A-Za-z][_^]/.test(String(v??''))?mathHtml(v):proseHtml(v)}
function workNorm(v){return arabicDigits(v??'').replace(/\s+/g,'').replace(/[−–—]/g,'-').replace(/[×xX·]/g,'*').replace(/÷/g,'/').replace(/[(){}]/g,'').replace(/₂/g,'2').replace(/₁/g,'1')}
function summaryExpression(step){if(step.carry_display)return step.carry_display;if(step.completed_display)return step.completed_display;if(step.result_target!==undefined)return (step.result_label||'')+' '+step.result_target;return ''}
function referencesHtml(q,si,step){
 let refs=step.references||[];
 if(!refs.length&&si>0&&state.done[key(q,si-1)]){const x=summaryExpression(q.steps[si-1]);if(x)refs=[{source:si,label:'من الخطوة السابقة',expression:x}]}
 refs=refs.filter(r=>r.source===undefined||state.done[key(q,Math.max(0,r.source-1))]);
 if(!refs.length)return '';
 return `<section class="needed-box"><div class="needed-head">📌 عبارات نحتاجها في هذه الخطوة</div>${refs.map(r=>`<div class="needed-row"><span class="needed-source">${esc(r.label||'استنتاج سابق')}</span><div class="needed-eq">${mathHtml(r.expression)}</div></div>`).join('')}</section>`
}
function guidedWorkHtml(g,done){if(!g||done)return '';return `<section class="guided-work"><div class="guided-title">✍️ ${esc(g.title||'مرحلة وسيطة')}</div><p>${esc(g.instruction||'')}</p><div class="guided-equation"><span>${mathHtml(g.equation_left||'')}</span><input id="guidedWork" autocomplete="off" placeholder="${attr(g.placeholder||'اكتب التحويل')}"></div></section>`}
function microEquationInput(eq,index){const parts=String(eq||'').split('?');if(parts.length<2)return mathHtml(eq);return `${mathHtml(parts.shift())}<input id="micro-${index}" data-micro-answer="1" inputmode="text" autocomplete="off" placeholder="؟">${mathHtml(parts.join('?'))}`}
function microPracticeHtml(step,done){
 if(done)return '';
 const rows=step.micro||[];if(!rows.length)return '';
 return `<section class="micro-practice"><div class="micro-practice-head">🧩 نبني الحل دون اختصار</div><p>أكمل العلاقات بالترتيب؛ لن تُقبل النتيجة النهائية قبل إكمالها.</p>${rows.map((row,i)=>{const a=Array.isArray(row)?row:[String(row),''];const needs=a[2]!==undefined&&a[2]!==null&&String(a[2])!=='';return `<div class="micro-practice-row" data-micro-row="${i}"><span class="micro-practice-index">${i+1}</span><div><div class="micro-practice-desc">${esc(a[0]||'')}</div>${a[1]?`<div class="micro-practice-eq">${needs?microEquationInput(a[1],i):mathHtml(a[1])}</div>`:''}</div></div>`}).join('')}</section>`
}
function microValueMatches(value,target,caseSensitive){
 const alternatives=String(target).split('|');
 for(const candidate of alternatives){const a=num(value),b=num(candidate);if(a!==null&&b!==null&&close(a,b,.001))return true;let got=workNorm(value),want=workNorm(candidate);if(!caseSensitive){got=got.toLowerCase();want=want.toLowerCase()}if(got===want||got.replace(/\*/g,'')===want.replace(/\*/g,''))return true}
 return false
}
function validateMicroPractice(step){
 const rows=step.micro||[];
 for(let i=0;i<rows.length;i++){const a=rows[i],target=Array.isArray(a)?a[2]:undefined;if(target===undefined||target===null||String(target)==='')continue;const input=document.getElementById('micro-'+i),row=document.querySelector(`[data-micro-row="${i}"]`);if(!input||!String(input.value).trim()){row&&row.classList.add('is-bad');input&&input.focus();toast('أكمل أولًا المرحلة رقم '+(i+1));return false}if(!microValueMatches(input.value,target,!!step.case_sensitive)){row&&row.classList.add('is-bad');input.focus();toast('راجع العلاقة في المرحلة رقم '+(i+1));return false}row&&row.classList.remove('is-bad');row&&row.classList.add('is-ok')}
 return true
}

function key(q,s){return q.id+':'+s}
function qDone(q){return q.steps.every((_,i)=>state.done[key(q,i)])}
function total(){return UNIT.questions.reduce((n,q)=>n+q.steps.length,0)}
function metrics(){let n=Object.keys(state.done).filter(k=>state.done[k]).length,p=Math.round(n*100/total());$('#stepDone').textContent=n+'/'+total();$('#unitPct').textContent=p+'%';$('#xp').textContent=n*10+' XP';const all=load(PROGRESS_KEY,{});all[UNIT.id]={percent:p,done:n,total:total(),at:new Date().toISOString(),version:UNIT.version};localStorage.setItem(PROGRESS_KEY,JSON.stringify(all))}
function currentIndex(q){return Math.max(0,Math.min(state.steps[q.id]||0,q.steps.length-1))}
function unlocked(q,i){return i===0||!!state.done[key(q,i-1)]}
function setStep(q,i){if(!unlocked(q,i)){toast('أكمل الخطوة السابقة أولًا');return}state.steps[q.id]=i;save();render()}
function moveStep(delta){const q=UNIT.questions[state.q],i=currentIndex(q),next=i+delta;if(next<0||next>=q.steps.length)return;if(delta>0&&!state.done[key(q,i)]){toast('تحقق من هذه الخطوة قبل الانتقال');return}setStep(q,next)}

function renderNav(){const box=$('#qnav');box.innerHTML=UNIT.questions.map((q,i)=>`<button class="qbtn ${i===state.q?'active':''} ${qDone(q)?'done':''}" data-i="${i}">${qDone(q)?'✓ ':''}${esc(q.title)}</button>`).join('');box.querySelectorAll('button').forEach(b=>b.onclick=()=>{state.q=+b.dataset.i;save();render()})}
function renderStepStrip(q,si){
 const box=$('#steps');
 box.innerHTML=q.steps.map((s,i)=>{const done=!!state.done[key(q,i)],carry=done?summaryExpression(s):'';return `<button class="step-tile ${done?'done':i===si?'current':''} ${unlocked(q,i)?'':'locked'}" data-si="${i}" ${unlocked(q,i)?'':'disabled'}><span class="step-number">${done?'✓':i+1}</span><span class="step-title">${esc((s.title||'').replace(/^الخطوة\s*\d+\s*[:：-]?\s*/,''))}</span>${carry?`<span class="step-result">${mathHtml(carry)}</span>`:''}</button>`}).join('');
 box.querySelectorAll('.step-tile').forEach(b=>b.onclick=()=>setStep(q,+b.dataset.si));
 requestAnimationFrame(()=>{const cur=box.querySelector('.current');if(cur)cur.scrollIntoView({behavior:'smooth',block:'nearest',inline:'center'})});
 wireHorizontalDrag(box);
}
function wireHorizontalDrag(el){if(el.dataset.dragReady)return;el.dataset.dragReady='1';let down=false,start=0,left=0,moved=false;el.addEventListener('pointerdown',e=>{if(e.pointerType!=='mouse')return;down=true;moved=false;start=e.clientX;left=el.scrollLeft;el.classList.add('dragging');el.setPointerCapture(e.pointerId)});el.addEventListener('pointermove',e=>{if(!down)return;const dx=e.clientX-start;if(Math.abs(dx)>5)moved=true;el.scrollLeft=left-dx});el.addEventListener('pointerup',e=>{down=false;el.classList.remove('dragging');try{el.releasePointerCapture(e.pointerId)}catch(_){}});el.addEventListener('click',e=>{if(moved){e.preventDefault();e.stopPropagation();moved=false}},true)}
function wireCardSwipe(){const card=$('#stepCard');let x0=null,y0=null;card.onpointerdown=e=>{if(e.target.closest('input,button'))return;x0=e.clientX;y0=e.clientY};card.onpointerup=e=>{if(x0===null)return;const dx=e.clientX-x0,dy=e.clientY-y0;x0=y0=null;if(Math.abs(dx)>70&&Math.abs(dx)>Math.abs(dy)*1.25)moveStep(dx<0?1:-1)}}
function microHtml(step){const rows=[...(step.micro||[]),...(step.micro2||[])];return rows.map((x,i)=>{const a=Array.isArray(x)?x:[String(x),''];let eq=a[1]||'';if(a[2]!==undefined&&a[2]!==null&&String(a[2])!=='')eq=eq.replace('?',String(a[2]).split('|')[0]);return `<div class="micro"><b>${i+1}</b><div><strong>${esc(a[0])}</strong>${eq?`<div class="micro-eq">${mathHtml(eq)}</div>`:''}</div></div>`}).join('')}
function solution(step){let result=step.completed_display||'';if(!result&&step.result_target!==undefined)result=(step.result_label||'النتيجة')+' '+step.result_target;const guided=step.guided_work?`<div class="guided-solution"><span>طريقة التحويل الصحيحة</span>${mathHtml(step.guided_work.equation_left+' '+step.guided_work.reveal)}</div>`:'';return `<div class="solution"><b>✅ اكتملت الخطوة</b>${guided}${microHtml(step)}${result?`<div class="result-eq">${equationOrText(result)}</div>`:''}</div>`}
/* ROOT_INTERMEDIATE_V1 */
function formulaInteractive(step,done){
 let out='<div class="formula-scroll"><div class="formula">';
 out+=`<span>${mathHtml(step.prefix||'')}</span>`;
 (step.blanks||[]).forEach((b,i)=>{out+=`<input data-blank="${i}" inputmode="decimal" ${done?'disabled':''} placeholder="${attr(b.label||'?')}"><span>${mathHtml(b.suffix||'')}</span>`});
 out+='</div></div>';
 if(step.has_root){
  out+=`<div class="result-row root-result-row"><b>المرحلة الوسيطة</b><div class="formula"><span>${mathHtml(step.root_prefix||'')}</span><input id="rootResult" inputmode="decimal" ${done?'disabled':''} placeholder="ما تحت الجذر"><span>${mathHtml(step.root_suffix||'')}</span></div></div>`;
 }
 out+=`<div class="result-row"><b>${esc(step.result_label||'الناتج')}</b><input id="result" inputmode="decimal" ${done?'disabled':''} placeholder="القيمة النهائية"></div>`;
 return out
}
function formulaProof(step,done){if(done)return '';return `${microPracticeHtml(step,false)}${guidedWorkHtml(step.guided_work,false)}<div class="answer-label final-label">${esc((step.guided_work?'بعد الاختزال، ':'بعد إكمال العلاقات السابقة، ')+(step.label||'اكتب النتيجة النهائية:'))}</div><div class="formula-scroll"><div class="formula proof-input"><span>${mathHtml(step.prefix||'')}</span><input id="proof" placeholder="${step.guided_work?'النتيجة النهائية':'أكمل هذه الخطوة'}"><span>${mathHtml(step.suffix||'')}</span></div></div><div class="proof-preview">${mathHtml(step.latex_preview||'أكمل العلاقة الرمزية')}</div>`}
function checkStep(q,si,step){
 const k=key(q,si);
 if(step.type&&!validateMicroPractice(step))return;
 if(step.guided_work){
  const w=$('#guidedWork')?.value||'';
  if(!w)return toast('اكتب أولًا الكسر الأول × مقلوب الكسر الثاني');
  const got=workNorm(w),accepted=(step.guided_work.accepted||[]).map(workNorm);
  if(!accepted.includes(got))return toast('راجع المقلوب: اقلب الكسر الثاني فقط ثم اضرب')
 }
 if(step.type){
  const v=$('#proof')?.value||'';
  if(!v)return toast('اكتب النتيجة النهائية أيضًا');
  const target=step.target;
  if(typeof target==='number'){
   const got=num(v);
   if(got===null||!close(got,target,step.tol||.01))return toast('النتيجة النهائية غير صحيحة بعد')
  }else if(!microValueMatches(v,target,!!step.case_sensitive))return toast('راجع الرموز ثم حاول مجددًا')
 }else{
  const ins=[...document.querySelectorAll('[data-blank]')];
  if(ins.some(x=>num(x.value)===null))return toast('أدخل قيم التعويض أولًا');
  for(let i=0;i<ins.length;i++)if(!close(num(ins[i].value),step.blanks[i].target,.001))return toast('إحدى قيم التعويض غير صحيحة');
  if(step.has_root){
   const rv=num($('#rootResult')?.value||'');
   if(rv===null)return toast('أدخل أولًا قيمة المرحلة الواقعة تحت الجذر');
   if(!close(rv,step.root_target,.01))return toast('راجع قيمة المرحلة الواقعة تحت الجذر')
  }
  const r=num($('#result')?.value);
  if(r===null)return toast('أدخل النتيجة النهائية');
  const targets=[step.result_target,step.alt_result_target].filter(x=>x!==undefined);
  if(!targets.some(t=>close(r,t,step.result_tol||.01)))return toast('النتيجة غير صحيحة بعد')
 }
 state.done[k]=true;save();toast('أحسنت — اكتملت الخطوة');render()
}
// PHYSICS_BOOK_FIGURES_V1
function questionFigure(q){if(!q.figure)return '';return `<figure class="question-figure"><img src="${attr(q.figure)}" alt="${attr(q.figure_caption||q.title||'رسم التمرين')}">${q.figure_caption?`<figcaption>${esc(q.figure_caption)}</figcaption>`:''}</figure>`}
function render(){
 const q=UNIT.questions[state.q],si=currentIndex(q),step=q.steps[si],k=key(q,si),done=!!state.done[k];
 renderNav();renderStepStrip(q,si);
 $('#statement').innerHTML=`<small><span class="type-chip ${q.type==='proof'?'proof':'interactive'}">${q.type==='proof'?'إثبات رمزي':'تمرين تفاعلي'}</span></small><h2>${esc(q.title)}</h2><p>${proseHtml(q.text)}</p>${questionFigure(q)}${qDone(q)&&q.conclusion?`<div class="solution">${proseHtml(q.conclusion)}</div>`:''}`;
 $('#stepCard').innerHTML=`<div class="step-head"><small>الخطوة ${si+1} من ${q.steps.length}</small><span class="swipe-note">↔ اسحب الخطوات أفقيًا</span></div><h2>${esc(step.title)}</h2><div class="law-guide-box"><b>القانون / المعطى</b><div>${proseHtml(step.law||'')}</div></div>${step.simple_explain?`<div class="explain-box">${proseHtml(step.simple_explain)}</div>`:''}${referencesHtml(q,si,step)}${step.type?formulaProof(step,done):formulaInteractive(step,done)}<div class="navrow"><button id="hint" class="btn outline">💡 تلميح</button><button id="check" class="btn primary" ${done?'disabled':''}>تحقق</button></div><div id="hintBox">${state.hints[k]&&!done?`<div class="notice">💡 ${proseHtml(step.hint||'راجع القانون.')}</div>`:''}</div>${done?solution(step):''}<div class="navrow"><button id="prev" class="btn outline" ${si===0?'disabled':''}>السابق</button><button id="next" class="btn blue" ${!done||si===q.steps.length-1?'disabled':''}>التالي</button></div>`;
 $('#hint').onclick=()=>{state.hints[k]=true;save();render()};$('#check').onclick=()=>checkStep(q,si,step);$('#prev').onclick=()=>moveStep(-1);$('#next').onclick=()=>moveStep(1);wireCardSwipe();metrics();if(pane)showPane(pane)
}
const formulas=UNIT.formulas||['P = m·v','K = P²/(2m)','I = F·Δt','I = ΔP','F = ΔP/Δt','ΣPᵢ = ΣP𝒇'];
function formulaPaneItem(x){if(Array.isArray(x))return `<div class="law mini-law"><b>${esc(x[0])}</b>${mathHtml(x[1])}</div>`;return `<div class="law mini-law">${mathHtml(x)}</div>`}
function calcHtml(){const keys=['7','8','9','÷','sin(','4','5','6','×','cos(','1','2','3','-','√(','0','.','(',')','+','π','^','⌫','AC','='];return `<h3>حاسبة علمية</h3><div id="display" class="calc-display">0</div><div class="calc-grid">${keys.map(k=>`<button class="${'=+-×÷^'.includes(k)?'op':''} ${k==='='?'equal':''}" data-k="${k}">${k}</button>`).join('')}</div>`}
function showPane(which){pane=which;const p=$('#dockPanel');p.classList.remove('hidden');if(which==='laws')p.innerHTML='<h3>ورقة القوانين</h3>'+formulas.map(formulaPaneItem).join('');if(which==='stmt'){const q=UNIT.questions[state.q];p.innerHTML=`<h3>نص التمرين</h3><p>${proseHtml(q.text)}</p>`}if(which==='calc'){p.innerHTML=calcHtml();wireCalc()}}
document.querySelectorAll('.rail button').forEach(b=>b.onclick=()=>pane===b.dataset.pane?(pane='', $('#dockPanel').classList.add('hidden')):showPane(b.dataset.pane));
function wireCalc(){let e='',disp=$('#display');document.querySelectorAll('.calc-grid button').forEach(b=>b.onclick=()=>{let k=b.dataset.k;if(k==='AC')e='';else if(k==='⌫')e=e.slice(0,-1);else if(k==='='){try{let x=e.replace(/π/g,'Math.PI').replace(/×/g,'*').replace(/÷/g,'/').replace(/\^/g,'**').replace(/√\(/g,'Math.sqrt(').replace(/sin\(/g,'Math.sin(Math.PI/180*').replace(/cos\(/g,'Math.cos(Math.PI/180*');e=String(Math.round(Function('return ('+x+')')()*1e10)/1e10)}catch(_){e='خطأ'}}else e+=k;disp.textContent=e||'0'})}
function net(){const on=navigator.onLine;$('#net').textContent=on?'متصل':'دون إنترنت';$('#net').classList.toggle('offline',!on);$('#mode').textContent=on?'متصل':'أوفلاين'}
addEventListener('online',net);addEventListener('offline',net);net();render();
