const crypto=require('crypto');
const clean=o=>{const x={...o};delete x._version;return x};
async function db(action,collection,id='',data={},version=null){
 let r;try{r=await fetch(process.env.SUPABASE_URL+'/rest/v1/rpc/ict12_access',{method:'POST',headers:{apikey:process.env.SUPABASE_KEY,'Content-Type':'application/json'},body:JSON.stringify({p_secret:process.env.DB_SECRET,p_action:action,p_collection:collection,p_id:id,p_data:clean(data),p_version:version}),signal:AbortSignal.timeout(20000)});}catch{const e=Error('Không kết nối được cơ sở dữ liệu. Vui lòng tải lại để kiểm tra trạng thái.');e.status=503;throw e;}
 const x=await r.json();if(!r.ok){console.error('ICT12 database error code:',String(x.code||r.status).slice(0,30));const e=Error(['40001','PT409'].includes(x.code)?'Dữ liệu vừa được cập nhật, hãy thử lại.':['42501','P0001'].includes(x.code)?x.message:'Không thể lưu dữ liệu. Vui lòng thử lại.');e.conflict=['40001','PT409'].includes(x.code);if(x.code==='42501')e.status=403;else if(r.status>=500&&!e.conflict)e.status=503;throw e;}return x;
}
const hash=s=>crypto.createHash('sha256').update(s).digest('hex');
function password(p){const salt=crypto.randomBytes(16).toString('hex');return salt+':'+crypto.scryptSync(p,salt,64).toString('hex')}
function verify(p,h){try{const [salt,key]=h.split(':');return crypto.timingSafeEqual(crypto.scryptSync(p,salt,64),Buffer.from(key,'hex'))}catch{return false}}
module.exports={db,hash,password,verify,clean};
