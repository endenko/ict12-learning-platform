import json,re,unicodedata,difflib
def norm(s):return re.sub(r'\s+',' ',unicodedata.normalize('NFC',s).lower()).strip()
base=[q for q in json.load(open('mcq.base.json'))];new=[q for q in json.load(open('../lib/mcq.json')) if q['id'].startswith('v3')]
B=[(q['id'],norm(q['question'])) for q in base];N=[(q['id'],norm(q['question']),q['options'][q['answer']]) for q in new]
hits=[]
for i,(a,s,_) in enumerate(N):
    for b,t in B:
        if s==t or difflib.SequenceMatcher(None,s,t).quick_ratio()>0.9 and difflib.SequenceMatcher(None,s,t).ratio()>0.9:hits.append((a,b))
    for b,t,_ in N[i+1:]:
        if s==t or difflib.SequenceMatcher(None,s,t).quick_ratio()>0.9 and difflib.SequenceMatcher(None,s,t).ratio()>0.9:hits.append((a,b))
print(len(hits));qs={q['id']:q['question'] for q in base+new}
for a,b in hits:print(a,'|',qs[a][:80],'||',b,'|',qs[b][:80])
