# ORCHESTRATION WORKTRACKER: FEAT-005 Skill Compliance

> **Workflow ID:** feat-005-compliance-20260130-001
> **Version:** 2.0.0
> **Status:** ACTIVE
> **Last Updated:** 2026-01-30T23:00:00Z
> **SSOT:** ORCHESTRATION.yaml

---

## Progress Dashboard

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                     FEAT-005 EXECUTION PROGRESS                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  TRACK A: SEQUENTIAL COMPLIANCE CHAIN (33h)                                  ║
║  ┌────────────────────────────────────────────────────────────────────────┐ ║
║  │ EN-027 Agent Defs:  [....................] 0% (0/7 tasks)  ⬜ READY    │ ║
║  │ EN-028 SKILL.md:    [....................] 0% (0/5 tasks)  🔒 BLOCKED  │ ║
║  │ EN-029 Docs:        [....................] 0% (0/4 tasks)  🔒 BLOCKED  │ ║
║  │ EN-030 Polish:      [....................] 0% (0/3 tasks)  🔒 BLOCKED  │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
║  TRACK B: MODEL SELECTION (34h) - PARALLEL                                   ║
║  ┌────────────────────────────────────────────────────────────────────────┐ ║
║  │ EN-031 Phase 1:     [....................] 0% (0/1 tasks)  ⬜ READY    │ ║
║  │ EN-031 Phase 2:     [....................] 0% (0/4 tasks)  🔒 BLOCKED  │ ║
║  │ EN-031 Phase 3:     [....................] 0% (0/1 tasks)  🔒 BLOCKED  │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
║  QUALITY GATES                                                               ║
║  ┌────────────────────────────────────────────────────────────────────────┐ ║
║  │ G-027: [ ] -.--   G-028: [ ] -.--   G-029: [ ] -.--   G-030: [ ] -.-- │ ║
║  │ G-031: [ ] -.--   G-FINAL: [ ] -.--                                   │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
║  OVERALL: [....................] 0%  (0/25 tasks, 0/6 gates)                ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## Track A: Sequential Compliance Chain

### EN-027: Agent Definition Compliance

**Status:** ⬜ READY | **Effort:** 10h | **Progress:** 0/7 tasks

| Task ID | Title | Effort | Status | Notes |
|---------|-------|--------|--------|-------|
| TASK-400 | Add identity section | 1h | ⬜ PENDING | Add to all 5 agents |
| TASK-401 | Add capabilities section | 1.5h | ⬜ PENDING | allowed_tools, forbidden_actions |
| TASK-402 | Add guardrails section | 3h | ⬜ PENDING | input_validation, output_filtering |
| TASK-403 | Add validation section | 2h | ⬜ PENDING | post_completion_checks |
| TASK-404 | Add constitution section | 1h | ⬜ PENDING | principles_applied |
| TASK-405 | Add session_context section | 1h | ⬜ PENDING | schema, on_receive, on_send |
| TASK-406 | Validate agent compliance | 0.5h | ⬜ PENDING | Checklist A-001 to A-043 |

**Quality Gate G-027:** ⬜ PENDING | Threshold: 0.90 | Score: -.-

---

### EN-028: SKILL.md Compliance

**Status:** 🔒 BLOCKED by EN-027 | **Effort:** 9h | **Progress:** 0/5 tasks

| Task ID | Title | Effort | Status | Notes |
|---------|-------|--------|--------|-------|
| TASK-407 | Add invoking section | 1h | 🔒 BLOCKED | 3 methods documented |
| TASK-408 | Enhance state passing | 2h | 🔒 BLOCKED | session_context schema |
| TASK-409 | Add persistence section | 1h | 🔒 BLOCKED | P-002 requirements |
| TASK-410 | Add self-critique | 1h | 🔒 BLOCKED | 5+ checklist items |
| TASK-411 | Restructure persona/output | 2h | 🔒 BLOCKED | Move to top-level |

**Quality Gate G-028:** 🔒 BLOCKED | Threshold: 0.90 | Score: -.-

---

### EN-029: Documentation Compliance

**Status:** 🔒 BLOCKED by EN-028 | **Effort:** 9h | **Progress:** 0/4 tasks

| Task ID | Title | Effort | Status | Notes |
|---------|-------|--------|--------|-------|
| TASK-412 | Add L2 architect section | 3h | 🔒 BLOCKED | PLAYBOOK.md |
| TASK-413 | Create anti-patterns | 3h | 🔒 BLOCKED | 4+ anti-patterns |
| TASK-414 | Declare pattern refs | 2h | 🔒 BLOCKED | PAT-xxx declarations |
| TASK-415 | Add constraints section | 1h | 🔒 BLOCKED | Violation consequences |

**Quality Gate G-029:** 🔒 BLOCKED | Threshold: 0.90 | Score: -.-

---

### EN-030: Documentation Polish

**Status:** 🔒 BLOCKED by EN-029 | **Effort:** 5h | **Progress:** 0/3 tasks

| Task ID | Title | Effort | Status | Notes |
|---------|-------|--------|--------|-------|
| TASK-416 | Add tool examples | 2h | 🔒 BLOCKED | Concrete invocations |
| TASK-417 | Add design rationale | 2h | 🔒 BLOCKED | RUNBOOK.md |
| TASK-418 | Add cross-skill refs | 1h | 🔒 BLOCKED | Integration examples |

**Quality Gate G-030:** 🔒 BLOCKED | Threshold: 0.95 | Score: -.-

---

## Track B: Model Selection (Parallel)

### EN-031: Model Selection Capability

**Status:** ⬜ READY (Phase 1) | **Effort:** 34h | **Progress:** 0/6 tasks

#### Phase 1: Validation (2h)

| Task ID | Title | Effort | Status | Notes |
|---------|-------|--------|--------|-------|
| TASK-419 | Validate Task tool model | 2h | ⬜ PENDING | **CRITICAL** - Early validation |

#### Phase 2: Implementation (24h)

| Task ID | Title | Effort | Status | Notes |
|---------|-------|--------|--------|-------|
| TASK-420 | Add CLI model params | 8h | 🔒 BLOCKED | --model-* flags |
| TASK-421 | Update SKILL.md docs | 4h | 🔒 BLOCKED | Model configuration |
| TASK-422 | Update agent definitions | 4h | 🔒 BLOCKED | Model override capability |
| TASK-423 | Implement profiles | 8h | 🔒 BLOCKED | economy/balanced/quality |

#### Phase 3: Testing (8h)

| Task ID | Title | Effort | Status | Notes |
|---------|-------|--------|--------|-------|
| TASK-424 | Integration testing | 8h | 🔒 BLOCKED | Different model combos |

**Quality Gate G-031:** ⬜ PENDING | Threshold: 0.90 | Score: -.-

---

## Cross-Pollination Status

| ID | Trigger | From | To | Status |
|----|---------|------|-----|--------|
| CP-1 | TASK-419 complete | Track B | Track A | ⬜ PENDING |
| CP-2 | EN-027 complete | Track A | Track B | ⬜ PENDING |
| CP-3 | TASK-420 complete | Track B | Track A | ⬜ PENDING |

---

## Quality Gate Summary

| Gate | Enabler | Threshold | Score | Status |
|------|---------|-----------|-------|--------|
| G-027 | EN-027 | 0.90 | -.-- | ⬜ PENDING |
| G-028 | EN-028 | 0.90 | -.-- | 🔒 BLOCKED |
| G-029 | EN-029 | 0.90 | -.-- | 🔒 BLOCKED |
| G-030 | EN-030 | 0.95 | -.-- | 🔒 BLOCKED |
| G-031 | EN-031 | 0.90 | -.-- | ⬜ PENDING |
| G-FINAL | All | 0.90 | -.-- | 🔒 BLOCKED |

---

## Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Tasks Complete | 0/25 | 25/25 |
| Enablers Complete | 0/5 | 5/5 |
| Quality Gates Passed | 0/6 | 6/6 |
| Effort Complete | 0h | 67h |
| Compliance Score | 52% | >= 95% |
| Estimated Days Remaining | 6 | 0 |

---

## Execution Log

| Timestamp | Event | Details |
|-----------|-------|---------|
| 2026-01-30T23:00:00Z | WORKFLOW_CREATED | v2.0 aligned with existing task files |

---

## Next Actions

**Immediate (can start now):**

1. **Track A:** Start TASK-400 (Add identity section to all 5 agents)
2. **Track B:** Start TASK-419 (Validate Task tool model parameter)

Both tracks can execute in parallel from day 1.

---

## Legend

| Symbol | Meaning |
|--------|---------|
| ⬜ | PENDING - Ready to start |
| 🔄 | IN_PROGRESS - Currently executing |
| ✅ | COMPLETE - Successfully finished |
| ❌ | FAILED - Needs attention |
| 🔒 | BLOCKED - Waiting on dependency |

---

*Worktracker Version: 2.0.0*
*Last Updated: 2026-01-30T23:00:00Z*
