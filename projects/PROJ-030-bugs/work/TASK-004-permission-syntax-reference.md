# TASK-004: Claude Code permission syntax reference (#179)

> **Type:** task
> **Status:** in_progress
> **Priority:** medium
> **Created:** 2026-03-10
> **Parent:** PROJ-030-bugs
> **Owner:** saucer-boy

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this task covers |
| [Description](#description) | Technical details |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Related Items](#related-items) | Linked issues and entities |
| [History](#history) | Status changes |

---

## Summary

Create and maintain a reference document (`docs/reference/claude-code-permissions.md`) covering Claude Code permission syntax — patterns, wildcards, evaluation order, settings scope, Skill() patterns, MCP patterns, and Bash patterns.

## Description

During the #181/#182 investigation, significant time was spent discovering how Claude Code permission patterns work (Skill() naming, Bash syntax deprecation, plugin namespaces, hook JSON formats). This reference document captures those findings so future sessions don't repeat the research.

The file already exists at `docs/reference/claude-code-permissions.md` with initial content. This task tracks ensuring it covers all discovered patterns including the A/B test results from BUG-005.

---

## Acceptance Criteria

- [ ] `docs/reference/claude-code-permissions.md` covers Skill() patterns (short, prefixed, wildcard)
- [ ] Bash syntax section documents space vs colon, with deprecation note
- [ ] MCP wildcard section documents dual namespace pattern
- [ ] Hook JSON format section documents PreToolUse `hookSpecificOutput` with source URL
- [ ] Permission inheritance section documents subagent vs skill gap (#18950)
- [ ] A/B test results from BUG-005 referenced

---

## Related Items

- **GitHub Issue:** [#179](https://github.com/geekatron/jerry/issues/179)
- **Related Bug:** [BUG-005](BUG-005-skill-permission-pattern.md) — Skill permission pattern investigation
- **Related Doc:** `docs/reference/claude-code-permissions.md`
- **Related Doc:** `docs/explanation/permission-security-model.md`

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-03-10 | pending | Created from #179 |
| 2026-03-14 | in_progress | Partial content exists. BUG-005 findings need integration. |
