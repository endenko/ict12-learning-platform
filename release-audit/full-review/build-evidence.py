"""Compile authored per-item notes into a hash-bound auditable ledger; never generates semantic verdicts from keywords."""
import json,hashlib,re,datetime
from pathlib import Path
r=Path(__file__).resolve().parents[2];d=Path(__file__).resolve().parent
notes={}
for p in sorted(d.glob('notes-*.tsv')):
 for line in p.read_text().splitlines():
  id,note=line.split('\t',1);assert id not in notes;notes[id]=(note,p.name)
remaining=json.loads((d/'remaining.json').read_text());corrections=json.loads((d/'corrections.json').read_text());patch={p['id']:p for p in corrections}
current={k:{q['id']:q for q in json.loads((r/f'lib/{k}.json').read_text())} for k in ['mcq','tf']}
# Exact pages only where read directly; other entries honestly retain chapter/section page ranges.
exact={'q2':'5–6','q3':'6','q4':'6','q5':'6','q11':'6','q13':'7–8','q32':'14–15','q33':'15','q47':'21','q49':'22','q50':'23','q51':'23–24','q52':'24','q53':'25','q54':'24','q57':'23–24','q58':'23–24','ext-l16-q06':'89','ext-l17-q05':'99','ext-l17-q06':'99','ext-l27-q03':'148','ext-l28-q05':'152–153'}
source_catalog={
'dartmouth1956':{'url':'https://home.dartmouth.edu/about/artificial-intelligence-ai-coined-dartmouth','finding':'1956 seminal research-field workshop; official Dartmouth history'},
'proposal1955':{'url':'http://www-formal.stanford.edu/jmc/history/dartmouth/dartmouth.html','finding':'Primary proposal dated August31,1955, explicitly uses artificial intelligence and plans summer1956'},
'cisco-switch':{'url':'https://www.cisco.com/c/en/us/support/docs/switches/catalyst-6000-series-switches/23563-143.html','finding':'Known MAC/VLAN forwarding versus unknown-unicast flooding'},
'cisco-crc':{'url':'https://www.cisco.com/c/en/us/support/docs/ios-nx-os-software/nx-os-software/217554-understand-cyclic-redundancy-check-crc.html','finding':'FCS/CRC detects corruption; store-and-forward can drop corrupt frames; cut-through nuances distinguished'},
'rfc9293':{'url':'https://www.rfc-editor.org/rfc/rfc9293.html','section':'2.2,3.1,3.4,3.8.1','finding':'Reliable in-order byte stream; ports; byte sequence numbers; retransmission'},
'rfc1812':{'url':'https://www.rfc-editor.org/rfc/rfc1812.html','section':'2.2.3,2.2.5,5.2.4','finding':'Destination/forwarding table next-hop and longest-prefix/default route behavior; IP no universal delivery guarantee'},
'microsoft-sharing':{'url':'https://support.microsoft.com/en-us/windows/file-sharing-over-a-network-in-windows-b58704b2-f53a-4b82-7bc1-80f9994725bf','finding':'Official Windows local sharing, Specific people, discovery; Windows10/11 versions distinguished'},
'mdn-strong':{'url':'https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/strong','finding':'Importance versus stress emphasis and default bold presentation'},
'mdn-video':{'url':'https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/video','finding':'Video may carry audio-only content; controls/poster/sources/autoplay'},
'mdn-url':{'url':'https://developer.mozilla.org/en-US/docs/Learn_web_development/Howto/Web_mechanics/What_is_a_URL','finding':'Relative resolution, fragments and absolute URLs; hosts not universal for all schemes'},
'mdn-table':{'url':'https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/td','finding':'colspan and rowspan grid extents'},
'mdn-display':{'url':'https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/display','finding':'Inner/outer display; table has block-level outer box but table inner layout'},
'mdn-specificity':{'url':'https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cascade/Specificity','finding':'Compare specificity only within prevailing origin/layer; source order later in cascade'},
'mdn-line-height':{'url':'https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/line-height','finding':'Line-box size, not an unconditional universal baseline distance'},
'mdn-font-style':{'url':'https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/font-style','finding':'Italic directly requests the italic face; inherit is conditional on parent'},
'mdn-inheritance':{'url':'https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cascade/Inheritance','finding':'Inherited values come from parent computed values'},
'google-sites-style':{'url':'https://support.google.com/sites/answer/6372865?hl=en','finding':'Themes/colors/fonts; top/side navigation'},
'google-sites-pages':{'url':'https://support.google.com/sites/answer/98216?hl=en','finding':'Page tree, new page, header image and footer'},
'google-sites-content':{'url':'https://support.google.com/sites/answer/90538?hl=en','finding':'Content blocks; Brand Images/logo/favicon'},
'google-sites-publish':{'url':'https://support.google.com/sites/answer/6372880','finding':'Preview/publish/published-viewer permissions are separate operations'},
'google-forms-publish':{'url':'https://support.google.com/docs/answer/2839588?hl=en','finding':'Current Forms must be published with responder permissions separately from Sites'},
'google-forms-responses':{'url':'https://support.google.com/docs/answer/139706?hl=en','finding':'Responses Summary/Individual, Sheets link, response collection and sign-in'},
'google-forms-sheets':{'url':'https://support.google.com/docs/answer/2917686?hl=en','finding':'Linked Sheets receive response data; permissions managed separately'},
'google-forms-updates':{'url':'https://support.google.com/docs/answer/16319311?hl=en','finding':'Granular responder-access changes; older forms upgraded by Dec2025'},
}
(d/'sources.json').write_text(json.dumps(source_catalog,ensure_ascii=False,indent=2)+'\n')
def refs(q):
 id=q['id'];l=q['lesson'];out=[]
 if id=='q2':out+=['dartmouth1956','proposal1955']
 if id=='q32':out+=['cisco-switch']
 if id=='q49':out+=['cisco-crc','rfc9293']
 if id in ['q50','q51','q57','q58']:out+=['rfc1812']
 if id in ['q52','q54','q56']:out+=['rfc9293']
 if l==5:out+=['microsoft-sharing']
 if l==8:out+=['mdn-strong']
 if l==9:out+=['mdn-table']
 if l==10:out+=['mdn-url']
 if l==11:out+=['mdn-video']
 if l==14:out+=['mdn-font-style','mdn-line-height','mdn-inheritance','mdn-specificity']
 if l==16:out+=['mdn-display']
 if l==17:out+=['mdn-specificity']
 if l in [23,24,25,26,28]:out+=['google-sites-content','google-sites-pages','google-sites-style','google-sites-publish']
 if l==27:out+=['google-forms-publish','google-forms-responses','google-forms-sheets','google-forms-updates']
 return out
hashof=lambda o:hashlib.sha256(json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
ledger=[]
for kind in ['mcq','tf']:
 for q in remaining[kind]:
  ids=[(q['id'],None)] if kind=='mcq' else [(q['id']+'.'+s['label'],i) for i,s in enumerate(q['statements'])]
  for id,idx in ids:
   assert id in notes,id
   now=current[kind][q['id']];note,nfile=notes[id]
   before=q if idx is None else {'scenario':q['scenario'],'statement':q['statements'][idx]}
   after=now if idx is None else {'scenario':now['scenario'],'statement':now['statements'][idx]}
   changed=before!=after
   ledger.append({'id':id,'kind':'mcq' if idx is None else 'tf-statement','round':'remaining-semantic-completion','review':'internal semantic reading of full question/options or scenario/statement, key and rationale','bookReference':q['review'],'printedPagesDirectlyVerified':exact.get(q['id']),'referencePrecision':'specific printed page(s)' if q['id'] in exact else 'printed chapter/section range, not a claimed line-exact citation','sourceIds':refs(q),'lesson':q['lesson'],'topic':q['topic'],'scope':'grade12 ICT textbook core or its worked application','pedagogicalLevel':q['level'] if idx is None else q['statements'][idx]['level'],'levelLimit':'author-assigned instructional category, not empirically calibrated difficulty','optionLengths':[len(o) for o in now['options']] if idx is None else None,'keyBefore':q['answer'] if idx is None else q['statements'][idx]['answer'],'keyAfter':now['answer'] if idx is None else now['statements'][idx]['answer'],'verdict':'corrected wording/rationale/context; key retained' if changed else 'retain after internal semantic review','semanticEvidence':note,'authoredNoteFile':nfile,'beforeSHA256':hashof(before),'afterSHA256':hashof(after),'currentContent':after})
assert len(ledger)==448 and len(notes)==448
assert len({x['id'] for x in ledger})==448
(d/'item-ledger.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger))
summary={'reviewedThisRound':{'mcq':328,'tfGroups':30,'tfStatements':120,'authoredPerItemNotes':448},'previousInternalReview':{'mcq':140,'tfGroups':43,'tfStatements':172},'cumulativeInternalReview':{'mcq':468,'tfGroups':73,'tfStatements':292,'independentExpertCertification':False},'corrections':{'questionOrGroupRecords':len(corrections),'mcq':sum(p['kind']=='mcq' for p in corrections),'tfGroupContextOrStatement':sum(p['kind']=='tf' for p in corrections),'changedKeys':0,'historicalResultsRegraded':0},'manualNotesNotAutoGeneratedFromKeywords':True,'ledger':'release-audit/full-review/item-ledger.jsonl','sourceCatalog':'release-audit/full-review/sources.json','unresolvedDemonstrablyWrongKeyInReviewedBank':[],'limitations':['Internal review only, not independent subject-expert certification','Some distractors are easy; NB/TH/VD not psychometrically calibrated','Textbook third-party UI may differ; current official Forms publishing behavior clarified','Source ranges not represented as exact-page proof where only chapter reference is available']}
(d/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:summary[k] for k in ['reviewedThisRound','cumulativeInternalReview','corrections']},ensure_ascii=False,indent=2))
