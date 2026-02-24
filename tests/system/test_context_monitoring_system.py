# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
System tests for context_monitoring bounded context.

Tests verify component interaction across the full monitoring pipeline:
    - Estimator → CheckpointService → Repository → ResumptionGenerator
    - Pre-compact → checkpoint creation → session-start → resumption injection
    - Full monitoring lifecycle with real filesystem I/O
    - Checkpoint roundtrip fidelity with all FillEstimate fields

Test Distribution:
    - Happy Path (60%): 8 tests
    - Negative (30%): 3 tests
    - Edge (10%): 1 test

Acceptance Criteria Coverage:
    - AC-FEAT001-001: Token counting through full pipeline
    - AC-FEAT001-002: Tier classification progression
    - AC-FEAT001-003: XML tag generation from real estimates
    - AC-FEAT001-004: Checkpoint lifecycle (create → persist → retrieve → acknowledge)
    - AC-FEAT001-005: Fail-open XML tag (monitoring-ok=false)
    - AC-FEAT001-006: Resumption context from real checkpoint + ORCHESTRATION.yaml

References:
    - FEAT-001: Context Detection (EN-003, EN-004)
    - PROJ-004: Context Resilience
    - H-07: Composition root exclusivity (note: system tests wire manually
      because the production bootstrap requires a full project environment;
      composition root testing is covered by E2E tests via the actual CLI)
"""

from __future__ import annotations

from pathlib import Path
from typing import NamedTuple

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
from src.context_monitoring.domain.value_objects.fill_estimate import FillEstimate
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


class SystemComponents(NamedTuple):
    """Typed container for system test component wiring."""

    estimator: ContextFillEstimator
    checkpoint_service: CheckpointService
    checkpoint_repo: FilesystemCheckpointRepository
    resumption_generator: ResumptionContextGenerator
    threshold_config: ConfigThresholdAdapter
    tmp_path: Path


pytestmark = [
    pytest.mark.system,
    pytest.mark.integration,  # system tests are a superset of integration
]


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture()
def system_components(tmp_path: Path) -> SystemComponents:
    """Wire all real context_monitoring components together.

    Note: Manual wiring is used instead of the production composition root
    (src/bootstrap.py) because bootstrap requires a full project environment
    with CLI context. E2E tests exercise the composition root via `jerry` CLI.

    Returns a typed NamedTuple for IDE support and self-documentation.
    """
    # Infrastructure (lock_dir scoped to tmp_path for test isolation)
    file_adapter = AtomicFileAdapter(lock_dir=tmp_path / "locks")
    checkpoint_dir = tmp_path / "checkpoints"

    # Configuration
    layered = LayeredConfigAdapter(
        env_prefix="JERRY_",
        root_config_path=tmp_path / "config.toml",
        defaults={
            "context_monitor.nominal_threshold": 0.55,
            "context_monitor.warning_threshold": 0.70,
            "context_monitor.critical_threshold": 0.80,
            "context_monitor.emergency_threshold": 0.88,
            "context_monitor.compaction_detection_threshold": 10000,
            "context_monitor.enabled": True,
        },
    )
    threshold_config = ConfigThresholdAdapter(config=layered)

    # Application services
    reader = JsonlTranscriptReader()
    estimator = ContextFillEstimator(reader=reader, threshold_config=threshold_config)
    repo = FilesystemCheckpointRepository(
        checkpoint_dir=checkpoint_dir,
        file_adapter=file_adapter,
    )
    checkpoint_service = CheckpointService(repository=repo)
    resumption_generator = ResumptionContextGenerator()

    return SystemComponents(
        estimator=estimator,
        checkpoint_service=checkpoint_service,
        checkpoint_repo=repo,
        resumption_generator=resumption_generator,
        threshold_config=threshold_config,
        tmp_path=tmp_path,
    )


# =============================================================================
# Full Pipeline: Estimate → Checkpoint → Resumption
# =============================================================================


class TestFullMonitoringPipeline:
    """System: Full monitoring pipeline from transcript to resumption context.

    References: FEAT-001 (EN-003, EN-004), PROJ-004
    """

    def test_estimate_checkpoint_resume_lifecycle(
        self, system_components: SystemComponents, create_transcript
    ) -> None:
        """Full lifecycle: estimate → checkpoint → persist → resume."""
        estimator = system_components.estimator
        checkpoint_service = system_components.checkpoint_service
        checkpoint_repo = system_components.checkpoint_repo
        resumption_gen = system_components.resumption_generator
        tmp_path = system_components.tmp_path

        # Step 1: Estimate context fill from real transcript
        transcript = create_transcript(tmp_path / "session.jsonl", 170_000)
        estimate = estimator.estimate(str(transcript))
        assert estimate.tier == ThresholdTier.CRITICAL
        assert estimate.monitoring_ok is True

        # Step 2: Create checkpoint from estimate
        checkpoint = checkpoint_service.create_checkpoint(estimate, "pre-compact")
        assert checkpoint.checkpoint_id == "cx-001"
        assert checkpoint.context_state.tier == ThresholdTier.CRITICAL

        # Step 3: Verify checkpoint persisted to filesystem
        persisted = checkpoint_repo.get_latest_unacknowledged()
        assert persisted is not None
        assert persisted.checkpoint_id == "cx-001"
        assert persisted.context_state.fill_percentage == pytest.approx(0.85)

        # Step 4: Generate resumption context (empty without orchestration)
        xml = resumption_gen.generate(checkpoint)
        # Without orchestration_path, resumption_state is None -> empty string
        assert xml == ""

    def test_multiple_checkpoints_returns_latest(self, system_components: SystemComponents) -> None:
        """Multiple checkpoints: get_latest_unacknowledged returns the most recent."""
        checkpoint_service = system_components.checkpoint_service
        checkpoint_repo = system_components.checkpoint_repo

        fill_low = FillEstimate(fill_percentage=0.5, tier=ThresholdTier.NOMINAL)
        fill_high = FillEstimate(
            fill_percentage=0.9, tier=ThresholdTier.EMERGENCY, token_count=180_000
        )

        checkpoint_service.create_checkpoint(fill_low, "test")
        checkpoint_service.create_checkpoint(fill_high, "test")

        latest = checkpoint_repo.get_latest_unacknowledged()
        assert latest is not None
        assert latest.checkpoint_id == "cx-002"
        assert latest.context_state.tier == ThresholdTier.EMERGENCY

    def test_acknowledge_then_get_returns_previous(
        self, system_components: SystemComponents
    ) -> None:
        """After acknowledging latest, get_latest returns previous checkpoint."""
        checkpoint_service = system_components.checkpoint_service
        checkpoint_repo = system_components.checkpoint_repo

        fill = FillEstimate(fill_percentage=0.5, tier=ThresholdTier.NOMINAL)
        checkpoint_service.create_checkpoint(fill, "test")
        checkpoint_service.create_checkpoint(fill, "test")

        checkpoint_repo.acknowledge("cx-002")
        latest = checkpoint_repo.get_latest_unacknowledged()
        assert latest is not None
        assert latest.checkpoint_id == "cx-001"

    def test_checkpoint_preserves_all_fill_estimate_fields(
        self, system_components: SystemComponents, create_transcript
    ) -> None:
        """Full pipeline preserves monitoring_ok, context_window, context_window_source."""
        estimator = system_components.estimator
        checkpoint_service = system_components.checkpoint_service
        checkpoint_repo = system_components.checkpoint_repo
        tmp_path = system_components.tmp_path

        transcript = create_transcript(tmp_path / "t.jsonl", 150_000)
        estimate = estimator.estimate(str(transcript))

        # Verify estimate has real context_window values from config
        assert estimate.context_window == 200_000
        assert estimate.context_window_source == "default"
        assert estimate.monitoring_ok is True

        checkpoint_service.create_checkpoint(estimate, "test")
        retrieved = checkpoint_repo.get_latest_unacknowledged()

        assert retrieved is not None
        assert retrieved.context_state.monitoring_ok is True
        assert retrieved.context_state.context_window == 200_000
        assert retrieved.context_state.context_window_source == "default"


# =============================================================================
# Checkpoint with Orchestration State
# =============================================================================


class TestCheckpointWithOrchestration:
    """System: Checkpoint captures ORCHESTRATION.yaml when present.

    References: FEAT-001 (EN-003), PROJ-004
    """

    def test_checkpoint_includes_orchestration_state(self, tmp_path: Path) -> None:
        """Checkpoint includes orchestration state from real YAML file."""
        # Create ORCHESTRATION.yaml
        orch_path = tmp_path / "ORCHESTRATION.yaml"
        orch_content = "workflow:\n  id: test-workflow-001\n  status: ACTIVE\n"
        orch_path.write_text(orch_content)

        # Wire components with orchestration path
        repo = FilesystemCheckpointRepository(
            checkpoint_dir=tmp_path / "checkpoints",
            file_adapter=AtomicFileAdapter(lock_dir=tmp_path / "locks"),
        )
        service = CheckpointService(
            repository=repo,
            orchestration_path=orch_path,
        )
        generator = ResumptionContextGenerator()

        # Create checkpoint
        fill = FillEstimate(
            fill_percentage=0.85,
            tier=ThresholdTier.CRITICAL,
            token_count=170_000,
        )
        checkpoint = service.create_checkpoint(fill, "pre-compact")

        # Verify resumption state captured
        assert checkpoint.resumption_state is not None
        assert "orchestration_raw" in checkpoint.resumption_state

        # Verify resumption XML generated
        xml = generator.generate(checkpoint)
        assert "<resumption-context>" in xml
        assert "<checkpoint-id>cx-001</checkpoint-id>" in xml
        assert "<recovery-state>" in xml

    def test_resumption_xml_reflects_context_state(self, tmp_path: Path) -> None:
        """Resumption XML contains fill percentage and tier from checkpoint context state."""
        orch_path = tmp_path / "ORCHESTRATION.yaml"
        orch_path.write_text("workflow:\n  id: wf-042\n  status: PAUSED\n")

        repo = FilesystemCheckpointRepository(
            checkpoint_dir=tmp_path / "checkpoints",
            file_adapter=AtomicFileAdapter(lock_dir=tmp_path / "locks"),
        )
        service = CheckpointService(
            repository=repo,
            orchestration_path=orch_path,
        )
        generator = ResumptionContextGenerator()

        fill = FillEstimate(
            fill_percentage=0.91,
            tier=ThresholdTier.EMERGENCY,
            token_count=182_000,
        )
        checkpoint = service.create_checkpoint(fill, "pre-compact")
        xml = generator.generate(checkpoint)

        # Verify context state values reflected in XML
        assert "<fill-percentage>0.9100</fill-percentage>" in xml
        assert "<tier>EMERGENCY</tier>" in xml
        assert "<checkpoint-id>cx-001</checkpoint-id>" in xml
        assert "<created-at>" in xml
        # Verify orchestration content propagated into recovery state
        assert "wf-042" in xml

    def test_missing_orchestration_still_creates_checkpoint(self, tmp_path: Path) -> None:
        """Checkpoint creation succeeds even when ORCHESTRATION.yaml is missing."""
        missing_path = tmp_path / "nonexistent" / "ORCHESTRATION.yaml"
        repo = FilesystemCheckpointRepository(
            checkpoint_dir=tmp_path / "checkpoints",
            file_adapter=AtomicFileAdapter(lock_dir=tmp_path / "locks"),
        )
        service = CheckpointService(
            repository=repo,
            orchestration_path=missing_path,
        )

        fill = FillEstimate(fill_percentage=0.5, tier=ThresholdTier.NOMINAL)
        checkpoint = service.create_checkpoint(fill, "test")

        assert checkpoint.checkpoint_id == "cx-001"
        assert checkpoint.resumption_state is None


# =============================================================================
# XML Tag Generation Pipeline
# =============================================================================


class TestXmlTagPipeline:
    """System: XML tag generation from real estimates.

    References: FEAT-001 (EN-004), PROJ-004
    """

    def test_xml_tag_reflects_real_estimate(
        self, system_components: SystemComponents, create_transcript
    ) -> None:
        """XML tag content matches real estimate values."""
        estimator = system_components.estimator
        tmp_path = system_components.tmp_path

        transcript = create_transcript(tmp_path / "t.jsonl", 145_000)
        estimate = estimator.estimate(str(transcript))
        tag = estimator.generate_context_monitor_tag(estimate)

        assert "<tier>WARNING</tier>" in tag
        assert "<token-count>145000</token-count>" in tag
        assert "<context-window>200000</context-window>" in tag
        assert "<context-window-source>default</context-window-source>" in tag
        assert "<monitoring-ok>true</monitoring-ok>" in tag
        assert "Consider checkpointing" in tag

    def test_fail_open_xml_tag_shows_monitoring_not_ok(
        self, system_components: SystemComponents
    ) -> None:
        """Fail-open estimate produces XML with monitoring-ok=false."""
        estimator = system_components.estimator

        result = estimator.estimate("/nonexistent.jsonl")
        tag = estimator.generate_context_monitor_tag(result)

        assert "<tier>NOMINAL</tier>" in tag
        assert "<monitoring-ok>false</monitoring-ok>" in tag
        assert "<token-count>N/A</token-count>" in tag


# =============================================================================
# Threshold Tier Progression
# =============================================================================


class TestTierProgression:
    """System: Verify tier progression as context fills across real components.

    References: FEAT-001 (EN-004), PROJ-004
    """

    def test_tier_progression_across_fill_levels(
        self, system_components: SystemComponents, create_transcript
    ) -> None:
        """Tiers progress correctly as fill increases through real pipeline."""
        estimator = system_components.estimator
        tmp_path = system_components.tmp_path

        test_cases = [
            (50_000, ThresholdTier.NOMINAL),  # 25%
            (115_000, ThresholdTier.LOW),  # 57.5%
            (145_000, ThresholdTier.WARNING),  # 72.5%
            (165_000, ThresholdTier.CRITICAL),  # 82.5%
            (180_000, ThresholdTier.EMERGENCY),  # 90%
        ]

        for i, (tokens, expected_tier) in enumerate(test_cases):
            transcript = create_transcript(tmp_path / f"t_{i}.jsonl", tokens)
            result = estimator.estimate(str(transcript))
            assert result.tier == expected_tier, (
                f"Expected {expected_tier} at {tokens} tokens, got {result.tier}"
            )


# =============================================================================
# Checkpoint List All
# =============================================================================


class TestCheckpointListAll:
    """System: Verify list_all returns complete checkpoint history.

    References: FEAT-001 (EN-003), PROJ-004
    """

    def test_list_all_returns_all_checkpoints(self, system_components: SystemComponents) -> None:
        """list_all returns both acknowledged and unacknowledged checkpoints."""
        checkpoint_service = system_components.checkpoint_service
        checkpoint_repo = system_components.checkpoint_repo

        fill = FillEstimate(fill_percentage=0.5, tier=ThresholdTier.NOMINAL)

        # Create 3 checkpoints, acknowledge the first
        checkpoint_service.create_checkpoint(fill, "test")
        checkpoint_service.create_checkpoint(fill, "test")
        checkpoint_service.create_checkpoint(fill, "test")
        checkpoint_repo.acknowledge("cx-001")

        all_checkpoints = checkpoint_repo.list_all()
        assert len(all_checkpoints) == 3
        ids = [c.checkpoint_id for c in all_checkpoints]
        assert ids == ["cx-001", "cx-002", "cx-003"]
