# Learning Quizz — Tin học 12 ICT

## Bản hoàn thiện có kiểm chứng — 09/11/2026 (UTC+7)

Đã triển khai cùng URL https://ict12-learning-platform.vercel.app ; production22 Playwright checks PASS,0 lỗi JS không bắt, không cần duyệt SSO mới. Chi tiết `DEPLOYMENT.md`.

Phần này là hiện trạng mới nhất; các phần v2/bản nền bên dưới là lịch sử, không thay thế chính sách hiện tại.

- **Phân phối dạy học chỉnh được**: học kỳ từng bài, nhãn chủ đề, nhãn học kỳ đề và phạm vi thật bốn đề giữa/cuối kỳ. Mặc định khuyến nghị, không gán một lịch học kỳ “chính thức toàn quốc”. Phạm vi thiếu câu bị từ chối. Lượt làm lưu snapshot ngân hàng riêng, đổi kế hoạch không chấm lại lịch sử.
- **Bảo mật/đúng hạn**: chấm server; không key/lời giải trước nộp, kể cả luồng ôn câu sai khi còn bài đang làm. Kiểm tra lớp/giao bài ở API và DB. Hạn đóng nghiêm ngặt: chưa nộp hợp lệ thì đóng, giữ nháp cho giáo viên, **không nhận điểm**, không ân hạn; chính sách hiện trước và trong bài. Xử lý đồng thời đóng bài và CAS 409 rõ ràng.
- **Định dạng thi**: bộ ICT là24 TN +2 nhóm Đ/S chung +2 ICT (đề thật in6 nhóm gồm cả CS). Đúng 0/1/2/3/4 ý chấm0/0,1/0,25/0,5/1. Giữ chế độ luyện40s/lượt, không tự nhận mô phỏng50 phút chính thức. Không có quy luật mọi nhóm đều2 đúng–2 sai.
- **Nội dung**: kiểm cấu trúc tất cả468 TN +292 ý Đ/S/45 đề, đối chiếu đủ28 bài với PDF. Đã rà ngữ nghĩa nội bộ toàn bộ468 TN +292 ý Đ/S (vòng cuối328 TN +120 ý), có448 nhận xét từng câu/ý và nguồn đối chiếu, thêm31 sửa diễn đạt/giải thích/ngữ cảnh (gồm một chỉnh nhất quán t10.c thuộc vòng trước, không đếm trùng), không đổi khóa vòng này. Không tự nhận chứng nhận chuyên gia độc lập; mức độ chưa hiệu chỉnh thực nghiệm. Xem `release-audit/CONTENT_AUDIT.md` và `release-audit/full-review/REVIEW_REPORT.md`.
- **Riêng tư & vận hành**: BXH học sinh dùng mã HMAC, không tên/lớp/tài khoản; chỉ giáo viên đối chiếu danh tính. Thống kê/xuất điểm mặc định loại TEST; lọc lớp/tài khoản TEST để xem riêng. Excel an toàn công thức; CSV xử lý cả khoảng trắng/kí tự điều khiển đứng đầu. Hạn chế lạm dụng bền vững/atomic, session vô hiệu ngay khi khóa/reset, CSRF/JSON validation.
- **Khôi phục & hướng dẫn**: lỗi mạng/đồng bộ có nút lấy lại câu, đồng hồ không dừng; phiên hết hạn quay lại đăng nhập; trang tải lỗi có thử lại. Help ngắn cho học sinh/giáo viên, nguồn kiểm chứng và giới hạn chống gian lận thực tế. Công cụ backup riêng `scripts/backup.js`, quyền0700/0600; không public, không chia sẻ dữ liệu/mật khẩu hash. Runbook `release-audit/SECURITY_RECOVERY.md`.
- **Kiểm thử hoàn tất nội dung**: production22 checks sau triển khai cuối PASS; local/production mỗi bên92 lượt đề +1 lượt luyện sai;20 tình huống Chromium nội dung;365 trường hợp chấm Đ/S. Có hồ sơ448 mục, patch tái tạo và nguồn/trang; `release-audit/full-review/REPRODUCE.md`. Source `ict12-release-ready-source.zip` chỉ dành người vận hành (có ngân hàng đáp án), không public cho học sinh.
- **Kiểm thử mới**: `tests/readiness-*.js`, `tests/readiness-semantics.py`; báo cáo `tests/readiness-*-results.json`, Playwright mobile390px, deadline thật, phân quyền, lộ lời giải, scope/snapshot, bài THPT đủ40 lượt, Excel, mất mạng/khôi phục và preserving passwords/results. Xem `DEPLOYMENT.md`/`HANDOVER.json` để biết trạng thái triển khai thực tế; không suy từ kiểm thử local thành production.

Chạy kiểm thử thuần: `node tests/unit.js && node tests/upgrade-unit.js && node tests/readiness-unit.js`; `python3 tests/readiness-semantics.py`; `node tests/readiness-browser-semantics.js`. E2E dùng biến mật khẩu admin đã có trong môi trường an toàn, tuyệt đối không echo/in/log/lưu lại plaintext. Local runtime cuối:3006, không dùng các server cũ3000/3001/3005 để kiểm bản này.

## Nâng cấp v2 (09/11/2026, UTC+7) — đã triển khai Vercel

- Giao diện dashboard/quản trị/làm bài responsive; điện thoại có tab cuộn ngang và đồng hồ sticky, không bỏ chống gian lận.
- **Lớp & bài giao**: tạo lớp, xếp học sinh hiện có vào lớp, giao đề có giờ mở/hạn nộp (nhập/hiện UTC+7). Học sinh có bài giao phải bắt đầu từ mục này. Hạn được chốt khi bắt đầu; ngừng giao chỉ chặn lượt mới. Sau hạn trả HTTP 403, bài đóng không nhận điểm; trigger DB cũng chặn ghi bài trễ.
- **Tiến bộ & huy hiệu**: biểu đồ điểm 30 lượt gần nhất, dữ liệu chữ thay thế, tỉ lệ đúng A–G, lượt đầu/10 điểm/3 ngày liên tiếp/vững chủ đề (>=20 lượt trả lời và >=80% đúng). Thống kê quản trị có trung bình/phân bố điểm/câu yếu xếp đầu.
- **Bảng xếp hạng**: mặc định ẩn, giáo viên bật tại tab riêng; điểm tốt nhất mỗi đề, tổng thể là trung bình điểm tốt nhất, đồng điểm ưu tiên số đề. Chỉ hiện hai từ cuối họ tên và lớp, không hiện tài khoản; không tính TEST/tài khoản khóa/luyện câu sai.
- **Excel .xlsx**: xuất theo bộ lọc lớp/đề/học sinh, tùy chọn sheet từng câu; điểm là số, dữ liệu người dùng là chuỗi không phải công thức. Giới hạn 3 MB trước base64, yêu cầu lọc nếu lớn hơn.
- **Ôn câu sai**: mặc định chỉ hiện câu sai sau nộp, có công tắc xem tất cả; luyện lại tối đa 15 TN + 2 nhóm Đ/S từ lịch sử. Câu đã sửa đúng trong lượt luyện gần nhất được loại khỏi nhóm sai. Đề nguồn phải đang mở và cho xem đáp án. Luyện có snapshot riêng trên server, có thể tiếp tục khi tải lại.
- Giữ nguyên mật khẩu admin, tài khoản cũ/kết quả cũ/chấm phía server/RLS. Migration mở rộng collection và thêm trigger, không xóa dữ liệu. Chi tiết: `upgrades/design.md`, `upgrades/migration.sql`.
- Lời giải đã tồn tại cho đủ 468 TN + 73 nhóm Đ/S (292 ý). Giữ lại lời giải chuyên biệt; kiểm tra phủ 100% và đối chiếu mẫu SGK, không tuyên bố thẩm định biên tập mới từng câu. `tests/upgrade-explanation-audit.json`.
- Kiểm thử: `tests/upgrade-unit-results.json`, `tests/upgrade-e2e-results.json` và ảnh `tests/upgrade-*.png`. Bản source `ict12-platform-source.zip` chỉ gồm runtime và tài liệu không có secret; `deploy-request.json` gồm đúng 14 runtime files.

Các mục bên dưới là lịch sử v1; trạng thái triển khai hiện hành xem `DEPLOYMENT.md` và `HANDOVER.json`.

## Cập nhật toàn bộ sách (07/11/2026)

Hiện có **45 đề**, **28 bài học SGK**, 3 mục kiến thức tiền đề lớp 10–11 chỉ dùng trong đề THPT; ngân hàng **468 trắc nghiệm + 73 đúng/sai**. 28 đề bài học (15+2), 7 đề chủ đề A–G (18+2), 3 đề kết hợp AB/BC/ABC (45+9), 4 đề giữa/cuối kỳ (45+9, phân chia học kỳ là **đề xuất**, giáo viên xác nhận), 3 đề thi thử THPT (24+4). Dashboard chia riêng các nhóm này.

THPT chính thức 50 phút; chế độ luyện tại đây giữ 40 giây/câu hoặc ý, tổng tối đa 26 phút 40 giây. Ma trận 40/30/30 là lựa chọn biên soạn, không phải tỉ lệ bắt buộc đã xác minh của Bộ. Nội dung mới đã nhập từ `content-staging/`; xem `CONTENT_HANDOVER.json`, `validation-report.json` và `content-validation-full.json`. Các phần mô tả A–C bên dưới là ghi chép giai đoạn đầu, không phải tổng hiện tại. **Không chạy lại các make-bank.py/make-tf.py/make-exams.py cũ vì sẽ ghi đè ngân hàng mở rộng.** Bản sao trước import nằm trong `content-staging/import-backups/`.

## Trạng thái v1 (lịch sử, không phải hiện tại)

Ứng dụng đầy đủ chạy trên box tại http://localhost:3000, dùng dữ liệu Supabase thật. **Chưa triển khai Vercel**: connector từ chối quyền ghi vào team `endenkos-projects` (HTTP 403, cần authorize_team_access). Không thử vượt qua giới hạn bằng CLI/tài khoản khác. Website A cũ được giữ nguyên.

## Tài liệu đã đọc

SGK **Tin học 12 – Kết nối tri thức với cuộc sống, định hướng Tin học ứng dụng**, trang in 5–38, PDF trang 7–40. PDF ảnh: trang 7–15 đọc từ bản render cũ; trang 16–40 render bằng pdftoppm và đọc trực tiếp. Không dựa vào OCR rỗng trong bản trích xuất cũ.

Tên trong sách dùng **Chủ đề 1, 2, 3**, được gắn nhãn A/B/C cho phù hợp yêu cầu:

- A: Máy tính và xã hội tri thức. Bài 1: Làm quen với trí tuệ nhân tạo; Bài 2: Trí tuệ nhân tạo trong khoa học và đời sống.
- B: Mạng máy tính và Internet. Bài 3: Một số thiết bị mạng thông dụng; Bài 4: Giao thức mạng; Bài 5: Thực hành chia sẻ tài nguyên trên mạng.
- C: **Đạo đức, pháp luật và văn hóa trong môi trường số**. Bài 6: Giao tiếp và ứng xử trong không gian mạng. Không phải chủ đề lưu trữ/tìm kiếm.

## Cấu trúc đề

**Lịch sử bản nền 12 đề (hiện đã có45 đề như phần trên):** A/B/C mỗi đề 18 trắc nghiệm (12 NB + 4 TH + 2 VD), 2 đúng-sai; 6 đề bài học mỗi đề 15 trắc nghiệm (9 NB + 4 TH + 2 VD), 2 đúng-sai; 3 đề tổng hợp AB/BC/ABC mỗi đề 45 trắc nghiệm (30 NB + 10 TH + 5 VD), 9 đúng-sai.

Tất cả câu đúng-sai đều có kịch bản, 4 ý a–d, 2 TH + 2 VD; số ý đúng/sai không cố định (đã bỏ quy luật 2 đúng + 2 sai ở bản hoàn thiện). Mỗi câu có giải thích, bài/mục/trang cần xem lại. Ngân hàng: 123 trắc nghiệm + 23 đúng-sai (92 ý). Có tái sử dụng câu giữa các bộ đề, không lặp câu trong cùng bộ. A giữ nội dung cũ; thông tin phân loại bài học được bổ sung.

Độ dài phương án kiểm bằng số kí tự Unicode: dài nhất/ngắn nhất tối đa **1,1471**, tức chênh không quá 14,71% theo phương án ngắn nhất. Các ý đúng-sai tối đa 11,77%. Đáp án A–D cân bằng trong từng đề cố định (chênh tối đa 1); lúc làm bài thứ tự câu/phương án xáo ngẫu nhiên.

Đây là đề **theo dạng câu hỏi và cách chấm THPT 2025**, không phải đề thi chính thức hay bản sao nguyên cấu trúc số câu của đề chính thức.

## Chạy trên box

```sh
cd /workspace/ict12-platform
npm run dev
```

Không có dependency runtime. Node.js 24. Biến môi trường `.env` chỉ dành cho server. Không chia sẻ `.env`, DB_SECRET.txt, ADMIN_CREDENTIALS.txt hay schema.sql (có hash và bản ghi bootstrap).

Đăng nhập giáo viên: `/admin`. Thông tin quản trị được lưu duy nhất dạng rõ trong `ADMIN_CREDENTIALS.txt`, quyền 600. Đổi mật khẩu sau bàn giao. Mật khẩu lưu trên DB là scrypt với salt riêng. Không có đăng kí công khai, email hay OAuth.

## Cơ sở dữ liệu

Supabase dự án hiện có **endenko's Project**, ref `afhgfdkozdwtjdsvldzj`, đã được khôi phục từ trạng thái INACTIVE. Không tạo project trả phí mới. Chỉ thêm schema độc lập `ict12_private`, không đụng dữ liệu ứng dụng khác.

Lựa chọn triển khai: lưu document JSONB cho users, sessions, exams (thiết lập), attempts (gồm từng đáp án và kết quả), violations và rate limit. Hai bảng đều bật RLS, không có policy cho client, không cấp quyền đọc bảng cho anon/authenticated. Schema private không được công khai qua PostgREST. `public.ict12_access` là SECURITY INVOKER gọi hàm SECURITY DEFINER đặt trong schema private, search_path rỗng và kiểm tra SHA-256 của secret server trước mọi thao tác. Không dùng/expose service-role key. Chỉ server có secret, browser chỉ gọi API cùng nguồn.

Ngân hàng và đáp án nằm trong `lib/exams.json`, chỉ được bundle vào serverless function, không vào `public/`. Server chỉ gửi câu hiện tại và các lựa chọn, không gửi key trước nộp. Khóa tài khoản/reset mật khẩu đổi sessionVersion, lập tức vô hiệu mọi phiên cũ. Cookie HttpOnly/Secure/SameSite=Strict, phiên 12 giờ. Giới hạn thử sai đăng nhập 8 lần/15 phút cho cặp tài khoản/IP. Có kiểm tra Origin, CSP và chống chèn CSV formula.

Mỗi thao tác ghi dùng optimistic version check, không ghi đè âm thầm; tạo lượt thi dùng transaction advisory lock để tránh vượt lượt khi mở nhiều tab.

## Hướng dẫn giáo viên

1. Đăng nhập `/admin`.
2. **Học sinh**: nhập mỗi dòng `username,password,name,class`; hỗ trợ CSV quoted hoặc tab, tối đa 200 dòng/lần. Mật khẩu cấp tối thiểu 8 kí tự; thông báo danh sách tạo thành công/lỗi. Có tìm tên/lớp/tài khoản, khóa/mở khóa, đặt lại mật khẩu và xem kết quả từng học sinh.
3. **Bộ đề**: mở/đóng; số lượt/học sinh 1–100; ẩn/hiện đáp án sau nộp; ngưỡng tự nộp vi phạm 1–20. Ngưỡng vi phạm mới chỉ áp dụng lượt bắt đầu sau khi lưu. Đóng đề không hủy bài đang làm.
4. **Kết quả**: lọc đề, lớp, học sinh; xem chi tiết đáp án, điểm gốc và điểm /10, thời gian, vi phạm; xuất CSV UTF-8 phù hợp Excel.
5. **Phân tích lớp**: phần trăm đúng theo chủ đề/bài/mức độ; câu sai có giải thích và vị trí cần ôn; thống kê từng câu, phương án sai phổ biến; nhật kí sự kiện kèm thời gian máy chủ UTC+7. Chọn học sinh để drill-down.
6. **Mật khẩu**: đổi mật khẩu của chính người đăng nhập, sau đó đăng nhập lại.

Học sinh có theo bài/chủ đề/giữa kỳ, lịch sử riêng và phân tích riêng. <60% cần ôn lại, 60–79% củng cố, >=80% nắm vững; khuyến nghị đọc lại mục, ghi ý chính, làm lại bài học, đối chiếu giải thích.

## Đồng hồ và chống gian lận

- Mỗi trắc nghiệm và mỗi ý đúng-sai có 40 giây; xác nhận/đến hạn chuyển tiếp, không quay lại. Đáp án đã gửi lưu ngay. Máy chủ quyết định deadline và chấm điểm, chỉnh đồng hồ trình duyệt không thêm thời gian server.
- Khi mất mạng/rời trang, đồng hồ vẫn chạy; server tự bỏ trống các lượt đã quá hạn khi có request tiếp theo. Bài hết hạn toàn bộ được chấm khi học sinh/giáo viên tải lại dữ liệu, không có cron chạy nền.
- Rời tab/mất tiêu điểm/thoát fullscreen/tải lại tiếp tục bài được ghi nhận. Gộp sự kiện sát nhau 1,8 giây để không đếm tab+blur+fullscreen thành 3 lỗi của cùng một lần rời trang. Tự nộp server khi tới ngưỡng, mặc định 3.
- Chặn chọn/copy/paste/kéo/menu chuột phải và một số phím tắt trong lúc làm bài; watermark tên/tài khoản; che mờ khi mất focus.
- **Không thể chặn tuyệt đối screenshot, điện thoại thứ hai, extension/devtools hay client bị chỉnh sửa.** PrintScreen có thể không phát sự kiện trên một số hệ điều hành. Mobile/Safari có thể không hỗ trợ fullscreen; ứng dụng vẫn hoạt động với những kiểm soát còn lại. Không hứa ngăn được AI từ ảnh chụp. Nhật kí là tín hiệu để giáo viên xem xét, không tự khẳng định ý định gian lận.

## Triển khai khi có quyền Vercel

1. Người dùng cho phép team Vercel qua link authorize_team_access mới (link chỉ hiệu lực 10 phút). Không reconnect hay dùng scope khác.
2. Thử lại đúng create_project bị 403: team `team_blt8sqvJQ9ixAqMCP9WBUGga`, name `ict12-learning-platform`, framework null, outputDirectory public; env SUPABASE_URL, SUPABASE_KEY, DB_SECRET lấy từ file box, loại encrypted cho production/preview.
3. Gửi create_deployment từ `deploy-request.json` (file data tham chiếu `$file:/...`), target production. Không đưa file mật khẩu/.env vào source deployment. Manifest chỉ gồm 11 file runtime.
4. Kiểm tra deployment READY, alias và `/api`. Chạy lại `TEST_BASE=https://... node tests/e2e.js` để kiểm thử HTTPS/cookie thật. Chưa được xác minh bước này do quyền Vercel bị từ chối.

Nguồn deploy secret-free: `ict12-platform-source.zip` (không có thông tin xác thực). Bản đầy đủ/thiết lập nằm trên box.

## Giới hạn mở rộng

Thiết kế document nhỏ gọn phù hợp lớp/trường quy mô vừa. Các truy vấn danh sách hiện tải mọi attempt của phạm vi, thống kê tính ở API, và mỗi attempt giữ snapshot đáp án. Nếu dùng cho hàng nghìn học sinh đồng thời hoặc nhiều năm dữ liệu cần phân trang, bảng đáp án chuẩn hóa, tổng hợp SQL, lưu trữ/retention và kiểm thử tải. Chưa có tính năng biên soạn câu hỏi trong UI, xóa học sinh hoặc tạo lại ngân hàng bằng AI; không được quảng cáo như LMS quy mô lớn.

## Kết quả kiểm thử

- `tests/unit-results.json`: đủ 12 đề, cấu trúc, độ dài lựa chọn, không trùng câu, chấm 0/10, chấm đúng-sai từng mức 0/0,1/0,25/0,5/1, hết hạn server đều đạt.
- `tests/e2e-results.json`: Playwright/Chromium hoàn thành **23 lượt** bài học (0 điểm) và **81 lượt** đề ABC (10 điểm); đăng nhập quản trị/học sinh, tạo CSV, khuyến nghị bài yếu, tự nộp 3 vi phạm, lịch sử, responsive 390px, lọc bảng điểm, CSV, thống kê từng câu và nhật kí, ẩn đáp án, khóa tài khoản/vô hiệu phiên đều đạt. **0 lỗi JavaScript không xử lí**; console có HTTP 403 chủ động trong ca kiểm tra chặn học sinh truy cập API quản trị.
- `tests/api-results.json`: 10 ca về khóa đề, chỉ gửi câu hiện tại không có key, chặn hai bài đồng thời, chống ghi đè đáp án đồng thời, hết hạn server, không quay lại, hạn lượt, phân quyền, rate limit, cách li bài làm đều đạt.
- `tests/security-results.json`: sai secret bị HTTP 401; bảng private không lộ qua Data API (404); không có secret trong JS công khai.
- `tests/final-smoke-results.json`: backend cuối cùng, import theo lô/kiểm tra dòng trùng và không hợp lệ, sửa họ tên/lớp, khóa tài khoản qua UI; 0 lỗi JavaScript.
- Các tài khoản kiểm thử được ghi rõ “KIỂM THỬ / KHÔNG DÙNG”, lớp TEST, đã khóa và vô hiệu phiên cũ; giữ lại kết quả làm dữ liệu minh chứng, có thể lọc ra bằng lớp.
- Ảnh minh chứng nằm trong `tests/*.png`. Kiểm thử diễn ra trên box với Supabase thật, **chưa phải production Vercel**.

Kiểm thử mở rộng: `tests/expanded-e2e-results.json` PASS: 28 bài/7 nhóm, 4 đề học kỳ có nhãn đề xuất, 3 đề THPT; hoàn thành Bài 7 đủ 23 lượt và đề THPT 01 đủ 40 lượt, đều 10/10; lưu và phân tích kết quả; 0 lỗi JavaScript. Tài khoản kiểm thử lớp TEST đã khóa. `tests/expanded-unit-results.json` kiểm tra đủ 45 đề PASS.

Render fallback: xem `RENDER_HANDOVER.md`. Adapter Node production đã kiểm thử tại localhost:3001 (đăng nhập quản trị/học sinh, làm đủ 23 lượt Bài 7 đạt 10/10, lưu kết quả, 0 lỗi JavaScript; tài khoản TEST đã khóa). Vẫn chưa có public deployment vì thiếu nguồn Git có thể xuất bản và workspace Render được xác nhận. `npm start` dành cho production với biến môi trường được cung cấp; `npm run dev` cho box local.
