## ❌ Regression Analysis — ps-architect

**Mode:** Full  **Verdict:** `REGRESSION`  **Merge:** `BLOCK`

### Versions
- **Baseline:** `baseline:ps-architect`  N=20
- **Candidate:** `candidate:ps-architect`  N=20

### Per-Metric Results

| Metric | p-value | Cohen's r | Effect | mean_A | mean_B | CI_A [lo, hi] | CI_B [lo, hi] | Classification |
|--------|---------|-----------|--------|--------|--------|--------------|--------------|----------------|
| composite_score | 0.0000 | 0.877 | Medium-to-Large | 0.934 | 0.861 | [0.481, 0.855] | [0.000, 0.161] | `REGRESSION` |

### Wilson Score Confidence Intervals (95%)
- **composite_score** Version A: [0.481, 0.855]; Version B: [0.000, 0.161]

### Narrative
Candidate prompt shows statistically significant regression in composite_score (p=0.0000, r=0.877, effect=Medium-to-Large). Mean composite score changed by -0.0729 (A=0.9342 → B=0.8613).
