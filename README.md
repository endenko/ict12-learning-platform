# Learning Quizz — Tin học 12 ICT

## v4 — Tự học lý thuyết, video bài giảng & tiến độ học (12/11/2026, UTC+7)

**Học sinh** có tab mới **Học lý thuyết** (ngay sau "Bài học"):
- **Lộ trình học**: 28 bài theo 7 chủ đề, vòng tiến độ tổng, nút "Tiếp tục: Bài N", ôn thẻ đến hạn, tìm kiếm toàn bộ lý thuyết (không dấu vẫn tìm được, ví dụ `giao thuc`, `colspan`). Trang chủ "Bài học" có thẻ **Lộ trình học** theo chủ đề.
- **Trang bài học** (mục lục bên trái, thanh tiến độ đọc, bài trước/sau): mục tiêu, các mục lý thuyết có tiêu đề, ví dụ, bảng, sơ đồ (CSS), ví dụ HTML/CSS **chạy trực tiếp** trong khung cách li, hộp **Ghi nhớ**, **Lỗi thường gặp**, **Thuật ngữ**.
- **Video bài giảng**: video của giáo viên lớp mình (ưu tiên) + danh sách chung đã kiểm tra; bấm mới tải (youtube-nocookie). Tự đánh dấu "đã xem" sau 60 giây hoặc bấm "Đánh dấu đã xem".
- **Thẻ ghi nhớ** (lật thẻ, Đã thuộc / Chưa thuộc, lặp lại ngắt quãng 1-3-7-16-35 ngày; thẻ chưa thuộc quay lại sau 10 phút), **Kiểm tra nhanh** 4 câu/bài (không tính điểm, phản hồi + giải thích ngay), **Luyện đề bài này** (mở danh sách đề của bài).
- **Thực hành HTML/CSS** (Bài 7–18 – chủ đề D trong nền tảng này): sửa mã, xem kết quả ngay trong `iframe sandbox=""` (không chạy JavaScript), lưu trên máy.
- Hoàn thành bài khi **đọc ≥ 80% và trả lời hết câu kiểm tra nhanh**. % bài = 40% đọc + 20% thẻ đã thuộc (hộp ≥ 3) + 25% câu đúng + 15% video (nếu bài có video).

**Giáo viên** – mục **✦ Tự học & tài liệu** trong cổng giáo viên:
- **Tiến độ tự học** theo lớp: bản đồ nhiệt 28 bài, từng học sinh (tiến độ, bài hoàn thành, thẻ, câu đúng, **học lý thuyết trước khi luyện đề**), bấm tên → báo cáo chi tiết có mục "Tự học lý thuyết".
- **Giao học lý thuyết**: "Học lý thuyết Bài N" cho lớp, có hạn; học sinh thấy cùng mục "Bài được giao"; thống kê đúng hạn / muộn / chưa xong.
- **Tài liệu bài học**: soạn văn bản (đậm, nghiêng, tiêu đề, danh sách, liên kết) + link PDF/Drive cho các lớp của mình. Nội dung **được làm sạch trên máy chủ** (`lib/sanitize.js`: danh sách thẻ cho phép, chỉ `href` http/https/mailto) và làm sạch lần nữa khi hiển thị.
- **Video bài giảng**: dán link YouTube/Vimeo → máy chủ kiểm tra qua oEmbed (tồn tại + cho phép nhúng) → thêm, sắp xếp, xóa, lưu (tối đa 8/bài). Admin quản lí danh sách chung.

**Nội dung:** 28 bài lý thuyết (87 mục, 224 thẻ ghi nhớ, 112 câu kiểm tra nhanh, 150 thuật ngữ, 13 ví dụ HTML/CSS chạy trực tiếp) – nguồn `content-v4/theory/*.txt`, build bằng `python3 content-v4/build-theory.py` → `public/theory.json` + `lib/theory-index.json`. Video: 56 video tiếng Việt (2/bài, 0 bài thiếu) tìm bằng `content-v4/videos/find-videos.py`, đều được kiểm tra oEmbed 200 và tiêu đề khớp số bài; nạp bằng `node --env-file=.env scripts/seed-videos.js` (kiểm tra lại oEmbed, không ghi đè danh sách admin đã sửa).

**Bảo mật & dữ liệu:** migration bổ sung `migrations/v4-learning.sql` (Supabase `ict12_v4_learning`): thêm collection progress / materials / videos / studytasks + chỉ mục ownerId; `scoped_check` thêm nhánh kiểm tra sở hữu cho tài liệu, video, nhiệm vụ (giáo viên chỉ ghi vào lớp của mình, không sửa danh sách chung). Không xóa/sửa dữ liệu cũ. CSP chỉ thêm `frame-src` youtube-nocookie/player.vimeo và ảnh `i.ytimg.com`.

**Kiểm thử v4:** `node tests/v4-unit.js` (14) · `TEST_BASE=… TEST_TAG=… node --env-file=.env tests/v4-e2e.js` (desktop + mobile 390 px + dark mode; 24 bước + 18 kiểm tra cách li API/DB) · `tests/v4-regression.js` (luồng giao bài/làm bài v2–v3 + "đã học lý thuyết trước khi luyện đề"). Nếu không có mật khẩu admin trong môi trường, test tự tạo tài khoản giáo viên TEST trực tiếp trong DB và tự khóa sau khi chạy.

## v3 — Cổng giáo viên & đánh giá chi tiết (12/11/2026, UTC+7)

**Vai trò:** `admin` (quản trị toàn trường) · `teacher` (giáo viên, chỉ thấy lớp của mình) · `student`.

### Admin tạo tài khoản giáo viên đầu tiên
1. Đăng nhập `/admin` bằng tài khoản `admin` (mật khẩu không đổi).
2. Mở tab **★ Cổng giáo viên** → mục **Giáo viên** ở thanh bên.
3. Ô "Tạo tài khoản giáo viên": mỗi dòng `Họ tên, tên đăng nhập (tuỳ chọn), email (tuỳ chọn)` → **Tạo tài khoản**. Hệ thống tạo mật khẩu ngẫu nhiên, **chỉ hiển thị một lần** → bấm **Tải CSV** hoặc **In phiếu tài khoản** để trao cho giáo viên.
4. Tại cùng màn hình: **Đặt lại MK** (mật khẩu mới hiển thị một lần, phiên cũ bị đăng xuất), **Khóa / Mở khóa**.
5. Lớp cũ (do admin tạo trước v3) có thể giao cho giáo viên: mục **Lớp học** → chọn "Giáo viên phụ trách" trên thẻ lớp. Admin cũng có thể tạo lớp và chọn giáo viên phụ trách ngay khi tạo.

Giáo viên đăng nhập ở trang chủ hoặc `/admin` và được đưa thẳng vào **cổng giáo viên** (thanh điều hướng bên trái; trên điện thoại là thanh cuộn ngang).

### Chức năng giáo viên
- **Lớp học:** tạo lớp (tên duy nhất toàn trường, ví dụ `12A1-2026`), lưu trữ/mở lại; **nhập học sinh** từ Excel `.xlsx`/CSV (cột "Họ tên", tuỳ chọn "Tài khoản") hoặc dán danh sách → xem trước → tạo tài khoản; tên đăng nhập tự sinh (ví dụ `anhnv.12a1`), mật khẩu ngẫu nhiên, tải CSV/in phiếu.
- **Học sinh:** tìm/lọc, trạng thái trực tuyến/đang làm bài, đặt lại mật khẩu, khóa, chuyển lớp (chỉ giữa các lớp của mình).
- **Đánh giá chi tiết từng học sinh** (giáo viên + admin): biểu đồ điểm theo thời gian, % đúng theo chủ đề, bản đồ thành thạo Bài 1–28, điểm mạnh/yếu, câu hay sai & nhầm lẫn thường gặp, thời gian mỗi câu (TB, trung vị, sai trong <3 giây, hết giờ — ghi nhận từ v3), nhật ký chống gian lận, lịch sử bài làm + xem chi tiết từng câu, tình trạng bài giao (đúng hạn / làm bù sau hạn / thiếu / đang mở), **mức đánh giá Giỏi ≥ 8,0 · Khá 6,5–<8,0 · Đạt 5,0–<6,5 · Chưa đạt < 5,0** (TB 10 bài kiểm tra gần nhất, không tính luyện tập), **nhận xét tiếng Việt tự động** + gợi ý ôn tập, **ghi chú riêng** của giáo viên (học sinh không thấy), **In / Lưu PDF**.
- **Học sinh tự xem** tab "Báo cáo của tôi" (bản rút gọn: không có ghi chú GV, nhật ký vi phạm chi tiết hay đáp án câu sai).
- **Phân tích lớp:** điểm TB, phân bố điểm, tỉ lệ đạt, xếp mức, chủ đề/bài yếu nhất, xu hướng theo tháng, HS cần quan tâm (điểm < 5, đang giảm, thiếu bài, không hoạt động > 14 ngày, nhiều vi phạm), bảng xếp hạng, **phân tích câu hỏi** (độ khó p, độ phân biệt D theo nhóm 27%, tần suất chọn từng phương án, cảnh báo phương án không ai chọn), so sánh các lớp, **xuất Excel** (4 trang tính).
- **Giao bài:** chọn lớp + đề (ngân hàng hoặc đề tự tạo), giờ mở/đóng, số lượt tối đa (1–20), hiện đáp án (ngay sau khi nộp / sau khi đóng / không).
- **Tạo đề:** chọn từng câu từ ngân hàng (lọc bài, mức độ, loại, từ khóa) hoặc **ngẫu nhiên theo ma trận** (bài × NB/TH/VD + số câu Đ/S). Đề của giáo viên chỉ hiện với học sinh lớp được giao.
- **Ngân hàng câu hỏi riêng:** nhập theo định dạng `N|Câu hỏi|Đúng|Sai1|Sai2|Sai3|Giải thích|Bài` (và `TF|…`), chỉ người tạo thấy.
- **Thông báo** cho lớp (hiện trên trang chủ học sinh) · **Trực tuyến**: ai đang online / đang làm bài (tự làm mới 15 giây).

### Đánh giá giáo viên (admin)
Mục **Giáo viên** → bấm tên giáo viên: số lớp/học sinh, bài đã giao, đề tự tạo, tỉ lệ HS tham gia 30 ngày, tỉ lệ hoàn thành đúng hạn, điểm TB các lớp và thay đổi theo tháng, bảng các lớp, nhật ký hoạt động. Đây là **tổng quan trung lập** để hỗ trợ, không phải điểm xếp loại giáo viên.

### Phân quyền & bảo mật
- Mọi kiểm tra quyền ở **máy chủ** (`lib/portal.js`): giáo viên chỉ đọc lớp có `ownerId` = mình, học sinh thuộc các lớp đó, bài làm/vi phạm/bài giao/thông báo của các lớp đó; dữ liệu khác trả 404.
- Mọi thao tác **ghi** của giáo viên đi qua RPC `scoped_put`: Postgres kiểm tra lại quyền sở hữu (`ict12_private.scoped_check`, lỗi 42501) — kể cả khi API có lỗi. Không thể tạo lớp trùng tên lớp của tài khoản đang có (chặn chiếm quyền học sinh qua tên lớp).
- Khóa service-role không được dùng; ứng dụng vẫn chỉ gọi RPC bằng khóa công khai + bí mật máy chủ. Migration chỉ bổ sung: `migrations/v3-teacher.sql`, `migrations/v3-teacher-2.sql` (không xóa/sửa dữ liệu, giữ nguyên mọi tài khoản và mật khẩu admin).
- Kiểm thử cách li: `tests/v3-e2e.js` dùng 2 giáo viên thật, kiểm tra ~28 hành vi chéo (API 404/400 + từ chối ở cơ sở dữ liệu).

### Kiểm thử v3
`node tests/v3-unit.js` (16) · `TEST_BASE=… TEST_TAG=… node --env-file=.env tests/v3-e2e.js` (Playwright, desktop + mobile 390 px, tự khóa tài khoản TEST và lưu trữ lớp TEST sau khi chạy).
Production deployment: `dpl_8AZjSzTHonTY9y3RfLhJgs27ZB6v` (READY, alias ict12-learning-platform.vercel.app) — v3 e2e production 20 checks + 27 isolation checks PASS; v2 e2e production 22/22 PASS; test accounts locked, TEST classes archived (`tests/v3-cleanup-results.json`).

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


## v2 upgrade (2026-11-11)
- Content: 790 new MC + 50 new Đ/S (lib/mcq-v3.json, lib/tf-v3.json; authoring in content-v3/, build with `python3 content-v3/build.py`, QA with `python3 content-v3/qa.py`).
- Lesson variants: Bài 1–13 → v2–v5 (5 sets each), Bài 14–28 → v2–v4 (4 sets each); 97 new lesson sets, ~15 TN + 2 Đ/S, pairwise overlap ≤4 questions.
- GK/CK: midterm-1, final-1, midterm-2, final-2 each have -v2..-v5 (5 sets per term). THPT 2025-format mocks: thpt-ict-01..10 (24 TN + 4 Đ/S). Total exams: 165.
- Questions and options are still shuffled per attempt server-side; 40 s/step and no going back are unchanged.
- Features: random mixed practice (topic/lesson/level), bookmarks + bookmark practice, retry-wrong, per-lesson mastery grid, lesson/exam search and filters, admin bulk import (tab "Nhập câu hỏi", closed by default, archive = soft-delete).
- UI: public/theme.css (design system + dark mode + mobile + reduced motion) and public/ui.js (overrides app.js renderers).
- Tests: tests/v2-unit.js (12/12), tests/v2-e2e.js (22/22 against local, preview and production; TEST_BASE / TEST_TAG env).
- Production deployment: dpl_DY7yywiT8qTEJBMYw1hPZo9HTYMW (preview dpl_5KfnkMSGLevXivgLLrmXZztJNEtA).
- Anti-cheat option lengths (2026-11-11 follow-up): all 790 new MC items now meet max/min option length <= 1.15 (was 438 failing); the key is the unique longest option in 13.2% of items (was 41.8%); 'pick the longest' scores 24.7% (was 50.0%) and 'pick the shortest' 22.1% (was 9.8%), near the 25% chance level. The strict 1.15 test in tests/unit.js again applies to every item, new ones included. Named-term items fixed: Win+P Extend/Duplicate (L22) and Google Forms question types (L27). Production deployment: dpl_CQdDRghEH4bUjsAzpEkpvbBEP5CY (previous v2: dpl_DY7yywiT8qTEJBMYw1hPZo9HTYMW).
