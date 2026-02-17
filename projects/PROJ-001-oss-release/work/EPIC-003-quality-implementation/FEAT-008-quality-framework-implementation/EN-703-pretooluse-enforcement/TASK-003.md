# TASK-003: Implement V-039 AST Type Hint Enforcement

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
id: "TASK-003"
work_type: TASK
title: "Implement V-039 AST Type Hint Enforcement"
description: |
  Parse function/method signatures via AST. Verify all public functions
  and methods have type annotations on parameters and return types.
  Flag missing type hints on public API surfaces.
classification: ENABLER
status: DONE
resolution: null
priority: HIGH
assignee: ""
created_by: "Claude"
created_at: "2026-02-14"
updated_at: "2026-02-14"
parent_id: "EN-703"
tags:
  - "enforcement"
  - "ast"
  - "type-hints"
  - "V-039"
activity: DEVELOPMENT
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Summary

Implement the V-039 AST Type Hint Enforcement checker. This vector parses Python function and method signatures via AST to verify that all public functions and methods have type annotations on their parameters and return types. Private functions (prefixed with underscore) are excluded from enforcement. This ensures the Jerry coding standard of "type hints REQUIRED on all public functions and methods" is enforced deterministically at write-time.

## Acceptance Criteria

- [ ] AST-based function/method signature parsing implemented
- [ ] Missing parameter type annotations detected on public functions
- [ ] Missing return type annotations detected on public functions
- [ ] Private functions/methods (underscore prefix) excluded from enforcement
- [ ] `self` and `cls` parameters excluded from type hint requirement
- [ ] Violations reported with function name, parameter name, and line number
- [ ] Checker integrates with `PreToolEnforcementEngine` via common protocol

## Implementation Notes

- Use `ast.FunctionDef` and `ast.AsyncFunctionDef` nodes to find function definitions
- Check `node.args.args` for parameter annotations and `node.returns` for return annotation
- Public functions are those without a leading underscore in their name
- `__init__` and other dunder methods: enforce parameter types but return type is optional for `__init__`
- Consider method context: methods inside classes need `self`/`cls` exclusion

**Design Source:** EPIC-002 EN-403/TASK-003 (PreToolUse design), coding-standards.md Type Hints section

## Related Items

- Parent: [EN-703: PreToolUse Enforcement Engine](EN-703-pretooluse-enforcement.md)
- Depends on: TASK-001 (engine class provides the integration point)
- Related: EN-704 TASK-004 (pre-commit type hint validation complements this)

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
