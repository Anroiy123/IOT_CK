# IOT_CK - Nhận dạng cử chỉ điều khiển xe và tay máy

Đề tài sử dụng webcam trên laptop để nhận dạng cử chỉ tay bằng mô hình CNN,
sau đó gửi lệnh qua Wi-Fi tới ESP32 để điều khiển xe và tay máy.

## Kiến trúc hiện tại

```text
Webcam laptop
  -> Gateway trên laptop
     - MediaPipe phát hiện và cắt vùng bàn tay
     - gửi ảnh JPEG tới Azure
  -> FastAPI + CNN trên Azure Container Apps
  -> Gateway lọc confidence và ánh xạ cử chỉ thành lệnh
  -> WebSocket qua Wi-Fi
  -> ESP32
  -> L298N + motor / PCA9685 + servo
```

Azure là cloud chính của bản demo hiện tại. Local FastAPI được giữ làm fallback
và để benchmark. Hugging Face Spaces chỉ còn là phương án triển khai phụ.

ESP32 không xử lý ảnh. Khi vận hành qua Wi-Fi, ESP32 không bắt buộc nối USB với
laptop; USB chỉ cần để nạp firmware, xem Serial Monitor hoặc cấp nguồn tạm thời.

## Trạng thái dự án

Cập nhật ngày 14/06/2026:

- Firmware ESP32 điều khiển được motor và bốn servo.
- Gateway điều khiển ESP32 bằng WebSocket; HTTP `/health` và `/state` chỉ dùng
  để kiểm tra.
- Gateway có camera UI, MediaPipe crop, safety filter, log CSV,
  `session_id` và `request_id`.
- CNN baseline MobileNetV3Small đã được huấn luyện bằng dữ liệu của 5 người.
- Model đã được đóng gói trong image trên GitHub Container Registry (GHCR).
- API đang chạy trên Azure Container Apps tại Japan East.
- Bộ test hiện tại: `28 passed`.

Azure API hiện tại:

```text
https://iot-ck-gesture-api.graysky-cdd83781.japaneast.azurecontainerapps.io
```

Kiểm tra:

```powershell
$AzureUrl = "https://iot-ck-gesture-api.graysky-cdd83781.japaneast.azurecontainerapps.io"
Invoke-RestMethod "$AzureUrl/health"
Invoke-RestMethod "$AzureUrl/v1/model"
```

Kết quả mong đợi:

```json
{"status":"ok"}
```

```json
{"model_version":"cnn-s05-partial-v1","model_type":"cnn"}
```

## Chạy nhanh

Các lệnh trong phần này chạy tại thư mục project trên laptop, không chạy trong
Azure Cloud Shell:

```powershell
cd "C:\Users\hunga\OneDrive\Desktop\project\IOT_CK"
```

### 1. Chuẩn bị môi trường Python

Yêu cầu:

- Windows 10/11.
- Python 3.11.
- Webcam laptop hoặc webcam USB.
- VS Code và PlatformIO nếu cần nạp lại firmware.

Tạo môi trường:

```powershell
py -3.11 -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Không dùng Python 3.14 cho môi trường TensorFlow của project này.

### 2. Tạo file `.env`

Tạo `.env` tại thư mục gốc:

```dotenv
AZURE_GESTURE_API_KEY=KHOA_API_DA_DAT_TREN_AZURE
ESP32_COMMAND_TOKEN=TOKEN_DA_NAP_VAO_ESP32
```

Không thêm dấu `<` và `>` vào giá trị thật. Ví dụ `"<API_KEY>"` chỉ là
placeholder trong tài liệu và sẽ bị Azure từ chối.

Hai khóa có mục đích khác nhau:

| Biến | Nơi sử dụng | Mục đích |
|---|---|---|
| `AZURE_GESTURE_API_KEY` | Gateway và Azure API | Xác thực request `/v1/predict` |
| `ESP32_COMMAND_TOKEN` | Gateway và firmware ESP32 | Xác thực lệnh WebSocket |

Các khóa này do nhóm tự đặt, không lấy từ Azure Portal hoặc Hugging Face.
`.env` đã được Git ignore; không commit secret lên GitHub.

Nếu quên Azure API key, đặt một key mới:

```powershell
$NewApiKey = "TAO_MOT_KHOA_MOI_DU_DAI"

az containerapp update `
  --name iot-ck-gesture-api `
  --resource-group rg-iot-ck-gesture `
  --set-env-vars GESTURE_API_KEY=$NewApiKey

$env:AZURE_GESTURE_API_KEY = $NewApiKey
```

Sau đó cập nhật cùng giá trị vào `.env`.

### 3. Kiểm tra camera và Azure, chưa chạy xe

```powershell
.\scripts\run_gateway_azure.ps1 `
  -AzureUrl "https://iot-ck-gesture-api.graysky-cdd83781.japaneast.azurecontainerapps.io" `
  -DryRun
```

`-DryRun` vẫn mở camera và gọi model Azure nhưng không gửi lệnh tới ESP32.
Nhấn `q` để thoát.

### 4. Chạy thật với ESP32

Đảm bảo laptop và ESP32 cùng mạng Wi-Fi, sau đó lấy địa chỉ IP từ Serial
Monitor hoặc router:

```powershell
Invoke-RestMethod "http://<ESP32_IP>/health"
Invoke-RestMethod "http://<ESP32_IP>/state"
```

Chạy gateway:

```powershell
.\scripts\run_gateway_azure.ps1 `
  -AzureUrl "https://iot-ck-gesture-api.graysky-cdd83781.japaneast.azurecontainerapps.io" `
  -Esp32Host "<ESP32_IP>" `
  -Speed 255 `
  -DriveRepeatMs 200 `
  -DriveHoldMs 550
```

Khi demo tay máy, `rock` và `peace` dùng ngưỡng riêng thấp hơn để chuyển mode
nhanh hơn, còn lệnh servo vẫn giữ ngưỡng chính `0.80`:

```powershell
.\scripts\run_gateway_azure.ps1 `
  -AzureUrl "https://iot-ck-gesture-api.graysky-cdd83781.japaneast.azurecontainerapps.io" `
  -Esp32Host "<ESP32_IP>" `
  -Speed 200 `
  -ModeMinConfidence 0.60 `
  -ModeRequired 2 `
  -MinConfidence 0.80 `
  -NormalRequired 3 `
  -ServoCooldownMs 350
```

Luồng thao tác tay máy: đưa `rock` để vào `arm`, dùng `one/two` để chọn khớp,
dùng `like/dislike` để tăng/giảm góc, và dùng `peace` để quay lại `car`.

Gateway kết nối tới:

```text
ws://<ESP32_IP>:81/
```

## Cử chỉ và chức năng

| Label | Cách làm tay | Chế độ xe | Chế độ tay máy |
|---|---|---|---|
| `stop` | Xòe bàn tay, năm ngón rõ | Dừng xe | Dừng motor |
| `peace` | Chữ V mở rộng | Chuyển sang chế độ xe | Chuyển sang chế độ xe |
| `rock` | Giơ ngón trỏ và ngón út | Chuyển sang chế độ tay máy | Giữ chế độ tay máy |
| `like` | Ngón cái hướng lên | Tiến | Tăng góc khớp 5 độ |
| `dislike` | Ngón cái hướng xuống | Lùi | Giảm góc khớp 5 độ |
| `one` | Một ngón trỏ | Rẽ trái | Chọn khớp trước |
| `two` | Hai ngón giữ sát nhau | Rẽ phải | Chọn khớp tiếp |
| `no_gesture` | Không có cử chỉ hợp lệ | Không phát lệnh | Không phát lệnh |

Thứ tự khớp:

```text
base -> lower -> upper -> gripper
```

`peace` và `two` dễ nhầm. Khi thao tác và thu dữ liệu, `peace` cần tạo chữ V
rộng; `two` giữ hai ngón gần nhau và thẳng.

## Luồng xử lý gateway

1. Đọc frame từ webcam.
2. MediaPipe tìm bàn tay và crop vùng quan tâm nếu tìm thấy.
3. Gateway mã hóa ảnh thành JPEG và gọi Azure `/v1/predict`.
4. Gateway nhận `gesture`, `confidence`, `inference_ms` và model version.
5. Safety filter yêu cầu kết quả đủ tin cậy và ổn định.
6. Gesture mapper chuyển cử chỉ thành lệnh xe hoặc tay máy.
7. Gateway gửi JSON qua WebSocket tới ESP32.
8. ESP32 trả ACK và gateway ghi toàn bộ thời gian vào CSV.

Mặc định gateway vẫn gọi cloud khi MediaPipe không phát hiện được tay; trường
hợp đó ảnh toàn frame được gửi lên model. Chỉ dùng tùy chọn sau khi muốn bỏ qua
cloud nếu MediaPipe không thấy tay:

```powershell
-SkipCloudWithoutHand
```

UI camera được lật ngang để hoạt động như gương. Việc lật chỉ áp dụng cho ảnh
hiển thị; ảnh gửi tới model không bị lật.

## Cơ chế an toàn

- Cử chỉ thường cần confidence từ `0.80` và xuất hiện 3 lần liên tiếp.
- `stop` cần confidence từ `0.80` và xuất hiện 2 lần liên tiếp.
- Gateway gửi `stop` khi camera lỗi, cloud lỗi, WebSocket lỗi hoặc quá thời
  gian deadman 600 ms.
- ESP32 từ chối command token sai, sequence cũ và TTL không hợp lệ.
- ESP32 tự dừng motor nếu không nhận lệnh hợp lệ trong 600 ms.
- Servo bị giới hạn góc riêng cho từng khớp và thay đổi 5 độ mỗi lệnh.

Không hạ confidence hoặc số lần xác nhận chỉ để xe phản hồi nhanh hơn nếu chưa
đo lại false activation.

## Phần cứng và pinout

| Chức năng | ESP32 GPIO |
|---|---:|
| L298N ENA | 13 |
| L298N IN1 | 12 |
| L298N IN2 | 14 |
| L298N IN3 | 27 |
| L298N IN4 | 26 |
| L298N ENB | 25 |
| PCA9685 SDA | 21 |
| PCA9685 SCL | 22 |

Thông số firmware:

- PCA9685: địa chỉ `0x40`, tần số 50 Hz.
- WebSocket: port `81`.
- HTTP debug: port `80`.
- PWM motor: 5 kHz, độ phân giải 8 bit.
- Watchdog command: 600 ms.
- Servo channel 0-3: `base`, `lower`, `upper`, `gripper`.

Khi boot, motor được dừng và PWM bằng 0. Firmware hiện đưa bốn servo về các góc
khởi tạo `90`, `90`, `90`, `60`; vì vậy servo có thể chuyển động ngay sau khi
ESP32 khởi động.

GPIO12 là strapping pin. Nếu ESP32 boot không ổn định, chuyển dây IN1 sang
GPIO33 và cập nhật `PIN_IN1` trong `firmware/include/config.h`.

Motor và servo phải có nguồn phù hợp và chung GND với ESP32. Không cấp toàn bộ
motor/servo trực tiếp từ chân 5V của ESP32.

## Cấu hình và nạp firmware

File bí mật:

```text
firmware/include/config.h
```

Các giá trị bắt buộc:

```cpp
#define WIFI_SSID "TEN_WIFI"
#define WIFI_PASSWORD "MAT_KHAU_WIFI"
#define COMMAND_TOKEN "TOKEN_DIEU_KHIEN"
```

`COMMAND_TOKEN` phải trùng với `ESP32_COMMAND_TOKEN` trong `.env`.

Build firmware:

```powershell
.\.venv\Scripts\pio.exe run -d firmware
```

Upload vào ESP32 trên `COM5`:

```powershell
.\.venv\Scripts\pio.exe run -d firmware -t upload
```

Mở Serial Monitor:

```powershell
.\.venv\Scripts\pio.exe device monitor -p COM5 -b 115200
```

PIO Home không bắt buộc để build hoặc upload.

## Gateway UI và log

Cửa sổ gateway hiển thị:

- Mode hiện tại: `car` hoặc `arm`.
- Gesture và confidence model trả về.
- Tổng latency của frame.
- Command vừa gửi.

Log Azure mặc định:

```text
reports/gateway_azure_latency.csv
```

Mỗi dòng gồm:

- `session_id`, `request_id`.
- Gesture, confidence, mode và command.
- Thời gian capture và preprocessing.
- Cloud RTT và model inference.
- ESP32 ACK và tổng latency.

Nên tạo file log riêng cho mỗi phiên đo:

```powershell
.\scripts\run_gateway_azure.ps1 `
  -AzureUrl "https://iot-ck-gesture-api.graysky-cdd83781.japaneast.azurecontainerapps.io" `
  -DryRun `
  -Log "reports\gateway_azure_demo_01.csv"
```

## Cloud API

### `GET /health`

Trả trạng thái hoạt động:

```json
{"status":"ok"}
```

### `GET /v1/model`

Trả model đang được load:

```json
{"model_version":"cnn-s05-partial-v1","model_type":"cnn"}
```

### `POST /v1/predict`

Header:

```text
X-API-Key: KHOA_API_DA_DAT_TREN_AZURE
```

Body cho một ảnh:

```json
{
  "image_b64": "JPEG_BASE64",
  "session_id": "demo-session",
  "request_id": "request-001"
}
```

Gateway hiện gửi danh sách ảnh bằng trường `images_b64`; API hỗ trợ cả
`image_b64` và `images_b64`.

Response:

```json
{
  "gesture": "like",
  "confidence": 0.91,
  "inference_ms": 68.2,
  "model_version": "cnn-s05-partial-v1",
  "model_type": "cnn",
  "session_id": "demo-session",
  "request_id": "request-001"
}
```

## Azure Container Apps

Luồng build và deploy:

```text
GitHub Actions
  -> build deploy/azure/Dockerfile
  -> đóng gói FastAPI + model CNN
  -> push ghcr.io/anroiy123/iot-ck-gesture-api:azure
  -> Azure Container Apps kéo image từ GHCR
```

Tài nguyên hiện tại:

| Thành phần | Giá trị |
|---|---|
| Subscription | Azure for Students |
| Resource group | `rg-iot-ck-gesture` |
| Environment | `iot-ck-env` |
| Container App | `iot-ck-gesture-api` |
| Region | Japan East |
| Image | `ghcr.io/anroiy123/iot-ck-gesture-api:azure` |
| CPU/RAM | 1 CPU / 2 GiB |
| Min replicas hiện tại | 1 |
| Max replicas | 1 |

Model `models/gesture-cnn-baseline-s05-partial.keras` nằm trong GitHub
repository và được copy trực tiếp vào image. Azure không tải model từ Hugging
Face khi container khởi động.

### Deploy hoặc cập nhật

Chạy trong Bash/Azure Cloud Shell:

```bash
git clone https://github.com/Anroiy123/IOT_CK.git
cd IOT_CK
export GESTURE_API_KEY="KHOA_API_TU_DAT"
bash scripts/deploy_azure_container_app.sh
```

Script tự thử các region fallback nếu Azure for Students chặn region ban đầu.
Script deploy mặc định với `min-replicas=0` và `max-replicas=1`. Sau lần
deploy gần nhất, app đã được chỉnh thủ công thành `min-replicas=1` để phục vụ
demo.

### Cấu hình trước và sau demo

Giữ một replica khi demo để giảm cold start:

```powershell
az containerapp update `
  --name iot-ck-gesture-api `
  --resource-group rg-iot-ck-gesture `
  --min-replicas 1 `
  --max-replicas 1
```

Sau demo, cho phép scale về 0 để giảm chi phí:

```powershell
az containerapp update `
  --name iot-ck-gesture-api `
  --resource-group rg-iot-ck-gesture `
  --min-replicas 0 `
  --max-replicas 1
```

Azure for Students vẫn có thể phát sinh chi phí nếu vượt hạn mức. Theo dõi
Cost Management và budget alert trong Azure Portal.

## Chạy local làm fallback

Local mode vẫn giữ luồng `gateway -> FastAPI -> model -> gateway -> ESP32`,
nhưng bỏ RTT Internet.

Terminal 1:

```powershell
.\scripts\run_cloud_local.ps1
```

Kiểm tra:

```powershell
Invoke-RestMethod "http://127.0.0.1:8001/health"
Invoke-RestMethod "http://127.0.0.1:8001/v1/model"
Start-Process "http://127.0.0.1:8001/docs"
```

Terminal 2, dry-run:

```powershell
.\scripts\run_gateway.ps1 `
  -CloudUrl "http://127.0.0.1:8001" `
  -ApiKey "local-dev" `
  -DryRun
```

Chạy thật:

```powershell
.\scripts\run_gateway.ps1 `
  -CloudUrl "http://127.0.0.1:8001" `
  -ApiKey "local-dev" `
  -Esp32Host "<ESP32_IP>" `
  -Esp32Token $env:ESP32_COMMAND_TOKEN `
  -Speed 255
```

## Hugging Face Spaces

Repo vẫn giữ cấu hình trong `deploy/huggingface/` và script
`scripts/deploy_huggingface_space.ps1` để đối chiếu cloud provider. Đây không
phải backend chính của bản demo hiện tại.

## Dataset và model

### Dataset hiện tại

| Thành phần | Giá trị |
|---|---:|
| Số người | 5 (`s01` đến `s05`) |
| Số lớp | 8 |
| Số clip | 570 |
| Số frame | 8.550 |
| Train | 5.400 frame |
| Validation | 1.350 frame |
| Test | 1.800 frame |
| Cách chia | Theo người |

`s05` có 90 clip; `s01`-`s04` có 120 clip/người. `peace` và `no_gesture`
có 900 frame/lớp; sáu lớp còn lại có 1.125 frame/lớp.

Các cột `split` trong `data/metadata.csv` hiện chưa được ghi trực tiếp. Số liệu
train/validation/test ở trên lấy từ file metrics của lần huấn luyện theo người.

### CNN baseline bắt buộc

Model đang dùng:

```text
models/gesture-cnn-baseline-s05-partial.keras
```

| Chỉ số test | Giá trị |
|---|---:|
| Accuracy | 83,33% |
| Macro F1 | 83,37% |
| Kích thước ảnh | 160 x 160 |
| Backbone | MobileNetV3Small |
| Pretrained | ImageNet |

Metrics đầy đủ:

```text
reports/cnn_baseline_s05_partial_metrics.json
```

CNN-LSTM là mô hình so sánh nâng cao. Repo hiện có kiến trúc
`TimeDistributed(MobileNetV3Small) -> LSTM(64) -> Softmax`, nhưng chưa có kết
quả huấn luyện/đánh giá hoàn chỉnh để thay CNN baseline.

### Huấn luyện CNN

```powershell
.\.venv\Scripts\python.exe -m ml.train_cnn `
  --epochs 10 `
  --batch-size 16 `
  --output-model "models/gesture-cnn-baseline.keras" `
  --metrics-out "reports/cnn_baseline_metrics.json"
```

Benchmark inference local:

```powershell
.\.venv\Scripts\python.exe -m ml.benchmark_local `
  --model-path "models/gesture-cnn-baseline-s05-partial.keras" `
  --iterations 30
```

## Thu dữ liệu

Quy ước:

- Mỗi clip khoảng 1,5 giây.
- 10 FPS, khoảng 15 frame/clip.
- Ảnh crop được resize về 160 x 160.
- Dữ liệu nằm tại `data/raw/<subject>/<gesture>/<clip_id>/`.
- Metadata nằm tại `data/metadata.csv`.

Ví dụ thu đủ tám lớp:

```powershell
.\.venv\Scripts\python.exe -m ml.collect_data `
  --subject s06 `
  --clips-per-label 15 `
  --background complex `
  --lighting bright
```

Nhấn `Space` để bắt đầu từng clip và `q` để dừng.

Khi thu lại một lớp:

1. Xóa các clip sai trong `data/raw/<subject>/<gesture>/`.
2. Xóa đúng các dòng tương ứng khỏi `data/metadata.csv`.
3. Chạy lại tool với `--labels <gesture>`.

Không chia ngẫu nhiên theo frame vì các frame trong cùng clip gần như giống
nhau và gây data leakage.

## Kết quả latency hiện có

### Azure sau warm-up

Từ các dòng hợp lệ có `cloud_rtt_ms > 0` trong
`reports/gateway_azure_latency.csv`:

| Thành phần | Median | p95 |
|---|---:|---:|
| Cloud RTT | 155,77 ms | 172,89 ms |
| Inference | 62,36 ms | 72,03 ms |
| Tổng gateway | 172,32 ms | 194,58 ms |

Frame đầu sau khi container/model khởi động có thể chậm hơn đáng kể. Báo cáo
cold start riêng, không trộn với số liệu warm.

### Hugging Face trước đây

Các lần đo cũ trên Hugging Face có RTT cao hơn Azure. File
`reports/gateway_huggingface_latency.csv` được giữ để so sánh provider, không
đại diện cho backend demo hiện tại.

## Tiêu chí đánh giá

### Mức tối thiểu

- Nhận dạng và ánh xạ đủ 8 lớp.
- Chia train/validation/test theo người, không chia ngẫu nhiên theo frame.
- Báo cáo accuracy, Macro F1, confusion matrix và latency.
- Có cloud mode, local fallback và log `session_id`/`request_id`.
- ESP32 dừng khi gateway lỗi hoặc mất lệnh quá 600 ms.

### Mức mục tiêu

- Macro F1 trên người chưa xuất hiện trong train từ 0,90.
- Accuracy nền phức tạp giảm không quá 10 điểm phần trăm.
- False activation trên `no_gesture` dưới 2%.
- Median end-to-end không quá 300 ms; p95 không quá 500 ms.
- ESP32 áp dụng lệnh dừng trong 100 ms sau khi nhận.
- Không brownout khi motor và servo hoạt động đồng thời.

Kết quả CNN hiện tại chưa đạt mục tiêu Macro F1 0,90.

## Chạy test

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Kết quả xác minh ngày 14/06/2026:

```text
28 passed
```

## Troubleshooting

### UI hiện `cloud_error (0.00)`

Gateway không nhận được response hợp lệ từ cloud.

1. Kiểm tra có đang truyền nguyên placeholder `"<API_KEY>"` hay không.
2. Kiểm tra `.env` chứa đúng `AZURE_GESTURE_API_KEY`.
3. Kiểm tra endpoint `/health`.
4. Xem thông báo lỗi trong terminal và các cột `cloud_rtt_ms`, `inference_ms`
   trong CSV.
5. Nếu key sai, Azure trả HTTP `401`.

Các phiên gateway cũ có thể ghi lỗi cloud thành `no_gesture (0.00)`. Phiên bản
hiện tại dùng `cloud_error` để phân biệt với kết quả thật của model.

### UI hiện `no_gesture` nhưng confidence lớn hơn `0.00`

Cloud đã chạy model và model thật sự chọn lớp `no_gesture`. Cần:

- Đưa tay gần camera hơn và đủ sáng.
- Giữ cử chỉ giống quy ước khi thu dữ liệu.
- Kiểm tra ảnh crop/dataset và chất lượng model.

### Có gesture nhưng không có command

- Confidence phải từ `0.80`.
- Cử chỉ thường phải lặp 3 lần; `stop` lặp 2 lần.
- Kiểm tra cột `command` trong CSV.
- Đảm bảo không chạy với `-DryRun`.

### Có `command: forward` nhưng xe không chạy

- Gateway mặc định dùng `-Speed 180`; một số xe cần PWM cao hơn để thắng ma sát.
- Chạy demo với `-Speed 255`.
- Nếu xe chỉ giật từng nhịp, tăng thời gian giữ lệnh, ví dụ
  `-DriveHoldMs 800`, nhưng vẫn phải giữ khả năng dừng an toàn.
- Nếu vừa test WebSocket thủ công với `seq` lớn, hãy dùng bản gateway mới nhất.
  Gateway sẽ đọc `/state` để tiếp tục từ `last_seq`; nếu chạy bản cũ, ESP32 có
  thể từ chối lệnh là `stale_seq`.
- Nếu `esp32_ack_ms` trong CSV khác 0 nhưng bánh vẫn không quay, kiểm tra nguồn
  motor, GND chung, dây `ENA/ENB` và dây `IN1..IN4`.

### ESP32 không phản hồi

1. Kiểm tra laptop và ESP32 cùng Wi-Fi.
2. Lấy lại IP từ Serial Monitor vì DHCP có thể đổi IP.
3. Gọi `http://<ESP32_IP>/health`.
4. Kiểm tra `ESP32_COMMAND_TOKEN` trùng `COMMAND_TOKEN`.
5. Kiểm tra firewall/router có chặn thiết bị trong cùng mạng.

### Azure request đầu chậm

- Đặt `min-replicas=1` trước demo.
- Gọi `/health` và gửi vài request warm-up trước khi đo.
- Báo cáo cold start riêng.

### PlatformIO Home không mở

Không cần PIO Home. Dùng trực tiếp:

```powershell
.\.venv\Scripts\pio.exe run -d firmware
.\.venv\Scripts\pio.exe run -d firmware -t upload
```

## Cấu trúc repository

```text
firmware/                 Firmware PlatformIO chính cho ESP32
arduino/                  Bản Arduino IDE dùng khi cần
gateway/                  Camera, MediaPipe, cloud client, safety, WebSocket
cloud/                    FastAPI và inference
common/                   Protocol, label và gesture mapping
ml/                       Thu dữ liệu, train, benchmark và model policy
deploy/azure/              Dockerfile cho Azure
deploy/huggingface/        Cấu hình provider phụ
data/                     Metadata và dữ liệu thu
models/                   Model đã huấn luyện
reports/                  Metrics và latency log
scripts/                  Script setup, chạy và deploy
tests/                    Pytest
```

## Hạn chế và việc còn lại

- CNN hiện đạt Macro F1 83,37%, chưa đạt mục tiêu 90%.
- `one`, `two`, `like` và `dislike` vẫn còn nhầm lẫn.
- Dataset chưa cân bằng hoàn toàn giữa các lớp.
- CNN-LSTM chưa được huấn luyện và đánh giá đầy đủ.
- Chưa có báo cáo hoàn chỉnh theo nền đơn giản/phức tạp và false activation.
- Servo command đã có cooldown; nếu tay máy còn giật hoặc nhầm khớp, cần đo
  thêm log theo từng khớp và cải thiện dataset cho `one/two/like/dislike`.
- Cần đo thêm latency nhiều phiên và tách cold start/warm request.

## Tài liệu liên quan

- [Yêu cầu đề tài](requirement.txt)
- [Quy ước cử chỉ](label.md)
- [Công việc tiếp theo](NEXT_STEPS.md)
- [Dữ liệu](data/README.md)
- [Model](models/README.md)
- [Báo cáo](reports/README.md)
