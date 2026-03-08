# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""MR-001: Paraphrase Consistency metamorphic relation.

Definition (behavioral-contracts.md Section C.1):
    Paraphrasing the user-facing portion of a system prompt should not change
    output quality by more than 0.05 (absolute delta).

Tolerance: 0.05 (max |score_original - score_paraphrased|)
Violation condition: Wilcoxon p < 0.05 AND mean_delta > 0.05 (both required)
Effect size threshold: Cohen's r >= 0.30 (medium effect)
Minimum sample size: 20 pairs (ADR-001 FM-002)

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
# Paraphrase templates
# ---------------------------------------------------------------------------

# A curated set of simple, rule-based paraphrase transformations that preserve
# semantic meaning without requiring an LLM call.  This keeps the transform()
# method deterministic and free of external dependencies.
#
# Each entry is a (pattern, replacement) tuple.  Patterns are applied in order;
# the first match wins.  If no pattern matches, the fallback transformation
# normalises whitespace and rephrases the opening clause.
_PARAPHRASE_SUBSTITUTIONS: list[tuple[str, str]] = [
    # Imperative verbs -> synonyms
    (r"\bResearch\b", "Survey"),
    (r"\bresearch\b", "survey"),
    (r"\bInvestigate\b", "Examine"),
    (r"\binvestigate\b", "examine"),
    (r"\bAnalyze\b", "Evaluate"),
    (r"\banalyze\b", "evaluate"),
    (r"\bAnalyse\b", "Assess"),
    (r"\banalyse\b", "assess"),
    (r"\bCreate\b", "Produce"),
    (r"\bcreate\b", "produce"),
    (r"\bGenerate\b", "Produce"),
    (r"\bgenerate\b", "produce"),
    (r"\bSummarise\b", "Condense"),
    (r"\bsummarise\b", "condense"),
    (r"\bSummarize\b", "Condense"),
    (r"\bsummarize\b", "condense"),
    (r"\bDocument\b", "Record"),
    (r"\bdocument\b", "record"),
    (r"\bExplain\b", "Describe"),
    (r"\bexplain\b", "describe"),
    (r"\bDescribe\b", "Detail"),
    (r"\bdescribe\b", "detail"),
    (r"\bIdentify\b", "Determine"),
    (r"\bidentify\b", "determine"),
    (r"\bCompare\b", "Contrast and compare"),
    (r"\bcompare\b", "contrast and compare"),
    (r"\bEvaluate\b", "Assess"),
    (r"\bevaluate\b", "assess"),
    # Common phrases
    (r"\bwith respect to\b", "regarding"),
    (r"\bin order to\b", "to"),
    (r"\bprovide a\b", "give a"),
    (r"\bprovide an\b", "give an"),
    (r"\butilise\b", "use"),
    (r"\butilize\b", "use"),
    (r"\bimplement\b", "build"),
    (r"\bImplement\b", "Build"),
    (r"\bensure\b", "make sure"),
    (r"\bEnsure\b", "Make sure"),
    (r"\bfocus on\b", "concentrate on"),
    (r"\bFocus on\b", "Concentrate on"),
    (r"\bapproaches\b", "methods"),
    (r"\bapproach\b", "method"),
    (r"\bpatterns\b", "practices"),
    (r"\bpattern\b", "practice"),
    (r"\barchitecture\b", "design"),
    (r"\bArchitecture\b", "Design"),
]


class ParaphraseConsistency(MetamorphicRelation):
    """MR-001: Paraphrase Consistency.

    Tests that paraphrasing the task description portion of a prompt does not
    change output quality by more than the tolerance threshold.

    Tolerance values (from behavioral-contracts.md C.1):
        max_delta  = 0.05   (absolute mean score delta)
        p_alpha    = 0.05   (Wilcoxon significance level)
        effect_r   = 0.30   (Cohen's r minimum for practical significance)

    Violation condition (both must be true):
        1. Wilcoxon signed-rank p-value < 0.05
        2. Mean absolute delta across pairs > 0.05

    A single condition alone does not constitute a violation per the contracts;
    this dual-condition requirement reduces false positives from LLM sampling
    variance (LLMORPH baseline: 8.6% false positive rate).
    """

    mr_id: str = "MR-001"
    mr_name: str = "Paraphrase Consistency"
    minimum_sample_size: int = 20

    # Tolerance from behavioral-contracts.md Section C.1
    TOLERANCE: float = 0.05
    # Wilcoxon significance level
    P_ALPHA: float = 0.05
    # Minimum Cohen's r for practical significance
    EFFECT_R_THRESHOLD: float = 0.30

    def transform(self, input_text: str) -> str:
        """Apply a rule-based paraphrase to the input text.

        Substitutes common imperative verbs and phrases with synonyms to
        produce a semantically equivalent but lexically distinct variant.
        Transformations are deterministic; no external services are called.

        Multiple substitutions may apply; they are applied sequentially so that
        later substitutions do not re-match the outputs of earlier ones (each
        pattern targets distinct tokens).

        Args:
            input_text: The original prompt text to paraphrase.

        Returns:
            Paraphrased text preserving the original semantic intent.

        Raises:
            ValueError: If ``input_text`` is empty.
        """
        if not input_text or not input_text.strip():
            raise ValueError(
                f"{self.mr_id}: input_text must be non-empty for paraphrase transform."
            )

        result = input_text
        applied_any = False
        for pattern, replacement in _PARAPHRASE_SUBSTITUTIONS:
            new_result = re.sub(pattern, replacement, result)
            if new_result != result:
                result = new_result
                applied_any = True

        if not applied_any:
            # Fallback: normalise double spaces and append a restatement clause.
            result = re.sub(r"  +", " ", input_text.strip())
            result = result + " (Please address the above task.)"

        return result

    def evaluate(
        self,
        original_scores: Sequence[float],
        transformed_scores: Sequence[float],
    ) -> MRResult:
        """Evaluate paraphrase consistency across paired score sequences.

        Applies the dual-condition violation check from contracts C.1:
        1. Wilcoxon signed-rank p < 0.05
        2. Mean absolute delta > TOLERANCE (0.05)

        Effect size is computed as Cohen's r = Z / sqrt(N), where Z is the
        Wilcoxon Z-score (|statistic| normalised).

        Args:
            original_scores: Quality scores from N original-prompt runs.
            transformed_scores: Quality scores from N paraphrased-prompt runs.

        Returns:
            ``MRResult`` with verdict, delta, effect size, p-value, and evidence.

        Raises:
            InsufficientSamplesError: If len(original_scores) < 20.
            ValueError: Mismatched lengths or out-of-range scores.
        """
        self._validate_inputs(original_scores, transformed_scores)

        n = len(original_scores)
        mean_orig = self._mean(original_scores)
        mean_trans = self._mean(transformed_scores)
        mean_delta = abs(mean_orig - mean_trans)

        # Compute Wilcoxon signed-rank test
        p_value, effect_r = _wilcoxon_p_and_effect(
            list(original_scores), list(transformed_scores), n
        )

        # Dual-condition violation: both p < alpha AND mean_delta > tolerance
        statistically_significant = p_value < self.P_ALPHA
        practically_significant = mean_delta > self.TOLERANCE
        violated = statistically_significant and practically_significant

        if violated:
            if effect_r >= self.EFFECT_R_THRESHOLD:
                severity = MRViolationSeverity.REGRESSION
            else:
                severity = MRViolationSeverity.WARNING
            passed = False
            evidence = (
                f"MR-001 VIOLATED: paraphrase changed quality by {mean_delta:.4f} "
                f"(tolerance {self.TOLERANCE}). "
                f"Wilcoxon p={p_value:.4f} (alpha {self.P_ALPHA}), "
                f"Cohen's r={effect_r:.3f} (threshold {self.EFFECT_R_THRESHOLD}). "
                f"mean_original={mean_orig:.4f}, mean_paraphrased={mean_trans:.4f}, N={n}."
            )
        else:
            severity = MRViolationSeverity.PASS
            passed = True
            reason_parts: list[str] = []
            if not statistically_significant:
                reason_parts.append(
                    f"Wilcoxon p={p_value:.4f} >= alpha {self.P_ALPHA} (not significant)"
                )
            if not practically_significant:
                reason_parts.append(f"mean_delta={mean_delta:.4f} <= tolerance {self.TOLERANCE}")
            evidence = (
                "MR-001 PASSED: " + "; ".join(reason_parts) + ". "
                f"mean_original={mean_orig:.4f}, mean_paraphrased={mean_trans:.4f}, "
                f"Cohen's r={effect_r:.3f}, N={n}."
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
            tolerance=self.TOLERANCE,
            effect_size=effect_r,
            p_value=p_value,
            severity=severity,
            evidence=evidence,
        )


# ---------------------------------------------------------------------------
# Shared statistical helper (module-private)
# ---------------------------------------------------------------------------


def _wilcoxon_p_and_effect(a: list[float], b: list[float], n: int) -> tuple[float, float]:
    """Compute Wilcoxon signed-rank p-value and Cohen's r effect size.

    Requires scipy.stats.wilcoxon.  Raises RuntimeError when scipy is not
    installed to prevent silent all-PASS results in environments lacking the
    dependency (Priority 2: scipy fallback must not mask violations).

    Uses ``zero_method='wilcox'`` (zero differences excluded from ranking);
    a conservative choice appropriate for bounded LLM score distributions
    where tied pairs are common.  See scipy ``wilcoxon`` documentation for
    alternative methods (``'pratt'``, ``'zsplit'``).

    Cohen's r = |W_statistic| / sqrt(N * (N + 1) * (2*N + 1) / 6) is the
    rank-biserial correlation approximation for the Wilcoxon test.

    Used by MR-001, MR-003, MR-004, and MR-005 for two-sided testing.

    Args:
        a: Original score list of length N.
        b: Transformed score list of length N.
        n: Sample size (len(a) == len(b) == n).

    Returns:
        Tuple of (p_value, cohens_r).  Both are floats in [0.0, 1.0].

    Raises:
        RuntimeError: If scipy is not installed.
    """
    if not _SCIPY_AVAILABLE:  # pragma: no cover
        raise RuntimeError(
            "scipy is not installed -- MR evaluation cannot produce valid "
            "statistical results. Install scipy for reliable MR testing: "
            "uv add scipy"
        )

    differences = [x - y for x, y in zip(a, b, strict=False)]
    non_zero = [d for d in differences if d != 0]
    if not non_zero:
        # All differences are zero: no effect.
        return 1.0, 0.0

    result = wilcoxon(a, b, alternative="two-sided", zero_method="wilcox")
    p_value = float(result.pvalue)

    # Cohen's r from the Wilcoxon statistic
    # W-statistic range for Wilcoxon is [0, n*(n+1)/2]
    # Rank-biserial r = 1 - (4 * W) / (n * (n + 1))  (two-sided version)
    w_max = n * (n + 1) / 2
    if w_max > 0:
        cohens_r = abs(1.0 - (4.0 * result.statistic) / (n * (n + 1)))
        cohens_r = min(cohens_r, 1.0)
    else:  # pragma: no cover
        cohens_r = 0.0

    return p_value, cohens_r
