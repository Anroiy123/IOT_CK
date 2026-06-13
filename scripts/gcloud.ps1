param(
  [Parameter(ValueFromRemainingArguments = $true)]
  [string[]]$GcloudArgs
)

$sdkRoot = Join-Path $env:LOCALAPPDATA "Google\Cloud SDK\google-cloud-sdk"
$python = Join-Path $sdkRoot "platform\bundledpython\python.exe"
$entrypoint = Join-Path $sdkRoot "lib\gcloud.py"

if (-not (Test-Path $python) -or -not (Test-Path $entrypoint)) {
  throw "Khong tim thay Google Cloud SDK trong $sdkRoot"
}

& $python $entrypoint @GcloudArgs
exit $LASTEXITCODE
