# EN-006: Context Injection Design

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** medium
> **Impact:** medium
> **Created:** 2026-01-26T00:00:00Z
> **Due:** TBD
> **Completed:**
> **Parent:** FEAT-001
> **Owner:** Claude
> **Target Sprint:** Sprint 2
> **Effort Points:** 5
> **Gate:** GATE-4 (Design Review)

---

## Summary

Design a context injection mechanism that allows existing Jerry agents (ps-researcher, ps-analyst, ps-synthesizer, etc.) to be leveraged with transcript-specific context and prompts. This is an advanced feature that enables reuse of battle-tested agents while specializing their behavior for transcript processing.

**Technical Justification:**
- Reuses proven agent implementations
- Reduces new code/agent development
- Provides flexibility for different transcript types
- Enables orchestration-driven specialization

---

## Benefit Hypothesis

**We believe that** designing a context injection mechanism for existing agents

**Will result in** flexible agent reuse without duplicating agent logic

**We will know we have succeeded when:**
- 5W2H analysis documents when/why/how users would use this
- Context injection specification is complete
- Orchestration integration is designed
- Human approval received at GATE-4

---

## Acceptance Criteria

### Definition of Done

- [ ] 5W2H analysis for context injection use cases
- [ ] Context injection specification created
- [ ] Orchestration plan integration designed
- [ ] Agent prompt template mechanism designed
- [ ] Example orchestration plans created
- [ ] ps-critic review passed
- [ ] Human approval at GATE-4

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | Who: Target users identified | [ ] |
| AC-2 | What: Mechanism clearly defined | [ ] |
| AC-3 | When: Trigger conditions specified | [ ] |
| AC-4 | Where: Integration points documented | [ ] |
| AC-5 | Why: Value proposition articulated | [ ] |
| AC-6 | How: Implementation approach designed | [ ] |
| AC-7 | How much: Performance impact assessed | [ ] |

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Owner | Effort | Blocked By | Link |
|----|-------|--------|-------|--------|------------|------|
| TASK-030 | 5W2H Analysis: Context Injection | pending | ps-analyst | 1 | EN-003 | [TASK-030](./TASK-030-5w2h-analysis.md) |
| TASK-031 | Context Injection Specification | pending | ps-architect | 2 | TASK-030 | [TASK-031](./TASK-031-context-injection-spec.md) |
| TASK-032 | Orchestration Integration Design | pending | ps-architect | 1 | TASK-031 | [TASK-032](./TASK-032-orchestration-integration.md) |
| TASK-033 | Example Orchestration Plans | pending | ps-architect | 1 | TASK-032 | [TASK-033](./TASK-033-example-plans.md) |
| TASK-034 | ps-critic Review & GATE-4 Prep | pending | ps-critic | 1 | TASK-033 | [TASK-034](./TASK-034-critic-review.md) |

### Workflow Phases

```
PHASE 1: Analysis
├── TASK-030: 5W2H Analysis (ps-analyst)
│   └── Deliverable: docs/analysis/en006-5w2h-context-injection.md

PHASE 2: Specification
├── TASK-031: Context Injection Specification (ps-architect)
│   └── Deliverables:
│       ├── docs/specs/SPEC-context-injection.md
│       └── docs/specs/schemas/context-injection-schema.json

PHASE 3: Integration Design
├── TASK-032: Orchestration Integration Design (ps-architect)
│   └── Deliverable: docs/design/en006-orchestration-integration.md

PHASE 4: Examples & Validation
├── TASK-033: Example Orchestration Plans (ps-architect)
│   └── Deliverables: docs/examples/context-injection/
└── TASK-034: ps-critic Review & GATE-4 Prep (ps-critic)
    └── Deliverable: FEAT-001--CRIT-EN006-review.md

GATE-4: Human Approval
```

### Orchestration Artifacts

| Artifact | Purpose | Location |
|----------|---------|----------|
| ORCHESTRATION_PLAN.md | Workflow strategy | [ORCHESTRATION_PLAN.md](./orchestration/ORCHESTRATION_PLAN.md) |
| ORCHESTRATION.yaml | Machine-readable state | [ORCHESTRATION.yaml](./orchestration/ORCHESTRATION.yaml) |

---

## 5W2H Analysis Framework

### Who (Target Users)

**Primary Users:**
- Power users wanting custom transcript analysis
- Developers extending transcript skill capabilities
- Teams with domain-specific entity extraction needs

**Use Cases:**
1. Legal team wants legal-specific term extraction
2. Sales team wants deal-related action item focus
3. Engineering team wants technical debt identification

### What (Mechanism Definition)

**Context Injection** is the ability to:
1. Provide domain-specific context to existing agents
2. Override default prompts with specialized versions
3. Pass artifacts between agents with additional metadata

**Components:**
- Context Payload: Domain knowledge, entity definitions, extraction rules
- Prompt Templates: Customizable agent instructions
- Artifact Metadata: Additional context attached to outputs

### When (Trigger Conditions)

**Scenarios where context injection is valuable:**
1. Processing transcripts from specialized domains
2. Needing custom entity types beyond standard set
3. Requiring specific output formats
4. Integrating with domain-specific systems

### Where (Integration Points)

```
┌─────────────────────────────────────────────────────────────────┐
│                    CONTEXT INJECTION POINTS                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ORCHESTRATION_PLAN.yaml                                        │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ context_injection:                                         │ │
│  │   domain: "transcript-legal"                              │ │
│  │   context_files:                                           │ │
│  │     - legal-terms.yaml                                    │ │
│  │     - jurisdiction-rules.md                               │ │
│  │   prompt_overrides:                                        │ │
│  │     entity_extraction: legal-entity-prompt.md             │ │
│  └───────────────────────────────────────────────────────────┘ │
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                   AGENT EXECUTION                            ││
│  │  ┌──────────────────┐    ┌──────────────────┐              ││
│  │  │  Base Agent      │ + │ Injected Context │ = Specialized ││
│  │  │  (ps-analyst)    │    │ (legal-terms)    │   Behavior    ││
│  │  └──────────────────┘    └──────────────────┘              ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Why (Value Proposition)

1. **Reuse:** Don't rebuild agent logic for each domain
2. **Flexibility:** Adapt to new domains via configuration
3. **Maintainability:** Core agents stay stable, customization is separate
4. **Testability:** Can test context configurations independently

### How (Implementation Approach)

**Phase 1 (Design):** This enabler
- Specify context payload format
- Define prompt template mechanism
- Design orchestration integration

**Phase 2 (Implementation):** EN-013 in FEAT-002
- Implement context loader
- Implement prompt merger
- Implement metadata passing

### How Much (Performance/Complexity Impact)

| Aspect | Impact | Mitigation |
|--------|--------|------------|
| Context loading | ~100-500ms | Cache context files |
| Prompt merging | ~10ms | Pre-compile templates |
| Metadata overhead | ~5% token increase | Optimize payload |

---

## Example Orchestration Plan

```yaml
# ORCHESTRATION_PLAN: legal-transcript-analysis.yaml

orchestration:
  name: "Legal Transcript Analysis"
  version: "1.0.0"

context_injection:
  domain: "legal"
  context_files:
    - path: contexts/legal-terms.yaml
      type: entity_definitions
    - path: contexts/legal-extraction-rules.md
      type: extraction_rules
  prompt_overrides:
    entity_extraction:
      template: prompts/legal-entity-extraction.md
      variables:
        jurisdiction: "{{jurisdiction}}"
        case_type: "{{case_type}}"

pipeline:
  - stage: parse
    agent: transcript-parser
    # No context injection - standard parsing

  - stage: extract
    agent: ps-analyst  # Existing Jerry agent
    context_injection: true  # Apply legal context

  - stage: synthesize
    agent: ps-synthesizer  # Existing Jerry agent
    context_injection: true
```

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-001: Analysis & Design](../FEAT-001-analysis-design.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | EN-003 | Requirements inform use cases |
| Depends On | EN-004 | ADRs guide mechanism design |
| Blocks | EN-013 | Implementation needs this design |

### Related Enablers

- EN-013: Context Injection Implementation (FEAT-002)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-26 | Claude | pending | Enabler created |
| 2026-01-26 | Claude | pending | Task files created (TASK-030..034), orchestration artifacts added |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Product Backlog Item (tagged Architecture) |
| **SAFe** | Enabler Story |
| **JIRA** | Task |
