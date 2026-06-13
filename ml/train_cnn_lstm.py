from __future__ import annotations

import argparse


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
    outputs = tf.keras.layers.Dense(num_classes, activation="softmax")(x)
    model = tf.keras.Model(inputs, outputs, name="gesture_cnn_lstm_comparison")
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    return model


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--num-classes", type=int, default=8)
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    model = build_model(args.num_classes)
    if args.summary:
        model.summary()


if __name__ == "__main__":
    main()
