# Runbook: ENFORCE-008d Domain Refactoring

> **Document ID**: RUNBOOK-001-008d
> **Version**: 1.0
> **Date**: 2026-01-09
> **Project**: PROJ-001-plugin-cleanup
> **Task**: ENFORCE-008d - Refactor to Unified Design
> **Pattern**: BDD Red/Green/Refactor with Full Test Pyramid
> **Status**: DRAFT - AWAITING VALIDATION

---

## Executive Summary

This runbook provides step-by-step execution instructions for ENFORCE-008d: Refactoring `src/session_management/` domain layer to use Shared Kernel patterns.

**Prerequisites**:
- Shared Kernel implemented: `src/shared_kernel/` (58 tests) ✅
- Phase 7 Design Canon: `synthesis/PROJ-001-e-011-v1-jerry-design-canon.md` ✅
- ADR-013 Shared Kernel: `decisions/PROJ-001-e-013-v1-adr-shared-kernel.md` ✅

**Outcome**:
- `src/session_management/domain/` uses Shared Kernel types
- 102 new/updated tests pass
- Zero regressions

---

## Pre-Flight Checklist

Before starting ANY work, verify:

| # | Check | Command/Location | Expected |
|---|-------|------------------|----------|
| 1 | Shared Kernel tests pass | `pytest tests/shared_kernel/ -v` | 58 passed |
| 2 | Session Mgmt tests pass | `pytest tests/session_management/ -v` | 57 passed |
| 3 | Branch is correct | `git branch --show-current` | `cc/task-subtask` |
| 4 | Working tree clean | `git status` | No uncommitted changes |
| 5 | Read Design Canon | `synthesis/PROJ-001-e-011-v1-jerry-design-canon.md` | Understand patterns |
| 6 | Read ADR-013 | `decisions/PROJ-001-e-013-v1-adr-shared-kernel.md` | Understand contracts |
| 7 | Read WORKTRACKER | `WORKTRACKER.md` → Current Focus | Know active subtask |

**STOP**: If any check fails, resolve before proceeding.

---

## Stage Execution Order

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ STAGE R: RESEARCH PHASE (R-008d.0)                                              │
│ Duration: ~30 min | Agent: Orchestrator | Parallel: No                          │
│ Input: ADR-013, Design Canon, src/session_management/                           │
│ Output: research/PROJ-001-R-008d-domain-refactoring.md                          │
│ Commit: Yes                                                                     │
└─────────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│ STAGE I.1: VALUE OBJECTS (I-008d.1)                                             │
│ Duration: ~60 min | Agent: Orchestrator | Parallel: No                          │
│ Input: R-008d.0 output                                                          │
│ Output: Updated project_id.py, new tests                                        │
│ Commit: Yes (after each subtask)                                                │
└─────────────────────────────────────────────────────────────────────────────────┘
                                      │
              ┌───────────────────────┴───────────────────────┐
              ▼                                               ▼
┌─────────────────────────────────┐         ┌─────────────────────────────────────┐
│ STAGE I.2: ENTITIES (I-008d.2)  │         │ STAGE I.3: NEW OBJECTS (I-008d.3)   │
│ Duration: ~60 min               │         │ Duration: ~45 min                   │
│ Agent: Worker A                 │  ║      │ Agent: Worker B                     │
│ Parallel: YES (with I-008d.3)   │  ║      │ Parallel: YES (with I-008d.2)       │
│ Input: I-008d.1 output          │  ║      │ Input: R-008d.0 output              │
│ Output: Updated project_info.py │  ║      │ Output: session_id.py, session.py   │
│ Commit: Yes                     │  ║      │ Commit: Yes                         │
└─────────────────────────────────┘         └─────────────────────────────────────┘
              │                                               │
              └───────────────────────┬───────────────────────┘
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│ STAGE I.4: INFRASTRUCTURE (I-008d.4)                                            │
│ Duration: ~45 min | Agent: Orchestrator | Parallel: No                          │
│ Input: I-008d.1, I-008d.2, I-008d.3 outputs                                     │
│ Output: Updated adapters, migration script                                       │
│ Commit: Yes                                                                     │
└─────────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│ STAGE E: EVIDENCE PHASE (E-008d)                                                │
│ Duration: ~15 min | Agent: Orchestrator | Parallel: No                          │
│ Input: All stage outputs                                                        │
│ Output: Full test run, coverage report                                          │
│ Commit: Yes (final)                                                             │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Stage R: Research Phase (R-008d.0)

### Objective
Complete 5W1H analysis and Context7 research before ANY implementation.

### Inputs
| Artifact | Path | Purpose |
|----------|------|---------|
| Design Canon | `synthesis/PROJ-001-e-011-v1-jerry-design-canon.md` | Pattern definitions |
| ADR-013 | `decisions/PROJ-001-e-013-v1-adr-shared-kernel.md` | Implementation spec |
| Current Domain | `src/session_management/domain/` | Gap analysis source |
| Shared Kernel | `src/shared_kernel/` | Target patterns |

### Tasks

| ID | Task | Status | Evidence |
|----|------|--------|----------|
| R.1 | Review ADR-013 implementation spec | ⏳ | Notes in output |
| R.2 | Analyze current ProjectId implementation | ⏳ | Current vs target table |
| R.3 | Analyze current ProjectInfo implementation | ⏳ | Current vs target table |
| R.4 | Context7: Query DDD value object migration | ⏳ | 2+ citations |
| R.5 | Context7: Query entity refactoring patterns | ⏳ | 2+ citations |
| R.6 | Identify breaking changes | ⏳ | Breaking change matrix |
| R.7 | Document file change inventory | ⏳ | MODIFY/CREATE/DELETE list |
| R.8 | Write research artifact | ⏳ | research/PROJ-001-R-008d-*.md |

### Output
```
research/PROJ-001-R-008d-domain-refactoring.md
```

### Commit Checkpoint
```bash
git add research/PROJ-001-R-008d-domain-refactoring.md
git commit -m "research(proj-001): complete R-008d.0 - domain refactoring analysis

- 5W1H analysis for ProjectId/ProjectInfo refactoring
- Context7 research with citations
- Breaking change assessment
- File change inventory

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

### Resume Protocol
If context compacts during R-008d.0:
1. Read `WORKTRACKER.md` → Current Focus
2. Check if `research/PROJ-001-R-008d-domain-refactoring.md` exists
3. If exists: Review completion status in file, continue from incomplete section
4. If not exists: Start fresh from R.1

---

## Stage I.1: Value Object Refactoring (I-008d.1)

### Objective
Refactor ProjectId to extend VertexId, extract slug property.

### Prerequisites
- R-008d.0 COMPLETE ✅

### Inputs
| Artifact | Path | Purpose |
|----------|------|---------|
| Research | `research/PROJ-001-R-008d-domain-refactoring.md` | Implementation guidance |
| Current ProjectId | `src/session_management/domain/value_objects/project_id.py` | Refactor target |
| VertexId | `src/shared_kernel/vertex_id.py` | Base class |

### Subtasks

#### I-008d.1.1: Refactor ProjectId to Extend VertexId

**BDD Cycle**:

| Phase | Action | Files | Tests |
|-------|--------|-------|-------|
| RED | Write failing tests for new ProjectId format | `tests/session_management/unit/test_project_id.py` | 10 |
| GREEN | Update ProjectId to extend VertexId | `src/session_management/domain/value_objects/project_id.py` | - |
| REFACTOR | Clean up, verify no regressions | All affected | - |

**Test Cases (RED phase)**:
```python
# tests/session_management/unit/test_project_id.py (NEW)

def test_project_id_extends_vertex_id():
    """ProjectId should inherit from VertexId base class."""

def test_project_id_generate_creates_valid_format():
    """generate() should create PROJ-{uuid8} format."""

def test_project_id_from_string_parses_valid():
    """from_string() should parse valid PROJ-{uuid8}."""

def test_project_id_rejects_old_format_with_slug():
    """Old format PROJ-NNN-slug should be rejected."""

def test_project_id_rejects_invalid_hex():
    """Invalid hex characters should be rejected."""

# ... (10 tests total per R-008d research)
```

**Implementation (GREEN phase)**:
```python
# src/session_management/domain/value_objects/project_id.py

from src.shared_kernel.vertex_id import VertexId

class ProjectId(VertexId):
    """Project identity extending Shared Kernel VertexId."""
    _prefix = "PROJ"

    # ... implementation per ADR-013
```

**Commit Checkpoint**:
```bash
git add tests/session_management/unit/test_project_id.py src/session_management/domain/value_objects/project_id.py
git commit -m "feat(session-mgmt): refactor ProjectId to extend VertexId (I-008d.1.1)

RED: 10 new tests for ProjectId format
GREEN: ProjectId extends VertexId base
REFACTOR: Format PROJ-{uuid8}, old format rejected

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

#### I-008d.1.2: Extract Slug as Separate Property

**BDD Cycle**:

| Phase | Action | Files | Tests |
|-------|--------|-------|-------|
| RED | Write tests for slug property | `test_project_info.py` | 5 |
| GREEN | Add slug to ProjectInfo | `project_info.py` | - |
| REFACTOR | Update adapter to populate slug | `filesystem_adapter.py` | - |

**Commit Checkpoint**:
```bash
git commit -m "feat(session-mgmt): add slug property to ProjectInfo (I-008d.1.2)"
```

#### T-008d.1.3: Update Value Object Tests

**BDD Cycle**:

| Phase | Action | Files | Tests |
|-------|--------|-------|-------|
| RED | Identify tests failing from format change | All test files | - |
| GREEN | Update test values to new format | Test files | - |
| REFACTOR | Consolidate duplicate tests | Test files | - |

**Commit Checkpoint**:
```bash
git commit -m "test(session-mgmt): update VO tests for new format (T-008d.1.3)"
```

### Stage I.1 Exit Criteria
- [ ] 40 tests pass (existing 57 + new - updated)
- [ ] ProjectId extends VertexId
- [ ] ProjectId format is PROJ-{uuid8}
- [ ] Slug is separate property on ProjectInfo
- [ ] 3 commits created

### Resume Protocol
If context compacts during I-008d.1:
1. Read `WORKTRACKER.md` → Current Focus
2. Run `pytest tests/session_management/unit/test_project_id.py -v`
3. Check commit log: `git log --oneline -5`
4. Identify last completed subtask from commits
5. Continue from next incomplete subtask

---

## Stage I.2 & I.3: Parallel Execution

### Parallel Safety Analysis

| Aspect | I-008d.2 (Entities) | I-008d.3 (New Objects) | Conflict? |
|--------|---------------------|------------------------|-----------|
| Files Modified | `project_info.py` | NEW: `session_id.py`, `session.py` | NO |
| Tests Created | `test_project_info.py` | `test_session_id.py`, `test_session.py` | NO |
| Shared Kernel Usage | EntityBase, IAuditable | VertexId, EntityBase | NO (read-only) |
| Domain Imports | May import SessionId | Imports ProjectId | POTENTIAL |

**Conflict Mitigation**:
- I-008d.3.3 (add session_id to ProjectInfo) MUST wait until I-008d.2 completes
- I-008d.3.1 and I-008d.3.2 can proceed in parallel with I-008d.2

**Merge Strategy**:
If running in parallel sessions:
1. Each session works on separate branch: `cc/008d-2-entities`, `cc/008d-3-new-objects`
2. After both complete: merge into `cc/task-subtask`
3. Run full test suite after merge
4. Resolve any import conflicts

### Stage I.2: Entity Refactoring (I-008d.2)

*[Detailed subtasks I-008d.2.1, I-008d.2.2, I-008d.2.3 follow same pattern as I.1]*

### Stage I.3: New Domain Objects (I-008d.3)

*[Detailed subtasks I-008d.3.1, I-008d.3.2, I-008d.3.3 follow same pattern as I.1]*

---

## Stage I.4: Infrastructure Updates (I-008d.4)

### Prerequisites
- I-008d.1 COMPLETE ✅
- I-008d.2 COMPLETE ✅
- I-008d.3 COMPLETE ✅

### Inputs
| Artifact | Path | Purpose |
|----------|------|---------|
| Updated ProjectId | `src/session_management/domain/value_objects/project_id.py` | New format |
| Updated ProjectInfo | `src/session_management/domain/entities/project_info.py` | New properties |
| New SessionId | `src/session_management/domain/value_objects/session_id.py` | New VO |
| New Session | `src/session_management/domain/aggregates/session.py` | New aggregate |

### Subtasks

#### I-008d.4.1: Update FilesystemProjectAdapter
#### I-008d.4.2: Migrate Existing Projects
#### T-008d.4.3: Update Infrastructure Tests

*[Follow same BDD pattern]*

---

## Stage E: Evidence Phase (E-008d)

### Objective
Verify all tests pass, document evidence, create final commit.

### Tasks

| ID | Task | Command | Expected |
|----|------|---------|----------|
| E.1 | Run Shared Kernel tests | `pytest tests/shared_kernel/ -v` | 58 passed |
| E.2 | Run Session Mgmt unit tests | `pytest tests/session_management/unit/ -v` | 80+ passed |
| E.3 | Run Session Mgmt integration tests | `pytest tests/session_management/integration/ -v` | 12+ passed |
| E.4 | Run architecture tests | `pytest tests/session_management/architecture/ -v` | 5 passed |
| E.5 | Check coverage | `pytest --cov=src/session_management --cov-report=term-missing` | ≥90% |
| E.6 | Verify zero regressions | Compare test count before/after | No decrease |

### Evidence Artifact
```
reports/PROJ-001-E-008d-evidence.md

Contents:
- Test run output (copy/paste)
- Coverage report
- Commit hashes for each stage
- Regression check: before/after test counts
```

### Final Commit
```bash
git add reports/PROJ-001-E-008d-evidence.md
git commit -m "docs(proj-001): complete ENFORCE-008d with evidence

- R-008d.0: Research complete
- I-008d.1-4: Implementation complete
- T-008d: All tests pass (102 tests)
- E-008d: Coverage 92%, zero regressions

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Session Handoff Protocol

When context compaction is imminent or session ends:

### Step 1: Checkpoint Current State
```bash
# 1. Commit any uncommitted work
git add -A
git commit -m "WIP: checkpoint before context compact"

# 2. Note current subtask in WORKTRACKER
```

### Step 2: Update WORKTRACKER
Edit `WORKTRACKER.md`:
```markdown
### Current State (DATE)

- **Active Phase**: I-008d.2 (or wherever you are)
- **Active Subtask**: I-008d.2.1 - Refactor ProjectInfo
- **Last Commit**: abc1234
- **Blocker**: None
- **Next Action**: Continue GREEN phase of I-008d.2.1
```

### Step 3: Resume in New Session

1. Read this file: `runbooks/RUNBOOK-001-008d-domain-refactoring.md`
2. Read `WORKTRACKER.md` → Current Focus
3. Run pre-flight checklist
4. Check `git log --oneline -5` for last commits
5. Run `pytest tests/session_management/ -v` to verify current state
6. Continue from documented subtask

---

## Troubleshooting

### Tests Failing After Refactoring
1. Check if old format tests need updating
2. Verify imports use correct paths (`src.shared_kernel.*`)
3. Check for circular imports

### Merge Conflicts (Parallel Execution)
1. Always merge I-008d.2 first (it modifies existing files)
2. Then merge I-008d.3 (creates new files)
3. Fix any import conflicts manually

### Context Compaction Mid-Subtask
1. The BDD phases (RED/GREEN/REFACTOR) should be atomic
2. If compaction happens mid-phase, restart that phase
3. Tests serve as verification of completion

---

## Validation Checklist

Before declaring ENFORCE-008d complete:

- [ ] R-008d.0 research artifact exists
- [ ] Context7 citations documented (5+)
- [ ] All BDD cycles completed (visible in commit history)
- [ ] 102 tests pass (run full suite)
- [ ] Coverage ≥ 90%
- [ ] Zero regressions (test count same or higher)
- [ ] Architecture tests validate boundaries
- [ ] Evidence artifact created
- [ ] WORKTRACKER updated to show completion
- [ ] PHASE-06-ENFORCEMENT.md verification checklist complete

---

## Document History

| Date | Author | Changes |
|------|--------|---------|
| 2026-01-09 | Claude | Initial creation |
