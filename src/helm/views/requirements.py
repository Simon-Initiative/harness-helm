from __future__ import annotations

from rich.console import Group
from rich.syntax import Syntax
from rich.table import Table
from textual.containers import VerticalScroll
from textual.widgets import Static

from helm.models import FeatureState


class RequirementsView(VerticalScroll, can_focus=True):
    def compose(self):
        yield Static(id="requirements-body")

    def apply_feature_state(self, state: FeatureState) -> None:
        self.query_one("#requirements-body", Static).update(render_requirements(state))


def render_requirements(state: FeatureState):
    summary = state.snapshot.requirements
    sections: list[object] = [
        summary_table(summary),
        requirements_table(summary),
    ]
    if summary.acceptance_criteria:
        sections.append(acceptance_criteria_table(summary))
    if not summary.items and state.snapshot.documents["requirements.yml"].content.strip():
        sections.append(
            Syntax(
                state.snapshot.documents["requirements.yml"].content,
                "yaml",
                line_numbers=True,
                word_wrap=True,
            )
        )
    return Group(*sections)


def summary_table(summary) -> Table:
    table = Table(title="Requirements Summary", expand=True, box=None, pad_edge=False)
    table.add_column("Metric", ratio=2)
    table.add_column("Value", ratio=4)
    table.add_row("Requirements", str(len(summary.items)))
    table.add_row("Acceptance Criteria", str(len(summary.acceptance_criteria)))
    table.add_row(
        "Statuses",
        ", ".join(f"{name}: {value}" for name, value in sorted(summary.by_status.items())) or "none",
    )
    return table


def requirements_table(summary) -> Table:
    table = Table(title="Functional Requirements", expand=True, box=None, pad_edge=False)
    table.add_column("ID", ratio=1)
    table.add_column("Status", ratio=1)
    table.add_column("Title", ratio=4)
    table.add_column("Proof", ratio=2)
    for item in summary.items:
        table.add_row(item.key, item.status, item.title, item.validated_by)
    if not summary.items:
        table.add_row("-", "-", "No parsed requirements", "-")
    return table


def acceptance_criteria_table(summary) -> Table:
    table = Table(title="Acceptance Criteria", expand=True, box=None, pad_edge=False)
    table.add_column("ID", ratio=1)
    table.add_column("FR", ratio=1)
    table.add_column("Status", ratio=1)
    table.add_column("Verification", ratio=1)
    table.add_column("Title", ratio=4)
    for item in summary.acceptance_criteria:
        table.add_row(
            item.key,
            item.requirement_key or "-",
            item.status,
            item.verification_method,
            item.title,
        )
    return table
