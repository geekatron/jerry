# TASK-002: Add tests for plugin manifest validation

> **Type:** task
> **Status:** IN_PROGRESS
> **Priority:** HIGH
> **Created:** 2026-02-10
> **Parent:** BUG-001
> **Owner:** —
> **Activity:** TESTING

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

Add or update unit tests to verify that plugin manifest validation works correctly for all three manifests. Tests should cover:
1. Valid marketplace manifest with `keywords` field passes validation
2. Invalid manifest with truly unknown property still fails
3. All three manifests (plugin.json, marketplace.json, hooks.json) pass validation

### Acceptance Criteria

- [ ] Test exists verifying `keywords` field is accepted in marketplace plugin items
- [ ] Test exists verifying unknown properties are still rejected
- [ ] Test exists verifying all three manifests pass the validation script
- [ ] All tests pass with `uv run pytest`
- [ ] No regressions in existing test suite

### Implementation Notes

Tests should live in `tests/` following existing conventions. Check for existing validation tests first before creating new files.

Possible test cases:
```python
def test_marketplace_json_with_keywords_passes_validation():
    """keywords field should be accepted in marketplace plugin items."""

def test_marketplace_json_with_unknown_property_fails_validation():
    """Truly unknown properties should still be rejected."""

def test_all_manifests_pass_validation():
    """All three manifests pass the validation script."""
```

### Related Items

- Parent: [BUG-001: Marketplace manifest schema error](./BUG-001-marketplace-manifest-schema-error.md)
- Enabler: [EN-001: Fix Plugin Validation](./EN-001-fix-plugin-validation.md)
- Depends On: [TASK-001: Add keywords to marketplace schema](./TASK-001-add-keywords-to-marketplace-schema.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Test file | Code | TBD — test path determined during implementation |

### Verification

- [ ] Acceptance criteria verified
- [ ] `uv run pytest` passes with new tests included
- [ ] Test fails without TASK-001 fix (confirms test is valid)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-10 | Created | Initial creation |
| 2026-02-10 | Updated | Revised after root cause correction — focus on marketplace schema, not Draft 2020-12 |
