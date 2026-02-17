# TASK-006: Create or Extract Hook Output JSON Schema Definition

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
id: "TASK-006"
work_type: TASK
title: "Create or Extract Hook Output JSON Schema Definition"
status: pending
priority: HIGH
parent_id: "BUG-002"
assignee: "Claude"
created_at: "2026-02-17"
activity: RESEARCH
effort: 3
```

---

## Content

### Description

Find an existing JSON Schema definition for Claude Code hook outputs, or generate one from the official documentation, and persist it as a reusable artifact in the repository. This schema file becomes the single source of truth that TASK-005's tests validate against — and that future hook development must conform to.

**Research approach (in priority order):**

1. **Check Claude Code source/releases:** Search the `anthropics/claude-code` repository (GitHub, Context7) for an exported or internal JSON Schema file for hook output validation. If Claude Code already has one, extract it.

2. **Check official documentation:** The debug log already shows the expected schema structure. The official docs (code.claude.com/docs/en/hooks) document the per-event output fields. Use these as the authoritative source.

3. **Generate from documentation:** If no machine-readable schema exists, create JSON Schema files (draft 2020-12) from the documented output structures for each hook event type.

**Schema files to produce:**

| File | Covers |
|------|--------|
| `schemas/hooks/hook-output-base.schema.json` | Common fields: `continue`, `stopReason`, `suppressOutput`, `systemMessage` |
| `schemas/hooks/user-prompt-submit-output.schema.json` | `decision`, `reason`, `hookSpecificOutput.hookEventName`, `hookSpecificOutput.additionalContext` |
| `schemas/hooks/pre-tool-use-output.schema.json` | `hookSpecificOutput.hookEventName`, `permissionDecision`, `permissionDecisionReason`, `updatedInput`, `additionalContext` |
| `schemas/hooks/post-tool-use-output.schema.json` | `decision`, `reason`, `hookSpecificOutput.hookEventName`, `additionalContext`, `updatedMCPToolOutput` |
| `schemas/hooks/session-start-output.schema.json` | `hookSpecificOutput.hookEventName`, `additionalContext` |
| `schemas/hooks/subagent-stop-output.schema.json` | `decision`, `reason` |
| `schemas/hooks/permission-request-output.schema.json` | `hookSpecificOutput.hookEventName`, `decision.behavior`, `updatedInput`, `updatedPermissions` |

**Integration points:**
- TASK-005 tests import these schemas and validate hook output against them using `jsonschema` library
- Pre-commit hook or CI step can validate schema files themselves
- Future hook development references schemas as contract

### Acceptance Criteria

- [ ] Research complete: checked Claude Code repo for existing schema files
- [ ] JSON Schema files created (or extracted) for all hook event output types used by Jerry
- [ ] Schema files stored at `schemas/hooks/` (or similar discoverable location)
- [ ] Schemas cover: required fields, field types, enum values, `hookEventName` constraints
- [ ] Schemas validated against known-good output (e.g., `session_start_hook.py` output)
- [ ] Schemas validated against known-bad output (e.g., the broken `user-prompt-submit.py` output should fail)
- [ ] TASK-005 tests reference these schemas (dependency: TASK-006 should complete before or alongside TASK-005)
- [ ] Schema version/source documented (link to official docs revision or Claude Code version)

### Implementation Notes

The debug log already reveals the internal validation schema structure:
```json
{
  "continue": "boolean (optional)",
  "suppressOutput": "boolean (optional)",
  "stopReason": "string (optional)",
  "decision": "\"approve\" | \"block\" (optional)",
  "reason": "string (optional)",
  "systemMessage": "string (optional)",
  "hookSpecificOutput": {
    "for UserPromptSubmit": {
      "hookEventName": "\"UserPromptSubmit\"",
      "additionalContext": "string (required)"
    }
  }
}
```

This can be translated directly into JSON Schema draft 2020-12 format. The `jsonschema` Python library (already likely available or can be `uv add --dev`) provides validation.

### Related Items

- Parent: [BUG-002](../BUG-002-hook-schema-validation-failures.md)
- Blocks: [TASK-005](./TASK-005-add-hook-schema-tests.md) (tests should validate against these schemas)
- Source: [DISC-002](../../DISC-002-hook-schema-non-compliance.md) (discovery with evidence)
- Reference: [Claude Code Hooks Docs](https://code.claude.com/docs/en/hooks)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-17 | Created | Initial creation. Research + schema generation task. |
