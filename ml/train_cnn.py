from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import numpy as np
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split

from common.protocol import GESTURES
from ml.data_split import split_by_subject


@dataclass(frozen=True)
class DatasetSplit:
    train: list[dict[str, str]]
    val: list[dict[str, str]]
    test: list[dict[str, str]]
    strategy: str
    warning: str | None = None


def build_model(num_classes: int, image_size: int = 160, weights: str | None = "imagenet"):
    import tensorflow as tf

    base = tf.keras.applications.MobileNetV3Small(
        input_shape=(image_size, image_size, 3),
        include_top=False,
        weights=weights,
        pooling="avg",
    )
    base.trainable = False
    inputs = tf.keras.Input((image_size, image_size, 3))
    x = tf.keras.applications.mobilenet_v3.preprocess_input(inputs)
    x = base(x, training=False)
    x = tf.keras.layers.Dropout(0.2)(x)
    outputs = tf.keras.layers.Dense(num_classes, activation="softmax")(x)
    model = tf.keras.Model(inputs, outputs, name="gesture_cnn_baseline")
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    return model


def load_metadata(metadata_path: Path, *, require_found_files: bool = True) -> list[dict[str, str]]:
    if not metadata_path.exists():
        raise FileNotFoundError(f"Metadata file not found: {metadata_path}")
    root = metadata_path.parent.parent if metadata_path.parent.name == "data" else Path.cwd()
    rows: list[dict[str, str]] = []
    with metadata_path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            if row.get("gesture") not in GESTURES:
                continue
            image_path = Path(row["file"])
            if not image_path.is_absolute():
                image_path = root / image_path
            if require_found_files and not image_path.exists():
                continue
            normalized = dict(row)
            normalized["file"] = str(image_path)
            rows.append(normalized)
    if not rows:
        raise ValueError(f"No usable metadata rows found in {metadata_path}")
    return rows


def label_mapping(labels: Sequence[str] = GESTURES) -> dict[str, int]:
    return {label: index for index, label in enumerate(labels)}


def make_split(rows: Sequence[dict[str, str]], *, seed: int = 42, smoke: bool = False) -> DatasetSplit:
    rows = list(rows)
    subjects = {row["subject_id"] for row in rows}
    if len(subjects) >= 3 and not smoke:
        splits = split_by_subject(rows, train_ratio=0.70, val_ratio=0.15, seed=seed)
        return DatasetSplit(splits["train"], splits["val"], splits["test"], strategy="subject")

    warning = (
        "Only one or two subjects are available, so this run uses stratified frame-level split. "
        "Use at least 4 subjects for report-grade evaluation."
    )
    labels = [row["gesture"] for row in rows]
    train_rows, temp_rows = train_test_split(rows, test_size=0.30, random_state=seed, stratify=labels)
    temp_labels = [row["gesture"] for row in temp_rows]
    stratify_temp = temp_labels if _can_stratify(temp_labels) else None
    val_rows, test_rows = train_test_split(temp_rows, test_size=0.50, random_state=seed, stratify=stratify_temp)
    return DatasetSplit(train_rows, val_rows, test_rows, strategy="frame_stratified_smoke", warning=warning)


def _can_stratify(labels: Sequence[str]) -> bool:
    _, counts = np.unique(np.asarray(labels), return_counts=True)
    return bool(len(counts) > 1 and counts.min() >= 2)


def cap_rows_per_class(rows: Sequence[dict[str, str]], max_per_class: int, *, seed: int = 42) -> list[dict[str, str]]:
    if max_per_class <= 0:
        return list(rows)
    rng = np.random.default_rng(seed)
    capped: list[dict[str, str]] = []
    for label in GESTURES:
        label_rows = [row for row in rows if row["gesture"] == label]
        if len(label_rows) > max_per_class:
            indices = rng.choice(len(label_rows), size=max_per_class, replace=False)
            capped.extend(label_rows[int(index)] for index in indices)
        else:
            capped.extend(label_rows)
    return capped


def load_images(rows: Sequence[dict[str, str]], label_to_id: dict[str, int], *, image_size: int) -> tuple[np.ndarray, np.ndarray]:
    import cv2

    images: list[np.ndarray] = []
    labels: list[int] = []
    for row in rows:
        image = cv2.imread(row["file"])
        if image is None:
            continue
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (image_size, image_size), interpolation=cv2.INTER_AREA)
        images.append(image.astype("float32"))
        labels.append(label_to_id[row["gesture"]])
    if not images:
        raise ValueError("No images could be loaded from the selected metadata rows")
    return np.stack(images, axis=0), np.asarray(labels, dtype="int64")


def train_from_metadata(args: argparse.Namespace) -> dict[str, object]:
    import tensorflow as tf

    rows = load_metadata(args.metadata)
    if args.max_per_class > 0:
        rows = cap_rows_per_class(rows, args.max_per_class, seed=args.seed)
    split = make_split(rows, seed=args.seed, smoke=args.smoke)
    label_to_id = label_mapping()
    id_to_label = {index: label for label, index in label_to_id.items()}

    x_train, y_train = load_images(split.train, label_to_id, image_size=args.image_size)
    x_val, y_val = load_images(split.val, label_to_id, image_size=args.image_size)
    x_test, y_test = load_images(split.test, label_to_id, image_size=args.image_size)

    tf.keras.utils.set_random_seed(args.seed)
    weights = None if args.no_pretrained or args.smoke else "imagenet"
    model = build_model(len(GESTURES), image_size=args.image_size, weights=weights)
    callbacks = [
        tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=args.patience, restore_best_weights=True),
    ]
    history = model.fit(
        x_train,
        y_train,
        validation_data=(x_val, y_val),
        epochs=args.epochs,
        batch_size=args.batch_size,
        callbacks=callbacks,
        verbose=2,
    )

    probabilities = model.predict(x_test, batch_size=args.batch_size, verbose=0)
    y_pred = probabilities.argmax(axis=1)
    labels = list(range(len(GESTURES)))
    metrics: dict[str, object] = {
        "model_name": "gesture_cnn_baseline",
        "model_type": "cnn",
        "labels": list(GESTURES),
        "label_to_id": label_to_id,
        "split_strategy": split.strategy,
        "warning": split.warning,
        "counts": {
            "total": len(rows),
            "train": len(x_train),
            "val": len(x_val),
            "test": len(x_test),
        },
        "subjects": sorted({row["subject_id"] for row in rows}),
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "macro_f1": float(f1_score(y_test, y_pred, labels=labels, average="macro", zero_division=0)),
        "classification_report": classification_report(
            y_test,
            y_pred,
            labels=labels,
            target_names=[id_to_label[index] for index in labels],
            output_dict=True,
            zero_division=0,
        ),
        "confusion_matrix": confusion_matrix(y_test, y_pred, labels=labels).tolist(),
        "history": {key: [float(value) for value in values] for key, values in history.history.items()},
        "image_size": args.image_size,
        "epochs_requested": args.epochs,
        "batch_size": args.batch_size,
        "pretrained": weights == "imagenet",
    }

    args.output_model.parent.mkdir(parents=True, exist_ok=True)
    args.metrics_out.parent.mkdir(parents=True, exist_ok=True)
    model.save(args.output_model)
    args.metrics_out.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return metrics


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata", type=Path, default=Path("data/metadata.csv"))
    parser.add_argument("--output-model", type=Path, default=Path("models/gesture-cnn-baseline.keras"))
    parser.add_argument("--metrics-out", type=Path, default=Path("reports/cnn_baseline_metrics.json"))
    parser.add_argument("--num-classes", type=int, default=len(GESTURES))
    parser.add_argument("--image-size", type=int, default=160)
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--patience", type=int, default=2)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--max-per-class", type=int, default=0)
    parser.add_argument("--smoke", action="store_true", help="Use frame-level split and random MobileNet weights for a fast pipeline test.")
    parser.add_argument("--no-pretrained", action="store_true", help="Do not download/use ImageNet weights.")
    parser.add_argument("--summary", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.summary:
        model = build_model(args.num_classes, image_size=args.image_size, weights=None if args.no_pretrained else "imagenet")
        model.summary()
        return
    metrics = train_from_metadata(args)
    print(json.dumps({key: metrics[key] for key in ("accuracy", "macro_f1", "split_strategy", "counts", "warning")}, indent=2))


if __name__ == "__main__":
    main()
