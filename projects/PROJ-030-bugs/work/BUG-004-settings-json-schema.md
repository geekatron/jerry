# BUG-004: settings.json uses undocumented field names (#180)

> **Type:** bug
> **Status:** completed
> **Priority:** medium
> **Impact:** medium
> **Severity:** major
> **Created:** 2026-03-10
> **Completed:** 2026-03-14
> **Parent:** PROJ-030-bugs
> **Owner:** saucer-boy
> **Found In:** 0.29.0
> **Fix Version:** 0.29.1

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and key details |
| [Steps to Reproduce](#steps-to-reproduce) | Steps to reproduce the issue |
| [Fix Description](#fix-description) | Solution approach and changes made |
| [Acceptance Criteria](#acceptance-criteria) | Conditions for bug to be fixed |
| [Related Items](#related-items) | Hierarchy and related work items |
| [History](#history) | Status changes and key events |

---

## Summary

`.claude/settings.json` contained fields not recognized by Claude Code's schema: `version`, `project`, `rules`, `commands`, `context`, `preferences`. These fields were silently ignored at runtime, creating false confidence that the configuration was functional.

---

## Steps to Reproduce

1. Open `.claude/settings.json`
2. Observe fields: `version`, `project`, `rules`, `commands`, `context`, `preferences`
3. Check against Claude Code JSON Schema — none of these fields are recognized
4. Fields are silently ignored at runtime with no error or warning

**Key Details:**
- **Symptom:** Settings fields silently ignored; no error but no effect
- **Frequency:** Every session start
- **Workaround:** None needed — fields were inert

---

## Fix Description

### Solution Approach

Remove all non-schema fields from settings.json. Migrate from deprecated `allowed_tools`/`require_approval` to the current `allow`/`ask`/`deny` permission syntax. Add JSON Schema (`$schema`) for validation.

### Changes Made

- Removed 8 invalid top-level fields (`version`, `project`, `rules`, `commands`, `context`, `preferences`, `hooks`, `stash`)
- Migrated `permissions.allowed_tools` → `permissions.allow`
- Migrated `permissions.require_approval` → `permissions.ask`
- Added `permissions.deny` for `curl`/`wget`
- Added `$schema` reference for validation
- Created `docs/schemas/claude-code-settings-v1.schema.json`
- Created `scripts/validate_settings_local.py` validation script

---

## Acceptance Criteria

- [x] settings.json contains only Claude Code recognized fields
- [x] JSON Schema validation passes with 0 errors
- [x] Permission entries use current `allow`/`ask`/`deny` syntax

---

## Related Items

- **GitHub Issue:** [#180](https://github.com/geekatron/jerry/issues/180)
- **Related Bug:** [BUG-005](BUG-005-skill-permission-pattern.md) — Skill permission pattern (#181)
- **Research:** `projects/PROJ-030-bugs/research/settings-json-field-extraction.md`
- **Design:** `projects/PROJ-030-bugs/work/settings-json-architecture-design.md`

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-03-10 | pending | Initial report |
| 2026-03-14 | completed | Schema-valid settings committed |
