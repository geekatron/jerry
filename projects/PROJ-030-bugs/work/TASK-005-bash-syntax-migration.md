# TASK-005: Migrate deprecated Bash(:*) syntax (#182)

> **Type:** task
> **Status:** completed
> **Priority:** medium
> **Created:** 2026-03-11
> **Completed:** 2026-03-14
> **Parent:** PROJ-030-bugs
> **Owner:** saucer-boy

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Description](#description) | What was done and why |
| [Acceptance Criteria](#acceptance-criteria) | Conditions for task to be done |
| [Related Items](#related-items) | Hierarchy and related work items |
| [History](#history) | Status changes and key events |

---

## Summary

All Bash permission entries in `.claude/settings.json` and `.claude/settings.local.json` used the deprecated `Bash(command:*)` colon syntax. Claude Code documentation confirms the colon form is deprecated in favor of `Bash(command *)` space syntax. GitHub Issue #33595 reports the colon form may silently fail in some versions.

## Description

Migrated all Bash entries from colon to space syntax. Removed all Bash entries from settings.local.json since they were either subsumed by settings.json or removed for safety reasons during C4 tournament review.

---

## Acceptance Criteria

- [x] All `Bash(:*)` entries migrated to `Bash( *)` space syntax in settings.json
- [x] All Bash entries removed from settings.local.json (subsumed by settings.json or removed for safety)
- [x] No deprecated colon syntax remains in committed settings files

---

## Related Items

- **GitHub Issue:** [#182](https://github.com/geekatron/jerry/issues/182)
- **Related Bug:** [BUG-004](BUG-004-settings-json-schema.md) — settings.json invalid fields (#180)
- **Related Bug:** [BUG-005](BUG-005-skill-permission-pattern.md) — Skill permission pattern (#181)
- **Research:** `projects/PROJ-030-bugs/research/skill-permission-bash-syntax-research.md`

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-03-11 | pending | Initial report |
| 2026-03-14 | completed | All Bash entries migrated or removed |
