from __future__ import annotations

from pathlib import Path

from helm.derive.work_item import build_work_item_snapshot
from helm.models import PlanPhase, WorkItemSnapshot
from helm.parsers.plan import parse_plan_document
from helm.readers.files import resolve_work_item_dir


def load_work_item(raw_path: str | Path) -> WorkItemSnapshot:
    return build_work_item_snapshot(raw_path)


def parse_plan_phases(markdown_text: str) -> list[PlanPhase]:
    return parse_plan_document(markdown_text).phases
