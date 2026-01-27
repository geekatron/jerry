# TASK-128: Create meeting.yaml Extended Domain Schema

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-014 (Domain Context Files Implementation)
-->

---

## Frontmatter

```yaml
id: "TASK-128"
work_type: TASK
title: "Create meeting.yaml Extended Domain Schema"
description: |
  Create the meeting.yaml domain schema that extends transcript.yaml
  with meeting-specific entities: attendee, agenda_item, follow_up.

classification: ENABLER
status: BACKLOG
resolution: null
priority: MEDIUM
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-26T19:30:00Z"
updated_at: "2026-01-26T19:30:00Z"

parent_id: "EN-014"

tags:
  - "implementation"
  - "domain-context"
  - "meeting-domain"
  - "domain-inheritance"

effort: 1
acceptance_criteria: |
  - meeting.yaml created extending transcript.yaml
  - Meeting-specific entities: attendee, agenda_item, follow_up
  - Extraction rules for meeting entities
  - prompt_guidance with meeting-specific advice

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

Create the meeting domain schema (`meeting.yaml`) that extends the core transcript.yaml with meeting-specific entities. This demonstrates the domain inheritance model where specialized domains build on the base transcript entities.

### File Location

```
skills/transcript/contexts/meeting.yaml
```

### Domain Inheritance

```
transcript.yaml
     │
     │ extends
     ▼
meeting.yaml
  ├── Inherits: action_item, decision, question, speaker, topic
  └── Adds: attendee, agenda_item, follow_up
```

### Meeting-Specific Entities

| Entity | Description | Attributes |
|--------|-------------|------------|
| attendee | Person present in meeting | name, role (enum), department, present_from_ms, present_to_ms |
| agenda_item | Item from meeting agenda | title, presenter, allocated_time_min, actual_time_min, status (enum) |
| follow_up | Post-meeting follow-up | text, owner, target_meeting, priority (enum) |

### Role Enumerations

```yaml
attendee.role:
  - "organizer"
  - "presenter"
  - "participant"
  - "guest"

agenda_item.status:
  - "covered"
  - "deferred"
  - "skipped"

follow_up.priority:
  - "high"
  - "medium"
  - "low"
```

### Extraction Rules

| Rule ID | Entity Type | Confidence | Priority | Tier |
|---------|-------------|------------|----------|------|
| attendees | attendee | 0.85 | 0 | rule |
| agenda_items | agenda_item | 0.75 | 6 | llm |
| follow_ups | follow_up | 0.7 | 7 | ml |

### Acceptance Criteria

- [ ] File created at `skills/transcript/contexts/meeting.yaml`
- [ ] `schema_version: "1.0.0"` present
- [ ] `domain: "meeting"` set
- [ ] `extends: "transcript"` declared
- [ ] All 3 meeting entities defined (attendee, agenda_item, follow_up)
- [ ] Enum values for roles and statuses
- [ ] `extraction_rules` for meeting entities
- [ ] `prompt_guidance` with meeting-specific advice
- [ ] YAML syntax valid
- [ ] Passes JSON Schema validation (TASK-129)

### Prompt Guidance Requirements

The `prompt_guidance` section must include:
- [ ] Attendees guidance (roll call, speaker labels, join/leave tracking)
- [ ] Agenda Items guidance (structure recognition, topic transitions)
- [ ] Follow-ups guidance (distinct from action items, future meetings)
- [ ] Note about inheriting transcript.yaml entities

### Related Items

- Parent: [EN-014: Domain Context Files Implementation](./EN-014-domain-context-files.md)
- Blocked By: [TASK-127: transcript.yaml](./TASK-127-transcript-domain-schema.md)
- Blocks: [TASK-130: Schema validation](./TASK-130-schema-validation.md)
- References: [SPEC-context-injection.md Section 3.3](../../FEAT-001-analysis-design/EN-006-context-injection-design/docs/specs/SPEC-context-injection.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| meeting.yaml | Implementation | skills/transcript/contexts/meeting.yaml |
| Schema validation result | Evidence | (in this file) |

### Verification

- [ ] File created at correct location
- [ ] Extends transcript.yaml correctly
- [ ] All 3 meeting entities defined
- [ ] YAML syntax validates
- [ ] JSON Schema validation passes
- [ ] Reviewed by: (pending)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-26 | Created | Initial task creation per EN-014 |
