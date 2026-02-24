# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
HooksStopGateHandler - CLI handler for the Stop hook gate.

Reads the cross-invocation state file written by ``jerry context estimate``
(status line) and blocks Claude from stopping at EMERGENCY tier. At all
other tiers (including when the state file is unavailable), allows stop.

This is the enforcement mechanism for DEC-004 D-010: Stop hook gate at
EMERGENCY only. Blocking Claude from stopping is aggressive, so it only
engages at EMERGENCY tier to force checkpoint before the user loses state.

Design Principles:
    - **Fail-open**: Any state file error allows stop (approve).
    - **Exit 0 always**: The handler always exits 0.
    - **Valid JSON always**: Response is always valid JSON.
    - **EMERGENCY only**: Only the EMERGENCY tier blocks stop.

References:
    - EN-014: Stop Hook Gate (context-stop-gate.py)
    - DEC-004 D-010: Stop hook gate at EMERGENCY only
    - ST-006: Automatic Session Rotation
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

import json
import logging
import sys
from typing import Any

from src.context_monitoring.application.ports.context_state_store import (
    IContextStateStore,
)
from src.context_monitoring.domain.value_objects.threshold_tier import ThresholdTier

logger = logging.getLogger(__name__)

# The reason provided when blocking Claude at EMERGENCY tier
_BLOCK_REASON = (
    "Context critically full (EMERGENCY tier). "
    "You must checkpoint state to ORCHESTRATION.yaml and "
    "tell the user to run /compact or /clear before finishing."
)

# System message injected when blocking at EMERGENCY tier
_BLOCK_SYSTEM_MESSAGE = (
    "Context fill is at EMERGENCY tier. "
    "Checkpoint critical state (ORCHESTRATION.yaml, WORKTRACKER.md) "
    "before stopping. Inform the user to run /compact or /clear."
)


class HooksStopGateHandler:
    """CLI handler for the Claude Code Stop hook gate.

    Reads the cross-invocation state file and blocks Claude from
    stopping at EMERGENCY tier. At all other tiers, allows stop.

    Fail-open: any error reading state results in allowing stop.

    Attributes:
        _context_state_store: State store for cross-invocation tier.

    Example:
        >>> handler = HooksStopGateHandler(context_state_store=store)
        >>> exit_code = handler.handle(stdin_json)
        >>> assert exit_code == 0
    """

    def __init__(self, context_state_store: IContextStateStore) -> None:
        """Initialize with the state store.

        Args:
            context_state_store: Store for reading cross-invocation state.
        """
        self._context_state_store = context_state_store

    def handle(self, stdin_json: str) -> int:
        """Handle a Stop hook event.

        Reads the state file to determine the current tier. If EMERGENCY,
        blocks Claude from stopping with an actionable reason. Otherwise,
        approves the stop.

        Args:
            stdin_json: The JSON payload from the Claude Code hook.

        Returns:
            Exit code (always 0).
        """
        tier = self._load_state_tier()

        response: dict[str, Any]
        if tier == ThresholdTier.EMERGENCY:
            logger.warning("Stop gate BLOCKING at EMERGENCY tier")
            response = {
                "decision": "block",
                "reason": _BLOCK_REASON,
                "systemMessage": _BLOCK_SYSTEM_MESSAGE,
            }
        else:
            response = {"decision": "approve"}

        print(json.dumps(response))
        return 0

    def _load_state_tier(self) -> ThresholdTier | None:
        """Load the last known tier from the state file.

        Fail-open: returns None on any failure (allows stop).

        Returns:
            ThresholdTier from state file, or None if unavailable.
        """
        try:
            state = self._context_state_store.load()
            if state is None:
                return None
            return ThresholdTier(state.last_tier)
        except Exception as exc:  # noqa: BLE001
            print(
                f"[hooks/stop] State file read failed: {exc}",
                file=sys.stderr,
            )
            return None
