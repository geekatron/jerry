# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for ContextEstimateService application service."""

from __future__ import annotations

from src.context_monitoring.application.ports.context_state import ContextState
from src.context_monitoring.application.services.context_estimate_service import (
    ContextEstimateService,
)
from src.context_monitoring.domain.services.context_estimate_computer import (
    ContextEstimateComputer,
)
from src.context_monitoring.domain.value_objects.context_usage_input import (
    ContextUsageInput,
)
from src.context_monitoring.domain.value_objects.rotation_action import RotationAction
from src.context_monitoring.domain.value_objects.threshold_tier import ThresholdTier


class InMemoryStateStore:
    """In-memory implementation of IContextStateStore for testing."""

    def __init__(self, initial_state: ContextState | None = None) -> None:
        self._state = initial_state
        self.save_count = 0

    def load(self) -> ContextState | None:
        return self._state

    def save(self, state: ContextState) -> None:
        self._state = state
        self.save_count += 1

    @property
    def saved_state(self) -> ContextState | None:
        return self._state


class FailingStateStore:
    """State store that raises on every operation."""

    def load(self) -> ContextState | None:
        raise OSError("disk full")

    def save(self, state: ContextState) -> None:
        raise OSError("disk full")


def _make_usage(
    *,
    input_tokens: int = 8500,
    cache_creation: int = 5000,
    cache_read: int = 12000,
    window_size: int = 200000,
    session_id: str = "abc123",
) -> ContextUsageInput:
    return ContextUsageInput(
        session_id=session_id,
        input_tokens=input_tokens,
        cache_creation_input_tokens=cache_creation,
        cache_read_input_tokens=cache_read,
        context_window_size=window_size,
    )


class TestEstimate:
    """Test the full estimation pipeline."""

    def test_basic_pipeline(self) -> None:
        """Pipeline computes estimate, detects no compaction, persists state."""
        store = InMemoryStateStore()
        computer = ContextEstimateComputer()
        service = ContextEstimateService(computer, store)

        result = service.estimate(
            _make_usage(
                input_tokens=80000,
                cache_creation=40000,
                cache_read=40000,
                window_size=200000,
            )
        )

        assert result.estimate.fill_percentage == 0.8
        assert result.estimate.tier == ThresholdTier.CRITICAL
        assert result.compaction.detected is False
        assert result.action == RotationAction.CHECKPOINT  # moderate default
        assert "nominal" in result.thresholds

    def test_state_persisted_after_estimate(self) -> None:
        """State is saved after each estimate for next invocation."""
        store = InMemoryStateStore()
        service = ContextEstimateService(ContextEstimateComputer(), store)

        service.estimate(_make_usage(session_id="sess-1"))

        assert store.save_count == 1
        saved = store.saved_state
        assert saved is not None
        assert saved.previous_session_id == "sess-1"
        assert saved.previous_tokens == 25500  # 8500 + 5000 + 12000

    def test_compaction_detected_on_second_call(self) -> None:
        """Second call detects compaction when tokens drop significantly."""
        store = InMemoryStateStore(
            ContextState(
                previous_tokens=180000,
                previous_session_id="abc123",
                last_tier="emergency",
                last_rotation_action="emergency_handoff",
            )
        )
        service = ContextEstimateService(ContextEstimateComputer(), store)

        result = service.estimate(
            _make_usage(
                input_tokens=20000,
                cache_creation=10000,
                cache_read=16000,
                session_id="abc123",
            )
        )

        assert result.compaction.detected is True
        assert result.compaction.from_tokens == 180000
        assert result.compaction.to_tokens == 46000

    def test_session_id_change_detected(self) -> None:
        """Session ID change (from /clear) detected as new session."""
        store = InMemoryStateStore(
            ContextState(
                previous_tokens=180000,
                previous_session_id="old-session",
                last_tier="emergency",
                last_rotation_action="emergency_handoff",
            )
        )
        service = ContextEstimateService(ContextEstimateComputer(), store)

        result = service.estimate(_make_usage(session_id="new-session"))

        assert result.compaction.session_id_changed is True
        assert result.compaction.detected is False


class TestFailOpen:
    """Test fail-open behavior when state store fails."""

    def test_estimate_succeeds_when_load_fails(self) -> None:
        """Estimate still works when state store load fails."""
        service = ContextEstimateService(
            ContextEstimateComputer(),
            FailingStateStore(),
        )
        result = service.estimate(_make_usage())

        # Estimate should still compute correctly
        assert result.estimate.used_tokens == 25500
        # No compaction since no previous state
        assert result.compaction.detected is False

    def test_estimate_succeeds_when_save_fails(self) -> None:
        """Estimate returned even if state save fails."""
        service = ContextEstimateService(
            ContextEstimateComputer(),
            FailingStateStore(),
        )
        result = service.estimate(_make_usage())

        assert result.estimate.tier is not None
        assert result.action is not None


class TestEstimateDegraded:
    """Test degraded fallback estimate."""

    def test_degraded_returns_safe_defaults(self) -> None:
        """Degraded estimate has NOMINAL tier and zero tokens."""
        service = ContextEstimateService(
            ContextEstimateComputer(),
            InMemoryStateStore(),
        )
        result = service.estimate_degraded()

        assert result.estimate.fill_percentage == 0.0
        assert result.estimate.tier == ThresholdTier.NOMINAL
        assert result.estimate.is_estimated is True
        assert result.estimate.used_tokens == 0
        assert result.action == RotationAction.NONE
        assert result.compaction.detected is False
