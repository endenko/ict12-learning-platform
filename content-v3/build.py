import json,random,sys,glob,itertools,copy
from collections import Counter
from parse import parse_file
ROOT='/workspace/ict12-platform/'
E=json.load(open(ROOT+'lib/exams.json'))
BASE=[e for e in E if not e.get('generated')]
bankM=json.load(open(ROOT+'content-v3/mcq.base.json'));bankT=json.load(open(ROOT+'content-v3/tf.base.json'))
LESS={l['id']:l for l in json.load(open(ROOT+'lib/lessons.json'))}
rng=random.Random(20261111)
NEW_M={};NEW_T={}
for p in sorted(glob.glob('lessons/L*.txt')):
    lid,m,t,errs=parse_file(p)
    for q in m:
        q.pop('_line',None);q.pop('section',None) if False else None
        # pre-shuffle options deterministically, balanced position
        NEW_M[q['id']]=q
    for q in t: q.pop('_line',None);NEW_T[q['id']]=q
# balanced answer positions for new MC
pos=0
for i,q in enumerate(sorted(NEW_M.values(),key=lambda q:q['id'])):
    opts=q['options'];c=opts[0];d=opts[1:];rng.shuffle(d);k=i%4;d.insert(k,c);q['options']=d;q['answer']=k
allM={q['id']:q for q in bankM};allM.update({q['id']:q for e in BASE for q in e['mcq']});allM.update(NEW_M)
allT={q['id']:q for q in bankT};allT.update({q['id']:q for e in BASE for q in e['tf']});allT.update(NEW_T)
def lesson_variants(lid,K,limit=4,iters=20000,seed=0):
    r=random.Random(lid*100+K+seed)
    v1=next(e for e in BASE if e['id']==f'lesson-{lid}')
    v1m=[q['id'] for q in v1['mcq']];v1t=[q['id'] for q in v1['tf']]
    poolM=[i for i,q in allM.items() if q['lesson']==lid and i not in v1m]
    poolT=[i for i,q in allT.items() if q['lesson']==lid and i not in v1t]
    candM=poolM+v1m;candT=poolT+v1t
    def init():
        vs=[]
        for j in range(K):
            m=r.sample(candM,15);t=r.sample(candT,2);vs.append([m,t])
        return vs
    def cost(vs):
        sets=[set(v1m)|set(v1t)]+[set(m)|set(t) for m,t in vs];c=0
        for a,b in itertools.combinations(range(len(sets)),2):
            o=len(sets[a]&sets[b]);c+=max(0,o-limit)*100
        for m,t in vs:
            lv=Counter(allM[i]['level'] for i in m);c+=abs(lv['NB']-9)+abs(lv['TH']-4)+abs(lv['VD']-2)
            c+=sum(5 for i in t if i in v1t)*0  # allowed
            if all(i in v1t for i in t):c+=50
        return c
    vs=init();cur=cost(vs)
    for it in range(iters):
        j=r.randrange(K);m,t=vs[j]
        if r.random()<0.85:
            k=r.randrange(15);x=r.choice(candM)
            if x in m:continue
            old=m[k];m[k]=x;c=cost(vs)
            if c<=cur:cur=c
            else:m[k]=old
        else:
            k=r.randrange(2);x=r.choice(candT)
            if x in t:continue
            old=t[k];t[k]=x;c=cost(vs)
            if c<=cur:cur=c
            else:t[k]=old
        if cur==0:break
    return vs,cur

def meta(src):return {k:src[k] for k in ('seconds','attemptLimit','showAnswers','open','maxViolations')}
def topics_of(m,t):return sorted({q['topic'] for q in m+t})
def build():
    out=[];report={}
    used=Counter()
    for lid in range(1,29):
        K=4 if lid<=13 else 3
        best=None
        for s in range(8):
            vs,c=lesson_variants(lid,K,iters=30000,seed=s)
            if c<100 and (best is None or c<best[1]):best=(vs,c)
            if best and best[1]==0:break
        assert best, lid
        v1=next(e for e in BASE if e['id']==f'lesson-{lid}')
        report[lid]=K
        for n,(m,t) in enumerate(best[0],start=2):
            mq=[copy.deepcopy(allM[i]) for i in m];tq=[copy.deepcopy(allT[i]) for i in t]
            for i in m+t:used[i]+=1
            out.append({'id':f'lesson-{lid}-v{n}','title':v1['title']+f' · Đề {n}','kind':'lesson','topics':topics_of(mq,tq),'mcq':mq,'tf':tq,**meta(v1),'variant':n,'lessonId':lid,'generated':True})
    # term variants
    R=random.Random(7)
    scopes={'midterm-1':list(range(1,8)),'final-1':list(range(1,15)),'midterm-2':list(range(15,22)),'final-2':list(range(15,29))}
    titles={'midterm-1':'Giữa kỳ 1 · Bài 1–7','final-1':'Cuối kỳ 1 · Bài 1–14','midterm-2':'Giữa kỳ 2 · Bài 15–21','final-2':'Cuối kỳ 2 · Bài 15–28'}
    for key,ids in scopes.items():
        base=next(e for e in BASE if e['id']==key);tu=Counter(q['id'] for q in base['mcq']+base['tf'])
        for n in range(2,6):
            def pick(pool,k):
                groups={}
                for q in sorted(pool,key=lambda q:(tu[q['id']],R.random())):groups.setdefault(q['lesson'],[]).append(q)
                order=list(groups);R.shuffle(order);res=[]
                while len(res)<k:
                    moved=False
                    for l in order:
                        if groups[l] and len(res)<k:res.append(groups[l].pop(0));moved=True
                    if not moved:raise SystemExit('short '+key)
                return res
            mc=[q for q in allM.values() if q['lesson'] in ids]
            m=pick([q for q in mc if q['level']=='NB'],30)+pick([q for q in mc if q['level']=='TH'],10)+pick([q for q in mc if q['level']=='VD'],5)
            t=pick([q for q in allT.values() if q['lesson'] in ids],9)
            for q in m+t:tu[q['id']]+=1
            mq=[copy.deepcopy(q) for q in m];tq=[copy.deepcopy(q) for q in t]
            out.append({'id':f'{key}-v{n}','title':titles[key]+f' · Đề {n}','kind':'combined','topics':topics_of(mq,tq),'mcq':mq,'tf':tq,**meta(base),'termKey':key,'variant':n,'generated':True})
    # THPT 04..10
    tb=[e for e in BASE if e['id'].startswith('thpt')];tu=Counter(q['id'] for e in tb for q in e['mcq']+e['tf'])
    quota={'A':2,'B':3,'C':2,'D':6,'E':2,'F':2,'G':5}
    def least(pool,k):
        p=sorted(pool,key=lambda q:(tu[q['id']],R.random()));return p[:k]
    for n in range(4,11):
        m=least([q for q in allM.values() if q['lesson']==101],1)+least([q for q in allM.values() if q['lesson'] in(111,112)],1)
        for tp,k in quota.items():
            pool=[q for q in allM.values() if q['topic']==tp and q['lesson']<=28]
            # mix levels: roughly 55% NB 30% TH 15% VD
            lv=least([q for q in pool if q['level']=='NB'],max(1,round(k*.5)));rest=least([q for q in pool if q['level']!='NB' and q not in lv],k-len(lv));m+=lv+rest
        common=least([q for q in allT.values() if 1<=q['lesson']<=6],1)+least([q for q in allT.values() if 7<=q['lesson']<=18],1)
        ict=least([q for q in allT.values() if 22<=q['lesson']<=28],1)+least([q for q in allT.values() if 19<=q['lesson']<=21 or q['lesson']==112],1)
        for q in m+common+ict:tu[q['id']]+=1
        R.shuffle(m)
        mq=[copy.deepcopy(q) for q in m];tq=[copy.deepcopy(q) for q in common+ict]
        assert len(mq)==24 and len(tq)==4
        out.append({'id':f'thpt-ict-{n:02d}','title':f'Thi thử tốt nghiệp THPT · Tin học ICT · Đề {n:02d} (luyện 40s/ý)','kind':'combined','topics':topics_of(mq,tq),'mcq':mq,'tf':tq,**meta(tb[0]),'tfCommonIds':[q['id'] for q in common],'tfICTIds':[q['id'] for q in ict],'variant':n,'generated':True})
    for e in out:
        for q in e['mcq']+e['tf']:q.pop('section',None) if False else None
    return out,report
if __name__=='__main__':
    out,rep=build()
    exams=BASE+out
    json.dump(exams,open(ROOT+'lib/exams.json','w'),ensure_ascii=False)
    json.dump(list(NEW_M.values()),open(ROOT+'lib/mcq-v3.json','w'),ensure_ascii=False)
    json.dump(list(NEW_T.values()),open(ROOT+'lib/tf-v3.json','w'),ensure_ascii=False)
    print('exams',len(exams),'generated',len(out),'newMC',len(NEW_M),'newTF',len(NEW_T))
    print(Counter((e['kind'],e.get('termKey') or ('thpt' if e['id'].startswith('thpt') else '')) for e in out))
