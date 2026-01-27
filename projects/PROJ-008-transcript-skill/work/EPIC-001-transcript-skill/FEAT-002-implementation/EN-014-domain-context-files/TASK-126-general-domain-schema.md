# TASK-126: Create general.yaml Baseline Domain Schema

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-014 (Domain Context Files Implementation)
-->

---

## Frontmatter

```yaml
id: "TASK-126"
work_type: TASK
title: "Create general.yaml Baseline Domain Schema"
description: |
  Create the general.yaml baseline domain schema file for fallback
  entity extraction when no specific domain is specified.

classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-26T19:30:00Z"
updated_at: "2026-01-26T19:30:00Z"

parent_id: "EN-014"

tags:
  - "implementation"
  - "domain-context"
  - "general-domain"
  - "REQ-CI-F-001"

effort: 1
acceptance_criteria: |
  - general.yaml created in contexts/ folder
  - Schema version and domain metadata present
  - Minimal entity definitions (statement, reference)
  - Low confidence thresholds for broad coverage
  - Generic prompt_guidance

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

Create the baseline domain schema (`general.yaml`) that provides fallback entity extraction when no specific domain is specified. This schema has minimal, generic entities applicable to any text type with low confidence thresholds for broad coverage.

### File Location

```
skills/transcript/contexts/general.yaml
```

### Schema Content

```yaml
# contexts/general.yaml
# Baseline domain schema for general transcript analysis
# Implements: REQ-CI-F-001

schema_version: "1.0.0"
domain: "general"
display_name: "General Transcript Analysis"

entity_definitions:
  statement:
    description: "General statement or assertion"
    attributes:
      - name: "text"
        type: "string"
        required: true
      - name: "speaker"
        type: "string"
      - name: "timestamp_ms"
        type: "integer"

  reference:
    description: "Reference to external entity (person, document, etc.)"
    attributes:
      - name: "text"
        type: "string"
        required: true
      - name: "reference_type"
        type: "enum"
        values: ["person", "document", "organization", "other"]

extraction_rules:
  - id: "statements"
    entity_type: "statement"
    confidence_threshold: 0.5
    priority: 1
  - id: "references"
    entity_type: "reference"
    confidence_threshold: 0.6
    priority: 2

prompt_guidance: |
  When analyzing general transcripts:

  1. Extract significant statements that convey information
  2. Identify references to external entities
  3. Use low confidence thresholds - this is the baseline

  This is the fallback domain when no specific domain matches.
```

### Design Rationale

| Decision | Rationale |
|----------|-----------|
| Minimal entities | Avoid over-extraction in unknown domains |
| Low thresholds | Broad coverage as baseline |
| Generic patterns | No domain assumptions |
| No inheritance | Base domain, doesn't extend anything |

### Acceptance Criteria

- [ ] File created at `skills/transcript/contexts/general.yaml`
- [ ] `schema_version: "1.0.0"` present
- [ ] `domain: "general"` set
- [ ] `display_name: "General Transcript Analysis"` set
- [ ] Entity definitions for `statement` and `reference`
- [ ] `extraction_rules` with low confidence thresholds
- [ ] `prompt_guidance` with generic advice
- [ ] YAML syntax valid
- [ ] Passes JSON Schema validation (TASK-129)

### Related Items

- Parent: [EN-014: Domain Context Files Implementation](./EN-014-domain-context-files.md)
- Blocked By: EN-013 (context injection mechanism)
- Blocks: [TASK-127: transcript.yaml](./TASK-127-transcript-domain-schema.md), [TASK-129: JSON Schema](./TASK-129-domain-json-schema.md)
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
- [ ] JSON Schema validation passes
- [ ] Reviewed by: (pending)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-26 | Created | Initial task creation per EN-014 |
