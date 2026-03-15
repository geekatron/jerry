# TASK-003: Consolidate pre_tool_use.py into CLI enforcement pipeline (#150)

> **Type:** task
> **Status:** in_progress
> **Priority:** high
> **Created:** 2026-03-09
> **Parent:** EN-001
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

Consolidate the standalone `scripts/pre_tool_use.py` into the jerry CLI enforcement pipeline. The SecurityEnforcementEngine (#150) has been implemented and integrated via `hooks/hooks.json`, but the deprecated standalone script still exists at `scripts/pre_tool_use.py`.

## Description

GitHub Issue #150 created the SecurityEnforcementEngine as a consolidated pre-tool-use enforcement pipeline with 82 tests. The standalone script is now marked DEPRECATED per CHANGELOG.md. This task tracks the final removal of the deprecated script and verification that all enforcement runs through the CLI path.

Related issues:
- #177 (Remove deprecated scripts/pre_tool_use.py after #150 migration verification)
- #178 (Consolidate dual SubagentStop hooks)

---

## Acceptance Criteria

- [ ] `scripts/pre_tool_use.py` removed from repository
- [ ] All enforcement runs through `jerry hooks pre-tool-use` CLI path
- [ ] No references to `scripts/pre_tool_use.py` remain in hooks.json or settings files
- [ ] All 82 SecurityEnforcementEngine tests pass
- [ ] GitHub Issues #150, #177 closable after completion

---

## Related Items

- **Parent:** [EN-001](EN-001-ci-pipeline-hardening.md)
- **GitHub Issue:** [#150](https://github.com/geekatron/jerry/issues/150)
- **Related:** [#177](https://github.com/geekatron/jerry/issues/177) — Remove deprecated script
- **Related:** [#178](https://github.com/geekatron/jerry/issues/178) — Consolidate dual SubagentStop hooks

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-03-09 | pending | Created as EN-001 Task #6 |
| 2026-03-10 | in_progress | SecurityEnforcementEngine implemented (#150). Deprecated script still present. |
