#!/usr/bin/env python3
"""Search YouTube for Vietnamese Tin học 12 (Kết nối tri thức) lesson videos, keep only titles matching the lesson number + title,
and verify each with the public oEmbed endpoint (HTTP 200 => exists and embeddable). Writes candidates.json + seed.json."""
import json, re, time, unicodedata, urllib.parse, urllib.request, os
ROOT = os.path.dirname(os.path.abspath(__file__))
lessons = [l for l in json.load(open(os.path.join(ROOT, '..', '..', 'lib', 'lessons.json'))) if l['id'] <= 28]
UA = {'User-Agent': 'Mozilla/5.0', 'Accept-Language': 'vi'}
def norm(s):
    s = unicodedata.normalize('NFD', s.lower()).replace('đ', 'd'); s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9 ]', ' ', s)
def words(s): return [w for w in norm(s).split() if len(w) > 1 and w not in {'va', 'cac', 'mot', 'so', 'voi', 'cua', 'trong', 'vao', 'cho'}]
def search(q):
    req = urllib.request.Request('https://www.youtube.com/results?search_query=' + urllib.parse.quote(q), headers=UA)
    s = urllib.request.urlopen(req, timeout=30).read().decode('utf-8')
    d = json.loads(re.search(r'var ytInitialData = (\{.*?\});</script>', s).group(1))
    def walk(o):
        if isinstance(o, dict):
            if 'videoRenderer' in o:
                v = o['videoRenderer']
                yield {'id': v['videoId'], 'title': ''.join(r['text'] for r in v['title']['runs']), 'channel': (v.get('ownerText', {}).get('runs') or [{}])[0].get('text', ''), 'length': v.get('lengthText', {}).get('simpleText', '')}
            for x in o.values(): yield from walk(x)
        elif isinstance(o, list):
            for x in o: yield from walk(x)
    return list(walk(d))
def oembed(vid):
    url = 'https://www.youtube.com/oembed?format=json&url=' + urllib.parse.quote(f'https://www.youtube.com/watch?v={vid}')
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20); return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e: return e.code, None
def secs(t):
    p = [int(x) for x in t.split(':')] if t else []
    return sum(v * 60 ** i for i, v in enumerate(reversed(p)))
cands, seed = {}, {}
for L in lessons:
    n, title = L['id'], L['title']; tw = set(words(title))
    found = {}
    for q in [f'Tin học 12 kết nối tri thức Bài {n} {title}', f'Tin học 12 ICT Bài {n} {title}']:
        for v in search(q): found.setdefault(v['id'], v)
        time.sleep(1)
    ok = []
    for v in found.values():
        t = norm(v['title'])
        if not re.search(rf'\bbai\s*0?{n}\b', t): continue
        if not re.search(r'\b(12|tin hoc 12|lop 12)\b', t): continue
        overlap = len(tw & set(t.split())) / max(1, len(tw))
        if overlap < 0.6 or not (120 <= secs(v['length']) <= 3600): continue
        v['overlap'] = round(overlap, 2); ok.append(v)
    ok.sort(key=lambda v: (-v['overlap'], 'vietjack' not in norm(v['channel'])))
    verified = []
    for v in ok[:6]:
        st, meta = oembed(v['id'])
        v['oembed'] = st
        if st == 200 and meta:
            v['oembedTitle'] = meta.get('title'); v['author'] = meta.get('author_name')
            # oEmbed title must still match the lesson (guards against a reused/changed video)
            if re.search(rf'\bbai\s*0?{n}\b', norm(meta['title'])) and len(tw & set(norm(meta['title']).split())) / max(1, len(tw)) >= 0.6:
                verified.append({'id': v['id'], 'title': meta['title'][:200], 'author': (meta.get('author_name') or '')[:100], 'provider': 'youtube'})
        if len(verified) >= 2: break
        time.sleep(0.3)
    cands[n] = ok[:6]; seed[n] = verified
    print(n, len(found), len(ok), [ (x['author'], x['title'][:60]) for x in verified], flush=True)
json.dump(cands, open(os.path.join(ROOT, 'candidates.json'), 'w'), ensure_ascii=False, indent=1)
json.dump({'checkedAt': time.strftime('%Y-%m-%dT%H:%M:%S%z'), 'method': 'YouTube search + oEmbed 200 + title match (lesson number and >=60% title words)', 'lessons': seed}, open(os.path.join(ROOT, 'seed.json'), 'w'), ensure_ascii=False, indent=1)
