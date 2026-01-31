# ORCHESTRATION_PLAN: Transcript Skill Development

> **Plan ID:** ORCH-001
> **Version:** 1.0.0
> **Status:** ACTIVE
> **Created:** 2026-01-26T00:00:00Z
> **Last Updated:** 2026-01-26T00:00:00Z
> **SSOT:** [ORCHESTRATION.yaml](./ORCHESTRATION.yaml)

---

## Overview

This orchestration plan coordinates the semi-supervised development of the Transcript Skill through 6 phases with human approval gates. The workflow uses problem-solving agents for research, analysis, and synthesis, with built-in checkpoints for human oversight.

**Key Characteristics:**
- Semi-supervised workflow with 6 human approval gates
- Cross-pollinated pipeline: research feeds requirements feeds design
- Prompt-based agents (Phase 1), Python enhancement (Phase 2 if needed)
- Token-managed artifacts (<35K per file)
- Bidirectional deep linking between all artifacts

---

## Workflow Visualization

```
+==============================================================================+
|                 TRANSCRIPT SKILL ORCHESTRATION PIPELINE                       |
+==============================================================================+
|                                                                               |
|  ┌─────────────────────────────────────────────────────────────────────────┐ |
|  │ PHASE 1: PARALLEL RESEARCH                                               │ |
|  │ ─────────────────────────────                                            │ |
|  │                                                                          │ |
|  │    ┌──────────────────────────────────────────────────────────────────┐ │ |
|  │    │                    EN-001: Market Analysis                        │ │ |
|  │    │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐   │ │ |
|  │    │  │ Pocket  │ │Otter.ai │ │Fireflies│ │  Grain  │ │  tl;dv  │   │ │ |
|  │    │  │Research │ │Research │ │Research │ │Research │ │Research │   │ │ |
|  │    │  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘   │ │ |
|  │    │       │           │           │           │           │         │ │ |
|  │    │       └───────────┴─────┬─────┴───────────┴───────────┘         │ │ |
|  │    │                         ▼                                        │ │ |
|  │    │             ┌─────────────────────┐                             │ │ |
|  │    │             │  Feature Matrix     │                             │ │ |
|  │    │             │  Synthesis          │                             │ │ |
|  │    │             └─────────────────────┘                             │ │ |
|  │    └──────────────────────────────────────────────────────────────────┘ │ |
|  │                                                                          │ |
|  │    ┌──────────────────────────────────────────────────────────────────┐ │ |
|  │    │                EN-002: Technical Standards                        │ │ |
|  │    │  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐    │ │ |
|  │    │  │ VTT Format  │ │ SRT Format  │ │ NLP/NER Best Practices │    │ │ |
|  │    │  │ Research    │ │ Research    │ │ Research                │    │ │ |
|  │    │  └─────────────┘ └─────────────┘ └─────────────────────────┘    │ │ |
|  │    └──────────────────────────────────────────────────────────────────┘ │ |
|  │                                                                          │ |
|  │                    SYNC BARRIER + ps-critic Review                       │ |
|  │                                 │                                        │ |
|  │    ┌────────────────────────────┴─────────────────────────────────────┐ │ |
|  │    │                   ★ GATE-1: Research Review ★                     │ │ |
|  │    │                   (Human Approval Required)                       │ │ |
|  │    └────────────────────────────┬─────────────────────────────────────┘ │ |
|  └─────────────────────────────────┼───────────────────────────────────────┘ |
|                                    │                                         |
|                                    ▼                                         |
|  ┌─────────────────────────────────────────────────────────────────────────┐ |
|  │ PHASE 2: REQUIREMENTS SYNTHESIS                                          │ |
|  │ ──────────────────────────────────                                       │ |
|  │                                                                          │ |
|  │    ┌──────────────────────────────────────────────────────────────────┐ │ |
|  │    │                    EN-003: Requirements Synthesis                  │ │ |
|  │    │                                                                    │ │ |
|  │    │  ┌────────────┐  ┌────────────┐  ┌────────────┐                  │ │ |
|  │    │  │   5W2H     │  │  Ishikawa  │  │   FMEA     │                  │ │ |
|  │    │  │  Analysis  │  │  Diagram   │  │  Analysis  │                  │ │ |
|  │    │  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘                  │ │ |
|  │    │        └───────────────┼───────────────┘                          │ │ |
|  │    │                        ▼                                          │ │ |
|  │    │              ┌───────────────────┐                                │ │ |
|  │    │              │ Requirements Spec │                                │ │ |
|  │    │              │ (L0/L1/L2)        │                                │ │ |
|  │    │              └─────────┬─────────┘                                │ │ |
|  │    │                        ▼                                          │ │ |
|  │    │              ┌───────────────────┐                                │ │ |
|  │    │              │ ps-critic Review  │                                │ │ |
|  │    │              └───────────────────┘                                │ │ |
|  │    └──────────────────────────────────────────────────────────────────┘ │ |
|  │                                                                          │ |
|  │    ┌────────────────────────────────────────────────────────────────┐   │ |
|  │    │                   ★ GATE-2: Requirements Review ★               │   │ |
|  │    │                   (Human Approval Required)                     │   │ |
|  │    └────────────────────────────┬───────────────────────────────────┘   │ |
|  └─────────────────────────────────┼───────────────────────────────────────┘ |
|                                    │                                         |
|                                    ▼                                         |
|  ┌─────────────────────────────────────────────────────────────────────────┐ |
|  │ PHASE 3: ARCHITECTURE DECISIONS                                          │ |
|  │ ─────────────────────────────────                                        │ |
|  │                                                                          │ |
|  │    ┌──────────────────────────────────────────────────────────────────┐ │ |
|  │    │                    EN-004: Architecture Decision Records           │ │ |
|  │    │                                                                    │ │ |
|  │    │  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐        │ │ |
|  │    │  │ ADR-001   │ │ ADR-002   │ │ ADR-003   │ │ ADR-004   │        │ │ |
|  │    │  │ Agent     │ │ Artifact  │ │ Deep      │ │ File      │        │ │ |
|  │    │  │ Arch      │ │ Structure │ │ Linking   │ │ Splitting │        │ │ |
|  │    │  └─────┬─────┘ └─────┬─────┘ └─────┬─────┘ └─────┬─────┘        │ │ |
|  │    │        │             │             │             │               │ │ |
|  │    │        └─────────────┴──────┬──────┴─────────────┘               │ │ |
|  │    │                             ▼                                     │ │ |
|  │    │                    ┌───────────────┐                             │ │ |
|  │    │                    │ ADR-005       │                             │ │ |
|  │    │                    │ Agent Impl    │                             │ │ |
|  │    │                    └───────┬───────┘                             │ │ |
|  │    │                            ▼                                     │ │ |
|  │    │                   ┌───────────────────┐                          │ │ |
|  │    │                   │ ps-critic Review  │                          │ │ |
|  │    │                   └───────────────────┘                          │ │ |
|  │    └──────────────────────────────────────────────────────────────────┘ │ |
|  │                                                                          │ |
|  │    ┌────────────────────────────────────────────────────────────────┐   │ |
|  │    │                   ★ GATE-3: Architecture Review ★               │   │ |
|  │    │                   (Human Approval Required)                     │   │ |
|  │    └────────────────────────────┬───────────────────────────────────┘   │ |
|  └─────────────────────────────────┼───────────────────────────────────────┘ |
|                                    │                                         |
|                                    ▼                                         |
|  ┌─────────────────────────────────────────────────────────────────────────┐ |
|  │ PHASE 4: DESIGN DOCUMENTATION                                            │ |
|  │ ───────────────────────────────                                          │ |
|  │                                                                          │ |
|  │    ┌──────────────────────────────────────────────────────────────────┐ │ |
|  │    │               EN-005: Design Documentation (Parallel)             │ │ |
|  │    │  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐        │ │ |
|  │    │  │VTT Parser │ │ Entity    │ │ Mind Map  │ │ Artifact  │        │ │ |
|  │    │  │Design     │ │ Extract   │ │ Generator │ │ Packager  │        │ │ |
|  │    │  └───────────┘ └───────────┘ └───────────┘ └───────────┘        │ │ |
|  │    │  ┌───────────┐ ┌───────────┐                                     │ │ |
|  │    │  │Deep Link  │ │Worktracker│                                     │ │ |
|  │    │  │ System    │ │Integration│                                     │ │ |
|  │    │  └───────────┘ └───────────┘                                     │ │ |
|  │    └──────────────────────────────────────────────────────────────────┘ │ |
|  │                                                                          │ |
|  │    ┌──────────────────────────────────────────────────────────────────┐ │ |
|  │    │               EN-006: Context Injection Design (Parallel)         │ │ |
|  │    │                                                                    │ │ |
|  │    │  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐        │ │ |
|  │    │  │ 5W2H Analysis │  │ Spec Document │  │ Example Plans │        │ │ |
|  │    │  └───────────────┘  └───────────────┘  └───────────────┘        │ │ |
|  │    └──────────────────────────────────────────────────────────────────┘ │ |
|  │                                                                          │ |
|  │                    SYNC BARRIER + ps-critic Review                       │ |
|  │                                                                          │ |
|  │    ┌────────────────────────────────────────────────────────────────┐   │ |
|  │    │                   ★ GATE-4: Design Review ★                     │   │ |
|  │    │                   (Human Approval Required)                     │   │ |
|  │    └────────────────────────────┬───────────────────────────────────┘   │ |
|  └─────────────────────────────────┼───────────────────────────────────────┘ |
|                                    │                                         |
|          ══════════════════════════╪═══════════════════════════════         |
|                  FEAT-001 COMPLETE │ FEAT-002 BEGINS                        |
|          ══════════════════════════╪═══════════════════════════════         |
|                                    │                                         |
|                                    ▼                                         |
|  ┌─────────────────────────────────────────────────────────────────────────┐ |
|  │ PHASE 5: CORE IMPLEMENTATION                                             │ |
|  │ ──────────────────────────────                                           │ |
|  │                                                                          │ |
|  │    ┌──────────────────────────────────────────────────────────────────┐ │ |
|  │    │               EN-007: VTT Parser Implementation                    │ │ |
|  │    │  ┌───────────────┐ ┌───────────────┐ ┌───────────────┐          │ │ |
|  │    │  │Parser Agent   │ │Speaker ID     │ │Timestamp      │          │ │ |
|  │    │  │Prompt         │ │Logic          │ │Normalization  │          │ │ |
|  │    │  └───────────────┘ └───────────────┘ └───────────────┘          │ │ |
|  │    │  ┌───────────────┐ ┌───────────────┐                            │ │ |
|  │    │  │Chunking       │ │Unit Tests     │                            │ │ |
|  │    │  │Strategy       │ │               │                            │ │ |
|  │    │  └───────────────┘ └───────────────┘                            │ │ |
|  │    └──────────────────────────────┬───────────────────────────────────┘ │ |
|  │                                   │                                      │ |
|  │                                   ▼                                      │ |
|  │    ┌──────────────────────────────────────────────────────────────────┐ │ |
|  │    │               EN-008: Entity Extraction Pipeline                   │ │ |
|  │    │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐   │ │ |
|  │    │  │Speaker  │ │ Topic   │ │Question │ │ Action  │ │  Idea   │   │ │ |
|  │    │  │Profiler │ │Extractor│ │Detector │ │Extractor│ │Extractor│   │ │ |
|  │    │  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘   │ │ |
|  │    │  ┌─────────────┐ ┌─────────────────┐                           │ │ |
|  │    │  │  Decision   │ │   Confidence    │                           │ │ |
|  │    │  │  Extractor  │ │   Scoring       │                           │ │ |
|  │    │  └─────────────┘ └─────────────────┘                           │ │ |
|  │    └──────────────────────────────────────────────────────────────────┘ │ |
|  │                                                                          │ |
|  │                    SYNC BARRIER + Integration Tests                      │ |
|  │                                                                          │ |
|  │    ┌────────────────────────────────────────────────────────────────┐   │ |
|  │    │                   ★ GATE-5: Core Implementation Review ★        │   │ |
|  │    │                   (Human Approval Required)                     │   │ |
|  │    └────────────────────────────┬───────────────────────────────────┘   │ |
|  └─────────────────────────────────┼───────────────────────────────────────┘ |
|                                    │                                         |
|                                    ▼                                         |
|  ┌─────────────────────────────────────────────────────────────────────────┐ |
|  │ PHASE 6: OUTPUT GENERATION & INTEGRATION                                 │ |
|  │ ──────────────────────────────────────────                               │ |
|  │                                                                          │ |
|  │    ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐      │ |
|  │    │     EN-009       │ │     EN-010       │ │     EN-011       │      │ |
|  │    │   Mind Map       │ │    Artifact      │ │   Worktracker    │      │ |
|  │    │   Generator      │ │   Packaging      │ │   Integration    │      │ |
|  │    │  ┌────────────┐  │ │  ┌────────────┐  │ │  ┌────────────┐  │      │ |
|  │    │  │Mermaid Gen │  │ │  │Token Count │  │ │  │Suggestion  │  │      │ |
|  │    │  │ASCII Gen   │  │ │  │File Split  │  │ │  │Generator   │  │      │ |
|  │    │  │Deep Links  │  │ │  │Fwd Links   │  │ │  │Task Create │  │      │ |
|  │    │  └────────────┘  │ │  │Backlinks   │  │ │  │Story Create│  │      │ |
|  │    │                  │ │  │Index Gen   │  │ │  │Decision Rec│  │      │ |
|  │    │                  │ │  └────────────┘  │ │  └────────────┘  │      │ |
|  │    └──────────────────┘ └──────────────────┘ └──────────────────┘      │ |
|  │                                                                          │ |
|  │    ┌──────────────────┐ ┌──────────────────┐                            │ |
|  │    │     EN-012       │ │     EN-013       │                            │ |
|  │    │   Skill CLI      │ │ Context Injection│                            │ |
|  │    │   Interface      │ │ Implementation   │                            │ |
|  │    │  ┌────────────┐  │ │  ┌────────────┐  │                            │ |
|  │    │  │SKILL.md    │  │ │  │Context Load│  │                            │ |
|  │    │  │Cmd Handler │  │ │  │Prompt Merge│  │                            │ |
|  │    │  │Progress    │  │ │  │Metadata    │  │                            │ |
|  │    │  │Errors      │  │ │  │Examples    │  │                            │ |
|  │    │  └────────────┘  │ │  └────────────┘  │                            │ |
|  │    └──────────────────┘ └──────────────────┘                            │ |
|  │                                                                          │ |
|  │                    SYNC BARRIER + E2E Tests                              │ |
|  │                                                                          │ |
|  │    ┌────────────────────────────────────────────────────────────────┐   │ |
|  │    │                   ★ GATE-6: Final Review ★                      │   │ |
|  │    │                   (Human Approval Required)                     │   │ |
|  │    └────────────────────────────┬───────────────────────────────────┘   │ |
|  └─────────────────────────────────┼───────────────────────────────────────┘ |
|                                    │                                         |
|                                    ▼                                         |
|                    ┌────────────────────────────────────┐                   |
|                    │       TRANSCRIPT SKILL             │                   |
|                    │       COMPLETE & RELEASED          │                   |
|                    │                                    │                   |
|                    │  /transcript process meeting.vtt   │                   |
|                    └────────────────────────────────────┘                   |
+==============================================================================+
```

---

## Phase Details

### Phase 1: Parallel Research

**Duration:** Variable (depends on research depth)
**Parallel Tracks:** 2 (Market + Technical)
**Agents:** ps-researcher (x8), ps-synthesizer
**Gate:** GATE-1

#### EN-001: Market Analysis Research

| Task | Agent | Input | Output |
|------|-------|-------|--------|
| TASK-001 | ps-researcher | heypocket.com | Pocket analysis doc |
| TASK-002 | ps-researcher | otter.ai | Otter.ai analysis doc |
| TASK-003 | ps-researcher | fireflies.ai | Fireflies analysis doc |
| TASK-004 | ps-researcher | grain.com | Grain analysis doc |
| TASK-005 | ps-researcher | tldv.io | tl;dv analysis doc |
| TASK-006 | ps-synthesizer | All 5 docs | Feature comparison matrix |

#### EN-002: Technical Standards Research

| Task | Agent | Input | Output |
|------|-------|-------|--------|
| TASK-007 | ps-researcher | W3C WebVTT spec | VTT format analysis |
| TASK-008 | ps-researcher | SRT standards | SRT format analysis |
| TASK-009 | ps-researcher | NLP/NER literature | Best practices doc |

**Sync Barrier:** All 9 tasks complete → ps-critic review → GATE-1

---

### Phase 2: Requirements Synthesis

**Duration:** Variable
**Sequential:** Yes (depends on Phase 1)
**Agents:** ps-analyst, ps-synthesizer, ps-critic
**Gate:** GATE-2

#### EN-003: Requirements Synthesis

| Task | Agent | Input | Output |
|------|-------|-------|--------|
| TASK-010 | ps-analyst | Research findings | 5W2H analysis |
| TASK-011 | ps-analyst | Problem domain | Ishikawa diagram |
| TASK-012 | ps-analyst | Requirements | FMEA analysis |
| TASK-013 | ps-synthesizer | All analyses | Requirements spec (L0/L1/L2) |
| TASK-014 | ps-critic | Requirements spec | Review findings |

**Sync Barrier:** ps-critic approval → GATE-2

---

### Phase 3: Architecture Decisions

**Duration:** Variable
**Sequential:** Yes (depends on Phase 2)
**Agents:** ps-architect, ps-critic
**Gate:** GATE-3

#### EN-004: Architecture Decision Records

| Task | Agent | Input | Output |
|------|-------|-------|--------|
| TASK-016 | ps-architect | Requirements | ADR-001: Agent Architecture |
| TASK-017 | ps-architect | Requirements | ADR-002: Artifact Structure |
| TASK-018 | ps-architect | Requirements | ADR-003: Bidirectional Linking |
| TASK-019 | ps-architect | Requirements | ADR-004: File Splitting |
| TASK-020 | ps-architect | Requirements | ADR-005: Agent Implementation |
| TASK-021 | ps-critic | All ADRs | Review findings |

**Sync Barrier:** ps-critic approval → GATE-3

---

### Phase 4: Design Documentation

**Duration:** Variable
**Parallel Tracks:** 2 (EN-005 + EN-006)
**Agents:** ps-architect, ps-critic
**Gate:** GATE-4

#### EN-005: Design Documentation (Parallel)

All 6 component designs can be worked in parallel:
- VTT Parser Design
- Entity Extraction Pipeline Design
- Mind Map Generator Design
- Artifact Packager Design
- Deep Linking System Design
- Worktracker Integration Design

#### EN-006: Context Injection Design (Parallel)

- 5W2H Analysis
- Context Injection Specification
- Example Orchestration Plans

**Sync Barrier:** All designs complete → ps-critic review → GATE-4

---

### Phase 5: Core Implementation

**Duration:** Variable
**Sequential:** EN-007 → EN-008
**Agents:** Custom prompt-based agents
**Gate:** GATE-5

#### EN-007: VTT Parser Implementation

Sequential implementation of parser components.

#### EN-008: Entity Extraction Pipeline

Sequential after EN-007 (needs parser output).

**Sync Barrier:** Integration tests passing → GATE-5

---

### Phase 6: Output Generation & Integration

**Duration:** Variable
**Parallel Tracks:** EN-009, EN-010, EN-011 can parallelize after EN-008
**Sequential:** EN-012 needs EN-010; EN-013 needs EN-006
**Gate:** GATE-6

**Sync Barrier:** E2E tests passing → GATE-6 → RELEASE

---

## Checkpointing Strategy

### Checkpoint Triggers

| Trigger | Action |
|---------|--------|
| Task completion | Update ORCHESTRATION.yaml state |
| Gate reached | Full checkpoint + human notification |
| Error encountered | Checkpoint + pause for review |
| Session end | Full checkpoint with context |

### Checkpoint Contents

```yaml
checkpoint:
  timestamp: "2026-01-26T10:30:00Z"
  phase: 1
  gate_pending: GATE-1
  completed_tasks: [TASK-001, TASK-002, TASK-003]
  in_progress_tasks: [TASK-004]
  pending_tasks: [TASK-005, TASK-006, TASK-007, TASK-008, TASK-009]
  artifacts_produced:
    - path: research/pocket-analysis.md
      tokens: 8500
    - path: research/otterai-analysis.md
      tokens: 7200
  agent_state:
    ps-researcher:
      active: true
      current_task: TASK-004
```

---

## Human Approval Protocol

### Gate Notification Format

```
╭─────────────────────────────────────────────────────────────────╮
│                   ★ GATE-1: Research Review ★                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Phase 1 (Parallel Research) is complete.                       │
│                                                                  │
│  Completed Work:                                                 │
│  ✓ EN-001: Market Analysis Research                             │
│    - 5 competitive products analyzed                             │
│    - Feature comparison matrix synthesized                       │
│  ✓ EN-002: Technical Standards Research                         │
│    - VTT format documented                                       │
│    - NLP/NER best practices compiled                            │
│                                                                  │
│  Artifacts for Review:                                           │
│  1. research/pocket-analysis.md (8.5K tokens)                   │
│  2. research/otterai-analysis.md (7.2K tokens)                  │
│  3. research/fireflies-analysis.md (6.8K tokens)                │
│  4. research/grain-analysis.md (7.1K tokens)                    │
│  5. research/tldv-analysis.md (6.5K tokens)                     │
│  6. research/feature-matrix.md (4.2K tokens)                    │
│  7. research/vtt-format-spec.md (5.1K tokens)                   │
│  8. research/nlp-best-practices.md (8.9K tokens)                │
│                                                                  │
│  ps-critic Findings:                                             │
│  - 2 minor issues (documented in review.md)                     │
│  - Recommendation: APPROVE with notes                            │
│                                                                  │
│  Your Options:                                                   │
│  [APPROVE]     Proceed to Phase 2: Requirements Synthesis       │
│  [REVISE]      Request specific revisions (detail required)     │
│  [REJECT]      Return to Phase 1 (reason required)              │
│                                                                  │
╰─────────────────────────────────────────────────────────────────╯
```

### Approval Actions

| Action | Result |
|--------|--------|
| APPROVE | Proceed to next phase, checkpoint saved |
| REVISE | Specific tasks re-queued, partial checkpoint |
| REJECT | Phase restarted, checkpoint discarded |

---

## Error Handling

### Error Categories

| Category | Handling |
|----------|----------|
| Agent failure | Retry 3x, then escalate to human |
| Token overflow | Split artifact, re-validate links |
| Validation failure | Block gate, detail issues |
| External API error | Exponential backoff, then skip |

### Recovery Protocol

1. Checkpoint current state
2. Log error with full context
3. Attempt automatic recovery (if applicable)
4. Escalate to human if recovery fails
5. Resume from checkpoint after resolution

---

## Related Documents

| Document | Purpose |
|----------|---------|
| [WORKTRACKER.md](../../WORKTRACKER.md) | Task tracking |
| [ORCHESTRATION.yaml](./ORCHESTRATION.yaml) | Machine-readable state (SSOT) |
| [EPIC-001](../EPIC-001-transcript-skill.md) | Epic definition |
| [FEAT-001](../FEAT-001-analysis-design/FEAT-001-analysis-design.md) | Analysis & Design feature |
| [FEAT-002](../FEAT-002-implementation/FEAT-002-implementation.md) | Implementation feature |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-26 | Claude | Initial orchestration plan created |
