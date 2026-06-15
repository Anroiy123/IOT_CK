from __future__ import annotations

import argparse
import time

import numpy as np

def main() -> None:
    import tensorflow as tf

    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", required=True)
    parser.add_argument("--model-type", choices=("cnn", "cnn_lstm"), default="cnn")
    parser.add_argument("--image-size", type=int, default=160)
    parser.add_argument("--frames", type=int, default=8)
    parser.add_argument("--iterations", type=int, default=30)
    args = parser.parse_args()

    model = tf.keras.models.load_model(args.model_path)
    if args.model_type == "cnn_lstm":
        sample = np.zeros((1, args.frames, args.image_size, args.image_size, 3), dtype=np.float32)
    else:
        sample = np.zeros((1, args.image_size, args.image_size, 3), dtype=np.float32)

    durations = []
    for _ in range(args.iterations):
        start = time.perf_counter()
        model.predict(sample, batch_size=1, verbose=0)
        durations.append((time.perf_counter() - start) * 1000)
    durations.sort()
    median = durations[len(durations) // 2]
    p95 = durations[int(len(durations) * 0.95) - 1]
    print({"median_latency_ms": round(median, 2), "p95_latency_ms": round(p95, 2)})


if __name__ == "__main__":
    main()
