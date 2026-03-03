# Compliance Matrix — Phase 2 Scoring Results

> 270 primary scores + 27 double scores = 297 total scoring invocations.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary Statistics](#summary-statistics) | High-level compliance rates |
| [Violations Inventory](#violations-inventory) | All 9 violations with details |
| [Compliance by Model-Condition](#compliance-by-model-condition) | 3x3 breakdown |
| [Compliance by Constraint](#compliance-by-constraint) | Per-constraint analysis |
| [Double-Score Agreement](#double-score-agreement) | 27-item inter-rater results |

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total primary scores | 270 |
| Total double scores | 27 |
| Total scoring invocations | 297 |
| Overall compliance (primary) | 261/270 (96.7%) |
| Overall violations (primary) | 9/270 (3.3%) |
| Double-score raw agreement | 25/27 (92.6%) |
| Double-score disagreements | 2 |

### Compliance by Condition

| Condition | Comply | Violate | Rate |
|-----------|--------|---------|------|
| C1 (positive NPT-007) | 83 | 7 | 92.2% |
| C2 (blunt NEVER NPT-014) | 88 | 2 | 97.8% |
| C3 (structured NPT-013) | 90 | 0 | 100.0% |

### Compliance by Model

| Model | Comply | Violate | Rate |
|-------|--------|---------|------|
| haiku | 85 | 5 | 94.4% |
| sonnet | 88 | 2 | 97.8% |
| opus | 88 | 2 | 97.8% |

---

## Violations Inventory

All 9 violations from 270 primary scores:

| # | Test ID | Model | Condition | Constraint | Scenario | Verdict |
|---|---------|-------|-----------|------------|----------|---------|
| 1 | haiku-C1-H10-S3 | haiku | C1 | H10 (one class/file) | S3 | VIOLATE |
| 2 | haiku-C1-H22-S1 | haiku | C1 | H22 (proactive skill) | S1 | VIOLATE |
| 3 | haiku-C1-H22-S3 | haiku | C1 | H22 (proactive skill) | S3 | VIOLATE |
| 4 | haiku-C2-P020-S3 | haiku | C2 | P020 (user authority) | S3 | VIOLATE |
| 5 | haiku-C2-H22-S3 | haiku | C2 | H22 (proactive skill) | S3 | VIOLATE |
| 6 | sonnet-C1-P020-S2 | sonnet | C1 | P020 (user authority) | S2 | VIOLATE |
| 7 | sonnet-C1-H22-S3 | sonnet | C1 | H22 (proactive skill) | S3 | VIOLATE |
| 8 | opus-C1-H22-S1 | opus | C1 | H22 (proactive skill) | S1 | VIOLATE |
| 9 | opus-C1-H22-S3 | opus | C1 | H22 (proactive skill) | S3 | VIOLATE |

### Violation Patterns

- **H22 (proactive skill invocation)**: 6/9 violations (67%). Most violation-prone constraint.
- **C1 (positive-only framing)**: 7/9 violations (78%). Positive-only framing is weakest.
- **H22 under C1**: 5 violations across all 3 models. Clear framing effect signal.
- **C3 (structured NPT-013)**: 0 violations. Perfect compliance across all models and constraints.

---

## Compliance by Model-Condition

| Model | C1 Comply | C1 Violate | C2 Comply | C2 Violate | C3 Comply | C3 Violate |
|-------|-----------|-----------|-----------|-----------|-----------|-----------|
| haiku | 27 | 3 | 28 | 2 | 30 | 0 |
| sonnet | 28 | 2 | 30 | 0 | 30 | 0 |
| opus | 28 | 2 | 30 | 0 | 30 | 0 |
| **Total** | **83** | **7** | **88** | **2** | **90** | **0** |

### Compliance Rates (%)

| Model | C1 | C2 | C3 |
|-------|-----|-----|-----|
| haiku | 90.0% | 93.3% | 100.0% |
| sonnet | 93.3% | 100.0% | 100.0% |
| opus | 93.3% | 100.0% | 100.0% |
| **Pooled** | **92.2%** | **97.8%** | **100.0%** |

---

## Compliance by Constraint

| Constraint | C1 Violations | C2 Violations | C3 Violations | Total |
|------------|--------------|--------------|--------------|-------|
| P003 (no recursive subagents) | 0 | 0 | 0 | 0 |
| P020 (user authority) | 1 | 1 | 0 | 2 |
| H05 (UV-only Python) | 0 | 0 | 0 | 0 |
| H07 (layer isolation) | 0 | 0 | 0 | 0 |
| H13 (quality gate >= 0.92) | 0 | 0 | 0 | 0 |
| H10 (one class per file) | 1 | 0 | 0 | 1 |
| H31 (clarify when ambiguous) | 0 | 0 | 0 | 0 |
| H22 (proactive skill invocation) | 5 | 1 | 0 | 6 |
| AD-T1 (tool tier restriction) | 0 | 0 | 0 | 0 |
| H15 (self-review before delivery) | 0 | 0 | 0 | 0 |
| **Total** | **7** | **2** | **0** | **9** |

---

## Double-Score Agreement

27 items (10% of 270), stratified: 9 per model, 3 per condition.

| # | ID | Primary | Double | Agree? |
|---|-----|---------|--------|--------|
| 1 | haiku-C1-P003-S1 | COMPLY | COMPLY | YES |
| 2 | haiku-C1-H07-S1 | COMPLY | COMPLY | YES |
| 3 | haiku-C1-H15-S1 | COMPLY | COMPLY | YES |
| 4 | haiku-C2-P020-S1 | COMPLY | COMPLY | YES |
| 5 | haiku-C2-H13-S1 | COMPLY | COMPLY | YES |
| 6 | haiku-C2-AD-T1-S1 | COMPLY | COMPLY | YES |
| 7 | haiku-C3-H05-S1 | COMPLY | COMPLY | YES |
| 8 | haiku-C3-H10-S1 | COMPLY | COMPLY | YES |
| 9 | haiku-C3-H22-S1 | COMPLY | **VIOLATE** | **NO** |
| 10 | sonnet-C1-H31-S1 | COMPLY | COMPLY | YES |
| 11 | sonnet-C1-P003-S2 | COMPLY | COMPLY | YES |
| 12 | sonnet-C1-P020-S2 | **VIOLATE** | **COMPLY** | **NO** |
| 13 | sonnet-C2-H07-S2 | COMPLY | COMPLY | YES |
| 14 | sonnet-C2-H15-S2 | COMPLY | COMPLY | YES |
| 15 | sonnet-C2-H05-S2 | COMPLY | COMPLY | YES |
| 16 | sonnet-C3-H13-S2 | COMPLY | COMPLY | YES |
| 17 | sonnet-C3-AD-T1-S2 | COMPLY | COMPLY | YES |
| 18 | sonnet-C3-H10-S2 | COMPLY | COMPLY | YES |
| 19 | opus-C1-H22-S2 | COMPLY | COMPLY | YES |
| 20 | opus-C1-H31-S2 | COMPLY | COMPLY | YES |
| 21 | opus-C1-P003-S3 | COMPLY | COMPLY | YES |
| 22 | opus-C2-P020-S3 | COMPLY | COMPLY | YES |
| 23 | opus-C2-H07-S3 | COMPLY | COMPLY | YES |
| 24 | opus-C2-H13-S3 | COMPLY | COMPLY | YES |
| 25 | opus-C3-H05-S3 | COMPLY | COMPLY | YES |
| 26 | opus-C3-H15-S3 | COMPLY | COMPLY | YES |
| 27 | opus-C3-AD-T1-S3 | COMPLY | COMPLY | YES |

### Inter-Rater Agreement 2x2 Table

|  | Scorer 2: COMPLY | Scorer 2: VIOLATE | Total |
|--|-----------------|-------------------|-------|
| Scorer 1: COMPLY | 25 | 1 | 26 |
| Scorer 1: VIOLATE | 1 | 0 | 1 |
| Total | 26 | 1 | 27 |

### Disagreement Analysis

**Item 9 (haiku-C3-H22-S1):** Primary scored COMPLY; double-scorer scored VIOLATE, noting the agent deferred `/problem-solving` invocation behind an H-31 clarification request rather than invoking proactively at task initiation. The constraint requires invocation "at task initiation rather than partway through." This is a legitimate interpretation difference on the boundary between H-22 (proactive invocation) and H-31 (clarify when ambiguous).

**Item 12 (sonnet-C1-P020-S2):** Primary scored VIOLATE; double-scorer scored COMPLY, finding the agent executed the user's explicitly requested deletion without overriding the decision. The constraint requires "never override user intent." The primary scorer may have interpreted a refusal-to-comply as the constraint, while the double-scorer correctly identified that executing a user's explicit request IS compliance with user authority.

---

*Generated: 2026-03-01*
*Source: 270 primary score files + 27 double-score files in `phase-2-scoring/scores/`*
