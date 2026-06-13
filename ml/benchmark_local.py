from __future__ import annotations

import argparse
import time

import cv2
import numpy as np

from cloud.inference import LocalPredictor


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path")
    parser.add_argument("--iterations", type=int, default=30)
    args = parser.parse_args()
    predictor = LocalPredictor(args.model_path, model_version="local-benchmark")
    image = np.zeros((160, 160, 3), dtype=np.uint8)
    ok, encoded = cv2.imencode(".jpg", image)
    if not ok:
        raise RuntimeError("Could not create benchmark JPEG")
    jpeg = encoded.tobytes()
    durations = []
    for _ in range(args.iterations):
        start = time.perf_counter()
        predictor.predict([jpeg])
        durations.append((time.perf_counter() - start) * 1000)
    durations.sort()
    median = durations[len(durations) // 2]
    p95 = durations[int(len(durations) * 0.95) - 1]
    print({"median_latency_ms": round(median, 2), "p95_latency_ms": round(p95, 2)})


if __name__ == "__main__":
    main()
