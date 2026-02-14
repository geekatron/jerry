# TASK-005: Implement V-041 AST One-Class-Per-File Check

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
title: "Implement V-041 AST One-Class-Per-File Check"
description: |
  Count public class definitions per file via AST. Flag files with more
  than one public class (classes not prefixed with underscore).
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
  - "one-class-per-file"
  - "V-041"
activity: DEVELOPMENT
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Summary

Implement the V-041 AST One-Class-Per-File Check. This vector counts public class definitions per file via AST analysis and flags files containing more than one public class. Public classes are those without a leading underscore prefix. This enforces the mandatory one-class-per-file rule from Jerry's file organization standards, preventing multi-class files from being written through the PreToolUse hook.

## Acceptance Criteria

- [ ] AST-based public class counting implemented
- [ ] Files with more than one public class flagged as violations
- [ ] Private classes (underscore prefix) excluded from the count
- [ ] Violation report includes the names and line numbers of all public classes found
- [ ] Exception handling: test files and `__init__.py` files may be excluded or configurable
- [ ] Checker integrates with `PreToolEnforcementEngine` via common protocol

## Implementation Notes

- Use `ast.ClassDef` nodes at the module level to find class definitions
- Public classes: name does not start with underscore
- The one-class-per-file rule from file-organization.md has one exception: "Related small value objects may be grouped"
- Consider making exclusions configurable (e.g., test files, `__init__.py`)
- Report should list all public classes found when count > 1

**Design Source:** EPIC-002 EN-403/TASK-003 (PreToolUse design), file-organization.md One Class Per File Rule section

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
