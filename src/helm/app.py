from __future__ import annotations

from textual.app import App, ComposeResult
from textual.widgets import Button, ContentSwitcher

from helm.store import WorkItemStore
from helm.ui.state import VIEW_SEQUENCE
from helm.views.document import DocumentView
from helm.views.overview import OverviewView
from helm.views.requirements import RequirementsView
from helm.widgets.footer import FooterStrip
from helm.widgets.header import HeaderStrip


class HelmApp(App[None]):
    CSS = """
    Screen {
        layout: vertical;
        background: #000814;
        color: #8fd3ff;
    }

    HeaderStrip {
        height: auto;
        padding: 0 1;
        background: #001d3d;
        color: #d7dce2;
        border: heavy #c6ccd3;
    }

    FooterStrip {
        height: auto;
        padding: 0 1;
        background: #00111f;
        color: #d7dce2;
        border: heavy #c6ccd3;
    }

    #header-app-name {
        width: 8;
        text-style: bold;
        color: #ffffff;
    }

    #header-feature-label {
        width: 1fr;
        color: #c6ccd3;
    }

    #header-view-label {
        width: auto;
        color: #8fd3ff;
    }

    .header-line {
        height: auto;
        padding-top: 1;
    }

    .nav-line {
        height: auto;
        padding-bottom: 1;
    }

    .nav-button {
        margin-right: 1;
        min-width: 14;
        background: #00111f;
        color: #d7dce2;
        border: round #8b949e;
    }

    .nav-button.active {
        background: #1f2937;
        color: #8fd3ff;
        text-style: bold;
        border: round #d7dce2;
    }

    #main-switcher {
        height: 1fr;
        background: #000000;
        border-left: heavy #c6ccd3;
        border-right: heavy #c6ccd3;
    }

    OverviewView, RequirementsView, DocumentView {
        height: 1fr;
        padding: 1 2;
        color: #8fd3ff;
        background: #000000;
    }

    Markdown {
        color: #8fd3ff;
        background: #000000;
    }

    OverviewView Static, RequirementsView Static {
        color: #8fd3ff;
    }
    """

    BINDINGS = [
        ("1", "select_view('overview')", "Overview"),
        ("2", "select_view('prd')", "PRD"),
        ("3", "select_view('fdd')", "FDD"),
        ("4", "select_view('plan')", "Plan"),
        ("5", "select_view('requirements')", "Requirements"),
        ("tab", "next_view", "Next View"),
        ("shift+tab", "previous_view", "Prev View"),
        ("r", "refresh", "Refresh"),
        ("q", "quit", "Quit"),
    ]

    def __init__(self, store: WorkItemStore, poll_interval: float = 1.0) -> None:
        super().__init__()
        self.store = store
        self.poll_interval = poll_interval
        self._view_tokens: dict[str, tuple] = {}

    def compose(self) -> ComposeResult:
        yield HeaderStrip()
        with ContentSwitcher(initial="overview", id="main-switcher"):
            yield OverviewView(id="overview")
            yield DocumentView(id="prd")
            yield DocumentView(id="fdd")
            yield DocumentView(id="plan")
            yield RequirementsView(id="requirements")
        yield FooterStrip()

    def on_mount(self) -> None:
        self.refresh_screen("initial load", force_content=True)
        self.set_interval(self.poll_interval, self.poll_for_changes)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if not event.button.id or not event.button.id.startswith("nav-"):
            return
        self.action_select_view(event.button.id.removeprefix("nav-"))

    def action_select_view(self, view_name: str) -> None:
        if view_name not in VIEW_SEQUENCE:
            return
        self.store.set_view(view_name)
        self.refresh_screen(f"view switched to {view_name}")

    def action_next_view(self) -> None:
        view_name = self.store.cycle_view(1)
        self.refresh_screen(f"view switched to {view_name}")

    def action_previous_view(self) -> None:
        view_name = self.store.cycle_view(-1)
        self.refresh_screen(f"view switched to {view_name}")

    def action_refresh(self) -> None:
        self.store.refresh("manual refresh")
        self.refresh_screen("manual refresh", force_content=True)

    def poll_for_changes(self) -> None:
        changed, changed_files = self.store.refresh_if_changed()
        if changed:
            self.refresh_screen(f"file change detected: {', '.join(changed_files)}", force_content=True)

    def refresh_screen(self, reason: str, force_content: bool = False) -> None:
        self.store.ui.last_status_message = reason
        state = self.store.feature_state
        self.query_one("#main-switcher", ContentSwitcher).current = state.selected_view
        self.query_one(HeaderStrip).apply_feature_state(state)
        self.query_one(FooterStrip).apply_feature_state(state)
        self.refresh_active_view(state, force_content=force_content)
        self.focus_active_view(state.selected_view)

    def refresh_active_view(self, state, force_content: bool) -> None:
        view_name = state.selected_view
        token = self.view_token(view_name, state)
        if not force_content and self._view_tokens.get(view_name) == token:
            return

        if view_name == "overview":
            self.query_one(OverviewView).apply_feature_state(state)
        elif view_name == "requirements":
            self.query_one(RequirementsView).apply_feature_state(state)
        elif view_name == "prd":
            self.query_one("#prd", DocumentView).update_document(self.render_document("prd.md"))
        elif view_name == "fdd":
            self.query_one("#fdd", DocumentView).update_document(self.render_document("fdd.md"))
        elif view_name == "plan":
            self.query_one("#plan", DocumentView).update_document(self.render_document("plan.md"))

        self._view_tokens[view_name] = token

    def focus_active_view(self, view_name: str) -> None:
        if view_name == "overview":
            self.set_focus(self.query_one(OverviewView))
        elif view_name == "requirements":
            self.set_focus(self.query_one(RequirementsView))
        else:
            self.set_focus(self.query_one(f"#{view_name}", DocumentView))

    def view_token(self, view_name: str, state) -> tuple:
        snapshot = state.snapshot
        if view_name == "overview":
            return (
                view_name,
                tuple(
                    (
                        name,
                        document.exists,
                        document.modified_ns,
                        document.read_error,
                    )
                    for name, document in snapshot.documents.items()
                ),
                tuple(snapshot.requirements.by_status.items()),
                tuple(snapshot.requirements.acceptance_criteria_by_status.items()),
                tuple((phase.title, phase.state, phase.checked_items, phase.unchecked_items) for phase in snapshot.plan.phases),
                tuple(snapshot.capabilities.required_names),
                tuple(snapshot.errors),
            )
        if view_name == "requirements":
            document = snapshot.documents["requirements.yml"]
            return (
                view_name,
                document.exists,
                document.modified_ns,
                document.read_error,
                len(snapshot.requirements.items),
                len(snapshot.requirements.acceptance_criteria),
                tuple(snapshot.errors),
            )
        document_name = {
            "prd": "prd.md",
            "fdd": "fdd.md",
            "plan": "plan.md",
        }[view_name]
        document = snapshot.documents[document_name]
        return (view_name, document.exists, document.modified_ns, document.read_error)

    def render_document(self, name: str) -> str:
        document = self.store.snapshot.documents[name]
        if document.exists and document.content.strip():
            return document.content
        return f"# Missing\n\n`{name}` is not available in `{self.store.snapshot.root_path}`."
