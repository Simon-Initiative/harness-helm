from __future__ import annotations

from pathlib import Path

from helm.derive.feature_state import build_feature_state
from helm.derive.work_item import build_work_item_snapshot, build_work_item_snapshot_from_documents
from helm.models import DocumentSnapshot, FeatureState, WorkItemSnapshot
from helm.readers.files import read_document
from helm.ui.state import UIState, VIEW_SEQUENCE
from helm.watcher import PollingWatcher


class WorkItemStore:
    def __init__(self, raw_path: str | Path) -> None:
        self.root_path = Path(raw_path).expanduser().resolve()
        self.ui = UIState()
        self.snapshot = build_work_item_snapshot(self.root_path)
        self.watcher = PollingWatcher(self.snapshot.documents)

    def refresh(self, reason: str) -> WorkItemSnapshot:
        self.snapshot = build_work_item_snapshot(self.root_path)
        self.watcher.update_documents(self.snapshot.documents)
        self.ui.last_status_message = reason
        return self.snapshot

    def refresh_if_changed(self) -> tuple[bool, list[str]]:
        changed_files = self.watcher.changed_files()
        if not changed_files:
            return False, []
        self.snapshot = self._refresh_changed_documents(changed_files)
        self.watcher.update_documents(self.snapshot.documents)
        self.ui.last_status_message = f"file change detected: {', '.join(changed_files)}"
        return True, changed_files

    def _refresh_changed_documents(self, changed_files: list[str]) -> WorkItemSnapshot:
        documents: dict[str, DocumentSnapshot] = dict(self.snapshot.documents)
        errors: list[str] = []

        for name in changed_files:
            existing = documents[name]
            refreshed, read_errors = read_document(existing.path, name)
            documents[name] = refreshed
            errors.extend(read_errors)

        for name, document in documents.items():
            if name not in changed_files and not document.exists:
                errors.append(f"Missing required file: {name}")

        return build_work_item_snapshot_from_documents(self.root_path, documents, errors)

    @property
    def feature_state(self) -> FeatureState:
        return build_feature_state(self.snapshot, self.ui)

    def set_view(self, view_name: str) -> None:
        if view_name in VIEW_SEQUENCE:
            self.ui.active_view = view_name

    def cycle_view(self, direction: int) -> str:
        current_index = VIEW_SEQUENCE.index(self.ui.active_view)
        next_index = (current_index + direction) % len(VIEW_SEQUENCE)
        self.ui.active_view = VIEW_SEQUENCE[next_index]
        return self.ui.active_view
