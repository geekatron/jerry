# EN-004: Architecture Decision Records

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-01-26 (ps-architect)
PURPOSE: Technical/infrastructure work that enables future value delivery

DESCRIPTION:
  Technical/infrastructure work that enables future value delivery.
  SAFe concept for architectural runway, tech debt, etc.

EXTENDS: DeliveryItem -> WorkItem

NOTE: Enabler is SAFe's formal construct for non-feature work.
      ADO approximates via ValueArea. JIRA uses labeling.
      Trace: CROSS-DOMAIN-SYNTHESIS.md Section 6.1 (Recommendation 3)
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Enabler Type:** architecture
> **Created:** 2026-01-26T00:00:00Z
> **Due:** TBD
> **Completed:**
> **Parent:** FEAT-001
> **Owner:** Claude
> **Effort:** 8

<!--
STATUS VALUES: pending | in_progress | completed
PRIORITY VALUES: critical | high | medium | low
IMPACT VALUES: critical | high | medium | low
ENABLER_TYPE VALUES: infrastructure | exploration | architecture | compliance
TIMESTAMPS: Use ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)
EFFORT: Story points (1-13 Fibonacci recommended)
-->

---

## Template Structure

```
+---------------------------------------------------------------------+
|                        ENABLER TEMPLATE                              |
|                    Version 1.0.0 (ONTOLOGY-aligned)                  |
+---------------------------------------------------------------------+
| Header Block (blockquote)                                            |
|   |-- type: "enabler"                          [COMPLIANT]           |
|   |-- status: pending                          [COMPLIANT]           |
|   |-- priority: high                           [COMPLIANT]           |
|   |-- impact: high                             [COMPLIANT]           |
|   |-- enabler_type: architecture               [COMPLIANT]           |
|   |-- created: 2026-01-26T00:00:00Z            [COMPLIANT]           |
|   |-- due: TBD                                 [COMPLIANT]           |
|   |-- completed: (empty)                       [COMPLIANT]           |
|   |-- parent: FEAT-001                         [COMPLIANT]           |
|   |-- owner: Claude                            [COMPLIANT]           |
|   +-- effort: 8                                [COMPLIANT]           |
+---------------------------------------------------------------------+
| Summary Section                                 [COMPLIANT]          |
| Problem Statement                               [COMPLIANT]          |
| Business Value                                  [COMPLIANT]          |
| Technical Approach                              [COMPLIANT]          |
| NFRs Addressed                                  [COMPLIANT]          |
| Children (Tasks)                                [COMPLIANT]          |
| Progress Summary                                [COMPLIANT]          |
| Acceptance Criteria                             [COMPLIANT]          |
| Risks and Mitigations                           [COMPLIANT]          |
| History                                         [COMPLIANT]          |
+---------------------------------------------------------------------+

CONTAINMENT:
  allowed_parents: [Feature, Epic]
  allowed_children: [Task]
  max_depth: 1
```

---

## Frontmatter

```yaml
# =============================================================================
# ENABLER WORK ITEM
# Source: ONTOLOGY-v1.md Section 3.4.9 (Enabler Entity Schema)
# =============================================================================

# Identity (inherited from WorkItem - Section 2.1)
id: "EN-004"                              # Required, immutable - Format: EN-NNN
work_type: ENABLER                        # Required, immutable - Discriminator
title: "Architecture Decision Records"    # Required, 1-500 chars

# Classification
classification: ENABLER                   # INV-EN02: classification should be ENABLER

# State (see State Machine below)
status: pending                           # Required - pending | in_progress | completed
resolution: null                          # Optional - Set when status is completed

# Priority & Impact
priority: high                            # Required - critical | high | medium | low
impact: high                              # Required - critical | high | medium | low

# People
assignee: "Claude"                        # Optional - Engineer responsible
created_by: "Claude"                      # Required, auto-populated

# Timestamps (auto-managed)
created_at: "2026-01-26T00:00:00Z"        # Required, auto, immutable (ISO 8601)
updated_at: "2026-01-26T00:00:00Z"        # Required, auto (ISO 8601)
completed_at: null                        # Optional - When enabler completed (ISO 8601)

# Hierarchy
parent_id: "FEAT-001"                     # Required - Feature or Epic ID

# Tags
tags:
  - enabler
  - architecture
  - adr
  - transcript-skill
  - gate-3

# =============================================================================
# DELIVERY ITEM PROPERTIES (Section 3.3.2)
# =============================================================================
effort: 8                                 # Story points
acceptance_criteria: |
  - ADR-001 through ADR-005 created using proper template
  - All ADRs reviewed by ps-critic
  - Human approval at GATE-3
due_date: null                            # Optional - ISO 8601 date

# =============================================================================
# ENABLER-SPECIFIC PROPERTIES (Section 3.4.9)
# =============================================================================
enabler_type: architecture                # REQUIRED: infrastructure | exploration | architecture | compliance
nfrs:
  - "NFR-001: 35K token limit"
  - "NFR-002: Modular agent architecture"
technical_debt_category: null             # Optional - Category of tech debt being addressed
```

---

## Summary

Create formal Architecture Decision Records (ADRs) documenting key technical decisions for the Transcript Skill. Each ADR captures the context, decision, and consequences to provide traceability and enable future maintainers to understand why decisions were made.

**Technical Scope:**
- ADR-001: Agent Architecture - Define agent structure and communication
- ADR-002: Artifact Structure & Token Management - Define output layout and limits
- ADR-003: Bidirectional Deep Linking - Define linking strategy
- ADR-004: File Splitting Strategy - Define how to handle large artifacts
- ADR-005: Agent Implementation Approach - Define phased implementation strategy

---

## Enabler Type Classification

<!--
Source: ONTOLOGY-v1.md Section 3.4.9 (Enabler.specific.enabler_type)
-->

| Type | Description | Examples |
|------|-------------|----------|
| **INFRASTRUCTURE** | Platform, tooling, DevOps enablers | CI/CD pipelines, monitoring setup |
| **EXPLORATION** | Research and proof-of-concept work | Technology spikes, prototypes |
| **ARCHITECTURE** | Architectural runway and design work | Service decomposition, API design |
| **COMPLIANCE** | Security, regulatory, and compliance requirements | GDPR implementation, SOC2 controls |

**This Enabler Type:** ARCHITECTURE

---

## Problem Statement

The Transcript Skill requires multiple architectural decisions before implementation can begin. Without formal ADRs:

1. **Decision Traceability Lost**: Future maintainers won't understand WHY decisions were made
2. **Re-litigation Risk**: Same decisions may be debated repeatedly
3. **Implementation Ambiguity**: Developers may interpret requirements differently
4. **Technical Debt**: Undocumented decisions become implicit knowledge that leaves with team members

**Key Questions Requiring ADRs:**
- What agent architecture should we use?
- How should artifacts be structured to stay under token limits?
- How do we maintain traceability via deep linking?
- How do we handle artifacts that exceed size limits?
- Should we use prompt-based or Python-based agents?

---

## Business Value

Formal ADRs provide foundational architectural guidance that enables:

1. **Implementation Clarity**: Developers have clear direction
2. **Maintainability**: Future teams understand the "why"
3. **Quality**: Decisions are reviewed and validated
4. **Traceability**: All decisions link to requirements (EN-003)

### Features Unlocked

- FEAT-002: Implementation (blocked until ADRs complete)
- EN-005: Design Documentation (needs ADR context)
- EN-006: Context Injection Design (needs ADR context)

---

## Technical Approach

Use the @problem-solving skill with specialized agents to research and create each ADR:

1. **Research Phase**: ps-researcher agent gathers industry best practices
2. **Architecture Phase**: ps-architect agent synthesizes options and drafts ADR
3. **Review Phase**: ps-critic agent provides feedback for revision
4. **Iteration**: Feedback loop until quality threshold met (0.90+)

### Architecture Diagram

```
+==============================================================================+
|                     EN-004 ADR CREATION WORKFLOW                              |
+==============================================================================+
|                                                                               |
|  For each ADR (001-005):                                                     |
|                                                                               |
|  ┌─────────────────────────────────────────────────────────────────────────┐ |
|  │                                                                          │ |
|  │  ┌────────────────┐     ┌────────────────┐     ┌────────────────┐       │ |
|  │  │  ps-researcher │────►│  ps-architect  │────►│   ps-critic    │       │ |
|  │  │                │     │                │     │                │       │ |
|  │  │  Deep Research │     │  Draft ADR     │     │  Review &      │       │ |
|  │  │  - EN-001/002  │     │  - 3+ Options  │     │  Feedback      │       │ |
|  │  │  - EN-003 Reqs │     │  - Rationale   │     │  - Quality     │       │ |
|  │  │  - Best Prctcs │     │  - Conseqnces  │     │  - Consistency │       │ |
|  │  └────────────────┘     └────────┬───────┘     └───────┬────────┘       │ |
|  │                                  │                     │                 │ |
|  │                                  │    ┌────────────────┘                 │ |
|  │                                  │    │                                  │ |
|  │                                  ▼    ▼                                  │ |
|  │                         ┌──────────────────┐                             │ |
|  │                         │  Revision Loop   │                             │ |
|  │                         │  Until Score     │                             │ |
|  │                         │  >= 0.90         │                             │ |
|  │                         └────────┬─────────┘                             │ |
|  │                                  │                                       │ |
|  │                                  ▼                                       │ |
|  │                         ┌──────────────────┐                             │ |
|  │                         │  ADR Complete    │                             │ |
|  │                         │  → docs/adrs/    │                             │ |
|  │                         └──────────────────┘                             │ |
|  │                                                                          │ |
|  └─────────────────────────────────────────────────────────────────────────┘ |
|                                                                               |
|  After all ADRs:                                                             |
|                                                                               |
|  ┌──────────────────────────────────────────────────────────────────────┐   |
|  │                    ★ GATE-3: Architecture Review ★                    │   |
|  │                    (Human Approval Required)                          │   |
|  └──────────────────────────────────────────────────────────────────────┘   |
|                                                                               |
+==============================================================================+
```

---

## Non-Functional Requirements (NFRs) Addressed

<!--
RECOMMENDED: NFRs this enabler addresses
Source: ONTOLOGY-v1.md Section 3.4.9 (Enabler.specific.nfrs)
-->

| NFR Category | Requirement | Current State | Target State |
|--------------|-------------|---------------|--------------|
| Token Management | NFR-001: 35K token limit | Undefined | ADR-002, ADR-004 document strategy |
| Maintainability | Future maintainer understanding | No formal documentation | ADRs provide decision context |
| Traceability | Decision traceability | Implicit | Explicit via ADRs |
| Quality | Architecture review process | None | ps-critic review + GATE-3 |

---

## ADR Template Reference

> **MANDATORY:** All ADRs MUST use the repository's official ADR template.

**Template Location:** [`docs/knowledge/exemplars/templates/adr.md`](../../../../../docs/knowledge/exemplars/templates/adr.md)

**Template Format:** Michael Nygard's ADR Format (2011) with PS Integration

**Key Sections in Template:**
- **Context** - Background, Constraints, Forces
- **Options Considered** - At least 3 options with pros/cons
- **Decision** - Choice with rationale and alignment scoring
- **Consequences** - Positive, Negative, Neutral, Risks
- **Implementation** - Action items, Validation criteria
- **PS Integration** - Exploration entry linking

**Template Version:** 1.0 (Phase 38.17)

**Prior Art:**
- IETF RFC Process
- C4 Architecture Documentation
- Michael Nygard's ADR Format (2011)

---

## Planned ADRs

### ADR-001: Agent Architecture
**Scope:** Define the architecture for transcript processing agents
- Custom agents vs existing Jerry agents
- Agent responsibilities and boundaries
- Inter-agent communication patterns
- Orchestration model

### ADR-002: Artifact Structure & Token Management
**Scope:** Define output artifact structure
- Directory layout for transcript packets
- Token budget per artifact (35K limit)
- Naming conventions
- Index/manifest structure

### ADR-003: Bidirectional Deep Linking
**Scope:** Define linking strategy between artifacts
- Link format specification
- Backlinks section structure
- Anchor generation rules
- Cross-artifact navigation

### ADR-004: File Splitting Strategy
**Scope:** Define how large artifacts are split
- Split trigger criteria (token thresholds)
- Naming for split files
- Navigation between split files
- Cross-reference handling

### ADR-005: Agent Implementation Approach
**Scope:** Define phased implementation strategy
- Phase 1: Prompt-based (YAML/MD)
- Phase 2: Python-based (if needed)
- Migration path between phases
- Hybrid model considerations

---

## Children (Tasks)

<!--
OPTIONAL: Track child tasks.
Source: ONTOLOGY-v1.md Section 3.4.9 - containment
allowed_children: [Task]
max_depth: 1
-->

### Task Inventory

| ID | Title | Status | Effort | Owner | Blocked By |
|----|-------|--------|--------|-------|------------|
| [TASK-001](./TASK-001-agent-architecture-adr.md) | Create ADR-001: Agent Architecture | pending | 2 | ps-architect | - |
| [TASK-002](./TASK-002-artifact-structure-adr.md) | Create ADR-002: Artifact Structure | pending | 2 | ps-architect | TASK-001 |
| [TASK-003](./TASK-003-bidirectional-linking-adr.md) | Create ADR-003: Bidirectional Linking | pending | 1 | ps-architect | TASK-002 |
| [TASK-004](./TASK-004-file-splitting-adr.md) | Create ADR-004: File Splitting Strategy | pending | 1 | ps-architect | TASK-002, TASK-003 |
| [TASK-005](./TASK-005-agent-implementation-adr.md) | Create ADR-005: Agent Implementation | pending | 1 | ps-architect | TASK-001 |
| [TASK-006](./TASK-006-ps-critic-adr-review.md) | ps-critic ADR Review | pending | 1 | ps-critic | TASK-001..005 |

### Task Dependency Graph

```
TASK-001 (Agent Architecture)
    │
    ├──────────────────┐
    │                  │
    ▼                  ▼
TASK-002          TASK-005
(Artifact)        (Implementation)
    │
    ├──────────────────┐
    │                  │
    ▼                  ▼
TASK-003          TASK-004
(Linking)         (Splitting)
    │                  │
    └──────────────────┘
             │
             ▼
         TASK-006
      (ps-critic Review)
             │
             ▼
         ★ GATE-3 ★
```

---

## Progress Summary

<!--
REQUIRED: Track overall enabler progress.
Update regularly as tasks progress.
-->

### Status Overview

```
+------------------------------------------------------------------+
|                   ENABLER PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Tasks:     [....................] 0% (0/6 completed)             |
| Effort:    [....................] 0% (0/8 points completed)      |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                             |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Tasks** | 6 |
| **Completed Tasks** | 0 |
| **Total Effort (points)** | 8 |
| **Completed Effort** | 0 |
| **Completion %** | 0% |

---

## Acceptance Criteria

<!--
REQUIRED: Conditions for enabler to be considered complete.
Should be defined before status is in_progress (INV-D02).
-->

### Definition of Done

- [ ] ADR-001: Agent Architecture created and reviewed
- [ ] ADR-002: Artifact Structure & Token Management created and reviewed
- [ ] ADR-003: Bidirectional Deep Linking created and reviewed
- [ ] ADR-004: File Splitting Strategy created and reviewed
- [ ] ADR-005: Agent Implementation Approach created and reviewed
- [ ] All ADRs follow `docs/knowledge/exemplars/templates/adr.md`
- [ ] ps-critic review passed (quality score >= 0.90)
- [ ] Human approval at GATE-3

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | Each ADR has Context section with problem statement | [ ] |
| AC-2 | Each ADR has Decision section with clear choice | [ ] |
| AC-3 | Each ADR has Consequences section (pros/cons/neutral) | [ ] |
| AC-4 | Each ADR references supporting research (EN-001, EN-002, EN-003) | [ ] |
| AC-5 | ADRs are numbered and dated | [ ] |
| AC-6 | At least 3 alternative options documented per ADR | [ ] |
| AC-7 | All ADRs are consistent with each other | [ ] |
| AC-8 | ADRs stored in `docs/adrs/` directory | [ ] |

---

## Evidence

<!--
COMPLETION EVIDENCE: Verification that this enabler meets technical requirements.
Include NFR measurements, performance benchmarks, and technical proof points.
This is audit trail evidence (proving work was done), not knowledge evidence (research citations).
-->

### Deliverables

| Deliverable | Type | Description | Link |
|-------------|------|-------------|------|
| ADR-001 | Architecture Decision Record | Agent Architecture | [docs/adrs/ADR-001-agent-architecture.md](../../../../../docs/adrs/ADR-001-agent-architecture.md) |
| ADR-002 | Architecture Decision Record | Artifact Structure | [docs/adrs/ADR-002-artifact-structure.md](../../../../../docs/adrs/ADR-002-artifact-structure.md) |
| ADR-003 | Architecture Decision Record | Bidirectional Linking | [docs/adrs/ADR-003-bidirectional-linking.md](../../../../../docs/adrs/ADR-003-bidirectional-linking.md) |
| ADR-004 | Architecture Decision Record | File Splitting | [docs/adrs/ADR-004-file-splitting.md](../../../../../docs/adrs/ADR-004-file-splitting.md) |
| ADR-005 | Architecture Decision Record | Agent Implementation | [docs/adrs/ADR-005-agent-implementation.md](../../../../../docs/adrs/ADR-005-agent-implementation.md) |
| Review Report | Review Document | ps-critic ADR Review | TBD |

### Technical Verification

| Criterion | Verification Method | Evidence | Verified By | Date |
|-----------|---------------------|----------|-------------|------|
| Template Compliance | Manual review | ADR structure matches template | ps-critic | TBD |
| Option Analysis | Manual review | 3+ options per ADR | ps-critic | TBD |
| Quality Score | Automated scoring | Score >= 0.90 | ps-critic | TBD |
| Human Approval | GATE-3 review | Approval recorded | Human | TBD |

### Verification Checklist

- [ ] All acceptance criteria verified
- [ ] All tasks completed
- [ ] ps-critic quality score >= 0.90
- [ ] Technical review complete
- [ ] Human approval at GATE-3

---

## Implementation Plan

<!--
RECOMMENDED: Phased implementation approach
-->

### Phase 1: Research & Draft (TASK-001 through TASK-005)

For each ADR:
1. Use ps-researcher to gather research from EN-001, EN-002, EN-003
2. Use ps-architect to draft ADR with 3+ options
3. Use ps-critic for feedback loop
4. Iterate until quality score >= 0.90
5. Persist to `docs/adrs/`

### Phase 2: Final Review (TASK-006)

1. ps-critic comprehensive review of all 5 ADRs
2. Check inter-ADR consistency
3. Generate final review report
4. Submit for GATE-3 human approval

---

## Risks and Mitigations

<!--
RECOMMENDED: Known risks and mitigation strategies
-->

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Options not comprehensive enough | Medium | High | ps-researcher deep research; multiple sources |
| ADRs inconsistent with each other | Medium | Medium | ps-critic cross-ADR consistency check |
| Research from EN-001/002 insufficient | Low | High | Additional web research via @problem-solving |
| Quality score below threshold | Medium | Low | Iteration with feedback loop until 0.90+ |

---

## Dependencies

<!--
RECOMMENDED: Dependencies and items this enabler unlocks
-->

### Depends On

- [EN-003: Requirements Synthesis](../EN-003-requirements-synthesis/EN-003-requirements-synthesis.md) - Requirements inform architecture decisions
- [EN-001: Market Analysis](../EN-001-market-analysis/EN-001-market-analysis.md) - Competitive research informs options
- [EN-002: Technical Standards](../EN-002-technical-standards/EN-002-technical-standards.md) - Technical constraints inform decisions

### Enables

- [EN-005: Design Documentation](../EN-005-design-documentation/EN-005-design-documentation.md) - Design needs ADR context
- [EN-006: Context Injection Design](../EN-006-context-injection-design/EN-006-context-injection-design.md) - Context design needs ADRs
- [FEAT-002: Implementation](../../FEAT-002-implementation/FEAT-002-implementation.md) - Implementation blocked until ADRs complete

---

## State Machine Reference

<!--
Source: ONTOLOGY-v1.md Section 3.4.9 - state_machine
Simplified to match worktracker conventions.
-->

```
+-------------------------------------------------------------------+
|                   ENABLER STATE MACHINE                            |
+-------------------------------------------------------------------+
|                                                                    |
|   +---------+     +-------------+     +-----------+               |
|   | PENDING |---->| IN_PROGRESS |---->| COMPLETED |               |
|   +---------+     +-------------+     +-----------+               |
|        |               |                   |                       |
|        v               v                   v                       |
|   (Planning)     (Implementing)      (Delivered)                  |
|                                                                    |
+-------------------------------------------------------------------+

Allowed Transitions:
- pending -> in_progress: Start implementation
- in_progress -> completed: All tasks done + GATE-3 approved
- in_progress -> pending: Deprioritized
- completed -> in_progress: Reopened
```

---

## Containment Rules

<!--
Source: ONTOLOGY-v1.md Section 3.4.9 (Enabler.containment)
-->

| Rule | Value |
|------|-------|
| **Allowed Children** | Task |
| **Allowed Parents** | Feature, Epic |
| **Max Depth** | 1 |

### Hierarchy Diagram

```
FEAT-001: Analysis & Design
|
+-- EN-004: Architecture Decision Records (this enabler)
    |
    +-- TASK-001: Create ADR-001: Agent Architecture
    +-- TASK-002: Create ADR-002: Artifact Structure
    +-- TASK-003: Create ADR-003: Bidirectional Linking
    +-- TASK-004: Create ADR-004: File Splitting Strategy
    +-- TASK-005: Create ADR-005: Agent Implementation
    +-- TASK-006: ps-critic ADR Review
```

---

## Invariants

<!--
Source: ONTOLOGY-v1.md Section 3.4.9 (Enabler.invariants)
-->

- **INV-D01:** effort must be non-negative (inherited from DeliveryItem) ✓
- **INV-D02:** acceptance_criteria should be defined before in_progress (inherited) ✓
- **INV-EN01:** enabler_type is REQUIRED ✓ (architecture)
- **INV-EN02:** classification should be ENABLER ✓
- **INV-EN03:** Enabler can have Feature or Epic as parent ✓ (FEAT-001)

---

## Related Items

<!--
RECOMMENDED: Link to related work items and artifacts.
-->

### Hierarchy

- **Parent:** [FEAT-001: Analysis & Design](../FEAT-001-analysis-design.md)

### Related Items

- **Related Enabler:** [EN-003: Requirements Synthesis](../EN-003-requirements-synthesis/EN-003-requirements-synthesis.md)
- **Related Bug:** [BUG-001: Template Non-Compliance](../FEAT-001--BUG-001-template-non-compliance.md)
- **Blocks:** [EN-005: Design Documentation](../EN-005-design-documentation/EN-005-design-documentation.md)
- **Blocks:** [FEAT-002: Implementation](../../FEAT-002-implementation/FEAT-002-implementation.md)

---

## Architecture Runway Impact

<!--
OPTIONAL: For ARCHITECTURE type enablers
-->

**Current Runway:** No formal architecture decisions documented

**Post-Enabler Runway:** 5 ADRs providing foundational architecture guidance for:
- Agent structure and communication
- Artifact layout and token management
- Linking and traceability
- Scalability via file splitting
- Implementation approach flexibility

---

## History

<!--
RECOMMENDED: Track status changes and key events.
Use ISO 8601 timestamps.
-->

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-26 | Claude | pending | Enabler created |
| 2026-01-26 | Claude | pending | Updated to reference proper ADR template (BUG-001 fix) |
| 2026-01-26 | Claude | pending | Updated to full ENABLER template with enabler-scoped task IDs |
| 2026-01-26 | Claude | pending | Created 6 individual task files (TASK-001 through TASK-006) |

---

## System Mapping

<!--
Source: ONTOLOGY-v1.md Section 3.4.9 (Enabler.system_mapping)
-->

| System | Mapping |
|--------|---------|
| **Azure DevOps** | PBI with ValueArea=Architectural |
| **SAFe** | Enabler (Architecture type) |
| **JIRA** | Story with 'enabler' and 'architecture' labels |

---

<!--
DESIGN RATIONALE:
Enabler is SAFe's formal construct for non-feature work.
ADO approximates via ValueArea. JIRA uses labeling.
Modeled as first-class for SAFe compatibility.
Trace: CROSS-DOMAIN-SYNTHESIS.md Section 6.1 (Recommendation 3)

PATTERN COMPLIANCE:
- P-001: Blockquote Header [COMPLIANT]
- P-002: Summary Section [COMPLIANT]
- P-005: History/Changelog [COMPLIANT]
- P-006: ISO 8601 Timestamps [COMPLIANT]
- P-007: Horizontal Rule Separators [COMPLIANT]
- P-019: Parent Reference [COMPLIANT]
- Children Tracking Section [COMPLIANT]
- Progress Summary Section [COMPLIANT]

WORKTRACKER ALIGNMENT:
- Status values: pending, in_progress, completed (per work-items.md)
- Priority/Impact: critical, high, medium, low (per work-items.md)
-->
