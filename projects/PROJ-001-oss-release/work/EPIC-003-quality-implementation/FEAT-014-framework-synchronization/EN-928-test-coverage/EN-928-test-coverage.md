# EN-928: Test Coverage Expansion

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-17 (Claude)
PURPOSE: Add test coverage for adversarial strategy templates and skill integration
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** medium
> **Impact:** medium
> **Enabler Type:** infrastructure
> **Created:** 2026-02-17
> **Due:** ---
> **Completed:** ---
> **Parent:** FEAT-014
> **Owner:** ---
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

Add test coverage for adversarial strategy templates and skill integration. Currently no tests validate that all 10 strategy templates exist, conform to TEMPLATE-FORMAT.md, or can be loaded by agents. Per H-21 (90% line coverage), test gaps undermine quality assurance.

**Technical Scope:**
- Create architecture tests for adversarial template structure validation
- Create integration tests for adversary skill file and agent reference validation
- Verify full test suite passes with H-21 compliance

---

## Problem Statement

The adversarial strategy templates created in FEAT-009 have no automated tests validating their structural integrity. Template format validation is only done manually. If a template is accidentally corrupted or a section is removed, there is no CI gate to catch it.

---

## Business Value

Automated template and skill validation tests are essential for maintaining the quality framework's integrity as the codebase evolves. Without these tests, regressions in the adversarial strategy templates would go undetected until a tournament execution fails, creating costly rework cycles.

### Features Unlocked

- Enables CI-gated protection of adversarial strategy templates against accidental corruption
- Provides automated validation of skill file structure and agent references

---

## Technical Approach

1. Create tests/architecture/test_adversarial_templates.py -- validate all 10 templates exist and match TEMPLATE-FORMAT.md structure
2. Create tests/integration/test_adversary_skill.py -- validate skill files, agent references, PLAYBOOK structure
3. Run full test suite to verify no regressions and coverage meets H-21

---

## Children (Tasks)

| ID | Title | Status | Activity | Agents |
|----|-------|--------|----------|--------|
| TASK-001 | Create test_adversarial_templates.py (template structure validation) | pending | DEVELOPMENT | ps-architect |
| TASK-002 | Create test_adversary_skill.py (skill integration validation) | pending | DEVELOPMENT | ps-architect |
| TASK-003 | Run full test suite and verify H-21 coverage | pending | TESTING | ps-critic |

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

- [ ] test_adversarial_templates.py validates all 10 templates against TEMPLATE-FORMAT.md
- [ ] test_adversary_skill.py validates skill files and agent references
- [ ] Full test suite passes with >= 90% line coverage (H-21)
- [ ] Tests integrated into CI pipeline

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| 1 | test_adversarial_templates.py exists in tests/architecture/ | [ ] |
| 2 | Test validates all 10 strategy templates exist | [ ] |
| 3 | Test validates template structure matches TEMPLATE-FORMAT.md | [ ] |
| 4 | test_adversary_skill.py exists in tests/integration/ | [ ] |
| 5 | Test validates skill files and agent references | [ ] |
| 6 | Test validates PLAYBOOK structure | [ ] |
| 7 | Full test suite passes with >= 90% line coverage | [ ] |

---

## Evidence

### Deliverables

| # | Deliverable | Path | Status |
|---|-------------|------|--------|
| 1 | --- | --- | Pending |

### Verification Checklist

- [ ] All acceptance criteria verified
- [ ] All technical criteria verified
- [ ] Quality gate score >= 0.92
- [ ] Creator-critic-revision cycle completed (minimum 3 iterations)
- [ ] No regressions introduced

---

## Dependencies

### Task Dependencies

TASK-001 and TASK-002 can run in parallel. TASK-003 depends on both TASK-001 and TASK-002 completing first.

```
TASK-001 (template tests) --+
                             +--> TASK-003 (full suite verification)
TASK-002 (skill tests) -----+
```

---

## Related Items

### Hierarchy
- **Parent Feature:** [FEAT-014: Framework Synchronization](../FEAT-014-framework-synchronization.md)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-17 | Claude | pending | Enabler created for FEAT-014 framework synchronization. |
