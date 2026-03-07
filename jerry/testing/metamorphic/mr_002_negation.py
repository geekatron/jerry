# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""MR-002: Negation Handling metamorphic relation.

Definition (behavioral-contracts.md Section C.2):
    Negating a key positive constraint in the prompt (e.g., changing
    "include evidence quality citations" to "do not include evidence quality
    citations") should produce measurably DIFFERENT output quality.  This
    relation is DIRECTIONAL: a violation occurs when the agent does NOT
    respond to the negation (i.e. scores remain indistinguishable despite
    the constraint being negated).

Tolerance / effect expectation:
    Effect size threshold : Cohen's r >= 0.40 (large effect expected for constraint
                            negation, per contracts C.2)
    Minimum detectable change: >= 0.08 in the affected dimension
    Violation condition: Wilcoxon p >= 0.10 AND mean_delta < 0.05 (agent ignoring negation)
    Minimum sample size: 15 pairs (reduced from 20; detecting presence of large effect)

Effect size metric (contracts C.2):
    Cohen's r (rank-biserial correlation) derived from the one-sided Wilcoxon statistic:
        r = 1 - (2 * W) / (n * (n + 1))
    This matches the Cohen's r metric used in MR-001, MR-003, MR-004, and MR-005.
    The contracts specify "Cohen's r >= 0.40" for this MR.

Domain isolation: MUST NOT import DeepEval, promptfoo, or any adapter (H-07).
One class per file (H-10).
"""

from __future__ import annotations

import re
from collections.abc import Sequence

from jerry.testing.metamorphic.base import (
    MetamorphicRelation,
    MRResult,
    MRViolationSeverity,
)

try:
    from scipy.stats import wilcoxon

    _SCIPY_AVAILABLE = True
except ImportError:  # pragma: no cover
    _SCIPY_AVAILABLE = False


# ---------------------------------------------------------------------------
# Negation pattern catalog
# ---------------------------------------------------------------------------

# Each entry is a (positive_pattern, negated_replacement) tuple.
# Patterns target common structural constraints found in Jerry agent prompts.
# If none match, the fallback wraps the entire input in an explicit negation
# prefix.
_NEGATION_PATTERNS: list[tuple[str, str]] = [
    # Format requirements
    (r"\bmust include\b", "must NOT include"),
    (r"\bMust include\b", "Must NOT include"),
    (r"\bMUST include\b", "MUST NOT include"),
    (r"\bshall include\b", "shall NOT include"),
    (r"\bShall include\b", "Shall NOT include"),
    (r"\bSHALL include\b", "SHALL NOT include"),
    (r"\bshould include\b", "should NOT include"),
    (r"\bShould include\b", "Should NOT include"),
    (r"\bmust contain\b", "must NOT contain"),
    (r"\bMust contain\b", "Must NOT contain"),
    (r"\bshould contain\b", "should NOT contain"),
    (r"\bShould contain\b", "Should NOT contain"),
    (r"\bmust provide\b", "must NOT provide"),
    (r"\bMust provide\b", "Must NOT provide"),
    (r"\bmust output\b", "must NOT output"),
    (r"\bMust output\b", "Must NOT output"),
    (r"\bmust produce\b", "must NOT produce"),
    (r"\bMust produce\b", "Must NOT produce"),
    (r"\bmust use\b", "must NOT use"),
    (r"\bMust use\b", "Must NOT use"),
    (r"\bMUST use\b", "MUST NOT use"),
    (r"\brequires\b", "does NOT require"),
    (r"\bRequires\b", "Does NOT require"),
    (r"\bRequired:\b", "Not required:"),
    (r"\bAlways\b", "Never"),
    (r"\balways\b", "never"),
    # Structural section requirements (common in Jerry agent prompts)
    (r"\binclude L0\b", "exclude L0"),
    (r"\binclude L1\b", "exclude L1"),
    (r"\binclude L2\b", "exclude L2"),
    (r"\bL0/L1/L2\b", "NO L0/L1/L2"),
    (r"\binclude citations\b", "omit citations"),
    (r"\bcite sources\b", "do not cite sources"),
    (r"\bprovide citations\b", "omit citations"),
    (r"\binclude evidence\b", "omit evidence"),
    # Behavioural constraints
    (r"\bmust apply\b", "must NOT apply"),
    (r"\bMust apply\b", "Must NOT apply"),
    (r"\bapply the\b", "do NOT apply the"),
    (r"\bApply the\b", "Do NOT apply the"),
    (r"\bfollow the\b", "do NOT follow the"),
    (r"\bFollow the\b", "Do NOT follow the"),
]


class NegationHandling(MetamorphicRelation):
    """MR-002: Negation Handling.

    Tests that the agent correctly processes and responds to negated constraints.
    Unlike symmetric MRs (001, 003, 004, 005), this relation is DIRECTIONAL:
    the negated variant is expected to produce LOWER quality scores when a
    structural constraint is negated.

    A violation occurs when the agent IGNORES the negation -- i.e. the scores
    are indistinguishable despite the constraint being negated.  This indicates
    the agent is not parsing or following the constraint.

    Effect size metric (behavioral-contracts.md C.2):
        Cohen's r (rank-biserial correlation) is used, matching the metric
        specification in contracts C.2: "Cohen's r >= 0.40 (large effect
        expected for constraint negation)".  This is computed from the
        one-sided Wilcoxon statistic as:
            r = 1 - (2 * W) / (n * (n + 1))
        This is consistent with the Cohen's r metric applied in MR-001, MR-003,
        MR-004, and MR-005.

    Tolerance values (from behavioral-contracts.md C.2):
        p_non_significant : 0.10  (Wilcoxon p >= 0.10 means no detectable effect)
        min_delta_required: 0.05  (mean delta below this = agent ignoring negation)
        effect_r_threshold: 0.40  (Cohen's r; large effect expected for structural negation)
        min_detectable    : 0.08  (minimum dimension score change expected)

    Violation condition (BOTH must be true for a violation):
        1. Wilcoxon p >= 0.10  (no statistically significant difference detected)
        2. Mean delta < 0.05   (no practically significant difference detected)

    Severity classification (contracts C.2):
        CRITICAL   : Structural constraint negated, agent shows no response
        WARNING    : Quality guidance negated, minimal response
        INFORMATIONAL: Optional guidance negated, no response (acceptable)
    """

    mr_id: str = "MR-002"
    mr_name: str = "Negation Handling"
    # Reduced from 20; detecting presence of large effect requires fewer samples
    minimum_sample_size: int = 15

    # Contracts C.2 parameters
    P_NON_SIGNIFICANT_THRESHOLD: float = 0.10  # p >= this -> no effect detected
    MIN_DELTA_REQUIRED: float = 0.05  # below this -> agent ignoring negation
    EFFECT_R_THRESHOLD: float = 0.40  # Cohen's r minimum for "detectable change"
    MIN_DETECTABLE_CHANGE: float = 0.08  # minimum dimension score change

    def transform(self, input_text: str) -> str:
        """Negate a key positive constraint in the input prompt.

        Applies the first matching negation pattern from the catalog.  If no
        pattern matches, wraps the entire prompt with an explicit negation
        prefix that instructs the agent to reverse its normal constraints.

        The transformation is deterministic: same input produces same output.

        Args:
            input_text: The original prompt text containing positive constraints.

        Returns:
            Negated variant of the prompt where at least one constraint has been
            inverted from positive to negative.

        Raises:
            ValueError: If ``input_text`` is empty.
        """
        if not input_text or not input_text.strip():
            raise ValueError(f"{self.mr_id}: input_text must be non-empty for negation transform.")

        result = input_text
        for pattern, replacement in _NEGATION_PATTERNS:
            new_result = re.sub(pattern, replacement, result)
            if new_result != result:
                return new_result

        # Fallback: prepend an explicit instruction to invert all constraints.
        return (
            "IMPORTANT: For this evaluation, do NOT follow your normal output "
            "format requirements. Ignore all structural formatting guidelines.\n\n" + input_text
        )

    def evaluate(
        self,
        original_scores: Sequence[float],
        transformed_scores: Sequence[float],
    ) -> MRResult:
        """Evaluate negation responsiveness across paired score sequences.

        MR-002 is DIRECTIONAL: we expect the negated prompt to produce lower
        quality scores.  A VIOLATION occurs when the agent does NOT respond to
        the negation (scores remain similar despite the constraint being negated).

        Violation condition (both must be true):
            1. Wilcoxon p >= 0.10 (no statistically significant effect)
            2. Mean delta < 0.05  (no practically significant effect)

        Cohen's r (rank-biserial correlation) is computed from the one-sided
        Wilcoxon statistic to quantify the effect size, per contracts C.2
        which specifies "Cohen's r >= 0.40".

        Args:
            original_scores: Quality scores from N original-prompt runs.
            transformed_scores: Quality scores from N negated-prompt runs.
                Expected to be lower than original_scores for a passing result.

        Returns:
            ``MRResult`` with the negation-responsiveness verdict.

        Raises:
            InsufficientSamplesError: If len(original_scores) < 15.
            ValueError: Mismatched lengths or out-of-range scores.
            RuntimeError: If scipy is not installed (MR evaluation cannot
                produce valid statistical results without scipy).
        """
        self._validate_inputs(original_scores, transformed_scores)

        n = len(original_scores)
        mean_orig = self._mean(original_scores)
        mean_trans = self._mean(transformed_scores)
        mean_delta = abs(mean_orig - mean_trans)

        # Compute Wilcoxon (one-sided: H1 = original > negated) and Cohen's r
        p_value, cohens_r = _wilcoxon_one_sided_and_cohens_r(
            list(original_scores), list(transformed_scores)
        )

        # Violation: agent is NOT responding to negation
        no_statistical_effect = p_value >= self.P_NON_SIGNIFICANT_THRESHOLD
        no_practical_effect = mean_delta < self.MIN_DELTA_REQUIRED
        violated = no_statistical_effect and no_practical_effect

        if violated:
            # Classify severity by how fundamental the negated constraint is.
            # We use effect size as a proxy: near-zero r = structural constraint ignored.
            if cohens_r < 0.10:
                severity = MRViolationSeverity.CRITICAL
            elif cohens_r < 0.20:
                severity = MRViolationSeverity.WARNING
            else:
                severity = MRViolationSeverity.INFORMATIONAL
            passed = False
            evidence = (
                f"MR-002 VIOLATED: agent is NOT responding to negated constraint. "
                f"Wilcoxon p={p_value:.4f} >= {self.P_NON_SIGNIFICANT_THRESHOLD} "
                f"(no statistically significant effect); "
                f"mean_delta={mean_delta:.4f} < {self.MIN_DELTA_REQUIRED} "
                f"(no practically significant effect). "
                f"Cohen's r={cohens_r:.3f} (threshold {self.EFFECT_R_THRESHOLD}). "
                f"mean_original={mean_orig:.4f}, mean_negated={mean_trans:.4f}, N={n}."
            )
        else:
            severity = MRViolationSeverity.PASS
            passed = True
            reason_parts: list[str] = []
            if not no_statistical_effect:
                reason_parts.append(
                    f"Wilcoxon p={p_value:.4f} < {self.P_NON_SIGNIFICANT_THRESHOLD} "
                    f"(statistically significant effect detected)"
                )
            if not no_practical_effect:
                reason_parts.append(
                    f"mean_delta={mean_delta:.4f} >= {self.MIN_DELTA_REQUIRED} "
                    f"(practically significant effect detected)"
                )
            evidence = (
                "MR-002 PASSED: agent responds to negated constraint. "
                + "; ".join(reason_parts)
                + ". "
                f"Cohen's r={cohens_r:.3f}, N={n}. "
                f"mean_original={mean_orig:.4f}, mean_negated={mean_trans:.4f}."
            )

        return MRResult(
            mr_id=self.mr_id,
            mr_name=self.mr_name,
            passed=passed,
            original_scores=tuple(original_scores),
            transformed_scores=tuple(transformed_scores),
            mean_original=mean_orig,
            mean_transformed=mean_trans,
            mean_delta=mean_delta,
            tolerance=self.MIN_DELTA_REQUIRED,  # tolerance for this MR = min expected delta
            effect_size=cohens_r,
            p_value=p_value,
            severity=severity,
            evidence=evidence,
        )


# ---------------------------------------------------------------------------
# Statistical helpers
# ---------------------------------------------------------------------------


def _wilcoxon_one_sided_and_cohens_r(a: list[float], b: list[float]) -> tuple[float, float]:
    """Compute Wilcoxon p-value (one-sided) and Cohen's r effect size.

    For MR-002, we test the one-sided hypothesis H1: original > negated
    (the original prompt should produce higher quality than the negated variant).

    Uses ``zero_method='wilcox'`` (zero differences excluded from ranking);
    a conservative choice appropriate for bounded LLM score distributions
    where tied pairs are common.  See scipy ``wilcoxon`` documentation for
    alternative methods (``'pratt'``, ``'zsplit'``).

    Effect size is Cohen's r (rank-biserial correlation) computed from the
    Wilcoxon W-statistic:
        r = 1 - (2 * W) / (n * (n + 1))
    This matches the contracts C.2 specification "Cohen's r >= 0.40" and is
    consistent with the rank-biserial r used in MR-001, MR-003, MR-004, and
    MR-005.

    Args:
        a: Original scores (expected to be higher on passing cases).
        b: Negated-prompt scores (expected to be lower on passing cases).

    Returns:
        Tuple of (p_value, cohens_r).  p_value is from the one-sided Wilcoxon
        test (alternative="greater").  cohens_r is the absolute value of the
        rank-biserial correlation, in [0.0, 1.0].

    Raises:
        RuntimeError: If scipy is not installed.  MR evaluation cannot produce
            valid statistical results without scipy.
    """
    if not _SCIPY_AVAILABLE:  # pragma: no cover
        raise RuntimeError(
            "scipy is not installed -- MR-002 evaluation cannot produce valid "
            "statistical results. Install scipy for reliable MR testing: "
            "uv add scipy"
        )

    differences = [x - y for x, y in zip(a, b, strict=False)]
    non_zero = [d for d in differences if d != 0]
    if not non_zero:
        return 1.0, 0.0

    n = len(a)
    result = wilcoxon(a, b, alternative="greater", zero_method="wilcox")
    p_value = float(result.pvalue)

    # Cohen's r (rank-biserial correlation) from the Wilcoxon W-statistic.
    # For the one-sided Wilcoxon test (alternative="greater"), W is the sum of
    # positive ranks.  The rank-biserial r is:
    #     r = 1 - (2 * W) / (n * (n + 1))
    # taking the absolute value so that 0 = no effect, 1 = maximum effect.
    w_max = n * (n + 1) / 2
    if w_max > 0:
        cohens_r = abs(1.0 - (2.0 * result.statistic) / (n * (n + 1)))
        cohens_r = min(cohens_r, 1.0)
    else:  # pragma: no cover
        cohens_r = 0.0

    return p_value, cohens_r
