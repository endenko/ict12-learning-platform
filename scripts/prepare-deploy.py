#!/usr/bin/env python3
import json,hashlib,base64
from pathlib import Path
root=Path(__file__).resolve().parents[1]
files=['package.json','vercel.json','public/index.html','public/app.js','public/base.css','public/style.css','api/index.js','lib/db.js','lib/engine.js','lib/exams.json','lib/lessons.json','lib/features.js','lib/xlsx.js','server.js','lib/curriculum.js','lib/legacy-exams-v2.json']
u=root/'release-audit/uploads';u.mkdir(exist_ok=True);manifest=[];upload=[]
for i,f in enumerate(files):
 b=(root/f).read_bytes();sha=hashlib.sha1(b).hexdigest();manifest.append({'file':f,'sha':sha,'size':len(b)});base=u/f'{i}.base64';base.write_text(base64.b64encode(b).decode());upload.append({'file':f,'sha':sha,'size':len(b),'base64Path':str(base.resolve())})
req={'teamId':'team_blt8sqvJQ9ixAqMCP9WBUGga','forceNew':'1','requestBody':{'name':'ict12-learning-platform','project':'ict12-learning-platform','target':'production','files':manifest,'projectSettings':{'framework':None,'outputDirectory':'public','nodeVersion':'24.x'}}}
(root/'deploy-upload-request.json').write_text(json.dumps(req,indent=2));(root/'release-audit/upload-manifest.json').write_text(json.dumps(upload,indent=2))
print('Frozen deployment manifest:',len(files),'explicit runtime files; no env, credentials, backups, tests or documents included')
