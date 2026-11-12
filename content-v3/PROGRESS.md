# v3 content authoring progress (executor notes)
Format: lessons/LNN.txt; lines: #section | N/T/V|q|correct|w1|w2|w3|expl | TF|scenario|T/F|text|expl x4
Check: python3 parse.py lessons/LNN.txt ; fix: printf 'LINE\tFIELD\ttext' | python3 fix.py file
Target per lesson: ~36 new MC (minus free pool items) + 2-3 TF. Plan: v2..v4 per lesson = 12 new + 3 reused MC from v1 + 1 new TF + 1 old TF.
Done: L01-L28 authored + extras; next build.py
WARNING: fix.py field idx: 0=level,1=question,2=correct,3-5=distractors,6=expl. Always re-print edited lines.
## Status (build stage)
- All L01-L28 authored; build.py -> lib/exams.json (165 exams, 120 generated), lib/mcq-v3.json, lib/tf-v3.json. Original lib/mcq.json/tf.json untouched (restored from *.base.json).
- Lesson variants: L1-13 v2..v5 (4 extra), L14-28 v2..v4 (3 extra); pairwise overlap <=4 (MC+TF). Term v2..v5 each; THPT 04..10.
- Backend: lib/mix.js (practiceMix, bookmarks, importQuestions), api patched, curriculum termKey/seed, features mastery.
- Tests: unit/upgrade-unit/readiness-unit/content-audit-unit pass.
- Next: frontend redesign (public/app.js, style.css), e2e, deploy.
