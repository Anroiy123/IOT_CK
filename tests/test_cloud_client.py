from __future__ import annotations

from gateway.cloud_client import CloudGestureClient


class FakeResponse:
    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict[str, object]:
        return {
            "gesture": "stop",
            "confidence": 0.95,
            "inference_ms": 12.5,
            "model_version": "test-v1",
            "model_type": "cnn",
            "session_id": "session-1",
            "request_id": "request-1",
        }


class FakeSession:
    def __init__(self) -> None:
        self.headers: dict[str, str] = {}
        self.calls: list[tuple[str, dict[str, object], float]] = []
        self.closed = False

    def post(self, url: str, *, json: dict[str, object], timeout: float) -> FakeResponse:
        self.calls.append((url, json, timeout))
        return FakeResponse()

    def close(self) -> None:
        self.closed = True


def test_cloud_client_reuses_injected_session() -> None:
    session = FakeSession()
    client = CloudGestureClient("https://example.test/", "secret", timeout_s=2.0, session=session)

    first = client.predict([b"jpeg"], session_id="session-1", request_id="request-1")
    second = client.predict([b"jpeg"], session_id="session-1", request_id="request-2")
    client.close()

    assert first.gesture == "stop"
    assert second.gesture == "stop"
    assert session.headers["X-API-Key"] == "secret"
    assert len(session.calls) == 2
    assert session.calls[0][0] == "https://example.test/v1/predict"
    assert session.calls[0][2] == 2.0
    assert session.closed is True
