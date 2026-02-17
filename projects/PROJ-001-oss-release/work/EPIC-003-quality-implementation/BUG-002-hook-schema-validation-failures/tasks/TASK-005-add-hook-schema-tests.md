# TASK-005: Add Hook Output Schema Validation Tests

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
id: "TASK-005"
work_type: TASK
title: "Add Hook Output Schema Validation Tests"
status: pending
priority: HIGH
parent_id: "BUG-002"
assignee: "Claude"
created_at: "2026-02-17"
activity: TESTING
effort: 3
```

---

## Content

### Description

Add automated tests that validate all hook scripts produce JSON conforming to the Claude Code hook schema. This prevents regression of the schema validation issues found in DISC-002.

**Test coverage required:**

1. **UserPromptSubmit hook:**
   - Output includes `hookSpecificOutput.hookEventName == "UserPromptSubmit"`
   - Output includes `hookSpecificOutput.additionalContext` (string)
   - No extraneous top-level fields

2. **PreToolUse hook:**
   - Block decisions use `hookSpecificOutput.permissionDecision == "deny"`
   - Allow decisions use `hookSpecificOutput.permissionDecision == "allow"`
   - Ask decisions use `hookSpecificOutput.permissionDecision == "ask"`
   - All include `hookSpecificOutput.hookEventName == "PreToolUse"`
   - Error cases exit 0 (not exit 2)

3. **SubagentStop hook:**
   - Output conforms to SubagentStop decision control
   - Input parsing uses correct field names
   - Exit codes follow protocol

4. **SessionStart hook (regression):**
   - Confirm existing correct behavior is preserved
   - Output includes `hookSpecificOutput.hookEventName == "SessionStart"`

**Schema reference:** code.claude.com/docs/en/hooks

### Acceptance Criteria

- [ ] Test file created: `tests/test_hook_schema_compliance.py`
- [ ] All 4 hook scripts have schema validation tests
- [ ] Tests verify hookEventName presence and correct value
- [ ] Tests verify decision field names (not deprecated)
- [ ] Tests verify exit code behavior
- [ ] All tests pass with `uv run pytest`

### Related Items

- Parent: [BUG-002](../BUG-002-hook-schema-validation-failures.md)
- Reference: DISC-002 (discovery with full findings)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-17 | Created | Initial creation |
