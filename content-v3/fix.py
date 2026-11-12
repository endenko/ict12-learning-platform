import sys
# stdin rows: "LINE<TAB>text" replaces line; "LINE<TAB>k<TAB>text" replaces field k (0-based split by |)
p=sys.argv[1];L=open(p,encoding='utf-8').read().split('\n')
rows=sys.stdin.read().strip().split('\n')
for row in rows:
    parts=row.split('\t')
    n=int(parts[0])-1
    if len(parts)==2:L[n]=parts[1]
    else:
        f=L[n].split('|');f[int(parts[1])]=parts[2];L[n]='|'.join(f)
open(p,'w',encoding='utf-8').write('\n'.join(L))
for n in sorted({int(r.split('\t')[0]) for r in rows}):print(n,'|'.join(L[n-1].split('|')[1:6])[:220])
for row in sys.stdin and []:pass
