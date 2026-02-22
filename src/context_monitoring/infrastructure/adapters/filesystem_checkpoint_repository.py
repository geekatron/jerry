# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
FilesystemCheckpointRepository - Filesystem-backed checkpoint persistence.

Implements ICheckpointRepository using the filesystem for checkpoint
storage. Each checkpoint is stored as a JSON file with the naming
convention ``{checkpoint_id}.json`` (e.g., cx-001.json).

Acknowledgment is tracked via ``.acknowledged`` marker files alongside
the checkpoint JSON files.

Sequential IDs follow the pattern cx-NNN (cx-001, cx-002, ...).

Uses AtomicFileAdapter for crash-safe file operations.

References:
    - EN-003: Context Monitoring Bounded Context Foundation
    - FEAT-002: Checkpoint Management
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

from src.context_monitoring.domain.value_objects.checkpoint_data import CheckpointData
from src.context_monitoring.domain.value_objects.fill_estimate import FillEstimate
from src.context_monitoring.domain.value_objects.threshold_tier import ThresholdTier
from src.infrastructure.adapters.persistence.atomic_file_adapter import AtomicFileAdapter

logger = logging.getLogger(__name__)


class FilesystemCheckpointRepository:
    """Filesystem-backed checkpoint repository.

    Stores checkpoints as JSON files in the configured directory.
    Uses AtomicFileAdapter for crash-safe writes and sequential
    checkpoint ID generation (cx-001, cx-002, ...).

    Attributes:
        checkpoint_dir: Directory for checkpoint files
        file_adapter: AtomicFileAdapter for safe file operations

    Example:
        >>> adapter = AtomicFileAdapter()
        >>> repo = FilesystemCheckpointRepository(
        ...     checkpoint_dir=Path(".jerry/checkpoints"),
        ...     file_adapter=adapter,
        ... )
        >>> repo.save(checkpoint_data)
    """

    def __init__(
        self,
        checkpoint_dir: Path,
        file_adapter: AtomicFileAdapter,
    ) -> None:
        """Initialize the repository.

        Args:
            checkpoint_dir: Directory for storing checkpoint JSON files.
            file_adapter: AtomicFileAdapter for crash-safe file operations.
        """
        self._checkpoint_dir = checkpoint_dir
        self._file_adapter = file_adapter

    def save(self, checkpoint: CheckpointData) -> None:
        """Persist a checkpoint as a JSON file.

        Creates the checkpoint directory if it does not exist.

        Args:
            checkpoint: The CheckpointData to persist.
        """
        self._checkpoint_dir.mkdir(parents=True, exist_ok=True)
        file_path = self._checkpoint_dir / f"{checkpoint.checkpoint_id}.json"
        data = self._serialize(checkpoint)
        content = json.dumps(data, indent=2, ensure_ascii=False)
        self._file_adapter.write_atomic(file_path, content)
        logger.debug("Saved checkpoint %s to %s", checkpoint.checkpoint_id, file_path)

    def get_latest_unacknowledged(self) -> CheckpointData | None:
        """Get the most recent unacknowledged checkpoint.

        Returns:
            The latest CheckpointData that has not been acknowledged,
            or None if no unacknowledged checkpoints exist.
        """
        checkpoints = self._load_all_sorted()
        for cp in reversed(checkpoints):
            if not self._is_acknowledged(cp.checkpoint_id):
                return cp
        return None

    def acknowledge(self, checkpoint_id: str) -> None:
        """Mark a checkpoint as acknowledged by creating a marker file.

        Args:
            checkpoint_id: The ID of the checkpoint to acknowledge.
        """
        self._checkpoint_dir.mkdir(parents=True, exist_ok=True)
        marker_path = self._checkpoint_dir / f"{checkpoint_id}.acknowledged"
        self._file_adapter.write_atomic(marker_path, "")
        logger.debug("Acknowledged checkpoint %s", checkpoint_id)

    def list_all(self) -> list[CheckpointData]:
        """List all checkpoints (acknowledged and unacknowledged).

        Returns:
            List of all CheckpointData instances, ordered by checkpoint ID.
        """
        return self._load_all_sorted()

    def next_checkpoint_id(self) -> str:
        """Generate the next sequential checkpoint ID.

        Scans existing checkpoint files to determine the next number.

        Returns:
            The next checkpoint ID (e.g., cx-001, cx-002).
        """
        existing = self._get_existing_ids()
        if not existing:
            return "cx-001"

        max_num = max(self._parse_id_number(cid) for cid in existing)
        return f"cx-{max_num + 1:03d}"

    def _get_existing_ids(self) -> list[str]:
        """Get list of existing checkpoint IDs from filesystem.

        Returns:
            List of checkpoint ID strings.
        """
        if not self._checkpoint_dir.exists():
            return []

        ids = []
        for path in self._checkpoint_dir.glob("cx-*.json"):
            checkpoint_id = path.stem
            ids.append(checkpoint_id)
        return sorted(ids)

    def _parse_id_number(self, checkpoint_id: str) -> int:
        """Extract the numeric part from a checkpoint ID.

        Args:
            checkpoint_id: Checkpoint ID (e.g., cx-001).

        Returns:
            The numeric part as an integer.
        """
        # cx-001 -> 001 -> 1
        return int(checkpoint_id.split("-", 1)[1])

    def _is_acknowledged(self, checkpoint_id: str) -> bool:
        """Check if a checkpoint has been acknowledged.

        Args:
            checkpoint_id: The checkpoint ID to check.

        Returns:
            True if the .acknowledged marker file exists.
        """
        marker_path = self._checkpoint_dir / f"{checkpoint_id}.acknowledged"
        return marker_path.exists()

    def _load_all_sorted(self) -> list[CheckpointData]:
        """Load all checkpoint files, sorted by ID.

        Returns:
            List of CheckpointData instances, sorted by checkpoint ID.
        """
        if not self._checkpoint_dir.exists():
            return []

        checkpoints = []
        for path in sorted(self._checkpoint_dir.glob("cx-*.json")):
            try:
                content = self._file_adapter.read_with_lock(path)
                if content:
                    data = json.loads(content)
                    cp = self._deserialize(data)
                    checkpoints.append(cp)
            except (json.JSONDecodeError, KeyError, ValueError) as exc:
                logger.warning("Failed to load checkpoint %s: %s", path, exc)
        return checkpoints

    def _serialize(self, checkpoint: CheckpointData) -> dict:
        """Serialize CheckpointData to a dict for JSON storage.

        Args:
            checkpoint: The CheckpointData to serialize.

        Returns:
            Dictionary representation for JSON.
        """
        return {
            "checkpoint_id": checkpoint.checkpoint_id,
            "context_state": {
                "fill_percentage": checkpoint.context_state.fill_percentage,
                "tier": checkpoint.context_state.tier.value,
                "token_count": checkpoint.context_state.token_count,
                "monitoring_ok": checkpoint.context_state.monitoring_ok,
                "context_window": checkpoint.context_state.context_window,
                "context_window_source": checkpoint.context_state.context_window_source,
            },
            "resumption_state": checkpoint.resumption_state,
            "created_at": checkpoint.created_at,
        }

    def _deserialize(self, data: dict) -> CheckpointData:
        """Deserialize a dict from JSON storage to CheckpointData.

        Args:
            data: Dictionary from JSON file.

        Returns:
            Reconstructed CheckpointData instance.
        """
        context_data = data["context_state"]
        context_state = FillEstimate(
            fill_percentage=context_data["fill_percentage"],
            tier=ThresholdTier(context_data["tier"]),
            token_count=context_data.get("token_count"),
            monitoring_ok=context_data.get("monitoring_ok", True),
            context_window=context_data.get("context_window", 200_000),
            context_window_source=context_data.get("context_window_source", "default"),
        )
        return CheckpointData(
            checkpoint_id=data["checkpoint_id"],
            context_state=context_state,
            resumption_state=data.get("resumption_state"),
            created_at=data["created_at"],
        )
