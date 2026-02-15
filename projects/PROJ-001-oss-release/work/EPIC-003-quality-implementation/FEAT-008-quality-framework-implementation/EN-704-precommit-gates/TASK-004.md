# TASK-004: Add Type Hint Validation as Pre-commit Step

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
| [Time Tracking](#time-tracking) | Effort estimates and actuals |
| [Related Items](#related-items) | Cross-references and dependencies |
| [Evidence](#evidence) | Proof of completion |
| [History](#history) | Change log |

---

## Frontmatter

```yaml
id: "TASK-004"
work_type: TASK
title: "Add Type Hint Validation as Pre-commit Step"
description: |
  Configure mypy or a lightweight type hint checker as a pre-commit step
  to catch missing type annotations on public APIs at commit time.
classification: ENABLER
status: DONE
resolution: null
priority: MEDIUM
assignee: ""
created_by: "Claude"
created_at: "2026-02-14"
updated_at: "2026-02-14"
parent_id: "EN-704"
tags:
  - "pre-commit"
  - "mypy"
  - "type-hints"
  - "type-checking"
activity: DEVELOPMENT
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Summary

Configure mypy (or a lightweight alternative) as a pre-commit step to catch missing type annotations and type errors at commit time. This complements EN-703's V-039 real-time type hint enforcement by providing deeper static analysis at the commit boundary. The mypy configuration must match Jerry's `pyproject.toml` `[tool.mypy]` settings for consistency.

## Acceptance Criteria

- [ ] Type hint validation hook added to `.pre-commit-config.yaml`
- [ ] Hook configured to use Jerry's mypy settings from `pyproject.toml`
- [ ] Missing type annotations on public APIs detected
- [ ] Hook passes on the current codebase (baseline violations addressed or suppressed)
- [ ] Per-module overrides respected (e.g., relaxed rules for tests)

## Implementation Notes

- Use `https://github.com/pre-commit/mirrors-mypy` as the repo
- Include `additional_dependencies` for type stubs as needed
- The existing `[tool.mypy]` configuration in `pyproject.toml` sets `strict = true`
- May need to address pre-existing type errors or add `# type: ignore` comments
- Consider running mypy only on staged files for performance

**Design Source:** tool-configuration.md mypy Configuration section

## Related Items

- Parent: [EN-704: Pre-commit Quality Gates](EN-704-precommit-gates.md)
- Depends on: TASK-001 (base pre-commit configuration)
- Related: EN-703 TASK-003 (V-039 type hint enforcement at L3)

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
