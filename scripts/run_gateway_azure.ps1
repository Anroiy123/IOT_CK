param(
  [Parameter(Mandatory=$true)][string]$AzureUrl,
  [string]$ApiKey = $env:AZURE_GESTURE_API_KEY,
  [string]$Esp32Host = "192.168.2.126",
  [string]$Esp32Token = $env:ESP32_COMMAND_TOKEN,
  [int]$Camera = 0,
  [string]$Log = "reports/gateway_azure_latency.csv",
  [int]$MaxFrames = 0,
  [switch]$Headless,
  [switch]$DryRun,
  [switch]$SkipCloudWithoutHand
)

$envPath = Join-Path (Split-Path $PSScriptRoot -Parent) ".env"
if (Test-Path $envPath) {
  $localEnv = ConvertFrom-StringData (Get-Content -Raw $envPath)
  if (-not $ApiKey -and $localEnv.AZURE_GESTURE_API_KEY) { $ApiKey = $localEnv.AZURE_GESTURE_API_KEY }
  if (-not $ApiKey -and $localEnv.GESTURE_API_KEY) { $ApiKey = $localEnv.GESTURE_API_KEY }
  if (-not $Esp32Token -and $localEnv.ESP32_COMMAND_TOKEN) { $Esp32Token = $localEnv.ESP32_COMMAND_TOKEN }
}

if (-not $ApiKey) {
  throw "Thieu ApiKey. Dat AZURE_GESTURE_API_KEY/GESTURE_API_KEY hoac truyen -ApiKey."
}
if (-not $DryRun -and -not $Esp32Token) {
  throw "Thieu Esp32Token. Dat ESP32_COMMAND_TOKEN hoac truyen -Esp32Token."
}

$arguments = @{
  CloudUrl = $AzureUrl.TrimEnd("/")
  ApiKey = $ApiKey
  Esp32Host = $Esp32Host
  Esp32Token = $Esp32Token
  Camera = $Camera
  Log = $Log
  MaxFrames = $MaxFrames
}
if ($Headless) { $arguments.Headless = $true }
if ($DryRun) { $arguments.DryRun = $true }
if ($SkipCloudWithoutHand) { $arguments.SkipCloudWithoutHand = $true }

& (Join-Path $PSScriptRoot "run_gateway.ps1") @arguments
