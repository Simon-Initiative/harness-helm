from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class CapabilityRequirement:
    name: str
    required: bool
    evidence: list[str] = field(default_factory=list)


@dataclass(slots=True)
class CapabilitySummary:
    items: list[CapabilityRequirement] = field(default_factory=list)

    @property
    def required_names(self) -> list[str]:
        return [item.name for item in self.items if item.required]
