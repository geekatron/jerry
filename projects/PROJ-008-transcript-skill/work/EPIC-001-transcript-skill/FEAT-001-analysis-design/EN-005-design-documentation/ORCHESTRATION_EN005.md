# EN-005 Orchestration Plan: Design Documentation

> **Workflow ID:** en005-tdd-20260126-001
> **Project:** PROJ-008-transcript-skill
> **Enabler:** EN-005 Design Documentation
> **Status:** ACTIVE
> **Gate:** GATE-4 (Design Review)
> **Created:** 2026-01-26

---

## L0: Executive Summary (ELI5)

Think of this like creating blueprints before building a house:

1. **TDD (Technical Design Documents)** = The main blueprints
   - What rooms we're building (agents)
   - How they connect (data flow)
   - What materials we need (tokens, formats)

2. **AGENT.md Files** = Instruction manuals for each worker
   - What each agent does
   - How to give them instructions
   - What they produce

3. **PLAYBOOK & RUNBOOK** = Operating procedures
   - How to build it step by step (PLAYBOOK)
   - What to do when things go wrong (RUNBOOK)

**Bottom Line:** We create all the documentation before we build, so implementation goes smoothly.

---

## L1: Technical Workflow (Engineer)

### Workflow Pattern

EN-005 uses a **Sequential with Critic Feedback** pattern:

```
+==============================================================================+
|                    EN-005 DESIGN DOCUMENTATION WORKFLOW                       |
+==============================================================================+
|                                                                               |
|  PHASE 1: TECHNICAL DESIGN DOCUMENTS (TDD)                                   |
|  ┌─────────────────────────────────────────────────────────────────────────┐ |
|  │                                                                          │ |
|  │     ┌───────────────────────────────────────────────────────────┐       │ |
|  │     │              TASK-001: TDD Overview                        │       │ |
|  │     │      (Transcript Skill Architecture Document)              │       │ |
|  │     └───────────────────────────┬───────────────────────────────┘       │ |
|  │                                 │                                        │ |
|  │           ┌─────────────────────┼─────────────────────┐                 │ |
|  │           │                     │                     │                 │ |
|  │           ▼                     ▼                     ▼                 │ |
|  │   ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐        │ |
|  │   │   TASK-002      │  │   TASK-003      │  │   (Parallel)    │        │ |
|  │   │ TDD: ts-parser  │  │ TDD: ts-extractor│  │                │        │ |
|  │   └────────┬────────┘  └────────┬────────┘  └────────┬────────┘        │ |
|  │            │                    │                    │                  │ |
|  │            └────────────────────┼────────────────────┘                  │ |
|  │                                 │                                        │ |
|  │                                 ▼                                        │ |
|  │                    ┌─────────────────────┐                              │ |
|  │                    │      TASK-004       │                              │ |
|  │                    │  TDD: ts-formatter  │                              │ |
|  │                    │   (depends on 2,3)  │                              │ |
|  │                    └─────────────────────┘                              │ |
|  │                                                                          │ |
|  └─────────────────────────────────┼────────────────────────────────────────┘ |
|                                    │                                          |
|                                    ▼                                          |
|  PHASE 2: AGENT DEFINITIONS                                                   |
|  ┌─────────────────────────────────────────────────────────────────────────┐ |
|  │                                                                          │ |
|  │   ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐        │ |
|  │   │   TASK-005      │  │   TASK-006      │  │   TASK-007      │        │ |
|  │   │ ts-parser       │  │ ts-extractor    │  │ ts-formatter    │        │ |
|  │   │  AGENT.md       │  │  AGENT.md       │  │  AGENT.md       │        │ |
|  │   └────────┬────────┘  └────────┬────────┘  └────────┬────────┘        │ |
|  │            │  (parallel)        │                    │                  │ |
|  │            └────────────────────┼────────────────────┘                  │ |
|  │                                 │                                        │ |
|  │                                 ▼                                        │ |
|  │                    ┌─────────────────────┐                              │ |
|  │                    │      TASK-008       │                              │ |
|  │                    │     SKILL.md        │                              │ |
|  │                    │   (orchestrator)    │                              │ |
|  │                    └─────────────────────┘                              │ |
|  │                                                                          │ |
|  └─────────────────────────────────┼────────────────────────────────────────┘ |
|                                    │                                          |
|                                    ▼                                          |
|  PHASE 3: OPERATIONAL DOCUMENTATION                                           |
|  ┌─────────────────────────────────────────────────────────────────────────┐ |
|  │                                                                          │ |
|  │   ┌─────────────────────┐          ┌─────────────────────┐              │ |
|  │   │      TASK-009       │          │      TASK-010       │              │ |
|  │   │  PLAYBOOK-en005.md  │          │  RUNBOOK-en005.md   │              │ |
|  │   │ (execution steps)   │          │ (troubleshooting)   │              │ |
|  │   └─────────────────────┘          └─────────────────────┘              │ |
|  │              (parallel execution)                                        │ |
|  │                                                                          │ |
|  └─────────────────────────────────┼────────────────────────────────────────┘ |
|                                    │                                          |
|                                    ▼                                          |
|  PHASE 4: QUALITY REVIEW (CRITIC FEEDBACK LOOP)                              |
|  ┌─────────────────────────────────────────────────────────────────────────┐ |
|  │                                                                          │ |
|  │   ┌─────────────────────┐          ┌─────────────────────┐              │ |
|  │   │     TASK-011        │          │     TASK-012        │              │ |
|  │   │   ps-critic         │          │   ps-critic         │              │ |
|  │   │ Review: TDD Docs    │          │ Review: Agents      │              │ |
|  │   └──────────┬──────────┘          └──────────┬──────────┘              │ |
|  │              │                                │                          │ |
|  │              └────────────────┬───────────────┘                          │ |
|  │                               │                                          │ |
|  │                               ▼                                          │ |
|  │              ┌────────────────────────────────┐                          │ |
|  │              │         TASK-013               │                          │ |
|  │              │   ps-critic Final Review       │                          │ |
|  │              │   (quality >= 0.90 required)   │                          │ |
|  │              └────────────────┬───────────────┘                          │ |
|  │                               │                                          │ |
|  │    ┌─────────────────────────┬┴───────────────────────────┐             │ |
|  │    │                         │                            │             │ |
|  │    ▼                         │                            ▼             │ |
|  │  PASS                        │                         FAIL             │ |
|  │  (score >= 0.90)             │                    (score < 0.90)        │ |
|  │    │                         │                            │             │ |
|  │    │                         │        ┌───────────────────┘             │ |
|  │    │                         │        │                                 │ |
|  │    │                         │        ▼                                 │ |
|  │    │                         │   ┌──────────────┐                       │ |
|  │    │                         │   │ Revision     │                       │ |
|  │    │                         │   │ (max 3 iter) │                       │ |
|  │    │                         │   └──────┬───────┘                       │ |
|  │    │                         │          │                               │ |
|  │    │                         └──────────┘ (feedback loop)               │ |
|  │    │                                                                     │ |
|  └────┼─────────────────────────────────────────────────────────────────────┘ |
|       │                                                                       |
|       ▼                                                                       |
|  ╔═══════════════════════════════════════════════════════════════════════╗   |
|  ║                    ★ GATE-4: Design Review ★                          ║   |
|  ║                    (Human Approval Required)                          ║   |
|  ╚═══════════════════════════════════════════════════════════════════════╝   |
|       │                                                                       |
|       ▼                                                                       |
|  ┌───────────────────────────────────────────────────────────────────────┐   |
|  │                      EN-005 COMPLETE                                  │   |
|  │                  Proceed to FEAT-002 Implementation                   │   |
|  └───────────────────────────────────────────────────────────────────────┘   |
+==============================================================================+
```

### ADR Alignment

| ADR | Key Decision | EN-005 Impact |
|-----|--------------|---------------|
| ADR-001 | Hybrid Architecture (3 custom agents + ps-critic) | TDD defines each agent's responsibilities |
| ADR-002 | Hierarchical Packet Structure | ts-formatter design includes packet generation |
| ADR-003 | Custom Anchors with Backlinks | ts-formatter implements anchor registry |
| ADR-004 | Semantic Boundary Split (31.5K) | ts-formatter handles split logic |
| ADR-005 | Phased Implementation (Prompt first) | AGENT.md files are Phase 1 deliverables |

### Task Dependency Graph

```
┌─────────┐
│ TASK-001│ ◄─────────── TDD Overview (first)
└────┬────┘
     │
     ├────────────┬────────────┐
     │            │            │
     ▼            ▼            │
┌─────────┐ ┌─────────┐       │
│ TASK-002│ │ TASK-003│ (parallel)
└────┬────┘ └────┬────┘       │
     │            │            │
     └──────┬─────┘            │
            │                  │
            ▼                  │
       ┌─────────┐            │
       │ TASK-004│ ◄──────────┘ (depends on 2,3)
       └────┬────┘
            │
            ▼
   ┌────────┼────────┬────────┐
   │        │        │        │
   ▼        ▼        ▼        │
┌──────┐ ┌──────┐ ┌──────┐   │
│TASK-5│ │TASK-6│ │TASK-7│ (parallel)
└──┬───┘ └──┬───┘ └──┬───┘   │
   │        │        │        │
   └────────┼────────┘        │
            │                 │
            ▼                 │
       ┌─────────┐            │
       │ TASK-008│ ◄──────────┘ (SKILL.md)
       └────┬────┘
            │
   ┌────────┴────────┐
   │                 │
   ▼                 ▼
┌──────┐         ┌──────┐
│TASK-9│         │TASK-10│ (parallel)
└──┬───┘         └──┬───┘
   │                 │
   └────────┬────────┘
            │
   ┌────────┼────────┐
   │                 │
   ▼                 ▼
┌───────┐        ┌───────┐
│TASK-11│        │TASK-12│ (parallel reviews)
└───┬───┘        └───┬───┘
    │                │
    └────────┬───────┘
             │
             ▼
        ┌─────────┐
        │ TASK-013│ (final review)
        └────┬────┘
             │
             ▼
        ╔═════════╗
        ║ GATE-4  ║
        ╚═════════╝
```

---

## L2: Strategic Context (Architect)

### Design Decisions Informing EN-005

#### From ADR-001: Agent Architecture

The **Hybrid Architecture** decision means EN-005 must design:

1. **ts-parser**: VTT/SRT/TXT → Canonical JSON
   - Format detection
   - Normalization
   - Speaker voice tag parsing

2. **ts-extractor**: Canonical JSON → Entity List
   - Tiered extraction (Rule → ML → LLM)
   - Confidence scoring
   - Citation generation

3. **ts-formatter**: Entity List → Output Packet
   - Packet structure generation
   - Token counting
   - File splitting
   - Backlinks generation

4. **ps-critic integration**: Quality gate (score >= 0.90)

#### From ADR-002: Artifact Structure

The **Hierarchical Packet Structure** requires ts-formatter to:

```
{session-id}-transcript-output/
├── 00-index.md           # Master manifest
├── 01-summary.md         # Executive summary
├── 02-speakers/          # Speaker profiles
├── 03-topics/            # Topics (may split)
├── 04-entities/          # Action items, decisions, questions
├── 05-timeline/          # Chronological view
├── 07-mindmap/           # Mermaid + ASCII
└── 08-workitems/         # Jerry integration
```

Token budgets per artifact are defined in ADR-002.

#### From ADR-003: Bidirectional Linking

The **Custom Anchors** approach requires:

- Anchor format: `<a id="{type}-{nnn}"></a>`
- Entity types: speaker, topic, action, question, decision, idea, segment, span
- Backlinks section auto-generated per file
- Link validation before write

#### From ADR-004: File Splitting

The **Semantic Boundary Split** requires:

- 31.5K soft limit (90% of 35K)
- Split at `##` headings
- Fallback to `###` if section too large
- Index file + navigation headers

#### From ADR-005: Implementation Approach

The **Phased Implementation** means:

- Phase 1: AGENT.md files (prompt-based)
- Phase 2: Python scripts (if triggers met)
- Migration triggers documented but not implemented in EN-005

### Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| TDD scope creep | MEDIUM | MEDIUM | Strict acceptance criteria per task |
| Agent design drift from ADRs | LOW | HIGH | ADR traceability in each TDD |
| Token budget miscalculation | MEDIUM | LOW | Conservative estimates + validation |
| Quality review fails | LOW | MEDIUM | Incremental reviews, max 3 iterations |
| GATE-4 rejection | LOW | HIGH | Pre-flight checklist before human review |

### Success Criteria

| Criterion | Threshold | Measurement |
|-----------|-----------|-------------|
| TDD Completeness | 100% | All sections present per template |
| ADR Alignment | 100% | All ADR decisions referenced |
| Quality Score | >= 0.90 | ps-critic aggregate score |
| Template Compliance | 100% | Follows Jerry templates |
| Token Budget | < 35K per file | Actual vs. budgeted |

---

## Deliverables Registry

### Phase 1: TDD Documents

| ID | Deliverable | Path | Status | Token Budget |
|----|-------------|------|--------|--------------|
| TDD-001 | Transcript Skill Overview | docs/TDD-transcript-skill.md | PENDING | ~15K |
| TDD-002 | ts-parser Agent Design | docs/TDD-ts-parser.md | PENDING | ~10K |
| TDD-003 | ts-extractor Agent Design | docs/TDD-ts-extractor.md | PENDING | ~12K |
| TDD-004 | ts-formatter Agent Design | docs/TDD-ts-formatter.md | PENDING | ~15K |

### Phase 2: Agent Definitions

| ID | Deliverable | Path | Status | Token Budget |
|----|-------------|------|--------|--------------|
| AGENT-001 | ts-parser AGENT.md | agents/ts-parser/AGENT.md | PENDING | ~3K |
| AGENT-002 | ts-extractor AGENT.md | agents/ts-extractor/AGENT.md | PENDING | ~5K |
| AGENT-003 | ts-formatter AGENT.md | agents/ts-formatter/AGENT.md | PENDING | ~4K |
| AGENT-004 | SKILL.md Orchestrator | SKILL.md | PENDING | ~3K |

### Phase 3: Operational Documentation

| ID | Deliverable | Path | Status | Token Budget |
|----|-------------|------|--------|--------------|
| OPS-001 | EN-005 PLAYBOOK | docs/PLAYBOOK-en005.md | PENDING | ~8K |
| OPS-002 | EN-005 RUNBOOK | docs/RUNBOOK-en005.md | PENDING | ~6K |

### Phase 4: Quality Artifacts

| ID | Deliverable | Path | Status |
|----|-------------|------|--------|
| REV-001 | TDD Review | review/tdd-review.md | PENDING |
| REV-002 | Agent Review | review/agent-review.md | PENDING |
| REV-003 | Final Review | review/EN-005-final-review.md | PENDING |

---

## Execution Notes

### Parallel Execution Opportunities

1. **Phase 1**: TASK-002 and TASK-003 can run in parallel after TASK-001
2. **Phase 2**: TASK-005, TASK-006, TASK-007 can all run in parallel
3. **Phase 3**: TASK-009 and TASK-010 can run in parallel
4. **Phase 4**: TASK-011 and TASK-012 can run in parallel

### Quality Gate Strategy

The ps-critic feedback loop in Phase 4 allows up to 3 iterations:

```
Iteration 1: Initial review
  │
  ├─► score >= 0.90 → PASS → proceed to GATE-4
  │
  └─► score < 0.90 → REVISE → Iteration 2
                        │
                        ├─► score >= 0.90 → PASS
                        │
                        └─► score < 0.90 → Iteration 3
                                  │
                                  ├─► score >= 0.90 → PASS
                                  │
                                  └─► ESCALATE to human
```

### Checkpoint Strategy

Checkpoints are created at:

1. End of each phase completion
2. After each ps-critic review iteration
3. Before GATE-4 submission

---

## Source Documents

### EN-003 Requirements (40 requirements informing design)

| Category | Count | Key Requirements |
|----------|-------|------------------|
| Stakeholder Needs (STK) | 10 | VTT/SRT processing, speaker ID, action items |
| Functional Requirements (FR) | 15 | Parsing, extraction, output generation |
| Non-Functional Requirements (NFR) | 10 | Performance, accuracy, robustness |
| Interface Requirements (IR) | 5 | CLI, SKILL.md, hexagonal architecture |

**Source:** `EN-003-requirements-synthesis/requirements/REQUIREMENTS-SPECIFICATION.md`

### EN-004 ADRs (5 architecture decisions)

| ADR | Quality Score | Status |
|-----|---------------|--------|
| ADR-001: Agent Architecture | 0.92 | APPROVED |
| ADR-002: Artifact Structure | 0.91 | APPROVED |
| ADR-003: Bidirectional Linking | 0.93 | APPROVED |
| ADR-004: File Splitting | 0.94 | APPROVED |
| ADR-005: Agent Implementation | 0.92 | APPROVED |

**Aggregate Quality:** 0.924 (passed GATE-3)

---

## Supporting Documents

### Discoveries

| ID | Title | Path | Status |
|----|-------|------|--------|
| DISC-001 | Design Documentation Inputs | FEAT-001--DISC-001-design-inputs.md | DOCUMENTED |

**Key Findings:**
- 40 requirements mapped to 3 agents (ts-parser, ts-extractor, ts-formatter)
- 6 design patterns from EN-003 require TDD documentation
- 5 YELLOW risks need explicit design mitigation
- All deliverables fit within 35K token budget

### Decisions

| ID | Title | Path | Status |
|----|-------|------|--------|
| DEC-001 | Design Documentation Approach | FEAT-001--DEC-001-design-approach.md | ACCEPTED |

**Key Decisions:**
- DEC-001-001: L0/L1/L2 structure for all TDDs
- DEC-001-002: ADR Compliance Checklist in each TDD
- DEC-001-003: Requirements Traceability Matrix (EN-003 → TDD)
- DEC-001-004: Sequential TDD development order
- DEC-001-005: AGENT.md follows PS_AGENT_TEMPLATE
- DEC-001-006: ps-critic review at 0.90 threshold
- DEC-001-007: PLAYBOOK aligns with 4 implementation phases
- DEC-001-008: RUNBOOK covers 5 YELLOW risks
- DEC-001-009: Token budget monitoring (31.5K soft limit)
- DEC-001-010: Bidirectional linking per ADR-003

---

## References

| # | Reference | Type | Path |
|---|-----------|------|------|
| 1 | Requirements Specification | EN-003 | EN-003-requirements-synthesis/requirements/REQUIREMENTS-SPECIFICATION.md |
| 2 | NASA SE Requirements | EN-003 | EN-003-requirements-synthesis/requirements/NASA-SE-REQUIREMENTS.md |
| 3 | EN-004 Final Review | Review | EN-004-architecture-decisions/review/EN-004-final-review.md |
| 4 | ADR-001 Agent Architecture | ADR | docs/adrs/ADR-001-agent-architecture.md |
| 5 | ADR-002 Artifact Structure | ADR | docs/adrs/ADR-002-artifact-structure.md |
| 6 | ADR-003 Bidirectional Linking | ADR | docs/adrs/ADR-003-bidirectional-linking.md |
| 7 | ADR-004 File Splitting | ADR | docs/adrs/ADR-004-file-splitting.md |
| 8 | ADR-005 Agent Implementation | ADR | docs/adrs/ADR-005-agent-implementation.md |
| 9 | Design Inputs Discovery | Discovery | FEAT-001--DISC-001-design-inputs.md |
| 10 | Design Approach Decisions | Decision | FEAT-001--DEC-001-design-approach.md |
| 11 | TDD Template | Template | .context/templates/design/TDD.template.md |
| 12 | PLAYBOOK Template | Template | .context/templates/design/PLAYBOOK.template.md |
| 13 | RUNBOOK Template | Template | .context/templates/design/RUNBOOK.template.md |
| 14 | PS_AGENT_TEMPLATE | Framework | skills/problem-solving/agents/PS_AGENT_TEMPLATE.md |

---

*Orchestration Plan Version: 1.0*
*Workflow ID: en005-tdd-20260126-001*
*Constitutional Compliance: P-002 (persisted), P-003 (single nesting), P-020 (user authority)*
