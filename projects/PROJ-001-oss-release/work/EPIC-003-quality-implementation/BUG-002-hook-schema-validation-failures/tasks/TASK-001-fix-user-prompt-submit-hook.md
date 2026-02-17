# TASK-001: Fix UserPromptSubmit Hook — Add hookEventName

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
id: "TASK-001"
work_type: TASK
title: "Fix UserPromptSubmit Hook — Add hookEventName"
status: pending
priority: CRITICAL
parent_id: "BUG-002"
assignee: "Claude"
created_at: "2026-02-17"
activity: DEVELOPMENT
effort: 1
```

---

## Content

### Description

Add the required `hookEventName: "UserPromptSubmit"` field to the `hookSpecificOutput` dict in `hooks/user-prompt-submit.py`.

**Current (broken, line 57-63):**
```python
output = {
    "hookSpecificOutput": {
        "additionalContext": (
            f"<quality-reinforcement>\n{result.preamble}\n</quality-reinforcement>"
        ),
    },
}
```

**Fixed:**
```python
output = {
    "hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit",
        "additionalContext": (
            f"<quality-reinforcement>\n{result.preamble}\n</quality-reinforcement>"
        ),
    },
}
```

**Reference:** `scripts/session_start_hook.py:38-39` (correct pattern)

### Acceptance Criteria

- [ ] `hookEventName: "UserPromptSubmit"` present in output JSON
- [ ] Hook passes Claude Code schema validation (no errors in debug log)
- [ ] L2 quality reinforcement content reaches Claude context

### Related Items

- Parent: [BUG-002](../BUG-002-hook-schema-validation-failures.md)
- File: `hooks/user-prompt-submit.py`

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-17 | Created | Initial creation |
