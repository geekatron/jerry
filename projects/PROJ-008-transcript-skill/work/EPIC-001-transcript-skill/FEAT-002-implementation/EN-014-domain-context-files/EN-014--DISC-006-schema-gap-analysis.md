# EN-014:DISC-006: Schema Gap Analysis - EN-006 Features vs domain-schema.json

<!--
TEMPLATE: Discovery
VERSION: 1.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9, worktracker.md (Discovery File)
CREATED: 2026-01-29 (EN-014 Schema Extension Workflow)
PURPOSE: Document schema gaps between EN-006 domain context artifacts and current domain-schema.json
TRIGGER: Audit of EN-006 artifacts revealed features not supported by current schema
-->

> **Type:** discovery
> **Status:** DOCUMENTED
> **Priority:** HIGH
> **Impact:** HIGH
> **Created:** 2026-01-29T00:00:00Z
> **Completed:** 2026-01-29T00:00:00Z
> **Parent:** EN-014
> **Owner:** Claude
> **Source:** EN-006 artifact audit during TASK-150..159 preparation

---

## Frontmatter

```yaml
id: "EN-014:DISC-006"
work_type: DISCOVERY
title: "Schema Gap Analysis - EN-006 Features vs domain-schema.json"

classification: TECHNICAL

status: DOCUMENTED
resolution: null

priority: HIGH
impact: HIGH

assignee: "Claude"
created_by: "Claude"

created_at: "2026-01-29T00:00:00Z"
updated_at: "2026-01-29T00:00:00Z"
completed_at: "2026-01-29T00:00:00Z"

parent_id: "EN-014"

tags:
  - "schema-gap"
  - "domain-context"
  - "en-006"
  - "relationships"
  - "metadata"
  - "context-rules"
  - "validation"

finding_type: GAP
confidence_level: HIGH
source: "EN-006 artifact audit"
research_method: "Artifact comparison analysis"

validated: true
validation_date: "2026-01-29T00:00:00Z"
validated_by: "Claude"
```

---

## State Machine

**Current State:** `DOCUMENTED`

```
PENDING → IN_PROGRESS → DOCUMENTED
                            ↑
                       (completed)
```

---

## Summary

**Core Finding:** The EN-006 context injection design artifacts contain 4 feature categories (relationships, metadata, context_rules, validation) that are **not supported** by the current `domain-schema.json`. Promoting EN-006 artifacts to production domain YAML files (TASK-150..159) without schema extension will result in **silent data loss** and degraded extraction intelligence.

**Key Findings:**
1. **Entity Relationships** - EN-006 defines inter-entity links (blocks, resolves, triggers) with no schema support
2. **Domain Metadata** - target_users, transcript_types, key_use_cases have no schema representation
3. **Context Rules** - Meeting-type-specific extraction focus has no schema mechanism
4. **Schema Validation** - min_entities, required_entities constraints cannot be expressed

**Validation:** Confirmed through direct artifact comparison (EN-006 sources vs domain-schema.json)

---

## Context

### Background

During preparation for TASK-150..159 (EN-006 artifact promotion to domain YAML files), an audit was conducted to verify transformation requirements. The audit revealed that the EN-006 domain context design includes rich semantic features that the current `domain-schema.json` cannot represent.

### Research Question

**What features in EN-006 artifacts cannot be represented in the current domain-schema.json, and what is the impact of this gap?**

### Investigation Approach

1. Read all EN-006 domain context specification files
2. Read current `domain-schema.json` schema definition
3. Compare feature-by-feature for schema coverage
4. Document gaps with specific examples
5. Assess impact of each gap on extraction quality

---

## Finding

### Gap 1: Entity Relationships

**Source:** `EN-006/docs/domains/01-software-engineering/entities/entity-definitions.yaml`

```yaml
# EN-006 Source - NOT SUPPORTED
entities:
  blocker:
    relationships:
      - type: "blocks"
        target: "commitment"
        cardinality: "many-to-many"
      - type: "resolved_by"
        target: "action_item"
        cardinality: "one-to-many"
```

**Current Schema Support:** ❌ No `relationships` property in entity schema

**Impact:**
- Loss of semantic connections between entities
- Cannot express "blocker blocks commitment" relationship
- Mindmap generator cannot create relationship edges
- Extraction agents lose context about entity interactions

### Gap 2: Domain Metadata

**Source:** `EN-006/docs/domains/01-software-engineering/domain-definition.yaml`

```yaml
# EN-006 Source - NOT SUPPORTED
metadata:
  target_users:
    - "Software Engineers"
    - "Tech Leads"
    - "Engineering Managers"
  transcript_types:
    - "Daily standup"
    - "Sprint planning"
    - "Retrospective"
  key_use_cases:
    - "Track commitments and blockers"
    - "Surface decisions and action items"
    - "Identify team dependencies"
```

**Current Schema Support:** ❌ No `metadata` section in schema

**Impact:**
- Loss of domain context for extraction prioritization
- Cannot tailor extraction to specific meeting types
- User-facing documentation loses valuable context
- Domain selection heuristics cannot use this data

### Gap 3: Context Rules

**Source:** `EN-006/docs/domains/01-software-engineering/extraction/context-rules.yaml`

```yaml
# EN-006 Source - NOT SUPPORTED
context_rules:
  standup:
    meeting_type: "daily_standup"
    primary_entities:
      - commitment
      - blocker
    secondary_entities:
      - action_item
    extraction_focus: "What did you do? What will you do? What blocks you?"

  sprint_planning:
    meeting_type: "sprint_planning"
    primary_entities:
      - commitment
      - action_item
    secondary_entities:
      - blocker
    extraction_focus: "Sprint goals, capacity, story assignments"
```

**Current Schema Support:** ❌ No `context_rules` mechanism

**Impact:**
- Cannot vary extraction priority by meeting type
- All meetings treated identically regardless of context
- Loss of domain-specific extraction intelligence
- Extraction confidence cannot be context-weighted

### Gap 4: Schema Validation Rules

**Source:** `EN-006/docs/domains/01-software-engineering/validation/validation-rules.yaml`

```yaml
# EN-006 Source - NOT SUPPORTED
validation:
  min_entities: 4
  required_entities:
    - commitment
    - blocker
    - action_item
  optional_entities:
    - decision
    - risk
  extraction_threshold: 0.7
```

**Current Schema Support:** ❌ No `validation` section

**Impact:**
- Cannot enforce minimum entity count per domain
- Cannot validate required vs optional entities
- Schema validation only checks structure, not domain completeness
- Quality gates cannot use domain-specific thresholds

---

## Evidence

### Source Documentation

| Evidence ID | Type | Description | Source | Date |
|-------------|------|-------------|--------|------|
| E-001 | Schema | domain-schema.json current definition | `skills/transcript/contexts/domain-schema.json` | 2026-01-29 |
| E-002 | Spec | EN-006 software-engineering entity definitions | `EN-006/docs/domains/01-software-engineering/entities/entity-definitions.yaml` | 2026-01-29 |
| E-003 | Spec | EN-006 software-engineering domain definition | `EN-006/docs/domains/01-software-engineering/domain-definition.yaml` | 2026-01-29 |
| E-004 | Spec | EN-006 context rules specification | `EN-006/docs/domains/01-software-engineering/extraction/context-rules.yaml` | 2026-01-29 |
| E-005 | Spec | EN-006 validation rules specification | `EN-006/docs/domains/01-software-engineering/validation/validation-rules.yaml` | 2026-01-29 |

### Gap Summary Matrix

| Gap ID | Feature | EN-006 Has | Schema Has | Gap Type |
|--------|---------|------------|------------|----------|
| GAP-001 | Entity Relationships | ✅ | ❌ | Missing property |
| GAP-002 | Domain Metadata | ✅ | ❌ | Missing section |
| GAP-003 | Context Rules | ✅ | ❌ | Missing mechanism |
| GAP-004 | Validation Rules | ✅ | ❌ | Missing section |

---

## Implications

### Impact on Project

Proceeding with TASK-150..159 (domain YAML promotion) **without schema extension** will result in:

1. **Silent Data Loss** - Relationships, metadata, context_rules, validation will be dropped
2. **Degraded Extraction** - Agents lose domain intelligence designed in EN-006
3. **Incomplete Mindmaps** - EN-009 mindmap generator cannot create relationship edges
4. **Quality Regression** - Domain-specific quality gates cannot be implemented

### Design Decisions Affected

| Decision | Impact | Required Action |
|----------|--------|-----------------|
| ADR-EN014-001 (pending) | Schema extension strategy | Create ADR before TASK-150..159 |
| TDD-domain-schema-v2 (pending) | Technical design for V2 schema | Create TDD with backward compatibility |
| TASK-150..159 | Domain YAML promotion | **BLOCKED** until schema extended |

### Risks Identified

| Risk | Severity | Mitigation |
|------|----------|------------|
| Promoting artifacts without schema support | HIGH | Block TASK-150..159 until TASK-169 approved |
| Schema extension breaks existing YAML files | MEDIUM | Ensure backward compatibility in TDD |
| Scope creep during schema extension | MEDIUM | Constrain to 4 identified gaps only |
| Insufficient research on schema patterns | MEDIUM | Require TASK-164 research with citations |

### Opportunities Created

- **Proper Foundation** - Schema V2 will properly support EN-006 design intent
- **Reusable Patterns** - Research may identify industry-standard relationship patterns
- **Quality Gates** - Validation rules enable domain-specific quality enforcement
- **Contextual Intelligence** - Context rules enable meeting-type-aware extraction

---

## Relationships

### Creates

- [TASK-164](./TASK-164-research-schema-extensibility.md) - Research: Schema Extensibility Patterns
- [TASK-165](./TASK-165-analysis-gap-impact.md) - Analysis: Gap Impact Assessment
- [TASK-166](./TASK-166-adr-schema-extension.md) - ADR: Schema Extension Strategy
- [TASK-167](./TASK-167-tdd-schema-v2.md) - TDD: Schema V2 Design
- [TASK-168](./TASK-168-final-adversarial-review.md) - Final Adversarial Review
- [TASK-169](./TASK-169-human-gate.md) - GATE: Human Approval

### Blocks

- [TASK-150](./TASK-150-software-engineering-domain.md) - Software Engineering Domain YAML
- [TASK-151](./TASK-151-software-architecture-domain.md) - Software Architecture Domain YAML
- [TASK-152](./TASK-152-product-management-domain.md) - Product Management Domain YAML
- [TASK-153](./TASK-153-user-experience-domain.md) - User Experience Domain YAML
- [TASK-154](./TASK-154-cloud-engineering-domain.md) - Cloud Engineering Domain YAML
- [TASK-155](./TASK-155-security-engineering-domain.md) - Security Engineering Domain YAML
- [TASK-156](./TASK-156-domain-schema-promotion.md) - Domain Schema Promotion
- [TASK-157](./TASK-157-spec-files-promotion.md) - Spec Files Promotion
- [TASK-158](./TASK-158-skill-md-domain-update.md) - SKILL.md Domain Update
- [TASK-159](./TASK-159-domain-load-validation.md) - Domain Load Validation

### Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [EN-014-domain-context-files.md](./EN-014-domain-context-files.md) | Parent enabler |
| Workflow | [EN-014--WORKFLOW-schema-extension.md](./EN-014--WORKFLOW-schema-extension.md) | Schema extension workflow |
| Schema | [domain-schema.json](../../../../skills/transcript/contexts/domain-schema.json) | Current schema (gaps here) |
| Reference | [SPEC-context-injection.md](../../FEAT-001-analysis-design/EN-006-context-injection-design/docs/specs/SPEC-context-injection.md) | EN-006 specification |

---

## Recommendations

### Immediate Actions

1. **Block TASK-150..159** - Add explicit dependency on TASK-169 (Human Approval Gate)
2. **Create TASK-164..169** - Research, Analysis, ADR, TDD, Review, Gate tasks
3. **Update ORCHESTRATION.yaml** - Reflect new dependency chain

### Long-term Considerations

- **Schema Versioning** - Consider semantic versioning for domain-schema.json
- **Migration Tooling** - May need tools to upgrade existing YAML files to V2
- **Documentation** - Update SKILL.md with schema V2 features

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-29 | Claude | Created discovery document from EN-006 artifact audit |

---

## Metadata

```yaml
id: "EN-014:DISC-006"
parent_id: "EN-014"
work_type: DISCOVERY
title: "Schema Gap Analysis - EN-006 Features vs domain-schema.json"
status: DOCUMENTED
priority: HIGH
impact: HIGH
created_by: "Claude"
created_at: "2026-01-29T00:00:00Z"
updated_at: "2026-01-29T00:00:00Z"
completed_at: "2026-01-29T00:00:00Z"
tags: ["schema-gap", "domain-context", "en-006", "relationships", "metadata", "context-rules", "validation"]
source: "EN-006 artifact audit"
finding_type: GAP
confidence_level: HIGH
validated: true
blocks:
  - "TASK-150"
  - "TASK-151"
  - "TASK-152"
  - "TASK-153"
  - "TASK-154"
  - "TASK-155"
  - "TASK-156"
  - "TASK-157"
  - "TASK-158"
  - "TASK-159"
creates:
  - "TASK-164"
  - "TASK-165"
  - "TASK-166"
  - "TASK-167"
  - "TASK-168"
  - "TASK-169"
```
