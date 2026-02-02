---
name: worktracker
description: Work item tracking and task management using the Jerry Framework hierarchy (Initiative, Epic, Feature, Story, Task, Enabler, Bug, Impediment). Manages WORKTRACKER.md manifests, tracks progress, and enforces template usage for consistent work decomposition.
version: "1.0.0"
allowed-tools: Read, Write, Glob, Task, Edit
activation-keywords:
  - "work tracker"
  - "worktracker"
  - "work-tracker"
  - "update the work tracker"
  - "update the work-tracker"
  - "update the worktracker"
  - "/worktracker"
  - "/jerry:worktracker"

---

# Worktracker Skill

> **Version:** 1.0.0
> **Framework:** Jerry Worktracking Framework v1.0
> **Constitutional Compliance:** Jerry Constitution v1.0 (P-002, P-003, P-020)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | What this skill does and core capabilities |
| [When to Use This Skill](#when-to-use-this-skill) | Activation triggers and use cases |
| [Core Rules (Always Loaded)](#core-rules-always-loaded) | Behavior rules loaded via `@` import |
| [Quick Reference](#quick-reference) | Entity hierarchy, templates, key locations |
| [Additional Resources](#additional-resources) | Links to detailed rule files |

---

## Overview

The Worktracker skill provides comprehensive work item tracking and task management capabilities within the Jerry Framework. It implements a hierarchical work decomposition structure compatible with ADO Scrum, SAFe, and JIRA methodologies.

### Core Capabilities

- **Work Item Hierarchy**: Initiative → Epic → Feature → Story/Enabler → Task → Subtask
- **Progress Tracking**: Status management, effort tracking, completion metrics
- **Template Enforcement**: Consistent work item creation using standardized templates
- **Manifest Management**: WORKTRACKER.md files as single source of truth
- **System Mappings**: Compatible with ADO Scrum, SAFe, and JIRA workflows

### When to Use This Skill

Invoke `/worktracker` when you need to:
- Create, update, or track work items
- Understand the entity hierarchy and relationships
- Follow proper template usage for work items
- Navigate the project directory structure
- Map between Jerry entities and external systems (ADO, SAFe, JIRA)

---

## Core Rules (Always Loaded)

The following rules are automatically loaded when this skill is invoked:

@rules/worktracker-behavior-rules.md

---

## Quick Reference

### Entity Containment (What Can Contain What)

| Parent | Allowed Children |
|--------|------------------|
| Initiative | Epic |
| Epic | Capability, Feature |
| Feature | Story, Enabler |
| Story | Task, Subtask |
| Enabler | Task |
| Task | Subtask |
| Bug | Task |

### Template Locations

| Template | Path |
|----------|------|
| All worktracker templates | `.context/templates/worktracker/` |
| Epic | `.context/templates/worktracker/EPIC.md` |
| Feature | `.context/templates/worktracker/FEATURE.md` |
| Enabler | `.context/templates/worktracker/ENABLER.md` |
| Story | `.context/templates/worktracker/STORY.md` |
| Task | `.context/templates/worktracker/TASK.md` |
| Bug | `.context/templates/worktracker/BUG.md` |
| Discovery | `.context/templates/worktracker/DISCOVERY.md` |
| Decision | `.context/templates/worktracker/DECISION.md` |

### Key File Locations

| File | Purpose |
|------|---------|
| `projects/{ProjectId}/WORKTRACKER.md` | Global manifest for project |
| `projects/{ProjectId}/work/` | Work decomposition folder |
| `.context/templates/worktracker/` | All worktracker templates |

---

## Additional Resources

### Rule Files

For detailed reference, the following rule files are available:

- **Entity Hierarchy**: [worktracker-entity-hierarchy.md](./rules/worktracker-entity-hierarchy.md) - Work item types, classification matrix, and containment rules
- **System Mappings**: [worktracker-system-mappings.md](./rules/worktracker-system-mappings.md) - ADO Scrum, SAFe, and JIRA mappings
- **Directory Structure**: [worktracker-directory-structure.md](./rules/worktracker-directory-structure.md) - Complete folder hierarchy with examples
- **Templates**: [worktracker-templates.md](./rules/worktracker-templates.md) - Template locations and usage rules
