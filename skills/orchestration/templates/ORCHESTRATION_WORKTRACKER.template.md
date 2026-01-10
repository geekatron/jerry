# ORCHESTRATION_WORKTRACKER.md

> **Document ID:** {PROJECT_ID}-ORCH-TRACKER
> **Project:** {PROJECT_ID}
> **Workflow:** {WORKFLOW_NAME}
> **Status:** {STATUS}
> **Version:** 1.0
> **Created:** {CREATED_DATE}
> **Last Updated:** {UPDATED_DATE}

---

## 1. Execution Dashboard

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                        ORCHESTRATION EXECUTION STATUS                          ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  PIPELINE A                              PIPELINE B                           ║
║  ══════════                              ══════════                           ║
║  Phase 1: ████████████ 100% ✅            Phase 1: ████████████ 100% ✅        ║
║  Phase 2: ░░░░░░░░░░░░   0% ⏳            Phase 2: ░░░░░░░░░░░░   0% ⏳        ║
║                                                                               ║
║  SYNC BARRIERS                                                                ║
║  ═════════════                                                                ║
║  Barrier 1: ████████████ COMPLETE ✅                                          ║
║  Barrier 2: ░░░░░░░░░░░░ PENDING ⏳                                           ║
║                                                                               ║
║  Overall Progress: ██████░░░░░░ 50%                                           ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

## 2. Phase Execution Log

### 2.1 PHASE 1 - {STATUS}

#### Pipeline A Phase 1: {NAME}

| Agent | Status | Started | Completed | Artifacts | Notes |
|-------|--------|---------|-----------|-----------|-------|
| {agent-id} | {STATUS} | {date} | {date} | {artifact.md} | {notes} |

**Phase 1 Artifacts:**
- [ ] `{path/to/artifact1.md}`
- [ ] `{path/to/artifact2.md}`

#### Pipeline B Phase 1: {NAME}

| Agent | Status | Started | Completed | Artifacts | Notes |
|-------|--------|---------|-----------|-----------|-------|
| {agent-id} | {STATUS} | {date} | {date} | {artifact.md} | {notes} |

---

### 2.2 BARRIER 1 - {STATUS}

| Direction | Artifact | Status | Key Content |
|-----------|----------|--------|-------------|
| a→b | {artifact-name.md} | {STATUS} | {summary} |
| b→a | {artifact-name.md} | {STATUS} | {summary} |

**Barrier 1 Artifacts:**
- [ ] `{path/to/cross-pollination/barrier-1/a-to-b/artifact.md}`
- [ ] `{path/to/cross-pollination/barrier-1/b-to-a/artifact.md}`

---

### 2.3 PHASE 2 - {STATUS}

{Repeat pattern for each phase}

---

## 3. Agent Execution Queue

### 3.1 Current Queue (Priority Order)

| Priority | Agent | Pipeline | Phase | Dependencies | Status |
|----------|-------|----------|-------|--------------|--------|
| 1 | {agent-id} | {pipeline} | {phase} | {dependencies} | {STATUS} |
| 2 | {agent-id} | {pipeline} | {phase} | {dependencies} | {STATUS} |

### 3.2 Execution Groups

```
GROUP 1 (Parallel):
  ┌─────────────────────────────────────────────────────────────┐
  │ agent-a-001 ─┬─ agent-a-002                                 │
  │              │                                              │
  │ agent-b-001 ─┴─ agent-b-002                                 │
  └─────────────────────────────────────────────────────────────┘
                              ▼
GROUP 2 (Sequential - Barrier):
  ┌─────────────────────────────────────────────────────────────┐
  │ a→b cross-pollination │ b→a cross-pollination               │
  └─────────────────────────────────────────────────────────────┘
```

---

## 4. Blockers and Issues

### 4.1 Active Blockers

| ID | Description | Blocking | Severity | Owner | Resolution |
|----|-------------|----------|----------|-------|------------|
| {id} | {description} | {what-blocked} | {L/M/H} | {owner} | {status} |

### 4.2 Resolved Issues

| ID | Description | Resolution | Resolved |
|----|-------------|------------|----------|
| {id} | {description} | {how-resolved} | {date} |

---

## 5. Checkpoints

### 5.1 Checkpoint Log

| ID | Timestamp | Trigger | State | Recovery Point |
|----|-----------|---------|-------|----------------|
| CP-001 | {ISO-8601} | {trigger} | {state-summary} | {recovery-point} |

### 5.2 Next Checkpoint Target

**{CP-ID}: {Name}**
- Trigger: {What triggers this checkpoint}
- Expected Artifacts: {List of expected artifacts}
- Recovery Point: {What can be recovered from here}

---

## 6. Metrics

### 6.1 Execution Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Phases Complete | {n}/{total} | {target} | {emoji} |
| Barriers Complete | {n}/{total} | {target} | {emoji} |
| Agents Executed | {n}/{total} | {target} | {emoji} |
| Artifacts Created | {n}/{total} | {target} | {emoji} |

### 6.2 Quality Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Agent Success Rate | {%} | >95% | {emoji} |
| Barrier Validation Pass | {%} | 100% | {emoji} |

---

## 7. Execution Notes

### 7.1 Session Log

| Timestamp | Event | Details |
|-----------|-------|---------|
| {ISO-8601} | {event-type} | {details} |

### 7.2 Lessons Learned

| ID | Lesson | Application |
|----|--------|-------------|
| LL-001 | {lesson} | {how-to-apply} |

---

## 8. Next Actions

### 8.1 Immediate

1. [ ] {Action 1}
2. [ ] {Action 2}
3. [ ] {Action 3}

### 8.2 Subsequent

{N}. [ ] {Action N}

---

## 9. Resumption Context

### 9.1 For Next Session

```
RESUMPTION CHECKLIST
====================

1. Read ORCHESTRATION_PLAN.md for strategic context
2. Read this ORCHESTRATION_WORKTRACKER.md for execution state
3. Read ORCHESTRATION.yaml for machine-readable state
4. Check "Next Actions" section for pending work
5. Verify no new blockers in "Blockers and Issues"
6. Continue from "Agent Execution Queue" priority order
```

### 9.2 Cross-Session Portability

All paths in this document are repository-relative. No ephemeral references.
Any Claude session (CLI, Web, other machines) can resume work.

---

*Document ID: {PROJECT_ID}-ORCH-TRACKER*
*Version: 1.0*
*Last Checkpoint: {CP-ID}*
