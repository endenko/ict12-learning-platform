#!/usr/bin/env python3
"""Build public/theory.json (lesson theory content) and lib/theory-index.json (server-side counts) from theory/*.txt."""
import json, re, glob, sys, os
ROOT = os.path.dirname(os.path.abspath(__file__))
lessons = {l['id']: l for l in json.load(open(os.path.join(ROOT, '..', 'lib', 'lessons.json')))}
out = {}
def blocks(lines):
    res, i = [], 0
    while i < len(lines):
        ln = lines[i]
        if not ln.strip(): i += 1; continue
        if ln.startswith(':::code'):
            parts = ln.split(); lang = parts[1] if len(parts) > 1 else 'html'; live = 'live' in parts
            j = i + 1; code = []
            while lines[j] != ':::end': code.append(lines[j]); j += 1
            res.append({'t': 'code', 'lang': lang, 'live': live, 'code': '\n'.join(code)}); i = j + 1; continue
        m = re.match(r':::(note|flow|stack) (.*)', ln)
        if m:
            k, v = m.groups()
            if k == 'note': res.append({'t': 'note', 'text': v})
            elif k == 'flow': res.append({'t': 'flow', 'steps': [s.strip() for s in v.split(' > ')]})
            else: res.append({'t': 'stack', 'layers': [s.strip() for s in v.split(' | ')]})
            i += 1; continue
        if ln.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                rows.append([c.strip() for c in lines[i].strip().strip('|').split(' | ')]); i += 1
            res.append({'t': 'table', 'head': rows[0], 'rows': rows[1:]}); continue
        if ln.startswith('- '):
            items = []
            while i < len(lines) and lines[i].startswith('- '): items.append(lines[i][2:].strip()); i += 1
            res.append({'t': 'ul', 'items': items}); continue
        assert not ln.startswith(':::'), ln
        res.append({'t': 'p', 'text': ln.strip()}); i += 1
    return res
for f in sorted(glob.glob(os.path.join(ROOT, 'theory', '*.txt'))):
    for chunk in open(f, encoding='utf-8').read().split('=== ')[1:]:
        head, *body = chunk.split('\n'); lid = int(head.strip()); L = lessons[lid]
        parts, cur = [], None
        for ln in body:
            if ln.startswith('@'):
                name, _, title = ln[1:].partition(' '); cur = {'k': name, 'title': title.strip(), 'lines': []}; parts.append(cur)
            elif cur is not None: cur['lines'].append(ln.rstrip())
        les = {'id': lid, 'topic': L['topic'], 'title': L['title'], 'pages': L['pages'], 'goals': [], 'sections': [], 'remember': [], 'mistakes': [], 'terms': [], 'cards': [], 'checks': []}
        for p in parts:
            li = [x for x in p['lines'] if x.strip()]
            if p['k'] == 'goals': les['goals'] = [x[2:] for x in li]
            elif p['k'] == 'sec': les['sections'].append({'id': f's{len(les["sections"])+1}', 'title': p['title'], 'blocks': blocks(p['lines'])})
            elif p['k'] == 'remember': les['remember'] = [x[2:] for x in li]
            elif p['k'] == 'mistakes': les['mistakes'] = [dict(zip(('wrong', 'right'), x[2:].split(' => '))) for x in li]
            elif p['k'] == 'terms': les['terms'] = [dict(zip(('term', 'def'), x[2:].split(' :: ', 1))) for x in li]
            elif p['k'] == 'cards': les['cards'] = [dict(zip(('front', 'back'), x[2:].split(' :: ', 1))) for x in li]
            elif p['k'] == 'check':
                q = None
                for x in li:
                    if x.startswith('? '): q = {'q': x[2:], 'options': [], 'answer': 0, 'explain': ''}; les['checks'].append(q)
                    elif x.startswith('+ '): q['answer'] = len(q['options']); q['options'].append(x[2:])
                    elif x.startswith('- '): q['options'].append(x[2:])
                    elif x.startswith('= '): q['explain'] = x[2:]
                    else: raise SystemExit(f'L{lid} bad check line {x!r}')
            else: raise SystemExit(f'L{lid} unknown part {p["k"]}')
        errs = []
        if len(les['goals']) < 2: errs.append('goals')
        if len(les['sections']) < 2: errs.append('sections')
        if len(les['remember']) < 2: errs.append('remember')
        if len(les['mistakes']) < 2 or any(len(m) != 2 for m in les['mistakes']): errs.append('mistakes')
        if len(les['terms']) < 4 or any(len(t) != 2 for t in les['terms']): errs.append('terms')
        if len(les['cards']) < 6 or any(len(c) != 2 for c in les['cards']): errs.append('cards')
        if not 3 <= len(les['checks']) <= 5 or any(len(c['options']) != 4 or not c['explain'] for c in les['checks']): errs.append('checks')
        if errs: raise SystemExit(f'L{lid}: {errs}')
        les['words'] = len(re.findall(r'\w+', json.dumps(les['sections'], ensure_ascii=False)))
        out[lid] = les
missing = [i for i in range(1, 29) if i not in out]
if missing: raise SystemExit(f'missing {missing}')
data = {'version': 1, 'lessons': [out[i] for i in range(1, 29)]}
json.dump(data, open(os.path.join(ROOT, '..', 'public', 'theory.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
index = {str(l['id']): {'sections': len(l['sections']), 'cards': len(l['cards']), 'checks': len(l['checks']), 'answers': [c['answer'] for c in l['checks']]} for l in data['lessons']}
json.dump(index, open(os.path.join(ROOT, '..', 'lib', 'theory-index.json'), 'w'), separators=(',', ':'))
print('lessons', len(out), 'sections', sum(len(l['sections']) for l in out.values()), 'cards', sum(len(l['cards']) for l in out.values()), 'checks', sum(len(l['checks']) for l in out.values()), 'terms', sum(len(l['terms']) for l in out.values()), 'live examples', sum(1 for l in out.values() for s in l['sections'] for b in s['blocks'] if b['t'] == 'code' and b['live']), 'bytes', os.path.getsize(os.path.join(ROOT, '..', 'public', 'theory.json')))
