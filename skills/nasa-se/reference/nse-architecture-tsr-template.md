# Trade Study Report Template

> Runtime template for nse-architecture agent. Load via Read tool when generating trade study output.

```markdown
# Trade Study Report: [Decision Title]

> **Document ID:** TSR-[PROJECT]-[NNN]
> **Version:** [X.Y]
> **Date:** [YYYY-MM-DD]
> **Author:** [Name/Role]
> **Status:** [Draft/In Review/Approved]

---

## 1. Purpose and Scope

### 1.1 Decision Statement
[Clear statement of the design decision to be made]

### 1.2 Scope
- **System/Subsystem:** [What is being designed]
- **Phase:** [Concept/Preliminary/Detailed]
- **Driving Requirements:** [Key requirements this decision addresses]

### 1.3 Constraints
| Type | Constraint | Impact |
|------|------------|--------|
| Budget | | |
| Schedule | | |
| Technical | | |
| Programmatic | | |

---

## 2. Evaluation Criteria

### 2.1 Must-Have Criteria (Pass/Fail)
| # | Criterion | Source | Threshold |
|---|-----------|--------|-----------|
| M1 | | REQ-XXX | |
| M2 | | REQ-XXX | |

### 2.2 Want Criteria (Weighted)
| # | Criterion | Source | Weight | Rationale |
|---|-----------|--------|--------|-----------|
| W1 | Performance | REQ-XXX | 25% | |
| W2 | Cost | Constraint | 20% | |
| W3 | Schedule | Constraint | 15% | |
| W4 | Risk | Engineering | 20% | |
| W5 | Reliability | REQ-XXX | 10% | |
| W6 | Maintainability | REQ-XXX | 10% | |
| **Total** | | | **100%** | |

---

## 3. Alternatives

### 3.1 Alternative A: [Name]
**Description:** [Concept description]
**TRL:** [1-9]
**Key Characteristics:**
- [Bullet points]

### 3.2 Alternative B: [Name]
**Description:** [Concept description]
**TRL:** [1-9]
**Key Characteristics:**
- [Bullet points]

### 3.3 Alternative C: [Name]
**Description:** [Concept description]
**TRL:** [1-9]
**Key Characteristics:**
- [Bullet points]

---

## 3.4 Requirements Trace Matrix (P-040)

> **P-040 Traceability:** Per [INCOSE best practices](https://www.incose.org/docs/default-source/working-groups/requirements-wg/monthlymeetings2024/traceability_110524.pdf)
> and [NPR 7123.1D](https://nodis3.gsfc.nasa.gov/displayDir.cfm?t=NPR&c=7123&s=1B), all design
> alternatives must trace to requirements they address.

| Requirement | Description | Alt A | Alt B | Alt C | Notes |
|-------------|-------------|:-----:|:-----:|:-----:|-------|
| REQ-XXX-001 | [Brief desc] | Full | Partial | Gap | |
| REQ-XXX-002 | [Brief desc] | Full | Full | Full | |
| REQ-XXX-003 | [Brief desc] | Partial | Full | N/A | |

**Legend:** Full coverage | Partial coverage | Gap (not addressed) | N/A (not applicable)

**Coverage Summary:**
| Alternative | Full | Partial | Gap | Coverage % |
|-------------|------|---------|-----|------------|
| Alt A | X | Y | Z | NN% |
| Alt B | X | Y | Z | NN% |
| Alt C | X | Y | Z | NN% |

**Gap Analysis:**
- [List any requirements not fully addressed by any alternative]
- [Identify risks from coverage gaps]

---

## 4. Trade Matrix

### 4.1 Must-Have Screening
| Criterion | Alt A | Alt B | Alt C |
|-----------|-------|-------|-------|
| M1 | PASS | PASS | FAIL |
| M2 | PASS | PASS | PASS |
| **Proceed?** | **YES** | **YES** | **NO** |

### 4.2 Weighted Scoring
*Scale: 1 (Poor) to 5 (Excellent)*

| Criterion | Weight | Alt A Score | A Weighted | Alt B Score | B Weighted |
|-----------|--------|-------------|------------|-------------|------------|
| W1: Performance | 25% | | | | |
| W2: Cost | 20% | | | | |
| W3: Schedule | 15% | | | | |
| W4: Risk | 20% | | | | |
| W5: Reliability | 10% | | | | |
| W6: Maintainability | 10% | | | | |
| **Total** | **100%** | | **[Sum]** | | **[Sum]** |

### 4.3 Color-Coded Summary
| Alternative | Score | Assessment |
|-------------|-------|------------|
| Alternative A | [X.XX] | GREEN / YELLOW / RED |
| Alternative B | [X.XX] | GREEN / YELLOW / RED |

---

## 5. Sensitivity Analysis

### 5.1 Weight Sensitivity
| Scenario | Weight Change | Winner | Margin |
|----------|---------------|--------|--------|
| Baseline | As defined | Alt [X] | [Y.YY] |
| Cost +10% | Cost=30% | Alt [X] | [Y.YY] |
| Risk +10% | Risk=30% | Alt [X] | [Y.YY] |

### 5.2 Score Sensitivity
[Analysis of how score changes would affect the outcome]

---

## 6. Risks and Mitigations

| Alternative | Key Risks | Severity | Mitigation |
|-------------|-----------|----------|------------|
| A | | | |
| B | | | |

---

## 7. Recommendation

### 7.1 Selected Alternative
**Recommended: Alternative [X]**

### 7.2 Rationale
[Clear explanation of why this alternative is recommended]

### 7.3 Conditions/Assumptions
- [Assumption 1]
- [Assumption 2]

---

## 8. Decision Record

| Field | Value |
|-------|-------|
| Decision | [Selected alternative] |
| Date | [Approval date] |
| Approver | [Name/Role] |
| Review Forum | [PDR/CDR/CCB] |

---

## Appendices

### A. Detailed Alternative Descriptions
### B. Scoring Rationale
### C. Supporting Data
### D. References

---

*DISCLAIMER: This trade study is AI-generated guidance based on NASA Systems
Engineering standards. It is advisory only and does not constitute official NASA
guidance. All architecture decisions require human review and professional
engineering judgment. Not for use in mission-critical decisions without SME validation.*
```
