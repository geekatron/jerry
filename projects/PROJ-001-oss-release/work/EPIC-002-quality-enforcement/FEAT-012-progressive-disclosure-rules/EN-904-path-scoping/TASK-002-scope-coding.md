# TASK-002: Add paths frontmatter to coding-standards.md

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** BACKLOG
> **Priority:** HIGH
> **Activity:** DEVELOPMENT
> **Created:** 2026-02-16
> **Parent:** EN-904

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Content](#content) | Description, acceptance criteria, implementation notes |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Status changes and key events |

---

## Content

### Description

Add YAML frontmatter with `paths: ["src/**/*.py", "tests/**/*.py"]` to `coding-standards.md`.

The frontmatter should be added at the very top of the file, before the existing title:

```yaml
---
paths:
  - "src/**/*.py"
  - "tests/**/*.py"
---
```

Coding standards (H-11 type hints, H-12 docstrings, naming conventions, error handling) apply to both source and test code, so both `src/` and `tests/` paths are included.

### Acceptance Criteria

- [ ] YAML frontmatter present at top of file
- [ ] `paths` field covers both `src/` and `tests/`
- [ ] Manual load test passed (Python editing loads rule)
- [ ] Manual load test passed (markdown editing does NOT load rule)

### Implementation Notes

Ensure the frontmatter does not break the file parsing or the `.claude/rules/` symlink. The coding-standards rules are relevant to both source code and test code, so both glob patterns must be included.

### Related Items

- Parent: [EN-904: Path Scoping Implementation](EN-904-path-scoping.md)
- Parallel: TASK-001, TASK-003 (other scoping tasks)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Scoped coding-standards.md | Code change | pending |

### Verification

- [ ] Acceptance criteria verified
- [ ] Manual load test documented
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Initial creation. Part of EN-904 path scoping. |
