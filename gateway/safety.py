from __future__ import annotations

from dataclasses import dataclass, fields


@dataclass(frozen=True)
class SafetyPolicy:
    normal_required: int = 3
    mode_required: int = 2
    stop_required: int = 2
    min_confidence: float = 0.80
    mode_min_confidence: float = 0.60
    no_command_timeout_ms: int = 600
    servo_cooldown_ms: int = 250


class GestureStabilizer:
    def __init__(self, policy: SafetyPolicy) -> None:
        self.policy = policy
        self._last_gesture: str | None = None
        self._count = 0

    def accept(self, gesture: str, confidence: float) -> str | None:
        gesture = (gesture or "").strip().lower()
        if gesture in {"", "no_gesture", "none"} or confidence < self._min_confidence_for(gesture):
            self._last_gesture = None
            self._count = 0
            return None

        if gesture == self._last_gesture:
            self._count += 1
        else:
            self._last_gesture = gesture
            self._count = 1

        required = self._required_count_for(gesture)
        return gesture if self._count >= required else None

    def _min_confidence_for(self, gesture: str) -> float:
        if gesture in {"peace", "rock"}:
            return self.policy.mode_min_confidence
        return self.policy.min_confidence

    def _required_count_for(self, gesture: str) -> int:
        if gesture == "stop":
            return self.policy.stop_required
        if gesture in {"peace", "rock"}:
            return self.policy.mode_required
        return self.policy.normal_required


@dataclass(frozen=True)
class LatencyLogRow:
    session_id: str
    request_id: str
    gesture: str
    confidence: float
    mode: str
    command: str
    capture_ms: float
    preprocess_ms: float
    cloud_rtt_ms: float
    inference_ms: float
    esp32_ack_ms: float
    total_ms: float

    @classmethod
    def header(cls) -> list[str]:
        return [field.name for field in fields(cls)]

    def to_csv_row(self) -> dict[str, str]:
        result: dict[str, str] = {}
        for field in fields(self):
            value = getattr(self, field.name)
            result[field.name] = f"{value:.2f}" if isinstance(value, float) else str(value)
        return result
