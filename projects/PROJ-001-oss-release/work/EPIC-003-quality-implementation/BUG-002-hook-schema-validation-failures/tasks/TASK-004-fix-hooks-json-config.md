# TASK-004: Fix hooks.json Configuration

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
CREATED: 2026-02-17 (Claude)
-->

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Frontmatter](#frontmatter) | Task metadata |
| [Content](#content) | Description and acceptance criteria |
| [History](#history) | Status changes |

---

## Frontmatter

```yaml
id: "TASK-004"
work_type: TASK
title: "Fix hooks.json Configuration"
status: pending
priority: MEDIUM
parent_id: "BUG-002"
assignee: "Claude"
created_at: "2026-02-17"
activity: DEVELOPMENT
effort: 1
```

---

## Content

### Description

Fix `hooks/hooks.json` to remove invalid/unnecessary configuration.

**Changes required:**

1. **Line 17:** Remove `"matcher": "*"` from `UserPromptSubmit` — per docs, UserPromptSubmit doesn't support matchers and always fires on every occurrence. The matcher is silently ignored.

2. **Lines 40-51:** Move the `Stop` entry to `SubagentStop` (handled in TASK-003, but this task ensures hooks.json is correct after all changes).

3. **Validate all entries** against supported matcher values per event type:
   - `SessionStart`: `startup`, `resume`, `clear`, `compact`
   - `UserPromptSubmit`: no matcher support
   - `PreToolUse`: tool names (`Bash`, `Edit|Write`, etc.)
   - `SubagentStop`: agent type names

### Acceptance Criteria

- [ ] No matchers on events that don't support them
- [ ] All event names match Claude Code hook lifecycle
- [ ] JSON is valid and well-formed

### Related Items

- Parent: [BUG-002](../BUG-002-hook-schema-validation-failures.md)
- File: `hooks/hooks.json`

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-17 | Created | Initial creation |
