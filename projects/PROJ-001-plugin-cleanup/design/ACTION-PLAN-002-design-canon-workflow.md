# Action Plan: Design Canon & Shared Kernel Workflow

> **Document ID**: ACTION-PLAN-002
> **Date**: 2026-01-10
> **Project**: PROJ-001-plugin-cleanup
> **Phase**: Phase 7 - Design Document Synthesis (Final Stage)
> **Pattern**: Full Decision Workflow (Pattern 5)
> **Predecessor**: ACTION-PLAN-001 (Tiers 1-6 COMPLETED)

---

## Executive Summary

ACTION-PLAN-001 successfully executed Tiers 1-6, producing artifacts e-001 through e-010. This plan completes Phase 7 by executing the **Full Decision Workflow** pattern to:

1. Create the authoritative **Jerry Design Canon v1.0**
2. Produce the **Shared Kernel Implementation Guide**
3. Validate completeness
4. Generate completion report

Upon completion, **Phase 6 (Project Enforcement)** will be unblocked.

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

### Task: SYNTH-003 - Jerry Design Canon v1.0

**Agent**: `ps-synthesizer`

**PS Context**:
```
PS ID: PROJ-001
Entry ID: e-011
Topic: Jerry Design Canon v1.0
```

**Input Artifacts**:
```
projects/PROJ-001-plugin-cleanup/research/PROJ-001-e-001-worktracker-proposal-extraction.md
projects/PROJ-001-plugin-cleanup/research/PROJ-001-e-002-plan-graph-model.md
projects/PROJ-001-plugin-cleanup/research/PROJ-001-e-003-revised-architecture-foundation.md
projects/PROJ-001-plugin-cleanup/research/PROJ-001-e-004-strategic-plan-v3.md
projects/PROJ-001-plugin-cleanup/research/PROJ-001-e-005-industry-best-practices.md
projects/PROJ-001-plugin-cleanup/synthesis/PROJ-001-e-006-unified-architecture-canon.md
```

**Output**: `projects/PROJ-001-plugin-cleanup/synthesis/PROJ-001-e-011-jerry-design-canon-v1.md`

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
Entry ID: e-012
Topic: Canon-Implementation Gap Analysis
```

**Input Artifacts**:
```
projects/PROJ-001-plugin-cleanup/synthesis/PROJ-001-e-011-jerry-design-canon-v1.md (Stage 1 output)
src/session_management/ (current implementation)
projects/PROJ-001-plugin-cleanup/analysis/PROJ-001-e-007-implementation-gap-analysis.md (previous)
```

**Output**: `projects/PROJ-001-plugin-cleanup/analysis/PROJ-001-e-012-canon-implementation-gap.md`

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
Entry ID: e-013
Topic: Shared Kernel Implementation ADR
```

**Input Artifacts**:
```
projects/PROJ-001-plugin-cleanup/synthesis/PROJ-001-e-011-jerry-design-canon-v1.md (Stage 1)
projects/PROJ-001-plugin-cleanup/analysis/PROJ-001-e-012-canon-implementation-gap.md (Stage 2)
```

**Output**: `projects/PROJ-001-plugin-cleanup/decisions/PROJ-001-e-013-adr-shared-kernel.md`

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
Entry ID: e-014
Topic: Canon Completeness Validation
```

**Input Artifacts**:
```
projects/PROJ-001-plugin-cleanup/synthesis/PROJ-001-e-011-jerry-design-canon-v1.md (Stage 1)
projects/PROJ-001-plugin-cleanup/decisions/PROJ-001-e-013-adr-shared-kernel.md (Stage 3)
projects/PROJ-001-plugin-cleanup/research/PROJ-001-e-001-worktracker-proposal-extraction.md
projects/PROJ-001-plugin-cleanup/research/PROJ-001-e-002-plan-graph-model.md
```

**Output**: `projects/PROJ-001-plugin-cleanup/analysis/PROJ-001-e-014-canon-validation.md`

**Objective**:
Validate completeness:
1. **Research Coverage**: Do canon patterns trace to research findings?
2. **Gap Coverage**: Does ADR address all gaps from analysis?
3. **Actionability**: Is implementation guide executable?
4. **Orphan Check**: Any requirements without implementation path?

**Validation Matrix**:
| Research Finding | Canon Pattern | ADR Section | Validated |
|------------------|---------------|-------------|-----------|

---

## Stage 5: Report (ps-reporter)

### Task: Phase 7 Completion Status Report

**Agent**: `ps-reporter`

**PS Context**:
```
PS ID: PROJ-001
Entry ID: e-015
Topic: Phase 7 Completion Report
```

**Input Artifacts**:
```
All e-001 through e-014 artifacts
projects/PROJ-001-plugin-cleanup/WORKTRACKER.md
```

**Output**: `projects/PROJ-001-plugin-cleanup/reports/PROJ-001-e-015-phase7-completion.md`

**Objective**:
Generate completion report:
1. **Phase 7 Metrics**: Tasks completed, artifacts produced
2. **Artifact Traceability**: Full document chain visualization
3. **Phase 6 Unblock Confirmation**: Prerequisites satisfied
4. **Recommendations**: Next steps for Phase 6
5. **Quality Assessment**: Canon quality indicators

---

## Execution Order

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ STAGE 1: ps-synthesizer (SYNTH-003)                                          │
│ Input: e-001 through e-006                                                   │
│ Output: e-011 jerry-design-canon-v1.md                                       │
│ Duration: ~10-15 minutes                                                     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STAGE 2: ps-analyst (Gap Analysis)                                           │
│ Input: e-011 + src/session_management/                                       │
│ Output: e-012 canon-implementation-gap.md                                    │
│ Duration: ~5-10 minutes                                                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STAGE 3: ps-architect (SYNTH-004)                                            │
│ Input: e-011 + e-012                                                         │
│ Output: e-013 adr-shared-kernel.md                                           │
│ Duration: ~10-15 minutes                                                     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STAGE 4: ps-validator (Completeness)                                         │
│ Input: e-011 + e-013 + research docs                                         │
│ Output: e-014 canon-validation.md                                            │
│ Duration: ~5-10 minutes                                                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STAGE 5: ps-reporter (Completion)                                            │
│ Input: All artifacts + WORKTRACKER                                           │
│ Output: e-015 phase7-completion.md                                           │
│ Duration: ~5-10 minutes                                                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
                     ┌────────────────────────────────┐
                     │  PHASE 7 COMPLETE (100%)        │
                     │  PHASE 6 UNBLOCKED              │
                     │  ENFORCE-008d can proceed       │
                     └────────────────────────────────┘
```

---

## State Passing Protocol

| Stage | Agent | Output Key | Artifact Path | Next Agent Input |
|-------|-------|------------|---------------|------------------|
| 1 | ps-synthesizer | `synthesizer_output` | `synthesis/PROJ-001-e-011-*` | Stage 2, 3, 4 |
| 2 | ps-analyst | `analyst_output` | `analysis/PROJ-001-e-012-*` | Stage 3 |
| 3 | ps-architect | `architect_output` | `decisions/PROJ-001-e-013-*` | Stage 4 |
| 4 | ps-validator | `validator_output` | `analysis/PROJ-001-e-014-*` | Stage 5 |
| 5 | ps-reporter | `reporter_output` | `reports/PROJ-001-e-015-*` | (Terminal) |

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

| Criterion | Measure | Validated |
|-----------|---------|-----------|
| e-011 exists | Design Canon created | ⬜ |
| e-012 exists | Gap analysis complete | ⬜ |
| e-013 exists | ADR defines implementation guide | ⬜ |
| e-014 exists | Validation confirms completeness | ⬜ |
| e-015 exists | Status report generated | ⬜ |
| WORKTRACKER | Phase 7 at 100% | ⬜ |
| WORKTRACKER | Phase 6 shows UNBLOCKED | ⬜ |

---

## WORKTRACKER Updates Required

After each stage, update `WORKTRACKER.md`:

**After Stage 1**:
```markdown
### SYNTH-003: Design Canon Creation ✅
- **Status**: COMPLETED
- **Output**: `synthesis/PROJ-001-e-011-jerry-design-canon-v1.md`
```

**After Stage 3**:
```markdown
### SYNTH-004: Shared Kernel Implementation Guide ✅
- **Status**: COMPLETED
- **Output**: `decisions/PROJ-001-e-013-adr-shared-kernel.md`
```

**After Stage 5**:
```markdown
| Phase 7: Design Document Synthesis | ✅ COMPLETED | 100% |
| Phase 6: Project Enforcement | 🔄 IN PROGRESS | 55% → continuing |
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

- [ ] User approves ACTION-PLAN-002
- [ ] Proceed with Stage 1 (ps-synthesizer)

---

*Action Plan Version: 1.0*
*Pattern: Full Decision Workflow (Pattern 5)*
*Constitutional Compliance: Jerry Constitution v1.0*
*Created: 2026-01-10*
