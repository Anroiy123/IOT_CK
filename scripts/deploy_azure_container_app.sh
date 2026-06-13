#!/usr/bin/env bash
set -euo pipefail

RESOURCE_GROUP="${RESOURCE_GROUP:-rg-iot-ck-gesture}"
LOCATION="${LOCATION:-southeastasia}"
ENVIRONMENT="${ENVIRONMENT:-iot-ck-env}"
APP_NAME="${APP_NAME:-iot-ck-gesture-api}"
IMAGE="${IMAGE:-ghcr.io/anroiy123/iot-ck-gesture-api:azure}"
API_KEY="${GESTURE_API_KEY:?Set GESTURE_API_KEY before running this script}"

az account show --output table
az group create --name "$RESOURCE_GROUP" --location "$LOCATION" --output table

az provider register --namespace Microsoft.App --wait

if ! az containerapp env show --name "$ENVIRONMENT" --resource-group "$RESOURCE_GROUP" >/dev/null 2>&1; then
  az containerapp env create \
    --name "$ENVIRONMENT" \
    --resource-group "$RESOURCE_GROUP" \
    --location "$LOCATION" \
    --logs-destination none \
    --output table
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
