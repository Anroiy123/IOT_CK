from __future__ import annotations

import base64
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np

from common.protocol import GESTURES


@dataclass(frozen=True)
class Prediction:
    gesture: str
    confidence: float
    inference_ms: float


class LocalPredictor:
    def __init__(
        self,
        model_path: str | None = None,
        model_type: str = "cnn",
        model_version: str = "local-dev",
        image_size: int = 160,
    ) -> None:
        self.model_path = model_path
        self.model_type = model_type
        self.model_version = model_version
        self.image_size = image_size
        self.labels = GESTURES
        self._model = None
        if model_path:
            import tensorflow as tf

            path = Path(model_path)
            if not path.exists():
                raise FileNotFoundError(f"Model file not found: {path}")
            self._model = tf.keras.models.load_model(path)
            output_classes = int(self._model.output_shape[-1])
            if output_classes != len(self.labels):
                raise ValueError(f"Model has {output_classes} output classes, expected {len(self.labels)}")

    def predict(self, images: Iterable[bytes]) -> Prediction:
        start = time.perf_counter()
        if self._model is None:
            return Prediction("no_gesture", 0.0, (time.perf_counter() - start) * 1000)
        batch = preprocess_jpegs(images, image_size=self.image_size)
        probabilities = np.asarray(self._model.predict(batch, verbose=0), dtype="float32")
        mean_probabilities = probabilities.mean(axis=0)
        class_id = int(mean_probabilities.argmax())
        return Prediction(
            gesture=self.labels[class_id],
            confidence=float(mean_probabilities[class_id]),
            inference_ms=(time.perf_counter() - start) * 1000,
        )


def preprocess_jpegs(images: Iterable[bytes], *, image_size: int = 160) -> np.ndarray:
    import cv2

    processed: list[np.ndarray] = []
    for image_bytes in images:
        encoded = np.frombuffer(image_bytes, dtype=np.uint8)
        image = cv2.imdecode(encoded, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("Invalid JPEG image")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (image_size, image_size), interpolation=cv2.INTER_AREA)
        processed.append(image.astype("float32"))
    if not processed:
        raise ValueError("At least one JPEG image is required")
    return np.stack(processed, axis=0)


def decode_images(image_b64: str | None = None, images_b64: list[str] | None = None) -> list[bytes]:
    values = images_b64 if images_b64 else ([image_b64] if image_b64 else [])
    try:
        return [base64.b64decode(value, validate=True) for value in values]
    except (ValueError, base64.binascii.Error) as exc:
        raise ValueError("Invalid base64 image") from exc
