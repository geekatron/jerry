# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
HooksPromptSubmitHandler - CLI handler for the UserPromptSubmit hook.

Reads Claude Code ``UserPromptSubmit`` JSON from stdin, invokes the
ContextFillEstimator and PromptReinforcementEngine, and returns a JSON
response with ``additionalContext`` combining the context-monitor tag
and quality reinforcement preamble.

Design Principles:
    - **Fail-open everywhere**: Each step is wrapped in try/except.
      Step failures log to stderr, but processing continues.
    - **Exit 0 always**: The handler always exits 0 even on partial failure.
    - **Valid JSON always**: The response is always valid JSON.

References:
    - EN-006: jerry hooks CLI Command Namespace
    - EN-705: L2 Per-Prompt Reinforcement Hook
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

import json
import logging
import sys
from typing import Any

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


class HooksPromptSubmitHandler:
    """CLI handler for the Claude Code UserPromptSubmit hook.

    Combines context fill estimation and quality reinforcement into a
    single ``additionalContext`` payload for the hook response.

    Each processing step is fail-open: failures log to stderr and
    processing continues with an empty contribution from the failed step.

    Attributes:
        _context_fill_estimator: Service for estimating context window fill.
        _checkpoint_service: Service for creating checkpoints (AE-006c/d).
        _reinforcement_engine: Engine for generating L2 quality reinforcement.

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
    ) -> None:
        """Initialize the handler with required services.

        Args:
            context_fill_estimator: Service for estimating context window fill.
            checkpoint_service: Service for creating checkpoints (AE-006c/d enforcement).
            reinforcement_engine: Engine for generating quality reinforcement.
        """
        self._context_fill_estimator = context_fill_estimator
        self._checkpoint_service = checkpoint_service
        self._reinforcement_engine = reinforcement_engine

    def handle(self, stdin_json: str) -> int:
        """Handle a UserPromptSubmit hook event.

        Reads the hook input JSON, extracts transcript_path, runs fill
        estimation and reinforcement generation (both fail-open), and
        prints the combined JSON response to stdout.

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
        except (json.JSONDecodeError, ValueError) as exc:
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

        # Step 3: AE-006c/d enforcement — auto-checkpoint at CRITICAL/EMERGENCY (fail-open)
        if fill_estimate is not None and fill_estimate.tier in self._CHECKPOINT_TIERS:
            self._enforce_checkpoint(fill_estimate, context_parts)

        # Step 4: Quality reinforcement (fail-open)
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

    def _enforce_checkpoint(
        self,
        fill_estimate: FillEstimate,
        context_parts: list[str],
    ) -> None:
        """Enforce AE-006c/d: create checkpoint and warn user at high fill tiers.

        At CRITICAL tier (>= 0.80, AE-006c): auto-checkpoint.
        At EMERGENCY tier (>= 0.88, AE-006d): auto-checkpoint + user warning + handoff preparation.

        Both steps are fail-open: checkpoint failure does not block the hook.

        Args:
            fill_estimate: Current context fill estimate with tier.
            context_parts: Mutable list of context strings to append warnings to.
        """
        # Auto-checkpoint (AE-006c + AE-006d)
        try:
            checkpoint = self._checkpoint_service.create_checkpoint(
                context_state=fill_estimate,
                trigger=f"ae006_{fill_estimate.tier.value}",
            )
            logger.info(
                "AE-006%s auto-checkpoint created: %s (fill=%.2f)",
                "d" if fill_estimate.tier == ThresholdTier.EMERGENCY else "c",
                checkpoint.checkpoint_id,
                fill_estimate.fill_percentage,
            )
        except Exception as exc:  # noqa: BLE001
            print(
                f"[hooks/prompt-submit] AE-006 auto-checkpoint failed: {exc}",
                file=sys.stderr,
            )

        # User warning at EMERGENCY tier (AE-006d)
        if fill_estimate.tier == ThresholdTier.EMERGENCY:
            pct = int(fill_estimate.fill_percentage * 100)
            warning_xml = (
                "<context-emergency>\n"
                f"  Context window is {pct}% full (EMERGENCY tier).\n"
                "  A checkpoint has been created. Consider completing current work\n"
                "  and preparing for session handoff.\n"
                "</context-emergency>"
            )
            context_parts.append(warning_xml)
