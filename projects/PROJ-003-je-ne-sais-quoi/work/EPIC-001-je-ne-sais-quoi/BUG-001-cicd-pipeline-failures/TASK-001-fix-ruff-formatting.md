# TASK-001: Fix Ruff Formatting in main.py

<!--
TEMPLATE: Task (DRAFT)
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 0.1.0
CREATED: 2026-02-20 (Claude)
-->

> **Type:** task
> **Status:** done
> **Priority:** high
> **Created:** 2026-02-20
> **Completed:** 2026-02-20
> **Parent:** BUG-001

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Content](#content) | Description and acceptance criteria |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Status changes |

---

## Content

### Description

Run `ruff format` on `src/interface/cli/main.py` to fix the formatting violation detected by CI. The violation was introduced during FEAT-004/EE-008 implementation (the `_handle_why()` function and `jerry why` namespace routing).

### Steps

1. Run `uv run ruff format src/interface/cli/main.py --config=pyproject.toml`
2. Verify: `uv run ruff format --check . --config=pyproject.toml` exits 0
3. Verify: `uv run pytest tests/ -q --tb=short` still passes (3299 tests)

### Acceptance Criteria

- [x] `ruff format --check . --config=pyproject.toml` exits 0 (0 files to reformat)
- [x] All 3299 tests still pass

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Formatted main.py | Code | `src/interface/cli/main.py` |

### Verification

- [x] Acceptance criteria verified
- [x] `ruff format --check` passes

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-20 | pending | Task created. 1 file needs formatting. |
| 2026-02-20 | done | `ruff format` applied. 414 files pass `--check`. |
