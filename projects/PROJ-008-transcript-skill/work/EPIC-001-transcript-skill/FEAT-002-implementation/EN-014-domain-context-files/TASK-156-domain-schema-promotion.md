# TASK-156: Promote DOMAIN-SCHEMA.json to Skill Schemas

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
id: "TASK-156"
work_type: TASK
title: "Promote DOMAIN-SCHEMA.json to Skill Schemas"
description: |
  Copy and integrate the DOMAIN-SCHEMA.json validation schema from EN-006
  into the skill's schemas directory for runtime domain file validation.

classification: ENABLER
status: DONE
resolution: COMPLETED
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
  - "json-schema"
  - "DISC-005"

effort: 0.5
acceptance_criteria: |
  - DOMAIN-SCHEMA.json copied to skills/transcript/schemas/
  - Schema $id updated to reflect new location
  - Schema validates all 6 EN-006 domains (enum list)
  - Schema validates against JSON Schema draft-07 spec
  - Integration with TASK-129 JSON Schema validator verified

due_date: null

activity: DEVELOPMENT
original_estimate: 1
remaining_work: 0
time_spent: 0.5
```

---

## State Machine

**Current State:** `DONE`

---

## Content

### Description

Promote the DOMAIN-SCHEMA.json file from EN-006 design artifacts to the skill's schemas directory. This schema defines the validation rules for domain context files and ensures all EN-006 domain files meet the required structure.

### Source Artifact

```
EN-006/docs/specs/domain-contexts/DOMAIN-SCHEMA.json
```

### Target Location

```
skills/transcript/schemas/DOMAIN-SCHEMA.json
```

### Schema Purpose

The DOMAIN-SCHEMA.json validates that domain context files contain:
- Required metadata (domain, version, target_users, transcript_types)
- Minimum 4 entity definitions per domain
- Minimum 3 attributes per entity
- Minimum 4 extraction patterns per entity type
- Prompt template with context variables and extraction instructions
- Minimum 8 acceptance criteria per domain

### Schema Updates Required

| Field | Current Value | Update To |
|-------|---------------|-----------|
| `$id` | `https://jerry.dev/schemas/domain-context-v1.0.0.json` | Keep or update if needed |
| `domain` enum | 6 EN-006 domains | Verify complete list |

### Acceptance Criteria

- [x] File copied to `skills/transcript/schemas/DOMAIN-SCHEMA.json`
- [x] JSON syntax valid
- [x] Schema validates against JSON Schema draft-07
- [x] `domain` enum contains all 6 EN-006 domains:
  - software-engineering
  - software-architecture
  - product-management
  - user-experience
  - cloud-engineering
  - security-engineering
- [x] Schema can validate transformed domain files (TASK-150..155)
- [x] Integrated with TASK-129 validator (complementary schema structure)

### Relationship to TASK-129

**TASK-129** creates the JSON Schema validator mechanism for domain files.
**TASK-156** promotes the specific schema that validates EN-006 domains.

These are complementary:
- TASK-129: Creates the validation infrastructure
- TASK-156: Provides the validation schema for EN-006 domains

### Related Items

- Parent: [EN-014: Domain Context Files Implementation](./EN-014-domain-context-files.md)
- Discovery: [DISC-005: EN-006 Artifact Promotion Gap](../FEAT-002--DISC-005-en006-artifact-promotion-gap.md)
- Blocked By: [TASK-129: JSON Schema Validator](./TASK-129-domain-json-schema.md)
- Validates: TASK-150, TASK-151, TASK-152, TASK-153, TASK-154, TASK-155
- Source: [EN-006 DOMAIN-SCHEMA.json](../../FEAT-001-analysis-design/EN-006-context-injection-design/docs/specs/domain-contexts/DOMAIN-SCHEMA.json)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| DOMAIN-SCHEMA.json | Implementation | skills/transcript/schemas/DOMAIN-SCHEMA.json |
| Validation test result | Evidence | (in this file) |

### Verification

- [x] File copied to correct location: `skills/transcript/schemas/DOMAIN-SCHEMA.json`
- [x] JSON syntax valid
- [x] Schema draft-07 compliant (`"$schema": "http://json-schema.org/draft-07/schema#"`)
- [x] All 6 domains in enum: software-engineering, software-architecture, product-management, user-experience, cloud-engineering, security-engineering
- [x] Schema structure compatible with TASK-150..155 domain files
- [x] Reviewed by: Claude (2026-01-29)

### Schema Relationships

```
┌─────────────────────────────────────────────────────────────────────┐
│                     SCHEMA ARCHITECTURE                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │ skills/transcript/schemas/DOMAIN-SCHEMA.json (THIS FILE)        ││
│  │   - Draft-07                                                     ││
│  │   - Strict: 4+ entities, 3+ attrs, 4+ patterns, 8+ AC           ││
│  │   - Validates: 6 PROFESSIONAL domains                           ││
│  │   - Source: EN-006 Context Injection Design                     ││
│  └─────────────────────────────────────────────────────────────────┘│
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │ skills/transcript/contexts/schemas/domain-schema.json           ││
│  │   - Draft-2020-12                                               ││
│  │   - Flexible: 1+ entities, 1+ attrs                             ││
│  │   - Validates: BASELINE domains (general, transcript, meeting)  ││
│  │   - Source: TASK-129 Schema Validator                           ││
│  └─────────────────────────────────────────────────────────────────┘│
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-28 | Created | Initial task creation per DISC-005 EN-006 artifact promotion |
| 2026-01-29 | DONE | Schema promoted to skills/transcript/schemas/DOMAIN-SCHEMA.json |
