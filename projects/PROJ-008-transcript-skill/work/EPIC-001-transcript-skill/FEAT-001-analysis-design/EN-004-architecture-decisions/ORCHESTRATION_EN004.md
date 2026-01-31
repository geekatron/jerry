# ORCHESTRATION_PLAN: EN-004 Architecture Decision Records

> **Document ID:** PROJ-008-EN004-ORCH-PLAN
> **Project:** PROJ-008-transcript-skill
> **Workflow ID:** `en004-adr-20260126-001`
> **Status:** ACTIVE
> **Version:** 1.0
> **Created:** 2026-01-26T00:00:00Z
> **Last Updated:** 2026-01-26T00:00:00Z

---

## 1. Executive Summary

This orchestration plan coordinates the creation of 5 Architecture Decision Records (ADRs) for the Transcript Skill using a sequential workflow with feedback-critic loops. Each ADR follows a three-wave process: deep research, drafting, and iterative review until quality threshold is met.

**Current State:** Ready to execute
**Orchestration Pattern:** Sequential with Feedback-Critic Loops

### 1.1 Workflow Identification

| Field | Value | Source |
|-------|-------|--------|
| Workflow ID | `en004-adr-20260126-001` | auto |
| ID Format | `{purpose}-{YYYYMMDD}-{NNN}` | semantic-date-seq |
| Base Path | `projects/PROJ-008-transcript-skill/work/EPIC-001-transcript-skill/FEAT-001-analysis-design/EN-004-architecture-decisions/` | Dynamic |
| ADR Output | `docs/adrs/` | Repository root |

**Quality Gate:** All ADRs must achieve quality score >= 0.90 from ps-critic

---

## 2. Workflow Architecture

### 2.1 Pipeline Diagram

```
+=============================================================================+
|           EN-004 ARCHITECTURE DECISIONS ORCHESTRATION WORKFLOW              |
+=============================================================================+
|                                                                              |
|  For each ADR (ADR-001 → ADR-005):                                          |
|                                                                              |
|  ┌────────────────────────────────────────────────────────────────────────┐ |
|  │                           WAVE 1: RESEARCH                              │ |
|  │                                                                         │ |
|  │    ┌─────────────────────────────────────────────────────────────────┐ │ |
|  │    │                      ps-researcher                                │ │ |
|  │    │  • Deep research on ADR topic                                    │ │ |
|  │    │  • Context7 documentation lookup                                 │ │ |
|  │    │  • Web search for industry best practices                        │ │ |
|  │    │  • Existing Jerry patterns analysis                              │ │ |
|  │    │  • EN-003 requirements alignment check                           │ │ |
|  │    │                                                                   │ │ |
|  │    │  OUTPUT: research/{adr-id}-research.md                           │ │ |
|  │    └─────────────────────────────────────────────────────────────────┘ │ |
|  │                                    │                                    │ |
|  │                                    ▼                                    │ |
|  └────────────────────────────────────┼────────────────────────────────────┘ |
|                                       │                                      |
|  ┌────────────────────────────────────┼────────────────────────────────────┐ |
|  │                           WAVE 2: DRAFT                                 │ |
|  │                                    │                                    │ |
|  │    ┌───────────────────────────────┴─────────────────────────────────┐ │ |
|  │    │                      ps-architect                                 │ │ |
|  │    │  • Analyze research findings                                     │ │ |
|  │    │  • Define 3+ options with pros/cons                              │ │ |
|  │    │  • Make decision with rationale                                  │ │ |
|  │    │  • Document consequences (positive, negative, neutral)           │ │ |
|  │    │  • Identify risks and mitigations                                │ │ |
|  │    │                                                                   │ │ |
|  │    │  OUTPUT: docs/adrs/ADR-{NNN}-{slug}.md                           │ │ |
|  │    └─────────────────────────────────────────────────────────────────┘ │ |
|  │                                    │                                    │ |
|  │                                    ▼                                    │ |
|  └────────────────────────────────────┼────────────────────────────────────┘ |
|                                       │                                      |
|  ┌────────────────────────────────────┼────────────────────────────────────┐ |
|  │                          WAVE 3: REVIEW                                 │ |
|  │                                    │                                    │ |
|  │    ┌───────────────────────────────┴─────────────────────────────────┐ │ |
|  │    │                       ps-critic                                   │ │ |
|  │    │  • Template compliance check                                     │ │ |
|  │    │  • Content quality assessment                                    │ │ |
|  │    │  • Options analysis validation                                   │ │ |
|  │    │  • Decision rationale clarity                                    │ │ |
|  │    │  • Requirements alignment check                                  │ │ |
|  │    │                                                                   │ │ |
|  │    │  OUTPUT: review/{adr-id}-review.md                               │ │ |
|  │    │  SCORE: 0.00 - 1.00                                              │ │ |
|  │    └─────────────────────────────────────────────────────────────────┘ │ |
|  │                                    │                                    │ |
|  │                                    ▼                                    │ |
|  │                         ┌──────────────────┐                            │ |
|  │                         │ Quality >= 0.90? │                            │ |
|  │                         └────────┬─────────┘                            │ |
|  │                              NO  │  YES                                 │ |
|  │                         ┌────────┴────────┐                             │ |
|  │                         ▼                 ▼                             │ |
|  │                    ┌─────────┐      ┌───────────┐                       │ |
|  │                    │ REVISE  │      │CHECKPOINT │                       │ |
|  │                    │ Loop to │      │Next ADR or│                       │ |
|  │                    │ Wave 2  │      │ TASK-006  │                       │ |
|  │                    └─────────┘      └───────────┘                       │ |
|  │                                                                         │ |
|  └─────────────────────────────────────────────────────────────────────────┘ |
|                                                                              |
|  After ALL 5 ADRs complete (quality >= 0.90 each):                          |
|                                                                              |
|  ┌─────────────────────────────────────────────────────────────────────────┐ |
|  │                     TASK-006: FINAL ps-critic REVIEW                    │ |
|  │                                                                         │ |
|  │  • Cross-ADR consistency check                                          │ |
|  │  • Inter-ADR reference validation                                       │ |
|  │  • Requirements coverage verification                                   │ |
|  │  • Overall architecture coherence                                       │ |
|  │                                                                         │ |
|  │  OUTPUT: review/EN-004-final-review.md                                  │ |
|  │  AGGREGATE SCORE: Average of all 5 ADR scores                          │ |
|  └───────────────────────────────┬─────────────────────────────────────────┘ |
|                                  │                                           |
|                                  ▼                                           |
|  ╔═══════════════════════════════════════════════════════════════════════╗  |
|  ║                    ★ GATE-3: Architecture Review ★                     ║  |
|  ║                      (Human Approval Required)                         ║  |
|  ║                                                                        ║  |
|  ║  Deliverables:                                                         ║  |
|  ║  • ADR-001: Agent Architecture                                         ║  |
|  ║  • ADR-002: Artifact Structure & Token Management                      ║  |
|  ║  • ADR-003: Bidirectional Deep Linking                                 ║  |
|  ║  • ADR-004: File Splitting Strategy                                    ║  |
|  ║  • ADR-005: Agent Implementation Approach                              ║  |
|  ║  • EN-004 Final Review Report                                          ║  |
|  ╚═══════════════════════════════════════════════════════════════════════╝  |
|                                                                              |
+=============================================================================+
```

### 2.2 Orchestration Pattern Classification

| Pattern | Applied | Description |
|---------|---------|-------------|
| Sequential | Yes | ADRs execute in dependency order |
| Concurrent | No | Single ADR at a time |
| Feedback Loop | Yes | Revise until quality >= 0.90 |
| Checkpointing | Yes | After each ADR passes review |

---

## 3. ADR Execution Order

ADRs are executed in dependency order:

```
ADR-001: Agent Architecture
    │
    ├─────────────────────────┐
    │                         │
    ▼                         ▼
ADR-002: Artifact          ADR-005: Agent
Structure                  Implementation
    │                         (depends on ADR-001)
    │
    ├─────────────────────────┐
    │                         │
    ▼                         ▼
ADR-003: Bidirectional    ADR-004: File
Linking                   Splitting
(depends on ADR-002)      (depends on ADR-002)
    │                         │
    └───────────┬─────────────┘
                │
                ▼
         TASK-006: Final
         ps-critic Review
                │
                ▼
            ★ GATE-3 ★
```

**Execution Sequence:**
1. ADR-001 (Agent Architecture) - Foundation for all other ADRs
2. ADR-002 (Artifact Structure) - Depends on ADR-001
3. ADR-003 (Bidirectional Linking) - Depends on ADR-002
4. ADR-004 (File Splitting) - Depends on ADR-002
5. ADR-005 (Agent Implementation) - Depends on ADR-001
6. TASK-006 (Final Review) - Depends on all 5 ADRs

---

## 4. Agent Registry

### 4.1 Research Agents (Wave 1)

| Agent ID | ADR | Role | Output Artifact |
|----------|-----|------|-----------------|
| ps-r-001 | ADR-001 | Research agent architecture patterns | research/adr-001-research.md |
| ps-r-002 | ADR-002 | Research artifact structure best practices | research/adr-002-research.md |
| ps-r-003 | ADR-003 | Research bidirectional linking patterns | research/adr-003-research.md |
| ps-r-004 | ADR-004 | Research file splitting strategies | research/adr-004-research.md |
| ps-r-005 | ADR-005 | Research agent implementation approaches | research/adr-005-research.md |

### 4.2 Architecture Agents (Wave 2)

| Agent ID | ADR | Role | Output Artifact |
|----------|-----|------|-----------------|
| ps-a-001 | ADR-001 | Draft ADR using template | docs/adrs/ADR-001-agent-architecture.md |
| ps-a-002 | ADR-002 | Draft ADR using template | docs/adrs/ADR-002-artifact-structure.md |
| ps-a-003 | ADR-003 | Draft ADR using template | docs/adrs/ADR-003-bidirectional-linking.md |
| ps-a-004 | ADR-004 | Draft ADR using template | docs/adrs/ADR-004-file-splitting.md |
| ps-a-005 | ADR-005 | Draft ADR using template | docs/adrs/ADR-005-agent-implementation.md |

### 4.3 Review Agents (Wave 3)

| Agent ID | ADR | Role | Output Artifact |
|----------|-----|------|-----------------|
| ps-c-001 | ADR-001 | Review and score | review/adr-001-review.md |
| ps-c-002 | ADR-002 | Review and score | review/adr-002-review.md |
| ps-c-003 | ADR-003 | Review and score | review/adr-003-review.md |
| ps-c-004 | ADR-004 | Review and score | review/adr-004-review.md |
| ps-c-005 | ADR-005 | Review and score | review/adr-005-review.md |
| ps-c-006 | ALL | Final cross-ADR review | review/EN-004-final-review.md |

---

## 5. Feedback Loop Protocol

### 5.1 Quality Threshold

**Minimum Score:** 0.90

### 5.2 Scoring Criteria

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Template Compliance | 20% | Follows ADR template structure |
| Options Analysis | 25% | 3+ options with clear pros/cons |
| Decision Rationale | 25% | Clear reasoning for choice |
| Requirements Alignment | 15% | Traces to EN-003 requirements |
| Consequences Coverage | 15% | Positive, negative, neutral documented |

### 5.3 Feedback Loop Rules

```
IF score < 0.90:
  1. Document specific feedback in review artifact
  2. Return to ps-architect (Wave 2)
  3. ps-architect revises ADR based on feedback
  4. Return to ps-critic (Wave 3)
  5. Repeat until score >= 0.90 or max_iterations (3) reached

IF max_iterations reached AND score < 0.90:
  1. Escalate to human for decision
  2. Human may: approve as-is, provide guidance, or reject
```

### 5.4 Revision Tracking

Each ADR tracks revision history:

```yaml
revisions:
  - iteration: 1
    score: 0.72
    feedback: "Missing risk analysis section"
  - iteration: 2
    score: 0.88
    feedback: "Improve Option 2 pros/cons detail"
  - iteration: 3
    score: 0.93
    feedback: "PASSED - Minor suggestion: add citation for pattern"
```

---

## 6. Checkpointing Strategy

### 6.1 Checkpoint Triggers

| Trigger | When | Recovery Point |
|---------|------|----------------|
| ADR_PASSED | Quality >= 0.90 | Start of next ADR |
| WAVE_COMPLETE | After each wave | Current wave complete |
| ITERATION_END | After each feedback loop | Current iteration |
| MANUAL | User-triggered | Current state |

### 6.2 Checkpoint Contents

```yaml
checkpoint:
  id: "CP-EN004-{ADR}-{iteration}"
  timestamp: "2026-01-26T12:00:00Z"
  adr_id: "ADR-001"
  current_wave: 3
  iteration: 2
  score: 0.88
  artifacts:
    - research/adr-001-research.md
    - docs/adrs/ADR-001-agent-architecture.md (v2)
    - review/adr-001-review.md (iteration 2)
  next_action: "ps-architect revise based on feedback"
```

---

## 7. Execution Constraints

### 7.1 Hard Constraints (Jerry Constitution)

| Constraint | ID | Enforcement |
|------------|----|----|
| Single agent nesting | P-003 | Main context → worker agents only |
| File persistence | P-002 | All artifacts persisted to filesystem |
| No deception | P-022 | Transparent quality scores |
| User authority | P-020 | Human approves GATE-3 |

### 7.2 Soft Constraints

| Constraint | Value | Rationale |
|------------|-------|-----------|
| Max feedback iterations | 3 | Prevent infinite loops |
| Min quality score | 0.90 | Ensure ADR quality |
| Research depth | Deep | Context7 + Web + Jerry patterns |

---

## 8. Success Criteria

### 8.1 Per-ADR Exit Criteria

| Criterion | Validation |
|-----------|------------|
| Quality score >= 0.90 | ps-critic final score |
| Template compliance | All sections present |
| 3+ options documented | Count in ADR |
| Rationale clear | Human-readable justification |
| Requirements traced | References to EN-003 |

### 8.2 EN-004 Completion Criteria

| Criterion | Validation |
|-----------|------------|
| All 5 ADRs complete | Status = COMPLETE for each |
| All scores >= 0.90 | ps-critic final scores |
| Cross-ADR consistency | TASK-006 review passed |
| GATE-3 approved | Human approval received |

---

## 9. Artifact Locations

### 9.1 Input Artifacts

| Artifact | Location |
|----------|----------|
| ADR Template | docs/knowledge/exemplars/templates/adr.md |
| Requirements Spec | EN-003-requirements-synthesis/synthesis/ |
| Prior Research | EN-001-market-analysis/, EN-002-technical-standards/ |

### 9.2 Output Artifacts

| Category | Location |
|----------|----------|
| Research | EN-004-architecture-decisions/research/ |
| ADRs | docs/adrs/ |
| Reviews | EN-004-architecture-decisions/review/ |
| State | EN-004-architecture-decisions/ORCHESTRATION_EN004.yaml |

---

## 10. Resumption Context

### 10.1 Current Execution State

```
WORKFLOW STATUS AS OF 2026-01-26
================================

ADR-001: Agent Architecture
  Wave 1 (Research):    PENDING
  Wave 2 (Draft):       PENDING
  Wave 3 (Review):      PENDING
  Score:                --

ADR-002: Artifact Structure
  Status:               BLOCKED (depends on ADR-001)

ADR-003: Bidirectional Linking
  Status:               BLOCKED (depends on ADR-002)

ADR-004: File Splitting
  Status:               BLOCKED (depends on ADR-002)

ADR-005: Agent Implementation
  Status:               BLOCKED (depends on ADR-001)

TASK-006: Final Review
  Status:               BLOCKED (depends on all ADRs)
```

### 10.2 Next Actions

1. Execute Wave 1 for ADR-001: ps-researcher deep research
2. Execute Wave 2 for ADR-001: ps-architect draft ADR
3. Execute Wave 3 for ADR-001: ps-critic review
4. Iterate until ADR-001 score >= 0.90
5. Proceed to ADR-002 (depends on ADR-001)

---

## 11. Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-26 | Claude | Initial EN-004 orchestration plan created |

---

*Document ID: PROJ-008-EN004-ORCH-PLAN*
*Workflow ID: en004-adr-20260126-001*
*Version: 1.0*
*Constitutional Compliance: Jerry Constitution v1.0*
