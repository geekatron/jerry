# EN-204: Validation & Testing

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-01 (Claude)
PURPOSE: Validate the CLAUDE.md optimization achieves all targets
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** critical
> **Impact:** critical
> **Enabler Type:** compliance
> **Created:** 2026-02-01T00:00:00Z
> **Due:** 2026-02-12T00:00:00Z
> **Completed:** -
> **Parent:** FEAT-002
> **Owner:** -
> **Effort:** 5

---

## Summary

Validate that the CLAUDE.md optimization achieves all quantitative and qualitative targets. This includes token count verification, skill invocation testing, navigation pointer validation, and typical workflow testing.

**Technical Scope:**
- Fresh session baseline testing
- Context token count verification
- Skill invocation testing
- Navigation pointer validation
- Typical workflow testing
- Issue documentation

---

## Enabler Type Classification

**This Enabler Type:** COMPLIANCE (verification and validation)

---

## Problem Statement

Without thorough validation, we cannot confirm:
1. Token count reduction targets met
2. All skills load correctly
3. No broken references or missing content
4. Typical workflows remain functional

---

## Business Value

Validation ensures:
- Optimization targets verified before release
- No regression in functionality
- Issues identified and documented
- Confidence in OSS readiness

### Features Unlocked

- Verified OSS release readiness
- Documented quality metrics

---

## Technical Approach

Execute a comprehensive validation plan covering:

### Quantitative Validation

| Metric | Target | Validation Method |
|--------|--------|-------------------|
| CLAUDE.md lines | 60-80 | `wc -l CLAUDE.md` |
| Session start tokens | < 5,000 | Claude Code `/context` |
| Worktracker skill lines | 400+ | `wc -l skills/worktracker/rules/*.md` |

### Qualitative Validation

| Criterion | Validation |
|-----------|------------|
| Skill invocation | Manual test of /worktracker |
| Navigation pointers | Follow each pointer |
| Typical workflows | Create project, work items |

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Effort | Owner |
|----|-------|--------|--------|-------|
| [TASK-001](./TASK-001-fresh-session-baseline.md) | Start fresh Claude Code session for baseline | pending | 0.5 | - |
| [TASK-002](./TASK-002-verify-token-count.md) | Verify context token count at session start | pending | 1 | - |
| [TASK-003](./TASK-003-test-worktracker-skill.md) | Test /worktracker skill invocation | pending | 1 | - |
| [TASK-004](./TASK-004-test-navigation-pointers.md) | Test navigation pointers resolve | pending | 1 | - |
| [TASK-005](./TASK-005-test-typical-workflows.md) | Test typical workflows | pending | 1 | - |
| [TASK-006](./TASK-006-document-issues.md) | Document issues found | pending | 0.5 | - |

### Task Dependencies

```
TASK-001 (Fresh session)
    |
    +---> TASK-002 (Token count)
              |
              +---> TASK-003, TASK-004, TASK-005 (can run in parallel)
                        |
                        +---> TASK-006 (Document issues)
```

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   ENABLER PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Tasks:     [....................] 0% (0/6 completed)             |
| Effort:    [....................] 0% (0/5 points completed)      |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                             |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Tasks** | 6 |
| **Completed Tasks** | 0 |
| **Total Effort (points)** | 5 |
| **Completed Effort** | 0 |
| **Completion %** | 0% |

---

## Acceptance Criteria

### Definition of Done

- [ ] Session start tokens < 5,000
- [ ] All skills load correctly
- [ ] No broken references
- [ ] Typical workflows unchanged
- [ ] Issues documented and triaged

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| TC-1 | Token count verified | [ ] |
| TC-2 | /worktracker skill works | [ ] |
| TC-3 | All navigation pointers work | [ ] |
| TC-4 | Project creation workflow works | [ ] |
| TC-5 | Work item creation workflow works | [ ] |

---

## Test Scenarios

### TS-1: Fresh Session Test

Start new Claude Code session, verify token count at session start.

**Expected:** Context utilization < 50%

### TS-2: Skill Invocation Test

Invoke `/worktracker`, verify content loads.

**Expected:** All entity hierarchy and mapping information available

### TS-3: Navigation Test

Follow each pointer in CLAUDE.md, verify target exists.

**Expected:** All pointers resolve correctly

### TS-4: Workflow Test

Create project, create work items, complete typical tasks.

**Expected:** No regression from previous behavior

### TS-5: OSS Contributor Test

Simulate new contributor experience.

**Expected:** Understanding structure within 5 minutes

---

## Evidence

### Deliverables

| Deliverable | Type | Description | Link |
|-------------|------|-------------|------|
| Test Results | Documentation | Validation test results | (in task files) |
| Issue Log | Documentation | Issues found during validation | (TASK-006) |

### Validation Metrics

| Metric | Target | Actual | Pass |
|--------|--------|--------|------|
| Session tokens | < 5,000 | - | [ ] |
| Line count | 60-80 | - | [ ] |
| Skill load | Success | - | [ ] |
| Pointer resolution | 100% | - | [ ] |
| Workflow tests | Pass | - | [ ] |

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Undiscovered issues | Medium | Medium | Comprehensive test coverage |
| Workflow regressions | Low | High | Test all typical workflows |
| Token count miss | Low | Medium | Iterative refinement |

---

## Dependencies

### Depends On

- [EN-201: Worktracker Skill Extraction](../EN-201-worktracker-skill-extraction/EN-201-worktracker-skill-extraction.md)
- [EN-202: CLAUDE.md Rewrite](../EN-202-claude-md-rewrite/EN-202-claude-md-rewrite.md)
- [EN-203: TODO Section Migration](../EN-203-todo-section-migration/EN-203-todo-section-migration.md)

### Enables

- [EN-205: Documentation Update](../EN-205-documentation-update/EN-205-documentation-update.md)

---

## Related Items

### Hierarchy

- **Parent:** [FEAT-002: CLAUDE.md Optimization](../FEAT-002-claude-md-optimization.md)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-01T00:00:00Z | Claude | pending | Enabler created |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | PBI with ValueArea=Architectural |
| **SAFe** | Enabler (COMPLIANCE type) |
| **JIRA** | Story with 'enabler' label |
