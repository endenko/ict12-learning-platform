// Seeds the global (admin) video list of each lesson from content-v4/videos/seed.json.
// Re-verifies every video with oEmbed right before writing; never overwrites a list an admin already edited.
// Usage: node --env-file=.env scripts/seed-videos.js
const {db}=require('../lib/db'),L=require('../lib/learn'),seed=require('../content-v4/videos/seed.json');
(async()=>{const out={at:new Date().toISOString(),seeded:{},skipped:[],rejected:[]};
 for(const [n,items] of Object.entries(seed.lessons)){const id='g:'+n,cur=await db('get','videos',id);if(cur&&cur.updatedBy&&cur.updatedBy!=='seed'){out.skipped.push(+n);continue}
  const ok=[];for(const it of items){try{ok.push(await L.verifyVideo({provider:'youtube',id:it.id}))}catch(e){out.rejected.push({lesson:+n,id:it.id,reason:e.message})}}
  await db('put','videos',id,{id,lesson:+n,ownerId:L.GLOBAL,items:ok,updatedAt:new Date().toISOString(),updatedBy:'seed'},cur?cur._version:null);out.seeded[n]=ok.length}
 require('fs').writeFileSync(__dirname+'/../content-v4/videos/seed-result.json',JSON.stringify(out,null,1));
 console.log('lessons seeded',Object.keys(out.seeded).length,'videos',Object.values(out.seeded).reduce((a,b)=>a+b,0),'without video',Object.entries(out.seeded).filter(([,v])=>!v).map(([k])=>k),'rejected',out.rejected.length,'skipped',out.skipped.length)})().catch(e=>{console.error(e.message);process.exit(1)});
