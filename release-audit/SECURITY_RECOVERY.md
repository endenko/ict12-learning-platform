# Security, scheduling and recovery — 09/11/2026 (UTC+7)

## Enforced boundaries

- Grading, content snapshots, true keys, rationales and shuffle orders remain server-only. Public bundle contains UI only. Current question is an allow-listed projection, never `customExam`/`steps`/raw documents.
- Authenticated student can read only their attempt. Admin endpoints require current server-side role. Locked/version-changed accounts lose existing sessions immediately. Passwords remain salted scrypt hashes; existing administrator password was verified, never reset/printed.
- Cookie: random256-bit token, HttpOnly, SameSite=Strict, 12h; Secure in production. Database stores token hash, not token. Role, lock, session version and finite expiry are checked per request. No public self-signup or reset endpoint.
- Exact Origin and Sec-Fetch-Site CSRF checks; JSON-only POST, bounded body, typed action/data/answer validation. No blind retries of writes; duplicate index/CAS conflicts do not answer two questions.
- No student review/analysis rationales while **any** own active attempt exists. Review privacy follows live source settings, including older remedial attempts. Practice requires every origin to remain open/review-enabled; new practice snapshots carry per-question provenance so a custom scope does not break history or authorize through an unrelated source.
- Leaderboard is opt-in/admin controlled, authenticated only, excludes locked/TEST/remedial; student view uses server-HMAC pseudonyms and no names/classes/account IDs. It is pseudonymization, not a guarantee nobody can infer a classmate from scores. Teachers see identity for legitimate review.
- XLSX text is OOXML `inlineStr`, never formula nodes; numeric scores numeric. CSV prefixes formula-like strings even after whitespace/control prefix. Teacher-only detailed exports contain personal learning data and must be handled as school records.
- Fixed persistent atomic rate buckets: login IP300/15min, account30/15min plus legacy eight-failure account/IP block; authenticated180/min; heavy analytics/export20/min. Concurrent admission test passed. These are application safeguards, not DDoS/identity guarantees. Rate rows are small but not automatically purged; operators should monitor DB growth before broad rollout.

## Database verification / shared-project boundary

`ict12_private.config` and `.documents`: RLS enabled, no policies (intentional fail-closed), no anon/authenticated table grants. Private SECURITY DEFINER access function has empty search_path and verifies the high-entropy server-held shared secret **before every action**. Public wrapper is SECURITY INVOKER with empty search_path. Anonymous execute permission is intentional to support the existing server RPC adapter; knowledge of the public API key alone does not authorize it. Keys/secrets are never shipped to browsers. Trigger function is not executable by public/anon/authenticated.

Additive migrations applied through Supabase connector:
1. `ict12_release_atomic_limits_assignment_guards` (`migration.sql`): atomic rate action; assignment existence/class/open/close/snapshot validation.
2. `ict12_assignment_snapshot_defense` (`deadline-defense.sql`): immutable schedule even if assignmentId were removed, generic close cap, member lock check.

3. `ict12_cas_conflict_http_status` (`conflict-status.sql`): application version conflicts use PT409 instead of retryable serialization SQLSTATE40001; driver recognizes both. Five concurrent-answer races then returned exactly one200/one409 each. Concurrent deadline reconciliation refetches derived state, so late writes converge to403/closed rather than spurious409.

No rows/passwords/results were rewritten/deleted by migrations. Supabase security advisor reported intentional RLS-no-policy INFO for these private tables. It also reported **existing shared `public` schema/Auth warnings unrelated to this standalone app**; left untouched to preserve the original A-only/other site. Do not claim the whole shared project has no warnings. Advisor explanations: https://supabase.com/docs/guides/database/database-linter and https://supabase.com/docs/guides/auth/password-security .

## Strict assignment policy (shown before start and while taking)

1. User must be in the assigned class; no free-start bypass for an enabled assignment of that exam. Future open and expired close are rejected server-side. The DB independently validates insertion, membership and schedule, not just UI.
2. Schedule is snapshotted at start. Disabling an exam prevents new starts of that exam. Disabling an assignment prevents new starts under that assignment; if the base exam remains open, free practice is available again. An already-started eligible attempt retains its announced deadline. There is no mutable assignment-edit API: disable/create replacement for a new schedule.
3. Answer and final-submit writes must pass server and DB checks **before close**, with no grace. Last question can finish the attempt automatically if received in time. A request queued/network-delayed into closure can be rejected; aim to submit early, not at the last second.
4. Once close has arrived, an unfinished attempt becomes `closed`, **not submitted**, no accepted score. Previously received choices are retained as a teacher-only draft. Student gets no draft keys/rationale. Moving out of the assigned class or locking the member also closes the old assigned attempt.
5. Per-question40s expiry and strict assignment close are different. Browser disconnect does not pause either. Unfinished records reconcile on the next student/admin request, not a scheduled background job. No claim that closing time automatically grants a score.

## Recoverability and operator runbook

- Student: server persists acknowledged answers. Unconfirmed local selections are not promised saved. Network failure is visible; `Lấy lại câu hiện tại` resyncs server state without pausing time. A failed write must be checked before retry. Expired/locked session returns to login, retaining server records. Home load has an explicit retry screen.
- Teacher: exports are filtered by historical class/exam, detailed XLSX optional; JSON teaching-plan download preserves configuration. Closed assignments have teacher-only draft viewing for disputes, not silently accepted scores or retroactive deadline overrides.
- Operator snapshot utility (not deployed/public):
  - `node --env-file=.env scripts/backup.js`
  - `node scripts/backup.js --verify /absolute/path/to/snapshot.json`
  - Outputs only path/counts/checksum verdict, never data, password hashes or env values. Private directory0700/file0600 under `private-backups/`; excludes sessions/rate and server secrets. Includes users' password hashes and personal records: **never put in source archive, public/, Git, export, or message attachment**.
  - Collections read sequentially; snapshot is checksum-validated, **not transaction-consistent**. Take during a quiet maintenance window for best consistency. A private verified snapshot exists; see box-only `backup-receipt.json` for location, not contents.
- Restore is an operator maintenance action, not a student/admin API. Do not overwrite production to “test recovery”. Validate backup/project/checksum, preserve a fresh pre-restore snapshot, and restore only the lost records after comparing current versions. Existing accepted assignment history may need DB-owner maintenance import because live insertion triggers correctly reject after-close submissions; do not disable guards in a public RPC. Restore role/version/hash/result documents as historical records, then revoke old sessions; never recalculate old scores. Reapply missing additive schema objects from schema/migration files, keep deployment env intact and run smoke tests before reopening. **No destructive PostgreSQL restore drill was performed against production.** A local serialization/restore round-trip is supplementary evidence, not that claim.
- Vercel rollback: redeploy last known-good manifest using connector; leave additive schema in place. Do not roll back/replace the database or reset passwords. Keep full question snapshots for already-started attempts and historical submitted results.
- Source release archives use an explicit safe whitelist, never whole-directory archives. No new paid backup service/PITR, messages, or storage sharing was created.

## Honest operating limits

School-sized JSONB storage/analytics are unpaginated and not load-certified. Detailed export is capped3MB, filter class/exam if too large. Repeated full question snapshots consume space; monitor project quota and keep operator backups before large enrollment. Browser anti-cheat is only detection/deterrence, not screenshot, device, extension, AI, or camera control; no intrusive permission requests. Teacher judgement is required for focus-event disputes and content review before consequential tests.

Existing shared-project advisor references (outside this app; not changed): [anonymous GraphQL discovery](https://supabase.com/docs/guides/database/database-linter?lint=0026_pg_graphql_anon_table_exposed), [signed-in GraphQL discovery](https://supabase.com/docs/guides/database/database-linter?lint=0027_pg_graphql_authenticated_table_exposed), [public definer function execution](https://supabase.com/docs/guides/database/database-linter?lint=0028_anon_security_definer_function_executable), [Auth password protection](https://supabase.com/docs/guides/auth/password-security#password-strength-and-leaked-password-protection). Private intentional fail-closed INFO: [RLS enabled without policies](https://supabase.com/docs/guides/database/database-linter?lint=0008_rls_enabled_no_policy).
