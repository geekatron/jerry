# BUG-011: Pre-commit pytest hook only triggers on Python file changes

> **Type:** bug
> **Status:** done
> **Priority:** high
> **Impact:** high
> **Severity:** major
> **Created:** 2026-02-11
> **Due:** —
> **Completed:** 2026-02-11
> **Parent:** EN-004
> **Owner:** —
> **Found In:** —
> **Fix Version:** —

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and key details |
| [Reproduction Steps](#reproduction-steps) | Steps to reproduce the issue |
| [Environment](#environment) | Environment where bug occurs |
| [Root Cause Analysis](#root-cause-analysis) | Investigation and root cause |
| [Acceptance Criteria](#acceptance-criteria) | Conditions for bug to be fixed |
| [Children](#children) | Tasks to resolve this bug |
| [Related Items](#related-items) | Hierarchy and related items |
| [History](#history) | Status changes |

---

## Summary

The pytest pre-commit hook in `.pre-commit-config.yaml` (line 75) uses `types: [python]`, which means it only triggers when Python files are staged. Commits that only modify markdown files (`.md`) skip the entire test suite, including architecture tests that validate markdown content (e.g., `test_no_hardcoded_absolute_paths`, `test_no_cross_project_references`). This creates a blind spot where markdown-only commits bypass local quality gates and only fail in CI.

**Key Details:**
- **Symptom:** Markdown-only commits pass pre-commit hooks locally but fail architecture tests in CI
- **Frequency:** Every commit that modifies only markdown files (common in worktracker/documentation work)
- **Workaround:** Manually run `uv run pytest tests/project_validation/` before committing markdown changes

---

## Reproduction Steps

### Prerequisites

- Pre-commit hooks installed (`uv run pre-commit install`)

### Steps to Reproduce

1. Modify only a markdown file (e.g., add a hardcoded absolute path to a worktracker entity)
2. Stage the change: `git add projects/PROJ-001-oss-release/work/.../*.md`
3. Commit: `git commit -m "update docs"`
4. Observe: pre-commit hooks run but pytest is **skipped** (no Python files staged)
5. Push to remote — CI runs full test suite and fails on architecture tests

### Expected Result

The pytest hook runs on markdown-only commits, catching architecture test violations before they reach CI.

### Actual Result

The pytest hook is skipped entirely. The commit succeeds locally. CI fails.

---

## Environment

| Attribute | Value |
|-----------|-------|
| **Repository** | geekatron/jerry |
| **File** | `.pre-commit-config.yaml` |
| **Hook** | `pytest` (lines 69-81) |
| **Configuration** | `types: [python]` (line 75) |
| **Affected Tests** | `tests/project_validation/architecture/test_path_conventions.py` |

---

## Root Cause Analysis

### Root Cause

The `types: [python]` filter on the pytest pre-commit hook was a reasonable default when the test suite only validated Python code. However, the architecture test suite now includes tests that validate markdown file content within `projects/` directories:

- `test_no_hardcoded_absolute_paths` — scans `.md` files for hardcoded absolute path patterns
- `test_no_cross_project_references` — scans for cross-project path leakage
- `test_synthesis_contains_canon_doc` — validates synthesis directory content

These tests run against markdown files but are only triggered by the pytest hook, which requires Python file changes.

### Contributing Factors

- The pytest hook was configured before architecture tests were added for markdown validation
- `types: [python]` is the pre-commit default for Python test runners
- No separate hook exists for project validation tests
- The gap was masked when Python and markdown files were committed together (common case)

---

## Acceptance Criteria

### Fix Verification

- [x] Markdown-only commits trigger the pytest hook (or a separate project validation hook)
- [x] Architecture tests that validate markdown content run locally before CI
- [x] Python-only commits continue to work as before
- [x] Hook execution time remains reasonable (no unnecessary double-runs)
- [x] Configuration is documented in `.pre-commit-config.yaml` comments

### Quality Checklist

- [x] Existing tests still passing
- [x] No new issues introduced
- [x] Pre-commit hook configuration validated with `pre-commit run --all-files`

---

## Children

| ID | Title | Status | Priority |
|----|-------|--------|----------|
| [TASK-001](./BUG-011--TASK-001-add-markdown-to-pytest-trigger.md) | Add markdown file types to pytest pre-commit hook trigger | done | high |

---

## Related Items

### Hierarchy

- **Parent:** [EN-004: Fix Pre-commit Hook Coverage](./EN-004-fix-precommit-hook-coverage.md)

### Related Bugs

- **BUG-010:** Session start hook warns but doesn't auto-install pre-commit hooks — related pre-commit gap

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-11 | Claude | pending | Bug filed after markdown content fix caused CI failure that was not caught locally. Root cause: pytest hook `types: [python]` skips markdown-only commits. |
| 2026-02-11 | Claude | done | Resolved via TASK-001: `types_or: [python, markdown]` applied per DEC-002. All AC verified. |
