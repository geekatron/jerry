# TASK-003: Integrate Type Checking (mypy) into CI

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
id: "TASK-003"
work_type: TASK
title: "Integrate type checking (mypy) into CI"
description: |
  Add mypy type checking to the CI quality workflow. mypy enforces type safety across the
  codebase in strict mode per pyproject.toml configuration. Type checking at CI level (L5)
  catches type errors that may bypass local development checks.
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
  - "type-checking"
  - "mypy"
activity: DEVELOPMENT
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Add a step to the GitHub Actions quality workflow that runs mypy type checking via `uv run mypy src/`. mypy must run in strict mode as configured in `pyproject.toml`. This enforces:

- All public functions have type hints
- No implicit `Any` types
- Return types are explicit
- Type narrowing is correct

Type checking at CI level ensures type safety is maintained regardless of local environment configuration.

### Acceptance Criteria

- [ ] CI workflow includes a step running `uv run mypy src/`
- [ ] mypy runs in strict mode per pyproject.toml configuration
- [ ] Type errors cause the CI pipeline to fail
- [ ] CI step output clearly shows type error locations and descriptions

### Implementation Notes

- mypy configuration is in `pyproject.toml` under `[tool.mypy]`
- Use `uv run mypy src/` (not `python -m mypy`)
- Strict mode settings: `disallow_untyped_defs`, `warn_return_any`, etc.
- Per-module overrides for tests and scripts may relax strictness

### Related Items

- Parent: [EN-710: CI Pipeline Quality Integration](EN-710-ci-pipeline-integration.md)
- Depends on: TASK-001 (workflow must exist first)
- Blocks: TASK-006 (verification requires all test steps)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| mypy CI step | Workflow step | `.github/workflows/quality.yml` |

### Verification

- [ ] Acceptance criteria verified
- [ ] mypy step runs successfully in CI
- [ ] Intentional type error correctly fails the pipeline
- [ ] Reviewed by: —

---

## History

| Date | Status | Notes |
|------------|-------------|--------------------------------|
| 2026-02-14 | Created | Initial creation from EN-710 task decomposition |
