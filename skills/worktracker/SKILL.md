---
name: worktracker
description: Work item tracking and task management using the Jerry Framework hierarchy (Initiative, Epic, Feature, Story, Task, Enabler, Bug, Impediment). Manages WORKTRACKER.md manifests, tracks progress, and enforces template usage for consistent work decomposition.
version: "1.1.0"
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

> **Version:** 1.1.0
> **Framework:** Jerry Worktracking Framework v1.0
> **Constitutional Compliance:** Jerry Constitution v1.0 (P-002, P-003, P-020)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | What this skill does and core capabilities |
| [When to Use This Skill](#when-to-use-this-skill) | Activation triggers and use cases |
| [Core Rules (Always Loaded)](#core-rules-always-loaded) | Behavior rules loaded via `@` import |
| [Worktracker Agents](#worktracker-agents) | Specialized agents for verification, visualization, auditing |
| [Quick Reference](#quick-reference) | Entity hierarchy, templates, key locations |
| [Additional Resources](#additional-resources) | Links to detailed rule files |

---

## Overview

The Worktracker skill provides comprehensive work item tracking and task management capabilities within the Jerry Framework. It implements a hierarchical work decomposition structure compatible with ADO Scrum, SAFe, and JIRA methodologies.

### Core Capabilities

- **Work Item Hierarchy**: Initiative → Epic → Feature → Story/Enabler → Task → Subtask
- **Progress Tracking**: Status management, effort tracking, completion metrics
- **Template Enforcement**: Consistent work item creation using standardized templates
- **Content Quality**: AC clarity, brevity limits, anti-pattern detection (WTI-008, WTI-009)
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
@rules/worktracker-templates.md
@rules/worktracker-content-standards.md

---

## Worktracker Agents

The worktracker skill includes specialized agents for advanced operations. These agents follow the **worker pattern** and are invoked by MAIN CONTEXT (Claude) via the Task tool, maintaining P-003 compliance.

### Available Agents

| Agent | Model | Purpose | Invocation Example |
|-------|-------|---------|-------------------|
| `wt-verifier` | sonnet | Validate acceptance criteria before closure | "Verify EN-001 is ready for closure" |
| `wt-visualizer` | haiku | Generate Mermaid diagrams for hierarchies | "Create a hierarchy diagram for FEAT-002" |
| `wt-auditor` | sonnet | Audit cross-file integrity and templates | "Audit the worktracker for PROJ-009" |

### Agent Selection Guide

| User Intent | Keywords | Agent |
|-------------|----------|-------|
| Verify completion readiness | "verify", "check ready", "validate AC" | wt-verifier |
| Generate visual diagrams | "diagram", "visualize", "show hierarchy" | wt-visualizer |
| Check integrity/compliance | "audit", "check integrity", "find orphans" | wt-auditor |
| Full status report | "status of", "progress on" | wt-verifier + wt-visualizer |

### Agent Files

| Agent | Location |
|-------|----------|
| wt-verifier | `skills/worktracker/agents/wt-verifier.md` |
| wt-visualizer | `skills/worktracker/agents/wt-visualizer.md` |
| wt-auditor | `skills/worktracker/agents/wt-auditor.md` |

### P-003 Compliance (Critical)

**Agents are workers, NOT orchestrators:**
- Agents are invoked via `Task` tool from MAIN CONTEXT
- Agents **DO NOT** spawn subagents
- Agents return results to MAIN CONTEXT for presentation to user

```
User Request --> MAIN CONTEXT --> Task(wt-verifier) --> Report --> User
                     |
                     +-- Agents never invoke other agents (P-003)
```

### WTI Rules Enforced

Agents enforce Worktracker Integrity (WTI) rules defined in `.context/templates/worktracker/WTI_RULES.md`:

| Rule | Description | Enforcing Agent |
|------|-------------|-----------------|
| WTI-001 | Real-Time State | wt-auditor |
| WTI-002 | No Closure Without Verification | wt-verifier |
| WTI-003 | Truthful State | wt-verifier, wt-auditor |
| WTI-004 | Synchronize Before Reporting | wt-auditor |
| WTI-005 | Atomic State Updates | wt-auditor |
| WTI-006 | Evidence-Based Closure | wt-verifier |
| WTI-008 | Content Quality Standards | wt-auditor |
| WTI-009 | Collaboration Before Creation | (interactive -- MAIN CONTEXT) |

### Output Templates

Agent outputs use standardized templates:

| Template | Purpose | Location |
|----------|---------|----------|
| VERIFICATION_REPORT.md | wt-verifier output | `.context/templates/worktracker/` |
| AUDIT_REPORT.md | wt-auditor output | `.context/templates/worktracker/` |

### When to Use Agents vs Rules

| Scenario | Recommendation |
|----------|----------------|
| Simple work item creation | Use rules only |
| Pre-closure verification | Use wt-verifier |
| Understanding work structure | Use wt-visualizer |
| Finding integrity issues | Use wt-auditor |
| Full project health check | Use all three agents |

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
- **TODO Integration**: [todo-integration-rules.md](./rules/todo-integration-rules.md) - META TODO items, TODO↔Worktracker sync rules

> **Rule Loading Tiers:** Auto-loaded rules (behavior-rules, templates) are loaded via `@` import because they contain enforcement rules needed for every worktracker operation. Reference rules (entity-hierarchy, system-mappings, directory-structure, todo-integration) are loaded on-demand to conserve context budget.
