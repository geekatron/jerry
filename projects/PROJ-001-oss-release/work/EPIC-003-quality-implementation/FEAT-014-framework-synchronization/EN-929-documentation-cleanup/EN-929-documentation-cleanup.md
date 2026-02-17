# EN-929: Minor Documentation Cleanup

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-17 (Claude)
PURPOSE: Bundle of minor documentation improvements from codebase gap analysis
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** low
> **Impact:** low
> **Enabler Type:** infrastructure
> **Created:** 2026-02-17
> **Due:** --
> **Completed:** --
> **Parent:** FEAT-014
> **Owner:** --
> **Effort:** 2

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this enabler delivers |
| [Problem Statement](#problem-statement) | Why this work is needed |
| [Business Value](#business-value) | How this enabler supports parent feature delivery |
| [Technical Approach](#technical-approach) | How we will implement it |
| [Children (Tasks)](#children-tasks) | Task breakdown |
| [Progress Summary](#progress-summary) | Current completion status |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Evidence](#evidence) | Deliverables and verification |
| [Dependencies](#dependencies) | Dependencies and items enabled |
| [Related Items](#related-items) | Hierarchy and related work |
| [History](#history) | Change log |

---

## Summary

Bundle of minor documentation improvements identified during the codebase gap analysis. Includes template naming clarification, agent directory documentation, architecture-orchestration integration reference, and rule index verification. None are blockers but all improve framework consistency and discoverability.

**Technical Scope:**
- Clarify adversarial template naming and versioning conventions
- Document agent vs template file distinction in skill agent directories
- Add orchestration pattern reference to architecture standards
- Verify HARD rule index completeness in quality-enforcement.md
- Improve adversary SKILL.md usage guidance

---

## Problem Statement

Several minor documentation inconsistencies and gaps were identified during the PROJ-001 codebase audit. Individually each is low priority, but collectively they create friction for framework users. Template naming conventions in the adversary skill are unclear (templates are static files, not generated), agent directories lack README files distinguishing agent files from template/extension files, architecture-standards.md does not reference orchestration patterns, H-16 may be missing from the quality-enforcement.md HARD Rule Index, and the adversary SKILL.md "When NOT to Use" guidance could be more comprehensive.

---

## Business Value

Fixing these documentation gaps supports FEAT-014 by ensuring the framework is internally consistent and discoverable. Clear documentation reduces onboarding friction and prevents agents from misinterpreting conventions, which directly supports framework synchronization goals.

### Features Unlocked

- Enables consistent agent execution by eliminating documentation ambiguity
- Improves framework discoverability for new users and agents

---

## Technical Approach

1. Clarify template naming conventions in adversary SKILL.md (templates are static files, not generated)
2. Add brief README to agent directories distinguishing agent files from template/extension files
3. Add architecture-orchestration integration paragraph to architecture-standards.md
4. Verify H-16 (Steelman before critique) appears in quality-enforcement.md HARD Rule Index
5. Improve adv-executor vs ps-critic selection guidance in adversary SKILL.md

All five tasks are independent and can run in parallel.

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Activity | Owner |
|----|-------|--------|----------|-------|
| TASK-001 | Clarify adversarial template naming in SKILL.md Dependencies section | pending | DEVELOPMENT | ps-architect |
| TASK-002 | Document agent vs template file distinction in PS and NSE agent dirs | pending | DEVELOPMENT | ps-architect |
| TASK-003 | Add orchestration pattern reference to architecture-standards.md | pending | DEVELOPMENT | ps-architect |
| TASK-004 | Verify H-16 in quality-enforcement.md HARD Rule Index | pending | REVIEW | ps-critic |
| TASK-005 | Improve "When NOT to Use" guidance in adversary SKILL.md | pending | DEVELOPMENT | ps-architect |

---

## Progress Summary

### Status Overview

```
[                    ] 0% (0/5 tasks)
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| Total Tasks | 5 |
| Completed | 0 |
| In Progress | 0 |
| Pending | 5 |
| Blocked | 0 |
| Completion | 0% |

---

## Acceptance Criteria

### Definition of Done

- [ ] Adversary SKILL.md clarifies template naming and versioning
- [ ] Agent directories have clear distinction between agent files and support files
- [ ] architecture-standards.md references orchestration patterns
- [ ] H-16 verified in quality-enforcement.md index (fix if missing)
- [ ] adversary SKILL.md "When to Use" section is comprehensive

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| TC-1 | Template naming clarification uses MEDIUM-tier language (SHOULD/RECOMMENDED) | [ ] |
| TC-2 | Agent directory READMEs follow H-23/H-24 navigation requirements if over 30 lines | [ ] |
| TC-3 | Architecture-orchestration reference is consistent with existing standards format | [ ] |
| TC-4 | H-16 row in HARD Rule Index matches format of existing entries | [ ] |
| TC-5 | Adversary SKILL.md guidance is actionable and consistent with skill table style | [ ] |

---

## Evidence

### Deliverables

| # | Deliverable | Path | Status |
|---|-------------|------|--------|
| 1 | -- | -- | Pending |

### Verification Checklist

- [ ] All acceptance criteria verified
- [ ] All technical criteria verified
- [ ] No regressions introduced
- [ ] Changes consistent with existing documentation style

---

## Dependencies

### Depends On

- None (all tasks are independent)

### Enables

- Improved framework consistency for future PROJ-001 work

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-014: Framework Synchronization](../FEAT-014-framework-synchronization.md)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-17 | Claude | pending | Enabler created from PROJ-001 codebase gap analysis findings |
