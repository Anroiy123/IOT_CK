param(
  [string]$ApiKey = $env:GESTURE_API_KEY,
  [string]$Esp32Host = "192.168.2.126",
  [string]$Esp32Token = $env:ESP32_COMMAND_TOKEN,
  [int]$Camera = 0,
  [string]$Log = "reports/gateway_huggingface_latency.csv",
  [int]$MaxFrames = 0,
  [switch]$Headless,
  [switch]$DryRun
)

$envPath = Join-Path (Split-Path $PSScriptRoot -Parent) ".env"
if (Test-Path $envPath) {
  $localEnv = ConvertFrom-StringData (Get-Content -Raw $envPath)
  if (-not $ApiKey) { $ApiKey = $localEnv.GESTURE_API_KEY }
  if (-not $Esp32Token) { $Esp32Token = $localEnv.ESP32_COMMAND_TOKEN }
}

if (-not $ApiKey) {
  throw "Thieu ApiKey. Dat GESTURE_API_KEY hoac truyen -ApiKey."
}
if (-not $DryRun -and -not $Esp32Token) {
  throw "Thieu Esp32Token. Dat ESP32_COMMAND_TOKEN hoac truyen -Esp32Token."
}

$arguments = @{
  CloudUrl = "https://anroiy-iot-ck-gesture-api.hf.space"
  ApiKey = $ApiKey
  Esp32Host = $Esp32Host
  Esp32Token = $Esp32Token
  Camera = $Camera
  Log = $Log
  MaxFrames = $MaxFrames
}
if ($Headless) { $arguments.Headless = $true }
if ($DryRun) { $arguments.DryRun = $true }

& (Join-Path $PSScriptRoot "run_gateway.ps1") @arguments
