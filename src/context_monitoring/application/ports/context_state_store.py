# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
IContextStateStore - Port for cross-invocation context state persistence.

Defines the protocol for loading and saving context monitoring state
between CLI invocations (status line calls, hook events).

References:
    - FEAT-002: Status Line / Context Monitoring Unification
    - EN-010: Application Port (IContextStateStore) + ContextEstimateService
    - DEC-004 D-004: Cross-invocation state via port
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from src.context_monitoring.application.ports.context_state import ContextState


@runtime_checkable
class IContextStateStore(Protocol):
    """Port for cross-invocation context state persistence.

    Implementations persist a small state file that bridges the gap
    between separate CLI invocations (status line, hooks).

    Example:
        >>> state = store.load()
        >>> if state is not None:
        ...     print(state.previous_tokens)
    """

    def load(self) -> ContextState | None:
        """Load the persisted context state.

        Returns:
            The saved ContextState, or None if no state exists yet.
        """
        ...

    def save(self, state: ContextState) -> None:
        """Save context state for the next invocation.

        Must use atomic writes to prevent corruption from concurrent
        invocations.

        Args:
            state: The state to persist.
        """
        ...
