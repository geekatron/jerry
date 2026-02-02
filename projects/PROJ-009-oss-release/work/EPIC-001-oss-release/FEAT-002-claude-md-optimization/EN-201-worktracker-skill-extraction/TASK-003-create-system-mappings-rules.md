# TASK-003: Create worktracker-system-mappings.md

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
-->

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Frontmatter](#frontmatter) | Task metadata |
| [Content](#content) | Description and target file structure |
| [Time Tracking](#time-tracking) | Effort metrics |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Change log |

---

## Frontmatter

```yaml
id: "TASK-003"
work_type: TASK
title: "Create worktracker-system-mappings.md"
description: |
  Create the system mappings rules file containing ADO Scrum, SAFe, and JIRA
  entity mappings for the canonical worktracker model.

classification: ENABLER
status: DONE
resolution: COMPLETED
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
  - mappings

effort: 2
acceptance_criteria: |
  - Entity mapping summary table included
  - Mapping complexity table included
  - Complete entity mapping by system
  - ADO Scrum entity types documented
  - SAFe entity types documented
  - JIRA entity types documented
due_date: null

activity: DOCUMENTATION
original_estimate: 2
remaining_work: 2
time_spent: null
```

---

## Content

### Description

Extract the system mappings documentation from CLAUDE.md and create a standalone rules file at `skills/worktracker/rules/worktracker-system-mappings.md`.

### Content to Extract from CLAUDE.md

**Source location:** CLAUDE.md `<worktracker>` section, System Mapping Summary

1. **Section 3.1: Entity Mapping Table** (~20 lines)
   - Canonical to ADO/SAFe/JIRA mappings

2. **Section 3.2: Mapping Complexity** (~10 lines)
   - Direction and complexity ratings

3. **Section 4.1: Complete Entity Mapping** (~25 lines)
   - Full mapping table with notes

4. **Section 4.1.1-4.1.3: Entity Mapping by System** (~60 lines)
   - ADO Scrum Entity Types
   - SAFe Entity Types
   - JIRA Entity Types

**Total:** ~120 lines

### Acceptance Criteria

- [ ] Entity mapping summary table (Canonical, ADO Scrum, SAFe, JIRA)
- [ ] Mapping complexity table (Direction, Complexity, Notes)
- [ ] Complete entity mapping table with Native column and Notes
- [ ] ADO Scrum entity types with canonical mapping
- [ ] SAFe entity types with canonical mapping
- [ ] JIRA entity types with canonical mapping

### Target File Structure

```markdown
# Worktracker System Mappings

## 1. Entity Mapping Summary

[Table: Canonical, ADO Scrum, SAFe, JIRA]

## 2. Mapping Complexity

[Table: Direction, Complexity, Notes]

## 3. Complete Entity Mapping

[Table: Canonical Entity, ADO Scrum, SAFe, JIRA, Native, Notes]

## 4. Entity Mapping by System

### 4.1 ADO Scrum Entity Types
[Table: ADO Type, Canonical Mapping, Notes]

### 4.2 SAFe Entity Types
[Table: SAFe Type, Canonical Mapping, Notes]

### 4.3 JIRA Entity Types
[Table: JIRA Type, Canonical Mapping, Notes]
```

### Related Items

- Parent: [EN-201: Worktracker Skill Extraction](./EN-201-worktracker-skill-extraction.md)
- Source: CLAUDE.md Section 3-4 in `<worktracker>` block
- Target: skills/worktracker/rules/worktracker-system-mappings.md

---

## Time Tracking

| Metric | Value |
|---------|-------|
| Original Estimate | 2 hours |
| Remaining Work | 2 hours |
| Time Spent | 0 hours |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| System Mappings Rules | Documentation | skills/worktracker/rules/worktracker-system-mappings.md |

### Verification

- [ ] All mapping content extracted from CLAUDE.md
- [ ] File validates markdown syntax
- [ ] Tables properly formatted
- [ ] Content matches source exactly
- [ ] Reviewed by: -

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-01 | Created | Initial creation |
