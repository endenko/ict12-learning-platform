import sys,json
sys.path.insert(0,'.');from parse import load_bank
bm,bt=load_bank()
for lid in map(int,sys.argv[1:]):
    for q in bm:
        if q['lesson']==lid:print(q['level'][0],q['question'],'=>',q['options'][q['answer']])
    for q in bt:
        if q['lesson']==lid:print('TF',q['scenario'][:90],'|',' / '.join(('T ' if s['answer'] else 'F ')+s['text'][:50] for s in q['statements']))
