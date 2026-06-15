from __future__ import annotations

from dataclasses import dataclass


DEFAULT_ACCEPTANCE_CRITERIA = {
    "minimum": {
        "macro_f1": 0.85,
        "p95_latency_ms": 500,
        "false_activation_no_gesture": 0.02,
    },
    "target": {
        "macro_f1": 0.90,
        "median_latency_ms": 300,
        "robustness_drop_max": 0.10,
    },
}


@dataclass(frozen=True)
class ModelMetrics:
    name: str
    macro_f1: float
    p95_latency_ms: float
    median_latency_ms: float


@dataclass(frozen=True)
class ModelDecision:
    selected: str
    reason: str


def required_experiments() -> list[dict[str, object]]:
    return [
        {"name": "cnn", "required": True, "role": "baseline"},
        {"name": "cnn_lstm", "required": True, "role": "comparison"},
    ]


def choose_model(cnn: ModelMetrics, cnn_lstm: ModelMetrics) -> ModelDecision:
    f1_gain = cnn_lstm.macro_f1 - cnn.macro_f1
    cnn_latency_advantage = cnn_lstm.p95_latency_ms > 0 and cnn.p95_latency_ms <= cnn_lstm.p95_latency_ms * 0.8
    if f1_gain <= 0.02 and cnn_latency_advantage:
        return ModelDecision("cnn", "cnn accuracy close to cnn_lstm and latency at least 20 percent better")
    if f1_gain >= 0.02 and cnn_lstm.p95_latency_ms <= DEFAULT_ACCEPTANCE_CRITERIA["minimum"]["p95_latency_ms"]:
        return ModelDecision("cnn_lstm", "cnn_lstm improves macro_f1 by at least 2 points within p95 latency budget")
    return ModelDecision("cnn", "cnn remains mandatory baseline and safer default")
