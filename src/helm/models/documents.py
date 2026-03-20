from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class DocumentSnapshot:
    name: str
    path: Path
    content: str
    exists: bool
    modified_ns: int | None
    read_error: str | None = None

    @property
    def is_healthy(self) -> bool:
        return self.exists and self.read_error is None
