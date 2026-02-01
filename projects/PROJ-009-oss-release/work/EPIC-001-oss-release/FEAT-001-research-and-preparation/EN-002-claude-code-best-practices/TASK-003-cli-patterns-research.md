# TASK-003: CLI Patterns Research

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Frontmatter](#frontmatter) | Task metadata |
| [Description](#description) | Key findings and acceptance criteria |
| [History](#history) | Change log |

---

## Frontmatter

```yaml
id: "TASK-003"
work_type: TASK
title: "CLI Patterns Research"
status: DONE
priority: MEDIUM
assignee: "ps-researcher-claude-code"
parent_id: "EN-002"
effort: 1
activity: RESEARCH
```

---

## Description

Research Claude Code CLI patterns including command structure, output formatting, and integration with IDE extensions.

### Key Findings

- CLI follows namespace pattern (jerry session/items/projects)
- JSON output mode for programmatic access
- Exit codes follow Unix conventions

### Acceptance Criteria

- [x] Command patterns documented
- [x] Output formatting researched
- [x] IDE integration patterns identified

### Related Items

- Parent: [EN-002](./EN-002-claude-code-best-practices.md)
- Output: [claude-code-best-practices.md](../orchestration/oss-release-20260131-001/ps/phase-0/ps-researcher-claude-code/claude-code-best-practices.md)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-01 | DONE | Research complete |
