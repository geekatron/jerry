# STORY-006: GitHub Issue Scan for Frontmatter Gotchas

> **Type:** story
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Created:** 2026-03-27T02:00:00Z
> **Due:**
> **Completed:** 2026-03-27T03:30:00Z
> **Parent:** FEAT-001
> **Owner:** adam.nowak
> **Effort:** 3

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What was done |
| [Evidence](#evidence) | Delivery artifacts |

---

## Summary

Scanned 36 GitHub issues in `anthropics/claude-code` for frontmatter parsing bugs, undocumented fields, breaking changes, and tool restriction issues. Key findings:
- F-001: Multiline YAML silently breaks discovery (#4700)
- F-009: Task renamed to Agent in v2.1.63 (#29677)
- F-016: disallowedTools bypassed via Bash (#31292)
- F-019: Hooks in agent frontmatter not executed for subagents (#18392)
- 13 runtime-limitation annotations added to both schemas

---

## Evidence

| Deliverable | Path |
|-------------|------|
| Research artifact | `work/research/github-issue-scan-frontmatter.md` |
| Schema annotations | `docs/schemas/claude-code-frontmatter-v1.schema.json` (7 annotations) |
| Schema annotations | `docs/schemas/claude-code-skill-frontmatter-v1.schema.json` (6 annotations) |
