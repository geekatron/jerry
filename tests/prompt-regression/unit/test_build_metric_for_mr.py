# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""Unit tests for DeepEvalAdapter.build_metric_for_mr() (CG-010).

Tests that build_metric_for_mr() constructs a JerryGEvalDeepEvalMetric from
a MetamorphicRelation without making any LLM API calls.  All MetamorphicRelation
instances are stubbed using a minimal concrete subclass so that no real MR
transform/evaluate logic is exercised.

Coverage targets (FIX-WI4-C):
    1. Happy path: valid MR -> JerryGEvalDeepEvalMetric with correct threshold.
    2. Empty mr_id raises ValueError.
    3. Empty mr_name raises ValueError.
    4. quality_floor=None falls back to adapter default_threshold.
    5. Explicit quality_floor overrides default_threshold.

Pytest markers used:
    @pytest.mark.unit  -- fast, no I/O, no LLM calls

References:
    - CG-010: build_metric_for_mr() addition to DeepEvalAdapter
    - FR-010: Five Universal Metamorphic Relations
    - FR-021: Debiasing (position randomization + rubric shuffling, C-007)
    - H-20: BDD test-first (90% line coverage target)
    - system-design.md §1.4: G-Eval-as-proxy design path vs. full MR protocol
"""

from __future__ import annotations

from collections.abc import Sequence

import pytest

from jerry.testing.evaluation.debiasing import DebiasingStrategy
from jerry.testing.evaluation.deepeval_adapter import DeepEvalAdapter
from jerry.testing.evaluation.jerry_geval_deepeval_metric import JerryGEvalDeepEvalMetric
from jerry.testing.metamorphic.base import MetamorphicRelation, MRResult, MRViolationSeverity

# ---------------------------------------------------------------------------
# Stub MetamorphicRelation
# ---------------------------------------------------------------------------


class _StubMR(MetamorphicRelation):
    """Minimal concrete MetamorphicRelation for unit testing.

    Sets mr_id and mr_name as class attributes.  transform() and evaluate()
    are implemented with the minimum viable stub logic so pytest can construct
    instances without any external dependencies.
    """

    mr_id: str = "MR-STUB"
    mr_name: str = "Stub Invariant"
    minimum_sample_size: int = 1  # relax for stubs

    def transform(self, input_text: str) -> str:
        """Return the input unchanged (identity transform)."""
        return input_text

    def evaluate(
        self,
        original_scores: Sequence[float],
        transformed_scores: Sequence[float],
    ) -> MRResult:
        """Return a trivial PASS result for all inputs."""
        return MRResult(
            mr_id=self.mr_id,
            mr_name=self.mr_name,
            passed=True,
            original_scores=tuple(original_scores),
            transformed_scores=tuple(transformed_scores),
            mean_original=1.0,
            mean_transformed=1.0,
            mean_delta=0.0,
            tolerance=0.05,
            effect_size=0.0,
            p_value=1.0,
            severity=MRViolationSeverity.PASS,
            evidence="Stub: always passes.",
        )


class _EmptyIdMR(_StubMR):
    """Stub with an intentionally empty mr_id to trigger ValueError."""

    mr_id: str = ""
    mr_name: str = "Non-empty Name"


class _EmptyNameMR(_StubMR):
    """Stub with an intentionally empty mr_name to trigger ValueError."""

    mr_id: str = "MR-STUB-ID"
    mr_name: str = ""


# ---------------------------------------------------------------------------
# Shared fixture: an adapter that never calls any LLM API.
# ---------------------------------------------------------------------------


@pytest.fixture
def adapter(monkeypatch: pytest.MonkeyPatch) -> DeepEvalAdapter:
    """DeepEvalAdapter configured for unit testing.

    Sets ANTHROPIC_API_KEY so that __post_init__ validation passes for the
    default Claude model_name.  No actual API calls are made -- the tests
    only exercise object construction.

    Args:
        monkeypatch: pytest monkeypatch fixture for environment manipulation.

    Returns:
        DeepEvalAdapter with a deterministic DebiasingStrategy (seed=42).
    """
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-unit")
    return DeepEvalAdapter(
        model_name="claude-sonnet-4-20250514",
        debiasing_strategy=DebiasingStrategy(seed=42),
        default_threshold=0.82,
    )


# ---------------------------------------------------------------------------
# Tests for build_metric_for_mr()
# ---------------------------------------------------------------------------


class TestBuildMetricForMr:
    """Unit tests for DeepEvalAdapter.build_metric_for_mr().

    All tests operate purely on object construction; no LLM calls are made.
    """

    @pytest.mark.unit
    def test_build_metric_for_mr_happy_path(self, adapter: DeepEvalAdapter) -> None:
        """Happy path: valid MR returns a JerryGEvalDeepEvalMetric instance.

        Arrange:
            - A _StubMR with non-empty mr_id ("MR-STUB") and mr_name.
        Act:
            - Call adapter.build_metric_for_mr(mr) with default quality_floor.
        Assert:
            - Returned object is an instance of JerryGEvalDeepEvalMetric.
            - Returned metric threshold equals adapter.default_threshold (0.82).

        References:
            - CG-010: build_metric_for_mr() addition to DeepEvalAdapter
        """
        mr = _StubMR()

        metric = adapter.build_metric_for_mr(mr)

        assert isinstance(metric, JerryGEvalDeepEvalMetric), (
            f"Expected JerryGEvalDeepEvalMetric, got {type(metric).__name__}"
        )
        assert metric.threshold == adapter.default_threshold, (
            f"Expected threshold={adapter.default_threshold}, got {metric.threshold}"
        )

        # --- Internal structure assertions ---
        # Verify the domain metric has exactly one criterion (one MR -> one criterion).
        assert metric._jerry_metric.criteria, (
            "Expected at least one criterion in the constructed JerryGEvalMetric"
        )
        first_criterion = metric._jerry_metric.criteria[0]

        # Criterion name must match the MR's mr_id class attribute.
        assert first_criterion.name == "MR-STUB", (
            f"Expected criterion name 'MR-STUB', got '{first_criterion.name}'"
        )

        # Single-criterion metric: weight must be 1.0 so composite == criterion score.
        assert first_criterion.weight == 1.0, (
            f"Expected criterion weight 1.0, got {first_criterion.weight}"
        )

        # Criterion description must embed the MR name for judge intelligibility.
        assert "Stub Invariant" in first_criterion.description, (
            f"Expected criterion description to contain 'Stub Invariant', "
            f"got: {first_criterion.description!r}"
        )

    @pytest.mark.unit
    def test_build_metric_for_mr_empty_mr_id_raises_value_error(
        self, adapter: DeepEvalAdapter
    ) -> None:
        """Empty mr_id raises ValueError before any metric is constructed.

        Arrange:
            - A _EmptyIdMR stub with mr_id="" and non-empty mr_name.
        Act:
            - Call adapter.build_metric_for_mr(mr).
        Assert:
            - ValueError is raised (mr_id is required for criterion construction).

        References:
            - CG-010: Validation guard on mr_id
        """
        mr = _EmptyIdMR()

        with pytest.raises(ValueError, match="mr_id"):
            adapter.build_metric_for_mr(mr)

    @pytest.mark.unit
    def test_build_metric_for_mr_empty_mr_name_raises_value_error(
        self, adapter: DeepEvalAdapter
    ) -> None:
        """Empty mr_name raises ValueError before any metric is constructed.

        Arrange:
            - A _EmptyNameMR stub with non-empty mr_id and mr_name="".
        Act:
            - Call adapter.build_metric_for_mr(mr).
        Assert:
            - ValueError is raised (mr_name is required for criterion description).

        References:
            - CG-010: Validation guard on mr_name
        """
        mr = _EmptyNameMR()

        with pytest.raises(ValueError, match="mr_name"):
            adapter.build_metric_for_mr(mr)

    @pytest.mark.unit
    def test_build_metric_for_mr_quality_floor_none_uses_default(
        self, adapter: DeepEvalAdapter
    ) -> None:
        """quality_floor=None falls back to adapter.default_threshold.

        Arrange:
            - _StubMR with valid mr_id and mr_name.
            - adapter.default_threshold = 0.82.
        Act:
            - Call adapter.build_metric_for_mr(mr, quality_floor=None).
        Assert:
            - metric.threshold == 0.82 (the adapter default, not some other value).

        References:
            - CG-010: quality_floor defaulting logic
        """
        mr = _StubMR()

        metric = adapter.build_metric_for_mr(mr, quality_floor=None)

        assert metric.threshold == adapter.default_threshold, (
            f"quality_floor=None should fall back to default_threshold={adapter.default_threshold}, "
            f"got metric.threshold={metric.threshold}"
        )

    @pytest.mark.unit
    def test_build_metric_for_mr_quality_floor_override(self, adapter: DeepEvalAdapter) -> None:
        """Explicit quality_floor overrides the adapter default.

        Arrange:
            - _StubMR with valid mr_id and mr_name.
            - adapter.default_threshold = 0.82 (default).
        Act:
            - Call adapter.build_metric_for_mr(mr, quality_floor=0.85).
        Assert:
            - metric.threshold == 0.85 (the explicit override, not 0.82).

        References:
            - CG-010: quality_floor override path
        """
        mr = _StubMR()
        explicit_floor: float = 0.85

        metric = adapter.build_metric_for_mr(mr, quality_floor=explicit_floor)

        assert metric.threshold == explicit_floor, (
            f"Expected metric.threshold={explicit_floor} (explicit override), "
            f"got {metric.threshold}"
        )
        assert metric.threshold != adapter.default_threshold, (
            "Explicit quality_floor should differ from default_threshold when the test "
            "override (0.85) != default (0.82)"
        )
