from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

import numpy as np
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score

from common.protocol import GESTURES
from ml.model_policy import ModelMetrics, choose_model
from ml.sequence_utils import ClipSample, build_clip_samples, load_sequence_images
from ml.train_cnn import label_mapping, load_images, load_metadata, make_split


def _evaluate_classification(
    y_true: np.ndarray,
    probabilities: np.ndarray,
    *,
    labels: list[int],
    id_to_label: dict[int, str],
) -> dict[str, Any]:
    y_pred = probabilities.argmax(axis=1)
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "macro_f1": float(f1_score(y_true, y_pred, labels=labels, average="macro", zero_division=0)),
        "classification_report": classification_report(
            y_true,
            y_pred,
            labels=labels,
            target_names=[id_to_label[index] for index in labels],
            output_dict=True,
            zero_division=0,
        ),
        "confusion_matrix": confusion_matrix(y_true, y_pred, labels=labels).tolist(),
        "y_true": y_true.tolist(),
        "y_pred": y_pred.tolist(),
    }


def aggregate_frame_probabilities_to_clips(
    rows: list[dict[str, str]],
    probabilities: np.ndarray,
    *,
    label_to_id: dict[str, int],
) -> tuple[list[dict[str, Any]], np.ndarray, np.ndarray]:
    grouped: dict[tuple[str, str, str], dict[str, Any]] = {}
    for row, frame_probabilities in zip(rows, probabilities):
        key = (row["subject_id"], row["gesture"], row["clip_id"])
        clip = grouped.setdefault(
            key,
            {
                "subject_id": row["subject_id"],
                "gesture": row["gesture"],
                "clip_id": row["clip_id"],
                "background": row.get("background", "unknown"),
                "lighting": row.get("lighting", "unknown"),
                "frame_count": 0,
                "probabilities": [],
            },
        )
        clip["frame_count"] += 1
        clip["probabilities"].append(np.asarray(frame_probabilities, dtype="float32"))

    clip_predictions: list[dict[str, Any]] = []
    y_true: list[int] = []
    probs: list[np.ndarray] = []
    for clip in grouped.values():
        mean_probabilities = np.mean(np.stack(clip["probabilities"], axis=0), axis=0)
        class_id = int(mean_probabilities.argmax())
        clip_predictions.append(
            {
                "subject_id": clip["subject_id"],
                "gesture": clip["gesture"],
                "predicted_gesture": GESTURES[class_id],
                "clip_id": clip["clip_id"],
                "background": clip["background"],
                "lighting": clip["lighting"],
                "frame_count": clip["frame_count"],
                "confidence": float(mean_probabilities[class_id]),
                "probabilities": {label: float(mean_probabilities[index]) for label, index in label_to_id.items()},
            }
        )
        y_true.append(label_to_id[clip["gesture"]])
        probs.append(mean_probabilities)
    return clip_predictions, np.asarray(y_true, dtype="int64"), np.stack(probs, axis=0)


def summarize_robustness(predictions: list[dict[str, Any]], *, label_to_id: dict[str, int]) -> dict[str, Any]:
    results: dict[str, dict[str, Any]] = {}
    for background in ("simple", "complex"):
        background_predictions = [item for item in predictions if item["background"] == background]
        if not background_predictions:
            results[background] = {"count": 0, "accuracy": 0.0, "macro_f1": 0.0}
            continue
        y_true = np.asarray([label_to_id[item["gesture"]] for item in background_predictions], dtype="int64")
        y_pred = np.asarray([label_to_id[item["predicted_gesture"]] for item in background_predictions], dtype="int64")
        results[background] = {
            "count": len(background_predictions),
            "accuracy": float(accuracy_score(y_true, y_pred)),
            "macro_f1": float(f1_score(y_true, y_pred, average="macro", zero_division=0)),
        }
    results["accuracy_drop"] = float(results["simple"]["accuracy"] - results["complex"]["accuracy"])
    results["macro_f1_drop"] = float(results["simple"]["macro_f1"] - results["complex"]["macro_f1"])
    return results


def summarize_false_activation(predictions: list[dict[str, Any]]) -> dict[str, Any]:
    negatives = [item for item in predictions if item["gesture"] == "no_gesture"]
    false_positives = [item for item in negatives if item["predicted_gesture"] != "no_gesture"]
    count = len(negatives)
    rate = len(false_positives) / count if count else 0.0
    return {
        "count": count,
        "false_positive_count": len(false_positives),
        "rate": float(rate),
    }


def benchmark_predictions(model, sample_batch: np.ndarray, *, iterations: int, batch_size: int) -> dict[str, Any]:
    durations: list[float] = []
    for _ in range(iterations):
        start = time.perf_counter()
        model.predict(sample_batch, batch_size=batch_size, verbose=0)
        durations.append((time.perf_counter() - start) * 1000)
    durations.sort()
    return {
        "iterations": iterations,
        "median": round(durations[len(durations) // 2], 2),
        "p95": round(durations[max(0, int(len(durations) * 0.95) - 1)], 2),
    }


def evaluate_cnn(
    model_path: Path,
    test_rows: list[dict[str, str]],
    robustness_rows: list[dict[str, str]],
    *,
    label_to_id: dict[str, int],
    image_size: int,
    batch_size: int,
    benchmark_iterations: int,
) -> dict[str, Any]:
    import tensorflow as tf

    labels = list(range(len(GESTURES)))
    id_to_label = {index: label for label, index in label_to_id.items()}
    model = tf.keras.models.load_model(model_path)
    x_test, _ = load_images(test_rows, label_to_id, image_size=image_size)
    probabilities = np.asarray(model.predict(x_test, batch_size=batch_size, verbose=0), dtype="float32")
    clip_predictions, y_true, clip_probabilities = aggregate_frame_probabilities_to_clips(
        test_rows,
        probabilities,
        label_to_id=label_to_id,
    )
    robustness_x, _ = load_images(robustness_rows, label_to_id, image_size=image_size)
    robustness_probabilities = np.asarray(model.predict(robustness_x, batch_size=batch_size, verbose=0), dtype="float32")
    robustness_predictions, _, _ = aggregate_frame_probabilities_to_clips(
        robustness_rows,
        robustness_probabilities,
        label_to_id=label_to_id,
    )
    metrics = _evaluate_classification(y_true, clip_probabilities, labels=labels, id_to_label=id_to_label)
    return {
        "model_path": str(model_path),
        "model_type": "cnn",
        "evaluation_unit": "clip_mean_probability",
        "counts": {
            "test_frames": len(test_rows),
            "test_clips": len(clip_predictions),
        },
        **{key: metrics[key] for key in ("accuracy", "macro_f1", "classification_report", "confusion_matrix")},
        "robustness_scope": "all_clips",
        "robustness": summarize_robustness(robustness_predictions, label_to_id=label_to_id),
        "false_activation_no_gesture": summarize_false_activation(robustness_predictions),
        "local_latency_ms": benchmark_predictions(model, x_test[:1], iterations=benchmark_iterations, batch_size=1),
        "test_predictions": clip_predictions,
    }


def evaluate_cnn_lstm(
    model_path: Path,
    test_clips: list[ClipSample],
    robustness_clips: list[ClipSample],
    *,
    label_to_id: dict[str, int],
    image_size: int,
    batch_size: int,
    benchmark_iterations: int,
) -> dict[str, Any]:
    import tensorflow as tf

    labels = list(range(len(GESTURES)))
    id_to_label = {index: label for label, index in label_to_id.items()}
    model = tf.keras.models.load_model(model_path)
    x_test, y_true = load_sequence_images(test_clips, label_to_id, image_size=image_size)
    probabilities = np.asarray(model.predict(x_test, batch_size=batch_size, verbose=0), dtype="float32")
    metrics = _evaluate_classification(y_true, probabilities, labels=labels, id_to_label=id_to_label)

    y_pred = probabilities.argmax(axis=1)
    predictions = [
        {
            "subject_id": clip.subject_id,
            "gesture": clip.gesture,
            "predicted_gesture": id_to_label[int(pred_id)],
            "clip_id": clip.clip_id,
            "background": clip.background,
            "lighting": clip.lighting,
            "frame_count": len(clip.files),
            "confidence": float(probabilities[index][int(pred_id)]),
            "probabilities": {id_to_label[i]: float(probabilities[index][i]) for i in labels},
        }
        for index, (clip, pred_id) in enumerate(zip(test_clips, y_pred))
    ]
    robustness_x, _ = load_sequence_images(robustness_clips, label_to_id, image_size=image_size)
    robustness_probabilities = np.asarray(model.predict(robustness_x, batch_size=batch_size, verbose=0), dtype="float32")
    robustness_pred_ids = robustness_probabilities.argmax(axis=1)
    robustness_predictions = [
        {
            "subject_id": clip.subject_id,
            "gesture": clip.gesture,
            "predicted_gesture": id_to_label[int(pred_id)],
            "clip_id": clip.clip_id,
            "background": clip.background,
            "lighting": clip.lighting,
            "frame_count": len(clip.files),
            "confidence": float(robustness_probabilities[index][int(pred_id)]),
            "probabilities": {id_to_label[i]: float(robustness_probabilities[index][i]) for i in labels},
        }
        for index, (clip, pred_id) in enumerate(zip(robustness_clips, robustness_pred_ids))
    ]
    return {
        "model_path": str(model_path),
        "model_type": "cnn_lstm",
        "evaluation_unit": "clip_sequence",
        "counts": {
            "test_sequences": len(x_test),
            "test_clips": len(predictions),
        },
        **{key: metrics[key] for key in ("accuracy", "macro_f1", "classification_report", "confusion_matrix")},
        "robustness_scope": "all_clips",
        "robustness": summarize_robustness(robustness_predictions, label_to_id=label_to_id),
        "false_activation_no_gesture": summarize_false_activation(robustness_predictions),
        "local_latency_ms": benchmark_predictions(model, x_test[:1], iterations=benchmark_iterations, batch_size=1),
        "test_predictions": predictions,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata", type=Path, default=Path("data/metadata.csv"))
    parser.add_argument("--cnn-model", type=Path, default=Path("models/gesture-cnn-baseline-s05-partial.keras"))
    parser.add_argument("--cnn-lstm-model", type=Path, default=Path("models/gesture-cnn-lstm-comparison.keras"))
    parser.add_argument("--output", type=Path, default=Path("reports/cnn_comparison_summary.json"))
    parser.add_argument("--image-size", type=int, default=160)
    parser.add_argument("--frames", type=int, default=8)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--benchmark-iterations", type=int, default=30)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = load_metadata(args.metadata)
    split = make_split(rows, seed=args.seed, smoke=False)
    label_to_id = label_mapping()

    cnn = evaluate_cnn(
        args.cnn_model,
        split.test,
        rows,
        label_to_id=label_to_id,
        image_size=args.image_size,
        batch_size=args.batch_size,
        benchmark_iterations=args.benchmark_iterations,
    )
    test_clips = build_clip_samples(split.test, frames=args.frames)
    robustness_clips = build_clip_samples(rows, frames=args.frames)
    cnn_lstm = evaluate_cnn_lstm(
        args.cnn_lstm_model,
        test_clips,
        robustness_clips,
        label_to_id=label_to_id,
        image_size=args.image_size,
        batch_size=args.batch_size,
        benchmark_iterations=args.benchmark_iterations,
    )

    decision = choose_model(
        ModelMetrics(
            name="cnn",
            macro_f1=cnn["macro_f1"],
            p95_latency_ms=cnn["local_latency_ms"]["p95"],
            median_latency_ms=cnn["local_latency_ms"]["median"],
        ),
        ModelMetrics(
            name="cnn_lstm",
            macro_f1=cnn_lstm["macro_f1"],
            p95_latency_ms=cnn_lstm["local_latency_ms"]["p95"],
            median_latency_ms=cnn_lstm["local_latency_ms"]["median"],
        ),
    )

    summary = {
        "labels": list(GESTURES),
        "split_strategy": split.strategy,
        "test_subjects": sorted({row["subject_id"] for row in split.test}),
        "models": {
            "cnn": cnn,
            "cnn_lstm": cnn_lstm,
        },
        "comparison": {
            "selected_model": decision.selected,
            "reason": decision.reason,
            "macro_f1_gain_lstm_minus_cnn": round(cnn_lstm["macro_f1"] - cnn["macro_f1"], 6),
            "latency_p95_delta_ms_lstm_minus_cnn": round(
                cnn_lstm["local_latency_ms"]["p95"] - cnn["local_latency_ms"]["p95"],
                2,
            ),
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(
        json.dumps(
            {
                "selected_model": decision.selected,
                "cnn_macro_f1": cnn["macro_f1"],
                "cnn_lstm_macro_f1": cnn_lstm["macro_f1"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
