# IOT_CK - Gesture Recognition CarArm

De tai: thiet bi nhan dang cu chi tay dung Deep Learning de dieu khien xe va tay may. Model suy luan duoc dat tren cloud; laptop lam gateway camera va ESP32 chi phu trach dieu khien motor/servo.

## Trang thai hien tai

Tinh den ngay 2026-06-13:

- ESP32 da nap firmware thanh cong qua Arduino IDE/Arduino CLI tren COM5.
- ESP32 da ket noi Wi-Fi va dang co IP 192.168.2.126.
- HTTP debug cua ESP32 da test:
  - GET http://192.168.2.126/health tra {"status":"ok"}.
  - GET http://192.168.2.126/state tra state hop le, motor dung, servo giu goc an toan.
- WebSocket dieu khien ws://192.168.2.126:81/ da ACK lenh stop, do tre khoang 7.71 ms.
- Webcam laptop mo duoc voi camera index 0, frame 640x480.
- MediaPipe cropper chay duoc.
- Cloud API local chay duoc tai http://127.0.0.1:8001.
- Gateway UI da chay duoc va hien mode, gesture, confidence, latency va command.
- Motor banh xe va servo tay may da duoc test rieng truoc do va hoat dong binh thuong.
- Chua co model nhan dang that, nen Cloud API local hien tra fallback no_gesture.

Trang thai nay co nghia la phan tich hop co ban da xong:

    Webcam -> Gateway MediaPipe/crop -> Cloud API -> Gateway -> ESP32 WebSocket -> L298N/PCA9685

## Viec can lam tiep

Thu tu nen lam tiep:

1. Tao cong cu thu du lieu cu chi.
2. Thu du lieu thu nho de kiem tra pipeline.
3. Huan luyen CNN baseline bat buoc.
4. Do local inference de so sanh voi cloud.
5. Huan luyen CNN-LSTM de so sanh nang cao.
6. Deploy model len Cloud Run.
7. Chay gateway voi Cloud Run that va test xe bang cu chi.
8. Do latency, confusion matrix, macro F1 va viet bao cao.

## Kien truc he thong

    Laptop webcam
        |
        v
    Gateway laptop
      - doc camera
      - MediaPipe detect/crop ban tay
      - hien UI
      - ghi CSV latency
        |
        v
    Cloud API / Cloud Run
      - /health
      - /v1/model
      - /v1/predict
        |
        v
    Gateway laptop
      - loc confidence
      - chong kich hoat sai
      - map gesture -> command
        |
        v
    ESP32 qua WebSocket port 81
      - L298N dieu khien motor banh xe
      - PCA9685 dieu khien servo tay may

HTTP tren ESP32 chi dung de debug:

    GET /health
    GET /state

Kenh dieu khien chinh xuong ESP32 la WebSocket.

## Cau truc thu muc

| Thu muc | Vai tro |
| --- | --- |
| arduino/ | Sketch Arduino IDE da nap thanh cong cho ESP32 |
| firmware/ | Ban PlatformIO cua firmware, giu de phat trien tiep neu can |
| gateway/ | Webcam, MediaPipe crop, Cloud client, UI, WebSocket transport, CSV log |
| cloud/ | FastAPI API cho local dev va Cloud Run |
| ml/ | Train CNN baseline, CNN-LSTM, split data, benchmark local inference |
| common/ | Protocol chung: mode, action, command payload, gesture mapping |
| data/ | Metadata va huong dan dataset; khong commit anh/video lon |
| models/ | Metadata model; model that nen luu Cloud Storage |
| reports/ | CSV latency, ket qua danh gia, confusion matrix |
| scripts/ | Script setup, gateway, deploy Cloud Run |
| tests/ | Pytest cho protocol, gateway safety, cloud API, ML policy |

## Pinout he thong

Tai lieu nay phan anh cach noi day hien tai.

### 1. He thong nguon

| Diem xuat phat | Diem den 1 | Diem den 2 | Diem den 3 |
| --- | --- | --- | --- |
| Pin Duong (+) 11.1V | L298N 12V | Mini560 IN+ |  |
| Pin Am (-) / GND | L298N GND | Mini560 IN- | Testboard dai GND |
| Mini560 OUT+ | Testboard dai 5V |  |  |
| Mini560 OUT- | Testboard dai GND |  |  |
| Testboard dai 5V | ESP32 5V/VIN | PCA9685 domino V+ |  |
| Testboard dai GND | ESP32 GND | PCA9685 domino GND | PCA9685 header GND |

### 2. Tin hieu banh xe: ESP32 -> L298N

| Chan ESP32 | Chan L298N | Chuc nang |
| --- | --- | --- |
| GPIO 13 | ENA | Toc do cum banh trai PWM |
| GPIO 12 | IN1 | Chieu quay 1 cum trai |
| GPIO 14 | IN2 | Chieu quay 2 cum trai |
| GPIO 27 | IN3 | Chieu quay 1 cum phai |
| GPIO 26 | IN4 | Chieu quay 2 cum phai |
| GPIO 25 | ENB | Toc do cum banh phai PWM |

Luu y: GPIO12 la chan strapping cua ESP32. Neu sau nay ESP32 boot khong on dinh, chuyen IN1 sang GPIO33 va sua firmware.

### 3. Tin hieu canh tay: ESP32 -> PCA9685

| Chan ESP32 | Chan PCA9685 | Chuc nang |
| --- | --- | --- |
| 3V3 | VCC | Nguon logic I2C |
| GPIO 21 | SDA | Du lieu I2C |
| GPIO 22 | SCL | Xung nhip I2C |

### 4. Thiet bi chap hanh

| Nguon phat | Diem cam | Thiet bi |
| --- | --- | --- |
| L298N OUT1 va OUT2 | Kep song song 2 motor | 2 banh xe trai |
| L298N OUT3 va OUT4 | Kep song song 2 motor | 2 banh xe phai |
| PCA9685 slot 0 | Cam -> PWM, Do -> V+, Nau -> GND | Servo base |
| PCA9685 slot 1 | Cam -> PWM, Do -> V+, Nau -> GND | Servo tay duoi |
| PCA9685 slot 2 | Cam -> PWM, Do -> V+, Nau -> GND | Servo tay tren |
| PCA9685 slot 3 | Cam -> PWM, Do -> V+, Nau -> GND | Servo gripper |

## Ghi chu an toan phan cung

- Tat ca GND phai noi chung: pin, L298N, Mini560, ESP32, PCA9685.
- PCA9685 VCC lay tu ESP32 3V3.
- PCA9685 V+ lay 5V tu Mini560 de cap cho servo.
- Khong cap servo tu chan 3V3 cua ESP32.
- Chan 5V cua L298N de trong trong cau hinh hien tai.
- Khi test lenh motor, nen ke banh xe khoi mat dat.
- Firmware co watchdog: neu khong nhan lenh hop le qua 600 ms thi xe tu dung.

## Firmware ESP32

### Cach chinh hien tai: Arduino IDE

Sketch da nap thanh cong:

    arduino/IOT_CK_CarArm/IOT_CK_CarArm.ino

File cau hinh rieng:

    arduino/IOT_CK_CarArm/config.h

config.h chua Wi-Fi va token dieu khien, khong commit len Git.

Noi dung can co:

    #define WIFI_SSID "ten_wifi"
    #define WIFI_PASSWORD "mat_khau_wifi"
    #define COMMAND_TOKEN "token_bi_mat"

Thu vien Arduino da dung:

- esp32:esp32 core 3.3.10
- ArduinoJson
- WebSockets
- Adafruit PWM Servo Driver
- Adafruit BusIO

Lenh da dung de bien dich:

    & 'C:\Users\hunga\AppData\Local\Programs\Arduino IDE\resources\app\lib\backend\resources\arduino-cli.exe' compile --fqbn esp32:esp32:esp32 arduino\IOT_CK_CarArm

Lenh da dung de nap:

    & 'C:\Users\hunga\AppData\Local\Programs\Arduino IDE\resources\app\lib\backend\resources\arduino-cli.exe' upload -p COM5 --fqbn esp32:esp32:esp32 arduino\IOT_CK_CarArm

Log nap da xac nhan:

    Chip type: ESP32-D0WD-V3
    MAC: 20:9b:a9:60:d0:cc
    Hash of data verified
    Hard resetting via RTS pin

Log khoi dong da xac nhan:

    IOT_CK CarArm starting
    Connecting WiFi...
    WiFi connected. IP: 192.168.2.126
    HTTP debug: port 80 (/health, /state)
    WebSocket command: port 81
    Serial test: f/b/l/r/s, joint 0-3, +/-

### Lenh test ESP32

Kiem tra health:

    Invoke-RestMethod -Uri 'http://192.168.2.126/health'

Kiem tra state:

    Invoke-RestMethod -Uri 'http://192.168.2.126/state' | ConvertTo-Json -Depth 5

Gui lenh stop qua WebSocket:

    .\.venv\Scripts\python.exe -c "import json, time, websocket; ws=websocket.create_connection('ws://192.168.2.126:81/', timeout=3); payload={'seq':1001,'session_id':'manual-smoke','request_id':'ws-stop-smoke','mode':'car','action':'stop','speed':0,'ttl_ms':600,'token':'<ESP32_TOKEN>'}; t=time.perf_counter(); ws.send(json.dumps(payload)); print(ws.recv()); print('ack_ms=',round((time.perf_counter()-t)*1000,2)); ws.close()"

### PlatformIO

PlatformIO Home hien da mo lai duoc trong VS Code. Tuy nhien firmware da duoc nap thanh cong bang Arduino IDE, nen duong chinh tam thoi la arduino/.

Ban PlatformIO van nam trong:

    firmware/

Neu muon quay lai PlatformIO, mo folder repo trong VS Code roi chon project co firmware/platformio.ini.

## Cloud API local

Cloud API dung FastAPI. Local dev hien chay tai:

    http://127.0.0.1:8001

Chay server local:

    .\.venv\Scripts\python.exe -m uvicorn cloud.app:app --host 127.0.0.1 --port 8001

Endpoint:

    GET  /health
    GET  /v1/model
    POST /v1/predict

Kiem tra nhanh trong trinh duyet:

    http://127.0.0.1:8001/health
    http://127.0.0.1:8001/docs

Trang root http://127.0.0.1:8001/ khong phai endpoint cua app, nen khong dung de kiem tra.

Hien tai neu chua co model, API se tra:

    gesture = no_gesture
    confidence = 0.0

Day la fallback an toan, khong phai loi.

## Gateway laptop

Chay gateway voi Cloud API local:

    .\scripts\run_gateway.ps1 -CloudUrl http://127.0.0.1:8001 -ApiKey local-dev -Esp32Token <ESP32_TOKEN>

Mac dinh script dung:

    ESP32 host: 192.168.2.126
    ESP32 WebSocket: ws://192.168.2.126:81/
    Camera index: 0
    Log CSV: reports/gateway_latency.csv

Neu can chi dinh lai:

    .\scripts\run_gateway.ps1 -CloudUrl http://127.0.0.1:8001 -ApiKey local-dev -Esp32Host 192.168.2.126 -Esp32Token <ESP32_TOKEN> -Camera 0

Gateway UI hien:

    mode: car
    gesture: no_gesture (0.00)
    latency: <ms>
    command: -

Neu thay no_gesture (0.00) trong giai doan nay thi dung, vi chua co model that.

Chay smoke test khong hien UI:

    .\scripts\run_gateway.ps1 -CloudUrl http://127.0.0.1:8001 -ApiKey local-dev -Esp32Token <ESP32_TOKEN> -Headless -MaxFrames 10 -Log reports\gateway_smoke.csv

Gateway co co che an toan:

- stop chi can 2 prediction lien tiep.
- Lenh thuong can confidence >= 0.80 trong 3 prediction lien tiep.
- Khong co lenh hop le qua 600 ms thi gui stop.
- Camera loi, cloud timeout hoac Wi-Fi/ESP32 loi thi uu tien dung xe.
- Moi dong log co session_id va request_id.

## Bo cu chi

| Cu chi | Chuc nang |
| --- | --- |
| stop | Dung khan cap toan he thong |
| peace | Chuyen sang che do xe |
| rock | Chuyen sang che do tay may |
| like | Xe tien hoac tang goc servo |
| dislike | Xe lui hoac giam goc servo |
| one | Xe trai hoac chon khop truoc |
| two | Xe phai hoac chon khop tiep |
| no_gesture | Khong phat lenh |

Trong che do tay may, khop duoc chon vong:

    base -> lower -> upper -> gripper -> base

## ML va danh gia

CNN la baseline bat buoc. CNN-LSTM la mo hinh so sanh nang cao.

### Train CNN baseline

Train smoke voi du lieu s01 hien tai de kiem tra pipeline:

    .\.venv\Scripts\python.exe -m ml.train_cnn --metadata data\metadata.csv --epochs 1 --batch-size 8 --max-per-class 12 --smoke --no-pretrained --output-model models\gesture-cnn-baseline-smoke.keras --metrics-out reports\cnn_baseline_smoke_metrics.json

Ket qua smoke gan nhat:

    split_strategy: frame_stratified_smoke
    total samples used: 96
    train/val/test: 67/14/15
    accuracy: 0.1333
    macro_f1: 0.0294

Ket qua nay chi xac nhan pipeline train chay duoc. Khong dung de bao cao accuracy vi moi co mot subject va chi train 1 epoch voi random weights.

Sau khi co du s01-s04, train nghiem tuc hon:

    .\.venv\Scripts\python.exe -m ml.train_cnn --metadata data\metadata.csv --epochs 10 --batch-size 16 --output-model models\gesture-cnn-baseline.keras --metrics-out reports\cnn_baseline_metrics.json

Khi co tu 3 subject tro len va khong dung --smoke, script se uu tien split theo subject.

### Muc toi thieu

- Macro F1 tren nguoi chua xuat hien trong train >= 0.85.
- p95 end-to-end latency <= 500 ms.
- False activation tren no_gesture < 2%.
- Xe tu dung trong 600 ms khi mat lenh hop le.

### Muc muc tieu

- Macro F1 tren nguoi chua xuat hien trong train >= 0.90.
- Median end-to-end latency <= 300 ms.
- Accuracy tren background phuc tap giam khong qua 10 diem phan tram.
- Bao cao rieng cold start Cloud Run.

### Du lieu can thu

Muc chuan cho demo cuoi:

- It nhat 4 nguoi.
- Moi nguoi toi thieu 15 clip/lop.
- 8 lop cu chi.
- Moi clip khoang 1.5 giay, 10 FPS.
- Co nen don gian, nen phuc tap va 2 dieu kien sang.
- Chia train/validation/test theo nguoi, khong chia ngau nhien theo frame.

Muc thu nho de kiem tra pipeline:

- 1 nguoi.
- 5-10 clip/lop.
- Muc tieu chi la dam bao tool thu du lieu, metadata va train script chay duoc.

Thu du lieu thu nho voi webcam:

    .\.venv\Scripts\python.exe -m ml.collect_data --subject s01 --clips-per-label 5 --background simple --lighting bright

Cach dung cua tool:

- Cua so camera hien label va clip hien tai.
- Nhan SPACE de bat dau quay tung clip.
- Tool dem nguoc 3 giay, sau do quay 1.5 giay o 10 FPS.
- Nhan q de thoat som.
- Anh da crop/resize duoc luu vao data/raw/<subject>/<label>/<clip_id>/.
- Metadata duoc ghi vao data/metadata.csv theo tung frame.

Neu chi muon thu mot nhan de test nhanh:

    .\.venv\Scripts\python.exe -m ml.collect_data --subject s01 --labels like --clips-per-label 2

## Cloud deployment

API cloud co the chay tren Cloud Run hoac Hugging Face Spaces.

### Hugging Face Spaces

Day la phuong an demo cloud mien phi uu tien hien tai vi Google Cloud yeu cau
prepayment cho billing account.

Tao token Hugging Face co quyen write tai:

    https://huggingface.co/settings/tokens

Dang nhap CLI:

    .\.venv\Scripts\huggingface-cli.exe login

Tao va upload Docker Space:

    .\scripts\deploy_huggingface_space.ps1 -Space <HF_USERNAME>/iot-ck-gesture-api -Create

Neu khong muon login CLI, truyen token truc tiep cho script:

    .\scripts\deploy_huggingface_space.ps1 -Space <HF_USERNAME>/iot-ck-gesture-api -Create -Token <HF_WRITE_TOKEN>

Trong Hugging Face Space, dat secret:

    GESTURE_API_KEY=<SPACE_API_KEY>

Sau khi Space build xong, gateway dung URL dang:

    https://<HF_USERNAME>-iot-ck-gesture-api.hf.space

Space hien tai cua du an:

    https://anroiy-iot-ck-gesture-api.hf.space

Chay gateway voi Hugging Face Space:

    $env:GESTURE_API_KEY="<SPACE_API_KEY>"
    $env:ESP32_COMMAND_TOKEN="<ESP32_TOKEN>"
    .\scripts\run_gateway_huggingface.ps1

Test camera/cloud ma khong gui lenh den ESP32:

    $env:GESTURE_API_KEY="<SPACE_API_KEY>"
    .\scripts\run_gateway_huggingface.ps1 -DryRun

### Cloud Run

Cloud Run van duoc giu nhu phuong an chinh khi billing Google Cloud da active:

    .\scripts\deploy_cloud_run.ps1 -ProjectId <PROJECT_ID> -Demo

Che do -Demo dat min-instances=1 de giam cold start khi bao cao/demo.

Khu vuc de xuat:

    asia-southeast1

Credential va API key khong commit len Git. Dung bien moi truong/secret cua
Cloud Run hoac Hugging Face Spaces.

## Lenh kiem tra nhanh

Chay test Python:

    .\.venv\Scripts\python.exe -m pytest -q

Ket qua gan nhat:

    17 passed

Kiem tra camera/MediaPipe:

    .\.venv\Scripts\python.exe -c "import cv2; from gateway.preprocess import MediaPipeCropper; cap=cv2.VideoCapture(0); print('camera_open=',cap.isOpened()); ok,frame=cap.read(); print('frame_ok=',ok,'shape=',None if not ok else frame.shape); c=MediaPipeCropper(); r=c.crop(frame) if ok else None; print('mediapipe=',r is not None,'hand=',None if r is None else r.found_hand,'crop=',None if r is None else r.image.shape); cap.release()"

## Bao mat

Khong commit cac file chua thong tin that:

    arduino/*/config.h
    firmware/include/config.h
    .env

Neu bi lo Wi-Fi password hoac token demo, doi token trong firmware va gateway script truoc khi demo cong khai.

## Tai lieu doi chieu

- So do tong the hien tai: [shapes at 26-06-10 21.57.01.png](./shapes%20at%2026-06-10%2021.57.01.png)
- Requirement de tai: [requirement.txt](./requirement.txt)
