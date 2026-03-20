from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class PlanPhase:
    title: str
    level: int
    line_number: int
    kind: str = "phase"
    checked_items: int = 0
    unchecked_items: int = 0
    state: str = "unknown"

    @property
    def checklist_item_count(self) -> int:
        return self.checked_items + self.unchecked_items

    @property
    def has_checklist(self) -> bool:
        return self.checklist_item_count > 0

    @property
    def is_complete(self) -> bool:
        return self.has_checklist and self.unchecked_items == 0


@dataclass(slots=True)
class PlanSummary:
    phases: list[PlanPhase] = field(default_factory=list)

    @property
    def phase_count(self) -> int:
        return len(self.phases)
