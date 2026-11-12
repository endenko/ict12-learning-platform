# Production deployment

## v4 — self-study theory, videos, learning progress · 2026-11-12 (UTC+7)
- Database: `migrations/v4-learning.sql` (additive; applied to Supabase afhgfdkozdwtjdsvldzj as migration `ict12_v4_learning`). New collections: progress, materials, videos, studytasks; index on data->>'ownerId'; scoped_check ownership branches for materials/videos/studytasks.
- Seed videos (idempotent, re-verifies oEmbed, skips admin-edited lessons): `node --env-file=.env scripts/seed-videos.js` → 28 lessons, 56 videos.
- Deploy files: prepare-deploy.py adds lib/learn.js, lib/sanitize.js, lib/theory-index.json, public/learn.js, public/learn.css, public/theory.json. vercel.json CSP adds frame-src/child-src https://www.youtube-nocookie.com https://player.vimeo.com and img-src https://i.ytimg.com.
- Production deployment: `dpl_6mgJqKw1rT9ULsxJ9CUwAtBy9Aid` (READY, alias ict12-learning-platform.vercel.app). Production: v4 e2e 24 checks + 18 isolation PASS, v4 regression 6/6 PASS; test data locked/archived (`tests/v4-cleanup-results.json`).

## v3 — teacher portal · 2026-11-12 (UTC+7)
- Database: apply `migrations/v3-teacher.sql` then `migrations/v3-teacher-2.sql` (additive; already applied to Supabase project afhgfdkozdwtjdsvldzj as migrations `ict12_v3_teacher_portal` and `ict12_v3_teacher_class_name_guard`). New collections: notes, announcements, questions, activity, presence. New RPC actions: `list_in`, `scoped_put`.
- Deploy files: `scripts/prepare-deploy.py` now includes lib/report.js, lib/roster.js, lib/portal.js, public/portal.js, public/portal.css.
- First teacher: admin → ★ Cổng giáo viên → Giáo viên → create (see README "Admin tạo tài khoản giáo viên đầu tiên").
- Production deployment: `dpl_8AZjSzTHonTY9y3RfLhJgs27ZB6v` (READY, alias ict12-learning-platform.vercel.app) — v3 e2e production 20 checks + 27 isolation checks PASS; v2 e2e production 22/22 PASS; test accounts locked, TEST classes archived (`tests/v3-cleanup-results.json`).

## Current authoritative release — full-bank completion · 2026-11-09T10:02:56.314317+07:00 (UTC+7)

- LIVE_VERIFIED: https://ict12-learning-platform.vercel.app ; deployment `dpl_GFDykbHYVAAxTabbRN3A32HmxzNf` READY, same project/team/alias, no SSO approval required.16 runtime files; only public help/server-side exam bank changed. No DB migration this round.
- Remaining328 TN +120 TF statements internally reviewed; cumulative468 TN +73 groups/292 statements.448 per-item notes plus separate t10.c consistency follow-up.31 content-only corrections (28 MCQ +3 TF records); keys/levels/IDs and historical results unchanged. Internal review, not independent expert certification.
- Final production22-check Playwright PASS,0 uncaught JS errors, mobile390px, strict real deadline403 with server-observed post-close proof (+2073ms). Final local/production content runs each92 exam+1 practice steps; exact live wording/rationale, active-key privacy and10/10 grading PASS.
- All45 banks/copies,365 TF scoring cases,20 actual Chromium semantics, bounded DB secret/deadline/atomic tests, native Excel/openpyxl (1 score+81 details,0 formulas), public hashes/private paths/security, both preservation baselines and original A-only HTTP200 PASS. TEST cleanup verified. Initial subsecond-clock harness failure retained and corrected, no application grace period.
- Evidence and genuine limits: `release-audit/RELEASE_REPORT.md`, `release-audit/full-review/REVIEW_REPORT.md`, `HANDOVER.json.contentCompletion`. Safe source archive regenerated without secrets/private backups/student datasets; operator-only because it contains answer banks. No load certification or destructive restore drill.

## Historical deployment phases (superseded by the block above)

- Live: https://ict12-learning-platform.vercel.app
- Admin: https://ict12-learning-platform.vercel.app/admin
- Hosting: Vercel, project `ict12-learning-platform`, team `endenkos-projects`, Node 24, region hnd1.
- Public HTTPS; Vercel deployment protection disabled for this student platform.
- Backend: Supabase `endenko’s Project` (`afhgfdkozdwtjdsvldzj`), private RLS-protected ICT12 schema.
- Encrypted server environment variables: SUPABASE_URL, SUPABASE_KEY, DB_SECRET. No secret source files uploaded.
- Admin credentials: `/workspace/ict12-platform/ADMIN_CREDENTIALS.txt` (mode 600).
- Production Playwright: admin login, issued TEST student login, all 23 steps of lesson 7 completed, score 10.00, analysis saved, zero uncaught JavaScript errors.
- TEST student `test_fullbook_64763228` locked; lock and admin result visibility independently verified.
- Production secret and answer-bank URLs all returned 404.
- 45 exam sets; textbook lessons A–G, proposed term mapping, three THPT training mocks.
- Original A-only site left unchanged.
- Verification files: `tests/vercel-production-smoke-results.json`, `tests/vercel-production-admin-verification.json`, `tests/vercel-public-http-results.json`, `tests/vercel-production-secret-paths.json`.
- Updated: 2026-11-07T22:20:10.355655+07:00 (Asia/Saigon).

## Nâng cấp v2 — 2026-11-09T00:12:21.765300+07:00 (UTC+7)

- Production READY: https://ict12-learning-platform.vercel.app
- Deployment: `dpl_FEy9AiRCdqQYjCHKdEQejoJZBKpy`; all 14 runtime files uploaded by SHA; existing encrypted environment inherited. No SSO approval needed this time.
- Six upgrade groups complete; additive migration applied to private ICT12 schema; credentials and prior data preserved.
- Local Playwright: 18 checks PASS, zero uncaught JS errors; grading all 45 exams, XLSX/openpyxl, security and actual late-submit/answer 403 verified.
- Production HTTPS E2E PASS: all 18 checks, zero uncaught JavaScript errors, mobile 390px, class assignments, true deadline 403, admin toggle, complete 23-step exam, remedial resume, XLSX download. Evidence: `tests/upgrade-production-e2e-results.json`.
- Production private-path/auth/CSRF checks PASS; downloaded workbook opens in openpyxl with both sheets. TEST account locked and test assignments disabled.
- Local reviewed runtime remains on http://localhost:3005 (older servers on 3000/3001 may retain v1 API in memory).

## Trạng thái trước triển khai (lịch sử) — 2026-11-09T09:17:53.191736+07:00 (UTC+7)

- State: READY_FOR_DEPLOYMENT; production still v2 until a new deployment is confirmed.
- Exact whitelist:16 runtime files, includes new curriculum module and private legacy v2 bank. `deploy-upload-request.json`; `release-audit/upload-manifest.json`. No credentials/env/backups/evidence in deployment.
- Local Playwright22 checks PASS, zero uncaught JS errors; full40-step THPT10/10; strict real deadline403 including simultaneous closure; classes/ownership/review privacy, XLSX,390px, offline/resync/session expiry/logout/home retry. Final smoke verifies legacy draft source and default TEST exclusion.
- Units all45 exams and365 TF partial-credit cases PASS; actual XLSX opened with openpyxl (one filtered score row +81 answer rows, formula-like name remains string). SQL/RPC wrong-secret and immutable deadline guards PASS; concurrent bucket admits exactly5 of12. Baseline passwords/accepted results unchanged. Original A-only site HTTP200 and untouched.
- Three additive migrations recorded in HANDOVER. Source/content/security/recovery details: `release-audit/CONTENT_AUDIT.md`, `release-audit/SECURITY_RECOVERY.md`. Semantic review140 TN +172 TF statements, not a claim of entire-bank teacher certification.
- Deployment must use same Vercel connector/team/project. If403, create a fresh `authorize_team_access` link, save `VERCEL_APPROVAL_LINK.txt`, return immediately. No CLI, temporary deployment, repository or new service fallback.

## Completion release — LIVE_VERIFIED · 2026-11-09T09:28:47.693855+07:00 (UTC+7)

- Live unchanged URL: https://ict12-learning-platform.vercel.app ; admin `/admin`.
- Final deployment `dpl_AY2mZsDyPat47XCDxG74JfYqTm5i`, READY at 2026-11-09T09:22:55.838000+07:00 (UTC+7), production alias confirmed, existing encrypted env inherited. No fresh SSO approval required.
- Final production Playwright:22 checks PASS, zero uncaught JS errors. `tests/readiness-production-results.json`; cleanup verified (TEST users locked, assignments disabled, teacher configuration restored). The final suite also checks historical scope titles cannot be relabeled by later teacher edits.
- Post-release smoke: legacy v2 drafts use original keys/wording, legacy accepted-result titles remain original, default statistics/export exclude TEST, all45 sets loaded, original A-only site HTTP200. `tests/readiness-production-final-smoke-results.json`.
- All4 live public assets match exact source hashes; CSP/frame/no-store/anonymous denial and no configured secret values in public files PASS. `tests/readiness-live-artifact-results.json`.
- Production .xlsx reopened in openpyxl:1 filtered result +81 answer-detail rows, formula-like identity remains string, score numeric, no formulas. `tests/readiness-excel-results.json`.
- Baseline original passwords and accepted result payloads unchanged; private RLS/privileges verified, no active unsnapshotted attempt. Original A-only project untouched.
- Final source manifest16 files; source archive `ict12-release-ready-source.zip` excludes env, credentials, private backups and student datasets. Private operator snapshot receipts remain box-only. Do not upload them.
- Honest limits: semantic audit140 MCQ +172 TF statements (not the entire bank); no large-load certification or destructive production DB restore drill; anti-cheat is browser deterrence only. See audit/runbook for precise scope and shared-project warning boundary.


## v2 upgrade (2026-11-11)
- Content: 790 new MC + 50 new Đ/S (lib/mcq-v3.json, lib/tf-v3.json; authoring in content-v3/, build with `python3 content-v3/build.py`, QA with `python3 content-v3/qa.py`).
- Lesson variants: Bài 1–13 → v2–v5 (5 sets each), Bài 14–28 → v2–v4 (4 sets each); 97 new lesson sets, ~15 TN + 2 Đ/S, pairwise overlap ≤4 questions.
- GK/CK: midterm-1, final-1, midterm-2, final-2 each have -v2..-v5 (5 sets per term). THPT 2025-format mocks: thpt-ict-01..10 (24 TN + 4 Đ/S). Total exams: 165.
- Questions and options are still shuffled per attempt server-side; 40 s/step and no going back are unchanged.
- Features: random mixed practice (topic/lesson/level), bookmarks + bookmark practice, retry-wrong, per-lesson mastery grid, lesson/exam search and filters, admin bulk import (tab "Nhập câu hỏi", closed by default, archive = soft-delete).
- UI: public/theme.css (design system + dark mode + mobile + reduced motion) and public/ui.js (overrides app.js renderers).
- Tests: tests/v2-unit.js (12/12), tests/v2-e2e.js (22/22 against local, preview and production; TEST_BASE / TEST_TAG env).
- Production deployment: dpl_DY7yywiT8qTEJBMYw1hPZo9HTYMW (preview dpl_5KfnkMSGLevXivgLLrmXZztJNEtA).
- Anti-cheat option lengths (2026-11-11 follow-up): all 790 new MC items now meet max/min option length <= 1.15 (was 438 failing); the key is the unique longest option in 13.2% of items (was 41.8%); 'pick the longest' scores 24.7% (was 50.0%) and 'pick the shortest' 22.1% (was 9.8%), near the 25% chance level. The strict 1.15 test in tests/unit.js again applies to every item, new ones included. Named-term items fixed: Win+P Extend/Duplicate (L22) and Google Forms question types (L27). Production deployment: dpl_CQdDRghEH4bUjsAzpEkpvbBEP5CY (previous v2: dpl_DY7yywiT8qTEJBMYw1hPZo9HTYMW).
