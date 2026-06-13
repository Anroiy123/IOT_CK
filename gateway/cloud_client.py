from __future__ import annotations

import base64
import time
from dataclasses import dataclass
from typing import Iterable

import requests


@dataclass(frozen=True)
class CloudPrediction:
    gesture: str
    confidence: float
    inference_ms: float
    model_version: str
    model_type: str
    session_id: str
    request_id: str
    rtt_ms: float


class CloudGestureClient:
    def __init__(
        self,
        base_url: str,
        api_key: str,
        timeout_s: float = 1.5,
        session: requests.Session | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout_s = timeout_s
        self.session = session or requests.Session()
        self.session.headers.update({"X-API-Key": self.api_key})

    def predict(self, jpeg_images: Iterable[bytes], *, session_id: str, request_id: str) -> CloudPrediction:
        encoded = [base64.b64encode(image).decode("ascii") for image in jpeg_images]
        payload = {"images_b64": encoded, "session_id": session_id, "request_id": request_id}
        start = time.perf_counter()
        response = self.session.post(
            f"{self.base_url}/v1/predict",
            json=payload,
            timeout=self.timeout_s,
        )
        rtt_ms = (time.perf_counter() - start) * 1000
        response.raise_for_status()
        data = response.json()
        return CloudPrediction(
            gesture=data["gesture"],
            confidence=float(data["confidence"]),
            inference_ms=float(data["inference_ms"]),
            model_version=data["model_version"],
            model_type=data["model_type"],
            session_id=data["session_id"],
            request_id=data["request_id"],
            rtt_ms=rtt_ms,
        )

    def close(self) -> None:
        self.session.close()
