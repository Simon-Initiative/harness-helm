from __future__ import annotations

from pathlib import Path

from helm.models import DocumentSnapshot, WorkItemSnapshot
from helm.parsers import (
    parse_capabilities_from_prd,
    parse_plan_document,
    parse_requirements_document,
)
from helm.readers.files import read_work_item_documents, resolve_work_item_dir


def build_work_item_snapshot(raw_path: str | Path) -> WorkItemSnapshot:
    root = resolve_work_item_dir(raw_path)
    documents, errors = read_work_item_documents(root)
    return build_work_item_snapshot_from_documents(root, documents, errors)


def build_work_item_snapshot_from_documents(
    root: Path,
    documents: dict[str, DocumentSnapshot],
    base_errors: list[str] | None = None,
) -> WorkItemSnapshot:
    errors = list(base_errors or [])
    plan = parse_plan_document(documents["plan.md"].content)
    requirements, requirement_errors = parse_requirements_document(documents["requirements.yml"].content)
    capabilities = parse_capabilities_from_prd(documents["prd.md"].content)
    errors.extend(requirement_errors)

    for document in documents.values():
        if document.read_error:
            errors.append(f"Failed to read {document.name}: {document.read_error}")

    return WorkItemSnapshot(
        root_path=root,
        feature_slug=root.name,
        documents=documents,
        plan=plan,
        requirements=requirements,
        capabilities=capabilities,
        errors=errors,
    )
