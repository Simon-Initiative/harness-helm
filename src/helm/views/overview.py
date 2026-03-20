from __future__ import annotations

from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from textual.containers import VerticalScroll
from textual.widgets import Static

from helm.models import FeatureState


class OverviewView(VerticalScroll, can_focus=True):
    def compose(self):
        yield Static(id="overview-body")

    def apply_feature_state(self, state: FeatureState) -> None:
        self.query_one("#overview-body", Static).update(render_overview(state))


def render_overview(state: FeatureState):
    overview = state.overview
    sections: list[object] = []

    sections.append(framed(requirements_table(overview), "REQUIREMENTS"))
    sections.append(framed(plan_table(overview), "PLAN PHASES"))
    sections.append(framed(feature_facts_table(overview.feature_facts), "FEATURE FACTS"))
    if overview.warnings:
        sections.append(framed(warnings_table(overview.warnings), "WARNINGS / GAPS"))

    return Group(*sections)


def framed(renderable, title: str) -> Panel:
    return Panel(
        renderable,
        title=f"[bold #d7dce2]{title}[/bold #d7dce2]",
        border_style="#c6ccd3",
        padding=(0, 1),
    )


def requirements_table(overview) -> Table:
    table = Table(expand=True, box=None, pad_edge=False)
    table.add_column("Metric", ratio=2)
    table.add_column("Value", ratio=4)
    table.add_row("Requirements", str(overview.requirement_total))
    table.add_row("Acceptance Criteria", str(overview.acceptance_criteria_total))
    table.add_row("Requirement Status", format_counts(overview.requirement_status_counts))
    table.add_row("Acceptance Status", format_counts(overview.acceptance_status_counts))
    return table


def plan_table(overview) -> Table:
    table = Table(expand=True, box=None, pad_edge=False)
    table.add_column("Phase", ratio=5)
    table.add_column("State", ratio=2)
    table.add_column("Checklist", ratio=2)
    for phase in overview.phase_states:
        checklist = f"{phase.checked_items}/{phase.checked_items + phase.unchecked_items}"
        state_label = "complete" if phase.is_complete else phase.state
        table.add_row(phase.title, state_label, checklist)
    if not overview.phase_states:
        table.add_row("No parsed execution phases", "-", "-")
    return table


def feature_facts_table(facts: list[str]) -> Table:
    table = Table(expand=True, box=None, pad_edge=False)
    table.add_column("Fact", ratio=1)
    for fact in facts:
        table.add_row(Text.from_markup(fact))
    return table


def warnings_table(warnings: list[str]) -> Table:
    table = Table(expand=True, box=None, pad_edge=False)
    table.add_column("Issue", ratio=1)
    for warning in warnings:
        table.add_row(warning)
    return table


def format_counts(counts: dict[str, int]) -> str:
    if not counts:
        return "none"
    return ", ".join(f"{name}: {value}" for name, value in sorted(counts.items()))
