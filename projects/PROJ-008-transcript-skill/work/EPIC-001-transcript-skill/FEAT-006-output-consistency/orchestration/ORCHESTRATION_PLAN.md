# ORCHESTRATION_PLAN.md

> **Document ID:** PROJ-008-FEAT-006-ORCH-PLAN
> **Project:** PROJ-008-transcript-skill
> **Workflow ID:** `feat-006-output-consistency-20260131-001`
> **Status:** ACTIVE
> **Version:** 1.0
> **Created:** 2026-01-31
> **Last Updated:** 2026-01-31

---

## 1. Executive Summary

Address critical transcript skill output inconsistency when using different LLM models (Sonnet vs Opus). The workflow performs systematic gap analysis, historical research, industry best practices research, specification design, and implementation with adversarial critic validation at each phase.

**Current State:** Workflow initialized, Phase 0 ready for execution

**Orchestration Pattern:** Sequential Pipeline with Adversarial Critic Loops

### 1.1 Workflow Identification

| Field | Value | Source |
|-------|-------|--------|
| Workflow ID | `feat-006-output-consistency-20260131-001` | auto |
| ID Format | `{purpose}-{YYYYMMDD}-{NNN}` | semantic-date-seq |
| Base Path | `projects/PROJ-008-transcript-skill/work/EPIC-001-transcript-skill/FEAT-006-output-consistency/orchestration/` | Dynamic |

**Artifact Output Locations:**
- Research: `docs/research/`
- Analysis: `docs/analysis/`
- Decisions: `docs/decisions/`
- Critiques: `critiques/`

---

## 2. Workflow Architecture

### 2.1 Pipeline Diagram

```
FEAT-006 OUTPUT CONSISTENCY ORCHESTRATION
=========================================

 ┌────────────────────────────────────────────────────────────────────────────┐
 │                           PHASE 0: GAP ANALYSIS                             │
 │  ═══════════════════════════════════════════════════════════════════════   │
 │                                                                             │
 │  ┌───────────────────────────────────────────────────────────────────┐    │
 │  │ ps-analyst                                                         │    │
 │  │ ──────────────────────────────────────────────────────────────────│    │
 │  │ Compare:                                                           │    │
 │  │ • Downloads/chats/2026-01-30-certificate-       │    │
 │  │   architecture/ (Sonnet - CORRECT)                                 │    │
 │  │ • Downloads/chats/2026-01-30-certificate-       │    │
 │  │   architecture-opus-v2/ (Opus - INCORRECT)                         │    │
 │  │                                                                    │    │
 │  │ Deliverable: gap-analysis.md                                       │    │
 │  └───────────────────────────────────────────────────────────────────┘    │
 │                                 │                                          │
 │                                 ▼                                          │
 │  ┌───────────────────────────────────────────────────────────────────┐    │
 │  │ ps-critic (G-001)                                                  │    │
 │  │ ──────────────────────────────────────────────────────────────────│    │
 │  │ Quality Gate >= 0.85                                               │    │
 │  │ PASS → Continue to Phase 1                                         │    │
 │  │ FAIL → Feedback upstream, iterate                                  │    │
 │  └───────────────────────────────────────────────────────────────────┘    │
 └────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
 ┌────────────────────────────────────────────────────────────────────────────┐
 │                       PHASE 1: HISTORICAL RESEARCH                          │
 │  ═══════════════════════════════════════════════════════════════════════   │
 │                                                                             │
 │  ┌───────────────────────────────────────────────────────────────────┐    │
 │  │ ps-researcher                                                      │    │
 │  │ ──────────────────────────────────────────────────────────────────│    │
 │  │ Search FEAT-001 for existing template specifications:              │    │
 │  │ • ADR-002 (packet structure)                                       │    │
 │  │ • ADR-003 (anchor registry)                                        │    │
 │  │ • ADR-004 (file splitting)                                         │    │
 │  │ • TDD-transcript-skill.md                                          │    │
 │  │ • ts-formatter agent definition                                    │    │
 │  │                                                                    │    │
 │  │ Deliverable: historical-research.md                                │    │
 │  └───────────────────────────────────────────────────────────────────┘    │
 │                                 │                                          │
 │                                 ▼                                          │
 │  ┌───────────────────────────────────────────────────────────────────┐    │
 │  │ ps-critic (G-002)                                                  │    │
 │  │ ──────────────────────────────────────────────────────────────────│    │
 │  │ Quality Gate >= 0.85                                               │    │
 │  └───────────────────────────────────────────────────────────────────┘    │
 └────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
 ┌────────────────────────────────────────────────────────────────────────────┐
 │                       PHASE 2: INDUSTRY RESEARCH (DEEP)                     │
 │  ═══════════════════════════════════════════════════════════════════════   │
 │                                                                             │
 │  ┌───────────────────────────────────────────────────────────────────┐    │
 │  │ ps-researcher + nse-requirements-engineer                          │    │
 │  │ ──────────────────────────────────────────────────────────────────│    │
 │  │ Deep Research:                                                     │    │
 │  │ • Context7: Library documentation patterns                         │    │
 │  │ • WebSearch: Meeting transcript format standards                   │    │
 │  │ • WebSearch: Citation/linking systems best practices               │    │
 │  │ • WebSearch: Multi-persona documentation (ELI5, Engineer, Arch)    │    │
 │  │                                                                    │    │
 │  │ Frameworks Applied:                                                │    │
 │  │ • 5W2H (What, Why, Who, When, Where, How, How Much)                │    │
 │  │ • Ishikawa (Fishbone root cause)                                   │    │
 │  │ • Pareto Analysis (80/20)                                          │    │
 │  │ • FMEA (Failure Mode Effects Analysis)                             │    │
 │  │ • 8D (Eight Disciplines)                                           │    │
 │  │ • NASA SE Handbook                                                 │    │
 │  │                                                                    │    │
 │  │ Deliverable: industry-research.md                                  │    │
 │  └───────────────────────────────────────────────────────────────────┘    │
 │                                 │                                          │
 │                                 ▼                                          │
 │  ┌───────────────────────────────────────────────────────────────────┐    │
 │  │ ps-critic (G-003)                                                  │    │
 │  │ ──────────────────────────────────────────────────────────────────│    │
 │  │ Quality Gate >= 0.85                                               │    │
 │  └───────────────────────────────────────────────────────────────────┘    │
 └────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
 ┌────────────────────────────────────────────────────────────────────────────┐
 │                      PHASE 3: SPECIFICATION DESIGN                          │
 │  ═══════════════════════════════════════════════════════════════════════   │
 │                                                                             │
 │  ┌───────────────────────────────────────────────────────────────────┐    │
 │  │ ps-architect + nse-architect                                       │    │
 │  │ ──────────────────────────────────────────────────────────────────│    │
 │  │ Design golden output template specification:                       │    │
 │  │ • File structure (exact names, order)                              │    │
 │  │ • Naming conventions                                               │    │
 │  │ • Citation/linking format                                          │    │
 │  │ • Navigation link requirements                                     │    │
 │  │ • Content structure for each file type                             │    │
 │  │                                                                    │    │
 │  │ Deliverables:                                                      │    │
 │  │ • ADR-007-output-template-specification.md                         │    │
 │  │ • golden-template-spec.md                                          │    │
 │  └───────────────────────────────────────────────────────────────────┘    │
 │                                 │                                          │
 │                                 ▼                                          │
 │  ┌───────────────────────────────────────────────────────────────────┐    │
 │  │ ps-critic (G-004)                                                  │    │
 │  │ ──────────────────────────────────────────────────────────────────│    │
 │  │ Quality Gate >= 0.90 (higher threshold for spec)                   │    │
 │  └───────────────────────────────────────────────────────────────────┘    │
 └────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
 ┌────────────────────────────────────────────────────────────────────────────┐
 │                         PHASE 4: IMPLEMENTATION                             │
 │  ═══════════════════════════════════════════════════════════════════════   │
 │                                                                             │
 │  ┌───────────────────────────────────────────────────────────────────┐    │
 │  │ Implementation Tasks                                               │    │
 │  │ ──────────────────────────────────────────────────────────────────│    │
 │  │ 1. Update ts-formatter agent definition                            │    │
 │  │    - Add template enforcement section                              │    │
 │  │    - Add guardrails to prevent model drift                         │    │
 │  │ 2. Update SKILL.md with template specification                     │    │
 │  │ 3. Update PLAYBOOK.md with validation steps                        │    │
 │  │ 4. Create validation test cases                                    │    │
 │  │                                                                    │    │
 │  │ Deliverables:                                                      │    │
 │  │ • Updated agents/ts-formatter.md                                   │    │
 │  │ • Updated SKILL.md                                                 │    │
 │  │ • validation-test-cases.yaml                                       │    │
 │  └───────────────────────────────────────────────────────────────────┘    │
 │                                 │                                          │
 │                                 ▼                                          │
 │  ┌───────────────────────────────────────────────────────────────────┐    │
 │  │ ps-critic (G-005)                                                  │    │
 │  │ ──────────────────────────────────────────────────────────────────│    │
 │  │ Quality Gate >= 0.90                                               │    │
 │  └───────────────────────────────────────────────────────────────────┘    │
 └────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
 ┌────────────────────────────────────────────────────────────────────────────┐
 │                        PHASE 5: VALIDATION & REVIEW                         │
 │  ═══════════════════════════════════════════════════════════════════════   │
 │                                                                             │
 │  ┌───────────────────────────────────────────────────────────────────┐    │
 │  │ Validation Tasks                                                   │    │
 │  │ ──────────────────────────────────────────────────────────────────│    │
 │  │ 1. Run transcript skill with economy profile                       │    │
 │  │ 2. Run transcript skill with balanced profile                      │    │
 │  │ 3. Run transcript skill with quality profile                       │    │
 │  │ 4. Run transcript skill with speed profile                         │    │
 │  │ 5. Compare outputs for structural consistency                      │    │
 │  │                                                                    │    │
 │  │ Deliverables:                                                      │    │
 │  │ • validation-report.md (all profiles)                              │    │
 │  └───────────────────────────────────────────────────────────────────┘    │
 │                                 │                                          │
 │                                 ▼                                          │
 │  ┌───────────────────────────────────────────────────────────────────┐    │
 │  │ ps-critic (G-FINAL)                                                │    │
 │  │ ──────────────────────────────────────────────────────────────────│    │
 │  │ Final Quality Gate >= 0.95                                         │    │
 │  │ Validates entire feature completion                                │    │
 │  └───────────────────────────────────────────────────────────────────┘    │
 └────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Orchestration Pattern Classification

| Pattern | Applied | Description |
|---------|---------|-------------|
| Sequential | Yes | Phases execute in order |
| Concurrent | No | Single pipeline |
| Barrier Sync | No | No cross-pollination needed |
| Adversarial | Yes | ps-critic validation at each phase |
| Hierarchical | Yes | Orchestrator delegates to agents |

---

## 3. Phase Definitions

### 3.1 Phase Summary

| Phase | Name | Purpose | Agents | Status |
|-------|------|---------|--------|--------|
| 0 | Gap Analysis | Compare Sonnet vs Opus outputs | ps-analyst | PENDING |
| 1 | Historical Research | Find existing template specs | ps-researcher | PENDING |
| 2 | Industry Research | Deep industry best practices | ps-researcher, nse-req-eng | PENDING |
| 3 | Specification Design | Create golden template spec | ps-architect, nse-architect | PENDING |
| 4 | Implementation | Update agent definitions | direct-work | PENDING |
| 5 | Validation & Review | Test all profiles | validation + ps-critic | PENDING |

### 3.2 Input/Output Matrix

| Phase | Inputs | Outputs |
|-------|--------|---------|
| 0 | Two transcript output directories | gap-analysis.md |
| 1 | Gap analysis + FEAT-001 artifacts | historical-research.md |
| 2 | Gap + Historical + External sources | industry-research.md |
| 3 | All research artifacts | ADR-007 + golden-template-spec.md |
| 4 | Specification documents | Updated agent/skill files |
| 5 | Implementation + test transcript | validation-report.md |

---

## 4. Quality Gate Protocol

### 4.1 Adversarial Critic Loop

```
FOR EACH PHASE:
┌─────────────────────────────────────────────────────────────────┐
│                     ADVERSARIAL CRITIC LOOP                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   1. Agent executes phase work                                  │
│      └─► Produces deliverable artifact                          │
│                                                                  │
│   2. ps-critic evaluates artifact                               │
│      └─► Applies quality criteria                               │
│      └─► Generates critique with score                          │
│                                                                  │
│   3. Quality Gate Check                                         │
│      ├─► IF score >= threshold → PASS, continue to next phase   │
│      └─► IF score < threshold → FAIL, iterate                   │
│                                                                  │
│   4. IF FAIL:                                                    │
│      ├─► Critique provides specific feedback                    │
│      ├─► Feedback sent upstream to agent                        │
│      ├─► Agent revises artifact                                 │
│      └─► Loop back to step 2 (max 3 iterations)                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Quality Gate Thresholds

| Gate | Phase | Threshold | Criteria |
|------|-------|-----------|----------|
| G-001 | Phase 0 | >= 0.85 | Gap completeness, evidence quality |
| G-002 | Phase 1 | >= 0.85 | Research depth, source citations |
| G-003 | Phase 2 | >= 0.85 | Framework coverage, industry sources |
| G-004 | Phase 3 | >= 0.90 | Spec completeness, clarity, traceability |
| G-005 | Phase 4 | >= 0.90 | Implementation correctness, guardrails |
| G-FINAL | Phase 5 | >= 0.95 | All profiles consistent, acceptance criteria met |

---

## 5. Agent Registry

### 5.1 Phase 0 Agents

| Agent ID | Role | Input Artifacts | Output Artifacts | Status |
|----------|------|-----------------|------------------|--------|
| ps-analyst-001 | Gap Analysis | Two transcript directories | docs/analysis/gap-analysis.md | PENDING |
| ps-critic-G001 | Quality Gate | gap-analysis.md | critiques/G-001-critique.md | PENDING |

### 5.2 Phase 1 Agents

| Agent ID | Role | Input Artifacts | Output Artifacts | Status |
|----------|------|-----------------|------------------|--------|
| ps-researcher-001 | Historical Research | FEAT-001 artifacts | docs/research/historical-research.md | PENDING |
| ps-critic-G002 | Quality Gate | historical-research.md | critiques/G-002-critique.md | PENDING |

### 5.3 Phase 2 Agents

| Agent ID | Role | Input Artifacts | Output Artifacts | Status |
|----------|------|-----------------|------------------|--------|
| ps-researcher-002 | Industry Research | External sources | docs/research/industry-research.md | PENDING |
| nse-req-eng-001 | Requirements Analysis | Industry research | docs/analysis/requirements-synthesis.md | PENDING |
| ps-critic-G003 | Quality Gate | industry-research.md | critiques/G-003-critique.md | PENDING |

### 5.4 Phase 3 Agents

| Agent ID | Role | Input Artifacts | Output Artifacts | Status |
|----------|------|-----------------|------------------|--------|
| ps-architect-001 | Spec Design | All research | docs/decisions/ADR-007.md | PENDING |
| nse-architect-001 | Spec Validation | ADR-007 | docs/analysis/spec-validation.md | PENDING |
| ps-critic-G004 | Quality Gate | ADR-007 + spec | critiques/G-004-critique.md | PENDING |

### 5.5 Phase 4 Agents

| Agent ID | Role | Input Artifacts | Output Artifacts | Status |
|----------|------|-----------------|------------------|--------|
| direct-work | Implementation | Specifications | Updated skill files | PENDING |
| ps-critic-G005 | Quality Gate | Updated files | critiques/G-005-critique.md | PENDING |

### 5.6 Phase 5 Agents

| Agent ID | Role | Input Artifacts | Output Artifacts | Status |
|----------|------|-----------------|------------------|--------|
| validation | Profile Testing | Test transcript | validation-report.md | PENDING |
| ps-critic-FINAL | Final Gate | All deliverables | critiques/G-FINAL-critique.md | PENDING |

---

## 6. State Management

### 6.1 State Files

| File | Purpose |
|------|---------|
| `ORCHESTRATION.yaml` | Machine-readable state (SSOT) |
| `ORCHESTRATION_WORKTRACKER.md` | Tactical execution documentation |
| `ORCHESTRATION_PLAN.md` | This file - strategic context |

### 6.2 Artifact Path Structure

```
FEAT-006-output-consistency/
├── FEAT-006-output-consistency.md    # Feature file
├── orchestration/
│   ├── ORCHESTRATION_PLAN.md         # This file
│   ├── ORCHESTRATION_WORKTRACKER.md  # Tactical tracking
│   ├── ORCHESTRATION.yaml            # Machine state
│   └── critiques/
│       ├── G-001-critique.md
│       ├── G-002-critique.md
│       ├── G-003-critique.md
│       ├── G-004-critique.md
│       ├── G-005-critique.md
│       └── G-FINAL-critique.md
├── docs/
│   ├── research/
│   │   ├── historical-research.md
│   │   └── industry-research.md
│   ├── analysis/
│   │   ├── gap-analysis.md
│   │   ├── requirements-synthesis.md
│   │   └── spec-validation.md
│   └── decisions/
│       └── ADR-007-output-template-specification.md
└── EN-030-gap-analysis/              # Enabler folders (future)
    └── EN-030-gap-analysis.md
```

---

## 7. Execution Constraints

### 7.1 Hard Constraints (Jerry Constitution)

| Constraint | ID | Enforcement |
|------------|----|----|
| Single agent nesting | P-003 | Orchestrator → Worker only |
| File persistence | P-002 | All state to filesystem |
| No deception | P-022 | Transparent reasoning |
| User authority | P-020 | User approves gates |

### 7.2 Soft Constraints

| Constraint | Value | Rationale |
|------------|-------|-----------|
| Max critic iterations | 3 | Avoid infinite loops |
| Checkpoint frequency | PHASE | Recovery at phase boundaries |
| Research depth | Deep | User-requested thorough research |

---

## 8. Success Criteria

### 8.1 Phase-Level Exit Criteria

| Phase | Exit Criteria |
|-------|---------------|
| 0 | Gap analysis identifies all structural differences |
| 1 | All existing template specs found and documented |
| 2 | Industry best practices cited with sources |
| 3 | ADR-007 approved with complete specification |
| 4 | All skill files updated per specification |
| 5 | All 4 profiles produce consistent output |

### 8.2 Feature Completion Criteria

| Criterion | Validation |
|-----------|------------|
| All phases complete | All phase status = COMPLETE |
| All quality gates pass | All G-* scores >= threshold |
| Acceptance criteria met | All AC-* verified in FEAT-006 |
| Profile consistency | Same structure across all 4 profiles |

---

## 9. Risk Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| No existing template spec in FEAT-001 | Medium | Low | Proceed to industry research |
| Industry standards vary widely | Medium | Medium | Synthesize common patterns |
| Implementation breaks other features | Low | High | Test all profiles before merge |
| Model-specific behavior persists | Medium | High | Add strict guardrails + validation |

---

## 10. Resumption Context

### 10.1 Current Execution State

```
WORKFLOW STATUS AS OF 2026-01-31
================================

Phase 0 (Gap Analysis):        PENDING
Phase 1 (Historical Research): PENDING
Phase 2 (Industry Research):   PENDING
Phase 3 (Specification):       PENDING
Phase 4 (Implementation):      PENDING
Phase 5 (Validation):          PENDING

Quality Gates:
  G-001: PENDING
  G-002: PENDING
  G-003: PENDING
  G-004: PENDING
  G-005: PENDING
  G-FINAL: PENDING
```

### 10.2 Next Actions

1. Execute Phase 0: ps-analyst gap analysis
2. Run G-001 quality gate
3. If PASS, proceed to Phase 1
4. If FAIL, iterate with critic feedback

---

*Document ID: PROJ-008-FEAT-006-ORCH-PLAN*
*Workflow ID: feat-006-output-consistency-20260131-001*
*Version: 1.0*
*Cross-Session Portable: All paths are repository-relative*
