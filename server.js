'use strict';
// Production adapter for Render. Credentials are supplied only via environment variables.
const http=require('node:http'),fs=require('node:fs'),path=require('node:path');
for(const name of ['SUPABASE_URL','SUPABASE_KEY','DB_SECRET'])if(!process.env[name])throw Error('Missing required environment variable: '+name);
if(process.env.NODE_ENV==='production'&&process.env.LOCAL_DEV)throw Error('LOCAL_DEV must not be enabled in production');
const handler=require('./api/index'),configuration=require('./vercel.json');
const securityHeaders=configuration.headers[0].headers;
const assets=new Map([['/','index.html'],['/admin','index.html'],['/admin/','index.html'],['/index.html','index.html'],['/app.js','app.js'],['/base.css','base.css'],['/style.css','style.css'],['/ui.js','ui.js'],['/theme.css','theme.css'],['/portal.js','portal.js'],['/portal.css','portal.css'],['/learn.js','learn.js'],['/learn.css','learn.css'],['/theory.json','theory.json']]);
const types={'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.json':'application/json; charset=utf-8'};
const server=http.createServer(async(req,res)=>{
 for(const h of securityHeaders)res.setHeader(h.key,h.value);
 res.status=s=>{res.statusCode=s;return res};res.json=x=>{res.setHeader('Content-Type','application/json; charset=utf-8');res.end(JSON.stringify(x))};
 try{
  const pathname=new URL(req.url,'http://localhost').pathname;
  if(pathname==='/healthz'){
   if(!['GET','HEAD'].includes(req.method))return res.status(405).json({error:'Method not allowed'});
   res.setHeader('Cache-Control','no-store');return req.method==='HEAD'?res.end():res.json({status:'ok'});
  }
  if(pathname==='/api'||pathname==='/api/index'){
   if(req.method==='POST'){
    if(!String(req.headers['content-type']||'').toLowerCase().startsWith('application/json'))return res.status(415).json({error:'Yêu cầu cần định dạng JSON.'});
    const chunks=[];let length=0;for await(const chunk of req){length+=chunk.length;if(length>200000)return res.status(413).json({error:'Yêu cầu quá lớn.'});chunks.push(chunk)}req.body=Buffer.concat(chunks).toString('utf8');
   }
   return await handler(req,res);
  }
  if(!['GET','HEAD'].includes(req.method))return res.status(405).json({error:'Method not allowed'});
  const asset=assets.get(pathname);if(!asset)return res.status(404).json({error:'Not found'});
  const bytes=await fs.promises.readFile(path.join(__dirname,'public',asset));res.setHeader('Content-Type',types[path.extname(asset)]);res.setHeader('Content-Length',bytes.length);res.setHeader('Cache-Control','no-cache');if(req.method==='HEAD')return res.end();res.end(bytes);
 }catch(error){console.error('ICT12 server request failed:',error.name);if(!res.headersSent)res.status(500).json({error:'Máy chủ gặp lỗi. Vui lòng thử lại.'});else res.destroy()}
});
server.requestTimeout=120000;server.headersTimeout=30000;
server.listen(Number(process.env.PORT)||10000,'0.0.0.0',()=>console.log('ICT12 server listening on configured PORT'));
for(const signal of ['SIGTERM','SIGINT'])process.on(signal,()=>{server.close(()=>process.exit(0));setTimeout(()=>process.exit(0),25000).unref()});
