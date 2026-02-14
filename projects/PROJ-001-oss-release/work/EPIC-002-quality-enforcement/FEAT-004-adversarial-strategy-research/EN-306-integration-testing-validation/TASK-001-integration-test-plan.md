# TASK-001: Integration Test Plan -- Adversarial Strategy Cross-Skill Validation

<!--
DOCUMENT-ID: FEAT-004:EN-306:TASK-001
VERSION: 1.0.0
AGENT: ps-validator-306
DATE: 2026-02-13
STATUS: Complete
PARENT: EN-306 (Integration Testing & Validation)
FEATURE: FEAT-004 (Adversarial Strategy Research & Skill Enhancement)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
ACTIVITY: TESTING
-->

> **Version:** 1.0.0
> **Agent:** ps-validator-306
> **Quality Target:** >= 0.92
> **Purpose:** Comprehensive integration test plan covering all 10 adversarial strategies across all 3 enhanced skills (/problem-solving, /nasa-se, /orchestration)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this test plan covers |
| [Test Scope](#test-scope) | Boundaries of integration testing |
| [Test Strategy](#test-strategy) | Overall testing approach |
| [Coverage Matrix](#coverage-matrix) | 10 strategies x 3 skills = 30 combinations |
| [Inter-Skill Coordination Tests](#inter-skill-coordination-tests) | Cross-skill interaction test cases |
| [Test Data and Prerequisites](#test-data-and-prerequisites) | Required inputs and setup |
| [Test Execution Approach](#test-execution-approach) | How tests are structured and executed |
| [Pass/Fail Criteria](#passfail-criteria) | Definition of done for testing |
| [Risk Assessment](#risk-assessment) | Testing risks and mitigations |
| [Traceability](#traceability) | Mapping to EN-306 acceptance criteria |
| [References](#references) | Source citations |

---

## Summary

This integration test plan defines the comprehensive testing approach for verifying that all 10 adversarial strategies from ADR-EPIC002-001 function correctly across the 3 enhanced skills: /problem-solving (EN-304), /nasa-se (EN-305), and /orchestration (EN-307). The plan covers:

1. **Strategy-Skill Coverage Matrix:** 30 test combinations (10 strategies x 3 skills) verifying that each strategy's mode/integration is correctly specified in each skill.
2. **Intra-Skill Tests:** Per-skill verification that all strategy modes produce expected outputs per their specifications.
3. **Inter-Skill Coordination Tests:** Cross-skill tests verifying that orchestration loops correctly coordinate creator-critic cycles between /problem-solving and /nasa-se agents.
4. **Quality Gate Tests:** Verification that the 0.92 threshold, anti-leniency calibration, and circuit breaker logic work consistently across skills.
5. **Backward Compatibility Tests:** Verification that existing workflows function identically without adversarial context.

**Test context:** These are design-phase test specifications. They define WHAT to test and HOW to verify, based on the design artifacts from EN-304, EN-305, and EN-307. Actual runtime test execution will occur during implementation.

---

## Test Scope

### In Scope

| Category | Coverage |
|----------|----------|
| Strategy mode definitions | All 10 modes in ps-critic (EN-304 TASK-002) |
| Strategy mode definitions | All adversarial modes in nse-verification and nse-reviewer (EN-305 TASK-002/003) |
| Strategy-gate mapping | 10x5 strategy-to-gate matrix (EN-305 TASK-004) |
| Orchestration cycle generation | Creator-critic-revision pattern injection (EN-307 TASK-002) |
| Quality gate tracking | Score recording, aggregation, pass/fail (EN-307 TASK-003) |
| Invocation protocol | Explicit, automatic, and multi-mode selection (EN-304 TASK-003) |
| Backward compatibility | BC-304-001 through BC-304-003, BC-305-001 through BC-305-005 |
| Cross-enabler SSOT | FMEA scale, token budgets, strategy IDs, quality dimensions, threshold |

### Out of Scope

| Category | Reason |
|----------|--------|
| nse-qa adversarial modes | Formally descoped per EN-305-F002 |
| Automated test execution scripts | Implementation phase deliverable |
| Performance benchmarking | Future optimization concern |
| A/B testing of strategy combinations | Out of FEAT-004 MVP scope |

---

## Test Strategy

### Testing Levels

| Level | Description | Coverage |
|-------|-------------|----------|
| **Unit** | Individual strategy mode produces correct output structure | 30 test cases (10 strategies x 3 skill contexts) |
| **Integration** | Multi-mode pipeline executes with correct sequencing | 4 pipeline test cases (C1, C2, C3, C4) |
| **Cross-Skill** | Orchestration coordinates PS/NSE agents in adversarial cycles | 6 cross-skill test scenarios |
| **Regression** | Backward compatibility with pre-adversarial workflows | 7 BC test cases (EN-304) + 5 BC test cases (EN-305) |

### Verification Approach

Since this is a design-phase validation (markdown specifications, not executable code), verification uses:

1. **Specification Inspection:** Verify that each mode definition contains all required components per FR-304-002.
2. **Schema Validation:** Verify that invocation context schemas are consistent across skills.
3. **Traceability Analysis:** Verify that each strategy's implementation traces to its source requirements.
4. **Consistency Checking:** Verify cross-enabler SSOT alignment (token costs, FMEA scale, quality dimensions).
5. **Scenario Walkthrough:** Trace each test scenario through the specifications to confirm expected outcomes.

---

## Coverage Matrix

### Strategy x Skill Coverage

| # | Strategy | ps-critic (EN-304) | nse-verification (EN-305) | nse-reviewer (EN-305) | orch-planner (EN-307) | orch-tracker (EN-307) | orch-synthesizer (EN-307) |
|---|----------|-------------------|--------------------------|----------------------|----------------------|----------------------|--------------------------|
| 1 | S-001 Red Team | `red-team` mode | -- | `adversarial-redteam` mode | Strategy assignment at C3+ | Score tracking | Finding synthesis |
| 2 | S-002 Devil's Advocate | `devils-advocate` mode | -- | `adversarial-critique` mode | Strategy assignment at C2+ | Score tracking | Finding synthesis |
| 3 | S-003 Steelman | `steelman` mode | -- | `steelman-critique` mode | Strategy assignment at C2+ | Score tracking | Finding synthesis |
| 4 | S-004 Pre-Mortem | `pre-mortem` mode | -- | `adversarial-premortem` mode | Strategy assignment at C3+ | Score tracking | Finding synthesis |
| 5 | S-007 Constitutional AI | `constitutional` mode | `adversarial-compliance` mode | -- | Strategy assignment at C2+ | Score tracking | Finding synthesis |
| 6 | S-010 Self-Refine | `self-refine` mode | Pre-step (always) | -- | Strategy assignment at C1+ | Score tracking | Finding synthesis |
| 7 | S-011 CoVe | `chain-of-verification` mode | `adversarial-verification` mode | -- | Strategy assignment at C4 | Score tracking | Finding synthesis |
| 8 | S-012 FMEA | `fmea` mode | -- | `adversarial-fmea` mode | Strategy assignment at C3+ | Score tracking | Finding synthesis |
| 9 | S-013 Inversion | `inversion` mode | `adversarial-challenge` mode | -- | Strategy assignment at C3+ | Score tracking | Finding synthesis |
| 10 | S-014 LLM-as-Judge | `llm-as-judge` mode | `adversarial-scoring` mode | `adversarial-scoring` mode | Score threshold config | Score recording + gate | Trend analysis |

### Coverage Summary

- **Total strategy-skill combinations:** 30 (as shown in matrix above, counting only primary mode definitions)
- **Strategy definitions verified:** 10 in ps-critic + 4 in nse-verification + 6 in nse-reviewer = 20 mode definitions
- **Orchestration integrations:** 10 strategies x 3 agents (planner, tracker, synthesizer) = 30 integration points
- **Review gate mappings:** 10 strategies x 5 gates (SRR, PDR, CDR, TRR, FRR) = 50 combinations

---

## Inter-Skill Coordination Tests

### ITC-001: Creator (PS) to Critic (PS) Cycle via Orchestration

**Scenario:** orch-planner generates a workflow where ps-architect creates an artifact and ps-critic reviews it using adversarial modes.

| Step | Actor | Action | Expected Outcome |
|------|-------|--------|-----------------|
| 1 | orch-planner | Detect C2 criticality for TGT-ARCH artifact | Adversarial cycle injected into execution queue |
| 2 | orch-planner | Assign strategies to ps-critic | `adversarial_strategies: [S-003, S-007, S-002, S-014]` |
| 3 | ps-architect | Create initial artifact (Group N) | Artifact persisted; S-010 self-refine applied during creation |
| 4 | ps-critic | Execute C2 pipeline (Group N+1) | steelman -> constitutional -> devils-advocate -> llm-as-judge |
| 5 | orch-tracker | Record iteration 1 scores | `scores: { artifact: 0.78 }` in iteration tracking |
| 6 | ps-architect | Revise artifact (Group N+2) | Revision addresses ps-critic findings |
| 7 | ps-critic | Score revised artifact (Group N+3) | llm-as-judge + chain-of-verification |
| 8 | orch-tracker | Record iteration 2 scores | `scores: { artifact: 0.93 }`, `delta: +0.15`, `threshold_met: true` |
| 9 | orch-tracker | Quality gate determination | PASS (0.93 >= 0.92) |

**Pass Criteria:** All 9 steps trace correctly through EN-304 TASK-003 (invocation protocol), EN-307 TASK-002 (cycle generation), EN-307 TASK-003 (quality gate tracking).

### ITC-002: Creator (PS) to Critic (NSE) Cycle via Orchestration

**Scenario:** orch-planner generates a workflow where ps-researcher creates requirements and nse-verification reviews them at SRR gate.

| Step | Actor | Action | Expected Outcome |
|------|-------|--------|-----------------|
| 1 | orch-planner | Detect C2 criticality for TGT-REQ at SRR | Adversarial cycle with nse-verification critic |
| 2 | orch-planner | Assign SRR strategies to nse-verification | S-013 (adversarial-challenge) + S-007 (adversarial-compliance) + S-014 (adversarial-scoring) |
| 3 | ps-researcher | Create requirements artifact | Requirements document persisted |
| 4 | nse-verification | Execute SRR review | adversarial-challenge generates anti-requirements; adversarial-compliance evaluates NPR 7123.1D; adversarial-scoring produces quality score |
| 5 | orch-tracker | Record scores | Per-strategy findings recorded |
| 6 | ps-researcher | Revise requirements | Address nse-verification findings |
| 7 | nse-verification | Re-score | Updated quality score |
| 8 | orch-tracker | Gate determination | PASS/REVISE/ESCALATE |

**Pass Criteria:** Strategy-to-gate mapping from EN-305 TASK-004 correctly drives nse-verification mode selection at SRR.

### ITC-003: Cross-Skill Barrier with Quality Gate

**Scenario:** Sync barrier between two phases requires all upstream quality gates to pass before cross-pollination.

| Step | Actor | Action | Expected Outcome |
|------|-------|--------|-----------------|
| 1 | orch-tracker | Phase 1 quality score: 0.935 | PASS recorded |
| 2 | orch-tracker | Phase 2 quality score: 0.88 | FAIL (< 0.92) |
| 3 | orch-tracker | Barrier quality gate check | Barrier NOT crossed; Phase 2 blocks downstream |
| 4 | orch-tracker | Escalation | Blocker created per FR-307-014; P-020 escalation |

**Pass Criteria:** Barrier enforcement per FR-307-018 prevents cross-pollination when any upstream phase fails quality gate.

### ITC-004: NSE Review Gate Progression (SRR -> PDR -> CDR -> TRR -> FRR)

**Scenario:** Full lifecycle review gate progression with increasing criticality.

| Gate | Default Criticality | Required Strategies | Expected Token Budget |
|------|-------------------|--------------------|--------------------|
| SRR | C2 | S-014, S-013, S-007, S-010 | ~12,100 |
| PDR | C2 | S-014, S-002, S-004, S-003, S-010 | ~15,200 |
| CDR | C3 | S-014, S-007, S-012, S-002, S-003, S-010 + recommended | ~27,200-35,100 |
| TRR | C2 | S-014, S-011, S-007, S-010 | ~18,000 |
| FRR | C4 | All 10 strategies | ~50,300 |

**Pass Criteria:** Strategy-to-gate mapping from EN-305 TASK-004 produces correct strategy sets; token budgets align with EN-304 TASK-002 canonical token cost table.

### ITC-005: Orchestration Synthesizer Adversarial Summary

**Scenario:** orch-synthesizer produces final synthesis incorporating adversarial review findings from both PS and NSE pipelines.

| Step | Input | Expected Output |
|------|-------|----------------|
| 1 | PS pipeline findings (ps-critic modes) | Adversarial review summary section (FR-307-019) |
| 2 | NSE pipeline findings (nse-verification, nse-reviewer) | Quality score trend analysis (FR-307-020) |
| 3 | Cross-pipeline comparison | Cross-pipeline pattern extraction (FR-307-021) |
| 4 | Strategy effectiveness data | Strategy effectiveness report (FR-307-022) |
| 5 | Accepted findings and deferrals | Residual risk documentation (FR-307-023) |

**Pass Criteria:** orch-synthesizer spec (EN-307 TASK-006) includes all 7 adversarial synthesis steps (A1 through A7).

### ITC-006: Auto-Escalation Across Skills

**Scenario:** Governance file modification triggers auto-escalation, affecting both PS and NSE adversarial mode selection.

| Step | Trigger | PS Impact | NSE Impact | ORCH Impact |
|------|---------|-----------|------------|-------------|
| 1 | Modify `.claude/rules/coding-standards.md` | AE-002: C3 minimum | FR-305-034: C3/C4 governance escalation | FR-307-001: C3 adversarial cycle |
| 2 | C3 mode activation | 6 required strategies (C3 pipeline) | C3 gate strategy set | Full adversarial cycle with 3+ iterations |
| 3 | Token budget adaptation | TOK-FULL: full C3 set (~31,300-38,900) | Per-gate C3 token budget | Budget estimation in plan |

**Pass Criteria:** Auto-escalation produces consistent C3 behavior across all 3 skills per EN-303 TASK-004 escalation rules.

---

## Test Data and Prerequisites

### Test Artifacts (Design-Phase Specifications)

| Test Category | Required Input | Source |
|--------------|---------------|--------|
| PS mode tests | Mode definitions (10) | EN-304 TASK-002 |
| PS invocation tests | Invocation protocol | EN-304 TASK-003 |
| PS agent spec tests | ps-critic v3.0.0 spec | EN-304 TASK-004 |
| NSE mode tests | nse-verification modes (4+1) | EN-305 TASK-002/005 |
| NSE mode tests | nse-reviewer modes (6) | EN-305 TASK-003/006 |
| NSE gate mapping tests | 10x5 mapping matrix | EN-305 TASK-004 |
| ORCH cycle tests | orch-planner v3.0.0 spec | EN-307 TASK-004 |
| ORCH quality tests | orch-tracker v3.0.0 spec | EN-307 TASK-005 |
| ORCH synthesis tests | orch-synthesizer v3.0.0 spec | EN-307 TASK-006 |
| Backward compat tests | BC-T-001 through BC-T-007 | EN-304 TASK-003 |

### Prerequisites

| # | Prerequisite | Status | Verified By |
|---|-------------|--------|-------------|
| 1 | EN-304 all 10 tasks complete | PASS (0.928) | TASK-010 validation report |
| 2 | EN-305 all 8 acceptance criteria met | PASS (0.928) | TASK-010 validation report |
| 3 | EN-307 all 11 acceptance criteria met | PASS (0.928) | TASK-010 validation report |
| 4 | Cross-enabler SSOT verified consistent | PASS | TASK-010 cross-enabler assessment |
| 5 | ADR-EPIC002-001 ratified | ACCEPTED | EN-302 TASK-005 |

---

## Test Execution Approach

### Execution Order

```
Phase 1: Intra-Skill Unit Tests
  |
  +---> PS mode tests (10 strategies in ps-critic) -----> TASK-002
  |
  +---> NSE mode tests (10 strategies in nse-verification + nse-reviewer) -----> TASK-003
  |
  +---> ORCH loop tests (orchestration feedback cycle tests) -----> TASK-004
  |
Phase 2: Cross-Skill Integration Tests
  |
  +---> ITC-001 through ITC-006 (inter-skill coordination)
  |
Phase 3: Backward Compatibility Tests
  |
  +---> BC-T-001 through BC-T-007 (PS) + BC-305 tests (NSE)
  |
Phase 4: Cross-Platform Assessment
  |
  +---> macOS, Linux, Windows compatibility -----> TASK-005
  |
Phase 5: QA Audit and Reporting
  |
  +---> QA audit against FEAT-004 ACs -----> TASK-006
  +---> Status report -----> TASK-007
  +---> Configuration baseline -----> TASK-008
```

---

## Pass/Fail Criteria

### Overall Test Plan Pass Criteria

| # | Criterion | Threshold |
|---|-----------|-----------|
| 1 | All 10 strategies have verified mode definitions in /problem-solving | 10/10 |
| 2 | All 10 strategies have verified mappings in /nasa-se (via nse-verification or nse-reviewer) | 10/10 |
| 3 | All 10 strategies have verified integration points in /orchestration | 10/10 |
| 4 | Inter-skill coordination tests pass | 6/6 scenarios |
| 5 | Backward compatibility tests pass | 12/12 (7 PS + 5 NSE) |
| 6 | Cross-enabler SSOT consistency verified | 7/7 dimensions |
| 7 | No BLOCKING findings remain | 0 blocking |

### Individual Test Case Pass Criteria

| Test Level | Pass | Fail |
|-----------|------|------|
| Mode definition test | Mode contains all 7 required components (FR-304-002) | Missing component |
| Invocation test | Protocol handles explicit, automatic, and multi-mode selection | Selection failure or incorrect mode set |
| Pipeline test | Sequencing constraints (SEQ-001 through SEQ-005) satisfied | Constraint violation |
| Quality gate test | Score >= 0.92 produces PASS; < 0.92 produces REVISE | Incorrect gate determination |
| Backward compat test | Identical behavior without adversarial context | Behavior regression |

---

## Risk Assessment

| # | Risk | Probability | Impact | Mitigation |
|---|------|------------|--------|------------|
| 1 | nse-qa adversarial modes not testable (descoped) | HIGH | LOW | Descoping documented; requirements preserved; test deferred to follow-up enabler |
| 2 | FRR token budget estimate inaccurate | MEDIUM | MEDIUM | Flag for cross-agent budget analysis before FRR usage |
| 3 | EN-305 backward compatibility test specs not independently defined | MEDIUM | MEDIUM | Cross-reference EN-304 BC-T-001 through BC-T-007 as exemplar |
| 4 | Token budget adaptation not testable at design phase | HIGH | LOW | Budget adaptation is specification-level; runtime testing deferred |
| 5 | Cross-skill orchestration complexity not fully exercised | MEDIUM | MEDIUM | Live ORCHESTRATION.yaml serves as proof-of-concept (NFR-307-008) |

---

## Traceability

| EN-306 AC | Coverage |
|-----------|----------|
| AC-1 | This document -- integration test plan covering 10 strategies x 3 skills |

### Requirements to Test Case Mapping

| Requirement Source | Test Cases |
|-------------------|------------|
| FR-304-001 (10 modes) | PS mode tests: 10 mode definitions |
| FR-304-003 (explicit selection) | PS invocation: explicit mode selection |
| FR-304-004 (automatic selection) | PS invocation: context-driven selection |
| FR-304-005 (multi-mode pipeline) | PS pipeline: C1-C4 canonical pipelines |
| FR-305-026 (strategy-gate mapping) | NSE gate: 10x5 mapping verification |
| FR-307-002 (cycle injection) | ORCH cycle: creator-critic-revision pattern |
| FR-307-018 (barrier quality gate) | ITC-003: barrier enforcement |
| BC-304-001 through BC-304-003 | Backward compatibility: BC-T-001 through BC-T-007 |
| BC-305-001 through BC-305-005 | Backward compatibility: NSE regression tests |

---

## References

| # | Citation | Relevance |
|---|----------|-----------|
| 1 | EN-304 TASK-002 (Mode Design) | 10 adversarial mode definitions for ps-critic |
| 2 | EN-304 TASK-003 (Invocation Protocol) | Selection algorithm, pipeline execution, BC tests |
| 3 | EN-305 TASK-001 (Requirements) | 50 formal requirements for NSE adversarial enhancement |
| 4 | EN-305 TASK-004 (Gate Mapping) | 10x5 strategy-to-gate matrix |
| 5 | EN-307 TASK-001 (Requirements) | 44 formal requirements for orchestration enhancement |
| 6 | EN-307 TASK-002 (Planner Design) | Adversarial cycle detection and injection |
| 7 | EN-307 TASK-003 (Tracker Design) | Quality gate tracking and enforcement |
| 8 | EN-304 TASK-010 (Validation Report) | Cross-enabler consistency verification |
| 9 | ADR-EPIC002-001 | 10 selected strategies, quality layers, P-003 compliance |

---

*Document ID: FEAT-004:EN-306:TASK-001*
*Agent: ps-validator-306*
*Created: 2026-02-13*
*Status: Complete*
