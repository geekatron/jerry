# EN-929: Minor Documentation Cleanup

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-17 (Claude)
PURPOSE: Bundle of minor documentation improvements from codebase gap analysis
-->

> **Type:** enabler
> **Status:** done
> **Priority:** low
> **Impact:** low
> **Enabler Type:** infrastructure
> **Created:** 2026-02-17
> **Due:** --
> **Completed:** 2026-02-17
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
| TASK-001 | Clarify adversarial template naming in SKILL.md Dependencies section | done | DEVELOPMENT | ps-architect |
| TASK-002 | Document agent vs template file distinction in PS and NSE agent dirs | done | DEVELOPMENT | ps-architect |
| TASK-003 | Add orchestration pattern reference to architecture-standards.md | N/A | REVIEW | -- |
| TASK-004 | Verify H-16 in quality-enforcement.md HARD Rule Index | N/A | REVIEW | -- |
| TASK-005 | Improve "When NOT to Use" guidance in adversary SKILL.md | N/A | REVIEW | -- |

---

## Progress Summary

### Status Overview

```
[####################] 100% (5/5 tasks — 2 done, 3 N/A)
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| Total Tasks | 5 |
| Completed | 2 |
| N/A | 3 |
| In Progress | 0 |
| Pending | 0 |
| Blocked | 0 |
| Completion | 100% |

---

## Acceptance Criteria

### Definition of Done

- [x] Adversary SKILL.md clarifies template naming and versioning
- [x] Agent directories have clear distinction between agent files and support files
- [x] architecture-standards.md references orchestration patterns (verified: already exists at line 122)
- [x] H-16 verified in quality-enforcement.md index (verified: present at lines 56, 96)
- [x] adversary SKILL.md "When to Use" section is comprehensive (verified: 6 bullets already solid)

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| TC-1 | Template naming clarification uses MEDIUM-tier language (SHOULD/RECOMMENDED) | [x] |
| TC-2 | Agent directory READMEs follow H-23/H-24 navigation requirements if over 30 lines | [x] (both under 30 lines — exempt) |
| TC-3 | Architecture-orchestration reference is consistent with existing standards format | [x] (N/A — already exists) |
| TC-4 | H-16 row in HARD Rule Index matches format of existing entries | [x] (N/A — already present) |
| TC-5 | Adversary SKILL.md guidance is actionable and consistent with skill table style | [x] (N/A — already comprehensive) |

---

## Evidence

### Deliverables

| # | Deliverable | Path | Status |
|---|-------------|------|--------|
| 1 | Template naming convention in adversary SKILL.md | `skills/adversary/SKILL.md` | Done |
| 2 | PS agents directory README | `skills/problem-solving/agents/README.md` | Done |
| 3 | NSE agents directory README | `skills/nasa-se/agents/README.md` | Done |
| 4 | Orchestration plan | `EN-929-documentation-cleanup/orchestration/en929-doccleanup-20260217-001/` | Done |

### Verification Checklist

- [x] All acceptance criteria verified — TASK-001: naming convention added. TASK-002: READMEs created. TASK-003: already exists (N/A). TASK-004: H-16 confirmed present (N/A). TASK-005: guidance already comprehensive (N/A).
- [x] All technical criteria verified — TC-1 through TC-5 all checked.
- [x] No regressions introduced
- [x] Changes consistent with existing documentation style

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
| 2026-02-17 | Claude | done | Orchestrated execution (en929-doccleanup-20260217-001). Phase 1 verify: TASK-001/002 applicable, TASK-003/004/005 N/A (already done or not needed). Phase 2: TASK-001 (naming convention added to SKILL.md Dependencies), TASK-002 (PS + NSE agent READMEs created). Phase 3: skipped (no C3 tasks applicable). |
