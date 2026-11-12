// Practice helpers: random mixed practice, bookmarks and teacher bulk import.
const E=require('./engine'),crypto=require('crypto'),lessons=require('./lessons.json');
const fail=(m,s=400)=>{const e=Error(m);e.status=s;throw e};
function pool(all){const allowed=all.filter(e=>e.open&&e.showAnswers),map=new Map();for(const e of allowed)for(const type of['mcq','tf'])for(const q of e[type]){const k=type+':'+q.id;if(!map.has(k))map.set(k,{type,q,origins:new Set()});map.get(k).origins.add(e.id)}return map}
function pick(rows,n){return E.shuffle(rows).slice(0,n)}
function assemble(id,title,chosen,extra={}){const mcq=[],tf=[],origins=new Set(),questionOrigins={};for(const c of chosen){(c.type==='mcq'?mcq:tf).push(c.q);questionOrigins[c.type+':'+c.q.id]=[...c.origins];c.origins.forEach(o=>origins.add(o))}return{id,title,kind:'practice',topics:[...new Set([...mcq,...tf].map(q=>q.topic))].sort(),mcq,tf,origins:[...origins],questionOrigins,seconds:40,...extra}}
function mix(all,data={}){
 const topics=Array.isArray(data.topics)?data.topics.filter(t=>/^[A-G]$/.test(t)):[],ls=Array.isArray(data.lessons)?data.lessons.map(Number).filter(n=>Number.isInteger(n)&&n>=1&&n<=28):[];
 const count=Math.min(40,Math.max(5,Number.isInteger(+data.count)?+data.count:20)),tfCount=Math.min(4,Math.max(0,Number.isInteger(+data.tf)?+data.tf:2));
 const level=['NB','TH','VD'].includes(data.level)?data.level:null;
 const rows=[...pool(all).values()].filter(c=>c.q.lesson<=28&&(!topics.length||topics.includes(c.q.topic))&&(!ls.length||ls.includes(c.q.lesson)));
 const mc=rows.filter(c=>c.type==='mcq'&&(!level||c.q.level===level)),tf=rows.filter(c=>c.type==='tf');
 if(mc.length<5)fail('Phạm vi đã chọn chưa đủ câu hỏi đang mở và cho xem đáp án.');
 const chosen=[...pick(mc,count),...pick(tf,tfCount)];
 const label=ls.length?'Bài '+ls.slice(0,8).join(', ')+(ls.length>8?'…':''):topics.length?'Chủ đề '+topics.join(', '):'Toàn bộ chương trình';
 return assemble('practice-mix','Luyện ngẫu nhiên · '+label,chosen,{scopeTopics:topics,scopeLessons:ls});
}
function fromBookmarks(all,items){const p=pool(all),chosen=[];for(const it of items){const c=p.get(it.type+':'+it.id);if(c&&chosen.filter(x=>x.type===c.type).length<(c.type==='mcq'?30:4))chosen.push(c)}if(!chosen.length)fail('Chưa có câu đánh dấu nào thuộc đề đang mở và cho xem đáp án.');return assemble('practice-bookmarks','Luyện câu đã đánh dấu',chosen)}
function canonical(all){const m=new Map();for(const e of all||E.exams)for(const type of['mcq','tf'])for(const q of e[type])if(!m.has(type+':'+q.id))m.set(type+':'+q.id,q);return m}
function exists(type,id,all){return canonical(all).has(type+':'+id)}
function describe(items,all){const m=canonical(all);return items.map(it=>{const q=m.get(it.type+':'+it.id);return q?{type:it.type,id:it.id,at:it.at,lesson:q.lesson,topic:q.topic,text:String(it.type==='mcq'?q.question:q.scenario).slice(0,220)}:null}).filter(Boolean)}
const TRUE=new Set(['t','true','đ','d','đúng','dung','1']),FALSE=new Set(['f','false','s','sai','0']);
function parseImport(data){
 const title=String(data.title||'').trim(),text=String(data.text||'');if(!title||title.length>120)fail('Tên đề cần 1–120 kí tự.');if(!text.trim()||text.length>150000)fail('Nội dung câu hỏi trống hoặc quá dài.');
 const defLesson=Number(data.lesson)||0,mcq=[],tf=[],warnings=[],lv={N:'NB',T:'TH',V:'VD'};
 const lessonOf=v=>{const n=Number(v||defLesson);return lessons.some(l=>l.id===n)?n:0};
 const lim=(s,n,where)=>{s=String(s||'').trim();if(!s)fail(where+': thiếu nội dung.');if(s.length>n)fail(where+': quá '+n+' kí tự.');return s};
 text.split(/\r?\n/).forEach((raw,i)=>{const line=raw.trim();if(!line||line.startsWith('#'))return;const f=line.split('|').map(x=>x.trim()),w='Dòng '+(i+1);
  if(f[0].toUpperCase()==='TF'){if(f.length<14)fail(w+': câu đúng/sai cần TF|tình huống|Đ/S|nhận định|giải thích ×4.');const lesson=lessonOf(f[14]);const statements=[0,1,2,3].map(k=>{const v=f[2+3*k].toLowerCase();if(!TRUE.has(v)&&!FALSE.has(v))fail(w+': đáp án nhận định phải là Đ/S.');return{label:'abcd'[k],level:k<2?'TH':'VD',text:lim(f[3+3*k],400,w),answer:TRUE.has(v),explanation:lim(f[4+3*k],400,w)}});tf.push({id:'gv-t'+(tf.length+1)+'-'+crypto.randomBytes(3).toString('hex'),type:'tf',topic:lessons.find(l=>l.id===lesson)?.topic||'GV',lesson,scenario:lim(f[1],1200,w),statements,review:lesson?`Bài ${lesson} – ${lessons.find(l=>l.id===lesson).title}`:'Đề giáo viên'});return}
  const L=f[0].toUpperCase();if(!lv[L]||f.length<7)fail(w+': câu trắc nghiệm cần N|câu hỏi|đáp án đúng|sai 1|sai 2|sai 3|giải thích (N/T/V).');
  const correct=lim(f[2],300,w),wrong=[f[3],f[4],f[5]].map(x=>lim(x,300,w)),opts=[correct,...wrong];if(new Set(opts.map(o=>o.toLowerCase())).size<4)fail(w+': các phương án bị trùng.');
  const lens=opts.map(o=>o.length);if(lens[0]>Math.max(...lens.slice(1))+12||Math.max(...lens)>1.8*Math.min(...lens)&&Math.max(...lens)-Math.min(...lens)>12)warnings.push(w+': độ dài phương án chênh lệch, dễ đoán.');
  const order=E.shuffle([0,1,2,3]),lesson=lessonOf(f[7]);mcq.push({id:'gv-m'+(mcq.length+1)+'-'+crypto.randomBytes(3).toString('hex'),type:'mcq',topic:lessons.find(l=>l.id===lesson)?.topic||'GV',lesson,level:lv[L],question:lim(f[1],600,w),options:order.map(k=>opts[k]),answer:order.indexOf(0),explanation:lim(f[6],600,w),review:lesson?`Bài ${lesson} – ${lessons.find(l=>l.id===lesson).title}`:'Đề giáo viên'})});
 if(!mcq.length&&!tf.length)fail('Chưa có câu hỏi hợp lệ.');if(mcq.length>100||tf.length>20)fail('Tối đa 100 câu trắc nghiệm và 20 câu đúng/sai mỗi đề.');
 return{title,description:String(data.description||'').slice(0,300),mcq,tf,topics:[...new Set([...mcq,...tf].map(q=>q.topic))].sort(),warnings:warnings.slice(0,50)};
}
module.exports={mix,fromBookmarks,describe,exists,parseImport};
