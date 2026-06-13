from pathlib import Path

from ml.train_cnn import cap_rows_per_class, label_mapping, load_metadata, make_split


def test_label_mapping_uses_stable_gesture_order():
    mapping = label_mapping()

    assert mapping["stop"] == 0
    assert mapping["no_gesture"] == 7


def test_make_split_falls_back_to_frame_split_for_single_subject():
    rows = []
    for label in ("stop", "peace", "rock", "like", "dislike", "one", "two", "no_gesture"):
        for index in range(5):
            rows.append({"subject_id": "s01", "gesture": label, "file": f"{label}_{index}.jpg"})

    split = make_split(rows, smoke=True, seed=1)

    assert split.strategy == "frame_stratified_smoke"
    assert split.warning is not None
    assert len(split.train) + len(split.val) + len(split.test) == len(rows)


def test_cap_rows_per_class_limits_each_class():
    rows = [
        {"subject_id": "s01", "gesture": "like", "file": f"like_{index}.jpg"}
        for index in range(10)
    ] + [
        {"subject_id": "s01", "gesture": "stop", "file": f"stop_{index}.jpg"}
        for index in range(3)
    ]

    capped = cap_rows_per_class(rows, 4, seed=1)

    assert sum(1 for row in capped if row["gesture"] == "like") == 4
    assert sum(1 for row in capped if row["gesture"] == "stop") == 3


def test_load_metadata_resolves_relative_files(tmp_path):
    image_path = tmp_path / "data" / "raw" / "s01" / "like" / "clip" / "frame_000.jpg"
    image_path.parent.mkdir(parents=True)
    image_path.write_bytes(b"fake")
    metadata = tmp_path / "data" / "metadata.csv"
    metadata.write_text(
        "file,subject_id,gesture,clip_id,frame_index,timestamp_ms,background,lighting,split,found_hand\n"
        "data/raw/s01/like/clip/frame_000.jpg,s01,like,clip,0,0,unknown,unknown,,1\n",
        encoding="utf-8",
    )

    rows = load_metadata(metadata)

    assert len(rows) == 1
    assert Path(rows[0]["file"]).is_absolute()
