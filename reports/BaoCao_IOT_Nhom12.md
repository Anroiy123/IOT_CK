**BỘ KHOA HỌC VÀ CÔNG NGHỆ**

**HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG**

**CƠ SỞ TẠI THÀNH PHỐ HỒ CHÍ MINH**

**----------o0o----------**

**BÁO CÁO**

**ĐỒ ÁN MÔN HỌC**

**THIẾT KẾ THIẾT BỊ ĐIỀU KHIỂN BẰNG CỬ CHỈ TAY SỬ DỤNG DEEP LEARNING CHO
ĐIỀU KHIỂN THÔNG MINH XE TỰ HÀNH**

| **Thông tin**        | **Nội dung**            |
|:---------------------|:------------------------|
| Môn học              | Phát triển ứng dụng IOT |
| Giảng viên hướng dẫn | Đàm Minh Lịnh           |
| Nhóm thực hiện       | Nhóm 12                 |
| Lớp                  | D22CQPTUD01-N           |

| **MSSV**   | **Họ tên**      | **Email**                         | **Vai trò** |
|:-----------|:----------------|:----------------------------------|:------------|
| N22DCPT035 | Trần Quang Hùng | n22dcpt035@student.ptithcm.edu.vn | Nhóm trưởng |
| N22DCPT052 | Vũ Quang Long   | n22dcpt052@student.ptithcm.edu.vn | Thành viên  |

TP. Hồ Chí Minh, 15 / 6 / 2026

> **Hướng dẫn dàn trang khi đưa vào Google Docs/Microsoft Word:** khổ A4;
> Times New Roman; nội dung 11 pt; tiêu đề chương 16 pt đậm; tiêu đề mục
> 13 pt đậm; giãn dòng 1,5; căn đều hai lề; lề trái 3,0 cm, lề phải 2,0 cm,
> lề trên 2,0 cm, lề dưới 2,0 cm; khoảng cách sau đoạn 6 pt. Với cấu hình
> này, toàn bộ nội dung, bảng, công thức và hình minh họa trong file được
> thiết kế cho khoảng 40-55 trang. Số trang thực tế có thể thay đổi theo
> cách xuống dòng của bảng và kích thước hình.

# **LỜI CẢM ƠN**

Nhóm sinh viên chúng em xin gửi lời cảm ơn chân thành đến Học viện Công
nghệ Bưu chính Viễn thông và quý thầy cô đã tạo điều kiện để nhóm được
tiếp cận các kiến thức về IoT, trí tuệ nhân tạo và triển khai hệ thống
nhúng trong môi trường thực tế.

Đặc biệt, nhóm xin cảm ơn thầy Đàm Minh Lịnh đã hướng dẫn định hướng đề
tài, nhấn mạnh yêu cầu về nguồn tài liệu khoa học, tiêu chí đánh giá mô
hình và yêu cầu trình bày báo cáo theo cấu trúc nghiên cứu.

Do thời gian thực hiện và điều kiện phần cứng còn hạn chế, hệ thống chắc
chắn chưa thể đạt mức hoàn thiện như một sản phẩm thương mại. Nhóm mong
nhận được góp ý để tiếp tục cải thiện mô hình nhận dạng, mở rộng dữ liệu
và tối ưu độ trễ điều khiển.

# **TÓM TẮT**

Báo cáo trình bày quá trình thiết kế và thực nghiệm một thiết bị điều
khiển xe tự hành bằng cử chỉ tay sử dụng Deep Learning. Hệ thống dùng
webcam laptop, gateway MediaPipe crop, cloud API FastAPI trên Azure
Container Apps và ESP32 điều khiển L298N/PCA9685.

Mô hình chính là CNN MobileNetV3Small, ảnh đầu vào 160x160, huấn luyện
trên bộ dữ liệu nội bộ gồm 5 người, 8 lớp, 570 clip và 8,550 frame. Kết
quả offline đạt accuracy 83.33% và macro F1 83.37%. Azure RTT median
158.08 ms, p95 171.58 ms.

Đóng góp chính là pipeline end-to-end từ nhận dạng cử chỉ đến điều khiển
phần cứng, có confidence threshold, voting/stabilization, cooldown
servo, sequence number, token và deadman timeout. Báo cáo cũng chỉ ra
các hạn chế như nhầm lẫn giữa one/two/like/dislike và chưa đánh giá đủ
robustness trước nền phức tạp.

# **MỤC LỤC**

Danh mục thuật ngữ và từ viết tắt

Chương 1. Giới thiệu

Chương 2. Nghiên cứu liên quan

Chương 3. Mô hình đề xuất

Chương 4. Thực nghiệm, đánh giá và thảo luận

Kết luận, hạn chế và hướng phát triển

Tài liệu tham khảo

Phụ lục

# **DANH MỤC HÌNH**

Hình 3.1. Kiến trúc hệ thống

Hình 3.2. Trình tự xử lý online

Hình 3.3. Ảnh mẫu gesture

Hình 4.1. Phân bố dataset

Hình 4.2. Lịch sử huấn luyện

Hình 4.3. Confusion matrix

Hình 4.4. So sánh latency

# **DANH MỤC BẢNG**

Bảng 1.1. Mục tiêu và tiêu chí

Bảng 2.1. So sánh nghiên cứu liên quan

Bảng 3.1. Cử chỉ và chức năng

Bảng 3.2. Tham số model

Bảng 4.1. Thống kê dataset

Bảng 4.2. Kết quả offline

Bảng 4.3. Độ trễ online

# **DANH MỤC THUẬT NGỮ VÀ TỪ VIẾT TẮT**

| **Từ viết tắt** | **Tên đầy đủ** | **Diễn giải** |
|:---|:---|:---|
| AI | Artificial Intelligence | Trí tuệ nhân tạo |
| CNN | Convolutional Neural Network | Mạng nơ-ron tích chập |
| CNN-LSTM | CNN + Long Short-Term Memory | Mô hình kết hợp không gian và chuỗi thời gian |
| DL | Deep Learning | Học sâu |
| ESP32 | Espressif ESP32 | Vi điều khiển Wi-Fi/Bluetooth |
| FastAPI | FastAPI framework | Framework triển khai API suy diễn |
| HCI | Human-Computer Interaction | Tương tác người - máy |
| HGR | Hand Gesture Recognition | Nhận dạng cử chỉ tay |
| HRI | Human-Robot Interaction | Tương tác người - robot |
| IoT | Internet of Things | Internet vạn vật |
| PCA9685 | 16-channel PWM driver | Mạch mở rộng PWM điều khiển servo |
| RTT | Round Trip Time | Thời gian khứ hồi khi gọi cloud API |
| WebSocket | RFC 6455 WebSocket | Kênh truyền lệnh hai chiều |

# **CHƯƠNG 1. GIỚI THIỆU**

Trong các hệ thống tương tác người - máy, cử chỉ tay là một kênh giao
tiếp tự nhiên vì người dùng không cần thiết bị cầm tay và có thể truyền
đạt lệnh nhanh bằng chuyển động trực quan. Các nghiên cứu tổng quan về
hand gesture recognition chỉ ra rằng nhận dạng cử chỉ đã phát triển từ
đặc trưng thủ công sang học sâu trên ảnh, depth, skeleton hoặc cảm biến
đeo \[4\], \[2\], \[1\].

Đề tài này xuất phát từ yêu cầu thiết kế thiết bị nhận dạng cử chỉ tay
sử dụng Deep Learning cho điều khiển thông minh xe tự hành. Khác với bài
toán chỉ phân loại ảnh offline, hệ thống cần xử lý liên tục: camera đọc
frame, mô hình suy diễn cử chỉ, gateway lọc nhiễu, truyền lệnh qua mạng
và vi điều khiển thực thi trên motor/servo.

Deep Learning phù hợp với bài toán vì CNN học đặc trưng không gian của
bàn tay, trong khi CNN-LSTM hoặc 3D-CNN phù hợp hơn với cử chỉ động
\[6\], \[7\], \[12\], \[13\]. Đề tài chọn CNN MobileNetV3Small làm mô
hình chính, đồng thời giữ CNN-LSTM như hướng mở rộng.

Ở tầng tiền xử lý, MediaPipe Hands cho thấy khả năng phát hiện bàn tay
và landmark theo thời gian thực từ camera RGB đơn \[5\]. Repo hiện tại
dùng MediaPipe để crop vùng bàn tay trước khi gửi ảnh lên cloud, giúp
giảm nhiễu nền nhưng vẫn đáp ứng yêu cầu model lưu trữ trên cloud.

Trong tương tác người - robot, các nghiên cứu gần đây nhấn mạnh rằng
nhận dạng cử chỉ cần được đánh giá trong điều kiện vận hành thực tế, bao
gồm nền phức tạp, khoảng cách camera, tốc độ phản hồi và trạng thái an
toàn của robot \[1\], \[21\], \[15\].

## **1.1 Bối cảnh và tính cấp thiết**

Sự phát triển của IoT tạo điều kiện để các thiết bị nhúng như ESP32 kết
nối trực tiếp với gateway, cloud và cơ cấu chấp hành. Khi kết hợp với
AI, thiết bị nhúng không nhất thiết phải tự xử lý toàn bộ ảnh; nó có thể
nhận lệnh đã được suy diễn từ gateway hoặc cloud service.

Nếu cử chỉ bị nhận sai trong hệ robot, lỗi có thể dẫn đến chuyển động
không mong muốn. Vì vậy hệ thống đề xuất không truyền mọi dự đoán thành
lệnh ngay mà dùng confidence threshold, số lần lặp liên tiếp và deadman
timeout.

## **1.2 Mục tiêu, phạm vi và đóng góp**

| **Nhóm mục tiêu** | **Nội dung** | **Tiêu chí đánh giá** |
|:---|:---|:---|
| Nhận dạng | Phân loại 8 lớp cử chỉ tay | Accuracy, macro F1, confusion matrix |
| Thời gian thực | Gateway xử lý webcam và gọi cloud online | RTT, inference_ms, total_ms |
| Triển khai IoT | ESP32 nhận lệnh qua WebSocket | ACK, sequence, token, deadman timeout |
| An toàn | Không phát lệnh khi confidence thấp hoặc cloud lỗi | stop tự động, cooldown servo |
| Học thuật | Liên hệ CNN, CNN-LSTM, HGR/HRI, cloud/edge AI | Tài liệu IEEE/ACM/Elsevier và Zotero |

*Bảng 1.1. Mục tiêu và tiêu chí đánh giá đề tài*

Đóng góp thứ nhất là thiết kế pipeline end-to-end từ camera đến phần
cứng. Đóng góp thứ hai là xây dựng dataset nội bộ có metadata rõ ràng
theo subject, gesture, clip và frame. Đóng góp thứ ba là triển khai CNN
trên Azure. Đóng góp thứ tư là tích hợp cơ chế an toàn ở gateway và
firmware.

Báo cáo gồm bốn chương: giới thiệu, nghiên cứu liên quan, mô hình đề
xuất, thực nghiệm và thảo luận. Phần cuối trình bày kết luận, hạn chế và
hướng phát triển theo ba đoạn đúng yêu cầu.

## **1.3 Vấn đề nghiên cứu**

Một hệ thống nhận dạng cử chỉ dùng để trình diễn trên tập ảnh có thể được
đánh giá chủ yếu bằng độ chính xác. Tuy nhiên, khi đầu ra của mô hình được
dùng để điều khiển một xe có động cơ, bài toán trở thành một hệ thống điều
khiển có yếu tố an toàn. Một dự đoán sai không còn chỉ là một nhãn sai trên
màn hình mà có thể làm xe tiến, lùi hoặc đổi hướng ngoài ý muốn. Vì vậy,
đề tài phải giải quyết đồng thời bốn vấn đề: nhận dạng đúng cử chỉ; phản hồi
đủ nhanh; truyền lệnh tin cậy; và đưa hệ thống về trạng thái dừng khi bất kỳ
thành phần nào mất ổn định.

Vấn đề thứ nhất là biến thiên hình ảnh. Cùng một cử chỉ có thể có hình dạng
khác nhau khi người dùng thay đổi góc cổ tay, khoảng cách đến camera, tay
trái hoặc tay phải, màu da, ánh sáng và phông nền. Ngược lại, các lớp như
`one`, `two`, `like` và `dislike` có thể tạo ra những vùng ảnh tương đối
giống nhau nếu bàn tay bị nghiêng hoặc crop mất đầu ngón. Các tổng quan về
HGR đều xem phân đoạn bàn tay, lựa chọn đặc trưng và khả năng tổng quát hóa
giữa người dùng là những khó khăn cốt lõi [1]-[4]. Điều này giải thích vì
sao đề tài không chỉ thu thập nhiều frame liên tiếp của một người mà tổ
chức dữ liệu theo `subject_id`, `clip_id` và điều kiện thu nhận.

Vấn đề thứ hai là ràng buộc thời gian thực. Tổng thời gian từ lúc cử chỉ
xuất hiện đến lúc cơ cấu chấp hành phản ứng bao gồm thời gian camera lấy
ảnh, phát hiện bàn tay, crop và mã hóa JPEG, truyền request lên cloud, suy
diễn mô hình, truyền phản hồi về gateway, ổn định dự đoán và gửi lệnh đến
ESP32. Chỉ đo `inference_ms` của mô hình là chưa đủ vì người dùng cảm nhận
toàn bộ độ trễ đầu-cuối. Do đó, đề tài phân tách log thành
`capture_ms`, `preprocess_ms`, `cloud_rtt_ms`, `inference_ms`,
`esp32_ack_ms` và `total_ms`. Hai thống kê median và p95 được dùng song
song để phản ánh cả trường hợp thông thường lẫn phần đuôi độ trễ.

Vấn đề thứ ba là sự khác biệt giữa dự đoán và lệnh điều khiển. Một camera
30 FPS có thể tạo ra hàng chục dự đoán mỗi giây; nếu tất cả dự đoán được
chuyển thành lệnh, động cơ và servo sẽ rung hoặc đổi trạng thái liên tục.
Gateway vì thế cần một lớp quyết định nằm sau mô hình. Lớp này kiểm tra
confidence, yêu cầu cử chỉ lặp lại qua nhiều frame, áp dụng cooldown cho
servo, giới hạn tần suất lệnh lái và ưu tiên tuyệt đối lệnh `stop`. Thiết kế
này phân tách trách nhiệm rõ ràng: mạng học sâu giải quyết nhận dạng, còn
logic xác định tính hợp lệ và an toàn của hành động được mô tả bằng quy tắc
có thể kiểm thử.

Vấn đề thứ tư là phụ thuộc mạng khi suy diễn trên cloud. Cloud giúp quản lý
model tập trung và phù hợp với mục tiêu phát triển ứng dụng IoT, nhưng kết
nối mạng có thể xuất hiện jitter, mất gói, lỗi DNS, cold start hoặc timeout.
Một hệ thống điều khiển không được phép giữ nguyên lệnh tiến chỉ vì request
mới chưa trả về. Đề tài giải quyết bằng deadman timeout ở gateway và
firmware: nếu không nhận lệnh hợp lệ trong một khoảng thời gian xác định,
xe phải dừng. Đây là nguyên tắc fail-safe, tức là lỗi truyền thông dẫn hệ
thống về trạng thái ít nguy hiểm hơn thay vì tiếp tục hành động cũ.

## **1.4 Câu hỏi nghiên cứu**

Từ các vấn đề trên, báo cáo đặt ra năm câu hỏi nghiên cứu. Thứ nhất, một
CNN nhẹ dựa trên MobileNetV3Small có thể phân biệt tám trạng thái cử chỉ
trên dữ liệu nội bộ nhiều người với accuracy và macro F1 ở mức nào? Thứ
hai, những cặp lớp nào gây nhầm lẫn chính và nguyên nhân hình ảnh của các
nhầm lẫn đó là gì? Thứ ba, độ trễ online của cloud inference có đủ cho một
mô hình xe điều khiển ở tốc độ thấp hay không? Thứ tư, confidence threshold,
voting và deadman timeout ảnh hưởng thế nào đến độ ổn định của lệnh? Thứ
năm, kiến trúc cloud hiện tại có thể chuyển sang edge inference mà không
thay đổi giao diện giữa gateway và firmware hay không?

Các câu hỏi được trả lời bằng hai nhóm thực nghiệm. Nhóm offline đo chất
lượng mô hình trên tập kiểm tra tách theo người, sử dụng accuracy,
precision, recall, F1 và confusion matrix. Nhóm online đo độ trễ và hành vi
hệ thống qua log gateway, đồng thời kiểm tra các trường hợp confidence
thấp, mất kết nối và lệnh quá hạn. Cách tổ chức này tránh việc kết luận về
khả năng vận hành chỉ từ một chỉ số phân loại.

## **1.5 Đối tượng và phạm vi nghiên cứu**

Đối tượng nghiên cứu là thiết bị điều khiển xe mô hình bằng tám nhãn đầu
vào: `stop`, `peace`, `rock`, `like`, `dislike`, `one`, `two` và
`no_gesture`. Trong chế độ xe, các nhãn được ánh xạ thành dừng, tiến, lùi,
rẽ trái, rẽ phải hoặc chuyển chế độ. Trong chế độ tay máy, một số nhãn được
dùng để chọn khớp và tăng hoặc giảm góc servo. `no_gesture` không tạo lệnh
và được xem là lớp nền quan trọng để giảm kích hoạt giả.

Phạm vi phần cứng gồm webcam RGB, máy tính chạy gateway, dịch vụ suy diễn
cloud, ESP32, mạch điều khiển động cơ L298N và bộ điều khiển servo PCA9685.
L298N được dùng theo trạng thái hiện tại của prototype; trong phiên bản tối
ưu năng lượng có thể thay bằng TB6612FNG để giảm sụt áp và tổn hao. Báo cáo
không tuyên bố xe đạt mức tự hành theo nghĩa phương tiện tự lập kế hoạch
đường đi. Cụm từ “xe tự hành” trong đề tài được hiểu là nền tảng xe robot có
khả năng nhận lệnh thông minh và có thể tích hợp thêm cảm biến tránh vật
cản, encoder hoặc thuật toán lập kế hoạch trong tương lai.

Phạm vi dữ liệu hiện tại gồm 5 người, 570 clip và 8.550 frame. Mô hình chính
là phân loại ảnh crop đơn khung. CNN-LSTM được chuẩn bị như một hướng thực
nghiệm cho cử chỉ động nhưng chưa được dùng để thay thế kết quả baseline.
Báo cáo không đưa ra số liệu của một thí nghiệm chưa chạy; các cấu hình
70/20/10 và 80/20 được mô tả như giao thức đánh giá bổ sung để thực hiện
trên Google Colab hoặc Kaggle.

## **1.6 Phương pháp nghiên cứu**

Đề tài sử dụng phương pháp nghiên cứu thực nghiệm theo vòng lặp. Đầu tiên,
nhóm khảo sát các công trình về HGR, mô hình nhẹ, dữ liệu cử chỉ động và
điều khiển robot để xác định yêu cầu. Tiếp theo, nhóm thiết kế taxonomy tám
nhãn và quy trình thu dữ liệu theo nhiều người. Dữ liệu được kiểm tra bằng
metadata nhằm loại ảnh không phát hiện được bàn tay và hạn chế rò rỉ giữa
train với test.

Sau khi có dữ liệu, MobileNetV3Small pretrained ImageNet được fine-tune cho
tám lớp. Kết quả được phân tích không chỉ bằng accuracy mà còn bằng macro
F1 và ma trận nhầm lẫn. Việc dùng macro F1 là cần thiết vì nó cho mỗi lớp
trọng số ngang nhau, nhờ đó một lớp khó như `one` không bị che khuất bởi
các lớp dễ. Các nghiên cứu về thước đo phân loại cũng khuyến nghị xem xét
precision, recall và F1 theo lớp thay vì chỉ báo cáo một giá trị accuracy
tổng [25], [26].

Cuối cùng, model được đóng gói sau API FastAPI và kết nối với gateway.
Gateway được chạy ở chế độ thật và chế độ dry-run để tách lỗi nhận dạng khỏi
lỗi cơ khí. Log CSV cung cấp dữ liệu định lượng cho phân tích latency. Các
test tự động kiểm tra giao thức, safety policy, API, tiền xử lý và giao diện
gateway. Phương pháp này giúp kết quả có khả năng tái lập tốt hơn một video
demo đơn lẻ.

## **1.7 Ý nghĩa khoa học và thực tiễn**

Về khoa học, đề tài minh họa cách chuyển một mô hình phân loại thị giác
thành hệ thống cyber-physical hoàn chỉnh. Điểm quan trọng không nằm ở việc
đề xuất một kiến trúc mạng hoàn toàn mới mà ở sự kết hợp có kiểm chứng giữa
tiền xử lý bàn tay, mô hình nhẹ, API cloud, logic ổn định lệnh và firmware
fail-safe. Đây là khoảng nối thường bị giản lược trong các báo cáo chỉ tập
trung vào độ chính xác mô hình.

Về thực tiễn, prototype có thể được dùng làm nền tảng giảng dạy cho IoT,
AI, giao thức mạng và hệ thống nhúng. Kiến trúc phân tầng cho phép thay thế
từng thành phần: camera có thể chuyển sang Raspberry Pi Camera; Azure có
thể chuyển sang máy chủ local; L298N có thể chuyển sang TB6612FNG; CNN có
thể chuyển sang CNN-LSTM hoặc model landmark. Miễn là schema request,
response và command được giữ ổn định, các tầng còn lại không cần viết lại
toàn bộ.

# **CHƯƠNG 2. NGHIÊN CỨU LIÊN QUAN**

Các nghiên cứu liên quan được chia thành năm nhóm: tổng quan HGR/HRI,
CNN cho ảnh tĩnh, CNN-LSTM/3D-CNN cho cử chỉ động, landmark/crop bàn tay
và ứng dụng điều khiển robot \[1\], \[2\], \[3\].

CNN trực tiếp trên ảnh crop giữ được thông tin hình dạng bàn tay, còn
landmark giúp giảm chiều dữ liệu. CNN-LSTM hoặc 3D-CNN mạnh hơn với cử
chỉ động nhưng cần dữ liệu video/sequence và chi phí tính toán cao hơn
\[12\], \[13\], \[10\].

Các nghiên cứu robot/mobile robot/robotic arm sử dụng gesture nhấn mạnh
yếu tố real-time và an toàn \[15\], \[16\], \[17\], \[18\]. Điều này phù
hợp với thiết kế gateway chỉ chấp nhận gesture ổn định và firmware tự
dừng khi timeout.

| **Nghiên cứu** | **Nhóm** | **Dữ liệu** | **Mô hình** | **Ưu điểm** | **Hạn chế** | **Liên hệ** |
|:---|:---|:---|:---|:---|:---|:---|
| Jalayer et al. (2026) | Review HGR/HRI | Nhiều nghiên cứu HRI | Deep learning vision-based | Tổng quan rộng | Không phải demo cụ thể | Nền Ch.1-2 |
| Oudah et al. (2020) | Review HGR | Vision-based HGR | Computer vision/ML | Tổng hợp pipeline | Ít tập trung cloud IoT | Pipeline xử lý |
| MediaPipe Hands | Hand tracking | RGB camera | Palm detector + landmark | Real-time | Không phân loại 8 label | Crop/tiền xử lý |
| MobileNetV3 | Backbone nhẹ | ImageNet | NAS + NetAdapt | Tối ưu tài nguyên | Cần fine-tune | CNN baseline |
| Jester Dataset | Dataset gesture | 148k video | 3D CNN baseline | Dataset lớn | Label khác dự án | So sánh dữ liệu |
| Devineau et al. | Skeleton HGR | Skeletal data | Deep learning | Giảm chiều | Cần landmark | Hướng CNN-LSTM |
| Molchanov et al. | Dynamic HGR | Video sequence | Recurrent 3D CNN | Khai thác thời gian | Nặng hơn CNN | Hướng phát triển |
| Hu & Wang | Gesture + UAV | Camera/gesture | Deep learning + control | Liên hệ robot | Khác phần cứng | HRI điều khiển |
| Islam et al. | Robotic arm | Gesture control | Robot arm integration | Gần tay máy | Không cloud DL | Cơ cấu |
| ACM robot control | Robot control | Real-time gesture | Predictive classification | Gần bài toán | Cần full metadata | Real-time |

*Bảng 2.1. So sánh nghiên cứu liên quan*

## **2.1 Nhận dạng cử chỉ tay dựa trên thị giác máy tính**

Pipeline phổ biến gồm thu nhận ảnh, phát hiện bàn tay, tách vùng quan
tâm, trích xuất đặc trưng và phân loại. Chất lượng dữ liệu đầu vào quyết
định đáng kể hiệu năng mô hình. Trong repo hiện tại, MediaPipe crop giảm
nhiễu từ nền trước khi ảnh được resize về 160x160 cho CNN.

## **2.2 CNN, CNN-LSTM và mô hình nhẹ**

MobileNetV3Small phù hợp với mục tiêu mô hình nhẹ và demo thời gian
thực. CNN-LSTM hoặc 3D-CNN phù hợp với gesture động nhưng yêu cầu dữ
liệu chuỗi đầy đủ hơn. Do dataset hiện tại chủ yếu phục vụ gesture
tĩnh/đơn khung, CNN baseline là lựa chọn thực dụng.

## **2.3 Điều khiển robot bằng cử chỉ**

Với robot vật lý, hệ thống cần có lệnh dừng, xử lý mất kết nối và tránh
phát lệnh khi confidence không đủ. Đề tài triển khai các cơ chế này ở
hai lớp: gateway và firmware ESP32.

## **2.4 Khoảng trống nghiên cứu**

Khoảng trống của đề tài là cân bằng giữa accuracy, latency, cloud
deployment và safety. Nhiều nghiên cứu chỉ báo cáo accuracy, trong khi
hệ IoT cần đánh giá cả độ trễ, log online và hành vi khi lỗi mạng.

## **2.5 Nhóm nghiên cứu tổng quan HGR/HRI**

Nhóm nghiên cứu tổng quan giúp xác định bức tranh chung của bài toán. Công
trình của Jalayer và cộng sự tập trung vào hand detection, hand
segmentation và hand gesture recognition trong bối cảnh tương tác
người-robot [1]. Điểm phù hợp với đề tài là cách nhìn HGR như một thành
phần trong hệ HRI, không tách rời khỏi môi trường robot. Bài tổng quan này
cho thấy các mô hình học sâu có thể cải thiện khả năng biểu diễn đặc trưng
so với đặc trưng thủ công, nhưng cũng chỉ ra các vấn đề còn mở như môi
trường phức tạp, dữ liệu ít, khả năng chạy thời gian thực và độ tin cậy khi
robot phản hồi lại người dùng.

Oudah, Al-Naji và Chahl trình bày một tổng quan rộng về nhận dạng cử chỉ
dựa trên thị giác máy tính [2]. Pipeline điển hình gồm phát hiện vùng tay,
tiền xử lý, trích xuất đặc trưng và phân loại. Cách phân rã này gần với
thiết kế của đề tài: MediaPipe đảm nhiệm phát hiện/crop bàn tay, CNN đảm
nhiệm phân loại, gateway đảm nhiệm chuyển dự đoán thành hành động. So với
các pipeline truyền thống, đề tài bổ sung thêm tầng cloud và tầng firmware,
vì vậy phần đánh giá cần vượt ra ngoài accuracy.

Sarma và Bhuyan tổng hợp các phương pháp, database và tiến bộ gần đây của
vision-based HGR cho HCI [3]. Tài liệu này hữu ích khi đặt câu hỏi về dữ
liệu: một bộ dữ liệu tốt cần mô tả người dùng, môi trường, số lớp, cách
chia tập và dạng cử chỉ tĩnh hay động. Dataset nội bộ của đề tài còn nhỏ
nếu so với các database công khai, nhưng có ưu điểm là được thu theo đúng
nhãn điều khiển xe và có metadata theo subject. Điều này phù hợp với mục
tiêu xây dựng prototype, đồng thời cũng bộc lộ hạn chế về khả năng tổng
quát hóa.

Pavlovic, Sharma và Huang là tài liệu nền tảng cũ nhưng vẫn có giá trị vì
đặt HGR vào lịch sử HCI [4]. Trước khi deep learning phổ biến, các hệ thống
thường dựa vào màu da, contour, đặc trưng hình học hoặc mô hình xác suất.
Các phương pháp này giúp hiểu vì sao crop bàn tay và chuẩn hóa ảnh vẫn quan
trọng ngay cả khi dùng CNN. Nếu ảnh đầu vào chứa quá nhiều nền, CNN có thể
học các tương quan không mong muốn thay vì học hình dạng bàn tay.

## **2.6 Nhóm nghiên cứu về landmark và tiền xử lý bàn tay**

MediaPipe Hands là một thành phần quan trọng vì nó giải quyết bài toán phát
hiện bàn tay thời gian thực trên camera RGB [5]. Thay vì gửi toàn bộ frame
camera lên cloud, gateway crop vùng quan tâm quanh bàn tay. Cách làm này có
ba lợi ích. Thứ nhất, kích thước dữ liệu truyền đi nhỏ hơn. Thứ hai, model
ít bị nhiễu bởi nền. Thứ ba, pipeline vẫn có thể chạy trên webcam phổ thông
mà không cần camera depth. Hạn chế là MediaPipe có thể mất tay khi ánh sáng
xấu, tay quá xa camera hoặc bị che khuất. Vì vậy metadata có trường
`found_hand` để phân biệt ảnh crop thành công và ảnh không phát hiện được
tay.

Các hướng dựa trên landmark có thể đi xa hơn crop. Ví dụ, một mô hình có
thể dùng 21 điểm landmark làm đầu vào cho MLP, LSTM hoặc graph neural
network. Ưu điểm là dữ liệu nhỏ, ít phụ thuộc màu da và nền. Nhược điểm là
toàn bộ hệ thống phụ thuộc vào chất lượng landmark; nếu landmark rung hoặc
sai vị trí, model phía sau cũng bị ảnh hưởng. Đề tài chọn ảnh crop làm
baseline để giữ lại thông tin hình dạng bàn tay, đồng thời vẫn để ngỏ hướng
kết hợp landmark trong phiên bản sau.

## **2.7 Nhóm nghiên cứu về CNN nhẹ**

MobileNetV3 được thiết kế bằng kết hợp neural architecture search và
NetAdapt nhằm cân bằng accuracy với độ trễ trên thiết bị tài nguyên hạn chế
[6]. Backbone này phù hợp với đề tài vì input 160x160 và tám lớp không yêu
cầu một mạng rất lớn. Với dữ liệu nội bộ chỉ 8.550 frame, dùng một backbone
pretrained giúp giảm rủi ro overfitting so với huấn luyện CNN sâu từ đầu.
MobileNetV2 cũng là nền tảng quan trọng nhờ inverted residual và linear
bottleneck [7], cung cấp lý do kỹ thuật cho việc dùng các họ MobileNet trong
bài toán cần mô hình nhẹ.

Tuy nhiên, mô hình nhẹ không tự động bảo đảm hệ thống nhẹ. Nếu cloud RTT
lớn hoặc gateway tiền xử lý chậm, tổng latency vẫn cao dù inference của CNN
nhanh. Vì vậy đề tài xem MobileNetV3Small như một lựa chọn hợp lý ở tầng
model, còn toàn bộ pipeline vẫn phải được đo bằng log online. Đây là điểm
khác với các bài chỉ benchmark model trong môi trường offline.

## **2.8 Nhóm nghiên cứu về dữ liệu và cử chỉ động**

Jester Dataset cung cấp một tập video lớn cho nhận dạng cử chỉ tay [8].
Ý nghĩa của Jester đối với đề tài không phải là dùng trực tiếp nhãn của nó
mà là tham chiếu về cách dữ liệu cử chỉ động cần được tổ chức. Một cử chỉ
động không chỉ là một ảnh; nó bao gồm hướng chuyển động, thời điểm bắt đầu,
thời điểm kết thúc và ngữ cảnh trước-sau. Nếu đề tài muốn phân biệt các lệnh
phức tạp hơn, ví dụ vẫy tay sang trái hoặc xoay cổ tay, pipeline phải chuyển
từ single-frame CNN sang sequence model.

Molchanov và cộng sự đề xuất recurrent 3D convolutional neural network cho
online detection và classification của dynamic hand gestures [12]. Điểm
đáng chú ý là bài toán online không thể đợi toàn bộ video kết thúc rồi mới
dự đoán; hệ thống phải đưa ra quyết định sớm. Đây là tư tưởng gần với yêu
cầu điều khiển xe. Tuy nhiên, 3D-CNN thường nặng hơn CNN 2D và yêu cầu dữ
liệu video nhiều hơn. Với dataset hiện tại, dùng 3D-CNN ngay có thể làm hệ
thống phức tạp mà chưa chắc cải thiện kết quả.

Nunez và cộng sự kết hợp CNN với LSTM cho nhận dạng hành động và cử chỉ dựa
trên skeleton [13]. Ý tưởng này phù hợp với hướng phát triển của đề tài:
MediaPipe có thể cung cấp chuỗi landmark, CNN có thể trích đặc trưng ảnh,
LSTM có thể mô hình hóa thay đổi theo thời gian. Repo đã có khung
`train_cnn_lstm.py`, nhưng báo cáo hiện tại không dùng nó làm kết quả chính
vì chưa có thực nghiệm đầy đủ. Đây là cách trình bày thận trọng: nêu hướng
nghiên cứu có cơ sở nhưng không gán số liệu khi chưa chạy.

## **2.9 Nhóm nghiên cứu về điều khiển robot bằng cử chỉ**

Các nghiên cứu điều khiển UAV, robotic arm hoặc mobile robot bằng cử chỉ
cho thấy đầu ra của HGR thường phải qua một tầng ánh xạ lệnh [15]-[20].
Một nhãn cử chỉ không nhất thiết tương ứng trực tiếp với motor; nó có thể
được hiểu khác nhau theo mode, theo trạng thái robot hoặc theo ngữ cảnh an
toàn. Trong đề tài này, `like` là tiến ở chế độ xe nhưng là tăng góc khớp ở
chế độ tay máy. Vì vậy `GestureMapper` phải biết mode hiện tại, còn
`GestureStabilizer` phải quyết định nhãn đó đã đủ tin cậy hay chưa.

Bài về predictive hand gesture classification for real time robot control
của Hu, Xu, Ma và Cao nhấn mạnh yêu cầu dự đoán sớm trong điều khiển robot
[19]. Konda và Konigs nghiên cứu tương tác thời gian thực với mobile robot
bằng cử chỉ [20]. Các hướng này củng cố nhận định rằng độ trễ và độ ổn định
lệnh là thước đo quan trọng. Nếu hệ thống nhận dạng đúng nhưng chậm, người
dùng vẫn cảm thấy khó điều khiển; nếu hệ thống nhận dạng nhanh nhưng rung
lệnh, robot cũng không vận hành tốt.

## **2.10 So sánh và rút ra yêu cầu thiết kế**

Từ các công trình liên quan có thể rút ra năm yêu cầu thiết kế. Thứ nhất,
tiền xử lý phải giảm nhiễu nền nhưng không làm mất thông tin bàn tay. Thứ
hai, model phải đủ nhẹ để phục vụ thời gian thực, đồng thời có khả năng
fine-tune trên dữ liệu nhỏ. Thứ ba, đánh giá offline cần dùng nhiều thước đo
và tránh leakage giữa người dùng. Thứ tư, đánh giá online phải đo latency
đầu-cuối thay vì chỉ đo inference. Thứ năm, mọi dự đoán cần đi qua tầng an
toàn trước khi thành lệnh vật lý.

Bảng 2.1 đã tổng hợp mười nghiên cứu tiêu biểu, nhưng phần phân tích trên
cho thấy không có một công trình đơn lẻ nào giải quyết trọn vẹn bài toán
của đề tài theo đúng bối cảnh môn IoT. Các bài HGR thường mạnh về mô hình
nhưng không bàn sâu firmware. Các bài robot thường có demo điều khiển nhưng
không luôn công bố pipeline cloud hoặc log latency. Các tài liệu cloud/API
giúp triển khai dịch vụ nhưng không thay thế được đánh giá mô hình. Do đó,
đề tài chọn hướng tích hợp: dùng nghiên cứu HGR để thiết kế mô hình, dùng
nghiên cứu robot để thiết kế tầng lệnh, và dùng nguyên tắc IoT để tổ chức
giao tiếp giữa gateway, cloud và ESP32.

# **CHƯƠNG 3. MÔ HÌNH ĐỀ XUẤT**

## **3.1 Sơ đồ mô hình phát hiện và điều khiển**

Mô hình đề xuất kết hợp nhận dạng cử chỉ bằng Deep Learning và điều
khiển IoT theo kiến trúc phân tầng. Webcam và gateway chạy trên laptop,
cloud API đảm nhiệm suy diễn CNN, ESP32 tập trung điều khiển motor và
servo.

Gateway nhận frame từ webcam, crop vùng bàn tay bằng MediaPipe, mã hóa
JPEG và gửi request có session_id/request_id lên Azure API. Cloud trả về
gesture, confidence, inference_ms và model_version. Gateway dùng safety
filter trước khi gửi lệnh WebSocket tới ESP32.

<img src="reports/md_media/media/image1.png"
style="width:6.5in;height:2.6in" />

*Hình 3.1. Kiến trúc hệ thống điều khiển xe tự hành bằng cử chỉ tay*

<img src="reports/md_media/media/image2.png"
style="width:6.5in;height:3.17778in" />

*Hình 3.2. Trình tự xử lý online theo thời gian thực*

## **3.2 Các thành phần của hệ thống**

Tầng dữ liệu gồm data/raw và metadata.csv. Mỗi dòng metadata ghi frame,
subject_id, gesture, clip_id, timestamp, background, lighting, split và
found_hand. Metadata chi tiết giúp kiểm soát subject split và tránh
leakage.

Tầng mô hình gồm script thu dữ liệu, train CNN, train CNN-LSTM định
hướng và benchmark local. Model demo là
gesture-cnn-baseline-s05-partial.keras, nhận ảnh RGB 160x160 và phân
loại 8 nhãn.

Tầng cloud gồm FastAPI, inference và Dockerfile triển khai Azure.
Endpoint /health trả trạng thái, /v1/model trả model_version và
/v1/predict nhận ảnh base64.

Tầng gateway gồm camera capture, MediaPipeCropper, CloudGestureClient,
GestureStabilizer, GestureMapper và transport WebSocket/DryRun. Log CSV
ghi session_id, request_id, capture_ms, preprocess_ms, cloud_rtt_ms,
inference_ms, esp32_ack_ms và total_ms.

Tầng firmware ESP32 gồm HTTP /health, HTTP /state và WebSocket port 81.
Firmware kiểm tra token, sequence và TTL; nếu token sai hoặc quá hạn thì
dừng motor.

| **Label**  | **Ký hiệu**            | **Chế độ xe**         | **Chế độ tay máy** |
|:-----------|:-----------------------|:----------------------|:-------------------|
| stop       | Bàn tay mở             | Dừng xe               | Dừng motor         |
| peace      | Chữ V rộng             | Chuyển chế độ xe      | Chuyển chế độ xe   |
| rock       | Ký hiệu rock           | Chuyển chế độ tay máy | Giữ chế độ tay máy |
| like       | Ngón cái lên           | Tiến                  | Tăng góc khớp 5 độ |
| dislike    | Ngón cái xuống         | Lùi                   | Giảm góc khớp 5 độ |
| one        | Một ngón trỏ           | Rẽ trái               | Chọn khớp trước    |
| two        | Hai ngón               | Rẽ phải               | Chọn khớp tiếp     |
| no_gesture | Không có cử chỉ hợp lệ | Không phát lệnh       | Không phát lệnh    |

*Bảng 3.1. Các lớp cử chỉ và chức năng điều khiển*

<img src="reports/md_media/media/image3.png"
style="width:6.2in;height:2.95909in" />

*Hình 3.3. Một số ảnh mẫu trong bộ dữ liệu cử chỉ*

## **3.3 Bảng tham số model**

| **Tham số**    | **Giá trị**                                            |
|:---------------|:-------------------------------------------------------|
| Tên model      | gesture_cnn_baseline                                   |
| Loại model     | cnn                                                    |
| Backbone       | MobileNetV3Small                                       |
| Pretrained     | ImageNet                                               |
| Kích thước ảnh | 160 x 160                                              |
| Số lớp         | 8                                                      |
| Nhãn           | stop, peace, rock, like, dislike, one, two, no_gesture |
| Epoch          | 10                                                     |
| Batch size     | 16                                                     |
| Split strategy | subject                                                |
| Train/Val/Test | 5400 / 1350 / 1800 frame                               |

*Bảng 3.2. Tham số mô hình CNN baseline*

## **3.4 Công thức, tiêu chí đánh giá và tối ưu**

Softmax chuyển vector logit z thành xác suất lớp: p_i = exp(z_i) / sum_j
exp(z_j). Lớp dự đoán là lớp có xác suất lớn nhất; confidence là xác
suất của lớp được chọn.

Accuracy = số mẫu dự đoán đúng / tổng số mẫu. Precision = TP / (TP +
FP), recall = TP / (TP + FN), F1 = 2 \* precision \* recall /
(precision + recall). Macro F1 là trung bình F1 theo từng lớp.

Latency online được tách thành capture_ms, preprocess_ms, cloud_rtt_ms,
inference_ms, esp32_ack_ms và total_ms. Báo cáo dùng median và p95 vì
log thời gian thực có outlier do cold start, mạng Wi-Fi hoặc container
cloud.

Safety filter yêu cầu confidence tối thiểu và số frame ổn định liên
tiếp. Firmware dùng token để tránh lệnh lạ, sequence để chống lệnh cũ,
TTL để chống lệnh quá hạn và deadman timeout 600 ms để tự dừng motor.

## **3.5 Thiết kế dữ liệu và quy trình thu nhận**

Dữ liệu của đề tài được thiết kế theo đơn vị clip và frame. Một clip là
một lần người dùng thực hiện một cử chỉ trong một khoảng thời gian ngắn;
từ clip đó hệ thống tách ra nhiều frame để huấn luyện mô hình. Cách tổ chức
này phù hợp với quy trình thu thập bằng webcam vì người dùng không cần chụp
từng ảnh thủ công. Đồng thời, metadata theo clip giúp kiểm soát rò rỉ dữ
liệu: nếu frame của cùng một clip xuất hiện đồng thời trong train và test,
kết quả có thể bị lạc quan vì các frame liên tiếp rất giống nhau.

Các trường metadata quan trọng gồm `subject_id`, `gesture`, `clip_id`,
`frame_path`, `timestamp`, `background`, `lighting`, `split` và
`found_hand`. `subject_id` cho biết người thực hiện cử chỉ; `gesture` là
nhãn huấn luyện; `clip_id` liên kết các frame trong cùng lượt quay;
`background` và `lighting` ghi điều kiện thu thập; `found_hand` phản ánh
MediaPipe có phát hiện được bàn tay hay không. Với một báo cáo học thuật,
metadata này quan trọng không kém số lượng ảnh vì nó cho phép người đọc
đánh giá độ tin cậy của giao thức thử nghiệm.

Quy trình thu nhận gồm bốn bước. Bước một, người thực hiện đứng trước
camera ở khoảng cách ổn định và chọn nhãn cần thu. Bước hai, gateway hoặc
script capture ghi video ngắn, lấy frame và lưu ảnh thô. Bước ba, MediaPipe
phát hiện bàn tay và crop vùng quan tâm. Bước bốn, metadata được cập nhật
để lưu đường dẫn ảnh, nhãn và điều kiện thu. Trong quá trình thu, nhóm cần
tránh để cùng một người thực hiện toàn bộ dữ liệu vì model sẽ học đặc điểm
cá nhân của bàn tay. Việc mở rộng subject s06-s10 được xem là ưu tiên cao
trong hướng phát triển.

Dataset hiện tại cân bằng tương đối giữa các lớp chính: `stop`, `rock`,
`like`, `dislike`, `one` và `two` có 1.125 frame mỗi lớp; `peace` và
`no_gesture` có 900 frame mỗi lớp. `no_gesture` là lớp đặc biệt vì nó không
đại diện cho một lệnh mà đại diện cho trạng thái không phát lệnh. Nếu lớp
này quá ít hoặc quá đơn giản, hệ thống có thể kích hoạt giả khi người dùng
không ra lệnh. Vì vậy phiên bản sau cần thu `no_gesture` trong nhiều hoàn
cảnh: không có tay, tay nằm ngoài vùng điều khiển, tay đang chuyển động
chưa thành cử chỉ, và các vật thể có màu hoặc hình dạng gần giống bàn tay.

## **3.6 Tiền xử lý ảnh và chuẩn hóa đầu vào**

Mỗi frame từ camera được xử lý trước khi đưa vào CNN. Nếu gửi nguyên frame
640x480 hoặc 1280x720, mô hình sẽ phải học cả nền, bàn, tường, ánh sáng và
các vật thể xung quanh. Điều này làm tăng nguy cơ overfitting, đặc biệt khi
dataset nhỏ. MediaPipe được dùng để tìm bàn tay và xác định bounding box.
Gateway mở rộng bounding box một khoảng nhỏ để không cắt mất đầu ngón, sau
đó crop ảnh, resize về 160x160 và chuẩn hóa theo yêu cầu của MobileNetV3.

Quá trình resize cần giữ ý nghĩa hình học của cử chỉ. Nếu crop quá chặt,
các lớp như `one` và `two` dễ mất thông tin số ngón. Nếu crop quá rộng,
nền quay lại làm nhiễu mô hình. Trong triển khai hiện tại, mục tiêu là cân
bằng giữa hai lỗi này. Một cải tiến tiếp theo là padding ảnh về hình vuông
trước khi resize để giảm méo tỷ lệ. Một cải tiến khác là lưu thêm landmark
MediaPipe song song với ảnh crop để huấn luyện model đa đầu vào.

Đối với cloud inference, ảnh crop được mã hóa JPEG và gửi qua API dưới dạng
base64. Cách này thuận tiện cho JSON request và dễ debug bằng log, nhưng có
chi phí mã hóa/giải mã. Nếu hệ thống cần tốc độ cao hơn, có thể chuyển sang
multipart upload hoặc gRPC stream. Tuy nhiên, với prototype môn học, JSON
base64 giúp schema rõ ràng và dễ kiểm thử bằng unit test.

## **3.7 Kiến trúc mô hình CNN baseline**

Mô hình chính của đề tài là `gesture_cnn_baseline`, sử dụng
MobileNetV3Small pretrained ImageNet làm backbone. Phần đầu vào nhận ảnh
RGB 160x160. Backbone trích đặc trưng không gian của bàn tay, sau đó phần
classification head ánh xạ đặc trưng sang tám lớp. Optimizer trong script
huấn luyện là Adam, hàm mất mát là sparse categorical cross-entropy và
metric chính khi huấn luyện là accuracy. Kết quả cuối cùng được đánh giá
bổ sung bằng macro F1 và confusion matrix.

Việc dùng pretrained ImageNet có hai lý do. Thứ nhất, các lớp đầu của CNN
học được cạnh, góc, texture và pattern thị giác cơ bản có thể tái sử dụng
cho ảnh bàn tay. Thứ hai, dữ liệu nội bộ chưa đủ lớn để huấn luyện một mô
hình sâu từ đầu. MobileNetV3Small là lựa chọn thỏa hiệp: nhẹ hơn các model
lớn như ResNet50 nhưng vẫn có năng lực biểu diễn tốt hơn một CNN tự thiết
kế rất nông.

Trong báo cáo, CNN baseline không được trình bày như giải pháp tối ưu cuối
cùng. Nó là đường chuẩn có thể chạy, đo được và tích hợp được với cloud.
Các hướng nâng cấp gồm fine-tune nhiều block hơn, dùng augmentation mạnh
hơn, thêm focal loss cho lớp khó, dùng temporal smoothing ở mức feature,
hoặc chuyển sang CNN-LSTM. Mỗi hướng nâng cấp cần đi kèm đánh giá offline
và online, vì tăng accuracy nhưng làm tăng latency quá nhiều có thể không
phù hợp với điều khiển thời gian thực.

## **3.8 Công thức huấn luyện và đánh giá**

Gọi tập dữ liệu huấn luyện là D = {(x_i, y_i)} với x_i là ảnh crop và y_i
là nhãn thuộc một trong tám lớp. Mô hình f_theta tạo ra vector logit z. Xác
suất lớp k được tính bằng softmax:

`p_k = exp(z_k) / sum_j exp(z_j)`

Hàm mất mát sparse categorical cross-entropy cho một mẫu là:

`L_i = -log(p_{y_i})`

Mất mát trung bình trên batch B là:

`L = (1 / |B|) * sum_{i in B} L_i`

Trong suy diễn, nhãn dự đoán là:

`y_hat = argmax_k p_k`

Confidence là `max_k p_k`. Tuy nhiên, confidence của mạng nơ-ron không
phải xác suất đúng tuyệt đối; nó là mức tự tin của model theo phân phối dữ
liệu đã học. Vì vậy gateway không dùng confidence một mình mà kết hợp với
số frame liên tiếp. Nếu model dự đoán `like` với confidence 0,82 trong một
frame nhưng frame kế tiếp chuyển sang `dislike`, gateway không phát lệnh
ngay. Nếu cùng nhãn xuất hiện ổn định trong ba frame liên tiếp và vượt
ngưỡng, lệnh mới được chấp nhận.

Các chỉ số theo lớp được tính như sau. Với một lớp c, TP là số mẫu thuộc c
và được dự đoán c; FP là số mẫu không thuộc c nhưng bị dự đoán c; FN là số
mẫu thuộc c nhưng bị dự đoán sang lớp khác. Khi đó:

`precision_c = TP_c / (TP_c + FP_c)`

`recall_c = TP_c / (TP_c + FN_c)`

`F1_c = 2 * precision_c * recall_c / (precision_c + recall_c)`

Macro F1 là trung bình F1 trên tất cả lớp:

`macro_F1 = (1 / C) * sum_c F1_c`

Với bài toán điều khiển, macro F1 có ý nghĩa hơn accuracy tổng nếu dữ liệu
không hoàn toàn cân bằng hoặc nếu một lớp điều khiển quan trọng bị yếu. Ví
dụ, lớp `stop` cần recall cao vì bỏ sót lệnh dừng nguy hiểm hơn việc nhận
nhầm một frame không quan trọng. Trong triển khai an toàn, `stop` còn được
yêu cầu số frame xác nhận ít hơn lệnh thường để phản hồi nhanh hơn.

## **3.9 Safety filter và bộ ổn định cử chỉ**

Safety filter là cầu nối giữa model và hệ thống điều khiển. Nó nhận
`gesture` và `confidence` từ cloud, sau đó quyết định có phát lệnh hay
không. Chính sách hiện tại gồm bốn tham số chính: `min_confidence = 0.80`,
`mode_min_confidence = 0.60`, số frame liên tiếp cho lệnh thường là 3 và số
frame liên tiếp cho `stop` là 2. `peace` và `rock` là các cử chỉ chuyển mode
nên có ngưỡng riêng thấp hơn để việc chuyển mode không quá khó, nhưng vẫn
phải qua kiểm tra ổn định.

Pseudocode của bộ ổn định có thể mô tả như sau:

```text
Input: gesture, confidence, previous_gesture, stable_count
if gesture is empty or gesture == no_gesture:
    reset stable_count
    return None
threshold = mode_min_confidence if gesture in {peace, rock} else min_confidence
if confidence < threshold:
    reset stable_count
    return None
if gesture == previous_gesture:
    stable_count += 1
else:
    previous_gesture = gesture
    stable_count = 1
required = 2 if gesture == stop else 3
if stable_count >= required:
    return gesture
return None
```

Cơ chế này làm tăng latency quyết định thêm vài frame, nhưng đổi lại giảm
lệnh sai đơn lẻ. Với camera 30 FPS, yêu cầu ba frame liên tiếp tương đương
khoảng 100 ms nếu mọi frame đều xử lý kịp. Trong thực tế, do cloud RTT lớn
hơn thời gian frame, gateway không nhất thiết gửi mọi frame lên cloud. Vì
vậy tham số này cần được cân chỉnh dựa trên log thực tế và cảm giác điều
khiển khi demo.

Ngoài filter ở gateway, firmware cũng có safety riêng. ESP32 kiểm tra token
để tránh client lạ gửi lệnh, kiểm tra sequence để bỏ lệnh cũ, kiểm tra TTL
để bỏ lệnh quá hạn, và dừng xe khi quá deadman timeout. Lý do đặt safety ở
cả gateway lẫn firmware là không tin tuyệt đối vào một tầng duy nhất. Nếu
gateway treo sau khi gửi lệnh tiến, firmware vẫn phải tự dừng. Nếu Wi-Fi
chập chờn, xe không được tiếp tục chạy chỉ vì lệnh cuối cùng vẫn còn trong
bộ nhớ.

## **3.10 Giao thức gateway - cloud - ESP32**

Giao tiếp gateway - cloud dùng HTTP API. Endpoint `/health` trả trạng thái
dịch vụ để kiểm tra container còn sống. Endpoint `/v1/model` trả thông tin
model như `model_version` và danh sách nhãn. Endpoint `/v1/predict` nhận
ảnh và trả dự đoán. Một response điển hình gồm `gesture`, `confidence`,
`inference_ms` và `model_version`. Gateway bổ sung `session_id` và
`request_id` vào log để truy vết mỗi request.

Giao tiếp gateway - ESP32 dùng WebSocket. So với HTTP polling, WebSocket
phù hợp hơn vì gateway có thể đẩy lệnh ngay khi cử chỉ được chấp nhận. Một
message lệnh cần có `seq`, `token`, `command`, `mode`, `joint`, `ttl_ms` và
timestamp. `seq` tăng đơn điệu để firmware bỏ qua lệnh lặp hoặc lệnh đến
muộn. `token` là lớp xác thực đơn giản cho prototype. `ttl_ms` tránh việc
một lệnh bị delay vẫn được thực thi sau khi không còn hợp lệ.

Tầng command mapper chuyển gesture thành hành động. Ví dụ, trong drive mode,
`like` tương ứng `forward`, `dislike` tương ứng `backward`, `one` tương ứng
`left`, `two` tương ứng `right`, `stop` tương ứng `stop`. Trong arm mode,
`one` và `two` chọn khớp, còn `like` và `dislike` tăng/giảm góc khớp. Cách
thiết kế này giúp dùng cùng một mô hình gesture cho nhiều chức năng mà không
cần huấn luyện thêm nhãn.

## **3.11 Triển khai cloud inference**

Cloud service được triển khai bằng FastAPI. Khi container khởi động,
`GestureModel` load file `.keras`, danh sách nhãn và kích thước ảnh. Khi
nhận request, service giải mã ảnh, resize/chuẩn hóa, chạy model và trả về
kết quả. FastAPI phù hợp với prototype vì viết ít mã boilerplate, tự tạo
OpenAPI schema và dễ kiểm thử endpoint. Azure Container Apps phù hợp vì có
thể đóng gói service bằng Docker và triển khai độc lập với gateway.

Một điểm cần chú ý là cold start. Nếu container scale về 0 hoặc lâu không
nhận request, request đầu tiên có thể chậm hơn đáng kể. Báo cáo vì thế tách
warm latency và thảo luận p95 thay vì chỉ dùng median. Trong demo trực tiếp,
nên gọi `/health` hoặc `/v1/model` trước khi bắt đầu để làm nóng container.
Nếu yêu cầu phản hồi liên tục, có thể cấu hình min replicas hoặc chuyển một
phần suy diễn về edge.

Triển khai cloud cũng đặt ra yêu cầu không để lộ secret. Báo cáo không chèn
API key, Wi-Fi password hoặc command token thật. Các giá trị nhạy cảm phải
đặt trong `.env`, secret của nền tảng triển khai hoặc file cấu hình không
commit. Trong markdown này, mọi token chỉ được mô tả như giá trị minh họa.

## **3.12 Tối ưu và cải tiến đề xuất**

Cải tiến đầu tiên là augmentation dữ liệu. Các biến đổi hợp lý gồm thay đổi
độ sáng, contrast, dịch chuyển nhẹ, xoay nhẹ và background đơn giản/phức tạp.
Không nên lật ảnh tùy tiện nếu cử chỉ có ý nghĩa trái-phải, nhưng với bộ
nhãn hiện tại phần lớn cử chỉ không phụ thuộc trái-phải nên có thể thử và
đánh giá. Augmentation phải được áp dụng trên train, không áp dụng trên test
ngoại trừ chuẩn hóa cần thiết.

Cải tiến thứ hai là hiệu chỉnh confidence. Nếu model thường quá tự tin ở
các lớp nhầm, gateway threshold có thể không đủ. Có thể dùng temperature
scaling trên validation set để hiệu chỉnh xác suất, hoặc dùng threshold
riêng cho từng lớp. Ví dụ, nếu `like` có precision thấp vì nhận nhầm nhiều
mẫu khác thành `like`, threshold của `like` có thể cao hơn threshold chung.
Tuy nhiên, threshold riêng cần được kiểm tra bằng confusion matrix và log
thực tế để tránh làm giảm recall quá mức.

Cải tiến thứ ba là temporal model. Thay vì phân loại từng frame độc lập,
gateway có thể gom N frame liên tiếp và gửi batch lên cloud. Cloud tính
trung bình xác suất hoặc dùng CNN-LSTM. Cách trung bình xác suất đơn giản
hơn, dễ triển khai và ít tăng chi phí. CNN-LSTM mạnh hơn với cử chỉ động
nhưng cần dataset theo sequence và thời gian huấn luyện lớn hơn.

Cải tiến thứ tư là edge fallback. Khi cloud lỗi hoặc RTT vượt ngưỡng, gateway
có thể chuyển sang model local. Điều này không mâu thuẫn với yêu cầu cloud
vì cloud vẫn là backend chính; edge chỉ là cơ chế dự phòng. Repo hiện có log
local cho thấy RTT thấp hơn đáng kể, nhưng cần đánh giá lại accuracy và tài
nguyên khi chạy đồng thời với MediaPipe và UI.

# **CHƯƠNG 4. THỰC NGHIỆM, ĐÁNH GIÁ VÀ THẢO LUẬN**

## **4.1 Môi trường thực nghiệm**

Môi trường thực nghiệm gồm laptop Windows chạy gateway và webcam, Azure
Container Apps chạy FastAPI inference, ESP32 kết nối Wi-Fi nhận lệnh
WebSocket, L298N điều khiển motor DC và PCA9685 điều khiển bốn servo tay
máy.

| **Thành phần**  | **Giá trị**                |
|:----------------|:---------------------------|
| Số người        | 5                          |
| Số lớp          | 8                          |
| Số clip         | 570                        |
| Số frame        | 8,550                      |
| Train           | 5,400 frame                |
| Validation      | 1,350 frame                |
| Test            | 1,800 frame                |
| Chiến lược chia | Theo người (subject split) |

*Bảng 4.1. Thống kê dataset*

<img src="reports/md_media/media/image4.png"
style="width:6.3in;height:2.52in" />

*Hình 4.1. Phân bố dữ liệu theo cử chỉ và theo người*

### **4.1.1 Phát hiện thời gian thực (online)**

Azure hiện có 11,179 dòng log; 6,622 dòng có cloud_rtt_ms lớn hơn 0.
Cloud RTT median 158.08 ms và p95 171.58 ms. Inference median 64.01 ms
và p95 74.28 ms.

So với Hugging Face, Azure ổn định hơn trong log hiện tại: Hugging Face
RTT median 338.18 ms và p95 822.99 ms. Local fallback có RTT thấp nhưng
không phản ánh yêu cầu cloud deployment.

| **Provider** | **Rows** | **RTT med** | **RTT p95** | **Infer med** | **Infer p95** | **Total med** | **Total p95** |
|:---|:---|:---|:---|:---|:---|:---|:---|
| Azure | 11179 | 158.08 | 171.58 | 64.01 | 74.28 | 170.38 | 282.89 |
| Hugging Face | 9818 | 338.18 | 822.99 | 76.66 | 105.25 | 18.25 | 396.96 |
| Local | 2900 | 4.61 | 22.18 | 0.07 | 0.07 | 33.94 | 82.41 |

*Bảng 4.3. Thống kê độ trễ online*

<img src="reports/md_media/media/image5.png"
style="width:6in;height:3.38823in" />

*Hình 4.4. So sánh độ trễ cloud RTT*

### **4.1.2 Đánh giá model offline**

Đánh giá offline dùng subject split để tránh data leakage giữa các frame
cùng clip. Số frame train/validation/test là 5,400/1,350/1,800. Nếu cần
báo cáo thêm 70/20/10 hoặc 80/20, cần chạy bổ sung một cấu hình split
khác.

Mô hình đạt accuracy 83.33% và macro F1 83.37%. Các lớp no_gesture,
peace, rock và stop có F1 tương đối cao; one, two, like và dislike còn
nhầm lẫn.

| **Lớp**    | **Precision** | **Recall** | **F1** | **Support** |
|:-----------|:--------------|:-----------|:-------|:------------|
| stop       | 0.979         | 0.831      | 0.899  | 225         |
| peace      | 0.995         | 0.889      | 0.939  | 225         |
| rock       | 0.852         | 0.947      | 0.897  | 225         |
| like       | 0.592         | 0.960      | 0.732  | 225         |
| dislike    | 0.799         | 0.742      | 0.770  | 225         |
| one        | 0.866         | 0.547      | 0.670  | 225         |
| two        | 0.793         | 0.751      | 0.772  | 225         |
| no_gesture | 0.983         | 1.000      | 0.991  | 225         |

*Bảng 4.2. Kết quả đánh giá offline theo lớp*

<img src="reports/md_media/media/image6.png"
style="width:6in;height:3.375in" />

*Hình 4.2. Lịch sử huấn luyện CNN baseline*

<img src="reports/md_media/media/image7.png"
style="width:5.8in;height:5.075in" />

*Hình 4.3. Confusion matrix của CNN MobileNetV3Small*

## **4.2 Thảo luận**

Về accuracy, kết quả 83,33% đủ cho demo nhưng chưa đạt mục tiêu 0,90
macro F1. Các lớp có hình dạng rõ như no_gesture, peace và rock ổn định
hơn; one/two/like/dislike bị ảnh hưởng bởi góc tay và số lượng mẫu.

Về latency, Azure là backend chính hợp lý hơn Hugging Face trong log
hiện tại. Median RTT khoảng 158 ms đủ cho demo nếu gateway dùng
smoothing và không yêu cầu điều khiển tốc độ cao.

Về an toàn, hệ thống có nhiều lớp bảo vệ: không phát lệnh khi confidence
thấp, gửi stop khi cloud lỗi, dùng token/sequence/TTL ở firmware và
deadman timeout.

Về kiến trúc, cloud đúng yêu cầu đề tài nhưng làm tăng phụ thuộc mạng.
Phiên bản edge AI trên laptop hoặc Raspberry Pi có thể giảm RTT, trong
khi cloud vẫn phù hợp cho quản lý model tập trung.

## **4.3 Giao thức thực nghiệm online**

Thực nghiệm online nhằm trả lời câu hỏi: khi người dùng đưa tay trước
camera, hệ thống mất bao lâu để tạo ra dự đoán và lệnh điều khiển? Để đo
được điều này, gateway không chỉ in kết quả lên màn hình mà ghi log CSV cho
mỗi request. Mỗi dòng log là một quan sát gồm thời gian capture, tiền xử lý,
round-trip đến cloud, thời gian inference do cloud báo về, thời gian ACK từ
ESP32 nếu có và tổng thời gian xử lý. Cách ghi log này cho phép phân tích
sau khi demo, thay vì chỉ dựa vào cảm nhận chủ quan.

Quy trình đo online gồm các bước. Bước một, khởi động cloud service và kiểm
tra `/health`. Bước hai, khởi động gateway với đúng URL backend, token và
địa chỉ WebSocket của ESP32. Bước ba, để người dùng thực hiện từng cử chỉ
trong khoảng thời gian đủ dài để gateway ghi nhiều quan sát. Bước bốn, lưu
log vào `reports/gateway_azure_latency.csv`. Bước năm, tính median, p95 và
số dòng hợp lệ. Các request lỗi cần được ghi nhận thay vì bỏ qua âm thầm,
vì tỉ lệ lỗi cũng là một tiêu chí vận hành.

Khi đọc Bảng 4.3, cần phân biệt `cloud_rtt_ms` và `inference_ms`.
`inference_ms` là thời gian model chạy trong cloud container. `cloud_rtt_ms`
bao gồm truyền ảnh lên, xử lý request, inference, serialize response và
truyền kết quả về. Nếu `inference_ms` chỉ khoảng 64 ms nhưng RTT là 158 ms,
phần còn lại đến từ mạng, FastAPI, mã hóa ảnh, container và overhead HTTP.
Vì vậy tối ưu model chỉ giải quyết một phần latency.

Kết quả Azure median RTT 158,08 ms và p95 171,58 ms cho thấy backend tương
đối ổn định trong log hiện tại. Với xe mô hình chạy tốc độ thấp và có
stabilizer, mức này chấp nhận được cho demo. Tuy nhiên, nếu xe chạy nhanh
hoặc cần phản hồi tránh vật cản, cloud RTT này sẽ không đủ; khi đó cảm biến
an toàn và điều khiển khẩn cấp phải nằm ở ESP32 hoặc edge device, không chờ
cloud.

Hugging Face có median RTT 338,18 ms và p95 822,99 ms trong log hiện tại.
Điều này không có nghĩa Hugging Face luôn kém hơn trong mọi trường hợp,
nhưng với cấu hình thử nghiệm của nhóm, nó kém ổn định hơn Azure. Local
fallback có RTT rất thấp, song local không đáp ứng hoàn toàn mục tiêu triển
khai cloud. Kết luận hợp lý là Azure được chọn làm backend chính cho báo cáo,
local được giữ làm baseline kỹ thuật và hướng fallback.

## **4.4 Giao thức thực nghiệm offline**

Thực nghiệm offline nhằm đánh giá năng lực phân loại của model mà không bị
nhiễu bởi mạng, ESP32 hoặc UI. Đầu vào là tập ảnh crop đã chuẩn hóa; đầu ra
là nhãn dự đoán. Kết quả được so với nhãn thật để tính accuracy, precision,
recall, F1 và confusion matrix. Offline evaluation cần được xem là điều kiện
cần nhưng chưa đủ: model offline tốt vẫn có thể tạo trải nghiệm điều khiển
kém nếu latency cao hoặc lệnh rung.

Repo hiện tại dùng `split_strategy = subject`. Đây là cách chia thận trọng
hơn so với random frame split vì test set chứa người không nằm trong train
hoặc validation. Khi chia ngẫu nhiên frame, các frame gần như giống nhau từ
cùng một clip có thể nằm ở cả train và test, làm tăng điểm số một cách
không thực tế. Subject split kiểm tra khả năng tổng quát hóa sang người mới,
phù hợp hơn với ứng dụng thật.

Tỉ lệ hiện tại theo số frame là 5.400 train, 1.350 validation và 1.800 test
trên tổng 8.550 frame. Tỉ lệ này xấp xỉ 63,2% / 15,8% / 21,1%, khác yêu cầu
70/20/10 hoặc 80/20 mà thầy gợi ý. Báo cáo cần ghi rõ điều này để tránh hiểu
nhầm. Subject split được dùng cho kết quả chính vì giảm leakage; 70/20/10
và 80/20 nên được chạy như hai thí nghiệm bổ sung nếu có thời gian.

Giao thức 70/20/10 có thể thực hiện như sau: gom dữ liệu theo `clip_id`,
shuffle có seed cố định, chọn 70% clip cho train, 20% cho test và 10% cho
validation, đảm bảo phân bố nhãn gần cân bằng. Không nên chia theo frame rời
nếu các frame cùng clip rất giống nhau. Giao thức 80/20 có thể bỏ validation
hoặc tách validation từ train bằng cross-validation nội bộ. Nếu huấn luyện
trên Google Colab hoặc Kaggle, cần lưu seed, commit hash, file metadata và
tham số train để kết quả tái lập.

## **4.5 Phân tích kết quả theo lớp**

Kết quả tổng thể accuracy 83,33% và macro F1 83,37% cho thấy model đã học
được đặc trưng chính của tám lớp nhưng chưa đủ mạnh để xem là hoàn thiện.
Lớp `no_gesture` đạt F1 0,991, tức là trạng thái không cử chỉ tương đối dễ
phân biệt trong dữ liệu hiện tại. Tuy nhiên, kết quả này cần được kiểm tra
thêm trong nền phức tạp, vì `no_gesture` ngoài thực tế đa dạng hơn nhiều so
với ảnh không cử chỉ trong dataset.

Lớp `peace` đạt F1 0,939 và `rock` đạt F1 0,897. Đây là các cử chỉ có hình
dạng đặc trưng, số ngón và hướng ngón rõ. Lớp `stop` có precision rất cao
0,979 nhưng recall 0,831, nghĩa là khi model dự đoán stop thì thường đúng,
nhưng vẫn bỏ sót một phần mẫu stop. Với hệ điều khiển, bỏ sót stop là vấn đề
quan trọng. Có thể cân nhắc tăng trọng số lớp stop trong loss hoặc giảm số
frame xác nhận stop như hệ thống hiện đã làm.

Lớp `like` có recall cao 0,960 nhưng precision thấp 0,592. Điều này nghĩa
là hầu hết mẫu like được nhận ra, nhưng nhiều mẫu lớp khác bị kéo về like.
Confusion matrix cho thấy một phần `peace`, `dislike`, `one` và `two` bị
nhận thành `like`. Nguyên nhân có thể là vùng ngón cái hoặc hướng bàn tay
tạo đặc trưng giống nhau khi crop chưa đủ tốt. Với lớp có precision thấp,
threshold riêng hoặc dữ liệu bổ sung là cần thiết.

Lớp `one` có F1 thấp nhất 0,670. Recall 0,547 cho thấy gần một nửa mẫu one
bị nhận sang lớp khác, đặc biệt sang `two`, `dislike`, `rock` hoặc `like`.
Đây là kết quả hợp lý nếu ngón trỏ bị nghiêng, crop thiếu đầu ngón hoặc nền
làm mờ contour. Lớp `two` cũng bị nhầm sang `like` và `one`. Hai lớp này nên
được ưu tiên thu thêm dữ liệu với nhiều góc cổ tay và nhiều khoảng cách.

Lớp `dislike` đạt F1 0,770 và bị nhầm đáng kể sang `like`. Đây là cặp đối
xứng theo hướng ngón cái; nếu camera nhìn từ góc trước và crop không giữ đủ
hướng cổ tay, model có thể nhầm. Một cải tiến là thêm augmentation xoay có
kiểm soát, hoặc dùng landmark để xác định hướng vector ngón cái so với lòng
bàn tay. Nếu chỉ tăng dữ liệu mà không tăng đa dạng góc nhìn, model có thể
vẫn lặp lại lỗi cũ.

## **4.6 Phân tích latency và trải nghiệm điều khiển**

Trong điều khiển thời gian thực, median latency phản ánh trải nghiệm thông
thường, còn p95 phản ánh các thời điểm người dùng có thể cảm thấy khựng.
Với Azure, median RTT khoảng 158 ms và p95 khoảng 172 ms là tương đối ổn.
Tuy nhiên, tổng thời gian `total_ms` có p95 282,89 ms, cao hơn RTT vì còn
bao gồm xử lý gateway và các bước phụ. Nếu cộng thêm yêu cầu nhiều frame ổn
định, thời gian từ cử chỉ mới đến lệnh có thể vượt 300 ms. Đây là mức chấp
nhận được cho xe chạy chậm, nhưng chưa phù hợp với điều khiển tốc độ cao.

Hệ thống có thể giảm cảm giác trễ bằng ba cách. Thứ nhất, không gửi request
quá dày; gateway có thể lấy mẫu frame ở tần suất phù hợp để tránh queue.
Thứ hai, dùng smoothing ở đầu ra để lệnh không đổi liên tục; người dùng sẽ
chấp nhận một độ trễ nhỏ nếu xe phản hồi ổn định. Thứ ba, đặt lệnh an toàn
khẩn cấp ở local: stop do mất kết nối hoặc cảm biến vật cản không được phụ
thuộc cloud.

Khi demo, nên phân biệt hai chế độ. Chế độ cloud chính dùng Azure để thể
hiện đúng yêu cầu IoT và cloud AI. Chế độ local fallback dùng để chứng minh
pipeline vẫn có thể hoạt động khi mạng không ổn định. Nếu thầy yêu cầu so
sánh, bảng latency hiện có đủ để cho thấy trade-off: cloud thuận tiện cho
triển khai và quản lý model, local nhanh hơn nhưng phụ thuộc cấu hình máy
gateway.

## **4.7 Kiểm thử phần mềm và độ tin cậy hệ thống**

Repo hiện tại có kết quả `34 passed`, bao gồm các test cho API, protocol,
safety, preprocessing và UI gateway. Test tự động không thay thế thử nghiệm
phần cứng, nhưng giúp đảm bảo các quy tắc quan trọng không bị hỏng khi sửa
mã. Ví dụ, nếu thay đổi mapping gesture mà làm mất lệnh stop, test có thể
phát hiện sớm. Nếu thay đổi schema log mà thiếu `cloud_rtt_ms`, phân tích
latency sau này sẽ bị ảnh hưởng.

Các nhóm test quan trọng gồm test `/health` và `/v1/model`, test cloud
client parse response, test `GestureStabilizer`, test protocol WebSocket và
test preprocessing. Với hệ IoT, test protocol đặc biệt quan trọng vì lỗi
nhỏ trong JSON command có thể khiến firmware bỏ lệnh hoặc thực thi sai.
Trong phiên bản tiếp theo, nên bổ sung test mô phỏng mất kết nối Wi-Fi,
token sai, sequence cũ, TTL quá hạn và deadman timeout trên firmware bằng
hardware-in-the-loop hoặc mock WebSocket.

## **4.8 So sánh với yêu cầu ban đầu**

So với mục tiêu nhận dạng, hệ thống đã phân loại đủ tám lớp và có kết quả
định lượng. Tuy nhiên, macro F1 83,37% chưa đạt mức kỳ vọng 90%, nên không
nên trình bày như một model hoàn thiện. So với mục tiêu thời gian thực, hệ
thống đã có log online và Azure median RTT ở mức dùng được cho demo. So với
mục tiêu IoT, gateway đã gửi lệnh WebSocket đến ESP32 và firmware có cơ chế
token/sequence/TTL. So với mục tiêu an toàn, hệ thống có threshold,
stabilization và deadman timeout, nhưng vẫn cần thử nghiệm thực địa nhiều
hơn.

Yêu cầu của thầy về 70/20/10 hoặc 80/20 được xử lý bằng cách ghi rõ hiện
trạng và đề xuất thí nghiệm bổ sung. Đây là cách báo cáo trung thực hơn việc
đổi tên subject split thành 70/20/10. Nếu có thời gian chạy lại, nhóm nên
thực hiện hai notebook trên Colab hoặc Kaggle: một notebook 70/20/10 theo
clip stratified, một notebook 80/20 theo clip hoặc subject-aware holdout.
Kết quả bổ sung có thể đưa vào phụ lục hoặc cập nhật Bảng 4.2.

## **4.9 Các mối đe dọa đến tính hợp lệ**

Mối đe dọa thứ nhất là kích thước dataset. Năm người là chưa đủ để kết luận
model tổng quát tốt cho nhiều người dùng. Độ đa dạng về màu da, kích thước
bàn tay, thói quen ra dấu và tốc độ chuyển động còn thấp. Điều này ảnh
hưởng trực tiếp đến các lớp khó như `one` và `two`.

Mối đe dọa thứ hai là điều kiện thu dữ liệu. Nếu phần lớn dữ liệu được thu
trong cùng một phòng, cùng camera và cùng ánh sáng, model có thể học các đặc
trưng môi trường. Khi chuyển sang nền khác, accuracy có thể giảm. Do đó,
phiên bản sau cần chia dữ liệu theo background và lighting, không chỉ theo
subject.

Mối đe dọa thứ ba là đánh giá online phụ thuộc thời điểm mạng. Latency Azure
được đo trên log hiện tại, nhưng có thể thay đổi theo Wi-Fi, khu vực triển
khai, trạng thái container và thời điểm trong ngày. Vì vậy báo cáo không nên
tuyên bố một giá trị latency cố định cho mọi môi trường; cần ghi rõ đây là
kết quả trong điều kiện thử nghiệm của nhóm.

Mối đe dọa thứ tư là cơ khí và nguồn điện. Nếu nguồn motor yếu, ESP32 brownout
hoặc dây nối lỏng, hệ thống có thể lỗi dù model dự đoán đúng. Báo cáo hiện
tập trung vào pipeline phần mềm và giao thức; đánh giá cơ khí chi tiết cần
được bổ sung nếu chuyển prototype thành sản phẩm ổn định.

## **4.10 Đề xuất thực nghiệm bổ sung trên Colab/Kaggle**

Để đáp ứng đầy đủ yêu cầu đánh giá offline, nhóm nên chuẩn bị notebook chạy
trên Google Colab hoặc Kaggle. Notebook cần mount hoặc upload dataset, đọc
metadata, kiểm tra phân bố lớp, tạo split có seed cố định, huấn luyện model,
lưu history, xuất classification report và confusion matrix. Mọi artifact
nên lưu vào `reports/` để báo cáo có thể cập nhật tự động.

Với split 70/20/10, quy trình đề xuất là stratified theo `gesture` ở mức
`clip_id`. Nếu một clip có nhiều frame, toàn bộ frame của clip đi cùng một
tập. Train dùng 70% clip, test 20%, validation 10%. Kết quả nên được báo cáo
song song với subject split, vì hai giao thức trả lời hai câu hỏi khác nhau:
70/20/10 đo hiệu năng khi dữ liệu phân phối tương tự nhau, subject split đo
khả năng tổng quát sang người mới.

Với split 80/20, có hai lựa chọn. Lựa chọn một là train 80%, test 20% và lấy
validation từ một phần train bằng callback validation_split. Lựa chọn hai là
dùng 80/20 nhiều lần với seed khác nhau rồi báo cáo trung bình và độ lệch
chuẩn. Lựa chọn hai đáng tin cậy hơn nhưng tốn thời gian hơn. Nếu dùng
Kaggle, có thể chạy nhiều seed bằng GPU T4; nếu dùng Colab miễn phí, nên
giới hạn epoch hoặc dùng early stopping.

Các kết quả bổ sung cần có cùng định dạng với file metrics hiện tại:
`accuracy`, `macro_f1`, `classification_report`, `confusion_matrix`,
`history`, `image_size`, `epochs_requested` và `batch_size`. Khi format giữ
ổn định, báo cáo có thể tự động đọc và vẽ lại bảng/hình. Đây là cách tốt
hơn việc nhập số liệu thủ công, vì giảm nguy cơ sai lệch giữa code và báo
cáo.

# **KẾT LUẬN, HẠN CHẾ VÀ HƯỚNG PHÁT TRIỂN**

Kết quả đạt được: Nhóm đã xây dựng được hệ thống end-to-end điều khiển
xe/tay máy bằng cử chỉ tay, bao gồm dataset 8 lớp, mô hình CNN
MobileNetV3Small, API FastAPI triển khai trên Azure Container Apps,
gateway xử lý webcam/MediaPipe/safety filter và firmware ESP32 nhận lệnh
WebSocket để điều khiển L298N/PCA9685. Hệ thống có log latency,
session_id/request_id, cơ chế xác thực token, sequence, TTL, deadman
timeout và bộ test tự động hiện chạy 34 passed.

Hạn chế: Mô hình hiện đạt accuracy 83,33% và macro F1 83,37%, chưa đạt
mục tiêu macro F1 0,90. Dataset vẫn còn hạn chế về số người, nền phức
tạp, ánh sáng và các cử chỉ dễ nhầm như one/two/like/dislike. Đánh giá
robustness theo background phức tạp, false activation trên no_gesture và
cấu hình split 70/20/10 hoặc 80/20 chưa được chạy như một thí nghiệm bổ
sung độc lập.

Hướng phát triển: Nhóm cần mở rộng dataset theo nhiều người, nhiều
khoảng cách và nhiều background; huấn luyện/đánh giá CNN-LSTM hoặc mô
hình attention nhẹ cho chuỗi frame; tối ưu cloud cold start và cân nhắc
edge inference để giảm RTT; cải thiện cơ khí, nguồn và chống brownout;
bổ sung dashboard giám sát realtime và quy trình Zotero để quản lý tài
liệu tham khảo theo chuẩn học thuật.

# **TÀI LIỆU THAM KHẢO**

\[1\] R. Jalayer, M. Jalayer, C. Orsenigo, and M. Tomizuka, “A review on
deep learning for vision-based hand detection, hand segmentation and
hand gesture recognition in human-robot interaction,” Robotics and
Computer-Integrated Manufacturing, vol. 97, 103110, 2026. DOI:
10.1016/j.rcim.2025.103110. URL:
https://doi.org/10.1016/j.rcim.2025.103110.

\[2\] M. Oudah, A. Al-Naji, and J. Chahl, “Hand gesture recognition
based on computer vision: a review of techniques,” Journal of Imaging,
vol. 6, no. 8, 73, 2020. DOI: 10.3390/jimaging6080073. URL:
https://doi.org/10.3390/jimaging6080073.

\[3\] D. Sarma and M. K. Bhuyan, “Methods, databases and recent
advancement of vision-based hand gesture recognition for HCI systems: a
review,” SN Computer Science, vol. 2, 436, 2021. DOI:
10.1007/s42979-021-00827-x. URL:
https://doi.org/10.1007/s42979-021-00827-x.

\[4\] V. I. Pavlovic, R. Sharma, and T. S. Huang, “Visual interpretation
of hand gestures for human-computer interaction: a review,” IEEE
Transactions on Pattern Analysis and Machine Intelligence, 1997. DOI:
10.1109/34.598226. URL: https://doi.org/10.1109/34.598226.

\[5\] F. Zhang et al., “MediaPipe Hands: On-device real-time hand
tracking,” arXiv:2006.10214, 2020. URL:
https://arxiv.org/abs/2006.10214.

\[6\] A. Howard et al., “Searching for MobileNetV3,” IEEE/CVF
International Conference on Computer Vision (ICCV), 2019. DOI:
10.1109/ICCV.2019.00140. URL:
https://openaccess.thecvf.com/content_ICCV_2019/html/Howard_Searching_for_MobileNetV3_ICCV_2019_paper.html.

\[7\] M. Sandler, A. Howard, M. Zhu, A. Zhmoginov, and L.-C. Chen,
“MobileNetV2: Inverted residuals and linear bottlenecks,” IEEE/CVF
Conference on Computer Vision and Pattern Recognition (CVPR), 2018. DOI:
10.1109/CVPR.2018.00474. URL: https://doi.org/10.1109/CVPR.2018.00474.

\[8\] J. Materzynska, G. Berger, I. Bax, and R. Memisevic, “The Jester
Dataset: A large-scale video dataset of human gestures,” ICCV Workshops,
2019. URL:
https://openaccess.thecvf.com/content_ICCVW_2019/papers/HANDS/Materzynska_The_Jester_Dataset_A_Large-Scale_Video_Dataset_of_Human_Gestures_ICCVW_2019_paper.pdf.

\[9\] G. Devineau, F. Moutarde, W. Xi, and J. Yang, “Deep learning for
hand gesture recognition on skeletal data,” 13th IEEE International
Conference on Automatic Face & Gesture Recognition, 2018. DOI:
10.1109/FG.2018.00025. URL: https://doi.org/10.1109/FG.2018.00025.

\[10\] Q. De Smedt, H. Wannous, and J.-P. Vandeborre, “Skeleton-based
dynamic hand gesture recognition,” IEEE CVPR Workshops, 2016. DOI:
10.1109/CVPRW.2016.153. URL: https://doi.org/10.1109/CVPRW.2016.153.

\[11\] A. Mujahid et al., “Real-time hand gesture recognition based on
deep learning YOLOv3 model,” Applied Sciences, vol. 11, no. 9, 4164,
2021. DOI: 10.3390/app11094164. URL:
https://doi.org/10.3390/app11094164.

\[12\] P. Molchanov, S. Gupta, K. Kim, and J. Kautz, “Online detection
and classification of dynamic hand gestures with recurrent 3D
convolutional neural networks,” IEEE Conference on Computer Vision and
Pattern Recognition, 2016. DOI: 10.1109/CVPR.2016.454. URL:
https://doi.org/10.1109/CVPR.2016.454.

\[13\] J. C. Nunez et al., “Convolutional neural networks and long
short-term memory for skeleton-based human activity and hand gesture
recognition,” Pattern Recognition, vol. 76, 2018. DOI:
10.1016/j.patcog.2017.10.033. URL:
https://doi.org/10.1016/j.patcog.2017.10.033.

\[14\] F. Khan et al., “3D hand gestures segmentation and optimized
classification using deep learning,” IEEE Access, 2021. DOI:
10.1109/ACCESS.2021.3114871. URL:
https://doi.org/10.1109/ACCESS.2021.3114871.

\[15\] B. Hu and J. Wang, “Deep learning based hand gesture recognition
and UAV flight controls,” 24th International Conference on Automation
and Computing, 2018. DOI: 10.23919/IConAC.2018.8748953. URL:
https://doi.org/10.23919/IConAC.2018.8748953.

\[16\] H. He and Y. Dan, “The research and design of smart mobile
robotic arm based on gesture controlled,” International Conference on
Advanced Mechatronic Systems, 2020. DOI:
10.1109/ICAMechS49982.2020.9310156. URL:
https://doi.org/10.1109/ICAMechS49982.2020.9310156.

\[17\] J. Islam, A. Ghosh, M. I. Iqbal, S. Meem, and N. Ahmad,
“Integration of home assistance with a gesture controlled robotic arm,”
IEEE Region 10 Symposium, 2020. DOI: 10.1109/TENSYMP50017.2020.9230893.
URL: https://doi.org/10.1109/TENSYMP50017.2020.9230893.

\[18\] D. Dissanayake and contributors, “Real-time hand gesture
recognition for robotic arm and home automation,” ACM International
Conference Proceedings, 2021. DOI: 10.1145/3459104.3459142. URL:
https://dl.acm.org/doi/fullHtml/10.1145/3459104.3459142.

\[19\] Y. Hu, J. Xu, Z. Ma, and G. Cao, “Predictive hand gesture
classification for real time robot control,” ACM International
Conference Proceedings, 2018. DOI: 10.1145/3240876.3240914. URL:
https://dl.acm.org/doi/10.1145/3240876.3240914.

\[20\] K. R. Konda and A. Konigs, “Real time interaction with mobile
robots using hand gestures,” ACM International Conference Proceedings,
2012. DOI: 10.1145/2157689.2157743. URL:
https://dl.acm.org/doi/10.1145/2157689.2157743.

\[21\] B. Kwolek, “Continuous hand gesture recognition for human-robot
collaborative assembly,” ICCV Workshop on Assistive Computer Vision and
Robotics, 2023. URL:
https://openaccess.thecvf.com/content/ICCV2023W/ACVR/papers/Kwolek_Continuous_Hand_Gesture_Recognition_for_Human-Robot_Collaborative_Assembly_ICCVW_2023_paper.pdf.

\[22\] R. E. Nogales and M. E. Benalcazar, “Hand gesture recognition
using automatic feature extraction and deep learning algorithms with
memory,” Big Data and Cognitive Computing, vol. 7, no. 2, 102, 2023.
DOI: 10.3390/bdcc7020102. URL: https://doi.org/10.3390/bdcc7020102.

\[23\] S. Skaria, A. Al-Hourani, R. J. Evans, and collaborators,
“Hand-gesture recognition using two-antenna Doppler radar with deep
convolutional neural networks,” IEEE Sensors Journal, vol. 19, no. 8,
2019. DOI: 10.1109/JSEN.2019.2892073. URL:
https://doi.org/10.1109/JSEN.2019.2892073.

\[24\] H. Li et al., “Hand gesture recognition enhancement based on
spatial fuzzy matching in Leap Motion,” IEEE Transactions on Industrial
Informatics, vol. 16, no. 3, 2020. DOI: 10.1109/TII.2019.2931140. URL:
https://doi.org/10.1109/TII.2019.2931140.

\[25\] M. Sokolova and G. Lapalme, “A systematic analysis of performance
measures for classification tasks,” Information Processing & Management,
vol. 45, no. 4, 2009. DOI: 10.1016/j.ipm.2009.03.002. URL:
https://doi.org/10.1016/j.ipm.2009.03.002.

\[26\] D. M. W. Powers, “Evaluation: From precision, recall and
F-measure to ROC, informedness, markedness and correlation,” Journal of
Machine Learning Technologies, vol. 2, no. 1, 2011. URL:
https://www.researchgate.net/publication/228529307.

\[27\] Microsoft, “Azure Container Apps documentation,” Microsoft Learn,
2026. URL: https://learn.microsoft.com/azure/container-apps/.

\[28\] FastAPI contributors, “FastAPI documentation,” FastAPI official
documentation, 2026. URL: https://fastapi.tiangolo.com/.

\[29\] I. Fette and A. Melnikov, “The WebSocket Protocol,” IETF RFC
6455, 2011. DOI: 10.17487/RFC6455. URL:
https://www.rfc-editor.org/rfc/rfc6455.

# **PHỤ LỤC A. KIỂM TRA NGUỒN VÀ QUY TRÌNH ZOTERO**

Phụ lục này đáp ứng lưu ý về bài báo khoa học thuộc danh mục ISI/Scopus.
Khi hoàn thiện bản nộp cuối, nhóm nên import file BibTeX đi kèm vào
Zotero, kiểm tra từng DOI trên publisher page, sau đó đối chiếu
journal/conference trên SCImago, Scopus Sources hoặc Web of Science
Journal Info.

| **\#** | **Nguồn** | **Venue** | **DOI** | **Ghi chú** |
|:---|:---|:---|:---|:---|
| 1 | A review on deep learning for vision-based hand detecti | Robotics and Computer-Integrated Manufacturin | 10.1016/j.rcim.2025.103110 | Elsevier journal; SCImago/WoS page available |
| 2 | Hand gesture recognition based on computer vision: a re | Journal of Imaging, vol. 6, no. 8, 73 | 10.3390/jimaging6080073 | Peer-reviewed journal |
| 3 | Methods, databases and recent advancement of vision-bas | SN Computer Science, vol. 2, 436 | 10.1007/s42979-021-00827-x | Springer journal; index check recommended |
| 4 | Visual interpretation of hand gestures for human-comput | IEEE Transactions on Pattern Analysis and Mac | 10.1109/34.598226 | IEEE journal |
| 5 | MediaPipe Hands: On-device real-time hand tracking | arXiv:2006.10214 | N/A | Technical preprint; foundational implementation |
| 6 | Searching for MobileNetV3 | IEEE/CVF International Conference on Computer | 10.1109/ICCV.2019.00140 | IEEE/CVF conference |
| 7 | MobileNetV2: Inverted residuals and linear bottlenecks | IEEE/CVF Conference on Computer Vision and Pa | 10.1109/CVPR.2018.00474 | IEEE/CVF conference |
| 8 | The Jester Dataset: A large-scale video dataset of huma | ICCV Workshops | N/A | CVF workshop paper |
| 9 | Deep learning for hand gesture recognition on skeletal | 13th IEEE International Conference on Automat | 10.1109/FG.2018.00025 | IEEE conference |
| 10 | Skeleton-based dynamic hand gesture recognition | IEEE CVPR Workshops | 10.1109/CVPRW.2016.153 | IEEE/CVF workshop |
| 11 | Real-time hand gesture recognition based on deep learni | Applied Sciences, vol. 11, no. 9, 4164 | 10.3390/app11094164 | Peer-reviewed journal |
| 12 | Online detection and classification of dynamic hand ges | IEEE Conference on Computer Vision and Patter | 10.1109/CVPR.2016.454 | IEEE/CVF conference |
| 13 | Convolutional neural networks and long short-term memor | Pattern Recognition, vol. 76 | 10.1016/j.patcog.2017.10.033 | Elsevier journal |
| 14 | 3D hand gestures segmentation and optimized classificat | IEEE Access | 10.1109/ACCESS.2021.3114871 | IEEE Access; SCImago page available |
| 15 | Deep learning based hand gesture recognition and UAV fl | 24th International Conference on Automation a | 10.23919/IConAC.2018.8748953 | IEEE-indexed conference |
| 16 | The research and design of smart mobile robotic arm bas | International Conference on Advanced Mechatro | 10.1109/ICAMechS49982.2020.9310156 | IEEE conference |
| 17 | Integration of home assistance with a gesture controlle | IEEE Region 10 Symposium | 10.1109/TENSYMP50017.2020.9230893 | IEEE conference |
| 18 | Real-time hand gesture recognition for robotic arm and | ACM International Conference Proceedings | 10.1145/3459104.3459142 | ACM conference |
| 19 | Predictive hand gesture classification for real time ro | ACM International Conference Proceedings | 10.1145/3240876.3240914 | ACM conference |
| 20 | Real time interaction with mobile robots using hand ges | ACM International Conference Proceedings | 10.1145/2157689.2157743 | ACM conference |
| 21 | Continuous hand gesture recognition for human-robot col | ICCV Workshop on Assistive Computer Vision an | N/A | CVF workshop |
| 22 | Hand gesture recognition using automatic feature extrac | Big Data and Cognitive Computing, vol. 7, no. | 10.3390/bdcc7020102 | Peer-reviewed journal |
| 23 | Hand-gesture recognition using two-antenna Doppler rada | IEEE Sensors Journal, vol. 19, no. 8 | 10.1109/JSEN.2019.2892073 | IEEE journal |
| 24 | Hand gesture recognition enhancement based on spatial f | IEEE Transactions on Industrial Informatics, | 10.1109/TII.2019.2931140 | IEEE journal |
| 25 | A systematic analysis of performance measures for class | Information Processing & Management, vol. 45, | 10.1016/j.ipm.2009.03.002 | Elsevier journal |
| 26 | Evaluation: From precision, recall and F-measure to ROC | Journal of Machine Learning Technologies, vol | N/A | Evaluation reference; index check recommended |
| 27 | Azure Container Apps documentation | Microsoft Learn | N/A | Technical documentation |
| 28 | FastAPI documentation | FastAPI official documentation | N/A | Technical documentation |
| 29 | The WebSocket Protocol | IETF RFC 6455 | 10.17487/RFC6455 | IETF standard |

## **A.1 Phiếu nguồn \[1\]**

Tên nguồn: A review on deep learning for vision-based hand detection,
hand segmentation and hand gesture recognition in human-robot
interaction

Tác giả/năm: R. Jalayer, M. Jalayer, C. Orsenigo, and M. Tomizuka
(2026). Venue: Robotics and Computer-Integrated Manufacturing, vol. 97,
103110. DOI/URL: 10.1016/j.rcim.2025.103110.

Lý do dùng trong báo cáo: nguồn này hỗ trợ phần nền tảng HGR/HRI; ghi
chú kiểm tra: Elsevier journal; SCImago/WoS page available.

Các trường cần rà soát trong Zotero trước khi nộp: tên tác giả đầy đủ,
tiêu đề, năm, volume/issue, trang, DOI, publisher và loại tài liệu. Với
journal, đối chiếu ISSN/venue trên SCImago, Scopus Sources hoặc Web of
Science Journal Info; với conference, đối chiếu trang IEEE Xplore, ACM
DL hoặc CVF chính thức.

Cách sử dụng trong báo cáo: không trích nguyên văn dài; diễn giải kết
quả liên quan bằng lời của nhóm và đặt số trích dẫn IEEE ở cuối nhận
định. ResearchGate chỉ dùng để tìm bản đọc, không dùng làm bằng chứng
xác nhận chỉ mục.

## **A.2 Phiếu nguồn \[2\]**

Tên nguồn: Hand gesture recognition based on computer vision: a review
of techniques

Tác giả/năm: M. Oudah, A. Al-Naji, and J. Chahl (2020). Venue: Journal
of Imaging, vol. 6, no. 8, 73. DOI/URL: 10.3390/jimaging6080073.

Lý do dùng trong báo cáo: nguồn này hỗ trợ phần nền tảng HGR/HRI; ghi
chú kiểm tra: Peer-reviewed journal.

Các trường cần rà soát trong Zotero trước khi nộp: tên tác giả đầy đủ,
tiêu đề, năm, volume/issue, trang, DOI, publisher và loại tài liệu. Với
journal, đối chiếu ISSN/venue trên SCImago, Scopus Sources hoặc Web of
Science Journal Info; với conference, đối chiếu trang IEEE Xplore, ACM
DL hoặc CVF chính thức.

Cách sử dụng trong báo cáo: không trích nguyên văn dài; diễn giải kết
quả liên quan bằng lời của nhóm và đặt số trích dẫn IEEE ở cuối nhận
định. ResearchGate chỉ dùng để tìm bản đọc, không dùng làm bằng chứng
xác nhận chỉ mục.

## **A.3 Phiếu nguồn \[3\]**

Tên nguồn: Methods, databases and recent advancement of vision-based
hand gesture recognition for HCI systems: a review

Tác giả/năm: D. Sarma and M. K. Bhuyan (2021). Venue: SN Computer
Science, vol. 2, 436. DOI/URL: 10.1007/s42979-021-00827-x.

Lý do dùng trong báo cáo: nguồn này hỗ trợ phần nền tảng HGR/HRI; ghi
chú kiểm tra: Springer journal; index check recommended.

Các trường cần rà soát trong Zotero trước khi nộp: tên tác giả đầy đủ,
tiêu đề, năm, volume/issue, trang, DOI, publisher và loại tài liệu. Với
journal, đối chiếu ISSN/venue trên SCImago, Scopus Sources hoặc Web of
Science Journal Info; với conference, đối chiếu trang IEEE Xplore, ACM
DL hoặc CVF chính thức.

Cách sử dụng trong báo cáo: không trích nguyên văn dài; diễn giải kết
quả liên quan bằng lời của nhóm và đặt số trích dẫn IEEE ở cuối nhận
định. ResearchGate chỉ dùng để tìm bản đọc, không dùng làm bằng chứng
xác nhận chỉ mục.

## **A.4 Phiếu nguồn \[4\]**

Tên nguồn: Visual interpretation of hand gestures for human-computer
interaction: a review

Tác giả/năm: V. I. Pavlovic, R. Sharma, and T. S. Huang (1997). Venue:
IEEE Transactions on Pattern Analysis and Machine Intelligence. DOI/URL:
10.1109/34.598226.

Lý do dùng trong báo cáo: nguồn này hỗ trợ phần nền tảng HGR/HRI; ghi
chú kiểm tra: IEEE journal.

Các trường cần rà soát trong Zotero trước khi nộp: tên tác giả đầy đủ,
tiêu đề, năm, volume/issue, trang, DOI, publisher và loại tài liệu. Với
journal, đối chiếu ISSN/venue trên SCImago, Scopus Sources hoặc Web of
Science Journal Info; với conference, đối chiếu trang IEEE Xplore, ACM
DL hoặc CVF chính thức.

Cách sử dụng trong báo cáo: không trích nguyên văn dài; diễn giải kết
quả liên quan bằng lời của nhóm và đặt số trích dẫn IEEE ở cuối nhận
định. ResearchGate chỉ dùng để tìm bản đọc, không dùng làm bằng chứng
xác nhận chỉ mục.

## **A.5 Phiếu nguồn \[5\]**

Tên nguồn: MediaPipe Hands: On-device real-time hand tracking

Tác giả/năm: F. Zhang et al. (2020). Venue: arXiv:2006.10214. DOI/URL:
https://arxiv.org/abs/2006.10214.

Lý do dùng trong báo cáo: nguồn này hỗ trợ phần mô hình, dữ liệu hoặc
triển khai; ghi chú kiểm tra: Technical preprint; foundational
implementation.

Các trường cần rà soát trong Zotero trước khi nộp: tên tác giả đầy đủ,
tiêu đề, năm, volume/issue, trang, DOI, publisher và loại tài liệu. Với
journal, đối chiếu ISSN/venue trên SCImago, Scopus Sources hoặc Web of
Science Journal Info; với conference, đối chiếu trang IEEE Xplore, ACM
DL hoặc CVF chính thức.

Cách sử dụng trong báo cáo: không trích nguyên văn dài; diễn giải kết
quả liên quan bằng lời của nhóm và đặt số trích dẫn IEEE ở cuối nhận
định. ResearchGate chỉ dùng để tìm bản đọc, không dùng làm bằng chứng
xác nhận chỉ mục.

## **A.6 Phiếu nguồn \[6\]**

Tên nguồn: Searching for MobileNetV3

Tác giả/năm: A. Howard et al. (2019). Venue: IEEE/CVF International
Conference on Computer Vision (ICCV). DOI/URL: 10.1109/ICCV.2019.00140.

Lý do dùng trong báo cáo: nguồn này hỗ trợ phần mô hình, dữ liệu hoặc
triển khai; ghi chú kiểm tra: IEEE/CVF conference.

Các trường cần rà soát trong Zotero trước khi nộp: tên tác giả đầy đủ,
tiêu đề, năm, volume/issue, trang, DOI, publisher và loại tài liệu. Với
journal, đối chiếu ISSN/venue trên SCImago, Scopus Sources hoặc Web of
Science Journal Info; với conference, đối chiếu trang IEEE Xplore, ACM
DL hoặc CVF chính thức.

Cách sử dụng trong báo cáo: không trích nguyên văn dài; diễn giải kết
quả liên quan bằng lời của nhóm và đặt số trích dẫn IEEE ở cuối nhận
định. ResearchGate chỉ dùng để tìm bản đọc, không dùng làm bằng chứng
xác nhận chỉ mục.

## **A.7 Phiếu nguồn \[7\]**

Tên nguồn: MobileNetV2: Inverted residuals and linear bottlenecks

Tác giả/năm: M. Sandler, A. Howard, M. Zhu, A. Zhmoginov, and L.-C. Chen
(2018). Venue: IEEE/CVF Conference on Computer Vision and Pattern
Recognition (CVPR). DOI/URL: 10.1109/CVPR.2018.00474.

Lý do dùng trong báo cáo: nguồn này hỗ trợ phần mô hình, dữ liệu hoặc
triển khai; ghi chú kiểm tra: IEEE/CVF conference.

Các trường cần rà soát trong Zotero trước khi nộp: tên tác giả đầy đủ,
tiêu đề, năm, volume/issue, trang, DOI, publisher và loại tài liệu. Với
journal, đối chiếu ISSN/venue trên SCImago, Scopus Sources hoặc Web of
Science Journal Info; với conference, đối chiếu trang IEEE Xplore, ACM
DL hoặc CVF chính thức.

Cách sử dụng trong báo cáo: không trích nguyên văn dài; diễn giải kết
quả liên quan bằng lời của nhóm và đặt số trích dẫn IEEE ở cuối nhận
định. ResearchGate chỉ dùng để tìm bản đọc, không dùng làm bằng chứng
xác nhận chỉ mục.

## **A.8 Phiếu nguồn \[8\]**

Tên nguồn: The Jester Dataset: A large-scale video dataset of human
gestures

Tác giả/năm: J. Materzynska, G. Berger, I. Bax, and R. Memisevic (2019).
Venue: ICCV Workshops. DOI/URL:
https://openaccess.thecvf.com/content_ICCVW_2019/papers/HANDS/Materzynska_The_Jester_Dataset_A_Large-Scale_Video_Dataset_of_Human_Gestures_ICCVW_2019_paper.pdf.

Lý do dùng trong báo cáo: nguồn này hỗ trợ phần mô hình, dữ liệu hoặc
triển khai; ghi chú kiểm tra: CVF workshop paper.

Các trường cần rà soát trong Zotero trước khi nộp: tên tác giả đầy đủ,
tiêu đề, năm, volume/issue, trang, DOI, publisher và loại tài liệu. Với
journal, đối chiếu ISSN/venue trên SCImago, Scopus Sources hoặc Web of
Science Journal Info; với conference, đối chiếu trang IEEE Xplore, ACM
DL hoặc CVF chính thức.

Cách sử dụng trong báo cáo: không trích nguyên văn dài; diễn giải kết
quả liên quan bằng lời của nhóm và đặt số trích dẫn IEEE ở cuối nhận
định. ResearchGate chỉ dùng để tìm bản đọc, không dùng làm bằng chứng
xác nhận chỉ mục.

## **A.9 Phiếu nguồn \[9\]**

Tên nguồn: Deep learning for hand gesture recognition on skeletal data

Tác giả/năm: G. Devineau, F. Moutarde, W. Xi, and J. Yang (2018). Venue:
13th IEEE International Conference on Automatic Face & Gesture
Recognition. DOI/URL: 10.1109/FG.2018.00025.

Lý do dùng trong báo cáo: nguồn này hỗ trợ phần mô hình, dữ liệu hoặc
triển khai; ghi chú kiểm tra: IEEE conference.

Các trường cần rà soát trong Zotero trước khi nộp: tên tác giả đầy đủ,
tiêu đề, năm, volume/issue, trang, DOI, publisher và loại tài liệu. Với
journal, đối chiếu ISSN/venue trên SCImago, Scopus Sources hoặc Web of
Science Journal Info; với conference, đối chiếu trang IEEE Xplore, ACM
DL hoặc CVF chính thức.

Cách sử dụng trong báo cáo: không trích nguyên văn dài; diễn giải kết
quả liên quan bằng lời của nhóm và đặt số trích dẫn IEEE ở cuối nhận
định. ResearchGate chỉ dùng để tìm bản đọc, không dùng làm bằng chứng
xác nhận chỉ mục.

## **A.10 Phiếu nguồn \[10\]**

Tên nguồn: Skeleton-based dynamic hand gesture recognition

Tác giả/năm: Q. De Smedt, H. Wannous, and J.-P. Vandeborre (2016).
Venue: IEEE CVPR Workshops. DOI/URL: 10.1109/CVPRW.2016.153.

Lý do dùng trong báo cáo: nguồn này hỗ trợ phần mô hình, dữ liệu hoặc
triển khai; ghi chú kiểm tra: IEEE/CVF workshop.

Các trường cần rà soát trong Zotero trước khi nộp: tên tác giả đầy đủ,
tiêu đề, năm, volume/issue, trang, DOI, publisher và loại tài liệu. Với
journal, đối chiếu ISSN/venue trên SCImago, Scopus Sources hoặc Web of
Science Journal Info; với conference, đối chiếu trang IEEE Xplore, ACM
DL hoặc CVF chính thức.

Cách sử dụng trong báo cáo: không trích nguyên văn dài; diễn giải kết
quả liên quan bằng lời của nhóm và đặt số trích dẫn IEEE ở cuối nhận
định. ResearchGate chỉ dùng để tìm bản đọc, không dùng làm bằng chứng
xác nhận chỉ mục.

## **A.11 Phiếu nguồn \[11\]**

Tên nguồn: Real-time hand gesture recognition based on deep learning
YOLOv3 model

Tác giả/năm: A. Mujahid et al. (2021). Venue: Applied Sciences, vol. 11,
no. 9, 4164. DOI/URL: 10.3390/app11094164.

Lý do dùng trong báo cáo: nguồn này hỗ trợ phần mô hình, dữ liệu hoặc
triển khai; ghi chú kiểm tra: Peer-reviewed journal.

Các trường cần rà soát trong Zotero trước khi nộp: tên tác giả đầy đủ,
tiêu đề, năm, volume/issue, trang, DOI, publisher và loại tài liệu. Với
journal, đối chiếu ISSN/venue trên SCImago, Scopus Sources hoặc Web of
Science Journal Info; với conference, đối chiếu trang IEEE Xplore, ACM
DL hoặc CVF chính thức.

Cách sử dụng trong báo cáo: không trích nguyên văn dài; diễn giải kết
quả liên quan bằng lời của nhóm và đặt số trích dẫn IEEE ở cuối nhận
định. ResearchGate chỉ dùng để tìm bản đọc, không dùng làm bằng chứng
xác nhận chỉ mục.

## **A.12 Phiếu nguồn \[12\]**

Tên nguồn: Online detection and classification of dynamic hand gestures
with recurrent 3D convolutional neural networks

Tác giả/năm: P. Molchanov, S. Gupta, K. Kim, and J. Kautz (2016). Venue:
IEEE Conference on Computer Vision and Pattern Recognition. DOI/URL:
10.1109/CVPR.2016.454.

Lý do dùng trong báo cáo: nguồn này hỗ trợ phần mô hình, dữ liệu hoặc
triển khai; ghi chú kiểm tra: IEEE/CVF conference.

Các trường cần rà soát trong Zotero trước khi nộp: tên tác giả đầy đủ,
tiêu đề, năm, volume/issue, trang, DOI, publisher và loại tài liệu. Với
journal, đối chiếu ISSN/venue trên SCImago, Scopus Sources hoặc Web of
Science Journal Info; với conference, đối chiếu trang IEEE Xplore, ACM
DL hoặc CVF chính thức.

Cách sử dụng trong báo cáo: không trích nguyên văn dài; diễn giải kết
quả liên quan bằng lời của nhóm và đặt số trích dẫn IEEE ở cuối nhận
định. ResearchGate chỉ dùng để tìm bản đọc, không dùng làm bằng chứng
xác nhận chỉ mục.

## **A.13 Phiếu nguồn \[13\]**

Tên nguồn: Convolutional neural networks and long short-term memory for
skeleton-based human activity and hand gesture recognition

Tác giả/năm: J. C. Nunez et al. (2018). Venue: Pattern Recognition, vol.
76. DOI/URL: 10.1016/j.patcog.2017.10.033.

Lý do dùng trong báo cáo: nguồn này hỗ trợ phần mô hình, dữ liệu hoặc
triển khai; ghi chú kiểm tra: Elsevier journal.

Các trường cần rà soát trong Zotero trước khi nộp: tên tác giả đầy đủ,
tiêu đề, năm, volume/issue, trang, DOI, publisher và loại tài liệu. Với
journal, đối chiếu ISSN/venue trên SCImago, Scopus Sources hoặc Web of
Science Journal Info; với conference, đối chiếu trang IEEE Xplore, ACM
DL hoặc CVF chính thức.

Cách sử dụng trong báo cáo: không trích nguyên văn dài; diễn giải kết
quả liên quan bằng lời của nhóm và đặt số trích dẫn IEEE ở cuối nhận
định. ResearchGate chỉ dùng để tìm bản đọc, không dùng làm bằng chứng
xác nhận chỉ mục.

## **A.14 Phiếu nguồn \[14\]**

Tên nguồn: 3D hand gestures segmentation and optimized classification
using deep learning

Tác giả/năm: F. Khan et al. (2021). Venue: IEEE Access. DOI/URL:
10.1109/ACCESS.2021.3114871.

Lý do dùng trong báo cáo: nguồn này hỗ trợ phần mô hình, dữ liệu hoặc
triển khai; ghi chú kiểm tra: IEEE Access; SCImago page available.

Các trường cần rà soát trong Zotero trước khi nộp: tên tác giả đầy đủ,
tiêu đề, năm, volume/issue, trang, DOI, publisher và loại tài liệu. Với
journal, đối chiếu ISSN/venue trên SCImago, Scopus Sources hoặc Web of
Science Journal Info; với conference, đối chiếu trang IEEE Xplore, ACM
DL hoặc CVF chính thức.

Cách sử dụng trong báo cáo: không trích nguyên văn dài; diễn giải kết
quả liên quan bằng lời của nhóm và đặt số trích dẫn IEEE ở cuối nhận
định. ResearchGate chỉ dùng để tìm bản đọc, không dùng làm bằng chứng
xác nhận chỉ mục.

## **A.15 Phiếu nguồn \[15\]**

Tên nguồn: Deep learning based hand gesture recognition and UAV flight
controls

Tác giả/năm: B. Hu and J. Wang (2018). Venue: 24th International
Conference on Automation and Computing. DOI/URL:
10.23919/IConAC.2018.8748953.

Lý do dùng trong báo cáo: nguồn này hỗ trợ phần mô hình, dữ liệu hoặc
triển khai; ghi chú kiểm tra: IEEE-indexed conference.

Các trường cần rà soát trong Zotero trước khi nộp: tên tác giả đầy đủ,
tiêu đề, năm, volume/issue, trang, DOI, publisher và loại tài liệu. Với
journal, đối chiếu ISSN/venue trên SCImago, Scopus Sources hoặc Web of
Science Journal Info; với conference, đối chiếu trang IEEE Xplore, ACM
DL hoặc CVF chính thức.

Cách sử dụng trong báo cáo: không trích nguyên văn dài; diễn giải kết
quả liên quan bằng lời của nhóm và đặt số trích dẫn IEEE ở cuối nhận
định. ResearchGate chỉ dùng để tìm bản đọc, không dùng làm bằng chứng
xác nhận chỉ mục.

## **A.16 Phiếu nguồn \[16\]**

Tên nguồn: The research and design of smart mobile robotic arm based on
gesture controlled

Tác giả/năm: H. He and Y. Dan (2020). Venue: International Conference on
Advanced Mechatronic Systems. DOI/URL:
10.1109/ICAMechS49982.2020.9310156.

Lý do dùng trong báo cáo: nguồn này hỗ trợ phần mô hình, dữ liệu hoặc
triển khai; ghi chú kiểm tra: IEEE conference.

Các trường cần rà soát trong Zotero trước khi nộp: tên tác giả đầy đủ,
tiêu đề, năm, volume/issue, trang, DOI, publisher và loại tài liệu. Với
journal, đối chiếu ISSN/venue trên SCImago, Scopus Sources hoặc Web of
Science Journal Info; với conference, đối chiếu trang IEEE Xplore, ACM
DL hoặc CVF chính thức.

Cách sử dụng trong báo cáo: không trích nguyên văn dài; diễn giải kết
quả liên quan bằng lời của nhóm và đặt số trích dẫn IEEE ở cuối nhận
định. ResearchGate chỉ dùng để tìm bản đọc, không dùng làm bằng chứng
xác nhận chỉ mục.

## **A.17 Phiếu nguồn \[17\]**

Tên nguồn: Integration of home assistance with a gesture controlled
robotic arm

Tác giả/năm: J. Islam, A. Ghosh, M. I. Iqbal, S. Meem, and N. Ahmad
(2020). Venue: IEEE Region 10 Symposium. DOI/URL:
10.1109/TENSYMP50017.2020.9230893.

Lý do dùng trong báo cáo: nguồn này hỗ trợ phần mô hình, dữ liệu hoặc
triển khai; ghi chú kiểm tra: IEEE conference.

Các trường cần rà soát trong Zotero trước khi nộp: tên tác giả đầy đủ,
tiêu đề, năm, volume/issue, trang, DOI, publisher và loại tài liệu. Với
journal, đối chiếu ISSN/venue trên SCImago, Scopus Sources hoặc Web of
Science Journal Info; với conference, đối chiếu trang IEEE Xplore, ACM
DL hoặc CVF chính thức.

Cách sử dụng trong báo cáo: không trích nguyên văn dài; diễn giải kết
quả liên quan bằng lời của nhóm và đặt số trích dẫn IEEE ở cuối nhận
định. ResearchGate chỉ dùng để tìm bản đọc, không dùng làm bằng chứng
xác nhận chỉ mục.

## **A.18 Phiếu nguồn \[18\]**

Tên nguồn: Real-time hand gesture recognition for robotic arm and home
automation

Tác giả/năm: D. Dissanayake and contributors (2021). Venue: ACM
International Conference Proceedings. DOI/URL: 10.1145/3459104.3459142.

Lý do dùng trong báo cáo: nguồn này hỗ trợ phần mô hình, dữ liệu hoặc
triển khai; ghi chú kiểm tra: ACM conference.

Các trường cần rà soát trong Zotero trước khi nộp: tên tác giả đầy đủ,
tiêu đề, năm, volume/issue, trang, DOI, publisher và loại tài liệu. Với
journal, đối chiếu ISSN/venue trên SCImago, Scopus Sources hoặc Web of
Science Journal Info; với conference, đối chiếu trang IEEE Xplore, ACM
DL hoặc CVF chính thức.

Cách sử dụng trong báo cáo: không trích nguyên văn dài; diễn giải kết
quả liên quan bằng lời của nhóm và đặt số trích dẫn IEEE ở cuối nhận
định. ResearchGate chỉ dùng để tìm bản đọc, không dùng làm bằng chứng
xác nhận chỉ mục.

## **A.19 Phiếu nguồn \[19\]**

Tên nguồn: Predictive hand gesture classification for real time robot
control

Tác giả/năm: Y. Hu, J. Xu, Z. Ma, and G. Cao (2018). Venue: ACM
International Conference Proceedings. DOI/URL: 10.1145/3240876.3240914.

Lý do dùng trong báo cáo: nguồn này hỗ trợ phần mô hình, dữ liệu hoặc
triển khai; ghi chú kiểm tra: ACM conference.

Các trường cần rà soát trong Zotero trước khi nộp: tên tác giả đầy đủ,
tiêu đề, năm, volume/issue, trang, DOI, publisher và loại tài liệu. Với
journal, đối chiếu ISSN/venue trên SCImago, Scopus Sources hoặc Web of
Science Journal Info; với conference, đối chiếu trang IEEE Xplore, ACM
DL hoặc CVF chính thức.

Cách sử dụng trong báo cáo: không trích nguyên văn dài; diễn giải kết
quả liên quan bằng lời của nhóm và đặt số trích dẫn IEEE ở cuối nhận
định. ResearchGate chỉ dùng để tìm bản đọc, không dùng làm bằng chứng
xác nhận chỉ mục.

## **A.20 Phiếu nguồn \[20\]**

Tên nguồn: Real time interaction with mobile robots using hand gestures

Tác giả/năm: K. R. Konda and A. Konigs (2012). Venue: ACM International
Conference Proceedings. DOI/URL: 10.1145/2157689.2157743.

Lý do dùng trong báo cáo: nguồn này hỗ trợ phần mô hình, dữ liệu hoặc
triển khai; ghi chú kiểm tra: ACM conference.

Các trường cần rà soát trong Zotero trước khi nộp: tên tác giả đầy đủ,
tiêu đề, năm, volume/issue, trang, DOI, publisher và loại tài liệu. Với
journal, đối chiếu ISSN/venue trên SCImago, Scopus Sources hoặc Web of
Science Journal Info; với conference, đối chiếu trang IEEE Xplore, ACM
DL hoặc CVF chính thức.

Cách sử dụng trong báo cáo: không trích nguyên văn dài; diễn giải kết
quả liên quan bằng lời của nhóm và đặt số trích dẫn IEEE ở cuối nhận
định. ResearchGate chỉ dùng để tìm bản đọc, không dùng làm bằng chứng
xác nhận chỉ mục.

## **A.21 Phiếu nguồn \[21\]**

Tên nguồn: Continuous hand gesture recognition for human-robot
collaborative assembly

Tác giả/năm: B. Kwolek (2023). Venue: ICCV Workshop on Assistive
Computer Vision and Robotics. DOI/URL:
https://openaccess.thecvf.com/content/ICCV2023W/ACVR/papers/Kwolek_Continuous_Hand_Gesture_Recognition_for_Human-Robot_Collaborative_Assembly_ICCVW_2023_paper.pdf.

Lý do dùng trong báo cáo: nguồn này hỗ trợ phần mô hình, dữ liệu hoặc
triển khai; ghi chú kiểm tra: CVF workshop.

Các trường cần rà soát trong Zotero trước khi nộp: tên tác giả đầy đủ,
tiêu đề, năm, volume/issue, trang, DOI, publisher và loại tài liệu. Với
journal, đối chiếu ISSN/venue trên SCImago, Scopus Sources hoặc Web of
Science Journal Info; với conference, đối chiếu trang IEEE Xplore, ACM
DL hoặc CVF chính thức.

Cách sử dụng trong báo cáo: không trích nguyên văn dài; diễn giải kết
quả liên quan bằng lời của nhóm và đặt số trích dẫn IEEE ở cuối nhận
định. ResearchGate chỉ dùng để tìm bản đọc, không dùng làm bằng chứng
xác nhận chỉ mục.

## **A.22 Phiếu nguồn \[22\]**

Tên nguồn: Hand gesture recognition using automatic feature extraction
and deep learning algorithms with memory

Tác giả/năm: R. E. Nogales and M. E. Benalcazar (2023). Venue: Big Data
and Cognitive Computing, vol. 7, no. 2, 102. DOI/URL:
10.3390/bdcc7020102.

Lý do dùng trong báo cáo: nguồn này hỗ trợ phần mô hình, dữ liệu hoặc
triển khai; ghi chú kiểm tra: Peer-reviewed journal.

Các trường cần rà soát trong Zotero trước khi nộp: tên tác giả đầy đủ,
tiêu đề, năm, volume/issue, trang, DOI, publisher và loại tài liệu. Với
journal, đối chiếu ISSN/venue trên SCImago, Scopus Sources hoặc Web of
Science Journal Info; với conference, đối chiếu trang IEEE Xplore, ACM
DL hoặc CVF chính thức.

Cách sử dụng trong báo cáo: không trích nguyên văn dài; diễn giải kết
quả liên quan bằng lời của nhóm và đặt số trích dẫn IEEE ở cuối nhận
định. ResearchGate chỉ dùng để tìm bản đọc, không dùng làm bằng chứng
xác nhận chỉ mục.

## **A.23 Phiếu nguồn \[23\]**

Tên nguồn: Hand-gesture recognition using two-antenna Doppler radar with
deep convolutional neural networks

Tác giả/năm: S. Skaria, A. Al-Hourani, R. J. Evans, and collaborators
(2019). Venue: IEEE Sensors Journal, vol. 19, no. 8. DOI/URL:
10.1109/JSEN.2019.2892073.

Lý do dùng trong báo cáo: nguồn này hỗ trợ phần mô hình, dữ liệu hoặc
triển khai; ghi chú kiểm tra: IEEE journal.

Các trường cần rà soát trong Zotero trước khi nộp: tên tác giả đầy đủ,
tiêu đề, năm, volume/issue, trang, DOI, publisher và loại tài liệu. Với
journal, đối chiếu ISSN/venue trên SCImago, Scopus Sources hoặc Web of
Science Journal Info; với conference, đối chiếu trang IEEE Xplore, ACM
DL hoặc CVF chính thức.

Cách sử dụng trong báo cáo: không trích nguyên văn dài; diễn giải kết
quả liên quan bằng lời của nhóm và đặt số trích dẫn IEEE ở cuối nhận
định. ResearchGate chỉ dùng để tìm bản đọc, không dùng làm bằng chứng
xác nhận chỉ mục.

## **A.24 Phiếu nguồn \[24\]**

Tên nguồn: Hand gesture recognition enhancement based on spatial fuzzy
matching in Leap Motion

Tác giả/năm: H. Li et al. (2020). Venue: IEEE Transactions on Industrial
Informatics, vol. 16, no. 3. DOI/URL: 10.1109/TII.2019.2931140.

Lý do dùng trong báo cáo: nguồn này hỗ trợ phần mô hình, dữ liệu hoặc
triển khai; ghi chú kiểm tra: IEEE journal.

Các trường cần rà soát trong Zotero trước khi nộp: tên tác giả đầy đủ,
tiêu đề, năm, volume/issue, trang, DOI, publisher và loại tài liệu. Với
journal, đối chiếu ISSN/venue trên SCImago, Scopus Sources hoặc Web of
Science Journal Info; với conference, đối chiếu trang IEEE Xplore, ACM
DL hoặc CVF chính thức.

Cách sử dụng trong báo cáo: không trích nguyên văn dài; diễn giải kết
quả liên quan bằng lời của nhóm và đặt số trích dẫn IEEE ở cuối nhận
định. ResearchGate chỉ dùng để tìm bản đọc, không dùng làm bằng chứng
xác nhận chỉ mục.

## **A.25 Phiếu nguồn \[25\]**

Tên nguồn: A systematic analysis of performance measures for
classification tasks

Tác giả/năm: M. Sokolova and G. Lapalme (2009). Venue: Information
Processing & Management, vol. 45, no. 4. DOI/URL:
10.1016/j.ipm.2009.03.002.

Lý do dùng trong báo cáo: nguồn này hỗ trợ phần mô hình, dữ liệu hoặc
triển khai; ghi chú kiểm tra: Elsevier journal.

Các trường cần rà soát trong Zotero trước khi nộp: tên tác giả đầy đủ,
tiêu đề, năm, volume/issue, trang, DOI, publisher và loại tài liệu. Với
journal, đối chiếu ISSN/venue trên SCImago, Scopus Sources hoặc Web of
Science Journal Info; với conference, đối chiếu trang IEEE Xplore, ACM
DL hoặc CVF chính thức.

Cách sử dụng trong báo cáo: không trích nguyên văn dài; diễn giải kết
quả liên quan bằng lời của nhóm và đặt số trích dẫn IEEE ở cuối nhận
định. ResearchGate chỉ dùng để tìm bản đọc, không dùng làm bằng chứng
xác nhận chỉ mục.

## **A.26 Phiếu nguồn \[26\]**

Tên nguồn: Evaluation: From precision, recall and F-measure to ROC,
informedness, markedness and correlation

Tác giả/năm: D. M. W. Powers (2011). Venue: Journal of Machine Learning
Technologies, vol. 2, no. 1. DOI/URL:
https://www.researchgate.net/publication/228529307.

Lý do dùng trong báo cáo: nguồn này hỗ trợ phần mô hình, dữ liệu hoặc
triển khai; ghi chú kiểm tra: Evaluation reference; index check
recommended.

Các trường cần rà soát trong Zotero trước khi nộp: tên tác giả đầy đủ,
tiêu đề, năm, volume/issue, trang, DOI, publisher và loại tài liệu. Với
journal, đối chiếu ISSN/venue trên SCImago, Scopus Sources hoặc Web of
Science Journal Info; với conference, đối chiếu trang IEEE Xplore, ACM
DL hoặc CVF chính thức.

Cách sử dụng trong báo cáo: không trích nguyên văn dài; diễn giải kết
quả liên quan bằng lời của nhóm và đặt số trích dẫn IEEE ở cuối nhận
định. ResearchGate chỉ dùng để tìm bản đọc, không dùng làm bằng chứng
xác nhận chỉ mục.

## **A.27 Phiếu nguồn \[27\]**

Tên nguồn: Azure Container Apps documentation

Tác giả/năm: Microsoft (2026). Venue: Microsoft Learn. DOI/URL:
https://learn.microsoft.com/azure/container-apps/.

Lý do dùng trong báo cáo: nguồn này hỗ trợ phần mô hình, dữ liệu hoặc
triển khai; ghi chú kiểm tra: Technical documentation.

Các trường cần rà soát trong Zotero trước khi nộp: tên tác giả đầy đủ,
tiêu đề, năm, volume/issue, trang, DOI, publisher và loại tài liệu. Với
journal, đối chiếu ISSN/venue trên SCImago, Scopus Sources hoặc Web of
Science Journal Info; với conference, đối chiếu trang IEEE Xplore, ACM
DL hoặc CVF chính thức.

Cách sử dụng trong báo cáo: không trích nguyên văn dài; diễn giải kết
quả liên quan bằng lời của nhóm và đặt số trích dẫn IEEE ở cuối nhận
định. ResearchGate chỉ dùng để tìm bản đọc, không dùng làm bằng chứng
xác nhận chỉ mục.

## **A.28 Phiếu nguồn \[28\]**

Tên nguồn: FastAPI documentation

Tác giả/năm: FastAPI contributors (2026). Venue: FastAPI official
documentation. DOI/URL: https://fastapi.tiangolo.com/.

Lý do dùng trong báo cáo: nguồn này hỗ trợ phần mô hình, dữ liệu hoặc
triển khai; ghi chú kiểm tra: Technical documentation.

Các trường cần rà soát trong Zotero trước khi nộp: tên tác giả đầy đủ,
tiêu đề, năm, volume/issue, trang, DOI, publisher và loại tài liệu. Với
journal, đối chiếu ISSN/venue trên SCImago, Scopus Sources hoặc Web of
Science Journal Info; với conference, đối chiếu trang IEEE Xplore, ACM
DL hoặc CVF chính thức.

Cách sử dụng trong báo cáo: không trích nguyên văn dài; diễn giải kết
quả liên quan bằng lời của nhóm và đặt số trích dẫn IEEE ở cuối nhận
định. ResearchGate chỉ dùng để tìm bản đọc, không dùng làm bằng chứng
xác nhận chỉ mục.

## **A.29 Phiếu nguồn \[29\]**

Tên nguồn: The WebSocket Protocol

Tác giả/năm: I. Fette and A. Melnikov (2011). Venue: IETF RFC 6455.
DOI/URL: 10.17487/RFC6455.

Lý do dùng trong báo cáo: nguồn này hỗ trợ phần mô hình, dữ liệu hoặc
triển khai; ghi chú kiểm tra: IETF standard.

Các trường cần rà soát trong Zotero trước khi nộp: tên tác giả đầy đủ,
tiêu đề, năm, volume/issue, trang, DOI, publisher và loại tài liệu. Với
journal, đối chiếu ISSN/venue trên SCImago, Scopus Sources hoặc Web of
Science Journal Info; với conference, đối chiếu trang IEEE Xplore, ACM
DL hoặc CVF chính thức.

Cách sử dụng trong báo cáo: không trích nguyên văn dài; diễn giải kết
quả liên quan bằng lời của nhóm và đặt số trích dẫn IEEE ở cuối nhận
định. ResearchGate chỉ dùng để tìm bản đọc, không dùng làm bằng chứng
xác nhận chỉ mục.

# **PHỤ LỤC B. ÁNH XẠ REPOSITORY VÀ MODULE**

| **File/thư mục** | **Vai trò** |
|:---|:---|
| gateway/main.py | Vòng lặp camera, gọi cloud, safety filter, UI, log CSV |
| gateway/preprocess.py | MediaPipe crop và hỗ trợ phân biệt one/two |
| gateway/safety.py | GestureStabilizer, SafetyPolicy và schema log latency |
| gateway/transport.py | DryRunTransport và WebSocketTransport |
| cloud/inference.py | Load model, preprocess JPEG, predict gesture |
| cloud/app.py | FastAPI endpoint /health, /v1/model, /v1/predict |
| common/protocol.py | Định nghĩa gesture, mode, action và mapper |
| firmware/src/main.cpp | Firmware ESP32, motor, servo, HTTP debug và WebSocket |
| ml/train_cnn.py | Huấn luyện CNN baseline |
| ml/train_cnn_lstm.py | Khung huấn luyện CNN-LSTM định hướng |
| reports/\*.csv | Log latency online |
| reports/\*.json | Metrics offline |

Báo cáo không nhúng secret từ .env, firmware/include/config.h hoặc token
thật. Các giá trị API key, Wi-Fi password và command token chỉ được mô
tả bằng giá trị minh họa khi cần minh họa.

# **PHỤ LỤC C. NHẬT KÝ KIỂM THỬ VÀ TIÊU CHÍ NGHIỆM THU**

Kiểm thử tự động được chạy bằng lệnh .\\venv\Scripts\python.exe -m
pytest -q. Kết quả mới nhất trong phiên tạo báo cáo: 34 passed in 2.23s.
Kết quả này khác README cũ ghi 28 passed vì repo hiện tại đã có thêm
test mới.

- API /health hoạt động

- /v1/model trả model_version

- Gateway dry-run gọi được cloud và ghi log

- ESP32 phản hồi /health và /state

- WebSocket nhận command hợp lệ

- Xe dừng khi mất lệnh quá timeout

# **PHỤ LỤC D. THAM SỐ VẬN HÀNH ĐỀ XUẤT**

| **Tham số**       | **Giá trị** | **Ý nghĩa**                            |
|:------------------|:------------|:---------------------------------------|
| MinConfidence     | 0.80        | Ngưỡng chính cho lệnh thường           |
| ModeMinConfidence | 0.60        | Ngưỡng chuyển mode rock/peace          |
| NormalRequired    | 3           | Số frame liên tiếp cho lệnh thường     |
| StopRequired      | 2           | Số frame liên tiếp cho stop            |
| DeadmanMs         | 600         | Gateway/firmware dừng khi quá hạn      |
| DriveRepeatMs     | 200         | Lặp lệnh xe khi đang giữ gesture       |
| DriveHoldMs       | 550         | Thời gian giữ lệnh xe                  |
| ServoCooldownMs   | 250-350     | Giảm rung servo khi nhận lệnh liên tục |

# **PHỤ LỤC E. DỮ LIỆU VÀ NHÃN**

| **Gesture** | **Số frame** | **Ghi chú**         |
|:------------|:-------------|:--------------------|
| stop        | 1125         | frame crop/metadata |
| peace       | 900          | frame crop/metadata |
| rock        | 1125         | frame crop/metadata |
| like        | 1125         | frame crop/metadata |
| dislike     | 1125         | frame crop/metadata |
| one         | 1125         | frame crop/metadata |
| two         | 1125         | frame crop/metadata |
| no_gesture  | 900          | frame crop/metadata |

- Thu thêm subject s06-s10 với nền simple/complex và lighting
  bright/normal/dim.

- Đo false activation bằng no_gesture trong 5 phút.

- Chạy split 70/20/10 và 80/20 như thí nghiệm bổ sung.

- Benchmark edge inference trên laptop/Raspberry Pi để so sánh cloud vs
  edge.

# **PHỤ LỤC F. ĐỐI CHIẾU YÊU CẦU CỦA THẦY**

| **Yêu cầu** | **Cách đáp ứng** |
|:---|:---|
| 40-70 trang | Bản in quyển có phụ lục nguồn, repo, test và thông số |
| Chương 1 có 10-15 bài báo | Trích nguồn nền tảng HGR/HRI/CNN |
| Chương 2 có 8-10 bài báo | Có bảng so sánh 10 nghiên cứu liên quan |
| Chương 3 có 3-5 bài cùng hướng | Trích MediaPipe, MobileNetV3, robot control, dynamic HGR |
| Chương 4 online/offline | Tách online latency và offline model metrics |
| 70/20/10 hoặc 80/20 | Ghi rõ hiện tại dùng subject split; đề xuất chạy bổ sung |
| Kết luận 3 đoạn | Đúng ba đoạn: đạt được, hạn chế, hướng phát triển |
| Zotero | Có BibTeX đi kèm để import Zotero |
