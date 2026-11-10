# Hoàn tất rà soát nội dung — 09/11/2026 (UTC+7)

## Phạm vi thực sự đã làm

- Vòng này đọc **328 câu TN, đủ bốn lựa chọn/đáp án/lời giải**, và **120 ý Đ/S thuộc30 tình huống**, đủ ngữ cảnh, mệnh đề, khóa và giải thích. Không dùng đếm câu hoặc dò từ khóa thay cho xét nội dung.
- `notes-1-4.tsv` … `notes-25-28.tsv`: **448 nhận xét được viết riêng theo từng mã câu/ý**, nêu lý do đúng/sai, sự khác biệt với nhiễu và giới hạn ngữ cảnh. `item-ledger.jsonl` gắn mỗi nhận xét với nội dung sau sửa, khóa trước/sau, fingerprint trước/sau, nguồn bài/trang và nguồn ngoài.
- Cộng vòng trước140 TN +172 ý: **468 TN +73 nhóm Đ/S /292 ý đã được rà ngữ nghĩa nội bộ**. Vòng trước giữ nguyên bằng chứng `../selection.json`, `../review-mcq.txt`, `../review-tf.txt`; vòng mới là phần bù không trùng. Đây **không phải chứng nhận/thẩm định chuyên gia độc lập**, không phải ngân hàng do Bộ GDĐT ban hành.
- Nguồn chính: bản quét SGK *Tin học12, Kết nối tri thức với cuộc sống, định hướng Tin học ứng dụng*, tệp đính kèm thực tế `01M6RAR3WEXWP0SF6C96V030BR.pdf`. Trang ghi trong hồ sơ là **trang in**; PDF lệch+2. Các nguồn tra cứu công khai đã đọc được ghi trong `sources.json`: lịch sử Dartmouth/đề xuất gốc1955, RFC9293/RFC1812, Cisco, Microsoft, MDN và trợ giúp chính thức Sites/Forms.
- Khi chỉ đối chiếu được phần/bài và khoảng trang, hồ sơ ghi rõ **khoảng trang**, không bịa trích dẫn chính xác từng dòng/trang. Một số điểm đã trực tiếp xem trang cụ thể được đánh dấu riêng.

## Sửa thực chất:31 bản ghi, không đổi khóa hay chấm lại lịch sử

**28 TN +3 bản ghi tình huống Đ/S**. Chi tiết trước/sau và lý do: `corrections.json`; tái tạo bằng `apply-corrections.py` từ baseline vòng1. Đồng bộ vào cả ngân hàng chuẩn và mọi bản sao trong45 bộ đề. Không đụng `legacy-exams-v2.json`, DB hay bài đã lưu.

1. **q2**: phân biệt đề xuất đã có thuật ngữ AI năm1955 với hội thảo1956 đánh dấu hình thành lĩnh vực; không tiếp tục dạy hai mốc như một.
2. **q32/q39/q49/q54/q57/q58**: giới hạn tra bảng MAC cho unicast đích đã học; SIM không đồng nghĩa mọi chuẩn3G/4G/5G đều là GSM; FCS phát hiện lỗi không tự yêu cầu phát lại; số thứ tự TCP là dòng byte; tuyến mặc định phải tồn tại; định tuyến không bảo đảm mọi gói luôn đến.
3. **q65/q98/q100**: chỉ rõ hộp thoại Windows theo sách, nêu tiền đề chưa có sự cho phép khi chia sẻ nhật ký, diễn đạt giảm căng thẳng rõ tiếng Việt.
4. **ext-l9-q11; ext-l10-q05/q13 và t2.a**: loại ô rowspan từ hàng trước khỏi bài tính đơn giản; tên máy chủ chỉ khẳng định cho URL HTTP/HTTPS đã cho; nêu trang hiện tại để liên kết tới tin.html chắc chắn là trang khác.
5. **ext-l11-q03/t2**: video cũng có thể phát âm thanh, nên hỏi thẻ chuyên dùng audio; thêm ảnh bị méo vào ngữ cảnh của ý đã hỏi.
6. **ext-l14-q02/q05/q11/q13; ext-l16-q06/q11; ext-l17-q11/q13**: inherit có thể nhận italic từ cha; line-height là hộp dòng; nêu cha trực tiếp khi tính em; giới hạn so sánh cascade cùng khối/style; display:table cũng có hộp ngoài dạng khối, nên yêu cầu khối thông thường không phải bảng; nêu rõ hộp khối trong bài tính content-box.
7. **ext-l21-q11; ext-l22-q11/q15; ext-l24-q02**: đối chiếu thông báo chính thức cùng trường đúng năm; Second screen only không tắt toàn bộ máy; nêu cáp HDMI trước khi chọn nguồn HDMI; phạm vi lưu dự án Sites theo phiên bản SGK.
8. **ext-l27-q09/q11**: giải thích hiện hành Forms cần xuất bản và quyền phản hồi riêng, không thừa hưởng tự động từ xuất bản Sites. Đối chiếu trợ giúp Google về thay đổi quyền Forms và nâng cấp biểu mẫu cũ.

9. **t10.c** (đã thuộc vòng trước, không đếm trùng vào120 ý còn lại): kiểm tra nhất quán cuối cùng còn phát hiện lời giải nói “đánh số các gói”; làm rõ số thứ tự **byte** theo RFC9293 §3.1/3.4 để thống nhất q54. Khóa true giữ nguyên. Hồ sơ riêng `followup-semantic-review.json`.

Một số mô tả SGK giản lược kỹ thuật (mã kiểm tra/phát lại, số thứ tự gói, ưu tiên CSS). Giải thích hiện tại giữ mức học phổ thông nhưng làm rõ bằng RFC/Cisco/MDN và ví dụ thực thi; không tuyên bố đây là bản đính chính chính thức của nhà xuất bản.

## Mức độ, phạm vi và điều chưa thể chứng nhận

-28 bài lớp12 ICT đều có trong ngân hàng. Phần tiền đề lớp10–11 đã được vòng trước rà, được tách riêng trong bộ luyện THPT; không đánh tráo thành bài mới lớp12.
- Các đáp án/nhiễu được xét theo **toàn bộ câu**, không chỉ chọn đáp án có vẻ đúng. Những trường hợp có thể đúng theo cách hiểu khác đã được thu hẹp tiền đề, không lật khóa âm thầm.
- Độ dài lựa chọn/ý vẫn≤1,15 lần; thứ tự câu và đáp án TN vẫn được trộn trên máy chủ. Mỗi nhóm vẫn2TH+2VD nhưng không buộc2đúng+2sai.
- **Nhiều câu là ôn tập cơ bản, nhiễu dễ loại**, nhất là nhận diện công cụ/hướng nghiệp/ứng xử. Nhãn NB/TH/VD là phân loại biên soạn, chưa được hiệu chỉnh bằng độ khó/độ phân biệt thực nghiệm; không coi ma trận tự biên soạn là chuẩn quốc gia hay chứng nhận đề thi có tính hệ trọng.
- **Không còn khóa sai hoặc đa đáp án đã xác định mà chưa xử lý** trong phạm vi rà soát. Điều này không phải cam kết không thể còn sai sót: chưa có hội đồng/chuyên gia độc lập thẩm định. Giáo viên vẫn cần duyệt khi dùng đánh giá có tính điểm.
- Tên nút/vị trí Windows, Google Sites/Forms theo ảnh SGK có thể đổi; đã kiểm chứng chức năng chính bằng trợ giúp chính thức nhưng không thao tác kiểm thử mọi giao diện/tài khoản bên thứ ba.
- Phân phối học kỳ là mặc định khuyến nghị, giáo viên chỉnh theo kế hoạch trường; không có tuyên bố một ánh xạ học kỳ chính thức dùng cho mọi trường.
- Dữ liệu cũ giữ ảnh chụp nội dung và điểm cũ, kể cả khi diễn đạt ngân hàng sau này được cải tiến. Không chấm lại kết quả cũ.

## Bằng chứng kiểm thử

- `tests/content-audit-unit-results.json`: phủ448 hồ sơ mới, phần bù không trùng, đồng bộ45 bộ, mọi khóa giữ nguyên, legacy byte-identical, snapshot giữ bối cảnh, mọi bước trước nộp không có khóa/lý giải.
- `tests/content-audit-browser-results.json`: **20 trường hợp Chromium thực**, gồm video phát nguồn audio, inherit italic/normal, em cha trực tiếp/gián tiếp, cascade layer thắng id, so sánh cùng style, content-box, colspan, bộ chọn, RGB/HSL, URL mailto không hostname và phân đoạn cùng/khác tài liệu.
- Các suite hồi quy về45 bộ đề,365 trường hợp chấm điểm Đ/S, lớp/quyền/hạn nộp, mobile, Excel, luyện sai và bảo toàn dữ liệu được chạy lại; kết quả/chốt triển khai được ghi trong HANDOVER và `release-audit/RELEASE_REPORT.md`, không suy diễn kiểm thử cục bộ thành đã triển khai production.
- Không có load test quy mô lớn hoặc thử khôi phục DB phá hủy production. Snapshot riêng được kiểm tra cấu trúc/checksum để so sánh bảo toàn; không gửi snapshot/credential ra ngoài hay đưa vào mã nguồn.
