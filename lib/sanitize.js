'use strict';
// Strict allowlist HTML sanitizer for teacher-entered rich text. Output contains only the tags below,
// no attributes except a sanitized href on <a> (http/https/mailto), and escaped text everywhere else.
const ALLOWED=new Set(['p','br','b','strong','i','em','u','s','ul','ol','li','h3','h4','blockquote','code','pre','a','hr','sub','sup','mark']);
const VOID=new Set(['br','hr']);
const DROP_CONTENT=new Set(['script','style','iframe','object','embed','svg','math','template','noscript','textarea','title','xmp','noembed','noframes','select','option','head','frameset','frame','plaintext','canvas','audio','video','form','button','input','link','meta','base']);
const ENTITY=/^&(#\d{1,7}|#x[0-9a-f]{1,6}|[a-z][a-z0-9]{1,31});/i;
function escText(s){let out='';for(let i=0;i<s.length;i++){const c=s[i];if(c==='&'){const m=s.slice(i).match(ENTITY);if(m){out+=m[0];i+=m[0].length-1;continue}out+='&amp;'}else if(c==='<')out+='&lt;';else if(c==='>')out+='&gt;';else if(c==='"')out+='&quot;';else out+=c}return out}
const escAttr=v=>String(v).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
function decodeAttr(v){return v.replace(/&#x([0-9a-f]+);?/gi,(_,h)=>String.fromCodePoint(parseInt(h,16)||0)).replace(/&#(\d+);?/g,(_,d)=>String.fromCodePoint(+d||0)).replace(/&colon;/gi,':').replace(/&tab;|&newline;/gi,'').replace(/&amp;/gi,'&')}
function safeUrl(raw){const v=decodeAttr(String(raw||'')).replace(/[\u0000-\u0020\u007f-\u009f]/g,'').trim();if(!v||v.length>500)return null;if(/^https?:\/\//i.test(v)||/^mailto:[^\s<>"]+@[^\s<>"]+$/i.test(v)){try{const u=new URL(v);if(!['http:','https:','mailto:'].includes(u.protocol))return null;return u.href}catch{return null}}return null}
function attrHref(attrs){const m=attrs.match(/(?:^|\s)href\s*=\s*("([^"]*)"|'([^']*)'|([^\s"'=<>`]+))/i);return m?safeUrl(m[2]??m[3]??m[4]):null}
function sanitizeHtml(input,max=20000){
 const s=String(input||'').slice(0,max*2).replace(/\u0000/g,'');const out=[],stack=[];let i=0;
 while(i<s.length){
  const lt=s.indexOf('<',i);if(lt<0){out.push(escText(s.slice(i)));break}
  if(lt>i)out.push(escText(s.slice(i,lt)));
  if(s.startsWith('<!--',lt)){const e=s.indexOf('-->',lt+4);i=e<0?s.length:e+3;continue}
  const m=s.slice(lt).match(/^<(\/?)([a-zA-Z][a-zA-Z0-9-]*)((?:\s+[^\s"'>\/=]+(?:\s*=\s*(?:"[^"]*"|'[^']*'|[^\s"'=<>`]+))?)*)\s*\/?>/);
  if(!m){out.push('&lt;');i=lt+1;continue}
  const [whole,close,rawName,attrs]=m,name=rawName.toLowerCase();i=lt+whole.length;
  if(DROP_CONTENT.has(name)){if(!close&&!VOID.has(name)){const re=new RegExp('</'+name+'\\s*>','i'),rest=s.slice(i),e=rest.search(re);i=e<0?s.length:i+e+rest.slice(e).match(re)[0].length}continue}
  if(!ALLOWED.has(name))continue;
  if(close){const k=stack.lastIndexOf(name);if(k<0)continue;while(stack.length>k)out.push('</'+stack.pop()+'>');continue}
  if(VOID.has(name)){out.push('<'+name+'>');continue}
  if(stack.length>=20)continue;
  if(name==='a'){const href=attrHref(attrs);out.push(href?`<a href="${escAttr(href)}" target="_blank" rel="noopener noreferrer nofollow">`:'<a>')}
  else out.push('<'+name+'>');
  stack.push(name)}
 while(stack.length)out.push('</'+stack.pop()+'>');
 let html=out.join('');if(html.length>max)html=sanitizeHtml(html.slice(0,max),max+1000);return html}
function textOf(html){return String(html||'').replace(/<[^>]*>/g,' ').replace(/&nbsp;/g,' ').replace(/\s+/g,' ').trim()}
module.exports={sanitizeHtml,safeUrl,textOf};
