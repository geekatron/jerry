# TASK-129: Create JSON Schema Validator for Domain Files

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-014 (Domain Context Files Implementation)
-->

---

## Frontmatter

```yaml
id: "TASK-129"
work_type: TASK
title: "Create JSON Schema Validator for Domain Files"
description: |
  Create a JSON Schema file for validating domain context YAML files
  ensuring consistent structure across all domain schemas.

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
  - "json-schema"
  - "validation"
  - "REQ-CI-F-009"

effort: 1
acceptance_criteria: |
  - JSON Schema file created
  - Schema validates domain YAML structure
  - Required fields enforced
  - Type constraints defined
  - Enum constraints for valid values

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

Create a JSON Schema file that validates the structure of domain context YAML files. This ensures all domain schemas follow a consistent structure with required fields, correct types, and valid enum values.

### File Location

```
skills/transcript/contexts/schemas/domain-schema.json
```

### Schema Structure

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://jerry-framework.dev/schemas/domain-context-1.0.0.json",
  "title": "Domain Context Schema",
  "description": "Schema for validating domain context YAML files",
  "type": "object",
  "required": ["schema_version", "domain", "entity_definitions"],
  "properties": {
    "schema_version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "domain": {
      "type": "string",
      "minLength": 1
    },
    "display_name": {
      "type": "string"
    },
    "extends": {
      "type": "string",
      "description": "Parent domain to inherit from"
    },
    "entity_definitions": {
      "type": "object",
      "additionalProperties": {
        "$ref": "#/$defs/entityDefinition"
      }
    },
    "extraction_rules": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/extractionRule"
      }
    },
    "prompt_guidance": {
      "type": "string"
    }
  }
}
```

### Schema Definitions ($defs)

```json
{
  "$defs": {
    "entityDefinition": {
      "type": "object",
      "required": ["description", "attributes"],
      "properties": {
        "description": { "type": "string" },
        "attributes": {
          "type": "array",
          "items": { "$ref": "#/$defs/attribute" }
        },
        "extraction_patterns": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },
    "attribute": {
      "type": "object",
      "required": ["name", "type"],
      "properties": {
        "name": { "type": "string" },
        "type": {
          "type": "string",
          "enum": ["string", "integer", "float", "boolean", "date", "array", "enum"]
        },
        "required": { "type": "boolean" },
        "default": {},
        "values": {
          "type": "array",
          "items": { "type": "string" }
        },
        "items": { "type": "string" }
      }
    },
    "extractionRule": {
      "type": "object",
      "required": ["id", "entity_type"],
      "properties": {
        "id": { "type": "string" },
        "entity_type": { "type": "string" },
        "confidence_threshold": {
          "type": "number",
          "minimum": 0,
          "maximum": 1
        },
        "priority": {
          "type": "integer",
          "minimum": 0
        },
        "tier": {
          "type": "string",
          "enum": ["rule", "ml", "llm"]
        }
      }
    }
  }
}
```

### Validation Rules

| Field | Rule | Error Message |
|-------|------|---------------|
| schema_version | Required, semver pattern | "must be X.Y.Z format" |
| domain | Required, non-empty | "domain is required" |
| entity_definitions | Required, object | "entity_definitions must be an object" |
| attributes[].type | Enum: string, integer, float, boolean, date, array, enum | "invalid type" |
| extraction_rules[].confidence_threshold | 0 ≤ value ≤ 1 | "must be between 0 and 1" |
| extraction_rules[].tier | Enum: rule, ml, llm | "must be rule, ml, or llm" |

### Acceptance Criteria

- [ ] JSON Schema file created at correct location
- [ ] `$schema` references draft-2020-12
- [ ] `$id` set to jerry-framework URL
- [ ] `required` fields: schema_version, domain, entity_definitions
- [ ] Entity definition schema complete
- [ ] Attribute schema with type enum
- [ ] Extraction rule schema with confidence constraints
- [ ] Tier enum for PAT-001 compliance
- [ ] `extends` field supported for domain inheritance
- [ ] Schema validates as valid JSON Schema

### Related Items

- Parent: [EN-014: Domain Context Files Implementation](./EN-014-domain-context-files.md)
- Blocked By: [TASK-126: general.yaml](./TASK-126-general-domain-schema.md)
- Blocks: [TASK-130: Schema validation](./TASK-130-schema-validation.md)
- References: [SPEC-context-injection.md Section 2.3](../../FEAT-001-analysis-design/EN-006-context-injection-design/docs/specs/SPEC-context-injection.md)
- References: REQ-CI-F-009 (Schema Validation)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| domain-schema.json | Implementation | skills/transcript/contexts/schemas/domain-schema.json |
| Schema validation result | Evidence | (in this file) |

### Verification

- [ ] JSON Schema file created
- [ ] Schema is valid JSON Schema draft-2020-12
- [ ] Required fields enforced
- [ ] Type constraints defined
- [ ] Enum constraints working
- [ ] Reviewed by: (pending)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-26 | Created | Initial task creation per EN-014 |
