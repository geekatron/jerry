# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Multi-pattern orchestration validation tests.

TASK-005: Validates that CheckpointService correctly handles various
ORCHESTRATION.yaml patterns beyond the sequential pattern used during
PROJ-004 implementation:
    - Cross-pollinated pipeline pattern
    - Fan-out/fan-in pattern
    - Single-pipeline sequential pattern
    - Multi-pipeline with sync barriers
    - Minimal/sparse ORCHESTRATION.yaml

All tests use real CheckpointService + FilesystemCheckpointRepository
(no mocks) to verify end-to-end structured field extraction and
write-back across orchestration patterns.

References:
    - EN-008 TASK-005: Multi-pattern orchestration validation
    - EN-008 TASK-001: Structured checkpoint field extraction
    - EN-008 TASK-003: Checkpoint write-back
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from src.context_monitoring.application.services.checkpoint_service import (
    CheckpointService,
)
from src.context_monitoring.application.services.resumption_context_generator import (
    ResumptionContextGenerator,
)
from src.context_monitoring.domain.value_objects.fill_estimate import FillEstimate
from src.context_monitoring.domain.value_objects.threshold_tier import ThresholdTier
from src.context_monitoring.infrastructure.adapters.filesystem_checkpoint_repository import (
    FilesystemCheckpointRepository,
)
from src.infrastructure.adapters.persistence.atomic_file_adapter import (
    AtomicFileAdapter,
)

pytestmark = [
    pytest.mark.integration,
]


# =============================================================================
# ORCHESTRATION.yaml patterns
# =============================================================================

_CROSS_POLLINATED_YAML = """\
workflow:
  id: "feat001-impl-20260220-001"
  name: "Cross-Pollinated Implementation"
  status: "ACTIVE"
pipelines:
  pipeline_a:
    id: "pipeline-a"
    current_phase: 2
    phases:
      - id: 1
        name: "Research"
        status: "COMPLETE"
        agents:
          - id: "ps-researcher"
            status: "COMPLETE"
      - id: 2
        name: "Analysis"
        status: "IN_PROGRESS"
        agents:
          - id: "ps-analyst"
            status: "IN_PROGRESS"
  pipeline_b:
    id: "pipeline-b"
    current_phase: 1
    phases:
      - id: 1
        name: "Architecture"
        status: "IN_PROGRESS"
        agents:
          - id: "nse-architecture"
            status: "IN_PROGRESS"
          - id: "ps-architect"
            status: "PENDING"
cross_pollination:
  sync_points:
    - after_phase: 1
      pipelines: ["pipeline-a", "pipeline-b"]
      type: "barrier"
next_actions:
  immediate:
    - action: "Complete pipeline_a Phase 2"
    - action: "Complete pipeline_b Phase 1"
  subsequent:
    - action: "Cross-pollinate findings at sync barrier"
resumption:
  recovery_state:
    current_phase: 2
    workflow_status: "ACTIVE"
    updated_at: "2026-02-20T14:00:00+00:00"
  quality_trajectory:
    gates_completed: []
    gates_remaining: ["QG-1"]
    current_gate: "QG-1"
    total_iterations_used: 0
  compaction_events:
    count: 0
    events: []
"""

_FAN_OUT_FAN_IN_YAML = """\
workflow:
  id: "feat002-fanout-20260221-001"
  name: "Fan-Out/Fan-In Workflow"
  status: "ACTIVE"
pipelines:
  pipeline_research:
    id: "pipeline-research"
    current_phase: 1
    phases:
      - id: 1
        name: "Parallel Research"
        status: "IN_PROGRESS"
        agents:
          - id: "researcher-api"
            status: "COMPLETE"
          - id: "researcher-db"
            status: "IN_PROGRESS"
          - id: "researcher-ui"
            status: "COMPLETE"
  pipeline_synthesis:
    id: "pipeline-synthesis"
    current_phase: 0
    phases:
      - id: 1
        name: "Synthesis"
        status: "PENDING"
        agents:
          - id: "ps-synthesizer"
            status: "PENDING"
next_actions:
  immediate:
    - action: "Complete researcher-db"
  subsequent:
    - action: "Fan-in to synthesis pipeline"
resumption:
  recovery_state:
    current_phase: 1
    workflow_status: "ACTIVE"
    updated_at: "2026-02-21T09:00:00+00:00"
  quality_trajectory:
    gates_completed: []
    gates_remaining: ["QG-1", "QG-2"]
    current_gate: "QG-1"
    total_iterations_used: 0
  compaction_events:
    count: 0
    events: []
"""

_SINGLE_PIPELINE_YAML = """\
workflow:
  id: "simple-001"
  name: "Simple Sequential"
  status: "ACTIVE"
pipelines:
  main:
    id: "main"
    current_phase: 3
    phases:
      - id: 1
        name: "Design"
        status: "COMPLETE"
        agents:
          - id: "designer"
            status: "COMPLETE"
      - id: 2
        name: "Implement"
        status: "COMPLETE"
        agents:
          - id: "implementer"
            status: "COMPLETE"
      - id: 3
        name: "Test"
        status: "IN_PROGRESS"
        agents:
          - id: "tester"
            status: "IN_PROGRESS"
next_actions:
  immediate:
    - action: "Complete test phase"
resumption:
  recovery_state:
    current_phase: 3
    workflow_status: "ACTIVE"
    updated_at: "2026-02-21T10:00:00+00:00"
  quality_trajectory:
    gates_completed: ["QG-1", "QG-2"]
    gates_remaining: []
    current_gate: null
    total_iterations_used: 5
  compaction_events:
    count: 2
    events:
      - checkpoint_id: "cx-001"
        fill_percentage: 0.82
        tier: "CRITICAL"
        timestamp: "2026-02-21T08:00:00+00:00"
      - checkpoint_id: "cx-002"
        fill_percentage: 0.89
        tier: "EMERGENCY"
        timestamp: "2026-02-21T09:30:00+00:00"
"""

_MINIMAL_YAML = """\
workflow:
  id: "minimal-001"
  status: "ACTIVE"
"""


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture()
def _make_service(tmp_path: Path):
    """Factory for creating CheckpointService with a given YAML pattern."""

    def _create(
        yaml_content: str,
    ) -> tuple[CheckpointService, FilesystemCheckpointRepository, Path]:
        orchestration_path = tmp_path / "ORCHESTRATION.yaml"
        orchestration_path.write_text(yaml_content, encoding="utf-8")

        checkpoint_repo = FilesystemCheckpointRepository(
            checkpoint_dir=tmp_path / "checkpoints",
            file_adapter=AtomicFileAdapter(lock_dir=tmp_path / "locks"),
        )
        service = CheckpointService(
            repository=checkpoint_repo,
            orchestration_path=orchestration_path,
        )
        return service, checkpoint_repo, orchestration_path

    return _create


# =============================================================================
# Cross-pollinated pattern
# =============================================================================


class TestCrossPollinated:
    """Validates structured extraction from cross-pollinated orchestration."""

    def test_extracts_agents_from_both_pipelines(self, _make_service) -> None:
        """Agent statuses include agents from all pipelines."""
        service, _, _ = _make_service(_CROSS_POLLINATED_YAML)
        fill = FillEstimate(fill_percentage=0.85, tier=ThresholdTier.CRITICAL)
        cp = service.create_checkpoint(context_state=fill, trigger="pre_compact")

        state = cp.resumption_state
        assert state is not None
        agent_ids = {a["id"] for a in state["agent_statuses"]}
        assert "ps-researcher" in agent_ids
        assert "ps-analyst" in agent_ids
        assert "nse-architecture" in agent_ids
        assert "ps-architect" in agent_ids

    def test_uses_first_pipeline_current_phase(self, _make_service) -> None:
        """current_phase uses the first pipeline encountered (pipeline_a=2)."""
        service, _, _ = _make_service(_CROSS_POLLINATED_YAML)
        fill = FillEstimate(fill_percentage=0.85, tier=ThresholdTier.CRITICAL)
        cp = service.create_checkpoint(context_state=fill, trigger="pre_compact")

        state = cp.resumption_state
        assert state is not None
        assert state["current_phase"] == 2

    def test_multiple_next_actions_extracted(self, _make_service) -> None:
        """Multiple immediate next actions are all extracted."""
        service, _, _ = _make_service(_CROSS_POLLINATED_YAML)
        fill = FillEstimate(fill_percentage=0.85, tier=ThresholdTier.CRITICAL)
        cp = service.create_checkpoint(context_state=fill, trigger="pre_compact")

        state = cp.resumption_state
        assert state is not None
        assert len(state["next_actions"]) == 2

    def test_resumption_xml_includes_multi_pipeline_agents(self, _make_service) -> None:
        """Resumption XML renders agents from multiple pipelines."""
        service, _, _ = _make_service(_CROSS_POLLINATED_YAML)
        fill = FillEstimate(fill_percentage=0.85, tier=ThresholdTier.CRITICAL)
        cp = service.create_checkpoint(context_state=fill, trigger="pre_compact")

        generator = ResumptionContextGenerator()
        xml = generator.generate(cp)
        assert "<agent_statuses>" in xml
        assert "ps-researcher" in xml
        assert "nse-architecture" in xml

    def test_write_back_preserves_cross_pollination(self, _make_service) -> None:
        """Write-back preserves cross_pollination section in ORCHESTRATION.yaml."""
        service, _, orchestration_path = _make_service(_CROSS_POLLINATED_YAML)
        fill = FillEstimate(fill_percentage=0.85, tier=ThresholdTier.CRITICAL)
        service.create_checkpoint(context_state=fill, trigger="pre_compact")

        data = yaml.safe_load(orchestration_path.read_text(encoding="utf-8"))
        assert "cross_pollination" in data
        assert data["cross_pollination"]["sync_points"][0]["type"] == "barrier"


# =============================================================================
# Fan-out/fan-in pattern
# =============================================================================


class TestFanOutFanIn:
    """Validates structured extraction from fan-out/fan-in orchestration."""

    def test_extracts_parallel_agents(self, _make_service) -> None:
        """Fan-out agents are all captured in agent_statuses."""
        service, _, _ = _make_service(_FAN_OUT_FAN_IN_YAML)
        fill = FillEstimate(fill_percentage=0.82, tier=ThresholdTier.CRITICAL)
        cp = service.create_checkpoint(context_state=fill, trigger="pre_compact")

        state = cp.resumption_state
        assert state is not None
        agent_ids = {a["id"] for a in state["agent_statuses"]}
        assert "researcher-api" in agent_ids
        assert "researcher-db" in agent_ids
        assert "researcher-ui" in agent_ids
        assert "ps-synthesizer" in agent_ids

    def test_mixed_agent_statuses(self, _make_service) -> None:
        """Agents have correct mixed statuses (COMPLETE, IN_PROGRESS, PENDING)."""
        service, _, _ = _make_service(_FAN_OUT_FAN_IN_YAML)
        fill = FillEstimate(fill_percentage=0.82, tier=ThresholdTier.CRITICAL)
        cp = service.create_checkpoint(context_state=fill, trigger="pre_compact")

        state = cp.resumption_state
        assert state is not None
        status_map = {a["id"]: a["status"] for a in state["agent_statuses"]}
        assert status_map["researcher-api"] == "COMPLETE"
        assert status_map["researcher-db"] == "IN_PROGRESS"
        assert status_map["researcher-ui"] == "COMPLETE"
        assert status_map["ps-synthesizer"] == "PENDING"

    def test_quality_gate_state_with_multiple_remaining(self, _make_service) -> None:
        """Quality gate state with multiple remaining gates."""
        service, _, _ = _make_service(_FAN_OUT_FAN_IN_YAML)
        fill = FillEstimate(fill_percentage=0.82, tier=ThresholdTier.CRITICAL)
        cp = service.create_checkpoint(context_state=fill, trigger="pre_compact")

        state = cp.resumption_state
        assert state is not None
        qg = state["quality_gate_state"]
        assert qg["gates_remaining"] == ["QG-1", "QG-2"]


# =============================================================================
# Single-pipeline sequential pattern
# =============================================================================


class TestSinglePipelineSequential:
    """Validates structured extraction from single sequential pipeline."""

    def test_extracts_all_phases_agents(self, _make_service) -> None:
        """Agents from all phases (complete + in-progress) captured."""
        service, _, _ = _make_service(_SINGLE_PIPELINE_YAML)
        fill = FillEstimate(fill_percentage=0.85, tier=ThresholdTier.CRITICAL)
        cp = service.create_checkpoint(context_state=fill, trigger="pre_compact")

        state = cp.resumption_state
        assert state is not None
        agent_ids = {a["id"] for a in state["agent_statuses"]}
        assert "designer" in agent_ids
        assert "implementer" in agent_ids
        assert "tester" in agent_ids

    def test_quality_gate_with_completed_gates(self, _make_service) -> None:
        """Quality gate state with completed gates and high iteration count."""
        service, _, _ = _make_service(_SINGLE_PIPELINE_YAML)
        fill = FillEstimate(fill_percentage=0.85, tier=ThresholdTier.CRITICAL)
        cp = service.create_checkpoint(context_state=fill, trigger="pre_compact")

        state = cp.resumption_state
        assert state is not None
        qg = state["quality_gate_state"]
        assert qg["gates_completed"] == ["QG-1", "QG-2"]
        assert qg["gates_remaining"] == []
        assert qg["current_gate"] is None
        assert qg["total_iterations_used"] == 5

    def test_write_back_accumulates_with_existing_events(self, _make_service) -> None:
        """Write-back adds to existing compaction_events (count=2 → 3)."""
        service, _, orchestration_path = _make_service(_SINGLE_PIPELINE_YAML)
        fill = FillEstimate(fill_percentage=0.85, tier=ThresholdTier.CRITICAL)
        service.create_checkpoint(context_state=fill, trigger="pre_compact")

        data = yaml.safe_load(orchestration_path.read_text(encoding="utf-8"))
        compaction = data["resumption"]["compaction_events"]
        assert compaction["count"] == 3  # Was 2, incremented by 1
        assert len(compaction["events"]) == 3  # Was 2, appended 1


# =============================================================================
# Minimal/sparse pattern
# =============================================================================


class TestMinimalOrchestration:
    """Validates graceful handling of minimal ORCHESTRATION.yaml."""

    def test_minimal_yaml_extracts_workflow_id(self, _make_service) -> None:
        """Minimal YAML with only workflow section extracts workflow_id."""
        service, _, _ = _make_service(_MINIMAL_YAML)
        fill = FillEstimate(fill_percentage=0.82, tier=ThresholdTier.CRITICAL)
        cp = service.create_checkpoint(context_state=fill, trigger="pre_compact")

        state = cp.resumption_state
        assert state is not None
        assert state["workflow_id"] == "minimal-001"
        assert state["workflow_status"] == "ACTIVE"

    def test_minimal_yaml_no_agent_statuses(self, _make_service) -> None:
        """Minimal YAML without pipelines produces no agent_statuses."""
        service, _, _ = _make_service(_MINIMAL_YAML)
        fill = FillEstimate(fill_percentage=0.82, tier=ThresholdTier.CRITICAL)
        cp = service.create_checkpoint(context_state=fill, trigger="pre_compact")

        state = cp.resumption_state
        assert state is not None
        assert "agent_statuses" not in state

    def test_minimal_yaml_write_back_creates_resumption_section(self, _make_service) -> None:
        """Write-back creates resumption section when it doesn't exist."""
        service, _, orchestration_path = _make_service(_MINIMAL_YAML)
        fill = FillEstimate(fill_percentage=0.82, tier=ThresholdTier.CRITICAL)
        service.create_checkpoint(context_state=fill, trigger="pre_compact")

        data = yaml.safe_load(orchestration_path.read_text(encoding="utf-8"))
        assert "resumption" in data
        assert "recovery_state" in data["resumption"]
        recovery = data["resumption"]["recovery_state"]
        assert recovery["last_checkpoint"] == "cx-001"

    def test_minimal_yaml_resumption_xml_still_valid(self, _make_service) -> None:
        """Minimal YAML produces valid resumption XML."""
        service, _, _ = _make_service(_MINIMAL_YAML)
        fill = FillEstimate(fill_percentage=0.82, tier=ThresholdTier.CRITICAL)
        cp = service.create_checkpoint(context_state=fill, trigger="pre_compact")

        generator = ResumptionContextGenerator()
        xml = generator.generate(cp)
        assert "<resumption-context>" in xml
        assert "<workflow_id>minimal-001</workflow_id>" in xml
        assert "</resumption-context>" in xml
