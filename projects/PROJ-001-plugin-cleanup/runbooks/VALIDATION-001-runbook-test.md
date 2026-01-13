# Validation Test: RUNBOOK-001-008d Fresh Context Simulation

> **Document ID**: VALIDATION-001
> **Date**: 2026-01-09
> **Purpose**: Validate that RUNBOOK-001-008d enables multi-session work
> **Method**: Simulate fresh context, verify information sufficiency

---

## Test Methodology

### Scenario
Simulate a new Claude session that has:
- NO prior context from previous conversations
- ONLY access to filesystem
- Must identify current task and proceed

### Test Protocol
1. Read ONLY `WORKTRACKER.md` and `RUNBOOK-001-008d-domain-refactoring.md`
2. Verify all required information is present
3. Attempt to identify current task
4. Attempt to identify next action
5. Verify dependencies can be resolved
6. Document gaps

---

## Fresh Context Simulation

### Step 1: Read WORKTRACKER.md

**Questions an agent must answer**:

| Question | Found in WORKTRACKER? | Location |
|----------|----------------------|----------|
| What project is this? | ✅ YES | Header: "PROJ-001-plugin-cleanup" |
| What is the current phase? | ✅ YES | Current Focus: "Phase 6" |
| What is the active task? | ✅ YES | Current Focus: "ENFORCE-008d" |
| What is the active subtask? | ✅ YES | Current Focus: "008d.0 - Research" |
| What are the predecessors? | ✅ YES | Work Item Index |
| What are the successors? | ✅ YES | Work Item Index |
| Where is detailed breakdown? | ✅ YES | Navigation: "PHASE-06-ENFORCEMENT.md" |

**Verdict**: ✅ WORKTRACKER provides sufficient entry point

---

### Step 2: Read PHASE-06-ENFORCEMENT.md

**Questions an agent must answer**:

| Question | Found in PHASE-06? | Location |
|----------|-------------------|----------|
| What is R-008d.0? | ✅ YES | Section R-008d.0 |
| What inputs does R-008d.0 need? | ⚠️ PARTIAL | Lists artifacts but not full paths |
| What output does R-008d.0 produce? | ✅ YES | research/PROJ-001-R-008d-*.md |
| What are acceptance criteria? | ✅ YES | Acceptance Criteria section |
| What tests need to be written? | ✅ YES | BDD test tables |

**Gap Identified**: Full artifact paths for inputs not consistently listed.

---

### Step 3: Read RUNBOOK-001-008d

**Questions an agent must answer**:

| Question | Found in RUNBOOK? | Location |
|----------|------------------|----------|
| Pre-flight checks? | ✅ YES | Pre-Flight Checklist |
| Exact commands to run? | ✅ YES | Pre-Flight, Evidence Phase |
| Stage execution order? | ✅ YES | Stage Execution Order diagram |
| Inputs for each stage? | ✅ YES | Stage sections |
| Outputs for each stage? | ✅ YES | Stage sections |
| Commit checkpoints? | ✅ YES | Each stage has commit template |
| Resume protocol? | ✅ YES | Resume Protocol sections |
| Parallel safety analysis? | ✅ YES | Parallel Safety Analysis section |
| Troubleshooting? | ✅ YES | Troubleshooting section |

**Verdict**: ✅ RUNBOOK provides complete execution guidance

---

## Gap Analysis

### Critical Gaps (Would Block Execution)

| ID | Gap | Severity | Mitigation |
|----|-----|----------|------------|
| NONE | - | - | - |

### Minor Gaps (Could Cause Confusion)

| ID | Gap | Severity | Mitigation |
|----|-----|----------|------------|
| G-001 | PHASE-06 doesn't list full artifact paths for all inputs | LOW | RUNBOOK provides paths |
| G-002 | No explicit "how to invoke parallel sessions" guide | MEDIUM | Add to RUNBOOK |
| G-003 | No example of WORKTRACKER update after stage complete | LOW | RUNBOOK has commit templates |

---

## Parallel Execution Validation

### Can I-008d.2 and I-008d.3 truly run in parallel?

**Analysis**:

| File | I-008d.2 | I-008d.3 | Conflict? |
|------|----------|----------|-----------|
| `project_info.py` | MODIFY | READ (for session_id reference) | ⚠️ POTENTIAL |
| `session_id.py` | NONE | CREATE | NO |
| `session.py` | NONE | CREATE | NO |
| `test_project_info.py` | MODIFY | NONE | NO |
| `test_session*.py` | NONE | CREATE | NO |

**Conflict Detail**:
- I-008d.3.3 adds `last_session_id: SessionId` to ProjectInfo
- This MUST wait until I-008d.2 completes (ProjectInfo → EntityBase)
- I-008d.3.1 and I-008d.3.2 have NO conflict

**Parallel Safety Verdict**: ✅ SAFE with constraint documented

The RUNBOOK correctly identifies:
> "I-008d.3.3 (add session_id to ProjectInfo) MUST wait until I-008d.2 completes"

---

## Handoff Protocol Validation

### Test: Can a session resume from checkpoint?

**Scenario**: Session compacts after completing I-008d.1.1

**Expected State After I-008d.1.1**:
- Commit exists: `feat(session-mgmt): refactor ProjectId to extend VertexId`
- Tests pass: `test_project_id.py` (10 tests)
- WORKTRACKER updated: Active subtask = I-008d.1.2

**Resume Steps** (from RUNBOOK):
1. Read WORKTRACKER.md → Current Focus: I-008d.1.2
2. Run pre-flight checklist
3. Check git log → See I-008d.1.1 commit
4. Run pytest → Verify 10 new tests pass
5. Continue with I-008d.1.2

**Verdict**: ✅ Resume protocol is complete

---

## Evidence of Validation

### Test 1: Entry Point Discovery

Starting with ZERO context, reading `WORKTRACKER.md`:

```
Current Focus:
> Active Phase: Phase 6 (ENFORCE-008d)
> Active Task: ENFORCE-008d - Refactor to Unified Design
> Active Subtask: 008d.0 - Research & Analysis (5W1H)

Next Actions:
1. Complete 5W1H analysis for 008d
2. Perform Context7 research on DDD refactoring patterns
3. Document industry best practices with citations
4. Create research artifact: research/PROJ-001-R-008d-domain-refactoring.md
```

**Finding**: ✅ Clear entry point identified

### Test 2: Dependency Resolution

From WORKTRACKER Work Item Index:

```
| 008d.0 | Research & Analysis | 6.008d | 🔄 | Phase 7 | 008d.1 |
| 008d.1.1 | ProjectId → VertexId | 6.008d.1 | ⏳ | 008d.0 | 008d.1.2 |
```

**Finding**: ✅ Dependencies clearly stated (Predecessors/Successors columns)

### Test 3: Execution Guidance

From RUNBOOK Stage R:

```
### Tasks
| ID | Task | Status | Evidence |
|----|------|--------|----------|
| R.1 | Review ADR-013 implementation spec | ⏳ | Notes in output |
| R.2 | Analyze current ProjectId implementation | ⏳ | Current vs target table |
...
```

**Finding**: ✅ Step-by-step tasks with expected evidence

### Test 4: Commit Checkpoint

From RUNBOOK:

```bash
git commit -m "research(proj-001): complete R-008d.0 - domain refactoring analysis

- 5W1H analysis for ProjectId/ProjectInfo refactoring
- Context7 research with citations
...
```

**Finding**: ✅ Exact commit message templates provided

---

## Overall Validation Verdict

| Criteria | Status | Evidence |
|----------|--------|----------|
| Entry point discoverable | ✅ PASS | WORKTRACKER Current Focus |
| Dependencies resolvable | ✅ PASS | Work Item Index |
| Execution order clear | ✅ PASS | RUNBOOK stage diagram |
| Inputs/outputs specified | ✅ PASS | RUNBOOK stage sections |
| Resume protocol works | ✅ PASS | RUNBOOK resume sections |
| Parallel safety analyzed | ✅ PASS | RUNBOOK parallel section |
| Commit checkpoints defined | ✅ PASS | RUNBOOK commit templates |

**OVERALL VERDICT**: ✅ **VALIDATED - Ready for Multi-Session Execution**

---

## Recommendations

### Before Proceeding

1. **Add to RUNBOOK**: Instructions for starting parallel sessions
2. **Add to WORKTRACKER**: Link to RUNBOOK in "Next Actions"
3. **Create**: `runbooks/README.md` as index

### During Execution

1. Follow RUNBOOK strictly
2. Update WORKTRACKER after each commit checkpoint
3. If deviating from RUNBOOK, document why

---

## Validation Test Complete

| Field | Value |
|-------|-------|
| Tester | Claude Opus 4.5 |
| Date | 2026-01-09 |
| Result | ✅ PASS |
| Confidence | HIGH |
| Ready for Execution | YES |
