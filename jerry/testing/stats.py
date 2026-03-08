# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""Core statistical functions for the Four-Layer Composite Test Harness.

This module is the SSOT for all statistical computation in the harness.  It is
shared between PROJ-036 (prompt regression) and PROJ-017 (skill evaluation
framework) as specified in FR-019.

Module boundaries (H-07):
    - Imports ONLY from stdlib, scipy, statsmodels, and jerry.testing.types.
    - MUST NOT import from jerry.testing.evaluation, jerry.testing.metamorphic,
      jerry.testing.baselines, jerry.testing.reports, or jerry.testing.layer4_stats.
    - All statistical logic lives here; layer4_stats.py orchestrates it but
      does not re-implement it.

Statistical methods implemented:
    1. Wilcoxon signed-rank test (scipy.stats.wilcoxon, two-sided) — FR-015
    2. Wilson score confidence intervals (statsmodels, method="wilson") — FR-016
    3. Bonferroni correction for multi-metric comparisons — FR-017
    4. Cohen's r effect size from Wilcoxon Z-statistic — per contracts.md D.4
    5. N >= 20 enforcement (InsufficientSamplesError) — FR-014

Named constants (FR-014, FR-016, FR-017 acceptance criteria):
    MIN_STATISTICAL_SAMPLE_SIZE = 20
    QUALITY_PASS_THRESHOLD      = 0.92
    BONFERRONI_K_FULL_SUITE     = 13
    BONFERRONI_ALPHA_FULL       = 0.004

References:
    [1] Wilcoxon (1945). Biometrics Bulletin 1(6).
    [2] Wilson (1927). JASA 22(158).
    [3] Cohen (1988). Statistical Power Analysis.
    [7] scipy.stats.wilcoxon docs (2024).
    [8] statsmodels proportion_confint docs (2024).
"""

from __future__ import annotations

import math
import statistics

import scipy.stats
import statsmodels.stats.proportion

from jerry.testing.types import (
    BonferroniConfig,
    EffectSizeLabel,
    EvaluationMode,
    MergeDecision,
    RateClass,
    RegressionClass,
    RegressionResult,
    ScoreArray,
    WilcoxonResult,
    WilsonResult,
)

# ---------------------------------------------------------------------------
# Named constants (FR-014, FR-016, FR-017 acceptance criteria)
# ---------------------------------------------------------------------------

#: Minimum number of paired observations required for Wilcoxon signed-rank.
#: FR-014: "The N=20 threshold shall be a named constant ... in jerry/testing/stats.py."
MIN_STATISTICAL_SAMPLE_SIZE: int = 20

#: Quality gate pass threshold (H-13 from quality-enforcement.md).
#: FR-016: "The 0.92 pass-rate threshold shall be the named constant
#: QUALITY_PASS_THRESHOLD = 0.92 in jerry/testing/stats.py."
QUALITY_PASS_THRESHOLD: float = 0.92

#: Number of simultaneous comparisons in the full evaluation suite.
#: Behavioral-contracts.md Section D.3: "6 S-014 dimensions + 1 composite
#: score + 5 MRs + 1 pass rate = 13."
BONFERRONI_K_FULL_SUITE: int = 13

#: Bonferroni-corrected alpha for the full 13-metric evaluation suite.
#: Contracts D.3: 0.05/13 = 0.003846..., rounded to 0.004 per contract convention
#: (conservative 3-significant-figure rounding).  Stored as a literal to match
#: the contracts-specified value exactly; round(0.05/13, 4) = 0.0038, which would
#: be a 5% relative error from the specified threshold.
BONFERRONI_ALPHA_FULL: float = 0.004

#: Significance threshold for REGRESSION classification (uncorrected).
_ALPHA_REGRESSION: float = 0.05

#: Significance threshold for MARGINAL classification (uncorrected).
_ALPHA_MARGINAL: float = 0.10

#: Effect size thresholds for Cohen's r (contracts.md Section D.4).
_EFFECT_NEGLIGIBLE: float = 0.10
_EFFECT_SMALL: float = 0.20
_EFFECT_MEDIUM_LARGE: float = 0.30


# ---------------------------------------------------------------------------
# Custom exceptions
# ---------------------------------------------------------------------------


class InsufficientSamplesError(ValueError):
    """Raised when either score array has fewer than MIN_STATISTICAL_SAMPLE_SIZE
    observations.

    FR-014 acceptance criterion: the error message shall use the format:
        "Wilcoxon requires N >= 20 per version (got {N_a}, {N_b}).
         Use Smoke mode for single-run structural checks only."
    """

    pass


class InvalidScoreArrayError(ValueError):
    """Raised when a score array fails validation (out-of-range values, all
    identical values that defeat significance testing, or non-numeric content).

    Addresses system-design.md security control: "Statistical comparison inputs
    are validated — the statistical engine rejects adversarially crafted score
    sequences."
    """

    pass


# ---------------------------------------------------------------------------
# Input validation
# ---------------------------------------------------------------------------


def _validate_score_array(
    scores: ScoreArray,
    name: str,
    *,
    require_variation: bool = False,
) -> None:
    """Validate a score array for range, type, and (optionally) variation.

    Args:
        scores:           The score array to validate.
        name:             Human-readable name used in error messages
                          (e.g., "scores_a").
        require_variation: When True, raises if all scores are identical.
                          Set to True for Wilcoxon inputs (all-identical
                          scores defeat significance testing and may represent
                          adversarial tampering).  Set to False (default) for
                          Wilson score interval inputs, where all-identical
                          scores are valid (e.g., every run passed the quality
                          gate, so all scores are 1.0 or all are 0.0).

    Raises:
        InvalidScoreArrayError: If any score is outside [0.0, 1.0], if the
            array is empty, or (when require_variation=True) if all scores
            are identical.
    """
    if not scores:
        raise InvalidScoreArrayError(f"{name} must not be empty.")

    for i, s in enumerate(scores):
        if not isinstance(s, int | float):
            raise InvalidScoreArrayError(f"{name}[{i}] is not numeric: {s!r}.")
        if not (0.0 <= float(s) <= 1.0):
            raise InvalidScoreArrayError(f"{name}[{i}] = {s} is out of range [0.0, 1.0].")

    if require_variation and len(set(scores)) == 1:
        # Detect degenerate all-identical sequences (adversarial tampering
        # guard for Wilcoxon inputs only).  All-zeros or all-ones sequences
        # produce W=0, p=1.0 trivially, which could suppress regression
        # signals.
        raise InvalidScoreArrayError(
            f"{name} contains all identical values ({scores[0]}). "
            "All-identical score arrays are degenerate distributions that "
            "defeat significance testing.  Verify the evaluation pipeline "
            "produced valid score variation."
        )


# ---------------------------------------------------------------------------
# Effect size helpers
# ---------------------------------------------------------------------------


def _cohens_r(statistic: float, n_pairs: int) -> float:
    """Compute Cohen's r effect size from a Wilcoxon signed-rank statistic.

    The Wilcoxon statistic W is converted to a Z-score using the normal
    approximation for the signed-rank distribution, then Cohen's r is
    derived as r = |Z| / sqrt(N) per Cohen (1988) and scipy docs [7].

    The expected value and variance of W under H0 for n non-tied pairs:
        mu_W  = n*(n+1)/4
        var_W = n*(n+1)*(2*n+1)/24

    Args:
        statistic: The Wilcoxon W statistic from scipy.stats.wilcoxon.
        n_pairs:   Number of paired observations.

    Returns:
        Cohen's r in [0.0, 1.0].
    """
    n = n_pairs
    if n <= 1:
        return 0.0
    mu_w = n * (n + 1) / 4.0
    var_w = n * (n + 1) * (2 * n + 1) / 24.0
    if var_w <= 0.0:
        return 0.0
    z = abs(statistic - mu_w) / math.sqrt(var_w)
    r = z / math.sqrt(n)
    # Clamp to [0, 1] for numerical robustness.
    return min(max(r, 0.0), 1.0)


def _effect_label(r: float) -> EffectSizeLabel:
    """Map Cohen's r to a human-readable effect size label.

    Per behavioral-contracts.md Section D.4:
        r < 0.10           → Negligible
        0.10 <= r < 0.20   → Small
        0.20 <= r < 0.30   → Small-to-Medium
        r >= 0.30          → Medium-to-Large

    Args:
        r: Cohen's r effect size (>= 0).

    Returns:
        EffectSizeLabel enum value.
    """
    if r < _EFFECT_NEGLIGIBLE:
        return EffectSizeLabel.NEGLIGIBLE
    if r < _EFFECT_SMALL:
        return EffectSizeLabel.SMALL
    if r < _EFFECT_MEDIUM_LARGE:
        return EffectSizeLabel.SMALL_TO_MEDIUM
    return EffectSizeLabel.MEDIUM_TO_LARGE


# ---------------------------------------------------------------------------
# Wilcoxon signed-rank test
# ---------------------------------------------------------------------------


def wilcoxon_signed_rank(
    scores_a: ScoreArray,
    scores_b: ScoreArray,
) -> WilcoxonResult:
    """Run the Wilcoxon signed-rank test on two paired score arrays.

    This is the raw statistical computation.  It does NOT enforce N >= 20 —
    that enforcement belongs to ``compare_versions()``.  Use this function
    when you need the raw test result and have already verified N.

    The test is always two-sided (alternative="two-sided") per behavioral-
    contracts.md Section D.1.  Tie handling uses scipy's default (average
    ranks, i.e., method="wilcox" in older APIs, or "auto" which selects
    the exact method for small N).

    Args:
        scores_a: Baseline score array (N floats in [0.0, 1.0]).
        scores_b: Candidate score array (N floats in [0.0, 1.0]).

    Returns:
        WilcoxonResult with statistic, p_value, cohens_r, effect_label,
        mean_delta, mean_a, mean_b.

    Raises:
        InvalidScoreArrayError: If either array fails validation.
    """
    _validate_score_array(scores_a, "scores_a", require_variation=True)
    _validate_score_array(scores_b, "scores_b", require_variation=True)

    n = len(scores_a)
    # Pair-wise; truncate to shorter array if lengths differ (caller should
    # ensure equal lengths but we handle gracefully).
    pairs = min(n, len(scores_b))
    a_paired = scores_a[:pairs]
    b_paired = scores_b[:pairs]

    stat, p = scipy.stats.wilcoxon(
        a_paired,
        b_paired,
        alternative="two-sided",
        # Use "wilcox" to match exact normal approximation; scipy default.
    )

    cohens_r = _cohens_r(float(stat), pairs)
    label = _effect_label(cohens_r)
    mean_a = statistics.mean(a_paired)
    mean_b = statistics.mean(b_paired)

    return WilcoxonResult(
        statistic=float(stat),
        p_value=float(p),
        n_pairs=pairs,
        cohens_r=cohens_r,
        effect_label=label,
        mean_delta=mean_b - mean_a,
        mean_a=mean_a,
        mean_b=mean_b,
    )


# ---------------------------------------------------------------------------
# Wilson score confidence intervals
# ---------------------------------------------------------------------------


def wilson_score_intervals(
    scores: ScoreArray,
    threshold: float = QUALITY_PASS_THRESHOLD,
    confidence: float = 0.95,
) -> WilsonResult:
    """Compute the Wilson score confidence interval for a quality pass rate.

    The pass rate is the proportion of scores >= ``threshold``.  The 95%
    Wilson score CI is computed using statsmodels.stats.proportion.
    proportion_confint with method="wilson" (FR-016).

    Wilson's method maintains near-nominal coverage for any N >= 10 and any
    proportion p, unlike the Wald (normal approximation) interval which
    exhibits poor coverage at extreme proportions and small N.

    Args:
        scores:     Score array to evaluate.
        threshold:  Pass threshold (default QUALITY_PASS_THRESHOLD = 0.92).
        confidence: Confidence level for the interval (default 0.95).

    Returns:
        WilsonResult with n_total, n_pass, pass_rate, ci_lower, ci_upper,
        ci_width.

    Raises:
        InvalidScoreArrayError: If the array fails validation.
    """
    _validate_score_array(scores, "scores")

    n_total = len(scores)
    n_pass = sum(1 for s in scores if s >= threshold)
    alpha = 1.0 - confidence

    lo, hi = statsmodels.stats.proportion.proportion_confint(
        count=n_pass,
        nobs=n_total,
        alpha=alpha,
        method="wilson",
    )

    pass_rate = n_pass / n_total if n_total > 0 else 0.0

    return WilsonResult(
        n_total=n_total,
        n_pass=n_pass,
        pass_rate=pass_rate,
        ci_lower=float(lo),
        ci_upper=float(hi),
        ci_width=float(hi) - float(lo),
    )


# ---------------------------------------------------------------------------
# Bonferroni correction
# ---------------------------------------------------------------------------


def bonferroni_correction(
    k: int,
    alpha_family: float = 0.05,
) -> BonferroniConfig:
    """Compute Bonferroni correction parameters for k simultaneous tests.

    The corrected per-test alpha = alpha_family / k.  For the full
    13-metric evaluation suite (6 S-014 dimensions + composite + 5 MRs
    + pass rate), use k=BONFERRONI_K_FULL_SUITE.

    FR-017 acceptance criterion: the report shall disclose the correction
    via BonferroniConfig.description.

    Args:
        k:             Number of simultaneous comparisons (>= 1).
        alpha_family:  Family-wise error rate target (default 0.05).

    Returns:
        BonferroniConfig with k, alpha_family, and alpha_per_test.

    Raises:
        ValueError: If k < 1 or alpha_family not in (0, 1).
    """
    if k < 1:
        raise ValueError(f"k must be >= 1, got {k}.")
    if not (0.0 < alpha_family < 1.0):
        raise ValueError(f"alpha_family must be in (0, 1), got {alpha_family}.")
    return BonferroniConfig(
        k=k,
        alpha_family=alpha_family,
        alpha_per_test=alpha_family / k,
    )


# ---------------------------------------------------------------------------
# Regression classification logic
# ---------------------------------------------------------------------------


def _classify_regression(
    wilcoxon_result: WilcoxonResult,
    alpha: float,
) -> RegressionClass:
    """Apply the combined p-value + effect-size classification rules.

    Per behavioral-contracts.md Section D.4 combined classification table:

        p >= 0.10 (any r)                  → NO_REGRESSION
        0.05 <= p < 0.10, r < 0.20         → NO_REGRESSION
        0.05 <= p < 0.10, r >= 0.20        → MARGINAL
        p < 0.05, r < 0.10                 → NO_REGRESSION (negligible effect)
        p < 0.05, 0.10 <= r < 0.30,        → MARGINAL (if mean_delta < 0)
          mean_delta < 0
        p < 0.05, r >= 0.30, mean_delta < 0 → REGRESSION
        p < 0.05, r >= any, mean_delta >= 0 → IMPROVEMENT

    Note: when a Bonferroni-corrected alpha is supplied, the REGRESSION
    threshold uses ``alpha`` and the MARGINAL threshold uses ``2 * alpha``.
    This preserves the relative ratio (MARGINAL = 2x the REGRESSION
    threshold) which mirrors the uncorrected 0.05/0.10 pair.

    Args:
        wilcoxon_result: Result of wilcoxon_signed_rank().
        alpha:           Effective significance threshold (may be
                         Bonferroni-corrected).

    Returns:
        RegressionClass.
    """
    p = wilcoxon_result.p_value
    r = wilcoxon_result.cohens_r
    delta = wilcoxon_result.mean_delta

    # Marginal threshold is always 2x the regression threshold.
    alpha_marginal = alpha * (_ALPHA_MARGINAL / _ALPHA_REGRESSION)

    # p >= alpha_marginal → no evidence of regression regardless of effect.
    if p >= alpha_marginal:
        return RegressionClass.NO_REGRESSION

    # alpha <= p < alpha_marginal (MARGINAL zone).
    if p >= alpha:
        if r < _EFFECT_SMALL:
            return RegressionClass.NO_REGRESSION
        return RegressionClass.MARGINAL

    # p < alpha (significant zone) — direction and effect size determine verdict.
    if r < _EFFECT_NEGLIGIBLE:
        # Statistically significant but practically negligible — not a regression.
        return RegressionClass.NO_REGRESSION

    if delta >= 0.0:
        # Candidate is better or equal — improvement or stable.
        return RegressionClass.IMPROVEMENT

    # delta < 0 (candidate is worse).
    if r < _EFFECT_MEDIUM_LARGE:
        # Medium effect but below the 0.30 block threshold.
        return RegressionClass.MARGINAL

    # p < alpha, r >= 0.30, delta < 0 — full regression.
    return RegressionClass.REGRESSION


def merge_decision_from_classification(cls: RegressionClass) -> MergeDecision:
    """Map a RegressionClass to a MergeDecision.

    Per behavioral-contracts.md Section D.5 and D.4:
        REGRESSION → BLOCK
        QUALITY_FLOOR_BREACH → BLOCK
        MARGINAL → ALLOW_WITH_WARNING
        IMPROVEMENT → ALLOW_WITH_WARNING (log but don't block)
        NO_REGRESSION → ALLOW
        STRUCTURAL_FAIL → BLOCK

    Part of the FR-019 public API for stats.py (used by layer4_stats.py).

    Args:
        cls: RegressionClass verdict.

    Returns:
        MergeDecision.
    """
    if cls in (
        RegressionClass.REGRESSION,
        RegressionClass.QUALITY_FLOOR_BREACH,
        RegressionClass.STRUCTURAL_FAIL,
    ):
        return MergeDecision.BLOCK
    if cls in (RegressionClass.MARGINAL, RegressionClass.IMPROVEMENT):
        return MergeDecision.ALLOW_WITH_WARNING
    return MergeDecision.ALLOW


def _rate_class(wilson_a: WilsonResult, wilson_b: WilsonResult) -> RateClass:
    """Determine pass-rate regression via Wilson interval non-overlap.

    Per behavioral-contracts.md Section D.2:
        If ci_b.upper < ci_a.lower (non-overlapping, b is lower) → RATE_REGRESSION.
        Otherwise → RATE_STABLE.

    Args:
        wilson_a: Wilson CI for baseline version.
        wilson_b: Wilson CI for candidate version.

    Returns:
        RateClass.
    """
    if wilson_b.ci_upper < wilson_a.ci_lower:
        return RateClass.RATE_REGRESSION
    return RateClass.RATE_STABLE


# ---------------------------------------------------------------------------
# Primary public API
# ---------------------------------------------------------------------------


def compare_versions(
    scores_a: ScoreArray,
    scores_b: ScoreArray,
    *,
    metric_id: str = "composite_score",
    agent_id: str = "unknown",
    version_key_a: str = "unknown:unknown",
    version_key_b: str = "unknown:unknown",
    evaluation_mode: EvaluationMode = EvaluationMode.FULL,
    alpha: float = _ALPHA_REGRESSION,
    bonferroni: BonferroniConfig | None = None,
) -> RegressionResult:
    """Compare two prompt versions using Wilcoxon signed-rank test.

    This is the primary entry point for Layer 4 statistical comparison.
    Enforces N >= MIN_STATISTICAL_SAMPLE_SIZE for both arrays (C-008, FR-014).

    NEVER uses point-estimate thresholds as a substitute for Wilcoxon (C-006).
    The only decision mechanism is the combined p-value + effect-size rule
    implemented in ``_classify_regression()``.

    N accumulation protocol (STANDARD mode):
        STANDARD mode produces N=10 scores per invocation.  This function
        requires N >= 20.  The caller (Layer 4 pipeline or CI workflow) MUST
        accumulate multiple STANDARD batches via BaselineStore before invoking
        this function.  If accumulated N < 20, this function raises
        InsufficientSamplesError.  FULL mode (N=30) always satisfies the
        minimum in one pass.  See BaselineStore module docstring for the
        full accumulation protocol.

    Args:
        scores_a:        Baseline score array (N floats in [0.0, 1.0]).
                         Must have len >= MIN_STATISTICAL_SAMPLE_SIZE.
        scores_b:        Candidate score array (N floats in [0.0, 1.0]).
                         Must have len >= MIN_STATISTICAL_SAMPLE_SIZE.
        metric_id:       Identifier of the metric being compared.
        agent_id:        Target agent identifier.
        version_key_a:   Baseline version key ("{hash}:{path}").
        version_key_b:   Candidate version key.
        evaluation_mode: Evaluation tier (must be FULL or STANDARD for
                         statistical comparison to be valid).
        alpha:           Effective significance threshold.  Defaults to 0.05.
                         When Bonferroni correction is applied, pass
                         bonferroni.alpha_per_test here.
        bonferroni:      Bonferroni correction metadata, if applicable.
                         When provided, alpha should be bonferroni.alpha_per_test.

    Returns:
        RegressionResult encapsulating the full comparison outcome.

    Raises:
        InsufficientSamplesError: If len(scores_a) < MIN_STATISTICAL_SAMPLE_SIZE
            or len(scores_b) < MIN_STATISTICAL_SAMPLE_SIZE.  The error message
            uses the exact format required by FR-014.
        InvalidScoreArrayError:   If either array contains out-of-range values,
            all-identical values, or non-numeric content.
        ValueError:               If alpha is outside the valid range (0.001, 0.10).
    """
    # --- N >= 20 enforcement (FR-014, C-008) --------------------------------
    n_a = len(scores_a)
    n_b = len(scores_b)
    if n_a < MIN_STATISTICAL_SAMPLE_SIZE or n_b < MIN_STATISTICAL_SAMPLE_SIZE:
        raise InsufficientSamplesError(
            f"Wilcoxon requires N >= {MIN_STATISTICAL_SAMPLE_SIZE} per version "
            f"(got {n_a}, {n_b}). "
            "Use Smoke mode for single-run structural checks only."
        )

    # --- Alpha range validation ---------------------------------------------
    # FR-015 specifies (0.01, 0.10) for the uncorrected single-metric case.
    # When Bonferroni correction is applied (k=13) the per-test alpha is
    # 0.05/13 ≈ 0.0038, which legitimately falls below 0.01.  We accept
    # any alpha in [0.001, 0.10] to accommodate both paths.
    if not (0.001 <= alpha <= 0.10):
        raise ValueError(
            f"alpha must be in [0.001, 0.10], got {alpha}. "
            "FR-015 specifies (0.01, 0.10) for uncorrected single-metric use; "
            "Bonferroni-corrected alpha (e.g. 0.05/13 ≈ 0.004) is also accepted."
        )

    # --- Core statistical computations -------------------------------------
    wilcoxon_res = wilcoxon_signed_rank(scores_a, scores_b)
    wilson_a = wilson_score_intervals(scores_a)
    wilson_b = wilson_score_intervals(scores_b)

    # --- Classification ----------------------------------------------------
    classification = _classify_regression(wilcoxon_res, alpha)
    rate_cls = _rate_class(wilson_a, wilson_b)

    # Promote to REGRESSION if rate regression is detected and Wilcoxon also
    # shows significant decline (belt-and-suspenders guard).
    if rate_cls == RateClass.RATE_REGRESSION and classification == RegressionClass.MARGINAL:
        classification = RegressionClass.REGRESSION

    merge = merge_decision_from_classification(classification)

    return RegressionResult(
        classification=classification,
        rate_class=rate_cls,
        merge_decision=merge,
        wilcoxon=wilcoxon_res,
        wilson_a=wilson_a,
        wilson_b=wilson_b,
        bonferroni=bonferroni,
        alpha=alpha,
        evaluation_mode=evaluation_mode,
        metric_id=metric_id,
        agent_id=agent_id,
        version_key_a=version_key_a,
        version_key_b=version_key_b,
        n_a=n_a,
        n_b=n_b,
    )


def compare_multiple_metrics(
    metric_scores: dict[str, tuple[ScoreArray, ScoreArray]],
    *,
    agent_id: str = "unknown",
    version_key_a: str = "unknown:unknown",
    version_key_b: str = "unknown:unknown",
    evaluation_mode: EvaluationMode = EvaluationMode.FULL,
    k: int | None = None,
    alpha_family: float = 0.05,
) -> tuple[dict[str, RegressionResult], BonferroniConfig]:
    """Compare multiple metrics simultaneously with Bonferroni correction.

    Applies Bonferroni correction across all metrics.  If k is not specified,
    defaults to len(metric_scores).  For the full 13-metric suite, pass
    k=BONFERRONI_K_FULL_SUITE to ensure the correct correction is applied
    even when not all metrics are present in a given call.

    Args:
        metric_scores:   Mapping of metric_id → (scores_a, scores_b).
        agent_id:        Target agent identifier.
        version_key_a:   Baseline version key.
        version_key_b:   Candidate version key.
        evaluation_mode: Evaluation tier.
        k:               Number of simultaneous comparisons for Bonferroni.
                         Defaults to len(metric_scores) when not specified.
        alpha_family:    Family-wise error rate (default 0.05).

    Returns:
        Tuple of (per_metric_results, bonferroni_config).
        per_metric_results maps metric_id → RegressionResult (each using
        the Bonferroni-corrected alpha).

    Raises:
        InsufficientSamplesError: If any score array has N < MIN_STATISTICAL_SAMPLE_SIZE.
        InvalidScoreArrayError:   If any score array fails validation.
        ValueError:               If metric_scores is empty.
    """
    if not metric_scores:
        raise ValueError("metric_scores must not be empty.")

    effective_k = k if k is not None else len(metric_scores)
    bc = bonferroni_correction(k=effective_k, alpha_family=alpha_family)

    results: dict[str, RegressionResult] = {}
    for metric_id, (sa, sb) in metric_scores.items():
        results[metric_id] = compare_versions(
            sa,
            sb,
            metric_id=metric_id,
            agent_id=agent_id,
            version_key_a=version_key_a,
            version_key_b=version_key_b,
            evaluation_mode=evaluation_mode,
            alpha=bc.alpha_per_test,
            bonferroni=bc,
        )

    return results, bc
