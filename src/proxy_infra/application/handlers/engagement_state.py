# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""EngagementState value object (H-10: one class per file)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class EngagementState:
    """Mutable engagement lifecycle state.

    Tracks the current state in the 7-state engagement lifecycle
    and records the history of state transitions.

    Attributes:
        engagement_id: Unique engagement identifier.
        current_state: Current lifecycle state.
        mode: Engagement mode (purple, split, single).
        transitions: History of (from_state, to_state, timestamp) transitions.
    """

    engagement_id: str
    current_state: str = "DEFINED"
    mode: str = "single"
    transitions: list = field(default_factory=list)

    def transition_to(self, new_state: str) -> None:
        """Record a state transition.

        Args:
            new_state: The target state.
        """
        self.transitions.append({
            "from": self.current_state,
            "to": new_state,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        self.current_state = new_state
