from __future__ import annotations

from pathlib import Path

from helm.derive.work_item import build_work_item_snapshot
from helm.models import WorkItemSnapshot


def refresh_work_item(raw_path: str | Path) -> WorkItemSnapshot:
    return build_work_item_snapshot(raw_path)
