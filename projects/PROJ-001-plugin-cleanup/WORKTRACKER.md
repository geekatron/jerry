# Work Tracker - PROJ-001-plugin-cleanup

> Multi-Project Support Cleanup - Persistent work tracking for context compaction survival.

**Last Updated**: 2026-01-09T23:30:00Z
**Project ID**: PROJ-001-plugin-cleanup
**Branch**: cc/task-subtask
**Environment Variable**: `JERRY_PROJECT=PROJ-001-plugin-cleanup`

---

## Enforced Principles

> These principles are NON-NEGOTIABLE. All work MUST adhere to them.

| ID | Principle | Enforcement |
|----|-----------|-------------|
| **P-BDD** | BDD Red/Green/Refactor with full test pyramid | HARD |
| **P-5W1H** | 5W1H research before ANY implementation | HARD |
| **P-RESEARCH** | Deep research (Context7 + industry) with citations | HARD |
| **P-EVIDENCE** | Data + evidence driven decisions | HARD |
| **P-PERSIST** | Persist ALL research/analysis to repository | HARD |
| **P-ARCH** | DDD, Hexagonal, ES, CQRS, Repository, DI | HARD |
| **P-REAL** | NO placeholders/stubs - real tests only | HARD |
| **P-EDGE** | Happy path + negative + edge + failure scenarios | HARD |
| **P-REGRESS** | Zero regressions - verify before marking complete | HARD |
| **P-COMPLETE** | No shortcuts - work completed in full | HARD |

### Test Pyramid (Required per Implementation Task)

```
                    ┌─────────────┐
                    │    E2E      │ ← Full workflow validation
                   ┌┴─────────────┴┐
                   │    System     │ ← Component interaction
                  ┌┴───────────────┴┐
                  │   Integration   │ ← Adapter/port testing
                 ┌┴─────────────────┴┐
                 │       Unit        │ ← Domain logic
                ┌┴───────────────────┴┐
                │ Contract+Architecture│ ← Interface compliance
                └─────────────────────┘
```

---

## Work Item Schema

> Every implementation task MUST follow this schema.

### Task Structure

```
TASK-XXX: [Title]
├── R-XXX: Research Phase
│   ├── 5W1H Analysis (mandatory)
│   ├── Context7 Research
│   ├── Industry Best Practices
│   ├── Citations/Sources
│   └── Output: research/PROJ-001-R-XXX-*.md
│
├── I-XXX: Implementation Phase
│   ├── Interface Contracts
│   ├── Files Changed
│   ├── Implementation Order
│   └── BDD Cycle (RED → GREEN → REFACTOR)
│
├── T-XXX: Test Phase
│   ├── Unit Tests (Happy, Edge, Negative, Boundary)
│   ├── Integration Tests
│   ├── System Tests
│   ├── E2E Tests
│   ├── Contract Tests
│   └── Architecture Tests
│
└── E-XXX: Evidence Phase
    ├── All Tests Pass
    ├── Coverage ≥ 90%
    ├── Commit Hash
    ├── Regression Check (0 regressions)
    └── PR/Review Link
```

### Test Matrix Template

| Category | Subcategory | Count | Location | Status |
|----------|-------------|-------|----------|--------|
| Unit | Happy Path | N | `tests/unit/test_*.py` | ⏳ |
| Unit | Edge Cases | N | `tests/unit/test_*.py` | ⏳ |
| Unit | Negative | N | `tests/unit/test_*.py` | ⏳ |
| Unit | Boundary | N | `tests/unit/test_*.py` | ⏳ |
| Integration | Adapters | N | `tests/integration/test_*.py` | ⏳ |
| System | Components | N | `tests/system/test_*.py` | ⏳ |
| E2E | Workflows | N | `tests/e2e/test_*.py` | ⏳ |
| Contract | Interfaces | N | `tests/contract/test_*.py` | ⏳ |
| Architecture | Boundaries | N | `tests/architecture/test_*.py` | ⏳ |

### 5W1H Template

| Question | Analysis |
|----------|----------|
| **What** | What needs to be done? |
| **Why** | Why is this needed? Business/technical justification |
| **Who** | Who/what is impacted? Stakeholders, components |
| **Where** | Where in the codebase? File paths, modules |
| **When** | When can this start? Dependencies, blockers |
| **How** | How will it be implemented? Approach, patterns |

---

## Navigation Graph

```
                         ┌─────────────────────────────────────────┐
                         │           WORKTRACKER.md                │
                         │         (INDEX + SCHEMA)                │
                         └─────────────────┬───────────────────────┘
                                           │
         ┌─────────────────────────────────┼─────────────────────────────┐
         │                                 │                             │
         ▼                                 ▼                             ▼
┌─────────────────┐             ┌─────────────────┐           ┌─────────────────┐
│   COMPLETED     │             │  IN PROGRESS    │           │    SUPPORT      │
│   Phases 1-5,7  │             │    Phase 6      │           │  BUGS, TECHDEBT │
└────────┬────────┘             └────────┬────────┘           └────────┬────────┘
         │                               │                             │
         ▼                               ▼                             ▼
work/PHASE-01-*.md              work/PHASE-06-*.md            work/PHASE-BUGS.md
work/PHASE-02-*.md               (CURRENT FOCUS)              work/PHASE-TECHDEBT.md
work/PHASE-03-*.md                      │
work/PHASE-04-*.md                      │
work/PHASE-05-*.md              ┌───────┴───────┐
work/PHASE-07-*.md              │               │
                                ▼               ▼
                          ENFORCE-008d    ENFORCE-009+
                          (Domain)        (Tests)
```

---

## Full Dependency Graph

```
Phase 1 ───► Phase 2 ───► Phase 3 ───► Phase 4 ───► Phase 5
(Infra)      (Core)       (Agents)     (Gov)        (Valid)
                                                       │
                                       ┌───────────────┤
                                       │               │
                                       ▼               ▼
                                   Phase 7         Phase 6
                                   (Design)        (Enforce)
                                       │               │
                                       │    ┌──────────┘
                                       │    │
                                       ▼    ▼
                              Shared Kernel (✅)
                                       │
                          ┌────────────┴────────────┐
                          │                         │
                          ▼                         ▼
                    ENFORCE-008d              ENFORCE-013
                    (Domain Refactor)         (Arch Tests)
                          │
    ┌─────────────────────┼─────────────────────┐
    │                     │                     │
    ▼                     ▼                     ▼
008d.0              008d.1-008d.3          008d.4
(Research)          (Domain)               (Infra)
    │                     │                     │
    │                     │                     │
    ▼                     ▼                     ▼
    └─────────────────────┴─────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          │               │               │
          ▼               ▼               ▼
    ENFORCE-009     ENFORCE-010     ENFORCE-011
    (App Tests)     (Infra Tests)   (E2E Tests)
          │               │               │
          └───────────────┴───────────────┘
                          │
                          ▼
                    ENFORCE-012-016
                    (Final Tasks)
```

---

## Quick Status Dashboard

| Phase | File | Status | Progress | Predecessors | Successors |
|-------|------|--------|----------|--------------|------------|
| 1 | [PHASE-01](work/PHASE-01-INFRASTRUCTURE.md) | ✅ DONE | 100% | None | Phase 2 |
| 2 | [PHASE-02](work/PHASE-02-CORE-UPDATES.md) | ✅ DONE | 100% | Phase 1 | Phase 3 |
| 3 | [PHASE-03](work/PHASE-03-AGENT-UPDATES.md) | ✅ DONE | 100% | Phase 2 | Phase 4 |
| 4 | [PHASE-04](work/PHASE-04-GOVERNANCE.md) | ✅ DONE | 100% | Phase 3 | Phase 5 |
| 5 | [PHASE-05](work/PHASE-05-VALIDATION.md) | ✅ DONE | 100% | Phase 4 | Phase 6, 7 |
| 6 | [PHASE-06](work/PHASE-06-ENFORCEMENT.md) | 🔄 ACTIVE | 60% | Phase 5, 7 | None |
| 7 | [PHASE-07](work/PHASE-07-DESIGN-SYNTHESIS.md) | ✅ DONE | 100% | Phase 5 | Phase 6 |
| BUGS | [PHASE-BUGS](work/PHASE-BUGS.md) | ✅ RESOLVED | 100% | - | - |
| TECHDEBT | [PHASE-TECHDEBT](work/PHASE-TECHDEBT.md) | ⏳ PENDING | 33% | - | - |

---

## Current Focus

> **Active Phase**: [PHASE-06-ENFORCEMENT](work/PHASE-06-ENFORCEMENT.md)
> **Active Task**: ENFORCE-008d - Refactor to Unified Design
> **Active Subtask**: 008d.0 - Research & Analysis (5W1H)

### Active Work Item Details

| Attribute | Value |
|-----------|-------|
| Task ID | ENFORCE-008d |
| Phase | R-008d.0 (Research) |
| Predecessors | Phase 7 (✅), Shared Kernel (✅) |
| Successors | ENFORCE-009, ENFORCE-010, ENFORCE-013 |
| Blocking | None |
| Blocked By | None |

### Next Actions

> **RUNBOOK**: [RUNBOOK-001-008d](runbooks/RUNBOOK-001-008d-domain-refactoring.md) - Step-by-step execution guide
> **VALIDATION**: [VALIDATION-001](runbooks/VALIDATION-001-runbook-test.md) - Runbook validation evidence

1. Read RUNBOOK-001-008d Pre-Flight Checklist
2. Execute Stage R: Research Phase (R-008d.0)
3. Create research artifact: `research/PROJ-001-R-008d-domain-refactoring.md`
4. Commit with checkpoint template from RUNBOOK

---

## Work Item Index

### Phase 6 Tasks (Active)

| ID | Title | Phase | Status | Predecessors | Successors |
|----|-------|-------|--------|--------------|------------|
| ENFORCE-008d | Refactor to Unified Design | 6 | 🔄 | Phase 7, SK | 009, 010, 013 |
| 008d.0 | Research & Analysis | 6.008d | 🔄 | Phase 7 | 008d.1 |
| 008d.1 | Value Object Refactoring | 6.008d | ⏳ | 008d.0 | 008d.2 |
| 008d.1.1 | ProjectId → VertexId | 6.008d.1 | ⏳ | 008d.0 | 008d.1.2 |
| 008d.1.2 | Extract slug property | 6.008d.1 | ⏳ | 008d.1.1 | 008d.1.3 |
| 008d.1.3 | Update VO tests | 6.008d.1 | ⏳ | 008d.1.2 | 008d.2 |
| 008d.2 | Entity Refactoring | 6.008d | ⏳ | 008d.1 | 008d.4 |
| 008d.2.1 | ProjectInfo → EntityBase | 6.008d.2 | ⏳ | 008d.1 | 008d.2.2 |
| 008d.2.2 | Add JerryUri | 6.008d.2 | ⏳ | 008d.2.1 | 008d.2.3 |
| 008d.2.3 | Add extensibility | 6.008d.2 | ⏳ | 008d.2.2 | 008d.3 |
| 008d.3 | New Domain Objects | 6.008d | ⏳ | 008d.0 | 008d.4 |
| 008d.3.1 | Create SessionId | 6.008d.3 | ⏳ | 008d.0 | 008d.3.2 |
| 008d.3.2 | Create Session aggregate | 6.008d.3 | ⏳ | 008d.3.1 | 008d.3.3 |
| 008d.3.3 | Add session_id to Project | 6.008d.3 | ⏳ | 008d.3.2 | 008d.4 |
| 008d.4 | Infrastructure Updates | 6.008d | ⏳ | 008d.1-3 | 009 |
| 008d.4.1 | Update adapters | 6.008d.4 | ⏳ | 008d.1-3 | 008d.4.2 |
| 008d.4.2 | Migrate existing projects | 6.008d.4 | ⏳ | 008d.4.1 | 008d.4.3 |
| 008d.4.3 | Update infra tests | 6.008d.4 | ⏳ | 008d.4.2 | 009 |
| ENFORCE-009 | Application Layer Tests | 6 | ⏳ | 008d | 011 |
| ENFORCE-010 | Infrastructure Tests | 6 | ⏳ | 008d | 011 |
| ENFORCE-011 | E2E Tests | 6 | ⏳ | 009, 010 | 012 |
| ENFORCE-012 | Contract Tests | 6 | ⏳ | 011 | 014 |
| ENFORCE-013 | Architecture Tests | 6 | ⏳ | 008d | 016 |
| ENFORCE-014 | Update CLAUDE.md | 6 | ⏳ | 011 | 015 |
| ENFORCE-015 | Update Manifest | 6 | ⏳ | 014 | 016 |
| ENFORCE-016 | Final Validation | 6 | ⏳ | ALL | None |

---

## Cross-Reference Index

### Runbooks (Execution Guides)

| ID | Title | Location | Validated |
|----|-------|----------|-----------|
| RUNBOOK-001 | ENFORCE-008d Domain Refactoring | `runbooks/RUNBOOK-001-008d-domain-refactoring.md` | ✅ |

### Validation Evidence

| ID | Title | Location | Result |
|----|-------|----------|--------|
| VALIDATION-001 | Runbook Fresh Context Test | `runbooks/VALIDATION-001-runbook-test.md` | ✅ PASS |

### Research Artifacts

| ID | Title | Location | Status |
|----|-------|----------|--------|
| R-001 | Worktracker Proposal Extraction | `research/e-001-*.md` | ✅ |
| R-002 | Plan Graph Model | `research/e-002-*.md` | ✅ |
| R-003 | Revised Architecture | `research/e-003-*.md` | ✅ |
| R-004 | Strategic Plan v3 | `research/e-004-*.md` | ✅ |
| R-005 | Industry Best Practices | `research/e-005-*.md` | ✅ |
| R-008d | Domain Refactoring | `research/PROJ-001-R-008d-*.md` | ⏳ |

### Decision Artifacts

| ID | Title | Location | Status |
|----|-------|----------|--------|
| ADR-002 | Project Enforcement | `design/ADR-002-*.md` | ✅ |
| ADR-003 | Code Structure | `design/ADR-003-*.md` | ✅ |
| ADR-004 | Session Management Alignment | `design/ADR-004-*.md` | ✅ |
| ADR-013 | Shared Kernel | `decisions/e-013-*.md` | ✅ |

### Implementation Artifacts

| ID | Title | Location | Tests | Status |
|----|-------|----------|-------|--------|
| I-SK | Shared Kernel | `src/shared_kernel/` | 58 | ✅ |
| I-SM | Session Management | `src/session_management/` | 57 | 🔄 |

### Test Suites

| Suite | Location | Count | Status |
|-------|----------|-------|--------|
| Shared Kernel Unit | `tests/shared_kernel/` | 58 | ✅ |
| Session Mgmt Domain | `tests/session_management/unit/` | 57 | ✅ |
| Session Mgmt Integration | `tests/session_management/integration/` | 0 | ⏳ |
| Session Mgmt E2E | `tests/session_management/e2e/` | 0 | ⏳ |

---

## Session Resume Protocol

When resuming work on this project:

1. **Read this file first** - Understand current focus and next actions
2. **Check Active Task** in Work Item Index
3. **Navigate to Phase File** for detailed subtask breakdown
4. **Check Predecessors** - Ensure all are complete
5. **Follow Work Item Schema** - R → I → T → E phases
6. **Update this file** after each significant change

---

## Verification Checklist

Before marking ANY task complete:

- [ ] 5W1H research documented and persisted
- [ ] Industry best practices consulted with citations
- [ ] All test categories implemented (Unit, Integration, System, E2E, Contract, Arch)
- [ ] BDD cycle completed (RED → GREEN → REFACTOR)
- [ ] Edge cases, negative cases, failure scenarios covered
- [ ] No placeholders or stubs in tests
- [ ] Coverage ≥ 90%
- [ ] Zero regressions (run full test suite)
- [ ] Commit created with evidence
- [ ] WORKTRACKER updated

---

## Document History

| Date | Author | Changes |
|------|--------|---------|
| 2026-01-09 | Claude | Initial creation |
| 2026-01-09 | Claude | Restructured to multi-file format |
| 2026-01-09 | Claude | Added Work Item Schema and Enforced Principles |
| 2026-01-09 | Claude | Added full dependency graph and cross-references |
| 2026-01-09 | Claude | Enhanced with Work Item Schema (R/I/T/E) and Enforced Principles |
| 2026-01-09 | Claude | Added RUNBOOK-001-008d and validation evidence |
