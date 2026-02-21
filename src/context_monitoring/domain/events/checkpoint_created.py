# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
CheckpointCreated - Domain event for checkpoint creation.

Emitted when a new checkpoint is created, typically before context
compaction to preserve resumption state.

Attributes:
    checkpoint_id: The sequential checkpoint ID (e.g., cx-001)
    trigger: What triggered the checkpoint (e.g., "pre_compact", "manual")

References:
    - EN-003: Context Monitoring Bounded Context Foundation
    - FEAT-002: Checkpoint Management
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from src.shared_kernel.domain_event import DomainEvent, _current_timestamp, _generate_event_id


@dataclass(frozen=True)
class CheckpointCreated(DomainEvent):
    """Event emitted when a checkpoint is created.

    Attributes:
        aggregate_id: Session or monitor identifier
        aggregate_type: Always "ContextMonitor"
        checkpoint_id: Sequential checkpoint ID (e.g., cx-001)
        trigger: What triggered the checkpoint creation

    Example:
        >>> event = CheckpointCreated(
        ...     aggregate_id="session-001",
        ...     aggregate_type="ContextMonitor",
        ...     checkpoint_id="cx-001",
        ...     trigger="pre_compact",
        ... )
    """

    checkpoint_id: str = ""
    trigger: str = ""

    def _payload(self) -> dict[str, Any]:
        """Return event-specific payload data."""
        return {
            "checkpoint_id": self.checkpoint_id,
            "trigger": self.trigger,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CheckpointCreated:
        """Deserialize from dictionary.

        Args:
            data: Dictionary containing event fields.

        Returns:
            Reconstructed CheckpointCreated instance.
        """
        timestamp_str = data.get("timestamp")
        timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else _current_timestamp()

        return cls(
            event_id=data.get("event_id", _generate_event_id()),
            aggregate_id=data["aggregate_id"],
            aggregate_type=data.get("aggregate_type", "ContextMonitor"),
            version=data.get("version", 1),
            timestamp=timestamp,
            checkpoint_id=data.get("checkpoint_id", ""),
            trigger=data.get("trigger", ""),
        )
