# Tài liệu Yêu cầu (Requirements Document)

## Introduction

Tính năng này tập trung vào việc điều khiển chuyển động của xe tự hành 4 bánh thông qua vi điều khiển ESP32 kết hợp mạch điều khiển động cơ L298N. Đây là bước kiểm thử cơ bản (basic test) ở mức phần cứng và firmware, được thực hiện TRƯỚC khi tích hợp với lệnh điều khiển từ Cloud/AI (nhận dạng cử chỉ tay).

Phạm vi tính năng bao gồm:
1. Xác lập kiến trúc cấp nguồn đúng theo thiết kế đã thống nhất và nối dây tín hiệu từ các chân GPIO của ESP32 sang các chân điều khiển của L298N (IN1-IN4, ENA, ENB).
2. Viết firmware kiểm thử trên ESP32 để điều khiển 4 bánh xe thực hiện các chuyển động: tiến, lùi, rẽ trái, rẽ phải, dừng; và điều chỉnh tốc độ bằng PWM.
3. Xác thực 4 bánh xe quay đúng chiều và đúng cụm trái/phải.

Việc nhận lệnh từ Cloud/AI là một tính năng riêng ở giai đoạn sau; tài liệu này chỉ nêu định hướng để firmware dễ mở rộng, không triển khai trong phạm vi hiện tại.

## Glossary

- **ESP32**: Vi điều khiển chính (ESP32 Devkit V1) đóng vai trò bộ não, xuất tín hiệu điều khiển và PWM tới L298N.
- **Car_Control_Firmware**: Phần mềm điều khiển chạy trên ESP32, chịu trách nhiệm sinh tín hiệu chiều quay và PWM cho L298N.
- **L298N**: Mạch điều khiển động cơ kép (dual H-bridge) nhận tín hiệu từ ESP32 và cấp công suất cho 4 động cơ DC.
- **Left_Motor_Group**: Cụm động cơ bánh trái, đấu song song vào ngõ ra OUT1/OUT2 của L298N.
- **Right_Motor_Group**: Cụm động cơ bánh phải, đấu song song vào ngõ ra OUT3/OUT4 của L298N.
- **IN1, IN2**: Chân logic của L298N quyết định chiều quay của Left_Motor_Group.
- **IN3, IN4**: Chân logic của L298N quyết định chiều quay của Right_Motor_Group.
- **ENA**: Chân enable/PWM của L298N điều chỉnh tốc độ Left_Motor_Group.
- **ENB**: Chân enable/PWM của L298N điều chỉnh tốc độ Right_Motor_Group.
- **PWM_Duty**: Giá trị độ rộng xung PWM, biểu diễn theo thang 0-255 (8-bit), điều khiển tốc độ động cơ.
- **Mini560**: Mạch hạ áp DC-DC chuyển 11.1V xuống 5V để cấp cho ESP32 (chân VIN) và PCA9685 (V+).
- **Battery_Pack**: Cụm pin 18650 cấp nguồn danh định 11.1V qua công tắc nguồn.
- **Common_Ground**: Điểm nối đất (Mass) chung giữa Battery_Pack, L298N, Mini560 và ESP32.
- **Movement_Command**: Một trong các lệnh chuyển động: TIẾN (forward), LÙI (backward), RẼ_TRÁI (turn left), RẼ_PHẢI (turn right), DỪNG (stop).
- **Safe_State**: Trạng thái mà cả hai cụm động cơ đều dừng (PWM_Duty = 0 hoặc các chân chiều ở mức thấp).

## Requirements

### Requirement 1: Kiến trúc cấp nguồn

**User Story:** Là người lắp ráp phần cứng, tôi muốn cấp nguồn đúng kiến trúc đã thống nhất, để các linh kiện hoạt động ổn định và an toàn ở đúng mức điện áp.

#### Acceptance Criteria

1. THE Battery_Pack SHALL cấp nguồn danh định 11.1V tới chân nguồn 12V của L298N thông qua công tắc nguồn.
2. THE Mini560 SHALL nhận điện áp đầu vào từ Battery_Pack và xuất điện áp 5V tới chân VIN của ESP32.
3. THE Common_Ground SHALL được nối chung giữa Battery_Pack, L298N, Mini560 và ESP32.
4. IF điện áp đầu ra của Mini560 nằm ngoài khoảng 4.8V đến 5.2V, THEN THE người lắp ráp SHALL ngắt công tắc nguồn trước khi cắm ESP32.
5. WHERE jumper 5V trên L298N được sử dụng, THE người lắp ráp SHALL gỡ jumper đó khi điện áp nguồn vượt 12V để tránh hỏng bộ ổn áp nội của L298N.

### Requirement 2: Nối dây tín hiệu ESP32 sang L298N

**User Story:** Là lập trình viên firmware, tôi muốn có sơ đồ ánh xạ chân GPIO cố định giữa ESP32 và L298N, để firmware điều khiển đúng chân và dễ bảo trì.

#### Acceptance Criteria

1. THE Car_Control_Firmware SHALL định nghĩa 6 chân GPIO của ESP32 ánh xạ tới IN1, IN2, IN3, IN4, ENA và ENB của L298N.
2. THE Car_Control_Firmware SHALL gán IN1 và IN2 để điều khiển chiều quay của Left_Motor_Group.
3. THE Car_Control_Firmware SHALL gán IN3 và IN4 để điều khiển chiều quay của Right_Motor_Group.
4. THE Car_Control_Firmware SHALL gán ENA để xuất PWM điều khiển tốc độ Left_Motor_Group và ENB để xuất PWM điều khiển tốc độ Right_Motor_Group.
5. WHERE một chân GPIO được chọn là chân strapping của ESP32, THE Car_Control_Firmware SHALL ghi rõ chân đó trong phần ghi chú để tránh xung đột khi khởi động.

### Requirement 3: Khởi tạo trạng thái an toàn khi bật nguồn

**User Story:** Là người vận hành, tôi muốn xe đứng yên ngay khi cấp nguồn, để tránh xe chạy ngoài ý muốn gây nguy hiểm.

#### Acceptance Criteria

1. WHEN ESP32 hoàn tất quá trình khởi động, THE Car_Control_Firmware SHALL đặt cả hai cụm động cơ về Safe_State.
2. WHEN ESP32 hoàn tất quá trình khởi động, THE Car_Control_Firmware SHALL đặt PWM_Duty của ENA và ENB về 0.
3. THE Car_Control_Firmware SHALL cấu hình 6 chân điều khiển ở chế độ OUTPUT trước khi xuất bất kỳ Movement_Command nào.

### Requirement 4: Thực thi các lệnh chuyển động

**User Story:** Là người kiểm thử, tôi muốn ra lệnh cho xe tiến, lùi, rẽ trái, rẽ phải và dừng, để xác nhận xe di chuyển đúng theo từng lệnh.

#### Acceptance Criteria

1. WHEN nhận Movement_Command TIẾN, THE Car_Control_Firmware SHALL đặt Left_Motor_Group và Right_Motor_Group cùng quay theo chiều tiến.
2. WHEN nhận Movement_Command LÙI, THE Car_Control_Firmware SHALL đặt Left_Motor_Group và Right_Motor_Group cùng quay theo chiều lùi.
3. WHEN nhận Movement_Command RẼ_TRÁI, THE Car_Control_Firmware SHALL đặt Right_Motor_Group quay theo chiều tiến và Left_Motor_Group quay theo chiều lùi hoặc dừng.
4. WHEN nhận Movement_Command RẼ_PHẢI, THE Car_Control_Firmware SHALL đặt Left_Motor_Group quay theo chiều tiến và Right_Motor_Group quay theo chiều lùi hoặc dừng.
5. WHEN nhận Movement_Command DỪNG, THE Car_Control_Firmware SHALL đặt cả hai cụm động cơ về Safe_State trong vòng 100ms.
6. IF nhận một Movement_Command không hợp lệ, THEN THE Car_Control_Firmware SHALL giữ nguyên Safe_State và ghi thông báo lỗi ra cổng Serial.

### Requirement 5: Điều khiển tốc độ bằng PWM

**User Story:** Là người kiểm thử, tôi muốn điều chỉnh tốc độ xe qua PWM, để kiểm tra dải tốc độ và sự cân bằng giữa hai cụm động cơ.

#### Acceptance Criteria

1. THE Car_Control_Firmware SHALL chấp nhận giá trị PWM_Duty trong khoảng 0 đến 255 cho mỗi cụm động cơ.
2. WHEN một Movement_Command kèm giá trị PWM_Duty được thực thi, THE Car_Control_Firmware SHALL xuất tín hiệu PWM tương ứng ra ENA và ENB.
3. IF giá trị PWM_Duty nhận vào lớn hơn 255, THEN THE Car_Control_Firmware SHALL giới hạn (clamp) giá trị về 255.
4. IF giá trị PWM_Duty nhận vào nhỏ hơn 0, THEN THE Car_Control_Firmware SHALL giới hạn (clamp) giá trị về 0.
5. THE Car_Control_Firmware SHALL sử dụng tần số PWM trong khoảng 1kHz đến 20kHz cho cả ENA và ENB.

### Requirement 6: Xác thực chiều quay và phân cụm động cơ

**User Story:** Là người kiểm thử, tôi muốn một quy trình xác thực rõ ràng cho từng bánh xe, để chắc chắn 4 bánh quay đúng chiều và đúng cụm trái/phải.

#### Acceptance Criteria

1. WHEN thực thi lệnh kiểm thử TIẾN, THE Left_Motor_Group SHALL quay sao cho bánh xe đẩy thân xe về phía trước.
2. WHEN thực thi lệnh kiểm thử TIẾN, THE Right_Motor_Group SHALL quay sao cho bánh xe đẩy thân xe về phía trước.
3. IF một bánh xe quay ngược chiều mong đợi khi thực thi lệnh kiểm thử, THEN THE người kiểm thử SHALL đảo cặp dây động cơ tương ứng tại ngõ ra L298N hoặc đảo logic chân IN trong firmware.
4. THE Car_Control_Firmware SHALL cung cấp một chuỗi kiểm thử tuần tự chạy lần lượt TIẾN, LÙI, RẼ_TRÁI, RẼ_PHẢI, DỪNG, mỗi bước cách nhau tối thiểu 1 giây.
5. WHEN mỗi bước trong chuỗi kiểm thử được thực thi, THE Car_Control_Firmware SHALL in tên Movement_Command hiện hành ra cổng Serial để đối chiếu trực quan.

### Requirement 7: Khả năng mở rộng cho lệnh từ Cloud (định hướng)

**User Story:** Là lập trình viên, tôi muốn lớp điều khiển động cơ tách biệt với nguồn phát lệnh, để sau này dễ thay nguồn lệnh kiểm thử bằng lệnh từ Cloud/AI mà không sửa lại logic động cơ.

#### Acceptance Criteria

1. THE Car_Control_Firmware SHALL tách hàm thực thi Movement_Command ra khỏi nguồn phát lệnh kiểm thử.
2. WHERE nguồn lệnh là chuỗi kiểm thử cục bộ, THE Car_Control_Firmware SHALL gọi cùng một tập hàm thực thi Movement_Command dùng chung cho mọi nguồn lệnh trong tương lai.
3. THE Car_Control_Firmware SHALL định nghĩa tập Movement_Command dưới dạng các hằng số hoặc kiểu liệt kê (enum) để nguồn lệnh khác có thể tham chiếu nhất quán.
