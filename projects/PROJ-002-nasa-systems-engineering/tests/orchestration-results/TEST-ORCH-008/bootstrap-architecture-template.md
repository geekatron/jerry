# Trade Study Report: [DECISION_TOPIC]

> **Document ID:** TSR-[PROJECT_ID]-001
> **Version:** 0.1
> **Date:** [DATE]
> **Author:** [AUTHOR_NAME]
> **Status:** [DRAFT / IN REVIEW / APPROVED]

---

## Document Control

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Author | [AUTHOR_NAME] | [DATE] | |
| Technical Reviewer | [REVIEWER_NAME] | | |
| Approver | [APPROVER_NAME] | | |

---

## 1. Purpose and Scope

### 1.1 Decision Statement
[Clear statement of the decision to be made. What are we choosing between?]

### 1.2 Scope
| Attribute | Value |
|-----------|-------|
| System/Subsystem | [SYSTEM_NAME] |
| WBS Element | [WBS_NUMBER] |
| Phase | [Formulation / Implementation] |
| Decision Type | [Architecture / Design / Make/Buy / Technology] |

**Driving Requirements:**
| Req ID | Title | Impact |
|--------|-------|--------|
| [REQ-XXX] | [TITLE] | [How this requirement influences the decision] |

### 1.3 Constraints

| Type | Constraint | Impact on Decision |
|------|------------|-------------------|
| Technical | [CONSTRAINT] | [IMPACT] |
| Cost | [CONSTRAINT] | [IMPACT] |
| Schedule | [CONSTRAINT] | [IMPACT] |
| Policy | [CONSTRAINT] | [IMPACT] |

### 1.4 Assumptions

| ID | Assumption | Risk if Invalid |
|----|------------|-----------------|
| A-001 | [ASSUMPTION_STATEMENT] | [RISK] |

---

## 2. Evaluation Criteria

### 2.1 Must-Have Criteria (Pass/Fail)

| # | Criterion | Source | Threshold | Verification |
|---|-----------|--------|-----------|--------------|
| M1 | [MANDATORY_CRITERION] | [REQ-XXX] | [PASS_CONDITION] | [HOW_VERIFIED] |
| M2 | [MANDATORY_CRITERION] | [REQ-XXX] | [PASS_CONDITION] | [HOW_VERIFIED] |
| M3 | [MANDATORY_CRITERION] | [STANDARD] | [PASS_CONDITION] | [HOW_VERIFIED] |

### 2.2 Want Criteria (Weighted)

| # | Criterion | Source | Weight | Rationale |
|---|-----------|--------|--------|-----------|
| W1 | [CRITERION_NAME] | [SOURCE] | [N]% | [WHY_IMPORTANT] |
| W2 | [CRITERION_NAME] | [SOURCE] | [N]% | [WHY_IMPORTANT] |
| W3 | [CRITERION_NAME] | [SOURCE] | [N]% | [WHY_IMPORTANT] |
| W4 | [CRITERION_NAME] | [SOURCE] | [N]% | [WHY_IMPORTANT] |
| W5 | [CRITERION_NAME] | [SOURCE] | [N]% | [WHY_IMPORTANT] |
| **Total** | | | **100%** | |

**Weighting Rationale:**
[Explain how weights were derived and why the balance is appropriate]

---

## 3. Alternatives

### 3.1 Alternative A: [ALTERNATIVE_NAME]

**Description:** [Detailed description of this alternative]

**Architecture/Design:**
```
[Diagram or structured representation of this alternative]
```

**Key Characteristics:**
- [CHARACTERISTIC_1]
- [CHARACTERISTIC_2]
- [CHARACTERISTIC_3]

**Advantages:**
- [ADVANTAGE_1]
- [ADVANTAGE_2]

**Disadvantages:**
- [DISADVANTAGE_1]
- [DISADVANTAGE_2]

**Estimated Cost:** [COST_ESTIMATE]
**Estimated Schedule:** [SCHEDULE_ESTIMATE]
**TRL:** [TECHNOLOGY_READINESS_LEVEL]

---

### 3.2 Alternative B: [ALTERNATIVE_NAME]

**Description:** [Detailed description]

**Architecture/Design:**
```
[Diagram or structured representation]
```

**Key Characteristics:**
- [CHARACTERISTIC_1]
- [CHARACTERISTIC_2]

**Advantages:**
- [ADVANTAGE_1]
- [ADVANTAGE_2]

**Disadvantages:**
- [DISADVANTAGE_1]
- [DISADVANTAGE_2]

**Estimated Cost:** [COST_ESTIMATE]
**Estimated Schedule:** [SCHEDULE_ESTIMATE]
**TRL:** [TECHNOLOGY_READINESS_LEVEL]

---

### 3.3 Alternative C: [ALTERNATIVE_NAME]

**Description:** [Detailed description]

**Key Characteristics:**
- [CHARACTERISTIC_1]
- [CHARACTERISTIC_2]

**Advantages / Disadvantages:**
[Summary]

**Estimated Cost:** [COST_ESTIMATE]
**Estimated Schedule:** [SCHEDULE_ESTIMATE]
**TRL:** [TRL]

---

## 4. Trade Matrix

### 4.1 Must-Have Screening

| Criterion | Alt A | Alt B | Alt C |
|-----------|-------|-------|-------|
| M1: [CRITERION] | [PASS/FAIL] | [PASS/FAIL] | [PASS/FAIL] |
| M2: [CRITERION] | [PASS/FAIL] | [PASS/FAIL] | [PASS/FAIL] |
| M3: [CRITERION] | [PASS/FAIL] | [PASS/FAIL] | [PASS/FAIL] |
| **Proceed to Want Scoring?** | **[YES/NO]** | **[YES/NO]** | **[YES/NO]** |

### 4.2 Weighted Scoring

*Scale: 1 (Poor) to 5 (Excellent)*

| Criterion | Weight | Alt A Raw | A Weighted | Alt B Raw | B Weighted | Alt C Raw | C Weighted |
|-----------|--------|-----------|------------|-----------|------------|-----------|------------|
| W1: [CRITERION] | [N]% | [1-5] | [CALC] | [1-5] | [CALC] | [1-5] | [CALC] |
| W2: [CRITERION] | [N]% | [1-5] | [CALC] | [1-5] | [CALC] | [1-5] | [CALC] |
| W3: [CRITERION] | [N]% | [1-5] | [CALC] | [1-5] | [CALC] | [1-5] | [CALC] |
| W4: [CRITERION] | [N]% | [1-5] | [CALC] | [1-5] | [CALC] | [1-5] | [CALC] |
| W5: [CRITERION] | [N]% | [1-5] | [CALC] | [1-5] | [CALC] | [1-5] | [CALC] |
| **Total** | **100%** | | **[TOTAL]** | | **[TOTAL]** | | **[TOTAL]** |

### 4.3 Scoring Rationale

**W1: [CRITERION_NAME]**
- Alt A ([SCORE]): [RATIONALE]
- Alt B ([SCORE]): [RATIONALE]
- Alt C ([SCORE]): [RATIONALE]

**W2: [CRITERION_NAME]**
- Alt A ([SCORE]): [RATIONALE]
- Alt B ([SCORE]): [RATIONALE]
- Alt C ([SCORE]): [RATIONALE]

[Continue for each criterion...]

### 4.4 Color-Coded Summary

| Alternative | Score | Assessment |
|-------------|-------|------------|
| **[ALT_NAME]** | **[SCORE]** | [RECOMMENDED / ACCEPTABLE / NOT_RECOMMENDED] |
| [ALT_NAME] | [SCORE] | [Status] |
| [ALT_NAME] | [SCORE] | [Status] |

---

## 5. Sensitivity Analysis

### 5.1 Weight Sensitivity

| Scenario | Weight Change | Winner | Margin |
|----------|---------------|--------|--------|
| Baseline | As defined | [ALT] | [MARGIN] |
| [SCENARIO_NAME] | [CHANGE] | [ALT] | [MARGIN] |
| [SCENARIO_NAME] | [CHANGE] | [ALT] | [MARGIN] |

**Findings:** [Summary of what the sensitivity analysis reveals]

### 5.2 Score Sensitivity

- [Finding about score sensitivity]
- Break-even: [What would need to change for different winner]

---

## 6. Risks and Mitigations

| Alternative | Key Risks | Severity | Mitigation |
|-------------|-----------|----------|------------|
| [ALT_A] | [RISK_1] | [H/M/L] | [MITIGATION] |
| [ALT_A] | [RISK_2] | [H/M/L] | [MITIGATION] |
| [ALT_B] | [RISK_1] | [H/M/L] | [MITIGATION] |
| [ALT_C] | [RISK_1] | [H/M/L] | [MITIGATION] |

---

## 7. Recommendation

### 7.1 Selected Alternative
**Recommended: [ALTERNATIVE_NAME]**

### 7.2 Rationale
1. [REASON_1]
2. [REASON_2]
3. [REASON_3]

### 7.3 Conditions and Assumptions
- [CONDITION_1]
- [CONDITION_2]
- [ASSUMPTION_DEPENDENCY]

### 7.4 Actions Required
| # | Action | Owner | Due Date |
|---|--------|-------|----------|
| 1 | [ACTION] | [OWNER] | [DATE] |
| 2 | [ACTION] | [OWNER] | [DATE] |

---

## 8. Decision Record

| Field | Value |
|-------|-------|
| Decision | [SELECTED_ALTERNATIVE] |
| Decision Date | [DATE] |
| Decision Authority | [APPROVER_NAME/ROLE] |
| Review Forum | [MEETING/REVIEW_NAME] |
| Decision Rationale | [BRIEF_SUMMARY] |

---

## 9. Alternatives Considered but Not Evaluated

| Alternative | Reason for Exclusion |
|-------------|---------------------|
| [ALT_NAME] | [REASON] |

---

## Appendix A: Cost Analysis

| Alternative | Development | Operations | Lifecycle Total |
|-------------|-------------|------------|-----------------|
| [ALT_A] | $[AMOUNT] | $[AMOUNT] | $[AMOUNT] |
| [ALT_B] | $[AMOUNT] | $[AMOUNT] | $[AMOUNT] |
| [ALT_C] | $[AMOUNT] | $[AMOUNT] | $[AMOUNT] |

**Cost Estimation Basis:** [Description of how costs were estimated]

---

## Appendix B: Schedule Analysis

| Alternative | Development Duration | Key Milestones | Risk to Schedule |
|-------------|---------------------|----------------|------------------|
| [ALT_A] | [DURATION] | [MILESTONES] | [H/M/L] |
| [ALT_B] | [DURATION] | [MILESTONES] | [H/M/L] |
| [ALT_C] | [DURATION] | [MILESTONES] | [H/M/L] |

---

## Appendix C: Trade Study Participants

| Name | Role | Organization | Contribution |
|------|------|--------------|--------------|
| [NAME] | [ROLE] | [ORG] | [CONTRIBUTION] |

---

## Appendix D: Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | [DATE] | [AUTHOR] | Initial draft |

---

## References

- NPR 7123.1D, NASA Systems Engineering Processes and Requirements
- NASA/SP-2016-6105 Rev2, NASA Systems Engineering Handbook
- NASA-HDBK-1009A, NASA Systems Engineering Guidelines for Work Products

---

*DISCLAIMER: This trade study report is AI-generated based on NASA Systems Engineering standards (NPR 7123.1D, NASA/SP-2016-6105). It is advisory only and does not constitute official NASA guidance. All architecture and design decisions require human review and professional engineering judgment. Trade study results must be validated by qualified Systems Engineers before use in mission-critical applications.*
