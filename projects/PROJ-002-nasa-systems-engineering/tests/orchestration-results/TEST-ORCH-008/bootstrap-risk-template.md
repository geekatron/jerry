# Risk Register: [PROJECT_NAME]

> **Document ID:** RISK-[PROJECT_ID]-001
> **Version:** 0.1
> **Date:** [DATE]
> **Status:** ACTIVE
> **Risk Manager:** [RISK_MANAGER_NAME]

---

## Document Control

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Risk Manager | [RISK_MANAGER_NAME] | [DATE] | |
| Project Manager | [PM_NAME] | | |
| Technical Authority | [TA_NAME] | | |

---

## Risk Summary Dashboard

| Level | Count | Change | Status |
|-------|-------|--------|--------|
| RED (16-25) | [N] | [+/-/--] | [Status] |
| YELLOW (8-15) | [N] | [+/-/--] | [Status] |
| GREEN (1-7) | [N] | [+/-/--] | [Status] |
| **Total Active** | **[N]** | | |

**Report Period:** [START_DATE] to [END_DATE]
**Next Review:** [NEXT_REVIEW_DATE]

---

## 5x5 Risk Matrix (Current State)

|  | **Consequence** |||||
|---|:---:|:---:|:---:|:---:|:---:|
| **Likelihood** | 1 (Min) | 2 (Low) | 3 (Mod) | 4 (High) | 5 (Max) |
| 5 (Very High) | | | | | |
| 4 (High) | | | | [R-XXX] | [R-XXX] |
| 3 (Moderate) | | | [R-XXX] | | |
| 2 (Low) | | [R-XXX] | | | |
| 1 (Very Low) | [R-XXX] | | | | |

*Place Risk IDs in appropriate cells based on L x C scoring*

---

## Likelihood Definitions

| Score | Level | Description | Criteria |
|-------|-------|-------------|----------|
| 5 | Very High | Near certain | >90% probability |
| 4 | High | Likely | 60-90% probability |
| 3 | Moderate | Possible | 30-60% probability |
| 2 | Low | Unlikely | 10-30% probability |
| 1 | Very Low | Remote | <10% probability |

## Consequence Definitions

| Score | Level | Cost Impact | Schedule Impact | Technical Impact | Safety Impact |
|-------|-------|-------------|-----------------|------------------|---------------|
| 5 | Maximum | >25% budget | >12 months slip | Mission failure | Loss of life |
| 4 | High | 15-25% budget | 6-12 months slip | Major redesign | Serious injury |
| 3 | Moderate | 5-15% budget | 3-6 months slip | Significant rework | Minor injury |
| 2 | Low | 1-5% budget | 1-3 months slip | Minor rework | First aid |
| 1 | Minimal | <1% budget | <1 month slip | Negligible | None |

---

## Active Risks

### R-001: [RISK_TITLE]

| Attribute | Value |
|-----------|-------|
| **ID** | R-001 |
| **Status** | [OPEN / MITIGATING / WATCH / CLOSED] |
| **Category** | [Technical / Schedule / Cost / Safety / Programmatic] |
| **Owner** | [RISK_OWNER_NAME] |
| **Identified** | [DATE] |
| **Last Updated** | [DATE] |

**Risk Statement:**
> IF [condition/event/trigger],
> THEN [consequence description],
> resulting in [impact on project objectives].

**Context:**
[Additional background, root cause analysis, or contributing factors]

| Factor | Score | Rationale |
|--------|-------|-----------|
| Likelihood | [1-5] | [Justification for score] |
| Consequence | [1-5] | [Justification for score] |
| **Risk Score** | **[L x C]** | [COLOR: RED/YELLOW/GREEN] |

**Mitigations Planned/Implemented:**

| # | Action | Type | Status | Due Date | Owner | Evidence |
|---|--------|------|--------|----------|-------|----------|
| 1 | [MITIGATION_ACTION] | [Prevent/Reduce/Accept] | [Planned/In Progress/Complete] | [DATE] | [NAME] | [EVIDENCE] |
| 2 | [MITIGATION_ACTION] | [Type] | [Status] | [DATE] | [NAME] | [EVIDENCE] |

**Residual Risk (post-mitigation):** Score [N] (L=[N], C=[N]) - [COLOR]
- [Explanation of why residual risk is at this level]

**Escalation:** [Escalation path if risk materializes or exceeds threshold]

**Watch Indicators:**
- [INDICATOR_1]
- [INDICATOR_2]

---

### R-002: [RISK_TITLE]

| Attribute | Value |
|-----------|-------|
| **ID** | R-002 |
| **Status** | |
| **Category** | |
| **Owner** | |
| **Identified** | [DATE] |
| **Last Updated** | [DATE] |

**Risk Statement:**
> IF [condition],
> THEN [consequence],
> resulting in [impact].

| Factor | Score | Rationale |
|--------|-------|-----------|
| Likelihood | | |
| Consequence | | |
| **Risk Score** | **[ ]** | |

**Mitigations:**

| # | Action | Type | Status | Due Date | Owner |
|---|--------|------|--------|----------|-------|
| 1 | | | | | |

---

## Opportunities (Positive Risks)

### O-001: [OPPORTUNITY_TITLE]

| Attribute | Value |
|-----------|-------|
| **ID** | O-001 |
| **Category** | [Cost Savings / Schedule Improvement / Technical Enhancement] |
| **Owner** | [NAME] |

**Opportunity Statement:**
> IF [condition], THEN [benefit], resulting in [positive impact].

| Factor | Score | Rationale |
|--------|-------|-----------|
| Probability | [1-5] | |
| Benefit | [1-5] | |
| **Opportunity Score** | **[ ]** | |

**Exploitation Actions:**
| # | Action | Status | Due Date | Owner |
|---|--------|--------|----------|-------|
| 1 | | | | |

---

## Risk Trends

| Metric | Previous | Current | Target | Trend |
|--------|----------|---------|--------|-------|
| Total Risks | [N] | [N] | - | [UP/DOWN/STABLE] |
| RED Risks | [N] | [N] | 0 unmitigated | |
| Total Exposure | [N] | [N] | <[TARGET] | |
| Residual Exposure | [N] | [N] | <[TARGET] | |
| Closed Risks | [N] | [N] | - | |
| New Risks (period) | [N] | [N] | - | |

---

## Closed Risks

| ID | Title | Original Score | Closure Date | Closure Reason |
|----|-------|----------------|--------------|----------------|
| [R-XXX] | [TITLE] | [SCORE] | [DATE] | [Mitigated / Not Realized / Transferred] |

---

## Risk Review Schedule

| Review Type | Frequency | Next Date | Participants |
|-------------|-----------|-----------|--------------|
| Risk Working Group | [Weekly/Bi-weekly] | [DATE] | [ROLES] |
| Risk Board | [Monthly] | [DATE] | [ROLES] |
| Project Status Review | [Bi-weekly] | [DATE] | [ROLES] |

---

## Risk Matrix Legend

| Score Range | Level | Color | Action Required |
|-------------|-------|-------|-----------------|
| 16-25 | RED | HIGH RISK | Immediate mitigation required; escalate to management |
| 8-15 | YELLOW | MEDIUM RISK | Active mitigation and monitoring required |
| 1-7 | GREEN | LOW RISK | Accept and monitor; document acceptance rationale |

---

## Escalation Thresholds

| Condition | Escalation Level | Action |
|-----------|------------------|--------|
| Any RED risk | Project Manager + Technical Authority | Immediate review, mitigation plan required |
| Total exposure >[THRESHOLD] | [AUTHORITY] | Risk reduction plan required |
| New RED risk identified | [AUTHORITY] | 48-hour mitigation plan |
| Risk realizes | [AUTHORITY] | Activate contingency plan |

---

## Appendix A: Risk Categories

| Category | Description | Examples |
|----------|-------------|----------|
| Technical | Design, implementation, performance risks | Software bugs, hardware failures |
| Schedule | Timeline and milestone risks | Delays, dependencies |
| Cost | Budget and resource risks | Overruns, funding gaps |
| Safety | Personnel and public safety risks | Hazards, accidents |
| Programmatic | Organizational, political, regulatory risks | Policy changes, approvals |

---

## Appendix B: Change Log

| Date | Author | Changes |
|------|--------|---------|
| [DATE] | [NAME] | Initial risk register |

---

## References

- NPR 8000.4C, Agency Risk Management Procedural Requirements
- NPR 7123.1D, NASA Systems Engineering Processes and Requirements
- NASA/SP-2011-3422, NASA Risk Management Handbook

---

*DISCLAIMER: This risk register is AI-generated based on NASA Systems Engineering standards (NPR 8000.4C, NPR 7123.1D). It is advisory only and does not constitute official NASA guidance. All risk management decisions require human review and professional engineering judgment. Risk assessments must be validated by qualified risk management professionals before use in mission-critical applications.*
