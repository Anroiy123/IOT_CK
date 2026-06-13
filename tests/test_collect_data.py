from pathlib import Path

import pytest

from ml.collect_data import append_metadata, clip_dir, make_clip_id, metadata_row, validate_labels


def test_validate_labels_accepts_known_gestures_and_normalizes_case():
    assert validate_labels(["Stop", "LIKE", "no_gesture"]) == ("stop", "like", "no_gesture")


def test_validate_labels_rejects_unknown_gesture():
    with pytest.raises(ValueError, match="Unknown gesture"):
        validate_labels(["wave"])


def test_clip_id_and_directory_are_stable():
    clip_id = make_clip_id("like", 3)

    assert clip_id.endswith("_like_003")
    assert clip_dir(Path("data/raw"), "s01", "like", clip_id) == Path("data/raw/s01/like") / clip_id


def test_append_metadata_writes_header_once(tmp_path):
    metadata_path = tmp_path / "metadata.csv"
    image_path = tmp_path / "data" / "raw" / "s01" / "like" / "clip1" / "frame_000.jpg"
    row = metadata_row(
        file_path=image_path,
        subject_id="s01",
        gesture="like",
        clip_id="clip1",
        frame_index=0,
        timestamp_ms=12,
        background="simple",
        lighting="bright",
        found_hand=True,
        base_dir=tmp_path,
    )

    assert append_metadata(metadata_path, [row]) == 1
    assert append_metadata(metadata_path, [row]) == 1

    lines = metadata_path.read_text(encoding="utf-8").splitlines()
    assert lines[0].startswith("file,subject_id,gesture,clip_id")
    assert len(lines) == 3
    assert "data/raw/s01/like/clip1/frame_000.jpg" in lines[1]
