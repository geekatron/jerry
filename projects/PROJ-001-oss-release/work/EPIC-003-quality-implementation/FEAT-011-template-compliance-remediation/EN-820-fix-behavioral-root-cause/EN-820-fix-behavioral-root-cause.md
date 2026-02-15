# EN-820: Fix Behavioral Root Cause

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** critical
> **Impact:** critical
> **Enabler Type:** infrastructure
> **Created:** 2026-02-15
> **Parent:** FEAT-011
> **Effort:** 3

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and technical scope |
| [Problem Statement](#problem-statement) | Why this enabler is needed |
| [Business Value](#business-value) | How enabler supports feature delivery |
| [Technical Approach](#technical-approach) | High-level technical approach |
| [Children (Tasks)](#children-tasks) | Task inventory and tracking |
| [Progress Summary](#progress-summary) | Overall enabler progress |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Evidence](#evidence) | Deliverables and verification |
| [Risks and Mitigations](#risks-and-mitigations) | Known risks and mitigations |
| [Dependencies](#dependencies) | Dependencies and items enabled |
| [Related Items](#related-items) | Hierarchy and related work |
| [History](#history) | Status changes and key events |

---

## Summary

Fix the 4 behavioral gaps causing worktracker template non-compliance. The primary root cause is that `worktracker-templates.md` is not `@`-imported in SKILL.md, so its CRITICAL template usage rules never reach agent context.

**Technical Scope:**
- Add `@rules/worktracker-templates.md` import to SKILL.md
- Add WTI-007 (Mandatory Template Usage) rule to behavior-rules.md
- Add template compliance reference to orchestration SKILL.md
- Add template reference to orchestration plan template

---

## Problem Statement

Template rules exist but are never loaded. The `@` import mechanism is the only auto-loading path for rules into agent context. Since only `worktracker-behavior-rules.md` is imported in the worktracker SKILL.md, all template compliance instructions in `worktracker-templates.md` are dead rules -- they exist on disk but never reach the agent during /worktracker invocation.

This means every entity file created by the worktracker skill is produced without awareness of the canonical template structure, leading to systemic non-compliance across EPIC, FEATURE, ENABLER, and TASK files.

---

## Business Value

Prevents future template non-compliance. All entity files created after this fix will follow canonical templates because the rules will be loaded into agent context at skill invocation time.

### Features Unlocked

- Reliable template compliance for all worktracker entity files
- Automated template validation potential (consistent structure enables tooling)

---

## Technical Approach

1. **Add `@rules/worktracker-templates.md` to SKILL.md imports** -- Single line addition after the existing `@rules/worktracker-behavior-rules.md` import. This is the primary fix that closes the root cause.
2. **Add WTI-007 section to behavior-rules.md** -- Defines procedural steps for mandatory template usage with entity-to-template mapping and anti-pattern warnings.
3. **Add template compliance row to orchestration SKILL.md** -- Ensures orchestration workflows reference worktracker templates in their Constitutional Compliance table.
4. **Add template reference note to ORCHESTRATION_PLAN.template.md** -- Ensures orchestration plan documents remind implementers to use canonical templates.

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Activity | Agents |
|----|-------|--------|----------|--------|
| TASK-001 | Add @import for worktracker-templates.md to SKILL.md | BACKLOG | DEVELOPMENT | ps-architect |
| TASK-002 | Add WTI-007 Mandatory Template Usage to behavior-rules.md | BACKLOG | DEVELOPMENT | ps-architect |
| TASK-003 | Add template compliance to orchestration SKILL.md | BACKLOG | DEVELOPMENT | ps-architect |
| TASK-004 | Add template reference to orchestration plan template | BACKLOG | DEVELOPMENT | ps-architect |

### Task Dependencies

TASK-001 and TASK-002 are parallel (foundation fixes). TASK-003 and TASK-004 are parallel (orchestration integration). No strict ordering between the two groups, but conceptually the foundation fixes should precede orchestration integration.

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   ENABLER PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Tasks:     [....................] 0% (0/4 completed)              |
| Effort:    [....................] 0% (0/3 points completed)       |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                               |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Tasks** | 4 |
| **Completed Tasks** | 0 |
| **Total Effort (points)** | 3 |
| **Completed Effort** | 0 |
| **Completion %** | 0% |

---

## Acceptance Criteria

### Definition of Done

- [ ] `@rules/worktracker-templates.md` is imported in SKILL.md
- [ ] WTI-007 rule is defined with procedural steps
- [ ] Orchestration skill references worktracker templates
- [ ] Creator-critic-revision cycle completed (min 3 iterations, >= 0.92)

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| TC-1 | SKILL.md loads worktracker-templates.md via `@` import | [ ] |
| TC-2 | WTI-007 specifies Read-template-first procedure | [ ] |
| TC-3 | Orchestration plan template includes worktracker template reference | [ ] |

---

## Evidence

### Deliverables

| Deliverable | Type | Description | Link |
|-------------|------|-------------|------|
| -- | -- | Unpopulated (pending status) | -- |

### Technical Verification

| Criterion | Verification Method | Evidence | Verified By | Date |
|-----------|---------------------|----------|-------------|------|
| TC-1 | Inspect SKILL.md imports | -- | -- | -- |
| TC-2 | Inspect behavior-rules.md WTI-007 | -- | -- | -- |
| TC-3 | Inspect orchestration plan template | -- | -- | -- |

### Verification Checklist

- [ ] All acceptance criteria verified
- [ ] All tasks completed
- [ ] Technical review complete
- [ ] Documentation updated

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Context token budget exceeded by adding second @import | Low | Medium | worktracker-templates.md is concise; measure token impact |
| WTI-007 rule conflicts with existing WTI rules | Low | Low | Review existing rules for overlap before adding |

---

## Dependencies

### Depends On

- DISC-001 (root cause analysis findings)

### Enables

- EN-821 (EPIC & FEATURE remediation)
- EN-822 (Enabler remediation)
- EN-823 (Task remediation)

---

## Related Items

### Hierarchy

- **Parent:** FEAT-011

### Related Items

- **Related Discovery:** DISC-001 (root cause analysis -- Gap 1-4 findings)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-15 | Claude | pending | Enabler created. Source: DISC-001 Gap 1-4. |
