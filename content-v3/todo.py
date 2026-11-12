import sys
sys.path.insert(0,'.')
from parse import parse_file
for a in sys.argv[1:]:
    lid,mcq,tf,e=parse_file('lessons/L%02d.txt'%int(a))
    print('== L%02d'%lid)
    for q in mcq:
        o=q['options'];L=[len(x) for x in o]
        bad=max(L)/min(L)>1.15; kl=L[0]>max(L[1:])
        if bad or kl:print(q['_line'],'BAD' if bad else 'KL',L,q['question'],'::',' | '.join(o))
