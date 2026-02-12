# TASK-001: @ Import Syntax Research

<!--
TEMPLATE: Task
VERSION: 0.1.0
-->

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Frontmatter](#frontmatter) | Task metadata |
| [Description](#description) | @ syntax behavior and acceptance criteria |
| [History](#history) | Change log |

---

## Frontmatter

```yaml
id: "TASK-001"
work_type: TASK
title: "@ Import Syntax Research"
status: DONE
priority: CRITICAL
assignee: "ps-researcher-decomposition"
parent_id: "EN-106"
effort: 1
activity: RESEARCH
```

---

## Description

Research the @ import syntax in Claude Code for including file content.

### @ Import Syntax

```markdown
See @docs/architecture.md for system design
Review @.claude/rules/coding-standards.md for style guide
```

### Behavior

- Content is included when Claude processes the reference
- Supports up to 5 hops of nested includes
- Best for critical context needed immediately
- Eager loading (on reference, not on demand)

### Acceptance Criteria

- [x] @ syntax behavior documented
- [x] Hop limit verified (5 levels)
- [x] Use cases identified

### Related Items

- Parent: [EN-106](./EN-106-decomposition-research.md)
- Output: [decomposition-best-practices.md](../orchestration/oss-release-20260131-001/ps/phase-0/ps-researcher-decomposition/decomposition-best-practices.md)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-01 | DONE | Research complete |
