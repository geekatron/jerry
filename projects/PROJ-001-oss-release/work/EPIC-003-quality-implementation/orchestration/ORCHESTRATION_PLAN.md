# ORCHESTRATION_PLAN.md

> **Document ID:** PROJ-001-ORCH-PLAN-EPIC003
> **Project:** PROJ-001-oss-release
> **Workflow ID:** epic003-impl-20260214-001
> **Status:** ACTIVE
> **Version:** 1.0
> **Created:** 2026-02-14
> **Updated:** 2026-02-14

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | High-level overview and objectives |
| [Workflow Architecture](#workflow-architecture) | Pipeline structure and phase diagram |
| [Phase Definitions](#phase-definitions) | Detailed phase breakdown with enablers |
| [Adversarial Review Protocol](#adversarial-review-protocol) | Creator-critic-revision cycle specification |
| [Phase Gate Protocol](#phase-gate-protocol) | Gate criteria and transition rules |
| [Agent Registry](#agent-registry) | Agent assignments by phase |
| [State Management](#state-management) | Paths, checkpoints, artifact structure |
| [Execution Constraints](#execution-constraints) | Constitutional and resource limits |
| [Success Criteria](#success-criteria) | Definition of done for EPIC-003 |
| [Risk Mitigations](#risk-mitigations) | Identified risks and countermeasures |
| [Resumption Context](#resumption-context) | Recovery and session continuity |

---

## Executive Summary

**EPIC-003 implements the designs produced by EPIC-002 into working code.**

EPIC-002 completed the DESIGN phase: 82 artifacts, 13 enablers, 2 ADRs (ADR-EPIC002-001 for adversarial strategy selection, ADR-EPIC002-002 for 5-layer hybrid enforcement architecture), 329+ test specifications. Zero code was written.

EPIC-003 transforms those designs into:
- Python enforcement engines (AST-based, hook-based)
- Optimized rule files (30K → 12.5K tokens)
- Quality SSOT constants file
- Enhanced skills with adversarial modes
- CI pipeline integration
- E2E integration tests

**Pattern:** Sequential 5-Phase Pipeline with Parallel Fan-Out within phases and Adversarial Review per enabler.

**Scale:** 1 pipeline, 5 phases, 11 enablers, 26 execution groups, ~81 effort points.

---

## Workflow Architecture

### Pipeline Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│              EPIC-003: Quality Framework Implementation              │
│              Pattern: Sequential + Fan-Out + Adversarial             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  PHASE 1: FOUNDATION (Sequential)                                    │
│  ┌──────────┐    ┌──────────┐                                       │
│  │  EN-701  │───►│  EN-702  │  EN-702 depends on EN-701 SSOT       │
│  │  SSOT    │    │  Rules   │                                       │
│  │  (5 pts) │    │  (8 pts) │                                       │
│  └──────────┘    └──────────┘                                       │
│         │                │                                           │
│         ▼                ▼                                           │
│  ═══════════════════════════════════════  GATE 1  ═══════════════    │
│                                                                      │
│  PHASE 2: DETERMINISTIC ENFORCEMENT (Parallel)                      │
│  ┌──────────┐    ┌──────────┐                                       │
│  │  EN-703  │    │  EN-704  │  Fan-out: parallel execution          │
│  │  PreTool │    │ PreCommit│                                       │
│  │ (13 pts) │    │  (5 pts) │                                       │
│  └──────────┘    └──────────┘                                       │
│         │                │                                           │
│         ▼                ▼                                           │
│  ═══════════════════════════════════════  GATE 2  ═══════════════    │
│                                                                      │
│  PHASE 3: PROBABILISTIC ENFORCEMENT (Parallel)                      │
│  ┌──────────┐    ┌──────────┐                                       │
│  │  EN-705  │    │  EN-706  │  Fan-out: parallel execution          │
│  │  Prompt  │    │ Session  │                                       │
│  │  (8 pts) │    │  (5 pts) │                                       │
│  └──────────┘    └──────────┘                                       │
│         │                │                                           │
│         ▼                ▼                                           │
│  ═══════════════════════════════════════  GATE 3  ═══════════════    │
│                                                                      │
│  PHASE 4: SKILL ENHANCEMENT (Parallel)                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                          │
│  │  EN-707  │  │  EN-708  │  │  EN-709  │  Fan-out: 3 parallel     │
│  │    PS    │  │   NSE    │  │   ORCH   │                           │
│  │  (8 pts) │  │  (8 pts) │  │  (8 pts) │                          │
│  └──────────┘  └──────────┘  └──────────┘                          │
│         │            │             │                                 │
│         ▼            ▼             ▼                                 │
│  ═══════════════════════════════════════  GATE 4  ═══════════════    │
│                                                                      │
│  PHASE 5: INTEGRATION & VALIDATION (Parallel)                       │
│  ┌──────────┐    ┌──────────┐                                       │
│  │  EN-710  │    │  EN-711  │  Fan-out: parallel execution          │
│  │    CI    │    │   E2E    │                                       │
│  │  (5 pts) │    │  (8 pts) │                                       │
│  └──────────┘    └──────────┘                                       │
│         │                │                                           │
│         ▼                ▼                                           │
│  ═══════════════════════════════════════  GATE 5  ═══════════════    │
│                                                                      │
│  ┌──────────────────────────────────┐                               │
│  │        FINAL SYNTHESIS           │                               │
│  │  Integration Report + Lessons    │                               │
│  └──────────────────────────────────┘                               │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Adversarial Cycle Per Enabler

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ CREATOR  │───►│ CRITIC   │───►│ REVISION │───►│ CRITIC   │
│ (build)  │    │ (iter 1) │    │ (fix)    │    │ (iter 2) │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
                                                      │
                                                >=0.92? ──► PASS
                                                <0.92?  ──► iter 3 or ESCALATE
```

---

## Phase Definitions

### Phase 1: Foundation

| Property | Value |
|----------|-------|
| **Enablers** | EN-701 (SSOT), EN-702 (Rule Optimization) |
| **Execution** | Sequential (EN-702 depends on EN-701) |
| **Total Effort** | 13 points |
| **Groups** | G1–G4 (EN-701), G5–G8 (EN-702) |

**EN-701: Quality Enforcement SSOT**
- Create `.context/rules/quality-enforcement.md`
- Consolidate: C1-C4 criticality, 0.92 threshold, S-001–S-014 strategies, AE-001–AE-006 escalation, HARD/MEDIUM/SOFT tiers
- Budget: under 2000 tokens
- Design source: ADR-EPIC002-002, EN-301 strategy catalog

**EN-702: Rule File Token Optimization**
- Optimize 10 `.context/rules/*.md` files: ~30K → ~12.5K tokens
- Apply tier vocabulary, add rule IDs (H-01 through H-24)
- Replace inline constants with EN-701 SSOT references
- Design source: EN-404 token budget analysis

### Phase 2: Deterministic Enforcement

| Property | Value |
|----------|-------|
| **Enablers** | EN-703 (PreToolUse), EN-704 (Pre-commit) |
| **Execution** | Parallel |
| **Total Effort** | 18 points |
| **Groups** | G6–G9 |
| **Gate** | Gate 2 |

**EN-703: PreToolUse Enforcement Engine**
- Create `src/infrastructure/internal/enforcement/pre_tool_enforcement_engine.py`
- Enhance `scripts/pre_tool_use.py` with engine integration
- Implement V-038 (import boundaries), V-039 (type hints), V-040 (docstrings), V-041 (one-class-per-file)
- AST-based, zero token cost, context-rot-immune
- Design source: EN-403 enforcement design

**EN-704: Pre-commit Quality Gates**
- Configure pre-commit with ruff, architecture boundary, type hint checks
- V-044 (scored 4.80 WCS)
- Last line of defense before version control
- Design source: EN-405

### Phase 3: Probabilistic Enforcement

| Property | Value |
|----------|-------|
| **Enablers** | EN-705 (UserPromptSubmit), EN-706 (SessionStart) |
| **Execution** | Parallel |
| **Total Effort** | 13 points |
| **Groups** | G11–G14 |
| **Gate** | Gate 3 |

**EN-705: UserPromptSubmit Quality Hook**
- Create `hooks/user-prompt-submit.py` (hook adapter)
- Create `src/infrastructure/internal/enforcement/prompt_reinforcement_engine.py`
- L2 Per-Prompt Reinforcement: re-inject critical rules every prompt
- 600-token budget, fail-open error handling
- Design source: EN-403, V-024

**EN-706: SessionStart Quality Context Enhancement**
- Create `src/infrastructure/internal/enforcement/session_quality_context_generator.py`
- XML preamble: quality gate, constitutional principles, strategies, criticality
- 700-token budget
- Design source: EN-406

### Phase 4: Skill Enhancement

| Property | Value |
|----------|-------|
| **Enablers** | EN-707 (PS), EN-708 (NSE), EN-709 (ORCH) |
| **Execution** | Parallel (3-way fan-out) |
| **Total Effort** | 24 points |
| **Groups** | G16–G19 |
| **Gate** | Gate 4 |

**EN-707: Problem-Solving Adversarial Mode**
- Update `skills/problem-solving/SKILL.md`, `PLAYBOOK.md`, agent files
- Integrate 10 adversarial strategies, quality scoring (S-014 LLM-as-Judge)
- Design source: EN-305

**EN-708: NASA-SE Adversarial Mode**
- Update `skills/nasa-se/SKILL.md`, `PLAYBOOK.md`, agent files
- V&V integration, risk-based quality gates (C1-C4)
- Design source: EN-305

**EN-709: Orchestration Adversarial Mode**
- Update `skills/orchestration/SKILL.md`, `PLAYBOOK.md`, agent files
- Adversarial cycles at sync barriers, phase gates >= 0.92
- Design source: EN-307

### Phase 5: Integration & Validation

| Property | Value |
|----------|-------|
| **Enablers** | EN-710 (CI), EN-711 (E2E) |
| **Execution** | Parallel |
| **Total Effort** | 13 points |
| **Groups** | G21–G24 |
| **Gate** | Gate 5 |

**EN-710: CI Pipeline Quality Integration**
- GitHub Actions workflow with architecture tests, mypy, ruff
- V-045 (scored 4.86 WCS)
- Design source: EN-405

**EN-711: E2E Integration Testing**
- Cross-layer interaction tests (L1-L5)
- Hook, rule, session, skill, performance tests
- Based on 204 test specifications from EN-404
- Design source: EN-404

---

## Adversarial Review Protocol

### Cycle Structure

Each enabler undergoes a minimum of 2 adversarial iterations:

| Step | Agent | Action | Output |
|------|-------|--------|--------|
| 1 | Creator | Build initial artifact | Code/content |
| 2 | Critic (iter 1) | Apply adversarial strategy | Critique with score |
| 3 | Creator | Revise based on critique | Revised artifact |
| 4 | Critic (iter 2) | Re-evaluate revised artifact | Final score |

### Quality Scoring Rubric (S-014 LLM-as-Judge)

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Correctness | 0.25 | Functional accuracy, no bugs |
| Completeness | 0.20 | All ACs met, no gaps |
| Architecture | 0.20 | Hexagonal compliance, layer boundaries |
| Robustness | 0.15 | Error handling, edge cases |
| Maintainability | 0.10 | Code clarity, documentation |
| Performance | 0.10 | Token budget, latency |

**Passing threshold:** Weighted score >= 0.92

### Strategy Assignments

| Enabler | Primary Strategy | Secondary Strategy |
|---------|-----------------|-------------------|
| EN-701 | S-014 LLM-as-Judge | S-003 Steelman |
| EN-702 | S-003 Steelman | S-013 Inversion |
| EN-703 | S-012 FMEA | S-001 Red Team |
| EN-704 | S-002 Devil's Advocate | S-011 Chain-of-Verification |
| EN-705 | S-004 Pre-Mortem | S-010 Self-Refine |
| EN-706 | S-007 Constitutional AI | S-014 LLM-as-Judge |
| EN-707 | S-003 Steelman | S-007 Constitutional AI |
| EN-708 | S-012 FMEA | S-001 Red Team |
| EN-709 | S-004 Pre-Mortem | S-013 Inversion |
| EN-710 | S-011 Chain-of-Verification | S-001 Red Team |
| EN-711 | S-012 FMEA | S-010 Self-Refine |

### Escalation Rules

| Condition | Action |
|-----------|--------|
| Score >= 0.92 after iter 2 | PASS — proceed to next group |
| Score 0.85–0.91 after iter 2 | Iter 3 with different strategy |
| Score < 0.85 after iter 2 | ESCALATE to user (P-020) |
| Score < 0.85 after iter 3 | BLOCK — user decision required |

---

## Phase Gate Protocol

### Gate Criteria (All Gates)

| Check | Description |
|-------|-------------|
| Quality Score | All enablers in phase >= 0.92 |
| Tests | `uv run pytest tests/` passes |
| Lint | `uv run ruff check src/` clean |
| Git | Clean working tree, committed |

### Gate-Specific Criteria

| Gate | Additional Criteria |
|------|-------------------|
| Gate 1 | `quality-enforcement.md` exists, under 2000 tokens; total rule tokens <= 12.5K |
| Gate 2 | PreToolEnforcementEngine unit tests pass; pre-commit hooks configured |
| Gate 3 | UserPromptSubmit hook functional; SessionStart preamble injecting |
| Gate 4 | All 3 skills have adversarial mode sections |
| Gate 5 | CI pipeline green; E2E tests passing; all 11 enablers >= 0.92 |

### Gate Transition Rules

```
IF all_enablers_in_phase.quality_score >= 0.92
   AND pytest_passes
   AND ruff_clean
   AND git_committed
THEN
   gate.status = PASSED
   next_phase.status = READY
   checkpoint.create()
ELSE
   gate.status = BLOCKED
   identify_failing_enablers()
   trigger_remediation_or_escalation()
```

---

## Agent Registry

### Phase 1 Agents

| Agent ID | Role | Enabler | Skill |
|----------|------|---------|-------|
| en701-creator | Creator | EN-701 | problem-solving |
| en701-critic | Critic | EN-701 | problem-solving |
| en702-creator | Creator | EN-702 | problem-solving |
| en702-critic | Critic | EN-702 | problem-solving |

### Phase 2 Agents

| Agent ID | Role | Enabler | Skill |
|----------|------|---------|-------|
| en703-creator | Creator | EN-703 | problem-solving |
| en703-critic | Critic | EN-703 | problem-solving |
| en704-creator | Creator | EN-704 | problem-solving |
| en704-critic | Critic | EN-704 | problem-solving |

### Phase 3 Agents

| Agent ID | Role | Enabler | Skill |
|----------|------|---------|-------|
| en705-creator | Creator | EN-705 | problem-solving |
| en705-critic | Critic | EN-705 | problem-solving |
| en706-creator | Creator | EN-706 | problem-solving |
| en706-critic | Critic | EN-706 | problem-solving |

### Phase 4 Agents

| Agent ID | Role | Enabler | Skill |
|----------|------|---------|-------|
| en707-creator | Creator | EN-707 | problem-solving |
| en707-critic | Critic | EN-707 | problem-solving |
| en708-creator | Creator | EN-708 | problem-solving |
| en708-critic | Critic | EN-708 | problem-solving |
| en709-creator | Creator | EN-709 | problem-solving |
| en709-critic | Critic | EN-709 | problem-solving |

### Phase 5 Agents

| Agent ID | Role | Enabler | Skill |
|----------|------|---------|-------|
| en710-creator | Creator | EN-710 | problem-solving |
| en710-critic | Critic | EN-710 | problem-solving |
| en711-creator | Creator | EN-711 | problem-solving |
| en711-critic | Critic | EN-711 | problem-solving |

### Synthesis Agents

| Agent ID | Role | Phase | Skill |
|----------|------|-------|-------|
| orch-synthesizer | Synthesizer | Final | orchestration |

---

## State Management

### Path Configuration

```
projects/PROJ-001-oss-release/work/EPIC-003-quality-implementation/
├── orchestration/
│   ├── ORCHESTRATION.yaml          # SSOT for workflow state
│   ├── ORCHESTRATION_PLAN.md       # This document
│   └── epic003-impl-20260214-001/  # Workflow artifacts
│       ├── impl/                   # Pipeline artifacts
│       │   ├── phase-1-foundation/
│       │   │   ├── en701-creator/
│       │   │   ├── en701-critic/
│       │   │   ├── en702-creator/
│       │   │   └── en702-critic/
│       │   ├── phase-2-deterministic/
│       │   ├── phase-3-probabilistic/
│       │   ├── phase-4-skills/
│       │   └── phase-5-integration/
│       ├── barriers/
│       │   ├── gate-1/
│       │   ├── gate-2/
│       │   ├── gate-3/
│       │   ├── gate-4/
│       │   └── gate-5/
│       └── synthesis/
└── FEAT-008-quality-framework-implementation/
    ├── EN-701-quality-enforcement-ssot/
    │   ├── EN-701-quality-enforcement-ssot.md
    │   └── TASK-*.md
    ├── EN-702-rule-optimization/
    │   ├── EN-702-rule-optimization.md
    │   └── TASK-*.md
    ... (EN-703 through EN-711)
```

### Checkpoint Strategy

Checkpoints are created at each phase gate:

| Checkpoint | Trigger | Contents |
|------------|---------|----------|
| CP-001 | Gate 1 passed | EN-701 + EN-702 artifacts, quality scores |
| CP-002 | Gate 2 passed | EN-703 + EN-704 artifacts, test results |
| CP-003 | Gate 3 passed | EN-705 + EN-706 artifacts, hook configs |
| CP-004 | Gate 4 passed | EN-707 + EN-708 + EN-709 skill updates |
| CP-005 | Gate 5 passed | EN-710 + EN-711 CI/test artifacts |

---

## Execution Constraints

### Constitutional Constraints (HARD)

| Constraint | Source | Enforcement |
|------------|--------|-------------|
| Max 1 level agent nesting | P-003 | Orchestrator → worker only |
| All state to filesystem | P-002 | ORCHESTRATION.yaml is SSOT |
| User authority on gates | P-020 | Escalation on gate failures |
| No deception | P-022 | Transparent quality scores |

### Resource Constraints (SOFT)

| Constraint | Value | Rationale |
|------------|-------|-----------|
| Max concurrent agents | 3 | Phase 4 has 3-way fan-out |
| Max barrier retries | 2 | Circuit breaker for stuck gates |
| Checkpoint frequency | Per phase | Balance recovery vs. overhead |

### Python Environment (HARD)

| Rule | Command |
|------|---------|
| Run tests | `uv run pytest tests/` |
| Run linting | `uv run ruff check src/` |
| Run CLI | `uv run jerry <command>` |
| NEVER use | `python`, `pip`, `pip3` directly |

---

## Success Criteria

### EPIC-003 Definition of Done

- [ ] All 11 enablers pass adversarial review (>= 0.92)
- [ ] All 5 phase gates passed
- [ ] `uv run pytest tests/` passes (all tests green)
- [ ] `uv run ruff check src/` clean (no violations)
- [ ] `quality-enforcement.md` SSOT created (< 2000 tokens)
- [ ] Rule files optimized (total <= 12.5K tokens)
- [ ] PreToolUse enforcement engine operational
- [ ] Pre-commit quality gates configured
- [ ] UserPromptSubmit hook functional
- [ ] SessionStart quality preamble injecting
- [ ] All 3 skills updated with adversarial modes
- [ ] CI pipeline includes quality enforcement
- [ ] E2E integration tests passing
- [ ] Final synthesis document produced

### Quality Metrics Target

| Metric | Target |
|--------|--------|
| Average enabler quality score | >= 0.92 |
| Minimum enabler quality score | >= 0.88 |
| Test pass rate | 100% |
| Lint violations | 0 |

---

## Risk Mitigations

| # | Risk | Likelihood | Impact | Mitigation |
|---|------|-----------|--------|------------|
| R1 | Token optimization loses semantic meaning | Medium | High | Adversarial review with S-013 Inversion; validate rules still enforceable |
| R2 | AST enforcement engine false positives | Medium | Medium | Extensive test coverage; fail-open error handling |
| R3 | Hook latency degrades developer experience | Low | Medium | 600/700 token budgets; performance benchmarks in EN-711 |
| R4 | Skill updates break existing functionality | Medium | High | Run full test suite at each gate; regression tests |
| R5 | Context rot degrades quality during long sessions | High | Medium | L2 re-injection (EN-705) compensates; session checkpoints |
| R6 | Phase dependencies create bottleneck | Low | Medium | Phase 1 is only sequential phase; all others fan-out |
| R7 | Pre-commit hooks slow developer workflow | Low | Low | Targeted file-type triggers; skip option for emergencies |
| R8 | E2E tests fragile due to hook dependencies | Medium | Medium | Mock hooks in unit tests; real hooks only in E2E |

---

## Resumption Context

### For Session Recovery

If resuming this workflow in a new session:

1. **Read ORCHESTRATION.yaml** — check `resumption.current_state` and `next_actions`
2. **Check git status** — verify working tree state
3. **Read latest checkpoint** — restore from last phase gate
4. **Identify current group** — find first non-COMPLETE group in execution_queue
5. **Continue execution** — pick up from identified group

### Files to Read on Resume

```
projects/PROJ-001-oss-release/work/EPIC-003-quality-implementation/orchestration/ORCHESTRATION.yaml
projects/PROJ-001-oss-release/work/EPIC-003-quality-implementation/FEAT-008-quality-framework-implementation/EN-{current}-*.md
```

---

*Generated by orch-planner agent v2.1.0*
*Last Updated: 2026-02-14*
