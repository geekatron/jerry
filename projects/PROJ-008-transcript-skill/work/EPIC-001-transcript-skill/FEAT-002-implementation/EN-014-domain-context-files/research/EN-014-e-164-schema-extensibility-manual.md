# EN-014-e-164: Research - Schema Extensibility Patterns

<!--
TEMPLATE: Research
VERSION: 1.0.0
SOURCE: docs/knowledge/exemplars/templates/research.md
TASK: TASK-164
ENABLER: EN-014 (Domain Context Files Implementation)
-->

---

## Frontmatter

```yaml
id: "EN-014-e-164"
type: "research"
title: "Schema Extensibility Patterns for Domain Context Files"
task_id: "TASK-164"
parent_id: "EN-014"
status: "COMPLETE"
created_at: "2026-01-29T00:00:00Z"
updated_at: "2026-01-29T00:00:00Z"
author: "Claude"
reviewers:
  - "ps-critic"
  - "nse-qa"
quality_threshold: 0.85
```

---

## L0: Executive Summary (ELI5)

### The Problem in Simple Terms

Imagine you have a recipe book (our domain schema) that tells you how to make different dishes. Right now, the recipe book can list ingredients and steps, but it can't tell you:
- Which ingredients go well together (relationships)
- Who the recipe is for - beginners or experts (metadata)
- Special rules for holiday cooking vs. everyday meals (context rules)
- How to check if you have all the required ingredients (validation)

We need to add these new pages to our recipe book without throwing away all the existing recipes.

### What We Found

We looked at how other big kitchens (industry standards) solved this problem:

1. **Add sticky notes to existing recipes** (JSON Schema extensions) - Easiest, works with what we have
2. **Use a completely new recipe format** (JSON-LD) - Very powerful, but means rewriting everything
3. **Add a special cover page with instructions** (Envelope pattern) - Good compromise

### The Recommendation

**Keep using JSON Schema but add custom keywords** - like adding sticky notes to our existing recipe book. This approach:
- Doesn't require rewriting existing recipes (low blast radius)
- Works with standard recipe readers (validators like ajv)
- Can be upgraded later if needed

---

## L1: Technical Analysis (Software Engineer)

### Problem Statement

The current domain schema (`domain-schema.json`) supports basic entity definitions and extraction rules but lacks four critical capabilities identified in [DISC-006](../EN-014--DISC-006-schema-gap-analysis.md):

| Gap ID | Capability | Current State | Required State |
|--------|------------|---------------|----------------|
| GAP-001 | Entity Relationships | Not supported | `blocks`, `resolves`, `triggers` links |
| GAP-002 | Domain Metadata | Not supported | `target_users`, `transcript_types`, `key_use_cases` |
| GAP-003 | Context Rules | Not supported | Meeting-type-specific extraction priorities |
| GAP-004 | Validation Rules | Not supported | `min_entities`, `required_entities` constraints |

### Research Questions Addressed

#### RQ-1: What patterns exist for representing entity relationships in JSON Schema?

**Findings:**

JSON Schema natively supports structural relationships via:
- `$ref` / `$defs` for schema composition
- `allOf`, `oneOf`, `anyOf` for schema combination
- `properties` with nested object definitions

However, **semantic relationships** (like "entity A blocks entity B") are NOT a native JSON Schema concern. Three patterns emerge:

| Pattern | Approach | Example |
|---------|----------|---------|
| **Embedded Object** | Define relationship as property | `"relationships": [{"type": "blocks", "target": "blocker"}]` |
| **Custom Keyword** | Extend JSON Schema vocabulary | `"x-relationships": {...}` |
| **External Linkage** | JSON-LD `@context` mapping | `"@context": {"blocks": "http://schema.org/isBlockedBy"}` |

**Industry Evidence:**
- OpenAPI 3.1 uses embedded objects for link relationships ([OpenAPI Spec](https://spec.openapis.org/oas/latest.html))
- CloudEvents uses extension attributes with `ext-` prefix ([CloudEvents Spec](https://cloudevents.io/))
- AsyncAPI uses custom `x-` extensions for non-standard properties ([AsyncAPI Spec](https://www.asyncapi.com/docs/reference/specification/v3.0.0))

#### RQ-2: How do industry standards (JSON-LD, OWL, GraphQL) model entity relationships?

**JSON-LD Approach:**

JSON-LD provides semantic relationships through IRIs (Internationalized Resource Identifiers):

```json
{
  "@context": {
    "blocks": "http://example.org/transcript#blocks",
    "commitment": "http://example.org/transcript#Commitment"
  },
  "@type": "commitment",
  "blocks": {"@id": "#blocker-001"}
}
```

**Pros:**
- Rich semantic expressiveness
- Interoperable with RDF/Linked Data ecosystem
- Self-describing documents

**Cons:**
- Significant learning curve
- Requires `@context` management
- Validation complexity (JSON-LD + JSON Schema dual validation)
- **HIGH blast radius** - fundamentally different paradigm

**GraphQL Approach:**

GraphQL uses typed fields for relationships:

```graphql
type Commitment {
  blockedBy: [Blocker!]
  triggers: [ActionItem!]
}
```

**Pros:**
- Strong typing
- Query-driven relationship traversal
- Excellent tooling

**Cons:**
- Requires GraphQL server infrastructure
- Not applicable to static schema definitions
- **VERY HIGH blast radius** - completely different technology stack

#### RQ-3: What extensibility patterns ($ref, $defs, additionalProperties) are recommended?

**JSON Schema Draft 2020-12 Extensibility Mechanisms:**

| Mechanism | Purpose | Validation Impact | Recommendation |
|-----------|---------|-------------------|----------------|
| `$vocabulary` | Declare custom vocabularies | Requires validator support | For formal standards only |
| Custom keywords (`x-*`) | Add metadata without validation | None (ignored by validators) | **RECOMMENDED** for metadata |
| `$defs` / `$ref` | Reusable schema components | Full validation | **RECOMMENDED** for composition |
| `additionalProperties` | Control object extensibility | Affects validation | Use carefully for compatibility |

**Ajv Custom Keywords (Most Practical):**

From [Ajv Documentation](https://ajv.js.org/keywords.html), custom keywords can be defined at 4 levels:

1. **Safe Code Generation** - Highest security, optimized
2. **Validate Function** - Simple validation logic
3. **Compile Function** - Complex conditional validation
4. **Macro Function** - Schema transformation

```javascript
// Example: Custom 'x-relationships' keyword
ajv.addKeyword({
  keyword: 'x-relationships',
  type: 'object',
  schemaType: 'array',
  validate: function(schema, data) {
    // Validate relationships against entity definitions
    return schema.every(rel =>
      data.entity_definitions.hasOwnProperty(rel.target)
    );
  }
});
```

#### RQ-4: How can context-aware validation rules be expressed in JSON Schema?

**Conditional Validation with `if`/`then`/`else`:**

JSON Schema 2020-12 supports conditional schemas:

```json
{
  "if": {
    "properties": {
      "context_type": {"const": "standup"}
    }
  },
  "then": {
    "properties": {
      "extraction_rules": {
        "required": ["commitment", "blocker"]
      }
    }
  }
}
```

**Custom Validation Keywords:**

For complex validation (e.g., `min_entities`, `required_entities`), custom keywords provide cleaner expression:

```json
{
  "x-validation": {
    "min_entities": 4,
    "required_entities": ["commitment", "blocker", "action_item"],
    "context_rules": {
      "standup": {
        "primary": ["commitment", "blocker"],
        "secondary": ["action_item"]
      }
    }
  }
}
```

#### RQ-5: What backward compatibility strategies minimize breaking changes?

**Key Findings from Research:**

From [JSON Schema Compatibility Guide](https://yokota.blog/2025/10/07/json-schema-compatibility-and-the-robustness-principle/):

| Compatibility Type | Definition | Strategy |
|--------------------|------------|----------|
| **Backward** | New schema reads old data | Add optional properties only |
| **Forward** | Old schema reads new data | Use `additionalProperties: true` |
| **Full** | Both directions | Difficult with JSON Schema |

**Best Practices from [Creek Service](https://www.creekservice.org/articles/2024/01/08/json-schema-evolution-part-1.html):**

1. **Never remove required fields** - Breaks backward compatibility
2. **Add optional fields with defaults** - Safe for backward compatibility
3. **Use additionalProperties carefully** - `true` = forward compatible, `false` = closed model
4. **Version the schema** - `schema_version` field for migration logic

**JSON Schema Future Direction:**

From [JSON Schema Blog](https://json-schema.org/blog/posts/future-of-json-schema):
> "The next release will be a long-lived version that is stable, but evolving. Strict backward and forward compatibility requirements must be followed for any change."

### Approach Comparison Matrix

| Criterion | JSON Schema + Custom Keywords | JSON-LD | GraphQL |
|-----------|-------------------------------|---------|---------|
| **Blast Radius** | LOW | HIGH | VERY HIGH |
| **Learning Curve** | Low (familiar syntax) | High (RDF concepts) | High (new paradigm) |
| **Tooling Support** | Excellent (ajv, jsonschema) | Moderate | Excellent (but different) |
| **Validation** | Native + custom | Complex (dual) | Different mechanism |
| **Migration Effort** | Hours | Days-Weeks | Weeks-Months |
| **Semantic Richness** | Moderate | Excellent | Good |
| **Industry Adoption** | Very High | Moderate | High |

---

## L2: Architectural Analysis (Principal Architect)

### 5W2H Analysis

| Question | Answer |
|----------|--------|
| **What** | Extend domain schema to support relationships, metadata, context rules, validation |
| **Why** | EN-006 design artifacts require capabilities not in current schema |
| **Who** | Transcript skill extractor agent, domain file authors |
| **Where** | `domain-schema.json`, individual domain YAML files |
| **When** | During EN-014 implementation, before TASK-150..159 |
| **How** | JSON Schema custom keywords + structured properties |
| **How Much** | Low effort (hours), low risk, high compatibility |

### Ishikawa (Fishbone) Analysis

```
                                   SCHEMA EXTENSIBILITY CHALLENGE
                                              │
    ┌──────────────┬──────────────┬──────────────┬──────────────┬──────────────┐
    │              │              │              │              │              │
    ▼              ▼              ▼              ▼              ▼              ▼
 METHODS       MACHINES       MATERIALS      MANPOWER       METRICS      ENVIRONMENT
    │              │              │              │              │              │
    ├─ JSON-LD     ├─ Validators  ├─ Existing    ├─ Learning   ├─ Validation ├─ Existing
    │  paradigm    │  (ajv)       │  schemas     │  curve      │  coverage   │  investment
    │  shift       │              │              │              │             │
    ├─ Custom      ├─ Language    ├─ EN-006      ├─ Team       ├─ Migration  ├─ Claude Code
    │  keywords    │  parsers     │  artifacts   │  familiarity│  time       │  ecosystem
    │              │              │              │              │             │
    └─ Envelope    └─ CI/CD       └─ Test data   └─ Support    └─ Blast      └─ Skill
       pattern        tools                         resources    radius        architecture
```

**Root Cause Analysis:**

The primary constraint is **existing JSON Schema investment**. The current schema:
- Uses JSON Schema Draft 2020-12
- Has 131+ lines of definitions
- Is integrated with transcript skill agents
- Has test data aligned to current structure

Changing to JSON-LD or GraphQL would require:
- Rewriting all schema files
- Updating all YAML domain files
- Modifying extractor agent logic
- Updating validation tests
- Retraining team on new paradigm

### FMEA (Failure Mode and Effects Analysis)

| Failure Mode | Effect | Severity (1-10) | Occurrence (1-10) | Detection (1-10) | RPN | Mitigation |
|--------------|--------|-----------------|-------------------|------------------|-----|------------|
| Custom keywords not validated | Invalid relationships accepted | 7 | 4 | 3 | 84 | Implement ajv custom keyword validation |
| Backward incompatibility | Existing domain files break | 9 | 3 | 2 | 54 | Schema versioning with migration |
| Validator doesn't support extensions | Runtime validation fails | 8 | 2 | 2 | 32 | Test with ajv-keywords library |
| JSON-LD migration delays project | Schedule overrun | 6 | 7 | 4 | 168 | **REJECT** JSON-LD approach |
| Custom keywords become technical debt | Long-term maintenance burden | 5 | 5 | 6 | 150 | Document clearly, plan for JSON Schema evolution |

**FMEA Decision:** Highest RPN (168) is JSON-LD migration risk. Avoid this failure mode by choosing JSON Schema extension approach.

### Pareto Analysis (80/20)

**20% of changes that deliver 80% of value:**

1. **Add `x-relationships` keyword** → Enables GAP-001 (entity relationships)
2. **Add `metadata` property** → Enables GAP-002 (domain metadata)
3. **Add `context_rules` property** → Enables GAP-003 (context-aware extraction)
4. **Add `x-validation` keyword** → Enables GAP-004 (validation rules)

These 4 additions address ALL identified gaps without schema paradigm change.

### Trade-off Analysis

```
                    HIGH SEMANTIC RICHNESS
                            │
                     JSON-LD │
                       ●     │
                            │
                            │
     ────────────────────────┼────────────────────────────
     HIGH BLAST              │              LOW BLAST
     RADIUS                  │              RADIUS
                            │
                            │      JSON Schema +
                            │      Custom Keywords
                            │           ●
                            │
                    LOW SEMANTIC RICHNESS
```

**Decision Point:** The transcript skill does not require RDF-level semantic interoperability. The relationships (`blocks`, `resolves`, `triggers`) are domain-specific and do not need external ontology mapping.

### One-Way Door Analysis

| Decision | Reversibility | Door Type |
|----------|---------------|-----------|
| Add custom keywords to JSON Schema | Easy to remove or modify | Two-way |
| Adopt JSON-LD as primary format | Difficult, requires full migration | **One-way** |
| Add new optional properties | Easy to remove | Two-way |
| Remove required properties | Breaks backward compat | One-way |

**Recommendation:** All proposed changes are **two-way doors** - we can iterate and adjust without significant rework.

---

## Problem-Solving Framework Application

### 8D Report Summary

| Discipline | Content |
|------------|---------|
| **D1: Team** | Claude (researcher), ps-critic, nse-qa |
| **D2: Problem** | Domain schema lacks 4 capabilities required by EN-006 |
| **D3: Containment** | N/A - no production impact yet |
| **D4: Root Cause** | JSON Schema standard doesn't natively support semantic relationships |
| **D5: Corrective Actions** | Extend schema with custom keywords + properties |
| **D6: Validation** | ajv custom keyword tests, schema migration tests |
| **D7: Prevention** | Document extension patterns, create migration guide |
| **D8: Team Recognition** | N/A |

### NASA SE Alignment

Per NPR 7123.1D:

| SE Process | Application |
|------------|-------------|
| **Requirements Analysis** | 4 gaps traced to EN-006 requirements |
| **Technical Planning** | TASK-164..169 workflow established |
| **Design Solution** | JSON Schema extension approach selected |
| **Verification** | ps-critic + nse-qa dual review |
| **Technical Assessment** | Trade study documented with evidence |
| **Technical Decision** | ADR to be created in TASK-166 |

---

## Recommendations

### Primary Recommendation

**Extend JSON Schema with custom keywords and structured properties.**

| Gap | Solution | Implementation |
|-----|----------|----------------|
| GAP-001 | `x-relationships` keyword | Custom ajv keyword for relationship validation |
| GAP-002 | `metadata` property | Standard JSON Schema property with nested object |
| GAP-003 | `context_rules` property | Standard JSON Schema property with conditional logic |
| GAP-004 | `x-validation` keyword | Custom ajv keyword for entity-level validation |

### Schema Extension Example

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "domain-schema-v2",
  "type": "object",
  "properties": {
    "schema_version": {"const": "2.0.0"},
    "metadata": {
      "type": "object",
      "properties": {
        "target_users": {"type": "array", "items": {"type": "string"}},
        "transcript_types": {"type": "array", "items": {"type": "string"}},
        "key_use_cases": {"type": "array", "items": {"type": "string"}}
      }
    },
    "entity_definitions": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "properties": {
          "x-relationships": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "type": {"enum": ["blocks", "resolves", "triggers", "related_to"]},
                "target": {"type": "string"}
              }
            }
          }
        }
      }
    },
    "context_rules": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "properties": {
          "primary_entities": {"type": "array", "items": {"type": "string"}},
          "secondary_entities": {"type": "array", "items": {"type": "string"}}
        }
      }
    },
    "x-validation": {
      "type": "object",
      "properties": {
        "min_entities": {"type": "integer", "minimum": 0},
        "required_entities": {"type": "array", "items": {"type": "string"}}
      }
    }
  }
}
```

### Migration Strategy

1. **Version bump**: `schema_version: "1.0.0"` → `"2.0.0"`
2. **Optional properties**: All new fields optional for backward compatibility
3. **Default values**: Empty arrays/objects for missing fields
4. **Validator upgrade**: Add ajv custom keywords
5. **Test coverage**: Contract tests for both v1 and v2 schemas

### Alternative Considered but Not Recommended

**JSON-LD Adoption**

While JSON-LD provides superior semantic expressiveness, it is **not recommended** due to:

1. **HIGH blast radius** - Requires rewriting all schema infrastructure
2. **Dual validation complexity** - JSON-LD + JSON Schema
3. **Learning curve** - RDF/Linked Data concepts unfamiliar to team
4. **Overkill** - Transcript skill doesn't require external ontology interop
5. **Schedule risk** - Estimated 2-3 weeks additional development

---

## Evidence and Citations

### Authoritative Sources

1. **JSON Schema Core 2020-12** - [https://json-schema.org/draft/2020-12/json-schema-core](https://json-schema.org/draft/2020-12/json-schema-core)
   - Official specification for JSON Schema extensibility

2. **Ajv JSON Schema Validator - Custom Keywords** - [https://ajv.js.org/keywords.html](https://ajv.js.org/keywords.html)
   - Industry-standard validator extension patterns

3. **JSON-LD Best Practices (W3C)** - [https://w3c.github.io/json-ld-bp/](https://w3c.github.io/json-ld-bp/)
   - W3C community guidance on JSON-LD adoption

4. **JSON Schema Compatibility and Robustness Principle** - [https://yokota.blog/2025/10/07/json-schema-compatibility-and-the-robustness-principle/](https://yokota.blog/2025/10/07/json-schema-compatibility-and-the-robustness-principle/)
   - Expert analysis on backward/forward compatibility

5. **Creek Service: Evolving JSON Schemas** - [https://www.creekservice.org/articles/2024/01/08/json-schema-evolution-part-1.html](https://www.creekservice.org/articles/2024/01/08/json-schema-evolution-part-1.html)
   - Practical schema evolution strategies

6. **Towards a Stable JSON Schema** - [https://json-schema.org/blog/posts/future-of-json-schema](https://json-schema.org/blog/posts/future-of-json-schema)
   - JSON Schema organization's compatibility direction

7. **AsyncAPI and CloudEvents Extension Patterns** - [https://www.asyncapi.com/blog/asyncapi-cloud-events](https://www.asyncapi.com/blog/asyncapi-cloud-events)
   - Industry standard extension attribute patterns

### Internal References

- [EN-014--DISC-006: Schema Gap Analysis](../EN-014--DISC-006-schema-gap-analysis.md)
- [EN-006 entity-definitions.yaml](../../EN-006-context-injection/entity-definitions.yaml)
- [EN-006 extraction-rules.yaml](../../EN-006-context-injection/extraction-rules.yaml)
- [domain-schema.json](../../../../skills/transcript/contexts/schemas/domain-schema.json)

---

## Quality Gates

| Reviewer | Target | Focus |
|----------|--------|-------|
| ps-critic | ≥ 0.85 | Research rigor, citation quality, completeness |
| nse-qa | ≥ 0.85 | NASA SE compliance, traceability, process rigor |

---

## Appendix A: Glossary

| Term | Definition |
|------|------------|
| **Blast Radius** | Scope of impact when making a technology change |
| **Custom Keyword** | User-defined JSON Schema keyword extending standard vocabulary |
| **IRI** | Internationalized Resource Identifier (JSON-LD) |
| **RPN** | Risk Priority Number (Severity × Occurrence × Detection) |
| **Schema Vocabulary** | Set of keywords recognized by a JSON Schema validator |

---

## Appendix B: Research Log

| Timestamp | Activity | Source |
|-----------|----------|--------|
| 2026-01-29 | Context7 JSON Schema lookup | context7.io |
| 2026-01-29 | Web search: JSON Schema 2020-12 patterns | Various |
| 2026-01-29 | Web search: JSON-LD vs JSON Schema | Various |
| 2026-01-29 | Web search: OpenAPI/AsyncAPI patterns | Various |
| 2026-01-29 | Web search: Backward compatibility | Various |
| 2026-01-29 | Web search: Ajv custom keywords | ajv.js.org |

---

*Research completed: 2026-01-29*
*Author: Claude*
*Task: TASK-164*
*Enabler: EN-014*
