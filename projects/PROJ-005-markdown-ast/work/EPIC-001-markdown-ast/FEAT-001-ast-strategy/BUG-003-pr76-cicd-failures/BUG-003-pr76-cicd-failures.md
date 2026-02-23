# BUG-003: CI/CD failures on PR #76 — lint errors + Windows test failures

> **Type:** bug
> **Status:** resolved
> **Priority:** high
> **Impact:** high
> **Severity:** major
> **Created:** 2026-02-23
> **Parent:** FEAT-001-ast-strategy
> **Owner:** Claude
> **Found In:** feature/PROJ-005-ast-universal-markdown-parser @ 25543998
> **GitHub Issue:** PR #76

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Bug overview |
| [Failure Analysis](#failure-analysis) | Categorized CI failures |
| [Root Cause Analysis](#root-cause-analysis) | Two distinct root causes |
| [Acceptance Criteria](#acceptance-criteria) | Fix verification conditions |
| [Tasks](#tasks) | Fix tasks |
| [Related Items](#related-items) | Links to PR, CI runs |

---

## Summary

PR #76 (`feature/PROJ-005-ast-universal-markdown-parser`) has 6 failing CI jobs across two categories:

1. **Lint & Format** (1 job): 8 ruff violations in new Phase 3 source and test files
2. **Windows Tests** (4 jobs): 4 `TestAstModify` tests failing on all Windows matrix combinations (pip/uv x 3.13/3.14)
3. **CI Success** (1 job): Gate job fails due to upstream failures

All Linux, macOS, and non-AST-modify tests pass. This is a merge blocker.

---

## Failure Analysis

### Lint Errors (8 violations)

| Rule | File | Line | Description |
|------|------|------|-------------|
| B905 | `src/domain/markdown_ast/document_type.py` | 282 | `zip()` without `strict=` |
| B905 | `src/domain/markdown_ast/document_type.py` | 293 | `zip()` without `strict=` |
| F401 | `tests/regression/test_golden_files.py` | 22 | Unused import `DocumentTypeDetector` |
| F811 | `tests/regression/test_golden_files.py` | 175 | Redefinition of `DocumentTypeDetector` |
| F541 | `tests/regression/test_golden_files.py` | 209 | f-string without placeholders |
| B905 | `tests/regression/test_golden_files.py` | 152 | `zip()` without `strict=` |
| I001 | `tests/security/test_adversarial_parsers.py` | 14 | Import block unsorted |
| I001 | `tests/security/test_redos_patterns.py` | 138 | Import block unsorted |
| I001 | `tests/unit/domain/markdown_ast/test_document_type.py` | 19 | Import block unsorted |
| I001 | `tests/unit/domain/markdown_ast/test_html_comment.py` | 24 | Import block unsorted |
| I001 | `tests/unit/domain/markdown_ast/test_schema_registry.py` | 19 | Import block unsorted |

### Windows Test Failures (4 tests x 4 matrix jobs = 16 failures)

| Test | Error | Root Cause |
|------|-------|------------|
| `TestAstModify::test_modify_returns_exit_code_0` | `assert 2 == 0` | `os.rename()` fails on Windows |
| `TestAstModify::test_modify_writes_file_back` | `assert 'done' in content` | File not modified (rename failed) |
| `TestAstModify::test_modify_outputs_json_status` | `JSONDecodeError` | No JSON output (rename error) |
| `TestMainAstRouting::test_main_routes_ast_modify` | `assert 2 == 0` | Same `os.rename()` issue |

---

## Root Cause Analysis

### Root Cause 1: Lint violations in new Phase 3 files

New source files and tests introduced in Phase 3 have ruff violations that were not caught by local pre-commit hooks (hooks check staged files only; CI checks entire repo). Violations are auto-fixable (`ruff check --fix` + `ruff format`).

### Root Cause 2: Windows `os.rename()` cannot replace existing files

`ast_commands.py:534` uses `os.rename(temp_path_str, str(target_path))` for atomic write. On Unix, `os.rename()` atomically replaces the target. On Windows, `os.rename()` raises `OSError` if the target file already exists. The fix is to use `os.replace()` which works cross-platform (atomically replaces on both Unix and Windows, available since Python 3.3).

---

## Acceptance Criteria

- [x] CI "Lint & Format" job passes (0 ruff errors)
- [x] All Windows test matrix jobs pass (0 failures)
- [x] CI "CI Success" gate job passes
- [x] PR #76 is mergeable
- [x] No regressions on Linux/macOS test suites

---

## Tasks

| ID | Task | Status |
|----|------|--------|
| TASK-001 | Fix ruff lint violations (auto-fix + manual cleanup) | completed |
| TASK-002 | Replace `os.rename()` with `os.replace()` in `ast_commands.py` | completed |
| TASK-003 | Verify all CI jobs pass after fixes | completed |

---

## Related Items

### Hierarchy

- **Parent:** [FEAT-001-ast-strategy](../FEAT-001-ast-strategy.md)

### Related Items

- **PR:** [#76](https://github.com/geekatron/jerry/pull/76)
- **CI Run:** GitHub Actions run 22315031135
- **Prior Bug:** BUG-001 (similar CI failures, different root causes, completed)
