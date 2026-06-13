# IOT_CK - Nhận dạng cử chỉ điều khiển xe và tay máy

Đề tài xây dựng hệ thống nhận dạng cử chỉ tay bằng Deep Learning để điều khiển
xe và tay máy qua ESP32.

Kiến trúc đang sử dụng:

```text
Webcam laptop
  -> Gateway: MediaPipe phát hiện/cắt bàn tay
  -> FastAPI + CNN (Hugging Face Spaces hoặc chạy local)
  -> Gateway lọc kết quả và ánh xạ lệnh
  -> WebSocket qua Wi-Fi
  -> ESP32
  -> L298N + motor / PCA9685 + servo
```

ESP32 không xử lý ảnh và không cần nối USB với laptop khi vận hành. USB chỉ cần
để nạp firmware, xem Serial Monitor hoặc cấp nguồn tạm thời.

## Trạng thái hiện tại

Cập nhật ngày 13/06/2026:

- Firmware ESP32 đã điều khiển được motor và bốn servo.
- Kênh điều khiển chính là WebSocket; HTTP chỉ dùng cho `/health` và `/state`.
- Gateway có giao diện camera, MediaPipe hand gate, safety filter và log CSV.
- CNN MobileNetV3Small đã được huấn luyện với dữ liệu của 5 người.
- FastAPI đã chạy local và đã deploy lên Hugging Face Spaces miễn phí.
- Connection pooling được dùng để giảm RTT cloud sau warm-up.
- Bộ test hiện tại: `28 passed`.

Hugging Face Space:

- Trang Space: <https://huggingface.co/spaces/anroiy/iot-ck-gesture-api>
- API: <https://anroiy-iot-ck-gesture-api.hf.space>
- Swagger: <https://anroiy-iot-ck-gesture-api.hf.space/docs>

## Kết quả hiện tại

### Dataset

| Thành phần | Giá trị |
|---|---:|
| Số người | 5 (`s01` đến `s05`) |
| Số lớp | 8 |
| Số clip | 570 |
| Số frame | 8.550 |
| Train | 5.400 frame |
| Validation | 1.350 frame |
| Test | 1.800 frame |
| Chiến lược chia | Theo người, không chia ngẫu nhiên theo frame |

`s05` hiện có 90 clip, ít hơn `s01`-`s04` (120 clip/người). Hai lớp
`peace` và `no_gesture` có 60 clip/lớp; các lớp còn lại có 75 clip/lớp.

### CNN baseline

Model đang dùng:

```text
models/gesture-cnn-baseline-s05-partial.keras
```

| Chỉ số test | Giá trị |
|---|---:|
| Accuracy | 83,33% |
| Macro F1 | 83,37% |
| Kích thước ảnh | 160 x 160 |
| Backbone | MobileNetV3Small, ImageNet pretrained |

Chi tiết từng lớp và confusion matrix:

```text
reports/cnn_baseline_s05_partial_metrics.json
```

### Latency Hugging Face

Số liệu từ `reports/gateway_huggingface_latency.csv`, chỉ tính các frame thực
sự phát hiện tay và gọi cloud:

| Thành phần | Median | p95 |
|---|---:|---:|
| Capture | 2,1 ms | 5,8 ms |
| MediaPipe + JPEG | 13,6 ms | 26,9 ms |
| Cloud RTT | 338,2 ms | 821,1 ms |
| Inference trên Space | 76,7 ms | 105,2 ms |
| ESP32 ACK (các frame có lệnh) | 69,1 ms | 137,0 ms |
| End-to-end gateway | 362,2 ms | 845,0 ms |

Model trên cloud không phải bottleneck chính; phần lớn latency đến từ mạng tới
Hugging Face. Vì vậy:

- **Cloud mode** dùng để chứng minh kiến trúc cloud và đo latency.
- **Local mode** nên dùng khi demo xe cần phản hồi nhanh và ổn định.

## Cử chỉ và chức năng

| Label | Cách làm tay | Chế độ xe | Chế độ tay máy |
|---|---|---|---|
| `stop` | Xòe bàn tay, 5 ngón rõ | Dừng xe | Dừng motor |
| `peace` | Chữ V rộng | Chuyển sang chế độ xe | Chuyển sang chế độ xe |
| `rock` | Ngón trỏ và ngón út | Chuyển sang tay máy | Chuyển sang tay máy |
| `like` | Ngón cái hướng lên | Tiến | Tăng góc khớp 5 độ |
| `dislike` | Ngón cái hướng xuống | Lùi | Giảm góc khớp 5 độ |
| `one` | Một ngón trỏ | Rẽ trái | Chọn khớp trước |
| `two` | Hai ngón sát nhau | Rẽ phải | Chọn khớp tiếp |
| `no_gesture` | Không có tay hợp lệ | Không phát lệnh | Không phát lệnh |

Thứ tự khớp tay máy:

```text
base -> lower -> upper -> gripper
```

`peace` và `two` dễ nhầm. Khi thu dữ liệu, `peace` nên tạo chữ V rộng, còn
`two` giữ hai ngón sát và thẳng.

## Cơ chế an toàn

- Cử chỉ thường cần confidence >= 0,80 và lặp 3 lần liên tiếp.
- `stop` cần 2 kết quả liên tiếp.
- Không thấy bàn tay thì MediaPipe trả `no_gesture` và không gọi cloud.
- Camera lỗi, cloud timeout hoặc WebSocket lỗi thì gateway cố gửi `stop`.
- ESP32 từ chối token sai, sequence cũ và TTL không hợp lệ.
- ESP32 tự dừng motor nếu không nhận lệnh hợp lệ trong 600 ms.
- Servo bị giới hạn góc theo từng khớp và chỉ thay đổi 5 độ mỗi lệnh.

Không hạ confidence hoặc số lần xác nhận chỉ để xe phản hồi nhanh hơn nếu chưa
đánh giá lại false activation.

## Phần cứng và pinout

Pinout firmware hiện tại:

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

PCA9685 dùng địa chỉ `0x40`, tần số 50 Hz. Servo dùng channel 0-3 theo thứ tự
`base`, `lower`, `upper`, `gripper`.

GPIO12 là strapping pin. Nếu ESP32 khởi động không ổn định, chuyển IN1 sang
GPIO33 và cập nhật `PIN_IN1` trong config.

Motor và servo phải dùng nguồn phù hợp, chung GND với ESP32. Không cấp toàn bộ
motor/servo trực tiếp từ chân 5V của ESP32.

## Cấu trúc repository

```text
firmware/                 PlatformIO firmware cho ESP32
arduino/                  Bản Arduino IDE/phần thử nghiệm phần cứng
gateway/                  Webcam, MediaPipe, cloud client, safety, WebSocket
cloud/                    FastAPI và model inference
ml/                       Thu dữ liệu, split, CNN, CNN-LSTM, benchmark
common/                   Protocol, label và ánh xạ cử chỉ
deploy/huggingface/       Docker Space configuration
data/                     Metadata và dữ liệu thu
models/                   Model đã huấn luyện
reports/                  Metrics, latency log và kết quả đánh giá
scripts/                  Script setup, chạy gateway và deploy
tests/                    Pytest
```

## Yêu cầu môi trường

- Windows 10/11 và PowerShell.
- Python 3.11. Không dùng Python 3.14 cho TensorFlow hiện tại.
- VS Code + PlatformIO hoặc PlatformIO CLI.
- ESP32 DevKit kết nối Wi-Fi cùng mạng với laptop.
- Webcam laptop/USB.

Tạo môi trường:

```powershell
py -3.11 -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Hoặc chạy script setup:

```powershell
.\scripts\setup_windows.ps1
```

Kiểm tra:

```powershell
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m pytest -q
```

## Cấu hình bí mật

Không commit SSID, mật khẩu, command token hoặc API key.

### ESP32

Tạo/chỉnh:

```text
firmware/include/config.h
```

Các giá trị bắt buộc:

```cpp
#define WIFI_SSID "TEN_WIFI"
#define WIFI_PASSWORD "MAT_KHAU_WIFI"
#define COMMAND_TOKEN "TOKEN_DIEU_KHIEN"
```

Giữ các hằng số pinout có sẵn trong file. `firmware/include/config.h` đã được
Git ignore.

### Gateway

Tạo file `.env` ở root:

```dotenv
GESTURE_API_KEY=API_KEY_CUA_CLOUD_API
ESP32_COMMAND_TOKEN=TOKEN_DIEU_KHIEN
```

`.env` đã được Git ignore. API key cloud và command token ESP32 có thể khác
nhau; không dùng Hugging Face access token làm API key của ứng dụng.

Phân biệt hai token quan trọng:

- `GESTURE_API_KEY`: khóa bí mật của API nhận dạng cử chỉ trên cloud. Gateway
  gửi khóa này trong header `X-API-Key` khi gọi `/v1/predict`.
- `ESP32_COMMAND_TOKEN`: khóa điều khiển ESP32. Gateway gửi khóa này trong gói
  WebSocket để ESP32 từ chối lệnh lạ.

Hai khóa này do nhóm tự đặt, không phải lấy từ Azure Portal, Hugging Face hay
Google Cloud. Không commit giá trị thật vào GitHub.

## Nạp firmware ESP32

Mặc định PlatformIO dùng board `esp32dev`, port upload/monitor `COM5`.

Build:

```powershell
.\.venv\Scripts\pio.exe run -d firmware
```

Upload:

```powershell
.\.venv\Scripts\pio.exe run -d firmware -t upload
```

Serial Monitor:

```powershell
.\.venv\Scripts\pio.exe device monitor -p COM5 -b 115200
```

Sau khi khởi động, Serial Monitor in IP Wi-Fi của ESP32. IP có thể thay đổi khi
router cấp DHCP lại.

Kiểm tra qua Wi-Fi:

```powershell
Invoke-RestMethod http://<ESP32_IP>/health
Invoke-RestMethod http://<ESP32_IP>/state
```

Kết quả `/health` mong đợi:

```json
{"status":"ok"}
```

HTTP không dùng để gửi lệnh điều khiển. Gateway gửi JSON qua:

```text
ws://<ESP32_IP>:81/
```

## Chạy hệ thống

### 1. Cloud mode - Hugging Face

Chế độ này đúng kiến trúc cloud của đề tài nhưng phụ thuộc Internet và có thể
có cold start.

Kiểm tra camera + cloud, không gửi lệnh tới ESP32:

```powershell
.\scripts\run_gateway_huggingface.ps1 -DryRun
```

Chạy thật:

```powershell
.\scripts\run_gateway_huggingface.ps1 -Esp32Host <ESP32_IP>
```

Nhấn `q` để thoát. Log mặc định:

```text
reports/gateway_huggingface_latency.csv
```

Nếu Space vừa ngủ, request đầu có thể chậm. Mở `/health` trước khi demo:

```powershell
Invoke-RestMethod https://anroiy-iot-ck-gesture-api.hf.space/health
```

### 2. Local mode - ưu tiên khi điều khiển xe

Terminal 1, chạy FastAPI và model trên laptop:

```powershell
.\scripts\run_cloud_local.ps1
```

Kiểm tra:

```powershell
Invoke-RestMethod http://127.0.0.1:8001/health
Start-Process http://127.0.0.1:8001/docs
```

Terminal 2, chạy gateway:

```powershell
$env:ESP32_COMMAND_TOKEN="TOKEN_DIEU_KHIEN"
.\scripts\run_gateway.ps1 `
  -CloudUrl http://127.0.0.1:8001 `
  -ApiKey local-dev `
  -Esp32Host <ESP32_IP> `
  -Esp32Token $env:ESP32_COMMAND_TOKEN
```

Local mode vẫn giữ pipeline MediaPipe -> FastAPI -> gateway -> ESP32, nhưng bỏ
RTT Internet nên phù hợp hơn khi quay demo xe.

### 3. Chạy gateway không điều khiển xe

Thêm `-DryRun` để xử lý camera, model và log nhưng không gửi lệnh tới ESP32:

```powershell
.\scripts\run_gateway.ps1 `
  -CloudUrl http://127.0.0.1:8001 `
  -ApiKey local-dev `
  -DryRun
```

## Gateway UI và log

Cửa sổ gateway hiển thị:

- Mode hiện tại: `car` hoặc `arm`.
- Gesture và confidence.
- Tổng latency của frame.
- Command vừa gửi.

CSV log gồm:

- `session_id`, `request_id`.
- Capture và preprocessing latency.
- Cloud RTT và model inference latency.
- ESP32 ACK latency.
- Gesture, confidence, mode và command.

Mỗi phiên demo nên dùng file log riêng để không trộn số liệu cũ.

## Cloud API

### `GET /health`

```json
{"status":"ok"}
```

### `GET /v1/model`

Trả model version và model type.

### `POST /v1/predict`

Header:

```text
X-API-Key: <GESTURE_API_KEY>
```

Body:

```json
{
  "image_b64": "<JPEG_BASE64>",
  "session_id": "demo-session",
  "request_id": "request-001"
}
```

Response:

```json
{
  "gesture": "like",
  "confidence": 0.91,
  "inference_ms": 82.4,
  "model_version": "cnn-s05-partial-v1",
  "model_type": "cnn",
  "session_id": "demo-session",
  "request_id": "request-001"
}
```

## Thu dữ liệu

Quy ước mặc định:

- Mỗi clip dài 1,5 giây.
- 10 FPS, khoảng 15 frame/clip.
- Ảnh crop được resize về 160 x 160.
- Dữ liệu lưu trong `data/raw/<subject>/<gesture>/<clip_id>/`.
- Metadata lưu trong `data/metadata.csv`.

Ví dụ thu đủ tám lớp cho một người:

```powershell
.\.venv\Scripts\python.exe -m ml.collect_data `
  --subject s06 `
  --clips-per-label 15 `
  --background complex `
  --lighting bright
```

Nhấn `Space` để bắt đầu từng clip, nhấn `q` để dừng.

Thu lại một lớp:

1. Xóa thư mục clip sai trong `data/raw/<subject>/<gesture>/`.
2. Xóa các dòng tương ứng trong `data/metadata.csv`.
3. Chạy lại tool với `--labels <gesture>`.

Không chia train/validation/test ngẫu nhiên theo frame vì các frame trong cùng
clip gần như giống nhau và sẽ gây data leakage.

## Huấn luyện và đánh giá

Huấn luyện CNN baseline:

```powershell
.\.venv\Scripts\python.exe -m ml.train_cnn `
  --epochs 10 `
  --batch-size 16 `
  --output-model models/gesture-cnn-baseline.keras `
  --metrics-out reports/cnn_baseline_metrics.json
```

Benchmark local:

```powershell
.\.venv\Scripts\python.exe -m ml.benchmark_local `
  --model-path models/gesture-cnn-baseline-s05-partial.keras `
  --iterations 30
```

Kiểm tra kiến trúc CNN-LSTM:

```powershell
.\.venv\Scripts\python.exe -m ml.train_cnn_lstm --summary
```

CNN là baseline bắt buộc. CNN-LSTM hiện mới có phần định nghĩa kiến trúc
`TimeDistributed(MobileNetV3Small) -> LSTM(64) -> Softmax`; pipeline tạo
sequence, huấn luyện và đánh giá đầy đủ vẫn cần hoàn thiện.

## Deploy Hugging Face Spaces

Đăng nhập CLI:

```powershell
.\.venv\Scripts\huggingface-cli.exe login
```

Chuẩn bị staging:

```powershell
.\scripts\deploy_huggingface_space.ps1 `
  -Space <HF_USERNAME>/iot-ck-gesture-api `
  -PrepareOnly
```

Tạo và upload Space:

```powershell
.\scripts\deploy_huggingface_space.ps1 `
  -Space <HF_USERNAME>/iot-ck-gesture-api `
  -Create
```

Đặt `GESTURE_API_KEY` trong Settings -> Variables and secrets của Space. Không
đưa Hugging Face access token hoặc API key vào repository.

Cloud Run vẫn có script `scripts/deploy_cloud_run.ps1`, nhưng project Google
Cloud hiện yêu cầu kích hoạt billing/prepayment nên không phải lựa chọn demo
miễn phí của nhóm.

## Deploy Azure Container Apps

Subscription đang dùng nên là `Azure for Students`. Nên dùng Azure Container
Apps Consumption với `min-replicas=0`, `max-replicas=1` để giảm chi phí. Theo
tài liệu Azure, Container Apps Consumption có free grant hằng tháng; nếu vượt
free grant hoặc bật thêm tài nguyên Azure khác thì vẫn có thể phát sinh phí.

Luồng deploy Azure của repo:

```text
GitHub Actions
  -> build deploy/azure/Dockerfile
  -> push image ghcr.io/anroiy123/iot-ck-gesture-api:azure
  -> Azure Container Apps kéo image public từ GHCR
```

Model `models/gesture-cnn-baseline-s05-partial.keras` được commit trực tiếp
trong GitHub repository vì file hiện chỉ khoảng 4,38 MB. Dockerfile Azure copy
model từ build context, nên pipeline Azure không phụ thuộc Hugging Face.

Các bước:

1. Commit và push các file Azure mới lên GitHub.
2. Mở GitHub repo `Anroiy123/IOT_CK`.
3. Vào Actions -> `Build Azure Container Image` -> `Run workflow`.
4. Chờ image `ghcr.io/anroiy123/iot-ck-gesture-api:azure` build xong.
5. Mở Azure Portal -> Cloud Shell.
6. Clone repo và chạy script:

```bash
git clone https://github.com/Anroiy123/IOT_CK.git
cd IOT_CK
export GESTURE_API_KEY="<AZURE_API_KEY>"
bash scripts/deploy_azure_container_app.sh
```

`<AZURE_API_KEY>` là chuỗi bí mật do nhóm tự chọn tại thời điểm deploy. Script
sẽ đưa giá trị này vào biến môi trường `GESTURE_API_KEY` của Azure Container
App. Gateway phải dùng lại đúng chuỗi đó ở tham số `-ApiKey` hoặc biến
`AZURE_GESTURE_API_KEY`.

Ví dụ demo có thể đặt:

```bash
export GESTURE_API_KEY="azure_iot_ck_2026_demo"
```

Không gõ nguyên chuỗi placeholder `"<AZURE_API_KEY>"` hoặc `"<API_KEY>"` khi
chạy thật. Nếu dùng placeholder, Azure sẽ trả `401` và gateway sẽ hiển thị
`no_gesture (0.00)` vì request cloud bị từ chối.

Script mặc định:

- Resource group: `rg-iot-ck-gesture`
- Region ban đầu: `southeastasia`; nếu Azure for Students policy chặn region
  này, script tự thử các region fallback cho Container Apps.
- Container Apps environment: `iot-ck-env`
- App name: `iot-ck-gesture-api`
- Image: `ghcr.io/anroiy123/iot-ck-gesture-api:azure`
- CPU/RAM: `1.0 CPU`, `2.0Gi`
- Scale: `min-replicas=0`, `max-replicas=1`
- Ingress: external HTTP, target port `7860`
- Logs destination: `none` để không tạo Log Analytics workspace. Gateway vẫn
  ghi log latency CSV ở laptop.

Sau khi script in URL Azure, kiểm tra:

```powershell
Invoke-RestMethod https://<AZURE_APP_URL>/health
Invoke-RestMethod https://<AZURE_APP_URL>/v1/model
```

Chạy gateway với Azure:

```powershell
$env:AZURE_GESTURE_API_KEY="AZURE_API_KEY_DA_DAT_LUC_DEPLOY"
.\scripts\run_gateway_azure.ps1 `
  -AzureUrl https://<AZURE_APP_URL> `
  -DryRun
```

Chạy thật với ESP32:

```powershell
$env:AZURE_GESTURE_API_KEY="AZURE_API_KEY_DA_DAT_LUC_DEPLOY"
$env:ESP32_COMMAND_TOKEN="TOKEN_DIEU_KHIEN_DA_NAP_VAO_ESP32"
.\scripts\run_gateway_azure.ps1 `
  -AzureUrl https://<AZURE_APP_URL> `
  -Esp32Host <ESP32_IP>
```

Khi test xong, nếu không cần giữ Azure chạy, xóa resource group để tránh chi phí:

```bash
az group delete --name rg-iot-ck-gesture --yes --no-wait
```

## Chạy test

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Kết quả gần nhất:

```text
28 passed
```

Test bao phủ protocol, gesture mapping, safety filter, cloud API, HTTP
connection reuse, data split, data collection và CNN pipeline.

## Troubleshooting

### ESP32 không phản hồi qua Wi-Fi

1. Kiểm tra ESP32 và laptop cùng mạng Wi-Fi.
2. Xem IP mới trong Serial Monitor.
3. Chạy `Invoke-RestMethod http://<ESP32_IP>/health`.
4. Cập nhật `-Esp32Host` khi chạy gateway.
5. Kiểm tra firewall/router có chặn client-to-client hay không.

### Gateway nhận tay nhưng không gửi command

- Confidence có thể thấp hơn 0,80.
- Cử chỉ chưa lặp đủ 3 lần; `stop` cần 2 lần.
- Xem cột `gesture`, `confidence`, `command` trong CSV.
- Kiểm tra command token trong gateway có khớp firmware.

### Hugging Face latency cao

- Gọi `/health` trước để đánh thức Space.
- Dùng mạng ổn định.
- Không đóng gateway liên tục vì HTTP session cần warm-up.
- Dùng local mode cho phần demo điều khiển xe.
- Giữ cloud mode để đo và báo cáo latency thực tế.

### PlatformIO không mở PIO Home

PIO Home không bắt buộc để build/upload:

```powershell
.\.venv\Scripts\pio.exe run -d firmware
.\.venv\Scripts\pio.exe run -d firmware -t upload
```

### ESP32 boot không ổn định

GPIO12 là strapping pin. Chuyển IN1 sang GPIO33 cả trong mạch và
`firmware/include/config.h`.

## Hạn chế và công việc tiếp theo

- Accuracy 83,33% và Macro F1 83,37% chưa đạt mục tiêu 90%.
- `one`, `two`, `like` và `dislike` còn nhầm lẫn đáng kể.
- Dữ liệu `s05`, `peace` và `no_gesture` chưa cân bằng với các lớp khác.
- Cần huấn luyện/đánh giá CNN-LSTM trên cùng subject split.
- Cần báo cáo accuracy theo nền đơn giản/phức tạp và false activation.
- Cần đo local/cloud latency theo nhiều phiên và báo cáo cold start riêng.
- Free Hugging Face Space không bảo đảm p95 dưới 500 ms.

Tiêu chí lựa chọn model cuối:

- Chọn CNN nếu accuracy thấp hơn CNN-LSTM không quá 2 điểm phần trăm và latency
  nhanh hơn ít nhất 20%.
- Chọn CNN-LSTM nếu cải thiện tối thiểu 2 điểm phần trăm và p95 end-to-end vẫn
  đáp ứng yêu cầu demo.

## Tài liệu liên quan

- Yêu cầu đề tài: [requirement.txt](requirement.txt)
- Quy ước cử chỉ: [label.md](label.md)
- Công việc tiếp theo: [NEXT_STEPS.md](NEXT_STEPS.md)
- TensorFlow: <https://www.tensorflow.org/install/pip>
- MediaPipe: <https://developers.google.com/mediapipe/solutions/vision/gesture_recognizer/python>
- Hugging Face Docker Spaces: <https://huggingface.co/docs/hub/en/spaces-sdks-docker>
- HaGRID: <https://github.com/hukenovs/hagrid>
