# Cong viec can lam tiep theo - IOT_CK

Cap nhat theo trang thai hien tai: xe da nhan lenh WebSocket va motor da co chuyen dong nhe. Gateway, Cloud API local, webcam, tool thu du lieu va smoke train CNN da chay duoc.

## 1. Trang thai da xong

- ESP32 da nap firmware bang Arduino IDE/Arduino CLI qua COM5.
- ESP32 dang o IP: 192.168.2.126.
- HTTP debug da hoat dong:
  - http://192.168.2.126/health
  - http://192.168.2.126/state
- WebSocket dieu khien da ACK:
  - ws://192.168.2.126:81/
- Motor banh xe da co phan hoi khi gui lenh test thu cong.
- Servo tay may va motor da duoc test rieng, phan cung co ban OK.
- Cloud API local da chay tai:
  - http://127.0.0.1:8001/health
  - http://127.0.0.1:8001/docs
- Gateway UI da hien camera, mode, gesture, confidence, latency va command.
- Da thu du lieu subject s01:
  - 8 label
  - 41 clip
  - 615 frame
- Da train smoke CNN baseline:
  - model: models/gesture-cnn-baseline-smoke.keras
  - metrics: reports/cnn_baseline_smoke_metrics.json
  - ket qua chi de kiem tra pipeline, khong dung bao cao accuracy.
- Test Python gan nhat: 25 passed.

## 2. Viec uu tien tiep theo

### 2.1. Thu them du lieu cho du 4 nguoi

Muc tieu toi thieu cho bao cao:

- s01, s02, s03, s04
- 8 label moi nguoi
- 15 clip moi label moi nguoi
- Moi clip 1.5 giay, 10 FPS
- Co nen don gian, nen phuc tap, anh sang sang/toi

Lenh thu subject moi:

    .\.venv\Scripts\python.exe -m ml.collect_data --subject s02 --clips-per-label 15 --background simple --lighting bright

Thu tiep:

    .\.venv\Scripts\python.exe -m ml.collect_data --subject s03 --clips-per-label 15 --background complex --lighting bright

    .\.venv\Scripts\python.exe -m ml.collect_data --subject s04 --clips-per-label 15 --background simple --lighting dim

Neu co thoi gian, thu them s05 de ket qua on dinh hon.

### 2.2. Kiem tra chat luong dataset

Can viet/bo sung script thong ke dataset:

- So clip moi label moi subject
- So frame moi label
- Ty le MediaPipe tim thay tay theo label
- Clip nao thieu frame
- Label nao bi lech qua nhieu

Lenh kiem tra nhanh tam thoi:

    .\.venv\Scripts\python.exe -c "import csv; from collections import Counter; rows=list(csv.DictReader(open('data/metadata.csv', encoding='utf-8'))); print(Counter((r['subject_id'], r['gesture']) for r in rows))"

Dieu kien dat truoc khi train nghiem tuc:

- Moi subject co du 8 label
- Moi label co toi thieu 15 clip/subject
- Moi clip co 15 frame
- Cac label co tay nen co found_hand cao, ly tuong tren 85%
- no_gesture nen co found_hand gan 0%

### 2.3. Train CNN baseline chinh thuc

Sau khi co du s01-s04:

    .\.venv\Scripts\python.exe -m ml.train_cnn --metadata data\metadata.csv --epochs 10 --batch-size 16 --output-model models\gesture-cnn-baseline.keras --metrics-out reports\cnn_baseline_metrics.json

Can doc:

    reports\cnn_baseline_metrics.json

Can ghi vao bao cao:

- Accuracy
- Macro F1
- Confusion matrix
- Subject split strategy
- Cac label hay bi nham

Muc toi thieu:

- Macro F1 >= 0.85
- False activation tren no_gesture < 2%

Muc muc tieu:

- Macro F1 >= 0.90
- Nen phuc tap giam accuracy khong qua 10 diem phan tram

### 2.4. Noi model that vao Cloud API local

Sau khi co:

    models\gesture-cnn-baseline.keras

Can sua cloud inference de load model that va tien xu ly anh giong train.

Sau do chay local:

    $env:MODEL_PATH="models\gesture-cnn-baseline.keras"
    $env:MODEL_TYPE="cnn"
    $env:MODEL_VERSION="cnn-local-v1"
    .\.venv\Scripts\python.exe -m uvicorn cloud.app:app --host 127.0.0.1 --port 8001

Kiem tra:

    http://127.0.0.1:8001/v1/model

Mong doi:

- model_type = cnn
- model_version = cnn-local-v1
- predict tra gesture that, khong con luon no_gesture

### 2.5. Chay gateway voi model local

Khi Cloud API local da tra gesture that:

    .\scripts\run_gateway.ps1 -CloudUrl http://127.0.0.1:8001 -ApiKey local-dev -Esp32Token iot_ck_2026_demo

Test truoc khi de xe chay that:

- Ke banh xe len
- Dung cu chi stop
- Dung peace de vao che do xe
- Dung like/dislike/one/two tung lenh mot
- Quan sat command tren UI
- Kiem tra xe co dung sau 600 ms khi khong co lenh hop le

Chi dat xe xuong nen khi:

- stop nhan on dinh
- no_gesture khong kich hoat lenh
- Xe dung dung khi mat tay/khoi khung hinh
- Lenh tien/lui/trai/phai dung chieu

### 2.6. Train CNN-LSTM de so sanh

Sau khi CNN baseline chay duoc:

- Dung clip_id trong data/metadata.csv de gom chuoi frame
- Moi sample CNN-LSTM nen gom 8 frame
- Train CNN-LSTM cung train/val/test split theo subject
- So sanh voi CNN baseline

Tieu chi chon model:

- Chon CNN neu F1 thap hon CNN-LSTM khong qua 2 diem phan tram va latency nhanh hon it nhat 20%.
- Chon CNN-LSTM neu F1 cao hon it nhat 2 diem phan tram va p95 end-to-end van duoi 500 ms.

### 2.7. Deploy Cloud Run

Sau khi Cloud API local voi model that chay on:

Can cai Google Cloud CLI va tao project Google Cloud.

Can co:

- Billing
- Budget alert 5 USD voi moc 50%, 90%, 100%
- Region: asia-southeast1
- Cloud Run
- Cloud Storage

Deploy demo:

    .\scripts\deploy_cloud_run.ps1 -ProjectId <PROJECT_ID> -Demo

Che do Demo phai co min-instances=1 de giam cold start.

Sau deploy:

- Lay Cloud Run URL
- Set API key bang secret/env
- Chay gateway voi Cloud Run URL that

### 2.8. Do latency va hoan thien bao cao

Can thu cac log:

- Gateway CSV: reports/gateway_latency.csv
- Cloud inference_ms
- Cloud RTT
- ESP32 ACK ms
- End-to-end latency
- Cold start Cloud Run rieng

Can bao cao:

- Accuracy
- Macro F1
- Confusion matrix
- Latency median
- Latency p95
- False activation tren no_gesture
- Robustness tren background phuc tap
- So sanh CNN vs CNN-LSTM
- Kien truc he thong
- Anh mach/xe/demo

## 3. Checklist ngan han

- [ ] Thu s02 du 8 label, 15 clip/label.
- [ ] Thu s03 du 8 label, 15 clip/label.
- [ ] Thu s04 du 8 label, 15 clip/label.
- [ ] Kiem tra dataset metadata va found_hand.
- [ ] Train CNN baseline chinh thuc.
- [ ] Doc metrics CNN va confusion matrix.
- [ ] Sua Cloud API de load model CNN that.
- [ ] Test gateway voi model local khi xe dang ke banh.
- [ ] Neu on, test xe chay ngan tren san.
- [ ] Train CNN-LSTM va so sanh.
- [ ] Deploy Cloud Run voi min-instances=1.
- [ ] Do latency va viet bao cao.

## 4. Luu y quan trong

- Chua nen demo dieu khien bang cu chi khi model chua dat toi thieu.
- Khong dung accuracy cua smoke train de bao cao.
- Khong chia train/test theo frame trong bao cao cuoi; phai chia theo subject.
- Khong commit data/raw, model .keras that, Wi-Fi password hoac token.
- Khi test xe that, luon dam bao stop hoat dong truoc.
- Neu ESP32 doi IP sau khi reconnect Wi-Fi, sua lai Esp32Host khi chay gateway.
