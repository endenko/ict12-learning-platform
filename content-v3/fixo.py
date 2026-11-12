import sys,unicodedata,itertools,hashlib
# stdin: "LINE<TAB>key~alt|d1~alt|d2|d3" -> picks combo, replaces fields 2..5
lid=int(sys.argv[1]);p='lessons/L%02d.txt'%lid;L=open(p,encoding='utf-8').read().split('\n')
def cat(l):
    return 'L' if l[0]>max(l[1:]) else ('S' if l[0]<min(l[1:]) else 'M')
for row in sys.stdin.read().strip().split('\n'):
    if not row.strip():continue
    n,opts=row.split('\t');n=int(n)-1
    alts=[[unicodedata.normalize('NFC',a.strip()) for a in x.split('§')] for x in opts.split('|')]
    assert len(alts)==4,row
    f=L[n].split('|');assert len(f)==7,(n+1,len(f))
    want=__import__('os').environ.get('WANT') or 'LSMM'[int(hashlib.md5(f'{lid}:{n}'.encode()).hexdigest(),16)%4]
    best=None
    for c in itertools.product(*alts):
        l=[len(x) for x in c];r=max(l)/min(l);k=cat(l)
        score=(r>1.15, r if r>1.15 else 0, 0 if k==want else (1 if k=='M' else 2), r)
        if best is None or score<best[0]:best=(score,c)
    o=list(best[1]);f[2:6]=o;L[n]='|'.join(f)
    l=[len(x) for x in o];r=max(l)/min(l)
    print(n+1,f[1][:60],'OK ' if r<=1.15 else 'BAD',round(r,3),l,cat(l),'want',want, '' if r<=1.15 else ' || '.join(o))
open(p,'w',encoding='utf-8').write('\n'.join(L))
