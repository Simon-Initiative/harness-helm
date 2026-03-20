from __future__ import annotations

from textual.widgets import Static

from helm.models import FeatureState


class FooterStrip(Static):
    def apply_feature_state(self, state: FeatureState) -> None:
        warning_count = len(state.overview.warnings)
        current_file = current_file_label(state.selected_view)
        hints = "1 Overview  2 PRD  3 FDD  4 Plan  5 Requirements  Tab Next  Shift+Tab Prev  r Refresh  q Quit"
        status = f"file: {current_file} | warnings: {warning_count} | {state.status_message}"
        self.update(f"{status}\n{hints}")


def current_file_label(selected_view: str) -> str:
    mapping = {
        "overview": "feature overview",
        "prd": "prd.md",
        "fdd": "fdd.md",
        "plan": "plan.md",
        "requirements": "requirements.yml",
    }
    return mapping[selected_view]
