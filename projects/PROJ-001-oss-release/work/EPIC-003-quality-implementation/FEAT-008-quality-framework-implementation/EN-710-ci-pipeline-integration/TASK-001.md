# TASK-001: Create GitHub Actions Quality Workflow Configuration

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
| [Time Tracking](#time-tracking) | Effort estimates and actuals |
| [Related Items](#related-items) | Dependencies and hierarchy |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Status changes and key events |

---

## Summary

```yaml
id: "TASK-001"
work_type: TASK
title: "Create GitHub Actions quality workflow configuration"
description: |
  Create the foundational GitHub Actions workflow file (.github/workflows/quality.yml)
  that will serve as the CI pipeline for quality enforcement. This workflow defines the
  pipeline structure, triggers, environment setup (UV-based Python), and job orchestration
  for all quality checks (architecture tests, type checking, linting, quality gates).
classification: ENABLER
status: DONE
resolution: null
priority: HIGH
assignee: ""
created_by: "Claude"
created_at: "2026-02-14"
updated_at: "2026-02-14"
parent_id: "EN-710"
tags:
  - "ci-pipeline"
  - "github-actions"
  - "quality-enforcement"
activity: DEVELOPMENT
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Create the `.github/workflows/quality.yml` file that defines the CI pipeline for quality enforcement. The workflow must:
- Trigger on push and pull request events
- Use UV for all Python operations (per project standards -- never use pip or system Python)
- Set up Python 3.11+ environment
- Define job structure for subsequent quality check steps (architecture tests, mypy, ruff)
- Configure appropriate caching for UV dependencies

This is the foundational task -- TASK-002 through TASK-004 depend on this workflow existing.

### Acceptance Criteria

- [ ] `.github/workflows/quality.yml` file exists with valid GitHub Actions syntax
- [ ] Workflow triggers on push to main and pull request events
- [ ] UV is used for all Python operations (no pip, no system Python)
- [ ] Python 3.11+ environment is correctly configured
- [ ] Dependency caching is configured for UV
- [ ] Workflow YAML passes GitHub Actions validation (valid syntax)

### Implementation Notes

- Follow UV-only pattern per `.context/rules/python-environment.md`
- Reference existing CI patterns from `.github/workflows/` if any exist
- Use `uv sync` for dependency installation, `uv run` for command execution
- Consider matrix strategy for Python version testing if appropriate

### Related Items

- Parent: [EN-710: CI Pipeline Quality Integration](EN-710-ci-pipeline-integration.md)
- Blocks: TASK-002 (architecture tests), TASK-003 (mypy), TASK-004 (ruff), TASK-005 (branch protection)

---

## Time Tracking

| Metric | Value |
|--------|-------|
| Original Estimate | — |
| Remaining Work | 0 hours |
| Time Spent | — |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| quality.yml | Workflow | `.github/workflows/quality.yml` |

### Verification

- [ ] Acceptance criteria verified
- [ ] Workflow YAML is valid GitHub Actions syntax
- [ ] UV is used exclusively for Python operations
- [ ] Reviewed by: —

---

## History

| Date | Status | Notes |
|------------|-------------|--------------------------------|
| 2026-02-14 | Created | Initial creation from EN-710 task decomposition |
