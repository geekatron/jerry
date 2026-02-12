# TASK-006: Update SKILL.md with Navigation Pointers

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
| [Content](#content) | Description and target structure |
| [Time Tracking](#time-tracking) | Effort metrics |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Change log |

---

## Frontmatter

```yaml
id: "TASK-006"
work_type: TASK
title: "Update SKILL.md with Navigation Pointers"
description: |
  Update the worktracker SKILL.md to include navigation pointers to all
  the newly created rules files, ensuring users can find relevant content.

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
  - navigation

effort: 1
acceptance_criteria: |
  - SKILL.md includes navigation table
  - All rules files referenced
  - Template references included
  - Purpose of each file documented
due_date: null

activity: DOCUMENTATION
original_estimate: 1
remaining_work: 1
time_spent: null
```

---

## Content

### Description

After creating all the rules files, update `skills/worktracker/SKILL.md` to include a navigation section that points to all relevant documentation.

### Dependencies

This task depends on completion of:
- TASK-001: Fix SKILL.md description bug
- TASK-002: Create worktracker-entity-hierarchy.md
- TASK-003: Create worktracker-system-mappings.md
- TASK-004: Create worktracker-behavior-rules.md
- TASK-005: Create worktracker-directory-structure.md

### Acceptance Criteria

- [x] Navigation table added to SKILL.md (NAV-006 compliant with anchor links)
- [x] All rules files listed with descriptions (Additional Resources section)
- [x] Template directory referenced (`.context/templates/worktracker/` in Quick Reference)
- [x] "When to Use" guidance included (When to Use This Skill section)
- [x] Quick reference section for common tasks (Entity containment, template paths, key files)

### Target Structure for SKILL.md

```markdown
# Worktracker Skill

## Purpose
[Updated description from TASK-001]

## Navigation

| Need | Location |
|------|----------|
| Entity types & hierarchy | rules/worktracker-entity-hierarchy.md |
| ADO/SAFe/JIRA mappings | rules/worktracker-system-mappings.md |
| WORKTRACKER.md behavior | rules/worktracker-behavior-rules.md |
| Directory conventions | rules/worktracker-directory-structure.md |
| Templates | .context/templates/worktracker/ |

## When to Use This Skill

Use `/worktracker` when:
- Creating or managing work items (Epics, Features, Stories, Tasks)
- Understanding entity hierarchy and relationships
- Mapping between systems (ADO, SAFe, JIRA)
- Creating project structures

## Quick Reference

[Common commands/patterns]
```

### Related Items

- Parent: [EN-201: Worktracker Skill Extraction](./EN-201-worktracker-skill-extraction.md)
- Target: skills/worktracker/SKILL.md

---

## Time Tracking

| Metric | Value |
|---------|-------|
| Original Estimate | 1 hour |
| Remaining Work | 0 hours |
| Time Spent | 1 hour |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Updated SKILL.md | Documentation | skills/worktracker/SKILL.md |

### Verification

- [x] Navigation table complete (5 sections with anchor links per NAV-006)
- [x] All links resolve correctly (entity-hierarchy, system-mappings, directory-structure, templates)
- [x] Reviewed by: Claude

### Evidence of Completion

| Change | Evidence |
|--------|----------|
| SKILL.md updated | 116 lines (was 67, +50 insertions) |
| Document Sections table | Lines 26-35 with anchor links |
| Quick Reference section | Lines 70-104 (entity containment, templates, key files) |
| Template directory path | `.context/templates/worktracker/` explicitly listed |
| Verification method | `wc -l` and `git diff --stat` |

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-01 | Created | Initial creation |
| 2026-02-01 | IN_PROGRESS | Started work on SKILL.md navigation |
| 2026-02-01 | DONE | Added NAV-006 compliant Document Sections table, Quick Reference section (entity containment, templates, key files), explicit template directory path |
