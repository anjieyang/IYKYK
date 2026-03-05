"""Tests for spend control."""

from __future__ import annotations

import pytest

from uncommon_route.spend_control import (
    InMemorySpendControlStorage,
    SpendControl,
    format_duration,
)


class TestSpendControl:
    def test_no_limits_allows_everything(self, spend_control: SpendControl) -> None:
        result = spend_control.check(100.0)
        assert result.allowed is True

    def test_per_request_limit(self, spend_control: SpendControl) -> None:
        spend_control.set_limit("per_request", 0.10)
        assert spend_control.check(0.05).allowed is True
        assert spend_control.check(0.15).allowed is False

        blocked = spend_control.check(0.15)
        assert blocked.blocked_by == "per_request"
        assert "Per-request limit" in (blocked.reason or "")

    def test_session_limit(self, spend_control: SpendControl) -> None:
        spend_control.set_limit("session", 1.00)
        assert spend_control.check(0.30).allowed is True

        spend_control.record(0.30, model="model-a")
        spend_control.record(0.30, model="model-a")
        spend_control.record(0.30, model="model-a")
        # spent 0.90, remaining 0.10
        assert spend_control.check(0.05).allowed is True
        assert spend_control.check(0.15).allowed is False

        blocked = spend_control.check(0.15)
        assert blocked.blocked_by == "session"

    def test_hourly_limit(self) -> None:
        clock = _FakeClock(1000.0)
        sc = SpendControl(storage=InMemorySpendControlStorage(), now_fn=clock)
        sc.set_limit("hourly", 2.00)

        sc.record(1.50, model="model-a")
        assert sc.check(0.40).allowed is True
        assert sc.check(0.60).allowed is False

        # Advance 1 hour → window resets
        clock.advance(3601)
        assert sc.check(2.00).allowed is True

    def test_daily_limit(self) -> None:
        clock = _FakeClock(1000.0)
        sc = SpendControl(storage=InMemorySpendControlStorage(), now_fn=clock)
        sc.set_limit("daily", 10.00)

        sc.record(9.50)
        assert sc.check(0.40).allowed is True
        assert sc.check(0.60).allowed is False

        # Advance 24h
        clock.advance(86401)
        assert sc.check(10.00).allowed is True

    def test_clear_limit(self, spend_control: SpendControl) -> None:
        spend_control.set_limit("per_request", 0.01)
        assert spend_control.check(0.05).allowed is False

        spend_control.clear_limit("per_request")
        assert spend_control.check(0.05).allowed is True

    def test_set_invalid_limit_raises(self, spend_control: SpendControl) -> None:
        with pytest.raises(ValueError):
            spend_control.set_limit("hourly", -1.0)
        with pytest.raises(ValueError):
            spend_control.set_limit("hourly", 0)

    def test_record_negative_raises(self, spend_control: SpendControl) -> None:
        with pytest.raises(ValueError):
            spend_control.record(-0.01)

    def test_status(self, spend_control: SpendControl) -> None:
        spend_control.set_limit("hourly", 5.00)
        spend_control.record(1.00, model="model-a")
        spend_control.record(0.50, model="model-b")

        s = spend_control.status()
        assert s.limits.hourly == 5.00
        assert s.spent["session"] == pytest.approx(1.50)
        assert s.remaining["hourly"] == pytest.approx(3.50)
        assert s.calls == 2

    def test_history(self, spend_control: SpendControl) -> None:
        spend_control.record(0.10, model="a")
        spend_control.record(0.20, model="b")
        spend_control.record(0.30, model="c")

        records = spend_control.history(limit=2)
        assert len(records) == 2
        assert records[0].model == "c"  # most recent first
        assert records[1].model == "b"

    def test_reset_session(self, spend_control: SpendControl) -> None:
        spend_control.set_limit("session", 1.00)
        spend_control.record(0.80)
        assert spend_control.check(0.30).allowed is False

        spend_control.reset_session()
        assert spend_control.check(0.30).allowed is True

    def test_get_spending_and_remaining(self) -> None:
        clock = _FakeClock(1000.0)
        sc = SpendControl(storage=InMemorySpendControlStorage(), now_fn=clock)
        sc.set_limit("hourly", 5.00)
        sc.set_limit("daily", 20.00)

        sc.record(2.00)
        assert sc.get_spending("hourly") == pytest.approx(2.00)
        assert sc.get_spending("daily") == pytest.approx(2.00)
        assert sc.get_spending("session") == pytest.approx(2.00)
        assert sc.get_remaining("hourly") == pytest.approx(3.00)
        assert sc.get_remaining("daily") == pytest.approx(18.00)

    def test_remaining_none_when_no_limit(self, spend_control: SpendControl) -> None:
        assert spend_control.get_remaining("hourly") is None
        assert spend_control.get_remaining("daily") is None
        assert spend_control.get_remaining("session") is None


class TestPersistence:
    def test_save_and_reload(self) -> None:
        storage = InMemorySpendControlStorage()
        sc1 = SpendControl(storage=storage)
        sc1.set_limit("hourly", 3.00)
        sc1.record(1.00, model="test-model")

        sc2 = SpendControl(storage=storage)
        assert sc2.limits.hourly == 3.00
        records = sc2.history()
        assert len(records) == 1
        assert records[0].model == "test-model"


class TestFormatDuration:
    def test_seconds(self) -> None:
        assert format_duration(30) == "30s"

    def test_minutes(self) -> None:
        assert format_duration(90) == "2 min"

    def test_hours(self) -> None:
        assert format_duration(7200) == "2h"

    def test_hours_and_minutes(self) -> None:
        assert format_duration(3660) == "1h 1m"


class _FakeClock:
    """Deterministic clock for testing time-windowed logic."""

    def __init__(self, start: float) -> None:
        self._now = start

    def __call__(self) -> float:
        return self._now

    def advance(self, seconds: float) -> None:
        self._now += seconds
