# TASK-002: Create required category directories in PROJ-001-oss-release

> **Type:** task
> **Status:** pending
> **Priority:** MEDIUM
> **Created:** 2026-02-11
> **Completed:** —
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

Create the required category directories in `projects/PROJ-001-oss-release/` so that project validation tests pass. Per ADR-003 and the test at `tests/project_validation/architecture/test_path_conventions.py:81-99`, each project must have at least 3 of: `research`, `synthesis`, `analysis`, `decisions`, `reports`, `design`.

Currently `PROJ-001-oss-release` only contains:
```
projects/PROJ-001-oss-release/
├── PLAN.md
├── WORKTRACKER.md
├── orchestration/
└── work/
```

The tests `test_project_has_required_structure` and `test_directory_structure_complete` both assert `len(existing_dirs) >= 3` from the expected set.

Additionally, the `TestCategoryConventions.test_only_valid_categories_used` test verifies all directories match the valid categories set: `{research, synthesis, analysis, decisions, reports, design, investigations, reviews, work, runbooks}`. The existing `orchestration/` directory is **not** in this valid set, which will cause a separate test failure.

### Acceptance Criteria

- [ ] At least 3 category directories created in `PROJ-001-oss-release/` from: research, synthesis, analysis, decisions, reports, design
- [ ] Each directory contains a `.gitkeep` file (so empty dirs are committed to git)
- [ ] `orchestration/` directory is either moved inside `work/` or added to the `valid_categories` fixture — needs decision (see Implementation Notes)
- [ ] `test_project_has_required_structure` passes
- [ ] `test_directory_structure_complete` passes
- [ ] `test_only_valid_categories_used` passes
- [ ] Fix works across Python 3.11-3.14 on both pip and uv CI jobs

### Implementation Notes

**Category directories to create:**
```bash
mkdir -p projects/PROJ-001-oss-release/{research,analysis,decisions}
touch projects/PROJ-001-oss-release/research/.gitkeep
touch projects/PROJ-001-oss-release/analysis/.gitkeep
touch projects/PROJ-001-oss-release/decisions/.gitkeep
```

These 3 satisfy the minimum requirement. `work/` already exists and is in the valid set.

**The `orchestration/` directory issue:**

The `orchestration/` directory exists in `PROJ-001-oss-release` but is NOT in the `valid_categories` fixture in `conftest.py`. This will cause `test_only_valid_categories_used` to fail with:
```
Invalid category directory: orchestration
```

Options:
1. **Add `orchestration` to `valid_categories`** — This is a legitimate project category used by the orchestration skill
2. **Move orchestration artifacts under `work/`** — Keeps the valid categories unchanged
3. **Add to `allowed_extras`** in the test — Like `tests` and `.jerry`

Option 1 is recommended since `orchestration/` is a first-class project directory per the orchestration skill.

### Files Involved

| File | Role | Change Needed |
|------|------|---------------|
| `projects/PROJ-001-oss-release/research/.gitkeep` | New file | Create empty directory marker |
| `projects/PROJ-001-oss-release/analysis/.gitkeep` | New file | Create empty directory marker |
| `projects/PROJ-001-oss-release/decisions/.gitkeep` | New file | Create empty directory marker |
| `tests/project_validation/conftest.py` | Test fixture | Add `orchestration` to `valid_categories` (line 168) |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Category directories | Filesystem | `projects/PROJ-001-oss-release/{research,analysis,decisions}/` |
| Updated valid_categories | Code | `tests/project_validation/conftest.py:168` |

### Verification

- [ ] `ls projects/PROJ-001-oss-release/` shows research, analysis, decisions directories
- [ ] `uv run pytest tests/project_validation/architecture/test_path_conventions.py -v` passes
- [ ] `uv run pytest tests/project_validation/integration/test_file_resolution.py -v` passes

---

## Related Items

- Parent: [BUG-005: Project validation tests reference non-existent PROJ-001-plugin-cleanup](./BUG-005-project-validation-missing-artifacts.md)
- Enabler: [EN-002: Fix Test Infrastructure](./EN-002-fix-test-infrastructure.md)
- Feature: [FEAT-001: Fix CI Build Failures](../FEAT-001-fix-ci-build-failures.md)
- Sibling: [TASK-001: Wire dynamic project discovery into project_id fixture](./BUG-005--TASK-001-wire-dynamic-project-discovery.md) (both needed for tests to pass)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-11 | pending | Created. Category directories + orchestration valid_categories fix. |
