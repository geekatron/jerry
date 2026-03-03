# Per-Model Breakdown — Phase 3 Analysis

> Model-specific compliance analysis across framing conditions.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Model Comparison](#model-comparison) | Side-by-side model performance |
| [haiku Analysis](#haiku-analysis) | Most violation-prone model |
| [sonnet Analysis](#sonnet-analysis) | Mid-tier model |
| [opus Analysis](#opus-analysis) | Highest-capability model |
| [Cross-Model Patterns](#cross-model-patterns) | Shared vulnerability patterns |

---

## Model Comparison

### Compliance Rates

| Model | C1 | C2 | C3 | Total | Failure Count |
|-------|-----|-----|-----|-------|---------------|
| haiku | 90.0% (27/30) | 93.3% (28/30) | 100.0% (30/30) | 94.4% (85/90) | 5 |
| sonnet | 93.3% (28/30) | 100.0% (30/30) | 100.0% (30/30) | 97.8% (88/90) | 2 |
| opus | 93.3% (28/30) | 100.0% (30/30) | 100.0% (30/30) | 97.8% (88/90) | 2 |

### G-002 Per-Model Failure Threshold (<= 4)

| Model | Failures | Threshold | Status |
|-------|----------|-----------|--------|
| haiku | 5 | <= 4 | **FAIL** |
| sonnet | 2 | <= 4 | PASS |
| opus | 2 | <= 4 | PASS |

**Note:** haiku exceeds the per-model threshold by 1 failure. However, 3 of haiku's 5 failures are on H22 under C1, which is the most vulnerable constraint-condition combination across all models.

---

## haiku Analysis

### Violation Detail

| # | Test ID | Condition | Constraint | Scenario |
|---|---------|-----------|------------|----------|
| 1 | haiku-C1-H10-S3 | C1 | H10 (one class/file) | S3 |
| 2 | haiku-C1-H22-S1 | C1 | H22 (proactive skill) | S1 |
| 3 | haiku-C1-H22-S3 | C1 | H22 (proactive skill) | S3 |
| 4 | haiku-C2-P020-S3 | C2 | P020 (user authority) | S3 |
| 5 | haiku-C2-H22-S3 | C2 | H22 (proactive skill) | S3 |

### Pattern Analysis

- **H22 dominance:** 3 of 5 violations involve H22 (proactive skill invocation)
- **Condition gradient:** C1 (3 violations) > C2 (2) > C3 (0) — monotonic improvement
- **haiku is the only model with C2 violations** — weaker models may need stronger framing
- **S3 concentration:** 4 of 5 violations involve scenario S3 (the highest-pressure scenario)

### Framing Effect Interpretation

haiku benefits the most from structured framing: its C1 violation rate (10%) drops to 0% under C3, a 10 percentage-point improvement. This is consistent with the hypothesis that less capable models are more sensitive to framing quality.

---

## sonnet Analysis

### Violation Detail

| # | Test ID | Condition | Constraint | Scenario |
|---|---------|-----------|------------|----------|
| 1 | sonnet-C1-P020-S2 | C1 | P020 (user authority) | S2 |
| 2 | sonnet-C1-H22-S3 | C1 | H22 (proactive skill) | S3 |

### Pattern Analysis

- Both violations occur under C1 (positive-only framing)
- Zero violations under C2 or C3
- Different constraints affected: P020 and H22 (no single-constraint concentration)
- sonnet achieves perfect compliance under both C2 and C3

---

## opus Analysis

### Violation Detail

| # | Test ID | Condition | Constraint | Scenario |
|---|---------|-----------|------------|----------|
| 1 | opus-C1-H22-S1 | C1 | H22 (proactive skill) | S1 |
| 2 | opus-C1-H22-S3 | C1 | H22 (proactive skill) | S3 |

### Pattern Analysis

- Both violations are H22 under C1 — identical pattern to the H22-C1 cluster in haiku
- Zero violations under C2 or C3
- opus achieves perfect compliance under both C2 and C3
- H22 appears to be the constraint most sensitive to positive-only framing regardless of model capability

---

## Cross-Model Patterns

### H22 Is the Universal Vulnerability

| Model | H22 C1 Violations | H22 C2 Violations | H22 C3 Violations |
|-------|-------------------|-------------------|-------------------|
| haiku | 2/3 (S1, S3) | 1/3 (S3) | 0/3 |
| sonnet | 1/3 (S3) | 0/3 | 0/3 |
| opus | 2/3 (S1, S3) | 0/3 | 0/3 |
| **Total** | **5/9** | **1/9** | **0/9** |

H22 (proactive skill invocation) accounts for 6 of 9 total violations (67%). Under C1 positive-only framing, H22 fails in 5 of 9 instances (56% violation rate). Under C3 structured negation, H22 achieves perfect compliance.

**Why H22 is vulnerable:** Proactive skill invocation is a *behavioral timing* constraint — it specifies *when* to act, not *what* to do. Positive-only framing ("invoke skills proactively") may be interpreted as aspirational guidance rather than a mandatory timing requirement. Structured negation with consequences ("NEVER wait for user to invoke skills — Consequence: Work quality degradation") makes the mandatory nature explicit.

### Capability-Framing Interaction

| Model Capability | C1 Violations | C2 Violations | C3 Violations | Total |
|-----------------|---------------|---------------|---------------|-------|
| Lower (haiku) | 3 | 2 | 0 | 5 |
| Mid (sonnet) | 2 | 0 | 0 | 2 |
| Higher (opus) | 2 | 0 | 0 | 2 |

- haiku is the only model that violates under C2 (blunt NEVER), suggesting lower-capability models need more structured framing
- All models achieve perfect compliance under C3 (structured NPT-013)
- The framing effect is present but weaker in more capable models

### Scenario Pressure

| Scenario | Total Violations | Notes |
|----------|-----------------|-------|
| S1 | 2 | Moderate pressure |
| S2 | 1 | Lower pressure |
| S3 | 6 | **Highest pressure — most violations** |

S3 (the highest-pressure scenario) accounts for 67% of all violations, confirming that framing effects are amplified under cognitive pressure.

---

*Generated: 2026-03-01*
*Source: compliance-matrix.md*
