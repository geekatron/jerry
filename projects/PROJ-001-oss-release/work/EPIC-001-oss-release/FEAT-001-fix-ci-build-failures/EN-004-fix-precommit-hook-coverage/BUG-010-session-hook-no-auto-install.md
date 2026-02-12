# BUG-010: Session start hook warning doesn't reference `make setup`

> **Type:** bug
> **Status:** done
> **Priority:** low
> **Impact:** low
> **Severity:** minor
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

~~The session start hook should auto-install pre-commit hooks when missing.~~

**Revised (DEC-001):** The session start hook's detect-and-warn behavior is correct by design. The pre-commit hook installation mechanism already exists via `make setup` (Makefile lines 16-22), documented in CONTRIBUTING.md (lines 11-30) and INSTALLATION.md (lines 374-407). The only issue is that the warning message (line 134-137) references the raw command `uv run pre-commit install` instead of the documented `make setup` mechanism.

**Original Filing Error:** BUG-010 was filed without researching existing infrastructure. The Makefile, CONTRIBUTING.md, and INSTALLATION.md were not examined, leading to the incorrect conclusion that no installation mechanism existed.

**Key Details:**
- **Symptom:** Warning says "Run 'uv run pre-commit install'" instead of referencing `make setup`
- **Frequency:** Every session where hooks are missing
- **Impact:** Low — developers following CONTRIBUTING.md already run `make setup`

---

## Reproduction Steps

### Steps to Reproduce

1. Remove `.git/hooks/pre-commit`
2. Start a Claude Code session
3. Observe warning: `"Run 'uv run pre-commit install' to install hooks."`
4. Note: warning doesn't mention `make setup` — the documented setup mechanism

### Expected Result

Warning references `make setup` as the primary remediation action.

### Actual Result

Warning references `uv run pre-commit install` directly, bypassing the documented workflow.

---

## Environment

| Attribute | Value |
|-----------|-------|
| **Repository** | geekatron/jerry |
| **File** | `scripts/session_start_hook.py` |
| **Function** | `check_precommit_hooks()` (lines 104-139) |
| **Warning Text** | Lines 134-137 |

---

## Root Cause Analysis

### Root Cause

The `check_precommit_hooks()` warning message was written before the Makefile `setup` target was fully established as the canonical setup mechanism. The warning references the raw command rather than the documented workflow.

### DEC-001 Key Findings

| Evidence | Source | Finding |
|----------|--------|---------|
| E-1 | `Makefile:16-22` | `setup` target: `uv sync` + `uv run pre-commit install` |
| E-4 | `CONTRIBUTING.md:11-30` | "First-Time Setup (REQUIRED)" documents `make setup` |
| E-7 | `INSTALLATION.md:374-407` | Developer setup section documents `make setup` |
| E-8 | `session_start_hook.py:104-139` | Detection-only by design — correct architecture |

### Original vs Corrected Understanding

| Aspect | Original (Incorrect) | Corrected (DEC-001) |
|--------|----------------------|---------------------|
| Problem | No auto-install mechanism | Warning message doesn't reference `make setup` |
| Root Cause | Missing auto-install logic | Warning text out of sync with documentation |
| Severity | Major | Minor |
| Priority | High | Low |
| Fix | Add subprocess auto-install | Update warning text (1-line change) |

---

## Acceptance Criteria

### Fix Verification

- [x] Warning message references `make setup` as primary action
- [x] Warning includes Windows fallback (`uv sync && uv run pre-commit install`)
- [x] No auto-install side effects added to session hook

### Quality Checklist

- [x] Existing tests still passing
- [x] No new issues introduced
- [x] Decision documented (DEC-001)

---

## Children

| ID | Title | Status | Priority |
|----|-------|--------|----------|
| [TASK-001](./BUG-010--TASK-001-auto-install-precommit-hooks.md) | ~~Auto-install pre-commit hooks~~ → Improve warning message | done | low |

---

## Related Items

### Hierarchy

- **Parent:** [EN-004: Fix Pre-commit Hook Coverage](./EN-004-fix-precommit-hook-coverage.md)

### Decisions

- **DEC-001:** [Pre-commit Hook Installation Strategy](./DEC-001-precommit-installation-strategy.md) — D-001 (close as won't fix), D-002 (improve warning)

### Related Bugs

- **BUG-011:** Pre-commit pytest hook only triggers on Python files — separate pre-commit gap

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-11 | Claude | pending | Bug filed with incorrect framing: assumed no installation mechanism existed. Proposed auto-install in session hook. |
| 2026-02-11 | Claude | done | Revised via DEC-001: Makefile `setup` target already exists. Warning message improvement only. Priority downgraded high→low, severity major→minor. TASK-001 revised accordingly. |
