import base64

import cv2
import numpy as np
import pytest
from fastapi.testclient import TestClient

from cloud.app import create_app
from cloud.inference import Prediction, preprocess_jpegs


class DummyPredictor:
    model_version = "dummy-v1"
    model_type = "cnn"

    def predict(self, images):
        assert images
        return Prediction(gesture="like", confidence=0.91, inference_ms=12.5)


def test_predict_requires_api_key():
    app = create_app(predictor=DummyPredictor(), api_key="secret")
    client = TestClient(app)

    response = client.post("/v1/predict", json={"image_b64": "abc"})

    assert response.status_code == 401


def test_predict_returns_request_session_and_model_metadata():
    app = create_app(predictor=DummyPredictor(), api_key="secret")
    client = TestClient(app)
    image_b64 = base64.b64encode(b"fake-jpeg").decode("ascii")

    response = client.post(
        "/v1/predict",
        headers={"X-API-Key": "secret"},
        json={"image_b64": image_b64, "session_id": "s1", "request_id": "r1"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "gesture": "like",
        "confidence": 0.91,
        "inference_ms": 12.5,
        "model_version": "dummy-v1",
        "model_type": "cnn",
        "session_id": "s1",
        "request_id": "r1",
    }


def test_preprocess_jpegs_returns_rgb_float_batch():
    image = np.zeros((12, 20, 3), dtype=np.uint8)
    image[:, :, 2] = 255
    ok, encoded = cv2.imencode(".jpg", image)
    assert ok

    batch = preprocess_jpegs([encoded.tobytes()], image_size=16)

    assert batch.shape == (1, 16, 16, 3)
    assert batch.dtype == np.float32
    assert batch[0, 0, 0, 0] > 240
    assert batch[0, 0, 0, 2] < 20


def test_preprocess_jpegs_rejects_invalid_image():
    with pytest.raises(ValueError, match="Invalid JPEG"):
        preprocess_jpegs([b"not-an-image"])
