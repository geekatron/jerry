# TASK-121: Create general.yaml Domain Schema

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-013 (Context Injection Implementation)
-->

---

## Frontmatter

```yaml
id: "TASK-121"
work_type: TASK
title: "Create general.yaml Domain Schema"
description: |
  Create the general.yaml domain schema file for the default domain
  with minimal/generic entity definitions per REQ-CI-F-001.

classification: ENABLER
status: BACKLOG
resolution: null
priority: MEDIUM
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-26T19:00:00Z"
updated_at: "2026-01-26T19:00:00Z"

parent_id: "EN-013"

tags:
  - "implementation"
  - "context-injection"
  - "domain-schema"
  - "REQ-CI-F-001"

effort: 1
acceptance_criteria: |
  - general.yaml created in contexts/ folder
  - Schema version and domain metadata present
  - Minimal entity_definitions for general use
  - prompt_guidance with general extraction advice
  - Validates against JSON Schema

due_date: null

activity: DEVELOPMENT
original_estimate: 2
remaining_work: 2
time_spent: 0
```

---

## State Machine

**Current State:** `BACKLOG`

---

## Content

### Description

Create the default domain schema file (`general.yaml`) that serves as the fallback when no specific domain is requested. This file contains minimal, generic entity definitions applicable to any text type.

### File Location

```
skills/transcript/contexts/general.yaml
```

### Schema Structure

```yaml
# Domain Schema for General Text Analysis
# Implements: REQ-CI-F-001
schema_version: "1.0.0"
domain: "general"
display_name: "General Text Analysis"

# Generic entity definitions (broad applicability)
entity_definitions:
  mention:
    description: "Named entity mentioned in text"
    attributes:
      - name: "text"
        type: "string"
        required: true
      - name: "entity_type"
        type: "string"
        enum: ["person", "organization", "location", "date", "other"]
      - name: "confidence"
        type: "float"

  topic:
    description: "Topic or subject discussed"
    attributes:
      - name: "name"
        type: "string"
        required: true
      - name: "keywords"
        type: "array"
      - name: "confidence"
        type: "float"

# Generic extraction rules
extraction_rules:
  - id: "mentions"
    entity_type: "mention"
    confidence_threshold: 0.6
    priority: 1
  - id: "topics"
    entity_type: "topic"
    confidence_threshold: 0.5
    priority: 2

# General guidance (domain-agnostic)
prompt_guidance: |
  When analyzing general text:

  1. **Named Entities**: Identify people, organizations, locations, and dates.
     Use standard NER patterns without domain-specific assumptions.

  2. **Topics**: Extract main topics being discussed.
     Look for recurring themes and subject matter.

  3. **Confidence Scoring**:
     - 0.8+ : Clear, unambiguous reference
     - 0.6-0.8: Probable entity with context support
     - 0.5-0.6: Possible entity, flag for review
     - <0.5: Do not extract

  This is a general domain - avoid domain-specific assumptions.
```

### Acceptance Criteria

- [ ] `contexts/general.yaml` file created
- [ ] `schema_version: "1.0.0"` present
- [ ] `domain: "general"` set
- [ ] At least 2 generic entity_definitions (mention, topic)
- [ ] extraction_rules with confidence thresholds
- [ ] prompt_guidance with general advice
- [ ] Validates against JSON Schema (TASK-124)
- [ ] YAML syntax valid

### Related Items

- Parent: [EN-013: Context Injection Implementation](./EN-013-context-injection.md)
- Blocked By: [TASK-120: SKILL.md context_injection section](./TASK-120-skill-context-injection.md)
- Blocks: [TASK-123: AGENT.md context sections](./TASK-123-agent-context-sections.md)
- References: [SPEC-context-injection.md Section 3.3](../../FEAT-001-analysis-design/EN-006-context-injection-design/docs/specs/SPEC-context-injection.md)
- References: REQ-CI-F-001 (Static Context Loading)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| general.yaml | Implementation | skills/transcript/contexts/general.yaml |
| Schema validation result | Evidence | (in this file) |

### Verification

- [ ] File created at correct location
- [ ] YAML syntax validates
- [ ] Schema structure complete
- [ ] Reviewed by: (pending)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-26 | Created | Initial task creation per EN-013 |
