# BUG-003: ValidationResult.__bool__ Causes CLI Serialization Issue

> **Bug:** Invalid ValidationResult serialized as null in CLI JSON output
> **Feature:** [FT-001](./FEATURE-WORKTRACKER.md) Session Hook Cleanup
> **Enabler:** [EN-001](./en-001-session-hook-tdd.md) Session Start Hook TDD Cleanup
> **Status:** RESOLVED ✅
> **Severity:** Medium
> **Found:** 2026-01-21
> **Fixed:** 2026-01-21

---

## Problem

When a project ID from local context was invalid (e.g., "invalid-format"), the CLI JSON output showed `"validation": null` instead of the actual validation failure message.

### Expected

```json
{
  "jerry_project": "invalid-format",
  "validation": {
    "is_valid": false,
    "messages": ["Invalid project ID 'invalid-format': Must match format PROJ-{nnn}-{slug}..."]
  }
}
```

### Actual

```json
{
  "jerry_project": "invalid-format",
  "validation": null
}
```

---

## Root Cause

The `ValidationResult` class implements `__bool__` to return `is_valid`:

```python
# src/session_management/domain/value_objects/validation_result.py:69-71
def __bool__(self) -> bool:
    """Allow using ValidationResult in boolean context."""
    return self.is_valid
```

The CLI adapter used truthiness to check if validation exists:

```python
# src/interface/cli/adapter.py:131-136 (BEFORE FIX)
"validation": {
    "is_valid": context["validation"].is_valid,
    "messages": context["validation"].messages,
}
if context["validation"]  # <-- Falsy when is_valid=False!
else None,
```

When `is_valid=False`, `__bool__` returns `False`, making the `if context["validation"]` check fail, resulting in `null` output.

---

## Fix

Changed the check from truthiness to explicit `None` comparison:

```python
# src/interface/cli/adapter.py:131-140 (AFTER FIX)
# Note: Use 'is not None' because ValidationResult.__bool__ returns is_valid
# which would be False for invalid results
"validation": {
    "is_valid": context["validation"].is_valid,
    "messages": list(context["validation"].messages),
}
if context["validation"] is not None
else None,
```

---

## Evidence

### Test Case Added

`tests/integration/cli/test_cli_local_context_integration.py::TestCLILocalContextNegative::test_invalid_project_in_local_context_returns_validation_error`

### Verification

```bash
# Before fix
$ CLAUDE_PROJECT_DIR=/tmp/test JERRY_PROJECT="" uv run jerry --json projects context
{"jerry_project": "invalid-format", "validation": null, ...}

# After fix
$ CLAUDE_PROJECT_DIR=/tmp/test JERRY_PROJECT="" uv run jerry --json projects context
{"jerry_project": "invalid-format", "validation": {"is_valid": false, "messages": [...]}, ...}
```

---

## Impact

- Users would not see validation error messages in JSON output
- Debugging invalid project configurations was difficult
- Session hook could not properly report validation failures to Claude

---

## Related Artifacts

- [EN-001](./en-001-session-hook-tdd.md): Parent enabler
- [DISC-008](./disc-008-bootstrap-wiring-gap.md): Discovery about bootstrap wiring

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-21 | Bug discovered during Phase 2 testing | Claude |
| 2026-01-21 | Fixed with `is not None` check | Claude |
