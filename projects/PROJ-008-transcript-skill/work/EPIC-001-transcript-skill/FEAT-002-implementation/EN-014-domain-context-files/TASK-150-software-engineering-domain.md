# TASK-150: Transform & Create software-engineering.yaml Domain Schema

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-014 (Domain Context Files Implementation)
DISCOVERY: DISC-005 (EN-006 Artifact Promotion Gap Analysis)
-->

---

## Frontmatter

```yaml
id: "TASK-150"
work_type: TASK
title: "Transform & Create software-engineering.yaml Domain Schema"
description: |
  Transform EN-006 software-engineering domain artifacts (entity-definitions.yaml,
  extraction-rules.yaml, prompt-templates.md) into a consolidated YAML file per
  SPEC-context-injection.md Section 3.3 design.

classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-28T21:30:00Z"
updated_at: "2026-01-28T21:30:00Z"

parent_id: "EN-014"

tags:
  - "implementation"
  - "domain-context"
  - "en006-promotion"
  - "software-engineering"
  - "DISC-005"

effort: 1
acceptance_criteria: |
  - software-engineering.yaml created in contexts/ folder
  - All 5 entities transformed: commitment, blocker, decision, action_item, risk
  - All extraction patterns merged from extraction-rules.yaml
  - prompt_guidance synthesized from prompt-templates.md
  - Schema version and domain metadata present
  - Passes JSON Schema validation (TASK-129)
  - Template variables use {{$variable}} format per SPEC

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

Transform the EN-006 software-engineering domain design artifacts into a single consolidated YAML file for runtime use by the transcript skill. This task implements the artifact promotion identified in DISC-005.

### Source Artifacts (EN-006)

```
EN-006/docs/specs/domain-contexts/01-software-engineering/
├── SPEC-software-engineering.md          # L0/L1/L2 domain documentation
├── entities/entity-definitions.yaml      # 5 entities: commitment, blocker, decision, action_item, risk
├── extraction/extraction-rules.yaml      # ~30 extraction patterns
├── prompts/prompt-templates.md           # Detailed extraction prompts
└── validation/acceptance-criteria.md     # Validation criteria
```

### Target Artifact

```
skills/transcript/contexts/software-engineering.yaml
```

### Transformation Rules

| Source Section | Target Section | Transformation |
|----------------|----------------|----------------|
| `entities/entity-definitions.yaml` → entities | `entity_definitions` | Flatten attributes to typed format |
| `extraction/extraction-rules.yaml` | `extraction_rules` | Add confidence thresholds, priorities |
| `prompts/prompt-templates.md` | `prompt_guidance` | Synthesize into concise guidance text |
| Metadata from all files | `schema_version`, `domain`, `display_name` | Consolidate metadata |

### Entity Transformation Example

**From EN-006 entity-definitions.yaml:**
```yaml
entities:
  commitment:
    description: "Work item a team member commits to complete..."
    attributes:
      - assignee: "Person making the commitment"
      - work_item: "Description of the work"
      - sprint: "Sprint or time period"
```

**To consolidated YAML:**
```yaml
entity_definitions:
  commitment:
    description: "Work item a team member commits to complete within a time period"
    attributes:
      - name: "assignee"
        type: "string"
        required: true
      - name: "work_item"
        type: "string"
        required: true
      - name: "sprint"
        type: "string"
      - name: "confidence"
        type: "enum"
        values: ["high", "medium", "low"]
    extraction_patterns:
      - "I will {{work_item}}"
      - "I'm going to {{work_item}}"
      - "I'll take {{work_item}}"
```

### Acceptance Criteria

- [ ] File created at `skills/transcript/contexts/software-engineering.yaml`
- [ ] `schema_version: "1.0.0"` present
- [ ] `domain: "software-engineering"` set
- [ ] `display_name: "Software Engineering Transcript Analysis"` set
- [ ] All 5 entities transformed (commitment, blocker, decision, action_item, risk)
- [ ] Each entity has minimum 3 attributes (per DOMAIN-SCHEMA.json)
- [ ] Extraction rules present with confidence thresholds (0.0-1.0)
- [ ] Extraction patterns merged (minimum 4 per entity type per schema)
- [ ] `prompt_guidance` synthesized with domain-specific advice
- [ ] Template variables in `{{$variable}}` format
- [ ] YAML syntax valid
- [ ] Passes JSON Schema validation (after TASK-129)

### Related Items

- Parent: [EN-014: Domain Context Files Implementation](./EN-014-domain-context-files.md)
- Discovery: [DISC-005: EN-006 Artifact Promotion Gap](../FEAT-002--DISC-005-en006-artifact-promotion-gap.md)
- Blocked By: [TASK-129: JSON Schema Validator](./TASK-129-domain-json-schema.md)
- Blocks: [TASK-157: SPEC Files Promotion](./TASK-157-spec-files-promotion.md), [TASK-158: SKILL.md Update](./TASK-158-skill-md-domain-update.md)
- Source: [EN-006 01-software-engineering](../../FEAT-001-analysis-design/EN-006-context-injection-design/docs/specs/domain-contexts/01-software-engineering/)
- References: [SPEC-context-injection.md Section 3.3](../../FEAT-001-analysis-design/EN-006-context-injection-design/docs/specs/SPEC-context-injection.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| software-engineering.yaml | Implementation | skills/transcript/contexts/software-engineering.yaml |
| Schema validation result | Evidence | (in this file) |

### Source Artifact Checksums

| File | Purpose | Lines |
|------|---------|-------|
| entity-definitions.yaml | Entities | ~110 |
| extraction-rules.yaml | Patterns | ~140 |
| prompt-templates.md | Prompts | ~303 |

### Verification

- [ ] File created at correct location
- [ ] YAML syntax validates
- [ ] All 5 entities present with attributes
- [ ] Extraction patterns merged correctly
- [ ] prompt_guidance synthesized
- [ ] JSON Schema validation passes
- [ ] Reviewed by: (pending)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-28 | Created | Initial task creation per DISC-005 EN-006 artifact promotion |
