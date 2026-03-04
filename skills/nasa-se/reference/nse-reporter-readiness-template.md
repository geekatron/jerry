# Review Readiness Assessment Template

> Runtime template for nse-reporter agent. Load via Read tool when generating review readiness assessments.

```markdown
# [Review Type] Readiness Assessment

> **Review:** [SRR/PDR/CDR/TRR/FRR]
> **Target Date:** [YYYY-MM-DD]
> **Assessment Date:** [YYYY-MM-DD]
> **Assessed By:** [Name/Role]

---

## Readiness Summary

### Overall Assessment: READY / CONDITIONALLY READY / NOT READY

| Category | Status | Critical Items |
|----------|:------:|----------------|
| Entrance Criteria | G/Y/R | [Count] not met |
| Documentation | G/Y/R | [Count] incomplete |
| Technical Maturity | G/Y/R | [Key issue] |
| Open Actions | G/Y/R | [Count] open |
| Risk Status | G/Y/R | [Count] RED risks |

---

## Entrance Criteria Status

| # | Criterion | Status | Evidence | Notes |
|---|-----------|:------:|----------|-------|
| 1 | [From checklist] | Met/Partial/Not Met | | |
| 2 | | | | |
| 3 | | | | |

**Entrance Criteria Met:** [X] of [Y] ([Z]%)

---

## Documentation Readiness

| Document | Required For | Status | Version | Notes |
|----------|--------------|:------:|---------|-------|
| Requirements Spec | Review | Y/N | | |
| Design Document | Review | Y/N | | |
| VCRM | Review | Y/N | | |
| Risk Register | Review | Y/N | | |
| ICDs | Review | Y/N | | |

---

## Open Action Items

### From Previous Reviews
| AI ID | Source | Description | Status | Impact |
|-------|--------|-------------|:------:|--------|
| | | | Done/InProgress/Not | |

### Total Open: [X] | Blocking: [Y]

---

## Risk Status for Review

### RED Risks Requiring Discussion
| Risk ID | Title | Score | Mitigation Status |
|---------|-------|-------|-------------------|
| | | | |

### Risk Summary
- RED: [X]
- YELLOW: [Y]
- GREEN: [Z]

---

## Recommendation

### Assessment: [READY / CONDITIONALLY READY / NOT READY]

**Rationale:**
[Explanation of assessment]

**Conditions (if applicable):**
1. [Condition 1 to be met before/during review]
2. [Condition 2]

**Recommended Actions Before Review:**
1. [Action 1]
2. [Action 2]

---

*DISCLAIMER: AI-generated readiness assessment. Final review readiness
determination requires human judgment and project authority approval.*
```
