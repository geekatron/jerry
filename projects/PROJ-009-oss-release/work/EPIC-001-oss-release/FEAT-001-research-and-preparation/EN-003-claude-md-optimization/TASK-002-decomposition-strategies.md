# TASK-002: Decomposition Strategies Research

<!--
TEMPLATE: Task
VERSION: 0.1.0
-->

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Frontmatter](#frontmatter) | Task metadata |
| [Description](#description) | Industry best practices and acceptance criteria |
| [History](#history) | Change log |

---

## Frontmatter

```yaml
id: "TASK-002"
work_type: TASK
title: "Decomposition Strategies Research"
status: DONE
priority: CRITICAL
assignee: "ps-researcher-claude-md"
parent_id: "EN-003"
effort: 2
activity: RESEARCH
```

---

## Description

Research decomposition strategies for large CLAUDE.md files including tiered approaches, progressive disclosure, and content organization.

### Industry Best Practices Found

From HumanLayer, Builder.io, and Anthropic:

1. **Keep it Lean and Focused**: "Less (instructions) is more"
2. **Progressive Disclosure**: "Tell Claude how to find information, not all the information"
3. **Pointers Over Copies**: "Include file:line references to point Claude to authoritative context"
4. **Modular Rules**: "Each file in .claude/rules/ should cover one topic"

### Acceptance Criteria

- [x] Industry sources analyzed
- [x] Decomposition patterns documented
- [x] Progressive disclosure strategy defined

### Related Items

- Parent: [EN-003](./EN-003-claude-md-optimization.md)
- Output: [claude-md-best-practices.md](../orchestration/oss-release-20260131-001/ps/phase-0/ps-researcher-claude-md/claude-md-best-practices.md)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-01 | DONE | Research complete |
