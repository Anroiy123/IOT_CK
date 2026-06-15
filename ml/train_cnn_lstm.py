from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score

from common.protocol import GESTURES
from ml.sequence_utils import build_clip_samples, load_sequence_images
from ml.train_cnn import label_mapping, load_metadata, make_split


def build_model(num_classes: int, image_size: int = 160, frames: int = 8):
    import tensorflow as tf

    base = tf.keras.applications.MobileNetV3Small(
        input_shape=(image_size, image_size, 3),
        include_top=False,
        weights="imagenet",
        pooling="avg",
    )
    base.trainable = False
    inputs = tf.keras.Input((frames, image_size, image_size, 3))
    x = tf.keras.layers.TimeDistributed(tf.keras.layers.Rescaling(1.0 / 127.5, offset=-1))(inputs)
    x = tf.keras.layers.TimeDistributed(base)(x)
    x = tf.keras.layers.LSTM(64)(x)
    x = tf.keras.layers.Dropout(0.2)(x)
    outputs = tf.keras.layers.Dense(num_classes, activation="softmax")(x)
    model = tf.keras.Model(inputs, outputs, name="gesture_cnn_lstm_comparison")
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    return model


def train_from_metadata(args: argparse.Namespace) -> dict[str, object]:
    import tensorflow as tf

    rows = load_metadata(args.metadata)
    split = make_split(rows, seed=args.seed, smoke=False)
    label_to_id = label_mapping()
    id_to_label = {index: label for label, index in label_to_id.items()}

    train_clips = build_clip_samples(split.train, frames=args.frames)
    val_clips = build_clip_samples(split.val, frames=args.frames)
    test_clips = build_clip_samples(split.test, frames=args.frames)

    x_train, y_train = load_sequence_images(train_clips, label_to_id, image_size=args.image_size)
    x_val, y_val = load_sequence_images(val_clips, label_to_id, image_size=args.image_size)
    x_test, y_test = load_sequence_images(test_clips, label_to_id, image_size=args.image_size)

    tf.keras.utils.set_random_seed(args.seed)
    model = build_model(len(GESTURES), image_size=args.image_size, frames=args.frames)
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

    probabilities = np.asarray(model.predict(x_test, batch_size=args.batch_size, verbose=0), dtype="float32")
    y_pred = probabilities.argmax(axis=1)
    labels = list(range(len(GESTURES)))
    metrics: dict[str, object] = {
        "model_name": "gesture_cnn_lstm_comparison",
        "model_type": "cnn_lstm",
        "labels": list(GESTURES),
        "label_to_id": label_to_id,
        "split_strategy": split.strategy,
        "warning": split.warning,
        "counts": {
            "total_frames": len(rows),
            "train_clips": len(train_clips),
            "val_clips": len(val_clips),
            "test_clips": len(test_clips),
            "train_sequences": len(x_train),
            "val_sequences": len(x_val),
            "test_sequences": len(x_test),
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
        "frames": args.frames,
        "epochs_requested": args.epochs,
        "batch_size": args.batch_size,
        "pretrained": True,
        "test_predictions": [
            {
                "subject_id": clip.subject_id,
                "gesture": clip.gesture,
                "predicted_gesture": id_to_label[int(pred_id)],
                "clip_id": clip.clip_id,
                "background": clip.background,
                "lighting": clip.lighting,
                "confidence": float(probabilities[index][int(pred_id)]),
                "probabilities": {id_to_label[i]: float(probabilities[index][i]) for i in labels},
            }
            for index, (clip, pred_id) in enumerate(zip(test_clips, y_pred))
        ],
    }

    args.output_model.parent.mkdir(parents=True, exist_ok=True)
    args.metrics_out.parent.mkdir(parents=True, exist_ok=True)
    model.save(args.output_model)
    args.metrics_out.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return metrics


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata", type=Path, default=Path("data/metadata.csv"))
    parser.add_argument("--output-model", type=Path, default=Path("models/gesture-cnn-lstm-comparison.keras"))
    parser.add_argument("--metrics-out", type=Path, default=Path("reports/cnn_lstm_metrics.json"))
    parser.add_argument("--image-size", type=int, default=160)
    parser.add_argument("--frames", type=int, default=8)
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--patience", type=int, default=2)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--summary", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.summary:
        model = build_model(len(GESTURES), image_size=args.image_size, frames=args.frames)
        model.summary()
        return
    metrics = train_from_metadata(args)
    print(
        json.dumps(
            {
                key: metrics[key]
                for key in ("accuracy", "macro_f1", "split_strategy", "counts", "warning")
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
