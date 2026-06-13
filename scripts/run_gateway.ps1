param(
  [Parameter(Mandatory=$true)][string]$CloudUrl,
  [Parameter(Mandatory=$true)][string]$ApiKey,
  [string]$Esp32Host = "192.168.2.126",
  [string]$Esp32Token = "CHANGE_ME",
  [int]$Camera = 0,
  [string]$Log = "reports/gateway_latency.csv",
  [int]$MaxFrames = 0,
  [switch]$Headless,
  [switch]$DryRun
)

$wsUrl = "ws://" + $Esp32Host + ":81/"
$gatewayArgs = @(
  "-m", "gateway.main",
  "--cloud-url", $CloudUrl,
  "--api-key", $ApiKey,
  "--esp32-ws", $wsUrl,
  "--esp32-token", $Esp32Token,
  "--camera", $Camera,
  "--log", $Log
)
if ($MaxFrames -gt 0) { $gatewayArgs += @("--max-frames", $MaxFrames) }
if ($Headless) { $gatewayArgs += "--headless" }
if ($DryRun) { $gatewayArgs += "--dry-run" }
./.venv/Scripts/python.exe @gatewayArgs
