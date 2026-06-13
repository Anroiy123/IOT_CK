from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np


@dataclass(frozen=True)
class CropResult:
    image: np.ndarray
    found_hand: bool


class MediaPipeCropper:
    def __init__(self, margin_ratio: float = 0.20) -> None:
        self.margin_ratio = margin_ratio
        self._hands: Any | None = None
        try:
            import mediapipe as mp

            self._mp = mp
            self._hands = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=1)
        except Exception:
            self._mp = None

    def crop(self, frame: np.ndarray) -> CropResult:
        if self._hands is None:
            return CropResult(frame, False)
        rgb = frame[:, :, ::-1]
        result = self._hands.process(rgb)
        if not result.multi_hand_landmarks:
            return CropResult(frame, False)
        h, w = frame.shape[:2]
        landmarks = result.multi_hand_landmarks[0].landmark
        xs = [point.x for point in landmarks]
        ys = [point.y for point in landmarks]
        x1 = max(0, int((min(xs) - self.margin_ratio) * w))
        y1 = max(0, int((min(ys) - self.margin_ratio) * h))
        x2 = min(w, int((max(xs) + self.margin_ratio) * w))
        y2 = min(h, int((max(ys) + self.margin_ratio) * h))
        if x2 <= x1 or y2 <= y1:
            return CropResult(frame, False)
        return CropResult(frame[y1:y2, x1:x2], True)
