# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ContextState - Cross-invocation context monitoring state.

Persisted between CLI invocations to enable compaction detection
and rotation action continuity.

References:
    - FEAT-002: Status Line / Context Monitoring Unification
    - EN-010: Application Port (IContextStateStore) + ContextEstimateService
    - DEC-004 D-004: Cross-invocation state via port
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ContextState:
    """Cross-invocation context monitoring state.

    Persisted between CLI invocations to enable compaction detection
    and rotation action continuity.

    Attributes:
        previous_tokens: Token count from previous invocation.
        previous_session_id: Session ID from previous invocation.
        last_tier: Last classified ThresholdTier name.
        last_rotation_action: Last rotation action name.
    """

    previous_tokens: int
    previous_session_id: str
    last_tier: str
    last_rotation_action: str
