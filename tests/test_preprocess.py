from types import SimpleNamespace

from gateway.preprocess import count_extended_fingers, disambiguate_one_two


def _landmarks(*, extended_fingers: tuple[int, ...]):
    landmarks = [SimpleNamespace(x=0.0, y=0.0, z=0.0) for _ in range(21)]
    finger_joints = ((5, 6, 8), (9, 10, 12), (13, 14, 16), (17, 18, 20))
    for finger_index, (mcp, pip, tip) in enumerate(finger_joints):
        landmarks[mcp] = SimpleNamespace(x=0.0, y=0.0, z=0.0)
        landmarks[pip] = SimpleNamespace(x=1.0, y=0.0, z=0.0)
        if finger_index in extended_fingers:
            landmarks[tip] = SimpleNamespace(x=2.0, y=0.0, z=0.0)
        else:
            landmarks[tip] = SimpleNamespace(x=1.0, y=1.0, z=0.0)
    return landmarks


def test_count_extended_fingers_uses_orientation_independent_joint_angles():
    assert count_extended_fingers(_landmarks(extended_fingers=(0,))) == 1
    assert count_extended_fingers(_landmarks(extended_fingers=(0, 1))) == 2


def test_disambiguate_one_two_uses_landmarks_only_for_the_confused_pair():
    assert disambiguate_one_two("one", 2) == "two"
    assert disambiguate_one_two("two", 1) == "one"
    assert disambiguate_one_two("like", 2) == "like"
    assert disambiguate_one_two("one", None) == "one"
    assert disambiguate_one_two("two", 3) == "two"
