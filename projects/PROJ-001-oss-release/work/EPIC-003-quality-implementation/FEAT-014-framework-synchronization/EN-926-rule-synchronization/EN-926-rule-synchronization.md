# EN-926: Rule Synchronization

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-17 (Claude)
PURPOSE: Synchronize framework rules with /adversary skill and quality enforcement SSOT
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Enabler Type:** infrastructure
> **Created:** 2026-02-17
> **Due:** --
> **Completed:** --
> **Parent:** FEAT-014
> **Owner:** --
> **Effort:** 3

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this enabler delivers |
| [Problem Statement](#problem-statement) | Why this work is needed |
| [Business Value](#business-value) | How this enabler supports parent feature delivery |
| [Technical Approach](#technical-approach) | How we'll implement it |
| [Children (Tasks)](#children-tasks) | Task breakdown |
| [Progress Summary](#progress-summary) | Current completion status |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Evidence](#evidence) | Deliverables and verification |
| [Dependencies](#dependencies) | Dependencies and task ordering |
| [Related Items](#related-items) | Dependencies and hierarchy |
| [History](#history) | Change log |

---

## Summary

Synchronize framework rules with the /adversary skill and quality enforcement SSOT. The mandatory-skill-usage rule (H-22) does not trigger for adversarial quality reviews, and quality-enforcement.md does not reference the /adversary skill as its operational implementation.

**Technical Scope:**
- Update mandatory-skill-usage.md trigger map to include /adversary
- Add Implementation section to quality-enforcement.md linking to /adversary
- Add adversary vs ps-critic selection guidance

---

## Problem Statement

H-22 triggers /problem-solving, /nasa-se, and /orchestration proactively but not /adversary. This means quality reviews that should use the adversary skill will not be automatically invoked. Additionally, quality-enforcement.md defines all strategies but does not link to the skill that operationalizes them. This gap undermines the quality enforcement framework's effectiveness.

---

## Business Value

Closing the rule synchronization gap ensures that adversarial quality reviews are triggered proactively when relevant keywords are detected, and that quality-enforcement.md serves as a complete reference linking strategy definitions to their operational implementation via the /adversary skill.

### Features Unlocked

- Automatic /adversary invocation for quality review, critique, and tournament keywords
- Complete traceability from quality enforcement strategies to their skill implementation

---

## Technical Approach

1. Add /adversary keywords to mandatory-skill-usage.md trigger map (quality review, critique, adversarial, tournament, red team, devil's advocate)
2. Update H-22 rule text to include adversarial quality reviews
3. Add Implementation section to quality-enforcement.md linking strategy catalog to /adversary skill
4. Add adversary vs ps-critic selection guidance to adversary SKILL.md

---

## Children (Tasks)

| ID | Title | Status | Activity | Owner |
|----|-------|--------|----------|-------|
| TASK-001 | Add /adversary triggers to mandatory-skill-usage.md H-22 | pending | DEVELOPMENT | ps-architect |
| TASK-002 | Add Implementation section to quality-enforcement.md | pending | DEVELOPMENT | ps-architect |
| TASK-003 | Add adversary vs ps-critic selection guidance to adversary SKILL.md | pending | DEVELOPMENT | ps-architect |

---

## Progress Summary

### Status Overview

```
[                    ] 0% (0/3 tasks)
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| Total Tasks | 3 |
| Completed | 0 |
| In Progress | 0 |
| Pending | 3 |
| Blocked | 0 |
| Completion | 0% |

---

## Acceptance Criteria

### Definition of Done

- [ ] mandatory-skill-usage.md H-22 includes /adversary with trigger keywords
- [ ] quality-enforcement.md has Implementation section referencing /adversary skill
- [ ] adversary SKILL.md includes when-to-use guidance distinguishing from ps-critic

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| 1 | H-22 trigger map includes /adversary with appropriate keywords | [ ] |
| 2 | quality-enforcement.md Implementation section links strategies to /adversary | [ ] |
| 3 | adversary SKILL.md distinguishes /adversary from ps-critic usage | [ ] |

---

## Evidence

### Deliverables

| # | Deliverable | Path | Status |
|---|-------------|------|--------|
| 1 | -- | -- | Pending |

### Verification Checklist

- [ ] All acceptance criteria verified
- [ ] All technical criteria verified
- [ ] Quality gate score >= 0.92
- [ ] Creator-critic-revision cycle completed (minimum 3 iterations)
- [ ] No regressions introduced

---

## Dependencies

### Task Dependencies

All 3 tasks can run in parallel (independent file modifications).

### Depends On

- None

### Enables

- Proactive /adversary invocation via H-22 triggers
- Complete strategy-to-skill traceability in quality enforcement SSOT

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-014: Framework Synchronization](../FEAT-014-framework-synchronization.md)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-17 | Claude | pending | Enabler created for FEAT-014 framework synchronization. |
