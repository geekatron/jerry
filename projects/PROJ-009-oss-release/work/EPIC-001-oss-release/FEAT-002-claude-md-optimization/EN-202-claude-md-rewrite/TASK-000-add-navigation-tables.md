# TASK-000: Add Navigation Tables to Worktracker Files

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
CREATED: 2026-02-01 (Claude)
PURPOSE: Apply FEAT-002:DEC-001 navigation table standard to all worktracker files
-->

> **Type:** task
> **Status:** complete
> **Priority:** high
> **Created:** 2026-02-01T18:00:00Z
> **Due:** -
> **Completed:** 2026-02-02T02:00:00Z
> **Parent:** EN-202
> **Owner:** ps-writer
> **Effort:** 2

---

## Document Sections

| Section | Purpose | Key Information |
|---------|---------|-----------------|
| **Summary** | What this task does | Navigation table updates |
| **Scope** | Which files to update | Worktracker rules, templates |
| **Implementation** | How to implement | Table format, placement |
| **Acceptance Criteria** | Definition of done | Checklist |
| **Related Items** | References | FEAT-002 decisions |

---

## Summary

Apply the navigation table standard established in [FEAT-002:DEC-001](../FEAT-002--DEC-001-navigation-table-standard.md) to all worktracker-related files. This task MUST complete before other EN-202 tasks because navigation tables improve Claude's comprehension of the files being rewritten.

**Why First?** The navigation table standard was discovered during EN-201. Applying it before the CLAUDE.md rewrite ensures all referenced files have proper structure for Claude to work with.

---

## Scope

### Files to Update

| Category | Location | Count | Format |
|----------|----------|-------|--------|
| Worktracker rules | `skills/worktracker/rules/*.md` | 5 | Section Index |
| Worktracker templates | `.context/templates/worktracker/*.md` | 10 | Section Index |
| Claude rules | `.claude/rules/*.md` | ~8 | Section Index (already partially done) |

### Already Compliant (Skip)

| Category | Location | Notes |
|----------|----------|-------|
| Skill files | `skills/*/SKILL.md` | Already have Triple-Lens tables |
| Playbooks | `skills/*/PLAYBOOK.md` | Already have Triple-Lens tables |

---

## Implementation

### Navigation Table Format

For worktracker rules and templates, use the **Section Index** format:

```markdown
## Document Sections

| Section | Purpose | Key Information |
|---------|---------|-----------------|
| **Section Name** | What it covers | Summary of content |
| **Another Section** | What it covers | Summary of content |
```

### Placement Rules

1. **After** YAML frontmatter (if present)
2. **After** title and metadata blockquote
3. **Before** first content section (e.g., ## Summary)

### Example (from markdown-navigation-standards.md)

```markdown
---
name: example
description: ...
---

# Document Title

> **Version:** 1.0.0

---

## Document Sections        <-- Navigation table goes HERE

| Section | Purpose |
|---------|---------|
| ... | ... |

---

## First Content Section    <-- Content starts AFTER
```

---

## Acceptance Criteria

### Definition of Done

- [x] All worktracker rules have navigation tables
- [x] All worktracker templates have navigation table section
- [x] All Claude rules have navigation tables (verify/add)
- [x] Each navigation table appears after frontmatter, before content
- [x] Tables use proper markdown table syntax

### Files Checklist

#### Worktracker Rules (`skills/worktracker/rules/`)

- [x] `worktracker-entity-hierarchy.md`
- [x] `worktracker-system-mappings.md`
- [x] `worktracker-behavior-rules.md` (already had navigation)
- [x] `worktracker-directory-structure.md`
- [x] `worktracker-templates.md`

#### Worktracker Templates (`.context/templates/worktracker/`)

- [x] `BUG.md`
- [x] `DECISION.md`
- [x] `DISCOVERY.md`
- [x] `ENABLER.md`
- [x] `EPIC.md`
- [x] `FEATURE.md`
- [x] `IMPEDIMENT.md`
- [x] `SPIKE.md`
- [x] `STORY.md`
- [x] `TASK.md`

---

## Related Items

### Hierarchy

- **Parent:** [EN-202: CLAUDE.md Rewrite](./EN-202-claude-md-rewrite.md)
- **Grandparent:** [FEAT-002: CLAUDE.md Optimization](../FEAT-002-claude-md-optimization.md)

### Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Decision | [FEAT-002:DEC-001](../FEAT-002--DEC-001-navigation-table-standard.md) | Navigation table standard decision |
| Discovery | [FEAT-002:DISC-001](../FEAT-002--DISC-001-navigation-tables-for-llm-comprehension.md) | Research findings |
| Rule | `.claude/rules/markdown-navigation-standards.md` | Enforcement rule |

---

## Evidence

### Deliverables

| Deliverable | Type | Description | Link |
|-------------|------|-------------|------|
| Updated rules | Documentation | Worktracker rules with navigation tables | skills/worktracker/rules/*.md |
| Updated templates | Documentation | Templates with navigation table section | .context/templates/worktracker/*.md |

### Verification

| Criterion | Verification Method | Evidence | Verified By | Date |
|-----------|---------------------|----------|-------------|------|
| Tables present | Manual review | - | - | - |
| Placement correct | Manual review | - | - | - |
| Format compliant | Markdown lint | - | - | - |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-01T18:00:00Z | Claude | pending | Task created per FEAT-002:DEC-001 |

---

## Metadata

```yaml
id: "TASK-000"
parent_id: "EN-202"
work_type: TASK
title: "Add Navigation Tables to Worktracker Files"
status: pending
priority: HIGH
created_by: "Claude"
created_at: "2026-02-01T18:00:00Z"
updated_at: "2026-02-01T18:00:00Z"
effort: 2
activity: DOCUMENTATION
tags: [navigation-table, documentation, llm-optimization]
```
