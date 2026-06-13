from __future__ import annotations

import os
import uuid
from typing import Any

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

from cloud.inference import LocalPredictor, decode_images


class PredictRequest(BaseModel):
    image_b64: str | None = None
    images_b64: list[str] = Field(default_factory=list)
    session_id: str | None = None
    request_id: str | None = None


def create_app(predictor: Any | None = None, api_key: str | None = None) -> FastAPI:
    app = FastAPI(title="IOT_CK Gesture Cloud API", version="0.1.0")
    predictor = predictor or LocalPredictor(os.getenv("MODEL_PATH"), os.getenv("MODEL_TYPE", "cnn"), os.getenv("MODEL_VERSION", "local-dev"))
    api_key = api_key if api_key is not None else os.getenv("GESTURE_API_KEY", "")

    def require_key(x_api_key: str | None = Header(default=None, alias="X-API-Key")) -> None:
        if api_key and x_api_key != api_key:
            raise HTTPException(status_code=401, detail="invalid api key")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/v1/model")
    def model() -> dict[str, str]:
        return {"model_version": predictor.model_version, "model_type": predictor.model_type}

    @app.post("/v1/predict", dependencies=[Depends(require_key)])
    def predict(body: PredictRequest) -> dict[str, Any]:
        try:
            images = decode_images(body.image_b64, body.images_b64)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        if not images:
            raise HTTPException(status_code=422, detail="image_b64 or images_b64 is required")
        try:
            prediction = predictor.predict(images)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        return {
            "gesture": prediction.gesture,
            "confidence": prediction.confidence,
            "inference_ms": prediction.inference_ms,
            "model_version": predictor.model_version,
            "model_type": predictor.model_type,
            "session_id": body.session_id or str(uuid.uuid4()),
            "request_id": body.request_id or str(uuid.uuid4()),
        }

    return app


app = create_app()
