# TASK-036: Orchestration Integration Design

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
-->

---

## Frontmatter

```yaml
# === IDENTITY (Auto-generated, Immutable) ===
id: "TASK-036"
work_type: TASK

# === CORE METADATA ===
title: "Orchestration Integration Design"
description: |
  Phase 3: Design how context injection integrates with Jerry's
  orchestration system (ORCHESTRATION_PLAN.yaml, SKILL.md, agent invocation).

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
created_at: "2026-01-26T16:00:00Z"
updated_at: "2026-01-26T16:00:00Z"

# === HIERARCHY ===
parent_id: "EN-006"

# === TAGS ===
tags:
  - "integration"
  - "orchestration"
  - "skill-md"
  - "phase-3"

# === DELIVERY ITEM PROPERTIES ===
effort: 2
acceptance_criteria: |
  See Acceptance Criteria section below
due_date: null

# === TASK-SPECIFIC PROPERTIES ===
activity: DESIGN
original_estimate: 2
remaining_work: 2
time_spent: 0

# === ORCHESTRATION ===
phase: 3
barrier: null
execution_mode: "PARALLEL_WITH_TASK_037_038"
ps_agent: "ps-architect"
blocked_by: "BARRIER-2"
```

---

## Content

### Description

Design the integration between the context injection mechanism and Jerry's orchestration infrastructure:

**Integration Points:**
1. **SKILL.md** - How to declare context injection capabilities
2. **ORCHESTRATION_PLAN.yaml** - Schema extension for context_injection section
3. **ORCHESTRATION.yaml** - State tracking for injected contexts
4. **Agent Invocation** - How orchestrator passes context to agents
5. **Error Propagation** - How injection failures are handled

### Integration Design Scope

```
CONTEXT INJECTION INTEGRATION POINTS
════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────┐
│                           SKILL.md                                   │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ context_injection:                                           │   │
│  │   supported: true                                            │   │
│  │   domains: [legal, sales, engineering]                       │   │
│  │   schema: $ref: context-injection-schema.json               │   │
│  └─────────────────────────────────────────────────────────────┘   │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATION_PLAN.yaml                           │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ context_injection:                                           │   │
│  │   enabled: true                                              │   │
│  │   domain: "legal"                                            │   │
│  │   context_files:                                             │   │
│  │     - path: contexts/legal-terms.yaml                       │   │
│  │   prompt_overrides:                                          │   │
│  │     ts-extractor:                                            │   │
│  │       template: prompts/legal-extraction.md                 │   │
│  └─────────────────────────────────────────────────────────────┘   │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      AGENT INVOCATION                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ Task(                                                        │   │
│  │   prompt=merged_prompt,  # Base + injected context          │   │
│  │   context=context_payload,                                   │   │
│  │   ...                                                        │   │
│  │ )                                                            │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

### Acceptance Criteria

- [ ] **AC-001:** SKILL.md context_injection section schema defined
- [ ] **AC-002:** ORCHESTRATION_PLAN.yaml extension documented
- [ ] **AC-003:** ORCHESTRATION.yaml state tracking designed
- [ ] **AC-004:** Agent invocation interface specified
- [ ] **AC-005:** Error propagation flow documented
- [ ] **AC-006:** P-003 (single nesting) compliance verified
- [ ] **AC-007:** Mermaid diagrams for integration flow
- [ ] **AC-008:** Example configurations provided
- [ ] **AC-009:** Backward compatibility addressed

### Deliverables

| Deliverable | Type | Link | Status |
|-------------|------|------|--------|
| Integration Design | Design | docs/design/en006-orchestration-integration.md | PENDING |

---

## History

| Date       | Status      | Notes                          |
|------------|-------------|--------------------------------|
| 2026-01-26 | Created     | Task created for redesigned workflow |

---

*Task ID: TASK-036*
*Workflow ID: en006-ctxinj-20260126-001*
*Phase: 3 (Integration, Risk & Examples)*
