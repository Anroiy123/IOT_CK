---
title: IOT CK Gesture API
emoji: "🖐️"
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: mit
app_port: 7860
---

# IOT_CK Gesture Cloud API

FastAPI service for the IOT_CK gesture-recognition demo.

Endpoints:

- `GET /health`
- `GET /v1/model`
- `POST /v1/predict`

`/v1/predict` expects `image_b64` or `images_b64` and returns the predicted
gesture, confidence, inference latency, model type, model version, session id,
and request id.

Set Space secret:

- `GESTURE_API_KEY`: API key required by the gateway in `X-API-Key`.
