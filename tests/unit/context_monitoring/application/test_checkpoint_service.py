# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Unit tests for CheckpointService.

Tests cover BDD scenarios from EN-003 and EN-008:
    - CheckpointService creates checkpoint on pre-compact
    - CheckpointService is fail-open when ORCHESTRATION.yaml absent
    - TASK-001: Structured checkpoint field extraction
    - TASK-003: Checkpoint write-back to ORCHESTRATION.yaml

References:
    - EN-003: Context Monitoring Bounded Context Foundation
    - EN-008: Context Resilience Hardening
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from src.context_monitoring.application.ports.checkpoint_repository import (
    ICheckpointRepository,
)
from src.context_monitoring.application.services.checkpoint_service import (
    CheckpointService,
)
from src.context_monitoring.domain.value_objects.fill_estimate import FillEstimate
from src.context_monitoring.domain.value_objects.threshold_tier import ThresholdTier

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture()
def mock_repository() -> MagicMock:
    """Create a mock ICheckpointRepository."""
    repo = MagicMock(spec=ICheckpointRepository)
    repo.next_checkpoint_id.return_value = "cx-001"
    return repo


_SAMPLE_ORCHESTRATION_YAML = """\
workflow:
  id: "feat001-impl-20260220-001"
  name: "FEAT-001 Implementation"
  status: "ACTIVE"
pipelines:
  pipeline_a:
    id: "pipeline-a"
    current_phase: 3
    phases:
      - id: 1
        name: "Phase 1"
        status: "COMPLETE"
        agents:
          - id: "agent-a-001"
            status: "COMPLETE"
      - id: 2
        name: "Phase 2"
        status: "IN_PROGRESS"
        agents:
          - id: "agent-a-002"
            status: "IN_PROGRESS"
next_actions:
  immediate:
    - action: "Execute Phase 3 agents"
  subsequent:
    - action: "Run quality gate"
resumption:
  recovery_state:
    current_phase: 3
    workflow_status: "ACTIVE"
    updated_at: "2026-02-20T10:00:00+00:00"
  quality_trajectory:
    gates_completed: ["QG-1"]
    gates_remaining: ["QG-2"]
    current_gate: "QG-2"
    total_iterations_used: 2
  compaction_events:
    count: 0
    events: []
"""


@pytest.fixture()
def service_with_orchestration(mock_repository: MagicMock, tmp_path: Path) -> CheckpointService:
    """Create a CheckpointService with an ORCHESTRATION.yaml present."""
    orchestration_path = tmp_path / "ORCHESTRATION.yaml"
    orchestration_path.write_text(_SAMPLE_ORCHESTRATION_YAML, encoding="utf-8")
    return CheckpointService(
        repository=mock_repository,
        orchestration_path=orchestration_path,
    )


@pytest.fixture()
def service_without_orchestration(mock_repository: MagicMock) -> CheckpointService:
    """Create a CheckpointService without an ORCHESTRATION.yaml."""
    return CheckpointService(
        repository=mock_repository,
        orchestration_path=Path("/nonexistent/ORCHESTRATION.yaml"),
    )


# =============================================================================
# BDD Scenario: CheckpointService creates checkpoint on pre-compact
# =============================================================================


class TestCreateCheckpointOnPreCompact:
    """Scenario: CheckpointService creates checkpoint on pre-compact.

    Given a valid context state and ORCHESTRATION.yaml,
    the service should create and save a checkpoint.
    """

    def test_creates_checkpoint_with_context_state(
        self,
        service_with_orchestration: CheckpointService,
        mock_repository: MagicMock,
    ) -> None:
        """CheckpointService creates a checkpoint with context state."""
        fill = FillEstimate(fill_percentage=0.82, tier=ThresholdTier.CRITICAL)
        result = service_with_orchestration.create_checkpoint(
            context_state=fill, trigger="pre_compact"
        )
        assert result is not None
        assert result.checkpoint_id == "cx-001"
        assert result.context_state.fill_percentage == 0.82
        mock_repository.save.assert_called_once()

    def test_includes_orchestration_state(
        self,
        service_with_orchestration: CheckpointService,
        mock_repository: MagicMock,
    ) -> None:
        """CheckpointService includes ORCHESTRATION.yaml content in resumption_state."""
        fill = FillEstimate(fill_percentage=0.82, tier=ThresholdTier.CRITICAL)
        result = service_with_orchestration.create_checkpoint(
            context_state=fill, trigger="pre_compact"
        )
        assert result is not None
        assert result.resumption_state is not None
        # TASK-001: Structured fields should be present
        assert "orchestration_raw" in result.resumption_state

    def test_checkpoint_has_created_at(
        self,
        service_with_orchestration: CheckpointService,
        mock_repository: MagicMock,
    ) -> None:
        """CheckpointService sets created_at on the checkpoint."""
        fill = FillEstimate(fill_percentage=0.82, tier=ThresholdTier.CRITICAL)
        result = service_with_orchestration.create_checkpoint(
            context_state=fill, trigger="pre_compact"
        )
        assert result is not None
        assert result.created_at != ""


# =============================================================================
# BDD Scenario: CheckpointService is fail-open when ORCHESTRATION.yaml absent
# =============================================================================


class TestFailOpenWithoutOrchestration:
    """Scenario: CheckpointService is fail-open when ORCHESTRATION.yaml absent.

    Given no ORCHESTRATION.yaml file,
    the service should still create a checkpoint without resumption state.
    """

    def test_creates_checkpoint_without_orchestration(
        self,
        service_without_orchestration: CheckpointService,
        mock_repository: MagicMock,
    ) -> None:
        """CheckpointService creates checkpoint even without ORCHESTRATION.yaml."""
        fill = FillEstimate(fill_percentage=0.82, tier=ThresholdTier.CRITICAL)
        result = service_without_orchestration.create_checkpoint(
            context_state=fill, trigger="pre_compact"
        )
        assert result is not None
        assert result.checkpoint_id == "cx-001"
        mock_repository.save.assert_called_once()

    def test_resumption_state_without_orchestration(
        self,
        service_without_orchestration: CheckpointService,
        mock_repository: MagicMock,
    ) -> None:
        """Without ORCHESTRATION.yaml, resumption_state has no orchestration key."""
        fill = FillEstimate(fill_percentage=0.82, tier=ThresholdTier.CRITICAL)
        result = service_without_orchestration.create_checkpoint(
            context_state=fill, trigger="pre_compact"
        )
        assert result is not None
        # Should either be None or a dict without 'orchestration'
        if result.resumption_state is not None:
            assert result.resumption_state.get("orchestration") is None

    def test_does_not_raise_on_missing_file(
        self,
        service_without_orchestration: CheckpointService,
        mock_repository: MagicMock,
    ) -> None:
        """No exception is raised when ORCHESTRATION.yaml is missing."""
        fill = FillEstimate(fill_percentage=0.5, tier=ThresholdTier.NOMINAL)
        # Should not raise
        result = service_without_orchestration.create_checkpoint(
            context_state=fill, trigger="manual"
        )
        assert result is not None


# =============================================================================
# BDD Scenario: TASK-001 Structured checkpoint field extraction
# =============================================================================


class TestStructuredCheckpointFieldExtraction:
    """Scenario: CheckpointService extracts structured fields from ORCHESTRATION.yaml.

    TASK-001: When ORCHESTRATION.yaml contains valid YAML, the service parses it
    and extracts structured fields (workflow_id, current_phase, agent_statuses, etc.)
    rather than storing raw text.
    """

    def test_extracts_workflow_metadata(
        self,
        service_with_orchestration: CheckpointService,
        mock_repository: MagicMock,
    ) -> None:
        """Structured fields include workflow_id, workflow_status, workflow_name."""
        fill = FillEstimate(fill_percentage=0.82, tier=ThresholdTier.CRITICAL)
        result = service_with_orchestration.create_checkpoint(
            context_state=fill, trigger="pre_compact"
        )
        state = result.resumption_state
        assert state is not None
        assert state["workflow_id"] == "feat001-impl-20260220-001"
        assert state["workflow_status"] == "ACTIVE"
        assert state["workflow_name"] == "FEAT-001 Implementation"

    def test_extracts_current_phase(
        self,
        service_with_orchestration: CheckpointService,
        mock_repository: MagicMock,
    ) -> None:
        """Structured fields include current_phase from pipelines."""
        fill = FillEstimate(fill_percentage=0.82, tier=ThresholdTier.CRITICAL)
        result = service_with_orchestration.create_checkpoint(
            context_state=fill, trigger="pre_compact"
        )
        state = result.resumption_state
        assert state is not None
        assert state["current_phase"] == 3

    def test_extracts_agent_statuses(
        self,
        service_with_orchestration: CheckpointService,
        mock_repository: MagicMock,
    ) -> None:
        """Structured fields include agent_statuses from pipeline phases."""
        fill = FillEstimate(fill_percentage=0.82, tier=ThresholdTier.CRITICAL)
        result = service_with_orchestration.create_checkpoint(
            context_state=fill, trigger="pre_compact"
        )
        state = result.resumption_state
        assert state is not None
        assert "agent_statuses" in state
        statuses = state["agent_statuses"]
        assert len(statuses) == 2
        assert {"id": "agent-a-001", "status": "COMPLETE"} in statuses
        assert {"id": "agent-a-002", "status": "IN_PROGRESS"} in statuses

    def test_extracts_quality_gate_state(
        self,
        service_with_orchestration: CheckpointService,
        mock_repository: MagicMock,
    ) -> None:
        """Structured fields include quality_gate_state from resumption section."""
        fill = FillEstimate(fill_percentage=0.82, tier=ThresholdTier.CRITICAL)
        result = service_with_orchestration.create_checkpoint(
            context_state=fill, trigger="pre_compact"
        )
        state = result.resumption_state
        assert state is not None
        assert "quality_gate_state" in state
        qg = state["quality_gate_state"]
        assert qg["gates_completed"] == ["QG-1"]
        assert qg["gates_remaining"] == ["QG-2"]
        assert qg["current_gate"] == "QG-2"
        assert qg["total_iterations_used"] == 2

    def test_extracts_recovery_state(
        self,
        service_with_orchestration: CheckpointService,
        mock_repository: MagicMock,
    ) -> None:
        """Structured fields include recovery_state from resumption section."""
        fill = FillEstimate(fill_percentage=0.82, tier=ThresholdTier.CRITICAL)
        result = service_with_orchestration.create_checkpoint(
            context_state=fill, trigger="pre_compact"
        )
        state = result.resumption_state
        assert state is not None
        assert "recovery_state" in state
        recovery = state["recovery_state"]
        assert recovery["current_phase"] == 3
        assert recovery["workflow_status"] == "ACTIVE"

    def test_extracts_next_actions(
        self,
        service_with_orchestration: CheckpointService,
        mock_repository: MagicMock,
    ) -> None:
        """Structured fields include next_actions (immediate) from top-level."""
        fill = FillEstimate(fill_percentage=0.82, tier=ThresholdTier.CRITICAL)
        result = service_with_orchestration.create_checkpoint(
            context_state=fill, trigger="pre_compact"
        )
        state = result.resumption_state
        assert state is not None
        assert "next_actions" in state
        assert len(state["next_actions"]) == 1
        assert state["next_actions"][0]["action"] == "Execute Phase 3 agents"

    def test_includes_orchestration_raw_as_fallback(
        self,
        service_with_orchestration: CheckpointService,
        mock_repository: MagicMock,
    ) -> None:
        """Structured result also includes orchestration_raw for full context."""
        fill = FillEstimate(fill_percentage=0.82, tier=ThresholdTier.CRITICAL)
        result = service_with_orchestration.create_checkpoint(
            context_state=fill, trigger="pre_compact"
        )
        state = result.resumption_state
        assert state is not None
        assert "orchestration_raw" in state
        assert "workflow:" in state["orchestration_raw"]

    def test_falls_back_to_raw_on_malformed_yaml(
        self,
        mock_repository: MagicMock,
        tmp_path: Path,
    ) -> None:
        """When YAML parsing fails, falls back to raw content string."""
        orchestration_path = tmp_path / "ORCHESTRATION.yaml"
        orchestration_path.write_text("{{invalid yaml: [", encoding="utf-8")
        service = CheckpointService(
            repository=mock_repository,
            orchestration_path=orchestration_path,
        )
        fill = FillEstimate(fill_percentage=0.82, tier=ThresholdTier.CRITICAL)
        result = service.create_checkpoint(context_state=fill, trigger="pre_compact")
        state = result.resumption_state
        assert state is not None
        assert "orchestration_raw" in state
        assert "invalid yaml" in state["orchestration_raw"]

    def test_falls_back_to_raw_on_non_dict_yaml(
        self,
        mock_repository: MagicMock,
        tmp_path: Path,
    ) -> None:
        """When YAML parses to non-dict (e.g. a list), falls back to raw."""
        orchestration_path = tmp_path / "ORCHESTRATION.yaml"
        orchestration_path.write_text("- item1\n- item2\n", encoding="utf-8")
        service = CheckpointService(
            repository=mock_repository,
            orchestration_path=orchestration_path,
        )
        fill = FillEstimate(fill_percentage=0.82, tier=ThresholdTier.CRITICAL)
        result = service.create_checkpoint(context_state=fill, trigger="pre_compact")
        state = result.resumption_state
        assert state is not None
        assert "orchestration_raw" in state

    def test_handles_empty_pipelines(
        self,
        mock_repository: MagicMock,
        tmp_path: Path,
    ) -> None:
        """When pipelines section is empty, no agent_statuses or current_phase."""
        orchestration_path = tmp_path / "ORCHESTRATION.yaml"
        orchestration_path.write_text(
            "workflow:\n  id: test\n  status: ACTIVE\npipelines: {}\n",
            encoding="utf-8",
        )
        service = CheckpointService(
            repository=mock_repository,
            orchestration_path=orchestration_path,
        )
        fill = FillEstimate(fill_percentage=0.82, tier=ThresholdTier.CRITICAL)
        result = service.create_checkpoint(context_state=fill, trigger="pre_compact")
        state = result.resumption_state
        assert state is not None
        assert "agent_statuses" not in state
        assert state["workflow_id"] == "test"

    def test_handles_missing_optional_sections(
        self,
        mock_repository: MagicMock,
        tmp_path: Path,
    ) -> None:
        """When optional sections (resumption, next_actions) are missing, no KeyError."""
        orchestration_path = tmp_path / "ORCHESTRATION.yaml"
        orchestration_path.write_text(
            "workflow:\n  id: minimal\n  status: PAUSED\n",
            encoding="utf-8",
        )
        service = CheckpointService(
            repository=mock_repository,
            orchestration_path=orchestration_path,
        )
        fill = FillEstimate(fill_percentage=0.50, tier=ThresholdTier.NOMINAL)
        result = service.create_checkpoint(context_state=fill, trigger="manual")
        state = result.resumption_state
        assert state is not None
        assert state["workflow_id"] == "minimal"
        assert state["workflow_status"] == "PAUSED"
        # quality_gate_state still present with empty defaults (resumption={} is valid dict)
        assert state["quality_gate_state"]["gates_completed"] == []
        assert state["quality_gate_state"]["gates_remaining"] == []


# =============================================================================
# BDD Scenario: TASK-003 Checkpoint write-back to ORCHESTRATION.yaml
# =============================================================================


class TestCheckpointWriteBack:
    """Scenario: CheckpointService writes checkpoint metadata back to ORCHESTRATION.yaml.

    TASK-003: After creating a checkpoint, the service updates the resumption
    section of ORCHESTRATION.yaml with checkpoint metadata.
    """

    def test_writes_checkpoint_id_to_recovery_state(
        self,
        service_with_orchestration: CheckpointService,
        mock_repository: MagicMock,
        tmp_path: Path,
    ) -> None:
        """Write-back includes last_checkpoint in recovery_state."""
        import yaml

        fill = FillEstimate(fill_percentage=0.85, tier=ThresholdTier.CRITICAL)
        service_with_orchestration.create_checkpoint(context_state=fill, trigger="pre_compact")
        orchestration_path = tmp_path / "ORCHESTRATION.yaml"
        data = yaml.safe_load(orchestration_path.read_text(encoding="utf-8"))
        recovery = data["resumption"]["recovery_state"]
        assert recovery["last_checkpoint"] == "cx-001"

    def test_writes_context_fill_to_recovery_state(
        self,
        service_with_orchestration: CheckpointService,
        mock_repository: MagicMock,
        tmp_path: Path,
    ) -> None:
        """Write-back includes context_fill_at_update in recovery_state."""
        import yaml

        fill = FillEstimate(fill_percentage=0.8512, tier=ThresholdTier.CRITICAL)
        service_with_orchestration.create_checkpoint(context_state=fill, trigger="pre_compact")
        orchestration_path = tmp_path / "ORCHESTRATION.yaml"
        data = yaml.safe_load(orchestration_path.read_text(encoding="utf-8"))
        recovery = data["resumption"]["recovery_state"]
        assert recovery["context_fill_at_update"] == 0.8512

    def test_writes_updated_at_to_recovery_state(
        self,
        service_with_orchestration: CheckpointService,
        mock_repository: MagicMock,
        tmp_path: Path,
    ) -> None:
        """Write-back includes updated_at timestamp in recovery_state."""
        import yaml

        fill = FillEstimate(fill_percentage=0.85, tier=ThresholdTier.CRITICAL)
        service_with_orchestration.create_checkpoint(context_state=fill, trigger="pre_compact")
        orchestration_path = tmp_path / "ORCHESTRATION.yaml"
        data = yaml.safe_load(orchestration_path.read_text(encoding="utf-8"))
        recovery = data["resumption"]["recovery_state"]
        assert "updated_at" in recovery
        assert len(recovery["updated_at"]) > 0

    def test_increments_compaction_events_count(
        self,
        service_with_orchestration: CheckpointService,
        mock_repository: MagicMock,
        tmp_path: Path,
    ) -> None:
        """Write-back increments compaction_events.count from 0 to 1."""
        import yaml

        fill = FillEstimate(fill_percentage=0.85, tier=ThresholdTier.CRITICAL)
        service_with_orchestration.create_checkpoint(context_state=fill, trigger="pre_compact")
        orchestration_path = tmp_path / "ORCHESTRATION.yaml"
        data = yaml.safe_load(orchestration_path.read_text(encoding="utf-8"))
        compaction = data["resumption"]["compaction_events"]
        assert compaction["count"] == 1

    def test_appends_compaction_event_entry(
        self,
        service_with_orchestration: CheckpointService,
        mock_repository: MagicMock,
        tmp_path: Path,
    ) -> None:
        """Write-back appends event entry with checkpoint_id, fill, tier, timestamp."""
        import yaml

        fill = FillEstimate(fill_percentage=0.85, tier=ThresholdTier.CRITICAL)
        service_with_orchestration.create_checkpoint(context_state=fill, trigger="pre_compact")
        orchestration_path = tmp_path / "ORCHESTRATION.yaml"
        data = yaml.safe_load(orchestration_path.read_text(encoding="utf-8"))
        events = data["resumption"]["compaction_events"]["events"]
        assert len(events) == 1
        event = events[0]
        assert event["checkpoint_id"] == "cx-001"
        assert event["fill_percentage"] == 0.85
        assert event["tier"] == "CRITICAL"
        assert "timestamp" in event

    def test_write_back_fail_open_when_no_orchestration(
        self,
        service_without_orchestration: CheckpointService,
        mock_repository: MagicMock,
    ) -> None:
        """Write-back does not raise when ORCHESTRATION.yaml is missing."""
        fill = FillEstimate(fill_percentage=0.85, tier=ThresholdTier.CRITICAL)
        # Should not raise
        result = service_without_orchestration.create_checkpoint(
            context_state=fill, trigger="pre_compact"
        )
        assert result is not None

    def test_write_back_preserves_existing_data(
        self,
        service_with_orchestration: CheckpointService,
        mock_repository: MagicMock,
        tmp_path: Path,
    ) -> None:
        """Write-back preserves existing ORCHESTRATION.yaml content."""
        import yaml

        fill = FillEstimate(fill_percentage=0.85, tier=ThresholdTier.CRITICAL)
        service_with_orchestration.create_checkpoint(context_state=fill, trigger="pre_compact")
        orchestration_path = tmp_path / "ORCHESTRATION.yaml"
        data = yaml.safe_load(orchestration_path.read_text(encoding="utf-8"))
        # Original workflow data preserved
        assert data["workflow"]["id"] == "feat001-impl-20260220-001"
        assert data["workflow"]["name"] == "FEAT-001 Implementation"
        # Original quality trajectory preserved
        assert data["resumption"]["quality_trajectory"]["current_gate"] == "QG-2"

    def test_write_back_with_no_path_configured(
        self,
        mock_repository: MagicMock,
    ) -> None:
        """Write-back is a no-op when orchestration_path is None."""
        service = CheckpointService(
            repository=mock_repository,
            orchestration_path=None,
        )
        fill = FillEstimate(fill_percentage=0.85, tier=ThresholdTier.CRITICAL)
        result = service.create_checkpoint(context_state=fill, trigger="pre_compact")
        assert result is not None
        assert result.resumption_state is None
