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
status: BACKLOG
resolution: null
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-29T00:00:00Z"
updated_at: "2026-01-29T00:00:00Z"

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
remaining_work: 5
time_spent: 0
```

---

## State Machine

**Current State:** `BACKLOG`

```
BACKLOG → IN_PROGRESS → DONE
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

- [ ] TDD created at `docs/design/TDD-EN014-domain-schema-v2.md`
- [ ] JSON Schema definition for all 4 features (relationships, metadata, context_rules, validation)
- [ ] Migration strategy from V1 to V2 documented
- [ ] Backward compatibility approach specified
- [ ] Validation rules and error handling defined
- [ ] At least 2 example YAML files demonstrating V2 features
- [ ] L0/L1/L2 audience sections included
- [ ] ps-critic quality review passes (≥ 0.85)
- [ ] nse-qa quality review passes (≥ 0.85)

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

| Metric            | Value    |
|-------------------|----------|
| Original Estimate | 5 hours  |
| Remaining Work    | 5 hours  |
| Time Spent        | 0 hours  |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| TDD Document | Markdown | docs/design/TDD-EN014-domain-schema-v2.md |
| Example V2 YAML | YAML | (within TDD or separate) |
| ps-critic Review | Quality Report | (pending) |
| nse-qa Review | Quality Report | (pending) |

### Verification

- [ ] TDD created at specified path
- [ ] All 4 schema features designed
- [ ] Migration strategy documented
- [ ] Example files created
- [ ] ps-critic score ≥ 0.85
- [ ] nse-qa score ≥ 0.85
- [ ] Reviewed by: (pending dual-reviewer)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-29 | Created | Initial creation per EN-014:DISC-006 |
