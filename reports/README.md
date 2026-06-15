# Reports

Final evidence must include:

- CNN baseline and CNN-LSTM confusion matrices
- macro F1 on unseen subjects
- robustness drop on complex backgrounds
- false activation rate for no_gesture
- local inference latency
- cloud inference latency
- end-to-end latency through ESP32 acknowledgement

Canonical outputs in the current repo:

- `cnn_baseline_s05_partial_metrics.json`: frame-level CNN baseline metrics
- `cnn_lstm_metrics.json`: CNN-LSTM training/evaluation metrics
- `cnn_comparison_summary.json`: clip-level comparison, robustness and false activation summary
- `gateway_azure_latency.csv`: online Azure latency log
