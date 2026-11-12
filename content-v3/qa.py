import json,itertools,re,unicodedata,difflib
from collections import Counter,defaultdict
E=json.load(open('../lib/exams.json'))
def norm(s):return re.sub(r'\W+',' ',unicodedata.normalize('NFC',s).lower()).strip()
errs=[];ids=Counter(e['id'] for e in E)
errs+=[f'dup exam id {k}' for k,v in ids.items() if v>1]
qdef={}
for e in E:
    for q in e['mcq']:
        o=q['options']
        if len(o)!=4 or len(set(o))!=4:errs.append(f"{e['id']} {q['id']} options")
        if q['answer'] not in range(4):errs.append(f"{q['id']} answer")
        if not q.get('explanation','').strip():errs.append(f"{q['id']} expl")
        if q['id'] in qdef and qdef[q['id']]!=json.dumps(q,sort_keys=True,ensure_ascii=False):errs.append('inconsistent '+q['id'])
        qdef[q['id']]=json.dumps(q,sort_keys=True,ensure_ascii=False)
    for t in e['tf']:
        if len(t['statements'])!=4 or any(type(s['answer'])!=bool or not s['explanation'] for s in t['statements']):errs.append(f"{t['id']} tf")
    if e.get('tfCommonIds') and len(e['mcq'])!=24:errs.append(e['id']+' thpt size')
    if len({q['id'] for q in e['mcq']})!=len(e['mcq']):errs.append(e['id']+' dup q in exam')
print('errors',errs[:20],len(errs))
def S(e):return {q['id'] for q in e['mcq']+e['tf']}
groups=defaultdict(list)
for e in E:
    if e['kind']=='lesson':groups['L'+str(e['mcq'][0]['lesson'])].append(e)
    elif e['id'].startswith('thpt'):groups['thpt'].append(e)
    elif e.get('termKey') or e['id'] in('midterm-1','final-1','midterm-2','final-2'):groups[e.get('termKey',e['id'])].append(e)
mx={}
for g,es in groups.items():
    mx[g]=(len(es),max((len(S(a)&S(b)) for a,b in itertools.combinations(es,2)),default=0))
print({k:v for k,v in mx.items()})
pos=Counter(q['answer'] for q in json.load(open('../lib/mcq-v3.json')))
print('answer pos new',pos)
# exact/near duplicate stems among new vs all bank
bank=json.load(open('../lib/mcq.json'))+json.load(open('../lib/mcq-v3.json'));st=defaultdict(list)
for q in bank:st[norm(q['question'])].append(q['id'])
d=[v for v in st.values() if len(v)>1];print('exact dup stems',len(d),d[:10])
