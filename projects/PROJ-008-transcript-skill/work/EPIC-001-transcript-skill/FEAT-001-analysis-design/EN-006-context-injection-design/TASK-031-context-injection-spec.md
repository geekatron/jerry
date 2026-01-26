# TASK-031: Context Injection Specification

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
-->

---

## Frontmatter

```yaml
# === IDENTITY (Auto-generated, Immutable) ===
id: "TASK-031"
work_type: TASK

# === CORE METADATA ===
title: "Context Injection Specification"
description: |
  Create the formal specification for the context injection mechanism.
  This spec defines the contract between orchestration plans and agents,
  including payload formats, injection points, and validation rules.

# === CLASSIFICATION ===
classification: ENABLER

# === LIFECYCLE STATE ===
status: BACKLOG
resolution: null

# === PRIORITY ===
priority: HIGH

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
  - "specification"
  - "context-injection"
  - "architecture"
  - "phase-2"

# === DELIVERY ITEM PROPERTIES ===
effort: 2
acceptance_criteria: |
  See Acceptance Criteria section below
due_date: null

# === TASK-SPECIFIC PROPERTIES ===
activity: DESIGN
original_estimate: 4
remaining_work: 4
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

Create the formal specification for the context injection mechanism. This is the authoritative document that defines how context injection works, serving as the contract between orchestration plans and agents.

**Specification Components:**
```
CONTEXT INJECTION SPECIFICATION
├── SCHEMA: Context payload format (YAML/JSON)
├── INJECTION POINTS: Where context enters agent execution
├── PROMPT TEMPLATES: Customizable agent instruction mechanism
├── ARTIFACT METADATA: Context attached to agent outputs
├── VALIDATION RULES: Schema validation and error handling
├── SECURITY CONSTRAINTS: What can/cannot be injected
└── VERSIONING: Compatibility and evolution strategy
```

**Key Design Decisions Required:**
1. Context payload schema (YAML vs JSON vs Markdown)
2. Injection timing (pre-execution vs during-execution)
3. Prompt override strategy (replace vs merge vs prepend)
4. Error handling for invalid context
5. Context caching and invalidation

### Acceptance Criteria

- [ ] **AC-001:** Context payload schema defined with JSON Schema validation
- [ ] **AC-002:** At least 3 injection points documented with sequence diagrams
- [ ] **AC-003:** Prompt template mechanism specified with variable substitution syntax
- [ ] **AC-004:** Artifact metadata format defined for output enrichment
- [ ] **AC-005:** Validation rules specified with error codes and recovery actions
- [ ] **AC-006:** Security constraints documented (no code injection, sanitization rules)
- [ ] **AC-007:** Versioning strategy defined for backward compatibility
- [ ] **AC-008:** Integration with existing SKILL.md orchestrator documented
- [ ] **AC-009:** Specification follows TDD template structure (L0/L1/L2)
- [ ] **AC-010:** Deliverable created at `docs/specs/SPEC-context-injection.md`

### Dependencies

| Type | Item | Status |
|------|------|--------|
| Input | TASK-030 5W2H Analysis | Pending |
| Input | EN-005 SKILL.md Orchestrator Design | Complete |
| Input | ADR-002 Artifact Structure | Complete |
| Output | TASK-032 Orchestration Integration | Blocked until this completes |

### Implementation Notes

**Agent Assignment:** ps-architect

**Key Sources to Reference:**
1. TASK-030 5W2H Analysis - Analysis findings drive spec decisions
2. ADR-002 Artifact Structure - Consistent artifact format
3. SKILL.md (skills/transcript/) - Current orchestration interface
4. Orchestration SKILL.md - Cross-pollination patterns

**Schema Design Requirements:**
```yaml
# Example Context Payload Schema
context_injection:
  version: "1.0.0"
  domain: string          # Required: domain identifier
  context_files:          # Optional: external context files
    - path: string
      type: enum[entity_definitions, extraction_rules, examples]
  prompt_overrides:       # Optional: agent prompt customization
    agent_id:
      template: string    # Path to template file
      variables: object   # Template variable values
  metadata:               # Optional: output enrichment
    tags: array[string]
    annotations: object
```

**Specification Sections:**
```markdown
# Context Injection Specification v1.0

## L0: Overview (ELI5)
[Simple explanation of what the spec defines]

## L1: Technical Specification (Engineer)
### 1. Context Payload Schema
### 2. Injection Points
### 3. Prompt Template Mechanism
### 4. Artifact Metadata
### 5. Validation Rules
### 6. Security Constraints
### 7. Error Handling

## L2: Design Rationale (Architect)
### Decision Log
### Trade-offs
### Evolution Path
```

### Related Items

- Parent: [EN-006 Context Injection Design](./EN-006-context-injection-design.md)
- Input: [TASK-030 5W2H Analysis](./TASK-030-5w2h-analysis.md)
- Reference: [ADR-002 Artifact Structure](../../docs/adrs/ADR-002-artifact-structure.md)
- Enables: [TASK-032 Orchestration Integration](./TASK-032-orchestration-integration.md)

---

## Time Tracking

| Metric            | Value           |
|-------------------|-----------------|
| Original Estimate | 4 hours         |
| Remaining Work    | 4 hours         |
| Time Spent        | 0 hours         |

---

## Evidence

### Deliverables

| Deliverable | Type | Link | Status |
|-------------|------|------|--------|
| SPEC-context-injection.md | Specification Document | docs/specs/SPEC-context-injection.md | PENDING |
| context-injection-schema.json | JSON Schema | docs/specs/schemas/context-injection-schema.json | PENDING |

### Verification

- [ ] Acceptance criteria verified
- [ ] JSON Schema validates correctly
- [ ] Sequence diagrams render correctly
- [ ] Security review completed
- [ ] ADR-002 alignment confirmed
- [ ] ps-critic review completed
- [ ] Reviewed by: TBD

---

## History

| Date       | Status      | Notes                          |
|------------|-------------|--------------------------------|
| 2026-01-26 | Created     | Initial task creation          |

---

*Task ID: TASK-031*
*Workflow ID: en006-ctxinj-20260126-001*
*Constitutional Compliance: P-002 (persisted), P-004 (provenance), P-011 (evidence-based)*
