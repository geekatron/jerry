# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
RotationAction - Graduated response action enumeration.

Represents the action Jerry recommends based on the current
context fill tier and aggressiveness configuration.

References:
    - FEAT-002: Status Line / Context Monitoring Unification
    - EN-009: Domain VOs + ContextEstimateComputer Service
    - DEC-003 D-006: Configurable aggressiveness
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

from enum import Enum


class RotationAction(Enum):
    """Graduated response action for context fill management.

    Ordered from least to most aggressive intervention. The action
    selected depends on the current ThresholdTier and the configured
    aggressiveness mode (conservative/moderate/aggressive).

    Attributes:
        NONE: No action needed. Context fill is healthy.
        LOG_WARNING: Log a warning. Context approaching limits.
        CHECKPOINT: Create a checkpoint of current state.
        REDUCE_VERBOSITY: Reduce output verbosity to conserve context.
        ROTATE: Recommend session rotation (/compact or /clear).
        EMERGENCY_HANDOFF: Force checkpoint and block further work
            until user takes action.

    Example:
        >>> action = RotationAction.CHECKPOINT
        >>> action.value
        'checkpoint'
    """

    NONE = "none"
    LOG_WARNING = "log_warning"
    CHECKPOINT = "checkpoint"
    REDUCE_VERBOSITY = "reduce_verbosity"
    ROTATE = "rotate"
    EMERGENCY_HANDOFF = "emergency_handoff"

    def __str__(self) -> str:
        """Return the action value as string."""
        return self.value
