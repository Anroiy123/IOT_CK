#!/usr/bin/env bash
set -euo pipefail

RESOURCE_GROUP="${RESOURCE_GROUP:-rg-iot-ck-gesture}"
LOCATION="${LOCATION:-southeastasia}"
ENVIRONMENT="${ENVIRONMENT:-iot-ck-env}"
APP_NAME="${APP_NAME:-iot-ck-gesture-api}"
IMAGE="${IMAGE:-ghcr.io/anroiy123/iot-ck-gesture-api:azure}"
API_KEY="${GESTURE_API_KEY:?Set GESTURE_API_KEY before running this script}"

create_environment_with_fallback() {
  local locations=(
    "$LOCATION"
    westus2
    westus3
    westus
    westcentralus
    centralus
    northcentralus
    southcentralus
    eastus2
    eastus
    canadacentral
    canadaeast
    westeurope
    northeurope
    uksouth
    ukwest
    swedencentral
    francecentral
    germanywestcentral
    japaneast
    australiaeast
    koreacentral
  )
  local tried=()
  local location
  for location in "${locations[@]}"; do
    if [[ " ${tried[*]} " == *" $location "* ]]; then
      continue
    fi
    tried+=("$location")
    echo "Trying Container Apps environment location: $location"
    if az containerapp env create \
      --name "$ENVIRONMENT" \
      --resource-group "$RESOURCE_GROUP" \
      --location "$location" \
      --logs-destination none \
      --output table; then
      LOCATION="$location"
      export LOCATION
      echo "Selected Container Apps location: $LOCATION"
      return 0
    fi
    echo "Location $location failed; trying next candidate..." >&2
  done
  echo "Could not create Container Apps environment in any candidate location." >&2
  echo "Run this command to inspect allowed policy locations:" >&2
  echo "az policy assignment list --scope /subscriptions/\$(az account show --query id -o tsv) -o jsonc" >&2
  return 1
}

az account show --output table
if az group show --name "$RESOURCE_GROUP" >/dev/null 2>&1; then
  az group show --name "$RESOURCE_GROUP" --query "{name:name, location:location}" --output table
else
  az group create --name "$RESOURCE_GROUP" --location "$LOCATION" --output table
fi

az provider register --namespace Microsoft.App --wait

if ! az containerapp env show --name "$ENVIRONMENT" --resource-group "$RESOURCE_GROUP" >/dev/null 2>&1; then
  create_environment_with_fallback
else
  LOCATION="$(az containerapp env show --name "$ENVIRONMENT" --resource-group "$RESOURCE_GROUP" --query location -o tsv)"
  export LOCATION
  echo "Using existing Container Apps environment in: $LOCATION"
fi

if az containerapp show --name "$APP_NAME" --resource-group "$RESOURCE_GROUP" >/dev/null 2>&1; then
  az containerapp update \
    --name "$APP_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --image "$IMAGE" \
    --set-env-vars \
      MODEL_PATH=models/gesture-cnn-baseline-s05-partial.keras \
      MODEL_TYPE=cnn \
      MODEL_VERSION=cnn-s05-partial-v1 \
      GESTURE_API_KEY="$API_KEY" \
    --cpu 1.0 \
    --memory 2.0Gi \
    --min-replicas 0 \
    --max-replicas 1 \
    --output table
else
  az containerapp create \
    --name "$APP_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --environment "$ENVIRONMENT" \
    --image "$IMAGE" \
    --target-port 7860 \
    --ingress external \
    --transport auto \
    --env-vars \
      MODEL_PATH=models/gesture-cnn-baseline-s05-partial.keras \
      MODEL_TYPE=cnn \
      MODEL_VERSION=cnn-s05-partial-v1 \
      GESTURE_API_KEY="$API_KEY" \
    --cpu 1.0 \
    --memory 2.0Gi \
    --min-replicas 0 \
    --max-replicas 1 \
    --output table
fi

FQDN="$(az containerapp show --name "$APP_NAME" --resource-group "$RESOURCE_GROUP" --query properties.configuration.ingress.fqdn -o tsv)"
echo "https://$FQDN"
