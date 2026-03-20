from __future__ import annotations

from helm.models import DocumentSnapshot


class PollingWatcher:
    """Tracks individual document signatures for polling-based refresh."""

    def __init__(self, documents: dict[str, DocumentSnapshot]) -> None:
        self._documents = documents
        self._signature = self._build_signature()

    def update_documents(self, documents: dict[str, DocumentSnapshot]) -> None:
        self._documents = documents
        self._signature = self._build_signature()

    def changed_files(self) -> list[str]:
        current = self._build_signature()
        changed = [
            name
            for name, signature in current.items()
            if signature != self._signature.get(name)
        ]
        if not changed:
            return []
        self._signature = current
        return sorted(changed)

    def _build_signature(self) -> dict[str, tuple[int, int]]:
        signature: dict[str, tuple[int, int]] = {}
        for name, document in self._documents.items():
            path = document.path
            if path.exists():
                stat = path.stat()
                signature[name] = (stat.st_mtime_ns, stat.st_size)
            else:
                signature[name] = (-1, -1)
        return signature
