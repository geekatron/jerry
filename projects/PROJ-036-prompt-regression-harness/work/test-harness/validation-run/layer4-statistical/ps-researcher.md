## ✅ Regression Analysis — ps-researcher

**Mode:** Full  **Verdict:** `IMPROVEMENT`  **Merge:** `ALLOW_WITH_WARNING`

### Versions
- **Baseline:** `baseline:ps-researcher`  N=20
- **Candidate:** `candidate:ps-researcher`  N=20

### Per-Metric Results

| Metric | p-value | Cohen's r | Effect | mean_A | mean_B | CI_A [lo, hi] | CI_B [lo, hi] | Classification |
|--------|---------|-----------|--------|--------|--------|--------------|--------------|----------------|
| composite_score | 0.0000 | 0.843 | Medium-to-Large | 0.871 | 0.930 | [0.000, 0.161] | [0.433, 0.819] | `IMPROVEMENT` |

### Wilson Score Confidence Intervals (95%)
- **composite_score** Version A: [0.000, 0.161]; Version B: [0.433, 0.819]

### Narrative
Candidate prompt shows statistically significant improvement in composite_score (p=0.0000, r=0.843, effect=Medium-to-Large). Mean composite score changed by +0.0595 (A=0.8708 → B=0.9303).
