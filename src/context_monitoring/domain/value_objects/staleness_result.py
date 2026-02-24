# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
StalenessResult -- Value object for ORCHESTRATION.yaml staleness detection.

Represents the outcome of checking whether an ORCHESTRATION.yaml file's
``resumption.recovery_state.updated_at`` timestamp is stale relative to
a reference time (e.g., phase start time).

This is a domain value object -- it uses only Python stdlib types.
No external imports are permitted (H-07).

References:
    - EN-005: PreToolUse Staleness Detection
    - FEAT-002: Pre-Tool-Use Hooks
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StalenessResult:
    """Immutable result of an ORCHESTRATION.yaml staleness check.

    This frozen dataclass captures whether the ORCHESTRATION.yaml file's
    recovery state timestamp is stale relative to a reference time.

    A non-stale result (passthrough) has ``is_stale=False`` and all other
    fields as ``None``. A stale result has ``is_stale=True`` with a
    human-readable ``warning_message`` and diagnostic timestamps.

    Attributes:
        is_stale: Whether the ORCHESTRATION.yaml is considered stale.
        warning_message: Human-readable warning if stale, None otherwise.
        updated_at: The ``updated_at`` value from ORCHESTRATION.yaml (ISO 8601),
            or None if not available.
        reference_time: The reference time used for comparison (ISO 8601),
            or None if not applicable.

    Example:
        >>> # Passthrough (not stale)
        >>> result = StalenessResult(is_stale=False)
        >>> result.is_stale
        False

        >>> # Stale detection
        >>> result = StalenessResult(
        ...     is_stale=True,
        ...     warning_message="ORCHESTRATION.yaml is stale",
        ...     updated_at="2026-02-18T10:00:00Z",
        ...     reference_time="2026-02-19T08:00:00Z",
        ... )
        >>> result.is_stale
        True
    """

    is_stale: bool
    warning_message: str | None = None
    updated_at: str | None = None
    reference_time: str | None = None
