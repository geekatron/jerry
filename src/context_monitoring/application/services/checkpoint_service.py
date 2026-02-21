# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
CheckpointService - Application service for checkpoint lifecycle.

Orchestrates checkpoint creation by:
1. Reading ORCHESTRATION.yaml for resumption state (fail-open)
2. Generating the next sequential checkpoint ID
3. Assembling CheckpointData with context state and metadata
4. Delegating persistence to the ICheckpointRepository

Fail-open behavior: If ORCHESTRATION.yaml is absent or unreadable,
the service proceeds without resumption state rather than failing.

References:
    - EN-003: Context Monitoring Bounded Context Foundation
    - FEAT-002: Checkpoint Management
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from src.context_monitoring.application.ports.checkpoint_repository import (
    ICheckpointRepository,
)
from src.context_monitoring.domain.value_objects.checkpoint_data import CheckpointData
from src.context_monitoring.domain.value_objects.fill_estimate import FillEstimate

logger = logging.getLogger(__name__)


class CheckpointService:
    """Application service for checkpoint lifecycle management.

    Orchestrates the creation of checkpoints by combining context state
    with optional ORCHESTRATION.yaml data and persisting via the
    repository port.

    Attributes:
        repository: The checkpoint repository for persistence
        orchestration_path: Path to ORCHESTRATION.yaml (optional)

    Example:
        >>> service = CheckpointService(
        ...     repository=filesystem_repo,
        ...     orchestration_path=Path("ORCHESTRATION.yaml"),
        ... )
        >>> cp = service.create_checkpoint(
        ...     context_state=fill_estimate,
        ...     trigger="pre_compact",
        ... )
    """

    def __init__(
        self,
        repository: ICheckpointRepository,
        orchestration_path: Path | None = None,
    ) -> None:
        """Initialize the CheckpointService.

        Args:
            repository: The checkpoint repository for persistence.
            orchestration_path: Path to ORCHESTRATION.yaml. If None or
                nonexistent, the service operates in fail-open mode.
        """
        self._repository = repository
        self._orchestration_path = orchestration_path

    def create_checkpoint(
        self,
        context_state: FillEstimate,
        trigger: str,
    ) -> CheckpointData:
        """Create and persist a new checkpoint.

        Reads ORCHESTRATION.yaml for resumption state (fail-open if absent),
        generates the next checkpoint ID, assembles CheckpointData, and
        persists via the repository.

        Args:
            context_state: Current context fill estimate.
            trigger: What triggered the checkpoint (e.g., "pre_compact", "manual").

        Returns:
            The created CheckpointData instance.
        """
        checkpoint_id = self._repository.next_checkpoint_id()
        resumption_state = self._build_resumption_state()
        created_at = datetime.now(UTC).isoformat()

        checkpoint = CheckpointData(
            checkpoint_id=checkpoint_id,
            context_state=context_state,
            resumption_state=resumption_state,
            created_at=created_at,
        )

        self._repository.save(checkpoint)
        logger.info(
            "Checkpoint %s created (trigger=%s, fill=%.2f)",
            checkpoint_id,
            trigger,
            context_state.fill_percentage,
        )

        return checkpoint

    def _build_resumption_state(self) -> dict[str, Any] | None:
        """Build resumption state from ORCHESTRATION.yaml.

        Reads the ORCHESTRATION.yaml file and returns its content
        as a dict under the 'orchestration' key. If the file is
        absent or unreadable, returns None (fail-open).

        Returns:
            Dict with orchestration data, or None if unavailable.
        """
        if self._orchestration_path is None:
            return None

        try:
            if not self._orchestration_path.exists():
                logger.debug(
                    "ORCHESTRATION.yaml not found at %s (fail-open)",
                    self._orchestration_path,
                )
                return None

            content = self._orchestration_path.read_text(encoding="utf-8")
            return {"orchestration": content}
        except (OSError, PermissionError) as exc:
            logger.warning(
                "Failed to read ORCHESTRATION.yaml at %s: %s (fail-open)",
                self._orchestration_path,
                exc,
            )
            return None
