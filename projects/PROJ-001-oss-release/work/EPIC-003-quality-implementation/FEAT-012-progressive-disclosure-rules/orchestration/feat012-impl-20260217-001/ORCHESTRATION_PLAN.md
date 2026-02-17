# ORCHESTRATION_PLAN.md

> **Document ID:** PROJ-001-ORCH-PLAN-FEAT012
> **Project:** PROJ-001-oss-release
> **Workflow ID:** `feat012-impl-20260217-001`
> **Status:** ACTIVE
> **Version:** 2.0
> **Created:** 2026-02-17
> **Last Updated:** 2026-02-17

---

## 1. Executive Summary

Orchestrate the progressive disclosure architecture for Jerry's rule framework. Restructure `.context/rules/` into a tiered hierarchy (HARD/MEDIUM/SOFT) with companion educational content, restore deleted guidance from git history, and implement path scoping for Python-specific rules. Five enablers (EN-902 through EN-906) address content restoration, pattern extraction, infrastructure implementation, and verification across 4 phases with C3-level adversarial quality enforcement.

**Current State:** Workflow not started. EN-901 (Rules Consolidation & Canonicalization) is already complete.

**Orchestration Pattern:** Sequential with Parallel Phases (single pipeline, phased enabler groups with internal parallelism)

### 1.1 Workflow Identification

| Field | Value | Source |
|-------|-------|--------|
| Workflow ID | `feat012-impl-20260217-001` | auto |
| ID Format | `{purpose}-{YYYYMMDD}-{NNN}` | semantic-date-seq |
| Base Path | `FEAT-012-progressive-disclosure-rules/orchestration/feat012-impl-20260217-001/` | Dynamic |

**Artifact Output Locations:**
- Pipeline: `orchestration/feat012-impl-20260217-001/impl/`
- Phase artifacts: `orchestration/feat012-impl-20260217-001/impl/phase-{N}/`
- Synthesis: `orchestration/feat012-impl-20260217-001/synthesis/`

### 1.2 Key Design Decisions

| Decision | Value | Rationale |
|----------|-------|-----------|
| Criticality Level | **C3 (Significant)** | Touches `.context/rules/` (AE-002), >10 files, >1 day to reverse |
| Quality Threshold | **>= 0.92** per enabler | H-13 (quality-enforcement SSOT) |
| Max Iterations | **3** per enabler | Standard C3 minimum |
| Strategy Set | **S-007, S-002, S-014, S-004, S-012, S-013** (required) + **S-001, S-003, S-010, S-011** (optional) | C3 adversarial quality protocol |
| Scoring | **S-014 LLM-as-Judge** | 6-dimension weighted rubric |
| Git Recovery Method | **Direct `git show` extraction** | EN-702 already indexed deleted content |

---

## 2. Workflow Architecture

### 2.1 Pipeline Diagram

```
FEAT-012 PROGRESSIVE DISCLOSURE RULES — SINGLE PIPELINE (C3)
============================================================

┌─────────────────────────────────────────────────────────────┐
│ PHASE 1: Content Restoration (EN-902, EN-903)              │
│ ────────────────────────────────────────────────────────── │
│ • EN-902: Companion Guide Files         [effort: 8]        │
│   - Restore deleted content from git history               │
│   - Create .context/guides/ directory structure            │
│   - Split educational vs. constitutional content           │
│ • EN-903: Code Pattern Extraction        [effort: 5]        │
│   - Extract port patterns to .context/patterns/            │
│   - Extract adapter patterns                                │
│   - Extract aggregate patterns                              │
│ Execution: PARALLEL (2 enablers, independent artifacts)     │
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
│ PHASE 2: Infrastructure (EN-904, EN-905)                    │
│ ────────────────────────────────────────────────────────── │
│ • EN-904: Path Scoping Implementation    [effort: 3]        │
│   - Add "scope: python" frontmatter to Python rules        │
│   - Update rule loading logic to respect scope             │
│ • EN-905: Bootstrap Exclusion & Validation [effort: 3]     │
│   - Exclude .context/guides/ from bootstrap token budget   │
│   - Add E2E tests for context bootstrap                    │
│ Execution: PARALLEL (2 enablers, independent components)    │
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
│ PHASE 3: Verification (EN-906)                              │
│ ────────────────────────────────────────────────────────── │
│ • EN-906: Fidelity Verification & Cross-Reference Testing  │
│   - E2E tests for cross-references                          │
│   - Fidelity verification (no dropped rules)                │
│   - Completeness verification (all deleted content found)   │
│ Execution: SEQUENTIAL (single enabler, validates all prior) │
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
│ PHASE 4: Integration & Synthesis                            │
│ ────────────────────────────────────────────────────────── │
│ • Run full E2E test suite                                   │
│ • Run ruff check + pytest                                   │
│ • Create FEAT-012 Final Synthesis                           │
│ • Verify all FEAT-012 acceptance criteria                   │
│ Execution: SEQUENTIAL                                       │
│ STATUS: PENDING (blocked by Phase 3)                        │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Orchestration Pattern Classification

| Pattern | Applied | Description |
|---------|---------|-------------|
| Sequential | Yes | Phases execute in order (content restoration before infrastructure) |
| Concurrent | Yes | Enablers within Phases 1 and 2 run in parallel |
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
   │       │    │  After 3 failed iterations:              │
   │       │    │  → HUMAN ESCALATION (AE-006)             │
   │       │    │                                          │
   │       │    ▼                                          │
   │       │  COMMIT                                       │
   │       │                                               │
   │       └───────────────────────────────────────────────┘

STRATEGIES APPLIED PER CYCLE (C3 LEVEL):

  Creator (ps-architect):
    • S-010 (Self-Refine): Self-review before submitting deliverable

  Critic (ps-critic):
    • S-014 (LLM-as-Judge): 6-dimension weighted rubric scoring (REQUIRED)
    • S-007 (Constitutional AI): Principle compliance check (REQUIRED)
    • S-003 (Steelman): Charitable reconstruction FIRST (H-16, OPTIONAL)
    • S-002 (Devil's Advocate): Strongest counterarguments (REQUIRED)
    • S-013 (Inversion): "How could this fail?" (REQUIRED)
    • S-004 (Pre-Mortem): "Imagine it failed — why?" (REQUIRED)
    • S-012 (FMEA): Systematic failure mode enumeration (REQUIRED)
    • S-011 (CoVe): Factual verification of claims (OPTIONAL)
    • S-001 (Red Team): Adversary simulation (OPTIONAL)

  Revision (ps-architect receives critic feedback):
    • S-003 (Steelman): Understand critic feedback charitably (OPTIONAL)
    • S-010 (Self-Refine): Self-review revised output (OPTIONAL)
```

---

## 3. Phase Definitions

### 3.1 Phase 1: Content Restoration

| Enabler | Title | Tasks | Effort | Dependencies |
|---------|-------|-------|--------|--------------|
| EN-902 | Companion Guide Files | 5 | 8 | None (uses git history from EN-702) |
| EN-903 | Code Pattern Extraction | 3 | 5 | None (independent of EN-902) |

**Execution Mode:** PARALLEL (2 enablers, independent output directories)

**Phase 1 Entry Criteria:**
- FEAT-012 worktracker entities exist on disk
- EN-702 index of deleted content available
- `.context/guides/` and `.context/patterns/` directories created

**Phase 1 Exit Criteria:**
- Both enablers pass >= 0.92 quality gate
- All 8 tasks marked DONE
- `.context/guides/` contains all restored educational content
- `.context/patterns/` contains port, adapter, aggregate pattern examples
- Git commit with clean working tree
- No broken cross-references (verified by grepping for now-missing anchors)

### 3.2 Phase 2: Infrastructure

| Enabler | Title | Tasks | Effort | Dependencies |
|---------|-------|-------|--------|--------------|
| EN-904 | Path Scoping Implementation | 3 | 3 | Needs EN-902 (guide files to reference) |
| EN-905 | Bootstrap Exclusion & Validation | 2 | 3 | Needs EN-902 (guide files to exclude) |

**Execution Mode:** PARALLEL (2 enablers, independent Python vs. markdown changes)

**Phase 2 Entry Criteria:**
- Phase 1 complete (CP-001 verified)
- `.context/guides/` directory exists and populated
- `.context/patterns/` directory exists and populated

**Phase 2 Exit Criteria:**
- Both enablers pass >= 0.92 quality gate
- All 5 tasks marked DONE
- Python-specific rules have `scope: python` frontmatter
- Bootstrap script excludes `.context/guides/`
- E2E tests for bootstrap context budget pass
- Git commit with clean working tree

### 3.3 Phase 3: Verification

| Enabler | Title | Tasks | Effort | Dependencies |
|---------|-------|-------|--------|--------------|
| EN-906 | Fidelity Verification & Cross-Reference Testing | 4 | 5 | Depends on EN-902, EN-903, EN-904, EN-905 (verifies all) |

**Execution Mode:** SEQUENTIAL (single enabler, validates all prior work)

**Phase 3 Entry Criteria:**
- Phase 2 complete (CP-002 verified)
- All infrastructure changes committed
- `.context/guides/` and `.context/patterns/` stable

**Phase 3 Exit Criteria:**
- EN-906 passes >= 0.92 quality gate
- All 4 tasks marked DONE
- E2E tests for cross-references pass
- Fidelity verification confirms no dropped rules
- Completeness verification confirms all deleted content restored
- `uv run pytest tests/e2e/` passes
- Git commit with clean working tree

### 3.4 Phase 4: Integration & Synthesis

| Step | Activity | Validation |
|------|----------|------------|
| 4.1 | Full E2E test suite | `uv run pytest tests/e2e/ -v` all pass |
| 4.2 | Ruff + type checks | `uv run ruff check src/` clean |
| 4.3 | Create Final Synthesis | Document FEAT-012 results, design decisions, cross-references to ADRs |
| 4.4 | Update FEAT-012 worktracker | Mark feature completed |
| 4.5 | Update EPIC-003 rollup | Increment completion percentage |

**Execution Mode:** SEQUENTIAL

**Phase 4 Entry Criteria:**
- Phases 1-3 complete (CP-003 verified)
- All 5 enablers at >= 0.92

**Phase 4 Exit Criteria:**
- All acceptance criteria from FEAT-012 verified:
  - `.context/rules/` organized by tier (HARD/MEDIUM/SOFT)
  - `.context/guides/` contains educational content
  - `.context/patterns/` contains code examples
  - Python-specific rules scoped
  - Bootstrap excludes `.context/guides/`
  - All cross-references valid
- Final Synthesis document created
- FEAT-012 marked completed
- EPIC-003 rollup updated

---

## 4. Adversarial Quality Protocol

### 4.1 C3 Strategy Deployment

This workflow uses **C3 (Significant) level** adversarial quality enforcement per the quality-enforcement SSOT.

**Required Strategies (6):**

| Strategy | ID | Role in Cycle | Applied By |
|----------|----|---------------|------------|
| LLM-as-Judge | S-014 | 6-dimension weighted rubric scoring | Critic (ps-critic) |
| Constitutional AI | S-007 | Principle-by-principle compliance | Critic |
| Devil's Advocate | S-002 | Strongest counterarguments | Critic |
| Pre-Mortem | S-004 | "Imagine it failed — why?" | Critic |
| FMEA | S-012 | Systematic failure mode enumeration | Critic |
| Inversion | S-013 | "How could this fail?" analysis | Critic |

**Optional Strategies (4):**

| Strategy | ID | Role in Cycle | Applied By |
|----------|----|---------------|------------|
| Red Team | S-001 | Adversary simulation | Critic |
| Steelman | S-003 | Charitable reconstruction FIRST (H-16) | Critic + Revision |
| Self-Refine | S-010 | Creator self-review before submission | Creator (ps-architect) |
| Chain-of-Verification | S-011 | Factual verification of claims | Critic |

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
| 1 | Initial deliverable (S-010 self-review) | Full C3 scoring (6 required + 4 optional strategies) | PASS or REVISE |
| 2 | Revise with critic feedback (S-003 + S-010) | Re-score with focus on prior gaps | PASS or REVISE |
| 3 | Final attempt with explicit gap closure | Final scoring | PASS or ESCALATE |
| 4+ | **HUMAN ESCALATION (AE-006)** | User reviews and directs | User decides |

### 4.4 Leniency Bias Countermeasures

Per S-014 implementation guidance, the critic must:
1. Score each dimension independently (no halo effect)
2. Resolve uncertain scores **downward**
3. Verify every Critical finding is reflected in dimensional scores
4. No dimension scored above 0.90 without exceptional evidence
5. Mathematically verify weighted composite calculation

---

## 5. Agent Registry

### 5.1 Phase 1 Agents

| Agent ID | Role | Model | Input | Output |
|----------|------|-------|-------|--------|
| en902-creator-iter1 | ps-architect | sonnet | EN-902 enabler + tasks + EN-702 index | `.context/guides/` files extracted from git history |
| en902-critic-iter1 | ps-critic | opus | Creator deliverables + all C3 strategies | Critic report with S-014 scores |
| en902-creator-iter2 | ps-architect | sonnet | Prior deliverable + critic feedback | Revised `.context/guides/` files |
| en902-critic-iter2 | ps-critic | opus | Revised deliverables | Iteration 2 scores |
| en903-creator-iter1 | ps-architect | sonnet | EN-903 enabler + tasks + existing src/ patterns | `.context/patterns/` files |
| en903-critic-iter1 | ps-critic | opus | Creator deliverables + all C3 strategies | Critic report with S-014 scores |

### 5.2 Phase 2 Agents

| Agent ID | Role | Model | Input | Output |
|----------|------|-------|-------|--------|
| en904-creator-iter1 | ps-architect | sonnet | EN-904 enabler + tasks + `.context/rules/` files | Modified rules with `scope: python` frontmatter |
| en904-critic-iter1 | ps-critic | opus | Creator deliverables | Critic report |
| en905-creator-iter1 | ps-architect | sonnet | EN-905 enabler + tasks + bootstrap script | Modified `src/bootstrap.py` + E2E tests |
| en905-critic-iter1 | ps-critic | opus | Creator deliverables | Critic report |

### 5.3 Phase 3 Agents

| Agent ID | Role | Model | Input | Output |
|----------|------|-------|-------|--------|
| en906-creator-iter1 | ps-architect | sonnet | EN-906 enabler + tasks + all Phase 1-2 artifacts | E2E tests + verification reports |
| en906-critic-iter1 | ps-critic | opus | Creator deliverables | Critic report |

### 5.4 Phase 4 Agents

| Agent ID | Role | Model | Input | Output |
|----------|------|-------|-------|--------|
| feat012-synthesizer | orch-synthesizer | sonnet | All phase results + quality scores | Final Synthesis |

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
FEAT-012-progressive-disclosure-rules/
└── orchestration/
    └── feat012-impl-20260217-001/
        ├── ORCHESTRATION_PLAN.md          (this file)
        ├── ORCHESTRATION_WORKTRACKER.md
        ├── ORCHESTRATION.yaml
        ├── impl/
        │   ├── phase-1-content-restoration/
        │   │   ├── en902-creator-iter1/   (guide files + extraction notes)
        │   │   ├── en902-critic-iter1/    (critic reports)
        │   │   ├── en902-creator-iter2/   (revised guide files)
        │   │   ├── en902-critic-iter2/
        │   │   ├── en903-creator-iter1/   (pattern files)
        │   │   └── en903-critic-iter1/
        │   ├── phase-2-infrastructure/
        │   │   ├── en904-creator-iter1/   (scoped rule files)
        │   │   ├── en904-critic-iter1/
        │   │   ├── en905-creator-iter1/   (bootstrap changes + tests)
        │   │   └── en905-critic-iter1/
        │   ├── phase-3-verification/
        │   │   ├── en906-creator-iter1/   (verification tests + reports)
        │   │   └── en906-critic-iter1/
        │   └── phase-4-integration/
        │       └── synthesis/
        └── checkpoints/
            ├── CP-001.yaml
            ├── CP-002.yaml
            └── CP-003.yaml
```

### 6.3 Checkpoint Strategy

| Trigger | When | Purpose |
|---------|------|---------|
| CP-001 | Phase 1 complete | Content restoration verified, rollback point before infrastructure changes |
| CP-002 | Phase 2 complete | Infrastructure changes verified, rollback point before verification |
| CP-003 | Phase 3 complete | All verification passed, pre-integration |
| MANUAL | User-triggered | Debug and inspection |

---

## 7. Execution Constraints

### 7.1 Hard Constraints (Jerry Constitution)

| Constraint | ID | Enforcement |
|------------|----|----|
| Single agent nesting | P-003 | Orchestrator -> Worker only. No agent-to-agent calls. |
| File persistence | P-002 | All state to filesystem. No transient planning. |
| No deception | P-022 | Transparent reasoning. Honest scoring. |
| User authority | P-020 | User approves at iteration 3 escalation. |
| Quality threshold | H-13 | >= 0.92 weighted composite per enabler |
| Steelman before critique | H-16 | S-003 MUST execute before S-002 (if S-003 applied) |
| Self-review required | H-15 | S-010 applied before every submission (if applied) |
| Governance escalation | H-19 | AE-002: `.context/rules/` changes auto-escalate to C3 |
| Tier vocabulary | quality-enforcement.md | HARD rules cannot be overridden |
| UV only | H-05, H-06 | Use `uv run` for all Python execution |

### 7.1.1 Worktracker Entity Templates

> **WTI-007:** Entity files created during orchestration MUST use canonical templates from `.context/templates/worktracker/`.

### 7.2 Soft Constraints

| Constraint | Value | Rationale |
|------------|-------|-----------|
| Max concurrent agents | 2 | Parallel enablers within Phases 1 and 2 |
| Max iterations per enabler | 3 | Standard C3 minimum before escalation |
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
| `.context/guides/` populated | Directory exists with >0 files |
| `.context/patterns/` populated | Directory exists with >0 files |
| Python rules scoped | Frontmatter `scope: python` present |
| Bootstrap excludes guides | `.context/guides/` not in token budget |
| Cross-references valid | E2E tests pass |
| `uv run pytest tests/e2e/` passes | Full E2E suite green |
| `uv run ruff check src/` clean | Linting passes |
| Final Synthesis created | synthesis/ directory |
| FEAT-012 marked completed | Worktracker status update |

---

## 9. Risk Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| EN-902 git recovery fails (missing commits) | Low | High | EN-702 already indexed deleted content. Fallback: manual reconstruction from remaining fragments. |
| EN-906 reveals broken cross-references | Medium | Medium | Creator runs grep for broken anchors before submission. Critic verifies all references resolve. |
| Bootstrap exclusion breaks existing tests | Medium | Medium | EN-905 includes E2E tests for bootstrap context budget. Run full test suite after changes. |
| Context rot during long phases | Medium | Medium | Each enabler is a fresh agent invocation. Re-read rules at phase boundaries. |
| Leniency bias in self-scoring | High | High | Critic uses strict rubric. Uncertain scores resolved downward. No dimension above 0.90 without evidence. |
| EN-904 path scoping logic errors | Low | Low | Path scoping is frontmatter-based (no code changes). Simple grep verification. |

---

## 10. Resumption Context

### 10.1 Current Execution State

```
WORKFLOW STATUS AS OF 2026-02-17
================================

Phase 1 (Content Restoration):  PENDING
  EN-902:                        PENDING
  EN-903:                        PENDING

Phase 2 (Infrastructure):       PENDING (blocked by Phase 1)
  EN-904:                        PENDING
  EN-905:                        PENDING

Phase 3 (Verification):         PENDING (blocked by Phase 2)
  EN-906:                        PENDING

Phase 4 (Integration):          PENDING (blocked by Phase 3)
  Final Synthesis:               PENDING

Checkpoints:
  CP-001:                        PENDING
  CP-002:                        PENDING
  CP-003:                        PENDING
```

### 10.2 Next Actions

1. Execute Phase 1: Launch EN-902 and EN-903 creator agents in parallel
2. Run critic cycle for each enabler (up to 3 iterations)
3. Git commit Phase 1 results
4. Create CP-001 checkpoint

---

**DISCLAIMER:** This orchestration plan is generated by an AI agent (orch-planner v2.2.0) and represents a proposed execution strategy. All design decisions, quality thresholds, and risk assessments should be reviewed and approved by human stakeholders before execution. The plan follows Jerry Constitution P-020 (User Authority) — users retain final decision-making authority.

---

*Document ID: PROJ-001-ORCH-PLAN-FEAT012*
*Workflow ID: feat012-impl-20260217-001*
*Version: 2.0*
*Cross-Session Portable: All paths are repository-relative*
