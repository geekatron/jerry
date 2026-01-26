# TASK-038: Example Orchestration Plans

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
-->

---

## Frontmatter

```yaml
# === IDENTITY (Auto-generated, Immutable) ===
id: "TASK-038"
work_type: TASK

# === CORE METADATA ===
title: "Example Orchestration Plans"
description: |
  Phase 3: Create 4 domain-specific example orchestration plans demonstrating
  context injection. Validated by ps-validator (schema) and nse-verification
  (verification approach).

# === CLASSIFICATION ===
classification: ENABLER

# === LIFECYCLE STATE ===
status: BACKLOG
resolution: null

# === PRIORITY ===
priority: MEDIUM

# === PEOPLE ===
assignee: "ps-architect + ps-validator + nse-verification"
created_by: "Claude"

# === TIMESTAMPS ===
created_at: "2026-01-26T16:00:00Z"
updated_at: "2026-01-26T16:00:00Z"

# === HIERARCHY ===
parent_id: "EN-006"

# === TAGS ===
tags:
  - "examples"
  - "orchestration"
  - "validation"
  - "phase-3"

# === DELIVERY ITEM PROPERTIES ===
effort: 2
acceptance_criteria: |
  See Acceptance Criteria section below
due_date: null

# === TASK-SPECIFIC PROPERTIES ===
activity: DOCUMENTATION
original_estimate: 3
remaining_work: 3
time_spent: 0

# === ORCHESTRATION ===
phase: 3
barrier: null
execution_mode: "PARALLEL_WITH_TASK_036_037"
ps_agent: "ps-architect"
validator: "ps-validator"
nse_agent: "nse-verification"
blocked_by: "BARRIER-2"
```

---

## Content

### Description

Create 4 example orchestration plans demonstrating context injection for different domains:

1. **01-generic-baseline/** - No context injection (comparison baseline)
2. **02-legal-domain/** - Legal transcript analysis
3. **03-sales-domain/** - Sales call analysis
4. **04-engineering-domain/** - Technical meeting analysis

**Each example includes:**
- ORCHESTRATION_PLAN.yaml with context_injection section
- Context files (entity definitions, extraction rules)
- Custom prompt templates
- Expected output samples

**Validation:**
- ps-validator: Schema validation against context-injection-schema.json
- nse-verification: VCRM (Verification Cross Reference Matrix) approach

### Example Directory Structure

```
docs/examples/context-injection/
├── README.md                          # Overview and usage guide
├── 01-generic-baseline/
│   ├── ORCHESTRATION_PLAN.yaml        # No context injection
│   └── expected-output/
│       └── sample-output.md
├── 02-legal-domain/
│   ├── ORCHESTRATION_PLAN.yaml        # Legal context injection
│   ├── contexts/
│   │   ├── legal-terms.yaml           # Entity definitions
│   │   └── contract-patterns.md       # Extraction rules
│   ├── prompts/
│   │   └── legal-extraction.md        # Custom prompt
│   └── expected-output/
│       └── sample-legal-output.md
├── 03-sales-domain/
│   ├── ORCHESTRATION_PLAN.yaml
│   ├── contexts/
│   │   └── sales-entities.yaml
│   ├── prompts/
│   │   └── deal-tracking.md
│   └── expected-output/
│       └── sample-sales-output.md
└── 04-engineering-domain/
    ├── ORCHESTRATION_PLAN.yaml
    ├── contexts/
    │   └── tech-patterns.yaml
    ├── prompts/
    │   └── decision-extraction.md
    └── expected-output/
        └── sample-engineering-output.md
```

### Domain-Specific Context Examples

**Legal Domain:**
```yaml
# contexts/legal-terms.yaml
entity_definitions:
  party:
    description: "Legal entity in contract"
    attributes:
      - name
      - role (buyer/seller/guarantor)
      - jurisdiction
  obligation:
    description: "Contractual obligation"
    attributes:
      - obligor
      - obligee
      - terms
      - deadline
  term:
    description: "Contract term or clause"
    attributes:
      - type (payment/delivery/warranty)
      - value
      - conditions
```

**Sales Domain:**
```yaml
# contexts/sales-entities.yaml
entity_definitions:
  deal:
    description: "Sales opportunity"
    attributes:
      - stage
      - value
      - close_date
  objection:
    description: "Customer objection"
    attributes:
      - type
      - response
      - resolved
  action_item:
    description: "Follow-up action"
    attributes:
      - owner
      - due_date
      - status
```

### Acceptance Criteria

**Example Content Criteria:**
- [ ] **AC-001:** 4 distinct domain examples created
- [ ] **AC-002:** Each example has complete ORCHESTRATION_PLAN.yaml
- [ ] **AC-003:** Each domain example has at least 1 context file
- [ ] **AC-004:** Each domain example has at least 1 custom prompt
- [ ] **AC-005:** Each example has expected output sample
- [ ] **AC-006:** Generic baseline shows behavior without injection

**Validation Criteria (ps-validator):**
- [ ] **AC-007:** All YAML files validate against schema
- [ ] **AC-008:** Context files follow entity_definitions format
- [ ] **AC-009:** Prompt templates have required sections

**Verification Criteria (nse-verification):**
- [ ] **AC-010:** VCRM links examples to requirements
- [ ] **AC-011:** Verification approach documented for each example
- [ ] **AC-012:** NASA SE Process 7, 8 compliance

**Documentation Criteria:**
- [ ] **AC-013:** README explains how to use each example
- [ ] **AC-014:** Examples demonstrate full context injection flow

### Deliverables

| Deliverable | Type | Link | Status |
|-------------|------|------|--------|
| Examples Directory | Documentation | docs/examples/context-injection/ | PENDING |
| README | Documentation | docs/examples/context-injection/README.md | PENDING |
| Generic Baseline | Example | docs/examples/context-injection/01-generic-baseline/ | PENDING |
| Legal Domain | Example | docs/examples/context-injection/02-legal-domain/ | PENDING |
| Sales Domain | Example | docs/examples/context-injection/03-sales-domain/ | PENDING |
| Engineering Domain | Example | docs/examples/context-injection/04-engineering-domain/ | PENDING |

---

## History

| Date       | Status      | Notes                          |
|------------|-------------|--------------------------------|
| 2026-01-26 | Created     | Task created for redesigned workflow |

---

*Task ID: TASK-038*
*Workflow ID: en006-ctxinj-20260126-001*
*Phase: 3 (Integration, Risk & Examples)*
*NASA SE: Process 7, 8 (Verification)*
