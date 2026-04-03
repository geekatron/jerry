# STORY-001: Research Anthropic Official Agent Definition Schema

<!--
TEMPLATE: Story
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
PURPOSE: Research and document all official Claude Code agent .md frontmatter fields
-->

> **Type:** story
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Created:** 2026-03-26T22:10:00Z
> **Due:**
> **Completed:** 2026-03-26T23:00:00Z
> **Parent:** FEAT-001
> **Owner:** adam.nowak
> **Effort:** 5

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [User Story](#user-story) | As a / I want / So that |
| [Summary](#summary) | Research scope and approach |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Children (Tasks)](#children-tasks) | Task breakdown |
| [Progress Summary](#progress-summary) | Overall progress |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Status changes |

---

## User Story

**As a** Jerry framework developer

**I want** an authoritative, research-backed inventory of all official Claude Code agent frontmatter fields

**So that** our agent definition schema (claude-code-frontmatter-v1.schema.json) accurately reflects what Anthropic actually supports and enforces at runtime

---

## Summary

Conduct systematic web research using Anthropic's official documentation, Claude Code GitHub repository, and community resources to discover and document every YAML frontmatter field that Claude Code recognizes for agent .md files. Document field types, constraints, defaults, and behavioral effects.

**Scope:**
- All 12+ documented frontmatter fields (name, description, model, tools, disallowedTools, mcpServers, permissionMode, maxTurns, skills, hooks, memory, background, isolation)
- Any undocumented or recently added fields
- Field interaction behaviors (e.g., tool inheritance when tools is omitted)
- Agent discovery mechanism (how Claude Code finds .md files in agents/ directories)

---

## Acceptance Criteria

- [ ] All official Claude Code agent frontmatter fields documented with type, constraints, and defaults
- [ ] Each field's behavioral effect documented (what happens at runtime)
- [ ] Field interaction behaviors documented (inheritance, overrides, conflicts)
- [ ] Agent discovery mechanism documented (directory scanning, naming conventions)
- [ ] All sources cited with URLs and access dates
- [ ] Findings compared against existing `docs/schemas/claude-code-frontmatter-v1.schema.json`
- [ ] Research artifact persisted to `projects/PROJ-024-tactical-work/work/research/anthropic-agent-schema-research.md`

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Owner |
|----|-------|--------|-------|
| TASK-001 | Web research: Anthropic docs, GitHub, community | in_progress | ps-researcher |
| TASK-002 | Document field inventory with types and constraints | pending | -- |
| TASK-003 | Compare against existing schema | pending | -- |

---

## Progress Summary

```
+------------------------------------------------------------------+
|                    STORY PROGRESS TRACKER                         |
+------------------------------------------------------------------+
| Tasks:     [######..............] 30% (0/3 completed)             |
+------------------------------------------------------------------+
| Overall:   [######..............] 30%                              |
+------------------------------------------------------------------+
```

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-001: Claude Code Schema Validation](../FEAT-001-claude-code-schema-validation.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Blocks | STORY-003 | Gap analysis needs this research output |
| Related | STORY-002 | Parallel skill schema research |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-26 | adam.nowak | in_progress | Story created; ps-researcher agent launched |
