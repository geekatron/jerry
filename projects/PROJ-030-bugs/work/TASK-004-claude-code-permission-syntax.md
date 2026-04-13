# TASK-004: Claude Code permission syntax reference (#179)

> **Type:** task
> **Status:** completed
> **Priority:** medium
> **Created:** 2026-03-11
> **Parent:** EN-001
> **GitHub Issue:** [#179](https://github.com/geekatron/jerry/issues/179)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What was done |
| [Acceptance Criteria](#acceptance-criteria) | Completion evidence |

---

## Summary

Created comprehensive Diataxis reference document at `docs/reference/claude-code-permissions.md` documenting Claude Code permission patterns (MCP wildcards, Bash patterns, skill permissions, evaluation order, settings scope). Created using `/diataxis` (diataxis-reference agent). All claims cite official Claude Code documentation.

Four findings identified during creation were triaged into separate work items (BUG-004 #180, BUG-005 #181, TASK-005 #182), all of which are completed.

## Acceptance Criteria

- [x] AC-1: Reference doc exists at `docs/reference/claude-code-permissions.md` (387 lines)
- [x] AC-2: Created using `/diataxis` diataxis-reference agent (commit `ecadf471`)
- [x] AC-3: All claims cite Claude Code official documentation (`code.claude.com` sources)
- [x] AC-4: Cross-references added to `mcp-tool-standards.md`
- [x] AC-5: `mkdocs.yml` nav updated
- [x] AC-6: Findings triaged — BUG-004 (#180), BUG-005 (#181), TASK-005 (#182) all completed

## Residual

GH #179 still open — should be closed.
