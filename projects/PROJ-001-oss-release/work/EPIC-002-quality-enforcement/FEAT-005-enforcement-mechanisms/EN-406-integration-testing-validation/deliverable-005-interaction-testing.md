# TASK-005: Enforcement Mechanism Interaction Testing

<!--
TEMPLATE: Task Deliverable
VERSION: 1.1.0
ENABLER: EN-406
AC: AC-5
CREATED: 2026-02-13 (ps-validator-406)
REVISED: 2026-02-14 (ps-revision-406) -- Iteration 1 critique fixes (F-012, F-013, F-014)
PURPOSE: Test specifications for enforcement mechanism interactions and conflict detection
-->

> **Type:** deliverable
> **Status:** complete
> **Parent:** EN-406-integration-testing-validation
> **AC Mapping:** AC-5 (All enforcement mechanism interactions tested with no conflicts)
> **Agent:** ps-validator-406
> **Created:** 2026-02-13

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | Interaction testing scope and approach |
| [Interaction Matrix](#interaction-matrix) | Complete mechanism interaction map |
| [Pairwise Interaction Tests](#pairwise-interaction-tests) | Two-mechanism interaction tests |
| [Three-Way Interaction Tests](#three-way-interaction-tests) | Full stack interaction tests |
| [Defense-in-Depth Chain Tests](#defense-in-depth-chain-tests) | Compensation chain validation |
| [Conflict Detection Tests](#conflict-detection-tests) | Potential conflict scenarios |
| [Gap Analysis Tests](#gap-analysis-tests) | Enforcement gap detection |
| [Requirements Traceability](#requirements-traceability) | Test-to-requirement mapping |
| [References](#references) | Source documents |

---

## Overview

This document specifies test cases for interactions between enforcement mechanisms. Unlike individual mechanism testing (TASK-002 through TASK-004), these tests focus on how mechanisms behave when multiple are active simultaneously. The key concerns are:

1. **Conflicts:** Do any two mechanisms produce contradictory enforcement signals?
2. **Gaps:** Are there enforcement scenarios where no mechanism provides coverage?
3. **Redundancy:** Is redundancy intentional (defense-in-depth) or wasteful?
4. **Compensation:** Does the L1->L2->L3 compensation chain work correctly?
5. **Performance:** Does the combined stack meet the <2s performance budget?

### Verification Method Distribution

> **Note on Analysis Verification:** 9 of 24 tests (37.5%) in this deliverable use Analysis or Analytical Assessment verification. This is intentional: interaction testing inherently involves cross-mechanism reasoning, gap analysis, and design rationale assessment that cannot be reduced to deterministic automated checks. Where possible, tests have been classified as Test (automated executable) or Inspection (manual review). The remaining Analysis-based tests address emergent properties (compensation chain effectiveness, enforcement gaps, context rot resilience) that require human judgment to evaluate.

### Mechanism Interaction Space

| | L1 Rules | L2 UserPromptSubmit | L3 PreToolUse | Session Preamble |
|---|---|---|---|---|
| **L1 Rules** | -- | TC-PW-001 | TC-PW-002 | TC-PW-003 |
| **L2 UserPromptSubmit** | -- | -- | TC-PW-004 | TC-PW-005 |
| **L3 PreToolUse** | -- | -- | -- | TC-PW-006 |
| **Session Preamble** | -- | -- | -- | -- |

### Test Summary

| Category | Test Count | ID Range |
|----------|------------|----------|
| Pairwise Interactions | 6 | TC-PW-001 through TC-PW-006 |
| Three-Way Interactions | 4 | TC-TW-001 through TC-TW-004 |
| Defense-in-Depth Chain | 5 | TC-DID-001 through TC-DID-005 |
| Conflict Detection | 5 | TC-CONF-001 through TC-CONF-005 |
| Gap Analysis | 4 | TC-GAP-001 through TC-GAP-004 |
| **Total** | **24** | |

---

## Interaction Matrix

### Complete Mechanism Inventory

| ID | Mechanism | Layer | Type | Token Cost | Rot Immunity |
|----|-----------|-------|------|------------|--------------|
| M1 | `.claude/rules/*.md` auto-loaded files | L1 | Static | ~12,476 | LOW |
| M2 | UserPromptSubmit V-024 hook | L2 | Dynamic | ~600/prompt | MEDIUM |
| M3 | PreToolUse V-038/V-041 hook | L3 | Active | 0 | HIGH |
| M4 | SessionStart quality preamble | L1+ | Static | ~435 | LOW |

### Interaction Types

| Type | Description | Concern Level |
|------|-------------|---------------|
| Reinforcing | Both mechanisms enforce the same rule | LOW (intentional defense-in-depth) |
| Complementary | Mechanisms cover different aspects | NONE (ideal) |
| Conflicting | Mechanisms produce contradictory signals | HIGH (must resolve) |
| Overlapping | Mechanisms partially overlap in coverage | MEDIUM (evaluate waste) |
| Independent | No interaction between mechanisms | NONE |

---

## Pairwise Interaction Tests

### TC-PW-001: L1 Rules + L2 UserPromptSubmit

| Field | Value |
|-------|-------|
| **ID** | TC-PW-001 |
| **Objective** | Verify L1 rules and L2 prompt reinforcement are complementary |
| **Mechanisms** | M1 (L1 Rules) + M2 (L2 UserPromptSubmit) |
| **Interaction Type** | Overlapping (intentional) |
| **Scenario** | Quality gate threshold (>= 0.92) specified in both L1 rules and L2 reinforcement |
| **Steps** | 1. Identify shared content between L1 rules and L2 output. 2. Verify L2 compact version complements L1 detailed version. 3. Check for contradictions. |
| **Expected Behavior** | L1 provides full rule detail (comprehensive, once); L2 provides compact reminder (per-prompt). Content is consistent but not redundant in purpose. |
| **Conflict Risk** | LOW - Different delivery mechanisms for same principles |
| **Pass Criteria** | No contradictions; L2 is compact subset of L1 themes; different token budgets serve different purposes |
| **Requirements** | REQ-403-010, REQ-404-001 |
| **Verification** | Inspection |

### TC-PW-002: L1 Rules + L3 PreToolUse

| Field | Value |
|-------|-------|
| **ID** | TC-PW-002 |
| **Objective** | Verify L1 rules and L3 pre-action blocking reinforce consistently |
| **Mechanisms** | M1 (L1 Rules) + M3 (L3 PreToolUse) |
| **Interaction Type** | Reinforcing (defense-in-depth) |
| **Scenario** | Import boundary rule (H-06) in L1 rules AND V-038 in L3 blocking |
| **Steps** | 1. Verify L1 states "domain cannot import infrastructure" (H-06). 2. Verify L3 blocks domain files importing infrastructure (V-038). 3. Confirm same boundary definition. |
| **Expected Behavior** | L1 instructs; L3 enforces. Same boundary, different mechanisms. L3 is deterministic backup for L1 guidance. |
| **Conflict Risk** | NONE - Mutually reinforcing |
| **Pass Criteria** | Boundary definitions identical; no conflict possible |
| **Requirements** | REQ-403-032, REQ-404-010 |
| **Verification** | Inspection |

### TC-PW-003: L1 Rules + Session Preamble

| Field | Value |
|-------|-------|
| **ID** | TC-PW-003 |
| **Objective** | Verify L1 rules and session preamble are complementary |
| **Mechanisms** | M1 (L1 Rules) + M4 (Session Preamble) |
| **Interaction Type** | Overlapping (designed) |
| **Scenario** | Constitutional principles (P-003, P-020, P-022) in both L1 rules and session preamble |
| **Steps** | 1. Extract principle references from L1 rules. 2. Extract from session preamble. 3. Verify consistency. |
| **Expected Behavior** | L1 rules contain full principle details; session preamble provides compact summary. Consistent definitions. |
| **Conflict Risk** | LOW - Designed overlap for resilience |
| **Pass Criteria** | No contradictions in principle definitions; preamble is accurate condensation |
| **Requirements** | REQ-404-020, FR-405-007 |
| **Verification** | Inspection |

### TC-PW-004: L2 UserPromptSubmit + L3 PreToolUse

| Field | Value |
|-------|-------|
| **ID** | TC-PW-004 |
| **Objective** | Verify L2 reinforcement and L3 blocking work together correctly |
| **Mechanisms** | M2 (L2 UserPromptSubmit) + M3 (L3 PreToolUse) |
| **Interaction Type** | Complementary (defense-in-depth) |
| **Scenario** | L2 reinforces "follow hexagonal architecture" then L3 blocks violation |
| **Steps** | 1. Trigger L2 with architecture-related prompt. 2. Attempt tool use that violates architecture. 3. Verify L3 blocks independently of L2. |
| **Expected Behavior** | L2 reinforces guidance (advisory); L3 blocks deterministically (enforcement). L3 operates independently - does not rely on L2 having been delivered. |
| **Conflict Risk** | NONE - L3 is independent deterministic enforcement |
| **Pass Criteria** | L3 blocks regardless of whether L2 reinforcement was delivered |
| **Requirements** | REQ-403-010, REQ-403-030 |
| **Verification** | Test |

### TC-PW-005: L2 UserPromptSubmit + Session Preamble

| Field | Value |
|-------|-------|
| **ID** | TC-PW-005 |
| **Objective** | Verify L2 per-prompt and session preamble are complementary |
| **Mechanisms** | M2 (L2 UserPromptSubmit) + M4 (Session Preamble) |
| **Interaction Type** | Complementary |
| **Scenario** | Session preamble establishes quality context once; L2 reinforces per prompt |
| **Steps** | 1. Capture session preamble content. 2. Capture L2 output for subsequent prompt. 3. Analyze overlap and complementarity. |
| **Expected Behavior** | Session preamble provides full context at start; L2 provides compact reinforcement as context degrades. Additive, not redundant. |
| **Conflict Risk** | LOW - By design complementary |
| **Pass Criteria** | Content complementary; no contradictions |
| **Requirements** | IR-405-003, REQ-403-010 |
| **Verification** | Inspection |

### TC-PW-006: L3 PreToolUse + Session Preamble

| Field | Value |
|-------|-------|
| **ID** | TC-PW-006 |
| **Objective** | Verify L3 operates independently of session preamble |
| **Mechanisms** | M3 (L3 PreToolUse) + M4 (Session Preamble) |
| **Interaction Type** | Independent |
| **Scenario** | L3 blocks violations regardless of whether session preamble was injected |
| **Steps** | 1. Test L3 with session preamble present. 2. Test L3 without session preamble (QUALITY_CONTEXT_AVAILABLE=False). 3. Verify identical L3 behavior. |
| **Expected Behavior** | L3 is context-rot immune; operates deterministically regardless of session context |
| **Conflict Risk** | NONE - Completely independent |
| **Pass Criteria** | Identical L3 behavior with and without preamble |
| **Requirements** | REQ-403-030 |
| **Verification** | Test |

---

## Three-Way Interaction Tests

### TC-TW-001: L1 + L2 + L3 Nominal Operation

| Field | Value |
|-------|-------|
| **ID** | TC-TW-001 |
| **Objective** | Verify all three enforcement layers operate correctly in a standard session |
| **Scenario** | Normal development session with all mechanisms active |
| **Steps** | 1. Start session (L1 rules loaded + session preamble). 2. Submit prompt (L2 reinforcement triggered). 3. Attempt valid tool use (L3 approves). 4. Attempt invalid tool use (L3 blocks). |
| **Expected Behavior** | L1 provides rules; L2 reinforces per prompt; L3 gates tool use. No interference. |
| **Pass Criteria** | All layers function correctly; no degradation from multi-layer operation |
| **Requirements** | FEAT-005 AC-13 |
| **Verification** | Test |

### TC-TW-002: L1 + L2 + L3 High-Criticality Operation

| Field | Value |
|-------|-------|
| **ID** | TC-TW-002 |
| **Objective** | Verify all layers respond appropriately to C4 critical operations |
| **Scenario** | User modifying governance document |
| **Steps** | 1. L2 detects C4 keywords, provides maximum reinforcement. 2. L3 detects governance file, escalates to C4. 3. L1 rules provide relevant constraints. |
| **Expected Behavior** | Coordinated C4 response: L2 maximum reinforcement + L3 governance escalation + L1 constitutional principles |
| **Pass Criteria** | All layers escalate consistently to C4 |
| **Requirements** | REQ-403-060, REQ-403-036, REQ-404-030 |
| **Verification** | Test |

### TC-TW-003: L1 + L2 + Session Preamble Token Budget

| Field | Value |
|-------|-------|
| **ID** | TC-TW-003 |
| **Objective** | Verify combined token cost of all context-consuming mechanisms |
| **Scenario** | Full session with all mechanisms active |
| **Steps** | 1. Measure L1 tokens (rules, ~11,176). 2. Add session preamble tokens (~435). 3. Add L2 per-prompt tokens (~600). 4. Calculate total first-prompt cost. |
| **Expected Output** | First-prompt total: ~12,211 (L1+preamble) + ~600 (L2) = ~12,811 tokens |
| **Pass Criteria** | Total within acceptable context window consumption |
| **Requirements** | REQ-404-001, PR-405-001 |
| **Verification** | Analysis |

### TC-TW-004: Rules + Hooks + Preamble Content Consistency

| Field | Value |
|-------|-------|
| **ID** | TC-TW-004 |
| **Objective** | Verify content consistency across all three delivery mechanisms |
| **Scenario** | Cross-reference quality gate threshold across all mechanisms |
| **Steps** | 1. Extract >= 0.92 threshold from L1 rules. 2. Extract from L2 output. 3. Extract from session preamble. 4. Verify all match. |
| **Expected Output** | Identical threshold value across all mechanisms |
| **Pass Criteria** | Zero inconsistencies in shared constants |
| **Requirements** | REQ-404-044, FR-405-006 |
| **Verification** | Inspection |

---

## Defense-in-Depth Chain Tests

### TC-DID-001: Compensation Chain - L1 Fully Available

| Field | Value |
|-------|-------|
| **ID** | TC-DID-001 |
| **Objective** | Verify defense-in-depth when L1 is fully available (early in session) |
| **Scenario** | Fresh session, minimal context consumption |
| **Steps** | 1. Start fresh session. 2. Verify L1 rules fully in context. 3. Verify L2 reinforcement present. 4. Verify L3 gating active. |
| **Expected Behavior** | All three layers active; L1 at full effectiveness; L2 and L3 provide additional assurance |
| **Pass Criteria** | All layers operational; defense-in-depth established |
| **Requirements** | REQ-403-085 |
| **Verification** | Test |

### TC-DID-002: Compensation Chain - L1 Degraded

| Field | Value |
|-------|-------|
| **ID** | TC-DID-002 |
| **Objective** | Verify L2 compensates when L1 degrades due to context rot |
| **Scenario** | Long session where L1 rules are buried deep in context |
| **Steps** | 1. Simulate long session (conceptual - L1 attention weight decreased). 2. Verify L2 per-prompt reinforcement still fresh (re-injected each prompt). 3. Verify L3 still blocking violations (deterministic, context-immune). |
| **Expected Behavior** | L2 re-injection compensates for L1 degradation; L3 continues deterministic enforcement |
| **Pass Criteria** | L2 reinforcement effective; L3 enforcement unchanged |
| **Requirements** | REQ-403-086 |
| **Verification** | Analytical Assessment |
| **Note** | Context rot cannot be reliably simulated in a test environment. This test verifies the *design rationale* that L2 re-injection compensates for L1 degradation, based on architectural analysis of the compensation chain. L3 deterministic behavior can be independently verified via TC-DID-003. |

### TC-DID-003: Compensation Chain - L1 + L2 Degraded

| Field | Value |
|-------|-------|
| **ID** | TC-DID-003 |
| **Objective** | Verify L3 maintains enforcement when both L1 and L2 are degraded |
| **Scenario** | Worst case: both L1 and L2 context influence diminished |
| **Steps** | 1. Assume L1 fully degraded. 2. Assume L2 influence diminished. 3. Verify L3 still blocks import violations. 4. Verify L3 still blocks one-class-per-file violations. |
| **Expected Behavior** | L3 operates as last line of defense; deterministic, zero-token, context-rot immune |
| **Pass Criteria** | L3 enforcement unaffected by L1/L2 state |
| **Requirements** | REQ-403-087, REQ-403-030 |
| **Verification** | Test |

### TC-DID-004: Compensation Chain - L3 Coverage Scope

| Field | Value |
|-------|-------|
| **ID** | TC-DID-004 |
| **Objective** | Assess which enforcement aspects L3 covers vs. which depend on L1/L2 |
| **Scenario** | Full inventory of enforcement rules vs. L3 coverage |
| **Steps** | 1. List all 24 HARD rules. 2. Identify which are enforceable by L3 (AST-verifiable). 3. Identify which depend solely on L1/L2 (behavioral guidance). |
| **Expected Output** | L3 covers: V-038 (import boundaries), V-041 (one-class-per-file), governance escalation. L1/L2 cover: naming conventions, documentation, testing, constitutional awareness. |
| **Pass Criteria** | Coverage matrix documented; gaps acknowledged with mitigation rationale |
| **Requirements** | REQ-403-085, REQ-403-086 |
| **Verification** | Analysis |

### TC-DID-005: Compensation Chain - Graceful Degradation Path

| Field | Value |
|-------|-------|
| **ID** | TC-DID-005 |
| **Objective** | Verify graceful degradation follows designed priority order |
| **Scenario** | Progressive failure of enforcement layers |
| **Steps** | 1. Remove L1 (rules not loaded) -> L2 and L3 still work. 2. Remove L2 (hook disabled) -> L3 still works. 3. Remove L3 (hook disabled) -> only L1 remains. |
| **Expected Behavior** | Each layer fails independently; remaining layers continue; system degrades gracefully |
| **Pass Criteria** | No cascading failures; each layer is independently resilient |
| **Requirements** | REQ-403-085, REQ-403-070 |
| **Verification** | Test |

---

## Conflict Detection Tests

### TC-CONF-001: Token Budget Conflict

| Field | Value |
|-------|-------|
| **ID** | TC-CONF-001 |
| **Objective** | Verify L1 rules + session preamble + L2 reinforcement do not exceed context budget |
| **Scenario** | Calculate combined token impact |
| **Steps** | 1. Sum: L1 rules (~11,176) + session preamble (~435) + CLAUDE.md + L2 (~600) + other auto-loaded content. 2. Compare to available context window. |
| **Expected Output** | Total context consumption documented and within acceptable limits |
| **Pass Criteria** | Combined enforcement token consumption MUST NOT exceed 15% of the available context window. For a 200K-token context window, this means total enforcement overhead (L1 + preamble + L2 per first prompt) MUST be <= 30,000 tokens. Current estimate: ~12,811 tokens (6.4% of 200K), well within threshold. |
| **Requirements** | REQ-404-001, PR-405-001 |
| **Verification** | Analysis |

### TC-CONF-002: Criticality Level Disagreement

| Field | Value |
|-------|-------|
| **ID** | TC-CONF-002 |
| **Objective** | Verify L2 and L3 agree on criticality for the same operation |
| **Scenario** | User modifies a rule file - both L2 and L3 should detect C3 |
| **Steps** | 1. Submit prompt about modifying rules (L2 detects C3). 2. Attempt tool use on rule file (L3 escalates to C3). 3. Compare criticality assessments. |
| **Expected Output** | Both L2 and L3 assess C3 for rule file modifications |
| **Pass Criteria** | Criticality agreement; or documented hierarchy if disagreement expected |
| **Requirements** | REQ-403-060, REQ-403-036 |
| **Verification** | Test |

### TC-CONF-003: Enforcement Signal Contradiction

| Field | Value |
|-------|-------|
| **ID** | TC-CONF-003 |
| **Objective** | Verify no scenario where one mechanism approves what another blocks |
| **Scenario** | Hypothetical: L1 rule says "you may" but L3 blocks |
| **Steps** | 1. Enumerate L3 blocking rules. 2. For each L3 rule, verify L1 does not contradict. 3. For each L3 rule, verify L2 does not contradict. |
| **Expected Output** | No contradictions found |
| **Pass Criteria** | Zero contradiction scenarios |
| **Requirements** | FEAT-005 AC-14 |
| **Verification** | Analysis |

### TC-CONF-004: Enforcement Ordering Ambiguity

| Field | Value |
|-------|-------|
| **ID** | TC-CONF-004 |
| **Objective** | Verify enforcement order is well-defined when multiple mechanisms trigger |
| **Scenario** | User submits prompt (L2) then immediately uses tool (L3) |
| **Steps** | 1. Document enforcement execution order. 2. Verify order is deterministic. 3. Verify order makes semantic sense. |
| **Expected Output** | Order: L1 (loaded at start) -> Session preamble (loaded at start) -> L2 (per prompt) -> L3 (per tool use). Well-defined, deterministic. |
| **Pass Criteria** | Execution order documented and deterministic |
| **Requirements** | FEAT-005 AC-13 |
| **Verification** | Inspection |

### TC-CONF-005: Fail-Open Conflict

| Field | Value |
|-------|-------|
| **ID** | TC-CONF-005 |
| **Objective** | Verify fail-open behavior is consistent across all mechanisms |
| **Scenario** | Each mechanism fails - verify all fail-open (not fail-closed) |
| **Steps** | 1. Force L2 failure -> operation proceeds. 2. Force L3 failure -> operation proceeds. 3. Force session preamble failure -> session starts. |
| **Expected Output** | All mechanisms fail-open; no mechanism can cause operational blockage through its own failure |
| **Pass Criteria** | Uniform fail-open behavior |
| **Requirements** | REQ-403-070 |
| **Verification** | Test |

---

## Gap Analysis Tests

### TC-GAP-001: HARD Rule Coverage Gap Analysis

| Field | Value |
|-------|-------|
| **ID** | TC-GAP-001 |
| **Objective** | Identify HARD rules not enforceable by any deterministic mechanism |
| **Scenario** | Map each of 24 HARD rules to enforcement mechanisms |
| **Steps** | 1. For each HARD rule (H-01 through H-24), identify which mechanisms can enforce it. 2. Identify rules enforceable only by L1/L2 (behavioral, non-deterministic). 3. Document coverage gaps. |
| **Expected Output** | Coverage matrix: H-xx -> {M1, M2, M3, M4} mapping |
| **Pass Criteria** | All HARD rules have at least one enforcement mechanism; gaps documented with rationale |
| **Requirements** | REQ-404-010, REQ-403-085 |
| **Verification** | Analysis |

### TC-GAP-002: Adversarial Strategy Coverage Gap

| Field | Value |
|-------|-------|
| **ID** | TC-GAP-002 |
| **Objective** | Verify all 10 adversarial strategies are referenced by at least one enforcement mechanism |
| **Scenario** | Map each strategy to enforcement mechanisms |
| **Steps** | 1. List 10 strategies. 2. Verify each appears in L1 rules, L2 output, or session preamble. |
| **Expected Output** | 10/10 strategies have enforcement coverage |
| **Pass Criteria** | No orphaned strategies |
| **Requirements** | REQ-404-020, SR-405-001 |
| **Verification** | Inspection |

### TC-GAP-003: File Type Coverage Gap

| Field | Value |
|-------|-------|
| **ID** | TC-GAP-003 |
| **Objective** | Identify file types not covered by L3 enforcement |
| **Scenario** | L3 only validates Python files in src/ |
| **Steps** | 1. List file types in repository. 2. Identify which L3 validates. 3. Document uncovered types. |
| **Expected Output** | L3 covers: .py files in src/. Not covered: .md, .yaml, .json, scripts/, tests/, etc. |
| **Pass Criteria** | Gaps documented; rationale for each (intentional/acceptable) |
| **Requirements** | REQ-403-039 |
| **Verification** | Analysis |

### TC-GAP-004: Context Rot Compensation Gap

| Field | Value |
|-------|-------|
| **ID** | TC-GAP-004 |
| **Objective** | Identify enforcement aspects lost when context fully rots |
| **Scenario** | Complete L1 + partial L2 degradation |
| **Steps** | 1. List all enforcement aspects. 2. Identify which survive complete L1 rot. 3. Identify which survive L2 degradation. 4. Document L3-only coverage. |
| **Expected Output** | L3-only coverage: import boundaries (V-038), one-class-per-file (V-041), governance escalation. Everything else depends on L1/L2 effectiveness. |
| **Pass Criteria** | Gap analysis documented; risk accepted or mitigated |
| **Requirements** | REQ-403-087, REQ-404-063 |
| **Verification** | Analysis |

---

## Requirements Traceability

| Test ID | Requirements Verified |
|---------|----------------------|
| TC-PW-001 | REQ-403-010, REQ-404-001 |
| TC-PW-002 | REQ-403-032, REQ-404-010 |
| TC-PW-003 | REQ-404-020, FR-405-007 |
| TC-PW-004 | REQ-403-010, REQ-403-030 |
| TC-PW-005 | IR-405-003, REQ-403-010 |
| TC-PW-006 | REQ-403-030 |
| TC-TW-001 | FEAT-005 AC-13 |
| TC-TW-002 | REQ-403-060, REQ-403-036, REQ-404-030 |
| TC-TW-003 | REQ-404-001, PR-405-001 |
| TC-TW-004 | REQ-404-044, FR-405-006 |
| TC-DID-001 | REQ-403-085 |
| TC-DID-002 | REQ-403-086 |
| TC-DID-003 | REQ-403-087, REQ-403-030 |
| TC-DID-004 | REQ-403-085, REQ-403-086 |
| TC-DID-005 | REQ-403-085, REQ-403-070 |
| TC-CONF-001 | REQ-404-001, PR-405-001 |
| TC-CONF-002 | REQ-403-060, REQ-403-036 |
| TC-CONF-003 | FEAT-005 AC-14 |
| TC-CONF-004 | FEAT-005 AC-13 |
| TC-CONF-005 | REQ-403-070 |
| TC-GAP-001 | REQ-404-010, REQ-403-085 |
| TC-GAP-002 | REQ-404-020, SR-405-001 |
| TC-GAP-003 | REQ-403-039 |
| TC-GAP-004 | REQ-403-087, REQ-404-063 |

---

## References

| Document | Path | Relevance |
|----------|------|-----------|
| TASK-001 Integration Test Plan | `TASK-001-integration-test-plan.md` | Master test plan, interaction matrix |
| TASK-002 Hook Testing | `TASK-002-hook-enforcement-testing.md` | Individual hook tests |
| TASK-003 Rule Testing | `TASK-003-rule-enforcement-testing.md` | Individual rule tests |
| TASK-004 Session Context Testing | `TASK-004-session-context-testing.md` | Individual session tests |
| EN-403 TASK-001 | `../EN-403-hook-based-enforcement/TASK-001-hook-requirements.md` | Defense-in-depth requirements |
| EN-404 TASK-003 | `../EN-404-rule-based-enforcement/TASK-003-tiered-enforcement.md` | Tiered enforcement, token budgets |
| EN-405 TASK-001 | `../EN-405-session-context-enforcement/TASK-001-requirements.md` | Session context requirements |
| ADR-EPIC002-002 | FEAT-004 outputs | 5-Layer architecture, compensation chain |

---

*Generated by ps-validator-406 | 2026-02-13 | EN-406 AC-5*
