# TASK-003: Add paths frontmatter to testing-standards.md

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

Add YAML frontmatter with `paths: ["tests/**/*.py"]` to `testing-standards.md`.

The frontmatter should be added at the very top of the file, before the existing title:

```yaml
---
paths:
  - "tests/**/*.py"
---
```

Testing standards (H-20 BDD test-first, H-21 90% coverage, test pyramid, naming conventions) are primarily relevant when editing test files.

### Acceptance Criteria

- [ ] YAML frontmatter present at top of file
- [ ] `paths` field set to `["tests/**/*.py"]`
- [ ] Manual load test passed (test file editing loads rule)
- [ ] Manual load test passed (markdown editing does NOT load rule)

### Implementation Notes

Ensure the frontmatter does not break the file parsing or the `.claude/rules/` symlink. Consider whether `tests/` path alone is sufficient or if `src/` should also be included (since H-20 BDD test-first applies when writing implementation code too). The current specification targets `tests/` only.

### Related Items

- Parent: [EN-904: Path Scoping Implementation](EN-904-path-scoping.md)
- Parallel: TASK-001, TASK-002 (other scoping tasks)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Scoped testing-standards.md | Code change | pending |

### Verification

- [ ] Acceptance criteria verified
- [ ] Manual load test documented
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Initial creation. Part of EN-904 path scoping. |
