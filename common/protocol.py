from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any


class Mode(StrEnum):
    CAR = "car"
    ARM = "arm"


class Action(StrEnum):
    STOP = "stop"
    FORWARD = "forward"
    BACKWARD = "backward"
    LEFT = "left"
    RIGHT = "right"
    SET_MODE = "set_mode"
    ARM_DELTA = "arm_delta"
    SELECT_JOINT = "select_joint"


ARM_JOINTS = ("base", "lower", "upper", "gripper")
GESTURES = ("stop", "peace", "rock", "like", "dislike", "one", "two", "no_gesture")


@dataclass(frozen=True)
class Command:
    seq: int
    session_id: str
    request_id: str
    mode: Mode
    action: Action
    speed: int = 0
    joint: str | None = None
    delta: int = 0
    ttl_ms: int = 600
    token: str | None = None

    def to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "seq": self.seq,
            "session_id": self.session_id,
            "request_id": self.request_id,
            "mode": self.mode.value,
            "action": self.action.value,
            "speed": max(0, min(255, int(self.speed))),
            "ttl_ms": max(1, int(self.ttl_ms)),
        }
        if self.joint is not None:
            payload["joint"] = self.joint
        if self.delta:
            payload["delta"] = self.delta
        if self.token is not None:
            payload["token"] = self.token
        return payload


def next_joint(current: str, step: int) -> str:
    if current not in ARM_JOINTS:
        current = ARM_JOINTS[0]
    index = ARM_JOINTS.index(current)
    return ARM_JOINTS[(index + step) % len(ARM_JOINTS)]


class GestureMapper:
    def __init__(self, speed: int = 180, servo_step: int = 5, ttl_ms: int = 600) -> None:
        self.speed = speed
        self.servo_step = servo_step
        self.ttl_ms = ttl_ms

    def map_gesture(self, gesture: str, mode: Mode, joint: str = "base") -> Command | None:
        gesture = (gesture or "").strip().lower()
        mode = Mode(mode)

        if gesture in {"", "no_gesture", "none", "unknown"}:
            return None
        if gesture == "stop":
            return self._template(mode=mode, action=Action.STOP, speed=0)
        if gesture == "peace":
            return self._template(mode=Mode.CAR, action=Action.SET_MODE)
        if gesture == "rock":
            return self._template(mode=Mode.ARM, action=Action.SET_MODE)

        if mode == Mode.CAR:
            car_actions = {
                "like": Action.FORWARD,
                "dislike": Action.BACKWARD,
                "one": Action.LEFT,
                "two": Action.RIGHT,
            }
            action = car_actions.get(gesture)
            if action is None:
                return None
            return self._template(mode=mode, action=action, speed=self.speed)

        if gesture == "like":
            return self._template(mode=mode, action=Action.ARM_DELTA, joint=joint, delta=self.servo_step)
        if gesture == "dislike":
            return self._template(mode=mode, action=Action.ARM_DELTA, joint=joint, delta=-self.servo_step)
        if gesture == "one":
            return self._template(mode=mode, action=Action.SELECT_JOINT, joint=next_joint(joint, -1))
        if gesture == "two":
            return self._template(mode=mode, action=Action.SELECT_JOINT, joint=next_joint(joint, 1))
        return None

    def _template(
        self,
        *,
        mode: Mode,
        action: Action,
        speed: int = 0,
        joint: str | None = None,
        delta: int = 0,
    ) -> Command:
        return Command(
            seq=0,
            session_id="",
            request_id="",
            mode=mode,
            action=action,
            speed=speed,
            joint=joint,
            delta=delta,
            ttl_ms=self.ttl_ms,
        )
