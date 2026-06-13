from __future__ import annotations

import argparse
import csv
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

from common.protocol import GESTURES
from gateway.preprocess import MediaPipeCropper


METADATA_COLUMNS = (
    "file",
    "subject_id",
    "gesture",
    "clip_id",
    "frame_index",
    "timestamp_ms",
    "background",
    "lighting",
    "split",
    "found_hand",
)


@dataclass(frozen=True)
class CaptureConfig:
    subject_id: str
    labels: tuple[str, ...]
    clips_per_label: int
    duration_s: float
    fps: int
    camera: int
    output_dir: Path
    metadata_path: Path
    background: str
    lighting: str
    image_size: int
    jpeg_quality: int
    countdown_s: int
    auto_start: bool

    @property
    def frames_per_clip(self) -> int:
        return max(1, round(self.duration_s * self.fps))


def validate_labels(labels: Iterable[str]) -> tuple[str, ...]:
    normalized = tuple(label.strip().lower() for label in labels)
    unknown = sorted(set(normalized) - set(GESTURES))
    if unknown:
        raise ValueError(f"Unknown gesture labels: {', '.join(unknown)}")
    if not normalized:
        raise ValueError("At least one label is required")
    return normalized


def make_clip_id(label: str, clip_number: int, started_at: datetime | None = None) -> str:
    started_at = started_at or datetime.now()
    return f"{started_at:%Y%m%d_%H%M%S}_{label}_{clip_number:03d}"


def clip_dir(output_dir: Path, subject_id: str, label: str, clip_id: str) -> Path:
    return output_dir / subject_id / label / clip_id


def metadata_row(
    *,
    file_path: Path,
    subject_id: str,
    gesture: str,
    clip_id: str,
    frame_index: int,
    timestamp_ms: int,
    background: str,
    lighting: str,
    found_hand: bool,
    base_dir: Path | None = None,
) -> dict[str, str]:
    stored_path = file_path
    if base_dir is not None:
        try:
            stored_path = file_path.relative_to(base_dir)
        except ValueError:
            stored_path = file_path
    return {
        "file": stored_path.as_posix(),
        "subject_id": subject_id,
        "gesture": gesture,
        "clip_id": clip_id,
        "frame_index": str(frame_index),
        "timestamp_ms": str(timestamp_ms),
        "background": background,
        "lighting": lighting,
        "split": "",
        "found_hand": "1" if found_hand else "0",
    }


def append_metadata(metadata_path: Path, rows: Iterable[dict[str, str]]) -> int:
    rows = list(rows)
    if not rows:
        return 0
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    write_header = not metadata_path.exists() or metadata_path.stat().st_size == 0
    with metadata_path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=METADATA_COLUMNS)
        if write_header:
            writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def run_capture(config: CaptureConfig) -> None:
    import cv2

    config.output_dir.mkdir(parents=True, exist_ok=True)
    cropper = MediaPipeCropper()
    cap = cv2.VideoCapture(config.camera)
    if not cap.isOpened():
        raise RuntimeError(f"Khong mo duoc camera index {config.camera}")

    print("Nhan SPACE de quay clip, q de thoat.")
    print(f"Subject: {config.subject_id}")
    print(f"Labels: {', '.join(config.labels)}")
    print(f"Frames/clip: {config.frames_per_clip}, FPS: {config.fps}, duration: {config.duration_s}s")

    try:
        for label in config.labels:
            for clip_number in range(1, config.clips_per_label + 1):
                if not config.auto_start:
                    if not _wait_for_start(cap, label, clip_number, config.clips_per_label):
                        return
                if config.countdown_s > 0:
                    if not _countdown(cap, label, config.countdown_s):
                        return
                rows = _capture_clip(cap, cropper, config, label, clip_number)
                append_metadata(config.metadata_path, rows)
                print(f"Saved {len(rows)} frames for {label} clip {clip_number}/{config.clips_per_label}")
    finally:
        cap.release()
        cv2.destroyAllWindows()


def _wait_for_start(cap, label: str, clip_number: int, clips_per_label: int) -> bool:
    import cv2

    while True:
        ok, frame = cap.read()
        if not ok:
            return False
        _draw_overlay(
            frame,
            [
                f"label: {label}",
                f"clip: {clip_number}/{clips_per_label}",
                "SPACE: record",
                "q: quit",
            ],
        )
        cv2.imshow("IOT_CK Collect Data", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord(" "):
            return True
        if key == ord("q"):
            return False


def _countdown(cap, label: str, countdown_s: int) -> bool:
    import cv2

    for remaining in range(countdown_s, 0, -1):
        deadline = time.perf_counter() + 1.0
        while time.perf_counter() < deadline:
            ok, frame = cap.read()
            if not ok:
                return False
            _draw_overlay(frame, [f"label: {label}", f"recording in {remaining}"])
            cv2.imshow("IOT_CK Collect Data", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                return False
    return True


def _capture_clip(cap, cropper: MediaPipeCropper, config: CaptureConfig, label: str, clip_number: int) -> list[dict[str, str]]:
    import cv2

    started_at = datetime.now()
    clip_id = make_clip_id(label, clip_number, started_at)
    target_dir = clip_dir(config.output_dir, config.subject_id, label, clip_id)
    target_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, str]] = []
    frame_interval_s = 1.0 / max(1, config.fps)
    base_time = time.perf_counter()

    for frame_index in range(config.frames_per_clip):
        next_frame_at = base_time + frame_index * frame_interval_s
        while time.perf_counter() < next_frame_at:
            time.sleep(0.001)

        ok, frame = cap.read()
        if not ok:
            break
        crop = cropper.crop(frame)
        image = cv2.resize(crop.image, (config.image_size, config.image_size), interpolation=cv2.INTER_AREA)
        file_path = target_dir / f"frame_{frame_index:03d}.jpg"
        cv2.imwrite(str(file_path), image, [int(cv2.IMWRITE_JPEG_QUALITY), config.jpeg_quality])

        elapsed_ms = int((time.perf_counter() - base_time) * 1000)
        rows.append(
            metadata_row(
                file_path=file_path,
                subject_id=config.subject_id,
                gesture=label,
                clip_id=clip_id,
                frame_index=frame_index,
                timestamp_ms=elapsed_ms,
                background=config.background,
                lighting=config.lighting,
                found_hand=crop.found_hand,
                base_dir=Path.cwd(),
            )
        )

        display = frame.copy()
        _draw_overlay(display, [f"REC {label}", f"frame {frame_index + 1}/{config.frames_per_clip}"])
        cv2.imshow("IOT_CK Collect Data", display)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    return rows


def _draw_overlay(frame, lines: list[str]) -> None:
    import cv2

    for index, line in enumerate(lines):
        cv2.putText(frame, line, (20, 35 + index * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 255, 0), 2)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Collect gesture image clips for IOT_CK.")
    parser.add_argument("--subject", required=True, help="Subject id, for example s01.")
    parser.add_argument("--labels", nargs="+", default=list(GESTURES), help="Gesture labels to collect.")
    parser.add_argument("--clips-per-label", type=int, default=5)
    parser.add_argument("--duration-s", type=float, default=1.5)
    parser.add_argument("--fps", type=int, default=10)
    parser.add_argument("--camera", type=int, default=0)
    parser.add_argument("--output-dir", type=Path, default=Path("data/raw"))
    parser.add_argument("--metadata", type=Path, default=Path("data/metadata.csv"))
    parser.add_argument("--background", choices=("simple", "complex", "unknown"), default="unknown")
    parser.add_argument("--lighting", choices=("bright", "dim", "mixed", "unknown"), default="unknown")
    parser.add_argument("--image-size", type=int, default=160)
    parser.add_argument("--jpeg-quality", type=int, default=90)
    parser.add_argument("--countdown-s", type=int, default=3)
    parser.add_argument("--auto-start", action="store_true", help="Do not wait for SPACE before each clip.")
    return parser.parse_args()


def config_from_args(args: argparse.Namespace) -> CaptureConfig:
    return CaptureConfig(
        subject_id=args.subject.strip(),
        labels=validate_labels(args.labels),
        clips_per_label=args.clips_per_label,
        duration_s=args.duration_s,
        fps=args.fps,
        camera=args.camera,
        output_dir=args.output_dir,
        metadata_path=args.metadata,
        background=args.background,
        lighting=args.lighting,
        image_size=args.image_size,
        jpeg_quality=max(1, min(100, args.jpeg_quality)),
        countdown_s=max(0, args.countdown_s),
        auto_start=args.auto_start,
    )


def main() -> None:
    run_capture(config_from_args(parse_args()))


if __name__ == "__main__":
    main()
