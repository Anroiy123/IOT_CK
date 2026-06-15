from ml.model_policy import (
    DEFAULT_ACCEPTANCE_CRITERIA,
    ModelMetrics,
    choose_model,
    required_experiments,
)


def test_acceptance_criteria_have_minimum_and_target_levels():
    assert DEFAULT_ACCEPTANCE_CRITERIA["minimum"]["macro_f1"] == 0.85
    assert DEFAULT_ACCEPTANCE_CRITERIA["target"]["macro_f1"] == 0.90
    assert DEFAULT_ACCEPTANCE_CRITERIA["minimum"]["p95_latency_ms"] == 500
    assert DEFAULT_ACCEPTANCE_CRITERIA["target"]["median_latency_ms"] == 300


def test_cnn_and_lstm_are_required_for_final_comparison():
    experiments = required_experiments()

    assert experiments[0]["name"] == "cnn"
    assert experiments[0]["required"] is True
    assert experiments[1]["name"] == "cnn_lstm"
    assert experiments[1]["required"] is True


def test_choose_cnn_when_accuracy_close_and_latency_is_much_better():
    cnn = ModelMetrics(name="cnn", macro_f1=0.90, p95_latency_ms=250, median_latency_ms=120)
    lstm = ModelMetrics(name="cnn_lstm", macro_f1=0.915, p95_latency_ms=380, median_latency_ms=200)

    assert choose_model(cnn, lstm).selected == "cnn"


def test_choose_lstm_when_it_improves_accuracy_and_stays_under_latency_budget():
    cnn = ModelMetrics(name="cnn", macro_f1=0.88, p95_latency_ms=250, median_latency_ms=120)
    lstm = ModelMetrics(name="cnn_lstm", macro_f1=0.91, p95_latency_ms=460, median_latency_ms=210)

    assert choose_model(cnn, lstm).selected == "cnn_lstm"
