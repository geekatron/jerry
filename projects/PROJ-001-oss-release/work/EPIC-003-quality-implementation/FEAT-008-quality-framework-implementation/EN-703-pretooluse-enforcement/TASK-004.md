# TASK-004: Implement V-040 AST Docstring Enforcement

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
id: "TASK-004"
work_type: TASK
title: "Implement V-040 AST Docstring Enforcement"
description: |
  Parse AST to check for docstrings on all public classes, functions,
  and methods. Verify presence (not content quality) of docstring nodes.
classification: ENABLER
status: BACKLOG
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
  - "docstrings"
  - "V-040"
activity: DEVELOPMENT
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Summary

Implement the V-040 AST Docstring Enforcement checker. This vector parses the Python AST to verify that all public classes, functions, and methods have docstrings present. The check validates presence only, not content quality -- ensuring a docstring node exists as the first statement in the body. This enforces the Jerry coding standard "REQUIRED on all public functions, classes, and modules" at write-time.

## Acceptance Criteria

- [ ] AST-based docstring presence check implemented for public classes
- [ ] AST-based docstring presence check implemented for public functions
- [ ] AST-based docstring presence check implemented for public methods
- [ ] Private classes/functions/methods (underscore prefix) excluded from enforcement
- [ ] Module-level docstring presence checked
- [ ] Violations reported with entity name, entity type, and line number
- [ ] Checker integrates with `PreToolEnforcementEngine` via common protocol

## Implementation Notes

- Use `ast.get_docstring(node)` to check for docstring presence on class/function nodes
- Public entities are those without a leading underscore (except dunder methods)
- For module-level docstrings, check the first statement of the module body
- Dunder methods like `__init__`, `__str__` should have docstrings enforced
- Empty docstrings (just `""""""`) should be flagged as missing

**Design Source:** EPIC-002 EN-403/TASK-003 (PreToolUse design), coding-standards.md Docstrings section

## Related Items

- Parent: [EN-703: PreToolUse Enforcement Engine](EN-703-pretooluse-enforcement.md)
- Depends on: TASK-001 (engine class provides the integration point)

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
