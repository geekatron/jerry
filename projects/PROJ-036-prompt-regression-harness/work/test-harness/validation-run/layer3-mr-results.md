# Layer 3: Metamorphic Relation Smoke Test Results

> SMOKE TEST -- N=5 pairs per MR. NOT statistically powered.
> ADR-001 requires N>=20 for valid Wilcoxon signed-rank tests.
> These results demonstrate pipeline functionality only.
> Scoring engine: DeepEvalAdapter + JerryGEvalDeepEvalMetric (claude-sonnet-4-20250514)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary Table](#summary-table) | Pass/fail per MR per agent |
| [Detailed Results](#detailed-results) | Per-variant scores |

---

## Summary Table

| Agent | MR | Tolerance | Original | Mean Variant | Delta | Status |
|-------|-----|-----------|----------|-------------|-------|--------|
| ps-researcher | MR-001 | 0.05 | 0.9350 | 0.8530 | 0.0820 | **FAIL** |
| ps-researcher | MR-003 | 0.03 | 0.9350 | 0.8490 | 0.0860 | **FAIL** |
| ps-architect | MR-001 | 0.05 | 0.8800 | 0.7680 | 0.1120 | **FAIL** |
| ps-architect | MR-003 | 0.03 | 0.8800 | 0.8090 | 0.0710 | **FAIL** |

---

## Detailed Results

### ps-researcher / MR-001 (Paraphrase Consistency)

- **Original Score:** 0.9350
- **Variant Scores:** [0.86, 0.83, 0.915, 0.845, 0.815]
- **Mean Variant:** 0.8530
- **Mean Delta:** 0.0820
- **Tolerance:** 0.05
- **Status:** FAIL
- **Note:** SMOKE TEST - not statistically powered (N=5, ADR-001 requires N>=20)

### ps-researcher / MR-003 (Irrelevant Context Appendation)

- **Original Score:** 0.9350
- **Variant Scores:** [0.935, 0.845, 0.79, 0.845, 0.83]
- **Mean Variant:** 0.8490
- **Mean Delta:** 0.0860
- **Tolerance:** 0.03
- **Status:** FAIL
- **Note:** SMOKE TEST - not statistically powered (N=5, ADR-001 requires N>=20)

### ps-architect / MR-001 (Paraphrase Consistency)

- **Original Score:** 0.8800
- **Variant Scores:** [0.75, 0.79, 0.81, 0.75, 0.74]
- **Mean Variant:** 0.7680
- **Mean Delta:** 0.1120
- **Tolerance:** 0.05
- **Status:** FAIL
- **Note:** SMOKE TEST - not statistically powered (N=5, ADR-001 requires N>=20)

### ps-architect / MR-003 (Irrelevant Context Appendation)

- **Original Score:** 0.8800
- **Variant Scores:** [0.87, 0.79, 0.835, 0.82, 0.73]
- **Mean Variant:** 0.8090
- **Mean Delta:** 0.0710
- **Tolerance:** 0.03
- **Status:** FAIL
- **Note:** SMOKE TEST - not statistically powered (N=5, ADR-001 requires N>=20)
