from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Protocol

from common.protocol import Command


class CommandTransport(Protocol):
    def send(self, command: Command) -> float:
        """Send a command and return ESP32 acknowledgement latency in ms."""


@dataclass
class DryRunTransport:
    sent: list[dict] | None = None

    def __post_init__(self) -> None:
        if self.sent is None:
            self.sent = []

    def send(self, command: Command) -> float:
        assert self.sent is not None
        self.sent.append(command.to_payload())
        return 0.0


class WebSocketTransport:
    def __init__(self, url: str) -> None:
        import websocket

        self._ws = websocket.create_connection(url, timeout=1.5)

    def send(self, command: Command) -> float:
        import time

        start = time.perf_counter()
        self._ws.send(json.dumps(command.to_payload()))
        self._ws.recv()
        return (time.perf_counter() - start) * 1000
