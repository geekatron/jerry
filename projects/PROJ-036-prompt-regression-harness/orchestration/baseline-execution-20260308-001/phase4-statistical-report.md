# Phase 4 — Statistical Comparison Report

> **Generated:** 2026-03-08T19:30:07.643041+00:00
> **Mode:** Pipeline Validation (Phase 2 self-analysis)

## Validation Mode Notice

This report uses Phase 2 scoring data for pipeline validation.
Phase 3 MR testing has not yet completed, so real baseline data
is not available for Wilcoxon signed-rank comparison. The statistics
below are descriptive only — not regression verdicts.

**To run full Phase 4:** Complete Phase 3 (`baseline_mr_runner.py`),
then re-run this script without `--validation-mode`.

## ps-researcher

**Overall:** INSUFFICIENT_DATA | **Merge:** DEFERRED | **N:** 5 prompts

| Dimension | N | Mean | Min | Max | Std | Pass Rate | Wilson CI | Classification |
|-----------|---|------|-----|-----|-----|-----------|----------|----------------|
| completeness | 5 | 0.4 | 0.0 | 1.0 | 0.3742 | 0.2 | [0.0362, 0.6245] | INSUFFICIENT_DATA |
| internal_consistency | 5 | 0.52 | 0.3 | 0.9 | 0.2387 | 0.0 | [0.0, 0.4345] | INSUFFICIENT_DATA |
| methodological_rigor | 5 | 0.4 | 0.2 | 0.7 | 0.2345 | 0.0 | [0.0, 0.4345] | INSUFFICIENT_DATA |
| evidence_quality | 5 | 0.22 | 0.0 | 0.7 | 0.2864 | 0.0 | [0.0, 0.4345] | INSUFFICIENT_DATA |
| actionability | 5 | 0.64 | 0.2 | 1.0 | 0.4037 | 0.2 | [0.0362, 0.6245] | INSUFFICIENT_DATA |
| traceability | 5 | 0.28 | 0.1 | 0.8 | 0.295 | 0.0 | [0.0, 0.4345] | INSUFFICIENT_DATA |
| composite | 5 | 0.421 | 0.27 | 0.755 | 0.1956 | 0.0 | [0.0, 0.4345] | INSUFFICIENT_DATA |

### Wilcoxon Status

- **completeness:** INSUFFICIENT_N — N=5 < 20. Wilcoxon requires Phase 3 data (N>=20).
- **internal_consistency:** INSUFFICIENT_N — N=5 < 20. Wilcoxon requires Phase 3 data (N>=20).
- **methodological_rigor:** INSUFFICIENT_N — N=5 < 20. Wilcoxon requires Phase 3 data (N>=20).
- **evidence_quality:** INSUFFICIENT_N — N=5 < 20. Wilcoxon requires Phase 3 data (N>=20).
- **actionability:** INSUFFICIENT_N — N=5 < 20. Wilcoxon requires Phase 3 data (N>=20).
- **traceability:** INSUFFICIENT_N — N=5 < 20. Wilcoxon requires Phase 3 data (N>=20).
- **composite:** INSUFFICIENT_N — N=5 < 20. Wilcoxon requires Phase 3 data (N>=20).

## ps-architect

**Overall:** INSUFFICIENT_DATA | **Merge:** DEFERRED | **N:** 4 prompts

| Dimension | N | Mean | Min | Max | Std | Pass Rate | Wilson CI | Classification |
|-----------|---|------|-----|-----|-----|-----------|----------|----------------|
| completeness | 4 | 0.575 | 0.4 | 0.8 | 0.2062 | 0.0 | [0.0, 0.4899] | INSUFFICIENT_DATA |
| internal_consistency | 4 | 0.45 | 0.2 | 0.6 | 0.1915 | 0.0 | [0.0, 0.4899] | INSUFFICIENT_DATA |
| methodological_rigor | 4 | 0.625 | 0.3 | 0.8 | 0.2217 | 0.0 | [0.0, 0.4899] | INSUFFICIENT_DATA |
| evidence_quality | 4 | 0.7 | 0.4 | 0.8 | 0.2 | 0.0 | [0.0, 0.4899] | INSUFFICIENT_DATA |
| actionability | 4 | 0.8 | 0.6 | 1.0 | 0.1826 | 0.25 | [0.0456, 0.6994] | INSUFFICIENT_DATA |
| traceability | 4 | 0.525 | 0.3 | 0.8 | 0.2217 | 0.0 | [0.0, 0.4899] | INSUFFICIENT_DATA |
| composite | 4 | 0.6075 | 0.49 | 0.675 | 0.0809 | 0.0 | [0.0, 0.4899] | INSUFFICIENT_DATA |

### Wilcoxon Status

- **completeness:** INSUFFICIENT_N — N=4 < 20. Wilcoxon requires Phase 3 data (N>=20).
- **internal_consistency:** INSUFFICIENT_N — N=4 < 20. Wilcoxon requires Phase 3 data (N>=20).
- **methodological_rigor:** INSUFFICIENT_N — N=4 < 20. Wilcoxon requires Phase 3 data (N>=20).
- **evidence_quality:** INSUFFICIENT_N — N=4 < 20. Wilcoxon requires Phase 3 data (N>=20).
- **actionability:** INSUFFICIENT_N — N=4 < 20. Wilcoxon requires Phase 3 data (N>=20).
- **traceability:** INSUFFICIENT_N — N=4 < 20. Wilcoxon requires Phase 3 data (N>=20).
- **composite:** INSUFFICIENT_N — N=4 < 20. Wilcoxon requires Phase 3 data (N>=20).

## Bonferroni Correction

When Phase 3 data is available, Bonferroni correction will be applied with:
- k = 6 dimensions (or k = 13 for full suite including MRs)
- alpha_family = 0.05
- alpha_per_test = 0.05 / 6 = 0.0083 (6-dimension) or 0.05 / 13 = 0.0038 (full suite)

## Interpretation Guidance

| Verdict | Meaning | Action |
|---------|---------|--------|
| NO_REGRESSION | No statistically significant quality decrease | Safe to merge |
| MARGINAL | Borderline result | Review dimension drivers before merging |
| REGRESSION | Significant quality decrease detected | Block merge; investigate |
| QUALITY_FLOOR_BREACH | Mean score below 0.92 threshold | Block merge; quality too low |
| INSUFFICIENT_DATA | N < 20 for Wilcoxon | Run Phase 3 to collect more data |
