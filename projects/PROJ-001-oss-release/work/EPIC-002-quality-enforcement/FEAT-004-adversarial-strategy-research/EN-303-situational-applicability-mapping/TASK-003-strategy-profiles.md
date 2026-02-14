# TASK-003: Per-Strategy Applicability Profiles

<!--
DOCUMENT-ID: FEAT-004:EN-303:TASK-003
VERSION: 1.0.0
AGENT: ps-architect
DATE: 2026-02-13
STATUS: Complete
PARENT: EN-303 (Situational Applicability Mapping)
FEATURE: FEAT-004 (Adversarial Strategy Research & Skill Enhancement)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
ACTIVITY: DESIGN
REQUIREMENTS: FR-003, FR-004, FR-005, FR-006, FR-007, FR-009, NFR-002, NFR-003, NFR-004
TARGET-ACS: 2, 3, 10, 11, 12
INPUT: TASK-001 (context taxonomy), ADR-EPIC002-001, EN-302 TASK-004 (scoring/synergy), Barrier-1 ENF-to-ADV
-->

> **Version:** 1.0.0
> **Agent:** ps-architect
> **Quality Target:** >= 0.92
> **Purpose:** For each of the 10 selected strategies, define a comprehensive applicability profile: when to use, when to avoid, complementary and tension pairings, preconditions, expected outcomes, token budget, enforcement layer mapping, platform considerations, and decision criticality mapping

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this document delivers and how it relates to the decision tree |
| [Profile Template](#profile-template) | Structure used for each strategy profile |
| [S-014: LLM-as-Judge](#s-014-llm-as-judge) | Applicability profile for the primary evaluation strategy |
| [S-003: Steelman Technique](#s-003-steelman-technique) | Applicability profile for the fairness enabler |
| [S-013: Inversion Technique](#s-013-inversion-technique) | Applicability profile for the generative anti-pattern strategy |
| [S-007: Constitutional AI Critique](#s-007-constitutional-ai-critique) | Applicability profile for the principle-based evaluation strategy |
| [S-002: Devil's Advocate](#s-002-devils-advocate) | Applicability profile for the core adversarial challenge strategy |
| [S-004: Pre-Mortem Analysis](#s-004-pre-mortem-analysis) | Applicability profile for the temporal reframing strategy |
| [S-010: Self-Refine](#s-010-self-refine) | Applicability profile for the self-improvement baseline |
| [S-012: FMEA](#s-012-fmea) | Applicability profile for the systematic failure analysis strategy |
| [S-011: Chain-of-Verification](#s-011-chain-of-verification) | Applicability profile for the factual verification strategy |
| [S-001: Red Team Analysis](#s-001-red-team-analysis) | Applicability profile for the adversary simulation strategy |
| [Consolidated Pairing Reference](#consolidated-pairing-reference) | Complete SYN, COM, and TEN pair catalog |
| [Enforcement Gap Analysis](#enforcement-gap-analysis) | Where adversarial strategies are the sole defense |
| [Excluded Strategy Coverage Gaps](#excluded-strategy-coverage-gaps) | What the 5 excluded strategies would have provided |
| [Traceability](#traceability) | Requirements and acceptance criteria coverage |
| [References](#references) | Source citations |

---

## Summary

This document provides the complete applicability profile for each of the 10 selected adversarial strategies from ADR-EPIC002-001. Each profile maps the strategy to the 8-dimension context taxonomy (TASK-001), documenting when to use, when to avoid, complementary pairings, tension pairings, preconditions, expected outcomes, token budget, enforcement layer mapping, platform portability, and decision criticality mapping.

These profiles are the input to the strategy selection decision tree (TASK-004). The decision tree operationalizes the guidance in these profiles into a deterministic selection algorithm.

---

## Profile Template

Each strategy profile follows this structure:

| Section | Content |
|---------|---------|
| **When to Use** | Context conditions (using TASK-001 dimension codes) that favor this strategy |
| **When to Avoid** | Context conditions that contraindicate this strategy, with rationale |
| **Complementary Pairings** | SYN and COM pairs with sequencing guidance |
| **Tension Pairings** | TEN pairs with conflict management guidance |
| **Preconditions** | What must be true before applying |
| **Expected Outcomes** | Output type, defect categories detected, quality improvement range |
| **Token Budget** | Per-invocation cost, token tier |
| **Enforcement Layer Mapping** | Primary delivery, portable fallback, enhanced delivery (with hooks) |
| **Platform Portability** | Classification and degradation notes |
| **Decision Criticality Mapping** | C1-C4 applicability with rationale |

---

## S-014: LLM-as-Judge

**Rank:** 1 | **Score:** 4.40 | **Family:** Iterative Self-Correction | **ADR Ref:** ADR-EPIC002-001

### When to Use

| Dimension | Favorable Values | Rationale |
|-----------|-----------------|-----------|
| Target Type | All (TGT-CODE, TGT-ARCH, TGT-REQ, TGT-RES, TGT-DEC, TGT-PROC) | Universal evaluation strategy; rubric can be adapted to any artifact type |
| Phase | PH-DESIGN, PH-IMPL, PH-VALID, PH-MAINT | Most valuable in validation phase; applicable whenever a scoring rubric exists |
| Criticality | CRIT-C1 through CRIT-C4 | Present at all quality layers (L0-L4); the only strategy spanning all criticality levels |
| Maturity | All (MAT-DRAFT through MAT-BASE) | Scoring is appropriate at any maturity; rubric dimensions adjust by maturity |
| Team | All (TEAM-SINGLE, TEAM-MULTI, TEAM-HIL) | Single-agent capable; human-in-loop enables calibration |
| Token Budget | TOK-FULL, TOK-CONST | Ultra-low cost (2,000 tokens) makes it feasible even under budget constraints |

### When to Avoid

| Condition | Rationale |
|-----------|-----------|
| PH-EXPLORE (early exploration) | No rubric exists yet to evaluate against; scoring is premature and may anchor subsequent work to arbitrary quality dimensions |
| TOK-EXHAUST with C1 context | Even at 2,000 tokens, if budget is truly exhausted and criticality is low, skip evaluation entirely |
| No calibrated rubric available | Uncalibrated scores are worse than no scores -- they create false confidence (TASK-002: R-014-FN leniency bias) |

### Complementary Pairings

| Partner | Type | Sequencing | Rationale |
|---------|------|-----------|-----------|
| S-007 | SYN | S-007 first, then S-014 scores | Constitutional AI evaluates compliance; LLM-as-Judge provides the numerical quality score. Together they produce both qualitative evaluation and quantitative score. |
| S-010 | COM | S-010 first, then S-014 scores the refined output | Self-Refine improves quality; Judge measures the improvement. Enables quality tracking across iterations. |
| S-003 | COM | S-003 first, then S-014 scores steelmanned argument | Steelman ensures fair representation; Judge evaluates quality. Prevents Judge from penalizing arguments that were poorly constructed rather than genuinely flawed. |
| S-013 | COM | S-013 generates anti-patterns, S-014 scores against them | Inversion creates quality criteria; Judge evaluates against those criteria. Synergistic criteria generation + evaluation. |

### Tension Pairings

None. S-014 has zero TEN or CON pairs within the selected 10.

### Preconditions

1. A scoring rubric must be defined (either generic quality rubric or artifact-specific rubric)
2. Rubric dimensions must be calibrated against human-scored reference sets (to mitigate R-014-FN leniency bias)
3. The artifact must be sufficiently complete to evaluate (not a stub or placeholder)

### Expected Outcomes

| Output | Description |
|--------|------------|
| **Numerical quality score** | 0.00-1.00 score on defined rubric dimensions (e.g., completeness, consistency, evidence quality, rigor, actionability, traceability) |
| **Dimension-level scores** | Per-dimension breakdown enabling targeted improvement |
| **Qualitative rationale** | Text explanation for each score, identifying specific strengths and weaknesses |
| **Pass/fail determination** | Whether the artifact meets the >= 0.92 quality gate threshold |

**Defect categories detected:** Quality shortfalls across rubric dimensions, inconsistencies, missing content, weak argumentation, insufficient evidence.

**Expected quality improvement:** Enables +0.05 to +0.15 improvement per creator-critic-revision cycle by providing specific, measurable feedback.

### Token Budget

- **Per-invocation:** ~2,000 tokens
- **Token tier:** Ultra-Low
- **Budget impact:** Negligible. Can be used in every review cycle without material budget impact.

### Enforcement Layer Mapping

| Layer | Delivery Mechanism | Context Rot Vulnerability |
|-------|-------------------|--------------------------|
| L1 (Static Context) | Rubric dimensions encoded in `.claude/rules/` | VULNERABLE -- rubric may be ignored after ~20K tokens |
| L2 (Per-Prompt) | Quality target (>= 0.92) reinforced via V-024 | IMMUNE |
| L3 (Pre-Action) | V-001 hook triggers Judge scoring before commit operations | IMMUNE |
| L4 (Post-Action) | V-002 hook triggers Judge scoring after file writes | MIXED |
| L5 (Post-Hoc) | Quality score verification in CI pipeline | IMMUNE |
| Process | V-057 Quality Gate requires Judge score >= threshold before closure | IMMUNE |

**Primary delivery:** Process (V-057 quality gate)
**Portable fallback:** L1 rubric + Process gate (no hooks needed)
**Enhanced delivery:** L3/L4 hooks for automatic pre/post scoring

### Platform Portability

**Classification:** Fully portable (degraded without hooks)
- PLAT-CC: Full capability (hooks enable automatic scoring triggers)
- PLAT-GENERIC: Process-triggered scoring (human or orchestrator manually invokes Judge). Rubric and scoring are inherently portable.
- Degradation: Loss of automatic trigger (L3/L4 hooks), but scoring capability itself is platform-independent.

### Decision Criticality Mapping

| Level | Required? | Role in Quality Layer | Rationale |
|-------|-----------|----------------------|-----------|
| C1 | Optional | L1 (Light Review) | Quick quality check; often sufficient alone for routine work |
| C2 | **Required** | L2 (Standard Critic) | Primary quality gate mechanism at the target operating layer |
| C3 | **Required** | L3 (Deep Review) | Quality scoring after deep review to confirm threshold met |
| C4 | **Required** | L4 (Tournament) | Final quality determination after maximum-intensity review |

---

## S-003: Steelman Technique

**Rank:** 2 | **Score:** 4.30 | **Family:** Dialectical Synthesis | **ADR Ref:** ADR-EPIC002-001

### When to Use

| Dimension | Favorable Values | Rationale |
|-----------|-----------------|-----------|
| Target Type | TGT-ARCH, TGT-DEC, TGT-RES, TGT-REQ | Most valuable for artifacts containing arguments, decisions, or analyses that need fair evaluation |
| Phase | PH-DESIGN, PH-IMPL | Best applied before adversarial critique to ensure fair engagement with the work |
| Criticality | CRIT-C1 through CRIT-C3 | Enabler strategy; enhances subsequent critique quality. C4 deploys all strategies, so included by default. |
| Team | All | Single-agent capable (embedded in prompt phase) |
| Token Budget | TOK-FULL, TOK-CONST, TOK-EXHAUST | Ultra-low cost (1,600 tokens) -- feasible even in exhausted budgets |

### When to Avoid

| Condition | Rationale |
|-----------|-----------|
| TGT-CODE (pure code review) | Code does not contain "arguments" to steelman; constitutional compliance check (S-007) is more appropriate |
| PH-EXPLORE (early exploration) | No formed argument to steelman yet |
| Standalone application (without follow-up critique) | Steelman without subsequent adversarial challenge produces only charitable reconstruction -- no defect detection |

### Complementary Pairings

| Partner | Type | Sequencing | Rationale |
|---------|------|-----------|-----------|
| S-002 | **SYN** | S-003 first, then S-002 | **Primary synergy pair.** Steelman-then-DA is the canonical Jerry review protocol. Steelman ensures DA addresses the strongest version of the argument, not a strawman. (EN-302 TASK-004 composition matrix) |
| S-007 | **SYN** | S-003 first, then S-007 | Steelman ensures constitutional evaluation engages with the best interpretation of the work. Prevents constitutional check from failing on presentation quality rather than substance. |
| S-001 | **SYN** | S-003 first, then S-001 | Steelman ensures Red Team attacks the strongest version of the defense, producing more meaningful vulnerabilities. |
| S-014 | COM | S-003 first, then S-014 | Steelmanned work receives fairer quality scoring. |

### Tension Pairings

| Partner | Type | Tension | Management |
|---------|------|---------|------------|
| S-010 | **TEN** | Both are "improvement-before-critique" strategies. S-003 strengthens another's argument; S-010 improves own output. Applying both may over-polish before critical review. | Scope separate: use S-010 for self-review of own drafts; use S-003 before reviewing others' work. Do not apply both to the same artifact in the same review pass. |

### Preconditions

1. Artifact must contain arguments, decisions, or analyses (not raw data or pure code)
2. A subsequent adversarial strategy must follow (S-003 alone does not detect defects)
3. The artifact must be sufficiently formed to reconstruct (not a stub)

### Expected Outcomes

| Output | Description |
|--------|------------|
| **Strengthened argument** | The work's argument reconstructed in its strongest possible form |
| **Identified assumptions** | Explicit listing of assumptions the argument depends on |
| **Clarified logic chain** | The reasoning path made explicit for subsequent critique |

**Defect categories detected:** None directly. Enables detection of deeper defects by subsequent strategies (prevents false positives from attacking weak formulations).

**Expected quality improvement:** Indirect -- improves subsequent strategy effectiveness by +0.05 to +0.10.

### Token Budget

- **Per-invocation:** ~1,600 tokens
- **Token tier:** Ultra-Low (lowest in catalog)
- **Budget impact:** Negligible.

### Enforcement Layer Mapping

| Layer | Delivery Mechanism | Context Rot Vulnerability |
|-------|-------------------|--------------------------|
| L1 (Static Context) | Steelman instruction encoded in critic agent rules | VULNERABLE |
| L2 (Per-Prompt) | Key steelman reminder in V-024 content | IMMUNE |
| Process | Critic workflow mandates steelman phase before adversarial challenge | IMMUNE |

**Primary delivery:** L1 rule + Process mandate
**Portable fallback:** L1 rule (steelman instruction in `.claude/rules/`) + Process gate
**Enhanced delivery:** L2 reinforcement adds context-rot immunity

### Platform Portability

**Classification:** Fully portable
- All delivery mechanisms (L1, L2, Process) are platform-independent
- No hook dependency whatsoever
- Identical capability across PLAT-CC, PLAT-CC-WIN, PLAT-GENERIC

### Decision Criticality Mapping

| Level | Required? | Role | Rationale |
|-------|-----------|------|-----------|
| C1 | Optional | L1 precondition for S-014 scoring | Lightweight addition that improves fairness |
| C2 | Recommended | L2 precondition for S-002/S-007 critique | Standard fairness practice at target operating layer |
| C3 | **Required** | L3 mandatory before deep adversarial challenge | Prevents wasted effort on strawman critique |
| C4 | **Required** | L4 foundation for all adversarial strategies | Essential at maximum intensity |

---

## S-013: Inversion Technique

**Rank:** 3 | **Score:** 4.25 | **Family:** Structured Decomposition | **ADR Ref:** ADR-EPIC002-001

### When to Use

| Dimension | Favorable Values | Rationale |
|-----------|-----------------|-----------|
| Target Type | All -- especially TGT-ARCH, TGT-PROC, TGT-DEC | Anti-pattern generation is universally valuable; most impactful for design and process artifacts |
| Phase | PH-EXPLORE, PH-DESIGN | Most valuable early when anti-pattern checklists can shape design. Generates reusable criteria. |
| Criticality | CRIT-C3, CRIT-C4 | Highest value at elevated criticality; anti-pattern checklists become verification criteria |
| Token Budget | TOK-FULL, TOK-CONST, TOK-EXHAUST | Ultra-low cost (2,100 tokens) |

### When to Avoid

| Condition | Rationale |
|-----------|-----------|
| PH-VALID, PH-MAINT (late phases) | Anti-pattern generation adds noise during validation; at this point, existing checklists should be used, not new ones generated |
| MAT-APPR or MAT-BASE (approved/baselined) | Generating new anti-patterns for approved work implies scope creep; use only if formal revision is underway |

### Complementary Pairings

| Partner | Type | Sequencing | Rationale |
|---------|------|-----------|-----------|
| S-007 | **SYN** | S-013 first, then S-007 evaluates against generated anti-patterns | Inversion generates "what would failure look like"; Constitutional AI verifies the artifact does not match those failure patterns. |
| S-012 | **SYN** | S-013 in parallel with S-012 | Inversion generates creative failure scenarios; FMEA provides systematic enumeration. Together they cover both creative and systematic failure analysis. |
| S-004 | **SYN** | S-013 and S-004 complement | Pre-Mortem imagines narrative failures; Inversion generates structural anti-patterns. Different angles on "how could this fail." |
| S-001 | **SYN** | S-013 first generates attack surface; S-001 exploits it | Inversion generates anti-patterns; Red Team uses them as attack vectors. |

### Tension Pairings

None. S-013 has zero TEN or CON pairs within the selected 10.

### Preconditions

1. The artifact must have a discernible purpose or success criteria (so inversion can produce meaningful failure criteria)
2. A consumer strategy must exist to use the anti-pattern output (S-007, S-012, S-001, or human reviewer)

### Expected Outcomes

| Output | Description |
|--------|------------|
| **Anti-pattern checklist** | Enumeration of failure modes, anti-patterns, and "how to guarantee this fails" scenarios |
| **Inverted success criteria** | The artifact's success criteria expressed as failure conditions |
| **Reusable verification criteria** | Anti-patterns persisted to `.jerry/data/` for consumption by other strategies and future reviews |

**Defect categories detected:** Design anti-patterns, unstated assumptions, failure modes not covered by positive requirements, blind spots in success criteria.

**Expected quality improvement:** +0.05 to +0.10 via enabling subsequent strategies with better criteria.

### Token Budget

- **Per-invocation:** ~2,100 tokens
- **Token tier:** Ultra-Low
- **Budget impact:** Negligible.

### Enforcement Layer Mapping

| Layer | Delivery Mechanism | Context Rot Vulnerability |
|-------|-------------------|--------------------------|
| L1 (Static Context) | Inversion prompt encoded as agent mode | VULNERABLE |
| L5 (Post-Hoc) | Anti-pattern checklists verified against artifact in CI | IMMUNE |
| Process | Anti-pattern generation mandated as step in design review workflow | IMMUNE |

**Primary delivery:** Process (mandated design review step)
**Portable fallback:** L1 prompt + Process gate
**Enhanced delivery:** None -- no hook benefit for single-pass generative strategy

### Platform Portability

**Classification:** Fully portable
- Single-pass generative prompt with no platform dependencies
- Anti-pattern output is plain text, universally parseable
- No hook dependency

### Decision Criticality Mapping

| Level | Required? | Role | Rationale |
|-------|-----------|------|-----------|
| C1 | Not recommended | N/A | Overkill for routine work |
| C2 | Optional | L2 criteria generation | Generates useful anti-patterns for standard reviews |
| C3 | **Required** | L3 failure criteria generation | Anti-pattern checklists are essential for deep review |
| C4 | **Required** | L4 comprehensive failure criteria | Maximum failure enumeration needed |

---

## S-007: Constitutional AI Critique

**Rank:** 4 | **Score:** 4.15 | **Family:** Iterative Self-Correction | **ADR Ref:** ADR-EPIC002-001

### When to Use

| Dimension | Favorable Values | Rationale |
|-----------|-----------------|-----------|
| Target Type | TGT-CODE (high), TGT-ARCH, TGT-REQ, TGT-DEC, TGT-PROC | Any artifact with codified standards to evaluate against. Code has the richest constitution (`.claude/rules/`). |
| Phase | PH-IMPL, PH-VALID, PH-MAINT | Most valuable when standards exist and compliance is expected |
| Criticality | CRIT-C2 through CRIT-C4 | Core strategy at the target operating layer (C2) and above |
| Token Budget | TOK-FULL, TOK-CONST | Medium cost (8,000-16,000); avoid in TOK-EXHAUST unless criticality demands it |

### When to Avoid

| Condition | Rationale |
|-----------|-----------|
| PH-EXPLORE (early exploration) | No constitution or standards defined yet to evaluate against |
| No `.claude/rules/` or equivalent standards | Constitutional AI requires codified principles; without them, the strategy has nothing to evaluate against |
| TOK-EXHAUST with C1 context | Medium token cost is unjustified for routine work in exhausted budgets |

### Complementary Pairings

| Partner | Type | Sequencing | Rationale |
|---------|------|-----------|-----------|
| S-003 | **SYN** | S-003 first | Steelman ensures constitutional evaluation engages with the best formulation |
| S-013 | **SYN** | S-013 generates anti-patterns, S-007 verifies non-match | Inversion provides additional criteria beyond the existing constitution |
| S-014 | **SYN** | S-007 evaluates, S-014 scores | Qualitative compliance evaluation + quantitative scoring |
| S-002 | **SYN** | S-007 first (structural compliance), then S-002 (argumentative challenge) | Constitutional check handles rule compliance; DA handles reasoning quality |

### Tension Pairings

None within the selected 10.

### Preconditions

1. Codified constitutional principles must exist (`.claude/rules/`, coding standards, architecture standards, etc.)
2. The artifact must be sufficiently complete to evaluate against principles (not a placeholder)
3. Constitutional principles must be relevant to the artifact type

### Expected Outcomes

| Output | Description |
|--------|------------|
| **Principle-by-principle compliance report** | Each constitutional principle evaluated with PASS/FAIL/PARTIAL |
| **Specific violation citations** | Exact locations where the artifact violates principles, with severity |
| **Remediation guidance** | Concrete suggestions for achieving compliance |

**Defect categories detected:** Standards violations, coding convention failures, architecture boundary violations, naming convention errors, documentation gaps.

**Expected quality improvement:** +0.10 to +0.20 per review cycle for artifacts with compliance issues.

### Token Budget

- **Per-invocation:** ~8,000-16,000 tokens (varies with number of constitutional principles and multi-pass depth)
- **Token tier:** Medium
- **Budget impact:** Significant. Budget-aware selection should use simplified single-pass in TOK-CONST.

### Enforcement Layer Mapping

| Layer | Delivery Mechanism | Context Rot Vulnerability |
|-------|-------------------|--------------------------|
| L1 (Static Context) | Constitutional principles in `.claude/rules/` | VULNERABLE -- principles may be forgotten after ~20K tokens |
| L2 (Per-Prompt) | Key principles reinforced via V-024 | IMMUNE |
| L3 (Pre-Action) | V-001 hook triggers constitutional check before file writes | IMMUNE |
| L5 (Post-Hoc) | Architecture tests verify structural principles | IMMUNE |
| Process | Review workflow mandates constitutional compliance check | IMMUNE |

**Primary delivery:** L1 rules (constitutional principles) + L3 hooks (automated trigger)
**Portable fallback:** L1 rules + L5 architecture tests + Process gate
**Enhanced delivery:** L3 hooks for real-time constitutional gating

### Platform Portability

**Classification:** Fully portable (degraded without hooks)
- PLAT-CC: Real-time gating via L3 hooks. Maximum enforcement.
- PLAT-GENERIC: Rule-based guidance (L1) + CI-based verification (L5) + Process gates. Loses real-time blocking but retains full compliance checking capability.
- Degradation: Loss of real-time blocking (L3); all violations still caught at L5/Process.

### Decision Criticality Mapping

| Level | Required? | Role | Rationale |
|-------|-----------|------|-----------|
| C1 | Not required | N/A | Token cost unjustified for routine work; L5 catches violations at commit |
| C2 | **Required** | L2 (Standard Critic) | Core strategy at target operating layer |
| C3 | **Required** | L3 (Deep Review) | Compliance is non-negotiable at high criticality |
| C4 | **Required** | L4 (Tournament) | Full multi-pass constitutional evaluation |

---

## S-002: Devil's Advocate

**Rank:** 5 | **Score:** 4.10 | **Family:** Role-Based Adversarialism | **ADR Ref:** ADR-EPIC002-001

### When to Use

| Dimension | Favorable Values | Rationale |
|-----------|-----------------|-----------|
| Target Type | TGT-ARCH, TGT-DEC, TGT-RES, TGT-REQ | Most valuable for artifacts containing conclusions, decisions, or recommendations that can be challenged |
| Phase | PH-DESIGN, PH-IMPL | Peak value during design when challenging assumptions has highest cost-avoidance multiplier |
| Criticality | CRIT-C2 through CRIT-C4 | Core adversarial challenge at the target operating layer and above |
| Team | TEAM-MULTI, TEAM-HIL | Most effective with a separate critic agent; limited as self-DA in single-agent mode |

### When to Avoid

| Condition | Rationale |
|-----------|-----------|
| PH-EXPLORE (early exploration) | Ideas are still forming; adversarial challenge is premature and may suppress creative exploration |
| TEAM-SINGLE (single agent self-DA) | Self-DA is mechanistically weak; the same model arguing against its own conclusions produces performative dissent (TASK-002: R-002-FP=6) |
| Without S-003 (Steelman) preceding it | DA without steelman risks attacking a strawman version of the argument, producing false positives |

### Complementary Pairings

| Partner | Type | Sequencing | Rationale |
|---------|------|-----------|-----------|
| S-003 | **SYN** | S-003 first, then S-002 | **Canonical Jerry review protocol.** Steelman ensures DA addresses strongest formulation. |
| S-007 | **SYN** | S-007 first (compliance), then S-002 (reasoning challenge) | Constitutional check handles structural compliance; DA challenges the reasoning quality and conclusion validity. |
| S-004 | COM | S-004 and S-002 independent | Pre-Mortem and DA provide complementary adversarial perspectives (temporal failure vs. argumentative challenge). |

### Tension Pairings

| Partner | Type | Tension | Management |
|---------|------|---------|------------|
| S-001 | **TEN** | Both provide adversarial challenge through role assignment. S-001 simulates an adversary's behavior; S-002 argues against conclusions. Concurrent application is redundant for the same artifact. | Scope separate: use S-002 for reasoning/decision quality; use S-001 for security/robustness concerns. Do not apply both to the same narrow artifact in the same pass. At C4, both are applied but to different aspects of the same artifact. |

### Preconditions

1. Artifact must contain conclusions, recommendations, or decisions that can be challenged
2. A separate critic agent should be available (TEAM-MULTI) for maximum effectiveness
3. Steelman (S-003) should have been applied first

### Expected Outcomes

| Output | Description |
|--------|------------|
| **Counter-arguments** | Strongest possible arguments against the artifact's conclusions |
| **Assumption challenges** | Explicit identification and challenge of unstated assumptions |
| **Alternative perspectives** | Different interpretations of the same evidence |
| **Weakness identification** | Specific weaknesses in reasoning, evidence, or logic |

**Defect categories detected:** Confirmation bias, weak reasoning, unsupported conclusions, unexamined assumptions, logical fallacies.

**Expected quality improvement:** +0.10 to +0.15 per review cycle.

### Token Budget

- **Per-invocation:** ~4,600 tokens
- **Token tier:** Low
- **Budget impact:** Moderate. Affordable at C2+; may be skipped at C1 or TOK-EXHAUST.

### Enforcement Layer Mapping

| Layer | Delivery Mechanism | Context Rot Vulnerability |
|-------|-------------------|--------------------------|
| L1 (Static Context) | Critic agent rules include DA role | VULNERABLE |
| Process | Critic step in creator-critic-revision cycle mandates adversarial challenge | IMMUNE |

**Primary delivery:** Process (critic workflow step)
**Portable fallback:** L1 critic rules + Process gate
**Enhanced delivery:** None -- DA is agent-executed, not hook-triggered

### Platform Portability

**Classification:** Fully portable
- Agent-executed strategy with no platform-specific dependencies
- Process gates are universal

### Decision Criticality Mapping

| Level | Required? | Role | Rationale |
|-------|-----------|------|-----------|
| C1 | Not required | N/A | Overkill for routine work; S-010 provides adequate self-check |
| C2 | **Required** | L2 (Standard Critic) | Core adversarial challenge at target operating layer |
| C3 | **Required** | L3 (Deep Review) | Essential adversarial perspective for high-risk decisions |
| C4 | **Required** | L4 (Tournament) | Multiple adversarial perspectives needed |

---

## S-004: Pre-Mortem Analysis

**Rank:** 6 | **Score:** 4.10 | **Family:** Role-Based Adversarialism | **ADR Ref:** ADR-EPIC002-001

### When to Use

| Dimension | Favorable Values | Rationale |
|-----------|-----------------|-----------|
| Target Type | TGT-ARCH, TGT-DEC, TGT-PROC | Unique temporal reframing is most valuable for plans, designs, and decisions |
| Phase | PH-DESIGN (primary), PH-EXPLORE | Maximum value in design phase when failure imagination can redirect effort. Also valuable early when plans are being formed. |
| Criticality | CRIT-C3, CRIT-C4 | Reserved for elevated criticality where failure consequences justify the investment |

### When to Avoid

| Condition | Rationale |
|-----------|-----------|
| PH-IMPL, PH-VALID, PH-MAINT (implementation and later) | Too late for failure imagination to redirect design; use verification strategies instead |
| TGT-CODE (pure code) | Pre-Mortem's temporal reframing ("it has failed") does not naturally apply to code artifacts; FMEA is more appropriate for code failure modes |
| CRIT-C1 (routine) | Token cost (5,600) is unjustified for routine work |

### Complementary Pairings

| Partner | Type | Sequencing | Rationale |
|---------|------|-----------|-----------|
| S-012 | **SYN** | S-004 first (creative), then S-012 (systematic) | Pre-Mortem identifies creative/strategic failure modes; FMEA provides systematic enumeration. Together they achieve comprehensive failure coverage. |
| S-013 | **SYN** | S-013 (structural anti-patterns), S-004 (narrative failures) | Complementary failure analysis: Inversion generates structural anti-patterns; Pre-Mortem generates narrative failure scenarios. |

### Tension Pairings

None within the selected 10.

### Preconditions

1. Artifact must describe a plan, design, or decision with a future success/failure horizon
2. Team composition should be TEAM-MULTI or TEAM-HIL (self-Pre-Mortem is weaker)

### Expected Outcomes

| Output | Description |
|--------|------------|
| **Failure cause inventory** | Enumeration of ways the plan/design could fail, generated from "it has already failed" perspective |
| **Mitigation recommendations** | Concrete actions to prevent each failure cause |
| **Risk prioritization** | Failure causes ranked by likelihood and impact |

**Defect categories detected:** Planning fallacy, optimism bias, unstated assumptions about success, missing risk mitigations, unexamined failure modes.

**Expected quality improvement:** +0.10 to +0.15 for design-phase artifacts.

### Token Budget

- **Per-invocation:** ~5,600 tokens
- **Token tier:** Low
- **Budget impact:** Moderate.

### Enforcement Layer Mapping

| Layer | Delivery Mechanism | Context Rot Vulnerability |
|-------|-------------------|--------------------------|
| Process | Design review workflow mandates Pre-Mortem step for C3+ artifacts | IMMUNE |

**Primary delivery:** Process (design review gate)
**Portable fallback:** Process gate (inherently portable)
**Enhanced delivery:** None -- process-triggered, not hook-triggered

### Platform Portability

**Classification:** Fully portable
- Process-based delivery has zero platform dependency
- No hooks, no platform-specific mechanisms

### Decision Criticality Mapping

| Level | Required? | Role | Rationale |
|-------|-----------|------|-----------|
| C1 | Not recommended | N/A | Overkill |
| C2 | Optional | L2 supplement | Can be added for design decisions at C2 if risk warrants |
| C3 | **Required** | L3 (Deep Review) | Failure imagination is essential for high-risk design |
| C4 | **Required** | L4 (Tournament) | Comprehensive failure analysis |

---

## S-010: Self-Refine

**Rank:** 7 | **Score:** 4.00 | **Family:** Iterative Self-Correction | **ADR Ref:** ADR-EPIC002-001

### When to Use

| Dimension | Favorable Values | Rationale |
|-----------|-----------------|-----------|
| Target Type | All | Universal self-improvement applicable to any artifact |
| Phase | All | Most valuable at PH-IMPL and PH-DESIGN as pre-critic baseline |
| Criticality | CRIT-C1 (primary), CRIT-C2 | Default baseline at L0 (Self-Check). Always-on for routine work. |
| Team | TEAM-SINGLE (primary) | Designed for single-agent self-review; also used as pre-step in multi-agent workflows |
| Token Budget | All (TOK-FULL, TOK-CONST, TOK-EXHAUST) | Ultra-low cost (2,000 tokens) |

### When to Avoid

| Condition | Rationale |
|-----------|-----------|
| As sole review for C3/C4 | Self-Refine alone is insufficient for high-criticality artifacts due to shared-model blind spot (DA-002) |
| Repeated application (> 3 iterations) | Diminishing returns after 2-3 iterations documented by Madaan et al. (2023) |

### Complementary Pairings

| Partner | Type | Sequencing | Rationale |
|---------|------|-----------|-----------|
| S-014 | COM | S-010 first, then S-014 | Self-improve, then score. Enables measuring improvement. |
| S-007 | COM | S-010 first, then S-007 | Self-improve basic quality, then constitutional compliance check. Reduces noise in constitutional review. |

### Tension Pairings

| Partner | Type | Tension | Management |
|---------|------|---------|------------|
| S-003 | **TEN** | Both are "improvement-before-critique" strategies. S-010 improves own output; S-003 strengthens another's argument. | Scope separate: S-010 for self-authored work; S-003 for evaluating others' work. Never apply both to the same artifact in the same pass. |

### Preconditions

1. Agent has just produced output that can be reviewed (not consuming external input)
2. Iteration count has not exceeded 3 (diminishing returns)

### Expected Outcomes

| Output | Description |
|--------|------------|
| **Improved artifact version** | Self-corrected version with identified issues fixed |
| **Self-assessment notes** | What the agent identified as needing improvement |

**Defect categories detected:** Surface-level errors, inconsistencies, incomplete sections, obvious logical gaps. Limited to defects the same model can self-identify (DA-002 constraint).

**Expected quality improvement:** +0.05 to +0.10 per iteration, diminishing after iteration 2.

### Token Budget

- **Per-invocation:** ~2,000 tokens
- **Token tier:** Ultra-Low
- **Budget impact:** Negligible.

### Enforcement Layer Mapping

| Layer | Delivery Mechanism | Context Rot Vulnerability |
|-------|-------------------|--------------------------|
| L1 (Static Context) | Self-review instruction in agent rules | VULNERABLE |
| L2 (Per-Prompt) | Self-review reminder via V-024 | IMMUNE |
| L4 (Post-Action) | V-002 hook triggers self-review after output | MIXED |

**Primary delivery:** L1 rule + L2 reinforcement
**Portable fallback:** L1 rule (self-review instruction in `.claude/rules/`)
**Enhanced delivery:** L4 hook for automatic post-output self-review trigger

### Platform Portability

**Classification:** Fully portable
- Self-review is an agent-internal behavior triggered by rules
- No platform-specific mechanism needed

### Decision Criticality Mapping

| Level | Required? | Role | Rationale |
|-------|-----------|------|-----------|
| C1 | **Required** (always-on) | L0 (Self-Check) | Baseline self-improvement for all work |
| C2 | Recommended | L0 pre-step before L2 critique | Cleans up obvious issues before dedicated critique |
| C3 | Optional | L0 pre-step | Included in higher layers by default |
| C4 | Optional | L0 pre-step | Included in higher layers by default |

---

## S-012: FMEA

**Rank:** 8 | **Score:** 3.75 | **Family:** Structured Decomposition | **ADR Ref:** ADR-EPIC002-001

### When to Use

| Dimension | Favorable Values | Rationale |
|-----------|-----------------|-----------|
| Target Type | TGT-ARCH, TGT-CODE, TGT-PROC, TGT-REQ | Systematic failure enumeration applicable to any artifact with identifiable components and failure modes |
| Phase | PH-DESIGN, PH-IMPL | Maximum value during design and implementation when failure modes can be prevented |
| Criticality | CRIT-C3, CRIT-C4 | Medium token cost (9,000) justifies use at elevated criticality |

### When to Avoid

| Condition | Rationale |
|-----------|-----------|
| PH-EXPLORE (early exploration) | Artifact too formless for systematic component enumeration |
| TOK-EXHAUST | Medium token cost (9,000) is too expensive in exhausted budgets |
| TGT-RES (research artifacts) | Research does not have "failure modes" in the FMEA sense; use S-011 (CoVe) for factual verification instead |

### Complementary Pairings

| Partner | Type | Sequencing | Rationale |
|---------|------|-----------|-----------|
| S-004 | **SYN** | S-004 first (creative), S-012 second (systematic) | Pre-Mortem + FMEA = comprehensive failure analysis (creative + systematic). Primary synergy pair. |
| S-013 | **SYN** | S-013 first (anti-patterns), S-012 maps to failure modes | Inversion generates anti-patterns; FMEA systematically evaluates them with severity/occurrence/detection scoring. |
| S-001 | **SYN** | S-012 identifies failure modes, S-001 tests exploitability | FMEA + Red Team = identify then attack. |

### Tension Pairings

None within the selected 10.

### Preconditions

1. Artifact must have identifiable components or elements that can fail
2. Failure mode categories relevant to the artifact type must be available (or generated by S-013)
3. H/M/L (or S/O/D) scoring criteria must be defined

### Expected Outcomes

| Output | Description |
|--------|------------|
| **FMEA table** | Component / Failure Mode / Effect / Severity / Occurrence / Detection / RPN |
| **Risk-prioritized failure inventory** | Failure modes ranked by RPN for remediation priority |
| **Detection gap analysis** | Failure modes with low detection scores needing additional mitigation |

**Defect categories detected:** Systematic failure modes, interaction effects (partial), severity assessments, detection gaps.

**Expected quality improvement:** +0.10 to +0.15 for design and architecture artifacts.

### Token Budget

- **Per-invocation:** ~9,000 tokens
- **Token tier:** Medium
- **Budget impact:** Significant. Reserve for C3+.

### Enforcement Layer Mapping

| Layer | Delivery Mechanism | Context Rot Vulnerability |
|-------|-------------------|--------------------------|
| L5 (Post-Hoc) | FMEA checklist verification in CI | IMMUNE |
| Process | Risk analysis step in design review workflow | IMMUNE |

**Primary delivery:** Process (design review risk analysis step)
**Portable fallback:** Process gate (universally portable)
**Enhanced delivery:** L5 CI verification of FMEA checklist compliance

### Platform Portability

**Classification:** Fully portable
- Process-based and CI-based delivery are platform-independent

### Decision Criticality Mapping

| Level | Required? | Role | Rationale |
|-------|-----------|------|-----------|
| C1 | Not recommended | N/A | Overkill; 9,000 tokens unjustified |
| C2 | Optional | L2 supplement for complex features | Can be added for features with significant failure surface |
| C3 | **Required** | L3 (Deep Review) | Systematic failure analysis essential at high criticality |
| C4 | **Required** | L4 (Tournament) | Comprehensive risk assessment |

---

## S-011: Chain-of-Verification

**Rank:** 9 | **Score:** 3.75 | **Family:** Structured Decomposition | **ADR Ref:** ADR-EPIC002-001

### When to Use

| Dimension | Favorable Values | Rationale |
|-----------|-----------------|-----------|
| Target Type | TGT-RES (primary), TGT-REQ, TGT-DEC | Factual verification is most critical for research, requirements with empirical claims, and evidence-based decisions |
| Phase | PH-VALID (primary), PH-IMPL | Maximum value during validation when factual claims must be verified |
| Criticality | CRIT-C3, CRIT-C4 | Reserved for elevated criticality; only factual verification strategy |

### When to Avoid

| Condition | Rationale |
|-----------|-----------|
| TGT-CODE (pure code) | Code correctness is verified by tests, not factual claim verification |
| PH-EXPLORE (early exploration) | Facts are being gathered, not verified |
| TOK-EXHAUST | Medium token cost (6,000) too expensive; defer to L5 CI checks |
| TEAM-SINGLE with strict context isolation requirement | Context isolation (answering verification questions without original output) is harder in single-agent mode |

### Complementary Pairings

| Partner | Type | Sequencing | Rationale |
|---------|------|-----------|-----------|
| S-014 | COM | S-011 verifies facts, S-014 scores overall quality | Factual verification + quality scoring = comprehensive evaluation. |
| S-002 | COM | S-002 challenges reasoning, S-011 verifies factual claims within that reasoning | DA handles logic quality; CoVe handles fact quality. Non-overlapping domains. |

### Tension Pairings

None within the selected 10.

### Preconditions

1. Artifact must contain factual claims, citations, or empirical assertions that can be independently verified
2. Verification agent should have access to reference knowledge (or external tools) to verify claims
3. Context isolation should be achievable (separate verification pass without the original artifact in context)

### Expected Outcomes

| Output | Description |
|--------|------------|
| **Verified claims list** | Each factual claim marked as VERIFIED, UNVERIFIED, or CONTRADICTED |
| **Corrected claims** | Factual corrections for contradicted claims |
| **Confidence assessment** | Verification confidence per claim (HIGH/MEDIUM/LOW based on available evidence) |

**Defect categories detected:** Hallucinations, factual errors, citation inaccuracies, unsupported empirical claims.

**Expected quality improvement:** +0.05 to +0.15 for research and evidence-heavy artifacts.

### Token Budget

- **Per-invocation:** ~6,000 tokens
- **Token tier:** Medium
- **Budget impact:** Moderate.

### Enforcement Layer Mapping

| Layer | Delivery Mechanism | Context Rot Vulnerability |
|-------|-------------------|--------------------------|
| L4 (Post-Action) | V-002 hook triggers factual verification after output | MIXED |
| Process | Verification step in research review workflow | IMMUNE |

**Primary delivery:** Process (verification workflow step)
**Portable fallback:** Process gate
**Enhanced delivery:** L4 hook for automatic post-output verification

### Platform Portability

**Classification:** Fully portable (degraded without hooks)
- PLAT-CC: L4 hook enables automatic verification trigger
- PLAT-GENERIC: Manual process-triggered verification. Full capability, reduced automation.

### Decision Criticality Mapping

| Level | Required? | Role | Rationale |
|-------|-----------|------|-----------|
| C1 | Not recommended | N/A | Factual verification overkill for routine changes |
| C2 | Optional | L2 supplement for evidence-heavy artifacts | Add when factual claims are central to the artifact |
| C3 | Recommended | L3 (Deep Review) | Important for high-risk decisions based on evidence |
| C4 | **Required** | L4 (Tournament) | All claims must be verified at maximum criticality |

---

## S-001: Red Team Analysis

**Rank:** 10 | **Score:** 3.35 | **Family:** Role-Based Adversarialism | **ADR Ref:** ADR-EPIC002-001

### When to Use

| Dimension | Favorable Values | Rationale |
|-----------|-----------------|-----------|
| Target Type | TGT-ARCH (primary), TGT-CODE (security-relevant), TGT-PROC (robustness) | Adversary simulation is most valuable for architecture, security, and robustness testing |
| Phase | PH-DESIGN (primary), PH-IMPL (security code) | Maximum value during design when architectural vulnerabilities can be addressed |
| Criticality | CRIT-C4 (primary), CRIT-C3 (for security-relevant artifacts) | Reserved for highest criticality; token cost (7,000) and adversary persona setup justify only for significant targets |

### When to Avoid

| Condition | Rationale |
|-----------|-----------|
| PH-EXPLORE | Premature adversarial pressure (TASK-002: R-001-QR=9) is highest in exploration phase |
| TGT-RES (research artifacts) | Research does not have "attackable" interfaces; use S-002 (DA) instead |
| CRIT-C1, CRIT-C2 (routine/standard) | Token cost unjustified; S-002 provides adequate adversarial challenge at lower criticality |
| TEAM-SINGLE | Self-Red-Team is mechanistically weak; needs separate critic with adversary persona |
| TOK-EXHAUST or TOK-CONST | Medium cost (7,000) too expensive in constrained budgets |

### Complementary Pairings

| Partner | Type | Sequencing | Rationale |
|---------|------|-----------|-----------|
| S-003 | **SYN** | S-003 first (steelman defense), then S-001 attacks | Red Team attacks the strongest version of the defense, producing more meaningful vulnerabilities. |
| S-012 | **SYN** | S-012 identifies failure modes, S-001 tests exploitability | FMEA provides systematic failure catalog; Red Team attempts to exploit them. |
| S-013 | **SYN** | S-013 generates anti-patterns/attack surface, S-001 exploits | Inversion provides attack vectors; Red Team weaponizes them. |
| S-007 | **SYN** | S-007 checks compliance, S-001 attempts to bypass | Constitutional check identifies intended defenses; Red Team tests if they hold under adversarial pressure. |

### Tension Pairings

| Partner | Type | Tension | Management |
|---------|------|---------|------------|
| S-002 | **TEN** | Both provide adversarial challenge via role assignment. S-001 simulates adversary behavior; S-002 argues against conclusions. | Scope separate: S-002 for reasoning/decision quality (all C2+ artifacts); S-001 for security/robustness (C3+ architecture and security artifacts). At C4, apply both to different aspects of the artifact. |

### Preconditions

1. Artifact must have an attackable surface (interfaces, security boundaries, access controls, trust boundaries)
2. An adversary persona must be defined appropriate to the threat model
3. Separate critic agent with adversary persona available (TEAM-MULTI)

### Expected Outcomes

| Output | Description |
|--------|------------|
| **Vulnerability report** | Identified attack vectors with severity ratings |
| **Exploitation scenarios** | How an adversary would exploit each vulnerability |
| **Mitigation recommendations** | Defenses and countermeasures for identified vulnerabilities |

**Defect categories detected:** Security vulnerabilities, architectural weaknesses, robustness gaps, trust boundary violations, bypass opportunities.

**Expected quality improvement:** +0.05 to +0.15 for architecture and security artifacts.

### Token Budget

- **Per-invocation:** ~7,000 tokens
- **Token tier:** Medium
- **Budget impact:** Significant. Reserve for C3+ security and C4.

### Enforcement Layer Mapping

| Layer | Delivery Mechanism | Context Rot Vulnerability |
|-------|-------------------|--------------------------|
| L3 (Pre-Action) | V-001 hook triggers Red Team check for security-tagged files | IMMUNE |
| Process | Security review gate for C3+ artifacts | IMMUNE |

**Primary delivery:** Process (security review gate)
**Portable fallback:** Process gate (universally portable)
**Enhanced delivery:** L3 hook for automatic security-tagged file review

### Platform Portability

**Classification:** Fully portable (degraded without hooks)
- PLAT-CC: L3 hooks enable automatic trigger for security-tagged files
- PLAT-GENERIC: Manual process-triggered Red Team review. Full capability, reduced automation.

### Decision Criticality Mapping

| Level | Required? | Role | Rationale |
|-------|-----------|------|-----------|
| C1 | Not recommended | N/A | Overkill |
| C2 | Not recommended | N/A | S-002 (DA) provides adequate adversarial challenge |
| C3 | Recommended (for security/architecture) | L3 (Deep Review) | Security and architecture artifacts warrant adversary simulation |
| C4 | **Required** | L4 (Tournament) | Maximum-intensity adversary simulation |

---

## Consolidated Pairing Reference

### Synergistic (SYN) Pairs -- 14 within Selected 10

| # | Pair | Sequencing | Primary Context |
|---|------|-----------|-----------------|
| 1 | S-003 + S-002 | S-003 first | Steelman-then-DA: canonical review protocol |
| 2 | S-003 + S-007 | S-003 first | Steelman-then-Constitutional: fair compliance evaluation |
| 3 | S-003 + S-001 | S-003 first | Steelman-then-Red-Team: attack strongest defense |
| 4 | S-007 + S-013 | S-013 first | Inversion-then-Constitutional: anti-pattern verification |
| 5 | S-007 + S-014 | S-007 first | Constitutional-then-Judge: compliance + scoring |
| 6 | S-007 + S-002 | S-007 first | Constitutional-then-DA: compliance then reasoning challenge |
| 7 | S-013 + S-012 | Parallel | Inversion + FMEA: creative + systematic failure analysis |
| 8 | S-013 + S-004 | Parallel | Inversion + Pre-Mortem: structural + narrative failure analysis |
| 9 | S-013 + S-001 | S-013 first | Inversion-then-Red-Team: generate attack surface then exploit |
| 10 | S-004 + S-012 | S-004 first | Pre-Mortem-then-FMEA: creative then systematic failure analysis |
| 11 | S-001 + S-012 | S-012 first | FMEA-then-Red-Team: identify then exploit failure modes |
| 12 | S-001 + S-007 | S-007 first | Constitutional-then-Red-Team: verify defenses then test under attack |
| 13 | S-014 + S-010 | S-010 first | Self-Refine-then-Judge: improve then score |
| 14 | S-003 + S-014 | S-003 first | Steelman-then-Judge: fair representation then scoring |

### Tension (TEN) Pairs -- 3 within Selected 10

| # | Pair | Tension Description | Management |
|---|------|-------------------|------------|
| 1 | S-001 + S-002 | Both adversarial via role assignment; redundant on same artifact | Scope separate: S-002 for reasoning quality, S-001 for security/robustness |
| 2 | S-003 + S-010 | Both "improvement-before-critique"; over-polishing risk | Scope separate: S-010 for self-authored work, S-003 for evaluating others' work |
| 3 | S-001 + S-002 (variant) | Per TASK-004 composition matrix, both deliver oppositional challenge | At C4, apply to different aspects of same artifact |

**Note:** The EN-302 TASK-004 composition matrix identifies 14 SYN, 26 COM, 3 TEN, 0 CON pairs within the selected 10. The 26 COM pairs are all remaining strategy combinations not listed as SYN or TEN -- they are compatible with no special sequencing or conflict management needed.

---

## Enforcement Gap Analysis

Per Barrier-1 ENF-to-ADV handoff "Implementation Capabilities -- What Enforcement CANNOT Do" and FR-008:

| Enforcement Gap | Why Enforcement Cannot Fill | Adversarial Strategies as Sole Defense | Coverage Assessment |
|-----------------|-----------------------------|---------------------------------------|---------------------|
| **Semantic quality** | AST checks structure, not meaning; "correct code" is not "good code" | S-002 (DA challenges reasoning quality), S-003 (Steelman ensures fair evaluation), S-007 (Constitutional AI evaluates against quality principles), S-014 (Judge scores quality) | COVERED -- 4 strategies address semantic quality from different angles |
| **Context rot prevention** | Inherent LLM limitation; no enforcement can prevent context degradation | S-010 (Self-Refine as lightweight self-correction), L2 reinforcement (V-024) compensates. Adversarial strategies cannot prevent rot but can detect degraded outputs. | PARTIALLY COVERED -- detection is feasible, prevention is not |
| **Novel violation types** | AST rules are pre-defined; cannot catch unknown patterns | S-001 (Red Team explores unknown attack vectors), S-013 (Inversion generates novel failure criteria), S-004 (Pre-Mortem imagines novel failures) | COVERED -- exploratory strategies can discover novel violations |
| **Social engineering bypass** | Users can disable hooks, bypass pre-commit (`--no-verify`) | Process gates (V-057 quality gate, V-060 evidence-based closure) block task closure without evidence. S-014 (Judge) provides quality evidence that must exist. | PARTIALLY COVERED -- process gates are primary defense; adversarial strategies provide evidence that gates require |

---

## Excluded Strategy Coverage Gaps

Per ADR-EPIC002-001 Consequences (Negative):

| Excluded Strategy | Gap Created | Partial Mitigation by Selected Strategies |
|-------------------|-----------|------------------------------------------|
| S-008 (Socratic Method) | Dunning-Kruger / Illusion of explanatory depth bias coverage lost | S-007 (principle-by-principle evaluation exposes gaps), S-012 (systematic enumeration surfaces competence gaps) -- partial coverage |
| S-006 (ACH) | Matrix-based multi-hypothesis evaluation lost | S-002 (oppositional challenge to conclusions), S-011 (factual verification) -- partial coverage of confirmation bias |
| S-005 (Dialectical Inquiry) | Formal thesis-antithesis-synthesis lost | S-003 + S-002 + reconciliation approximates ~70-80% of DI value |
| S-009 (Multi-Agent Debate) | Competitive multi-agent argumentation lost; L4 Tournament reduced | S-001 + S-002 provide multi-perspective adversarial challenge; L4 deploys 6+ strategies concurrently |
| S-015 (PAE) | Scope insensitivity bias coverage lost; graduated escalation as strategy lost | S-015 orchestration logic implemented in EN-307 as workflow configuration; scope coverage via orchestration |

---

## Traceability

### Requirements Coverage

| Requirement | How Addressed |
|-------------|--------------|
| FR-003 | Each profile includes enforcement layer mapping (primary, portable fallback, enhanced) |
| FR-004 | Each profile includes decision criticality mapping (C1-C4 with required/optional) |
| FR-005 | Each profile includes platform portability classification with PLAT-GENERIC fallback |
| FR-006 | Each profile includes token cost, tier, and budget impact |
| FR-007 | Consolidated Pairing Reference documents all 14 SYN pairs and 3 TEN pairs with management guidance |
| FR-009 | Creator-critic-revision cycle supported by S-010 (iteration 1), S-002/S-007 (iteration 2), S-014 (iteration 3) |
| NFR-002 | Token costs per strategy documented; cumulative budgets derivable from criticality mapping |
| NFR-003 | Every strategy has portable delivery mechanism documented |
| NFR-004 | When-to-avoid sections flag aggressive patterns under constrained budgets |

### Acceptance Criteria Coverage

| AC | How Addressed |
|----|--------------|
| AC-2 | All 10 strategy profiles present with complete applicability information |
| AC-3 | Each profile includes: when to use, when to avoid, pairings, preconditions, outcomes, enforcement layer mapping, platform portability |
| AC-10 | Blue Team review inputs prepared: context rot noted in enforcement mappings, portability classified, token budgets documented |
| AC-11 | Traceability to ADR-EPIC002-001 (strategy IDs, scores, quality layers) and Barrier-1 (enforcement layers, platform constraints) throughout |
| AC-12 | Every strategy has portable delivery mechanism (L1/L5/Process) documented in enforcement layer mapping |

---

## References

| # | Citation | Sections Referenced |
|---|----------|-------------------|
| 1 | ADR-EPIC002-001 (ACCEPTED) -- FEAT-004:EN-302:TASK-005 | Strategy IDs, scores, quality layers (L0-L4), criticality levels (C1-C4), synergy/tension pairs, token budgets |
| 2 | EN-302 TASK-004 -- FEAT-004:EN-302:TASK-004 | Scoring matrix, composition synergy verification (14 SYN, 26 COM, 3 TEN), per-strategy scoring justifications |
| 3 | Barrier-1 ENF-to-ADV Handoff -- EPIC002-CROSSPOLL-B1-ENF-TO-ADV | 5-Layer enforcement architecture, platform constraints, implementation capabilities (CAN/CANNOT), enforcement gaps, 4 RED systemic risks |
| 4 | EN-303 TASK-001 -- FEAT-004:EN-303:TASK-001 | Context taxonomy dimensions, dimension codes, cross-dimension interactions |
| 5 | EN-302 TASK-002 -- FEAT-004:EN-302:TASK-002 | Risk profiles per strategy (aggregate scores, RED/YELLOW/GREEN), specific risk IDs (R-001-QR, R-002-FP, R-014-FN) |

---

*Document ID: FEAT-004:EN-303:TASK-003*
*Agent: ps-architect*
*Created: 2026-02-13*
*Status: Complete*
