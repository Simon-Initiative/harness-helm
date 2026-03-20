from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class AcceptanceCriterion:
    key: str
    title: str
    status: str
    verification_method: str
    proofs: list[str] = field(default_factory=list)
    requirement_key: str | None = None


@dataclass(slots=True)
class RequirementItem:
    key: str
    title: str
    status: str
    validated_by: str
    acceptance_criteria: list[AcceptanceCriterion] = field(default_factory=list)


@dataclass(slots=True)
class RequirementsSummary:
    items: list[RequirementItem] = field(default_factory=list)
    acceptance_criteria: list[AcceptanceCriterion] = field(default_factory=list)

    @property
    def by_status(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for item in self.items:
            counts[item.status] = counts.get(item.status, 0) + 1
        return counts

    @property
    def acceptance_criteria_by_status(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for item in self.acceptance_criteria:
            counts[item.status] = counts.get(item.status, 0) + 1
        return counts
