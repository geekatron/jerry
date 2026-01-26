# TASK-033: Example Orchestration Plans

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
-->

---

## Frontmatter

```yaml
# === IDENTITY (Auto-generated, Immutable) ===
id: "TASK-033"
work_type: TASK

# === CORE METADATA ===
title: "Example Orchestration Plans"
description: |
  Create 3-5 example orchestration plans demonstrating context injection
  for different domains. These examples serve as templates and validation
  that the context injection design is practical and complete.

# === CLASSIFICATION ===
classification: ENABLER

# === LIFECYCLE STATE ===
status: BACKLOG
resolution: null

# === PRIORITY ===
priority: MEDIUM

# === PEOPLE ===
assignee: "ps-architect"
created_by: "Claude"

# === TIMESTAMPS ===
created_at: "2026-01-26T15:00:00Z"
updated_at: "2026-01-26T15:00:00Z"

# === HIERARCHY ===
parent_id: "EN-006"

# === TAGS ===
tags:
  - "examples"
  - "orchestration"
  - "context-injection"
  - "phase-4"

# === DELIVERY ITEM PROPERTIES ===
effort: 1
acceptance_criteria: |
  See Acceptance Criteria section below
due_date: null

# === TASK-SPECIFIC PROPERTIES ===
activity: DOCUMENTATION
original_estimate: 2
remaining_work: 2
time_spent: 0
```

---

## State Machine

**Initial State:** `BACKLOG`

**Valid States:** `BACKLOG`, `IN_PROGRESS`, `BLOCKED`, `DONE`, `REMOVED`

---

## Containment Rules

| Rule             | Value                           |
|------------------|---------------------------------|
| Allowed Children | Subtask                         |
| Allowed Parents  | Enabler                         |
| Max Depth        | 1                               |

---

## Content

### Description

Create 3-5 example orchestration plans that demonstrate context injection for different domains. These examples:
1. Validate the context injection specification is complete
2. Serve as templates for users creating custom workflows
3. Demonstrate the flexibility of the mechanism
4. Expose any gaps in the design

**Example Domains to Cover:**
```
EXAMPLE ORCHESTRATION PLANS
├── LEGAL: Legal transcript analysis (contracts, depositions)
├── SALES: Sales call analysis (deal tracking, objections)
├── ENGINEERING: Technical meeting analysis (decisions, action items)
├── MEDICAL: Clinical transcript analysis (diagnoses, treatments)
└── GENERIC: Baseline with no context injection (comparison)
```

**Each Example Must Include:**
1. ORCHESTRATION_PLAN.yaml with context_injection section
2. Context files (entity definitions, extraction rules)
3. Custom prompt templates for relevant agents
4. Expected output artifacts with injected metadata

### Acceptance Criteria

- [ ] **AC-001:** At least 4 distinct domain examples created (Legal, Sales, Engineering, Generic)
- [ ] **AC-002:** Each example includes complete ORCHESTRATION_PLAN.yaml
- [ ] **AC-003:** Each example includes at least 1 context file
- [ ] **AC-004:** Each example includes at least 1 custom prompt template
- [ ] **AC-005:** Each example includes expected output sample
- [ ] **AC-006:** Examples validate against context-injection-schema.json
- [ ] **AC-007:** Generic (no-injection) example shows baseline behavior
- [ ] **AC-008:** Examples follow ORCHESTRATION_PLAN.template.md structure
- [ ] **AC-009:** README.md explains how to use each example
- [ ] **AC-010:** Deliverables created at `docs/examples/context-injection/`

### Dependencies

| Type | Item | Status |
|------|------|--------|
| Input | TASK-032 Orchestration Integration Design | Pending |
| Input | TASK-031 Context Injection Specification | Pending |
| Input | EN-003 Use Case Examples | Complete |
| Output | GATE-4 Human Approval | Requires complete EN-006 |

### Implementation Notes

**Agent Assignment:** ps-architect

**Key Sources to Reference:**
1. TASK-031 Context Injection Specification - Schema to follow
2. TASK-032 Orchestration Integration - YAML format
3. EN-003 Use Cases - User scenarios to model

**Example Directory Structure:**
```
docs/examples/context-injection/
├── README.md                          # Overview and usage guide
├── 01-generic-baseline/
│   ├── ORCHESTRATION_PLAN.yaml        # No context injection
│   └── expected-output/
├── 02-legal-domain/
│   ├── ORCHESTRATION_PLAN.yaml        # Legal context injection
│   ├── contexts/
│   │   └── legal-terms.yaml
│   ├── prompts/
│   │   └── legal-extraction.md
│   └── expected-output/
├── 03-sales-domain/
│   ├── ORCHESTRATION_PLAN.yaml
│   ├── contexts/
│   │   └── sales-entities.yaml
│   ├── prompts/
│   │   └── deal-tracking.md
│   └── expected-output/
└── 04-engineering-domain/
    ├── ORCHESTRATION_PLAN.yaml
    ├── contexts/
    │   └── tech-patterns.yaml
    ├── prompts/
    │   └── decision-extraction.md
    └── expected-output/
```

**Legal Domain Example (skeleton):**
```yaml
# ORCHESTRATION_PLAN.yaml
orchestration:
  name: "Legal Transcript Analysis"
  version: "1.0.0"
  description: "Analyze legal transcripts for contract terms, obligations, parties"

context_injection:
  enabled: true
  domain: "legal"
  context_files:
    - path: contexts/legal-terms.yaml
      type: entity_definitions
    - path: contexts/contract-patterns.md
      type: extraction_rules
  prompt_overrides:
    ts-extractor:
      template: prompts/legal-extraction.md
      variables:
        jurisdiction: "US Federal"
        document_type: "Contract Review"

pipeline:
  - stage: parse
    agent: ts-parser
    context_injection: false  # Standard parsing
  - stage: extract
    agent: ts-extractor
    context_injection: true   # Apply legal context
  - stage: format
    agent: ts-formatter
    context_injection: true   # Include legal metadata
```

### Related Items

- Parent: [EN-006 Context Injection Design](./EN-006-context-injection-design.md)
- Input: [TASK-032 Orchestration Integration](./TASK-032-orchestration-integration.md)
- Input: [TASK-031 Context Injection Specification](./TASK-031-context-injection-spec.md)
- Enables: [GATE-4 Human Approval](../../FEAT-001-analysis-design.md)

---

## Time Tracking

| Metric            | Value           |
|-------------------|-----------------|
| Original Estimate | 2 hours         |
| Remaining Work    | 2 hours         |
| Time Spent        | 0 hours         |

---

## Evidence

### Deliverables

| Deliverable | Type | Link | Status |
|-------------|------|------|--------|
| Context Injection Examples | Example Directory | docs/examples/context-injection/ | PENDING |
| README.md | Usage Guide | docs/examples/context-injection/README.md | PENDING |
| 01-generic-baseline/ | Example | docs/examples/context-injection/01-generic-baseline/ | PENDING |
| 02-legal-domain/ | Example | docs/examples/context-injection/02-legal-domain/ | PENDING |
| 03-sales-domain/ | Example | docs/examples/context-injection/03-sales-domain/ | PENDING |
| 04-engineering-domain/ | Example | docs/examples/context-injection/04-engineering-domain/ | PENDING |

### Verification

- [ ] Acceptance criteria verified
- [ ] All examples validate against schema
- [ ] README provides clear usage instructions
- [ ] Examples cover distinct use cases
- [ ] Prompt templates are complete and usable
- [ ] ps-critic review completed
- [ ] Reviewed by: TBD

---

## History

| Date       | Status      | Notes                          |
|------------|-------------|--------------------------------|
| 2026-01-26 | Created     | Initial task creation          |

---

*Task ID: TASK-033*
*Workflow ID: en006-ctxinj-20260126-001*
*Constitutional Compliance: P-002 (persisted), P-004 (provenance), P-011 (evidence-based)*
