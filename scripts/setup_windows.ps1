param(
  [string]$ProjectId = "iot-ck-demo",
  [string]$Region = "asia-southeast1"
)

$ErrorActionPreference = "Stop"
Write-Host "Python 3.11:" (py -3.11 --version)
py -3.11 -m venv .venv
./.venv/Scripts/python.exe -m pip install --upgrade pip setuptools wheel
./.venv/Scripts/python.exe -m pip install -r requirements.txt
code --install-extension platformio.platformio-ide --force
./.venv/Scripts/python.exe -m pip install platformio==6.1.19

Write-Host "Google Cloud CLI may need an administrator-approved installer."
Write-Host "After gcloud auth login:"
Write-Host "gcloud config set project $ProjectId"
Write-Host "gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com storage.googleapis.com"
Write-Host "Region: $Region"
