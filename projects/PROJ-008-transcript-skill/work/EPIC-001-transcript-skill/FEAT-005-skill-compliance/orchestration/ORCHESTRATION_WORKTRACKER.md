# ORCHESTRATION WORKTRACKER: FEAT-005 Skill Compliance

> **Workflow ID:** feat-005-compliance-20260130-001
> **Version:** 3.1.0
> **Status:** ACTIVE
> **Last Updated:** 2026-01-31T05:00:00Z
> **SSOT:** ORCHESTRATION.yaml
> **Adversarial Protocol:** Enabled (6 patterns configured)
> **Execution Mode:** Background for parallel tracks (DEC-003)

---

## Progress Dashboard

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                     FEAT-005 EXECUTION PROGRESS (v3.0)                       ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  PHASE 0: SEQUENTIAL HARD GATE (MUST COMPLETE FIRST)                        ║
║  ┌────────────────────────────────────────────────────────────────────────┐ ║
║  │ TASK-419 Model Validation: [....................] 0%  ⬜ READY         │ ║
║  │ Gate G-PHASE0: [ ] PENDING (Binary PASS/FAIL)                          │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
║  ═════════════ PARALLEL TRACKS BEGIN AFTER G-PHASE0 PASS ═════════════════  ║
║                                                                              ║
║  TRACK A: SEQUENTIAL COMPLIANCE CHAIN (33h)              🔒 BLOCKED         ║
║  ┌────────────────────────────────────────────────────────────────────────┐ ║
║  │ EN-027 Agent Defs:  [....................] 0% (0/7 tasks)  🔒 BLOCKED  │ ║
║  │ EN-028 SKILL.md:    [....................] 0% (0/5 tasks)  🔒 BLOCKED  │ ║
║  │ EN-029 Docs:        [....................] 0% (0/4 tasks)  🔒 BLOCKED  │ ║
║  │ EN-030 Polish:      [....................] 0% (0/3 tasks)  🔒 BLOCKED  │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
║  TRACK B: MODEL SELECTION (32h) - PARALLEL                 🔒 BLOCKED       ║
║  ┌────────────────────────────────────────────────────────────────────────┐ ║
║  │ EN-031 Phase 2:     [....................] 0% (0/4 tasks)  🔒 BLOCKED  │ ║
║  │ EN-031 Phase 3:     [....................] 0% (0/1 tasks)  🔒 BLOCKED  │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
║  QUALITY GATES                                                               ║
║  ┌────────────────────────────────────────────────────────────────────────┐ ║
║  │ G-PHASE0: [ ] P/F   G-027: [ ] -.--   G-028: [ ] -.--   G-029: [ ] -.--│ ║
║  │ G-030: [ ] -.--     G-031: [ ] -.--   G-FINAL: [ ] -.--                │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
║  OVERALL: [....................] 0%  (0/25 tasks, 0/7 gates)                ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## Dependency Visualization (v3.0 Corrected)

```
                    ╔═══════════════════════════════╗
                    ║      PHASE 0: HARD GATE       ║
                    ║  TASK-419 Model Validation    ║
                    ║  Effort: 2h | Gate: G-PHASE0  ║
                    ╚═══════════════╤═══════════════╝
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    │    PASS ──────┴────── FAIL    │
                    │      │               │        │
                    │      ▼               ▼        │
                    │  [UNBLOCK]     [HARD STOP]    │
                    │   Tracks      Escalate to     │
                    │   A & B         User          │
                    └───────────────────────────────┘
                                    │
                                 PASS?
                                    │
          ┌─────────────────────────┴─────────────────────────┐
          │                                                   │
          ▼                                                   ▼
    ╔═══════════════════════════════╗       ╔═══════════════════════════════╗
    ║     TRACK A: COMPLIANCE       ║       ║   TRACK B: MODEL SELECTION    ║
    ║ EN-027 → EN-028 → EN-029 →    ║       ║  EN-031 (Phases 2-3 only)     ║
    ║         EN-030                ║       ║  Phase 1 = TASK-419 (Phase 0) ║
    ║ Effort: 33h sequential        ║       ║  Effort: 32h parallel         ║
    ╚═══════════════════════════════╝       ╚═══════════════════════════════╝
          │                                                   │
          │    ┌─────────────────────────────────────────┐    │
          │    │      CROSS-POLLINATION POINTS           │    │
          │    ├─────────────────────────────────────────┤    │
          └────│ CP-1: Phase 0 → Track A (model param)   │────┘
               │ CP-2: EN-027 → TASK-422 (YAML patterns) │
               │ CP-3: TASK-420 → EN-028 (CLI design)    │
               └─────────────────────────────────────────┘
                                    │
                                    ▼
                    ╔═══════════════════════════════╗
                    ║       G-FINAL SYNTHESIS       ║
                    ║    All gates must pass ≥ 0.90 ║
                    ╚═══════════════════════════════╝
```

---

## Execution Mode (v3.1.0 - DEC-003)

**Key Insight:** Each Task agent gets its own context window. Background execution enables TRUE parallelism. Foreground would make parallel tracks impossible.

| Component | Execution Mode | Rationale |
|-----------|---------------|-----------|
| **Phase 0** (TASK-419) | Foreground | Blocking gate - must know PASS/FAIL before anything else |
| **Track A agents** | **Background** | Enable parallelism with Track B |
| **Track B agents** | **Background** | Enable parallelism with Track A |
| **ps-critic** | Foreground | Quick evaluation, simpler iterative refinement |

### Why Background for Tracks?

```
FOREGROUND (impossible parallelism):
─────────────────────────────────────────────────────────────────────────
Orchestrator: Spawn EN-027 → BLOCKED 10h → Returns → NOW spawn TASK-420
              Track B didn't start until Track A step 1 finished!
─────────────────────────────────────────────────────────────────────────

BACKGROUND (true parallelism):
─────────────────────────────────────────────────────────────────────────
Orchestrator: Spawn EN-027 (background) → output_file_A
              Spawn TASK-420 (background) → output_file_B
              Spawn TASK-421 (background) → output_file_C
              │
              └── ALL THREE running simultaneously in separate contexts!
─────────────────────────────────────────────────────────────────────────
```

### Orchestrator Protocol

1. **Spawn**: Use `Task` tool with `run_in_background: true`
2. **Track**: Store `output_file` paths for each agent
3. **Poll**: Use `TaskOutput` or `Read` to check completion
4. **Update**: Update YAML after each completion, BEFORE spawning dependents
5. **Coordinate**: Spawn consumers only after producers complete (CP dependencies)

### Day 1 Parallel Execution Example

```
09:00 - G-PHASE0 PASS (Phase 0 complete)
        │
09:05 - Orchestrator spawns parallel (all background):
        ├── Task(EN-027) → output_file_A
        ├── Task(TASK-420) → output_file_B
        └── Task(TASK-421) → output_file_C
        │
        └── Orchestrator NOT blocked, all three running!

14:00 - EN-027 complete
        ├── Update YAML: EN-027 COMPLETE
        ├── ps-critic G-027 (foreground) → PASS
        └── Spawn TASK-422 (has CP-2 data)

15:00 - TASK-420 complete
        ├── Update YAML: TASK-420 COMPLETE
        └── CP-3 ready for EN-028
```

---

## Phase 0: Sequential Hard Gate

### TASK-419: Validate Task Tool Model Parameter

**Status:** ⬜ READY | **Effort:** 2h | **Is Hard Gate:** YES

**Purpose:** Validate whether Claude Code's Task tool accepts a `model` parameter for agent spawning before any other work begins.

| Acceptance Criteria | Status | Evidence |
|---------------------|--------|----------|
| Confirm model parameter exists in Task tool schema | ⬜ PENDING | - |
| Test invocation with model: haiku | ⬜ PENDING | - |
| Test invocation with model: sonnet | ⬜ PENDING | - |
| Document exact parameter values that work | ⬜ PENDING | - |
| Document any limitations discovered | ⬜ PENDING | - |

**Quality Gate G-PHASE0:** ⬜ PENDING | Type: Binary PASS/FAIL

**Failure Protocol:**
```
IF TASK-419 FAILS:
1. DO NOT proceed with Track A or Track B
2. Document failure details in TASK-419.md
3. Escalate to user with options:
   - Option A: Investigate alternative model selection approaches
   - Option B: Descope EN-031 entirely
   - Option C: User-provided workaround
4. AWAIT user decision before continuing
```

**Cross-Pollination on Complete (CP-1):**
- **Trigger:** TASK-419 completion (PASS or FAIL)
- **Information:** Model parameter validation results, exact syntax, limitations
- **Target:** Track A (EN-027) - inform agent definition schema
- **Artifact:** `EN-031-model-selection-capability/TASK-419-validate-task-model.md`

---

## Track A: Sequential Compliance Chain

**Status:** 🔒 BLOCKED by Phase 0 (G-PHASE0)

### EN-027: Agent Definition Compliance

**Status:** 🔒 BLOCKED by G-PHASE0 | **Effort:** 10h | **Progress:** 0/7 tasks

| Task ID | Title | Effort | Status | Notes |
|---------|-------|--------|--------|-------|
| TASK-400 | Add identity section | 1h | 🔒 BLOCKED | Add to all 5 agents |
| TASK-401 | Add capabilities section | 1.5h | 🔒 BLOCKED | allowed_tools, forbidden_actions |
| TASK-402 | Add guardrails section | 3h | 🔒 BLOCKED | input_validation, output_filtering |
| TASK-403 | Add validation section | 2h | 🔒 BLOCKED | post_completion_checks |
| TASK-404 | Add constitution section | 1h | 🔒 BLOCKED | principles_applied |
| TASK-405 | Add session_context section | 1h | 🔒 BLOCKED | schema, on_receive, on_send |
| TASK-406 | Validate agent compliance | 0.5h | 🔒 BLOCKED | Checklist A-001 to A-043 |

**Quality Gate G-027:** 🔒 BLOCKED | Threshold: 0.90 | Score: -.-

**Receives from Phase 0 (CP-1):** Model parameter validation results to inform agent definition schema for model overrides.

**Sends to Track B (CP-2):** Agent YAML schema patterns for model override capability (triggers TASK-422).

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

**Receives from Track B (CP-3):** CLI parameter design (--model-* flags) to document in SKILL.md.

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

## Track B: Model Selection (Parallel with Track A after Phase 0)

**Status:** 🔒 BLOCKED by Phase 0 (G-PHASE0)

### EN-031: Model Selection Capability

**Status:** 🔒 BLOCKED by G-PHASE0 | **Effort:** 32h | **Progress:** 0/5 tasks (Phase 1 is now Phase 0)

**Note:** EN-031 Phase 1 (TASK-419) has been promoted to Phase 0 as the sequential hard gate. Phases 2-3 remain as Track B, parallel with Track A.

#### Phase 2: Implementation (24h) - PARALLEL with Track A

| Task ID | Title | Effort | Status | Notes |
|---------|-------|--------|--------|-------|
| TASK-420 | Add CLI model params | 8h | 🔒 BLOCKED | --model-* flags |
| TASK-421 | Update SKILL.md docs | 4h | 🔒 BLOCKED | Model configuration |
| TASK-422 | Update agent definitions | 4h | 🔒 BLOCKED | Model override capability |
| TASK-423 | Implement profiles | 8h | 🔒 BLOCKED | economy/balanced/quality |

**Cross-Pollination:**
- **Receives (CP-2):** Agent YAML patterns from EN-027 for TASK-422
- **Sends (CP-3):** CLI parameter design from TASK-420 to EN-028 SKILL.md

#### Phase 3: Testing (8h) - AFTER Phase 2

| Task ID | Title | Effort | Status | Notes |
|---------|-------|--------|--------|-------|
| TASK-424 | Integration testing | 8h | 🔒 BLOCKED | Different model combos |

**Quality Gate G-031:** 🔒 BLOCKED | Threshold: 0.90 | Score: -.-

---

## Cross-Pollination Status (v3.0 Detailed)

| ID | Trigger | From | To | Status | Information Transferred |
|----|---------|------|-----|--------|------------------------|
| CP-1 | TASK-419 complete | Phase 0 | Track A (EN-027) | ⬜ PENDING | Model parameter validation results, exact syntax, limitations |
| CP-2 | G-027 PASS | Track A (EN-027) | Track B (TASK-422) | 🔒 BLOCKED | Agent YAML schema patterns for model override |
| CP-3 | TASK-420 complete | Track B | Track A (EN-028) | 🔒 BLOCKED | CLI parameter design (--model-* flags) |

### CP Flow Diagram

```
Phase 0                Track A                    Track B
────────               ───────                    ───────
TASK-419 ─────CP-1────► EN-027 ─────CP-2────────► TASK-422
    │                     │                           │
    │                     ▼                           │
    │                  EN-028 ◄────CP-3──────── TASK-420
    │                     │                           │
    │                     ▼                           │
    │                  EN-029                    TASK-423
    │                     │                           │
    │                     ▼                           │
    │                  EN-030                    TASK-424
    │                     │                           │
    └─────────────────────┴───────────────────────────┘
                          │
                          ▼
                      G-FINAL
```

---

## Quality Gate Summary (v3.0 with Phase 0)

| Gate | Scope | Type | Threshold | Score | Iteration | Status | Last Critique |
|------|-------|------|-----------|-------|-----------|--------|---------------|
| **G-PHASE0** | TASK-419 | Binary | PASS/FAIL | - | N/A | ⬜ PENDING | - |
| G-027 | EN-027 | Score | 0.90 | -.-- | 0/3 | 🔒 BLOCKED | - |
| G-028 | EN-028 | Score | 0.90 | -.-- | 0/3 | 🔒 BLOCKED | - |
| G-029 | EN-029 | Score | 0.90 | -.-- | 0/3 | 🔒 BLOCKED | - |
| G-030 | EN-030 | Score | 0.95 | -.-- | 0/3 | 🔒 BLOCKED | - |
| G-031 | EN-031 | Score | 0.90 | -.-- | 0/3 | 🔒 BLOCKED | - |
| G-FINAL | All | Score | 0.90 | -.-- | 0/3 | 🔒 BLOCKED | - |

### Adversarial Feedback Loop Protocol

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  FEEDBACK LOOP: Implementer → ps-critic → Refine (max 3 iterations)         │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  PHASE 0 (G-PHASE0): Binary PASS/FAIL - no iterations                       │
│    - PASS: Unblock Track A and Track B                                      │
│    - FAIL: HARD STOP - escalate to user                                     │
│                                                                              │
│  ALL OTHER GATES (G-027 through G-FINAL): Score-based with iterations       │
│    1. Complete enabler tasks                                                 │
│    2. Submit to ps-critic for evaluation against checklist                   │
│    3. IF score >= threshold: PASS → proceed to next enabler                 │
│    4. IF score < threshold AND iteration < 3: REFINE → address findings     │
│    5. IF iteration >= 3: ESCALATE → user decision required                  │
│                                                                              │
│  Critique artifacts: orchestration/critiques/{gate-id}-iteration-{n}.md     │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Critique Artifact Log

| Gate | Iteration | Score | Findings | Critique Path | Timestamp |
|------|-----------|-------|----------|---------------|-----------|
| - | - | - | - | - | - |

*No critiques generated yet*

---

## Metrics (v3.0)

| Metric | Current | Target |
|--------|---------|--------|
| Tasks Complete | 0/25 | 25/25 |
| Phase 0 Complete | 0/1 | 1/1 |
| Enablers Complete | 0/5 | 5/5 |
| Quality Gates Passed | 0/7 | 7/7 |
| Effort Complete | 0h | 67h |
| Compliance Score | 52% | >= 95% |
| Estimated Days Remaining | 6 | 0 |

---

## Execution Timeline (v3.0)

```
Day 0: Phase 0 - TASK-419 (2h)
       │
       ├── PASS? ──► Days 1-6: Parallel Tracks
       │
       └── FAIL? ──► HARD STOP - User Decision Required

Days 1-6 (if Phase 0 PASS):
┌─────────────────────────────────────────────────────────────┐
│ Track A (Sequential):                                       │
│   Day 1: EN-027 (10h)  ──► G-027                           │
│   Day 2-3: EN-028 (9h) ──► G-028                           │
│   Day 4-5: EN-029 (9h) ──► G-029                           │
│   Day 6: EN-030 (5h)   ──► G-030                           │
├─────────────────────────────────────────────────────────────┤
│ Track B (Parallel):                                         │
│   Days 1-4: Phase 2 (24h) - TASK-420, 421, 422, 423        │
│   Days 5-6: Phase 3 (8h)  - TASK-424 ──► G-031             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                        G-FINAL Synthesis
```

---

## Execution Log

| Timestamp | Event | Details |
|-----------|-------|---------|
| 2026-01-30T23:00:00Z | WORKFLOW_CREATED | v2.0 aligned with existing task files |
| 2026-01-31T00:30:00Z | FEEDBACK_LOOP_ADDED | v2.1 - Adversarial critic feedback loop with iteration tracking |
| 2026-01-31T02:00:00Z | DISC-003_CREATED | v2.2 - Identified dependency chain flaw |
| 2026-01-31T03:30:00Z | DEC-002_DOCUMENTED | v3.0 design decisions documented |
| 2026-01-31T04:00:00Z | v3.0_RELEASED | Corrected dependency chain - Phase 0 as sequential hard gate |
| 2026-01-31T05:00:00Z | **DEC-003_ACCEPTED** | v3.1 - Background execution for parallel tracks (true parallelism) |

---

## Next Actions (v3.0)

**CRITICAL: Phase 0 must complete first**

### Day 0: Phase 0 Execution

1. **Execute TASK-419** (Model Parameter Validation)
   - Test Task tool with `model: haiku`
   - Test Task tool with `model: sonnet`
   - Document results and limitations
   - Determine PASS/FAIL for G-PHASE0

2. **IF G-PHASE0 PASS:**
   - Update TASK-419 status to ✅ COMPLETE
   - Unblock Track A (EN-027) and Track B (EN-031 Phases 2-3)
   - Execute CP-1 (transfer validation results to Track A)
   - Proceed to Day 1

3. **IF G-PHASE0 FAIL:**
   - Document failure in TASK-419.md
   - HARD STOP all work
   - Escalate to user with decision options
   - AWAIT user decision

---

## Legend

| Symbol | Meaning |
|--------|---------|
| ⬜ | PENDING - Ready to start |
| 🔄 | IN_PROGRESS - Currently executing |
| ✅ | COMPLETE - Successfully finished |
| ❌ | FAILED - Needs attention |
| 🔒 | BLOCKED - Waiting on dependency |
| ⚠️ | ESCALATED - Max iterations reached or hard gate failed |

---

## Related Documents

| Document | Purpose | Path |
|----------|---------|------|
| DISC-003 | Dependency chain flaw discovery | `FEAT-005--DISC-003-orchestration-dependency-chain-flaw.md` |
| DEC-002 | v3.0 design decisions | `FEAT-005--DEC-002-orchestration-v3-design-decisions.md` |
| DEC-003 | Background execution decision | `FEAT-005--DEC-003-background-execution-for-parallelism.md` |
| ORCHESTRATION_PLAN.md | v3.1 strategic plan | `orchestration/ORCHESTRATION_PLAN.md` |
| ORCHESTRATION.yaml | v3.1 machine-readable SSOT | `orchestration/ORCHESTRATION.yaml` |

---

*Worktracker Version: 3.1.0*
*Last Updated: 2026-01-31T05:00:00Z*
*Change: v3.1 - Background execution for parallel tracks per DEC-003 (true parallelism enabled)*
