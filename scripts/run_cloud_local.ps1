param(
  [string]$ModelPath = "models\gesture-cnn-baseline-s05-partial.keras",
  [string]$ModelVersion = "cnn-s05-partial-v1",
  [string]$ApiKey = "local-dev",
  [int]$Port = 8001
)

if (-not (Test-Path $ModelPath)) {
  throw "Khong tim thay model: $ModelPath"
}

$env:MODEL_PATH = $ModelPath
$env:MODEL_TYPE = "cnn"
$env:MODEL_VERSION = $ModelVersion
$env:GESTURE_API_KEY = $ApiKey

.\.venv\Scripts\python.exe -m uvicorn cloud.app:app --host 127.0.0.1 --port $Port
