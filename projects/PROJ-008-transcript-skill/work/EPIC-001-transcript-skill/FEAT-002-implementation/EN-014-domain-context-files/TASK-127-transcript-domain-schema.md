# TASK-127: Create transcript.yaml Core Domain Schema

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-014 (Domain Context Files Implementation)
-->

---

## Frontmatter

```yaml
id: "TASK-127"
work_type: TASK
title: "Create transcript.yaml Core Domain Schema"
description: |
  Create the transcript.yaml core domain schema with all primary
  transcript entities: action_item, decision, question, speaker, topic.

classification: ENABLER
status: DONE
resolution: FIXED
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-26T19:30:00Z"
updated_at: "2026-01-28T22:30:00Z"
completed_at: "2026-01-28T11:15:00Z"

parent_id: "EN-014"

tags:
  - "implementation"
  - "domain-context"
  - "transcript-domain"
  - "REQ-CI-F-001"
  - "REQ-CI-F-007"

effort: 2
acceptance_criteria: |
  - transcript.yaml created with all core entities
  - Entity definitions: action_item, decision, question, speaker, topic
  - Extraction patterns for each entity
  - Confidence thresholds aligned with NFR-008
  - Comprehensive prompt_guidance with FR references

due_date: null

activity: DEVELOPMENT
original_estimate: 4
remaining_work: 4
time_spent: 0
```

---

## State Machine

**Current State:** `BACKLOG`

---

## Content

### Description

Create the core transcript domain schema (`transcript.yaml`) containing all primary entities for transcript analysis. This is the primary domain schema that other specialized domains (meeting, interview) extend.

### File Location

```
skills/transcript/contexts/transcript.yaml
```

### Entity Definitions

| Entity | Requirement | Description | Attributes |
|--------|-------------|-------------|------------|
| action_item | FR-006 | Task or commitment | text, assignee, due_date, confidence |
| decision | FR-007 | Decision made | text, decided_by, rationale |
| question | FR-008 | Question raised | text, asked_by, answered |
| speaker | FR-005 | Person speaking | name, role, segment_count, speaking_time_ms |
| topic | FR-009 | Topic segment | title, start_ms, end_ms, segment_ids |

### Extraction Rules

| Rule ID | Entity Type | Confidence | Priority | Tier (PAT-001) |
|---------|-------------|------------|----------|----------------|
| action_items | action_item | 0.7 | 1 | rule |
| decisions | decision | 0.8 | 2 | rule |
| questions | question | 0.75 | 3 | ml |
| speakers | speaker | 0.9 | 4 | rule |
| topics | topic | 0.7 | 5 | llm |

### Extraction Patterns

```yaml
action_item:
  - "{{assignee}} will {{text}}"
  - "{{assignee}}, can you {{text}}"
  - "action item: {{text}}"
  - "TODO: {{text}}"

decision:
  - "we've decided to {{text}}"
  - "the decision is {{text}}"
  - "let's go with {{text}}"
  - "agreed: {{text}}"
```

### Acceptance Criteria

- [ ] File created at `skills/transcript/contexts/transcript.yaml`
- [ ] `schema_version: "1.0.0"` present
- [ ] `domain: "transcript"` set
- [ ] All 5 core entities defined (action_item, decision, question, speaker, topic)
- [ ] Each entity has required attributes
- [ ] `extraction_patterns` for action_item and decision
- [ ] `extraction_rules` with PAT-001 tier assignments
- [ ] Confidence thresholds aligned with NFR-008
- [ ] Comprehensive `prompt_guidance` with FR references
- [ ] YAML syntax valid
- [ ] Passes JSON Schema validation (TASK-129)

### Prompt Guidance Requirements

The `prompt_guidance` section must include:
- [ ] Action Items guidance with FR-006 reference
- [ ] Decisions guidance with FR-007 reference
- [ ] Questions guidance with FR-008 reference
- [ ] Speakers guidance with PAT-003 4-pattern chain
- [ ] Topics guidance with FR-009 boundary detection
- [ ] Confidence scoring guidance with NFR-008 thresholds

### Related Items

- Parent: [EN-014: Domain Context Files Implementation](./EN-014-domain-context-files.md)
- Blocked By: [TASK-126: general.yaml](./TASK-126-general-domain-schema.md)
- Blocks: [TASK-128: meeting.yaml](./TASK-128-meeting-domain-schema.md)
- References: [SPEC-context-injection.md Section 3.3](../../FEAT-001-analysis-design/EN-006-context-injection-design/docs/specs/SPEC-context-injection.md)
- References: FR-005, FR-006, FR-007, FR-008, FR-009
- References: PAT-001 (Tiered Extraction), PAT-003 (Speaker Detection)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| transcript.yaml | Implementation | skills/transcript/contexts/transcript.yaml |
| Schema validation result | Evidence | (in this file) |

### Verification

- [ ] File created at correct location
- [ ] All 5 entities defined
- [ ] Extraction patterns complete
- [ ] YAML syntax validates
- [ ] JSON Schema validation passes
- [ ] Reviewed by: (pending)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-26 | Created | Initial task creation per EN-014 |
