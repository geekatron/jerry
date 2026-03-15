# TASK-006: Consolidate dual SubagentStop hooks (scripts/ + CLI) (#178)

> **Type:** task
> **Status:** pending
> **Priority:** medium
> **Created:** 2026-03-15
> **Parent:** EN-001
> **Owner:** unassigned

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

The SubagentStop hook has the same dual-hook architecture that #150 fixed for PreToolUse — a standalone script alongside a CLI wrapper, both running sequentially in hooks.json. This needs the same consolidation treatment.

## Description

After #150 consolidated PreToolUse into the SecurityEnforcementEngine via the jerry CLI, the SubagentStop hook still runs both a standalone script and a CLI wrapper. This creates the same maintenance burden and inconsistency that motivated #150. The fix follows the same pattern: consolidate into the CLI path and remove the standalone script.

---

## Acceptance Criteria

- [ ] SubagentStop hook runs through a single CLI path (not dual scripts)
- [ ] Standalone SubagentStop script removed or deprecated
- [ ] hooks.json updated with single SubagentStop entry
- [ ] Existing SubagentStop behavior preserved (session cleanup, state persistence)
- [ ] GitHub Issue #178 closable after completion

---

## Related Items

- **Parent:** [EN-001](EN-001-ci-pipeline-hardening.md)
- **GitHub Issue:** [#178](https://github.com/geekatron/jerry/issues/178)
- **Related:** [TASK-003](TASK-003-consolidate-pre-tool-use.md) — Same consolidation pattern for PreToolUse

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-03-15 | pending | Triaged from GitHub Issue #178. Same pattern as TASK-003/#177 consolidation. |
