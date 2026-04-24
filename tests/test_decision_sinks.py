"""Tests for uncommon_route.decision_sinks + the RouteStats wiring."""

from __future__ import annotations

import json
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any

import pytest

from uncommon_route.decision_sinks import (
    DecisionSink,
    NDJSONDecisionSink,
    WebhookDecisionSink,
    sinks_from_env,
)
from uncommon_route.stats import (
    InMemoryRouteStatsStorage,
    RouteRecord,
    RouteStats,
)


def _rec(**overrides: Any) -> RouteRecord:
    defaults: dict[str, Any] = dict(
        timestamp=time.time(),
        model="claude-sonnet-4-6",
        tier="medium",
        confidence=0.8,
        method="pool",
        estimated_cost=0.01,
        request_id="req-abc",
    )
    defaults.update(overrides)
    return RouteRecord(**defaults)


class _Capture(DecisionSink):
    def __init__(self) -> None:
        self.seen: list[RouteRecord] = []

    def emit(self, record: RouteRecord) -> None:
        self.seen.append(record)


class _Boom(DecisionSink):
    def emit(self, record: RouteRecord) -> None:
        raise RuntimeError("sink on fire")


class TestNDJSONDecisionSink:
    def test_appends_one_json_line_per_emit(self, tmp_path: Path) -> None:
        path = tmp_path / "nested" / "decisions.ndjson"
        sink = NDJSONDecisionSink(path)

        sink.emit(_rec(request_id="a"))
        sink.emit(_rec(request_id="b", tier="hard"))

        lines = path.read_text().splitlines()
        assert len(lines) == 2
        parsed = [json.loads(line) for line in lines]
        assert parsed[0]["request_id"] == "a"
        assert parsed[1]["request_id"] == "b"
        assert parsed[1]["tier"] == "hard"
        # all RouteRecord fields should be present
        assert "cache_read_input_tokens" in parsed[0]

    def test_concurrent_emit_does_not_interleave_lines(self, tmp_path: Path) -> None:
        path = tmp_path / "decisions.ndjson"
        sink = NDJSONDecisionSink(path)

        def burst(tag: str) -> None:
            for i in range(25):
                sink.emit(_rec(request_id=f"{tag}-{i}"))

        threads = [threading.Thread(target=burst, args=(str(i),)) for i in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        lines = path.read_text().splitlines()
        assert len(lines) == 100
        # every line must parse — no torn writes
        for line in lines:
            json.loads(line)


class TestWebhookDecisionSink:
    def test_posts_json_body_to_url(self) -> None:
        received: list[dict[str, Any]] = []
        ready = threading.Event()

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args: Any, **kwargs: Any) -> None:
                pass

            def do_POST(self) -> None:  # noqa: N802
                length = int(self.headers.get("Content-Length", "0"))
                body = self.rfile.read(length).decode("utf-8")
                received.append(json.loads(body))
                self.send_response(204)
                self.end_headers()
                ready.set()

        server = HTTPServer(("127.0.0.1", 0), Handler)
        host, port = server.server_address
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            sink = WebhookDecisionSink(f"http://{host}:{port}/hook", timeout=2.0)
            sink.emit(_rec(request_id="wh-1"))
            assert ready.wait(timeout=3.0), "webhook never received POST"
        finally:
            server.shutdown()
            server.server_close()

        assert received and received[0]["request_id"] == "wh-1"

    def test_swallows_connection_errors(self, caplog: pytest.LogCaptureFixture) -> None:
        # nothing is listening on this port — emit must not raise
        sink = WebhookDecisionSink("http://127.0.0.1:1/never", timeout=0.2)
        sink.emit(_rec(request_id="wh-fail"))
        # give the daemon thread a moment
        for _ in range(20):
            if any("WebhookDecisionSink" in r.message for r in caplog.records):
                break
            time.sleep(0.05)


class TestSinksFromEnv:
    def test_returns_empty_by_default(self) -> None:
        assert sinks_from_env({}) == []

    def test_builds_ndjson_sink(self, tmp_path: Path) -> None:
        env = {"UNCOMMON_ROUTE_DECISION_LOG": str(tmp_path / "d.ndjson")}
        sinks = sinks_from_env(env)
        assert len(sinks) == 1
        assert isinstance(sinks[0], NDJSONDecisionSink)

    def test_builds_webhook_sink_with_custom_timeout(self) -> None:
        env = {
            "UNCOMMON_ROUTE_DECISION_WEBHOOK": "https://example.invalid/hook",
            "UNCOMMON_ROUTE_DECISION_WEBHOOK_TIMEOUT": "2.5",
        }
        sinks = sinks_from_env(env)
        assert len(sinks) == 1
        assert isinstance(sinks[0], WebhookDecisionSink)
        assert sinks[0]._timeout == pytest.approx(2.5)

    def test_builds_both_when_both_set(self, tmp_path: Path) -> None:
        env = {
            "UNCOMMON_ROUTE_DECISION_LOG": str(tmp_path / "d.ndjson"),
            "UNCOMMON_ROUTE_DECISION_WEBHOOK": "https://example.invalid/hook",
        }
        sinks = sinks_from_env(env)
        assert [type(s).__name__ for s in sinks] == [
            "NDJSONDecisionSink",
            "WebhookDecisionSink",
        ]


class TestRouteStatsWiring:
    def test_record_emits_to_each_sink(self) -> None:
        cap = _Capture()
        rs = RouteStats(storage=InMemoryRouteStatsStorage(), sinks=[cap])

        rs.record(_rec(request_id="r1"))
        rs.record(_rec(request_id="r2", tier="hard"))

        assert [r.request_id for r in cap.seen] == ["r1", "r2"]
        # tier normalisation happens before emit
        assert cap.seen[1].tier == "HARD"

    def test_record_feedback_emits_updated_record(self) -> None:
        cap = _Capture()
        rs = RouteStats(storage=InMemoryRouteStatsStorage(), sinks=[cap])
        rs.record(_rec(request_id="req-1"))

        ok = rs.record_feedback(
            "req-1",
            signal="explicit",
            ok=False,
            action="downgrade",
            from_tier="hard",
            to_tier="medium",
            reason="overkill",
        )

        assert ok
        # two emits: the initial record and the feedback update
        assert len(cap.seen) == 2
        fb = cap.seen[1]
        assert fb.feedback_signal == "explicit"
        assert fb.feedback_action == "downgrade"
        assert fb.feedback_ok is False

    def test_one_broken_sink_does_not_break_others(self) -> None:
        cap = _Capture()
        rs = RouteStats(
            storage=InMemoryRouteStatsStorage(),
            sinks=[_Boom(), cap],
        )

        rs.record(_rec(request_id="resilient"))

        assert [r.request_id for r in cap.seen] == ["resilient"]

    def test_default_sinks_come_from_env(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        log_path = tmp_path / "auto.ndjson"
        monkeypatch.setenv("UNCOMMON_ROUTE_DECISION_LOG", str(log_path))

        rs = RouteStats(storage=InMemoryRouteStatsStorage())
        rs.record(_rec(request_id="from-env"))

        lines = log_path.read_text().splitlines()
        assert len(lines) == 1
        parsed = json.loads(lines[0])
        assert parsed["request_id"] == "from-env"

    def test_explicit_empty_sinks_overrides_env(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        log_path = tmp_path / "should-not-exist.ndjson"
        monkeypatch.setenv("UNCOMMON_ROUTE_DECISION_LOG", str(log_path))

        rs = RouteStats(storage=InMemoryRouteStatsStorage(), sinks=[])
        rs.record(_rec(request_id="silent"))

        assert not log_path.exists()
