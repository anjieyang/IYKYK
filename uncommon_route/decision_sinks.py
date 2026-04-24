"""Decision sinks — stream every RouteRecord to external consumers.

Stats are persisted to a rolling JSON file in `stats.py`. That's a store,
not a stream — a loop that wants to evaluate routing decisions in near
real-time has to diff the file on every tick, and anything older than
the retention window disappears.

Decision sinks fix that. Each time `RouteStats.record()` or
`record_feedback()` commits a record, every configured sink receives it
with zero further buffering. Downstream consumers (autoresearch loops,
dashboards, webhooks) consume the stream instead of polling storage.

Sinks are intentionally best-effort: failures are logged and swallowed.
Routing correctness does not depend on the stream landing.
"""

from __future__ import annotations

import json
import logging
import os
import threading
from abc import ABC, abstractmethod
from dataclasses import asdict
from pathlib import Path
from typing import TYPE_CHECKING, Any
from urllib import error as _urlerror
from urllib import request as _urlrequest

if TYPE_CHECKING:
    from uncommon_route.stats import RouteRecord

logger = logging.getLogger(__name__)


_ENV_NDJSON_PATH = "UNCOMMON_ROUTE_DECISION_LOG"
_ENV_WEBHOOK_URL = "UNCOMMON_ROUTE_DECISION_WEBHOOK"
_ENV_WEBHOOK_TIMEOUT = "UNCOMMON_ROUTE_DECISION_WEBHOOK_TIMEOUT"


class DecisionSink(ABC):
    """Receives each RouteRecord the moment it is committed."""

    @abstractmethod
    def emit(self, record: RouteRecord) -> None: ...


def _record_to_dict(record: RouteRecord) -> dict[str, Any]:
    return asdict(record)


class NDJSONDecisionSink(DecisionSink):
    """Append-only NDJSON file — one record per line, flushed on write.

    Safe under concurrent `emit` calls: writes are serialised by a lock.
    Parent directory is created on first write with mode 0700; the file
    itself uses 0600 to match the adjacent `stats.json` permissions.
    """

    def __init__(self, path: str | os.PathLike[str]) -> None:
        self._path = Path(path)
        self._lock = threading.Lock()

    def emit(self, record: RouteRecord) -> None:
        line = json.dumps(_record_to_dict(record), default=str, sort_keys=True)
        try:
            with self._lock:
                self._path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
                new_file = not self._path.exists()
                with self._path.open("a", encoding="utf-8") as fh:
                    fh.write(line + "\n")
                if new_file:
                    try:
                        self._path.chmod(0o600)
                    except OSError:
                        pass
        except OSError as exc:
            logger.warning("NDJSONDecisionSink write failed: %s", exc)


class WebhookDecisionSink(DecisionSink):
    """Fire-and-forget POST of each record to `url` as JSON.

    Each emit spawns a daemon thread so routing latency is untouched by
    slow endpoints. Failures are logged and never raised. A short
    timeout (default 1.0s) guards against hung receivers.
    """

    def __init__(self, url: str, timeout: float = 1.0) -> None:
        self._url = url
        self._timeout = max(0.1, timeout)

    def emit(self, record: RouteRecord) -> None:
        payload = json.dumps(_record_to_dict(record), default=str).encode("utf-8")
        threading.Thread(
            target=self._post,
            args=(payload,),
            daemon=True,
            name="uncommon-route-webhook",
        ).start()

    def _post(self, payload: bytes) -> None:
        req = _urlrequest.Request(
            self._url,
            data=payload,
            headers={"Content-Type": "application/json", "User-Agent": "uncommon-route/decision-sink"},
            method="POST",
        )
        try:
            with _urlrequest.urlopen(req, timeout=self._timeout):
                pass
        except (_urlerror.URLError, TimeoutError, OSError) as exc:
            logger.warning("WebhookDecisionSink POST failed: %s", exc)


def sinks_from_env(env: dict[str, str] | None = None) -> list[DecisionSink]:
    """Build sinks from environment variables.

    - `UNCOMMON_ROUTE_DECISION_LOG`       → NDJSONDecisionSink(path)
    - `UNCOMMON_ROUTE_DECISION_WEBHOOK`   → WebhookDecisionSink(url)
    - `UNCOMMON_ROUTE_DECISION_WEBHOOK_TIMEOUT` → float seconds (default 1.0)

    Returns an empty list when none are set — preserving the existing
    "no stream, no side effects" default.
    """
    src = env if env is not None else os.environ
    sinks: list[DecisionSink] = []

    path = (src.get(_ENV_NDJSON_PATH) or "").strip()
    if path:
        sinks.append(NDJSONDecisionSink(path))

    url = (src.get(_ENV_WEBHOOK_URL) or "").strip()
    if url:
        timeout_raw = (src.get(_ENV_WEBHOOK_TIMEOUT) or "").strip()
        try:
            timeout = float(timeout_raw) if timeout_raw else 1.0
        except ValueError:
            timeout = 1.0
        sinks.append(WebhookDecisionSink(url, timeout=timeout))

    return sinks
