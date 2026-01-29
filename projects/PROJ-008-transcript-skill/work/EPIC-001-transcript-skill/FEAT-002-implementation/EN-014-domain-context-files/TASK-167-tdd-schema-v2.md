# TASK-167: TDD - Schema V2 Design

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-014 (Domain Context Files Implementation)
WORKFLOW: EN-014--WORKFLOW-schema-extension.md
-->

---

## Frontmatter

```yaml
id: "TASK-167"
work_type: TASK
title: "TDD - Schema V2 Design"
description: |
  Create Technical Design Document for domain-schema.json V2 implementation.
  Define schema structure, migration strategy, validation rules, and
  backward compatibility approach per ADR-EN014-001 decision.

classification: ENABLER
status: DONE
resolution: COMPLETED
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-29T00:00:00Z"
updated_at: "2026-01-29T12:10:00Z"
completed_at: "2026-01-29T12:10:00Z"

parent_id: "EN-014"

tags:
  - "tdd"
  - "technical-design"
  - "schema-v2"
  - "json-schema"
  - "migration"

effort: 3
acceptance_criteria: |
  - TDD created with full schema V2 specification
  - JSON Schema definition for all 4 new features
  - Migration strategy for existing YAML files
  - Backward compatibility approach documented
  - Validation rules and error handling specified
  - Example YAML files demonstrating V2 features
  - ps-critic score >= 0.85
  - nse-qa score >= 0.85

due_date: null

activity: DESIGN
original_estimate: 5
remaining_work: 0
time_spent: 3
```

---

## State Machine

**Current State:** `DONE`

```
BACKLOG → IN_PROGRESS → DONE ← (current)
              ↓
           BLOCKED
```

---

## Content

### Description

This task creates a Technical Design Document (TDD) for implementing domain-schema.json V2. The TDD must translate the architectural decision from ADR-EN014-001 into detailed technical specifications.

### Schema V2 Features to Design

| Feature | Gap Addressed | Design Focus |
|---------|---------------|--------------|
| `relationships` | GAP-001 | Entity-to-entity link structure |
| `metadata` | GAP-002 | Domain context information |
| `context_rules` | GAP-003 | Meeting-type extraction config |
| `validation` | GAP-004 | Domain completeness constraints |

### TDD Structure

```markdown
# TDD: Domain Schema V2

## 1. Overview
[Purpose and scope of schema extension]

## 2. Schema Specification
### 2.1 Relationships Schema
### 2.2 Metadata Schema
### 2.3 Context Rules Schema
### 2.4 Validation Schema

## 3. Migration Strategy
### 3.1 V1 to V2 Migration Path
### 3.2 Backward Compatibility

## 4. Validation Rules
### 4.1 Schema Validation
### 4.2 Semantic Validation

## 5. Example Files
### 5.1 V2 Domain YAML Example
### 5.2 V1 Compatibility Example

## 6. Implementation Notes
[Technical considerations]
```

### JSON Schema Design Targets

**relationships:**
```yaml
relationships:
  - type: "blocks"
    target: "commitment"
    cardinality: "many-to-many"
```

**metadata:**
```yaml
metadata:
  target_users: ["Software Engineers", "Tech Leads"]
  transcript_types: ["Daily standup", "Sprint planning"]
  key_use_cases: ["Track commitments", "Surface decisions"]
```

**context_rules:**
```yaml
context_rules:
  standup:
    meeting_type: "daily_standup"
    primary_entities: [commitment, blocker]
    extraction_focus: "What did you do? What will you do?"
```

**validation:**
```yaml
validation:
  min_entities: 4
  required_entities: [commitment, blocker, action_item]
  extraction_threshold: 0.7
```

### Dependencies

**Blocked By:**
- TASK-166: ADR provides architectural decision to implement

**Input Artifacts:**
- TASK-166: ADR-EN014-001-schema-extension-strategy.md
- TASK-164: Research findings on schema patterns
- Current domain-schema.json (V1)

### Dual-Reviewer Quality Gate

| Reviewer | Threshold | Focus Area |
|----------|-----------|------------|
| ps-critic | ≥ 0.85 | TDD completeness, technical accuracy |
| nse-qa | ≥ 0.85 | NASA SE compliance, requirements traceability |
| Logic | AND | Both must pass |

### Acceptance Criteria

- [x] TDD created at `docs/design/TDD-EN014-domain-schema-v2.md`
- [x] JSON Schema definition for all 4 features (relationships, metadata, context_rules, validation)
- [x] Migration strategy from V1 to V2 documented
- [x] Backward compatibility approach specified
- [x] Validation rules and error handling defined
- [x] At least 2 example YAML files demonstrating V2 features
- [x] L0/L1/L2 audience sections included
- [x] ps-critic quality review passes (≥ 0.85) - **Score: 0.93 PASS**
- [x] nse-qa quality review passes (≥ 0.85) - **Score: 0.91 PASS**

### Implementation Notes

**Agent Assignment:** ps-architect (design) + domain expertise

**Design Method:**
1. Read ADR-EN014-001 for architectural decision
2. Review TASK-164 research for pattern details
3. Design JSON Schema extensions for each feature
4. Define migration and compatibility strategy
5. Create example YAML files
6. Document validation and error handling

**Output Artifact:**
```
docs/design/TDD-EN014-domain-schema-v2.md
```

### Related Items

- Parent: [EN-014: Domain Context Files Implementation](./EN-014-domain-context-files.md)
- Discovery: [EN-014:DISC-006: Schema Gap Analysis](./EN-014--DISC-006-schema-gap-analysis.md)
- Blocked By: [TASK-166: ADR Schema Extension](./TASK-166-adr-schema-extension.md)
- Blocks: [TASK-168: Final Adversarial Review](./TASK-168-final-adversarial-review.md)
- Workflow: [EN-014--WORKFLOW-schema-extension.md](./EN-014--WORKFLOW-schema-extension.md)

---

## Time Tracking

| Metric            | Value      |
|-------------------|------------|
| Original Estimate | 5 hours    |
| Remaining Work    | 0 hours    |
| Time Spent        | 3 hours    |

---

## Evidence

### Deliverables

| Deliverable | Type | Link | Status |
|-------------|------|------|--------|
| TDD Document | Markdown | [docs/design/TDD-EN014-domain-schema-v2.md](./docs/design/TDD-EN014-domain-schema-v2.md) | **COMPLETE** |
| Example V2 YAML | YAML | (within TDD Section 6.1-6.2) | **COMPLETE** |
| ps-critic Review | Quality Report | [critiques/en014-task167-iter1-critique.md](./critiques/en014-task167-iter1-critique.md) | **COMPLETE** (0.93) |
| nse-qa Review | Quality Report | [qa/en014-task167-iter1-qa.md](./qa/en014-task167-iter1-qa.md) | **COMPLETE** (0.91) |

### Verification

- [x] TDD created at specified path (1947 lines)
- [x] All 4 schema features designed ($defs: entityRelationship, domainMetadata, contextRule, validationRule)
- [x] Migration strategy documented (Section 4: SchemaVer v1.0.0→v1.1.0)
- [x] Example files created (software-engineering.yaml, general.yaml)
- [x] ps-critic score ≥ 0.85 (Score: **0.93**)
- [x] nse-qa score ≥ 0.85 (Score: **0.91**)
- [x] Reviewed by: ps-critic (v2.0.0) + nse-qa (v2.0.0) - Dual-reviewer PASS

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-29 | Created | Initial creation per EN-014:DISC-006 |
| 2026-01-29 | IN_PROGRESS | Started execution. TASK-166 (ADR) complete with decision: Option A (JSON Schema Extension v1.0.0→v1.1.0). Invoking ps-architect to create TDD. |
| 2026-01-29 | IN_PROGRESS | **ps-architect COMPLETE**: TDD created with full V1.1.0 JSON Schema specification (1947 lines). 4 $defs sections designed (entityRelationship, domainMetadata, contextRule, validationRule). L0/L1/L2 triple-lens, migration strategy, backward compatibility, 2 example YAML files. Artifact: [TDD-EN014-domain-schema-v2.md](./docs/design/TDD-EN014-domain-schema-v2.md) |
| 2026-01-29 | IN_PROGRESS | **ps-critic COMPLETE**: Quality review passed with score 0.93 (threshold 0.85). 0 major issues, 3 minor improvements, 12 positive findings. Artifact: [en014-task167-iter1-critique.md](./critiques/en014-task167-iter1-critique.md) |
| 2026-01-29 | DONE | **nse-qa COMPLETE**: NASA SE quality review passed with score 0.91 (threshold 0.85). NPR 7123.1D compliance verified (Process 14: 0.92, Process 15: 0.90, Process 16: 0.89). 0 critical, 0 major, 2 minor NCs, 12 observations. Dual-reviewer PASS. TASK-167 complete. |
