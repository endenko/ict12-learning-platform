'use strict';
// Roster helpers: read .xlsx/.csv uploads (server-side, no dependencies), generate usernames and passwords.
const zlib=require('zlib'),crypto=require('crypto');
const fail=(m,s=400)=>{const e=Error(m);e.status=s;throw e};
function unzip(buf){const files={};let eocd=-1;for(let i=buf.length-22;i>=Math.max(0,buf.length-65557);i--)if(buf.readUInt32LE(i)===0x06054b50){eocd=i;break}if(eocd<0)fail('Tệp Excel không hợp lệ.');
 const count=buf.readUInt16LE(eocd+10);let p=buf.readUInt32LE(eocd+16);if(count>2000)fail('Tệp Excel quá phức tạp.');
 for(let n=0;n<count;n++){if(buf.readUInt32LE(p)!==0x02014b50)fail('Tệp Excel không hợp lệ.');const method=buf.readUInt16LE(p+10),csize=buf.readUInt32LE(p+20),usize=buf.readUInt32LE(p+24),nl=buf.readUInt16LE(p+28),el=buf.readUInt16LE(p+30),cl=buf.readUInt16LE(p+32),off=buf.readUInt32LE(p+42),name=buf.slice(p+46,p+46+nl).toString('utf8');p+=46+nl+el+cl;
  if(!/^xl\/(sharedStrings\.xml|workbook\.xml|worksheets\/sheet\d+\.xml)$/.test(name))continue;if(usize>8e6)fail('Tệp Excel quá lớn.');
  const lnl=buf.readUInt16LE(off+26),lel=buf.readUInt16LE(off+28),data=buf.slice(off+30+lnl+lel,off+30+lnl+lel+csize);
  files[name]=(method===0?data:method===8?zlib.inflateRawSync(data,{maxOutputLength:8e6}):fail('Nén Excel không hỗ trợ.')).toString('utf8')}return files}
const unxml=s=>s.replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&quot;/g,'"').replace(/&apos;/g,"'").replace(/&#(\d+);/g,(_,d)=>String.fromCodePoint(+d)).replace(/&#x([0-9a-f]+);/gi,(_,h)=>String.fromCodePoint(parseInt(h,16))).replace(/&amp;/g,'&');
function readXlsx(buf){const f=unzip(buf);const shared=[];if(f['xl/sharedStrings.xml'])for(const m of f['xl/sharedStrings.xml'].matchAll(/<si>([\s\S]*?)<\/si>/g))shared.push(unxml([...m[1].matchAll(/<t[^>]*>([\s\S]*?)<\/t>/g)].map(x=>x[1]).join('')));
 const sheetName=Object.keys(f).filter(n=>n.startsWith('xl/worksheets/')).sort()[0];if(!sheetName)fail('Không tìm thấy trang tính.');const rows=[];
 for(const rm of f[sheetName].matchAll(/<row[^>]*>([\s\S]*?)<\/row>/g)){const row=[];for(const cm of rm[1].matchAll(/<c([^>]*?)(?:\/>|>([\s\S]*?)<\/c>)/g)){const attrs=cm[1],body=cm[2]||'',ref=attrs.match(/r="([A-Z]+)\d+"/)?.[1];let col=row.length;if(ref){col=0;for(const ch of ref)col=col*26+ch.charCodeAt(0)-64;col--}const type=attrs.match(/t="([^"]+)"/)?.[1];let v='';
   if(type==='inlineStr')v=unxml([...body.matchAll(/<t[^>]*>([\s\S]*?)<\/t>/g)].map(x=>x[1]).join(''));else{const raw=body.match(/<v>([\s\S]*?)<\/v>/)?.[1];v=raw==null?'':type==='s'?shared[+raw]??'':unxml(raw)}row[col]=String(v).trim()}rows.push(Array.from(row,x=>x??''));if(rows.length>2000)break}return rows}
function parseCSV(text){const rows=[];let row=[],cell='',q=false;const s=String(text).replace(/^\uFEFF/,'');const sep=(s.split('\n')[0].match(/\t/g)||[]).length>(s.split('\n')[0].match(/;/g)||[]).length?'\t':(s.split('\n')[0].match(/;/g)||[]).length>(s.split('\n')[0].match(/,/g)||[]).length?';':',';
 for(let i=0;i<s.length;i++){const ch=s[i];if(q){if(ch==='"'&&s[i+1]==='"'){cell+='"';i++}else if(ch==='"')q=false;else cell+=ch}else if(ch==='"')q=true;else if(ch===sep){row.push(cell.trim());cell=''}else if(ch==='\n'||ch==='\r'){if(ch==='\r'&&s[i+1]==='\n')i++;row.push(cell.trim());if(row.some(Boolean))rows.push(row);row=[];cell=''}else cell+=ch}row.push(cell.trim());if(row.some(Boolean))rows.push(row);return rows}
const strip=s=>String(s||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/đ/g,'d').replace(/Đ/g,'D');
const slug=s=>strip(s).toLowerCase().replace(/[^a-z0-9]+/g,'');
// Rows → [{name, username?}]. Header detection: "họ tên"/"name", "tài khoản"/"username". Otherwise column 1 = name (or STT, name).
function rosterRows(table){if(!table.length)return[];const head=table[0].map(h=>slug(h));const nameCol=head.findIndex(h=>/^(hoten|hovaten|ten|name|fullname|hotenhocsinh)$/.test(h)),userCol=head.findIndex(h=>/^(taikhoan|tendangnhap|username|user|login)$/.test(h));let body=table,nc=0,uc=-1;
 if(nameCol>=0){body=table.slice(1);nc=nameCol;uc=userCol}else if(table.length&&/^\d+$/.test(table[0][0]||'')&&table[0][1])nc=1;
 return body.map(r=>({name:String(r[nc]||'').replace(/\s+/g,' ').trim().slice(0,100),username:uc>=0?String(r[uc]||'').trim().toLowerCase():''})).filter(r=>r.name&&!/^(stt|họ tên|ho ten)$/i.test(r.name))}
function parseUpload({base64,text,filename}){let table;if(base64){if(typeof base64!=='string'||base64.length>190000)fail('Tệp quá lớn (tối đa khoảng 140 KB).');const buf=Buffer.from(base64,'base64');if(buf.slice(0,2).toString()==='PK')table=readXlsx(buf);else table=parseCSV(buf.toString('utf8'))}else table=parseCSV(String(text||''));const rows=rosterRows(table);if(!rows.length)fail('Không đọc được danh sách. Cần cột “Họ tên” (và tùy chọn “Tài khoản”).');if(rows.length>200)fail('Tối đa 200 học sinh mỗi lần.');return rows}
const ALPHA='abcdefghjkmnpqrstuvwxyz23456789';
function newPassword(n=10){let s='';for(let i=0;i<n;i++)s+=ALPHA[crypto.randomInt(ALPHA.length)];return s.slice(0,4)+'-'+s.slice(4)}
function usernameFor(name,className,taken){const parts=strip(name).toLowerCase().replace(/[^a-z\s]/g,' ').trim().split(/\s+/).filter(Boolean);const base=((parts.at(-1)||'hs')+(parts.slice(0,-1).map(p=>p[0]).join(''))).slice(0,16)+'.'+(slug(className).slice(0,8)||'hs');let u=base,i=1;while(taken.has(u)||u.length<3){i++;u=base+i}taken.add(u);return u}
module.exports={readXlsx,parseCSV,rosterRows,parseUpload,newPassword,usernameFor,slug,strip};
