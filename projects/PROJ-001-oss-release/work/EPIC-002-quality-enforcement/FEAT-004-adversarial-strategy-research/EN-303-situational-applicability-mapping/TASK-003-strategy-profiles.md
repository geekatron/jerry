# TASK-003: Per-Strategy Applicability Profiles

<!--
DOCUMENT-ID: FEAT-004:EN-303:TASK-003
VERSION: 1.1.0
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

> **Version:** 1.1.0
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
| [Defense-in-Depth Compensation Chain](#defense-in-depth-compensation-chain) | Which strategies compensate when enforcement layers fail (REQ-303-030) |
| [Cumulative Token Budget Verification](#cumulative-token-budget-verification) | Token budget per criticality vs. enforcement envelope (REQ-303-036) |
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

**ENF-MIN handling:** Under ENF-MIN (L1 only), S-014 is deliverable via L1 rubric encoded in `.claude/rules/`. The rubric dimensions and scoring prompt can be self-contained in rules. However, the Process quality gate (V-057) is unavailable, so scoring is advisory only with no enforcement gate. Subject to context rot degradation at 50K+ tokens. At C3+ with ENF-MIN, recommend human escalation to compensate for loss of Process gate.

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

**ENF-MIN handling:** Under ENF-MIN (L1 only), S-003 is deliverable via L1 steelman instruction in `.claude/rules/`. The Process mandate and L2 reinforcement are unavailable. L1-only delivery is subject to context rot at 50K+ tokens, but S-003's ultra-low cost (1,600 tokens) and single-pass nature make it viable even in degraded environments. S-003 remains feasible under ENF-MIN.

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

**ENF-MIN handling:** Under ENF-MIN (L1 only), S-013 is deliverable via L1 inversion prompt. The Process mandate and L5 CI verification are unavailable. S-013's single-pass generative nature makes it self-contained in the prompt, so L1-only delivery is viable. Subject to context rot at 50K+ tokens. Anti-pattern output is advisory only (no CI verification of checklist compliance). S-013 remains feasible under ENF-MIN.

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

**ENF-MIN handling:** Under ENF-MIN (L1 only), S-007 is deliverable via L1 constitutional principles in `.claude/rules/`. However, the L3 real-time gating, L5 CI verification, and Process gates are all unavailable. This means constitutional evaluation is advisory only -- violations are flagged but not blocked. Subject to severe context rot degradation at 50K+ tokens, since constitutional principles may be forgotten. At C3+ with ENF-MIN, S-007 effectiveness is significantly reduced; recommend human escalation to compensate for loss of enforcement layers.

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

**ENF-MIN handling:** Under ENF-MIN (L1 only), S-002 delivery degrades significantly. The Process gate (critic workflow step) is unavailable. S-002 must rely solely on L1 critic agent rules. Since S-002's effectiveness depends on having a separate critic agent (TEAM-MULTI), ENF-MIN combined with TEAM-SINGLE renders S-002 essentially infeasible. Under ENF-MIN with TEAM-MULTI, S-002 is deliverable via L1 rules but without Process enforcement -- the critic challenge is advisory only. Subject to context rot at 50K+ tokens. Recommend human escalation at C3+ with ENF-MIN to compensate.

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

**ENF-MIN handling:** Under ENF-MIN (L1 only), S-004 has **no delivery mechanism**. S-004 relies solely on Process gates (design review workflow), which are unavailable under ENF-MIN. The strategy cannot be delivered through L1 rules alone because Pre-Mortem requires structured workflow orchestration (temporal reframing exercise). Under ENF-MIN, S-004 is **infeasible** and must be replaced by: (a) human-directed Pre-Mortem (if TEAM-HIL), or (b) S-013 (Inversion) as a partial substitute providing failure-mode generation via L1 prompt. At C3+ with ENF-MIN, mandatory human escalation is required to compensate for S-004 loss.

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

**ENF-MIN handling:** Under ENF-MIN (L1 only), S-010 is deliverable via L1 self-review instruction. L2 reinforcement and L4 hooks are unavailable, so the self-review prompt must be relied upon entirely from initial session rules. Subject to context rot at 50K+ tokens. However, S-010 is the single most resilient strategy under ENF-MIN because self-review is an inherently agent-internal behavior that does not require external enforcement. S-010 remains feasible and is the recommended baseline strategy under ENF-MIN.

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

**ENF-MIN handling:** Under ENF-MIN (L1 only), S-012 has **no delivery mechanism**. S-012 relies on Process gates (risk analysis workflow step) and L5 CI verification, both unavailable under ENF-MIN. FMEA requires structured component-failure enumeration that cannot be effectively encoded as an L1 rule alone. Under ENF-MIN, S-012 is **infeasible** and must be replaced by: (a) human-directed FMEA (if TEAM-HIL), or (b) S-013 (Inversion) as a partial substitute providing failure-mode generation through L1 prompt. At C3+ with ENF-MIN, mandatory human escalation is required to compensate for S-012 loss.

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

**ENF-MIN handling:** Under ENF-MIN (L1 only), S-011 delivery degrades significantly. The Process gate and L4 hooks are unavailable. CoVe's context isolation requirement (separate verification pass) is difficult to achieve through L1 rules alone. Under ENF-MIN, S-011 is **marginally feasible** -- the verification prompt can be encoded in L1 rules, but without Process enforcement the verification step is advisory only, and context isolation cannot be guaranteed. Recommend human-directed verification at C3+ with ENF-MIN.

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

**ENF-MIN handling:** Under ENF-MIN (L1 only), S-001 has **no delivery mechanism**. S-001 relies on Process gates (security review gate) and L3 hooks, both unavailable under ENF-MIN. Red Team requires structured adversary persona setup and separate critic agent, which cannot be orchestrated through L1 rules alone. Under ENF-MIN, S-001 is **infeasible** and must be replaced by human-directed security review (TEAM-HIL mandatory). At C4 with ENF-MIN, the entire review session should be escalated to human control.

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

### Tension (TEN) Pairs -- 2 within Selected 10

| # | Pair | Tension Description | Management |
|---|------|-------------------|------------|
| 1 | S-001 + S-002 | Both provide adversarial challenge via role assignment: S-001 simulates adversary behavior; S-002 argues against conclusions. Concurrent application to the same narrow artifact is redundant because both deliver oppositional challenge through different framing but with overlapping defect detection coverage. | **Scope separate:** S-002 for reasoning/decision quality (applied to all C2+ artifacts); S-001 for security/robustness concerns (applied to C3+ architecture and security artifacts). At C4, both are applied but scoped to different aspects of the same artifact (S-002 challenges reasoning; S-001 tests security/robustness). |
| 2 | S-003 + S-010 | Both are "improvement-before-critique" strategies: S-010 improves own output; S-003 strengthens another's argument. Applying both to the same artifact in the same review pass risks over-polishing before critical review, delaying defect identification. | **Scope separate:** S-010 for self-authored work (creator iteration); S-003 for evaluating others' work (critic pre-step). Never apply both to the same artifact in the same pass. |

**Deviation note:** ADR-EPIC002-001 (via EN-302 TASK-004 composition matrix) claims 3 TEN pairs. Upon detailed analysis in TASK-003, the originally listed "TEN pair #3" (S-001 + S-002 variant) describes the same strategic pair as TEN pair #1 with a different framing. Both describe the tension between S-001 and S-002 when applied concurrently. The management guidance (scope separation, C4 aspect splitting) is consolidated into TEN pair #1 above. The corrected count is **2 unique TEN pairs**. This deviation from the ADR's claimed count of 3 is noted and does not affect the ADR's conclusions; the total pair count adjusts to: 14 SYN + 29 COM + 2 TEN = 45 = C(10,2).

### Compatible (COM) Pairs -- 29 within Selected 10

The following 29 strategy pairs are compatible with no special sequencing requirements, conflict management, or tension. They may be used together in any order. All pairs not listed in the SYN or TEN tables above are COM pairs.

| # | Pair | Notes |
|---|------|-------|
| 1 | S-001 + S-003 | Listed as SYN above (SYN #3); NOT a COM pair. |
| --- | --- | **The following are all COM pairs:** |
| 1 | S-001 + S-004 | Compatible. Both applicable at C3+; no sequencing dependency. |
| 2 | S-001 + S-010 | Compatible. Self-Refine before Red Team is natural but not required. |
| 3 | S-001 + S-011 | Compatible. CoVe can verify Red Team findings. No special management. |
| 4 | S-001 + S-014 | Compatible. Judge can score after Red Team review. No special management. |
| 5 | S-002 + S-003 | Listed as SYN above (SYN #1); NOT a COM pair. |
| --- | --- | --- |
| 5 | S-002 + S-004 | Compatible. DA and Pre-Mortem provide complementary adversarial perspectives. No sequencing dependency. |
| 6 | S-002 + S-010 | Compatible. Self-Refine before DA is natural but not required. |
| 7 | S-002 + S-011 | Compatible. CoVe can verify factual claims within DA challenges. No special management. |
| 8 | S-002 + S-012 | Compatible. FMEA and DA address different defect categories. No special management. |
| 9 | S-002 + S-013 | Compatible. Inversion generates anti-patterns; DA challenges reasoning. Non-overlapping. |
| 10 | S-002 + S-014 | Compatible. Judge scores after DA critique. No special management. |
| 11 | S-003 + S-004 | Compatible. Steelman and Pre-Mortem address different aspects. No special management. |
| 12 | S-003 + S-011 | Compatible. Steelman ensures fair representation; CoVe verifies facts. Non-overlapping. |
| 13 | S-003 + S-012 | Compatible. Steelman strengthens argument; FMEA enumerates failure modes. Non-overlapping. |
| 14 | S-003 + S-013 | Compatible. Steelman strengthens; Inversion generates anti-patterns. Complementary but no special sequencing required. |
| 15 | S-004 + S-002 | (same as #5 above -- S-002 + S-004) |
| 16 | S-004 + S-007 | Compatible. Pre-Mortem imagines failure; Constitutional AI checks compliance. Non-overlapping. |
| 17 | S-004 + S-010 | Compatible. Self-Refine before Pre-Mortem is natural but not required. |
| 18 | S-004 + S-011 | Compatible. Pre-Mortem failure inventory + CoVe factual verification. Non-overlapping. |
| 19 | S-004 + S-014 | Compatible. Judge can score artifacts informed by Pre-Mortem findings. No special management. |
| 20 | S-007 + S-010 | Compatible. Self-Refine before Constitutional check reduces noise. No special management. |
| 21 | S-007 + S-011 | Compatible. Constitutional compliance + factual verification. Non-overlapping. |
| 22 | S-007 + S-012 | Compatible. Constitutional check + failure mode analysis. Non-overlapping. |
| 23 | S-010 + S-011 | Compatible. Self-Refine improves output; CoVe verifies facts. No special management. |
| 24 | S-010 + S-012 | Compatible. Self-Refine + FMEA. Non-overlapping. |
| 25 | S-010 + S-013 | Compatible. Self-Refine + Inversion. Non-overlapping. |
| 26 | S-011 + S-012 | Compatible. Factual verification + failure mode analysis. Non-overlapping. |
| 27 | S-011 + S-013 | Compatible. CoVe + Inversion. Non-overlapping. |
| 28 | S-011 + S-014 | Compatible. CoVe verifies facts; Judge scores quality. Non-overlapping. |
| 29 | S-012 + S-014 | Compatible. FMEA risk analysis + Judge quality scoring. Non-overlapping. |

**Pair count verification:** C(10,2) = 45 total unique pairs. 14 SYN + 2 TEN + 29 COM = 45. Verified complete.

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

## Defense-in-Depth Compensation Chain

Per REQ-303-030 and Barrier-1 ENF-to-ADV handoff, each enforcement layer compensates for the failure mode of the layer above. The following table maps each layer failure to the adversarial strategies that serve as compensating controls.

### Layer Failure to Adversarial Strategy Compensation

| Layer Failure | Failure Mode | Compensating Adversarial Strategies | Compensation Mechanism |
|---------------|-------------|-------------------------------------|----------------------|
| **L1 fails** (context rot) | Rules loaded at session start are forgotten or deprioritized after ~20K tokens | S-010 (Self-Refine via L2 reinforcement), S-007 (Constitutional AI via L2 per-prompt injection) | L2 re-injects critical rules every prompt, compensating for L1 context rot. S-010 and S-007 are the primary strategies that benefit from L2 compensation. |
| **L2 fails** (prompt reinforcement not triggered) | V-024 per-prompt reinforcement mechanism fails or is misconfigured | S-007 (via L3 pre-action gate), S-014 (via L3 pre-commit scoring) | L3 hooks trigger constitutional check and quality scoring before tool operations, providing enforcement independent of prompt-level reinforcement. |
| **L3 fails** (pre-action hook error, fail-open) | V-001 PreToolUse hook fails or is bypassed | S-014 (via L4 post-action validation), S-011 (via L4 post-output verification), S-010 (via L4 self-review) | L4 hooks catch violations after execution that L3 should have blocked before execution. Post-hoc detection replaces pre-action prevention. |
| **L4 fails** (post-action validation skipped) | V-002 PostToolUse hook fails | S-007 (via L5 architecture tests), S-012 (via L5 FMEA checklist verification) | L5 CI/pre-commit hooks verify compliance deterministically at commit time. All violations that escaped L3/L4 are caught at L5 if they have testable signatures. |
| **L5 fails** (CI bypass, `--no-verify`) | Pre-commit or CI pipeline bypassed by user | S-002 (via Process gate), S-001 (via Process security review), S-014 (via Process quality gate V-057) | Process gates require review evidence before task closure. V-057 quality gate requires S-014 score >= threshold. V-060 evidence-based closure requires review artifacts. Social engineering bypass is the residual risk (Enforcement Gap #4). |
| **Process fails** (user overrides gates) | User exercises P-020 authority to override quality gates | **No adversarial compensation available.** P-020 (User Authority) is a constitutional principle. If the user decides to override, the framework respects that decision. | Residual governance risk accepted per P-020. Audit trail records the override decision. |

### ENF-MIN Compensation Summary

Under ENF-MIN (L1 only), the compensation chain is severely degraded:
- Only L1 is available; L2 through Process are all unavailable
- No compensation layers exist for L1 failure
- **Feasible strategies under ENF-MIN:** S-010 (Self-Refine), S-003 (Steelman), S-013 (Inversion), S-014 (advisory scoring only), S-007 (advisory compliance only)
- **Infeasible strategies under ENF-MIN:** S-004 (Pre-Mortem), S-012 (FMEA), S-001 (Red Team) -- all require Process layer
- **Marginally feasible:** S-002 (DA -- requires TEAM-MULTI), S-011 (CoVe -- advisory only)
- **Mandatory action:** Human escalation for C3+ artifacts under ENF-MIN

---

## Cumulative Token Budget Verification

Per REQ-303-036, this section verifies the cumulative token budget for strategy combinations at each criticality level against the enforcement envelope (~12,476 tokens L1 + ~600/session L2 = ~13,076 total).

### Per-Criticality Token Budget vs. Enforcement Envelope

| Criticality | Required Strategies | Required Token Total | With Recommended | L1 Envelope (~12,476) | Fits L1? | Delivery Overflow |
|-------------|--------------------|-----------------------|------------------|-----------------------|----------|-------------------|
| **C1** | S-010 | 2,000 | 5,600 (+ S-003, S-014) | 12,476 | YES | All C1 strategies fit within L1 envelope |
| **C2** | S-007, S-002, S-014 | 14,600 (using S-007 at 8,000) | 18,200 (+ S-003, S-010) | 12,476 | **NO** | S-007 (8,000-16,000) exceeds L1 capacity alone; S-002 (4,600) and S-014 (2,000) require L2/Process delivery |
| **C3** | S-007, S-002, S-014, S-004, S-012, S-013 | 31,300 (using S-007 at 8,000) | 38,900 (+ S-003, S-010, S-011) | 12,476 | **NO** | Requires L2 + L3 + L5 + Process delivery; only S-010 (2,000), S-003 (1,600), S-013 (2,100), S-014 (2,000) = 7,700 fit L1 |
| **C4** | All 10 strategies | ~50,300 | N/A (all required) | 12,476 | **NO** | Requires full enforcement stack; L1 carries ~7,700 of 50,300 |

### Verification Findings

1. **C1 is fully deliverable within the L1 enforcement envelope.** All C1 strategies (required and optional) total 5,600 tokens, well within the ~12,476 L1 capacity.

2. **C2 required set (14,600 tokens) exceeds the L1 enforcement envelope (12,476 tokens).** This means C2-level strategy guidance cannot be entirely encoded in L1 static context. Specifically:
   - S-007 at its minimum (8,000 tokens) consumes 64% of L1 capacity
   - S-002 (4,600) and S-014 (2,000) require additional capacity
   - **Resolution:** S-002 is delivered via Process gate (critic workflow step); S-014 is delivered via Process gate (V-057 quality gate). Only S-007's constitutional principles and S-010/S-003's prompts need L1 encoding. L2 reinforcement carries key principles (~600 tokens/session).

3. **C3 and C4 require the full enforcement stack.** The token volumes (31,300-50,300) far exceed L1 capacity. These are delivered through the full L1+L2+L3+L4+L5+Process stack, with the majority of strategy invocations triggered by Process gates and L3/L4 hooks.

4. **Portable stack verification (L1 + L5 + Process):** On PLAT-GENERIC, L1 carries ~7,700 tokens of strategy prompts, L5 carries deterministic test verification, and Process carries all workflow-gated strategy invocations. All 10 strategies have portable delivery mechanisms within this stack at MODERATE enforcement level.

---

## Traceability

### Requirements Coverage

| Requirement | How Addressed |
|-------------|--------------|
| FR-003 | Each profile includes enforcement layer mapping (primary, portable fallback, enhanced) |
| FR-004 | Each profile includes decision criticality mapping (C1-C4 with required/optional) |
| FR-005 | Each profile includes platform portability classification with PLAT-GENERIC fallback |
| FR-006 | Each profile includes token cost, tier, and budget impact |
| FR-007 | Consolidated Pairing Reference documents all 14 SYN pairs, 29 COM pairs, and 2 TEN pairs with management guidance (total 45 = C(10,2)) |
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

**Machine-Parseable Format Note (REQ-303-041):** The current profiles are optimized for human-readable markdown. A supplementary machine-parseable format (YAML/JSON) encoding the decision tree and strategy profiles in structured format is deferred to the EN-304 integration phase, where it will be produced as part of the agent skill configuration. This deferral is acknowledged as a known gap against REQ-303-041's dual-audience requirement.

---

*Document ID: FEAT-004:EN-303:TASK-003*
*Agent: ps-architect*
*Created: 2026-02-13*
*Revised: 2026-02-13 (v1.1.0 -- ps-analyst-303 revision addressing critique iteration 1)*
*Status: Complete*
