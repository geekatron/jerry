# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ContextThresholdReached - Domain event for threshold crossing.

Emitted when the context window fill level crosses a threshold tier
boundary (e.g., from LOW to WARNING, or WARNING to CRITICAL).

Attributes:
    tier: The threshold tier that was reached (e.g., "warning", "critical")
    fill_percentage: The fill level when the threshold was crossed

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
class ContextThresholdReached(DomainEvent):
    """Event emitted when context fill crosses a threshold tier.

    Attributes:
        aggregate_id: Session or monitor identifier
        aggregate_type: Always "ContextMonitor"
        tier: The threshold tier reached (nominal, low, warning, critical, emergency)
        fill_percentage: Fill level at time of crossing (0.0 to 1.0)

    Example:
        >>> event = ContextThresholdReached(
        ...     aggregate_id="session-001",
        ...     aggregate_type="ContextMonitor",
        ...     tier="warning",
        ...     fill_percentage=0.72,
        ... )
    """

    tier: str = ""
    fill_percentage: float = 0.0

    def _payload(self) -> dict[str, Any]:
        """Return event-specific payload data."""
        return {
            "tier": self.tier,
            "fill_percentage": self.fill_percentage,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ContextThresholdReached:
        """Deserialize from dictionary.

        Args:
            data: Dictionary containing event fields.

        Returns:
            Reconstructed ContextThresholdReached instance.
        """
        timestamp_str = data.get("timestamp")
        timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else _current_timestamp()

        return cls(
            event_id=data.get("event_id", _generate_event_id()),
            aggregate_id=data["aggregate_id"],
            aggregate_type=data.get("aggregate_type", "ContextMonitor"),
            version=data.get("version", 1),
            timestamp=timestamp,
            tier=data.get("tier", ""),
            fill_percentage=data.get("fill_percentage", 0.0),
        )
