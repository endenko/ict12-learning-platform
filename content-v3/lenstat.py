import glob,sys
sys.path.insert(0,'.')
from parse import parse_file
tot=fail=longest=shortest=uniqlong=0;fails=[]
for p in sorted(glob.glob('lessons/L*.txt')):
    lid,mcq,tf,e=parse_file(p)
    for q in mcq:
        L=[len(o) for o in q['options']];tot+=1
        r=max(L)/min(L)
        if r>1.15:fail+=1;fails.append((lid,q['_line'],round(r,2),L))
        if L[0]==max(L):longest+=1
        if L[0]>max(L[1:]):uniqlong+=1
        if L[0]==min(L):shortest+=1
print('total',tot,'fail1.15',fail,'key longest(incl tie)',longest,round(100*longest/tot,1),'unique longest',uniqlong,round(100*uniqlong/tot,1),'key shortest(incl tie)',shortest,round(100*shortest/tot,1))
if len(sys.argv)>1:
    for f in fails:print(*f)
