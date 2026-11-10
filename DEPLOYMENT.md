# Production deployment

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
