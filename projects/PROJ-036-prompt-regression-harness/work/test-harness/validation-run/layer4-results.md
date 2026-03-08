# Layer 4: Statistical Comparison Validation Results

> VALIDATION TEST -- synthetic baselines, not real historical data.
> N=20 per array (minimum for Wilcoxon signed-rank).
> Purpose: verify Layer4Pipeline wiring works end-to-end.

## Summary Table

| Agent | Floor | Phase 2 | Baseline Mean | Candidate Mean | Verdict |
|-------|-------|---------|---------------|----------------|---------|
| ps-researcher | 0.82 | 0.9350 | 0.8708 | 0.9303 | **WARNING** |
| ps-analyst | 0.85 | 0.5100 | 0.9076 | 0.5122 | **BLOCK** |
| ps-architect | 0.88 | 0.8600 | 0.9342 | 0.8613 | **BLOCK** |
| ps-critic | 0.83 | 0.5750 | 0.8875 | 0.5776 | **BLOCK** |
| adv-scorer | 0.9 | 0.7850 | 0.9588 | 0.7871 | **BLOCK** |

## Notes

- Baselines are synthetic (Gaussian centered at floor + 0.05, σ=0.03)
- Candidates are derived from Phase 2 composite (Gaussian, σ=0.02)
- No Bonferroni correction applied (single metric per agent)
- Seed: 42 for reproducibility
