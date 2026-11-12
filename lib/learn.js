'use strict';
// ICT12 v4 – self-study: theory reading progress, flashcards (Leitner spaced repetition), inline checks,
// lesson videos (verified YouTube/Vimeo embeds), teacher materials and "study theory" tasks.
const crypto=require('crypto'),{db,clean}=require('./db'),P=require('./portal'),{sanitizeHtml,safeUrl,textOf}=require('./sanitize'),IDX=require('./theory-index.json'),lessons=require('./lessons.json');
const ACTIONS=new Set(['learnData','learnProgress','videoCheck','learnVideosSave','materialSave','materialDelete','studyTaskSave','studyTaskClose','learnClass','learnStudent']);
const STAFF=new Set(['videoCheck','learnVideosSave','materialSave','materialDelete','studyTaskSave','studyTaskClose','learnClass','learnStudent']);
const DAY=86400000,BOX_DAYS=[0,1,3,7,16,35],GLOBAL='__global__';
const fail=(m,s=400)=>{const e=Error(m);e.status=s;throw e};
const now=()=>Date.now(),iso=()=>new Date().toISOString();
const lessonOk=n=>Number.isInteger(n)&&!!IDX[String(n)];
const title=n=>(lessons.find(l=>l.id===n)||{}).title||'';
const pid=(u,n)=>'lp:'+u+':'+n;
// ---------- videos ----------
function parseVideo(raw){const v=String(raw||'').trim();if(!v||v.length>300)return null;let u;try{u=new URL(/^https?:\/\//i.test(v)?v:'https://'+v)}catch{return null}
 const h=u.hostname.replace(/^www\.|^m\./,'').toLowerCase(),id=/^[A-Za-z0-9_-]{11}$/;
 if(h==='youtu.be'){const x=u.pathname.slice(1).split('/')[0];return id.test(x)?{provider:'youtube',id:x}:null}
 if(['youtube.com','youtube-nocookie.com','music.youtube.com'].includes(h)){const q=u.searchParams.get('v');if(q&&id.test(q))return{provider:'youtube',id:q};const m=u.pathname.match(/^\/(?:embed|shorts|live|v)\/([A-Za-z0-9_-]{11})(?:\/|$)/);return m?{provider:'youtube',id:m[1]}:null}
 if(h==='vimeo.com'||h==='player.vimeo.com'){const m=u.pathname.match(/^\/(?:video\/)?(\d{6,12})(?:\/|$)/);return m?{provider:'vimeo',id:m[1]}:null}
 return null}
async function verifyVideo(v){const page=v.provider==='youtube'?'https://www.youtube.com/watch?v='+v.id:'https://vimeo.com/'+v.id;
 const url=v.provider==='youtube'?'https://www.youtube.com/oembed?format=json&url='+encodeURIComponent(page):'https://vimeo.com/api/oembed.json?url='+encodeURIComponent(page);
 let r;try{r=await fetch(url,{signal:AbortSignal.timeout(8000),headers:{'User-Agent':'ICT12-Learning/1.0'}})}catch{fail('Không kiểm tra được video lúc này. Hãy thử lại.',503)}
 if(r.status!==200)fail(r.status===401||r.status===403?'Video này không cho phép nhúng vào trang khác.':'Không tìm thấy video (có thể đã bị xóa hoặc để riêng tư).');
 const m=await r.json().catch(()=>null);if(!m||!m.title)fail('Không đọc được thông tin video.');
 return{provider:v.provider,id:v.id,title:String(m.title).slice(0,200),author:String(m.author_name||'').slice(0,100),verifiedAt:iso()}}
function videoItem(x){return x&&['youtube','vimeo'].includes(x.provider)&&(x.provider==='youtube'?/^[A-Za-z0-9_-]{11}$/:/^\d{6,12}$/).test(x.id)?{provider:x.provider,id:x.id,title:String(x.title||'').slice(0,200),author:String(x.author||'').slice(0,100),verifiedAt:x.verifiedAt||null}:null}
// ---------- progress ----------
function summary(doc,n,videoCount){const ix=IDX[String(n)],d=doc||{};const read=Math.max(0,Math.min(100,Math.round(d.readPct||0)));
 const cards=d.cards||{},mastered=Object.values(cards).filter(c=>c.box>=3).length,seen=Object.keys(cards).length;
 const checks=d.checks||{},answered=Object.keys(checks).length,correct=Object.values(checks).filter(c=>c.correct).length;
 const watched=(d.videos||[]).length>0;
 const parts=[[read/100,0.4],[mastered/ix.cards,0.2],[correct/ix.checks,0.25]];if(videoCount)parts.push([watched?1:0,0.15]);
 const w=parts.reduce((a,p)=>a+p[1],0),percent=Math.round(100*parts.reduce((a,p)=>a+p[0]*p[1],0)/w);
 const complete=read>=80&&answered>=ix.checks;
 return{lesson:n,read,cardsMastered:mastered,cardsSeen:seen,cardsTotal:ix.cards,checksAnswered:answered,checksCorrect:correct,checksTotal:ix.checks,videoWatched:watched,percent,complete,completedAt:d.completedAt||null,readAt:d.readAt||null,updatedAt:d.updatedAt||null,started:!!doc}}
async function progressDocs(userIds){if(!userIds.length)return[];return(await db('list_in','progress','userId',{values:userIds})).map(clean)}
function taskStatus(t,doc){const done=doc?.completedAt?Date.parse(doc.completedAt):null,due=Date.parse(t.dueAt);if(done)return done<=due?'on_time':'late';return now()>due?'missing':'open'}
function studiedBefore(docs,attempts,all){const byLesson=new Map(docs.map(d=>[d.lesson,d])),exams=new Map(all.map(e=>[e.id,e]));const rows=[];
 for(const a of attempts){const e=exams.get(a.examId),ln=e&&e.kind==='lesson'?+(e.lessonId||e.mcq?.[0]?.lesson||0):0;if(!ln||a.practice)continue;const d=byLesson.get(ln),at=Date.parse(a.startedAt||a.createdAt||0)||0;
  rows.push({attemptId:a.id,lesson:ln,title:e.title,startedAt:a.startedAt||null,score:a.result?.score??null,studied:!!(d&&d.readAt&&Date.parse(d.readAt)<=at)})}
 return rows.sort((a,b)=>String(b.startedAt).localeCompare(String(a.startedAt)))}
async function videoDocs(owners){return(await db('list_in','videos','ownerId',{values:owners})).map(clean)}
async function classOwner(className){if(!className)return null;const all=(await db('list','classes')).map(clean);const c=all.find(c=>c.name===className&&!c.disabled);return c?.ownerId||null}
function videoMap(docs){const m={};for(const d of docs){if(!lessonOk(d.lesson))continue;const k=d.ownerId===GLOBAL?'global':'teacher';(m[d.lesson]||(m[d.lesson]={global:[],teacher:[]}))[k]=(d.items||[]).map(videoItem).filter(Boolean)}return m}
const pubMaterial=m=>({id:m.id,lesson:m.lesson,title:m.title,html:m.html,links:m.links||[],classNames:m.classNames,ownerId:m.ownerId,ownerName:m.ownerName,updatedAt:m.updatedAt||m.createdAt});
const pubTask=t=>({id:t.id,lesson:t.lesson,title:t.title,className:t.className,classId:t.classId,dueAt:t.dueAt,note:t.note||'',createdAt:t.createdAt,disabled:!!t.disabled});
async function handle(ctx,u,action,data,res){
 const send=x=>res.status(200).json(x),staff=u.role==='admin'||u.role==='teacher';
 if(STAFF.has(action)&&!staff)fail('Không có quyền giáo viên.',403);
 if(action==='learnData'){
  if(u.role==='student'){const owner=await classOwner(u.className);
   const [docs,vids,mats,tasks]=await Promise.all([progressDocs([u.id]),videoDocs(owner?[GLOBAL,owner]:[GLOBAL]),owner?db('list_in','materials','ownerId',{values:[owner]}):[],u.className?db('list_in','studytasks','className',{values:[u.className]}):[]]);
   const vm=videoMap(vids),byLesson=new Map(docs.map(d=>[d.lesson,d]));
   const progress=Object.keys(IDX).map(Number).map(n=>({...summary(byLesson.get(n),n,(vm[n]?.global.length||0)+(vm[n]?.teacher.length||0)),cards:byLesson.get(n)?.cards||{},checks:byLesson.get(n)?.checks||{},sections:byLesson.get(n)?.sections||[],videos:byLesson.get(n)?.videos||[]}));
   return send({progress,videos:vm,materials:mats.map(clean).filter(m=>!m.deleted&&(m.classNames||[]).includes(u.className)).map(pubMaterial),
    tasks:tasks.map(clean).filter(t=>!t.disabled&&Date.parse(t.opensAt||t.createdAt)<=now()).map(t=>({...pubTask(t),status:taskStatus(t,byLesson.get(t.lesson))})).sort((a,b)=>a.dueAt.localeCompare(b.dueAt)),serverNow:now()})}
  const sc=await P.scope(u);const owners=u.role==='admin'?null:[GLOBAL,u.id];
  const [vids,mats,tasks]=await Promise.all([owners?videoDocs(owners):db('list','videos').then(x=>x.map(clean)),u.role==='admin'?db('list','materials'):db('list_in','materials','ownerId',{values:[u.id]}),u.role==='admin'?db('list','studytasks'):(sc.names.size?db('list_in','studytasks','className',{values:[...sc.names]}):[])]);
  const vm={};for(const d of vids){if(!lessonOk(d.lesson))continue;const e=vm[d.lesson]||(vm[d.lesson]={global:[],mine:[],others:0});if(d.ownerId===GLOBAL)e.global=(d.items||[]).map(videoItem).filter(Boolean);else if(d.ownerId===u.id)e.mine=(d.items||[]).map(videoItem).filter(Boolean);else e.others+=(d.items||[]).length}
  return send({videos:vm,materials:mats.map(clean).filter(m=>!m.deleted&&(u.role==='admin'||m.ownerId===u.id)).map(pubMaterial),tasks:tasks.map(clean).filter(t=>!t.disabled&&(u.role==='admin'||t.ownerId===u.id)).map(pubTask),classes:sc.classes.filter(c=>!c.disabled).map(c=>({id:c.id,name:c.name,ownerId:c.ownerId||null}))})}
 if(action==='learnProgress'){if(u.role!=='student')fail('Chỉ học sinh mới lưu tiến độ học.',403);await ctx.throttle(res,'learn:'+u.id,120,60000);
  const n=+data.lesson;if(!lessonOk(n))fail('Bài học không hợp lệ.');const ix=IDX[String(n)],id=pid(u.id,n);
  for(let attempt=0;attempt<3;attempt++){const cur=await db('get','progress',id);const d=cur?clean(cur):{id,userId:u.id,lesson:n,readPct:0,sections:[],videos:[],cards:{},checks:{},firstAt:iso()};let result={};
   if(data.readPct!=null){const r=Math.max(0,Math.min(100,Math.round(+data.readPct||0)));if(r>d.readPct)d.readPct=r;if(d.readPct>=50&&!d.readAt)d.readAt=iso()}
   if(Array.isArray(data.sections))for(const s of data.sections.slice(0,20)){const k=+String(s).replace(/^s/,'');if(Number.isInteger(k)&&k>=1&&k<=ix.sections&&!d.sections.includes('s'+k))d.sections.push('s'+k)}
   if(data.video!=null){const v=videoItem({provider:data.video.provider,id:data.video.id});if(!v)fail('Video không hợp lệ.');const key=v.provider+':'+v.id;if(!d.videos.includes(key)&&d.videos.length<40)d.videos.push(key)}
   if(data.card!=null){const k=+data.card.index;if(!Number.isInteger(k)||k<0||k>=ix.cards)fail('Thẻ không hợp lệ.');const c=d.cards[k]||{box:0,seen:0};c.seen++;c.box=data.card.known?Math.min(5,(c.box||0)+1):1;c.due=now()+(data.card.known?BOX_DAYS[c.box]*DAY:10*60000);c.at=iso();d.cards[k]=c;result.card={index:k,...c}}
   if(data.check!=null){const k=+data.check.index,choice=+data.check.choice;if(!Number.isInteger(k)||k<0||k>=ix.checks||!Number.isInteger(choice)||choice<0||choice>3)fail('Câu hỏi không hợp lệ.');const correct=ix.answers[k]===choice;const prev=d.checks[k];d.checks[k]={correct:prev?.correct&&!correct?prev.correct:correct,first:prev?prev.first:correct,tries:(prev?.tries||0)+1,at:iso()};result.check={index:k,correct,answer:ix.answers[k]}}
   d.updatedAt=iso();const s=summary(d,n,1);if(s.complete&&!d.completedAt)d.completedAt=iso();
   try{if(cur)await db('put','progress',id,d,cur._version);else await db('put','progress',id,d);return send({ok:true,...result,progress:{...summary(d,n,+data.videoCount||0),cards:d.cards,checks:d.checks,sections:d.sections,videos:d.videos}})}catch(e){if(!e.conflict)throw e}}
  fail('Dữ liệu vừa được cập nhật, hãy thử lại.',409)}
 if(action==='videoCheck'){await ctx.throttle(res,'video:'+u.id,30,60000);const v=parseVideo(data.url);if(!v)fail('Chỉ hỗ trợ đường link YouTube hoặc Vimeo hợp lệ.');return send({video:await verifyVideo(v)})}
 if(action==='learnVideosSave'){const n=+data.lesson;if(!lessonOk(n))fail('Bài học không hợp lệ.');const global=data.scope==='global';if(global&&u.role!=='admin')fail('Chỉ quản trị viên sửa danh sách video chung.',403);
  if(!Array.isArray(data.items)||data.items.length>8)fail('Mỗi bài tối đa 8 video.');await ctx.throttle(res,'video:'+u.id,30,60000);
  const id=global?'g:'+n:'t:'+u.id+':'+n,cur=await db('get','videos',id),prev=new Map(((cur&&cur.items)||[]).map(x=>[x.provider+':'+x.id,x])),items=[],seen=new Set();
  for(const raw of data.items){const v=videoItem(raw)||parseVideo(raw?.url);if(!v)fail('Có video không hợp lệ.');const key=v.provider+':'+v.id;if(seen.has(key))continue;seen.add(key);items.push(prev.get(key)||await verifyVideo(v))}
  const doc={...(cur?clean(cur):{}),id,lesson:n,ownerId:global?GLOBAL:u.id,items,updatedAt:iso(),updatedBy:u.id};
  if(global)await db('put','videos',id,doc,cur?cur._version:null);else await P.put(u,'videos',{...doc,_version:cur?cur._version:undefined});
  await P.log(u,'Cập nhật video','Bài '+n+' ('+items.length+')');return send({ok:true,items})}
 const sc=await P.scope(u);
 if(action==='materialSave'){const n=+data.lesson;if(!lessonOk(n))fail('Bài học không hợp lệ.');const ids=Array.isArray(data.classIds)?[...new Set(data.classIds.map(String))].slice(0,30):[];if(!ids.length)fail('Chọn ít nhất một lớp.');
  const classNames=ids.map(id=>{const c=sc.classes.find(c=>c.id===id&&!c.disabled);if(!c)fail('Không tìm thấy lớp của bạn.',404);return c.name});
  const t=String(data.title||'').replace(/\s+/g,' ').trim();if(!t||t.length>150)fail('Tiêu đề cần 1–150 kí tự.');const html=sanitizeHtml(data.html||'',20000);
  const links=(Array.isArray(data.links)?data.links:[]).slice(0,10).map(l=>{const url=safeUrl(l?.url);if(!url)fail('Đường link phải bắt đầu bằng http:// hoặc https://');return{title:String(l.title||url).replace(/\s+/g,' ').trim().slice(0,150)||url,url}});
  if(!textOf(html)&&!links.length)fail('Hãy nhập nội dung hoặc đường link.');
  let cur=null;if(data.id){cur=await db('get','materials',String(data.id));if(!cur||cur.deleted||(u.role!=='admin'&&cur.ownerId!==u.id))fail('Không tìm thấy tài liệu.',404)}
  const doc={...(cur?clean(cur):{id:crypto.randomUUID(),createdAt:iso(),ownerId:u.id,ownerName:u.name}),lesson:n,title:t,html,links,classNames,updatedAt:iso()};
  if(u.role==='admin'&&!cur){const owners=new Set(ids.map(id=>sc.classes.find(c=>c.id===id).ownerId||null));if(owners.size!==1||[...owners][0]===null)fail('Quản trị viên chỉ thêm tài liệu cho các lớp của cùng một giáo viên.');doc.ownerId=[...owners][0];doc.ownerName=(sc.teachers.find(x=>x.id===doc.ownerId)||{}).name||'Giáo viên'}
  if(u.role==='admin')await db('put','materials',doc.id,doc,cur?cur._version:null);else await P.put(u,'materials',{...doc,_version:cur?cur._version:undefined});
  await P.log(u,data.id?'Sửa tài liệu':'Thêm tài liệu','Bài '+n+': '+t);return send({ok:true,material:pubMaterial(doc)})}
 if(action==='materialDelete'){const m=await db('get','materials',String(data.id||''));if(!m||m.deleted||(u.role!=='admin'&&m.ownerId!==u.id))fail('Không tìm thấy tài liệu.',404);
  const doc={...m,deleted:true,deletedAt:iso()};if(u.role==='admin')await db('put','materials',m.id,clean(doc),m._version);else await P.put(u,'materials',doc);return send({ok:true})}
 if(action==='studyTaskSave'){const n=+data.lesson;if(!lessonOk(n))fail('Bài học không hợp lệ.');const c=sc.classes.find(x=>x.id===String(data.classId||'')&&!x.disabled);if(!c)fail('Không tìm thấy lớp của bạn.',404);
  const due=Date.parse(data.dueAt),opens=data.opensAt?Date.parse(data.opensAt):now();if(!Number.isFinite(due)||!Number.isFinite(opens)||due<=now()||due<=opens)fail('Hạn hoàn thành phải sau thời điểm hiện tại.');
  const owner=u.role==='admin'?(c.ownerId||null):u.id;if(!owner)fail('Lớp chưa có giáo viên phụ trách.');
  const t={id:crypto.randomUUID(),ownerId:owner,classId:c.id,className:c.name,lesson:n,title:'Học lý thuyết Bài '+n+': '+title(n),note:String(data.note||'').replace(/\s+/g,' ').trim().slice(0,300),opensAt:new Date(opens).toISOString(),dueAt:new Date(due).toISOString(),createdAt:iso(),createdBy:u.id};
  if(u.role==='admin')await db('put','studytasks',t.id,t);else await P.put(u,'studytasks',t);await P.log(u,'Giao học lý thuyết',t.className+' · Bài '+n);return send({ok:true,task:pubTask(t)})}
 if(action==='studyTaskClose'){const t=await db('get','studytasks',String(data.id||''));if(!t||(u.role!=='admin'&&(t.ownerId!==u.id||!sc.names.has(t.className))))fail('Không tìm thấy nhiệm vụ.',404);
  const doc={...t,disabled:true,closedAt:iso()};if(u.role==='admin')await db('put','studytasks',t.id,clean(doc),t._version);else await P.put(u,'studytasks',doc);return send({ok:true})}
 if(action==='learnStudent'){const s=await db('get','users',String(data.id||''));if(!P.inScope(sc,s))fail('Không tìm thấy học sinh trong lớp của bạn.',404);
  const [docs,attempts,all,tasks]=await Promise.all([progressDocs([s.id]),db('list','attempts',s.id),ctx.settings(),s.className?db('list_in','studytasks','className',{values:[s.className]}):[]]);const by=new Map(docs.map(d=>[d.lesson,d]));
  const lessonsOut=Object.keys(IDX).map(Number).map(n=>summary(by.get(n),n,0));
  return send({learning:{lessons:lessonsOut,totals:totals(lessonsOut),tasks:tasks.map(clean).filter(t=>!t.disabled).map(t=>({...pubTask(t),status:taskStatus(t,by.get(t.lesson))})),beforeExam:studiedBefore(docs,attempts,all).slice(0,30)}})}
 if(action==='learnClass'){await ctx.throttle(res,'heavy:'+u.id,30,60000);const cls=data.classId?[sc.classes.find(c=>c.id===String(data.classId))].filter(Boolean):sc.classes.filter(c=>!c.disabled&&!/^TEST/i.test(c.name));if(data.classId&&!cls.length)fail('Không tìm thấy lớp của bạn.',404);
  const names=new Set(cls.map(c=>c.name)),students=sc.students.filter(s=>names.has(s.className)&&!s.locked);const ids=students.map(s=>s.id);
  const [docs,all,attempts,tasks]=await Promise.all([progressDocs(ids),ctx.settings(),ids.length?db('list_in','attempts','userId',{values:ids}):[],names.size?db('list_in','studytasks','className',{values:[...names]}):[]]);
  const byUser=new Map();for(const d of docs)(byUser.get(d.userId)||byUser.set(d.userId,[]).get(d.userId)).push(d);
  const rows=students.map(s=>{const ds=byUser.get(s.id)||[],by=new Map(ds.map(d=>[d.lesson,d])),ls=Object.keys(IDX).map(Number).map(n=>summary(by.get(n),n,0)),b=studiedBefore(ds,attempts.filter(a=>a.userId===s.id),all);
   return{id:s.id,name:s.name,className:s.className,totals:totals(ls),lessons:ls.map(l=>({lesson:l.lesson,percent:l.percent,complete:l.complete,read:l.read})),lessonExams:b.length,studiedBeforeExam:b.filter(x=>x.studied).length,lastActive:ds.map(d=>d.updatedAt).sort().at(-1)||null}}).sort((a,b)=>b.totals.percent-a.totals.percent||a.name.localeCompare(b.name,'vi'));
  const lessonAgg=Object.keys(IDX).map(Number).map(n=>{const xs=rows.map(r=>r.lessons[n-1]);return{lesson:n,title:title(n),started:xs.filter(x=>x.percent>0).length,complete:xs.filter(x=>x.complete).length,average:xs.length?Math.round(xs.reduce((a,x)=>a+x.percent,0)/xs.length):0}});
  const taskRows=tasks.map(clean).filter(t=>!t.disabled&&(u.role==='admin'||t.ownerId===u.id)).map(t=>{const st=students.filter(s=>s.className===t.className).map(s=>taskStatus(t,(byUser.get(s.id)||[]).find(d=>d.lesson===t.lesson)));return{...pubTask(t),counts:{on_time:st.filter(x=>x==='on_time').length,late:st.filter(x=>x==='late').length,missing:st.filter(x=>x==='missing').length,open:st.filter(x=>x==='open').length,total:st.length}}});
  return send({classes:cls.map(c=>c.name),students:rows,lessons:lessonAgg,tasks:taskRows})}
 fail('Thao tác không hợp lệ.')}
function totals(ls){const started=ls.filter(l=>l.started),complete=ls.filter(l=>l.complete).length;return{started:started.length,complete,percent:Math.round(ls.reduce((a,l)=>a+l.percent,0)/ls.length),cardsMastered:ls.reduce((a,l)=>a+l.cardsMastered,0),cardsTotal:ls.reduce((a,l)=>a+l.cardsTotal,0),checksCorrect:ls.reduce((a,l)=>a+l.checksCorrect,0),checksTotal:ls.reduce((a,l)=>a+l.checksTotal,0),videosWatched:ls.filter(l=>l.videoWatched).length}}
module.exports={ACTIONS,handle,parseVideo,verifyVideo,summary,taskStatus,studiedBefore,videoItem,GLOBAL};
