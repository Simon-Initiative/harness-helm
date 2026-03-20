from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from helm.models.work_item import WorkItemSnapshot


@dataclass(slots=True)
class FileState:
    name: str
    path: Path
    exists: bool
    modified_label: str
    status: str


@dataclass(slots=True)
class PhaseState:
    title: str
    state: str
    is_complete: bool
    checked_items: int
    unchecked_items: int


@dataclass(slots=True)
class OverviewStats:
    file_states: list[FileState] = field(default_factory=list)
    requirement_total: int = 0
    acceptance_criteria_total: int = 0
    requirement_status_counts: dict[str, int] = field(default_factory=dict)
    acceptance_status_counts: dict[str, int] = field(default_factory=dict)
    phase_count: int = 0
    completed_phase_count: int = 0
    phase_states: list[PhaseState] = field(default_factory=list)
    feature_facts: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass(slots=True)
class FeatureState:
    snapshot: WorkItemSnapshot
    selected_view: str
    status_message: str
    overview: OverviewStats

    @property
    def feature_slug(self) -> str:
        return self.snapshot.feature_slug

    @property
    def root_path(self) -> Path:
        return self.snapshot.root_path
