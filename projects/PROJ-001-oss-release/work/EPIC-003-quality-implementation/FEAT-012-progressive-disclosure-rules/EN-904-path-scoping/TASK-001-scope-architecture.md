# TASK-001: Add paths frontmatter to architecture-standards.md

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

Add YAML frontmatter with `paths: ["src/**/*.py"]` to `architecture-standards.md`. Verify file still loads correctly when editing Python and does NOT load when editing markdown.

The frontmatter should be added at the very top of the file, before the existing title:

```yaml
---
paths:
  - "src/**/*.py"
---
```

This ensures architecture layer boundaries (H-07, H-08, H-09, H-10) only load when Claude is editing source code files, not when editing documentation or worktracker files.

### Acceptance Criteria

- [ ] YAML frontmatter present at top of file
- [ ] `paths` field set to `["src/**/*.py"]`
- [ ] Manual load test passed (Python editing loads rule)
- [ ] Manual load test passed (markdown editing does NOT load rule)

### Implementation Notes

The `.claude/rules/` symlink points to `.context/rules/`. Ensure the frontmatter does not break the symlink or the file parsing. Test by starting a new Claude Code session editing a Python file (should see architecture rules) versus editing a markdown file (should not see architecture rules).

### Related Items

- Parent: [EN-904: Path Scoping Implementation](EN-904-path-scoping.md)
- Parallel: TASK-002, TASK-003 (other scoping tasks)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Scoped architecture-standards.md | Code change | pending |

### Verification

- [ ] Acceptance criteria verified
- [ ] Manual load test documented
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Initial creation. Part of EN-904 path scoping. |
