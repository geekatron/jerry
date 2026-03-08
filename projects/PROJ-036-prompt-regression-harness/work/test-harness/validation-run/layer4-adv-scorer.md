## ❌ Regression Analysis — adv-scorer

**Mode:** Full  **Verdict:** `REGRESSION`  **Merge:** `BLOCK`

### Versions
- **Baseline:** `baseline:adv-scorer`  N=20
- **Candidate:** `candidate:adv-scorer`  N=20

### Per-Metric Results

| Metric | p-value | Cohen's r | Effect | mean_A | mean_B | CI_A [lo, hi] | CI_B [lo, hi] | Classification |
|--------|---------|-----------|--------|--------|--------|--------------|--------------|----------------|
| composite_score | 0.0000 | 0.877 | Medium-to-Large | 0.959 | 0.787 | [0.764, 0.991] | [0.000, 0.161] | `REGRESSION` |

### Wilson Score Confidence Intervals (95%)
- **composite_score** Version A: [0.764, 0.991]; Version B: [0.000, 0.161]

### Narrative
Candidate prompt shows statistically significant regression in composite_score (p=0.0000, r=0.877, effect=Medium-to-Large). Mean composite score changed by -0.1718 (A=0.9588 → B=0.7871).
