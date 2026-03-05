"""Shared fixtures for UncommonRoute tests."""

from __future__ import annotations

import pytest

from uncommon_route.session import SessionConfig, SessionStore
from uncommon_route.spend_control import InMemorySpendControlStorage, SpendControl


@pytest.fixture
def session_store() -> SessionStore:
    return SessionStore(SessionConfig(enabled=True, timeout_s=60, header_name="x-session-id"))


@pytest.fixture
def spend_control() -> SpendControl:
    return SpendControl(storage=InMemorySpendControlStorage())
