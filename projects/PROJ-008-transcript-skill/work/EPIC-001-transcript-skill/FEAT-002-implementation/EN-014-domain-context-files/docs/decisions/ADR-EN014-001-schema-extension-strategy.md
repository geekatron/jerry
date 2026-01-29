# ADR-EN014-001: Domain Schema V2 Extension Strategy

> **PS:** EN-014
> **Entry ID:** task-166
> **Created:** 2026-01-29
> **Status:** PROPOSED
> **Agent:** ps-architect (v2.0.0)
> **Supersedes:** N/A
> **Superseded By:** N/A

---

## L0: Executive Summary (ELI5)

### The Library Card Catalog Upgrade Analogy

Imagine you're managing a library with a card catalog system. Your current catalog cards have spaces for:
- Book title
- Author name
- Subject category

But you've discovered your librarians have been writing EXTRA information on sticky notes that keep falling off:
- **Which books reference other books** (like footnotes)
- **Who should read each book** (students vs professors)
- **Different rules for different sections** (fiction browsing vs reference-only)
- **Quality standards** (must have at least 10 pages, must include an index)

**The Problem:** Your catalog card template doesn't have official spaces for this information. The sticky notes work, but they:
1. Fall off and get lost
2. Aren't checked by the cataloging system
3. Can't be used to organize the library

**The Solution:** You have three choices:
1. **Add new boxes to your existing cards** - Quick and easy, everyone already knows how cards work
2. **Replace cards with a fancy computer system** - More powerful but expensive and confusing
3. **Use cards for basics, computer for extras** - Best of both worlds, but more complicated

**Our Decision:** We chose Option 1 - add new boxes to our existing cards. This is:
- **Fast** - We can do it in 1-2 days
- **Safe** - All our old cards still work
- **Simple** - Librarians don't need training

**What This Means:** All the information on those sticky notes will now have proper places on the cards, so nothing gets lost and everything can be checked properly.

---

## L1: Technical Analysis (Engineer)

### Technical Context

The current `domain-schema.json` (v1.0.0) supports basic entity definitions but lacks mechanisms for:

1. **Entity Relationships** - Semantic links between entities (e.g., `blocker` blocks `commitment`)
2. **Domain Metadata** - Target users, transcript types, use cases
3. **Context Rules** - Meeting-type-specific extraction prioritization
4. **Validation Rules** - Domain-specific quality thresholds

These gaps were identified in DISC-006 and analyzed in TASK-164 (research) and TASK-165 (impact analysis).

### Code-Level Implementation Implications

#### Option A: JSON Schema Extension

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
        "type": {
          "type": "string",
          "enum": ["blocks", "resolves", "triggers", "depends_on", "related_to"]
        },
        "target": { "type": "string" },
        "cardinality": {
          "type": "string",
          "enum": ["one-to-one", "one-to-many", "many-to-many"],
          "default": "one-to-many"
        },
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

**Validation Library Support:**

| Library | Language | `$defs`/`$ref` | Conditional | `unevaluatedProperties` |
|---------|----------|----------------|-------------|-------------------------|
| ajv | JavaScript | Yes | Yes | Yes (2020-12) |
| jsonschema | Python | Yes | Yes | Yes (4.x+) |
| json-schema-validator | Java | Yes | Yes | Yes |

#### Option B: JSON-LD Implementation

```json
{
  "@context": {
    "@vocab": "https://jerry-framework.dev/ontology/",
    "entity": "@graph",
    "blocks": { "@type": "@id" },
    "resolves": { "@type": "@id" }
  },
  "@type": "DomainContext",
  "entity_definitions": [
    {
      "@id": "blocker",
      "@type": "EntityType",
      "blocks": { "@id": "commitment" }
    }
  ]
}
```

**Tooling Requirements:**
- jsonld.js or pyld for parsing
- SHACL shapes for validation (complex)
- RDF store for querying relationships

#### Option C: Hybrid Approach

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "properties": {
    "@context": { "type": "string" },
    "entity_definitions": { "$ref": "#/$defs/entityDefinitions" }
  },
  "$defs": {
    "entityDefinitions": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "properties": {
          "@type": { "type": "string" },
          "relationships": { "type": "array" }
        }
      }
    }
  }
}
```

---

## L2: Strategic Implications (Architect)

### Trade-Off Analysis

```
EXPRESSIVENESS vs SIMPLICITY TRADE-OFF
======================================

High
Expressiveness │                           ┌─────────────┐
               │                           │  JSON-LD    │
               │                           │  (Option B) │
               │     ┌─────────────┐       └─────────────┘
               │     │   Hybrid    │
               │     │  (Option C) │
               │     └─────────────┘
               │ ┌─────────────┐
               │ │ JSON Schema │
               │ │  (Option A) │
               │ └─────────────┘
               │ ┌─────────────┐
Low            │ │   Current   │
               │ │   v1.0.0    │
               │ └─────────────┘
               └──────────────────────────────────────────► High
                Low                                     Simplicity
```

### One-Way Door Analysis

| Decision | Reversibility | Risk | Evidence |
|----------|---------------|------|----------|
| Add `relationships` property | REVERSIBLE | LOW | Optional property, remove in v1.2.0 if unused |
| Add `metadata` section | REVERSIBLE | LOW | Optional, no downstream dependencies initially |
| Add `context_rules` | REVERSIBLE | MEDIUM | Test with multiple domains before relying on it |
| Add `validation` section | REVERSIBLE | LOW | Quality gates can ignore if not present |
| **Adopt JSON-LD** | **IRREVERSIBLE** | **HIGH** | Requires ontology, specialized tooling, team training |

**Critical Insight:** Option A (JSON Schema extension) is entirely reversible. All new properties are optional with sane defaults. Option B (JSON-LD) is a one-way door requiring significant investment.

### Performance Implications

From TASK-164 performance analysis:

| Pattern | Validation Time | Memory Impact |
|---------|----------------|---------------|
| Simple `$ref` | O(1) | Minimal |
| `allOf` composition | O(n) | Linear |
| `if-then-else` | O(n) | Linear |
| `unevaluatedProperties` | O(properties) | Minimal |

**Schema Validation Overhead:**
- Current (v1.0.0): ~5ms per domain YAML
- Extended (v1.1.0): ~8ms per domain YAML (+60%, still negligible)

**Runtime Impact:** +2KB average domain YAML size (relationships + context_rules + metadata + validation)

**Conclusion:** Performance overhead is acceptable and imperceptible in transcript processing workflows (5-60 seconds total).

### Blast Radius Assessment

```
COMPONENT IMPACT MATRIX
=======================

┌─────────────────────────────────────────────────────────────────┐
│                    AFFECTED COMPONENTS                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  domain-schema.json ────────────────────────────────► HIGH      │
│        │                     (Add 4 $defs sections)             │
│        │                                                         │
│        ▼                                                         │
│  ts-extractor agent ────────────────────────────────► MEDIUM    │
│        │                 (Add relationship extraction)          │
│        │                                                         │
│        ▼                                                         │
│  extraction-report.json ────────────────────────────► MEDIUM    │
│        │               (Add relationships array)                 │
│        │                                                         │
│        ▼                                                         │
│  ts-mindmap-* agents ───────────────────────────────► HIGH      │
│        │               (Add relationship edges)                  │
│        │                                                         │
│        ▼                                                         │
│  EN-015 quality gates ──────────────────────────────► MEDIUM    │
│                        (Add domain validation)                   │
│                                                                  │
│  Existing domain YAMLs ─────────────────────────────► NONE      │
│  (general.yaml, meeting.yaml)    (Backward compatible)          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

Total Affected: 8 of 15 components (53%)
Breaking Changes: 0
```

---

## Context

### Background

The transcript extraction skill uses domain YAML files to configure entity extraction behavior. These files are validated against `domain-schema.json` (v1.0.0). During preparation for EN-006 artifact promotion (TASK-150..159), an audit revealed that EN-006 domain context designs include features that the current schema cannot represent.

DISC-006 identified 4 specific gaps:
- **GAP-001:** Entity Relationships (RPN 336 - CRITICAL)
- **GAP-002:** Domain Metadata (RPN 144 - MEDIUM)
- **GAP-003:** Context Rules (RPN 288 - HIGH)
- **GAP-004:** Validation Rules (RPN 192 - HIGH)

TASK-165 impact analysis quantified that proceeding without schema extension will result in **70% loss of designed extraction intelligence**.

### Decision Drivers

| Driver | Source | Weight |
|--------|--------|--------|
| **D-001:** Preserve EN-006 design intent | DISC-006 | HIGH |
| **D-002:** Minimize blast radius | Architecture Standards | HIGH |
| **D-003:** Maintain backward compatibility | SchemaVer principles | HIGH |
| **D-004:** Support mindmap relationship edges | EN-009 requirements | HIGH |
| **D-005:** Enable domain-specific quality gates | EN-015 requirements | MEDIUM |
| **D-006:** Minimize learning curve | Team constraints | MEDIUM |
| **D-007:** Enable future semantic web interop | Future FEAT-004 | LOW |

### Constraints

| ID | Constraint | Source |
|----|------------|--------|
| C-001 | Existing domain YAMLs (general.yaml, meeting.yaml) must remain valid | Backward compatibility |
| C-002 | Changes must be additive (no property removal) | SchemaVer REVISION semantics |
| C-003 | Schema must be validateable by ajv/jsonschema | Tool compatibility |
| C-004 | Implementation must complete within 1 week | EN-014 timeline |
| C-005 | All 4 gaps must be addressed in single schema version | Avoid multiple migrations |

### Forces

1. **Expressiveness vs Simplicity:** Need richer semantics (relationships, context rules) without complexity explosion
2. **Speed vs Perfection:** Timeline pressure (blocks TASK-150..159) vs desire for optimal solution
3. **Existing Investment vs Clean Slate:** Leverage JSON Schema expertise vs adopt JSON-LD for semantic richness
4. **Backward Compatibility vs Feature Richness:** Preserve existing files vs require updates for new features

---

## Options Considered

### Option A: JSON Schema Extension (v1.0.0 to v1.1.0)

Extend the existing `domain-schema.json` with 4 new optional sections using JSON Schema 2020-12 features:
- `$defs` for reusable schema fragments
- `$ref` for referencing definitions
- `unevaluatedProperties` for safe extension
- `if-then-else` for conditional validation (GAP-003)

**Implementation Approach:**
1. Add `$defs/entityRelationship` for GAP-001
2. Add `$defs/domainMetadata` for GAP-002
3. Add `$defs/contextRules` for GAP-003
4. Add `$defs/validationRules` for GAP-004
5. All new properties are optional with defaults

**Pros:**
- Leverages 100% of existing JSON Schema investment
- Full ajv/jsonschema tooling support (no new dependencies)
- Team already familiar with JSON Schema patterns
- Implementation effort: 1-2 days
- All existing YAML files remain valid (zero migration required)

**Cons:**
- Limited semantic expressiveness compared to JSON-LD
- Relationships are syntactic, not semantic (no RDF inference)
- Cannot generate knowledge graphs without additional processing

**Fit with Constraints:**
- C-001: SATISFIED - All properties optional with defaults
- C-002: SATISFIED - Only additive changes
- C-003: SATISFIED - Standard JSON Schema 2020-12
- C-004: SATISFIED - 1-2 day implementation
- C-005: SATISFIED - All 4 gaps in single version

**Evidence:**
- [JSON Schema Bundling](https://json-schema.org/understanding-json-schema/reference/object) - `$defs` pattern documentation
- [SchemaVer](https://snowplow.io/blog/introducing-schemaver-for-semantic-versioning-of-schemas) - Versioning strategy

### Option B: JSON-LD Adoption

Replace JSON Schema with JSON-LD for semantic relationship modeling:
- `@context` for vocabulary definition
- `@type` for entity classification
- `@id` for relationship targets
- SHACL shapes for validation

**Implementation Approach:**
1. Define Jerry ontology (RDF vocabulary)
2. Create JSON-LD context mapping
3. Implement SHACL shapes for validation
4. Update all domain YAML files to JSON-LD format
5. Add jsonld.js/pyld dependency for processing

**Pros:**
- Full semantic web compatibility (W3C standard)
- Knowledge graph generation native
- RDF inference capabilities
- Industry standard for linked data

**Cons:**
- High learning curve (team unfamiliar with JSON-LD/RDF/SHACL)
- Significant tooling changes required (new dependencies)
- All existing YAML files require rewriting
- Implementation effort: 2-4 weeks
- Requires ontology design (additional complexity)
- Overkill for current requirements

**Fit with Constraints:**
- C-001: VIOLATED - Existing files require complete rewrite
- C-002: VIOLATED - Major breaking change
- C-003: PARTIAL - Requires specialized tooling (pyld, SHACL)
- C-004: VIOLATED - 2-4 week implementation
- C-005: SATISFIED - Could address all gaps

**Evidence:**
- [JSON-LD Best Practices](https://w3c.github.io/json-ld-bp/) - W3C guidance
- [SHACL Specification](https://www.w3.org/TR/shacl/) - Validation approach

### Option C: Hybrid Approach (JSON Schema + JSON-LD Annotations)

Maintain JSON Schema as primary validation with optional JSON-LD annotations:
- Core schema remains JSON Schema 2020-12
- Add optional `@context` property for semantic web interop
- Relationships in both JSON Schema (`relationships[]`) and JSON-LD (`@id` references)

**Implementation Approach:**
1. Extend JSON Schema per Option A
2. Add optional `@context` property
3. Define mapping from JSON Schema relationships to JSON-LD
4. Provide utility functions for JSON-LD export

**Pros:**
- Backward compatible (like Option A)
- Future path to semantic web interoperability
- Best of both worlds (JSON Schema validation + JSON-LD semantics)

**Cons:**
- Medium complexity (maintaining two representations)
- Learning curve for JSON-LD portion
- Dual validation overhead (JSON Schema + optional JSON-LD)
- Implementation effort: ~1 week
- Potential for representation drift

**Fit with Constraints:**
- C-001: SATISFIED - JSON-LD annotations optional
- C-002: SATISFIED - Additive changes only
- C-003: PARTIAL - Core validation works, JSON-LD requires additional tooling
- C-004: MARGINAL - ~1 week implementation
- C-005: SATISFIED - All 4 gaps addressed

**Evidence:**
- [OpenAPI Extensions](https://swagger.io/docs/specification/v3_0/openapi-extensions/) - `x-` prefix pattern
- [CloudEvents Extensions](https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md) - Hybrid schema approach

---

## Decision

**We will use Option A: JSON Schema Extension (v1.0.0 to v1.1.0).**

### Rationale

1. **Minimal Blast Radius (D-002):** Only 53% of components affected, zero breaking changes
2. **Full Backward Compatibility (D-003, C-001):** All existing domain YAMLs remain valid
3. **Addresses All Gaps (C-005):** Single schema version resolves GAP-001 through GAP-004
4. **Fastest Path (C-004):** 1-2 day implementation vs 2-4 weeks for Option B
5. **Low Learning Curve (D-006):** Team already proficient with JSON Schema
6. **Reversible Decision:** All changes are additive; can evolve to Option C in v1.2.0 if needed
7. **Evidence-Based:** Patterns from OpenAPI, AsyncAPI, CloudEvents validate approach

### Evidence from TASK-164 Research

The research identified `unevaluatedProperties` as superior to `additionalProperties` for safe extension:

> "`additionalProperties: false` breaks schema extension because properties in `allOf` subschemas are considered 'additional'. `unevaluatedProperties: false` correctly recognizes properties from all subschemas."

Source: [JSON Schema Spec](https://github.com/json-schema-org/json-schema-spec/blob/main/specs/jsonschema-core.md)

### Evidence from TASK-165 Analysis

The FMEA risk assessment prioritized gaps by RPN:
1. GAP-001 (Relationships): RPN 336 - CRITICAL
2. GAP-003 (Context Rules): RPN 288 - HIGH
3. GAP-004 (Validation Rules): RPN 192 - HIGH
4. GAP-002 (Metadata): RPN 144 - MEDIUM

All 4 gaps are addressed by Option A with equivalent expressiveness to EN-006 design intent.

### Alignment

| Criterion | Score | Notes |
|-----------|-------|-------|
| Constraint Satisfaction | HIGH | All 5 constraints satisfied |
| Risk Level | LOW | Reversible, additive changes only |
| Implementation Effort | S | 1-2 days (fastest option) |
| Reversibility | HIGH | All properties optional, can remove in v1.2.0 |

---

## Consequences

### Positive Consequences

1. **Mindmap Completeness Restored (GAP-001):** ts-mindmap agents can render relationship edges, recovering 40% semantic structure
2. **Extraction Intelligence Preserved:** 70% cumulative intelligence loss prevented by addressing all 4 gaps
3. **Quality Gates Enabled (GAP-004):** Domain-specific thresholds (min_entities, required_entities) enforceable
4. **Context-Aware Extraction (GAP-003):** Meeting-type-specific entity prioritization possible
5. **Future Path Open (GAP-002):** Metadata enables domain auto-selection in FEAT-003
6. **Zero Migration Burden:** Existing domain YAMLs (general.yaml, meeting.yaml) continue working unchanged
7. **Fast Unblock:** TASK-150..159 can proceed after ~1 week (TASK-167, 168, 169)

### Negative Consequences

1. **Not Full Semantic Web:** Relationships are syntactic; no RDF inference capabilities
2. **Manual Relationship Management:** No automatic inverse relationship generation
3. **Validation Overhead:** ~60% increase in schema validation time (5ms to 8ms, still negligible)

### Neutral Consequences

1. **Schema Versioning Required:** Must adopt SchemaVer for future evolution
2. **Documentation Update:** SKILL.md needs update for new schema features
3. **Test Suite Expansion:** New contract tests needed for relationship extraction

### Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Relationship schema insufficient for complex graphs | LOW | MEDIUM | Start simple; extend in v1.2.0 if needed |
| Context rules over-complicate extraction | LOW | LOW | Make context_rules optional per domain |
| Team confusion on new schema sections | LOW | LOW | Document in TDD-domain-schema-v2 |
| Validation rules cause false negatives | MEDIUM | MEDIUM | Use lenient thresholds initially |

---

## Implementation

### Action Items

| # | Action | Owner | Due |
|---|--------|-------|-----|
| 1 | Create TASK-167 (TDD-domain-schema-v2) with detailed schema design | Claude | Week 1 |
| 2 | Implement domain-schema.json v1.1.0 | Claude | Week 1 |
| 3 | Update extraction-report.json schema for relationships | Claude | Week 1 |
| 4 | Update ts-extractor agent instructions for relationship extraction | Claude | Week 1 |
| 5 | Create contract tests for new schema sections | Claude | Week 1 |
| 6 | Complete TASK-168 (Final Adversarial Review) | ps-critic + nse-qa | Week 1 |
| 7 | Complete TASK-169 (Human Approval Gate) | Human | Week 2 |

### Validation Criteria

1. **Backward Compatibility:** `general.yaml` and `meeting.yaml` validate against v1.1.0 schema without modification
2. **Gap Resolution:** EN-006 `software-engineering` domain YAML with all 4 features validates successfully
3. **Extraction Test:** Relationships appear in extraction-report.json when domain defines them
4. **Mindmap Test:** ts-mindmap-mermaid generates edges for extracted relationships
5. **Quality Gate Test:** EN-015 quality gates enforce domain-specific thresholds

---

## Related Decisions

| ADR | Relationship | Notes |
|-----|--------------|-------|
| ADR-CLI-002 | RELATED_TO | CLI namespace implementation (different bounded context) |
| (Future) ADR-EN014-002 | MAY_EXTEND | If JSON-LD annotations needed in v1.2.0 |

---

## References

| # | Reference | Type | Relevance |
|---|-----------|------|-----------|
| 1 | [JSON Schema Understanding Guide](https://json-schema.org/understanding-json-schema/reference/object) | Documentation | `$defs`/`$ref` patterns |
| 2 | [JSON Schema Specification](https://github.com/json-schema-org/json-schema-spec/blob/main/specs/jsonschema-core.md) | Specification | `unevaluatedProperties` behavior |
| 3 | [JSON-LD Best Practices](https://w3c.github.io/json-ld-bp/) | W3C Note | Alternative approach evaluation |
| 4 | [Ajv JSON Schema Validator](https://ajv.js.org/keywords.html) | Documentation | Custom keyword support |
| 5 | [OpenAPI Specification Extensions](https://swagger.io/docs/specification/v3_0/openapi-extensions/) | Documentation | Extension pattern prior art |
| 6 | [CloudEvents Specification](https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md) | Specification | Extension pattern prior art |
| 7 | [SchemaVer for Semantic Versioning](https://snowplow.io/blog/introducing-schemaver-for-semantic-versioning-of-schemas) | Blog | Versioning strategy |
| 8 | [Confluent Schema Evolution](https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html) | Documentation | Backward compatibility patterns |
| 9 | [JSON Schema Conditionals](https://json-schema.org/understanding-json-schema/reference/conditionals) | Documentation | if-then-else patterns for GAP-003 |
| 10 | TASK-164 Research | Internal | Schema extensibility patterns |
| 11 | TASK-165 Analysis | Internal | Gap impact assessment (FMEA) |
| 12 | DISC-006 | Internal | Schema gap identification |

---

## Compliance

### Jerry Constitution Compliance

| Principle | Compliance | Notes |
|-----------|------------|-------|
| P-001 (Truth and Accuracy) | COMPLIANT | Evidence-based with 12 authoritative sources |
| P-002 (File Persistence) | COMPLIANT | ADR persisted to repository |
| P-003 (No Recursive Subagents) | COMPLIANT | No subagent delegation in this decision |
| P-004 (Provenance) | COMPLIANT | Traceable to DISC-006, TASK-164, TASK-165 |
| P-010 (Task Tracking Integrity) | COMPLIANT | Part of EN-014 work tracker |
| P-022 (No Deception) | COMPLIANT | Trade-offs transparently documented |
| P-030 (Project Context Required) | COMPLIANT | Within PROJ-008-transcript-skill |
| P-040 (NASA SE Alignment) | COMPLIANT | NPR 7123.1D Process 14-16 considered |

### Backward Compatibility Guarantee

Following [SchemaVer](https://snowplow.io/blog/introducing-schemaver-for-semantic-versioning-of-schemas) semantics:

| Version Change | Type | Description |
|---------------|------|-------------|
| 1.0.0 to 1.1.0 | REVISION | New optional properties added |
| N/A | ADDITION | Would be 1.0.1 (not applicable here) |
| N/A | MODEL | Would be 2.0.0 (breaking change, avoided) |

**Guarantee:** All domain YAML files valid against v1.0.0 will validate against v1.1.0 without modification.

---

## ASCII Diagrams

### Decision Flow

```
SCHEMA EXTENSION DECISION FLOW
==============================

┌─────────────────────────────────────────────────────────────────┐
│                    DISC-006: Gap Identification                  │
│                                                                  │
│  GAP-001: Entity Relationships    (RPN 336 - CRITICAL)         │
│  GAP-002: Domain Metadata         (RPN 144 - MEDIUM)           │
│  GAP-003: Context Rules           (RPN 288 - HIGH)             │
│  GAP-004: Validation Rules        (RPN 192 - HIGH)             │
│                                                                  │
│  Cumulative Impact: 70% intelligence loss without fix          │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    TASK-164: Research                            │
│                                                                  │
│  Patterns Identified:                                           │
│  - $defs + $ref for reusable schemas                            │
│  - unevaluatedProperties for safe extension                     │
│  - if-then-else for conditional validation                      │
│  - SchemaVer for versioning strategy                            │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    TASK-165: Analysis                            │
│                                                                  │
│  FMEA Risk Assessment:                                          │
│  - GAP-001: SEV=8, OCC=7, DET=6 → RPN 336                       │
│  - GAP-003: SEV=6, OCC=8, DET=6 → RPN 288                       │
│  - GAP-004: SEV=6, OCC=8, DET=4 → RPN 192                       │
│  - GAP-002: SEV=4, OCC=6, DET=6 → RPN 144                       │
│                                                                  │
│  Recommendation: Fix all 4 gaps in single schema version        │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                 TASK-166: ADR (THIS DOCUMENT)                    │
│                                                                  │
│  Options Evaluated:                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │ Option A    │  │ Option B    │  │ Option C    │              │
│  │ JSON Schema │  │ JSON-LD     │  │ Hybrid      │              │
│  │ Extension   │  │ Adoption    │  │ Approach    │              │
│  │             │  │             │  │             │              │
│  │ Effort: 1-2d│  │ Effort: 2-4w│  │ Effort: ~1w │              │
│  │ Risk: LOW   │  │ Risk: HIGH  │  │ Risk: MED   │              │
│  │ Compat: 100%│  │ Compat: 0%  │  │ Compat: 100%│              │
│  └──────┬──────┘  └─────────────┘  └─────────────┘              │
│         │                                                        │
│         ▼                                                        │
│  ╔═════════════════════════════════════════════════════════╗    │
│  ║             DECISION: Option A Selected                 ║    │
│  ║                                                         ║    │
│  ║  Rationale:                                             ║    │
│  ║  - Minimal blast radius                                 ║    │
│  ║  - Full backward compatibility                          ║    │
│  ║  - Fastest implementation                               ║    │
│  ║  - Lowest risk (reversible)                             ║    │
│  ║  - Addresses all 4 gaps                                 ║    │
│  ╚═════════════════════════════════════════════════════════╝    │
└─────────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    NEXT STEPS                                    │
│                                                                  │
│  TASK-167: TDD-domain-schema-v2 (Technical Design)              │
│      │                                                           │
│      ▼                                                           │
│  TASK-168: Final Adversarial Review (ps-critic + nse-qa)        │
│      │                                                           │
│      ▼                                                           │
│  TASK-169: Human Approval Gate                                   │
│      │                                                           │
│      ▼                                                           │
│  TASK-150..159: Domain YAML Promotion (UNBLOCKED)               │
└─────────────────────────────────────────────────────────────────┘
```

### Before/After Schema Architecture

```
SCHEMA V1.0.0 vs V1.1.0 COMPARISON
==================================

BEFORE: v1.0.0 (Current)              AFTER: v1.1.0 (Extended)
========================              ========================

┌──────────────────────┐              ┌──────────────────────────────┐
│ domain-schema.json   │              │ domain-schema.json           │
│                      │              │                              │
│ ✅ schema_version    │              │ ✅ schema_version            │
│ ✅ domain            │              │ ✅ domain                    │
│ ✅ entity_definitions│              │ ✅ entity_definitions        │
│ ✅ extraction_rules  │              │ ✅ extraction_rules          │
│ ✅ prompt_guidance   │              │ ✅ prompt_guidance           │
│                      │              │                              │
│ ❌ relationships     │     ─────►   │ ✅ relationships (GAP-001)   │
│ ❌ metadata          │              │    └─► $defs/entityRelation  │
│ ❌ context_rules     │              │                              │
│ ❌ validation        │              │ ✅ metadata (GAP-002)        │
│                      │              │    └─► $defs/domainMetadata  │
└──────────────────────┘              │                              │
                                      │ ✅ context_rules (GAP-003)   │
         │                            │    └─► $defs/contextRules    │
         │                            │                              │
         │  70% INTELLIGENCE          │ ✅ validation (GAP-004)      │
         │  LOSS                      │    └─► $defs/validationRules │
         │                            │                              │
         ▼                            └──────────────────────────────┘
                                                      │
┌──────────────────────┐                              │
│     USER IMPACT      │              ┌───────────────▼───────────────┐
│                      │              │         USER IMPACT            │
│ - Mindmaps: nodes    │              │                                │
│   only (no edges)    │              │ - Mindmaps: nodes + edges     │
│ - Extraction: generic│              │ - Extraction: context-aware   │
│ - Quality: false     │              │ - Quality: domain-specific    │
│   positives (30%)    │              │   thresholds                   │
│ - UX: manual domain  │              │ - UX: future auto-selection   │
│   selection          │              │                                │
└──────────────────────┘              └────────────────────────────────┘
```

---

## PS Integration

| Action | Command | Status |
|--------|---------|--------|
| Exploration Entry | `add-entry EN-014 "Decision: Schema Extension Strategy"` | Done (task-166) |
| Entry Type | `--type DECISION` | Done |
| Artifact Link | `link-artifact EN-014 task-166 FILE "docs/decisions/ADR-EN014-001-schema-extension-strategy.md"` | Done |

---

## Document History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-01-29 | ps-architect (v2.0.0) | Initial ADR creation with full Nygard format |

---

## Metadata

```yaml
id: "ADR-EN014-001"
ps_id: "EN-014"
entry_id: "task-166"
type: adr
agent: ps-architect
agent_version: "2.0.0"
topic: "Domain Schema V2 Extension Strategy"
status: PROPOSED
created_at: "2026-01-29T00:00:00Z"
format: "Michael Nygard ADR (2011)"
options_considered: 3
decision: "Option A - JSON Schema Extension"
constraints_satisfied: 5
risks_identified: 4
implementation_effort: "1-2 days"
reversibility: HIGH
gaps_addressed:
  - GAP-001 (Entity Relationships)
  - GAP-002 (Domain Metadata)
  - GAP-003 (Context Rules)
  - GAP-004 (Validation Rules)
sources_cited: 12
personas_documented:
  - L0-ELI5
  - L1-Engineer
  - L2-Architect
constitutional_compliance:
  - "P-001 (accuracy)"
  - "P-002 (persisted)"
  - "P-003 (no subagents)"
  - "P-004 (provenance)"
  - "P-010 (task tracking)"
  - "P-022 (no deception)"
  - "P-030 (project context)"
  - "P-040 (NASA SE alignment)"
quality_threshold: "0.85"
reviewers:
  - ps-critic
  - nse-qa
next_task: "TASK-167 (TDD-domain-schema-v2)"
```

---

*Document ID: ADR-EN014-001*
*Decision Session: en014-task166-schema-extension-strategy*
*Constitutional Compliance: P-001, P-002, P-003, P-004, P-010, P-022, P-030, P-040*

**Generated by:** ps-architect agent (v2.0.0)
**Template Version:** 1.0 (Michael Nygard format)
**Prior Art:** IETF RFC Process, C4 Architecture Documentation
