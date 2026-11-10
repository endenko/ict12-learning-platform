import json,os
changes={
'q40':{'explanation':'Switch học địa chỉ MAC và thường chuyển khung unicast tới cổng đích đã biết, giảm xung đột so với hub; khung quảng bá hoặc đích chưa biết vẫn có thể được phát tràn.'},
'ext-l17-q01':{'options_replace':{'Con trỏ đang di chuyển trên liên kết.':'Con trỏ đang được đặt trên liên kết.'}},
'ext-l18-q01':{'question':'Theo mô hình website nhiều trang ở Bài 18, website có đặc điểm nào?'},
'ext-l19-q14':{'explanation':'Cần kiểm tra quạt và tản nhiệt. Trước khi mở máy phải tắt nguồn, ngắt điện và tuân thủ quy trình an toàn; không tự sửa nếu chưa đủ kĩ năng.'},
'ext-l7-t1':{'scenario_replace':{'head chứa title="CLB"':'head chứa <title>CLB</title>'}},
'ext-found-t2':{'scenario_append':' Các trường mã đều không nhận giá trị rỗng.'},
'ext-found-t3':{'statements':{'a':{'text_replace':{'TênKH':'TenKH'}}}},
}
variation={
't1':('b',True,'Gợi ý sách theo lịch sử mượn vẫn là nhiệm vụ hẹp, chưa chứng minh trí tuệ tổng quát.','Gợi ý cá nhân hóa là một nhiệm vụ hẹp; chưa đủ chứng minh mọi năng lực như người.'),
't4':('a',False,'Dự đoán nhu cầu nước từ môi trường chỉ là sao chép nguyên tệp dữ liệu.','Dự đoán rút ra kết quả từ dữ liệu môi trường; không chỉ sao chép tệp.'),
't7':('d',True,'Để nối LAN ra mạng ngoài, trường cần chức năng định tuyến của router phù hợp.','Router thực hiện định tuyến giữa các mạng; modem hay WAP không tự thay thế chức năng này.'),
't10':('a',False,'Địa chỉ IP tự dùng cổng ứng dụng để bảo đảm mọi gói tải tệp không bị mất.','IP không bảo đảm truyền đủ gói; TCP dùng cổng ở tầng giao vận để phân phối dữ liệu cho ứng dụng.'),
'ext-l7-t1':('b',True,'Để tạo đoạn mới, nhóm nên thêm phần tử p trong body.','Mỗi phần tử p trong body biểu diễn một đoạn văn.'),
'ext-l9-t1':('c',False,'Muốn ô đầu trải qua hai hàng, Bình nên đặt colspan="2".','colspan gộp cột; muốn trải qua hai hàng phải dùng rowspan="2".'),
'ext-l12-t1':('a',True,'Checkbox cho phép chọn nhiều sở thích độc lập trong nhóm.','Checkbox là các lựa chọn độc lập; không tự loại trừ như radio cùng name.'),
'ext-l14-t1':('b',False,'Cỡ chữ p vẫn bằng đúng 20px dù nhóm đã đặt font-size:1.5em.','Trong ngữ cảnh đã cho, 1.5em = 1.5 × 20px = 30px.'),
'ext-l17-t1':('d',True,'Khi các khai báo đều thường, #intro thắng bộ chọn p.note.','Cùng nguồn tác giả và cùng mức thường, bộ chọn ID có độ đặc hiệu cao hơn p.note.'),
'ext-l22-t1':('c',False,'HDMI trong ví dụ chỉ truyền hình, không thể mang âm thanh số.','HDMI thông thường có thể truyền cả hình ảnh và âm thanh số.'),
'ext-l24-t1':('c',True,'Muốn lớp xem bản công bố, An cần xuất bản và kiểm tra quyền người xem.','Xuất bản và cấp quyền xem phù hợp là hai bước cần kiểm tra.'),
'ext-l27-t1':('b',False,'Câu hỏi chọn một mức tự động ghi nhận mọi mức hài lòng cùng lúc.','Câu hỏi một lựa chọn chỉ ghi nhận một mức mỗi phản hồi.'),
}
for qid,(label,answer,text,why) in variation.items():changes.setdefault(qid,{}).setdefault('statements',{}).setdefault(label,{}).update(text=text,answer=answer,explanation=why)
changes.setdefault('t10',{}).setdefault('statements',{}).setdefault('b',{})['explanation']='IP lập địa chỉ và định tuyến nhưng không bảo đảm đủ/thứ tự gói; TCP cung cấp truyền byte tin cậy ở tầng giao vận cho ứng dụng.'

def patch(q):
 c=changes.get(q['id']);
 if not c:return
 for key in ['question','explanation']:
  if key in c:q[key]=c[key]
 if 'options_replace'in c:q['options']=[c['options_replace'].get(o,o) for o in q['options']]
 if 'scenario_replace'in c:
  for a,b in c['scenario_replace'].items():q['scenario']=q['scenario'].replace(a,b)
 if 'scenario_append'in c and not q['scenario'].endswith(c['scenario_append']):q['scenario']+=c['scenario_append']
 for st in q.get('statements',[]):
  sc=c.get('statements',{}).get(st['label'],{})
  for key in ['text','answer','explanation']:
   if key in sc:st[key]=sc[key]
  for a,b in sc.get('text_replace',{}).items():st['text']=st['text'].replace(a,b)
for filename in ['mcq','tf','exams']:
 x=json.load(open('release-audit/'+filename+'-v2.json'))
 if filename=='exams':
  for e in x:
   if e['id'].startswith('thpt-'):
    e['tfCommonIds']=[q['id'] for q in e['tf'][:2]]; e['tfICTIds']=[q['id'] for q in e['tf'][2:]]
   for q in e['mcq']+e['tf']:patch(q)
 else:
  for q in x:patch(q)
 open('lib/'+filename+'.json','w').write(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
open('release-audit/content-corrections.json','w').write(json.dumps({'changes':changes,'changedTrueFalseGroups':list(variation),'policy':'New attempts only; saved results and prior snapshots are not regraded.'},ensure_ascii=False,indent=2))
for q in json.load(open('lib/tf.json')):
 if q['id'] in changes:
  lens=[len(s['text']) for s in q['statements']]
  print(q['id'],lens,'ratio',round(max(lens)/min(lens),2))
