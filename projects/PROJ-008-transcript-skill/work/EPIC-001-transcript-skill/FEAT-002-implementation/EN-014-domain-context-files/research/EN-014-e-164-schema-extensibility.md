# Research: JSON Schema Extensibility Patterns for Domain Context

<!--
PS-ID: EN-014
Entry-ID: e-164
Agent: ps-researcher (v2.0.0)
Topic: Schema Extensibility Patterns for Domain Context Files
Created: 2026-01-29
Framework: 5W2H + Evidence-Based Analysis
-->

> **Research ID:** EN-014-e-164
> **Agent:** ps-researcher (v2.0.0)
> **Status:** COMPLETE
> **Created:** 2026-01-29T00:00:00Z
> **Topic:** Schema Extensibility Patterns for Domain Context Files

---

## L0: Executive Summary (ELI5)

### The Library Analogy

Imagine you have a library catalog system. Right now, it can list books with their titles and authors. But you want to also show:
- **Which books reference other books** (like a textbook citing sources)
- **Who should read each book** (students, teachers, researchers)
- **Different rules for different sections** (fiction vs. non-fiction has different organization)
- **Quality checks** (must have at least 3 books per category)

**The Problem:** Your current catalog form doesn't have spaces to write this extra information.

**The Solution:** You can:
1. **Add new sections to your form** (JSON Schema's `$defs` and `$ref` patterns)
2. **Use sticky notes with special colors** (like JSON-LD's `@type` and `@context` for relationships)
3. **Create conditional rules** ("IF this is a textbook, THEN require these extra fields")

**Key Finding:** We can extend our existing JSON Schema without starting over. The changes are "additive" - old forms still work, new forms have more features.

---

## L1: Technical Analysis (Engineer)

### Current Schema Gaps Analysis

The current `domain-schema.json` (v1.0.0) at `skills/transcript/contexts/schemas/domain-schema.json` supports:
- Entity definitions with attributes
- Extraction rules with tiers
- Prompt guidance
- Basic inheritance via `extends`

**What's Missing (4 Gaps from DISC-006):**

| Gap ID | Feature | Current State | Required Capability |
|--------|---------|---------------|---------------------|
| GAP-001 | Entity Relationships | None | blocks, resolves, triggers between entities |
| GAP-002 | Domain Metadata | None | target_users, transcript_types, key_use_cases |
| GAP-003 | Context Rules | None | Meeting-type-specific extraction focus |
| GAP-004 | Validation Rules | None | min_entities, required_entities constraints |

### JSON Schema 2020-12 Extensibility Mechanisms

Based on [JSON Schema Understanding Guide](https://json-schema.org/understanding-json-schema/reference/object), the following mechanisms are available:

#### 1. Schema Composition with `$defs` and `$ref`

The `$defs` keyword allows defining reusable schema fragments:

```json
{
  "$defs": {
    "relationship": {
      "type": "object",
      "properties": {
        "type": { "type": "string", "enum": ["blocks", "resolves", "triggers", "depends_on"] },
        "target": { "type": "string" },
        "cardinality": { "type": "string", "enum": ["one-to-one", "one-to-many", "many-to-many"] }
      },
      "required": ["type", "target"]
    }
  }
}
```

**Usage Pattern:** Reference via `"$ref": "#/$defs/relationship"` anywhere in the schema.

**Evidence:** [JSON Schema Bundling with $ref and $defs](https://json-schema.org/understanding-json-schema/reference/object) demonstrates nested schema references for complex compositions.

#### 2. `unevaluatedProperties` for Safe Extension

The key insight from JSON Schema spec research: **`unevaluatedProperties` is superior to `additionalProperties` for extensibility**.

```json
{
  "allOf": [
    { "$ref": "#/$defs/baseEntity" }
  ],
  "properties": {
    "relationships": { "$ref": "#/$defs/relationshipArray" }
  },
  "unevaluatedProperties": false
}
```

**Why This Matters:**
- `additionalProperties: false` **breaks** schema extension because properties in `allOf` subschemas are considered "additional"
- `unevaluatedProperties: false` correctly recognizes properties from all subschemas

**Evidence:** [JSON Schema Spec - unevaluatedProperties](https://github.com/json-schema-org/json-schema-spec/blob/main/specs/jsonschema-core.md) states: "Validates against property values not deemed 'evaluated'."

#### 3. Conditional Validation with `if-then-else`

For GAP-003 (Context Rules), JSON Schema's conditional keywords enable meeting-type-specific validation:

```json
{
  "allOf": [
    {
      "if": {
        "properties": { "meeting_type": { "const": "daily_standup" } }
      },
      "then": {
        "properties": {
          "primary_entities": {
            "type": "array",
            "contains": { "const": "commitment" }
          }
        }
      }
    }
  ]
}
```

**Evidence:** [JSON Schema Conditionals Reference](https://json-schema.org/understanding-json-schema/reference/conditionals) provides scalable patterns using `allOf` with nested `if-then` blocks.

#### 4. `dependentRequired` and `dependentSchemas`

For expressing inter-property dependencies (GAP-004):

```json
{
  "dependentRequired": {
    "context_rules": ["meeting_type"]
  },
  "dependentSchemas": {
    "validation": {
      "properties": {
        "min_entities": { "type": "integer", "minimum": 1 }
      }
    }
  }
}
```

**Evidence:** [dependentRequired documentation](https://json-schema.org/understanding-json-schema/reference/conditionals) shows this pattern for conditional property requirements.

### Entity Relationship Patterns Comparison

| Approach | Complexity | Tooling Support | Semantic Richness | Backward Compat |
|----------|------------|-----------------|-------------------|-----------------|
| **JSON Schema `$defs`** | Low | High (ajv, jsonschema) | Medium | Excellent |
| **JSON-LD `@context`** | High | Medium (specialized) | Excellent | Poor |
| **Custom `relationships` property** | Low | High | Medium | Excellent |
| **OpenAPI `x-` extensions** | Low | High | Low | Excellent |

#### Recommended Pattern: Inline Relationship Definition

Based on the evidence, the optimal pattern for GAP-001 (Entity Relationships) is:

```json
{
  "entityDefinition": {
    "type": "object",
    "properties": {
      "relationships": {
        "type": "array",
        "items": {
          "$ref": "#/$defs/entityRelationship"
        }
      }
    }
  },
  "$defs": {
    "entityRelationship": {
      "type": "object",
      "required": ["type", "target"],
      "properties": {
        "type": {
          "type": "string",
          "enum": ["blocks", "resolves", "triggers", "depends_on", "related_to"],
          "description": "Semantic relationship type"
        },
        "target": {
          "type": "string",
          "description": "Target entity type identifier"
        },
        "cardinality": {
          "type": "string",
          "enum": ["one-to-one", "one-to-many", "many-to-many"],
          "default": "one-to-many"
        },
        "bidirectional": {
          "type": "boolean",
          "default": false,
          "description": "Whether relationship is symmetric"
        }
      }
    }
  }
}
```

**Rationale:**
1. **Stays within JSON Schema ecosystem** - No new technology dependency
2. **Full ajv/jsonschema support** - Immediate validation capability
3. **Backward compatible** - `relationships` is optional; existing YAML files remain valid
4. **Expressive enough** - Covers blocks, resolves, triggers patterns from EN-006

### Validation Library Support

Research on validation library capabilities:

| Library | Language | Custom Keywords | Conditional | `unevaluatedProperties` |
|---------|----------|-----------------|-------------|-------------------------|
| **ajv** | JavaScript | Yes (plugins) | Yes | Yes (2020-12) |
| **jsonschema** | Python | Limited | Yes | Yes (4.x+) |
| **json-schema-validator** | Java | Yes | Yes | Yes |

**ajv Custom Keywords Example:**

```javascript
// From https://ajv.js.org/keywords.html
ajv.addKeyword({
  keyword: "minEntities",
  type: "object",
  validate: (schema, data) => {
    const entityCount = Object.keys(data.entity_definitions || {}).length;
    return entityCount >= schema;
  }
});
```

**Evidence:** [Ajv User Defined Keywords](https://ajv.js.org/keywords.html) demonstrates code generation and compile-time keyword extension patterns.

---

## L2: Strategic Implications (Architect)

### Technology Selection Decision Matrix

| Criterion | JSON Schema Extension | JSON-LD Adoption | Hybrid Approach |
|-----------|----------------------|------------------|-----------------|
| **Existing Investment** | Leverages 100% | Requires rewrite | 70% reuse |
| **Blast Radius** | Minimal | High | Medium |
| **Learning Curve** | Low | High | Medium |
| **Tool Chain Impact** | None | Significant | Minor |
| **Future Flexibility** | Medium | High | Medium-High |
| **Time to Implement** | 1-2 days | 2-4 weeks | 1 week |

**Recommendation:** **JSON Schema Extension** with optional JSON-LD annotations for future interoperability.

### Backward Compatibility Strategy

Following [SchemaVer semantic versioning for schemas](https://snowplow.io/blog/introducing-schemaver-for-semantic-versioning-of-schemas):

| Change Type | Version Impact | Example |
|-------------|----------------|---------|
| Add optional property | ADDITION (1.0.0 -> 1.0.1) | `relationships: []` |
| Add required property | REVISION (1.0.0 -> 1.1.0) | New required field |
| Remove property | MODEL (1.0.0 -> 2.0.0) | Breaking change |

**Proposed Schema V2 Versioning:**

```yaml
schema_version: "1.1.0"  # REVISION: New optional properties
```

**Migration Path:**
1. All new properties are **optional** with sane defaults
2. Existing YAML files validate against v1.1.0 unchanged
3. Schema validators use `"default"` values for missing properties

### Performance Considerations

| Pattern | Validation Time | Memory Impact | Notes |
|---------|----------------|---------------|-------|
| Simple `$ref` | O(1) | Minimal | Cached resolution |
| `allOf` composition | O(n) | Linear | n = number of subschemas |
| `if-then-else` | O(n) | Linear | Evaluated per condition |
| `unevaluatedProperties` | O(properties) | Minimal | Single pass |

**Recommendation:** Use `allOf` with `if-then` sparingly; prefer `$defs` composition for reusable patterns.

### One-Way Door Analysis

| Decision | Reversibility | Risk Level | Mitigation |
|----------|---------------|------------|------------|
| Add `relationships` property | Reversible | Low | Optional, backward compat |
| Add `metadata` section | Reversible | Low | Optional, backward compat |
| Add `context_rules` | Reversible | Medium | Test with multiple domains |
| Add `validation` section | Reversible | Low | Optional, progressive |
| Adopt JSON-LD fully | **Irreversible** | **High** | **NOT RECOMMENDED** |

### Architecture Decision Summary

```
┌────────────────────────────────────────────────────────────────┐
│                    RECOMMENDED APPROACH                        │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌─────────────────┐     ┌─────────────────┐                  │
│  │ Current Schema  │────►│ Extended Schema │                  │
│  │    v1.0.0       │     │    v1.1.0       │                  │
│  │                 │     │                 │                  │
│  │ - entities      │     │ - entities      │                  │
│  │ - rules         │     │ - rules         │                  │
│  │ - guidance      │     │ - guidance      │                  │
│  │                 │     │ + relationships │ ◄── GAP-001     │
│  │                 │     │ + metadata      │ ◄── GAP-002     │
│  │                 │     │ + context_rules │ ◄── GAP-003     │
│  │                 │     │ + validation    │ ◄── GAP-004     │
│  └─────────────────┘     └─────────────────┘                  │
│                                                                │
│  KEY: All new properties OPTIONAL with defaults               │
│       Existing YAML files remain 100% valid                   │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## Research Questions Analysis

### RQ-1: What patterns exist for representing entity relationships in JSON Schema?

**Answer:** Three primary patterns exist:

1. **Inline Array Pattern** (Recommended)
   ```json
   "relationships": [
     { "type": "blocks", "target": "commitment", "cardinality": "many-to-many" }
   ]
   ```

2. **Reference-Based Pattern**
   ```json
   "relationships": {
     "$ref": "https://example.com/schemas/relationships.json"
   }
   ```

3. **Nested Object Pattern**
   ```json
   "relationships": {
     "blocks": ["commitment", "action_item"],
     "resolves": ["blocker"]
   }
   ```

**Evidence:** [OpenAPI Extensions](https://swagger.io/docs/specification/v3_0/openapi-extensions/) and [CloudEvents Extensions](https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md) both use inline object patterns for extensibility.

### RQ-2: How do industry standards (JSON-LD, OWL, GraphQL) model entity relationships?

**JSON-LD Approach:**
```json
{
  "@context": "https://schema.org/",
  "@type": "Action",
  "object": { "@id": "commitment-123" },
  "result": { "@id": "action-item-456" }
}
```

**Advantages:** Semantic richness, W3C standard, knowledge graph compatibility
**Disadvantages:** Requires ontology, specialized tooling, learning curve

**Evidence:** [JSON-LD Best Practices](https://w3c.github.io/json-ld-bp/) states: "Use entity references SHOULD be used instead of string literals."

**GraphQL Approach:**
```graphql
type Entity {
  relationships: [Relationship!]!
}
type Relationship {
  type: RelationshipType!
  target: Entity!
}
```

**Relevance:** GraphQL patterns inform API design but don't directly apply to file-based schemas.

### RQ-3: What extensibility patterns (additionalProperties, $ref, $defs) are recommended?

**Ranked by Suitability:**

1. **`$defs` + `$ref`** - Best for reusable definitions
   - Evidence: [JSON Schema Bundling](https://json-schema.org/understanding-json-schema/reference/object)

2. **`unevaluatedProperties`** - Best for safe extension
   - Evidence: [JSON Schema Spec](https://github.com/json-schema-org/json-schema-spec/blob/main/specs/jsonschema-core.md)

3. **`additionalProperties: true`** - Allows any extension (permissive)
   - Risk: No validation of extension content

4. **`x-` prefix convention** - OpenAPI/AsyncAPI pattern
   - Evidence: [OpenAPI Extensions](https://swagger.io/docs/specification/v3_0/openapi-extensions/)
   - Use case: Vendor-specific extensions

**Recommendation:** Use `$defs` + `$ref` for structured extensions; avoid `additionalProperties: false` at root level.

### RQ-4: How can context-aware validation rules be expressed in JSON Schema?

**Pattern 1: Conditional Required Fields**
```json
{
  "if": {
    "properties": { "domain": { "const": "meeting" } }
  },
  "then": {
    "required": ["context_rules"]
  }
}
```

**Pattern 2: Dependent Schemas**
```json
{
  "dependentSchemas": {
    "context_rules": {
      "required": ["meeting_type"]
    }
  }
}
```

**Pattern 3: Validation Section**
```json
{
  "validation": {
    "min_entities": 4,
    "required_entities": ["commitment", "action_item"]
  }
}
```

**Evidence:** [JSON Schema Conditionals](https://json-schema.org/understanding-json-schema/reference/conditionals) provides postal code example demonstrating scalable conditional patterns.

### RQ-5: What backward compatibility strategies minimize breaking changes?

**Strategy Matrix:**

| Strategy | Description | Risk |
|----------|-------------|------|
| **Additive Only** | Only add optional properties | Lowest |
| **Default Values** | New required fields have defaults | Low |
| **Version Negotiation** | Support multiple schema versions | Medium |
| **Deprecation Cycle** | Mark old properties deprecated | Medium |
| **Breaking Version** | Major version bump | Highest |

**Best Practice from [Schema Evolution](https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html):**
> "Making new fields optional ensures backward compatibility when adding fields."

**Recommended Approach for domain-schema.json:**
1. Bump to v1.1.0 (REVISION)
2. All 4 new sections are OPTIONAL
3. Provide schema examples with new features
4. Document migration path in SKILL.md

---

## 5W2H Analysis Framework

### What?
Extend `domain-schema.json` from v1.0.0 to v1.1.0 to support:
- Entity relationships (GAP-001)
- Domain metadata (GAP-002)
- Context rules (GAP-003)
- Validation rules (GAP-004)

### Why?
- EN-006 artifacts contain rich semantic features that cannot be represented in current schema
- Without extension, promoting EN-006 to production causes **silent data loss**
- Extraction agents lose domain intelligence designed in EN-006

### Who?
- **Affected:** ts-extractor agent, domain YAML file authors, SKILL.md orchestrator
- **Implementing:** Schema architect, ps-architect agent
- **Reviewing:** ps-critic, nse-qa agents

### Where?
- `skills/transcript/contexts/schemas/domain-schema.json` (primary schema)
- `skills/transcript/contexts/domains/*.yaml` (consuming files)
- `skills/transcript/SKILL.md` (documentation)

### When?
- **Prerequisite for:** TASK-150..159 (domain YAML promotion)
- **Timeline:** 1-2 days implementation after ADR approval

### How?
1. Create ADR-EN014-001 documenting extension decision
2. Create TDD-domain-schema-v2 with technical design
3. Implement schema changes with backward compatibility
4. Update existing domain YAML files (general.yaml, meeting.yaml)
5. Validate with ajv/jsonschema

### How Much?
- **Effort:** 4-8 hours schema design + implementation
- **Risk:** Low (all changes are additive)
- **Testing:** Existing YAML files must pass v1.1.0 validation

---

## Sources Cited

| # | Source | Type | Authority | URL |
|---|--------|------|-----------|-----|
| 1 | JSON Schema Understanding Guide | Documentation | High | [json-schema.org](https://json-schema.org/understanding-json-schema/reference/object) |
| 2 | JSON Schema Specification | Specification | High | [GitHub](https://github.com/json-schema-org/json-schema-spec/blob/main/specs/jsonschema-core.md) |
| 3 | JSON-LD Best Practices | W3C Note | High | [W3C](https://w3c.github.io/json-ld-bp/) |
| 4 | Ajv JSON Schema Validator | Documentation | High | [ajv.js.org](https://ajv.js.org/keywords.html) |
| 5 | OpenAPI Specification Extensions | Documentation | High | [swagger.io](https://swagger.io/docs/specification/v3_0/openapi-extensions/) |
| 6 | CloudEvents Specification | Specification | High | [GitHub](https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md) |
| 7 | SchemaVer for Semantic Versioning | Blog/Prior Art | Medium | [Snowplow](https://snowplow.io/blog/introducing-schemaver-for-semantic-versioning-of-schemas) |
| 8 | Confluent Schema Evolution | Documentation | High | [Confluent Docs](https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html) |
| 9 | JSON Schema Conditionals Reference | Documentation | High | [json-schema.org](https://json-schema.org/understanding-json-schema/reference/conditionals) |

---

## Recommendations

### Primary Recommendation: JSON Schema Extension (v1.1.0)

**Decision:** Extend current JSON Schema with 4 new optional sections.

**Rationale:**
1. **Minimal blast radius** - No technology switch required
2. **Backward compatible** - Existing YAML files remain valid
3. **High tooling support** - ajv, jsonschema fully support patterns
4. **Evidence-based** - Patterns from OpenAPI, AsyncAPI, CloudEvents

### Schema V1.1.0 Structure

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://jerry-framework.dev/schemas/domain-context-1.1.0.json",
  "type": "object",
  "required": ["schema_version", "domain", "entity_definitions"],
  "properties": {
    "schema_version": { "type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$" },
    "domain": { "type": "string" },
    "entity_definitions": { "$ref": "#/$defs/entityDefinitions" },
    "extraction_rules": { "type": "array" },
    "prompt_guidance": { "type": "string" },
    "metadata": { "$ref": "#/$defs/domainMetadata" },
    "context_rules": { "$ref": "#/$defs/contextRules" },
    "validation": { "$ref": "#/$defs/validationRules" }
  },
  "$defs": {
    "entityRelationship": {
      "type": "object",
      "required": ["type", "target"],
      "properties": {
        "type": { "type": "string", "enum": ["blocks", "resolves", "triggers", "depends_on", "related_to"] },
        "target": { "type": "string" },
        "cardinality": { "type": "string", "enum": ["one-to-one", "one-to-many", "many-to-many"], "default": "one-to-many" },
        "bidirectional": { "type": "boolean", "default": false }
      }
    },
    "domainMetadata": {
      "type": "object",
      "properties": {
        "target_users": { "type": "array", "items": { "type": "string" } },
        "transcript_types": { "type": "array", "items": { "type": "string" } },
        "key_use_cases": { "type": "array", "items": { "type": "string" } }
      }
    },
    "contextRules": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "properties": {
          "meeting_type": { "type": "string" },
          "primary_entities": { "type": "array", "items": { "type": "string" } },
          "secondary_entities": { "type": "array", "items": { "type": "string" } },
          "extraction_focus": { "type": "string" }
        }
      }
    },
    "validationRules": {
      "type": "object",
      "properties": {
        "min_entities": { "type": "integer", "minimum": 0 },
        "required_entities": { "type": "array", "items": { "type": "string" } },
        "optional_entities": { "type": "array", "items": { "type": "string" } },
        "extraction_threshold": { "type": "number", "minimum": 0, "maximum": 1 }
      }
    }
  }
}
```

### Alternative Considered: JSON-LD Adoption

**NOT RECOMMENDED** for this phase due to:
- High learning curve (team unfamiliar with JSON-LD)
- Significant tooling changes required
- Existing JSON Schema investment would be lost
- Timeline constraints (EN-014 is blocking TASK-150..159)

**Future Consideration:** Add optional `@context` property for semantic web interoperability in v1.2.0 or v2.0.0.

### Implementation Sequence

```
TASK-164 (Research)    ──DONE──┐
                               │
TASK-165 (Analysis)   ◄────────┤
                               │
TASK-166 (ADR)        ◄────────┤
                               │
TASK-167 (TDD)        ◄────────┤
                               │
TASK-168 (Review)     ◄────────┤
                               │
TASK-169 (GATE)       ◄────────┘
                               │
                               ▼
                    TASK-150..159 UNBLOCKED
```

---

## Appendix A: Extended Entity Definition Example

```yaml
# Example: software-engineering.yaml with relationships
schema_version: "1.1.0"
domain: "software-engineering"

metadata:
  target_users:
    - "Software Engineers"
    - "Tech Leads"
  transcript_types:
    - "Daily standup"
    - "Sprint planning"
  key_use_cases:
    - "Track commitments and blockers"
    - "Surface decisions"

entity_definitions:
  blocker:
    description: "Issue preventing progress"
    attributes:
      - name: description
        type: string
        required: true
      - name: severity
        type: string
        enum: [low, medium, high, critical]
    relationships:
      - type: blocks
        target: commitment
        cardinality: many-to-many
      - type: resolved_by
        target: action_item
        cardinality: one-to-many

context_rules:
  standup:
    meeting_type: "daily_standup"
    primary_entities: [commitment, blocker]
    secondary_entities: [action_item]
    extraction_focus: "What did you do? What will you do? What blocks you?"

validation:
  min_entities: 4
  required_entities: [commitment, blocker, action_item]
  extraction_threshold: 0.7
```

---

## Appendix B: Validation Library Code Examples

### Python (jsonschema)

```python
import jsonschema
import yaml

# Load schema
with open("domain-schema.json") as f:
    schema = json.load(f)

# Load domain YAML
with open("software-engineering.yaml") as f:
    domain = yaml.safe_load(f)

# Validate
jsonschema.validate(domain, schema)
```

### JavaScript (ajv)

```javascript
import Ajv from "ajv";
import addFormats from "ajv-formats";

const ajv = new Ajv({ allErrors: true });
addFormats(ajv);

const validate = ajv.compile(schema);
const valid = validate(domain);
if (!valid) console.log(validate.errors);
```

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-29 | ps-researcher (v2.0.0) | Initial research document via proper skill invocation |

---

## Metadata

```yaml
id: "EN-014-e-164"
type: research
agent: ps-researcher
version: "2.0.0"
topic: "Schema Extensibility Patterns for Domain Context"
status: COMPLETE
created_at: "2026-01-29T00:00:00Z"
framework: 5W2H
sources_count: 9
research_questions: 5
gaps_addressed: 4
recommendation: "JSON Schema Extension v1.1.0"
next_task: "TASK-165 (Gap Impact Analysis)"
```
