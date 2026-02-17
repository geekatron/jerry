# TASK-002: Fix PreToolUse Hook — Migrate to hookSpecificOutput API

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
id: "TASK-002"
work_type: TASK
title: "Fix PreToolUse Hook — Migrate to hookSpecificOutput API"
status: pending
priority: HIGH
parent_id: "BUG-002"
assignee: "Claude"
created_at: "2026-02-17"
activity: DEVELOPMENT
effort: 3
```

---

## Content

### Description

Migrate `scripts/pre_tool_use.py` from deprecated top-level `decision`/`reason` fields to the current `hookSpecificOutput` format per Claude Code docs.

**Changes required:**

1. **Replace all `{"decision": "block", "reason": ...}` with:**
```python
{
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "reason string"
    }
}
```

2. **Replace `{"decision": "approve"}` with:**
```python
{
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "allow"
    }
}
```

3. **Replace `{"decision": "ask", ...}` with:**
```python
{
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": "reason string"
    }
}
```

4. **Fix exit codes:** Lines 370, 373 return `exit 2` on errors which **blocks tool calls**. Change to `exit 0` with empty JSON for fail-open behavior.

**Lines to modify:** 275, 286-289, 301-305, 336, 365, 369-373

### Acceptance Criteria

- [ ] All `decision` fields moved to `hookSpecificOutput.permissionDecision`
- [ ] Values use `"allow"`/`"deny"` (not `"approve"`/`"block"`)
- [ ] `hookEventName: "PreToolUse"` present in all `hookSpecificOutput` objects
- [ ] Error cases exit 0 with empty JSON (fail-open)
- [ ] Security guardrails still functional (blocking dangerous commands)

### Related Items

- Parent: [BUG-002](../BUG-002-hook-schema-validation-failures.md)
- File: `scripts/pre_tool_use.py`

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-17 | Created | Initial creation |
