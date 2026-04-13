# TASK-015: Add filename_pattern to agent-governance-v1.schema.json

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-03-31
> **Parent:** BUG-006
> **ADR:** [ADR-output-path-resolution-001](../../../docs/design/ADR-output-path-resolution-001.md)

---

## Summary

Add `filename_pattern` as an optional field to the `output` object in `docs/schemas/agent-governance-v1.schema.json`. This is Step 0 of the ADR migration guide and MUST execute before TASK-006/007/008 (governance YAML updates) to ensure schema validation accepts the new field.

## Schema Diff

```json
"output": {
  "type": "object",
  "properties": {
    "required": { "type": "boolean" },
    "location": { "type": "string" },
    "filename_pattern": {
      "type": "string",
      "description": "Filename template for Priority 2 base-path resolution (ADR-output-path-resolution-001). Interpolated with agent variables when caller provides OUTPUT CONTEXT.base_path."
    },
    "levels": { ... }
  }
}
```

Non-breaking additive change — existing agents without `filename_pattern` continue to validate.

## File

- `docs/schemas/agent-governance-v1.schema.json` — `output` object definition

## Acceptance Criteria

- [ ] `filename_pattern` field exists in schema `output` properties as type `string` with description
- [ ] Field is NOT in `required` array (optional)
- [ ] Existing agents without `filename_pattern` still pass validation: `uv run jerry schema validate`
- [ ] Schema itself is valid JSON Schema Draft 2020-12
