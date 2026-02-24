# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Unit tests for FilesystemCheckpointRepository.

Tests cover BDD scenarios from EN-003:
    - Save and retrieve a checkpoint
    - Sequential checkpoint ID generation (cx-001, cx-002, ...)
    - Acknowledged checkpoints are excluded from get_latest_unacknowledged
    - Acknowledgment creates marker file
    - Checkpoint directory auto-created

References:
    - EN-003: Context Monitoring Bounded Context Foundation
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

from pathlib import Path

import pytest

from src.context_monitoring.domain.value_objects.checkpoint_data import CheckpointData
from src.context_monitoring.domain.value_objects.fill_estimate import FillEstimate
from src.context_monitoring.domain.value_objects.threshold_tier import ThresholdTier
from src.context_monitoring.infrastructure.adapters.filesystem_checkpoint_repository import (
    FilesystemCheckpointRepository,
)
from src.infrastructure.adapters.persistence.atomic_file_adapter import AtomicFileAdapter

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture()
def atomic_adapter(tmp_path: Path) -> AtomicFileAdapter:
    """Create an AtomicFileAdapter with a temporary lock directory."""
    lock_dir = tmp_path / "locks"
    return AtomicFileAdapter(lock_dir=lock_dir)


@pytest.fixture()
def checkpoint_dir(tmp_path: Path) -> Path:
    """Return a path for checkpoints (not yet created)."""
    return tmp_path / "checkpoints"


@pytest.fixture()
def repository(
    atomic_adapter: AtomicFileAdapter, checkpoint_dir: Path
) -> FilesystemCheckpointRepository:
    """Create a FilesystemCheckpointRepository."""
    return FilesystemCheckpointRepository(
        checkpoint_dir=checkpoint_dir,
        file_adapter=atomic_adapter,
    )


def _make_fill_estimate(
    fill_pct: float = 0.7, tier: ThresholdTier = ThresholdTier.WARNING
) -> FillEstimate:
    """Create a FillEstimate for testing."""
    return FillEstimate(fill_percentage=fill_pct, tier=tier)


def _make_checkpoint_data(
    checkpoint_id: str = "cx-001",
    fill_pct: float = 0.7,
    tier: ThresholdTier = ThresholdTier.WARNING,
    resumption_state: dict | None = None,
) -> CheckpointData:
    """Create a CheckpointData for testing."""
    return CheckpointData(
        checkpoint_id=checkpoint_id,
        context_state=_make_fill_estimate(fill_pct, tier),
        resumption_state=resumption_state,
        created_at="2026-02-20T10:00:00+00:00",
    )


# =============================================================================
# BDD Scenario: Checkpoint directory auto-created
# =============================================================================


class TestCheckpointDirectoryAutoCreated:
    """Scenario: Checkpoint directory auto-created.

    Given a checkpoint_dir that does not exist,
    saving a checkpoint should create the directory.
    """

    def test_directory_created_on_save(
        self, repository: FilesystemCheckpointRepository, checkpoint_dir: Path
    ) -> None:
        """Save creates the checkpoint directory if it doesn't exist."""
        assert not checkpoint_dir.exists()
        cp = _make_checkpoint_data()
        repository.save(cp)
        assert checkpoint_dir.exists()


# =============================================================================
# BDD Scenario: Save and retrieve a checkpoint
# =============================================================================


class TestSaveAndRetrieveCheckpoint:
    """Scenario: Save and retrieve a checkpoint.

    Given a saved checkpoint,
    it should be retrievable via get_latest_unacknowledged.
    """

    def test_save_and_retrieve(self, repository: FilesystemCheckpointRepository) -> None:
        """Saved checkpoint can be retrieved."""
        cp = _make_checkpoint_data(checkpoint_id="cx-001", fill_pct=0.72)
        repository.save(cp)
        latest = repository.get_latest_unacknowledged()
        assert latest is not None
        assert latest.checkpoint_id == "cx-001"
        assert latest.context_state.fill_percentage == 0.72

    def test_list_all_returns_saved(self, repository: FilesystemCheckpointRepository) -> None:
        """list_all returns all saved checkpoints."""
        cp1 = _make_checkpoint_data(checkpoint_id="cx-001")
        cp2 = _make_checkpoint_data(checkpoint_id="cx-002")
        repository.save(cp1)
        repository.save(cp2)
        all_cps = repository.list_all()
        assert len(all_cps) == 2
        ids = {cp.checkpoint_id for cp in all_cps}
        assert ids == {"cx-001", "cx-002"}

    def test_get_latest_returns_most_recent(
        self, repository: FilesystemCheckpointRepository
    ) -> None:
        """get_latest_unacknowledged returns the most recently saved checkpoint."""
        cp1 = _make_checkpoint_data(checkpoint_id="cx-001")
        cp2 = _make_checkpoint_data(checkpoint_id="cx-002")
        repository.save(cp1)
        repository.save(cp2)
        latest = repository.get_latest_unacknowledged()
        assert latest is not None
        assert latest.checkpoint_id == "cx-002"


# =============================================================================
# BDD Scenario: Sequential checkpoint ID generation
# =============================================================================


class TestSequentialCheckpointIdGeneration:
    """Scenario: Sequential checkpoint ID generation.

    Given an empty checkpoint directory,
    the repository should generate cx-001, cx-002, etc.
    """

    def test_next_id_starts_at_001(self, repository: FilesystemCheckpointRepository) -> None:
        """First generated ID is cx-001."""
        next_id = repository.next_checkpoint_id()
        assert next_id == "cx-001"

    def test_next_id_increments(self, repository: FilesystemCheckpointRepository) -> None:
        """IDs increment sequentially after saves."""
        cp1 = _make_checkpoint_data(checkpoint_id="cx-001")
        repository.save(cp1)
        next_id = repository.next_checkpoint_id()
        assert next_id == "cx-002"

    def test_next_id_after_multiple_saves(self, repository: FilesystemCheckpointRepository) -> None:
        """IDs continue incrementing with multiple saves."""
        for i in range(1, 4):
            cp = _make_checkpoint_data(checkpoint_id=f"cx-{i:03d}")
            repository.save(cp)
        next_id = repository.next_checkpoint_id()
        assert next_id == "cx-004"


# =============================================================================
# BDD Scenario: Acknowledged checkpoints are excluded
# =============================================================================


class TestAcknowledgedCheckpointsExcluded:
    """Scenario: Acknowledged checkpoints are excluded.

    Given a checkpoint that has been acknowledged,
    it should not be returned by get_latest_unacknowledged.
    """

    def test_acknowledged_excluded_from_latest(
        self, repository: FilesystemCheckpointRepository
    ) -> None:
        """Acknowledged checkpoint is not returned by get_latest_unacknowledged."""
        cp = _make_checkpoint_data(checkpoint_id="cx-001")
        repository.save(cp)
        repository.acknowledge("cx-001")
        latest = repository.get_latest_unacknowledged()
        assert latest is None

    def test_older_unacknowledged_returned_when_latest_acknowledged(
        self, repository: FilesystemCheckpointRepository
    ) -> None:
        """When latest is acknowledged, returns the next most recent unacknowledged."""
        cp1 = _make_checkpoint_data(checkpoint_id="cx-001")
        cp2 = _make_checkpoint_data(checkpoint_id="cx-002")
        repository.save(cp1)
        repository.save(cp2)
        repository.acknowledge("cx-002")
        latest = repository.get_latest_unacknowledged()
        assert latest is not None
        assert latest.checkpoint_id == "cx-001"


# =============================================================================
# BDD Scenario: Acknowledgment creates marker file
# =============================================================================


class TestAcknowledgmentMarkerFile:
    """Scenario: Acknowledgment creates marker file.

    Given an acknowledgment of a checkpoint,
    a .acknowledged marker file should be created.
    """

    def test_marker_file_created(
        self,
        repository: FilesystemCheckpointRepository,
        checkpoint_dir: Path,
    ) -> None:
        """Acknowledging a checkpoint creates a .acknowledged marker file."""
        cp = _make_checkpoint_data(checkpoint_id="cx-001")
        repository.save(cp)
        repository.acknowledge("cx-001")
        marker = checkpoint_dir / "cx-001.acknowledged"
        assert marker.exists()

    def test_acknowledged_still_in_list_all(
        self, repository: FilesystemCheckpointRepository
    ) -> None:
        """Acknowledged checkpoints still appear in list_all."""
        cp = _make_checkpoint_data(checkpoint_id="cx-001")
        repository.save(cp)
        repository.acknowledge("cx-001")
        all_cps = repository.list_all()
        assert len(all_cps) == 1

    def test_get_latest_returns_none_when_all_acknowledged(
        self, repository: FilesystemCheckpointRepository
    ) -> None:
        """get_latest_unacknowledged returns None when all are acknowledged."""
        cp = _make_checkpoint_data(checkpoint_id="cx-001")
        repository.save(cp)
        repository.acknowledge("cx-001")
        assert repository.get_latest_unacknowledged() is None


# =============================================================================
# BDD Scenario: Checkpoint with resumption state
# =============================================================================


class TestCheckpointWithResumptionState:
    """Scenario: Checkpoint with resumption state round-trips correctly."""

    def test_resumption_state_preserved(self, repository: FilesystemCheckpointRepository) -> None:
        """Resumption state dict is preserved through save and retrieve."""
        resumption = {"current_phase": "implementation", "entity_id": "EN-003"}
        cp = _make_checkpoint_data(checkpoint_id="cx-001", resumption_state=resumption)
        repository.save(cp)
        latest = repository.get_latest_unacknowledged()
        assert latest is not None
        assert latest.resumption_state == resumption
