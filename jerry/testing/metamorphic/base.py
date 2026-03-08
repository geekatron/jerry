# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""Abstract base class for metamorphic relations in the Four-Layer Composite Test Harness.

This module defines the MetamorphicRelation ABC and the supporting types
MRViolationSeverity and MRResult.  InsufficientSamplesError is imported from
jerry.testing.stats (consolidated per QG-2 cross-stream consistency).

Domain layer: MUST NOT import DeepEval, promptfoo, or any adapter module (H-07).
The DeepEval adapter wraps these domain classes for pytest integration.

FR-010: Five Universal Metamorphic Relations
Behavioral contracts: Section C of behavioral-contracts.md

Architectural deviation notice -- FR-010 AC vs. domain ABC pattern:
    FR-010 acceptance criteria state that each MR "shall be implemented as a
    class inheriting from DeepEval's BaseMetric with a measure(test_case:
    LLMTestCase) -> float method".

    This implementation intentionally uses a domain ABC (MetamorphicRelation)
    instead of direct DeepEval BaseMetric inheritance.  This is an explicit
    architectural decision governed by H-07 (domain layer isolation):

    - The domain layer (this package) MUST NOT import framework-specific types.
      Inheriting from DeepEval BaseMetric would introduce a framework dependency
      directly into the domain, violating the hexagonal architecture constraint
      that domain classes have zero knowledge of adapter frameworks.

    - The adapter layer (jerry.testing.evaluation.deepeval_adapter) wraps each
      MetamorphicRelation subclass in a thin DeepEval BaseMetric adapter.  This
      adapter calls mr.transform() and mr.evaluate() and maps the MRResult to
      the BaseMetric interface (measure() returning 0.0 for violation, 1.0 for
      pass).

    - This approach is explicitly documented in system-design.md Section 4
      (H-07 Enforcement Rules) and system-design.md Section 1.4 (Module
      Decomposition).

    The FR-010 acceptance criteria text reflects an earlier design intent that
    predates the H-07 domain isolation decision.  The domain ABC pattern is the
    authoritative design.
"""

from __future__ import annotations

import statistics
from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass
from enum import Enum

from jerry.testing.stats import InsufficientSamplesError

# ---------------------------------------------------------------------------
# Domain enumerations
# ---------------------------------------------------------------------------


class MRViolationSeverity(str, Enum):
    """Severity level assigned to a metamorphic relation violation.

    Maps to the violation severity classification in behavioral-contracts.md
    Section C and Section C.6 MR Aggregation.
    """

    PASS = "PASS"
    INFORMATIONAL = "INFORMATIONAL"
    WARNING = "WARNING"
    REGRESSION = "REGRESSION"
    CRITICAL = "CRITICAL"


# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MRResult:
    """Result of a single metamorphic relation check.

    Produced by MetamorphicRelation.evaluate() for each MR applied to a batch
    of test cases.  This mirrors the MRResult type in jerry/testing/types.py;
    it is re-defined here so the metamorphic domain package has no dependency
    on the outer types module (H-07 domain isolation).

    Attributes:
        mr_id: Metamorphic relation identifier, e.g. "MR-001".
        mr_name: Human-readable relation name.
        passed: True when the MR invariant held across the sample.
        original_scores: Score sequence from the original (untransformed) inputs.
        transformed_scores: Score sequence from the transformed inputs.
        mean_original: Mean score across original runs.
        mean_transformed: Mean score across transformed runs.
        mean_delta: |mean_original - mean_transformed|.
        tolerance: Configured tolerance threshold for this MR.
        effect_size: Computed effect size (Cohen's r or directional Cohen's d).
        p_value: Wilcoxon signed-rank p-value (two-sided for symmetric MRs,
                 one-sided for MR-002 which expects a directional effect).
        severity: Violation severity classification.
        evidence: Human-readable explanation of the verdict.
    """

    mr_id: str
    mr_name: str
    passed: bool
    original_scores: tuple[float, ...]
    transformed_scores: tuple[float, ...]
    mean_original: float
    mean_transformed: float
    mean_delta: float
    tolerance: float
    effect_size: float
    p_value: float
    severity: MRViolationSeverity
    evidence: str


# ---------------------------------------------------------------------------
# Abstract base class
# ---------------------------------------------------------------------------


class MetamorphicRelation(ABC):
    """Abstract base class for all metamorphic relations in the harness.

    Each concrete subclass represents one MR (MR-001 through MR-005).
    The two required methods mirror the design contract in system-design.md
    Section 4 and the FR-010 acceptance criteria:

    - ``transform()`` -- applies a semantically neutral (or semantically
      directed, for MR-002) transformation to the input string.
    - ``evaluate()`` -- compares quality score sequences from the original and
      transformed inputs and returns an MRResult verdict.

    Domain isolation:
        This class MUST NOT import DeepEval, promptfoo, or any adapter.  The
        adapter layer wraps these domain classes for framework integration.
        Violation of this constraint breaks H-07 (domain layer isolation).

    Usage::

        # 1. Transform an input
        mr = ParaphraseConsistency()
        transformed = mr.transform(original_input)

        # 2. Obtain scores by running the agent on both versions (N >= 20)
        original_scores = run_agent_n_times(original_input, n=30)
        transformed_scores = run_agent_n_times(transformed, n=30)

        # 3. Evaluate
        result = mr.evaluate(original_scores, transformed_scores)
        if not result.passed:
            raise AssertionError(result.evidence)
    """

    # Subclasses set this in class body to identify themselves in error messages.
    mr_id: str = ""
    mr_name: str = ""

    # Minimum sample size required for this MR.  MR-002 uses 15; all others
    # use 20 per ADR-001 FM-002.  Subclasses may override.
    minimum_sample_size: int = 20

    @abstractmethod
    def transform(self, input_text: str) -> str:
        """Apply a semantically controlled transformation to the input text.

        The transformation must be:
        - Repeatable: given the same input, the output is deterministic
          (transformations that require LLM calls should cache internally or
          accept a random seed).
        - Semantically characterised: documented as neutral (MR-001, 003, 004,
          005) or directional (MR-002, negation).

        Args:
            input_text: The original prompt or user message text to transform.

        Returns:
            The transformed text ready to be used as an alternative input.

        Raises:
            ValueError: If ``input_text`` is empty or cannot be transformed.
        """
        ...

    @abstractmethod
    def evaluate(
        self,
        original_scores: Sequence[float],
        transformed_scores: Sequence[float],
    ) -> MRResult:
        """Compare quality score distributions and return an MR verdict.

        Both sequences must have equal length and satisfy the minimum sample
        size constraint for this MR.  Raise ``InsufficientSamplesError`` if the
        constraint is not met.

        Args:
            original_scores: Quality scores produced by running the agent on
                the original (untransformed) input, N times.  Each score is a
                float in [0.0, 1.0].
            transformed_scores: Quality scores produced by running the agent on
                the transformed input, N times.  Must have the same length as
                ``original_scores``.

        Returns:
            ``MRResult`` summarising whether the invariant held, the measured
            delta, effect size, p-value, and a human-readable evidence string.

        Raises:
            InsufficientSamplesError: If len(original_scores) < minimum_sample_size.
            ValueError: If the two sequences have different lengths, or if any
                score is outside [0.0, 1.0].
        """
        ...

    # ------------------------------------------------------------------
    # Shared validation helpers (available to all subclasses)
    # ------------------------------------------------------------------

    def _validate_inputs(
        self,
        original_scores: Sequence[float],
        transformed_scores: Sequence[float],
    ) -> None:
        """Validate score sequences before statistical analysis.

        Checks that:
        - The sample size meets the minimum for this MR.
        - Both sequences have equal length.
        - All scores are in the closed interval [0.0, 1.0].

        Args:
            original_scores: Score sequence from original inputs.
            transformed_scores: Score sequence from transformed inputs.

        Raises:
            InsufficientSamplesError: If len(original_scores) < minimum_sample_size.
            ValueError: Sequence length mismatch or score out of range.
        """
        n = len(original_scores)
        if n < self.minimum_sample_size:
            raise InsufficientSamplesError(
                f"{self.mr_id} requires at least {self.minimum_sample_size} sample "
                f"pairs for valid evaluation; received {n}.  Per ADR-001 FM-002, "
                f"Wilcoxon signed-rank is unreliable below N={self.minimum_sample_size}."
            )
        if len(transformed_scores) != n:
            raise ValueError(
                f"{self.mr_id}: original_scores length ({n}) does not match "
                f"transformed_scores length ({len(transformed_scores)})."
            )
        for i, s in enumerate(original_scores):
            if not 0.0 <= s <= 1.0:
                raise ValueError(f"{self.mr_id}: original_scores[{i}] = {s} is outside [0.0, 1.0].")
        for i, s in enumerate(transformed_scores):
            if not 0.0 <= s <= 1.0:
                raise ValueError(
                    f"{self.mr_id}: transformed_scores[{i}] = {s} is outside [0.0, 1.0]."
                )

    @staticmethod
    def _mean(scores: Sequence[float]) -> float:
        """Return the arithmetic mean of a score sequence.

        Args:
            scores: Non-empty sequence of floats.

        Returns:
            Arithmetic mean.
        """
        return statistics.mean(scores)

    @staticmethod
    def _std(scores: Sequence[float]) -> float:
        """Return the sample standard deviation of a score sequence.

        Uses statistics.stdev (Bessel-corrected, N-1 denominator).

        Args:
            scores: Sequence of at least 2 floats.

        Returns:
            Sample standard deviation.
        """
        if len(scores) < 2:
            return 0.0
        return statistics.stdev(scores)
