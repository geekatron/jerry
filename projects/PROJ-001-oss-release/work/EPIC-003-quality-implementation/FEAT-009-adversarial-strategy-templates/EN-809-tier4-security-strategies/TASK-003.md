# TASK-003: Creator-critic-revision quality cycle

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** pending
> **Priority:** HIGH
> **Activity:** REVIEW
> **Agents:** ps-critic
> **Created:** 2026-02-14
> **Parent:** EN-809

---

## Document Sections
| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this task delivers |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Evidence](#evidence) | Deliverables and verification |
| [Related Items](#related-items) | Parent and dependencies |
| [History](#history) | Change log |

---

## Summary

Apply the creator-critic-revision quality cycle to both S-001 Red Team Analysis and S-011 Chain-of-Verification templates produced by TASK-001 and TASK-002. This review task ensures both templates meet the >= 0.92 quality threshold per H-13 through a minimum of 3 iterations of the creator-critic-revision cycle per H-14.

The quality cycle for each template must:
1. **Critic phase**: Apply S-003 Steelman first (H-16) to identify the strongest interpretation of the template, then apply S-002 Devil's Advocate to challenge assumptions, completeness, and methodological rigor.
2. **Score phase**: Apply S-014 LLM-as-Judge rubric across all 6 dimensions (Completeness 0.20, Internal Consistency 0.20, Methodological Rigor 0.20, Evidence Quality 0.15, Actionability 0.15, Traceability 0.10).
3. **Revision phase**: Creator addresses critic findings, improving the template until the weighted composite score reaches >= 0.92.

### Acceptance Criteria
- [ ] S-001 Red Team template reviewed with >= 3 creator-critic-revision iterations
- [ ] S-011 CoVe template reviewed with >= 3 creator-critic-revision iterations
- [ ] S-003 Steelman applied before S-002 Devil's Advocate in each iteration (H-16)
- [ ] S-014 LLM-as-Judge scoring applied with all 6 dimensions and correct weights
- [ ] Both templates achieve weighted composite score >= 0.92
- [ ] Revision history documenting each iteration's findings and improvements
- [ ] Quality gate: Deliverable reviewed via creator-critic-revision cycle (min 3 iterations)
- [ ] Quality gate: Score >= 0.92 via S-014 LLM-as-Judge rubric
- [ ] Quality gate: S-003 Steelman applied before S-002 Devil's Advocate critique

### Related Items
- Parent: [EN-809: Tier 4 Security Strategy Templates](EN-809-tier4-security-strategies.md)
- Depends on: TASK-001 (S-001 template must exist)
- Depends on: TASK-002 (S-011 template must exist)

---

## Evidence
### Deliverables
| Deliverable | Type | Link |
|-------------|------|------|
| S-001 quality review report | Review artifact | --- |
| S-011 quality review report | Review artifact | --- |
| Iteration history (scores per iteration) | Quality evidence | --- |

### Verification
- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History
| Date | Status | Notes |
|------|--------|-------|
| 2026-02-14 | Created | Initial creation. |
