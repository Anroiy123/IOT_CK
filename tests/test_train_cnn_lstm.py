from ml.sequence_utils import build_clip_samples, sample_evenly_spaced_rows


def test_sample_evenly_spaced_rows_picks_sorted_subset():
    rows = [
        {"frame_index": str(index), "file": f"frame_{index}.jpg"}
        for index in range(15)
    ]

    sampled = sample_evenly_spaced_rows(rows, 8)

    assert [int(row["frame_index"]) for row in sampled] == [0, 2, 4, 6, 8, 10, 12, 14]


def test_build_clip_samples_groups_and_preserves_metadata():
    rows = []
    for index in range(10):
        rows.append(
            {
                "subject_id": "s01",
                "gesture": "like",
                "clip_id": "clip-a",
                "frame_index": str(index),
                "file": f"like_{index}.jpg",
                "background": "complex",
                "lighting": "bright",
            }
        )

    clips = build_clip_samples(rows, frames=4)

    assert len(clips) == 1
    assert clips[0].subject_id == "s01"
    assert clips[0].gesture == "like"
    assert clips[0].clip_id == "clip-a"
    assert clips[0].background == "complex"
    assert clips[0].lighting == "bright"
    assert clips[0].frame_indices == (0, 3, 6, 9)
