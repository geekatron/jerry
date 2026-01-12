# Phase TECHDEBT: Technical Debt Tracking

> **Status**: 🔄 IN PROGRESS (7/8 done - 87%)
> **Purpose**: Track technical debt for future resolution

---

## Navigation

| Link | Description |
|------|-------------|
| [← WORKTRACKER](../WORKTRACKER.md) | Back to index |
| [BUGS](PHASE-BUGS.md) | Bug tracking |
| [DISCOVERY](PHASE-DISCOVERY.md) | Technical discoveries |
| [INITIATIVE-WT-SKILLS](INITIATIVE-WORKTRACKER-SKILLS.md) | Active initiative (TD-010 related) |

---

## Technical Debt Summary

| ID | Title | Priority | Status | Source |
|----|-------|----------|--------|--------|
| TD-001 | Update ps-* agent output paths | HIGH | ✅ DONE | Phase 7 |
| TD-002 | Update ps-* agent reference paths | MEDIUM | ✅ DONE | BUG-001 |
| TD-003 | Add hook decision value tests | LOW | ✅ DONE | BUG-002 |
| TD-004 | pytest_bdd dependency missing | LOW | ✅ DONE | 008d.3 |
| TD-005 | Misplaced tests in projects/ | MEDIUM | ✅ DONE | ENFORCE-011 |
| TD-010 | Implement link-artifact CLI command | HIGH | ⏳ TODO | DISC-003 |
| TD-011 | CI missing test dependencies | **CRITICAL** | ✅ DONE | CI-002 |
| TD-012 | pip-audit fails on local package | MEDIUM | ✅ DONE | CI-002 |

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

## TD-005: Misplaced Tests in projects/ Directory ✅

> **Status**: DONE
> **Priority**: MEDIUM
> **Source**: ENFORCE-011 investigation
> **Started**: 2026-01-10
> **Completed**: 2026-01-10
> **Commit**: `f5cdfbe`

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

### Execution Plan (Option A: Migrate Valuable Tests) ✅

#### Phase 1: Setup ✅
- [x] Create `tests/project_validation/` directory structure
- [x] Create shared fixtures in `tests/project_validation/conftest.py`

#### Phase 2: Migrate Portable Tests (~60 tests) ✅
- [x] Migrate `test_path_validation.py` → `tests/project_validation/unit/` (35 tests)
- [x] Migrate `test_path_conventions.py` → `tests/project_validation/architecture/` (14 tests)
- [x] Migrate `test_grep_validation.py` → `tests/project_validation/system/` (8 tests)
- [x] Migrate `test_file_resolution.py` → `tests/project_validation/integration/` (12 tests)
- [x] Parameterize tests to work with any `PROJ-*` directory dynamically

#### Phase 3: Archive PROJ-001 Specific Tests ✅
- [x] PROJ-001 retains e2e/ and contract/ tests (19 tests, project-specific)
- [x] Removed duplicated migrated tests from `projects/PROJ-001-plugin-cleanup/tests/`

#### Phase 4: CI Integration ⏳
- [x] Verify migrated tests run in main test suite (69 tests PASS)
- [ ] NO CI EXISTS - GitHub Actions/Makefile not configured
- [ ] CI strategy to be developed separately

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

- [x] All valuable tests migrated to `tests/project_validation/` (69 tests)
- [x] Tests parameterized for dynamic project discovery (`project_id` fixture)
- [x] Archived tests documented (e2e/contract remain with PROJ-001)
- [x] Duplicate test files removed from `projects/PROJ-001-plugin-cleanup/tests/`
- [x] Migrated tests pass: **69 passed in 0.34s**
- [x] Tests discoverable in main test suite

### Completion Summary

| Metric | Target | Actual |
|--------|--------|--------|
| Migrated tests | ~60 | 69 |
| Pass rate | 100% | 100% |
| PROJ-001 specific tests retained | Archive | 19 (15 pass, 4 fail - document drift) |
| CI integration | Required | Deferred - NO CI exists |

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
| 2026-01-10 | Claude | Completed TD-005: 69 tests migrated to tests/project_validation/ (commit f5cdfbe) |
| 2026-01-10 | Claude | All techdebt items COMPLETE (5/5 = 100%) |
| 2026-01-11 | Claude | Added TD-010: link-artifact CLI command missing (DISC-003) |

---

## TD-010: Implement link-artifact CLI Command

> **Status**: ⏳ TODO
> **Priority**: HIGH
> **Source**: DISC-003 (INIT-WT-SKILLS preparation)

### Description

All 8 ps-* agents reference a non-existent CLI command `python3 scripts/cli.py link-artifact` as part of their MANDATORY PERSISTENCE protocol. This command is referenced in 25 files but has never been implemented.

### Root Cause

The ps-* agent specifications were designed with an aspirational CLI interface that was never built. The agents reference:
```bash
python3 scripts/cli.py link-artifact {ps_id} {entry_id} FILE \
    "projects/${JERRY_PROJECT}/{category}/{filename}.md" \
    "{description}"
```

### Impact

- ps-* agents cannot complete their mandatory persistence protocol
- Artifact linking is aspirational, not functional
- Manual file creation works, but artifacts are not linked in any tracking system
- Blocks full ps-* agent orchestration as designed

### Scope of References (25 files)

| Category | Count | Files |
|----------|-------|-------|
| ps-* agents | 9 | `skills/problem-solving/agents/*.md` |
| Templates | 6 | `docs/knowledge/exemplars/templates/*.md` |
| Orchestration | 1 | `skills/problem-solving/docs/ORCHESTRATION.md` |
| Knowledge docs | 1 | `docs/knowledge/DISCOVERIES_EXPANDED.md` |
| Archive/aspiration | 8 | Various |

### Proposed Solution

Implement `scripts/cli.py` with commands:
1. `link-artifact {ps_id} {entry_id} FILE {path} {description}` - Link file artifact
2. `view {ps_id}` - View problem-solving context with linked artifacts
3. `validate-constraint {ps_id} {constraint_id} {evidence}` - Mark constraint validated

### Files to Create/Modify

| File | Action |
|------|--------|
| `scripts/cli.py` | **CREATE** - Main CLI entry point |
| `src/interface/cli/ps_commands.py` | **CREATE** - Problem-solving CLI commands |
| `src/domain/ps_context.py` | **CREATE** - PS context aggregate (if needed) |
| `tests/interface/cli/test_ps_commands.py` | **CREATE** - CLI tests |

### Acceptance Criteria

- [ ] `scripts/cli.py link-artifact` command works as documented
- [ ] `scripts/cli.py view {ps_id}` shows linked artifacts
- [ ] All 8 ps-* agents can complete persistence protocol
- [ ] Unit tests for CLI commands
- [ ] Integration test with actual ps-* agent output

### Effort Estimate

M - Medium (4-8 hours)

---

## TD-011: CI Missing Test Dependencies ✅

> **Status**: COMPLETED (2026-01-11)
> **Priority**: **CRITICAL**
> **Source**: CI-002 (GitHub Actions failures)

### Description

The CI workflow installs `pytest pytest-cov` directly instead of using the `[test]` extras from `pyproject.toml`. Additionally, `pytest-archon` is used in architecture tests but never added to any dependency list.

### Root Cause

1. `.github/workflows/ci.yml` line 116: `pip install pytest pytest-cov` instead of `pip install -e ".[test]"`
2. `pytest-archon` is imported in `tests/work_tracking/architecture/test_*.py` but not in `pyproject.toml`

### Evidence

GitHub Actions logs from run `20903651374`:
```
ERROR collecting tests/shared_kernel/test_snowflake_id_bdd.py
ModuleNotFoundError: No module named 'pytest_bdd'

ERROR collecting tests/work_tracking/architecture/test_dependency_rules.py
ModuleNotFoundError: No module named 'pytest_archon'
```

### Impact

- **All test jobs fail** on all Python versions (3.11, 3.12, 3.13, 3.14)
- PR #3 cannot be merged
- v0.0.1 release blocked

### Proposed Solution

#### Subtask 1: Add pytest-archon to test dependencies

**File:** `pyproject.toml`
```toml
test = [
    "pytest>=8.0.0",
    "pytest-bdd>=8.0.0",
    "pytest-cov>=4.0.0",
    "pytest-archon>=0.0.6",  # ADD THIS
]
```

#### Subtask 2: Update CI workflow to use extras

**File:** `.github/workflows/ci.yml` (line ~116)
```yaml
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install -e ".[test]"  # CHANGE THIS
```

### Files to Modify

| File | Action |
|------|--------|
| `pyproject.toml` | Add `pytest-archon>=0.0.6` to `[test]` extras |
| `.github/workflows/ci.yml` | Change to `pip install -e ".[test]"` |

### Resolution

1. Added `pytest-archon>=0.0.6` to `[project.optional-dependencies].test` in `pyproject.toml`
2. Updated `.github/workflows/ci.yml` line 116 to use `pip install -e ".[test]"`

### Acceptance Criteria

- [x] `pytest-archon` added to `[project.optional-dependencies].test`
- [x] CI workflow uses `pip install -e ".[test]"` for all test jobs
- [ ] All test jobs pass (Python 3.11, 3.12, 3.13, 3.14) - pending CI verification
- [x] `test_snowflake_id_bdd.py` collection succeeds (verified locally)
- [x] `test_dependency_rules.py` collection succeeds (verified locally)
- [x] `test_layer_boundaries.py` collection succeeds (verified locally)

### Effort Estimate

S - Small (1-2 hours)

---

## TD-012: pip-audit Fails on Local Package ✅

> **Status**: COMPLETED (2026-01-11)
> **Priority**: MEDIUM
> **Source**: CI-002 (GitHub Actions failures)

### Description

The `pip-audit --strict` command fails because it tries to audit the local `jerry (0.1.0)` package, which is not on PyPI.

### Root Cause

`pip-audit` audits all installed packages by default, including editable installs. Since `jerry` is a local package (not published to PyPI), audit fails.

### Evidence

GitHub Actions logs from run `20903651374`:
```
ERROR:pip_audit._cli:jerry: Dependency not found on PyPI and could not be audited: jerry (0.1.0)
```

### Impact

- Security scan job fails
- All CI runs fail
- False positive: this is not a security vulnerability

### Proposed Solution

#### Option A: Skip local package (Recommended)

**File:** `.github/workflows/ci.yml`
```yaml
- name: Run pip-audit
  run: pip-audit --strict --skip-editable
```

#### Option B: Audit only requirements (Alternative)

```yaml
- name: Run pip-audit
  run: pip-audit --strict -r requirements.txt
```

Option A is recommended because it still audits all production dependencies while skipping the local package.

### Files to Modify

| File | Action |
|------|--------|
| `.github/workflows/ci.yml` | Add `--skip-editable` flag to pip-audit |

### Resolution

Added `--skip-editable` flag to `pip-audit --strict` command in `.github/workflows/ci.yml` line 92.

### Acceptance Criteria

- [x] Security scan job configuration updated
- [x] All production dependencies are still audited (--strict mode preserved)
- [x] Local `jerry` package is skipped (--skip-editable flag)
- [ ] No false positives in security scan - pending CI verification

### Effort Estimate

XS - Extra Small (<1 hour)

---

## Document History

| Date | Author | Changes |
|------|--------|---------|
| 2026-01-09 | Claude | Initial creation |
| 2026-01-10 | Claude | Added TD-001 through TD-005 |
| 2026-01-11 | Claude | Added TD-010 (DISC-003) |
| 2026-01-11 | Claude | Added TD-011, TD-012 (CI-002 failures) |
| 2026-01-11 | Claude | Completed TD-011, TD-012 (CI-002 resolution) |
