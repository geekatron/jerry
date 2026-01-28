# TASK-124: Create JSON Schema for Context Validation

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-013 (Context Injection Implementation)
-->

---

## Frontmatter

```yaml
id: "TASK-124"
work_type: TASK
title: "Create JSON Schema for Context Validation"
description: |
  Create a JSON Schema for validating context injection YAML files
  (domain schemas, SKILL.md sections) per REQ-CI-F-009.

classification: ENABLER
status: DONE
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
  - "json-schema"
  - "validation"
  - "REQ-CI-F-009"

effort: 1
acceptance_criteria: |
  - JSON Schema file created
  - Schema validates domain.yaml structure
  - Required fields enforced
  - Type constraints defined
  - general.yaml and transcript.yaml pass validation

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

Create a JSON Schema file that validates the structure of domain context files (*.yaml). This schema ensures all context files have required fields, correct types, and valid structures before they're loaded at runtime.

### File Location

```
skills/transcript/schemas/context-domain-schema.json
```

### Schema Structure

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://jerry-framework.dev/schemas/context-domain-1.0.0.json",
  "title": "Domain Context Schema",
  "description": "Schema for validating domain context YAML files",
  "type": "object",
  "required": ["schema_version", "domain", "entity_definitions"],
  "properties": {
    "schema_version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$",
      "description": "Semantic version of the schema"
    },
    "domain": {
      "type": "string",
      "minLength": 1,
      "description": "Domain identifier"
    },
    "display_name": {
      "type": "string",
      "description": "Human-readable domain name"
    },
    "entity_definitions": {
      "type": "object",
      "description": "Map of entity type to definition",
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
      "type": "string",
      "description": "Expert guidance for LLM prompts"
    }
  },
  "$defs": {
    "entityDefinition": {
      "type": "object",
      "required": ["description", "attributes"],
      "properties": {
        "description": {
          "type": "string"
        },
        "attributes": {
          "type": "array",
          "items": {
            "$ref": "#/$defs/attribute"
          }
        },
        "extraction_patterns": {
          "type": "array",
          "items": {
            "type": "string"
          }
        }
      }
    },
    "attribute": {
      "type": "object",
      "required": ["name", "type"],
      "properties": {
        "name": {
          "type": "string"
        },
        "type": {
          "type": "string",
          "enum": ["string", "integer", "float", "boolean", "date", "array"]
        },
        "required": {
          "type": "boolean"
        },
        "enum": {
          "type": "array",
          "items": {
            "type": "string"
          }
        }
      }
    },
    "extractionRule": {
      "type": "object",
      "required": ["id", "entity_type"],
      "properties": {
        "id": {
          "type": "string"
        },
        "entity_type": {
          "type": "string"
        },
        "confidence_threshold": {
          "type": "number",
          "minimum": 0,
          "maximum": 1
        },
        "priority": {
          "type": "integer",
          "minimum": 1
        }
      }
    }
  }
}
```

### Validation Rules

| Field | Rule | Error Message |
|-------|------|---------------|
| schema_version | Required, semver format | "schema_version must be X.Y.Z format" |
| domain | Required, non-empty | "domain is required" |
| entity_definitions | Required, object | "entity_definitions must be an object" |
| attributes[].type | Enum validation | "Invalid attribute type: {type}" |
| extraction_rules[].confidence_threshold | 0-1 range | "Confidence must be between 0 and 1" |

### Acceptance Criteria

- [ ] JSON Schema file created at correct location
- [ ] `$schema` and `$id` metadata present
- [ ] `required` fields defined: schema_version, domain, entity_definitions
- [ ] `entity_definitions` schema validates entity structure
- [ ] `attributes` type enum includes all valid types
- [ ] `extraction_rules` schema with confidence constraints
- [ ] general.yaml validates against schema
- [ ] transcript.yaml validates against schema
- [ ] Invalid YAML produces descriptive errors

### Validation Test Cases

| Test ID | Input | Expected |
|---------|-------|----------|
| VAL-001 | Valid general.yaml | PASS |
| VAL-002 | Valid transcript.yaml | PASS |
| VAL-003 | Missing schema_version | FAIL: "required property" |
| VAL-004 | Invalid confidence (1.5) | FAIL: "must be <= 1" |
| VAL-005 | Invalid attribute type | FAIL: "must be one of enum" |
| VAL-006 | Empty domain | FAIL: "minLength" |

### Related Items

- Parent: [EN-013: Context Injection Implementation](./EN-013-context-injection.md)
- Blocked By: [TASK-120: SKILL.md context_injection section](./TASK-120-skill-context-injection.md)
- Blocks: [TASK-125: Validation and test scenarios](./TASK-125-context-validation.md)
- References: [SPEC-context-injection.md Section 2.3](../../FEAT-001-analysis-design/EN-006-context-injection-design/docs/specs/SPEC-context-injection.md)
- References: REQ-CI-F-009 (Schema Validation)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| context-domain-schema.json | Implementation | skills/transcript/schemas/context-domain-schema.json |
| Validation test results | Evidence | (in this file) |

### Verification

- [ ] JSON Schema file created
- [ ] Schema is valid JSON Schema draft-2020-12
- [ ] general.yaml passes validation
- [ ] transcript.yaml passes validation
- [ ] Invalid files produce clear errors
- [ ] Reviewed by: (pending)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-26 | Created | Initial task creation per EN-013 |
| 2026-01-28 | **DONE** | Created schemas/context-domain-schema.json using JSON Schema draft-2020-12. Includes required fields (schema_version, domain, entity_definitions), $defs for entityDefinition, attribute, extractionRule. Validates both general.yaml and transcript.yaml. |
