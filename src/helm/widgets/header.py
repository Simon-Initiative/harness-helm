from __future__ import annotations

from pathlib import Path

from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Static

from helm.models import FeatureState
from helm.ui.state import VIEW_SEQUENCE


class HeaderStrip(Vertical):
    def compose(self):
        with Horizontal(classes="header-line"):
            yield Static("helm", id="header-app-name")
            yield Static("", id="header-feature-label")
            yield Static("", id="header-view-label")
        with Horizontal(classes="nav-line"):
            for index, view in enumerate(VIEW_SEQUENCE, start=1):
                yield Button(f"{index} {view.title()}", id=f"nav-{view}", classes="nav-button")

    def apply_feature_state(self, state: FeatureState) -> None:
        self.query_one("#header-feature-label", Static).update(shorten_path(state.root_path))
        self.query_one("#header-view-label", Static).update(f"view: {state.selected_view}")
        for view in VIEW_SEQUENCE:
            button = self.query_one(f"#nav-{view}", Button)
            button.remove_class("active")
            if view == state.selected_view:
                button.add_class("active")


def shorten_path(path: Path) -> str:
    parts = path.parts
    if len(parts) <= 4:
        return str(path)
    return f".../{'/'.join(parts[-4:])}"
