# TASK-002: Integrate Architecture Boundary Tests into CI

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
id: "TASK-002"
work_type: TASK
title: "Integrate architecture boundary tests into CI"
description: |
  Add architecture boundary test execution to the CI quality workflow. Architecture tests
  validate hexagonal architecture layer dependency rules (domain cannot import infrastructure,
  application cannot import interface, etc.) and ensure the composition root pattern is
  respected. These tests are critical L5 enforcement for the architecture standards.
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
  - "architecture-tests"
  - "boundary-enforcement"
activity: DEVELOPMENT
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Add a step to the GitHub Actions quality workflow that runs architecture boundary tests via `uv run pytest tests/architecture/`. These tests enforce layer dependency rules from the hexagonal architecture:

- Domain layer has no infrastructure imports
- Application layer has no interface imports
- Bootstrap is the sole infrastructure instantiation point
- CLI adapter receives dispatchers via injection

This ensures architecture violations are caught at the CI level (L5) even if local enforcement (L1-L4) is bypassed.

### Acceptance Criteria

- [ ] CI workflow includes a step running `uv run pytest tests/architecture/`
- [ ] Architecture test failures cause the CI pipeline to fail
- [ ] Architecture tests correctly validate layer boundary rules
- [ ] CI step output clearly identifies which boundary was violated on failure

### Implementation Notes

- Tests located at `tests/architecture/` per project standards
- Use `uv run pytest tests/architecture/ -v` for verbose output in CI logs
- Ensure test step depends on dependency installation step
- Consider separate job or step for architecture tests to parallelize

### Related Items

- Parent: [EN-710: CI Pipeline Quality Integration](EN-710-ci-pipeline-integration.md)
- Depends on: TASK-001 (workflow must exist first)
- Blocks: TASK-006 (verification requires all test steps)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Architecture test CI step | Workflow step | `.github/workflows/quality.yml` |

### Verification

- [ ] Acceptance criteria verified
- [ ] Architecture test step runs successfully in CI
- [ ] Intentional boundary violation correctly fails the pipeline
- [ ] Reviewed by: —

---

## History

| Date | Status | Notes |
|------------|-------------|--------------------------------|
| 2026-02-14 | Created | Initial creation from EN-710 task decomposition |
