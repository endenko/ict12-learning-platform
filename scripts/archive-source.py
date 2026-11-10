#!/usr/bin/env python3
import json,zipfile,subprocess
from pathlib import Path
r=Path(__file__).resolve().parents[1]
files=[x['file'] for x in json.loads((r/'deploy-upload-request.json').read_text())['requestBody']['files']]
files+=['lib/mcq.json','lib/tf.json','README.md','HANDOVER.json','DEPLOYMENT.md','schema-base.sql','deploy-upload-request.json','scripts/prepare-deploy.py','scripts/archive-source.py','scripts/backup.js','upgrades/migration.sql','release-audit/migration.sql','release-audit/deadline-defense.sql','release-audit/conflict-status.sql','release-audit/CONTENT_AUDIT.md','release-audit/SECURITY_RECOVERY.md','release-audit/RELEASE_REPORT.md','release-audit/content-audit.json','release-audit/content-corrections.json','release-audit/correct-content.py','release-audit/selection.json','release-audit/mcq-v2.json','release-audit/tf-v2.json','release-audit/exams-v2.json']
files+=['tests/unit.js','tests/upgrade-unit.js']+[str(p.relative_to(r)) for p in (r/'tests').glob('readiness-*.js')]+['tests/readiness-semantics.py']
# Explicit content-completion evidence whitelist; NEVER glob private snapshot receipts.
full_review=['remaining.json','round1-mcq.json','round1-tf.json','round1-exams.json','round1-content-audit.json','corrections.json','define-corrections.py','apply-corrections.py','build-evidence.py','item-ledger.jsonl','sources.json','summary.json','integrity-baseline.json','deployment.json','followup-semantic-review.json','REVIEW_REPORT.md','REPRODUCE.md','ENGINEERING_CHECK.md']
full_review+=['notes-'+x+'.tsv' for x in ['1-4','5-8','9-12','13-16','17-20','21-24','25-28']]
full_review+=['lessons-'+x+'.txt' for x in ['1-4','5-8','9-12','13-16','17-20','21-24','25-28']]
files+=['release-audit/full-review/'+x for x in full_review]+['testing-tools/package.json']
files+=['tests/'+x for x in ['content-audit-unit.js','content-audit-browser.js','content-live-audit.js','content-preservation.js','content-audit-unit-results.json','content-audit-browser-results.json','content-regression-unit-results.json','content-regression-upgrade-results.json','content-preservation-results.json']]
for x in ['content-local-live-results.json','content-production-live-results.json','readiness-production-results.json','readiness-production-final-smoke-results.json','readiness-excel-results.json','readiness-live-artifact-results.json']:
 if (r/'tests'/x).exists():files+=['tests/'+x]
files+=['release-audit/review-mcq.txt','release-audit/review-tf.txt']
files+=['tests/'+x for x in ['content-excel.py','content-production-deadline-boundary-harness-failure.json','readiness-db-runtime-results.json','readiness-unit-results.json','readiness-semantics-results.json','readiness-browser-semantics-results.json','readiness-local-results.json','readiness-local-final-smoke-results.json','readiness-preservation-results.json']]
files+=['release-audit/source-archive-files.json']
files=sorted(set(files));(r/'release-audit/source-archive-files.json').write_text(json.dumps(files,indent=2))
scan="const fs=require('fs'),assert=require('assert');for(const f of JSON.parse(fs.readFileSync('release-audit/source-archive-files.json'))){const t=fs.readFileSync(f,'utf8');for(const k of ['SUPABASE_KEY','DB_SECRET','ICT12_ADMIN_NEW_PASSWORD'])if(process.env[k])assert(!t.includes(process.env[k]),'Sensitive value in source candidate');}console.log('Source archive candidates passed secret-value scan; no values printed');"
subprocess.run(['node','--env-file=.env','-e',scan],cwd=r,check=True)
with zipfile.ZipFile(r/'ict12-release-ready-source.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in files:
  assert not any(x in f for x in ['private-backups','CREDENTIALS','backup-receipt','.env','APPROVAL_LINK'])
  z.write(r/f,f)
print('Created safe-whitelist source archive with',len(files),'files; no private backups, credentials, env or student datasets')
