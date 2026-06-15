import numpy as np

from ml.evaluate_models import (
    aggregate_frame_probabilities_to_clips,
    summarize_false_activation,
    summarize_robustness,
)
from ml.train_cnn import label_mapping


def test_aggregate_frame_probabilities_to_clips_averages_per_clip():
    mapping = label_mapping()
    rows = [
        {
            "subject_id": "s01",
            "gesture": "like",
            "clip_id": "clip-1",
            "background": "simple",
            "lighting": "bright",
        },
        {
            "subject_id": "s01",
            "gesture": "like",
            "clip_id": "clip-1",
            "background": "simple",
            "lighting": "bright",
        },
    ]
    probabilities = np.zeros((2, len(mapping)), dtype=np.float32)
    probabilities[0, mapping["like"]] = 0.9
    probabilities[0, mapping["stop"]] = 0.1
    probabilities[1, mapping["like"]] = 0.7
    probabilities[1, mapping["stop"]] = 0.3

    clips, y_true, clip_probabilities = aggregate_frame_probabilities_to_clips(rows, probabilities, label_to_id=mapping)

    assert len(clips) == 1
    assert clips[0]["predicted_gesture"] == "like"
    assert clips[0]["frame_count"] == 2
    assert y_true.tolist() == [mapping["like"]]
    assert round(float(clip_probabilities[0, mapping["like"]]), 2) == 0.8


def test_summarize_robustness_and_false_activation():
    mapping = label_mapping()
    predictions = [
        {"gesture": "like", "predicted_gesture": "like", "background": "simple"},
        {"gesture": "stop", "predicted_gesture": "peace", "background": "simple"},
        {"gesture": "like", "predicted_gesture": "stop", "background": "complex"},
        {"gesture": "no_gesture", "predicted_gesture": "no_gesture", "background": "complex"},
        {"gesture": "no_gesture", "predicted_gesture": "like", "background": "simple"},
    ]

    robustness = summarize_robustness(predictions, label_to_id=mapping)
    false_activation = summarize_false_activation(predictions)

    assert robustness["simple"]["count"] == 3
    assert robustness["complex"]["count"] == 2
    assert false_activation["count"] == 2
    assert false_activation["false_positive_count"] == 1
    assert false_activation["rate"] == 0.5
