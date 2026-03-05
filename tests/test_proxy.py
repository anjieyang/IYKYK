"""Integration tests for the proxy server with session + spend control."""

from __future__ import annotations

import json

import pytest
from starlette.testclient import TestClient

from uncommon_route.proxy import create_app
from uncommon_route.session import SessionConfig, SessionStore
from uncommon_route.spend_control import InMemorySpendControlStorage, SpendControl


@pytest.fixture
def client() -> TestClient:
    """Test client with in-memory session + spend control (no real upstream)."""
    session_store = SessionStore(SessionConfig(enabled=True, timeout_s=300))
    spend_control = SpendControl(storage=InMemorySpendControlStorage())
    app = create_app(
        upstream="http://127.0.0.1:1/fake",
        session_store=session_store,
        spend_control=spend_control,
    )
    return TestClient(app, raise_server_exceptions=False)


class TestHealthEndpoint:
    def test_health_returns_ok(self, client: TestClient) -> None:
        resp = client.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert data["router"] == "uncommon-route"

    def test_health_includes_sessions(self, client: TestClient) -> None:
        data = client.get("/health").json()
        assert "sessions" in data
        assert data["sessions"]["count"] == 0

    def test_health_includes_spending(self, client: TestClient) -> None:
        data = client.get("/health").json()
        assert "spending" in data
        assert "calls" in data["spending"]


class TestModelsEndpoint:
    def test_models_list(self, client: TestClient) -> None:
        resp = client.get("/v1/models")
        assert resp.status_code == 200
        data = resp.json()
        assert data["object"] == "list"
        model_ids = [m["id"] for m in data["data"]]
        assert "uncommon-route/auto" in model_ids


class TestChatCompletions:
    def test_virtual_model_routes(self, client: TestClient) -> None:
        resp = client.post("/v1/chat/completions", json={
            "model": "uncommon-route/auto",
            "messages": [{"role": "user", "content": "/debug what is 2+2"}],
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["model"] == "uncommon-route/debug"
        assert "UncommonRoute Debug" in data["choices"][0]["message"]["content"]

    def test_routing_headers_present(self, client: TestClient) -> None:
        """Non-debug requests forward to upstream; headers are set even if upstream fails."""
        resp = client.post("/v1/chat/completions", json={
            "model": "uncommon-route/auto",
            "messages": [{"role": "user", "content": "hello"}],
        })
        # Upstream is fake so we get 502, but routing headers should still be present
        assert resp.status_code == 502
        assert "x-uncommon-route-model" in resp.headers
        assert "x-uncommon-route-tier" in resp.headers

    def test_passthrough_no_routing_headers(self, client: TestClient) -> None:
        resp = client.post("/v1/chat/completions", json={
            "model": "some-other/model",
            "messages": [{"role": "user", "content": "hello"}],
        })
        # Upstream is fake, expect 502
        assert resp.status_code == 502
        assert "x-uncommon-route-model" not in resp.headers


class TestSpendEndpoint:
    def test_get_spend_status(self, client: TestClient) -> None:
        resp = client.get("/v1/spend")
        assert resp.status_code == 200
        data = resp.json()
        assert "limits" in data
        assert "calls" in data

    def test_set_and_get_limit(self, client: TestClient) -> None:
        resp = client.post("/v1/spend", json={
            "action": "set", "window": "hourly", "amount": 5.00,
        })
        assert resp.status_code == 200
        assert resp.json()["ok"] is True

        data = client.get("/v1/spend").json()
        assert data["limits"]["hourly"] == 5.00

    def test_clear_limit(self, client: TestClient) -> None:
        client.post("/v1/spend", json={"action": "set", "window": "daily", "amount": 10})
        client.post("/v1/spend", json={"action": "clear", "window": "daily"})
        data = client.get("/v1/spend").json()
        assert "daily" not in data["limits"]

    def test_reset_session(self, client: TestClient) -> None:
        resp = client.post("/v1/spend", json={"action": "reset_session"})
        assert resp.status_code == 200
        assert resp.json()["session_reset"] is True

    def test_invalid_action(self, client: TestClient) -> None:
        resp = client.post("/v1/spend", json={"action": "explode"})
        assert resp.status_code == 400


class TestSessionsEndpoint:
    def test_sessions_empty(self, client: TestClient) -> None:
        resp = client.get("/v1/sessions")
        assert resp.status_code == 200
        assert resp.json()["count"] == 0


class TestSpendControlIntegration:
    def test_spend_limit_blocks_request(self) -> None:
        """When spend limit is exhausted, chat completions returns 429."""
        session_store = SessionStore()
        sc = SpendControl(storage=InMemorySpendControlStorage())
        sc.set_limit("per_request", 0.0001)

        app = create_app(
            upstream="http://127.0.0.1:1/fake",
            session_store=session_store,
            spend_control=sc,
        )
        client = TestClient(app, raise_server_exceptions=False)

        resp = client.post("/v1/chat/completions", json={
            "model": "uncommon-route/auto",
            "messages": [{"role": "user", "content": "hello"}],
        })
        assert resp.status_code == 429
        assert "spend_limit_exceeded" in resp.json()["error"]["type"]
