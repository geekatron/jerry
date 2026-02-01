# TASK-002: Discovery Mechanisms Research

<!--
TEMPLATE: Task
VERSION: 0.1.0
-->

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Frontmatter](#frontmatter) | Task metadata |
| [Description](#description) | Discovery pattern and acceptance criteria |
| [History](#history) | Change log |

---

## Frontmatter

```yaml
id: "TASK-002"
work_type: TASK
title: "Discovery Mechanisms Research"
status: DONE
priority: HIGH
assignee: "ps-researcher-plugins"
parent_id: "EN-004"
effort: 1
activity: RESEARCH
```

---

## Description

Research how Claude Code discovers and loads plugins.

### Discovery Pattern

1. Claude Code looks for `.claude-plugin/manifest.json`
2. Hooks loaded from path specified in manifest
3. Skills loaded from skills directory
4. CLAUDE.md loaded if present

### Acceptance Criteria

- [x] Discovery sequence documented
- [x] Hook loading mechanism researched
- [x] Skills discovery documented

### Related Items

- Parent: [EN-004](./EN-004-plugins-research.md)
- Output: [plugins-best-practices.md](../orchestration/oss-release-20260131-001/ps/phase-0/ps-researcher-plugins/plugins-best-practices.md)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-01 | DONE | Research complete |
