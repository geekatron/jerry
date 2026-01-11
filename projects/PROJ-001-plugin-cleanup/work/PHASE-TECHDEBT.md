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
| TD-005 | Misplaced tests in projects/ | MEDIUM | ⏳ PENDING | ENFORCE-011 |

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

## TD-005: Misplaced Tests in projects/ Directory ⏳

> **Status**: PENDING
> **Priority**: MEDIUM
> **Source**: ENFORCE-011 investigation

### Description

Test files exist in `projects/PROJ-001-plugin-cleanup/tests/` which violates the project structure convention. Tests should be in `tests/` at the repository root, not within project workspaces.

### Files Found

| File | Lines | Purpose |
|------|-------|---------|
| `tests/unit/test_path_validation.py` | 292 | Path validation logic |
| `tests/contract/test_document_schema.py` | 270 | Document schema validation |
| `tests/integration/test_file_resolution.py` | 227 | File resolution tests |
| `tests/system/test_grep_validation.py` | 178 | Grep validation tests |
| `tests/architecture/test_path_conventions.py` | 270 | Path convention tests |
| `tests/e2e/test_document_traceability.py` | 263 | Document traceability |
| **Total** | **~1,500** | |

### Root Cause

Likely created during earlier skill development or path validation work. The tests appear to validate project documentation conventions rather than session_management code.

### Impact

- Confusing project structure
- Tests not running as part of CI (not in `tests/` root)
- Violates established convention: `projects/` for research/design only

### Proposed Solution

1. Review each test file to understand its purpose
2. If valid: Move to appropriate location in `tests/`
3. If obsolete: Remove with documentation
4. Update any imports/paths

### Files Affected

| Location | Action |
|----------|--------|
| `projects/PROJ-001-plugin-cleanup/tests/` | Remove directory after migration |
| `tests/project_validation/` | Potential new home if tests are valid |

### Acceptance Criteria

- [ ] All test files reviewed for relevance
- [ ] Valid tests migrated to `tests/` directory
- [ ] Obsolete tests removed
- [ ] No test files remain in `projects/*/`
- [ ] CI runs migrated tests

### Effort Estimate

S - Requires review and migration of ~1,500 lines

---

## Document History

| Date | Author | Changes |
|------|--------|---------|
| 2026-01-09 | Claude | Initial creation |
| 2026-01-09 | Claude | Migrated to multi-file format |
| 2026-01-10 | Claude | Added TD-004: pytest_bdd dependency |
| 2026-01-10 | Claude | Added TD-005: Misplaced tests in projects/ |
| 2026-01-10 | Claude | Completed TD-002: All 9 ps-* agents updated |
