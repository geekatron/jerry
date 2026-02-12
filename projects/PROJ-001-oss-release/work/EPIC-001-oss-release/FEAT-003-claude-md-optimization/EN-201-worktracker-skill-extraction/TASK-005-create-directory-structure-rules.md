# TASK-005: Create worktracker-directory-structure.md

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
id: "TASK-005"
work_type: TASK
title: "Create worktracker-directory-structure.md"
description: |
  Create the directory structure rules file containing the complete
  worktracker directory hierarchy with naming conventions and examples.

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
  - structure

effort: 1
acceptance_criteria: |
  - Complete directory tree documented
  - All naming conventions documented
  - Example file names provided
  - All entity types included
  - Relationship rules documented
due_date: null

activity: DOCUMENTATION
original_estimate: 1
remaining_work: 1
time_spent: null
```

---

## Content

### Description

Extract the directory structure documentation from CLAUDE.md and create a standalone rules file at `skills/worktracker/rules/worktracker-directory-structure.md`.

### Content to Extract from CLAUDE.md

**Source location:** CLAUDE.md `<worktracker>` section, "Work tracker (worktracker) Directory Structure"

The entire directory tree structure showing:
- Project folder structure
- WORKTRACKER.md location
- work/ folder hierarchy
- Epic folder structure with examples
- Feature folder structure with examples
- Enabler/Story folder structure with examples
- All file naming conventions

**Total:** ~111 lines

### Acceptance Criteria

- [ ] Complete directory tree documented
- [ ] projects/ root structure
- [ ] {ProjectId}/ folder structure
- [ ] work/{EpicId}-{slug}/ structure with examples
- [ ] {FeatureId}-{slug}/ structure with examples
- [ ] {EnablerId}-{slug}/ and {StoryId}-{slug}/ structures
- [ ] All file naming patterns documented
- [ ] Bug, Discovery, Impediment, Decision naming conventions
- [ ] Plans folder structure

### Target File Structure

```markdown
# Worktracker Directory Structure

## Overview

[Brief description of directory organization philosophy]

## Complete Directory Tree

```
projects/
└── {ProjectId}/
    ├── PLAN.md
    ├── WORKTRACKER.md
    └── work/
        └── {EpicId}-{slug}/
            ... [full tree]
```

## Naming Conventions

### Project Level
[Naming rules]

### Epic Level
[Naming rules]

### Feature Level
[Naming rules]

### Enabler/Story Level
[Naming rules]

### Task/Bug/Discovery Level
[Naming rules]
```

### Related Items

- Parent: [EN-201: Worktracker Skill Extraction](./EN-201-worktracker-skill-extraction.md)
- Source: CLAUDE.md "Work tracker (worktracker) Directory Structure" section
- Target: skills/worktracker/rules/worktracker-directory-structure.md

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
| Directory Structure Rules | Documentation | skills/worktracker/rules/worktracker-directory-structure.md |

### Verification

- [ ] All directory structure content extracted from CLAUDE.md
- [ ] File validates markdown syntax
- [ ] Tree diagrams render correctly
- [ ] Content matches source exactly
- [ ] Reviewed by: -

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-01 | Created | Initial creation |
