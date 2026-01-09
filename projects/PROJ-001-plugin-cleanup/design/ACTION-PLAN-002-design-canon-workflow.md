# Action Plan: Design Canon & Shared Kernel Workflow

> **Document ID**: ACTION-PLAN-002
> **Date**: 2026-01-10
> **Updated**: 2026-01-09
> **Project**: PROJ-001-plugin-cleanup
> **Phase**: Phase 7 - Design Document Synthesis (Final Stage)
> **Pattern**: Full Decision Workflow (Pattern 5) with Iterative Refinement
> **Predecessor**: ACTION-PLAN-001 (Tiers 1-6 COMPLETED)
> **Status**: ✅ APPROVED

---

## Executive Summary

ACTION-PLAN-001 successfully executed Tiers 1-6, producing artifacts e-001 through e-010. This plan completes Phase 7 by executing the **Full Decision Workflow** pattern with **Iterative Refinement** to:

1. Create the authoritative **Jerry Design Canon v1.0**
2. Produce the **Shared Kernel Implementation Guide**
3. Validate completeness
4. Generate completion report
5. **Iterate until validator reports no issues**

Upon completion, **Phase 6 (Project Enforcement)** will be unblocked.

---

## Iterative Refinement Protocol

### Key Principles

1. **Versioned Artifacts**: Each artifact is versioned (e.g., `e-011-v1`, `e-011-v2`)
2. **Stopping Condition**: Continue cycles until `ps-validator` reports **no issues**
3. **Commit Strategy**: Commit after **each stage** within cycles to enable resume

### Cycle Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              CYCLE N                                             │
│                                                                                  │
│  ps-synthesizer → ps-analyst → ps-architect → ps-validator → ps-reporter        │
│       │               │             │              │              │              │
│       ▼               ▼             ▼              ▼              ▼              │
│   e-011-vN       e-012-vN      e-013-vN       e-014-vN       e-015-vN           │
│                                                    │                             │
│                                          ┌────────┴────────┐                     │
│                                          │  Issues Found?  │                     │
│                                          └────────┬────────┘                     │
│                                                   │                              │
│                              ┌────────────────────┼────────────────────┐         │
│                              │ YES                │ NO                 │         │
│                              ▼                    ▼                    │         │
│                         CYCLE N+1            PHASE 7 COMPLETE          │         │
│                     (feed e-014-vN            (exit loop)              │         │
│                      back to Stage 1)                                  │         │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Refinement Inputs per Cycle

| Stage | Cycle 1 Input | Cycle N (N>1) Additional Input |
|-------|---------------|-------------------------------|
| ps-synthesizer | e-001→e-006 | + e-011-v(N-1) + e-014-v(N-1) validation feedback |
| ps-analyst | e-011-vN + src/ | + e-012-v(N-1) prior analysis |
| ps-architect | e-011-vN + e-012-vN | + e-013-v(N-1) prior ADR |
| ps-validator | e-011-vN + e-013-vN | Validates current version |
| ps-reporter | All artifacts | Full artifact chain + delta from prior cycle |

---

## Current State

### Completed Artifacts (ACTION-PLAN-001 Output)

| Entry ID | Type | Path | Status |
|----------|------|------|--------|
| e-001 | Research | `research/PROJ-001-e-001-worktracker-proposal-extraction.md` | ✅ |
| e-002 | Research | `research/PROJ-001-e-002-plan-graph-model.md` | ✅ |
| e-003 | Research | `research/PROJ-001-e-003-revised-architecture-foundation.md` | ✅ |
| e-004 | Research | `research/PROJ-001-e-004-strategic-plan-v3.md` | ✅ |
| e-005 | Research | `research/PROJ-001-e-005-industry-best-practices.md` | ✅ |
| e-006 | Synthesis | `synthesis/PROJ-001-e-006-unified-architecture-canon.md` | ✅ |
| e-007 | Analysis | `analysis/PROJ-001-e-007-implementation-gap-analysis.md` | ✅ |
| e-009 | Analysis | `analysis/PROJ-001-e-009-alignment-validation.md` | ✅ |
| e-010 | Report | `reports/PROJ-001-e-010-synthesis-status-report.md` | ✅ |

### Pending Tasks

| Task ID | Description | Blocker |
|---------|-------------|---------|
| SYNTH-003 | Design Canon Creation | None |
| SYNTH-004 | Shared Kernel Implementation Guide | SYNTH-003 |
| ENFORCE-008d | Refactor to Unified Design | SYNTH-004 |

---

## Full Decision Workflow (Pattern 5)

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ ps-synthesizer│ →  │  ps-analyst  │ →   │ ps-architect │ →   │ ps-validator │ →   │ ps-reporter  │
│              │     │              │     │              │     │              │     │              │
│ SYNTH-003    │     │ Gap Analysis │     │ SYNTH-004    │     │ Validation   │     │ Completion   │
│ Design Canon │     │ Canon vs Impl│     │ Shared Kernel│     │ Completeness │     │ Report       │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
       │                    │                    │                    │                    │
       ▼                    ▼                    ▼                    ▼                    ▼
    e-011               e-012                e-013                e-014                e-015
```

---

## Stage 1: Synthesis (ps-synthesizer)

### Task: SYNTH-003 - Jerry Design Canon

**Agent**: `ps-synthesizer`

**PS Context**:
```
PS ID: PROJ-001
Entry ID: e-011-vN (where N = cycle number)
Topic: Jerry Design Canon
```

**Input Artifacts (Cycle 1)**:
```
projects/PROJ-001-plugin-cleanup/research/PROJ-001-e-001-worktracker-proposal-extraction.md
projects/PROJ-001-plugin-cleanup/research/PROJ-001-e-002-plan-graph-model.md
projects/PROJ-001-plugin-cleanup/research/PROJ-001-e-003-revised-architecture-foundation.md
projects/PROJ-001-plugin-cleanup/research/PROJ-001-e-004-strategic-plan-v3.md
projects/PROJ-001-plugin-cleanup/research/PROJ-001-e-005-industry-best-practices.md
projects/PROJ-001-plugin-cleanup/synthesis/PROJ-001-e-006-unified-architecture-canon.md
```

**Additional Input (Cycle N, N>1)**:
```
projects/PROJ-001-plugin-cleanup/synthesis/PROJ-001-e-011-v{N-1}-jerry-design-canon.md (prior version)
projects/PROJ-001-plugin-cleanup/analysis/PROJ-001-e-014-v{N-1}-canon-validation.md (validation feedback)
```

**Output**: `projects/PROJ-001-plugin-cleanup/synthesis/PROJ-001-e-011-vN-jerry-design-canon.md`

**Objective**:
Create the **authoritative** Jerry Design Canon that:
1. **Consolidates** all extracted patterns into canonical definitions
2. **Establishes** binding architectural constraints (DDD, Hexagonal, CQRS, Event Sourcing)
3. **Defines** the Shared Kernel contract (VertexId, JerryUri, IAuditable, IVersioned, EntityBase)
4. **Provides** traceability matrix linking patterns to source documents
5. **Includes** L0/L1/L2 output levels

**Key Sections**:
- L0: Executive Summary (for stakeholders)
- L1: Technical Patterns (for developers)
  - Domain Patterns (Aggregates, Entities, Value Objects)
  - Architectural Patterns (Ports, Adapters, CQRS, Events)
  - Shared Kernel Specification
- L2: Strategic Implications (for architects)
  - Bounded Context Map
  - Evolution Strategy
  - Non-Negotiable Constraints

---

## Stage 2: Analysis (ps-analyst)

### Task: Canon Implementation Gap Analysis

**Agent**: `ps-analyst`

**PS Context**:
```
PS ID: PROJ-001
Entry ID: e-012-vN (where N = cycle number)
Topic: Canon-Implementation Gap Analysis
```

**Input Artifacts (Cycle 1)**:
```
projects/PROJ-001-plugin-cleanup/synthesis/PROJ-001-e-011-v1-jerry-design-canon.md (Stage 1 output)
src/session_management/ (current implementation)
projects/PROJ-001-plugin-cleanup/analysis/PROJ-001-e-007-implementation-gap-analysis.md (previous)
```

**Additional Input (Cycle N, N>1)**:
```
projects/PROJ-001-plugin-cleanup/analysis/PROJ-001-e-012-v{N-1}-canon-implementation-gap.md (prior analysis)
```

**Output**: `projects/PROJ-001-plugin-cleanup/analysis/PROJ-001-e-012-vN-canon-implementation-gap.md`

**Objective**:
Analyze delta between canon and implementation:
1. **Shared Kernel Gap**: What components are missing?
2. **Pattern Compliance**: Does current code follow canonical patterns?
3. **Prioritized Remediation**: Ordered list of changes needed
4. **Dependency Analysis**: What blocks what?

**Analysis Framework**: 5W1H + NASA SE Risk Assessment

---

## Stage 3: Decision (ps-architect)

### Task: SYNTH-004 - Shared Kernel Implementation Guide

**Agent**: `ps-architect`

**PS Context**:
```
PS ID: PROJ-001
Entry ID: e-013-vN (where N = cycle number)
Topic: Shared Kernel Implementation ADR
```

**Input Artifacts (Cycle 1)**:
```
projects/PROJ-001-plugin-cleanup/synthesis/PROJ-001-e-011-v1-jerry-design-canon.md (Stage 1)
projects/PROJ-001-plugin-cleanup/analysis/PROJ-001-e-012-v1-canon-implementation-gap.md (Stage 2)
```

**Additional Input (Cycle N, N>1)**:
```
projects/PROJ-001-plugin-cleanup/decisions/PROJ-001-e-013-v{N-1}-adr-shared-kernel.md (prior ADR)
```

**Output**: `projects/PROJ-001-plugin-cleanup/decisions/PROJ-001-e-013-vN-adr-shared-kernel.md`

**Objective**:
Create ADR (Nygard format) that:
1. **Defines** `src/shared_kernel/` module structure
2. **Specifies** implementation order (dependencies first)
3. **Documents** interface contracts for each component
4. **Establishes** migration path for `src/session_management/`
5. **Includes** test strategy for Shared Kernel

**ADR Sections**:
- Title: "ADR: Shared Kernel Module Implementation"
- Status: PROPOSED
- Context: Gap analysis findings
- Decision: Module structure and contracts
- Consequences: Migration impact
- Implementation Guide: Step-by-step

---

## Stage 4: Validation (ps-validator)

### Task: Canon & ADR Completeness Validation

**Agent**: `ps-validator`

**PS Context**:
```
PS ID: PROJ-001
Entry ID: e-014-vN (where N = cycle number)
Topic: Canon Completeness Validation
```

**Input Artifacts**:
```
projects/PROJ-001-plugin-cleanup/synthesis/PROJ-001-e-011-vN-jerry-design-canon.md (Stage 1)
projects/PROJ-001-plugin-cleanup/decisions/PROJ-001-e-013-vN-adr-shared-kernel.md (Stage 3)
projects/PROJ-001-plugin-cleanup/research/PROJ-001-e-001-worktracker-proposal-extraction.md
projects/PROJ-001-plugin-cleanup/research/PROJ-001-e-002-plan-graph-model.md
```

**Output**: `projects/PROJ-001-plugin-cleanup/analysis/PROJ-001-e-014-vN-canon-validation.md`

**Objective**:
Validate completeness:
1. **Research Coverage**: Do canon patterns trace to research findings?
2. **Gap Coverage**: Does ADR address all gaps from analysis?
3. **Actionability**: Is implementation guide executable?
4. **Orphan Check**: Any requirements without implementation path?

**CRITICAL: Validation Verdict**

The validator MUST output a clear verdict section:

```markdown
## Validation Verdict

**Status**: PASS | FAIL

### Issues Found (if FAIL)
| Issue ID | Severity | Description | Affected Artifact |
|----------|----------|-------------|-------------------|
| V-001    | CRITICAL | ...         | e-011-vN          |
| V-002    | MAJOR    | ...         | e-013-vN          |

### Recommendations for Next Cycle
1. ...
2. ...
```

If `Status: PASS`, the refinement loop terminates.
If `Status: FAIL`, proceed to Stage 5 then start Cycle N+1.

**Validation Matrix**:
| Research Finding | Canon Pattern | ADR Section | Validated |
|------------------|---------------|-------------|-----------|

---

## Stage 5: Report (ps-reporter)

### Task: Cycle Status Report

**Agent**: `ps-reporter`

**PS Context**:
```
PS ID: PROJ-001
Entry ID: e-015-vN (where N = cycle number)
Topic: Cycle N Status Report
```

**Input Artifacts**:
```
All e-001 through e-014-vN artifacts
projects/PROJ-001-plugin-cleanup/WORKTRACKER.md
projects/PROJ-001-plugin-cleanup/analysis/PROJ-001-e-014-vN-canon-validation.md (validation verdict)
```

**Output**: `projects/PROJ-001-plugin-cleanup/reports/PROJ-001-e-015-vN-cycle-status.md`

**Objective**:
Generate cycle status report:
1. **Cycle N Metrics**: Stages completed, artifacts produced
2. **Validation Status**: PASS or FAIL (from e-014-vN)
3. **Artifact Traceability**: Full document chain visualization
4. **Delta from Prior Cycle** (if N>1): What changed, what improved
5. **Next Steps**:
   - If PASS: Phase 7 COMPLETE, Phase 6 UNBLOCKED
   - If FAIL: Cycle N+1 recommendations

---

## Execution Order (Per Cycle)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ STAGE 1: ps-synthesizer (SYNTH-003)                                          │
│ Input: e-001→e-006 (+ e-011-v{N-1}, e-014-v{N-1} if N>1)                     │
│ Output: e-011-vN-jerry-design-canon.md                                       │
│ Action: COMMIT after completion                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STAGE 2: ps-analyst (Gap Analysis)                                           │
│ Input: e-011-vN + src/session_management/ (+ e-012-v{N-1} if N>1)           │
│ Output: e-012-vN-canon-implementation-gap.md                                 │
│ Action: COMMIT after completion                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STAGE 3: ps-architect (SYNTH-004)                                            │
│ Input: e-011-vN + e-012-vN (+ e-013-v{N-1} if N>1)                           │
│ Output: e-013-vN-adr-shared-kernel.md                                        │
│ Action: COMMIT after completion                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STAGE 4: ps-validator (Completeness)                                         │
│ Input: e-011-vN + e-013-vN + research docs                                   │
│ Output: e-014-vN-canon-validation.md (includes PASS/FAIL verdict)            │
│ Action: COMMIT after completion                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STAGE 5: ps-reporter (Cycle Status)                                          │
│ Input: All artifacts + WORKTRACKER + e-014-vN verdict                        │
│ Output: e-015-vN-cycle-status.md                                             │
│ Action: COMMIT after completion                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
                     ┌────────────────────────────────┐
                     │  CHECK e-014-vN VERDICT        │
                     └────────────────────────────────┘
                                      │
                      ┌───────────────┴───────────────┐
                      │                               │
                      ▼                               ▼
           ┌──────────────────┐            ┌──────────────────┐
           │  VERDICT: FAIL   │            │  VERDICT: PASS   │
           │                  │            │                  │
           │  → Cycle N+1     │            │  PHASE 7 COMPLETE│
           │  (N = N + 1)     │            │  PHASE 6 UNBLOCKED│
           │  goto STAGE 1    │            │  EXIT LOOP       │
           └──────────────────┘            └──────────────────┘
```

---

## State Passing Protocol

| Stage | Agent | Artifact Path (Cycle N) | Consumers |
|-------|-------|-------------------------|-----------|
| 1 | ps-synthesizer | `synthesis/PROJ-001-e-011-vN-jerry-design-canon.md` | Stage 2, 3, 4, Cycle N+1 Stage 1 |
| 2 | ps-analyst | `analysis/PROJ-001-e-012-vN-canon-implementation-gap.md` | Stage 3, Cycle N+1 Stage 2 |
| 3 | ps-architect | `decisions/PROJ-001-e-013-vN-adr-shared-kernel.md` | Stage 4, Cycle N+1 Stage 3 |
| 4 | ps-validator | `analysis/PROJ-001-e-014-vN-canon-validation.md` | Stage 5, Orchestrator (verdict check), Cycle N+1 Stage 1 |
| 5 | ps-reporter | `reports/PROJ-001-e-015-vN-cycle-status.md` | Orchestrator, WORKTRACKER |

### Cross-Cycle State

| From Cycle N | To Cycle N+1 | Purpose |
|--------------|--------------|---------|
| e-011-vN | ps-synthesizer input | Refine canon based on validation feedback |
| e-014-vN | ps-synthesizer input | Incorporate specific issues identified |
| e-012-vN | ps-analyst input | Build on prior gap analysis |
| e-013-vN | ps-architect input | Iterate on ADR decisions |

---

## Constitutional Compliance

| Principle | Enforcement |
|-----------|-------------|
| P-002: File Persistence | Each stage creates persistent artifact |
| P-003: No Recursive Subagents | Orchestrator invokes; agents don't nest |
| P-004: Explicit Provenance | Artifacts reference upstream documents |
| P-010: Task Tracking | WORKTRACKER.md updated after each stage |
| P-011: Evidence-Based | Patterns traced to research findings |

---

## Success Criteria

### Per-Cycle Criteria
| Criterion | Measure | Cycle 1 | Cycle 2 | Cycle N |
|-----------|---------|---------|---------|---------|
| e-011-vN exists | Design Canon created | ⬜ | ⬜ | ⬜ |
| e-012-vN exists | Gap analysis complete | ⬜ | ⬜ | ⬜ |
| e-013-vN exists | ADR created | ⬜ | ⬜ | ⬜ |
| e-014-vN exists | Validation complete | ⬜ | ⬜ | ⬜ |
| e-015-vN exists | Cycle report generated | ⬜ | ⬜ | ⬜ |
| Commits | 5 commits (one per stage) | ⬜ | ⬜ | ⬜ |

### Termination Criteria
| Criterion | Measure | Validated |
|-----------|---------|-----------|
| e-014-vN verdict | `Status: PASS` | ⬜ |
| WORKTRACKER | Phase 7 at 100% | ⬜ |
| WORKTRACKER | Phase 6 shows UNBLOCKED | ⬜ |
| Final artifacts | Symlinked/renamed to canonical (no -vN suffix) | ⬜ |

---

## WORKTRACKER Updates Required

After each stage, update `WORKTRACKER.md`:

**After Each Stage (commit message format)**:
```
docs(proj-001): complete cycle N stage M - {agent_name}
```

**After Stage 1 (any cycle)**:
```markdown
### SYNTH-003: Design Canon Creation 🔄
- **Status**: IN_PROGRESS (Cycle N)
- **Current Version**: e-011-vN
- **Output**: `synthesis/PROJ-001-e-011-vN-jerry-design-canon.md`
```

**After Stage 4 (validation)**:
```markdown
### SYNTH-004b: Canon Validation 🔄
- **Status**: Cycle N - VERDICT: {PASS|FAIL}
- **Output**: `analysis/PROJ-001-e-014-vN-canon-validation.md`
- **Issues Found**: {count} (if FAIL)
```

**After Final Cycle (PASS verdict)**:
```markdown
| Phase 7: Design Document Synthesis | ✅ COMPLETED | 100% |
| Phase 6: Project Enforcement | 🔄 IN PROGRESS | 55% → UNBLOCKED |

### Phase 7 Summary
- **Total Cycles**: N
- **Final Artifacts**: e-011-vN, e-012-vN, e-013-vN, e-014-vN, e-015-vN
- **Validation**: PASS
```

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Agent timeout | Break into smaller prompts if needed |
| Missing patterns | Cross-reference all 5 research docs |
| Canon too abstract | Include concrete code examples in L1 |
| ADR not actionable | Include step-by-step with file paths |

---

## Approval

- [x] User approves ACTION-PLAN-002 (2026-01-09)
- [x] User approves Iterative Refinement Protocol (2026-01-09)
- [ ] Proceed with Cycle 1 Stage 1 (ps-synthesizer)

---

*Action Plan Version: 2.0*
*Pattern: Full Decision Workflow (Pattern 5) with Iterative Refinement*
*Constitutional Compliance: Jerry Constitution v1.0*
*Created: 2026-01-10*
*Updated: 2026-01-09*
