# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
HooksPromptSubmitHandler - CLI handler for the UserPromptSubmit hook.

Reads Claude Code ``UserPromptSubmit`` JSON from stdin, invokes the
ContextFillEstimator and PromptReinforcementEngine, and returns a JSON
response with ``additionalContext`` combining the context-monitor tag,
graduated escalation, and quality reinforcement preamble.

Design Principles:
    - **Fail-open everywhere**: Each step is wrapped in try/except.
      Step failures log to stderr, but processing continues.
    - **Exit 0 always**: The handler always exits 0 even on partial failure.
    - **Valid JSON always**: The response is always valid JSON.

References:
    - EN-006: jerry hooks CLI Command Namespace
    - EN-705: L2 Per-Prompt Reinforcement Hook
    - ST-006: Graduated Escalation
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
from src.context_monitoring.application.services.checkpoint_service import (
    CheckpointService,
)
from src.context_monitoring.application.services.context_fill_estimator import (
    ContextFillEstimator,
)
from src.context_monitoring.domain.value_objects.fill_estimate import FillEstimate
from src.context_monitoring.domain.value_objects.threshold_tier import ThresholdTier
from src.infrastructure.internal.enforcement.prompt_reinforcement_engine import (
    PromptReinforcementEngine,
)

logger = logging.getLogger(__name__)

# Severity ordering for ThresholdTier comparison
_TIER_SEVERITY: dict[ThresholdTier, int] = {
    ThresholdTier.NOMINAL: 0,
    ThresholdTier.LOW: 1,
    ThresholdTier.WARNING: 2,
    ThresholdTier.CRITICAL: 3,
    ThresholdTier.EMERGENCY: 4,
}

# Tiers that receive graduated escalation messaging
_ESCALATION_TIERS = frozenset(
    {ThresholdTier.WARNING, ThresholdTier.CRITICAL, ThresholdTier.EMERGENCY}
)

# Graduated escalation messages (action-focused guidance)
_ESCALATION_MESSAGES: dict[ThresholdTier, str] = {
    ThresholdTier.WARNING: "Consider checkpointing critical state.",
    ThresholdTier.CRITICAL: "Checkpoint now. Reduce scope. Recommend /compact soon.",
    ThresholdTier.EMERGENCY: (
        "Context critically full. Checkpoint immediately. Tell user to run /compact or /clear."
    ),
}


class HooksPromptSubmitHandler:
    """CLI handler for the Claude Code UserPromptSubmit hook.

    Combines context fill estimation, graduated escalation, and
    quality reinforcement into a single ``additionalContext`` payload.

    Each processing step is fail-open: failures log to stderr and
    processing continues with an empty contribution from the failed step.

    Attributes:
        _context_fill_estimator: Service for estimating context window fill.
        _checkpoint_service: Service for creating checkpoints (AE-006c/d).
        _reinforcement_engine: Engine for generating L2 quality reinforcement.
        _context_state_store: Optional state store for cross-invocation tier.

    Example:
        >>> handler = HooksPromptSubmitHandler(
        ...     context_fill_estimator=estimator,
        ...     checkpoint_service=checkpoint_service,
        ...     reinforcement_engine=engine,
        ... )
        >>> exit_code = handler.handle(stdin_json)
    """

    # Tiers that trigger auto-checkpoint per AE-006c/d
    _CHECKPOINT_TIERS = frozenset({ThresholdTier.CRITICAL, ThresholdTier.EMERGENCY})

    def __init__(
        self,
        context_fill_estimator: ContextFillEstimator,
        checkpoint_service: CheckpointService,
        reinforcement_engine: PromptReinforcementEngine,
        context_state_store: IContextStateStore | None = None,
    ) -> None:
        """Initialize the handler with required services.

        Args:
            context_fill_estimator: Service for estimating context window fill.
            checkpoint_service: Service for creating checkpoints (AE-006c/d).
            reinforcement_engine: Engine for generating quality reinforcement.
            context_state_store: Optional store for cross-invocation state
                (written by status line, read here for graduated escalation).
        """
        self._context_fill_estimator = context_fill_estimator
        self._checkpoint_service = checkpoint_service
        self._reinforcement_engine = reinforcement_engine
        self._context_state_store = context_state_store

    def handle(self, stdin_json: str) -> int:
        """Handle a UserPromptSubmit hook event.

        Steps:
            1. Parse hook input JSON
            2. Estimate context fill from transcript (existing)
            3. Read cross-invocation state tier (ST-006)
            4. Determine effective tier (max of transcript and state)
            5. Auto-checkpoint at CRITICAL/EMERGENCY (AE-006c/d)
            6. Graduated escalation at WARNING+ (ST-006)
            7. Quality reinforcement (L2)

        All steps are fail-open. Always returns 0.

        Args:
            stdin_json: The JSON payload from the Claude Code hook.

        Returns:
            Exit code (always 0).
        """
        context_parts: list[str] = []

        # Step 1: Parse hook input (fail-open)
        hook_data: dict[str, Any] = {}
        try:
            hook_data = json.loads(stdin_json)
        except (json.JSONDecodeError, TypeError, ValueError) as exc:
            print(f"[hooks/prompt-submit] Failed to parse hook input: {exc}", file=sys.stderr)

        transcript_path: str = hook_data.get("transcript_path", "")

        # Step 2: Context fill estimation (fail-open)
        fill_estimate: FillEstimate | None = None
        if transcript_path:
            try:
                fill_estimate = self._context_fill_estimator.estimate(transcript_path)
                tag = self._context_fill_estimator.generate_context_monitor_tag(fill_estimate)
                context_parts.append(tag)
            except Exception as exc:  # noqa: BLE001
                print(
                    f"[hooks/prompt-submit] Context fill estimation failed: {exc}",
                    file=sys.stderr,
                )

        # Step 3: Read state file tier (fail-open, ST-006)
        state_tier = self._load_state_tier()

        # Step 4: Determine effective tier
        transcript_tier = fill_estimate.tier if fill_estimate is not None else None
        effective_tier = self._effective_tier(transcript_tier, state_tier)

        # Step 5: AE-006c/d enforcement — auto-checkpoint at CRITICAL/EMERGENCY (fail-open)
        if effective_tier is not None and effective_tier in self._CHECKPOINT_TIERS:
            self._create_auto_checkpoint(fill_estimate, effective_tier)

        # Step 6: Graduated escalation at WARNING+ (ST-006, fail-open)
        escalation = self._generate_escalation(effective_tier)
        if escalation:
            context_parts.append(escalation)

        # Step 7: Quality reinforcement (fail-open)
        try:
            reinforcement = self._reinforcement_engine.generate_reinforcement()
            if reinforcement.preamble:
                context_parts.append(reinforcement.preamble)
        except Exception as exc:  # noqa: BLE001
            print(
                f"[hooks/prompt-submit] Reinforcement generation failed: {exc}",
                file=sys.stderr,
            )

        # Assemble and emit response
        additional_context = "\n\n".join(context_parts)
        response: dict[str, Any] = {"additionalContext": additional_context}
        print(json.dumps(response))

        return 0

    def _load_state_tier(self) -> ThresholdTier | None:
        """Load the last known tier from the cross-invocation state file.

        The state file is written by ``jerry context estimate`` (status line)
        and contains the most recent context tier classification.

        Fail-open: returns None on any failure.

        Returns:
            ThresholdTier from state file, or None if unavailable.
        """
        if self._context_state_store is None:
            return None
        try:
            state = self._context_state_store.load()
            if state is None:
                return None
            return ThresholdTier(state.last_tier)
        except Exception as exc:  # noqa: BLE001
            print(
                f"[hooks/prompt-submit] State file read failed: {exc}",
                file=sys.stderr,
            )
            return None

    def _effective_tier(
        self,
        transcript_tier: ThresholdTier | None,
        state_tier: ThresholdTier | None,
    ) -> ThresholdTier | None:
        """Return the higher severity tier from transcript and state sources.

        Uses the conservative approach: if either source indicates a higher
        tier, that tier is used for checkpoint and escalation decisions.

        Args:
            transcript_tier: Tier from transcript-based estimation.
            state_tier: Tier from cross-invocation state file.

        Returns:
            The higher severity tier, or None if both are None.
        """
        if transcript_tier is None and state_tier is None:
            return None
        if transcript_tier is None:
            return state_tier
        if state_tier is None:
            return transcript_tier
        if _TIER_SEVERITY.get(state_tier, 0) > _TIER_SEVERITY.get(transcript_tier, 0):
            return state_tier
        return transcript_tier

    def _create_auto_checkpoint(
        self,
        fill_estimate: FillEstimate | None,
        effective_tier: ThresholdTier,
    ) -> None:
        """Create auto-checkpoint at CRITICAL/EMERGENCY tiers (AE-006c/d).

        Fail-open: checkpoint failure does not block the hook.

        Args:
            fill_estimate: Transcript-based fill estimate (may be None).
            effective_tier: The effective tier driving checkpoint creation.
        """
        try:
            context_state = (
                fill_estimate
                if fill_estimate is not None
                else FillEstimate(
                    fill_percentage=0.0,
                    tier=effective_tier,
                    token_count=None,
                )
            )
            checkpoint = self._checkpoint_service.create_checkpoint(
                context_state=context_state,
                trigger=f"ae006_{effective_tier.value}",
            )
            logger.info(
                "AE-006%s auto-checkpoint created: %s",
                "d" if effective_tier == ThresholdTier.EMERGENCY else "c",
                checkpoint.checkpoint_id,
            )
        except Exception as exc:  # noqa: BLE001
            print(
                f"[hooks/prompt-submit] AE-006 auto-checkpoint failed: {exc}",
                file=sys.stderr,
            )

    def _generate_escalation(self, tier: ThresholdTier | None) -> str | None:
        """Generate graduated escalation XML for WARNING+ tiers.

        Produces an XML ``<context-escalation>`` block with the tier name
        and action-focused guidance. The escalation message tells Claude
        what to do at each severity level.

        Args:
            tier: The effective tier to generate escalation for.

        Returns:
            XML string, or None for tiers below WARNING.
        """
        if tier is None or tier not in _ESCALATION_TIERS:
            return None

        message = _ESCALATION_MESSAGES.get(tier)
        if message is None:
            return None

        return (
            "<context-escalation>\n"
            f"  <tier>{tier.name}</tier>\n"
            f"  <action>{message}</action>\n"
            "</context-escalation>"
        )
