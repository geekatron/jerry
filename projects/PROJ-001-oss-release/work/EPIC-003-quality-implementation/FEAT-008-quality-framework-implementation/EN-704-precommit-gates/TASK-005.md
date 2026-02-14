# TASK-005: Validate Pre-commit Hooks on Current Codebase

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
id: "TASK-005"
work_type: TASK
title: "Validate Pre-commit Hooks on Current Codebase"
description: |
  Ensure all pre-commit hooks pass on the existing codebase before merging.
  Fix any pre-existing violations or configure appropriate baselines.
  Verify uv run pytest passes after all changes.
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
  - "validation"
  - "baseline"
  - "testing"
activity: TESTING
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Summary

Run all configured pre-commit hooks against the entire existing codebase to verify they pass cleanly. Fix any pre-existing violations that are discovered, or configure appropriate baselines/exclusions for known issues that cannot be immediately resolved. This ensures that the pre-commit gates do not introduce false positives or block legitimate development. Also verify that `uv run pytest` passes after all changes.

## Acceptance Criteria

- [ ] `pre-commit run --all-files` executes without errors
- [ ] All pre-existing violations fixed or explicitly baselined with justification
- [ ] No false positives from architecture boundary checks
- [ ] No false positives from type hint validation
- [ ] `uv run pytest` passes after all fixes and configuration changes
- [ ] Baseline exclusions documented if any were necessary

## Implementation Notes

- Run `pre-commit run --all-files` to check the entire codebase
- Address violations in priority order: fix > baseline > exclude
- For legitimate exclusions, add comments explaining why
- If mypy reveals many pre-existing type errors, consider a phased approach
- Run `uv run pytest` as the final validation step
- Document any baseline decisions for future reference

**Design Source:** testing-standards.md (validation requirements)

## Related Items

- Parent: [EN-704: Pre-commit Quality Gates](EN-704-precommit-gates.md)
- Depends on: TASK-001 through TASK-004 (all hooks must be configured first)

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
