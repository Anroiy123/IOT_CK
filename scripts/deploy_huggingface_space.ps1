param(
  [Parameter(Mandatory=$true)][string]$Space,
  [string]$ModelPath = "models/gesture-cnn-baseline-s05-partial.keras",
  [string]$ModelVersion = "cnn-s05-partial-v1",
  [string]$StageDir = ".hf_space_build",
  [string]$Token = "",
  [switch]$PrepareOnly,
  [switch]$Create
)

if (-not (Test-Path $ModelPath)) {
  throw "Khong tim thay model: $ModelPath"
}

$hfCommand = $null
$hf = Get-Command hf -ErrorAction SilentlyContinue
if ($hf) {
  $hfCommand = $hf.Source
}
if (-not $hfCommand) {
  $hf = Get-Command huggingface-cli -ErrorAction SilentlyContinue
  if ($hf) { $hfCommand = $hf.Source }
}
if (-not $hfCommand) {
  $venvHf = Join-Path (Get-Location) ".venv\Scripts\hf.exe"
  $venvHuggingFaceCli = Join-Path (Get-Location) ".venv\Scripts\huggingface-cli.exe"
  if (Test-Path $venvHf) {
    $hfCommand = $venvHf
  } elseif (Test-Path $venvHuggingFaceCli) {
    $hfCommand = $venvHuggingFaceCli
  }
}
if (-not $hfCommand) {
  throw "Khong tim thay hf CLI. Cai bang: python -m pip install -U huggingface_hub"
}
$env:PYTHONIOENCODING = "utf-8"

$stagePath = Join-Path (Get-Location) $StageDir
if (Test-Path $stagePath) {
  Remove-Item -LiteralPath $stagePath -Recurse -Force
}
New-Item -ItemType Directory -Path $stagePath | Out-Null
New-Item -ItemType Directory -Path (Join-Path $stagePath "models") | Out-Null

Copy-Item -Recurse -Force "cloud" (Join-Path $stagePath "cloud")
Copy-Item -Recurse -Force "common" (Join-Path $stagePath "common")
Copy-Item -Force $ModelPath (Join-Path $stagePath "models\gesture-cnn-baseline-s05-partial.keras")
Copy-Item -Force "deploy\huggingface\Dockerfile" (Join-Path $stagePath "Dockerfile")
Copy-Item -Force "deploy\huggingface\README.md" (Join-Path $stagePath "README.md")
Copy-Item -Force "deploy\huggingface\requirements.txt" (Join-Path $stagePath "requirements.txt")
Get-ChildItem -Path $stagePath -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
Get-ChildItem -Path $stagePath -Recurse -File -Include "*.pyc" | Remove-Item -Force

$envFile = Join-Path $stagePath ".env.example"
@"
MODEL_PATH=models/gesture-cnn-baseline-s05-partial.keras
MODEL_TYPE=cnn
MODEL_VERSION=$ModelVersion
GESTURE_API_KEY=CHANGE_ME
"@ | Set-Content -Encoding UTF8 $envFile

if ($PrepareOnly) {
  Write-Output "Da tao staging folder: $stagePath"
  Get-ChildItem -Recurse $stagePath | Select-Object FullName, Length
  exit 0
}

if ($Create) {
  $createArgs = @("repo", "create", $Space, "--repo-type", "space", "--space_sdk", "docker", "--exist-ok")
  if ($Token) { $createArgs += @("--token", $Token) }
  & $hfCommand @createArgs
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

$uploadArgs = @("upload", $Space, $stagePath, ".", "--repo-type", "space", "--commit-message", "Deploy IOT_CK gesture API")
if ($Token) { $uploadArgs += @("--token", $Token) }
& $hfCommand @uploadArgs
exit $LASTEXITCODE
