# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
E2E integration test: Context exhaustion → checkpoint → resumption pipeline.

TASK-004: Automated E2E test exercising the full detection → checkpoint →
resumption lifecycle. Uses real components (no mocks) with temporary filesystem
state to validate the complete pipeline from context fill estimation through
checkpoint creation and resumption context generation.

Test flow:
    1. Create a JSONL transcript at EMERGENCY fill level
    2. Estimate context fill (ContextFillEstimator)
    3. Create checkpoint with ORCHESTRATION.yaml (CheckpointService)
    4. Verify checkpoint persisted (FilesystemCheckpointRepository)
    5. Generate resumption XML (ResumptionContextGenerator)
    6. Acknowledge checkpoint
    7. Verify acknowledged checkpoint excluded from next retrieval

References:
    - EN-008 TASK-004: Automated E2E integration test
    - FEAT-001: Context Detection
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

from pathlib import Path

import pytest

from src.context_monitoring.application.services.checkpoint_service import (
    CheckpointService,
)
from src.context_monitoring.application.services.context_fill_estimator import (
    ContextFillEstimator,
)
from src.context_monitoring.application.services.resumption_context_generator import (
    ResumptionContextGenerator,
)
from src.context_monitoring.domain.value_objects.threshold_tier import ThresholdTier
from src.context_monitoring.infrastructure.adapters.config_threshold_adapter import (
    ConfigThresholdAdapter,
)
from src.context_monitoring.infrastructure.adapters.filesystem_checkpoint_repository import (
    FilesystemCheckpointRepository,
)
from src.context_monitoring.infrastructure.adapters.jsonl_transcript_reader import (
    JsonlTranscriptReader,
)
from src.infrastructure.adapters.configuration.layered_config_adapter import (
    LayeredConfigAdapter,
)
from src.infrastructure.adapters.persistence.atomic_file_adapter import (
    AtomicFileAdapter,
)

pytestmark = [
    pytest.mark.integration,
]

_ORCHESTRATION_YAML = """\
workflow:
  id: "feat001-impl-20260220-001"
  name: "FEAT-001 Implementation"
  status: "ACTIVE"
pipelines:
  pipeline_a:
    id: "pipeline-a"
    current_phase: 2
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
    - action: "Complete Phase 2 agents"
  subsequent:
    - action: "Run quality gate QG-1"
resumption:
  recovery_state:
    current_phase: 2
    workflow_status: "ACTIVE"
    updated_at: "2026-02-20T10:00:00+00:00"
  quality_trajectory:
    gates_completed: []
    gates_remaining: ["QG-1", "QG-2"]
    current_gate: "QG-1"
    total_iterations_used: 0
  compaction_events:
    count: 0
    events: []
"""


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture()
def e2e_env(tmp_path: Path) -> dict[str, object]:
    """Create a full E2E environment with real components.

    Returns a dict with all components and paths needed for E2E testing.
    """
    # Config
    layered_config = LayeredConfigAdapter(
        env_prefix="JERRY_",
        root_config_path=tmp_path / "config.toml",
        defaults={
            "context_monitor.nominal_threshold": 0.55,
            "context_monitor.warning_threshold": 0.70,
            "context_monitor.critical_threshold": 0.80,
            "context_monitor.emergency_threshold": 0.88,
            "context_monitor.enabled": True,
        },
    )
    threshold_config = ConfigThresholdAdapter(config=layered_config)

    # Estimator
    transcript_reader = JsonlTranscriptReader()
    estimator = ContextFillEstimator(
        reader=transcript_reader,
        threshold_config=threshold_config,
    )

    # Checkpoint infrastructure
    checkpoint_dir = tmp_path / "checkpoints"
    file_adapter = AtomicFileAdapter(lock_dir=tmp_path / "locks")
    checkpoint_repo = FilesystemCheckpointRepository(
        checkpoint_dir=checkpoint_dir,
        file_adapter=file_adapter,
    )

    # ORCHESTRATION.yaml
    orchestration_path = tmp_path / "ORCHESTRATION.yaml"
    orchestration_path.write_text(_ORCHESTRATION_YAML, encoding="utf-8")

    # CheckpointService with orchestration
    checkpoint_service = CheckpointService(
        repository=checkpoint_repo,
        orchestration_path=orchestration_path,
    )

    # Resumption generator
    resumption_generator = ResumptionContextGenerator()

    return {
        "estimator": estimator,
        "checkpoint_service": checkpoint_service,
        "checkpoint_repo": checkpoint_repo,
        "resumption_generator": resumption_generator,
        "orchestration_path": orchestration_path,
        "tmp_path": tmp_path,
    }


# =============================================================================
# E2E Test: Full exhaust → checkpoint → resume pipeline
# =============================================================================


class TestContextExhaustionE2E:
    """E2E: Full detection → checkpoint → resumption lifecycle.

    Exercises the complete pipeline with real components and temporary
    filesystem state. No mocks.
    """

    def test_full_exhaust_checkpoint_resume_pipeline(
        self,
        e2e_env: dict[str, object],
        create_transcript,
    ) -> None:
        """Full pipeline: detect EMERGENCY → create checkpoint → generate resumption XML."""
        estimator: ContextFillEstimator = e2e_env["estimator"]  # type: ignore[assignment]
        checkpoint_service: CheckpointService = e2e_env["checkpoint_service"]  # type: ignore[assignment]
        checkpoint_repo: FilesystemCheckpointRepository = e2e_env["checkpoint_repo"]  # type: ignore[assignment]
        resumption_generator: ResumptionContextGenerator = e2e_env["resumption_generator"]  # type: ignore[assignment]
        tmp_path: Path = e2e_env["tmp_path"]  # type: ignore[assignment]

        # Step 1: Create transcript at EMERGENCY level
        transcript = create_transcript(tmp_path / "transcript.jsonl", 180_000)

        # Step 2: Estimate context fill
        estimate = estimator.estimate(str(transcript))
        assert estimate.tier == ThresholdTier.EMERGENCY
        assert estimate.fill_percentage == pytest.approx(0.90)
        assert estimate.monitoring_ok is True

        # Step 3: Create checkpoint (triggers TASK-001 structured extraction + TASK-003 write-back)
        checkpoint = checkpoint_service.create_checkpoint(
            context_state=estimate,
            trigger="pre_compact",
        )
        assert checkpoint.checkpoint_id == "cx-001"
        assert checkpoint.context_state.tier == ThresholdTier.EMERGENCY

        # Step 4: Verify structured resumption state (TASK-001)
        state = checkpoint.resumption_state
        assert state is not None
        assert state["workflow_id"] == "feat001-impl-20260220-001"
        assert state["current_phase"] == 2
        assert "agent_statuses" in state
        assert "quality_gate_state" in state
        assert "orchestration_raw" in state

        # Step 5: Verify checkpoint persisted
        retrieved = checkpoint_repo.get_latest_unacknowledged()
        assert retrieved is not None
        assert retrieved.checkpoint_id == "cx-001"

        # Step 6: Generate resumption XML
        xml = resumption_generator.generate(checkpoint)
        assert "<resumption-context>" in xml
        assert "<checkpoint-id>cx-001</checkpoint-id>" in xml
        assert "<tier>EMERGENCY</tier>" in xml
        assert "<recovery-state>" in xml
        # TASK-001: Structured fields in XML, not raw content
        assert "<workflow_id>" in xml
        assert "<current_phase>" in xml
        assert "orchestration_raw" not in xml

        # Step 7: Acknowledge and verify consumed
        checkpoint_repo.acknowledge("cx-001")
        assert checkpoint_repo.get_latest_unacknowledged() is None

    def test_write_back_updates_orchestration_yaml(
        self,
        e2e_env: dict[str, object],
        create_transcript,
    ) -> None:
        """TASK-003: Checkpoint write-back updates ORCHESTRATION.yaml in-place."""
        import yaml

        estimator: ContextFillEstimator = e2e_env["estimator"]  # type: ignore[assignment]
        checkpoint_service: CheckpointService = e2e_env["checkpoint_service"]  # type: ignore[assignment]
        orchestration_path: Path = e2e_env["orchestration_path"]  # type: ignore[assignment]
        tmp_path: Path = e2e_env["tmp_path"]  # type: ignore[assignment]

        transcript = create_transcript(tmp_path / "transcript.jsonl", 170_000)
        estimate = estimator.estimate(str(transcript))

        checkpoint_service.create_checkpoint(context_state=estimate, trigger="pre_compact")

        # Verify ORCHESTRATION.yaml was updated
        data = yaml.safe_load(orchestration_path.read_text(encoding="utf-8"))
        recovery = data["resumption"]["recovery_state"]
        assert recovery["last_checkpoint"] == "cx-001"
        assert recovery["context_fill_at_update"] == pytest.approx(0.85)
        compaction = data["resumption"]["compaction_events"]
        assert compaction["count"] == 1
        assert len(compaction["events"]) == 1

    def test_multiple_checkpoints_sequential(
        self,
        e2e_env: dict[str, object],
        create_transcript,
    ) -> None:
        """Multiple checkpoints get sequential IDs and accumulate compaction events."""
        import yaml

        estimator: ContextFillEstimator = e2e_env["estimator"]  # type: ignore[assignment]
        checkpoint_service: CheckpointService = e2e_env["checkpoint_service"]  # type: ignore[assignment]
        checkpoint_repo: FilesystemCheckpointRepository = e2e_env["checkpoint_repo"]  # type: ignore[assignment]
        orchestration_path: Path = e2e_env["orchestration_path"]  # type: ignore[assignment]
        tmp_path: Path = e2e_env["tmp_path"]  # type: ignore[assignment]

        # First checkpoint
        t1 = create_transcript(tmp_path / "t1.jsonl", 170_000)
        e1 = estimator.estimate(str(t1))
        c1 = checkpoint_service.create_checkpoint(context_state=e1, trigger="pre_compact")
        assert c1.checkpoint_id == "cx-001"
        checkpoint_repo.acknowledge("cx-001")

        # Second checkpoint
        t2 = create_transcript(tmp_path / "t2.jsonl", 180_000)
        e2 = estimator.estimate(str(t2))
        c2 = checkpoint_service.create_checkpoint(context_state=e2, trigger="pre_compact")
        assert c2.checkpoint_id == "cx-002"

        # Verify latest unacknowledged is cx-002
        latest = checkpoint_repo.get_latest_unacknowledged()
        assert latest is not None
        assert latest.checkpoint_id == "cx-002"

        # Verify compaction events accumulated
        data = yaml.safe_load(orchestration_path.read_text(encoding="utf-8"))
        compaction = data["resumption"]["compaction_events"]
        assert compaction["count"] == 2
        assert len(compaction["events"]) == 2

    def test_pipeline_without_orchestration_yaml(
        self,
        create_transcript,
        tmp_path: Path,
    ) -> None:
        """Pipeline works end-to-end without ORCHESTRATION.yaml (fail-open)."""
        # Create estimator
        layered = LayeredConfigAdapter(
            env_prefix="JERRY_",
            root_config_path=tmp_path / "config.toml",
            defaults={
                "context_monitor.nominal_threshold": 0.55,
                "context_monitor.warning_threshold": 0.70,
                "context_monitor.critical_threshold": 0.80,
                "context_monitor.emergency_threshold": 0.88,
                "context_monitor.enabled": True,
            },
        )
        config = ConfigThresholdAdapter(config=layered)
        estimator = ContextFillEstimator(
            reader=JsonlTranscriptReader(),
            threshold_config=config,
        )

        # Create checkpoint service without orchestration
        checkpoint_repo = FilesystemCheckpointRepository(
            checkpoint_dir=tmp_path / "checkpoints",
            file_adapter=AtomicFileAdapter(lock_dir=tmp_path / "locks"),
        )
        service = CheckpointService(repository=checkpoint_repo)
        generator = ResumptionContextGenerator()

        # Run pipeline
        transcript = create_transcript(tmp_path / "t.jsonl", 180_000)
        estimate = estimator.estimate(str(transcript))
        assert estimate.tier == ThresholdTier.EMERGENCY

        checkpoint = service.create_checkpoint(context_state=estimate, trigger="pre_compact")
        assert checkpoint.resumption_state is None

        xml = generator.generate(checkpoint)
        assert xml == ""

        # Checkpoint still persisted and retrievable
        retrieved = checkpoint_repo.get_latest_unacknowledged()
        assert retrieved is not None
        assert retrieved.checkpoint_id == "cx-001"


class TestContextExhaustionE2EEdgeCases:
    """E2E edge cases: boundary conditions and error recovery."""

    def test_checkpoint_at_exact_emergency_boundary(
        self,
        e2e_env: dict[str, object],
        create_transcript,
    ) -> None:
        """Checkpoint at exactly 0.88 fill classifies as EMERGENCY."""
        estimator: ContextFillEstimator = e2e_env["estimator"]  # type: ignore[assignment]
        checkpoint_service: CheckpointService = e2e_env["checkpoint_service"]  # type: ignore[assignment]
        tmp_path: Path = e2e_env["tmp_path"]  # type: ignore[assignment]

        # 0.88 * 200_000 = 176_000
        transcript = create_transcript(tmp_path / "boundary.jsonl", 176_000)
        estimate = estimator.estimate(str(transcript))
        assert estimate.tier == ThresholdTier.EMERGENCY

        checkpoint = checkpoint_service.create_checkpoint(
            context_state=estimate, trigger="pre_compact"
        )
        assert checkpoint.context_state.tier == ThresholdTier.EMERGENCY

    def test_fail_open_estimate_produces_nominal_checkpoint(
        self,
        e2e_env: dict[str, object],
    ) -> None:
        """When estimation fails open, checkpoint still captures NOMINAL state."""
        estimator: ContextFillEstimator = e2e_env["estimator"]  # type: ignore[assignment]
        checkpoint_service: CheckpointService = e2e_env["checkpoint_service"]  # type: ignore[assignment]
        resumption_generator: ResumptionContextGenerator = e2e_env["resumption_generator"]  # type: ignore[assignment]

        # Estimate with missing file -> fail-open NOMINAL
        estimate = estimator.estimate("/nonexistent/transcript.jsonl")
        assert estimate.monitoring_ok is False

        checkpoint = checkpoint_service.create_checkpoint(
            context_state=estimate, trigger="error_recovery"
        )
        assert checkpoint.context_state.tier == ThresholdTier.NOMINAL
        assert checkpoint.context_state.monitoring_ok is False

        # Resumption XML still generated (with orchestration state)
        xml = resumption_generator.generate(checkpoint)
        assert "<resumption-context>" in xml
        assert "<tier>NOMINAL</tier>" in xml
