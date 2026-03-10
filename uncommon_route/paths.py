from __future__ import annotations

import os
from pathlib import Path


def data_dir() -> Path:
    override = os.environ.get("UNCOMMON_ROUTE_DATA_DIR", "").strip()
    if override:
        return Path(override).expanduser()
    return Path.home() / ".uncommon-route"


def data_file(*parts: str) -> Path:
    return data_dir().joinpath(*parts)
