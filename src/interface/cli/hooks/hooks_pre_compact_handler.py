# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
HooksPreCompactHandler - CLI handler for the PreCompact hook.

Reads Claude Code ``PreCompact`` JSON from stdin, creates a checkpoint
via CheckpointService, and abandons the current session with reason
"compaction".

Design Principles:
    - **Fail-open everywhere**: Each step is wrapped in try/except.
      Step failures log to stderr, but processing continues.
    - **Exit 0 always**: The handler always exits 0 even on partial failure.
    - **Valid JSON always**: The response is always valid JSON.

Note:
    The PreCompact hook does not support user approval (no ``decision``
    field in the response). This handler is purely side-effectful:
    it persists state before context compaction occurs.

References:
    - EN-006: jerry hooks CLI Command Namespace
    - EN-003: Checkpoint Management
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

import json
import logging
import sys
from typing import Any

from src.context_monitoring.application.ports.context_state import ContextState
from src.context_monitoring.application.ports.context_state_store import (
    IContextStateStore,
)
from src.context_monitoring.application.services.checkpoint_service import (
    CheckpointService,
)
from src.context_monitoring.application.services.context_fill_estimator import (
    ContextFillEstimator,
)
from src.context_monitoring.domain.value_objects.fill_estimate import FillEstimate
from src.context_monitoring.domain.value_objects.threshold_tier import ThresholdTier
from src.session_management.application.commands import AbandonSessionCommand
from src.session_management.application.handlers.commands.abandon_session_command_handler import (
    AbandonSessionCommandHandler,
)

logger = logging.getLogger(__name__)

# Fallback fill estimate when estimator is unavailable
_FALLBACK_FILL_ESTIMATE = FillEstimate(
    fill_percentage=0.0,
    tier=ThresholdTier.NOMINAL,
    token_count=None,
)


class HooksPreCompactHandler:
    """CLI handler for the Claude Code PreCompact hook.

    Creates a checkpoint to persist workflow state before context compaction,
    then abandons the current session with reason "compaction".

    Each processing step is fail-open: failures log to stderr and
    processing continues without blocking the compaction.

    Attributes:
        _checkpoint_service: Service for creating and persisting checkpoints.
        _context_fill_estimator: Service for estimating context fill level.
        _abandon_handler: Handler for abandoning the current session.
        _context_state_store: Optional store for cross-invocation state (EN-015).

    Example:
        >>> handler = HooksPreCompactHandler(
        ...     checkpoint_service=service,
        ...     context_fill_estimator=estimator,
        ...     abandon_handler=abandon_handler,
        ...     context_state_store=state_store,
        ... )
        >>> exit_code = handler.handle(stdin_json)
    """

    def __init__(
        self,
        checkpoint_service: CheckpointService,
        context_fill_estimator: ContextFillEstimator,
        abandon_handler: AbandonSessionCommandHandler,
        context_state_store: IContextStateStore | None = None,
    ) -> None:
        """Initialize the handler with required services.

        Args:
            checkpoint_service: Service for checkpoint lifecycle management.
            context_fill_estimator: Service for estimating context window fill.
            abandon_handler: Handler for AbandonSessionCommand.
            context_state_store: Optional cross-invocation state store (EN-015).
                When provided, the handler saves pre-compaction state so
                post-compaction hooks can detect the compaction event.
        """
        self._checkpoint_service = checkpoint_service
        self._context_fill_estimator = context_fill_estimator
        self._abandon_handler = abandon_handler
        self._context_state_store = context_state_store

    def handle(self, stdin_json: str) -> int:
        """Handle a PreCompact hook event.

        Creates a checkpoint capturing current context state, then abandons
        the session with reason "compaction". Both steps are fail-open.

        Args:
            stdin_json: The JSON payload from the Claude Code hook.

        Returns:
            Exit code (always 0).
        """
        response: dict[str, Any] = {}

        # Step 1: Parse hook input (fail-open)
        hook_data: dict[str, Any] = {}
        try:
            hook_data = json.loads(stdin_json)
        except (json.JSONDecodeError, TypeError, ValueError) as exc:
            print(f"[hooks/pre-compact] Failed to parse hook input: {exc}", file=sys.stderr)

        transcript_path: str = hook_data.get("transcript_path", "")
        session_id: str = hook_data.get("session_id", "")

        # Step 2: Estimate context fill (fail-open, use fallback)
        fill_estimate = _FALLBACK_FILL_ESTIMATE
        if transcript_path:
            try:
                fill_estimate = self._context_fill_estimator.estimate(transcript_path)
            except Exception as exc:  # noqa: BLE001
                print(
                    f"[hooks/pre-compact] Context fill estimation failed: {exc}",
                    file=sys.stderr,
                )

        # Step 2b: Save pre-compaction state to state store (EN-015, fail-open)
        self._save_pre_compaction_state(fill_estimate, session_id)

        # Step 3: Create checkpoint (fail-open)
        checkpoint_id: str | None = None
        try:
            checkpoint = self._checkpoint_service.create_checkpoint(
                context_state=fill_estimate,
                trigger="pre_compact",
            )
            checkpoint_id = checkpoint.checkpoint_id
            response["checkpoint_id"] = checkpoint_id
            logger.info("Checkpoint created: %s", checkpoint_id)
        except Exception as exc:  # noqa: BLE001
            print(
                f"[hooks/pre-compact] Checkpoint creation failed: {exc}",
                file=sys.stderr,
            )

        # Step 4: Abandon session with reason "compaction" (fail-open)
        try:
            command = AbandonSessionCommand(reason="compaction")
            events = self._abandon_handler.handle(command)
            abandoned_session_id = events[0].aggregate_id if events else None
            if abandoned_session_id:
                response["session_id"] = abandoned_session_id
                logger.info("Session abandoned (reason=compaction): %s", abandoned_session_id)
        except Exception as exc:  # noqa: BLE001
            print(
                f"[hooks/pre-compact] Session abandonment failed: {exc}",
                file=sys.stderr,
            )

        # Emit response (always valid JSON)
        print(json.dumps(response))
        return 0

    def _save_pre_compaction_state(
        self,
        fill_estimate: FillEstimate,
        session_id: str,
    ) -> None:
        """Save pre-compaction context state for post-compaction detection.

        EN-015: Records the current fill level and session ID before
        compaction fires. Post-compaction, the status line command
        detects the token drop (same session_id, lower token count)
        to classify the event as compaction.

        Fail-open: any error is logged and silently ignored.

        Args:
            fill_estimate: Current context fill estimate.
            session_id: Claude Code session ID from hook input.
        """
        if self._context_state_store is None:
            return

        try:
            state = ContextState(
                previous_tokens=fill_estimate.token_count or 0,
                previous_session_id=session_id,
                last_tier=fill_estimate.tier.name,
                last_rotation_action="CHECKPOINT",
            )
            self._context_state_store.save(state)
            logger.info(
                "Pre-compaction state saved (tier=%s, tokens=%s)",
                fill_estimate.tier.name,
                fill_estimate.token_count,
            )
        except Exception as exc:  # noqa: BLE001
            print(
                f"[hooks/pre-compact] State store save failed: {exc}",
                file=sys.stderr,
            )
