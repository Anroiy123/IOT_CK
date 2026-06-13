param(
  [Parameter(Mandatory=$true)][string]$ProjectId,
  [string]$Service = "gesture-api",
  [string]$Region = "asia-southeast1",
  [string]$ModelPath = "models/gesture-cnn-baseline-s05-partial.keras",
  [string]$ModelVersion = "cnn-s05-partial-v1",
  [string]$ApiKeySecret = "gesture-api-key",
  [switch]$Demo
)

if (-not (Test-Path $ModelPath)) {
  throw "Khong tim thay model: $ModelPath"
}

$nativeGcloud = Get-Command gcloud -ErrorAction SilentlyContinue
$gcloudCommand = if ($nativeGcloud) { $nativeGcloud.Source } else { Join-Path $PSScriptRoot "gcloud.ps1" }
if (-not (Test-Path $gcloudCommand)) {
  throw "Khong tim thay gcloud hoac scripts\\gcloud.ps1"
}

$deployArgs = @(
  "run", "deploy", $Service,
  "--project=$ProjectId",
  "--region=$Region",
  "--source=.",
  "--allow-unauthenticated",
  "--set-env-vars=MODEL_PATH=$ModelPath,MODEL_TYPE=cnn,MODEL_VERSION=$ModelVersion",
  "--set-secrets=GESTURE_API_KEY=$($ApiKeySecret):latest",
  "--memory=2Gi",
  "--cpu=2"
)
if ($Demo) { $deployArgs += "--min-instances=1" }
& $gcloudCommand @deployArgs
