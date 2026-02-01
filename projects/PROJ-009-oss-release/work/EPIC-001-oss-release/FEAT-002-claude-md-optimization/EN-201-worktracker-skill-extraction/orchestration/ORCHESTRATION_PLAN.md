# ORCHESTRATION_PLAN.md - EN-201 Worktracker Skill Extraction

> **Document ID:** EN-201-ORCH-PLAN
> **Project:** PROJ-009-oss-release
> **Workflow ID:** `en201-extraction-20260201-001`
> **Status:** ACTIVE
> **Version:** 1.0
> **Created:** 2026-02-01
> **Last Updated:** 2026-02-01

---

## 1. Executive Summary

This orchestration plan coordinates the parallel extraction of worktracker content from CLAUDE.md into modular rule files, with adversarial quality review loops ensuring 0.92+ quality threshold before integration.

**Problem:** CLAUDE.md contains 371 lines of worktracker content loaded at every session start, contributing to context rot.

**Solution:** Extract content to 4 modular rule files in `skills/worktracker/rules/`, loaded on-demand via `/worktracker` skill invocation.

**Current State:** TASK-001 complete (SKILL.md fixed). Ready to execute parallel extraction with quality gates.

**Orchestration Pattern:** Fan-Out/Fan-In with Generator-Critic Review Loops

### 1.1 Workflow Identification

| Field | Value | Source |
|-------|-------|--------|
| Workflow ID | `en201-extraction-20260201-001` | auto |
| ID Format | `{enabler}-{purpose}-{YYYYMMDD}-{NNN}` | semantic-date-seq |
| Base Path | `EN-201-worktracker-skill-extraction/orchestration/` | Enabler-scoped |

**Artifact Output Locations:**
- Extraction artifacts: `skills/worktracker/rules/`
- Critique artifacts: `orchestration/critiques/`
- QA artifacts: `orchestration/qa/`

---

## 2. Workflow Architecture

### 2.1 Pipeline Diagram

```
                         EN-201 ORCHESTRATION WORKFLOW
                         =============================
                              Quality Gate: 0.92
                            Max Iterations: 3/task

┌─────────────────────────────────────────────────────────────────────────────┐
│                        PHASE 1: CONTENT EXTRACTION (Fan-Out)                │
│                              Execution Mode: PARALLEL                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  │    TASK-002      │  │    TASK-003      │  │    TASK-004      │  │    TASK-005      │
│  │ Entity Hierarchy │  │ System Mappings  │  │  Behavior Rules  │  │ Directory Struct │
│  │     (~80 LOC)    │  │    (~120 LOC)    │  │     (~60 LOC)    │  │    (~111 LOC)    │
│  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘
│           │                     │                     │                     │
│           ▼                     ▼                     ▼                     ▼
│  ┌──────────────────────────────────────────────────────────────────────────────────┐
│  │                    GENERATOR-CRITIC LOOP (per task)                              │
│  │  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │  │                                                                             │ │
│  │  │     ┌─────────────┐         ┌─────────────┐         ┌─────────────┐        │ │
│  │  │     │  GENERATOR  │────────►│  ps-critic  │────────►│  Score ≥    │        │ │
│  │  │     │ (Extraction)│         │  (Evaluate) │         │   0.92?     │        │ │
│  │  │     └─────────────┘         └─────────────┘         └──────┬──────┘        │ │
│  │  │           ▲                                                │               │ │
│  │  │           │                                         NO     │   YES         │ │
│  │  │           │              ┌─────────────────────────────────┴───────┐       │ │
│  │  │           │              │                                         │       │ │
│  │  │           │              ▼                                         ▼       │ │
│  │  │           │     ┌─────────────────┐                      ┌─────────────┐   │ │
│  │  │           │     │ Iteration < 3?  │                      │   ACCEPT    │   │ │
│  │  │           │     └────────┬────────┘                      │  (Pass Gate)│   │ │
│  │  │           │              │                               └─────────────┘   │ │
│  │  │           │       YES    │    NO                                           │ │
│  │  │           │              ▼                                                 │ │
│  │  │           │     ┌─────────────────┐                                        │ │
│  │  │           └─────│  Revise with    │                                        │ │
│  │  │                 │  Feedback       │                                        │ │
│  │  │                 └─────────────────┘                                        │ │
│  │  │                          │ NO (iter ≥ 3)                                   │ │
│  │  │                          ▼                                                 │ │
│  │  │                 ┌─────────────────┐                                        │ │
│  │  │                 │ ESCALATE TO     │                                        │ │
│  │  │                 │ HUMAN REVIEW    │                                        │ │
│  │  │                 └─────────────────┘                                        │ │
│  │  └─────────────────────────────────────────────────────────────────────────────┘ │
│  └──────────────────────────────────────────────────────────────────────────────────┘
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
    ╔═════════════════════════════════════════════════════════════════════════╗
    ║                         SYNC BARRIER 1                                   ║
    ║  ┌───────────────────────────────────────────────────────────────────┐  ║
    ║  │ Condition: All 4 extractions ≥ 0.92 quality OR human-approved     │  ║
    ║  │ Artifacts: 4 rule files in skills/worktracker/rules/              │  ║
    ║  └───────────────────────────────────────────────────────────────────┘  ║
    ║  STATUS: PENDING                                                         ║
    ╚═════════════════════════════════════════════════════════════════════════╝
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                     PHASE 2: INTEGRATION REVIEW                              │
│                         Execution Mode: SEQUENTIAL                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                           nse-qa                                       │  │
│  │                    Integration Quality Audit                           │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │  │
│  │  │ Validates:                                                       │  │  │
│  │  │ • Complete content migration (no information loss)               │  │  │
│  │  │ • Consistent formatting across all 4 rule files                  │  │  │
│  │  │ • Cross-references between files are valid                       │  │  │
│  │  │ • Total extracted lines ≈ 371 (matching source)                  │  │  │
│  │  │ • Template compliance for each rule file                         │  │  │
│  │  └─────────────────────────────────────────────────────────────────┘  │  │
│  │                                                                       │  │
│  │  Quality Threshold: 0.92 | Max Iterations: 3 | Escalate: Human       │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
    ╔═════════════════════════════════════════════════════════════════════════╗
    ║                         SYNC BARRIER 2                                   ║
    ║  ┌───────────────────────────────────────────────────────────────────┐  ║
    ║  │ Condition: Integration review ≥ 0.92 OR human-approved            │  ║
    ║  │ Artifacts: QA report in orchestration/qa/                         │  ║
    ║  └───────────────────────────────────────────────────────────────────┘  ║
    ║  STATUS: PENDING                                                         ║
    ╚═════════════════════════════════════════════════════════════════════════╝
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PHASE 3: NAVIGATION & VALIDATION                          │
│                         Execution Mode: SEQUENTIAL                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────────────┐       ┌──────────────────────────┐           │
│  │       TASK-006           │──────►│       TASK-007           │           │
│  │ Update SKILL.md          │       │ Validate Skill Loading   │           │
│  │ Navigation Pointers      │       │ End-to-End Test          │           │
│  └──────────────────────────┘       └──────────────────────────┘           │
│                                                                             │
│  ps-critic review loop for each task (0.92 threshold)                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
                         ┌────────────────────────┐
                         │     EN-201 COMPLETE    │
                         │  All 7 Tasks Done      │
                         │  Enable EN-202, EN-203 │
                         └────────────────────────┘
```

### 2.2 Orchestration Pattern Classification

| Pattern | Applied | Description |
|---------|---------|-------------|
| Sequential | Yes | Phases execute in order (1→2→3) |
| Concurrent | Yes | Tasks 002-005 run in parallel within Phase 1 |
| Barrier Sync | Yes | Cross-pollination at barriers |
| Generator-Critic | Yes | Adversarial review loops per task |
| Fan-Out/Fan-In | Yes | Parallel extraction, integration review |

---

## 3. Phase Definitions

### 3.1 Phase 1: Content Extraction (Parallel)

| Task | Name | Source Content | Target File | LOC | Status |
|------|------|----------------|-------------|-----|--------|
| TASK-002 | Entity Hierarchy | CLAUDE.md §1.1-1.2 | `worktracker-entity-hierarchy.md` | ~80 | PENDING |
| TASK-003 | System Mappings | CLAUDE.md §3-4 | `worktracker-system-mappings.md` | ~120 | PENDING |
| TASK-004 | Behavior Rules | CLAUDE.md §Behavior | `worktracker-behavior-rules.md` | ~60 | PENDING |
| TASK-005 | Directory Structure | CLAUDE.md §Dir Struct | `worktracker-directory-structure.md` | ~111 | PENDING |

### 3.2 Phase 2: Integration Review

| Agent | Purpose | Input | Output | Status |
|-------|---------|-------|--------|--------|
| nse-qa | Integration audit | 4 rule files | QA report | PENDING |

### 3.3 Phase 3: Navigation & Validation

| Task | Name | Depends On | Status |
|------|------|------------|--------|
| TASK-006 | Update SKILL.md navigation | Phase 2 complete | BLOCKED |
| TASK-007 | Validate skill loading | TASK-006 complete | BLOCKED |

---

## 4. Agent Selection Rationale

### 4.1 Generator-Critic Pattern (Task-Level Review)

| Role | Agent | Rationale |
|------|-------|-----------|
| Generator | Main Context (Claude) | Content extraction is straightforward; no specialized agent needed |
| Critic | **ps-critic** | Purpose-built for iterative quality evaluation with scores |

**Why ps-critic over nse-qa for task-level review:**
- ps-critic: Designed for iterative generator-critic loops with quality scores
- nse-qa: Designed for artifact compliance validation (NASA standards)
- Task-level extraction benefits from iterative refinement (ps-critic's specialty)

### 4.2 Integration Review (Batch Review)

| Role | Agent | Rationale |
|------|-------|-----------|
| Integration Auditor | **nse-qa** | Validates all 4 files together for completeness, consistency, compliance |

**Why nse-qa for integration review:**
- Checklist-based validation against defined criteria
- Compliance scoring (pass/fail with percentages)
- Designed for artifact validation (work product quality)
- Can verify traceability (all source content accounted for)

### 4.3 Agent Capability Matrix

| Agent | Quality Score | Iterative Loop | Compliance Check | Traceability | Best For |
|-------|--------------|----------------|------------------|--------------|----------|
| ps-critic | 0.0-1.0 | ✅ Native | ❌ | ❌ | Per-task refinement |
| nse-qa | % score | ❌ | ✅ Native | ✅ | Batch validation |
| ps-reviewer | Severity | ❌ | ❌ | ❌ | Code/design review |
| nse-reviewer | Gate | ❌ | ✅ | ✅ | Technical reviews (SRR/PDR) |

---

## 5. Quality Criteria

### 5.1 Task-Level Evaluation Criteria (ps-critic)

| Criterion | Weight | Description | 0.92+ Threshold |
|-----------|--------|-------------|-----------------|
| Completeness | 0.30 | All source content extracted | No missing sections |
| Accuracy | 0.25 | Content matches source exactly | Zero content drift |
| Structure | 0.20 | Proper markdown formatting | Valid headers, tables, code blocks |
| Clarity | 0.15 | Clear and understandable | No ambiguous language |
| Integration | 0.10 | Works with existing rules | No conflicts with existing files |

**Quality Score Formula:** `Σ(criterion_score × criterion_weight)`

### 5.2 Integration Evaluation Criteria (nse-qa)

| Check ID | Criterion | Pass Condition |
|----------|-----------|----------------|
| INT-001 | Complete Migration | All 371 lines accounted for |
| INT-002 | No Information Loss | Diff shows no missing content |
| INT-003 | Consistent Formatting | Same style across all 4 files |
| INT-004 | Cross-References Valid | All internal links work |
| INT-005 | Template Compliance | Each file follows rules template |
| INT-006 | No Duplication | Content not duplicated across files |

---

## 6. Feedback Loop Protocol

### 6.1 Generator-Critic Loop (per task)

```
ITERATION PROTOCOL
==================

1. GENERATE
   - Extract content from CLAUDE.md
   - Create/update rule file
   - Document extraction mapping

2. CRITIQUE (ps-critic)
   - Evaluate against 5 criteria
   - Calculate weighted quality score
   - Identify specific improvement areas
   - Provide actionable feedback

3. DECISION
   IF score >= 0.92:
       → ACCEPT (proceed to barrier)
   ELIF iteration < 3:
       → REVISE (apply feedback, iterate)
   ELSE:
       → ESCALATE (human review required)

4. FEEDBACK UPSTREAM
   - Specific gaps identified
   - Evidence from source/target
   - Concrete revision instructions
   - Expected score improvement
```

### 6.2 Escalation Protocol

```
HUMAN ESCALATION (after 3 iterations)
=====================================

When: Quality score < 0.92 after 3 iterations

Actions:
1. Document iteration history with scores
2. Summarize blocking issues
3. Present to user with options:
   a) Accept with documented caveats
   b) Provide specific guidance for revision
   c) Take over manual editing
4. User decision recorded in orchestration state

Artifact: orchestration/escalations/TASK-{N}-escalation.md
```

---

## 7. Sync Barrier Protocol

### 7.1 Barrier 1: Phase 1 → Phase 2 Transition

```
BARRIER 1 CHECKLIST
===================

PRE-BARRIER (all must be true):
□ TASK-002 quality ≥ 0.92 OR human-approved
□ TASK-003 quality ≥ 0.92 OR human-approved
□ TASK-004 quality ≥ 0.92 OR human-approved
□ TASK-005 quality ≥ 0.92 OR human-approved
□ All 4 rule files exist in skills/worktracker/rules/
□ No blocking issues open

TRANSITION:
□ Create Phase 1 completion checkpoint
□ Aggregate quality scores for Phase 2 input
□ Update ORCHESTRATION.yaml status

POST-BARRIER:
□ Phase 2 (nse-qa) unblocked
□ Integration review can begin
```

### 7.2 Barrier 2: Phase 2 → Phase 3 Transition

```
BARRIER 2 CHECKLIST
===================

PRE-BARRIER:
□ nse-qa compliance ≥ 92% OR human-approved
□ No critical findings in QA report
□ All major findings addressed or accepted

TRANSITION:
□ Create Phase 2 completion checkpoint
□ Document QA findings summary
□ Update ORCHESTRATION.yaml status

POST-BARRIER:
□ TASK-006 unblocked
□ Navigation update can begin
```

---

## 8. State Files

| File | Purpose | Location |
|------|---------|----------|
| `ORCHESTRATION_PLAN.md` | Strategic context (this file) | `orchestration/` |
| `ORCHESTRATION.yaml` | Machine-readable state (SSOT) | `orchestration/` |
| `ORCHESTRATION_WORKTRACKER.md` | Tactical execution tracking | `orchestration/` |

### 8.1 Artifact Locations

```
EN-201-worktracker-skill-extraction/
├── orchestration/
│   ├── ORCHESTRATION_PLAN.md          # This file
│   ├── ORCHESTRATION.yaml             # Machine state
│   ├── ORCHESTRATION_WORKTRACKER.md   # Execution tracking
│   ├── critiques/                     # ps-critic outputs
│   │   ├── task-002-iter1-critique.md
│   │   ├── task-002-iter2-critique.md
│   │   └── ...
│   ├── qa/                            # nse-qa outputs
│   │   └── integration-qa-report.md
│   └── escalations/                   # Human escalation docs
│       └── (if needed)
└── ...
```

---

## 9. Execution Constraints

### 9.1 Hard Constraints (Jerry Constitution)

| Constraint | ID | Enforcement |
|------------|----|----|
| Single agent nesting | P-003 | Orchestrator → Worker only |
| File persistence | P-002 | All state to filesystem |
| No deception | P-022 | Transparent quality scores |
| User authority | P-020 | User approves escalations |

### 9.2 Workflow Constraints

| Constraint | Value | Rationale |
|------------|-------|-----------|
| Quality threshold | 0.92 | High bar for content extraction accuracy |
| Max iterations | 3 | Circuit breaker to prevent infinite loops |
| Max concurrent tasks | 4 | All Phase 1 tasks can run in parallel |
| Checkpoint frequency | PHASE | Recovery at phase boundaries |

---

## 10. Risk Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Content loss during extraction | Low | High | ps-critic validates completeness; nse-qa cross-checks |
| Quality threshold too strict | Medium | Medium | Human escalation path; threshold can be adjusted |
| Iteration loop stuck | Low | Medium | 3-iteration circuit breaker; human escalation |
| Agent hallucination | Low | Medium | Evidence-based critique; source comparison |
| Inconsistent formatting | Medium | Low | nse-qa integration check; template compliance |

---

## 11. Success Criteria

### 11.1 Phase Completion Criteria

| Phase | Criterion | Validation |
|-------|-----------|------------|
| Phase 1 | All 4 extractions ≥ 0.92 | ps-critic quality scores |
| Phase 2 | Integration review ≥ 92% | nse-qa compliance score |
| Phase 3 | Navigation works, skill loads | Manual verification |

### 11.2 Workflow Completion Criteria

| Criterion | Validation |
|-----------|------------|
| All 7 tasks complete | Task status = DONE |
| All barriers passed | Barrier status = COMPLETE |
| 371 lines migrated | Line count comparison |
| Skill loads correctly | `/worktracker` invocation test |
| EN-202, EN-203 unblocked | Dependency resolution |

---

## 12. Resumption Context

### 12.1 Current Execution State

```
WORKFLOW STATUS AS OF 2026-02-01
================================

Phase 1 (Content Extraction):
  TASK-002: PENDING
  TASK-003: PENDING
  TASK-004: PENDING
  TASK-005: PENDING

Phase 2 (Integration Review):
  nse-qa: BLOCKED (waiting Phase 1)

Phase 3 (Navigation & Validation):
  TASK-006: BLOCKED (waiting Phase 2)
  TASK-007: BLOCKED (waiting TASK-006)

Barriers:
  Barrier 1: PENDING
  Barrier 2: PENDING
```

### 12.2 Next Actions

1. Execute TASK-002 through TASK-005 in parallel
2. For each task: generate → ps-critic → iterate until ≥0.92
3. Upon all Phase 1 complete: pass Barrier 1
4. Execute nse-qa integration review
5. Continue to Phase 3

---

*Document ID: EN-201-ORCH-PLAN*
*Workflow ID: en201-extraction-20260201-001*
*Version: 1.0*
*Cross-Session Portable: All paths are repository-relative*
