# TASK-002: Skip uv-dependent tests in pip CI environments

> **Type:** task
> **Status:** DONE
> **Priority:** HIGH
> **Created:** 2026-02-11
> **Completed:** 2026-02-11
> **Parent:** BUG-006
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

Add `@pytest.mark.skipif(shutil.which("uv") is None, reason="uv not available in this environment")` to the `TestValidationScriptIntegration` class in `tests/contract/test_plugin_manifest_validation.py`. This class contains two tests that invoke `uv` via `subprocess.run(["uv", "run", "python", ...])`. In pip CI environments where `uv` is not installed, the subprocess call raises `FileNotFoundError` before the process starts.

The existing skip mechanism in `test_validation_script_uses_uv_run` (checking `result.stderr` for "uv: command not found") was unreachable because the `FileNotFoundError` exception prevents `result` from being created.

### Acceptance Criteria

- [x] `import shutil` added to test file imports
- [x] `@pytest.mark.skipif(shutil.which("uv") is None, ...)` decorator added to `TestValidationScriptIntegration` class
- [x] Both `test_all_manifests_pass_validation` and `test_validation_script_uses_uv_run` are covered by the skip
- [x] Tests pass in environments WITH uv (no false skips)
- [x] Tests gracefully skip in environments WITHOUT uv (no `FileNotFoundError`)

### Implementation Notes

Class-level decorator covers all methods in the class:

```python
import shutil

@pytest.mark.skipif(
    shutil.which("uv") is None,
    reason="uv not available in this environment",
)
class TestValidationScriptIntegration:
    """Contract: validate_plugin_manifests.py must validate all three manifests."""
    ...
```

`shutil.which("uv")` is preferred over try/except because:
- It checks PATH at collection time, not at test execution time
- It provides a clear skip reason in pytest output
- It follows pytest conventions for environment-dependent tests

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Updated test file (import) | Code | `tests/contract/test_plugin_manifest_validation.py:26` |
| Updated test file (skipif) | Code | `tests/contract/test_plugin_manifest_validation.py:319-322` |

### Verification

- [x] Acceptance criteria verified
- [x] `uv run pytest tests/contract/test_plugin_manifest_validation.py -v` → `11 passed in 0.54s` (uv available locally, tests run)
- [x] In pip CI, tests will show as `SKIPPED` instead of `FAILED`

### Diff

```diff
 import json
+import shutil
 import subprocess
 from pathlib import Path
 from typing import TYPE_CHECKING

...

+@pytest.mark.skipif(
+    shutil.which("uv") is None,
+    reason="uv not available in this environment",
+)
 class TestValidationScriptIntegration:
     """Contract: validate_plugin_manifests.py must validate all three manifests."""
```

---

## Related Items

- Parent: [BUG-006: Validation test CI regressions](./BUG-006-validation-test-ci-regressions.md)
- Enabler: [EN-003: Fix Validation Test Regressions](./EN-003-fix-validation-test-regressions.md)
- Regression Source: [EN-001/TASK-002: Add validation tests](../EN-001-fix-plugin-validation/TASK-002-add-validation-tests.md)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-11 | DONE | Created and completed. Added shutil.which guard at class level. |
