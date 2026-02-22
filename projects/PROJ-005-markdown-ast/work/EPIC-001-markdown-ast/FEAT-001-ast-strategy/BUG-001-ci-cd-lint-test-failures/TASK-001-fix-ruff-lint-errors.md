# TASK-001: Fix ruff lint errors in r01_poc.py

> **Type:** task
> **Status:** completed
> **Priority:** high
> **Created:** 2026-02-21
> **Completed:** 2026-02-22
> **Parent:** BUG-001-ci-cd-lint-test-failures
> **Owner:** Claude
> **Effort:** 1

---

## Summary

Fix or exclude the 32 ruff lint errors in `r01_poc.py` that cause the CI "Lint & Format" job to fail.

## Acceptance Criteria

- [x] `ruff check .` returns 0 errors
- [x] CI "Lint & Format" job passes
- [x] Approach chosen: exclude PoC path from ruff, fix inline, or delete file

## Delivery Evidence

### Approach

Exclude PoC from ruff + fix 22 pre-existing lint errors across the codebase.

### Changes

| File | Change | Category |
|------|--------|----------|
| `pyproject.toml` | Added ruff exclude: `projects/*/work/**/EN-*/r01_poc.py` | Exclude PoC |
| 6 test files | Auto-fixed via `ruff --fix` (I001, F401, F541) | Auto-fix |
| `scripts/st007_migration_comparison.py` | `# noqa: E402` + `_entity_type` unused var | Manual fix |
| `skills/ast/scripts/ast_ops.py` | Added `from err` for exception chaining (B904) | Manual fix |
| `tests/unit/interface/cli/test_ast_commands.py` | Removed unused `mock_stdout` binding (F841) | Manual fix |
| `tests/unit/scripts/test_st010_remaining_migrations.py` | `_i` unused loop var (B007) | Manual fix |
| `tests/integration/cli/test_ast_subprocess.py` | `ruff format` applied | Formatting |

### Verification

- `uv run ruff check .` — "All checks passed!"
- CI "Lint & Format" job: passed (run 22267538092)
- Commit: `9b34ca8`
