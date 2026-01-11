# Phase TECHDEBT: Technical Debt Tracking

> **Status**: ⏳ PENDING (25% - 1/4 done)
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
| TD-002 | Update ps-* agent reference paths | MEDIUM | ⏳ PENDING | BUG-001 |
| TD-003 | Add hook decision value tests | LOW | ⏳ PENDING | BUG-002 |
| TD-004 | pytest_bdd dependency missing | LOW | ⏳ PENDING | 008d.3 |

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

## TD-002: Update ps-* Agent Reference Paths ⏳

> **Status**: PENDING
> **Priority**: MEDIUM
> **Source**: BUG-001.5

### Description

When ps-* agents generate documents that REFERENCE other documents (e.g., synthesis referencing research), they should use project-centric paths (`projects/PROJ-001-plugin-cleanup/research/...`) not old `docs/` paths.

### Root Cause

TD-001 fixed OUTPUT paths but not REFERENCE paths within document content.

### Impact

Without this fix, new documents will continue to have broken lineage references.

### Files to Update

| File | Change Required |
|------|-----------------|
| `ps-synthesizer.md` | Update source citation format |
| `ps-analyst.md` | Update reference format |
| `ps-reporter.md` | Update document link format |
| `PS_AGENT_TEMPLATE.md` | Add reference path guidance |

### Acceptance Criteria

- [ ] ps-synthesizer uses project-relative paths in citations
- [ ] ps-analyst uses project-relative paths in references
- [ ] ps-reporter uses project-relative paths in links
- [ ] Template documents the reference path convention
- [ ] Tests validate reference paths

---

## TD-003: Add Hook Decision Value Tests ⏳

> **Status**: PENDING
> **Priority**: LOW
> **Source**: BUG-002.4

### Description

Add unit tests for `.claude/hooks/pre_tool_use.py` to validate correct decision values (`approve`/`block`) are returned.

### Rationale

Prevent regression if hook is modified in future.

### Test Cases

| Test | Description |
|------|-------------|
| `test_approve_decision_for_allowed_tools` | Verify allowed tools return `approve` |
| `test_block_decision_for_denied_tools` | Verify denied tools return `block` |
| `test_decision_format_matches_spec` | Verify format matches Claude Code spec |

### Acceptance Criteria

- [ ] Test file created at `tests/hooks/test_pre_tool_use.py`
- [ ] All 3 test cases implemented
- [ ] Tests pass
- [ ] CI includes hook tests

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

## TD-004: pytest_bdd Dependency Missing ⏳

> **Status**: PENDING
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

## Document History

| Date | Author | Changes |
|------|--------|---------|
| 2026-01-09 | Claude | Initial creation |
| 2026-01-09 | Claude | Migrated to multi-file format |
| 2026-01-10 | Claude | Added TD-004: pytest_bdd dependency |
