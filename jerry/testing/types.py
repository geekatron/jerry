# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""Shared type definitions for the Four-Layer Composite Test Harness.

This module defines the domain types shared across all layers of the harness:
Layer 1 (CI/CD gate), Layer 2 (evaluation backend), Layer 3 (metamorphic
relations), and Layer 4 (statistical comparison engine).

All types are pure data containers with no external dependencies beyond
Python stdlib.  They are the SSOT for data contracts between harness modules.

Design compliance:
    - H-07: Domain module — imports only stdlib.
    - H-10: One primary class/enum grouping per file (grouped by concern).
    - H-11: Type hints and docstrings on all public symbols.
"""

from __future__ import annotations

import dataclasses
from datetime import UTC, datetime
from enum import Enum

# ---------------------------------------------------------------------------
# Regression classification enumerations
# ---------------------------------------------------------------------------


class RegressionClass(str, Enum):
    """Classification of a Wilcoxon signed-rank comparison between two prompt
    versions.

    Classification rules (per behavioral-contracts.md Section D.1 and D.4):

    +--------------------------------+-------------------------------+
    | Condition                      | Classification                |
    +--------------------------------+-------------------------------+
    | p >= 0.10 (any effect size)    | NO_REGRESSION                 |
    | p < 0.05 AND r < 0.10          | NO_REGRESSION (negligible)    |
    | 0.05 <= p < 0.10, r < 0.20     | NO_REGRESSION (insufficient)  |
    | 0.05 <= p < 0.10, r >= 0.20    | MARGINAL                      |
    | p < 0.05, 0.10 <= r < 0.30,    |                               |
    |   mean_delta < 0               | MARGINAL                      |
    | p < 0.05, r >= 0.30,           |                               |
    |   mean_delta < 0               | REGRESSION (blocks merge)     |
    | p < 0.05, r >= 0.10,           |                               |
    |   mean_delta >= 0              | IMPROVEMENT                   |
    +--------------------------------+-------------------------------+

    Only REGRESSION triggers a merge block.  IMPROVEMENT is logged but
    does not block merge.
    """

    NO_REGRESSION = "NO_REGRESSION"
    MARGINAL = "MARGINAL"
    REGRESSION = "REGRESSION"
    IMPROVEMENT = "IMPROVEMENT"
    #: Injected by Layer 2 callers (e.g., DeepEval adapter) when mean(scores)
    #: falls below QUALITY_PASS_THRESHOLD.  Not produced by _classify_regression()
    #: in stats.py, which handles only statistical comparison classifications.
    QUALITY_FLOOR_BREACH = "QUALITY_FLOOR_BREACH"
    STRUCTURAL_FAIL = "STRUCTURAL_FAIL"


class RateClass(str, Enum):
    """Classification of Wilson score interval comparison for pass rates.

    Used alongside RegressionClass to detect regressions in the fraction of
    runs meeting the quality gate threshold (>= QUALITY_PASS_THRESHOLD).
    """

    RATE_STABLE = "RATE_STABLE"
    RATE_REGRESSION = "RATE_REGRESSION"


class EffectSizeLabel(str, Enum):
    """Cohen's r effect size label per Cohen (1988) conventions.

    Thresholds (per behavioral-contracts.md Section D.4):
        - r < 0.10:           Negligible
        - 0.10 <= r < 0.20:   Small
        - 0.20 <= r < 0.30:   Small-to-Medium
        - r >= 0.30:          Medium-to-Large
    """

    NEGLIGIBLE = "Negligible"
    SMALL = "Small"
    SMALL_TO_MEDIUM = "Small-to-Medium"
    MEDIUM_TO_LARGE = "Medium-to-Large"


class EvaluationMode(str, Enum):
    """Tiered evaluation modes (FR-005).

    Each mode defines the number of LLM runs per version, the active metric
    set, and whether statistical comparison is performed.
    """

    SMOKE = "Smoke"  # N=1; structural checks only; no statistical analysis
    STANDARD = "Standard"  # N=10; deterministic + LLM-as-Judge; no Wilcoxon
    FULL = "Full"  # N=30; all layers including Wilcoxon + Bonferroni


class MergeDecision(str, Enum):
    """Recommended merge action derived from regression classification."""

    ALLOW = "ALLOW"
    ALLOW_WITH_WARNING = "ALLOW_WITH_WARNING"
    BLOCK = "BLOCK"


# ---------------------------------------------------------------------------
# Core result data classes
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True)
class WilcoxonResult:
    """Raw output from a single Wilcoxon signed-rank test invocation.

    Attributes:
        statistic: The Wilcoxon test statistic W (sum of positive ranks).
        p_value:   Two-sided p-value from scipy.stats.wilcoxon.
        n_pairs:   Number of paired observations (len of input arrays).
        cohens_r:  Effect size Cohen's r = Z / sqrt(N).  Z is derived from
                   the statistic using the normal approximation.
        effect_label: Human-readable effect size classification.
        mean_delta:   mean(scores_b) - mean(scores_a).  Negative means the
                      candidate (b) is worse than the baseline (a).
        mean_a:    Mean of baseline score array.
        mean_b:    Mean of candidate score array.
    """

    statistic: float
    p_value: float
    n_pairs: int
    cohens_r: float
    effect_label: EffectSizeLabel
    mean_delta: float
    mean_a: float
    mean_b: float


@dataclasses.dataclass(frozen=True)
class WilsonResult:
    """Wilson score confidence interval for a pass-rate proportion.

    Computes the fraction of scores >= QUALITY_PASS_THRESHOLD that pass the
    Jerry quality gate (H-13) and the 95% Wilson score CI for that proportion.

    Attributes:
        n_total:     Total number of score observations.
        n_pass:      Number of scores >= QUALITY_PASS_THRESHOLD.
        pass_rate:   n_pass / n_total (point estimate).
        ci_lower:    Lower bound of 95% Wilson score confidence interval.
        ci_upper:    Upper bound of 95% Wilson score confidence interval.
        ci_width:    ci_upper - ci_lower.  Should be < 0.30 for N >= 20
                     (per behavioral-contracts.md Section D.2).
    """

    n_total: int
    n_pass: int
    pass_rate: float
    ci_lower: float
    ci_upper: float
    ci_width: float


@dataclasses.dataclass(frozen=True)
class BonferroniConfig:
    """Configuration and metadata for a Bonferroni multiple-testing correction.

    Attributes:
        k:                  Number of simultaneous comparisons.
        alpha_family:       Family-wise target error rate (default 0.05).
        alpha_per_test:     Effective per-test threshold = alpha_family / k.
        description:        Human-readable disclosure string for regression
                            reports (required by FR-017 acceptance criterion).
    """

    k: int
    alpha_family: float
    alpha_per_test: float

    @property
    def description(self) -> str:
        """Return the Bonferroni disclosure string for regression reports.

        Satisfies FR-017 acceptance criterion: "The regression report shall
        disclose the Bonferroni correction applied."
        """
        return (
            f"Bonferroni correction applied: alpha={self.alpha_family}, "
            f"K={self.k}, per-metric threshold={self.alpha_per_test:.4f}"
        )


@dataclasses.dataclass(frozen=True)
class RegressionResult:
    """Complete result of a Layer 4 statistical version comparison.

    Produced by ``compare_versions()`` in ``jerry.testing.stats``.  This is
    the primary handoff type from the statistical engine to the report
    generator and Layer 1 CI/CD gate.

    Attributes:
        classification:   Primary regression verdict (RegressionClass).
        rate_class:       Pass-rate regression via Wilson interval comparison.
        merge_decision:   Recommended merge action derived from classification.
        wilcoxon:         Raw Wilcoxon test results.
        wilson_a:         Wilson score CI for the baseline version.
        wilson_b:         Wilson score CI for the candidate version.
        bonferroni:       Bonferroni correction metadata (None for single-
                          metric comparisons where no correction was applied).
        alpha:            Significance threshold used for this comparison
                          (may be Bonferroni-corrected or uncorrected).
        evaluation_mode:  Mode in which comparison was performed.
        metric_id:        Identifier of the metric being compared.
        agent_id:         Target agent identifier.
        version_key_a:    Baseline version key (git hash + file path).
        version_key_b:    Candidate version key.
        n_a:              Sample size of baseline.
        n_b:              Sample size of candidate.
        timestamp:        UTC timestamp of comparison.
        dimension_driver: Metric or dimension ID that drove the classification
                          (populated by the report generator when Bonferroni
                          correction is applied to multiple metrics).
    """

    classification: RegressionClass
    rate_class: RateClass
    merge_decision: MergeDecision
    wilcoxon: WilcoxonResult
    wilson_a: WilsonResult
    wilson_b: WilsonResult
    bonferroni: BonferroniConfig | None
    alpha: float
    evaluation_mode: EvaluationMode
    metric_id: str
    agent_id: str
    version_key_a: str
    version_key_b: str
    n_a: int
    n_b: int
    timestamp: str = dataclasses.field(default_factory=lambda: datetime.now(UTC).isoformat())
    dimension_driver: str | None = None


@dataclasses.dataclass(frozen=True)
class MultiMetricResult:
    """Aggregated result across multiple metrics with Bonferroni correction.

    Produced by the multi-metric comparison path in ``layer4_stats.py``.

    Attributes:
        overall_classification: Worst-case classification across all metrics
                                 after Bonferroni correction.
        merge_decision:          Derived from overall_classification.
        per_metric:              Mapping of metric_id -> RegressionResult.
        bonferroni:              Bonferroni correction config used.
        dimension_driver:        Metric ID with the most significant result
                                 (lowest corrected p-value that drove verdict).
    """

    overall_classification: RegressionClass
    merge_decision: MergeDecision
    per_metric: dict[str, RegressionResult]
    bonferroni: BonferroniConfig
    dimension_driver: str | None


# ---------------------------------------------------------------------------
# Baseline store types
# ---------------------------------------------------------------------------


@dataclasses.dataclass
class BaselineRecord:
    """Persisted baseline data for a single agent-metric-version combination.

    Stored by ``jerry.testing.baselines.store.BaselineStore``.

    Attributes:
        version_key:        Composite key "{git_commit_hash}:{file_path}"
                            (per FR-004 format specification).
        agent_id:           Agent identifier (e.g., "ps-researcher").
        metric_id:          Metric identifier (e.g., "composite_score").
        scores:             Ordered list of N quality scores [0.0, 1.0].
        mean_score:         Mean of scores (pre-computed for fast gate checks).
        n_runs:             len(scores).
        evaluation_mode:    Mode used to collect baseline.
        model_version:      Pinned LLM model version string.
        captured_at:        ISO-8601 UTC timestamp of baseline capture.
        baseline_status:    "active" | "invalidated".
        invalidated_by:     Contract version that invalidated this baseline,
                            or None if still active.
    """

    version_key: str
    agent_id: str
    metric_id: str
    scores: list[float]
    mean_score: float
    n_runs: int
    evaluation_mode: EvaluationMode
    model_version: str
    captured_at: str
    baseline_status: str = "active"
    invalidated_by: str | None = None


@dataclasses.dataclass
class BaselineAuditEntry:
    """Summary row for the baseline audit CLI command.

    Produced by ``BaselineStore.audit()`` for the
    ``jerry test baseline audit`` command (FR-020 acceptance criterion).
    """

    version_key: str
    agent_id: str
    metric_id: str
    mean_score: float
    n_runs: int
    captured_at: str
    baseline_status: str
    age_days: float


# ---------------------------------------------------------------------------
# Report types
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True)
class ComparisonReport:
    """Full structured regression report for one agent evaluation.

    Matches the JSON schema defined in behavioral-contracts.md Section D.6.
    Produced by ``jerry.testing.reports.generator.ReportGenerator``.

    Attributes:
        evaluation_mode:            "Smoke" | "Standard" | "Full".
        agent:                      Agent identifier.
        prompt_version_baseline:    Git version key for baseline.
        prompt_version_candidate:   Git version key for candidate.
        n_baseline:                 Number of baseline runs.
        n_candidate:                Number of candidate runs.
        timestamp:                  ISO-8601 UTC evaluation timestamp.
        classification:             Overall verdict string.
        merge_recommendation:       "ALLOW" | "ALLOW_WITH_WARNING" | "BLOCK".
        dimension_driver:           Metric ID that drove the verdict, if any.
        narrative:                  Human-readable explanation of the verdict.
        per_metric_results:         RegressionResult per metric_id.
        multi_metric_result:        Aggregated Bonferroni-corrected result
                                    (None for single-metric comparisons).
    """

    evaluation_mode: str
    agent: str
    prompt_version_baseline: str
    prompt_version_candidate: str
    n_baseline: int
    n_candidate: int
    timestamp: str
    classification: str
    merge_recommendation: str
    dimension_driver: str | None
    narrative: str
    per_metric_results: dict[str, RegressionResult]
    multi_metric_result: MultiMetricResult | None


# ---------------------------------------------------------------------------
# Score array type alias
# ---------------------------------------------------------------------------

#: A validated list of N quality scores, each in [0.0, 1.0].
#: N >= MIN_STATISTICAL_SAMPLE_SIZE is enforced at call sites in stats.py.
ScoreArray = list[float]


# ---------------------------------------------------------------------------
# Model configuration types (EN-036-001)
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True)
class ModelPricing:
    """Per-model pricing for cost ledger differentiation (EN-036-001).

    Attributes:
        input_cost_per_million: Cost in USD per million input tokens.
        output_cost_per_million: Cost in USD per million output tokens.
    """

    input_cost_per_million: float
    output_cost_per_million: float


#: Model pricing lookup table for cost ledger accuracy.
#: Key is the model name prefix (matched case-insensitively).
#: Longer prefixes MUST appear before shorter ones for correct precedence.
#: Source: https://docs.anthropic.com/en/docs/about-claude/models (2026-03-07)
MODEL_PRICING: dict[str, ModelPricing] = {
    # Opus 4.5+ generation: $5/$25
    "claude-opus-4-6": ModelPricing(input_cost_per_million=5.0, output_cost_per_million=25.0),
    "claude-opus-4-5": ModelPricing(input_cost_per_million=5.0, output_cost_per_million=25.0),
    # Opus 4.0/4.1 legacy: $15/$75
    "claude-opus-4-1": ModelPricing(input_cost_per_million=15.0, output_cost_per_million=75.0),
    "claude-opus-4": ModelPricing(input_cost_per_million=15.0, output_cost_per_million=75.0),
    # Sonnet: $3/$15 (all 4.x versions)
    "claude-sonnet-4": ModelPricing(input_cost_per_million=3.0, output_cost_per_million=15.0),
    # Haiku 4.5: $1/$5
    "claude-haiku-4": ModelPricing(input_cost_per_million=1.0, output_cost_per_million=5.0),
}


def lookup_model_pricing(model_name: str) -> ModelPricing | None:
    """Look up pricing for a model by prefix match.

    Args:
        model_name: Full model identifier (e.g., "claude-sonnet-4-20250514").

    Returns:
        ModelPricing if a prefix match is found, None otherwise.
    """
    lower = model_name.lower()
    for prefix, pricing in MODEL_PRICING.items():
        if lower.startswith(prefix):
            return pricing
    return None


def format_composite_model_version(agent_model: str, judge_model: str) -> str:
    """Format a composite model version string for BaselineRecord.

    Args:
        agent_model: Model used for agent execution (e.g., "claude-opus-4-20250514").
        judge_model: Model used for G-Eval judge scoring (e.g., "claude-sonnet-4-20250514").

    Returns:
        Composite string in format "{agent_model}:{judge_model}".
    """
    return f"{agent_model}:{judge_model}"


def parse_composite_model_version(composite: str) -> tuple[str, str] | None:
    """Parse a composite model version string into (agent_model, judge_model).

    Args:
        composite: Composite string in format "{agent_model}:{judge_model}".

    Returns:
        Tuple of (agent_model, judge_model) if the format is valid, None otherwise.
    """
    parts = composite.split(":", 1)
    if len(parts) == 2 and parts[0] and parts[1]:
        return (parts[0], parts[1])
    return None
