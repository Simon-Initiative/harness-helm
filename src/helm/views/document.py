from __future__ import annotations

from textual.containers import VerticalScroll
from textual.widgets import Markdown


class DocumentView(VerticalScroll, can_focus=True):
    def compose(self):
        yield Markdown(id="document-markdown")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._last_content: str | None = None

    def update_document(self, content: str) -> None:
        if content == self._last_content:
            return
        self._last_content = content
        self.query_one("#document-markdown", Markdown).update(content)
