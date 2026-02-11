# TASK-001: Wire dynamic project discovery into project_id fixture

> **Type:** task
> **Status:** done
> **Priority:** MEDIUM
> **Created:** 2026-02-11
> **Completed:** 2026-02-11
> **Parent:** BUG-005
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

Replace the hardcoded `project_id` fixture in `tests/project_validation/conftest.py` (line 114) with dynamic project discovery using the existing `discover_projects()` function (lines 29-41).

Currently:
```python
@pytest.fixture(params=["PROJ-001-plugin-cleanup"])  # Can be expanded dynamically
def project_id(request: pytest.FixtureRequest) -> str:
    return request.param
```

`PROJ-001-plugin-cleanup` does not exist in the repository. The actual project is `PROJ-001-oss-release`. The `discover_projects()` function already exists and correctly discovers `PROJ-*` directories, but it is not wired into the fixture parameterization.

### Acceptance Criteria

- [x] `project_id` fixture uses `discover_projects()` for parameterization
- [x] Tests are parameterized against all existing `PROJ-*` directories
- [x] No hardcoded project IDs remain in the fixture
- [x] If no projects are discovered, tests skip gracefully (not fail) — uses `_SENTINEL_NO_PROJECTS` pattern
- [x] Existing tests (`TestProjectIsolation`, `TestCoreFilesExist`, `TestReferencesResolve`, `TestNegativeCases`) all work with the dynamically discovered project IDs
- [ ] Fix works across Python 3.11-3.14 on both pip and uv CI jobs (pending CI verification)

### Implementation Notes

**Approach: pytest_generate_tests hook (Recommended):**

Since `discover_projects()` requires the `project_root` path and `@pytest.fixture(params=...)` can't reference other fixtures, use `pytest_generate_tests` or compute params at module level:

```python
# Module-level discovery (runs at collection time)
_PROJECT_ROOT = _find_project_root(Path(__file__).parent)
_DISCOVERED_PROJECTS = [p.name for p in discover_projects(_PROJECT_ROOT)]


@pytest.fixture(params=_DISCOVERED_PROJECTS or ["NO_PROJECTS_FOUND"])
def project_id(request: pytest.FixtureRequest) -> str:
    if request.param == "NO_PROJECTS_FOUND":
        pytest.skip("No projects discovered in projects/ directory")
    return request.param
```

This approach:
- Runs discovery at collection time (before tests execute)
- Uses the existing `_find_project_root()` and `discover_projects()` functions
- Skips gracefully if no projects exist
- Parameterizes against ALL discovered projects

### Files Involved

| File | Role | Change Needed |
|------|------|---------------|
| `tests/project_validation/conftest.py` | Test fixture | Replace hardcoded params with dynamic discovery (line 114) |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Updated conftest.py | Code | `tests/project_validation/conftest.py:114` |

### Verification

- [ ] `uv run pytest tests/project_validation/ --collect-only` shows `PROJ-001-oss-release` (not `PROJ-001-plugin-cleanup`)
- [ ] `uv run pytest tests/project_validation/ -v` passes all tests
- [ ] No hardcoded `PROJ-001-plugin-cleanup` remains in conftest.py

---

## Related Items

- Parent: [BUG-005: Project validation tests reference non-existent PROJ-001-plugin-cleanup](./BUG-005-project-validation-missing-artifacts.md)
- Enabler: [EN-002: Fix Test Infrastructure](./EN-002-fix-test-infrastructure.md)
- Feature: [FEAT-001: Fix CI Build Failures](../FEAT-001-fix-ci-build-failures.md)
- Sibling: [TASK-002: Create required category directories in PROJ-001-oss-release](./BUG-005--TASK-002-create-category-directories.md) (both needed for tests to pass)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-11 | pending | Created. Wire discover_projects() into project_id fixture parameterization. |
| 2026-02-11 | done | Implemented module-level discovery with `_DISCOVERED_PROJECT_IDS`, `sorted()` for determinism, broadened exception handling `(RuntimeError, OSError, PermissionError)`, sentinel pattern for graceful skip. Adversarial critic feedback incorporated (RT-001, RT-002, RT-003). Committed in `4789625`. |
