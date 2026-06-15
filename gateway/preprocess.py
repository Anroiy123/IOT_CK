from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

import numpy as np


@dataclass(frozen=True)
class CropResult:
    image: np.ndarray
    found_hand: bool
    extended_fingers: int | None = None


_NON_THUMB_FINGER_JOINTS = (
    (5, 6, 8),
    (9, 10, 12),
    (13, 14, 16),
    (17, 18, 20),
)


def count_extended_fingers(landmarks: Any, min_pip_angle_deg: float = 140.0) -> int:
    """Count extended non-thumb fingers using orientation-independent joint angles."""
    count = 0
    for mcp_index, pip_index, tip_index in _NON_THUMB_FINGER_JOINTS:
        angle = _joint_angle_degrees(landmarks[mcp_index], landmarks[pip_index], landmarks[tip_index])
        if angle >= min_pip_angle_deg:
            count += 1
    return count


def disambiguate_one_two(gesture: str, extended_fingers: int | None) -> str:
    if gesture not in {"one", "two"} or extended_fingers not in {1, 2}:
        return gesture
    return "one" if extended_fingers == 1 else "two"


def _joint_angle_degrees(first: Any, vertex: Any, last: Any) -> float:
    first_vector = (first.x - vertex.x, first.y - vertex.y, first.z - vertex.z)
    last_vector = (last.x - vertex.x, last.y - vertex.y, last.z - vertex.z)
    first_length = math.sqrt(sum(component * component for component in first_vector))
    last_length = math.sqrt(sum(component * component for component in last_vector))
    if first_length == 0.0 or last_length == 0.0:
        return 0.0
    cosine = sum(a * b for a, b in zip(first_vector, last_vector)) / (first_length * last_length)
    return math.degrees(math.acos(max(-1.0, min(1.0, cosine))))


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
        extended_fingers = count_extended_fingers(landmarks)
        xs = [point.x for point in landmarks]
        ys = [point.y for point in landmarks]
        x1 = max(0, int((min(xs) - self.margin_ratio) * w))
        y1 = max(0, int((min(ys) - self.margin_ratio) * h))
        x2 = min(w, int((max(xs) + self.margin_ratio) * w))
        y2 = min(h, int((max(ys) + self.margin_ratio) * h))
        if x2 <= x1 or y2 <= y1:
            return CropResult(frame, False)
        return CropResult(frame[y1:y2, x1:x2], True, extended_fingers)
