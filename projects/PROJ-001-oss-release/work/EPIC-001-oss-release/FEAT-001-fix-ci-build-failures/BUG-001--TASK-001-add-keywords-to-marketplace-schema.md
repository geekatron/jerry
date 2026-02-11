# TASK-001: Add `keywords` property to marketplace plugin item schema

> **Type:** task
> **Status:** BACKLOG
> **Priority:** HIGH
> **Created:** 2026-02-10
> **Parent:** BUG-001
> **Owner:** —
> **Activity:** DEVELOPMENT

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Content](#content) | Description and acceptance criteria |
| [Evidence](#evidence) | Deliverables and verification |
| [Related Items](#related-items) | Parent and related work |
| [History](#history) | Status changes |

---

## Content

### Description

Add the `keywords` property to the plugin item definition in `schemas/marketplace.schema.json`. The marketplace manifest (`.claude-plugin/marketplace.json`) includes `keywords` in plugin items, but the schema does not define this property. With `"additionalProperties": false`, the validator correctly rejects it.

The `keywords` property already exists in `schemas/plugin.schema.json` (lines 82-89) and should be mirrored in the marketplace plugin item schema for consistency.

### Acceptance Criteria

- [ ] `schemas/marketplace.schema.json` plugin item properties include `keywords`
- [ ] `keywords` definition matches `plugin.schema.json` format (array of kebab-case strings, unique)
- [ ] `uv run python scripts/validate_plugin_manifests.py` passes locally (all 3 manifests)
- [ ] Plugin Validation CI check passes

### Implementation Notes

Add the following to `schemas/marketplace.schema.json` inside `properties.plugins.items.properties` (after `category` or `author`):

```json
"keywords": {
  "type": "array",
  "items": {
    "type": "string",
    "pattern": "^[a-z0-9-]+$"
  },
  "uniqueItems": true,
  "description": "Keywords for plugin discovery and categorization."
}
```

This matches the `keywords` definition in `schemas/plugin.schema.json` lines 82-89.

### Related Items

- Parent: [BUG-001: Marketplace manifest schema error](./FEAT-001--BUG-001-plugin-manifest-schema-error.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Updated marketplace.schema.json | Code | `schemas/marketplace.schema.json` |

### Verification

- [ ] Acceptance criteria verified
- [ ] `uv run python scripts/validate_plugin_manifests.py` outputs `[PASS]` for all manifests
- [ ] No regressions in other validation checks

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-10 | Created | Created after corrected root cause analysis |
