import json,pathlib
r=pathlib.Path(__file__).parent;L={x['id']:x for x in json.loads((r/'lib/lessons.json').read_text())};tf=[]
def add(n,sec,scenario,rows):
 ss=[]
 for i,line in enumerate(rows.strip().split('\n')):
  ans,text,ex=line.split(' :: ');ss.append(dict(label='abcd'[i],level='TH' if i<2 else 'VD',answer=ans=='T',text=text,explanation=ex))
 tf.append(dict(id=f't{len(tf)+1}',type='tf',topic=L[n]['topic'],lesson=n,section=sec,scenario=scenario,statements=ss,review=f'Bài {n} – {sec} (trang {L[n]["pages"]})'))
add(1,'1. Khái niệm về AI','Nhóm An làm trợ lí thư viện: nghe yêu cầu tiếng Việt, đọc ảnh phiếu viết tay rồi gợi ý sách dựa trên lịch sử mượn. Một bạn cho rằng cứ tự động hóa là có trí tuệ tổng quát.', '''T :: Hiểu yêu cầu nói tiếng Việt thể hiện khả năng xử lí ngôn ngữ của hệ thống. :: Hiểu tiếng nói là biểu hiện xử lí ngôn ngữ tự nhiên.
F :: Gợi ý sách theo lịch sử mượn đủ chứng minh máy có mọi năng lực như người. :: Gợi ý cá nhân hóa vẫn là nhiệm vụ hẹp.
T :: Để nhập phiếu viết tay, nhóm nên dùng nhận dạng chữ để tạo dữ liệu văn bản. :: Nhận dạng chữ phù hợp chuyển ảnh chữ viết sang văn bản.
F :: Để hiểu câu hỏi nói, nhóm chỉ cần sao chép tệp ghi âm sang một ổ đĩa khác. :: Sao chép âm thanh không có nghĩa hiểu nội dung yêu cầu.''')
add(1,'2. Một số ứng dụng của AI','Một bảo tàng thử robot thuyết minh. Camera giúp robot nhận biết vật cản; phần mềm nhận câu hỏi và trả lời. Robot chỉ phục vụ các chủ đề trưng bày đã được thiết kế.', '''F :: Nhận ra vật cản qua camera chỉ là tăng dung lượng lưu trữ của robot. :: Nhận biết môi trường là khả năng nhận thức.
T :: Trả lời câu hỏi bằng lời nói cần có khả năng xử lí ngôn ngữ tự nhiên. :: Hiểu và tạo lời nói là xử lí ngôn ngữ.
F :: Muốn giảm va chạm, nhóm nên bỏ camera rồi giữ nguyên mọi lệnh di chuyển. :: Bỏ cảm biến làm mất thông tin môi trường, không giải quyết va chạm.
T :: Muốn đón khách nói tiếng khác, nhóm cần bổ sung xử lí ngôn ngữ tương ứng. :: Cần xử lí ngôn ngữ phù hợp yêu cầu người sử dụng.''')
add(1,'2. Một số ứng dụng của AI','Lớp tìm hiểu MYCIN. Hệ thống hỏi triệu chứng rồi áp dụng các luật để gợi ý chẩn đoán. Một học sinh so sánh hệ này với bộ hẹn giờ bật chuông trường.', '''T :: Áp dụng tri thức và luật để rút kết luận là biểu hiện khả năng suy luận. :: MYCIN vận dụng luật suy diễn và tri thức chuyên gia.
F :: Bộ hẹn giờ bật chuông cố định có cùng năng lực suy luận như hệ MYCIN. :: Lặp thao tác cố định không đồng nghĩa suy luận từ tri thức.
T :: Khi minh họa suy luận, lớp nên trình bày cách luật dẫn tới một kết luận. :: Chuỗi luật và kết luận thể hiện quá trình suy luận.
F :: Khi cần nhận dạng phiếu khám viết tay, lớp chỉ nên tăng số cổng router. :: Cần nhận dạng chữ, không phải thêm cổng định tuyến.''')
add(2,'1. AI và sự phát triển của một số lĩnh vực','Trang trại dùng AI dự đoán thời điểm tưới từ độ ẩm và thời tiết. Sau khi thay cảm biến, mô hình đề xuất tưới quá nhiều. Quản lí định cho hệ thống thực hiện mọi khuyến nghị ngay.', '''T :: Dự đoán nhu cầu nước từ môi trường là ứng dụng AI trong nông nghiệp. :: AI hỗ trợ hợp lí hóa tưới tiêu từ dữ liệu môi trường.
F :: Có mô hình AI thì mọi dữ liệu cảm biến đều được bảo đảm đúng tuyệt đối. :: Cảm biến và dữ liệu đầu vào có thể sai.
F :: Khi dự báo bất thường, quản lí nên tưới ngay để tránh phải kiểm tra dữ liệu. :: Cần kiểm tra dữ liệu và đối chiếu điều kiện thực tế.
T :: Trước khi tưới, quản lí nên kiểm tra cảm biến và đối chiếu độ ẩm thực tế. :: Giám sát và kiểm chứng giảm tác hại từ quyết định sai.''')
add(2,'2. AI và một vài cảnh báo','Một nhóm dùng chatbot hỗ trợ ôn tập. Chatbot trả lời trôi chảy nhưng có thông tin khác sách. Nhóm còn định nhập hồ sơ cá nhân của các bạn để nhận tư vấn riêng.', '''F :: Trả lời trôi chảy có nghĩa chatbot đã có đủ trí tuệ tổng quát như người. :: Khả năng ngôn ngữ không đủ chứng minh trí tuệ tổng quát.
T :: Đưa hồ sơ cá nhân lên công cụ công khai có thể phát sinh nguy cơ riêng tư. :: Thu thập dữ liệu cá nhân làm tăng nguy cơ lạm dụng.
T :: Khi lời giải khác sách, nhóm nên đối chiếu nguồn tin cậy hoặc hỏi giáo viên. :: Cần kiểm chứng, không tin máy móc đầu ra AI.
F :: Khi muốn tư vấn riêng, nhóm nên gửi đủ hồ sơ người khác mà chưa xin phép. :: Cần bảo vệ dữ liệu cá nhân, không tùy tiện chia sẻ.''')
add(2,'2. AI và một vài cảnh báo','Bệnh viện thử công cụ AI phân tích ảnh. Bác sĩ không giải thích được một số kết quả. Đội kĩ thuật phát hiện mô hình có thể bị thay đổi khi chưa được cấp quyền.', '''T :: Khó giải thích cách tạo kết quả liên quan đến cảnh báo về minh bạch. :: AI có thể hoạt động như hộp đen khó giải thích quyết định.
F :: Mô hình bị thay đổi trái phép chỉ ảnh hưởng hình nền của máy phân tích. :: Tấn công mô hình có thể thay đổi kết quả, gây hại người bệnh.
F :: Khi chưa hiểu kết quả, bệnh viện nên bỏ mọi bước kiểm tra của bác sĩ. :: Con người cần giám sát các quyết định quan trọng.
T :: Khi có dấu hiệu can thiệp, đội kĩ thuật nên kiểm tra và bảo vệ mô hình. :: Cần bảo vệ dữ liệu và mô hình trước nguy cơ tấn công.''')
add(3,'1. Thiết bị mạng thông dụng','Phòng máy có 30 máy bàn nối hub. Khi nhiều máy truyền cùng lúc, mạng chậm do xung đột. Nhà trường muốn thêm máy tính bảng qua Wi-Fi và nối LAN ra Internet.', '''T :: Hub phát tín hiệu ra các cổng còn lại nên dễ gây xung đột khi đông máy. :: Hub phát tràn khiến nguy cơ xung đột tăng.
F :: WAP chủ yếu chuyển tín hiệu số thành tương tự để thay thế chức năng modem. :: WAP cung cấp kết nối không dây, không phải chức năng modem.
T :: Để giảm xung đột trong phòng, trường nên thay hub bằng switch đủ số cổng. :: Switch chuyển đúng cổng nhận, phù hợp LAN nhiều máy.
F :: Để nối các LAN qua Internet, trường chỉ cần dùng máy in thay cho router. :: Router dẫn đường giữa mạng, máy in không đảm nhiệm việc này.''')
add(3,'2. Thực hành kết nối máy tính với thiết bị mạng','Lan dùng máy bàn không có Wi-Fi; Minh dùng máy tính xách tay có Wi-Fi. Phòng đã có WAP bảo mật. Minh thấy tên mạng nhưng chưa nhập mật khẩu; Lan có sẵn cổng RJ45.', '''F :: Thấy tên một mạng Wi-Fi bảo mật đồng nghĩa đã được truy cập mạng đó. :: Mạng bảo mật yêu cầu xác thực đúng, không chỉ thấy tên.
T :: Cắm cáp RJ45 mới thiết lập kết nối vật lí, vẫn có thể cần cấu hình logic. :: Còn có cấu hình địa chỉ và kết nối tương ứng.
F :: Để Lan dùng Wi-Fi, nên thay dây nguồn mà không thêm bộ điều hợp mạng. :: Máy bàn cần bộ mạch/bộ điều hợp hỗ trợ Wi-Fi.
T :: Để Minh kết nối, cần chọn đúng mạng và nhập mật khẩu hợp lệ của mạng. :: Chọn mạng phù hợp, nhập đúng mật khẩu rồi kết nối.''')
add(3,'1. Thiết bị mạng thông dụng','Gia đình có một router Wi-Fi tích hợp modem. Các máy có dây nối cổng LAN, máy tính bảng nối Wi-Fi. Đường ra nhà cung cấp kết nối phía WAN.', '''T :: Cổng LAN kết nối thiết bị trong nhà, còn phía WAN hướng ra mạng ngoài. :: Router phân biệt cổng LAN với cổng WAN.
F :: Chức năng chuyển dạng tín hiệu của modem cũng chính là chức năng định tuyến. :: Chuyển tín hiệu và chọn đường là hai chức năng khác nhau.
T :: Nếu cần tăng số máy có dây, gia đình có thể nối thêm một switch phù hợp. :: Switch mở rộng kết nối có dây trong LAN.
F :: Nếu muốn thêm máy tính bảng, gia đình nên dùng cáp nguồn thay bộ Wi-Fi. :: Máy tính bảng kết nối không dây qua WAP/router Wi-Fi.''')
add(4,'2. Giao thức TCP/IP','An vừa tải tài liệu vừa trò chuyện trên cùng máy. Các gói tải về có thể đi những đường khác nhau và tới sai thứ tự. Một gói bị mất trong khi truyền.', '''T :: Cổng ứng dụng giúp phân biệt dữ liệu tải tệp với dữ liệu trò chuyện. :: TCP sử dụng cổng để phân phối dữ liệu đến đúng ứng dụng.
F :: IP tự bảo đảm đủ mọi gói, đúng thứ tự và chuyển đến đúng ứng dụng. :: IP lập địa chỉ và định tuyến; TCP đảm bảo tin cậy ở ứng dụng.
T :: Để khôi phục tệp, nơi nhận cần lắp ghép gói dựa trên số thứ tự tương ứng. :: TCP đánh số các gói để ráp đúng dữ liệu.
F :: Khi phát hiện mất gói, nên bỏ cơ chế gửi lại để vẫn bảo đảm tệp đầy đủ. :: Cần xác nhận và gửi lại khi thất lạc, sai sót.''')
add(4,'2. Giao thức TCP/IP','Router có bảng: nhóm 172.18.*.* qua cổng 2; nhóm 113.23.12.* qua cổng 3; cổng mặc định là 1. Hai gói lần lượt có đích 172.18.4.8 và 8.8.8.8.', '''F :: Bảng định tuyến tĩnh dùng để lựa chọn màu hiển thị của địa chỉ đích. :: Bảng dùng để chọn cổng chuyển tiếp theo nhóm địa chỉ.
T :: Khi địa chỉ không khớp mục cụ thể, router có thể dùng cổng mặc định. :: Cổng mặc định xử lí địa chỉ không có trong các nhóm.
F :: Gói có địa chỉ đích 172.18.4.8 nên được chuyển tiếp ngay qua cổng số 3. :: Gói khớp nhóm 172.18.*.* nên qua cổng 2.
T :: Gói có địa chỉ đích 8.8.8.8 nên được chuyển tiếp theo cổng mặc định 1. :: Không khớp nhóm cụ thể nên chọn mặc định.''')
add(4,'1. Giao thức mạng; 2. TCP/IP','Nhóm tìm hiểu gửi thư điện tử và duyệt web. Nhóm ghi lại giao thức SMTP, địa chỉ IPv4 và địa chỉ MAC; một bạn đổi byte 11000000 sang thập phân.', '''T :: SMTP liên quan gửi thư, còn POP3 hoặc IMAP liên quan nhận thư điện tử. :: Đây là các ví dụ về giao thức gửi và nhận thư trong bài.
F :: Địa chỉ IPv4 và địa chỉ MAC đều có cùng độ dài là 6 byte trên thiết bị. :: IPv4 có 4 byte; MAC có 6 byte theo sách.
T :: Với byte 11000000, nhóm nên ghi giá trị thập phân tương ứng bằng 192. :: 128 + 64 = 192.
F :: Khi cần dùng tên miền dễ nhớ, nhóm nên thay DNS bằng bộ hẹn giờ điện. :: DNS cho phép dùng tên chữ thay cho địa chỉ IP.''')
add(5,'1. Chia sẻ tệp và thư mục trên mạng cục bộ','Cô Mai chia sẻ thư mục bài đọc trong LAN. Học sinh chỉ cần xem, trợ giảng cần sửa. Máy học sinh đã phát hiện được máy cô nhưng chưa được cấp quyền.', '''T :: Nhìn thấy máy cô trong mạng không tự tạo quyền sửa thư mục bài đọc. :: Phát hiện máy và cấp quyền là hai điều kiện khác nhau.
F :: Quyền Read cho phép học sinh sửa và xóa mọi dữ liệu trong thư mục. :: Read chỉ cho phép đọc, không cho ghi sửa.
F :: Để bảo vệ bản gốc, cô nên cấp Read/Write cho mọi học sinh chưa xác định. :: Cấp quá rộng trái yêu cầu chỉ đọc và làm tăng rủi ro.
T :: Để trợ giảng sửa bài, cô nên cấp quyền đọc và ghi cho đúng người đó. :: Read/Write cho đúng đối tượng đáp ứng công việc.''')
add(5,'1. Chia sẻ tệp và thư mục trên mạng cục bộ','Nhóm hoàn tất dự án, cần thu hồi chia sẻ thư mục. Một bạn muốn chỉ đổi tên thư mục; bạn khác đề nghị bỏ Share this folder trong Advanced Sharing rồi kiểm tra từ máy bạn.', '''F :: Đổi tên thư mục là luôn thu hồi được mọi quyền chia sẻ đã cấp trước đó. :: Đổi tên không phải thao tác hủy chia sẻ được hướng dẫn.
T :: Bỏ Share this folder rồi xác nhận là cách hủy chia sẻ được nêu trong bài. :: Hủy chọn và OK/Apply là quy trình hủy chia sẻ.
T :: Sau khi hủy, nhóm nên kiểm tra từ máy khác để xác nhận không còn truy cập. :: Kiểm thử lại giúp xác nhận mục tiêu thu hồi truy cập.
F :: Để dữ liệu an toàn hơn, nhóm nên công bố mật khẩu trong thư mục Public. :: Công bố mật khẩu gây rủi ro, không bảo vệ dữ liệu.''')
add(5,'2. Chia sẻ máy in','Văn phòng có máy in nối máy A. Máy A được cài máy in và bật chia sẻ. Máy B muốn dùng máy in này; danh sách tự động chưa hiện máy in mong muốn.', '''T :: Máy A nhận yêu cầu và xếp hàng đợi khi đóng vai trò máy cung cấp dịch vụ in. :: Máy chủ in nhận và điều phối các lệnh in.
F :: Chia sẻ máy in buộc mọi máy khác phải mua thêm một máy in riêng giống hệt. :: Mục tiêu là dùng chung máy in, không cần mỗi máy một thiết bị.
T :: Nếu chưa thấy máy in, B có thể dùng mục máy in không có trong danh sách để tìm. :: Dùng The printer that I want isn't listed rồi Browse theo hướng dẫn.
F :: Sau khi thêm máy in mạng, B phải chép mọi tài liệu ra USB rồi mới gửi lệnh in. :: Sau kết nối có thể chọn trực tiếp máy in mạng khi in.''')
add(6,'1. Giao tiếp trong không gian mạng','Lớp họp trực tuyến để giảm việc đi lại. Bình nhắn một câu đùa ngắn khiến An hiểu là trách móc. Đang họp, mạng của một bạn bị mất và bạn không nghe được phần kết luận.', '''T :: Họp trực tuyến giúp tiết kiệm thời gian và chi phí di chuyển cho các bạn. :: Đây là ưu điểm của giao tiếp trực tuyến.
F :: Tin nhắn chữ luôn truyền đủ nét mặt và giọng điệu như khi gặp trực tiếp. :: Văn bản thiếu tín hiệu phi ngôn ngữ.
F :: Để tránh hiểu nhầm, Bình nên đăng câu chê bai An lên nhóm đông người hơn. :: Bêu xấu làm tăng tổn thương, không giải quyết hiểu nhầm.
T :: Để hỗ trợ bạn mất mạng, lớp nên gửi lại nội dung kết luận khi bạn kết nối. :: Đây là cách hỗ trợ thiết thực khi gặp sự cố kĩ thuật.''')
add(6,'2. Thể hiện tính nhân văn trong không gian mạng','Một bạn gửi ảnh nhật kí riêng của Hoa vào nhóm lớp mà chưa hỏi. Một số thành viên muốn đăng tiếp lên mạng; lớp trưởng nhắc mọi người giữ quyền riêng tư của Hoa.', '''F :: Chia sẻ trong nhóm kín thì không cần quan tâm sự cho phép của chủ nhật kí. :: Gửi cho bên thứ ba vẫn cần tôn trọng riêng tư.
T :: Đề nghị không phát tán ảnh riêng thể hiện tôn trọng người bị ảnh hưởng. :: Ngăn lan truyền thông tin riêng là hành vi tôn trọng.
T :: Người nhận ảnh nên dừng phát tán và tìm cách hỗ trợ Hoa xử lí sự việc. :: Cần hỗ trợ người bị tổn thương, không lan truyền thêm.
F :: Để giúp Hoa, lớp nên đăng lại toàn bộ nhật kí kèm tên thật cho mọi người xem. :: Đăng rộng làm tăng xâm phạm quyền riêng tư.''')
add(6,'2. Thể hiện tính nhân văn trong không gian mạng','Trong diễn đàn học tập, Minh phản đối lời giải của Hà bằng ngôn từ gay gắt. Hà chưa đọc hết ý kiến đã định công kích lại. Một bạn đề nghị cả hai tập trung vào lập luận.', '''T :: Phản biện lịch sự cần dùng ngôn từ đúng mực và tránh công kích cá nhân. :: Lịch sự và tôn trọng là yếu tố ứng xử nhân văn.
F :: Không đồng ý với lời giải cho phép xúc phạm danh dự người đã viết lời giải. :: Bất đồng không biện minh cho xúc phạm người khác.
T :: Hà nên đọc kĩ ý kiến và đưa lí do cụ thể thay vì dùng lời đe dọa Minh. :: Bình tĩnh, lắng nghe và phản biện có căn cứ.
F :: Nhóm nên khuyến khích châm chọc để hai bạn hiểu bài nhanh hơn và rõ hơn. :: Châm chọc gây tổn thương và làm cuộc trao đổi thiếu lành mạnh.''')
add(6,'1. Giao tiếp trong không gian mạng','Lan gặp một tài khoản mới nói có cùng sở thích. Tài khoản yêu cầu Lan gửi địa chỉ nhà và ảnh giấy tờ để được vào nhóm. Lan chưa biết ai đứng sau tài khoản.', '''F :: Người có chung sở thích trên mạng luôn cung cấp danh tính thật và đầy đủ. :: Tài khoản có thể ẩn danh hoặc giả mạo.
T :: Yêu cầu thông tin cá nhân có thể làm phát sinh nguy cơ đối với quyền riêng tư. :: Dữ liệu cá nhân có thể bị lộ hoặc lạm dụng.
F :: Lan nên gửi ngay ảnh giấy tờ để bảo đảm người lạ tin mình và giữ kết nối. :: Không nên tùy tiện gửi thông tin nhạy cảm cho người lạ.
T :: Lan nên dừng cung cấp dữ liệu và trao đổi với người đáng tin để được hỗ trợ. :: Bảo vệ dữ liệu và tìm hỗ trợ có trách nhiệm là phù hợp.''')
add(6,'2. Thể hiện tính nhân văn trong không gian mạng','Nam nhận bài viết chưa rõ nguồn nói xấu một bạn. Nhóm yêu cầu Nam chia sẻ cho nhanh. Một thành viên nhắc kiểm tra tính chính xác và tránh gây tổn hại danh tiếng.', '''T :: Chia sẻ thông tin chưa kiểm chứng có thể gây tổn hại danh tiếng người khác. :: Tin sai và tin đồn có thể gây tổn thương.
F :: Bài viết có nhiều lượt thích thì mọi nội dung đều đã được xác minh đúng. :: Lượt thích không thay cho xác minh nguồn và chứng cứ.
T :: Nam nên đọc kĩ, kiểm chứng nguồn và chưa chia sẻ khi thông tin còn đáng ngờ. :: Cần kiểm tra độ chính xác trước khi đăng hoặc chia sẻ.
F :: Nam nên thêm lời xúc phạm để người xem chú ý hơn tới bài viết đang lan truyền. :: Thêm lời xúc phạm làm tăng tác hại, không thể hiện nhân văn.''')
add(6,'2. Thể hiện tính nhân văn trong không gian mạng','Nhóm ôn tập gọi video. Một bạn mới ngại hỏi vì từng bị mỉa mai. Nhóm trưởng muốn tạo môi trường an toàn để mọi người góp ý và nhận hỗ trợ khi chưa hiểu bài.', '''F :: Chế giễu người hỏi là cách thể hiện sự thấu hiểu các khó khăn trong học tập. :: Thấu hiểu là cảm thông, không châm chọc.
T :: Lời động viên chân thành có thể giúp người gặp khó khăn cảm thấy được hỗ trợ. :: Hỗ trợ bao gồm động viên và an ủi.
F :: Nhóm nên chụp ảnh bạn đang bối rối rồi đăng công khai để buộc bạn tự tin hơn. :: Đăng ảnh gây tổn thương và có thể xâm phạm riêng tư.
T :: Nhóm nên giải thích rõ, dùng lời lịch sự và khuyến khích bạn đặt câu hỏi mới. :: Lịch sự, thấu hiểu và hỗ trợ giúp môi trường tích cực.''')
old=json.loads((r/'lib/old-a.json').read_text())
for q in old['trueFalse']:
 z=q.copy();z.update(id='a-old-'+str(q['id']),type='tf',topic='A',lesson=2,section='2. AI và một vài cảnh báo',review='Bài 2 – mục 1, 2 (trang 9–13)');tf.append(z)
(r/'lib/tf.json').write_text(json.dumps(tf,ensure_ascii=False,indent=2))
print('TF',len(tf))
