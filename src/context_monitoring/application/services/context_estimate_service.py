# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ContextEstimateService - Application service orchestrating context estimation.

Orchestrates the full pipeline: parse input -> compute estimate ->
detect compaction -> determine rotation action -> persist state.
Single entry point for CLI and hooks.

Fail-open design: Any exception results in degraded output with
safe defaults rather than propagating the exception.

References:
    - FEAT-002: Status Line / Context Monitoring Unification
    - EN-010: Application Port (IContextStateStore) + ContextEstimateService
    - DEC-004 D-007: Fail-open design
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

import logging

from src.context_monitoring.application.ports.context_state import ContextState
from src.context_monitoring.application.ports.context_state_store import (
    IContextStateStore,
)
from src.context_monitoring.application.services.estimate_result import EstimateResult
from src.context_monitoring.domain.services.context_estimate_computer import (
    ContextEstimateComputer,
)
from src.context_monitoring.domain.value_objects.compaction_result import (
    CompactionResult,
)
from src.context_monitoring.domain.value_objects.context_estimate import (
    ContextEstimate,
)
from src.context_monitoring.domain.value_objects.context_usage_input import (
    ContextUsageInput,
)
from src.context_monitoring.domain.value_objects.rotation_action import RotationAction
from src.context_monitoring.domain.value_objects.threshold_tier import ThresholdTier

logger = logging.getLogger(__name__)


class ContextEstimateService:
    """Application service for context estimation pipeline.

    Orchestrates domain computation, state persistence, and
    compaction detection. Designed as the single entry point
    for both the ``jerry context estimate`` CLI command and hooks.

    Attributes:
        _computer: Pure domain service for computation.
        _state_store: Port for cross-invocation state persistence.

    Example:
        >>> service = ContextEstimateService(computer, state_store)
        >>> result = service.estimate(usage_input)
        >>> print(result.estimate.tier)
        ThresholdTier.WARNING
    """

    def __init__(
        self,
        computer: ContextEstimateComputer,
        state_store: IContextStateStore,
    ) -> None:
        """Initialize the ContextEstimateService.

        Args:
            computer: Pure domain service for fill computation.
            state_store: Port for cross-invocation state persistence.
        """
        self._computer = computer
        self._state_store = state_store

    def estimate(self, usage: ContextUsageInput) -> EstimateResult:
        """Run the full context estimation pipeline.

        Steps:
            1. Compute fill estimate from exact usage data
            2. Load previous state for compaction detection
            3. Detect compaction or /clear event
            4. Determine rotation action
            5. Persist current state for next invocation

        Fail-open: state load/save failures are logged but do not
        prevent the estimate from being returned.

        Args:
            usage: Parsed context usage input from Claude Code JSON.

        Returns:
            EstimateResult with estimate, compaction, action, thresholds.
        """
        # Step 1: Compute fill estimate
        context_estimate = self._computer.compute(usage)

        # Step 2: Load previous state (fail-open)
        previous_state = self._load_state_safe()

        # Step 3: Detect compaction
        compaction = self._computer.detect_compaction(
            current_tokens=context_estimate.used_tokens,
            current_session_id=usage.session_id,
            previous_tokens=previous_state.previous_tokens if previous_state else None,
            previous_session_id=previous_state.previous_session_id if previous_state else None,
        )

        # Step 4: Determine rotation action
        action = self._computer.determine_rotation_action(context_estimate.tier)

        # Step 5: Persist state (fail-open)
        self._save_state_safe(
            ContextState(
                previous_tokens=context_estimate.used_tokens,
                previous_session_id=usage.session_id,
                last_tier=context_estimate.tier.value,
                last_rotation_action=action.value,
            )
        )

        return EstimateResult(
            estimate=context_estimate,
            compaction=compaction,
            action=action,
            thresholds=self._computer.thresholds,
        )

    def estimate_degraded(self) -> EstimateResult:
        """Return a degraded estimate for error cases.

        Used when the input is invalid or unparseable. Returns
        safe defaults (NOMINAL, no compaction, no action).

        Returns:
            EstimateResult with NOMINAL tier and safe defaults.
        """
        return EstimateResult(
            estimate=ContextEstimate(
                fill_percentage=0.0,
                used_tokens=0,
                window_size=200_000,
                tier=ThresholdTier.NOMINAL,
                is_estimated=True,
                fresh_tokens=0,
                cached_tokens=0,
                cache_creation_tokens=0,
            ),
            compaction=CompactionResult.no_compaction(0),
            action=RotationAction.NONE,
            thresholds=self._computer.thresholds,
        )

    def _load_state_safe(self) -> ContextState | None:
        """Load previous state with fail-open behavior.

        Returns:
            ContextState or None on any error.
        """
        try:
            return self._state_store.load()
        except Exception as exc:  # noqa: BLE001
            logger.warning("Failed to load context state: %s", exc)
            return None

    def _save_state_safe(self, state: ContextState) -> None:
        """Save state with fail-open behavior.

        Args:
            state: State to persist.
        """
        try:
            self._state_store.save(state)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Failed to save context state: %s", exc)
