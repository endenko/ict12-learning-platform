import json,pathlib,collections
r=pathlib.Path(__file__).parent
mc=json.loads((r/'lib/mcq.json').read_text());tf=json.loads((r/'lib/tf.json').read_text());less=json.loads((r/'lib/lessons.json').read_text())
# Correct original A lesson/section metadata by content, preserving original question and key.
for q in mc:
 if not q['id'].startswith('a-old'):continue
 k=int(q['id'].split('-')[-1]);n=1 if k in [1,2,3,4,5,6,7,8,9,10,11,13,14] else 2
 q['lesson']=n;q['section']=('1. Khái niệm về AI' if k in [1,2,3,4,5,6,7,13,14] else '2. Một số ứng dụng của AI') if n==1 else ('1. AI và sự phát triển của một số lĩnh vực' if k in [18] else '2. AI và một vài cảnh báo');q['review']=f'Bài {n} – {q["section"]} (trang {less[n-1]["pages"]})'
def pick(pool,counts,topic=None,lesson=None):
 out=[]
 for level,num in counts.items():
  candidates=[q for q in pool if q.get('level')==level and (not topic or q['topic']==topic) and(not lesson or q['lesson']==lesson) and not q['id'].startswith('a-old')]
  # Interleave lessons to balance across topic coverage.
  groups=collections.defaultdict(list)
  for q in candidates:groups[q['lesson']].append(q)
  ordered=[]
  while any(groups.values()):
   for g in groups.values():
    if g:ordered.append(g.pop(0))
  assert len(ordered)>=num,(level,num,topic,lesson,len(ordered));out+=ordered[:num]
 return out

def picktf(topic,num):
 groups=collections.defaultdict(list)
 for q in tf:
  if q['topic']==topic and not q['id'].startswith('a-old'):groups[q['lesson']].append(q)
 out=[]
 while len(out)<num:
  for g in groups.values():
   if g and len(out)<num:out.append(g.pop(0))
 return out

exams=[]
def make(id,title,kind,topics,qs,ts):
 qs=json.loads(json.dumps(qs));ts=json.loads(json.dumps(ts))
 for i,q in enumerate(qs):
  a=q['answer'];right=q['options'].pop(a);q['answer']=i%4;q['options'].insert(i%4,right)
 exams.append(dict(id=id,title=title,kind=kind,topics=topics,mcq=qs,tf=ts,seconds=40,attemptLimit=3,showAnswers=True,open=True,maxViolations=3))
make('topic-A','Chủ đề A · Máy tính và xã hội tri thức','topic',['A'],[q for q in mc if q['id'].startswith('a-old')],[q for q in tf if q['id'].startswith('a-old')])
for t,name in [('B','Mạng máy tính và Internet'),('C','Đạo đức, pháp luật và văn hóa trong môi trường số')]:make('topic-'+t,'Chủ đề '+t+' · '+name,'topic',[t],pick(mc,{'NB':12,'TH':4,'VD':2},t),picktf(t,2))
for x in less:make('lesson-'+str(x['id']),'Bài '+str(x['id'])+' · '+x['title'],'lesson',[x['topic']],pick(mc,{'NB':9,'TH':4,'VD':2},lesson=x['id']),[q for q in tf if q['lesson']==x['id']][:2])
for combo in ['AB','BC','ABC']:
 qs=[];ts=[]
 for i,t in enumerate(combo):
  counts=({'NB':10,'TH':3 if i<2 else 4,'VD':2 if i<2 else 1} if len(combo)==3 else {'NB':15,'TH':5,'VD':2 if i==0 else 3})
  qs+=pick(mc,counts,t)
  ts += picktf(t,3 if len(combo)==3 else (4 if i==0 else 5))
 make('combined-'+combo,'Giữa kỳ · '+' + '.join(combo),'combined',list(combo),qs,ts)
report=[]
for e in exams:
 assert len(set(q['question'] for q in e['mcq']))==len(e['mcq'])
 assert all(collections.Counter(s['level'] for s in q['statements'])=={'TH':2,'VD':2} for q in e['tf'])
 report.append(dict(id=e['id'],mcq=len(e['mcq']),tf=len(e['tf']),levels=dict(collections.Counter(q['level'] for q in e['mcq'])),answers=dict(collections.Counter(q['answer'] for q in e['mcq'])),topics=dict(collections.Counter(q['topic'] for q in e['mcq']))))
ratios=[max(map(len,q['options']))/min(map(len,q['options'])) for q in mc];assert max(ratios)<=1.15,max(ratios)
report={'exams':report,'uniqueMCQ':len(mc),'uniqueTF':len(tf),'mcqMaxOptionLengthRatio':max(ratios),'tfMaxStatementLengthRatio':max(max(len(s['text']) for s in q['statements'])/min(len(s['text']) for s in q['statements']) for q in tf),'source':'Kết nối tri thức – Tin học 12, định hướng ICT, Bài 1–6, trang 5–38. A/B/C là nhãn thuận tiện cho Chủ đề 1/2/3 của sách.'}
(r/'lib/exams.json').write_text(json.dumps(exams,ensure_ascii=False));(r/'content-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2))
