from __future__ import annotations

import re

from helm.models import PlanPhase, PlanSummary


HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
CHECKED_PATTERN = re.compile(r"^\s*[-*]\s+\[[xX]\]\s+")
UNCHECKED_PATTERN = re.compile(r"^\s*[-*]\s+\[\s\]\s+")
EXECUTION_HEADING_PATTERN = re.compile(r"^(Phase|Lane)\s+\d+\s*:", re.IGNORECASE)


def parse_plan_document(markdown_text: str) -> PlanSummary:
    phases: list[PlanPhase] = []
    current_phase: PlanPhase | None = None

    for line_number, raw_line in enumerate(markdown_text.splitlines(), start=1):
        line = raw_line.rstrip()
        match = HEADING_PATTERN.match(line.strip())
        if match:
            title = match.group(2).strip()
            if is_execution_heading(title):
                current_phase = PlanPhase(
                    title=title,
                    level=len(match.group(1)),
                    line_number=line_number,
                    kind=execution_kind(title),
                )
                phases.append(current_phase)
            else:
                current_phase = None
            continue

        if current_phase is None:
            continue

        if CHECKED_PATTERN.match(line):
            current_phase.checked_items += 1
        elif UNCHECKED_PATTERN.match(line):
            current_phase.unchecked_items += 1

    for phase in phases:
        phase.state = derive_phase_state(phase.checked_items, phase.unchecked_items)

    return PlanSummary(phases=phases)


def is_execution_heading(title: str) -> bool:
    return bool(EXECUTION_HEADING_PATTERN.match(title))


def execution_kind(title: str) -> str:
    if title.lower().startswith("lane "):
        return "lane"
    return "phase"


def derive_phase_state(checked_items: int, unchecked_items: int) -> str:
    total_items = checked_items + unchecked_items
    if total_items == 0:
        return "unknown"
    if unchecked_items == 0:
        return "completed"
    if checked_items == 0:
        return "not started"
    return "in progress"
