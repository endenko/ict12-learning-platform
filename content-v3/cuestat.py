import glob,sys,json
sys.path.insert(0,'.')
from parse import parse_file
def stats(items):
    n=len(items);L=S=uL=uS=0;rank=[0]*4
    for o in items:
        l=[len(x) for x in o];k=l[0]
        mx=max(l);mn=min(l)
        if k==mx:L+=1/l.count(mx)
        if k==mn:S+=1/l.count(mn)
        if k>max(l[1:]):uL+=1
        if k<min(l[1:]):uS+=1
        rank[sum(1 for x in l[1:] if x>k)]+=1
    return dict(n=n,longest_strategy=round(100*L/n,1),shortest_strategy=round(100*S/n,1),key_unique_longest=round(100*uL/n,1),key_unique_shortest=round(100*uS/n,1),distractors_longer_than_key_dist=rank)
new=[q['options'] for p in sorted(glob.glob('lessons/L*.txt')) for q in parse_file(p)[1]]
base=[q['options'][q['answer']:q['answer']+1]+[o for i,o in enumerate(q['options']) if i!=q['answer']] for q in json.load(open('mcq.base.json'))]
print('new ',stats(new));print('base',stats(base))
