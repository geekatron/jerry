# TASK-001: Context Loading Mechanisms Research

<!--
TEMPLATE: Task
VERSION: 0.1.0
-->

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Frontmatter](#frontmatter) | Task metadata |
| [Description](#description) | Loading mechanisms and acceptance criteria |
| [History](#history) | Change log |

---

## Frontmatter

```yaml
id: "TASK-001"
work_type: TASK
title: "Context Loading Mechanisms Research"
status: DONE
priority: CRITICAL
assignee: "ps-researcher-claude-md"
parent_id: "EN-103"
effort: 2
activity: RESEARCH
```

---

## Description

Research Claude Code context loading mechanisms including CLAUDE.md, .claude/rules/, skills, and @ import syntax.

### Loading Mechanisms Discovered

| Mechanism | Loading | Best For |
|-----------|---------|----------|
| CLAUDE.md | Always at session start | Identity, navigation |
| .claude/rules/*.md | Auto-loaded by Claude Code | Standards, rules |
| @file.md syntax | Eager on reference | Critical dependencies |
| Plain file reference | Lazy on access | Supporting docs |
| Skills | On-demand via /skill | Specialized workflows |

### Acceptance Criteria

- [x] All loading mechanisms documented
- [x] Auto-load vs on-demand distinguished
- [x] @ import syntax behavior verified

### Related Items

- Parent: [EN-103](./EN-103-claude-md-optimization.md)
- Output: [claude-md-best-practices.md](../orchestration/oss-release-20260131-001/ps/phase-0/ps-researcher-claude-md/claude-md-best-practices.md)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-01 | DONE | Research complete |
