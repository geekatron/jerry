# STORY-003: Gap Analysis and Schema Refinement

<!--
TEMPLATE: Story
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
PURPOSE: Compare research findings against existing schemas, produce refined versions
-->

> **Type:** story
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Created:** 2026-03-26T22:10:00Z
> **Due:**
> **Completed:** 2026-03-26T23:30:00Z
> **Parent:** FEAT-001
> **Owner:** adam.nowak
> **Effort:** 8

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [User Story](#user-story) | As a / I want / So that |
| [Summary](#summary) | Analysis scope and approach |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Children (Tasks)](#children-tasks) | Task breakdown |
| [Progress Summary](#progress-summary) | Overall progress |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Status changes |

---

## User Story

**As a** Jerry framework developer

**I want** a systematic gap analysis between our existing schemas and Anthropic's official specification, with refined schemas as output

**So that** our schema files are accurate, complete, and suitable for CI validation of all agent and skill definitions

---

## Summary

Take the research outputs from STORY-001 (agent schema) and STORY-002 (skill schema), compare them against the existing Jerry schemas, identify all gaps (missing fields, wrong types, incorrect constraints, missing enums), and produce refined schema files.

**Scope:**
- Field-by-field comparison: existing vs. researched
- Gap categorization: missing, incorrect type, wrong constraint, deprecated
- Refined `claude-code-frontmatter-v2.schema.json` (agent)
- Refined `claude-code-skill-frontmatter-v2.schema.json` (skill)
- Validation of all existing agent/skill definitions against refined schemas

---

## Acceptance Criteria

- [ ] Gap analysis document produced with field-by-field comparison
- [ ] Each gap categorized (missing, incorrect type, wrong constraint, deprecated, undocumented)
- [ ] Refined agent frontmatter schema produced and validated
- [ ] Refined skill frontmatter schema produced and validated
- [ ] All existing agent definitions (50+) validate against refined agent schema
- [ ] All existing SKILL.md files (15+) validate against refined skill schema
- [ ] Zero false positives (no valid definition rejected by refined schema)

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Owner |
|----|-------|--------|-------|
| TASK-001 | Produce gap analysis document | pending | ps-analyst |
| TASK-002 | Create refined agent frontmatter schema v2 | pending | -- |
| TASK-003 | Create refined skill frontmatter schema v2 | pending | -- |
| TASK-004 | Validate all existing definitions against refined schemas | pending | -- |
| TASK-005 | C4 adversarial review of refined schemas | pending | adv-executor |

---

## Progress Summary

```
+------------------------------------------------------------------+
|                    STORY PROGRESS TRACKER                         |
+------------------------------------------------------------------+
| Tasks:     [....................] 0% (0/5 completed)              |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                               |
+------------------------------------------------------------------+
```

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-001: Claude Code Schema Validation](../FEAT-001-claude-code-schema-validation.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | STORY-001 | Agent schema research must complete first |
| Depends On | STORY-002 | Skill schema research must complete first |
| Blocks | EN-001 | Security review needs refined schemas |
| Blocks | EN-002 | DX review needs refined schemas |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-26 | adam.nowak | pending | Story created; blocked on STORY-001 and STORY-002 research |
