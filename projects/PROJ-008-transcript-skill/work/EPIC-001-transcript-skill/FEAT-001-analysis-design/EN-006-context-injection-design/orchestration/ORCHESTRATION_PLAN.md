# ORCHESTRATION_PLAN.md

> **Document ID:** EN-006-ORCH-PLAN
> **Project:** PROJ-008-transcript-skill
> **Workflow ID:** `en006-ctxinj-20260126-001`
> **Status:** ACTIVE
> **Version:** 2.0
> **Created:** 2026-01-26
> **Last Updated:** 2026-01-26

---

## 1. Executive Summary

Design the context injection mechanism that allows existing Jerry agents (ps-researcher, ps-analyst, ps-synthesizer) to be specialized for domain-specific transcript processing. This is an advanced feature enabling agent reuse without code duplication.

**Current State:** Not started - tasks defined, orchestration configured

**Orchestration Pattern:** Sequential Pipeline with Quality Gate

### 1.1 Workflow Identification

| Field | Value | Source |
|-------|-------|--------|
| Workflow ID | `en006-ctxinj-20260126-001` | auto |
| ID Format | `{purpose}-{YYYYMMDD}-{NNN}` | semantic-date-seq |
| Base Path | `EN-006-context-injection-design/` | Work tracker location |

**Artifact Output Locations:**
- Analysis: `docs/analysis/en006-5w2h-context-injection.md`
- Specification: `docs/specs/SPEC-context-injection.md`
- Design: `docs/design/en006-orchestration-integration.md`
- Examples: `docs/examples/context-injection/`

---

## 2. Workflow Architecture

### 2.1 Pipeline Diagram

```
EN-006 CONTEXT INJECTION DESIGN WORKFLOW
========================================

┌─────────────────────────────────────────────────────────────────────┐
│ PHASE 1: ANALYSIS                                                    │
│ ─────────────────────────────────────────────────────────────────── │
│ TASK-030: 5W2H Analysis (ps-analyst)                                │
│   • Who: Target user personas                                        │
│   • What: Mechanism definition                                       │
│   • When: Trigger conditions                                         │
│   • Where: Integration points                                        │
│   • Why: Value proposition                                           │
│   • How: Implementation approach                                     │
│   • How Much: Performance impact                                     │
│ STATUS: PENDING                                                      │
│ OUTPUT: docs/analysis/en006-5w2h-context-injection.md               │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│ PHASE 2: SPECIFICATION                                               │
│ ─────────────────────────────────────────────────────────────────── │
│ TASK-031: Context Injection Specification (ps-architect)            │
│   • Context payload schema (JSON Schema)                             │
│   • Injection points definition                                      │
│   • Prompt template mechanism                                        │
│   • Validation rules                                                 │
│   • Security constraints                                             │
│ STATUS: BLOCKED by TASK-030                                          │
│ OUTPUTS:                                                             │
│   • docs/specs/SPEC-context-injection.md                            │
│   • docs/specs/schemas/context-injection-schema.json                │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│ PHASE 3: INTEGRATION DESIGN                                          │
│ ─────────────────────────────────────────────────────────────────── │
│ TASK-032: Orchestration Integration Design (ps-architect)           │
│   • SKILL.md modification pattern                                    │
│   • ORCHESTRATION_PLAN.yaml schema extension                        │
│   • State tracking in ORCHESTRATION.yaml                            │
│   • Agent invocation interface                                       │
│   • Error propagation design                                         │
│ STATUS: BLOCKED by TASK-031                                          │
│ OUTPUT: docs/design/en006-orchestration-integration.md              │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│ PHASE 4: EXAMPLES & VALIDATION                                       │
│ ─────────────────────────────────────────────────────────────────── │
│ TASK-033: Example Orchestration Plans (ps-architect)                │
│   • 01-generic-baseline/ (no injection)                             │
│   • 02-legal-domain/                                                 │
│   • 03-sales-domain/                                                 │
│   • 04-engineering-domain/                                           │
│ STATUS: BLOCKED by TASK-032                                          │
│ OUTPUT: docs/examples/context-injection/                            │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│ PHASE 5: QUALITY REVIEW                                              │
│ ─────────────────────────────────────────────────────────────────── │
│ TASK-034: ps-critic Review & GATE-4 Preparation (ps-critic)         │
│   • Review all deliverables                                          │
│   • Calculate quality score (>= 0.90 required)                      │
│   • Verify traceability                                              │
│   • Prepare GATE-4 approval request                                  │
│ STATUS: BLOCKED by TASK-033                                          │
│ OUTPUT: FEAT-001--CRIT-EN006-review.md                              │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
╔═════════════════════════════════════════════════════════════════════╗
║ GATE-4: HUMAN APPROVAL                                               ║
║ ═══════════════════════════════════════════════════════════════════ ║
║ Decision Point: Approve EN-006 design for FEAT-002 implementation   ║
║ STATUS: PENDING                                                      ║
╚═════════════════════════════════════════════════════════════════════╝
```

### 2.2 Orchestration Pattern Classification

| Pattern | Applied | Description |
|---------|---------|-------------|
| Sequential | **Yes** | Tasks execute in dependency order |
| Concurrent | No | Single pipeline, no parallelism |
| Barrier Sync | No | No cross-pollination barriers |
| Hierarchical | **Yes** | Orchestrator delegates to ps-* agents |

---

## 3. Phase Definitions

### 3.1 Phase Details

| Phase | Name | Purpose | Agent | Effort | Status |
|-------|------|---------|-------|--------|--------|
| 1 | Analysis | 5W2H framework analysis | ps-analyst | 1 | PENDING |
| 2 | Specification | Formal spec creation | ps-architect | 2 | BLOCKED |
| 3 | Integration | Orchestration integration | ps-architect | 1 | BLOCKED |
| 4 | Examples | Working examples | ps-architect | 1 | BLOCKED |
| 5 | Review | Quality validation | ps-critic | 1 | BLOCKED |

**Total Effort:** 6 story points

---

## 4. Dependencies

### 4.1 External Dependencies

| Dependency | Description | Status |
|------------|-------------|--------|
| EN-003 | Requirements inform use cases | Complete |
| EN-004 | ADRs guide mechanism design | Complete |
| EN-005 | Agent designs for integration | Complete |

### 4.2 Internal Dependencies

```
TASK-030 ──────► TASK-031 ──────► TASK-032 ──────► TASK-033 ──────► TASK-034 ──────► GATE-4
   │                │                │                │                │
   │                │                │                │                │
   ▼                ▼                ▼                ▼                ▼
5W2H            Spec &           Integration       Examples         Review
Analysis        Schema           Design                             Score >= 0.90
```

---

## 5. Agent Registry

| Task ID | Agent | Role | Input | Output | Status |
|---------|-------|------|-------|--------|--------|
| TASK-030 | ps-analyst | Research & Analysis | EN-003 reqs, ADR-001 | 5W2H analysis doc | PENDING |
| TASK-031 | ps-architect | Specification | TASK-030 output | Spec + JSON Schema | BLOCKED |
| TASK-032 | ps-architect | Design | TASK-031 output | Integration design | BLOCKED |
| TASK-033 | ps-architect | Documentation | TASK-032 output | Example plans | BLOCKED |
| TASK-034 | ps-critic | Quality Review | All above outputs | Review + score | BLOCKED |

---

## 6. State Management

### 6.1 State Files

| File | Purpose |
|------|---------|
| `ORCHESTRATION.yaml` | Machine-readable state (SSOT) |
| `ORCHESTRATION_PLAN.md` | This file - strategic context |

### 6.2 Artifact Path Structure

```
EN-006-context-injection-design/
├── orchestration/
│   ├── ORCHESTRATION_PLAN.md           # Strategic context
│   └── ORCHESTRATION.yaml              # Machine-readable state
├── TASK-030-5w2h-analysis.md
├── TASK-031-context-injection-spec.md
├── TASK-032-orchestration-integration.md
├── TASK-033-example-plans.md
├── TASK-034-critic-review.md
└── EN-006-context-injection-design.md   # Enabler

Deliverables:
├── docs/analysis/en006-5w2h-context-injection.md
├── docs/specs/SPEC-context-injection.md
├── docs/specs/schemas/context-injection-schema.json
├── docs/design/en006-orchestration-integration.md
├── docs/examples/context-injection/
└── FEAT-001--CRIT-EN006-review.md
```

---

## 7. Execution Constraints

### 7.1 Hard Constraints (Jerry Constitution)

| Constraint | ID | Enforcement |
|------------|----|----|
| Single agent nesting | P-003 | Orchestrator → Worker only |
| File persistence | P-002 | All outputs to filesystem |
| No deception | P-022 | Transparent quality scoring |
| User authority | P-020 | Human approves GATE-4 |

### 7.2 Soft Constraints

| Constraint | Value | Rationale |
|------------|-------|-----------|
| Quality threshold | >= 0.90 | GATE-4 readiness |
| Max iterations | 2 | ps-critic feedback loops |

---

## 8. Success Criteria

### 8.1 Phase Exit Criteria

| Phase | Exit Criteria |
|-------|---------------|
| 1: Analysis | 5W2H doc complete with all 7 W's, L0/L1/L2 format |
| 2: Spec | JSON Schema validates, security review complete |
| 3: Integration | Mermaid diagrams render, P-003 verified |
| 4: Examples | 4+ examples validate against schema |
| 5: Review | Quality score >= 0.90 |

### 8.2 Workflow Completion Criteria

| Criterion | Validation |
|-----------|------------|
| All tasks complete | All 5 tasks status = DONE |
| All deliverables exist | All paths verified |
| Quality gate passed | Score >= 0.90 |
| GATE-4 approved | Human approval received |

---

## 9. Risk Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Scope expansion | Medium | Medium | Strict adherence to 5W2H scope |
| Schema complexity | Low | High | Start simple, iterate |
| Integration conflicts | Medium | Medium | Early SKILL.md validation |

---

## 10. Resumption Context

### 10.1 Current Execution State

```
WORKFLOW STATUS AS OF 2026-01-26
================================

Phase 1 (Analysis):    PENDING
Phase 2 (Spec):        BLOCKED by Phase 1
Phase 3 (Integration): BLOCKED by Phase 2
Phase 4 (Examples):    BLOCKED by Phase 3
Phase 5 (Review):      BLOCKED by Phase 4

GATE-4: PENDING (requires Phase 5 completion)
```

### 10.2 Next Actions

1. Execute TASK-030 (5W2H Analysis) using ps-analyst
2. Upon completion, unblock and execute TASK-031
3. Continue sequential execution through TASK-034
4. Request GATE-4 human approval

---

*Document ID: EN-006-ORCH-PLAN*
*Workflow ID: en006-ctxinj-20260126-001*
*Version: 2.0*
*Constitutional Compliance: P-002, P-003, P-020, P-022*
