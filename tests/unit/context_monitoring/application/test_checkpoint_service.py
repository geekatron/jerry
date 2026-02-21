# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Unit tests for CheckpointService.

Tests cover BDD scenarios from EN-003:
    - CheckpointService creates checkpoint on pre-compact
    - CheckpointService is fail-open when ORCHESTRATION.yaml absent

References:
    - EN-003: Context Monitoring Bounded Context Foundation
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


@pytest.fixture()
def service_with_orchestration(mock_repository: MagicMock, tmp_path: Path) -> CheckpointService:
    """Create a CheckpointService with an ORCHESTRATION.yaml present."""
    orchestration_path = tmp_path / "ORCHESTRATION.yaml"
    orchestration_path.write_text(
        "current_phase: implementation\nentity_id: EN-003\n",
        encoding="utf-8",
    )
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
        # The resumption state should contain orchestration data
        assert "orchestration" in result.resumption_state

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
