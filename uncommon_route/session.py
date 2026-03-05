"""Session persistence store.

Tracks model selections per session to prevent model switching mid-task.
When a session is active, the router continues using the same model
instead of re-routing each request.

Includes three-strike escalation: if the same (failing) request is
retried 3+ times, the session auto-escalates to the next tier.
"""

from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class SessionEntry:
    model: str
    tier: str
    created_at: float
    last_used_at: float
    request_count: int = 1
    recent_hashes: list[str] = field(default_factory=list)
    strikes: int = 0
    escalated: bool = False


@dataclass
class SessionConfig:
    enabled: bool = True
    timeout_s: float = 30 * 60  # 30 minutes
    header_name: str = "x-session-id"


DEFAULT_SESSION_CONFIG = SessionConfig()


class SessionStore:
    """In-memory session store with timeout and three-strike escalation."""

    def __init__(self, config: SessionConfig | None = None) -> None:
        self._config = config or DEFAULT_SESSION_CONFIG
        self._sessions: dict[str, SessionEntry] = {}
        self._last_cleanup = time.monotonic()

    @property
    def config(self) -> SessionConfig:
        return self._config

    def get(self, session_id: str) -> SessionEntry | None:
        if not self._config.enabled or not session_id:
            return None
        entry = self._sessions.get(session_id)
        if entry is None:
            return None
        if time.monotonic() - entry.last_used_at > self._config.timeout_s:
            del self._sessions[session_id]
            return None
        return entry

    def set(self, session_id: str, model: str, tier: str) -> None:
        if not self._config.enabled or not session_id:
            return
        now = time.monotonic()
        existing = self._sessions.get(session_id)
        if existing:
            existing.last_used_at = now
            existing.request_count += 1
            if existing.model != model:
                existing.model = model
                existing.tier = tier
        else:
            self._sessions[session_id] = SessionEntry(
                model=model,
                tier=tier,
                created_at=now,
                last_used_at=now,
            )
        self._maybe_cleanup()

    def touch(self, session_id: str) -> None:
        if not self._config.enabled or not session_id:
            return
        entry = self._sessions.get(session_id)
        if entry:
            entry.last_used_at = time.monotonic()
            entry.request_count += 1

    def clear(self, session_id: str) -> None:
        self._sessions.pop(session_id, None)

    def clear_all(self) -> None:
        self._sessions.clear()

    def record_request_hash(self, session_id: str, content_hash: str) -> bool:
        """Record a request hash; returns True if escalation is warranted (3 consecutive identical hashes)."""
        entry = self._sessions.get(session_id)
        if entry is None:
            return False
        prev = entry.recent_hashes
        if prev and prev[-1] == content_hash:
            entry.strikes += 1
        else:
            entry.strikes = 0
        prev.append(content_hash)
        if len(prev) > 3:
            prev.pop(0)
        return entry.strikes >= 2 and not entry.escalated

    def escalate(
        self,
        session_id: str,
        tier_configs: dict[str, dict[str, Any]],
    ) -> tuple[str, str] | None:
        """Escalate session to the next tier. Returns (model, tier) or None if already at max.

        tier_configs maps tier name -> {"primary": str, "fallback": list[str]}.
        """
        entry = self._sessions.get(session_id)
        if entry is None:
            return None
        tier_order = ["SIMPLE", "MEDIUM", "COMPLEX", "REASONING"]
        try:
            idx = tier_order.index(entry.tier)
        except ValueError:
            return None
        if idx >= len(tier_order) - 1:
            return None
        next_tier = tier_order[idx + 1]
        next_cfg = tier_configs.get(next_tier)
        if not next_cfg:
            return None
        entry.model = next_cfg["primary"]
        entry.tier = next_tier
        entry.strikes = 0
        entry.escalated = True
        return entry.model, next_tier

    def stats(self) -> dict[str, Any]:
        now = time.monotonic()
        sessions = [
            {
                "id": sid[:8] + "...",
                "model": entry.model,
                "tier": entry.tier,
                "requests": entry.request_count,
                "age_s": round(now - entry.created_at),
            }
            for sid, entry in self._sessions.items()
        ]
        return {"count": len(self._sessions), "sessions": sessions}

    def _maybe_cleanup(self) -> None:
        now = time.monotonic()
        if now - self._last_cleanup < 300:
            return
        self._last_cleanup = now
        expired = [
            sid
            for sid, entry in self._sessions.items()
            if now - entry.last_used_at > self._config.timeout_s
        ]
        for sid in expired:
            del self._sessions[sid]


def get_session_id(
    headers: dict[str, str],
    header_name: str = DEFAULT_SESSION_CONFIG.header_name,
) -> str | None:
    """Extract session ID from request headers."""
    val = headers.get(header_name) or headers.get(header_name.lower())
    return val if val else None


def derive_session_id(messages: list[dict[str, Any]]) -> str | None:
    """Derive a session ID from the first user message (SHA-256 prefix)."""
    for msg in messages:
        if msg.get("role") == "user":
            content = msg.get("content", "")
            text = content if isinstance(content, str) else str(content)
            return hashlib.sha256(text.encode()).hexdigest()[:8]
    return None


def hash_request_content(content: str, tool_call_names: list[str] | None = None) -> str:
    """Hash the last user message + tool names for dedup / strike detection."""
    normalized = " ".join(content.split()).strip()[:500]
    suffix = f"|tools:{','.join(sorted(tool_call_names))}" if tool_call_names else ""
    return hashlib.sha256((normalized + suffix).encode()).hexdigest()[:12]
