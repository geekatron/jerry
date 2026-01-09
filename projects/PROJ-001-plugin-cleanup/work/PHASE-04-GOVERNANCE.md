# Phase 4: Governance Updates

> **Status**: ✅ COMPLETED (100%)
> **Goal**: Update governance documents for project isolation

---

## Navigation

| Link | Description |
|------|-------------|
| [← WORKTRACKER](../WORKTRACKER.md) | Back to index |
| [← Phase 3](PHASE-03-AGENT-UPDATES.md) | Previous phase |
| [Phase 5 →](PHASE-05-VALIDATION.md) | Next phase |

---

## Task Summary

| Task ID | Title | Status | Subtasks | Files Changed |
|---------|-------|--------|----------|---------------|
| UPDATE-008 | Update JERRY_CONSTITUTION.md | ✅ DONE | 1/1 | `docs/governance/JERRY_CONSTITUTION.md` |
| UPDATE-009 | Update BEHAVIOR_TESTS.md | ✅ DONE | 1/1 | `docs/governance/BEHAVIOR_TESTS.md` |

---

## UPDATE-008: Update JERRY_CONSTITUTION.md ✅

> **Status**: COMPLETED
> **File**: `docs/governance/JERRY_CONSTITUTION.md`

### Subtasks

| ID | Task | Status | Change |
|----|------|--------|--------|
| 008.1 | Update P-010 Task Tracking Integrity reference | ✅ | Project-relative path |

### Changes Made

```markdown
# P-010: Task Tracking Integrity

## Before
Agents MUST update docs/WORKTRACKER.md when completing tasks.

## After
Agents MUST update projects/${JERRY_PROJECT}/WORKTRACKER.md when completing tasks.
```

### Principle P-010 Details

| Attribute | Value |
|-----------|-------|
| ID | P-010 |
| Name | Task Tracking Integrity |
| Enforcement | Medium |
| Description | Agents must keep WORKTRACKER up to date |

### Acceptance Criteria

- [x] P-010 reference updated
- [x] Path uses project convention
- [x] Constitution remains valid

---

## UPDATE-009: Update BEHAVIOR_TESTS.md ✅

> **Status**: COMPLETED
> **File**: `docs/governance/BEHAVIOR_TESTS.md`

### Subtasks

| ID | Task | Status | Change |
|----|------|--------|--------|
| 009.1 | Update BHV-010 test scenario paths | ✅ | Project-relative paths |

### Changes Made

```markdown
# BHV-010: Task Tracking Test

## Before
Given: Agent completes a task
When: Checking docs/WORKTRACKER.md
Then: Task is marked complete

## After
Given: Agent completes a task
When: Checking projects/${JERRY_PROJECT}/WORKTRACKER.md
Then: Task is marked complete
```

### BHV-010 Test Scenario

| Step | Description |
|------|-------------|
| Given | Agent has completed a task |
| When | WORKTRACKER is checked |
| Then | Task status is updated |
| And | Timestamp is current |

### Acceptance Criteria

- [x] BHV-010 paths updated
- [x] Test scenario remains valid
- [x] Can be evaluated by LLM-as-judge

---

## Governance Principles Affected

| Principle | Impact |
|-----------|--------|
| P-001 (Truth) | No change |
| P-002 (Persistence) | No change |
| P-010 (Task Tracking) | Path updated |
| P-020 (User Authority) | No change |
| P-022 (No Deception) | No change |

---

## Phase Completion Evidence

| File | Changes | Verification |
|------|---------|--------------|
| `docs/governance/JERRY_CONSTITUTION.md` | P-010 path | `grep 'WORKTRACKER' JERRY_CONSTITUTION.md` |
| `docs/governance/BEHAVIOR_TESTS.md` | BHV-010 path | Test scenario valid |

---

## Session Context

### For Resuming Work

If resuming after this phase:
1. Phase 4 is complete - no remaining work
2. Proceed to [Phase 5: Validation](PHASE-05-VALIDATION.md)
3. Governance now aligned with project isolation

### Key Changes to Know

| Document | Change |
|----------|--------|
| Constitution | P-010 uses project paths |
| Behavior Tests | BHV-010 uses project paths |

### Why Governance Updates Matter

Governance documents define agent behavior rules. Updating them ensures:
1. Agents know where to update WORKTRACKER
2. Behavior tests validate correct paths
3. Constitution enforcement is accurate

---

## Document History

| Date | Author | Changes |
|------|--------|---------|
| 2026-01-09 | Claude | Initial completion |
| 2026-01-09 | Claude | Added detailed task breakdowns |
