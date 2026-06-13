from ml.data_split import split_by_subject


def test_split_by_subject_keeps_subjects_out_of_multiple_splits():
    rows = [
        {"subject_id": "a", "file": "a1.jpg"},
        {"subject_id": "a", "file": "a2.jpg"},
        {"subject_id": "b", "file": "b1.jpg"},
        {"subject_id": "c", "file": "c1.jpg"},
        {"subject_id": "d", "file": "d1.jpg"},
        {"subject_id": "e", "file": "e1.jpg"},
    ]

    splits = split_by_subject(rows, train_ratio=0.5, val_ratio=0.25, seed=1)

    subject_sets = {
        name: {row["subject_id"] for row in split_rows}
        for name, split_rows in splits.items()
    }
    assert subject_sets["train"].isdisjoint(subject_sets["val"])
    assert subject_sets["train"].isdisjoint(subject_sets["test"])
    assert subject_sets["val"].isdisjoint(subject_sets["test"])
    assert sum(len(v) for v in splits.values()) == len(rows)
