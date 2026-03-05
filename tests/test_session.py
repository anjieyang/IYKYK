"""Tests for session persistence store."""

from __future__ import annotations

import time

import pytest

from uncommon_route.session import (
    SessionConfig,
    SessionStore,
    derive_session_id,
    get_session_id,
    hash_request_content,
)


class TestSessionStore:
    def test_set_and_get(self, session_store: SessionStore) -> None:
        session_store.set("s1", "moonshot/kimi-k2.5", "SIMPLE")
        entry = session_store.get("s1")
        assert entry is not None
        assert entry.model == "moonshot/kimi-k2.5"
        assert entry.tier == "SIMPLE"
        assert entry.request_count == 1

    def test_get_missing_returns_none(self, session_store: SessionStore) -> None:
        assert session_store.get("nonexistent") is None

    def test_touch_increments_count(self, session_store: SessionStore) -> None:
        session_store.set("s1", "deepseek/deepseek-chat", "MEDIUM")
        session_store.touch("s1")
        session_store.touch("s1")
        entry = session_store.get("s1")
        assert entry is not None
        assert entry.request_count == 3

    def test_clear_removes_session(self, session_store: SessionStore) -> None:
        session_store.set("s1", "model-a", "SIMPLE")
        session_store.clear("s1")
        assert session_store.get("s1") is None

    def test_clear_all(self, session_store: SessionStore) -> None:
        session_store.set("s1", "model-a", "SIMPLE")
        session_store.set("s2", "model-b", "MEDIUM")
        session_store.clear_all()
        assert session_store.get("s1") is None
        assert session_store.get("s2") is None

    def test_timeout_expires_session(self) -> None:
        store = SessionStore(SessionConfig(enabled=True, timeout_s=0.01))
        store.set("s1", "model-a", "SIMPLE")
        time.sleep(0.02)
        assert store.get("s1") is None

    def test_disabled_store_is_noop(self) -> None:
        store = SessionStore(SessionConfig(enabled=False))
        store.set("s1", "model-a", "SIMPLE")
        assert store.get("s1") is None

    def test_update_model_on_existing_session(self, session_store: SessionStore) -> None:
        session_store.set("s1", "model-a", "SIMPLE")
        session_store.set("s1", "model-b", "MEDIUM")
        entry = session_store.get("s1")
        assert entry is not None
        assert entry.model == "model-b"
        assert entry.tier == "MEDIUM"
        assert entry.request_count == 2

    def test_stats(self, session_store: SessionStore) -> None:
        session_store.set("s1", "model-a", "SIMPLE")
        session_store.set("s2", "model-b", "COMPLEX")
        stats = session_store.stats()
        assert stats["count"] == 2
        assert len(stats["sessions"]) == 2


class TestThreeStrikeEscalation:
    def test_no_escalation_on_different_hashes(self, session_store: SessionStore) -> None:
        session_store.set("s1", "model-a", "SIMPLE")
        assert session_store.record_request_hash("s1", "hash-a") is False
        assert session_store.record_request_hash("s1", "hash-b") is False
        assert session_store.record_request_hash("s1", "hash-c") is False

    def test_escalation_on_three_identical_hashes(self, session_store: SessionStore) -> None:
        session_store.set("s1", "model-a", "SIMPLE")
        assert session_store.record_request_hash("s1", "same") is False
        assert session_store.record_request_hash("s1", "same") is False
        assert session_store.record_request_hash("s1", "same") is True

    def test_escalate_bumps_tier(self, session_store: SessionStore) -> None:
        session_store.set("s1", "model-a", "SIMPLE")
        tier_configs = {
            "SIMPLE": {"primary": "model-a", "fallback": []},
            "MEDIUM": {"primary": "model-b", "fallback": []},
            "COMPLEX": {"primary": "model-c", "fallback": []},
            "REASONING": {"primary": "model-d", "fallback": []},
        }
        result = session_store.escalate("s1", tier_configs)
        assert result is not None
        model, tier = result
        assert model == "model-b"
        assert tier == "MEDIUM"

    def test_escalate_at_max_tier_returns_none(self, session_store: SessionStore) -> None:
        session_store.set("s1", "model-d", "REASONING")
        tier_configs = {"REASONING": {"primary": "model-d", "fallback": []}}
        assert session_store.escalate("s1", tier_configs) is None

    def test_no_double_escalation(self, session_store: SessionStore) -> None:
        session_store.set("s1", "model-a", "SIMPLE")
        for _ in range(3):
            session_store.record_request_hash("s1", "same")
        tier_configs = {
            "SIMPLE": {"primary": "model-a", "fallback": []},
            "MEDIUM": {"primary": "model-b", "fallback": []},
        }
        session_store.escalate("s1", tier_configs)
        # After escalation, further identical hashes should NOT trigger again
        assert session_store.record_request_hash("s1", "same") is False


class TestHelpers:
    def test_get_session_id_from_headers(self) -> None:
        assert get_session_id({"x-session-id": "abc123"}) == "abc123"

    def test_get_session_id_missing(self) -> None:
        assert get_session_id({}) is None

    def test_get_session_id_empty(self) -> None:
        assert get_session_id({"x-session-id": ""}) is None

    def test_derive_session_id(self) -> None:
        messages = [
            {"role": "system", "content": "you are helpful"},
            {"role": "user", "content": "hello world"},
        ]
        sid = derive_session_id(messages)
        assert sid is not None
        assert len(sid) == 8

    def test_derive_session_id_no_user(self) -> None:
        messages = [{"role": "system", "content": "you are helpful"}]
        assert derive_session_id(messages) is None

    def test_derive_session_id_deterministic(self) -> None:
        messages = [{"role": "user", "content": "test prompt"}]
        assert derive_session_id(messages) == derive_session_id(messages)

    def test_hash_request_content(self) -> None:
        h1 = hash_request_content("hello world")
        h2 = hash_request_content("hello world")
        h3 = hash_request_content("different prompt")
        assert h1 == h2
        assert h1 != h3
        assert len(h1) == 12

    def test_hash_with_tool_names(self) -> None:
        h1 = hash_request_content("hello", ["tool_a", "tool_b"])
        h2 = hash_request_content("hello", ["tool_b", "tool_a"])
        h3 = hash_request_content("hello")
        assert h1 == h2  # sorted
        assert h1 != h3
