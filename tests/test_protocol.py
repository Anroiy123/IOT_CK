from common.protocol import (
    Action,
    Command,
    GestureMapper,
    Mode,
    next_joint,
)


def test_car_mode_maps_core_gestures_to_vehicle_actions():
    mapper = GestureMapper()

    assert mapper.map_gesture("peace", Mode.CAR).mode == Mode.CAR
    assert mapper.map_gesture("like", Mode.CAR).action == Action.FORWARD
    assert mapper.map_gesture("dislike", Mode.CAR).action == Action.BACKWARD
    assert mapper.map_gesture("one", Mode.CAR).action == Action.LEFT
    assert mapper.map_gesture("two", Mode.CAR).action == Action.RIGHT


def test_arm_mode_maps_gestures_to_joint_adjustments():
    mapper = GestureMapper()

    assert mapper.map_gesture("rock", Mode.CAR).mode == Mode.ARM
    assert mapper.map_gesture("like", Mode.ARM, joint="base").delta == 5
    assert mapper.map_gesture("dislike", Mode.ARM, joint="base").delta == -5
    assert mapper.map_gesture("one", Mode.ARM, joint="lower").joint == "base"
    assert mapper.map_gesture("two", Mode.ARM, joint="lower").joint == "upper"


def test_stop_and_no_gesture_are_safe():
    mapper = GestureMapper()

    assert mapper.map_gesture("stop", Mode.ARM).action == Action.STOP
    assert mapper.map_gesture("no_gesture", Mode.CAR) is None
    assert mapper.map_gesture("unknown", Mode.CAR) is None


def test_command_payload_contains_session_and_request_identity():
    command = Command(
        seq=7,
        session_id="session-1",
        request_id="request-1",
        mode=Mode.CAR,
        action=Action.FORWARD,
        speed=180,
        ttl_ms=600,
    )

    payload = command.to_payload()

    assert payload["seq"] == 7
    assert payload["session_id"] == "session-1"
    assert payload["request_id"] == "request-1"
    assert payload["mode"] == "car"
    assert payload["action"] == "forward"
    assert payload["ttl_ms"] == 600


def test_next_joint_wraps_through_robot_arm_joints():
    assert next_joint("base", 1) == "lower"
    assert next_joint("lower", 1) == "upper"
    assert next_joint("upper", 1) == "gripper"
    assert next_joint("gripper", 1) == "base"
    assert next_joint("base", -1) == "gripper"
