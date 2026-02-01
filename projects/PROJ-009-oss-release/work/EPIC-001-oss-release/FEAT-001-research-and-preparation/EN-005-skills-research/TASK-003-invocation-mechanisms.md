# TASK-003: Invocation Mechanisms Research

<!--
TEMPLATE: Task
VERSION: 0.1.0
-->

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Frontmatter](#frontmatter) | Task metadata |
| [Description](#description) | Invocation patterns and acceptance criteria |
| [History](#history) | Change log |

---

## Frontmatter

```yaml
id: "TASK-003"
work_type: TASK
title: "Invocation Mechanisms Research"
status: DONE
priority: HIGH
assignee: "ps-researcher-skills"
parent_id: "EN-005"
effort: 1
activity: RESEARCH
```

---

## Description

Research skill invocation mechanisms including /skill syntax and auto-suggestion.

### Invocation Patterns

1. **Explicit**: `/worktracker` - User invokes skill directly
2. **Context-based**: Claude suggests skill based on conversation
3. **Mandatory**: CLAUDE.md specifies when skills MUST be used

### On-Demand Loading Benefits

- Skills only loaded when invoked
- Reduces always-loaded token count
- Enables focused context for specific tasks

### Acceptance Criteria

- [x] Invocation patterns documented
- [x] Auto-suggestion mechanism researched
- [x] Token benefits quantified

### Related Items

- Parent: [EN-005](./EN-005-skills-research.md)
- Output: [skills-best-practices.md](../orchestration/oss-release-20260131-001/ps/phase-0/ps-researcher-skills/skills-best-practices.md)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-01 | DONE | Research complete |
