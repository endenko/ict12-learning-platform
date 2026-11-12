# Render fallback — prepared, not deployed

Vercel was retried once on 07/11/2026 and still returned HTTP 403 for team `endenkos-projects`. No new SSO link was generated.

## Exact blockers

1. Render MCP is available, but `create_web_service` accepts a Git repository source, not local files. Its prebuilt Docker image route is explicitly unsupported.
2. This session's `cursor-github` namespace does **not** expose create-repository, write-file or push-files tools. CloudAgent is also unavailable. No GitHub credentials were searched for, no lower-level API/CLI workaround was attempted, and no repository was created.
3. Render has no selected workspace. The connector explicitly requires the user to confirm a workspace before a write. The only listed candidate is **Learning, Improve myself**, ID `tea-dbkr6nei0phs73b32kb0`. It was not silently selected.

To proceed, obtain workspace confirmation and a PRIVATE GitHub repository containing the whitelisted source (or enable an authorized repository-writing/cloud-agent tool). Render's Git integration must be granted access to that repository.

## Reversible preparation completed

- `server.js`: production plain-HTTP Node adapter listening on `0.0.0.0:$PORT`, default 10000. HTTPS is terminated by Render. Preserves API auth, grading and Supabase data.
- Serves only explicitly whitelisted public assets; no question-bank, credentials or arbitrary filesystem access. Same CSP/security headers as Vercel. JSON body limit 200 kB, proper content types, health path `/healthz`, graceful shutdown.
- `npm start` now uses `node server.js`; `npm run dev` retains the prior local development server.
- Production startup requires SUPABASE_URL, SUPABASE_KEY and DB_SECRET; refuses LOCAL_DEV in NODE_ENV=production. No automatic .env reads in the production adapter. Cookies remain Secure in production.
- `ict12-render-source.zip` and `render-source-manifest.json`: secret-free whitelist for a PRIVATE repository. Do **not** upload this entire workspace. `.gitignore` excludes credentials, environment files, attachments and test artifacts.
- `render-create-request.pending.json`: free-plan Singapore Node service configuration. **Not submitted.** Missing `repo` and user-confirmed `workspaceId` intentionally. Secret values are file references to private box files, not source-code content.

## Intended hosting configuration

PRIVATE repo branch main; runtime node; free plan; Singapore; build `node --check server.js`; start `npm start`; optional HTTP health path `/healthz`. Env: NODE_ENV=production and the three existing Supabase variables. Do not set LOCAL_DEV in Render.

Existing Supabase remains the data store; no Render disk or database needed. Free Render web services can spin down when idle, causing cold starts. Public HTTPS/live URL and production browser testing cannot be verified until deployment is actually created and reaches live.

Credentials remain only at `/workspace/ict12-platform/ADMIN_CREDENTIALS.txt` (mode 600). Admin route `/admin`.
