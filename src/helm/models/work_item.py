from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from helm.models.capabilities import CapabilitySummary
from helm.models.documents import DocumentSnapshot
from helm.models.plan import PlanSummary
from helm.models.requirements import RequirementsSummary


@dataclass(slots=True)
class WorkItemSnapshot:
    root_path: Path
    feature_slug: str
    documents: dict[str, DocumentSnapshot]
    plan: PlanSummary
    requirements: RequirementsSummary
    capabilities: CapabilitySummary
    errors: list[str] = field(default_factory=list)

    @property
    def source_paths(self) -> list[Path]:
        return [document.path for document in self.documents.values()]
