# TASK-002: Create worktracker-entity-hierarchy.md

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
-->

---

## Frontmatter

```yaml
id: "TASK-002"
work_type: TASK
title: "Create worktracker-entity-hierarchy.md"
description: |
  Create the entity hierarchy rules file containing the complete WorkItem hierarchy,
  entity classification matrix, and hierarchy levels documentation.

classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: null
created_by: "Claude"
created_at: "2026-02-01T00:00:00Z"
updated_at: "2026-02-01T00:00:00Z"
parent_id: "EN-201"
tags:
  - enabler
  - extraction
  - worktracker

effort: 1
acceptance_criteria: |
  - Complete hierarchy tree documented
  - Entity classification matrix included
  - Hierarchy levels table included
  - Containment rules matrix included
due_date: null

activity: DOCUMENTATION
original_estimate: 1
remaining_work: 1
time_spent: null
```

---

## Content

### Description

Extract the entity hierarchy documentation from CLAUDE.md and create a standalone rules file at `skills/worktracker/rules/worktracker-entity-hierarchy.md`.

### Content to Extract from CLAUDE.md

**Source location:** CLAUDE.md `<worktracker>` section

1. **Section 1: Entity Hierarchy**
   - Complete Hierarchy Tree (~30 lines)
   - Hierarchy Levels table (~15 lines)

2. **Section 2: Entity Classification and Properties**
   - Classification Matrix (~15 lines)
   - Containment Rules Matrix (~15 lines)

**Total:** ~80 lines

### Acceptance Criteria

- [ ] Complete hierarchy tree with all entity types
- [ ] WorkItem abstract class documented
- [ ] StrategicItem, DeliveryItem, QualityItem, FlowControlItem abstracts documented
- [ ] Hierarchy levels (L0-L5) documented with owners
- [ ] Classification matrix with Container/Atomic/Quality Gates columns
- [ ] Containment rules showing allowed children per parent

### Target File Structure

```markdown
# Worktracker Entity Hierarchy

## 1. Complete Hierarchy Tree
[Tree diagram from CLAUDE.md]

## 2. Hierarchy Levels
[Table: Level, Category, Entities, Planning Horizon, Typical Owner]

## 3. Entity Classification Matrix
[Table: Entity, Category, Level, Container, Atomic, Quality Gates, Optional]

## 4. Containment Rules Matrix
[Table: Parent Type, Allowed Children]
```

### Related Items

- Parent: [EN-201: Worktracker Skill Extraction](./EN-201-worktracker-skill-extraction.md)
- Source: CLAUDE.md lines ~50-130
- Target: skills/worktracker/rules/worktracker-entity-hierarchy.md

---

## Time Tracking

| Metric | Value |
|---------|-------|
| Original Estimate | 1 hour |
| Remaining Work | 1 hour |
| Time Spent | 0 hours |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Entity Hierarchy Rules | Documentation | skills/worktracker/rules/worktracker-entity-hierarchy.md |

### Verification

- [ ] All hierarchy content extracted from CLAUDE.md
- [ ] File validates markdown syntax
- [ ] Content matches source exactly
- [ ] Reviewed by: -

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-01 | Created | Initial creation |
