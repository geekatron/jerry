# TASK-155: Transform & Create security-engineering.yaml Domain Schema

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
id: "TASK-155"
work_type: TASK
title: "Transform & Create security-engineering.yaml Domain Schema"
description: |
  Transform EN-006 security-engineering domain artifacts (entity-definitions.yaml,
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
  - "security-engineering"
  - "DISC-005"

effort: 1
acceptance_criteria: |
  - security-engineering.yaml created in contexts/ folder
  - All domain-specific entities transformed (vulnerability, threat, compliance, etc.)
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

Transform the EN-006 security-engineering domain design artifacts into a single consolidated YAML file for runtime use by the transcript skill. This domain focuses on security discussions, threat modeling, and compliance topics.

### Source Artifacts (EN-006)

```
EN-006/docs/specs/domain-contexts/06-security-engineering/
├── SPEC-security-engineering.md          # L0/L1/L2 domain documentation
├── entities/entity-definitions.yaml      # Security-specific entities
├── extraction/extraction-rules.yaml      # Security extraction patterns
├── prompts/prompt-templates.md           # Security analysis prompts
└── validation/acceptance-criteria.md     # Validation criteria
```

### Target Artifact

```
skills/transcript/contexts/security-engineering.yaml
```

### Expected Entities (Security Engineering Domain)

| Entity | Description | Key Attributes |
|--------|-------------|----------------|
| `vulnerability` | Security vulnerability | severity, cve_id, affected_component |
| `threat` | Identified threat | threat_actor, attack_vector, impact |
| `security_control` | Control discussion | control_type, implementation, status |
| `compliance_requirement` | Compliance topic | framework, requirement, status |
| `security_decision` | Security choice | topic, decision, risk_accepted |

### Acceptance Criteria

- [ ] File created at `skills/transcript/contexts/security-engineering.yaml`
- [ ] `schema_version: "1.0.0"` present
- [ ] `domain: "security-engineering"` set
- [ ] `display_name: "Security Engineering Transcript Analysis"` set
- [ ] All domain entities transformed (minimum 4 per DOMAIN-SCHEMA.json)
- [ ] Each entity has minimum 3 attributes
- [ ] Extraction rules present with confidence thresholds
- [ ] Extraction patterns merged (minimum 4 per entity type)
- [ ] `prompt_guidance` synthesized with security-specific advice
- [ ] Template variables in `{{$variable}}` format
- [ ] YAML syntax valid
- [ ] Passes JSON Schema validation (after TASK-129)

### Related Items

- Parent: [EN-014: Domain Context Files Implementation](./EN-014-domain-context-files.md)
- Discovery: [DISC-005: EN-006 Artifact Promotion Gap](../FEAT-002--DISC-005-en006-artifact-promotion-gap.md)
- Blocked By: [TASK-129: JSON Schema Validator](./TASK-129-domain-json-schema.md)
- Blocks: [TASK-157: SPEC Files Promotion](./TASK-157-spec-files-promotion.md), [TASK-158: SKILL.md Update](./TASK-158-skill-md-domain-update.md)
- Source: [EN-006 06-security-engineering](../../FEAT-001-analysis-design/EN-006-context-injection-design/docs/specs/domain-contexts/06-security-engineering/)
- References: [SPEC-context-injection.md Section 3.3](../../FEAT-001-analysis-design/EN-006-context-injection-design/docs/specs/SPEC-context-injection.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| security-engineering.yaml | Implementation | skills/transcript/contexts/security-engineering.yaml |
| Schema validation result | Evidence | (in this file) |

### Verification

- [ ] File created at correct location
- [ ] YAML syntax validates
- [ ] All domain entities present with attributes
- [ ] Extraction patterns merged correctly
- [ ] prompt_guidance synthesized
- [ ] JSON Schema validation passes
- [ ] Reviewed by: (pending)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-28 | Created | Initial task creation per DISC-005 EN-006 artifact promotion |
