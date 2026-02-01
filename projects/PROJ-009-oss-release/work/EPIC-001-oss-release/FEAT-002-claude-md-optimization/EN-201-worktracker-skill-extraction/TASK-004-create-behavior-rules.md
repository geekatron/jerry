# TASK-004: Create worktracker-behavior-rules.md

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
-->

---

## Frontmatter

```yaml
id: "TASK-004"
work_type: TASK
title: "Create worktracker-behavior-rules.md"
description: |
  Create the behavior rules file containing WORKTRACKER.md behavior,
  file relationships, and operational guidance for worktracker usage.

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
  - behavior

effort: 1
acceptance_criteria: |
  - WORKTRACKER.md behavior documented
  - File relationship rules documented
  - Traceability requirements documented
  - Acceptance criteria requirements documented
  - Evidence requirements documented
due_date: null

activity: DOCUMENTATION
original_estimate: 1
remaining_work: 1
time_spent: null
```

---

## Content

### Description

Extract the worktracker behavior documentation from CLAUDE.md and create a standalone rules file at `skills/worktracker/rules/worktracker-behavior-rules.md`.

### Content to Extract from CLAUDE.md

**Source location:** CLAUDE.md `<worktracker>` section, "Work tracker (worktracker) Behavior"

1. **WORKTRACKER.md Purpose** (~10 lines)
   - Global manifest tracking
   - Pointer with relationships

2. **Epic Folder Behavior** (~15 lines)
   - Epic folder structure
   - Epic markdown file purpose

3. **Feature Folder Behavior** (~15 lines)
   - Feature folder structure
   - Relationship maintenance

4. **Enabler/Story Behavior** (~15 lines)
   - Task tracking
   - Evidence requirements

5. **General Rules** (~15 lines)
   - Acceptance criteria requirements
   - Verifiable evidence
   - MCP Memory-Keeper usage

**Total:** ~60 lines

### Acceptance Criteria

- [ ] WORKTRACKER.md purpose and behavior documented
- [ ] Epic, Feature, Story, Enabler behaviors documented
- [ ] Relationship maintenance rules documented
- [ ] Traceability requirements documented
- [ ] Verifiable evidence requirements documented
- [ ] MCP Memory-Keeper integration noted

### Target File Structure

```markdown
# Worktracker Behavior Rules

## 1. WORKTRACKER.md Global Manifest

[Description of global manifest purpose and structure]

## 2. Epic Behavior

[Epic folder and file rules]

## 3. Feature Behavior

[Feature folder and file rules]

## 4. Enabler/Story Behavior

[Enabler and Story rules with task tracking]

## 5. Task and Artifact Behavior

[Task files, evidence requirements]

## 6. Relationship Maintenance

[Traceability and relationship rules]

## 7. MCP Memory-Keeper Integration

[Usage guidance for context persistence]
```

### Related Items

- Parent: [EN-201: Worktracker Skill Extraction](./EN-201-worktracker-skill-extraction.md)
- Source: CLAUDE.md "Work tracker (worktracker) Behavior" section
- Target: skills/worktracker/rules/worktracker-behavior-rules.md

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
| Behavior Rules | Documentation | skills/worktracker/rules/worktracker-behavior-rules.md |

### Verification

- [ ] All behavior content extracted from CLAUDE.md
- [ ] File validates markdown syntax
- [ ] Content matches source exactly
- [ ] Reviewed by: -

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-01 | Created | Initial creation |
