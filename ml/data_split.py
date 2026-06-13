from __future__ import annotations

import random
from collections.abc import Sequence


def split_by_subject(
    rows: Sequence[dict],
    *,
    train_ratio: float = 0.70,
    val_ratio: float = 0.15,
    seed: int = 42,
) -> dict[str, list[dict]]:
    subjects = sorted({row["subject_id"] for row in rows})
    rng = random.Random(seed)
    rng.shuffle(subjects)
    n_subjects = len(subjects)
    train_n = max(1, int(n_subjects * train_ratio)) if n_subjects else 0
    val_n = max(1, int(n_subjects * val_ratio)) if n_subjects - train_n > 1 else max(0, n_subjects - train_n)
    train_subjects = set(subjects[:train_n])
    val_subjects = set(subjects[train_n : train_n + val_n])
    test_subjects = set(subjects[train_n + val_n :])
    return {
        "train": [row for row in rows if row["subject_id"] in train_subjects],
        "val": [row for row in rows if row["subject_id"] in val_subjects],
        "test": [row for row in rows if row["subject_id"] in test_subjects],
    }
