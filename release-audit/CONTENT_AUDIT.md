# Content and curriculum release audit — 09/11/2026 (UTC+7)

## What was actually verified

- Supplied scanned **Tin học 12 — Kết nối tri thức với cuộc sống, định hướng Tin học ứng dụng**. Actual attachment: `01M6RAR3WEXWP0SF6C96V030BR.pdf` in the originating attachment folder. Contents and preface read from rendered pages; page numbers below are printed pages, not PDF offsets.
- All **28 lesson titles, topic grouping, and page ranges** matched against contents (printed 1–2) and `lib/lessons.json`. Preface printed 3 distinguishes common lessons 1–21 and ICT 22–28. A–G are app labels for the textbook's topics 1–7, not official curriculum letters.
- Structurally validated **468 MCQ +73 TF groups (292 statements), all 45 sets**: valid choices/keys, non-empty Vietnamese rationales, 2 TH +2 VD per TF group, no duplicate stems/scenarios within a set, every textbook lesson represented. This is NOT the same as semantic certification.
- **Cumulative internal semantic review completed:468 MCQ +73 TF groups/292 statements.** Round1 read140 MCQ +43 groups/172 statements (`selection.json`, `review-mcq.txt`, `review-tf.txt`). Completion round separately read all remaining328 MCQ +30 groups/120 statements, including every option/key/rationale and scenario. Authored448 individual notes and source-bound evidence: `full-review/item-ledger.jsonl`, `full-review/notes-*.tsv`, `full-review/sources.json`.
- This is **internal review, not independent expert certification or official approval**. Exact completion scope,31 corrections and pedagogical limits: `full-review/REVIEW_REPORT.md`. Page references honestly distinguish specific read pages from chapter/section ranges.
- Executable checks supplement reading: Python iteration/indexing/counts; SQL filtering, grouping, composite keys, joins, FK rejection and revenue; browser HTML/CSS/form checks in test evidence.

## Corrections

Exact patch and reproducible content-only transformation: `content-corrections.json`, `correct-content.py` (starts from `*-v2.json` baselines).

1. Switch rationale no longer claims it never floods: known unicast targeted; broadcast/unknown destinations can flood (`q40`).
2. CSS `:hover` does not require pointer movement (`ext-l17-q01`).
3. Website definition explicitly scoped to the textbook's **multi-page model**, avoiding a false claim that single-page websites cannot exist (`ext-l18-q01`).
4. Hardware service explanation requires shutdown/disconnection, trained safe procedure (`ext-l19-q14`).
5. HTML scenario uses `<title>CLB</title>`, not a `title="CLB"` attribute in head (`ext-l7-t1`).
6. Composite-key premise explicitly includes non-null code fields (`ext-found-t2`); `TenKH` spelling fixed (`ext-found-t3`).
7. TCP reliability/ports belong to transport, not application layer (`t10`).
8. Removed the unintended universal **2 true +2 false** guessing shortcut. Twelve reviewed groups now have one or three true statements; all still have 2 TH +2 VD. The official format specifies four statements, not a mandatory truth count. Rewritten statements and rationales are in the patch, not silently flipped keys.

Completion round adds **31 content-only patches:28 MCQ records +3 TF context/statement records**, with no key changes. These resolve history/network precision, HTML/audio/link ambiguity, CSS inherited values/table layout/cascade prerequisites, consent and HDMI premises, accurate display-mode descriptions and separate current Forms publication/access. Reproduce with `python3 release-audit/full-review/apply-corrections.py` from the included round1 baselines; see exact before/after in `full-review/corrections.json`. A final cross-bank pass also aligns previously reviewed t10.c with TCP byte sequence numbers (RFC9293), separately evidenced in `full-review/followup-semantic-review.json` without double-counting the remaining120 statements. The older `correct-content.py` alone reconstructs round1 only; apply the completion patch afterward.

No saved score/result or prior server snapshot was regraded. New-bank changes affect new attempts. Existing historical records retain their original question/answer context. Wrong-answer practice uses current canonical wording with original source permissions, and server-only per-question provenance handles teacher-customized term scopes.

## Official exam structure, and what this platform is not

- QĐ **764/QĐ-BGDĐT, 08/03/2024**: Tin học 50 minutes, 24 MCQ x0.25 =6; six printed TF groups =2 common +2 CS +2 ICT. ICT candidates answer 2 common +2 ICT =4 groups, not all six.
- TF: 0/1/2/3/4 correct statements =>0/0.1/0.25/0.5/1 point. These ICT mocks contain only the branch to be answered: 24 MCQ +4 groups, raw maximum10.
- Three mock banks explicitly separate common/ICT groups. This is **40-second-per-step, sequential speed practice**, not a faithful 50-minute navigation/timing simulator. Maximum40 steps x40s =26m40s.
- 2026's actual grade-level distribution is evidence about that paper, not a perpetual national blueprint. The bank's 40/30/30 difficulty mix is a pedagogical choice, not a verified mandated proportion.

Sources actually read (official pages and clearly identified legal mirrors):
1. Government 2026 paper/format: https://xaydungchinhsach.chinhphu.vn/thi-tot-nghiep-thpt-2026-de-thi-mon-tin-hoc-goi-y-dap-an-119260612145639712.htm
2. QĐ764 legal mirror/full text: https://thuvienphapluat.vn/van-ban/Giao-duc/Quyet-dinh-764-QD-BGDDT-2024-cau-truc-dinh-dang-de-thi-Ky-thi-tot-nghiep-trung-hoc-pho-thong-601389.aspx
3. Ministry Quality Management Department announcement: https://vqa.moet.gov.vn/vi/news/thong-bao/cau-truc-dinh-dang-de-thi-tot-nghiep-thpt-tu-nam-2025-74.html
4. CV5512 school planning legal mirror: https://thuvienphapluat.vn/cong-van/Giao-duc/Cong-van-5512-BGDDT-GDTrH-2020-xay-dung-va-to-chuc-thuc-hien-ke-hoach-giao-duc-cua-nha-truong-462988.aspx
5. TT32/2018 official curriculum PDF hosted by a public school: https://thptduchop.hungyen.edu.vn/upload/45988/20220622/thong-tu-32-2018-tt-bgddt-ban-hanh-chuong-trinh-giao-duc-pho-thong-moi_1__5ae70.pdf (reference found, not represented as fully read in this audit).

## Semester policy

No single universally official lesson-to-semester division was established. School teaching plans vary; CV5512 supports school's proactive education planning. Defaults are **explicit recommendations**: HK1 lessons1–14, HK2 15–28; midterm1 1–7, final1 1–14, midterm2 15–21, final2 15–28.

Teacher can edit lesson semesters, topic display names, exam semester labels and actual term-exam lesson scopes without code. Insufficient scope is rejected rather than silently filling from other lessons. A valid term remains45 MCQ (30NB/10TH/5VD) +9 TF groups; a broad scope is a pool, not a promise that every selected lesson has every question type. Saved attempts snapshot the effective bank; configuration changes do not rewrite previous results. Restoring recommended defaults is explicit.

## Genuine uncertainty / residual review needs

- No demonstrably wrong key or multiple-valid-answer issue identified by this internal review remains unresolved. No unreviewed remainder remains in the stated bank, but independent expert review and teacher approval before consequential assessment are still not claimed.
- Many items are introductory with easy distractors. NB/TH/VD categories and the fixed length balance are authorial constraints, not empirical difficulty/discrimination calibration.
- Google Sites/Forms and OS button names/locations may have changed since textbook screenshots. Current official Google help was checked; separate Forms publication/respondent permissions are now explicit in the relevant explanations. Items follow the supplied edition and intended function; no claim of testing every current third-party UI.
- Local banks are practice materials, not Ministry-issued/certified papers. Timings and navigation differ as disclosed.
- Previously recorded history remains historical, even where a later bank wording/rationale was improved; no retrospective score change without a separate authorized teacher decision.
