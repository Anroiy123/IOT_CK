from gateway.safety import GestureStabilizer, LatencyLogRow, SafetyPolicy


def test_stabilizer_requires_three_normal_predictions_before_command():
    policy = SafetyPolicy(normal_required=3, stop_required=2, min_confidence=0.8)
    stabilizer = GestureStabilizer(policy)

    assert stabilizer.accept("like", 0.91) is None
    assert stabilizer.accept("like", 0.92) is None
    assert stabilizer.accept("like", 0.93) == "like"


def test_stabilizer_allows_stop_after_two_predictions():
    stabilizer = GestureStabilizer(SafetyPolicy())

    assert stabilizer.accept("stop", 0.81) is None
    assert stabilizer.accept("stop", 0.82) == "stop"


def test_stabilizer_ignores_low_confidence_and_resets_sequence():
    stabilizer = GestureStabilizer(SafetyPolicy(min_confidence=0.8))

    assert stabilizer.accept("like", 0.9) is None
    assert stabilizer.accept("like", 0.4) is None
    assert stabilizer.accept("like", 0.9) is None


def test_latency_log_row_includes_request_and_session_ids():
    row = LatencyLogRow(
        session_id="s1",
        request_id="r1",
        gesture="like",
        confidence=0.92,
        mode="car",
        command="forward",
        capture_ms=12.0,
        preprocess_ms=8.0,
        cloud_rtt_ms=70.0,
        inference_ms=24.0,
        esp32_ack_ms=15.0,
        total_ms=129.0,
    )

    csv_row = row.to_csv_row()

    assert csv_row["session_id"] == "s1"
    assert csv_row["request_id"] == "r1"
    assert csv_row["total_ms"] == "129.00"
