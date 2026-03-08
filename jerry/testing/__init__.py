# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""Jerry testing utilities package.

Provides the Four-Layer Composite Test Harness for automated regression
detection across Jerry agent definitions.

FR-019 public API: The following names are the stable public exports of the
``jerry.testing`` package.  All are importable directly from this module as
a convenience re-export.

Statistical core (jerry.testing.stats):
    compare_versions             -- Single-metric Wilcoxon comparison.
    compare_multiple_metrics     -- Multi-metric comparison with Bonferroni.
    wilson_score_intervals       -- Wilson score CI for a pass-rate proportion.
    merge_decision_from_classification -- Map RegressionClass to MergeDecision.
    InsufficientSamplesError     -- N < MIN_STATISTICAL_SAMPLE_SIZE.
    MIN_STATISTICAL_SAMPLE_SIZE  -- N=20 minimum for Wilcoxon (FR-014).
    QUALITY_PASS_THRESHOLD       -- 0.92 quality gate constant (FR-016).
    BONFERRONI_K_FULL_SUITE      -- k=13 for full evaluation suite (FR-017).
    BONFERRONI_ALPHA_FULL        -- 0.004 per-test alpha for full suite (FR-017).

Domain types (jerry.testing.types):
    RegressionResult             -- Full Wilcoxon comparison outcome.
    RegressionClass              -- Classification enum (REGRESSION, MARGINAL, …).
    ScoreArray                   -- List[float] type alias for score sequences.

Subpackages:
    jerry.testing.evaluation     -- Layer 2 DeepEval evaluation backend.
    jerry.testing.baselines      -- BaselineStore adapter (FR-020).
    jerry.testing.reports        -- ReportGenerator adapter (FR-018).
    jerry.testing.layer4_stats   -- Layer4Pipeline orchestrator (FR-019).
"""

from jerry.testing.stats import (
    BONFERRONI_ALPHA_FULL,
    BONFERRONI_K_FULL_SUITE,
    MIN_STATISTICAL_SAMPLE_SIZE,
    QUALITY_PASS_THRESHOLD,
    InsufficientSamplesError,
    compare_multiple_metrics,
    compare_versions,
    merge_decision_from_classification,
    wilson_score_intervals,
)
from jerry.testing.types import (
    RegressionClass,
    RegressionResult,
    ScoreArray,
)

__all__ = [
    # Statistical core — FR-019 minimum exports
    "compare_versions",
    "compare_multiple_metrics",
    "wilson_score_intervals",
    "merge_decision_from_classification",
    "InsufficientSamplesError",
    "MIN_STATISTICAL_SAMPLE_SIZE",
    "QUALITY_PASS_THRESHOLD",
    "BONFERRONI_K_FULL_SUITE",
    "BONFERRONI_ALPHA_FULL",
    # Domain types
    "RegressionResult",
    "RegressionClass",
    "ScoreArray",
]
