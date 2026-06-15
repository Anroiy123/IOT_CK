# Cong viec tiep theo - IOT_CK

Cap nhat theo trang thai ngay 15/06/2026:

- Dataset noi bo hien co 5 subject, 570 clip, 8.550 frame.
- CNN baseline da co metrics frame-level va dang la model chinh.
- CNN-LSTM da duoc train/eval toi thieu de phuc vu so sanh hoc thuat.
- Da co summary clip-level, robustness theo background va false activation:
  - `reports/cnn_comparison_summary.json`
- Test Python hien tai: `38 passed`.

## 1. Da hoan tat

- Pipeline webcam -> gateway -> cloud -> ESP32 da chay.
- Azure latency log va local fallback da co artifact.
- CNN baseline da co:
  - `models/gesture-cnn-baseline-s05-partial.keras`
  - `reports/cnn_baseline_s05_partial_metrics.json`
- CNN-LSTM comparison da co:
  - `models/gesture-cnn-lstm-comparison.keras`
  - `reports/cnn_lstm_metrics.json`
- Bao cao Word sinh tu script da chay duoc:
  - `reports/BaoCao_IOT_Nhom12.docx`

## 2. Ket luan hien tai

- Chon `CNN` lam model chinh.
- Giu `CNN-LSTM` lam doi chung hoc thuat.
- Ly do:
  - CNN clip-level macro F1 tot hon ro ret.
  - CNN-LSTM hien tai co false activation `no_gesture` rat cao.
  - Latency local giua hai model khong du tot de bien minh cho CNN-LSTM.

## 3. Viec con lai uu tien cao

- Chay lai demo phan cung neu co dieu kien:
  - do false activation live voi `no_gesture`
  - do latency nhieu phien tren Azure
  - xac minh stop/deadman voi xe that
- Neu muon cai thien hoc thuat:
  - bo sung them subject va background cho cac cu chi `one/two/like/dislike`
  - thu fine-tune sau cho CNN-LSTM hoac doi sequence model nhe hon
- Neu muon chot ban nop:
  - kiem lai file Word/PDF cuoi
  - doi chieu cac bang/so lieu voi `reports/cnn_comparison_summary.json`
  - cap nhat anh demo phan cung neu can

## 4. Lenh quan trong

Train CNN-LSTM:

    .\.venv\Scripts\python.exe -m ml.train_cnn_lstm --epochs 6 --batch-size 8 --output-model models\gesture-cnn-lstm-comparison.keras --metrics-out reports\cnn_lstm_metrics.json

Sinh summary so sanh:

    .\.venv\Scripts\python.exe -m ml.evaluate_models --cnn-model models\gesture-cnn-baseline-s05-partial.keras --cnn-lstm-model models\gesture-cnn-lstm-comparison.keras --output reports\cnn_comparison_summary.json

Build bao cao:

    .\.venv\Scripts\python.exe reports\build_iot_report.py

Chay test:

    .\.venv\Scripts\python.exe -m pytest -q
