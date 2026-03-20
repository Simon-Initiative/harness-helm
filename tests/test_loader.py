from __future__ import annotations

from pathlib import Path

from helm.loader import load_work_item, parse_plan_phases
from helm.parsers import parse_requirements_document
from helm.parsers.capabilities import parse_capabilities_from_prd
from helm.store import WorkItemStore


FIXTURE_ROOT = Path(__file__).parent / "fixtures" / "sample_feature"


def test_parse_plan_phases_collects_markdown_headings() -> None:
    phases = parse_plan_phases(
        "# Feature Plan\n\n## Scope\nText\n\n## Phase 1: Bootstrap\n- [x] done\n\n### Slice A\n\n## Phase 2: Refresh\n- [ ] open\n\n## Decision Log\n"
    )
    assert [phase.title for phase in phases] == [
        "Phase 1: Bootstrap",
        "Phase 2: Refresh",
    ]
    assert phases[0].state == "completed"
    assert phases[0].is_complete is True
    assert phases[1].state == "not started"
    assert phases[1].is_complete is False


def test_load_work_item_reads_documents_and_requirements() -> None:
    snapshot = load_work_item(FIXTURE_ROOT)

    assert snapshot.feature_slug == "sample_feature"
    assert snapshot.plan.phase_count == 2
    assert len(snapshot.requirements.items) == 2
    assert len(snapshot.requirements.acceptance_criteria) == 2
    assert snapshot.documents["prd.md"].exists is True
    assert snapshot.requirements.items[0].key == "FR-1"
    assert snapshot.requirements.items[0].status == "validated"
    assert snapshot.requirements.items[1].validated_by == "tests/test_refresh.py"
    assert snapshot.requirements.acceptance_criteria[0].key == "AC-1"
    assert snapshot.plan.phases[0].state == "completed"
    assert snapshot.plan.phases[0].is_complete is True
    assert snapshot.plan.phases[1].state == "in progress"
    assert snapshot.plan.phases[1].is_complete is False
    assert "telemetry" in snapshot.capabilities.required_names
    assert "feature_flags" in snapshot.capabilities.required_names


def test_parse_plan_phase_without_checklist_is_not_complete() -> None:
    phases = parse_plan_phases(
        "# Plan\n\n## Phase 1: Discovery\nNarrative only\n\n## Phase 2: Build\n- [x] done\n"
    )

    assert phases[0].has_checklist is False
    assert phases[0].is_complete is False
    assert phases[0].state == "unknown"
    assert phases[1].is_complete is True


def test_load_work_item_reports_missing_required_files(tmp_path: Path) -> None:
    work_item_dir = tmp_path / "missing"
    work_item_dir.mkdir()
    (work_item_dir / "plan.md").write_text("# Empty plan\n", encoding="utf-8")

    snapshot = load_work_item(work_item_dir)

    assert "Missing required file: prd.md" in snapshot.errors
    assert "Missing required file: fdd.md" in snapshot.errors
    assert "Missing required file: requirements.yml" in snapshot.errors


def test_parse_capabilities_from_prd_extracts_required_capabilities() -> None:
    summary = parse_capabilities_from_prd(
        "## 8. Non-Functional Requirements\nTelemetry and observability matter. Performance matters.\n\n## 11. Feature Flagging, Rollout & Migration\nFeature flag required for rollout.\n"
    )

    assert summary.required_names == [
        "feature_flags",
        "telemetry",
        "performance_requirements",
    ]


def test_parse_capabilities_from_prd_respects_explicit_no_feature_flag() -> None:
    summary = parse_capabilities_from_prd(
        "## 11. Feature Flagging, Rollout & Migration\nNo feature flags present in this feature\n\n## 8. Non-Functional Requirements\nObservability and telemetry are required.\n"
    )

    assert "feature_flags" not in summary.required_names
    assert "telemetry" in summary.required_names


def test_parse_requirements_document_supports_nested_acceptance_criteria() -> None:
    summary, errors = parse_requirements_document(
        """
version: 1
requirements:
  - id: FR-001
    title: System shall do the thing
    status: proposed
    acceptance_criteria:
      - id: AC-001
        title: It works
        status: verified
        verification_method: automated
        proofs:
          - test/example_test.exs
"""
    )

    assert errors == []
    assert len(summary.items) == 1
    assert len(summary.acceptance_criteria) == 1
    assert summary.items[0].acceptance_criteria[0].key == "AC-001"
    assert summary.items[0].validated_by == "test/example_test.exs"


def test_parse_requirements_document_supports_top_level_acceptance_criteria() -> None:
    summary, errors = parse_requirements_document(
        """
requirements:
  - id: FR-001
    title: FR title
    status: verified
acceptance_criteria:
  - id: AC-001
    title: AC title
    status: verified
    verification_method: automated
    proofs:
      - docs/manual_qa.md
"""
    )

    assert errors == []
    assert len(summary.items) == 1
    assert len(summary.acceptance_criteria) == 1
    assert summary.acceptance_criteria[0].key == "AC-001"
    assert summary.acceptance_criteria[0].proofs == ["docs/manual_qa.md"]


def test_store_refresh_if_changed_reloads_changed_file(tmp_path: Path) -> None:
    work_item_dir = tmp_path / "feature"
    work_item_dir.mkdir()
    (work_item_dir / "prd.md").write_text("# PRD\n\nTelemetry required.\n", encoding="utf-8")
    (work_item_dir / "fdd.md").write_text("# FDD\n", encoding="utf-8")
    (work_item_dir / "plan.md").write_text("# Plan\n\n## Phase 1: Start\n- [ ] Start\n", encoding="utf-8")
    (work_item_dir / "requirements.yml").write_text(
        "requirements:\n  FR-1:\n    title: Test\n    status: pending\n",
        encoding="utf-8",
    )

    store = WorkItemStore(work_item_dir)
    assert store.snapshot.plan.phases[0].state == "not started"

    (work_item_dir / "plan.md").write_text("# Plan\n\n## Phase 1: Start\n- [x] Start\n", encoding="utf-8")

    changed, changed_files = store.refresh_if_changed()

    assert changed is True
    assert changed_files == ["plan.md"]
    assert store.snapshot.plan.phases[0].state == "completed"
    assert store.snapshot.plan.phases[0].is_complete is True
