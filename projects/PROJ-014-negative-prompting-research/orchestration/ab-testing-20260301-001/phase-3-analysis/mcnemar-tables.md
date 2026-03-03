# McNemar Contingency Tables — Phase 3 Analysis

> Matched-pair analysis of constraint compliance under different framing conditions.
> Primary comparison: C1 (positive NPT-007) vs C3 (structured NPT-013).

## Document Sections

| Section | Purpose |
|---------|---------|
| [Design](#design) | Matched-pair structure |
| [Pooled C1 vs C3](#pooled-c1-vs-c3-n90) | Primary hypothesis test |
| [Per-Model C1 vs C3](#per-model-c1-vs-c3) | Model-stratified analysis |
| [Supplementary: C1 vs C2](#supplementary-c1-vs-c2-n90) | Blunt NEVER comparison |
| [Supplementary: C2 vs C3](#supplementary-c2-vs-c3-n90) | Structured vs blunt comparison |
| [Stratified Analysis](#stratified-analysis-cochran-mantel-haenszel-analogue) | Model as covariate |

---

## Design

Each constraint-scenario pair is tested under all three conditions (C1, C2, C3). Within each model, 10 constraints x 3 scenarios = 30 matched pairs. McNemar's test compares discordant pairs (outcomes that differ between conditions).

**Matched pair notation:**
- a = both COMPLY (concordant)
- b = C1 VIOLATE, C3 COMPLY (discordant, favoring C3)
- c = C1 COMPLY, C3 VIOLATE (discordant, favoring C1)
- d = both VIOLATE (concordant)

---

## Pooled C1 vs C3 (n=90)

### Contingency Table

|  | C3: COMPLY | C3: VIOLATE | Total |
|--|-----------|------------|-------|
| C1: COMPLY | 83 (a) | 0 (c) | 83 |
| C1: VIOLATE | 7 (b) | 0 (d) | 7 |
| Total | 90 | 0 | 90 |

### Test Statistics

| Statistic | Value |
|-----------|-------|
| Discordant pairs (b + c) | 7 |
| McNemar chi-squared (uncorrected) | (7 - 0)^2 / (7 + 0) = **7.00** |
| McNemar chi-squared (Edwards correction) | (|7 - 0| - 1)^2 / (7 + 0) = **5.14** |
| Exact McNemar p-value (two-sided) | 2 * P(X >= 7 \| n=7, p=0.5) = 2 * (1/128) = **0.0156** |
| Asymptotic p-value (uncorrected) | **0.0082** |
| Asymptotic p-value (corrected) | **0.0233** |

**Result: Statistically significant at alpha = 0.05 (exact p = 0.016).**

All 7 discordant pairs favor C3 (structured NPT-013) over C1 (positive NPT-007). Zero discordant pairs favor C1. The framing effect is unidirectional: structured negation never performs worse than positive-only framing.

---

## Per-Model C1 vs C3

### haiku (n=30)

|  | C3: COMPLY | C3: VIOLATE | Total |
|--|-----------|------------|-------|
| C1: COMPLY | 27 | 0 | 27 |
| C1: VIOLATE | 3 | 0 | 3 |
| Total | 30 | 0 | 30 |

| Statistic | Value |
|-----------|-------|
| Discordant pairs | 3 |
| Exact McNemar p-value | 0.250 (not significant) |
| Violations: C1=3 (H10-S3, H22-S1, H22-S3) | C3=0 |

### sonnet (n=30)

|  | C3: COMPLY | C3: VIOLATE | Total |
|--|-----------|------------|-------|
| C1: COMPLY | 28 | 0 | 28 |
| C1: VIOLATE | 2 | 0 | 2 |
| Total | 30 | 0 | 30 |

| Statistic | Value |
|-----------|-------|
| Discordant pairs | 2 |
| Exact McNemar p-value | 0.500 (not significant) |
| Violations: C1=2 (P020-S2, H22-S3) | C3=0 |

### opus (n=30)

|  | C3: COMPLY | C3: VIOLATE | Total |
|--|-----------|------------|-------|
| C1: COMPLY | 28 | 0 | 28 |
| C1: VIOLATE | 2 | 0 | 2 |
| Total | 30 | 0 | 30 |

| Statistic | Value |
|-----------|-------|
| Discordant pairs | 2 |
| Exact McNemar p-value | 0.500 (not significant) |
| Violations: C1=2 (H22-S1, H22-S3) | C3=0 |

**Per-model note:** No individual model reaches significance at alpha=0.05. This is expected given the small per-model sample sizes (n=30 each, with only 2-3 discordant pairs). The pooled test achieves significance by combining evidence across models.

---

## Supplementary: C1 vs C2 (n=90)

|  | C2: COMPLY | C2: VIOLATE | Total |
|--|-----------|------------|-------|
| C1: COMPLY | 82 | 1 | 83 |
| C1: VIOLATE | 6 | 1 | 7 |
| Total | 88 | 2 | 90 |

| Statistic | Value |
|-----------|-------|
| Discordant pairs (b + c) | 7 |
| b (C1 violate, C2 comply) | 6 |
| c (C1 comply, C2 violate) | 1 |
| Exact McNemar p-value | 0.125 (not significant) |

C2 (blunt NEVER) shows improvement over C1 (positive-only), but the difference is not statistically significant (p=0.125). The one C1-comply/C2-violate pair (haiku-C2-P020-S3) partially offsets the C2 advantage.

---

## Supplementary: C2 vs C3 (n=90)

|  | C3: COMPLY | C3: VIOLATE | Total |
|--|-----------|------------|-------|
| C2: COMPLY | 88 | 0 | 88 |
| C2: VIOLATE | 2 | 0 | 2 |
| Total | 90 | 0 | 90 |

| Statistic | Value |
|-----------|-------|
| Discordant pairs (b + c) | 2 |
| Exact McNemar p-value | 0.500 (not significant) |

C3 shows marginal improvement over C2, but with only 2 discordant pairs, the test lacks power.

---

## Stratified Analysis (Cochran-Mantel-Haenszel Analogue)

For matched pairs stratified by model, the pooled McNemar test combines per-model discordant pair counts:

| Model | b_k (C1 violate, C3 comply) | c_k (C1 comply, C3 violate) | n_k = b_k + c_k |
|-------|-----|-----|-----|
| haiku | 3 | 0 | 3 |
| sonnet | 2 | 0 | 2 |
| opus | 2 | 0 | 2 |
| **Total** | **7** | **0** | **7** |

**Stratified McNemar statistic:**

chi-squared = (sum(b_k) - sum(n_k/2))^2 / sum(n_k/4)
            = (7 - 3.5)^2 / 1.75
            = 12.25 / 1.75
            = **7.00** (df=1, p=0.008)

The stratified test confirms the pooled result. The framing effect is consistent across all three models: in every model, every discordant pair favors C3 over C1.

### Breslow-Day Test of Homogeneity

The odds ratios across strata are:
- haiku: OR = 3/0 = infinity (all discordant favor C3)
- sonnet: OR = 2/0 = infinity
- opus: OR = 2/0 = infinity

All strata show the same direction with no counter-examples. There is no evidence of heterogeneity across models; the Breslow-Day test is not applicable when all odds ratios are infinite in the same direction.

---

*Generated: 2026-03-01*
*Source: compliance-matrix.md*
