## ❌ Regression Analysis — ps-analyst

**Mode:** Full  **Verdict:** `REGRESSION`  **Merge:** `BLOCK`

### Versions
- **Baseline:** `baseline:ps-analyst`  N=20
- **Candidate:** `candidate:ps-analyst`  N=20

### Per-Metric Results

| Metric | p-value | Cohen's r | Effect | mean_A | mean_B | CI_A [lo, hi] | CI_B [lo, hi] | Classification |
|--------|---------|-----------|--------|--------|--------|--------------|--------------|----------------|
| composite_score | 0.0000 | 0.877 | Medium-to-Large | 0.908 | 0.512 | [0.112, 0.469] | [0.000, 0.161] | `REGRESSION` |

### Wilson Score Confidence Intervals (95%)
- **composite_score** Version A: [0.112, 0.469]; Version B: [0.000, 0.161]

### Narrative
Candidate prompt shows statistically significant regression in composite_score (p=0.0000, r=0.877, effect=Medium-to-Large). Mean composite score changed by -0.3954 (A=0.9076 → B=0.5122).
