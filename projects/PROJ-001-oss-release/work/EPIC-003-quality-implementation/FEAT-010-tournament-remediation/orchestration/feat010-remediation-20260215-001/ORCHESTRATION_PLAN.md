# ORCHESTRATION_PLAN.md

> **Document ID:** PROJ-001-ORCH-PLAN-FEAT010
> **Project:** PROJ-001-oss-release
> **Workflow ID:** `feat010-remediation-20260215-001`
> **Status:** ACTIVE
> **Version:** 2.0
> **Created:** 2026-02-15
> **Last Updated:** 2026-02-15

---

## 1. Executive Summary

Orchestrate the remediation of 45 findings (7 Critical, 18 Major, 20 Minor) from the FEAT-009 C4 Tournament Review. The tournament scored FEAT-009 at 0.85 composite (REVISE band, gap of 0.07 to the 0.92 threshold). Seven enablers (EN-813 through EN-819) address these findings across 4 phases with C4-level adversarial quality enforcement.

**Current State:** Workflow not started

**Orchestration Pattern:** Sequential with Checkpoints (single pipeline, phased enabler groups)

### 1.1 Workflow Identification

| Field | Value | Source |
|-------|-------|--------|
| Workflow ID | `feat010-remediation-20260215-001` | auto |
| ID Format | `{purpose}-{YYYYMMDD}-{NNN}` | semantic-date-seq |
| Base Path | `FEAT-010-tournament-remediation/orchestration/feat010-remediation-20260215-001/` | Dynamic |

**Artifact Output Locations:**
- Pipeline: `orchestration/feat010-remediation-20260215-001/impl/`
- Phase artifacts: `orchestration/feat010-remediation-20260215-001/impl/phase-{N}/`
- Synthesis: `orchestration/feat010-remediation-20260215-001/synthesis/`

### 1.2 Key Design Decisions

| Decision | Value | Rationale |
|----------|-------|-----------|
| Criticality Level | **C4 (Critical)** | Remediating C4 tournament findings on framework governance templates |
| Quality Threshold | **>= 0.92** per enabler | H-13 (quality-enforcement SSOT) |
| Max Iterations | **4** per enabler | User directive: 4 iterations before human escalation |
| Strategy Set | **All 10** | C4 requires all selected strategies |
| Scoring | **S-014 LLM-as-Judge** | 6-dimension weighted rubric |

---

## 2. Workflow Architecture

### 2.1 Pipeline Diagram

```
FEAT-010 TOURNAMENT REMEDIATION — SINGLE PIPELINE (C4)
=======================================================

┌─────────────────────────────────────────────────────────────┐
│ PHASE 1: P0 Critical Fixes (EN-813, EN-814, EN-815)        │
│ ────────────────────────────────────────────────────────── │
│ • EN-813: Template Context Optimization      [effort: 5]   │
│ • EN-814: Finding ID Scoping & Uniqueness    [effort: 3]   │
│ • EN-815: Documentation & Navigation Fixes   [effort: 2]   │
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
│ PHASE 2: P1 Documentation & Runtime (EN-816, EN-817)        │
│ ────────────────────────────────────────────────────────── │
│ • EN-816: Skill Documentation Completeness   [effort: 3]   │
│ • EN-817: Runtime Enforcement                [effort: 5]   │
│ Execution: PARALLEL (2 enablers, independent files)         │
│ STATUS: PENDING                                             │
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
│ PHASE 3: P1 CI & SSOT (EN-818, EN-819)                      │
│ ────────────────────────────────────────────────────────── │
│ • EN-818: Template Validation CI Gate        [effort: 5]   │
│ • EN-819: SSOT Consistency & Resilience      [effort: 3]   │
│ Execution: PARALLEL (2 enablers, independent files)         │
│ STATUS: PENDING                                             │
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
│ PHASE 4: Integration Validation & Synthesis                  │
│ ────────────────────────────────────────────────────────── │
│ • Run full E2E test suite                                   │
│ • Run ruff check + pytest                                   │
│ • Create FEAT-010 Final Synthesis                           │
│ • Re-score FEAT-009 with S-014 to validate >= 0.92          │
│ Execution: SEQUENTIAL                                       │
│ STATUS: PENDING                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Orchestration Pattern Classification

| Pattern | Applied | Description |
|---------|---------|-------------|
| Sequential | Yes | Phases execute in order (P0 before P1) |
| Concurrent | Yes | Enablers within each phase run in parallel |
| Barrier Sync | No | Single pipeline, no cross-pollination needed |
| Hierarchical | Yes | Orchestrator delegates to worker agents |

### 2.3 Creator-Critic-Revision Cycle (Per Enabler)

```
   ┌──────────────────────────────────────────────────────┐
   │                ENABLER QUALITY CYCLE                  │
   │           (Applied to each EN-8xx enabler)            │
   │                                                       │
   │  ┌─────────┐     ┌─────────┐     ┌─────────┐        │
   │  │ CREATOR │────►│  CRITIC │────►│ REVISER │        │
   │  │(ps-arch)│     │(ps-crit)│     │(ps-arch)│        │
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
   │       │    │  After 4 failed iterations:              │
   │       │    │  → HUMAN ESCALATION (AE-006)             │
   │       │    │                                          │
   │       │    ▼                                          │
   │       │  COMMIT                                       │
   │       │                                               │
   └───────┴───────────────────────────────────────────────┘

STRATEGIES APPLIED PER CYCLE:

  Creator (ps-architect):
    • S-010 (Self-Refine): Self-review before submitting deliverable

  Critic (ps-critic):
    • S-014 (LLM-as-Judge): 6-dimension weighted rubric scoring
    • S-007 (Constitutional AI): Principle compliance check
    • S-003 (Steelman): Charitable reconstruction FIRST (H-16)
    • S-002 (Devil's Advocate): Strongest counterarguments AFTER S-003
    • S-013 (Inversion): "How could this fail?"
    • S-004 (Pre-Mortem): "Imagine it failed — why?"
    • S-012 (FMEA): Systematic failure mode enumeration
    • S-011 (CoVe): Factual verification of claims
    • S-001 (Red Team): Adversary simulation

  Revision (ps-architect receives critic feedback):
    • S-003 (Steelman): Understand critic feedback charitably
    • S-010 (Self-Refine): Self-review revised output
```

---

## 3. Phase Definitions

### 3.1 Phase 1: P0 Critical Fixes

| Enabler | Title | Tasks | Effort | Tournament Findings |
|---------|-------|-------|--------|---------------------|
| EN-813 | Template Context Optimization | 4 | 5 | T-001 (bloat) |
| EN-814 | Finding ID Scoping & Uniqueness | 3 | 3 | T-002 (ID collision) |
| EN-815 | Documentation & Navigation Fixes | 5 | 2 | T-007 (nav), T-023, T-026, T-027, T-028 |

**Execution Mode:** PARALLEL (3 enablers touch independent files)

**Phase 1 Entry Criteria:**
- FEAT-010 worktracker entities exist on disk
- Source material (C4 tournament synthesis) read and understood

**Phase 1 Exit Criteria:**
- All 3 enablers pass >= 0.92 quality gate
- All 12 tasks marked DONE
- Git commit with clean working tree
- `uv run pytest tests/e2e/` passes

### 3.2 Phase 2: P1 Documentation & Runtime

| Enabler | Title | Tasks | Effort | Tournament Findings |
|---------|-------|-------|--------|---------------------|
| EN-816 | Skill Documentation Completeness | 4 | 3 | T-008, T-014, T-022 |
| EN-817 | Runtime Enforcement | 5 | 5 | T-004, T-006, T-009 |

**Execution Mode:** PARALLEL (2 enablers, independent agent spec files)

**Phase 2 Entry Criteria:**
- Phase 1 complete (CP-001 verified)

**Phase 2 Exit Criteria:**
- Both enablers pass >= 0.92 quality gate
- All 9 tasks marked DONE
- Git commit with clean working tree

### 3.3 Phase 3: P1 CI & SSOT

| Enabler | Title | Tasks | Effort | Tournament Findings |
|---------|-------|-------|--------|---------------------|
| EN-818 | Template Validation CI Gate | 4 | 5 | T-005, T-003 |
| EN-819 | SSOT Consistency & Resilience | 4 | 3 | T-017, T-016 |

**Execution Mode:** PARALLEL (2 enablers, EN-818 is CI/Python, EN-819 is markdown)

**Phase 3 Entry Criteria:**
- Phase 2 complete (CP-002 verified)
- EN-817 runtime enforcement in place (EN-818 CI tests may reference it)

**Phase 3 Exit Criteria:**
- Both enablers pass >= 0.92 quality gate
- `uv run pytest tests/e2e/` passes (includes new validation tests)
- `uv run ruff check src/` clean (for validate_templates.py)
- Git commit with clean working tree

### 3.4 Phase 4: Integration Validation & Synthesis

| Step | Activity | Validation |
|------|----------|------------|
| 4.1 | Full E2E test suite | `uv run pytest tests/e2e/ -v` all pass |
| 4.2 | Ruff + type checks | `uv run ruff check src/` clean |
| 4.3 | Re-score FEAT-009 with S-014 | Composite >= 0.92 |
| 4.4 | Create Final Synthesis | Document remediation results |
| 4.5 | Update FEAT-010 worktracker | Mark feature completed |

**Execution Mode:** SEQUENTIAL

**Phase 4 Entry Criteria:**
- Phases 1-3 complete (CP-003 verified)
- All 7 enablers at >= 0.92

**Phase 4 Exit Criteria:**
- FEAT-009 re-scored at >= 0.92 composite
- Final Synthesis document created
- FEAT-010 marked completed
- EPIC-003 rollup updated (100% if FEAT-010 is last)

---

## 4. Adversarial Quality Protocol

### 4.1 C4 Strategy Deployment

This workflow uses **C4 (Critical) level** adversarial quality enforcement. All 10 selected strategies are deployed per the quality-enforcement SSOT.

| Strategy | ID | Role in Cycle | Applied By |
|----------|----|---------------|------------|
| Self-Refine | S-010 | Creator self-review before submission | Creator (ps-architect) |
| LLM-as-Judge | S-014 | 6-dimension weighted rubric scoring | Critic (ps-critic) |
| Constitutional AI | S-007 | Principle-by-principle compliance | Critic |
| Steelman | S-003 | Charitable reconstruction FIRST (H-16) | Critic + Revision |
| Devil's Advocate | S-002 | Strongest counterarguments AFTER S-003 | Critic |
| Inversion | S-013 | "How could this fail?" analysis | Critic |
| Pre-Mortem | S-004 | "Imagine it failed — why?" | Critic |
| FMEA | S-012 | Systematic failure mode enumeration | Critic |
| Chain-of-Verification | S-011 | Factual verification of claims | Critic |
| Red Team | S-001 | Adversary simulation | Critic |

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
| 1 | Initial deliverable (S-010 self-review) | Full C4 scoring (all 10 strategies) | PASS or REVISE |
| 2 | Revise with critic feedback (S-003 + S-010) | Re-score with focus on prior gaps | PASS or REVISE |
| 3 | Targeted revision of remaining gaps | Re-score remaining dimensions | PASS or REVISE |
| 4 | Final attempt with explicit gap closure | Final scoring | PASS or ESCALATE |
| 5+ | **HUMAN ESCALATION (AE-006)** | User reviews and directs | User decides |

### 4.4 Leniency Bias Countermeasures

Per the C4 tournament findings (T-020), the critic must:
1. Score each dimension independently (no halo effect)
2. Resolve uncertain scores **downward**
3. Verify every Critical finding is reflected in dimensional scores
4. No dimension scored above 0.90 without exceptional evidence
5. Mathematically verify weighted composite calculation

---

## 5. Agent Registry

### 5.1 Phase 1 Agents (per enabler)

| Agent ID | Role | Model | Input | Output |
|----------|------|-------|-------|--------|
| en813-creator | ps-architect | sonnet | EN-813 enabler + tasks + tournament T-001 | Modified adv-executor.md, PLAYBOOK.md |
| en813-critic | ps-critic | opus | Creator deliverables + all 10 strategies | Critic report with S-014 scores |
| en814-creator | ps-architect | sonnet | EN-814 enabler + tasks + tournament T-002 | Modified templates + TEMPLATE-FORMAT.md |
| en814-critic | ps-critic | opus | Creator deliverables + all 10 strategies | Critic report with S-014 scores |
| en815-creator | ps-architect | sonnet | EN-815 enabler + tasks + tournament T-007/T-023/T-026-T-028 | Modified templates + CLAUDE.md |
| en815-critic | ps-critic | opus | Creator deliverables + all 10 strategies | Critic report with S-014 scores |

### 5.2 Phase 2 Agents

| Agent ID | Role | Model | Input | Output |
|----------|------|-------|-------|--------|
| en816-creator | ps-architect | sonnet | EN-816 enabler + tasks + tournament T-008/T-014/T-022 | Modified SKILL.md, PLAYBOOK.md, adv-executor.md |
| en816-critic | ps-critic | opus | Creator deliverables | Critic report |
| en817-creator | ps-architect | sonnet | EN-817 enabler + tasks + tournament T-004/T-006/T-009 | Modified agent specs + E2E tests |
| en817-critic | ps-critic | opus | Creator deliverables | Critic report |

### 5.3 Phase 3 Agents

| Agent ID | Role | Model | Input | Output |
|----------|------|-------|-------|--------|
| en818-creator | ps-architect | sonnet | EN-818 enabler + tasks + tournament T-005/T-003 | validate_templates.py, pre-commit config, CI job |
| en818-critic | ps-critic | opus | Creator deliverables | Critic report |
| en819-creator | ps-architect | sonnet | EN-819 enabler + tasks + tournament T-017/T-016 | Modified quality-enforcement.md, templates, adv-executor.md |
| en819-critic | ps-critic | opus | Creator deliverables | Critic report |

### 5.4 Phase 4 Agents

| Agent ID | Role | Model | Input | Output |
|----------|------|-------|-------|--------|
| feat009-rescorer | ps-critic | opus | All FEAT-009 deliverables post-remediation | S-014 re-score report |
| feat010-synthesizer | orch-synthesizer | sonnet | All phase results + re-score | Final Synthesis |

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
FEAT-010-tournament-remediation/
└── orchestration/
    └── feat010-remediation-20260215-001/
        ├── ORCHESTRATION_PLAN.md          (this file)
        ├── ORCHESTRATION_WORKTRACKER.md
        ├── ORCHESTRATION.yaml
        ├── impl/
        │   ├── phase-1-p0-critical/
        │   │   ├── en813-creator/          (creator deliverables)
        │   │   ├── en813-critic/           (critic reports)
        │   │   ├── en814-creator/
        │   │   ├── en814-critic/
        │   │   ├── en815-creator/
        │   │   └── en815-critic/
        │   ├── phase-2-p1-docs-runtime/
        │   │   ├── en816-creator/
        │   │   ├── en816-critic/
        │   │   ├── en817-creator/
        │   │   └── en817-critic/
        │   ├── phase-3-p1-ci-ssot/
        │   │   ├── en818-creator/
        │   │   ├── en818-critic/
        │   │   ├── en819-creator/
        │   │   └── en819-critic/
        │   └── phase-4-integration/
        │       ├── feat009-rescore/
        │       └── synthesis/
        └── checkpoints/
```

### 6.3 Checkpoint Strategy

| Trigger | When | Purpose |
|---------|------|---------|
| CP-001 | Phase 1 complete | P0 Critical fixes verified, rollback point |
| CP-002 | Phase 2 complete | P1 docs + runtime verified |
| CP-003 | Phase 3 complete | P1 CI + SSOT verified, pre-integration |
| MANUAL | User-triggered | Debug and inspection |

---

## 7. Execution Constraints

### 7.1 Hard Constraints (Jerry Constitution)

| Constraint | ID | Enforcement |
|------------|----|----|
| Single agent nesting | P-003 | Orchestrator -> Worker only. No agent-to-agent calls. |
| File persistence | P-002 | All state to filesystem. No transient planning. |
| No deception | P-022 | Transparent reasoning. Honest scoring. |
| User authority | P-020 | User approves at iteration 4 escalation. |
| Quality threshold | H-13 | >= 0.92 weighted composite per enabler |
| Steelman before critique | H-16 | S-003 MUST execute before S-002 |
| Self-review required | H-15 | S-010 applied before every submission |

### 7.1.1 Worktracker Entity Templates

> **WTI-007:** Entity files created during orchestration MUST use canonical templates from `.context/templates/worktracker/`.

### 7.2 Soft Constraints

| Constraint | Value | Rationale |
|------------|-------|-----------|
| Max concurrent agents | 3 | Parallel enablers within a phase |
| Max iterations per enabler | 4 | User directive (override of default 3) |
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
| All 7 enablers pass >= 0.92 | Quality score tracking in ORCHESTRATION.yaml |
| FEAT-009 re-scored at >= 0.92 | Phase 4 S-014 re-assessment |
| `uv run pytest tests/e2e/` passes | Full E2E suite green |
| `uv run ruff check src/` clean | Linting passes |
| Final Synthesis created | synthesis/ directory |
| FEAT-010 marked completed | Worktracker status update |

---

## 9. Risk Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Enabler fails to reach 0.92 in 4 iterations | Medium | High | Human escalation at iteration 4 (AE-006). Focus critic feedback on weakest dimension. |
| Context rot during long phases | Medium | Medium | Each enabler is a fresh agent invocation. Re-read rules at phase boundaries. |
| EN-818 Python code fails ruff/pytest | Low | Medium | Creator runs `uv run ruff check` and `uv run pytest` before submitting. |
| EN-819 SSOT changes break existing tests | Medium | High | Run full E2E suite after EN-819 changes. Phase 3 includes validation. |
| Leniency bias in self-scoring | High | High | Critic uses strict rubric. Uncertain scores resolved downward. No dimension above 0.90 without evidence. |
| Circular dependency between enablers | Low | Low | All enablers designed to be independent within their phase. |

---

## 10. Resumption Context

### 10.1 Current Execution State

```
WORKFLOW STATUS AS OF 2026-02-15
================================

Phase 1 (P0 Critical):     PENDING
  EN-813:                   PENDING
  EN-814:                   PENDING
  EN-815:                   PENDING

Phase 2 (P1 Docs+Runtime): PENDING (blocked by Phase 1)
  EN-816:                   PENDING
  EN-817:                   PENDING

Phase 3 (P1 CI+SSOT):      PENDING (blocked by Phase 2)
  EN-818:                   PENDING
  EN-819:                   PENDING

Phase 4 (Integration):     PENDING (blocked by Phase 3)
  FEAT-009 Re-Score:        PENDING
  Final Synthesis:          PENDING

Checkpoints:
  CP-001:                   PENDING
  CP-002:                   PENDING
  CP-003:                   PENDING
```

### 10.2 Next Actions

1. Execute Phase 1: Launch EN-813, EN-814, EN-815 creator agents in parallel
2. Run critic cycle for each enabler (up to 4 iterations)
3. Git commit Phase 1 results
4. Create CP-001 checkpoint

---

*Document ID: PROJ-001-ORCH-PLAN-FEAT010*
*Workflow ID: feat010-remediation-20260215-001*
*Version: 2.0*
*Cross-Session Portable: All paths are repository-relative*
