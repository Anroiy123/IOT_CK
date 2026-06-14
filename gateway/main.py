from __future__ import annotations

import argparse
import csv
import json
import time
import uuid
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen

import cv2

from common.protocol import Action, Command, GestureMapper, Mode
from gateway.cloud_client import CloudGestureClient, CloudPrediction
from gateway.preprocess import MediaPipeCropper
from gateway.safety import GestureStabilizer, LatencyLogRow, SafetyPolicy
from gateway.transport import DryRunTransport, WebSocketTransport


def run_gateway(args: argparse.Namespace) -> None:
    session_id = args.session_id or str(uuid.uuid4())
    mapper = GestureMapper(speed=args.speed)
    stabilizer = GestureStabilizer(
        SafetyPolicy(
            normal_required=args.normal_required,
            mode_required=args.mode_required,
            stop_required=args.stop_required,
            min_confidence=args.min_confidence,
            mode_min_confidence=args.mode_min_confidence,
            servo_cooldown_ms=args.servo_cooldown_ms,
        )
    )
    cropper = MediaPipeCropper()
    cloud = CloudGestureClient(args.cloud_url, args.api_key)
    transport = DryRunTransport() if args.dry_run else WebSocketTransport(args.esp32_ws)
    mode = Mode.CAR
    joint = "base"
    seq = _initial_sequence(args.esp32_ws)
    frame_count = 0
    active_drive_template: Command | None = None
    active_drive_until = 0.0
    last_drive_repeat_at = 0.0
    last_servo_command_at = 0.0
    args.log.parent.mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        raise RuntimeError(f"Khong mo duoc camera index {args.camera}")

    with args.log.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=LatencyLogRow.header())
        if f.tell() == 0:
            writer.writeheader()
        last_command_at = time.perf_counter()
        while True:
            frame_start = time.perf_counter()
            ok, frame = cap.read()
            capture_ms = (time.perf_counter() - frame_start) * 1000
            request_id = str(uuid.uuid4())
            if not ok:
                seq = _send_stop_safely(transport, mapper, seq, session_id, request_id, mode, args.esp32_token)
                break

            prep_start = time.perf_counter()
            crop = cropper.crop(frame)
            ok_jpeg, encoded = cv2.imencode(".jpg", crop.image)
            preprocess_ms = (time.perf_counter() - prep_start) * 1000
            if not ok_jpeg:
                continue

            if not crop.found_hand and args.skip_cloud_without_hand:
                cloud_pred = CloudPrediction(
                    gesture="no_gesture",
                    confidence=0.0,
                    inference_ms=0.0,
                    model_version="mediapipe-gate",
                    model_type="hand-gate",
                    session_id=session_id,
                    request_id=request_id,
                    rtt_ms=0.0,
                )
            else:
                try:
                    cloud_pred = cloud.predict([encoded.tobytes()], session_id=session_id, request_id=request_id)
                except Exception as exc:
                    print(f"Cloud prediction failed: {exc}")
                    active_drive_template = None
                    seq = _send_stop_safely(transport, mapper, seq, session_id, request_id, mode, args.esp32_token)
                    cloud_pred = CloudPrediction(
                        gesture="cloud_error",
                        confidence=0.0,
                        inference_ms=0.0,
                        model_version="unavailable",
                        model_type="unavailable",
                        session_id=session_id,
                        request_id=request_id,
                        rtt_ms=0.0,
                    )
            accepted = stabilizer.accept(cloud_pred.gesture, cloud_pred.confidence)
            command_name = ""
            ack_ms = 0.0
            if accepted:
                template = mapper.map_gesture(accepted, mode, joint=joint)
                if template is not None:
                    now = time.perf_counter()
                    if _is_arm_action(template.action) and (now - last_servo_command_at) * 1000 < args.servo_cooldown_ms:
                        command_name = "cooldown"
                    else:
                        seq += 1
                        command = Command(
                            seq=seq,
                            session_id=session_id,
                            request_id=request_id,
                            mode=template.mode,
                            action=template.action,
                            speed=template.speed,
                            joint=template.joint,
                            delta=template.delta,
                            ttl_ms=template.ttl_ms,
                            token=args.esp32_token,
                        )
                        try:
                            ack_ms = transport.send(command)
                            mode = command.mode
                            if command.joint:
                                joint = command.joint
                            command_name = command.action.value
                            last_command_at = time.perf_counter()
                            if _is_drive_action(command.action):
                                active_drive_template = template
                                active_drive_until = last_command_at + args.drive_hold_ms / 1000
                                last_drive_repeat_at = last_command_at
                            else:
                                active_drive_template = None
                            if _is_arm_action(command.action):
                                last_servo_command_at = last_command_at
                        except Exception:
                            command_name = "send_failed"
                            active_drive_template = None

            now = time.perf_counter()
            if (
                not command_name
                and active_drive_template is not None
                and now <= active_drive_until
                and (now - last_drive_repeat_at) * 1000 >= args.drive_repeat_ms
            ):
                seq += 1
                command = Command(
                    seq=seq,
                    session_id=session_id,
                    request_id=request_id,
                    mode=active_drive_template.mode,
                    action=active_drive_template.action,
                    speed=active_drive_template.speed,
                    ttl_ms=active_drive_template.ttl_ms,
                    token=args.esp32_token,
                )
                try:
                    ack_ms = transport.send(command)
                    command_name = command.action.value
                    last_command_at = now
                    last_drive_repeat_at = now
                except Exception:
                    command_name = "send_failed"
                    active_drive_template = None
            elif active_drive_template is not None and now > active_drive_until:
                active_drive_template = None

            if (time.perf_counter() - last_command_at) * 1000 > args.deadman_ms:
                active_drive_template = None
                seq = _send_stop_safely(transport, mapper, seq, session_id, request_id, mode, args.esp32_token)
                last_command_at = time.perf_counter()

            total_ms = capture_ms + preprocess_ms + cloud_pred.rtt_ms + ack_ms
            writer.writerow(
                LatencyLogRow(
                    session_id=session_id,
                    request_id=request_id,
                    gesture=cloud_pred.gesture,
                    confidence=cloud_pred.confidence,
                    mode=mode.value,
                    command=command_name,
                    capture_ms=capture_ms,
                    preprocess_ms=preprocess_ms,
                    cloud_rtt_ms=cloud_pred.rtt_ms,
                    inference_ms=cloud_pred.inference_ms,
                    esp32_ack_ms=ack_ms,
                    total_ms=total_ms,
                ).to_csv_row()
            )
            display_frame = cv2.flip(frame, 1)
            _draw_ui(display_frame, mode.value, cloud_pred.gesture, cloud_pred.confidence, total_ms, command_name)
            if not args.headless:
                cv2.imshow("IOT_CK Gateway", display_frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            frame_count += 1
            if args.max_frames and frame_count >= args.max_frames:
                break
    cap.release()
    cv2.destroyAllWindows()
    cloud.close()


def _is_drive_action(action: Action) -> bool:
    return action in {Action.FORWARD, Action.BACKWARD, Action.LEFT, Action.RIGHT}


def _is_arm_action(action: Action) -> bool:
    return action in {Action.ARM_DELTA, Action.SELECT_JOINT}


def _initial_sequence(esp32_ws: str) -> int:
    try:
        parsed = urlparse(esp32_ws)
        host = parsed.hostname
        if not host:
            raise ValueError("missing ESP32 host")
        with urlopen(f"http://{host}/state", timeout=1.5) as response:
            state = json.loads(response.read().decode("utf-8"))
        return max(0, int(state.get("last_seq", 0)))
    except Exception:
        return int(time.time()) & 0x7FFFFFFF


def _send_stop_safely(transport, mapper: GestureMapper, seq: int, session_id: str, request_id: str, mode: Mode, token: str) -> int:
    template = mapper.map_gesture("stop", mode)
    if template is None:
        return seq
    seq += 1
    command = Command(
        seq=seq,
        session_id=session_id,
        request_id=request_id,
        mode=mode,
        action=template.action,
        speed=0,
        ttl_ms=template.ttl_ms,
        token=token,
    )
    try:
        transport.send(command)
    except Exception:
        pass
    return seq


def _draw_ui(frame, mode: str, gesture: str, confidence: float, latency_ms: float, command: str) -> None:
    lines = [
        f"mode: {mode}",
        f"gesture: {gesture} ({confidence:.2f})",
        f"latency: {latency_ms:.1f} ms",
        f"command: {command or '-'}",
    ]
    for index, line in enumerate(lines):
        cv2.putText(frame, line, (20, 35 + index * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cloud-url", required=True)
    parser.add_argument("--api-key", required=True)
    parser.add_argument("--esp32-ws", default="ws://192.168.4.1:81/")
    parser.add_argument("--esp32-token", default="CHANGE_ME")
    parser.add_argument("--camera", type=int, default=0)
    parser.add_argument("--speed", type=int, default=180)
    parser.add_argument("--deadman-ms", type=int, default=600)
    parser.add_argument("--min-confidence", type=float, default=0.80)
    parser.add_argument("--mode-min-confidence", type=float, default=0.60)
    parser.add_argument("--normal-required", type=int, default=3)
    parser.add_argument("--mode-required", type=int, default=2)
    parser.add_argument("--stop-required", type=int, default=2)
    parser.add_argument("--servo-cooldown-ms", type=int, default=250)
    parser.add_argument("--drive-repeat-ms", type=int, default=200)
    parser.add_argument("--drive-hold-ms", type=int, default=550)
    parser.add_argument("--session-id")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--headless", action="store_true")
    parser.add_argument(
        "--skip-cloud-without-hand",
        action="store_true",
        help="Debug mode: do not call cloud when MediaPipe does not detect a hand.",
    )
    parser.add_argument("--max-frames", type=int, default=0)
    parser.add_argument("--log", type=Path, default=Path("reports/gateway_latency.csv"))
    return parser.parse_args()


if __name__ == "__main__":
    run_gateway(parse_args())
