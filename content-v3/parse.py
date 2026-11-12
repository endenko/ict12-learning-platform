import json,re,sys,os,glob,difflib,unicodedata
ROOT=os.path.dirname(os.path.abspath(__file__))
LESSONS={l['id']:l for l in json.load(open(ROOT+'/../lib/lessons.json'))}
LV={'N':'NB','T':'TH','V':'VD'}
def norm(s):return re.sub(r'\W+',' ',unicodedata.normalize('NFC',s).lower()).strip()
def parse_file(path):
    lid=int(re.search(r'L(\d+)',os.path.basename(path)).group(1));L=LESSONS[lid]
    sec=None;mcq=[];tf=[];errs=[]
    for n,line in enumerate(open(path,encoding='utf-8'),1):
        line=line.strip()
        if not line or line.startswith('//'):continue
        if line.startswith('#'):sec=line[1:].strip();continue
        f=[x.strip() for x in line.split('|')]
        if f[0] in LV:
            if len(f)!=7:errs.append(f'{path}:{n} MC needs 7 fields, got {len(f)}');continue
            k=len(mcq)+1
            mcq.append({'id':f'v3-l{lid}-m{k:02d}','type':'mcq','topic':L['topic'],'lesson':lid,'level':LV[f[0]],'section':sec,'question':f[1],'options':f[2:6],'answer':0,'explanation':f[6],'review':f"Bài {lid} – {sec} (trang {L['pages']})",'_line':n})
        elif f[0]=='TF':
            if len(f)!=14:errs.append(f'{path}:{n} TF needs 14 fields, got {len(f)}');continue
            st=[]
            for i in range(4):
                a,t,e=f[2+3*i:5+3*i]
                if a not in('T','F'):errs.append(f'{path}:{n} TF answer must be T/F')
                st.append({'label':'abcd'[i],'level':'TH' if i<2 else 'VD','answer':a=='T','text':t,'explanation':e})
            k=len(tf)+1
            tf.append({'id':f'v3-l{lid}-t{k:02d}','type':'tf','topic':L['topic'],'lesson':lid,'section':sec,'scenario':f[1],'statements':st,'review':f"Bài {lid} – {sec} (trang {L['pages']})",'_line':n})
        else:errs.append(f'{path}:{n} unknown line type {f[0][:10]}')
        if sec is None:errs.append(f'{path}:{n} no section')
    return lid,mcq,tf,errs
def ratio(opts):
    l=[len(o) for o in opts];return max(l)/min(l)
def load_bank():
    e=json.load(open(ROOT+'/../lib/exams.json'))
    m={};t={}
    for x in e:
        for q in x['mcq']:m[q['id']]=q
        for q in x['tf']:t[q['id']]=q
    return list(m.values()),list(t.values())
def check(paths,limit=1.5,verbose=True):
    bm,bt=load_bank();bank=[(norm(q['question']),q['id'],q['lesson']) for q in bm]
    allnew=[];bad=0;report=[]
    for p in paths:
        lid,mcq,tf,errs=parse_file(p)
        for e in errs:report.append('ERR '+e);bad+=1
        longest=0
        for q in mcq:
            r=ratio(q['options'])
            if r>limit and max(len(o) for o in q['options'])-min(len(o) for o in q['options'])>6:report.append(f"LEN {lid}:{q['_line']} r={r:.2f} {[len(o) for o in q['options']]}");bad+=1
            gap=len(q['options'][0])-max(len(o) for o in q['options'][1:])
            if gap>2:longest+=1
            if gap>4:report.append(f"CUE {lid}:{q['_line']} {[len(o) for o in q['options']]}");bad+=1
            if len(set(q['options']))<4:report.append(f"DUPOPT {lid}:{q['_line']}");bad+=1
            nq=norm(q['question'])
            for s,i,l in bank:
                if l==lid and difflib.SequenceMatcher(None,nq,s).ratio()>0.88:report.append(f"DUPBANK {lid}:{q['_line']} ~ {i}");bad+=1;break
            for o in allnew:
                if difflib.SequenceMatcher(None,nq,o[0]).ratio()>0.88:report.append(f"DUPNEW {lid}:{q['_line']} ~ {o[1]}");bad+=1;break
            allnew.append((nq,f"{lid}:{q['_line']}"))
        for q in tf:
            l=[len(s['text']) for s in q['statements']]
            if max(l)/min(l)>1.45:report.append(f"TFLEN {lid}:{q['_line']} {l}")
        if verbose:report.append(f"L{lid}: {len(mcq)} MC ({sum(q['level']=='NB' for q in mcq)}/{sum(q['level']=='TH' for q in mcq)}/{sum(q['level']=='VD' for q in mcq)}), {len(tf)} TF, correct-longest {longest}")
    print('\n'.join(report));return bad
if __name__=='__main__':
    paths=sys.argv[1:] or sorted(glob.glob(ROOT+'/lessons/L*.txt'))
    sys.exit(1 if check(paths) else 0)
