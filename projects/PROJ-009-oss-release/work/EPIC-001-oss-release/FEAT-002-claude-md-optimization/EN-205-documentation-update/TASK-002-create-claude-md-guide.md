# TASK-002: Create CLAUDE-MD-GUIDE.md

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
title: "Create CLAUDE-MD-GUIDE.md"
description: |
  Create a contributor guide explaining the CLAUDE.md structure and
  how to find information in the Jerry framework.

classification: ENABLER
status: BACKLOG
resolution: null
priority: MEDIUM
assignee: null
created_by: "Claude"
created_at: "2026-02-01T00:00:00Z"
updated_at: "2026-02-01T00:00:00Z"
parent_id: "EN-205"
tags:
  - enabler
  - documentation
  - guide

effort: 1
acceptance_criteria: |
  - Guide created at docs/CLAUDE-MD-GUIDE.md
  - Structure explained clearly
  - "How to find information" section included
  - Suitable for new contributors
due_date: null

activity: DOCUMENTATION
original_estimate: 1
remaining_work: 1
time_spent: null
```

---

## Content

### Description

Create a dedicated guide for contributors explaining the CLAUDE.md structure, how to navigate the codebase, and how to contribute.

### Target Structure

```markdown
# CLAUDE.md Guide for Contributors

## Overview

Jerry uses a tiered context loading strategy to optimize LLM performance...

## Tiered Architecture

### Tier 1: CLAUDE.md (Always Loaded)
- Identity
- Navigation pointers
- Critical constraints
- Quick reference

### Tier 2: .claude/rules/ (Auto-Loaded)
- Coding standards
- Architecture standards
- Testing standards
- etc.

### Tier 3: Skills (On-Demand)
- /worktracker
- /problem-solving
- /nasa-se
- /orchestration
- /architecture

### Tier 4: Reference Docs (Explicit Access)
- docs/knowledge/
- docs/governance/
- .context/templates/

## How to Find Information

| Question | Location |
|----------|----------|
| How do I code? | .claude/rules/ |
| How do I track work? | /worktracker |
| What are the entity types? | /worktracker |
| etc. | etc. |

## Contributing to Context

When adding new features:
1. Determine appropriate tier
2. Add to correct location
3. Update navigation pointers if needed
```

### Acceptance Criteria

- [ ] Guide created at docs/CLAUDE-MD-GUIDE.md
- [ ] All tiers explained
- [ ] "How to find information" section included
- [ ] Clear and helpful for new contributors

### Related Items

- Parent: [EN-205: Documentation Update](./EN-205-documentation-update.md)
- Target: docs/CLAUDE-MD-GUIDE.md

---

## Time Tracking

| Metric | Value |
|---------|-------|
| Original Estimate | 1 hour |
| Remaining Work | 1 hour |
| Time Spent | 0 hours |

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-01 | Created | Initial creation |
