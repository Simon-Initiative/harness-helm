from __future__ import annotations

from pathlib import Path

from helm.models import DocumentSnapshot


EXPECTED_FILES = ("prd.md", "fdd.md", "plan.md", "requirements.yml")


def resolve_work_item_dir(raw_path: str | Path) -> Path:
    path = Path(raw_path).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"Work item directory does not exist: {path}")
    if not path.is_dir():
        raise NotADirectoryError(f"Work item path is not a directory: {path}")
    return path


def read_work_item_documents(root: Path) -> tuple[dict[str, DocumentSnapshot], list[str]]:
    documents: dict[str, DocumentSnapshot] = {}
    errors: list[str] = []

    for name in EXPECTED_FILES:
        snapshot, read_errors = read_document(root / name, name)
        documents[name] = snapshot
        errors.extend(read_errors)

    return documents, errors


def read_document(path: Path, name: str) -> tuple[DocumentSnapshot, list[str]]:
    if not path.exists():
        return (
            DocumentSnapshot(
                name=name,
                path=path,
                content="",
                exists=False,
                modified_ns=None,
            ),
            [f"Missing required file: {name}"],
        )

    try:
        content = path.read_text(encoding="utf-8")
        stat = path.stat()
    except OSError as exc:
        return (
            DocumentSnapshot(
                name=name,
                path=path,
                content="",
                exists=True,
                modified_ns=None,
                read_error=str(exc),
            ),
            [f"Failed to read {name}: {exc}"],
        )

    return (
        DocumentSnapshot(
            name=name,
            path=path,
            content=content,
            exists=True,
            modified_ns=stat.st_mtime_ns,
        ),
        [],
    )
