from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Sequence

import numpy as np


@dataclass(frozen=True)
class ClipSample:
    subject_id: str
    gesture: str
    clip_id: str
    background: str
    lighting: str
    files: tuple[str, ...]
    frame_indices: tuple[int, ...]


def sample_evenly_spaced_rows(rows: Sequence[dict[str, str]], frames: int) -> list[dict[str, str]]:
    if frames <= 0:
        raise ValueError("frames must be positive")
    ordered = sorted(rows, key=lambda row: int(row["frame_index"]))
    if len(ordered) < frames:
        raise ValueError(f"Clip has only {len(ordered)} frames, expected at least {frames}")
    if len(ordered) == frames:
        return list(ordered)
    indices = np.linspace(0, len(ordered) - 1, num=frames, dtype=int)
    return [ordered[int(index)] for index in indices]


def build_clip_samples(rows: Sequence[dict[str, str]], *, frames: int) -> list[ClipSample]:
    grouped: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[(row["subject_id"], row["gesture"], row["clip_id"])].append(row)

    clips: list[ClipSample] = []
    for (subject_id, gesture, clip_id), clip_rows in sorted(grouped.items()):
        selected = sample_evenly_spaced_rows(clip_rows, frames)
        first = selected[0]
        clips.append(
            ClipSample(
                subject_id=subject_id,
                gesture=gesture,
                clip_id=clip_id,
                background=first.get("background", "unknown"),
                lighting=first.get("lighting", "unknown"),
                files=tuple(row["file"] for row in selected),
                frame_indices=tuple(int(row["frame_index"]) for row in selected),
            )
        )
    return clips


def load_sequence_images(
    clips: Sequence[ClipSample],
    label_to_id: dict[str, int],
    *,
    image_size: int,
) -> tuple[np.ndarray, np.ndarray]:
    import cv2

    sequences: list[np.ndarray] = []
    labels: list[int] = []
    for clip in clips:
        frames: list[np.ndarray] = []
        for file_path in clip.files:
            image = cv2.imread(file_path)
            if image is None:
                frames = []
                break
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = cv2.resize(image, (image_size, image_size), interpolation=cv2.INTER_AREA)
            frames.append(image.astype("float32"))
        if not frames:
            continue
        sequences.append(np.stack(frames, axis=0))
        labels.append(label_to_id[clip.gesture])
    if not sequences:
        raise ValueError("No clip sequences could be loaded from the selected metadata rows")
    return np.stack(sequences, axis=0), np.asarray(labels, dtype="int64")
