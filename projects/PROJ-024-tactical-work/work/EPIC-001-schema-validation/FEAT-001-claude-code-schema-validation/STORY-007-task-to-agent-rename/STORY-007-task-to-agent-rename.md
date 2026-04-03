# STORY-007: Update Task->Agent Tool Rename Across Rule Files

<!--
TEMPLATE: Story
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
PURPOSE: Update all references to the deprecated "Task" tool name to "Agent" across Jerry rule files
-->

> **Type:** story
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Created:** 2026-03-27T06:00:00Z
> **Due:**
> **Completed:** 2026-03-27T03:00:00Z
> **Parent:** FEAT-001
> **Owner:** adam.nowak
> **Effort:** 3

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [User Story](#user-story) | As a / I want / So that |
| [Summary](#summary) | Scope of the rename |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Children (Tasks)](#children-tasks) | Task breakdown |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Status changes |

---

## User Story

**As a** Jerry framework developer reading the rule files

**I want** references to the subagent spawning tool to use its current name ("Agent") instead of the deprecated name ("Task")

**So that** the documentation matches current Claude Code behavior and hook scripts don't silently miss events due to the tool_name change

---

## Summary

Claude Code v2.1.63 renamed the `Task` tool to `Agent` (#29677). The old name still works as a runtime alias, but hook payloads now use `"Agent"` as `tool_name`. Jerry's rule files, agent-development-standards, and quality-enforcement references still use the old name. This creates confusion when reading Jerry docs alongside current Anthropic docs, and any hook script matching on `"Task"` silently misses.

**Scope:**
- `.context/rules/agent-development-standards.md` -- H-35, ASCII diagrams, T5 tier description, Pattern 2/3/4 references
- `.context/rules/quality-enforcement.md` -- if any Task tool references exist
- `.context/rules/agent-routing-standards.md` -- if any Task tool references exist
- `.context/rules/skill-standards.md` -- "Task tool code" invocation option
- Any hook scripts matching on tool_name "Task"
- settings.json permission patterns using Task(...)

**NOT in scope:**
- Worktracker entity type "Task" (TASK-001, etc.) -- this is Jerry's entity hierarchy, unrelated to Claude Code's tool rename
- The TaskCreate/TaskUpdate/TaskList/TaskGet/TaskStop tools -- these are Claude Code's task management tools, not the subagent spawning tool

---

## Acceptance Criteria

- [ ] All "Task tool" references in `.context/rules/` updated to "Agent tool" with note that "Task" is a backward-compatible alias
- [ ] H-35 updated: "Worker agents MUST NOT include `Agent` (or its alias `Task`) in `tools`"
- [ ] ASCII diagrams updated: `+-- Worker A (via Agent tool)`
- [ ] T5 description updated: "The Agent tool enables delegation"
- [ ] Hook scripts checked for tool_name matching -- any "Task" matches updated to handle both names
- [ ] settings.json permission patterns audited for Task(...) vs Agent(...)
- [ ] Grep confirms zero remaining "Task tool" references in rule files (excluding worktracker entity type)

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Owner |
|----|-------|--------|-------|
| TASK-001 | Grep and catalog all "Task tool" references in .context/rules/ | pending | -- |
| TASK-002 | Update agent-development-standards.md (H-35, diagrams, T5) | pending | -- |
| TASK-003 | Update skill-standards.md invocation section | pending | -- |
| TASK-004 | Audit hook scripts for tool_name matching | pending | -- |
| TASK-005 | Audit settings.json for Task(...) permission patterns | pending | -- |
| TASK-006 | Verify grep shows zero remaining "Task tool" in rules | pending | -- |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-001: Claude Code Schema Validation](../FEAT-001-claude-code-schema-validation.md)

### Source Findings

| Finding ID | Source | Description |
|-----------|--------|-------------|
| F-009 | GitHub issue scan | Task renamed to Agent in v2.1.63 (#29677) |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-27 | adam.nowak | pending | Story created from GitHub issue scan finding F-009 |
