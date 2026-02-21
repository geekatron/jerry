# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
CompactionDetected - Domain event for context compaction detection.

Emitted when a significant drop in token count is detected, indicating
that the LLM runtime has performed context compaction.

Attributes:
    previous_token_count: Token count before compaction
    current_token_count: Token count after compaction
    compaction_number: Sequential compaction number in this session

References:
    - EN-003: Context Monitoring Bounded Context Foundation
    - FEAT-001: Context Detection
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from src.shared_kernel.domain_event import DomainEvent, _current_timestamp, _generate_event_id


@dataclass(frozen=True)
class CompactionDetected(DomainEvent):
    """Event emitted when context compaction is detected.

    A compaction event is identified by a large drop in token count
    between consecutive measurements (exceeding the compaction detection
    threshold).

    Attributes:
        aggregate_id: Session or monitor identifier
        aggregate_type: Always "ContextMonitor"
        previous_token_count: Token count before compaction
        current_token_count: Token count after compaction
        compaction_number: Sequential compaction number in this session

    Example:
        >>> event = CompactionDetected(
        ...     aggregate_id="session-001",
        ...     aggregate_type="ContextMonitor",
        ...     previous_token_count=180000,
        ...     current_token_count=80000,
        ...     compaction_number=1,
        ... )
    """

    previous_token_count: int = 0
    current_token_count: int = 0
    compaction_number: int = 0

    def _payload(self) -> dict[str, Any]:
        """Return event-specific payload data."""
        return {
            "previous_token_count": self.previous_token_count,
            "current_token_count": self.current_token_count,
            "compaction_number": self.compaction_number,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CompactionDetected:
        """Deserialize from dictionary.

        Args:
            data: Dictionary containing event fields.

        Returns:
            Reconstructed CompactionDetected instance.
        """
        timestamp_str = data.get("timestamp")
        timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else _current_timestamp()

        return cls(
            event_id=data.get("event_id", _generate_event_id()),
            aggregate_id=data["aggregate_id"],
            aggregate_type=data.get("aggregate_type", "ContextMonitor"),
            version=data.get("version", 1),
            timestamp=timestamp,
            previous_token_count=data.get("previous_token_count", 0),
            current_token_count=data.get("current_token_count", 0),
            compaction_number=data.get("compaction_number", 0),
        )
