// Locks any unlocked TEST student accounts and archives (disables) TEST classes on the target deployment. Non-destructive.
const {chromium}=require('../testing-tools/node_modules/playwright'),fs=require('fs');const base=process.env.TEST_BASE||'https://ict12-learning-platform.vercel.app';
(async()=>{const b=await chromium.launch({executablePath:'/opt/google/chrome/chrome'}),p=await (await b.newContext()).newPage();
const call=async(action,data={})=>{const r=await p.request.post(base+'/api',{data:{action,data},headers:{origin:base}});const x=await r.json().catch(()=>({}));if(r.status()!==200)throw new Error(action+' '+r.status()+' '+JSON.stringify(x).slice(0,200));return x};
await p.goto(base+'/admin');await p.locator('#username').fill('admin');await p.locator('#password').fill(process.env.ICT12_ADMIN_NEW_PASSWORD);await p.locator('#login-form button').click();await p.locator('[data-tab]').first().waitFor({timeout:40000});
const d=await call('portalData');const out={base,at:new Date().toISOString(),lockedStudents:[],archivedClasses:[]};
for(const s of (d.students||[]).filter(s=>!s.locked&&(/^test/i.test(s.id)||/^TEST/.test(s.className||'')))){await call('studentLock',{id:s.id,locked:true});out.lockedStudents.push(s.id)}
for(const c of (d.classes||[]).filter(c=>!c.disabled&&/^TEST/.test(c.name))){await call('classArchive',{id:c.id,archived:true});out.archivedClasses.push(c.name)}
fs.writeFileSync(__dirname+'/v3-cleanup-results.json',JSON.stringify(out,null,1));console.log('locked',out.lockedStudents.length,'archived',out.archivedClasses.length);await b.close()})().catch(e=>{console.error(e.message);process.exit(1)});
