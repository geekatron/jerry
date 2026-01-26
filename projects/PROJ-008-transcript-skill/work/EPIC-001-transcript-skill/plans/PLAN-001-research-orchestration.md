# PLAN-001: Research Phase Orchestration

> **Plan ID:** PLAN-001
> **Status:** READY_FOR_EXECUTION
> **Created:** 2026-01-25T00:00:00Z
> **Phase:** 0 - Research & Discovery
> **Parent Feature:** FEAT-001
> **Estimated Duration:** 1-2 weeks

---

## Executive Summary

This plan defines the multi-agent orchestration workflow for the Research & Discovery phase (Phase 0) of the Transcript Skill project. It coordinates parallel research pipelines across competitive analysis, technical standards research, and requirements synthesis with sync barriers and quality gates.

---

## Orchestration Architecture

### Agent Roster

| Agent | Role | Tasks | Input | Output |
|-------|------|-------|-------|--------|
| ps-researcher (x5) | Competitive research | TASK-001..005 | Product URLs | Analysis docs |
| ps-researcher (x4) | Technical research | TASK-007..010 | Specs/papers | Tech docs |
| ps-synthesizer | Feature matrix | TASK-006 | Research docs | Matrix |
| ps-analyst (x3) | Framework analysis | TASK-011..013 | Research | 5W2H, Ishikawa, FMEA |
| nse-requirements | Requirements doc | TASK-014 | Analyses | Spec |
| ps-critic | Adversarial review | TASK-015 | Spec | Review |

### Pipeline Overview

```
+==============================================================================+
|                     PHASE 0: RESEARCH ORCHESTRATION PIPELINE                  |
+==============================================================================+
|                                                                               |
|  ┌─────────────────────────────────────────────────────────────────────────┐ |
|  │                         PHASE 0A: PARALLEL RESEARCH                      │ |
|  │                         ════════════════════════                         │ |
|  │                                                                           │ |
|  │   PIPELINE A: COMPETITIVE ANALYSIS          PIPELINE B: TECHNICAL        │ |
|  │   ─────────────────────────────────         ─────────────────────        │ |
|  │                                                                           │ |
|  │   ┌─────────┐ ┌─────────┐ ┌─────────┐      ┌─────────┐ ┌─────────┐      │ |
|  │   │TASK-001 │ │TASK-002 │ │TASK-003 │      │TASK-007 │ │TASK-008 │      │ |
|  │   │ Pocket  │ │Otter.ai │ │Fireflies│      │  VTT    │ │  SRT    │      │ |
|  │   └────┬────┘ └────┬────┘ └────┬────┘      └────┬────┘ └────┬────┘      │ |
|  │        │           │           │                │           │            │ |
|  │   ┌─────────┐ ┌─────────┐                  ┌─────────┐ ┌─────────┐      │ |
|  │   │TASK-004 │ │TASK-005 │                  │TASK-009 │ │TASK-010 │      │ |
|  │   │  Grain  │ │ tl;dv   │                  │ NLP/NER │ │Academic │      │ |
|  │   └────┬────┘ └────┬────┘                  └────┬────┘ └────┬────┘      │ |
|  │        │           │                            │           │            │ |
|  │        └─────┬─────┘                            └─────┬─────┘            │ |
|  │              │                                        │                  │ |
|  │   ┌──────────┴──────────┐              ┌──────────────┴────────────┐    │ |
|  │   │    TASK-006         │              │                           │    │ |
|  │   │ Feature Matrix      │              │                           │    │ |
|  │   │ (ps-synthesizer)    │              │                           │    │ |
|  │   └──────────┬──────────┘              │                           │    │ |
|  │              │                         │                           │    │ |
|  │   ┌──────────┴─────────────────────────┴────────────────────────┐  │    │ |
|  │   │                    SYNC BARRIER 1                            │  │    │ |
|  │   │          (All EN-001 + EN-002 tasks complete)               │  │    │ |
|  │   └──────────────────────────────────────────────────────────────┘  │    │ |
|  └─────────────────────────────────────────────────────────────────────────┘ |
|                                         │                                     |
|                                         ▼                                     |
|  ┌─────────────────────────────────────────────────────────────────────────┐ |
|  │                         PHASE 0B: FRAMEWORK ANALYSIS                     │ |
|  │                         ═══════════════════════════                      │ |
|  │                                                                           │ |
|  │   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                 │ |
|  │   │ TASK-011    │    │ TASK-012    │    │ TASK-013    │                 │ |
|  │   │   5W2H      │    │  Ishikawa   │    │   FMEA      │                 │ |
|  │   │(ps-analyst) │    │(ps-analyst) │    │(ps-analyst) │                 │ |
|  │   └──────┬──────┘    └──────┬──────┘    └──────┬──────┘                 │ |
|  │          │                  │                  │                         │ |
|  │   ┌──────┴──────────────────┴──────────────────┴──────┐                 │ |
|  │   │                    SYNC BARRIER 2                  │                 │ |
|  │   │          (All framework analyses complete)         │                 │ |
|  │   └────────────────────────────────────────────────────┘                 │ |
|  └─────────────────────────────────────────────────────────────────────────┘ |
|                                         │                                     |
|                                         ▼                                     |
|  ┌─────────────────────────────────────────────────────────────────────────┐ |
|  │                         PHASE 0C: SYNTHESIS & REVIEW                     │ |
|  │                         ═══════════════════════════                      │ |
|  │                                                                           │ |
|  │   ┌────────────────┐         ┌────────────────┐                         │ |
|  │   │   TASK-014     │ ──────▶ │   TASK-015     │                         │ |
|  │   │  Requirements  │         │   ps-critic    │                         │ |
|  │   │(nse-requirements)        │   Review       │                         │ |
|  │   └────────────────┘         └───────┬────────┘                         │ |
|  │                                      │                                   │ |
|  │                    ┌─────────────────┼─────────────────┐                │ |
|  │                    │                 │                 │                │ |
|  │                    ▼                 ▼                 ▼                │ |
|  │               ┌────────┐       ┌──────────┐     ┌─────────────┐        │ |
|  │               │APPROVED│       │  REVISE  │     │  ESCALATE   │        │ |
|  │               │        │       │(max 2x)  │     │ (to human)  │        │ |
|  │               └────┬───┘       └────┬─────┘     └──────┬──────┘        │ |
|  │                    │                │                  │                │ |
|  │                    │                └──────────────────┤                │ |
|  │                    │                                   │                │ |
|  │   ┌────────────────┴───────────────────────────────────┴──────────┐    │ |
|  │   │                    SYNC BARRIER 3                              │    │ |
|  │   │                   (Human Approval)                             │    │ |
|  │   └────────────────────────────────────────────────────────────────┘    │ |
|  └─────────────────────────────────────────────────────────────────────────┘ |
|                                         │                                     |
|                                         ▼                                     |
|                              ┌──────────────────────┐                        |
|                              │   PHASE 0 COMPLETE    │                        |
|                              │   Proceed to Phase 1  │                        |
|                              └──────────────────────┘                        |
+==============================================================================+
```

---

## Execution Phases

### Phase 0A: Parallel Research

**Duration:** 3-5 days
**Parallelism:** Up to 9 agents running concurrently

#### Pipeline A: Competitive Analysis (EN-001)

| Step | Task | Agent | Input | Output | Duration |
|------|------|-------|-------|--------|----------|
| A.1 | TASK-001 | ps-researcher | heypocket.com | POCKET-analysis.md | 2-4h |
| A.2 | TASK-002 | ps-researcher | otter.ai | OTTER-analysis.md | 2-4h |
| A.3 | TASK-003 | ps-researcher | fireflies.ai | FIREFLIES-analysis.md | 2-4h |
| A.4 | TASK-004 | ps-researcher | grain.com | GRAIN-analysis.md | 2-4h |
| A.5 | TASK-005 | ps-researcher | tldv.io | TLDV-analysis.md | 2-4h |
| A.6 | TASK-006 | ps-synthesizer | All analyses | FEATURE-MATRIX.md | 2-4h |

**Note:** A.1-A.5 run in parallel. A.6 waits for all to complete.

#### Pipeline B: Technical Standards (EN-002)

| Step | Task | Agent | Input | Output | Duration |
|------|------|-------|-------|--------|----------|
| B.1 | TASK-007 | ps-researcher | W3C WebVTT spec | VTT-SPECIFICATION.md | 2-4h |
| B.2 | TASK-008 | ps-researcher | SRT spec | SRT-SPECIFICATION.md | 2-4h |
| B.3 | TASK-009 | ps-researcher | NLP resources | NLP-NER-BEST-PRACTICES.md | 3-5h |
| B.4 | TASK-010 | ps-researcher | Academic sources | ACADEMIC-LITERATURE-REVIEW.md | 2-4h |

**Note:** B.1-B.4 run in parallel.

#### Sync Barrier 1

**Condition:** All tasks in EN-001 (TASK-001..006) AND EN-002 (TASK-007..010) complete.

**Verification:**
```yaml
sync_barrier_1:
  condition: ALL_COMPLETE
  required_artifacts:
    - research/POCKET-analysis.md
    - research/OTTER-analysis.md
    - research/FIREFLIES-analysis.md
    - research/GRAIN-analysis.md
    - research/TLDV-analysis.md
    - research/FEATURE-MATRIX.md
    - research/VTT-SPECIFICATION.md
    - research/SRT-SPECIFICATION.md
    - research/NLP-NER-BEST-PRACTICES.md
    - research/ACADEMIC-LITERATURE-REVIEW.md
```

---

### Phase 0B: Framework Analysis

**Duration:** 2-3 days
**Parallelism:** 3 agents running concurrently
**Prerequisite:** Sync Barrier 1 passed

#### Analysis Tasks (EN-003 Part 1)

| Step | Task | Agent | Input | Output | Duration |
|------|------|-------|-------|--------|----------|
| C.1 | TASK-011 | ps-analyst | All research | 5W2H-ANALYSIS.md | 3-5h |
| C.2 | TASK-012 | ps-analyst | All research | ISHIKAWA-DIAGRAM.md | 3-5h |
| C.3 | TASK-013 | ps-analyst | All research | FMEA-ANALYSIS.md | 4-6h |

**Note:** C.1-C.3 run in parallel.

#### Sync Barrier 2

**Condition:** All framework analysis tasks (TASK-011..013) complete.

**Verification:**
```yaml
sync_barrier_2:
  condition: ALL_COMPLETE
  required_artifacts:
    - research/5W2H-ANALYSIS.md
    - research/ISHIKAWA-DIAGRAM.md
    - research/FMEA-ANALYSIS.md
```

---

### Phase 0C: Synthesis & Review

**Duration:** 2-3 days
**Parallelism:** Sequential (requirements → review)
**Prerequisite:** Sync Barrier 2 passed

#### Synthesis Tasks (EN-003 Part 2)

| Step | Task | Agent | Input | Output | Duration |
|------|------|-------|-------|--------|----------|
| D.1 | TASK-014 | nse-requirements | All analyses | REQUIREMENTS-SPEC.md | 4-6h |
| D.2 | TASK-015 | ps-critic | Requirements | CRITIC-REVIEW.md | 2-4h |

**Note:** D.2 may loop back to D.1 if REVISE verdict (max 2 iterations).

#### Critic Review Protocol

```
┌───────────────────────────────────────────────────────────────┐
│                    CRITIC REVIEW PROTOCOL                      │
├───────────────────────────────────────────────────────────────┤
│                                                                │
│  INPUT: REQUIREMENTS-SPEC.md                                  │
│                                                                │
│  REVIEW CRITERIA:                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ 1. Traceability: All requirements cite evidence?        │ │
│  │ 2. INVEST: Requirements meet INVEST criteria?           │ │
│  │ 3. Verifiability: Acceptance criteria testable?         │ │
│  │ 4. Completeness: All failure modes mitigated?           │ │
│  │ 5. Consistency: No logical contradictions?              │ │
│  │ 6. Edge Cases: Unusual scenarios covered?               │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                                │
│  VERDICTS:                                                    │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ APPROVED     │ Proceed to Phase 1 implementation        │ │
│  │ REVISE       │ Specific issues listed, iteration N/2    │ │
│  │ ESCALATE     │ Fundamental issues, human decision       │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                                │
│  OUTPUT: CRITIC-REVIEW.md with verdict and feedback          │
└───────────────────────────────────────────────────────────────┘
```

#### Sync Barrier 3 (Human Approval)

**Condition:** ps-critic review APPROVED or ESCALATE decision made.

**Human Review Checklist:**
- [ ] Research thoroughness acceptable
- [ ] Feature matrix comprehensive
- [ ] Framework analyses valid
- [ ] Requirements complete and clear
- [ ] Critic concerns addressed
- [ ] Ready to proceed to implementation

---

## Cross-Pollination Points

### Research → Analysis Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    CROSS-POLLINATION MAP                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  COMPETITIVE RESEARCH (EN-001)                                  │
│  ────────────────────────────                                   │
│  Pocket Analysis ─────────────┐                                 │
│  Otter Analysis ──────────────┼──▶ Feature Matrix ─────────┐   │
│  Fireflies Analysis ──────────┤                             │   │
│  Grain Analysis ──────────────┤                             │   │
│  tl;dv Analysis ──────────────┘                             │   │
│                                                              │   │
│  TECHNICAL RESEARCH (EN-002)                                 │   │
│  ───────────────────────────                                 │   │
│  VTT Specification ───────────┐                             │   │
│  SRT Specification ───────────┼──▶ Tech Requirements ───────┼───▶
│  NLP Best Practices ──────────┤                             │   │
│  Academic Papers ─────────────┘                             │   │
│                                                              │   │
│                               ┌──────────────────────────────┘   │
│                               │                                  │
│                               ▼                                  │
│  FRAMEWORK ANALYSIS (EN-003)                                    │
│  ───────────────────────────                                    │
│  5W2H Analysis ───────────────┐                                 │
│  Ishikawa Diagram ────────────┼──▶ Requirements Spec           │
│  FMEA Analysis ───────────────┘                                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Agent Instructions

### ps-researcher Configuration

```yaml
agent: ps-researcher
mode: research
tools:
  - WebFetch
  - WebSearch
  - Read
  - Write
output_format: L0/L1/L2 documentation
citation_required: true
evidence_standard: high
```

### ps-analyst Configuration

```yaml
agent: ps-analyst
mode: analysis
inputs:
  - research documents
  - feature matrix
frameworks:
  - 5W2H
  - Ishikawa
  - FMEA
output_format: structured analysis with diagrams
```

### ps-synthesizer Configuration

```yaml
agent: ps-synthesizer
mode: synthesis
inputs:
  - all research documents
output:
  - FEATURE-MATRIX.md
  - feature-matrix.yaml (machine-readable)
```

### nse-requirements Configuration

```yaml
agent: nse-requirements
mode: requirements_engineering
inputs:
  - competitive analysis
  - technical research
  - framework analyses
output:
  - REQUIREMENTS-SPEC.md
standards:
  - INVEST criteria
  - NASA NPR 7123.1D (adapted)
```

### ps-critic Configuration

```yaml
agent: ps-critic
mode: adversarial_review
inputs:
  - REQUIREMENTS-SPEC.md
  - all research artifacts
output:
  - CRITIC-REVIEW.md
verdicts:
  - APPROVED
  - REVISE
  - ESCALATE
max_iterations: 2
```

---

## Quality Gates

### Gate 1: Research Quality

| Criterion | Threshold | Verification |
|-----------|-----------|--------------|
| Products analyzed | 5/5 | All analysis docs exist |
| Features documented | 10+ per product | Feature count in matrix |
| Citations per doc | 5+ | Citation count |
| L0/L1/L2 coverage | 100% | All levels present |

### Gate 2: Framework Quality

| Criterion | Threshold | Verification |
|-----------|-----------|--------------|
| 5W2H completeness | All 7 questions | Question coverage |
| Ishikawa categories | 6 categories | Category count |
| FMEA failure modes | 10+ modes | Mode count |
| FMEA RPN scores | All calculated | Score presence |

### Gate 3: Requirements Quality

| Criterion | Threshold | Verification |
|-----------|-----------|--------------|
| Requirements count | 15+ | Requirement count |
| INVEST compliance | 100% | Criteria checklist |
| Traceability | All traced | Evidence links |
| Critic approval | APPROVED | Review verdict |

---

## Checkpoints

### Checkpoint A: Post-Research

**Trigger:** Sync Barrier 1 reached
**Actions:**
1. Save orchestration state
2. Update WORKTRACKER.md
3. Notify user of progress
4. Create checkpoint file

### Checkpoint B: Post-Analysis

**Trigger:** Sync Barrier 2 reached
**Actions:**
1. Save orchestration state
2. Update WORKTRACKER.md
3. Review framework outputs
4. Create checkpoint file

### Checkpoint C: Pre-Human Review

**Trigger:** Critic review complete
**Actions:**
1. Save orchestration state
2. Package all artifacts for review
3. Generate summary report
4. Notify user for approval

---

## Related Artifacts

| Artifact | Path | Purpose |
|----------|------|---------|
| WORKTRACKER | `WORKTRACKER.md` | Track overall progress |
| FEAT-001 | `FEAT-001-competitive-research.md` | Parent feature |
| EN-001 | `EN-001-market-analysis.md` | Competitive research |
| EN-002 | `EN-002-technical-standards.md` | Technical research |
| EN-003 | `EN-003-requirements-synthesis.md` | Requirements synthesis |

---

## History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-25 | Claude | Initial orchestration plan created |
