"""Reproduce audited banks from round-one baselines, preserving the legacy bank and DB."""
import json,copy
from pathlib import Path
r=Path(__file__).resolve().parents[2];d=Path(__file__).resolve().parent
banks={k:json.loads((d/f'round1-{k}.json').read_text()) for k in ['mcq','tf','exams']}
for patch in json.loads((d/'corrections.json').read_text()):
 q=next(q for q in banks[patch['kind']] if q['id']==patch['id'])
 assert {f:q[f] for f in patch['before']}==patch['before'],patch['id']
 q.update(copy.deepcopy(patch['after']))
for e in banks['exams']:
 for kind in ['mcq','tf']:
  index={q['id']:q for q in banks[kind]}
  for i,q in enumerate(e[kind]):
   # Preserve exam-local routing metadata while synchronizing canonical content fields.
   assert q['id'] in index
   src=index[q['id']]
   for f in ['question','options','answer','explanation','scenario','statements','review']:
    if f in src:q[f]=copy.deepcopy(src[f])
for k,v in banks.items():(r/f'lib/{k}.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
print('Reproduced canonical banks and all45 exam copies; legacy bank and database untouched')
