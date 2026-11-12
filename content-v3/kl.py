import sys
sys.path.insert(0,'.')
from parse import parse_file
N=int(sys.argv[-1])
for a in sys.argv[1:-1]:
    lid,mcq,_,_=parse_file('lessons/L%02d.txt'%int(a));c=0
    print('== L%02d'%lid)
    for q in mcq:
        o=q['options'];l=[len(x) for x in o]
        if l[0]>max(l[1:]) and c<N:
            c+=1;print(q['_line'],l,q['question'][:70],'::',' | '.join(o))
