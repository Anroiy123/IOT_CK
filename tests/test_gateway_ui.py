from gateway.main import _ui_lines


def test_ui_lines_show_selected_arm_motor_in_arm_mode():
    lines = _ui_lines("arm", "upper", "no_gesture", 0.7, 179.1, "")

    assert lines == [
        "mode: arm",
        "arm motor: upper",
        "gesture: no_gesture (0.70)",
        "latency: 179.1 ms",
        "command: -",
    ]


def test_ui_lines_hide_arm_motor_in_car_mode():
    lines = _ui_lines("car", "upper", "like", 0.92, 101.0, "forward")

    assert "arm motor: upper" not in lines
    assert lines == [
        "mode: car",
        "gesture: like (0.92)",
        "latency: 101.0 ms",
        "command: forward",
    ]
