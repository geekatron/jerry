# ORCHESTRATION_PLAN.md

> **Document ID:** PROJ-001-ORCH-PLAN-FEAT014
> **Project:** PROJ-001-oss-release
> **Workflow ID:** `feat014-impl-20260217-001`
> **Status:** ACTIVE
> **Version:** 2.0
> **Created:** 2026-02-17
> **Last Updated:** 2026-02-17

---

## 1. Executive Summary

Orchestrate the synchronization of Jerry framework artifacts (agent registry, rules, skill documentation, tests) with deliverables from EPIC-002 (Progressive Disclosure) and EPIC-003 (Quality Implementation). Five enablers (EN-925 through EN-929) address registration gaps, rule updates, documentation completion, test coverage expansion, and minor documentation cleanup across 4 phases.

**Current State:** Workflow not started

**Orchestration Pattern:** Sequential with Parallel Fan-Out (single pipeline, phased enabler groups)

### 1.1 Workflow Identification

| Field | Value | Source |
|-------|-------|--------|
| Workflow ID | `feat014-impl-20260217-001` | auto |
| ID Format | `{purpose}-{YYYYMMDD}-{NNN}` | semantic-date-seq |
| Base Path | `FEAT-014-framework-synchronization/orchestration/feat014-impl-20260217-001/` | Dynamic |

**Artifact Output Locations:**
- Pipeline: `orchestration/feat014-impl-20260217-001/impl/`
- Phase artifacts: `orchestration/feat014-impl-20260217-001/impl/phase-{N}/`
- Synthesis: `orchestration/feat014-impl-20260217-001/synthesis/`

### 1.2 Key Design Decisions

| Decision | Value | Rationale |
|----------|-------|-----------|
| Criticality Level | **C2 (Standard)**, EN-926 elevated to **C3** | C2: Framework sync (reversible in 1 day, 3-10 files). EN-926 elevated to C3 per AE-002 (touches .context/rules/) |
| Quality Threshold | **>= 0.92** per enabler | H-13 (quality-enforcement SSOT) |
| Max Iterations | **3** per enabler | Standard creator→critic→revision cycle minimum |
| Strategy Set (C2) | **S-007, S-002, S-014** (required) + **S-003, S-010** (optional) | Per quality-enforcement.md C2 specification |
| Strategy Set (C3 for EN-926) | **S-007, S-002, S-014, S-004, S-012, S-013** (required) | Per quality-enforcement.md C3 specification |
| Scoring | **S-014 LLM-as-Judge** | 6-dimension weighted rubric |

---

## 2. Workflow Architecture

### 2.1 Pipeline Diagram

```
FEAT-014 FRAMEWORK SYNCHRONIZATION — SINGLE PIPELINE
=====================================================

┌─────────────────────────────────────────────────────────────┐
│ PHASE 1: Core Updates (3-way parallel fan-out)             │
│ ────────────────────────────────────────────────────────── │
│ • EN-925: Agent Registry Completion      [effort: 5, C2]   │
│ • EN-926: Rule Synchronization          [effort: 3, C3]   │
│ • EN-927: Skill Docs Completion         [effort: 5, C2]   │
│ Execution: PARALLEL (3 enablers, independent files)         │
│ STATUS: PENDING                                             │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
                    ╔═════════════╗
                    ║ CHECKPOINT  ║
                    ║   CP-001    ║
                    ╚═════════════╝
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ PHASE 2: Dependent Work (2-way parallel fan-out)            │
│ ────────────────────────────────────────────────────────── │
│ • EN-928: Test Coverage Expansion       [effort: 3, C2]   │
│ • EN-929: Minor Doc Cleanup             [effort: 2, C2]   │
│ Execution: PARALLEL (2 enablers, independent)               │
│ STATUS: PENDING (blocked by Phase 1)                        │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
                    ╔═════════════╗
                    ║ CHECKPOINT  ║
                    ║   CP-002    ║
                    ╚═════════════╝
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ PHASE 3: Verification                                        │
│ ────────────────────────────────────────────────────────── │
│ • Run full test suite (uv run pytest tests/)               │
│ • Run ruff check (uv run ruff check src/)                  │
│ • Verify all changes integrated correctly                   │
│ Execution: SEQUENTIAL                                       │
│ STATUS: PENDING (blocked by Phase 2)                        │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
                    ╔═════════════╗
                    ║ CHECKPOINT  ║
                    ║   CP-003    ║
                    ╚═════════════╝
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ PHASE 4: Synthesis                                           │
│ ────────────────────────────────────────────────────────── │
│ • Create FEAT-014 Final Synthesis                           │
│ • Update FEAT-014 worktracker status                        │
│ • Update EPIC-003 rollup                                    │
│ Execution: SEQUENTIAL                                       │
│ STATUS: PENDING (blocked by Phase 3)                        │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Orchestration Pattern Classification

| Pattern | Applied | Description |
|---------|---------|-------------|
| Sequential | Yes | Phases execute in order (Phase 1 before Phase 2) |
| Concurrent | Yes | Enablers within each phase run in parallel |
| Barrier Sync | No | Single pipeline, no cross-pollination needed |
| Hierarchical | Yes | Orchestrator delegates to worker agents |

### 2.3 Creator-Critic-Revision Cycle (Per Enabler)

```
   ┌──────────────────────────────────────────────────────┐
   │                ENABLER QUALITY CYCLE                  │
   │           (Applied to each EN-9xx enabler)            │
   │                                                       │
   │  ┌─────────┐     ┌─────────┐     ┌─────────┐        │
   │  │ CREATOR │────►│  CRITIC │────►│ REVISER │        │
   │  │  (impl) │     │ (critic)│     │  (impl) │        │
   │  └─────────┘     └────┬────┘     └────┬────┘        │
   │       │               │               │              │
   │       │          ┌────┴────┐          │              │
   │       │          │ SCORE?  │          │              │
   │       │          └────┬────┘          │              │
   │       │               │               │              │
   │       │    >= 0.92    │   < 0.92      │              │
   │       │    ┌──────────┤──────────┐    │              │
   │       │    │          │          │    │              │
   │       │    ▼          ▼          │    │              │
   │       │  PASS     FEEDBACK ──────┘────┘              │
   │       │    │      (loop back to CREATOR              │
   │       │    │       with critic findings)              │
   │       │    │                                          │
   │       │    │  After 3 iterations at C2:               │
   │       │    │  → User decision to continue/escalate    │
   │       │    │                                          │
   │       │    │  EN-926 (C3): 4th iteration available    │
   │       │    │                                          │
   │       │    ▼                                          │
   │       │  COMMIT                                       │
   │       │                                               │
   └───────┴───────────────────────────────────────────────┘

STRATEGIES APPLIED PER CYCLE:

  C2 Enablers (EN-925, EN-927, EN-928, EN-929):
    Creator:
      • S-010 (Self-Refine): Self-review before submitting deliverable (optional)

    Critic:
      • S-014 (LLM-as-Judge): 6-dimension weighted rubric scoring (REQUIRED)
      • S-007 (Constitutional AI): Principle compliance check (REQUIRED)
      • S-002 (Devil's Advocate): Strongest counterarguments (REQUIRED)
      • S-003 (Steelman): Charitable reconstruction (optional)

    Revision:
      • S-003 (Steelman): Understand critic feedback charitably (optional)
      • S-010 (Self-Refine): Self-review revised output (optional)

  C3 Enabler (EN-926 - touches .context/rules/):
    Creator:
      • S-010 (Self-Refine): Self-review before submitting (optional)

    Critic:
      • S-014 (LLM-as-Judge): 6-dimension weighted rubric (REQUIRED)
      • S-007 (Constitutional AI): Principle compliance (REQUIRED)
      • S-002 (Devil's Advocate): Counterarguments (REQUIRED)
      • S-004 (Pre-Mortem): "Imagine it failed — why?" (REQUIRED)
      • S-012 (FMEA): Systematic failure mode enumeration (REQUIRED)
      • S-013 (Inversion): "How could this fail?" (REQUIRED)
      • S-003 (Steelman): Charitable reconstruction (optional)
      • S-010 (Self-Refine): Applied in revision (optional)
      • S-011 (Chain-of-Verification): Factual verification (optional)
      • S-001 (Red Team): Adversary simulation (optional)
```

---

## 3. Phase Definitions

### 3.1 Phase 1: Core Updates

| Enabler | Title | Tasks | Effort | Criticality | Dependencies |
|---------|-------|-------|--------|-------------|--------------|
| EN-925 | Agent Registry Completion | 7 | 5 | C2 | None |
| EN-926 | Rule Synchronization | 3 | 3 | **C3 (AE-002)** | None |
| EN-927 | Skill Documentation Completion | 3 | 5 | C2 | None |

**Execution Mode:** PARALLEL (3 enablers touch independent files)

**Phase 1 Entry Criteria:**
- FEAT-014 worktracker entities exist on disk
- EPIC-002/003 deliverables available for reference

**Phase 1 Exit Criteria:**
- All 3 enablers pass >= 0.92 quality gate
- All 13 tasks marked DONE
- Git commit with clean working tree
- `uv run ruff check src/` passes (if Python files modified)

### 3.2 Phase 2: Dependent Work

| Enabler | Title | Tasks | Effort | Criticality | Dependencies |
|---------|-------|-------|--------|-------------|--------------|
| EN-928 | Test Coverage Expansion | 3 | 3 | C2 | EN-925, EN-926 (needs accurate agent list and rules) |
| EN-929 | Minor Documentation Cleanup | 5 | 2 | C2 | None |

**Execution Mode:** PARALLEL (2 enablers, independent workstreams)

**Phase 2 Entry Criteria:**
- Phase 1 complete (CP-001 verified)
- EN-925 agent registry updated (EN-928 needs agent list for test references)
- EN-926 rule updates committed (EN-928 needs to test against current rules)

**Phase 2 Exit Criteria:**
- Both enablers pass >= 0.92 quality gate
- All 8 tasks marked DONE
- `uv run pytest tests/` passes (includes new tests from EN-928)
- Git commit with clean working tree

### 3.3 Phase 3: Verification

| Step | Activity | Validation |
|------|----------|------------|
| 3.1 | Full test suite | `uv run pytest tests/ -v` all pass |
| 3.2 | Ruff linting | `uv run ruff check src/` clean |
| 3.3 | Type checking | `uv run mypy src/` clean (if applicable) |
| 3.4 | Pre-commit hooks | All hooks pass |
| 3.5 | Manual verification | Review AGENTS.md, rules/, skill docs for consistency |

**Execution Mode:** SEQUENTIAL

**Phase 3 Entry Criteria:**
- Phase 2 complete (CP-002 verified)
- All 5 enablers at >= 0.92

**Phase 3 Exit Criteria:**
- All automated checks pass
- Manual verification confirms no regressions
- Git working tree clean

### 3.4 Phase 4: Synthesis

| Step | Activity | Validation |
|------|----------|------------|
| 4.1 | Create Final Synthesis | Document all changes, impact, completion metrics |
| 4.2 | Update FEAT-014 worktracker | Mark feature completed, update enabler statuses |
| 4.3 | Update EPIC-003 rollup | Update completion percentage |

**Execution Mode:** SEQUENTIAL

**Phase 4 Entry Criteria:**
- Phase 3 complete (CP-003 verified)
- All enablers verified working correctly

**Phase 4 Exit Criteria:**
- Final Synthesis document created
- FEAT-014 marked completed
- EPIC-003 rollup updated

---

## 4. Adversarial Quality Protocol

### 4.1 Criticality-Driven Strategy Deployment

This workflow uses **C2 (Standard) level** for most enablers and **C3 (Significant) level** for EN-926 due to auto-escalation rule AE-002 (touches `.context/rules/`).

#### C2 Strategy Set (EN-925, EN-927, EN-928, EN-929)

| Strategy | ID | Role in Cycle | Applied By |
|----------|----|---------------|------------|
| LLM-as-Judge | S-014 | 6-dimension weighted rubric scoring (REQUIRED) | Critic |
| Constitutional AI | S-007 | Principle-by-principle compliance (REQUIRED) | Critic |
| Devil's Advocate | S-002 | Strongest counterarguments (REQUIRED) | Critic |
| Self-Refine | S-010 | Creator self-review before submission (optional) | Creator + Revision |
| Steelman | S-003 | Charitable reconstruction (optional) | Critic + Revision |

#### C3 Strategy Set (EN-926 - Rule Synchronization)

| Strategy | ID | Role in Cycle | Applied By |
|----------|----|---------------|------------|
| LLM-as-Judge | S-014 | 6-dimension weighted rubric scoring (REQUIRED) | Critic |
| Constitutional AI | S-007 | Principle compliance check (REQUIRED) | Critic |
| Devil's Advocate | S-002 | Strongest counterarguments (REQUIRED) | Critic |
| Pre-Mortem | S-004 | "Imagine it failed — why?" (REQUIRED) | Critic |
| FMEA | S-012 | Systematic failure mode enumeration (REQUIRED) | Critic |
| Inversion | S-013 | "How could this fail?" (REQUIRED) | Critic |
| Self-Refine | S-010 | Self-review (optional) | Creator + Revision |
| Steelman | S-003 | Charitable reconstruction (optional) | Critic + Revision |
| Chain-of-Verification | S-011 | Factual verification (optional) | Critic |
| Red Team | S-001 | Adversary simulation (optional) | Critic |

### 4.2 Scoring Dimensions

| Dimension | Weight | Minimum for PASS |
|-----------|--------|------------------|
| Completeness | 0.20 | 0.88 |
| Internal Consistency | 0.20 | 0.88 |
| Methodological Rigor | 0.20 | 0.88 |
| Evidence Quality | 0.15 | 0.85 |
| Actionability | 0.15 | 0.85 |
| Traceability | 0.10 | 0.85 |
| **Weighted Composite** | **1.00** | **>= 0.92** |

### 4.3 Iteration Protocol

| Iteration | Creator Action | Critic Action | Outcome |
|-----------|---------------|---------------|---------|
| 1 | Initial deliverable (S-010 optional self-review) | Full scoring (all required strategies) | PASS or REVISE |
| 2 | Revise with critic feedback (S-003 + S-010 optional) | Re-score with focus on prior gaps | PASS or REVISE |
| 3 | Targeted revision of remaining gaps | Re-score remaining dimensions | PASS or ESCALATE (C2) / REVISE (C3) |
| 4 (C3 only) | Final attempt for EN-926 | Final scoring | PASS or ESCALATE |

**Note:** C2 enablers have minimum 3 iterations. EN-926 (C3) has additional iteration capacity before escalation.

### 4.4 Leniency Bias Countermeasures

Per quality-enforcement.md and EPIC-003 learnings, the critic must:
1. Score each dimension independently (no halo effect)
2. Resolve uncertain scores **downward**
3. No dimension scored above 0.90 without exceptional evidence
4. Mathematically verify weighted composite calculation
5. Explicitly justify any dimension score >= 0.90

---

## 5. Agent Registry

### 5.1 Phase 1 Agents

| Agent ID | Role | Enabler | Input | Output |
|----------|------|---------|-------|--------|
| en925-creator | impl | EN-925 | Enabler spec + EPIC-002/003 agents | Updated AGENTS.md |
| en925-critic | critic | EN-925 | Creator deliverable + C2 strategies | Critic report with S-014 scores |
| en926-creator | impl | EN-926 | Enabler spec + quality-enforcement.md | Updated mandatory-skill-usage.md |
| en926-critic | critic | EN-926 | Creator deliverable + C3 strategies | Critic report with S-014 scores |
| en927-creator | impl | EN-927 | Enabler spec + architecture/bootstrap references | Updated architecture/SKILL.md, bootstrap/SKILL.md |
| en927-critic | critic | EN-927 | Creator deliverable + C2 strategies | Critic report with S-014 scores |

### 5.2 Phase 2 Agents

| Agent ID | Role | Enabler | Input | Output |
|----------|------|---------|-------|--------|
| en928-creator | impl | EN-928 | Enabler spec + test/ directory + EN-925/926 results | New test files |
| en928-critic | critic | EN-928 | Creator deliverable + C2 strategies | Critic report with S-014 scores |
| en929-creator | impl | EN-929 | Enabler spec + various docs | Updated documentation files |
| en929-critic | critic | EN-929 | Creator deliverable + C2 strategies | Critic report with S-014 scores |

### 5.3 Phase 3 Agents

| Agent ID | Role | Input | Output |
|----------|------|-------|--------|
| verifier | impl | All Phase 1-2 changes | Verification report |

### 5.4 Phase 4 Agents

| Agent ID | Role | Input | Output |
|----------|------|-------|--------|
| synthesizer | orch-synthesizer | All phase results + metrics | Final Synthesis |

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
FEAT-014-framework-synchronization/
└── orchestration/
    └── feat014-impl-20260217-001/
        ├── ORCHESTRATION_PLAN.md          (this file)
        ├── ORCHESTRATION_WORKTRACKER.md
        ├── ORCHESTRATION.yaml
        ├── impl/
        │   ├── phase-1-core-updates/
        │   │   ├── en925-creator/          (creator deliverables)
        │   │   ├── en925-critic/           (critic reports)
        │   │   ├── en926-creator/          (C3 criticality)
        │   │   ├── en926-critic/
        │   │   ├── en927-creator/
        │   │   └── en927-critic/
        │   ├── phase-2-dependent-work/
        │   │   ├── en928-creator/
        │   │   ├── en928-critic/
        │   │   ├── en929-creator/
        │   │   └── en929-critic/
        │   ├── phase-3-verification/
        │   │   └── verifier/
        │   └── phase-4-synthesis/
        │       └── synthesis/
        └── checkpoints/
```

### 6.3 Checkpoint Strategy

| Trigger | When | Purpose |
|---------|------|---------|
| CP-001 | Phase 1 complete | Core updates verified, rollback point |
| CP-002 | Phase 2 complete | Dependent work verified |
| CP-003 | Phase 3 complete | Verification passed, pre-synthesis |
| MANUAL | User-triggered | Debug and inspection |

---

## 7. Execution Constraints

### 7.1 Hard Constraints (Jerry Constitution)

| Constraint | ID | Enforcement |
|------------|----|----|
| Single agent nesting | P-003 | Orchestrator -> Worker only. No agent-to-agent calls. |
| File persistence | P-002 | All state to filesystem. No transient planning. |
| No deception | P-022 | Transparent reasoning. Honest scoring. |
| User authority | P-020 | User approves at escalation points. |
| Quality threshold | H-13 | >= 0.92 weighted composite per enabler |
| Self-review required | H-15 | S-010 applied before submission (optional for C2, recommended) |
| Steelman before critique | H-16 | S-003 before S-002 when both used |

### 7.1.1 Worktracker Entity Templates

> **WTI-007:** Entity files created during orchestration MUST use canonical templates from `.context/templates/worktracker/`.

### 7.2 Soft Constraints

| Constraint | Value | Rationale |
|------------|-------|-----------|
| Max concurrent agents | 3 | Parallel enablers within a phase |
| Max iterations per enabler | 3 (C2), 4 (C3) | Per criticality level specification |
| Checkpoint frequency | PHASE | Phase-level rollback granularity |
| Git commit frequency | Per phase | Clean working tree after each phase |

---

## 8. Success Criteria

### 8.1 Phase Exit Criteria (All Phases)

| Criterion | Validation |
|-----------|------------|
| All enablers in phase pass >= 0.92 | S-014 weighted composite score |
| All tasks marked DONE | Enabler task inventory check |
| Git commit with clean tree | `git status` clean |
| Pre-commit hooks pass | All hooks green |

### 8.2 Workflow Completion Criteria

| Criterion | Validation |
|-----------|------------|
| All 5 enablers pass >= 0.92 | Quality score tracking in ORCHESTRATION.yaml |
| `uv run pytest tests/` passes | Full test suite green |
| `uv run ruff check src/` clean | Linting passes |
| Final Synthesis created | synthesis/ directory |
| FEAT-014 marked completed | Worktracker status update |
| EPIC-003 rollup updated | Percentage reflects FEAT-014 completion |

---

## 9. Risk Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Enabler fails to reach 0.92 in allowed iterations | Medium | High | Focus critic feedback on weakest dimension. Escalate to user if needed. |
| Context rot during long phases | Low | Medium | Each enabler is a fresh agent invocation. Re-read rules at phase boundaries. |
| EN-926 rule changes break existing workflows | Medium | High | C3 criticality with full strategy set. Phase 3 verification includes manual review. |
| Test coverage expansion (EN-928) insufficient | Medium | Medium | EN-928 creator runs `uv run pytest` before submitting. Critic validates test quality. |
| Circular dependency between Phase 1 enablers | Low | Low | EN-925, EN-926, EN-927 designed to be independent. |
| Documentation inconsistencies after changes | Medium | Medium | Phase 3 includes manual verification step. EN-929 addresses minor cleanup. |

---

## 10. Resumption Context

### 10.1 Current Execution State

```
WORKFLOW STATUS AS OF 2026-02-17
================================

Phase 1 (Core Updates):       PENDING
  EN-925 (Agent Registry):     PENDING [C2]
  EN-926 (Rule Sync):          PENDING [C3 - AE-002]
  EN-927 (Skill Docs):         PENDING [C2]

Phase 2 (Dependent Work):     PENDING (blocked by Phase 1)
  EN-928 (Test Coverage):      PENDING [C2]
  EN-929 (Doc Cleanup):        PENDING [C2]

Phase 3 (Verification):       PENDING (blocked by Phase 2)

Phase 4 (Synthesis):          PENDING (blocked by Phase 3)

Checkpoints:
  CP-001:                      PENDING
  CP-002:                      PENDING
  CP-003:                      PENDING
```

### 10.2 Next Actions

1. Execute Phase 1: Launch EN-925, EN-926, EN-927 creator agents in parallel
2. Run critic cycle for each enabler (C2: 3 iterations, EN-926 C3: up to 4 iterations)
3. Git commit Phase 1 results
4. Create CP-001 checkpoint
5. Proceed to Phase 2 with EN-928, EN-929

---

**DISCLAIMER:** This orchestration plan is generated by the `orch-planner` agent (v2.2.0). The orchestrator agent will execute this plan and manage state via ORCHESTRATION.yaml and ORCHESTRATION_WORKTRACKER.md. All paths are repository-relative for cross-session portability.

---

*Document ID: PROJ-001-ORCH-PLAN-FEAT014*
*Workflow ID: feat014-impl-20260217-001*
*Version: 2.0*
*Cross-Session Portable: All paths are repository-relative*
