from __future__ import annotations

from datetime import datetime

from helm.models import FeatureState, FileState, OverviewStats, PhaseState, WorkItemSnapshot
from helm.ui.state import UIState


def build_feature_state(snapshot: WorkItemSnapshot, ui: UIState) -> FeatureState:
    overview = OverviewStats(
        file_states=build_file_states(snapshot),
        requirement_total=len(snapshot.requirements.items),
        acceptance_criteria_total=len(snapshot.requirements.acceptance_criteria),
        requirement_status_counts=snapshot.requirements.by_status,
        acceptance_status_counts=snapshot.requirements.acceptance_criteria_by_status,
        phase_count=snapshot.plan.phase_count,
        completed_phase_count=sum(1 for phase in snapshot.plan.phases if phase.is_complete),
        phase_states=[
            PhaseState(
                title=phase.title,
                state=phase.state,
                is_complete=phase.is_complete,
                checked_items=phase.checked_items,
                unchecked_items=phase.unchecked_items,
            )
            for phase in snapshot.plan.phases
        ],
        feature_facts=build_feature_facts(snapshot),
        warnings=list(snapshot.errors),
    )
    return FeatureState(
        snapshot=snapshot,
        selected_view=ui.active_view,
        status_message=ui.last_status_message,
        overview=overview,
    )


def build_file_states(snapshot: WorkItemSnapshot) -> list[FileState]:
    file_states: list[FileState] = []
    for name in ("prd.md", "fdd.md", "plan.md", "requirements.yml"):
        document = snapshot.documents[name]
        status = "present" if document.exists else "missing"
        if document.read_error:
            status = "read error"
        file_states.append(
            FileState(
                name=name,
                path=document.path,
                exists=document.exists,
                modified_label=format_modified_ns(document.modified_ns),
                status=status,
            )
        )
    return file_states


def format_modified_ns(modified_ns: int | None) -> str:
    if modified_ns is None:
        return "n/a"
    return datetime.fromtimestamp(modified_ns / 1_000_000_000).strftime("%Y-%m-%d %H:%M")


def build_feature_facts(snapshot: WorkItemSnapshot) -> list[str]:
    facts: list[str] = []
    required_capabilities = snapshot.capabilities.required_names
    if required_capabilities:
        facts.append(f"Required capabilities: {', '.join(required_capabilities)}")
    else:
        facts.append("Required capabilities: none detected")
    facts.append(f"Tracked source docs: {len(snapshot.documents)}")
    if snapshot.plan.phase_count:
        facts.append(f"Completed phases: {sum(1 for phase in snapshot.plan.phases if phase.is_complete)}/{snapshot.plan.phase_count}")
    return facts
