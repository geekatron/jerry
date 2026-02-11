# TASK-003: Specify Draft202012Validator in validation script (best practice)

> **Type:** task
> **Status:** BACKLOG
> **Priority:** MEDIUM
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

Update `scripts/validate_plugin_manifests.py` to explicitly specify `cls=jsonschema.Draft202012Validator` at all three `jsonschema.validate()` call sites. This is a **best practice** improvement — not the root cause fix for BUG-001 (which is TASK-001: adding `keywords` to marketplace schema).

All three schemas use JSON Schema Draft 2020-12. Specifying the validator class explicitly:
- Ensures correct interpretation if Draft 2020-12-specific features are used in the future
- Signals intent to future contributors
- Aligns with DEC-001

**Note:** This task alone will NOT fix the CI failure. TASK-001 must be completed first.

### Acceptance Criteria

- [ ] `validate_plugin_json()` (line ~90) uses `cls=jsonschema.Draft202012Validator`
- [ ] `validate_marketplace_json()` (line ~137) uses `cls=jsonschema.Draft202012Validator`
- [ ] `validate_hooks_json()` (line ~184) uses `cls=jsonschema.Draft202012Validator`
- [ ] `uv run python scripts/validate_plugin_manifests.py` passes locally
- [ ] No regressions

### Implementation Notes

The change at each call site is:

```python
# Before
jsonschema.validate(manifest, schema)

# After
jsonschema.validate(manifest, schema, cls=jsonschema.Draft202012Validator)
```

### Related Items

- Parent: [BUG-001: Marketplace manifest schema error](./FEAT-001--BUG-001-plugin-manifest-schema-error.md)
- Decision: [DEC-001: JSON Schema Validator Class Selection](./FEAT-001--DEC-001-json-schema-validator-class.md)
- Depends On: [TASK-001: Add keywords to marketplace schema](./BUG-001--TASK-001-add-keywords-to-marketplace-schema.md) (TASK-001 is the actual fix)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Updated validate_plugin_manifests.py | Code | `scripts/validate_plugin_manifests.py` |

### Verification

- [ ] Acceptance criteria verified
- [ ] `uv run python scripts/validate_plugin_manifests.py` outputs `[PASS]` for all manifests
- [ ] No regressions in other validation checks

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-10 | Created | Originally TASK-001; renumbered to TASK-003 after root cause correction |
| 2026-02-10 | Updated | Demoted from HIGH to MEDIUM priority — best practice, not root cause fix |
