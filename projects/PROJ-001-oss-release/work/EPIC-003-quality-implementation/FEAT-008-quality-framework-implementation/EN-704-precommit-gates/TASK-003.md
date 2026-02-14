# TASK-003: Add Architecture Boundary Check as Pre-commit Step

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
id: "TASK-003"
work_type: TASK
title: "Add Architecture Boundary Check as Pre-commit Step"
description: |
  Create a pre-commit hook that validates layer dependency rules
  (domain must not import infrastructure, etc.). Reuse AST analysis
  from EN-703's enforcement engine where possible.
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
  - "architecture"
  - "boundary-check"
  - "ast"
activity: DEVELOPMENT
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Summary

Create a pre-commit hook that validates hexagonal architecture layer dependency rules at commit time. This hook checks that domain does not import infrastructure, application does not import interface, etc. Where possible, reuse the AST analysis logic from EN-703's V-038 import boundary validation to avoid duplication. This is the L5 complement to L3's real-time import boundary enforcement.

## Acceptance Criteria

- [ ] Architecture boundary check hook added to `.pre-commit-config.yaml`
- [ ] Hook validates layer dependency rules for all staged Python files
- [ ] Reuses EN-703 V-038 import boundary logic where possible
- [ ] Clear error messages indicating which file, import, and boundary was violated
- [ ] Hook passes on the current codebase without false positives
- [ ] Hook script is executable and follows pre-commit local hook conventions

## Implementation Notes

- Can be implemented as a `local` hook in `.pre-commit-config.yaml`
- Create a script (e.g., `scripts/check_architecture_boundaries.py`) that the hook invokes
- Import and reuse the V-038 checker from EN-703 if available, otherwise implement standalone
- The hook receives a list of staged files as arguments
- Only check `.py` files within `src/` directory
- Exit code 0 = pass, non-zero = fail

**Design Source:** EPIC-002 EN-404 (rule enforcement), architecture-standards.md Dependency Rules section

## Related Items

- Parent: [EN-704: Pre-commit Quality Gates](EN-704-precommit-gates.md)
- Depends on: TASK-001 (base pre-commit configuration)
- Related: EN-703 TASK-002 (V-038 import boundary validation -- reuse logic)

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
