# EN-005: Design Documentation

<!--
TEMPLATE: Enabler
VERSION: 2.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
UPDATED: 2026-01-26 - Aligned with ADR-001 through ADR-005
-->

> **Type:** enabler
> **Status:** awaiting_approval
> **Priority:** high
> **Impact:** high
> **Created:** 2026-01-26T00:00:00Z
> **Updated:** 2026-01-26T09:00:00Z
> **Due:** TBD
> **Completed:**
> **Parent:** FEAT-001
> **Owner:** Claude
> **Target Sprint:** Sprint 2
> **Effort Points:** 13
> **Gate:** GATE-4 (Design Review)
> **Workflow ID:** en005-tdd-20260126-001

---

## Artifact Relocation Notice (2026-01-26)

> **Per DISC-004 and DEC-002:** Implementation artifacts have been relocated to `skills/transcript/` per Claude Code best practices. TDD documents (design specs) remain in EN-005.

### Relocation Summary

| Artifact | Original Location | New Location | Status |
|----------|-------------------|--------------|--------|
| ts-parser agent | agents/ts-parser/AGENT.md | **skills/transcript/agents/ts-parser.md** | RELOCATED |
| ts-extractor agent | agents/ts-extractor/AGENT.md | **skills/transcript/agents/ts-extractor.md** | RELOCATED |
| ts-formatter agent | agents/ts-formatter/AGENT.md | **skills/transcript/agents/ts-formatter.md** | RELOCATED |
| SKILL.md orchestrator | SKILL.md | **skills/transcript/SKILL.md** | RELOCATED |
| PLAYBOOK | docs/PLAYBOOK-en005.md | **skills/transcript/docs/PLAYBOOK.md** | RELOCATED |
| RUNBOOK | docs/RUNBOOK-en005.md | **skills/transcript/docs/RUNBOOK.md** | RELOCATED |

### Artifacts Remaining in EN-005 (Design Specs)

| Artifact | Location | Purpose |
|----------|----------|---------|
| TDD-transcript-skill.md | docs/ | Overall architecture spec |
| TDD-ts-parser.md | docs/ | Parser design spec |
| TDD-ts-extractor.md | docs/ | Extractor design spec |
| TDD-ts-formatter.md | docs/ | Formatter design spec |
| ps-critic reviews | review/ | Quality review artifacts |

**Rationale:** TDD documents are design specifications that inform implementation. AGENT.md and SKILL.md files are executable implementations that belong in `skills/transcript/` per Claude Code plugin conventions.

---

## Summary

Create comprehensive design documentation for the Transcript Skill aligned with the Architecture Decision Records (ADR-001 through ADR-005). This includes Technical Design Documents (TDDs) for each agent, AGENT.md definitions, and operational documentation (PLAYBOOK/RUNBOOK).

**Technical Justification:**
- Implements ADR-001 Hybrid Architecture (3 custom agents + ps-critic)
- Documents ADR-002 Hierarchical Packet Structure
- Specifies ADR-003 Bidirectional Linking implementation
- Details ADR-004 File Splitting logic
- Creates ADR-005 prompt-based agent definitions

---

## Benefit Hypothesis

**We believe that** creating detailed design documentation aligned with all ADR decisions

**Will result in** smooth implementation with clear specifications for each component

**We will know we have succeeded when:**
- Each agent has TDD with L0/L1/L2 perspectives
- AGENT.md files follow PS_AGENT_TEMPLATE.md
- SKILL.md orchestrator integrates all agents
- PLAYBOOK enables execution
- RUNBOOK enables troubleshooting
- Human approval received at GATE-4

---

## ADR Alignment Matrix

| ADR | Decision | EN-005 Deliverables |
|-----|----------|---------------------|
| ADR-001 | Hybrid Architecture | TDD for ts-parser, ts-extractor, ts-formatter, AGENT.md files |
| ADR-002 | Hierarchical Packet | ts-formatter TDD includes packet generation |
| ADR-003 | Custom Anchors | ts-formatter TDD includes anchor registry |
| ADR-004 | Semantic Split | ts-formatter TDD includes split logic |
| ADR-005 | Phased Implementation | AGENT.md (Phase 1), trigger monitoring spec |

---

## Acceptance Criteria

### Definition of Done

- [ ] TDD-001: Transcript Skill Overview complete
- [ ] TDD-002: ts-parser Agent Design complete
- [ ] TDD-003: ts-extractor Agent Design complete
- [ ] TDD-004: ts-formatter Agent Design complete
- [ ] AGENT-001: ts-parser AGENT.md created
- [ ] AGENT-002: ts-extractor AGENT.md created
- [ ] AGENT-003: ts-formatter AGENT.md created
- [ ] AGENT-004: SKILL.md orchestrator created
- [ ] OPS-001: PLAYBOOK-en005.md complete
- [ ] OPS-002: RUNBOOK-en005.md complete
- [ ] ps-critic aggregate quality score >= 0.90
- [ ] Human approval at GATE-4

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | All TDDs include L0/L1/L2 perspectives | [ ] |
| AC-2 | TDDs reference specific ADR decisions | [ ] |
| AC-3 | AGENT.md files follow PS_AGENT_TEMPLATE.md | [ ] |
| AC-4 | SKILL.md maintains P-003 single nesting | [ ] |
| AC-5 | ts-formatter implements ADR-002 packet structure | [ ] |
| AC-6 | ts-formatter implements ADR-003 anchor registry | [ ] |
| AC-7 | ts-formatter implements ADR-004 split logic | [ ] |
| AC-8 | Token budgets documented per component | [ ] |
| AC-9 | Data contracts (JSON schemas) defined | [ ] |
| AC-10 | Integration with ps-critic documented | [ ] |

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Agent | Effort | Blocked By | Artifact |
|----|-------|--------|-------|--------|------------|----------|
| [TASK-001](./TASK-001-tdd-overview.md) | TDD: Transcript Skill Overview | pending | ps-architect | 3 | - | docs/TDD-transcript-skill.md |
| [TASK-002](./TASK-002-tdd-ts-parser.md) | TDD: ts-parser Agent Design | pending | ps-architect | 2 | TASK-001 | docs/TDD-ts-parser.md |
| [TASK-003](./TASK-003-tdd-ts-extractor.md) | TDD: ts-extractor Agent Design | pending | ps-architect | 3 | TASK-001 | docs/TDD-ts-extractor.md |
| [TASK-004](./TASK-004-tdd-ts-formatter.md) | TDD: ts-formatter Agent Design | pending | ps-architect | 3 | TASK-002, TASK-003 | docs/TDD-ts-formatter.md |
| [TASK-005](./TASK-005-agent-ts-parser.md) | Create ts-parser AGENT.md | pending | ps-architect | 1 | TASK-002 | agents/ts-parser/AGENT.md |
| [TASK-006](./TASK-006-agent-ts-extractor.md) | Create ts-extractor AGENT.md | pending | ps-architect | 1 | TASK-003 | agents/ts-extractor/AGENT.md |
| [TASK-007](./TASK-007-agent-ts-formatter.md) | Create ts-formatter AGENT.md | pending | ps-architect | 1 | TASK-004 | agents/ts-formatter/AGENT.md |
| [TASK-008](./TASK-008-skill-md.md) | Create SKILL.md Orchestrator | pending | ps-architect | 2 | TASK-005, TASK-006, TASK-007 | SKILL.md |
| [TASK-009](./TASK-009-playbook.md) | Create EN-005 PLAYBOOK | pending | ps-architect | 2 | TASK-008 | docs/PLAYBOOK-en005.md |
| [TASK-010](./TASK-010-runbook.md) | Create EN-005 RUNBOOK | pending | ps-architect | 1 | TASK-008 | docs/RUNBOOK-en005.md |
| [TASK-011](./TASK-011-review-tdd.md) | ps-critic Review: TDD Documents | pending | ps-critic | 1 | TASK-004 | review/tdd-review.md |
| [TASK-012](./TASK-012-review-agents.md) | ps-critic Review: Agent Definitions | pending | ps-critic | 1 | TASK-008 | review/agent-review.md |
| [TASK-013](./TASK-013-final-review.md) | Final Review and GATE-4 Prep | pending | ps-critic | 1 | TASK-011, TASK-012 | review/EN-005-final-review.md |

**Total Effort:** 22 points (13 tasks)

---

## Orchestration Pipeline

```
+==============================================================================+
|                       EN-005 ORCHESTRATION PIPELINE                          |
+==============================================================================+
|                                                                               |
|  PHASE 1: TECHNICAL DESIGN DOCUMENTS (TDD)                                   |
|  ┌─────────────────────────────────────────────────────────────────────────┐ |
|  │                                                                          │ |
|  │     ┌───────────────────────────────────────────────────────────┐       │ |
|  │     │              TASK-001: TDD Overview                        │       │ |
|  │     └───────────────────────────┬───────────────────────────────┘       │ |
|  │                     ┌───────────┴───────────┐                           │ |
|  │                     ▼                       ▼                           │ |
|  │           ┌─────────────────┐     ┌─────────────────┐                  │ |
|  │           │   TASK-002      │     │   TASK-003      │ (parallel)       │ |
|  │           │ TDD: ts-parser  │     │ TDD: ts-extractor│                  │ |
|  │           └────────┬────────┘     └────────┬────────┘                  │ |
|  │                    └────────┬──────────────┘                           │ |
|  │                             ▼                                           │ |
|  │                   ┌─────────────────┐                                  │ |
|  │                   │    TASK-004     │                                  │ |
|  │                   │ TDD: ts-formatter│                                  │ |
|  │                   └─────────────────┘                                  │ |
|  └─────────────────────────────┼──────────────────────────────────────────┘ |
|                                ▼                                            |
|  PHASE 2: AGENT DEFINITIONS                                                 |
|  ┌─────────────────────────────────────────────────────────────────────────┐ |
|  │  ┌──────────┐  ┌──────────┐  ┌──────────┐                              │ |
|  │  │ TASK-005 │  │ TASK-006 │  │ TASK-007 │ (parallel)                   │ |
|  │  │ts-parser │  │ts-extractor│ │ts-formatter│                            │ |
|  │  │ AGENT.md │  │ AGENT.md │  │ AGENT.md │                              │ |
|  │  └────┬─────┘  └────┬─────┘  └────┬─────┘                              │ |
|  │       └─────────────┼─────────────┘                                    │ |
|  │                     ▼                                                   │ |
|  │           ┌─────────────────┐                                          │ |
|  │           │    TASK-008     │                                          │ |
|  │           │    SKILL.md     │                                          │ |
|  │           └─────────────────┘                                          │ |
|  └─────────────────────────────┼──────────────────────────────────────────┘ |
|                                ▼                                            |
|  PHASE 3: OPERATIONAL DOCS         PHASE 4: QUALITY REVIEW                  |
|  ┌─────────────────────┐           ┌─────────────────────────────────────┐ |
|  │ ┌───────┐ ┌───────┐ │           │ ┌───────┐ ┌───────┐                 │ |
|  │ │TASK-09│ │TASK-10│ │           │ │TASK-11│ │TASK-12│ → TASK-13       │ |
|  │ │PLAYBOOK││RUNBOOK│ │           │ │TDD Rev││Agent Rev│ → Final Review │ |
|  │ └───────┘ └───────┘ │           │ └───────┘ └───────┘                 │ |
|  └─────────────────────┘           └─────────────────────────────────────┘ |
|                                                                             |
|  ╔═══════════════════════════════════════════════════════════════════════╗ |
|  ║                    ★ GATE-4: Design Review ★                          ║ |
|  ║                    (Human Approval Required)                          ║ |
|  ╚═══════════════════════════════════════════════════════════════════════╝ |
+==============================================================================+
```

---

## Deliverables Summary

### Technical Design Documents

| Deliverable | Purpose | Token Budget |
|-------------|---------|--------------|
| TDD-transcript-skill.md | Overall architecture with C4 diagrams | ~15K |
| TDD-ts-parser.md | Parsing agent design, JSON schemas | ~10K |
| TDD-ts-extractor.md | Extraction agent, entity schemas | ~12K |
| TDD-ts-formatter.md | Formatting, splitting, backlinks | ~15K |

### Agent Definitions

| Deliverable | Purpose | Token Budget |
|-------------|---------|--------------|
| ts-parser/AGENT.md | Prompt-based parser agent | ~3K |
| ts-extractor/AGENT.md | Prompt-based extractor agent | ~5K |
| ts-formatter/AGENT.md | Prompt-based formatter agent | ~4K |
| SKILL.md | Orchestrator entry point | ~3K |

### Operational Documentation

| Deliverable | Purpose | Token Budget |
|-------------|---------|--------------|
| PLAYBOOK-en005.md | Execution procedures | ~8K |
| RUNBOOK-en005.md | Troubleshooting guide | ~6K |

---

## Supporting Documents

### Discoveries

| ID | Title | Status | Path |
|----|-------|--------|------|
| DISC-001 | Design Documentation Inputs | documented | [FEAT-001--DISC-001-design-inputs.md](./FEAT-001--DISC-001-design-inputs.md) |

### Decisions

| ID | Title | Status | Path |
|----|-------|--------|------|
| DEC-001 | Design Documentation Approach | accepted | [FEAT-001--DEC-001-design-approach.md](./FEAT-001--DEC-001-design-approach.md) |

**Key Decisions in DEC-001:**
- DEC-001-001: L0/L1/L2 structure for all TDDs
- DEC-001-002: ADR Compliance Checklist in each TDD
- DEC-001-003: Requirements Traceability Matrix
- DEC-001-004: Sequential TDD development
- DEC-001-005: AGENT.md follows PS_AGENT_TEMPLATE
- DEC-001-006: ps-critic review at 0.90 threshold
- DEC-001-007: PLAYBOOK phase alignment with EN-003 phases
- DEC-001-008: RUNBOOK risk-based structure for YELLOW risks
- DEC-001-009: Token budget monitoring (31.5K soft limit)
- DEC-001-010: Bidirectional linking per ADR-003

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-001: Analysis & Design](../FEAT-001-analysis-design.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | EN-003 | Requirements inform design (40 requirements) |
| Depends On | EN-004 | ADRs guide all design decisions |
| Depends On | ADR-001 | Agent architecture |
| Depends On | ADR-002 | Artifact structure |
| Depends On | ADR-003 | Bidirectional linking |
| Depends On | ADR-004 | File splitting strategy |
| Depends On | ADR-005 | Agent implementation approach |
| Blocks | FEAT-002 | Implementation uses design docs |

### Reference Documents

| Document | Path | Purpose |
|----------|------|---------|
| ADR-001 | docs/adrs/ADR-001-agent-architecture.md | Agent boundaries |
| ADR-002 | docs/adrs/ADR-002-artifact-structure.md | Packet structure |
| ADR-003 | docs/adrs/ADR-003-bidirectional-linking.md | Anchor system |
| ADR-004 | docs/adrs/ADR-004-file-splitting.md | Split strategy |
| ADR-005 | docs/adrs/ADR-005-agent-implementation.md | Phased approach |
| TDD Template | .context/templates/design/TDD.template.md | TDD format |
| PLAYBOOK Template | .context/templates/design/PLAYBOOK.template.md | Playbook format |
| RUNBOOK Template | .context/templates/design/RUNBOOK.template.md | Runbook format |

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   ENABLER PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Phase 1 (TDD):    [....................] 0% (0/4 tasks)          |
| Phase 2 (Agents): [....................] 0% (0/4 tasks)          |
| Phase 3 (Ops):    [....................] 0% (0/2 tasks)          |
| Phase 4 (Review): [....................] 0% (0/3 tasks)          |
+------------------------------------------------------------------+
| Overall:          [....................] 0% (0/13 tasks)         |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Tasks** | 13 |
| **Completed Tasks** | 0 |
| **Total Effort (points)** | 22 |
| **Completed Effort** | 0 |
| **Completion %** | 0% |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-26 | Claude | pending | Enabler created |
| 2026-01-26 | Claude | in_progress | Updated with ADR alignment, new task structure |
| 2026-01-26 | Claude | in_progress | Tasks 1-13 executed, ps-critic reviews complete |
| 2026-01-26 | Claude | awaiting_approval | DISC-002 identified scope creep, DEC-002 decision made |
| 2026-01-26 | Claude | awaiting_approval | DISC-004 research on file organization, artifacts relocated to skills/transcript/ |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Product Backlog Item (tagged Architecture) |
| **SAFe** | Enabler Story |
| **JIRA** | Task |
