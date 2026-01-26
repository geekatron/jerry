# TASK-032: Orchestration Integration Design

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
-->

---

## Frontmatter

```yaml
# === IDENTITY (Auto-generated, Immutable) ===
id: "TASK-032"
work_type: TASK

# === CORE METADATA ===
title: "Orchestration Integration Design"
description: |
  Design how context injection integrates with the orchestration system.
  This bridges the context injection specification with the existing
  SKILL.md orchestrator and Jerry's orchestration skill patterns.

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
  - "orchestration"
  - "integration"
  - "context-injection"
  - "phase-3"

# === DELIVERY ITEM PROPERTIES ===
effort: 1
acceptance_criteria: |
  See Acceptance Criteria section below
due_date: null

# === TASK-SPECIFIC PROPERTIES ===
activity: DESIGN
original_estimate: 3
remaining_work: 3
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

Design how context injection integrates with the orchestration system. This task bridges the context injection specification (TASK-031) with:
1. The Transcript Skill SKILL.md orchestrator
2. Jerry's orchestration skill patterns
3. ORCHESTRATION_PLAN.yaml/ORCHESTRATION.yaml artifacts

**Integration Design Scope:**
```
ORCHESTRATION INTEGRATION
├── SKILL.md MODIFICATIONS: Changes to orchestrator pattern
├── YAML EXTENSIONS: New context_injection section in ORCHESTRATION_PLAN
├── STATE TRACKING: How context flows through ORCHESTRATION.yaml
├── AGENT INVOCATION: Modified agent dispatch with context
└── ERROR PROPAGATION: Context-related error handling in workflow
```

**Key Design Questions:**
1. How does SKILL.md detect and load context injection config?
2. What YAML schema changes are needed for ORCHESTRATION_PLAN?
3. How is context state tracked during workflow execution?
4. How do existing agents receive injected context?
5. How are context-related errors surfaced to the orchestrator?

### Acceptance Criteria

- [ ] **AC-001:** SKILL.md modification pattern documented with before/after examples
- [ ] **AC-002:** ORCHESTRATION_PLAN.yaml schema extension specified
- [ ] **AC-003:** ORCHESTRATION.yaml state tracking for context documented
- [ ] **AC-004:** Agent invocation interface changes documented
- [ ] **AC-005:** Error propagation design covers at least 5 error scenarios
- [ ] **AC-006:** Integration aligns with Jerry orchestration skill patterns
- [ ] **AC-007:** P-003 compliance verified (single nesting preserved)
- [ ] **AC-008:** Integration design follows L0/L1/L2 documentation format
- [ ] **AC-009:** Mermaid sequence diagrams show integration flows
- [ ] **AC-010:** Deliverable created at `docs/design/en006-orchestration-integration.md`

### Dependencies

| Type | Item | Status |
|------|------|--------|
| Input | TASK-031 Context Injection Specification | Pending |
| Input | EN-005 SKILL.md Design | Complete |
| Input | Jerry Orchestration Skill | Reference |
| Output | TASK-033 Example Orchestration Plans | Blocked until this completes |

### Implementation Notes

**Agent Assignment:** ps-architect

**Key Sources to Reference:**
1. TASK-031 Context Injection Specification - Core spec to integrate
2. skills/transcript/SKILL.md - Current orchestrator design
3. skills/orchestration/SKILL.md - Jerry orchestration patterns
4. skills/orchestration/templates/ - ORCHESTRATION_PLAN template

**SKILL.md Integration Pattern:**
```markdown
# Transcript Skill (with Context Injection)

## Context Injection Support

### Detection
- Check for `context_injection` key in workflow config
- Load context files relative to workflow root
- Validate against context-injection-schema.json

### Loading
- Parse context files (YAML, JSON, Markdown)
- Build context payload
- Validate domain-specific rules

### Injection
- Before agent invocation, inject context into prompt
- Attach metadata to agent output
- Track context state in ORCHESTRATION.yaml
```

**ORCHESTRATION_PLAN.yaml Extension:**
```yaml
# New context_injection section
context_injection:
  enabled: true
  domain: "transcript-legal"
  context_files:
    - path: contexts/legal-terms.yaml
      type: entity_definitions
  prompt_overrides:
    ts-extractor:
      template: prompts/legal-extraction.md

pipeline:
  - stage: extract
    agent: ts-extractor
    context_injection: true  # New flag
```

### Related Items

- Parent: [EN-006 Context Injection Design](./EN-006-context-injection-design.md)
- Input: [TASK-031 Context Injection Specification](./TASK-031-context-injection-spec.md)
- Reference: [Jerry Orchestration Skill](../../../../../skills/orchestration/SKILL.md)
- Enables: [TASK-033 Example Orchestration Plans](./TASK-033-example-plans.md)

---

## Time Tracking

| Metric            | Value           |
|-------------------|-----------------|
| Original Estimate | 3 hours         |
| Remaining Work    | 3 hours         |
| Time Spent        | 0 hours         |

---

## Evidence

### Deliverables

| Deliverable | Type | Link | Status |
|-------------|------|------|--------|
| en006-orchestration-integration.md | Design Document | docs/design/en006-orchestration-integration.md | PENDING |

### Verification

- [ ] Acceptance criteria verified
- [ ] SKILL.md modification pattern reviewed
- [ ] YAML schema extension validated
- [ ] Sequence diagrams render correctly
- [ ] P-003 compliance confirmed
- [ ] Orchestration skill alignment verified
- [ ] ps-critic review completed
- [ ] Reviewed by: TBD

---

## History

| Date       | Status      | Notes                          |
|------------|-------------|--------------------------------|
| 2026-01-26 | Created     | Initial task creation          |

---

*Task ID: TASK-032*
*Workflow ID: en006-ctxinj-20260126-001*
*Constitutional Compliance: P-002 (persisted), P-003 (single nesting), P-004 (provenance)*
