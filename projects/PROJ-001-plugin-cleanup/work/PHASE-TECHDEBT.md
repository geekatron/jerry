# Phase TECHDEBT: Technical Debt Tracking

> **Status**: 🔄 IN PROGRESS (80% - 4/5 done)
> **Purpose**: Track technical debt for future resolution

---

## Navigation

| Link | Description |
|------|-------------|
| [← WORKTRACKER](../WORKTRACKER.md) | Back to index |
| [BUGS](PHASE-BUGS.md) | Bug tracking |
| [Phase 6](PHASE-06-ENFORCEMENT.md) | Current phase |

---

## Technical Debt Summary

| ID | Title | Priority | Status | Source |
|----|-------|----------|--------|--------|
| TD-001 | Update ps-* agent output paths | HIGH | ✅ DONE | Phase 7 |
| TD-002 | Update ps-* agent reference paths | MEDIUM | ✅ DONE | BUG-001 |
| TD-003 | Add hook decision value tests | LOW | ✅ DONE | BUG-002 |
| TD-004 | pytest_bdd dependency missing | LOW | ✅ DONE | 008d.3 |
| TD-005 | Misplaced tests in projects/ | MEDIUM | 🔄 IN PROGRESS | ENFORCE-011 |

---

## TD-001: Update ps-* Agent Output Paths ✅

> **Status**: COMPLETED
> **Priority**: HIGH
> **Source**: Phase 7

### Description

The ps-* agents now use `projects/${JERRY_PROJECT}/{category}/` for output paths instead of `docs/{category}/`.

### Files Updated

| File | Output Path |
|------|-------------|
| `ps-researcher.md` | `projects/${JERRY_PROJECT}/research/` |
| `ps-analyst.md` | `projects/${JERRY_PROJECT}/analysis/` |
| `ps-synthesizer.md` | `projects/${JERRY_PROJECT}/synthesis/` |
| `ps-architect.md` | `projects/${JERRY_PROJECT}/decisions/` |
| `ps-validator.md` | `projects/${JERRY_PROJECT}/analysis/` |
| `ps-reporter.md` | `projects/${JERRY_PROJECT}/reports/` |
| `ps-investigator.md` | `projects/${JERRY_PROJECT}/investigations/` |
| `ps-reviewer.md` | `projects/${JERRY_PROJECT}/reviews/` |
| `PS_AGENT_TEMPLATE.md` | Template updated |
| `ORCHESTRATION.md` | Diagram updated |

### Rationale

Per PROJ-001 project isolation principle, all project artifacts belong in the project directory.

---

## TD-002: Update ps-* Agent Reference Paths ✅

> **Status**: COMPLETED (2026-01-10)
> **Priority**: MEDIUM
> **Source**: BUG-001.5

### Description

When ps-* agents generate documents that REFERENCE other documents (e.g., synthesis referencing research), they should use project-centric paths (`projects/${JERRY_PROJECT}/research/...`) not old `docs/` paths.

### Root Cause

TD-001 fixed OUTPUT paths in YAML frontmatter but not REFERENCE paths within document body content.

### Resolution

Updated all 9 ps-* agent files to use project-centric paths throughout:

| File | References Updated |
|------|-------------------|
| `ps-synthesizer.md` | 7 occurrences |
| `ps-analyst.md` | 6 occurrences |
| `ps-reporter.md` | 6 occurrences |
| `ps-researcher.md` | 10 occurrences |
| `ps-architect.md` | 10 occurrences |
| `ps-validator.md` | 10 occurrences |
| `ps-reviewer.md` | 10 occurrences |
| `ps-investigator.md` | 10 occurrences |
| `PS_AGENT_TEMPLATE.md` | 3 occurrences |

### Acceptance Criteria

- [x] ps-synthesizer uses project-relative paths in citations
- [x] ps-analyst uses project-relative paths in references
- [x] ps-reporter uses project-relative paths in links
- [x] Template documents the reference path convention
- [x] All ps-* agents consistently use `projects/${JERRY_PROJECT}/` paths

---

## TD-003: Add Hook Decision Value Tests ✅

> **Status**: COMPLETED (2026-01-10)
> **Priority**: LOW
> **Source**: BUG-002.4

### Description

Add unit tests for `.claude/hooks/pre_tool_use.py` to validate correct decision values (`approve`/`block`) are returned.

### Resolution

Created comprehensive test suite with 23 tests across 4 test classes:

| Class | Tests | Description |
|-------|-------|-------------|
| `TestApproveDecision` | 6 | Verify allowed tools return `approve` |
| `TestBlockDecision` | 8 | Verify dangerous operations return `block` |
| `TestDecisionFormat` | 5 | Verify format matches Claude Code spec |
| `TestEdgeCases` | 4 | Edge case handling (empty input, unknown tools) |

### Test File

`tests/hooks/test_pre_tool_use.py` (304 lines)

### Acceptance Criteria

- [x] Test file created at `tests/hooks/test_pre_tool_use.py`
- [x] All 3 test case categories implemented (expanded to 23 tests)
- [x] Tests pass (1261 total tests in suite)
- [x] CI includes hook tests

---

## Technical Debt Template

When adding new technical debt, use this template:

```markdown
## TD-XXX: [Title]

> **Status**: ⏳ PENDING
> **Priority**: [HIGH|MEDIUM|LOW]
> **Source**: [Where discovered]

### Description
[What is the debt?]

### Root Cause
[Why does this debt exist?]

### Impact
[What happens if we don't fix it?]

### Proposed Solution
[How to address it?]

### Files Affected
| File | Change |
|------|--------|
| | |

### Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]

### Effort Estimate
[T-shirt size: XS/S/M/L/XL]
```

---

## TD-004: pytest_bdd Dependency Missing ✅

> **Status**: COMPLETED (2026-01-10)
> **Priority**: LOW
> **Source**: ENFORCE-008d.3 testing

### Description

`tests/shared_kernel/test_snowflake_id_bdd.py` requires `pytest_bdd` which is not in the project dependencies. This causes test collection to fail when running the full test suite.

### Root Cause

Test file was created with BDD syntax but dependency not added to requirements.

### Impact

- Test collection errors when running `pytest tests/shared_kernel/`
- Must use `--ignore` flag to skip this file
- BDD tests for SnowflakeId are not executing

### Proposed Solution

Either:
1. Add `pytest_bdd` to dev dependencies in `pyproject.toml`
2. Or remove/refactor the BDD test file to use standard pytest

### Files Affected

| File | Change |
|------|--------|
| `pyproject.toml` | Add pytest_bdd to dev dependencies |
| `tests/shared_kernel/test_snowflake_id_bdd.py` | Either enable or refactor |

### Acceptance Criteria

- [ ] Full test suite runs without collection errors
- [ ] BDD tests execute or are properly refactored

### Effort Estimate

XS - Simple dependency addition or file removal

---

## TD-005: Misplaced Tests in projects/ Directory 🔄

> **Status**: IN PROGRESS
> **Priority**: MEDIUM
> **Source**: ENFORCE-011 investigation
> **Started**: 2026-01-10

### Description

Test files exist in `projects/PROJ-001-plugin-cleanup/tests/` which violates the project structure convention. Tests should be in `tests/` at the repository root, not within project workspaces.

### Deep Analysis Results (2026-01-10)

#### Origin

| Attribute | Value |
|-----------|-------|
| Created | 2026-01-09 |
| Commit | `a911859` |
| Author | Claude Opus 4.5 |
| Purpose | BUG-001 regression prevention |

**Finding**: These are NOT temporary tests. They were deliberately created as a comprehensive BUG-001 regression test suite following the test pyramid methodology.

#### Test Inventory

| Category | Tests | Value | Portability | Action |
|----------|-------|-------|-------------|--------|
| Unit (path validation) | 35 | HIGH | Fully portable | **MIGRATE** |
| Architecture (ADR-003) | 14 | HIGH | Portable | **MIGRATE** |
| System (grep validation) | 6 | HIGH | Portable | **MIGRATE** |
| Integration (file resolution) | 22 | MEDIUM | Needs adaptation | **MIGRATE** |
| E2E (traceability) | 8 | MEDIUM | PROJ-001 specific | Archive |
| Contract (schema) | 13 | LOW | PROJ-001 specific | Archive |
| **Total** | **98** | | | |

#### Current State

- 93/98 tests pass (95% pass rate)
- 5 failures due to project evolution (new directories, new document formats)
- Tests NOT running in CI (not in `pytest.ini` testpaths)

### Root Cause

Created on 2026-01-09 as BUG-001 regression tests. Located in `projects/` because they validate project documentation - but this violates the convention that `projects/` should only contain research/design artifacts, not code.

### Impact

- Tests not running as part of CI
- Violates established convention
- Valuable regression tests being wasted

### Execution Plan (Option A: Migrate Valuable Tests)

#### Phase 1: Setup
- [ ] Create `tests/project_validation/` directory structure
- [ ] Create shared fixtures in `tests/project_validation/conftest.py`

#### Phase 2: Migrate Portable Tests (~60 tests)
- [ ] Migrate `test_path_validation.py` → `tests/project_validation/unit/`
- [ ] Migrate `test_path_conventions.py` → `tests/project_validation/architecture/`
- [ ] Migrate `test_grep_validation.py` → `tests/project_validation/system/`
- [ ] Parameterize tests to work with any `PROJ-*` directory dynamically

#### Phase 3: Archive PROJ-001 Specific Tests
- [ ] Document archived tests in this file
- [ ] Remove `projects/PROJ-001-plugin-cleanup/tests/` directory

#### Phase 4: CI Integration
- [ ] Verify migrated tests run in main test suite
- [ ] Update pytest.ini if needed
- [ ] Document test execution strategy

### Files Affected

| Source | Destination | Action |
|--------|-------------|--------|
| `projects/.../tests/unit/test_path_validation.py` | `tests/project_validation/unit/` | Migrate + parameterize |
| `projects/.../tests/architecture/test_path_conventions.py` | `tests/project_validation/architecture/` | Migrate + parameterize |
| `projects/.../tests/system/test_grep_validation.py` | `tests/project_validation/system/` | Migrate + parameterize |
| `projects/.../tests/integration/test_file_resolution.py` | `tests/project_validation/integration/` | Migrate + adapt |
| `projects/.../tests/e2e/test_document_traceability.py` | Archive | Document & remove |
| `projects/.../tests/contract/test_document_schema.py` | Archive | Document & remove |
| `projects/.../tests/conftest.py` | Merge into new conftest | Migrate fixtures |

### Acceptance Criteria

- [ ] All valuable tests migrated to `tests/project_validation/`
- [ ] Tests parameterized for dynamic project discovery
- [ ] Archived tests documented
- [ ] No test files remain in `projects/*/`
- [ ] Migrated tests pass (target: ~60 tests)
- [ ] Tests included in main test suite run

### Effort Estimate

S - 2-3 hours for extraction, parameterization, and verification

---

## Document History

| Date | Author | Changes |
|------|--------|---------|
| 2026-01-09 | Claude | Initial creation |
| 2026-01-09 | Claude | Migrated to multi-file format |
| 2026-01-10 | Claude | Added TD-004: pytest_bdd dependency |
| 2026-01-10 | Claude | Added TD-005: Misplaced tests in projects/ |
| 2026-01-10 | Claude | Completed TD-002: All 9 ps-* agents updated |
| 2026-01-10 | Claude | TD-005: Deep analysis complete, execution plan defined |
