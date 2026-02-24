# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ICheckpointRepository - Port for checkpoint persistence.

This port defines the contract for persisting, retrieving, and
acknowledging checkpoint data. Implementations bridge to the
underlying storage mechanism (e.g., filesystem).

Operations:
    - save: Persist a checkpoint
    - get_latest_unacknowledged: Get the most recent unacknowledged checkpoint
    - acknowledge: Mark a checkpoint as acknowledged
    - list_all: List all checkpoints (acknowledged and unacknowledged)
    - next_checkpoint_id: Generate the next sequential checkpoint ID

References:
    - EN-003: Context Monitoring Bounded Context Foundation
    - FEAT-002: Checkpoint Management
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from src.context_monitoring.domain.value_objects.checkpoint_data import CheckpointData


@runtime_checkable
class ICheckpointRepository(Protocol):
    """Port for checkpoint persistence operations.

    This protocol defines the contract for persisting and retrieving
    checkpoint data. Implementations handle the storage mechanism.

    Example:
        >>> repo: ICheckpointRepository = FilesystemCheckpointRepository(...)
        >>> repo.save(checkpoint_data)
        >>> latest = repo.get_latest_unacknowledged()
    """

    def save(self, checkpoint: CheckpointData) -> None:
        """Persist a checkpoint.

        Args:
            checkpoint: The CheckpointData to persist.
        """
        ...

    def get_latest_unacknowledged(self) -> CheckpointData | None:
        """Get the most recent unacknowledged checkpoint.

        Returns:
            The latest CheckpointData that has not been acknowledged,
            or None if no unacknowledged checkpoints exist.
        """
        ...

    def acknowledge(self, checkpoint_id: str) -> None:
        """Mark a checkpoint as acknowledged.

        Args:
            checkpoint_id: The ID of the checkpoint to acknowledge.
        """
        ...

    def list_all(self) -> list[CheckpointData]:
        """List all checkpoints (acknowledged and unacknowledged).

        Returns:
            List of all CheckpointData instances, ordered by ID.
        """
        ...

    def next_checkpoint_id(self) -> str:
        """Generate the next sequential checkpoint ID.

        Returns:
            The next checkpoint ID in the sequence (e.g., cx-001, cx-002).
        """
        ...
