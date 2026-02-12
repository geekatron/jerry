# TASK-001: Improve session hook warning to reference `make setup`

> **Type:** task
> **Status:** done
> **Priority:** low
> **Created:** 2026-02-11
> **Completed:** 2026-02-11
> **Parent:** BUG-010
> **Owner:** —
> **Activity:** DEVELOPMENT

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Content](#content) | Description and acceptance criteria |
| [Evidence](#evidence) | Deliverables and verification |
| [Related Items](#related-items) | Parent and related work |
| [History](#history) | Status changes |

---

## Content

### Description

~~Modify `scripts/session_start_hook.py` to auto-install pre-commit hooks when they are missing.~~

**Revised (DEC-001):** Update the warning message in `check_precommit_hooks()` (lines 134-137) to reference `make setup` as the primary remediation action, with the Windows fallback (`uv sync && uv run pre-commit install`).

**Why Revised:** Research via /problem-solving agents revealed that the auto-install approach is unnecessary because:
1. `make setup` (Makefile lines 16-22) already handles installation
2. CONTRIBUTING.md (lines 11-30) documents it as a required first step
3. The session hook's detect-and-warn role is intentional (separation of concerns)
4. Auto-installing during session start adds subprocess overhead and side effects

### Acceptance Criteria

- [x] Warning message references `make setup` as primary action
- [x] Warning includes Windows fallback
- [x] No auto-install subprocess calls added
- [x] Existing tests pass

### Implementation

**Before** (lines 134-137):
```python
return (
    "Pre-commit hooks are NOT installed. Tests will not run before commits.\n"
    "Run 'uv run pre-commit install' to install hooks."
)
```

**After:**
```python
return (
    "Pre-commit hooks are NOT installed. Tests will not run before commits.\n"
    "Run 'make setup' to install dependencies and hooks.\n"
    "(Windows: uv sync && uv run pre-commit install)"
)
```

### Files Involved

| File | Change Description |
|------|-------------------|
| `scripts/session_start_hook.py` | Update warning text in `check_precommit_hooks()` (lines 134-137) |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Updated warning text | Code | `scripts/session_start_hook.py:134-137` |
| Decision document | Decision | [DEC-001](./DEC-001-precommit-installation-strategy.md) |

### Verification

- [x] Warning references `make setup`
- [x] Warning includes Windows fallback
- [x] `uv run pytest tests/` passes
- [x] No auto-install logic added

---

## Related Items

- Parent: [BUG-010: Session start hook warning doesn't reference `make setup`](./BUG-010-session-hook-no-auto-install.md)
- Decision: [DEC-001: Pre-commit Hook Installation Strategy](./DEC-001-precommit-installation-strategy.md)
- Enabler: [EN-004: Fix Pre-commit Hook Coverage](./EN-004-fix-precommit-hook-coverage.md)
- Feature: [FEAT-001: Fix CI Build Failures](../FEAT-001-fix-ci-build-failures.md)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-11 | pending | Task created (original: auto-install pre-commit hooks). |
| 2026-02-11 | done | Revised via DEC-001: auto-install rejected. Task reduced to warning message improvement. Implementation is a 1-line text change. |
