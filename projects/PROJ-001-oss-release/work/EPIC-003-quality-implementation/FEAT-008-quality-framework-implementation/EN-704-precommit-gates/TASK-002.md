# TASK-002: Integrate Ruff Check as Pre-commit Step

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this task delivers |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Implementation Notes](#implementation-notes) | Technical guidance |
| [Related Items](#related-items) | Cross-references and dependencies |
| [Evidence](#evidence) | Proof of completion |
| [History](#history) | Change log |

---

## Frontmatter

```yaml
id: "TASK-002"
work_type: TASK
title: "Integrate Ruff Check as Pre-commit Step"
description: |
  Add ruff linting and formatting as a pre-commit step to enforce
  code style, import ordering, and common Python issues. Configure
  to match Jerry's pyproject.toml ruff settings.
classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: ""
created_by: "Claude"
created_at: "2026-02-14"
updated_at: "2026-02-14"
parent_id: "EN-704"
tags:
  - "pre-commit"
  - "ruff"
  - "linting"
  - "formatting"
activity: DEVELOPMENT
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Summary

Add ruff linting and formatting as pre-commit hooks. Ruff is Jerry's unified linting and formatting tool (per tool-configuration.md decision). The pre-commit step must use the same configuration as `pyproject.toml` to ensure consistency between local development and pre-commit enforcement. This catches style violations, import ordering issues, and common Python bugs at commit time.

## Acceptance Criteria

- [ ] Ruff check hook added to `.pre-commit-config.yaml`
- [ ] Ruff format hook added to `.pre-commit-config.yaml`
- [ ] Hooks configured to use Jerry's `pyproject.toml` ruff settings
- [ ] Auto-fix enabled for ruff check (`--fix` flag)
- [ ] Both hooks pass on the current codebase without errors

## Implementation Notes

- Use `https://github.com/astral-sh/ruff-pre-commit` as the repo
- Add both `ruff` (linting) and `ruff-format` (formatting) hooks
- Pin the ruff version to match the project's dependency
- The `--fix` flag on ruff check enables auto-correction of fixable issues
- Verify compatibility with the existing `pyproject.toml` `[tool.ruff]` section

**Design Source:** tool-configuration.md Ruff Configuration section, Pre-commit Configuration section

## Related Items

- Parent: [EN-704: Pre-commit Quality Gates](EN-704-precommit-gates.md)
- Depends on: TASK-001 (base pre-commit configuration)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| _None yet_ | — | — |

### Verification

- [ ] Acceptance criteria verified
- [ ] Code review passed
- [ ] Reviewed by: _pending_

---

## History

| Date | Status | Notes |
|------------|-------------|--------------------------------|
| 2026-02-14 | Created | Initial creation |
