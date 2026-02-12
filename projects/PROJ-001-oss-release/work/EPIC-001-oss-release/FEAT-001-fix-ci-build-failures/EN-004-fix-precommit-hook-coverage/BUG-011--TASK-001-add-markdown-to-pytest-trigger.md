# TASK-001: Add markdown file types to pytest pre-commit hook trigger

> **Type:** task
> **Status:** done
> **Priority:** high
> **Created:** 2026-02-11
> **Completed:** 2026-02-11
> **Parent:** BUG-011
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

Modify `.pre-commit-config.yaml` so that the pytest hook also triggers on markdown file changes, not just Python files. This ensures architecture tests that validate markdown content (hardcoded paths, cross-project references) run locally before commits reach CI.

### Acceptance Criteria

- [x] Markdown-only commits trigger pytest execution
- [x] Python-only commits continue to trigger pytest as before
- [x] Mixed Python+markdown commits trigger pytest once (not twice)
- [x] Hook execution time is reasonable (project validation tests add ~5-10s)
- [x] Configuration change is documented with a comment explaining why markdown is included
- [x] `pre-commit run --all-files` passes with the updated configuration

### Implementation Notes

**Option A: Add markdown to existing hook types (Recommended)**

Replace `types: [python]` with `types_or: [python, markdown]` on the pytest hook:

```yaml
- id: pytest
  name: pytest (full suite via uv)
  entry: uv run pytest
  language: system
  types_or: [python, markdown]
  pass_filenames: false
  stages: [pre-commit]
  args: [--tb=short, -q]
```

`types_or` means "trigger if ANY of these types are staged" (vs `types` which requires ALL).

**Option B: Separate project validation hook**

Add a dedicated hook that only runs architecture tests on markdown changes:

```yaml
- id: project-validation
  name: project validation (markdown)
  entry: uv run pytest tests/project_validation/ --tb=short -q
  language: system
  types: [markdown]
  pass_filenames: false
  stages: [pre-commit]
```

**Trade-offs:**
- Option A is simpler but runs the full test suite on markdown changes
- Option B is targeted but adds a second hook definition to maintain
- Option A is recommended because the full suite catches cross-cutting issues and the runtime difference is minimal with `pass_filenames: false`

### Files Involved

| File | Change Description |
|------|-------------------|
| `.pre-commit-config.yaml` | Change pytest hook `types: [python]` to `types_or: [python, markdown]` |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Updated pre-commit config | Config | `.pre-commit-config.yaml` |

### Verification

- [x] Stage only a `.md` file → pytest runs
- [x] Stage only a `.py` file → pytest runs
- [x] Stage both `.md` and `.py` → pytest runs once
- [x] `pre-commit run --all-files` passes
- [x] `uv run pytest tests/` passes

---

## Related Items

- Parent: [BUG-011: Pre-commit pytest hook only triggers on Python file changes](./BUG-011-precommit-pytest-python-only.md)
- Enabler: [EN-004: Fix Pre-commit Hook Coverage](./EN-004-fix-precommit-hook-coverage.md)
- Feature: [FEAT-001: Fix CI Build Failures](../FEAT-001-fix-ci-build-failures.md)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-11 | pending | Task created. Option A (types_or) recommended over separate hook. |
| 2026-02-11 | done | Option A implemented: `types_or: [python, markdown]` applied to pytest hook in `.pre-commit-config.yaml`. All pre-commit hooks pass. |
