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

## Additional Resources

- For folder structure and hierarchy, see [worktracker-folder-structure-and-hierarchy-rules.md](./rules/worktracker-folder-structure-and-hierarchy-rules.md)
- For template usage rules, see [worktracker-template-usage-rules.md](./rules/worktracker-template-usage-rules.md)
- For rules on worktracker entities, see [worktracker-entity-rules.md](./rules/worktracker-entity-rules.md)
- For usage examples, see [examples.md](examples.md)
