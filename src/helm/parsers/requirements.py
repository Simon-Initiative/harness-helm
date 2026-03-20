from __future__ import annotations

from typing import Any

import yaml

from helm.models import AcceptanceCriterion, RequirementItem, RequirementsSummary


def parse_requirements_document(raw_yaml: str) -> tuple[RequirementsSummary, list[str]]:
    if not raw_yaml.strip():
        return RequirementsSummary(), []

    try:
        data = yaml.safe_load(raw_yaml) or {}
    except yaml.YAMLError as exc:
        return RequirementsSummary(), [f"Failed to parse requirements.yml: {exc}"]

    global_acceptance_criteria = parse_acceptance_criteria_list(data.get("acceptance_criteria"), None)

    items: list[RequirementItem] = []
    nested_acceptance_criteria: list[AcceptanceCriterion] = []
    for key, value in iter_requirement_entries(data):
        item = build_requirement_item(key, value)
        if item is not None:
            items.append(item)
            nested_acceptance_criteria.extend(item.acceptance_criteria)

    items.sort(key=lambda requirement: requirement.key)
    all_acceptance_criteria = nested_acceptance_criteria + [
        item for item in global_acceptance_criteria if item.key not in {entry.key for entry in nested_acceptance_criteria}
    ]
    return RequirementsSummary(items=items, acceptance_criteria=all_acceptance_criteria), []


def iter_requirement_entries(data: Any) -> list[tuple[str, Any]]:
    if isinstance(data, dict):
        if isinstance(data.get("requirements"), list):
            return [
                (entry_key_from_list_item(index, item), item)
                for index, item in enumerate(data["requirements"], start=1)
            ]
        if isinstance(data.get("requirements"), dict):
            return list(data["requirements"].items())
        return [
            (key, value)
            for key, value in data.items()
            if isinstance(value, (dict, list, str, int, float, bool))
            and key not in {"meta", "metadata", "acceptance_criteria"}
        ]

    if isinstance(data, list):
        return [(entry_key_from_list_item(index, item), item) for index, item in enumerate(data, start=1)]

    return []


def entry_key_from_list_item(index: int, item: Any) -> str:
    if isinstance(item, dict):
        for field in ("id", "key", "slug"):
            value = item.get(field)
            if isinstance(value, str) and value.strip():
                return value.strip()
    return f"REQ-{index:03d}"


def build_requirement_item(key: str, value: Any) -> RequirementItem | None:
    if isinstance(value, dict):
        title = first_string(value, "title", "summary", "name", "requirement") or key
        status = normalize_status(first_string(value, "status", "state", "validation_state"))
        acceptance_criteria = parse_acceptance_criteria_list(value.get("acceptance_criteria"), key)
        validated_by = stringify_validation_source(
            value.get("validated_by")
            or value.get("validation")
            or value.get("proof")
            or value.get("implemented_by")
            or flatten_proofs(acceptance_criteria)
        )
        return RequirementItem(
            key=key,
            title=title,
            status=status,
            validated_by=validated_by,
            acceptance_criteria=acceptance_criteria,
        )

    if isinstance(value, list):
        return RequirementItem(
            key=key,
            title=key,
            status="listed",
            validated_by=", ".join(stringify_validation_source(entry) for entry in value) or "unknown",
        )

    if isinstance(value, str):
        return RequirementItem(key=key, title=value, status="unknown", validated_by="unknown")

    return None


def parse_acceptance_criteria_list(
    raw_items: Any,
    requirement_key: str | None,
) -> list[AcceptanceCriterion]:
    if not isinstance(raw_items, list):
        return []

    items: list[AcceptanceCriterion] = []
    for index, value in enumerate(raw_items, start=1):
        if not isinstance(value, dict):
            continue
        key = first_string(value, "id", "key", "slug") or f"AC-{index:03d}"
        title = first_string(value, "title", "summary", "name", "criterion") or key
        status = normalize_status(first_string(value, "status", "state", "validation_state"))
        verification_method = normalize_status(first_string(value, "verification_method")) or "unknown"
        proofs = normalize_proofs(value.get("proofs"))
        items.append(
            AcceptanceCriterion(
                key=key,
                title=title,
                status=status,
                verification_method=verification_method,
                proofs=proofs,
                requirement_key=requirement_key,
            )
        )
    return items


def flatten_proofs(acceptance_criteria: list[AcceptanceCriterion]) -> list[str]:
    proofs: list[str] = []
    for criterion in acceptance_criteria:
        proofs.extend(criterion.proofs)
    return proofs


def normalize_proofs(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def first_string(mapping: dict[str, Any], *keys: str) -> str | None:
    for key in keys:
        value = mapping.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def normalize_status(value: str | None) -> str:
    if not value:
        return "unknown"
    return value.strip().replace("_", " ").lower()


def stringify_validation_source(value: Any) -> str:
    if value is None:
        return "unknown"
    if isinstance(value, str):
        return value.strip() or "unknown"
    if isinstance(value, list):
        return ", ".join(stringify_validation_source(item) for item in value if item is not None) or "unknown"
    if isinstance(value, dict):
        for key in ("path", "file", "test", "status", "summary"):
            field = value.get(key)
            if isinstance(field, str) and field.strip():
                return field.strip()
        return "structured"
    return str(value)
