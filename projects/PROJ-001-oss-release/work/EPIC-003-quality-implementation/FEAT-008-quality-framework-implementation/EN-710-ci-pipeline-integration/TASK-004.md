# TASK-004: Integrate Ruff Linting into CI

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 0.1.0
-->

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this task delivers |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Implementation Notes](#implementation-notes) | Technical guidance |
| [Related Items](#related-items) | Dependencies and hierarchy |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Status changes and key events |

---

## Summary

```yaml
id: "TASK-004"
work_type: TASK
title: "Integrate ruff linting into CI"
description: |
  Add ruff linting to the CI quality workflow. Ruff enforces code style, import ordering,
  bug detection, and code quality rules per pyproject.toml configuration. Linting at CI
  level (L5) catches style and quality violations that bypass local pre-commit hooks.
classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: ""
created_by: "Claude"
created_at: "2026-02-14"
updated_at: "2026-02-14"
parent_id: "EN-710"
tags:
  - "ci-pipeline"
  - "linting"
  - "ruff"
activity: DEVELOPMENT
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Add a step to the GitHub Actions quality workflow that runs ruff linting via `uv run ruff check src/ tests/`. Ruff enforces:

- pycodestyle errors and warnings (E, W)
- Pyflakes checks (F)
- Import sorting (I)
- Bug detection (B -- flake8-bugbear)
- Code simplification (SIM)
- Type checking patterns (TCH)
- Pathlib usage (PTH)

Linting at CI level ensures code quality standards are enforced consistently, catching violations that may bypass local pre-commit hooks.

### Acceptance Criteria

- [ ] CI workflow includes a step running `uv run ruff check src/ tests/`
- [ ] Ruff uses configuration from pyproject.toml
- [ ] Linting violations cause the CI pipeline to fail
- [ ] CI step output clearly shows violation locations and rule codes

### Implementation Notes

- Ruff configuration is in `pyproject.toml` under `[tool.ruff]`
- Use `uv run ruff check src/ tests/` (not `ruff check` directly)
- Consider also running `uv run ruff format --check src/ tests/` for format verification
- Per-file ignores may apply for tests and scripts

### Related Items

- Parent: [EN-710: CI Pipeline Quality Integration](EN-710-ci-pipeline-integration.md)
- Depends on: TASK-001 (workflow must exist first)
- Blocks: TASK-006 (verification requires all test steps)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| ruff CI step | Workflow step | `.github/workflows/quality.yml` |

### Verification

- [ ] Acceptance criteria verified
- [ ] Ruff step runs successfully in CI
- [ ] Intentional linting violation correctly fails the pipeline
- [ ] Reviewed by: —

---

## History

| Date | Status | Notes |
|------------|-------------|--------------------------------|
| 2026-02-14 | Created | Initial creation from EN-710 task decomposition |
