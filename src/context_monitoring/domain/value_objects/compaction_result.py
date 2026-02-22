# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
CompactionResult - Compaction detection result value object.

Immutable value object representing whether a compaction or /clear
event was detected by comparing current state to previous state.

References:
    - FEAT-002: Status Line / Context Monitoring Unification
    - EN-009: Domain VOs + ContextEstimateComputer Service
    - DEC-004 D-012: session_id tracking for compaction vs clear detection
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CompactionResult:
    """Result of compaction detection.

    Compaction is detected by a significant token count drop within
    the same session_id. A session_id change indicates ``/clear``
    (new session), not compaction.

    Attributes:
        detected: True if compaction was detected.
        from_tokens: Previous token count before compaction.
            Zero if no prior state exists.
        to_tokens: Current token count after compaction.
        session_id_changed: True if the session_id changed,
            indicating a ``/clear`` event rather than compaction.

    Example:
        >>> result = CompactionResult(
        ...     detected=True,
        ...     from_tokens=180000,
        ...     to_tokens=46000,
        ...     session_id_changed=False,
        ... )
    """

    detected: bool
    from_tokens: int
    to_tokens: int
    session_id_changed: bool

    @classmethod
    def no_compaction(cls, current_tokens: int) -> CompactionResult:
        """Create a result indicating no compaction was detected.

        Args:
            current_tokens: Current token count.

        Returns:
            CompactionResult with detected=False.
        """
        return cls(
            detected=False,
            from_tokens=current_tokens,
            to_tokens=current_tokens,
            session_id_changed=False,
        )

    @classmethod
    def new_session(cls, current_tokens: int) -> CompactionResult:
        """Create a result for a new session (``/clear`` event).

        Args:
            current_tokens: Current token count in new session.

        Returns:
            CompactionResult with session_id_changed=True.
        """
        return cls(
            detected=False,
            from_tokens=0,
            to_tokens=current_tokens,
            session_id_changed=True,
        )
