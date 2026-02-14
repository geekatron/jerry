# TASK-002: Implement V-038 AST Import Boundary Validation

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
title: "Implement V-038 AST Import Boundary Validation"
description: |
  Parse Python AST to extract all imports. Check imports against layer
  dependency rules (domain cannot import infrastructure, application cannot
  import interface, etc.). Block file writes that introduce boundary violations.
  V-038 scored 4.92 WCS -- highest priority enforcement vector.
classification: ENABLER
status: BACKLOG
resolution: null
priority: CRITICAL
assignee: ""
created_by: "Claude"
created_at: "2026-02-14"
updated_at: "2026-02-14"
parent_id: "EN-703"
tags:
  - "enforcement"
  - "ast"
  - "import-boundary"
  - "V-038"
activity: DEVELOPMENT
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Summary

Implement the V-038 AST Import Boundary Validation checker. This vector parses Python AST to extract all import statements (both `import` and `from ... import`) and checks them against the hexagonal architecture layer dependency rules. Domain layer must not import from application, infrastructure, or interface. Application must not import from infrastructure or interface. Infrastructure must not import from interface. V-038 scored 4.92 WCS in the EN-402 priority analysis, making it the highest priority enforcement vector.

## Acceptance Criteria

- [ ] AST-based import extraction implemented (handles `import` and `from ... import`)
- [ ] Layer dependency rules encoded (domain, application, infrastructure, interface boundaries)
- [ ] Violations detected and reported with file path, line number, and violation description
- [ ] Shared kernel imports correctly allowed from all layers
- [ ] Edge cases handled: relative imports, conditional imports, TYPE_CHECKING blocks
- [ ] Checker integrates with `PreToolEnforcementEngine` via common protocol

## Implementation Notes

- Use `ast.parse()` to parse file content and `ast.walk()` to find Import/ImportFrom nodes
- Layer detection should be based on file path (e.g., `src/domain/` = domain layer)
- The dependency rules from architecture-standards.md:
  - `domain/` can import from: stdlib only (+ shared_kernel)
  - `application/` can import from: domain
  - `infrastructure/` can import from: domain, application
  - `interface/` can import from: domain, application, infrastructure
- TYPE_CHECKING imports should be excluded from enforcement

**Design Source:** EPIC-002 EN-402 (V-038 scored 4.92 WCS, highest priority vector)

## Related Items

- Parent: [EN-703: PreToolUse Enforcement Engine](EN-703-pretooluse-enforcement.md)
- Depends on: TASK-001 (engine class provides the integration point)
- Related: EN-704 TASK-003 (pre-commit boundary check reuses this logic)

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
