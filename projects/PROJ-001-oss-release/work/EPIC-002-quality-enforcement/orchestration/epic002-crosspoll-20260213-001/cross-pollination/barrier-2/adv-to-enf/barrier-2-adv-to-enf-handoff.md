# Barrier 2 Cross-Pollination Handoff: ADV to ENF

<!--
DOCUMENT-ID: EPIC-002:ORCH:BARRIER-2:ADV-TO-ENF
TYPE: Cross-Pollination Handoff Artifact
DATE: 2026-02-14
SOURCE-PIPELINE: ADV (FEAT-004: Adversarial Strategy Research)
TARGET-PIPELINE: ENF (FEAT-005: Enforcement Mechanisms)
BARRIER: Barrier 2 (ADV Phase 2 complete -> ENF Phase 3 begins)
AUTHOR: ps-synthesizer (orchestration worker)
STATUS: Complete
-->

> **Handoff ID:** BARRIER-2-ADV-TO-ENF
> **Date:** 2026-02-14
> **Source:** FEAT-004 (ADV Pipeline), Phase 2 -- EN-303
> **Target:** FEAT-005 (ENF Pipeline), Phase 3 -- EN-405
> **Barrier:** Barrier 2

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | What ADV Phase 2 produced and what ENF Phase 3 needs |
| [8-Dimension Context Taxonomy](#8-dimension-context-taxonomy) | The context dimensions that determine strategy selection at session time |
| [Per-Criticality Strategy Sets](#per-criticality-strategy-sets) | Required and optional strategies at each criticality level (C1-C4) |
| [Decision Tree for Strategy Selection](#decision-tree-for-strategy-selection) | How to select strategies based on context at session/review time |
| [Token Budget Constraints](#token-budget-constraints) | Per-strategy costs and cumulative budgets by criticality |
| [Strategy Pairings for Multi-Strategy Sessions](#strategy-pairings-for-multi-strategy-sessions) | SYN, TEN, and COM pairs with sequencing guidance |
| [ENF-MIN Handling for Degraded Environments](#enf-min-handling-for-degraded-environments) | Strategy feasibility and substitution under L1-only enforcement |
| [Defense-in-Depth Compensation Chain](#defense-in-depth-compensation-chain) | Which strategies compensate when enforcement layers fail |
| [Enforcement Layer Delivery Mapping](#enforcement-layer-delivery-mapping) | How each strategy maps to L1-L5 and Process layers |
| [Creator-Critic-Revision Cycle Integration](#creator-critic-revision-cycle-integration) | Strategy assignments per iteration of the review cycle |
| [Auto-Escalation Rules](#auto-escalation-rules) | Governance-driven criticality overrides |
| [Platform Adaptation](#platform-adaptation) | Portable fallback paths for non-Claude-Code environments |
| [Integration Guidance for EN-405](#integration-guidance-for-en-405) | Specific recommendations for session context enforcement |
| [Quality Gate and Scoring](#quality-gate-and-scoring) | How the 0.92 threshold maps to strategy deployment |
| [Source Artifact Traceability](#source-artifact-traceability) | Full list of source documents for this handoff |

---

## Executive Summary

### What ADV Phase 2 Produced

The ADV pipeline (FEAT-004) completed EN-303 (Situational Applicability Mapping) in Phase 2, producing four artifacts at v1.1.0 (quality score: 0.928, PASS):

1. **TASK-001 (Context Taxonomy)** -- Defined an 8-dimension context taxonomy that determines which adversarial strategies to apply in any given review situation. The 8 dimensions span 19,440 unique context combinations (reduced to 12,960 practical combinations via the ENF = f(PLAT) derivation with ENF-MIN override). Each dimension has a formal enumeration with codes, definitions, and impact on strategy selection.

2. **TASK-002 (Requirements)** -- Defined 42 formal "shall" requirements (REQ-303-001 through REQ-303-042) following NPR 7123.1D conventions. 30 HARD priority, 11 MEDIUM, 1 LOW. 100% coverage of all 11 functional requirements (FR-001 through FR-011) and all 7 non-functional requirements (NFR-001 through NFR-007). Bidirectional traceability to ADR-EPIC002-001 and Barrier-1 ENF-to-ADV handoff.

3. **TASK-003 (Strategy Profiles)** -- Produced comprehensive applicability profiles for all 10 selected strategies, covering: when to use, when to avoid, complementary and tension pairings, preconditions, expected outcomes, token budget, enforcement layer mapping (including ENF-MIN handling), platform portability, and decision criticality mapping. Also produced: a complete 45-pair catalog (14 SYN + 29 COM + 2 TEN = C(10,2)), enforcement gap analysis, excluded strategy coverage gaps, defense-in-depth compensation chain, and cumulative token budget verification per criticality.

4. **TASK-004 (Decision Tree)** -- Built a deterministic, O(1)-traversal decision tree that takes 8 context inputs and produces: (a) a base strategy set, (b) a delivery mechanism per strategy, (c) token-budget-adapted variants, (d) platform-adapted variants, (e) iteration-specific assignments for the creator-critic-revision cycle, and (f) escalation triggers. Includes auto-escalation rules (AE-001 through AE-006), ENF-MIN override rules (ENF-MIN-001 through ENF-MIN-004), PR-001 precedence rule, and fallback paths for ambiguous contexts.

### What ENF Phase 3 Needs

EN-405 (Session Context Enforcement) implements session start context injection that reminds Claude of quality framework requirements. EN-405 needs:

- **Strategy selection at session time** -- How to determine which strategies apply based on the current context (criticality, platform, token budget, target type, phase, maturity, team).
- **The context taxonomy dimensions** -- What to evaluate at session start to classify the review context.
- **Per-criticality strategy sets** -- What to inject at each criticality level (C1 through C4).
- **ENF-MIN handling** -- How to adapt when enforcement layers are degraded (L1 only).
- **Strategy pairings** -- Which strategies have synergistic, tension, or compatible relationships for multi-strategy sessions.
- **The compensation chain** -- Which strategies compensate for enforcement layer failures (defense-in-depth).
- **Token budget awareness** -- How to adapt strategy injection when context window is constrained.
- **Auto-escalation rules** -- When to override criticality for governance-sensitive artifacts.

This handoff provides all of the above, extracted from EN-303's four artifacts.

---

## 8-Dimension Context Taxonomy

EN-303 TASK-001 defines 8 dimensions that classify any review context:

| # | Dimension | Code | Values | Role in Session Context |
|---|-----------|------|--------|------------------------|
| 1 | Review Target Type | TGT | CODE, ARCH, REQ, RES, DEC, PROC | Determines strategy affinity (which strategies are most valuable for this artifact type) |
| 2 | Review Phase | PH | EXPLORE, DESIGN, IMPL, VALID, MAINT | Determines divergent vs. convergent strategy preference |
| 3 | Decision Criticality | CRIT | C1, C2, C3, C4 | **Primary branching dimension** -- determines strategy intensity and quality layer |
| 4 | Artifact Maturity | MAT | DRAFT, REVIEW, APPR, BASE | Restricts review scope for approved/baselined artifacts |
| 5 | Team Composition | TEAM | SINGLE, MULTI, HIL | Determines which strategies are executable (some require multi-agent) |
| 6 | Enforcement Layer Availability | ENF | FULL, PORT, MIN | Determines strategy delivery mechanisms (derived from PLAT with ENF-MIN override) |
| 7 | Platform Context | PLAT | CC, CC-WIN, GENERIC | Determines hook availability; default ENF derivation: CC/CC-WIN -> FULL; GENERIC -> PORT |
| 8 | Token Budget State | TOK | FULL, CONST, EXHAUST | Constrains strategy selection by token cost |

**Design Decision (ENF = f(PLAT)):** Enforcement layer availability is derived from platform context by default. ENF-MIN (degraded, L1-only) can be explicitly specified on any platform when the environment is degraded (CI broken, hooks disabled, emergency session). This reduces the practical decision space from 19,440 to 12,960 base combinations + ENF-MIN override handling.

### Context Dimensions EN-405 Must Evaluate at Session Start

For session context injection, EN-405 should evaluate (or allow the user/orchestrator to specify):

1. **CRIT** -- Assess based on artifact scope: governance files = auto-C3+; new ADRs = C3; routine code = C1; new features = C2.
2. **PLAT** -- Detect automatically: check for Claude Code hooks availability.
3. **TOK** -- Track token consumption; inject context rot warnings at 20K+ tokens.
4. **TGT** -- Infer from file paths or user task description.
5. **PH** -- Infer from task activity (research = EXPLORE; design = DESIGN; coding = IMPL; review = VALID; bug fix = MAINT).
6. **MAT** -- Infer from artifact state: new file = DRAFT; under review = REVIEW; committed/baselined = BASE.
7. **TEAM** -- Detect: single agent vs. orchestration context.
8. **ENF** -- Derive from PLAT; override to MIN if environment is degraded.

**Source:** EN-303 TASK-001, Taxonomy Summary Table (lines 369-378); TASK-004 Input Schema (lines 79-88).

---

## Per-Criticality Strategy Sets

The decision tree (TASK-004) defines base strategy sets per criticality level when TOK = FULL and PLAT = CC (full capability):

### C1: Routine (Quality Layer L0/L1)

| Category | Strategies | Token Budget |
|----------|-----------|-------------|
| **Required** | S-010 (Self-Refine) | 2,000 |
| **Optional** | S-003 (Steelman), S-014 (LLM-as-Judge) | +3,600 |
| **Total** | 1-3 strategies | 2,000 - 5,600 |

**Quality Target:** ~0.60 to ~0.80. Phase modifier: PH-EXPLORE uses S-010 only; PH-VALID uses S-014 only.

### C2: Significant (Quality Layer L2 -- Target Operating Layer)

| Category | Strategies | Token Budget |
|----------|-----------|-------------|
| **Required** | S-007 (Constitutional AI), S-002 (Devil's Advocate), S-014 (LLM-as-Judge) | 14,600 |
| **Recommended** | S-003 (Steelman), S-010 (Self-Refine) | +3,600 |
| **Total** | 3-5 strategies | 14,600 - 18,200 |

**Quality Target:** ~0.80 to ~0.92+. Phase modifier: PH-EXPLORE downgrades to C1 (unless auto-escalated via PR-001). TEAM-SINGLE replaces S-002 with S-010 (self-DA is weak).

### C3: Major (Quality Layer L3 -- Deep Review)

| Category | Strategies | Token Budget |
|----------|-----------|-------------|
| **Required** | S-007, S-002, S-014, S-004 (Pre-Mortem), S-012 (FMEA), S-013 (Inversion) | 31,300 |
| **Recommended** | S-003, S-010, S-011 (CoVe) | +7,600 |
| **Total** | 6-9 strategies | 31,300 - 38,900 |

**Quality Target:** ~0.92 to ~0.96. TEAM-SINGLE not recommended; escalate to TEAM-MULTI or TEAM-HIL. Human involvement recommended (ESC-005).

### C4: Critical (Quality Layer L4 -- Tournament)

| Category | Strategies | Token Budget |
|----------|-----------|-------------|
| **Required** | ALL 10 strategies | ~50,300 |

**Quality Target:** ~0.96+. TEAM-SINGLE not permitted. TEAM-HIL required. Human involvement mandatory (ESC-001).

**Source:** EN-303 TASK-004, Decision Tree Primary Path (lines 126-255); TASK-003, Decision Criticality Mapping per profile.

---

## Decision Tree for Strategy Selection

The decision tree uses criticality (CRIT) as the primary branch with three modifiers:

```
INPUT: 8 context dimensions
  |
  [Auto-Escalation Rules: AE-001 through AE-006]
  |
  PRIMARY BRANCH: CRIT (C1 / C2 / C3 / C4)
  |
  +-- MODIFIER 1: Token Budget (TOK-FULL / TOK-CONST / TOK-EXHAUST)
  |     -> Adapts strategy set for budget constraints
  |
  +-- MODIFIER 2: Platform (PLAT-CC / PLAT-CC-WIN / PLAT-GENERIC)
  |     -> Adapts delivery mechanism per strategy
  |
  +-- MODIFIER 3: Phase (PH-EXPLORE / PH-DESIGN / PH-IMPL / PH-VALID / PH-MAINT)
  |     -> Adjusts strategy emphasis
  |
  GATE CHECKS: Maturity (MAT) and Team (TEAM)
  |
  OUTPUT: Strategy set + delivery mechanisms + escalation flags
```

**Design Properties (all verified in TASK-004):**
- **Deterministic** -- Same inputs always produce same outputs
- **Complete** -- Every valid context combination produces a recommendation
- **O(1)** -- Fixed-depth traversal (max 4 levels: primary + 3 modifiers)
- **Traceable** -- Every recommendation traces to TASK-003 profiles and ADR-EPIC002-001

**Fallback Rule:** When in doubt, escalate to the next higher criticality level. Conservative escalation is always preferred over under-review.

**Source:** EN-303 TASK-004, Design Properties (lines 65-71); Fallback for Ambiguous Contexts (lines 397-424).

---

## Token Budget Constraints

### Per-Strategy Token Costs

| Token Tier | Strategies | Cost Range |
|------------|-----------|------------|
| Ultra-Low | S-003 (1,600), S-010 (2,000), S-014 (2,000), S-013 (2,100) | 1,600 - 2,100 |
| Low | S-002 (4,600), S-004 (5,600) | 4,600 - 5,600 |
| Medium | S-011 (6,000), S-001 (7,000), S-007 (8,000-16,000), S-012 (9,000) | 6,000 - 16,000 |

### Token-Constrained Adaptation (TOK-CONST: 5,000-20,000 tokens remaining)

| Criticality | Adapted Strategy Set | Token Cost |
|-------------|---------------------|------------|
| C1 | S-010 only | 2,000 |
| C2 | S-003 + S-014 + S-010 | 5,600 |
| C3 | S-003 + S-002 + S-014 + S-013 | 10,300 |
| C4 | S-003 + S-002 + S-013 + S-014 + S-007 (single-pass) | ~18,300 |

### Token-Exhausted Adaptation (TOK-EXHAUST: < 5,000 tokens remaining)

| Criticality | Adapted Strategy Set | Token Cost | Action |
|-------------|---------------------|------------|--------|
| C1 | S-010 only (or skip review) | 2,000 | Minimal self-check |
| C2 | S-003 + S-014 | 3,600 | **Below target quality** |
| C3 | S-014 scoring only | 2,000 | **MANDATORY human escalation (AE-006)** |
| C4 | **End session. Start fresh.** | 0 | **MANDATORY human review** |

### Cumulative Token Budget vs. Enforcement Envelope

The L1 enforcement envelope is ~12,476 tokens + ~600/session L2 = ~13,076 total. Key finding from TASK-003 verification:

- **C1 fits L1 envelope** (5,600 < 12,476)
- **C2 exceeds L1 envelope** (14,600 > 12,476) -- requires Process delivery for S-002 and S-014
- **C3/C4 require full enforcement stack** (31,300-50,300 far exceed L1 capacity)

### Context Rot Warning

When session token count exceeds 20K, L1-dependent strategy delivery degrades:

| Token Count | L1 Effectiveness (estimated) | L2-L5/Process |
|-------------|------------------------------|---------------|
| 0-20K | ~100% | ~100% |
| 20K-50K | ~60-80% | ~100% |
| 50K+ | ~40-60% | ~100% |

**EN-405 should inject context rot warnings at 20K+ tokens** recommending L2/L3/L5/Process delivery mechanisms and considering session restart for high-criticality reviews.

**Source:** EN-303 TASK-004, Token Budget Adaptation (lines 259-286); TASK-003, Cumulative Token Budget Verification (lines 1098-1123); TASK-001, Dimension 8 (lines 303-326).

---

## Strategy Pairings for Multi-Strategy Sessions

EN-303 TASK-003 catalogs all C(10,2) = 45 unique strategy pairs:

### Synergistic (SYN) Pairs -- 14

These pairs produce greater combined value than independent application. Sequencing matters.

| # | Pair | Sequencing | Primary Context |
|---|------|-----------|-----------------|
| 1 | S-003 + S-002 | S-003 first | **Canonical Jerry review protocol.** Steelman-then-DA ensures DA addresses strongest formulation. |
| 2 | S-003 + S-007 | S-003 first | Steelman-then-Constitutional: fair compliance evaluation. |
| 3 | S-003 + S-001 | S-003 first | Steelman-then-Red-Team: attack strongest defense. |
| 4 | S-007 + S-013 | S-013 first | Inversion-then-Constitutional: anti-pattern verification. |
| 5 | S-007 + S-014 | S-007 first | Constitutional-then-Judge: compliance + scoring. |
| 6 | S-007 + S-002 | S-007 first | Constitutional-then-DA: compliance then reasoning challenge. |
| 7 | S-013 + S-012 | Parallel | Inversion + FMEA: creative + systematic failure analysis. |
| 8 | S-013 + S-004 | Parallel | Inversion + Pre-Mortem: structural + narrative failure analysis. |
| 9 | S-013 + S-001 | S-013 first | Inversion-then-Red-Team: generate attack surface then exploit. |
| 10 | S-004 + S-012 | S-004 first | Pre-Mortem-then-FMEA: creative then systematic failure analysis. |
| 11 | S-001 + S-012 | S-012 first | FMEA-then-Red-Team: identify then exploit failure modes. |
| 12 | S-001 + S-007 | S-007 first | Constitutional-then-Red-Team: verify defenses then test under attack. |
| 13 | S-014 + S-010 | S-010 first | Self-Refine-then-Judge: improve then score. |
| 14 | S-003 + S-014 | S-003 first | Steelman-then-Judge: fair representation then scoring. |

### Tension (TEN) Pairs -- 2

These pairs have overlapping coverage or conflicting approaches. Require scope separation.

| # | Pair | Tension | Management |
|---|------|---------|------------|
| 1 | S-001 + S-002 | Both provide adversarial challenge via role assignment. Concurrent application to same narrow artifact is redundant. | **Scope separate:** S-002 for reasoning/decision quality (all C2+); S-001 for security/robustness (C3+ architecture/security). At C4, both applied to different aspects. |
| 2 | S-003 + S-010 | Both are "improvement-before-critique" strategies. Over-polishing before critical review risks delaying defect identification. | **Scope separate:** S-010 for self-authored work (creator iteration); S-003 for evaluating others' work (critic pre-step). Never apply both to same artifact in same pass. |

### Compatible (COM) Pairs -- 29

All remaining 29 pairs are compatible with no special sequencing or conflict management. They may be used together in any order.

**Pairing count verification:** 14 SYN + 2 TEN + 29 COM = 45 = C(10,2). Verified complete.

**Note:** ADR-EPIC002-001 originally claimed 3 TEN pairs. TASK-003 v1.1.0 analysis found that one claimed TEN pair was a restatement of another (S-001+S-002 double-counted). Corrected to 2 unique TEN pairs with COM adjusted to 29.

**Source:** EN-303 TASK-003, Consolidated Pairing Reference (lines 970-1040).

---

## ENF-MIN Handling for Degraded Environments

When enforcement is degraded to L1 only (ENF-MIN), strategy feasibility varies significantly:

### Per-Strategy Feasibility Under ENF-MIN

| Strategy | ENF-MIN Delivery | Feasibility | Substitute if Infeasible |
|----------|------------------|-------------|--------------------------|
| S-010 (Self-Refine) | L1 rule (self-review instruction) | **Feasible** -- most resilient strategy under ENF-MIN | N/A |
| S-003 (Steelman) | L1 rule (steelman instruction) | **Feasible** -- single-pass, ultra-low cost | N/A |
| S-013 (Inversion) | L1 rule (inversion prompt) | **Feasible** -- single-pass generative | N/A |
| S-014 (LLM-as-Judge) | L1 rule (rubric-based scoring) | **Feasible** -- advisory only, no Process gate enforcement | N/A |
| S-007 (Constitutional AI) | L1 rule (constitutional principles) | **Feasible** -- advisory only, no enforcement gating | N/A |
| S-002 (Devil's Advocate) | L1 rule (critic role assignment) | **Marginally feasible** -- requires TEAM-MULTI; advisory only | S-010 (self-review) |
| S-011 (Chain-of-Verification) | L1 rule (verification prompt) | **Marginally feasible** -- no context isolation guarantee | Human-directed verification |
| S-004 (Pre-Mortem) | None | **Infeasible** -- requires Process orchestration | S-013 (Inversion) as partial substitute |
| S-012 (FMEA) | None | **Infeasible** -- requires Process/L5 | S-013 (Inversion) as partial substitute |
| S-001 (Red Team) | None | **Infeasible** -- requires Process/L3 | Human-directed security review |

### ENF-MIN Adapted Strategy Sets by Criticality

| Criticality | ENF-MIN Strategy Set | Token Cost | Human Required? |
|-------------|---------------------|------------|-----------------|
| C1 | S-010 | 2,000 | No |
| C2 | S-010 + S-007 (advisory) + S-014 (advisory) | 12,000 | Recommended |
| C3 | S-010 + S-003 + S-013 + S-007 (advisory) + S-014 (advisory) | 15,700 | **Mandatory** (ENF-MIN-002) |
| C4 | **End session. Human review mandatory.** | 0 | **Mandatory** |

### ENF-MIN Override Rules

| Rule | Condition | Effect |
|------|-----------|--------|
| ENF-MIN-001 | ENF = MIN on any platform | Override default ENF derivation from PLAT. Treat delivery mechanisms as L1 only. |
| ENF-MIN-002 | ENF = MIN AND CRIT >= C3 | Add mandatory human escalation flag. |
| ENF-MIN-003 | ENF = MIN | Apply PLAT-GENERIC portable stack treatment for all delivery lookups. |
| ENF-MIN-004 | ENF = MIN | Flag infeasible strategies per feasibility table above. |

**Source:** EN-303 TASK-004, ENF-MIN Adaptation (lines 318-343); TASK-003, per-profile ENF-MIN handling paragraphs.

---

## Defense-in-Depth Compensation Chain

Each enforcement layer compensates for the failure of the layer above. The following table maps each layer failure to the adversarial strategies that serve as compensating controls:

| Layer Failure | Failure Mode | Compensating Adversarial Strategies | Compensation Mechanism |
|---------------|-------------|-------------------------------------|----------------------|
| **L1 fails** (context rot) | Rules forgotten/deprioritized after ~20K tokens | S-010 (via L2 reinforcement), S-007 (via L2 per-prompt injection) | L2 re-injects critical rules every prompt, compensating for L1 context rot. |
| **L2 fails** (reinforcement not triggered) | V-024 per-prompt reinforcement fails or misconfigured | S-007 (via L3 pre-action gate), S-014 (via L3 pre-commit scoring) | L3 hooks trigger constitutional check and quality scoring before tool operations. |
| **L3 fails** (pre-action hook error, fail-open) | V-001 PreToolUse hook fails or is bypassed | S-014 (via L4 post-action validation), S-011 (via L4 post-output verification), S-010 (via L4 self-review) | L4 hooks catch violations after execution that L3 should have blocked before. |
| **L4 fails** (post-action validation skipped) | V-002 PostToolUse hook fails | S-007 (via L5 architecture tests), S-012 (via L5 FMEA checklist verification) | L5 CI/pre-commit hooks verify compliance deterministically at commit time. |
| **L5 fails** (CI bypass, `--no-verify`) | Pre-commit or CI pipeline bypassed by user | S-002 (via Process gate), S-001 (via Process security review), S-014 (via Process quality gate V-057) | Process gates require review evidence before task closure. V-057 requires S-014 score >= threshold. |
| **Process fails** (user overrides gates) | User exercises P-020 authority to override | **No adversarial compensation available.** P-020 is a constitutional principle. | Residual governance risk accepted per P-020. Audit trail records override. |

### ENF-MIN Compensation Summary

Under ENF-MIN (L1 only), the compensation chain is severely degraded:
- Only L1 is available; L2 through Process are all unavailable
- No compensation layers exist for L1 failure
- **Feasible strategies:** S-010, S-003, S-013, S-014 (advisory), S-007 (advisory)
- **Infeasible strategies:** S-004, S-012, S-001 (all require Process layer)
- **Marginally feasible:** S-002 (requires TEAM-MULTI), S-011 (advisory only)
- **Mandatory action:** Human escalation for C3+ artifacts under ENF-MIN

**Source:** EN-303 TASK-003, Defense-in-Depth Compensation Chain (lines 1071-1095).

---

## Enforcement Layer Delivery Mapping

How each strategy maps to enforcement layers for delivery:

| Strategy | L1 (Static Context) | L2 (Per-Prompt) | L3 (Pre-Action) | L4 (Post-Action) | L5 (Post-Hoc) | Process |
|----------|---------------------|------------------|------------------|-------------------|----------------|---------|
| S-010 | Rule: self-review instruction | Reinforcement via V-024 | -- | V-002 hook triggers self-review | -- | -- |
| S-003 | Rule: steelman instruction | Key reminder via V-024 | -- | -- | -- | Critic workflow mandate |
| S-013 | Rule: inversion prompt | -- | -- | -- | Anti-pattern checklist in CI | Design review mandate |
| S-007 | Rules: constitutional principles | Key principles via V-024 | V-001 hook: pre-write check | -- | Architecture tests | Review workflow mandate |
| S-002 | Rule: critic agent role | -- | -- | -- | -- | Critic workflow step |
| S-004 | -- | -- | -- | -- | -- | Design review gate (C3+) |
| S-012 | -- | -- | -- | -- | FMEA checklist in CI | Risk analysis step |
| S-011 | -- | -- | -- | V-002 hook: verification | -- | Verification workflow step |
| S-014 | Rule: rubric dimensions | Quality target via V-024 | V-001 hook: pre-commit scoring | V-002 hook: post-write scoring | Quality score in CI | V-057 quality gate |
| S-001 | -- | -- | V-001 hook: security-tagged files | -- | -- | Security review gate |

**Context Rot Vulnerability:**
- L1: VULNERABLE (degrades after ~20K tokens)
- L2: IMMUNE (fresh injection each prompt)
- L3/L5/Process: IMMUNE (external mechanisms)
- L4: MIXED (hook is immune but agent critique may degrade)

**Source:** EN-303 TASK-003, per-profile Enforcement Layer Mapping tables; TASK-004, Enforcement Layer Integration (lines 427-480).

---

## Creator-Critic-Revision Cycle Integration

The decision tree supports the creator-critic-revision cycle (FR-009) with per-iteration strategy assignments:

### Standard 3-Iteration Cycle

| Iteration | Role | C1 Strategies | C2 Strategies | C3 Strategies | C4 Strategies |
|-----------|------|--------------|--------------|--------------|--------------|
| **1: Create** | Creator produces with self-review | S-010 | S-010 | S-010 | S-010 |
| **2: Critique** | Critic reviews adversarially | S-014 | S-003 + S-002 + S-007 + S-014 | S-003 + S-002 + S-007 + S-004 + S-012 + S-013 + S-014 | All 10 strategies |
| **3: Revise** | Creator revises; Judge scores | S-010 + S-014 | S-010 + S-014 | S-010 + S-014 + S-011 | S-010 + S-014 + S-011 |

### Extended Cycle (C3-C4, if quality gate not met)

| Iteration | Trigger | Strategies |
|-----------|---------|-----------|
| **4: Re-Critique** | S-014 score < 0.92 after iteration 3 | Repeat iteration 2 strategies |
| **5: Final Revision** | Score still < 0.92 after iteration 4 | S-010 + S-014 |
| **6: Human Escalation** | Score < 0.92 after iteration 5 | Human review per P-020 |

**Key Guidance for EN-405:** Session context injection should make the current iteration number and expected strategies explicit so agents know their role and which strategies to apply.

**Source:** EN-303 TASK-004, Creator-Critic-Revision Cycle Mapping (lines 346-372).

---

## Auto-Escalation Rules

These rules fire BEFORE decision tree traversal and may override the initial criticality determination:

| Rule | Condition | Effect | Source |
|------|-----------|--------|--------|
| **AE-001** | Artifact modifies `docs/governance/JERRY_CONSTITUTION.md` | Escalate to C3 minimum | FR-011 |
| **AE-002** | Artifact modifies any file in `.claude/rules/` | Escalate to C3 minimum | FR-011 |
| **AE-003** | Artifact is a new or modified ADR | Escalate to C3 minimum | TASK-001 |
| **AE-004** | Artifact modifies existing baselined ADR | Escalate to C4 | TASK-001 |
| **AE-005** | Artifact modifies security-relevant code (auth, crypto, access control) | Escalate to C3 minimum | TASK-001 |
| **AE-006** | Token budget is EXHAUST and criticality is C3+ | Add mandatory human escalation flag | Escalation Decision Logic |

**Precedence Rule (PR-001):** Auto-escalation overrides phase downgrade. If criticality was elevated by AE-001 through AE-005, phase modifiers SHALL NOT reduce the criticality below the auto-escalated level. Rationale: auto-escalation encodes hard governance constraints (FR-011, JERRY_CONSTITUTION); phase modifiers encode soft workflow optimization.

**Source:** EN-303 TASK-004, Auto-Escalation Rules (lines 92-121).

---

## Platform Adaptation

### Delivery Mechanism Shift for Non-Claude-Code Platforms

| Strategy | Full Stack (PLAT-CC) | Portable Stack (PLAT-GENERIC) |
|----------|---------------------|-------------------------------|
| S-010 | L1 + L2 + L4 hook | L1 rule only (subject to context rot) |
| S-003 | L1 + L2 | L1 rule only |
| S-013 | L1 + Process | L1 + Process (no change) |
| S-007 | L1 + L3 hook + L5 tests | L1 + L5 tests + Process gate |
| S-002 | Process gate | Process gate (no change) |
| S-004 | Process gate | Process gate (no change) |
| S-012 | Process + L5 CI | Process + L5 CI (no change) |
| S-011 | Process + L4 hook | Process only |
| S-014 | Process + L3/L4 hooks | Process only |
| S-001 | Process + L3 hook | Process only |

### Enforcement Level Summary

| Platform | Enforcement Level | Available Layers | Key Loss |
|----------|------------------|-----------------|----------|
| PLAT-CC | HIGH | L1, L2, L3, L4, L5, Process | None |
| PLAT-CC-WIN | HIGH (WSL caveats) | L1, L2, L3, L4, L5, Process | Potential WSL friction |
| PLAT-GENERIC | MODERATE | L1, L5, Process | L3 real-time blocking, L4 auto-validation, L2 per-prompt reinforcement |

**Key constraint:** All 10 strategies have portable delivery at MODERATE enforcement level. No strategy is inoperable on PLAT-GENERIC. The loss is in enforcement automation, not strategy capability.

**Source:** EN-303 TASK-004, Platform Adaptation (lines 289-316).

---

## Integration Guidance for EN-405

Based on the EN-303 findings, the following recommendations are specific to EN-405 (Session Context Enforcement):

### What to Inject at Session Start

1. **Quality gate threshold** -- >= 0.92 scoring target (S-014 backbone).
2. **Active criticality level** -- Determined by auto-escalation rules and artifact context.
3. **Strategy set for current criticality** -- From the per-criticality tables above.
4. **Creator-critic-revision iteration** -- Current iteration number and expected strategies.
5. **Context rot status** -- Token consumption tracking with warnings at 20K+.
6. **Platform/enforcement context** -- Detected PLAT and derived ENF values.
7. **Pairing guidance** -- Key SYN pairs relevant to current criticality (especially SYN #1: S-003 + S-002).

### Session Context Injection Per Criticality

| Criticality | Key Session Injections |
|-------------|----------------------|
| C1 | "Apply self-review (S-010). Optional quality scoring (S-014) if deliverable expected." |
| C2 | "Apply Steelman (S-003) before critique. Constitutional AI check (S-007) required. Devil's Advocate (S-002) required. Quality score >= 0.92 required (S-014)." |
| C3 | "Deep review active. 6 strategies required: S-007, S-002, S-014, S-004, S-012, S-013. Quality score >= 0.92. Consider human involvement." |
| C4 | "Tournament mode. All 10 strategies required. Human involvement mandatory. Quality score >= 0.96 target." |

### ENF-MIN Session Injection

When ENF-MIN is detected at session start:

1. Flag the degraded state explicitly: "WARNING: Enforcement degraded to L1 only."
2. Inject the ENF-MIN adapted strategy set for the current criticality.
3. Flag infeasible strategies (S-004, S-012, S-001) and their substitutes.
4. Inject mandatory human escalation flag for C3+.
5. Inject context rot awareness: L1-only delivery is vulnerable to degradation.

### Enforcement Gaps That Session Context Must Address

Per TASK-003 Enforcement Gap Analysis, adversarial strategies are the sole defense for:

| Gap | Session Context Response |
|-----|------------------------|
| **Semantic quality** (AST checks structure, not meaning) | Inject S-002, S-003, S-007, S-014 as mandatory for C2+ |
| **Context rot prevention** | Inject token tracking + 20K warning + session restart recommendation |
| **Novel violation types** (AST rules are pre-defined) | Inject S-001, S-013, S-004 for C3+ (exploratory strategies) |
| **Social engineering bypass** (users can disable hooks) | Inject Process gates (V-057, V-060) as final defense; flag if bypassed |

**Source:** EN-303 TASK-003, Enforcement Gap Analysis (lines 1044-1054); EN-405 enabler specification.

---

## Quality Gate and Scoring

### Quality Layer to Score Range Mapping

| Quality Layer | Criticality | Strategies Applied | Expected Score Range |
|---------------|------------|-------------------|--------------------|
| L0: Self-Check | C1 (always-on) | S-010 | ~0.60 to ~0.75 |
| L1: Light Review | C1 | S-003 + S-010 + S-014 | ~0.75 to ~0.85 |
| L2: Standard Critic | C2 | S-007 + S-002 + S-014 | ~0.85 to ~0.92+ |
| L3: Deep Review | C3 | L2 + S-004 + S-012 + S-013 | ~0.92 to ~0.96 |
| L4: Tournament | C4 | L3 + S-001 + S-011 | ~0.96+ |

**C1/C2 Transition Zone:** Quality scores in the 0.75-0.85 range indicate the artifact may need C2 review rather than C1. EN-405 should flag this transition zone.

### S-014 (LLM-as-Judge) as Scoring Backbone

S-014 is the only strategy spanning all criticality levels (C1 through C4). It provides:
- Structured rubric-based scoring (0.00-1.00)
- Dimension-level breakdowns (completeness, consistency, evidence quality, rigor, actionability, traceability)
- Pass/fail determination against >= 0.92 threshold
- Ultra-Low token cost (2,000) making it feasible even under budget exhaustion

**Known limitation:** Leniency bias (R-014-FN). Must be managed through rubric calibration.

**Source:** EN-303 TASK-003, S-014 profile (lines 79-173); TASK-004, Quality Target ranges per criticality.

---

## Source Artifact Traceability

| Artifact | Document ID | Version | Quality Score | Location |
|----------|------------|---------|--------------|----------|
| EN-303 TASK-001 (Context Taxonomy) | FEAT-004:EN-303:TASK-001 | 1.1.0 | 0.925 | `FEAT-004-adversarial-strategy-research/EN-303-situational-applicability-mapping/TASK-001-context-taxonomy.md` |
| EN-303 TASK-002 (Requirements) | FEAT-004:EN-303:TASK-002 | 1.1.0 | 0.917 | `FEAT-004-adversarial-strategy-research/EN-303-situational-applicability-mapping/TASK-002-requirements.md` |
| EN-303 TASK-003 (Strategy Profiles) | FEAT-004:EN-303:TASK-003 | 1.1.0 | 0.909 | `FEAT-004-adversarial-strategy-research/EN-303-situational-applicability-mapping/TASK-003-strategy-profiles.md` |
| EN-303 TASK-004 (Decision Tree) | FEAT-004:EN-303:TASK-004 | 1.1.0 | 0.926 | `FEAT-004-adversarial-strategy-research/EN-303-situational-applicability-mapping/TASK-004-decision-tree.md` |
| EN-303 Critique Iteration 2 | FEAT-004:EN-303:TASK-007-ITER-2 | 1.0.0 | Overall: 0.928 PASS | `FEAT-004-adversarial-strategy-research/EN-303-situational-applicability-mapping/TASK-007-critique-iteration-2.md` |
| ADR-EPIC002-001 | FEAT-004:EN-302:TASK-005 | ACCEPTED | 0.935 | `FEAT-004-adversarial-strategy-research/EN-302-strategy-selection-framework/TASK-005-selection-ADR.md` |
| Barrier-1 ADV-to-ENF Handoff | EPIC-002:ORCH:BARRIER-1:ADV-TO-ENF | Complete | N/A | `orchestration/epic002-crosspoll-20260213-001/cross-pollination/barrier-1/adv-to-enf/barrier-1-adv-to-enf-handoff.md` |
| EN-405 Enabler Specification | EN-405 | 1.0.0 | Pending | `FEAT-005-enforcement-mechanisms/EN-405-session-context-enforcement/EN-405-session-context-enforcement.md` |

All paths are relative to `projects/PROJ-001-oss-release/work/EPIC-002-quality-enforcement/`.

### Quality Assurance

- **EN-303 overall quality score:** 0.928 (PASS, >= 0.92 threshold)
- **Per-artifact scores:** TASK-001: 0.925, TASK-002: 0.917, TASK-003: 0.909, TASK-004: 0.926
- **Adversarial review:** 2 iterations. Iteration 1: 0.843 (FAIL). Iteration 2: 0.928 (PASS).
- **All blocking findings (3), major findings (5), and minor findings (4) resolved.** No mandatory remediation actions remain.
- **Residual advisory notes:** Machine-parseable format deferred to EN-304; quality improvement ranges are structured estimates pending empirical validation; COM pair table has minor formatting artifact.

---

*Document ID: EPIC-002:ORCH:BARRIER-2:ADV-TO-ENF*
*Created: 2026-02-14*
*Author: ps-synthesizer (orchestration worker)*
*Source Pipeline: ADV (FEAT-004)*
*Target Pipeline: ENF (FEAT-005)*
*Barrier: Barrier 2*
