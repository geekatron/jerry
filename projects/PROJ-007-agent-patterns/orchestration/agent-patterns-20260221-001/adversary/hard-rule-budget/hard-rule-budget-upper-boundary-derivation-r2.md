# HARD Rule Budget Upper Boundary Derivation

> **Criticality:** C4 (Critical) -- governance constraint affecting constitutional enforcement architecture
> **Quality Threshold:** >= 0.95
> **Created:** 2026-02-21
> **Status:** DRAFT (iteration 2)
> **Prior Score:** 0.90 (iteration 1) -- REVISE verdict
> **Revision Basis:** C4 tournament execution report (20260221T-C4T), 7 CRITICAL findings resolved

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | Derived upper boundary and recommendation |
| [Problem Statement](#problem-statement) | What we're solving and why |
| [Methodology](#methodology) | Three independent constraint families |
| [Constraint Family A: Token/Resource Budget](#constraint-family-a-tokenresource-budget) | L1 token capacity and signal quality |
| [Constraint Family B: Enforcement Coverage](#constraint-family-b-enforcement-coverage) | L2 re-injection capacity and L3-L5 compensating controls |
| [Constraint Family C: Instruction-Following Capacity](#constraint-family-c-instruction-following-capacity) | Empirical LLM constraint-tracking limits and rule conflict probability |
| [Synthesis: Binding Constraint Analysis](#synthesis-binding-constraint-analysis) | Which constraint family is the tightest |
| [Sensitivity Analysis](#sensitivity-analysis) | Robustness of the derived ceiling under parameter variation |
| [Rule Activation Profiles](#rule-activation-profiles) | Co-activation analysis by task type |
| [Recommendation](#recommendation) | Derived budget with rationale |
| [Draft Tier A/B Classification](#draft-tier-ab-classification) | Proposed classification of post-consolidation rules |
| [Exception Mechanism](#exception-mechanism) | Governance escalation path for ceiling expansion |
| [Implementation Path](#implementation-path) | How to get from 31 to the derived budget |
| [Evidence Index](#evidence-index) | Source traceability |

---

## Executive Summary

The current HARD rule ceiling of 35 was set retroactively without derivation. This analysis derives the upper boundary from three independent constraint families -- (A) Token/Resource Budget, (B) Enforcement Coverage, and (C) Instruction-Following Capacity -- encompassing five constituent analyses.

**Finding:** The binding constraint is **Enforcement Coverage** (Constraint Family B) -- the L2 re-injection engine currently processes only 8 markers from `quality-enforcement.md`, providing per-prompt emphasis for 10 distinct H-rules. An additional 8 L2-REINJECT markers exist in other auto-loaded rule files, providing structural emphasis for 17 more H-rules, but these are not processed by the engine. Combined with L3/L4/L5 compensating controls, the architecture supports meaningful enforcement across a broader set than the engine-processed L2 count alone suggests.

**Derived upper boundary: 25 HARD rules** (the maximum that can be meaningfully enforced given the current architecture), with the following allocation:

| Tier | Count | Enforcement Profile |
|------|-------|---------------------|
| Tier A: Full L2-protected (constitutional + quality) | 12 | Engine-processed L2 re-injection every prompt + L1 + L3/L4/L5 where applicable |
| Tier B: Structurally-emphasized (operational) | 13 | L1 session-start loading + structural L2 emphasis in auto-loaded files + L3/L5 compensating controls |
| **Total** | **25** | |

**Why 25 and not 14:** The binding constraint of ~14 engine-processed L2 rules establishes the Tier A count -- the number of rules with the highest enforcement reliability. The total of 25 is the operational capacity where Tier B rules still provide value above MEDIUM because they benefit from: (a) session-start loading with structural L2-REINJECT emphasis in their source files, (b) L3 deterministic gating (AST checks, immune to context rot), (c) L5 commit/CI verification (post-hoc, immune to context rot), and (d) domain partitioning that limits co-activation to 5-8 rules per interaction. Beyond 25, even these compensating controls cannot prevent aggregate enforcement degradation.

**On the coincidence of re-deriving 25:** The original designer set `<= 25` in EN-404 before any rules existed [E-009]. This derivation arrives at the same number through independent constraint analysis. We address this directly: the coincidence is explained by the fact that both analyses operate on the same underlying system constraints (200K context window, L2 token budget, human/LLM cognitive limits). The original designer's intuition was directionally correct. This derivation provides the principled justification that the original lacked. If the constraints had yielded 22 or 28, we would have reported that number instead.

---

## Problem Statement

The HARD rule budget in `quality-enforcement.md` currently states `<= 35`. This ceiling:

1. **Has no derivation.** It was set retroactively in commit `936d61c` to accommodate the existing count (31) plus headroom (4). No calculation, empirical analysis, or design rationale was recorded. [E-010]
2. **Has already been breached once.** The original ceiling of `<= 25` was silently exceeded when H-25..H-30 were added without updating the cap.
3. **Is about to be exhausted.** PROJ-007 proposes H-32..H-35, consuming the remaining 4 slots (100% utilization at 35/35).
4. **Determines system-level enforcement quality.** Every HARD rule competes for attention budget (token budget, LLM attention weight, L2 re-injection capacity). An unprincipled ceiling either over-constrains (blocking legitimate governance additions) or under-constrains (allowing enforcement quality to degrade).

**Question:** What is the principled upper boundary for HARD rules, derived from the actual constraints of the enforcement architecture?

**Constitutional context (P-020):** Changing the HARD rule ceiling is a governance change that directly affects all framework users' ability to add HARD rules. Per P-020 (User Authority), this change requires explicit user authorization and cannot be imposed unilaterally. This derivation provides the analytical basis; the decision to adopt the ceiling remains with the governance authority.

---

## Methodology

### Constraint Family Structure

The original iteration 1 analysis identified five constraints and claimed independence. Tournament review (IN-001, SR-001) correctly identified that three of the five are proxies for the same underlying variable -- "cognitive budget" (the finite capacity of an LLM to attend to, recall, and comply with simultaneously-loaded instructions).

**Revised framing:** Three independent constraint families, each containing constituent analyses that share causal structure within the family but are independent across families.

| Family | Constituent Analyses | Independence Basis |
|--------|---------------------|-------------------|
| **A: Token/Resource Budget** | (1) Token Budget, (4) Signal Quality | Both measure resource consumption -- tokens are the physical budget, signal quality is the diminishing-returns curve of that budget |
| **B: Enforcement Coverage** | (2) L2 Re-injection Coverage | Measures the enforcement architecture's ability to protect rules against context rot -- an architectural property independent of token budget or LLM cognition |
| **C: Instruction-Following Capacity** | (3) Instruction-Following Research, (5) Rule Conflict Probability | Both measure the LLM's cognitive capacity to track and comply with multiple constraints -- the "cognitive budget" variable |

**Why three families are genuinely independent:**

- **A vs. B:** Token budget is a resource allocation problem (how many tokens can we spend on rules?). Enforcement coverage is an architecture problem (how does the enforcement engine protect rules against context rot?). A system could have ample token budget but poor enforcement coverage, or vice versa.
- **A vs. C:** Token budget measures how many rules fit in context. Instruction-following capacity measures how many rules the LLM can simultaneously comply with. A model could have a 1M-token context window but still fail at >10 simultaneous constraints.
- **B vs. C:** Enforcement coverage measures the architecture's rot-resistance. Instruction-following capacity measures the LLM's compliance capability. Perfect L2 re-injection does not help if the LLM cannot track 30 constraints; conversely, perfect instruction-following does not help if rules rot out of context.

The convergence of three independent families on the 20-25 range is meaningful because they measure different system properties. Within each family, constituent analyses corroborate each other but do not count as additional independent evidence.

---

## Constraint Family A: Token/Resource Budget

> Constituent analyses: Token Budget (formerly Constraint 1) + Signal Quality (formerly Constraint 4)

### Token Budget Analysis

#### Data

From ADR-EPIC002-002 [E-001] and current rule file measurements:

| Parameter | Value | Source |
|-----------|-------|--------|
| Total context window | 200,000 tokens | Claude model specification |
| L1 enforcement budget (target) | 12,476 tokens | ADR-EPIC002-002 [E-001] |
| L1 enforcement budget (current actual) | ~14,245 tokens | Measured from rule file sizes |
| Total enforcement budget | ~15,100 tokens (7.6%) | quality-enforcement.md SSOT |
| Critical max budget | ~17,000 tokens (8.5%) | ADR-EPIC002-002 [E-001] |
| Per-HARD-rule L1 cost | ~300-500 tokens | Measured (range across files) |
| Mean per-HARD-rule L1 cost | ~410 tokens | Computed from 14,245 tokens / ~35 content units (31 rules + file overhead) |

#### Analysis

The L1 budget of 12,476 tokens must accommodate:
- HARD rule definitions and context (~410 tokens/rule average)
- MEDIUM/SOFT standards (which share the same files)
- Section headers, navigation tables, metadata

Not all L1 tokens are consumed by HARD rules -- rule files contain MEDIUM and SOFT standards, examples, and explanatory text. Estimating HARD-rule-specific content at ~60% of file tokens:

**Effective HARD rule L1 budget:** 12,476 x 0.60 = ~7,486 tokens
**Max rules at 410 tokens/rule:** 7,486 / 410 = **~18 rules** (if L1 budget is the binding constraint)

However, this underestimates because:
- Some files are dense with HARD rules (quality-enforcement.md: 8 rules in 3,730 tokens = 466/rule)
- Some files carry mostly context (project-workflow.md: 1 rule in 737 tokens)
- Consolidation would reduce per-rule overhead

**Note on per-rule cost estimate (SR-002):** The 410 tokens/rule figure includes non-HARD content (MEDIUM/SOFT standards, metadata). The true HARD-specific cost may be 200-300 tokens/rule if file overhead is excluded. This is accounted for via the 60% ratio, which isolates HARD-specific content. See Sensitivity Analysis for the impact of varying this ratio.

**Token budget ceiling: ~30-40 rules** (at current overhead) or **~18-25 rules** (if HARD-rule-specific budget is isolated). This is a soft constraint -- it can be managed through rule consolidation and file optimization.

### Signal Quality Analysis

From nse-risk-001-risk-assessment.md [E-008] (PROJ-007):

```
Compliance
Quality
  ^
  |        .-----------
  |      ./
  |    ./
  |  ./        <- Sweet spot (~20-25 rules)
  |./
  +-----|---------|---------|---> Rule Count
       10       20        30
```

Key finding: "Beyond the sweet spot, each additional rule: (a) consumes ~400-500 tokens of L1 budget, (b) increases probability of rule conflicts (combinatorial growth), (c) increases cognitive load on agents, (d) reduces working context for actual deliverables."

Consolidation candidates identified: H-25..H-30 (6 rules) and H-07..H-09 (3 rules).

**Note on independence (SR-001):** The nse-risk-001 assessment was produced within the same project and may share epistemic biases with this derivation. Its "20-25 sweet spot" is treated as a corroborative data point within Family A (reinforcing the token budget analysis from a different angle), not as an independent constraint family. The original EN-404 design intent (`<= 25`) [E-009] is similarly a prior belief -- it was the designer's pre-empirical judgment, subsequently overridden in practice (commit 936d61c raised it to 35). We do not treat it as evidence of correctness, but note that the designer's intuition was directionally aligned with this analysis.

### Family A Verdict

Token budget alone suggests **25-40 rules** depending on consolidation. Signal quality analysis corroborates the **20-25 range**. Family A ceiling: **~25 rules.** This is **not the binding constraint** at current rule density, but it establishes an upper bound.

---

## Constraint Family B: Enforcement Coverage

> Constituent analysis: L2 Re-injection Coverage + L3-L5 Compensating Controls

### L2-REINJECT Marker Ecosystem -- Precise Inventory

The L2-REINJECT marker system operates at two levels, which must be clearly distinguished:

#### Level 1: Engine-Processed L2 (quality-enforcement.md only)

The prompt reinforcement engine (`prompt_reinforcement_engine.py`, line 243 [E-002]) reads L2-REINJECT markers from `quality-enforcement.md` only. These markers are injected into every prompt, providing the strongest defense against context rot.

| # | Rank | Declared Tokens | H-Rules Referenced | Content Summary |
|---|------|----------------|--------------------|-----------------|
| 1 | 1 | 50 | H-01, H-02, H-03 | Constitutional constraints (P-003, P-020, P-022) |
| 2 | 2 | 90 | H-13, H-14 | Quality gate threshold, creator-critic cycle |
| 3 | 2 | 50 | H-31 | Ambiguity clarification |
| 4 | 3 | 25 | H-05, H-06 | UV-only Python |
| 5 | 4 | 30 | *(S-014 strategy)* | LLM-as-Judge leniency bias counteraction |
| 6 | 5 | 30 | H-15 | Self-review before presenting |
| 7 | 6 | 100 | *(Criticality levels)* | C1-C4 levels, AE-002, AE-001/AE-004 |
| 8 | 8 | 40 | H-19 | Governance escalation per AE rules |
| | **Total** | **415** | **10 distinct H-rules** | |

**Key distinction (CV-001 resolution):** There are **8 markers** and **10 distinct H-rules** referenced. These are different counts measuring different things. The engine processes 8 markers; those 8 markers provide L2 emphasis for 10 H-rules. Markers 5 and 7 reference strategies/concepts rather than specific H-rules, but marker 7 implicitly covers H-19 via the AE escalation rules.

**L2 budget utilization:** 415 of 600 declared tokens = 69% utilization. Remaining capacity: ~185 tokens = ~3-4 additional markers at ~50 tokens each. **Maximum engine-processed L2 H-rule coverage: ~14 rules** (10 current + ~4 additional).

#### Level 2: Structurally-Emphasized L1 (other auto-loaded rule files)

Eight additional L2-REINJECT markers exist in other auto-loaded rule files. The prompt reinforcement engine does NOT process these markers. However, because these files are auto-loaded into L1 context at session start via `.claude/rules/` symlinks, the L2-REINJECT HTML comment structure provides structural emphasis within the L1 context window -- the content is present and formatted distinctly, even though it is not re-injected per-prompt.

| # | File | Rank | Declared Tokens | H-Rules Referenced |
|---|------|------|----------------|--------------------|
| 1 | architecture-standards.md | 4 | 60 | H-07, H-08, H-09, H-10 |
| 2 | coding-standards.md | 7 | 60 | H-11, H-12 |
| 3 | testing-standards.md | 5 | 40 | H-20, H-21 |
| 4 | mandatory-skill-usage.md | 6 | 50 | H-22 |
| 5 | markdown-navigation-standards.md | 7 | 25 | H-23, H-24 |
| 6 | skill-standards.md | 7 | 70 | H-25, H-26, H-27, H-28, H-29, H-30 |
| 7 | python-environment.md | 3 | 50 | H-05, H-06 *(duplicate of QE marker 4)* |
| 8 | mcp-tool-standards.md | 9 | 70 | MCP-001, MCP-002 *(file-scoped, not H-rules)* |
| | **Total** | | **425** | **17 additional H-rules** (plus H-05/H-06 duplicated) |

#### Combined L2-REINJECT Coverage Summary

| Metric | Count | Details |
|--------|-------|---------|
| Total L2-REINJECT markers | **16** | 8 engine-processed + 8 structurally-emphasized |
| Total declared tokens | **840** | 415 (engine) + 425 (structural) |
| Files containing markers | **9** | quality-enforcement.md + 8 other rule files |
| H-rules with engine-processed L2 | **10** | H-01..H-03, H-05, H-06, H-13..H-15, H-19, H-31 |
| H-rules with structural L2 emphasis only | **17** | H-07..H-12, H-20..H-30 |
| H-rules with ANY L2 emphasis | **27** | 10 + 17 (H-05/H-06 counted once) |
| H-rules with NO L2 emphasis | **4** | H-04, H-16, H-17, H-18 |

**(CV-002 resolution):** The engine limitation (reading only `quality-enforcement.md`) is an **implementation gap**, not an **architectural constraint**. If the engine were updated to read all 9 files containing L2-REINJECT markers, the L2 budget would need to increase from 600 to ~840+ tokens (a 40% increase), but the architectural capacity for L2-protected rules would jump from 10 to 27. This is a tractable engineering change, not a fundamental limitation. The derivation proceeds based on the **current** engine implementation as the binding constraint, while noting this implementation gap as a future expansion path.

### L3-L5 Compensating Controls Analysis

The enforcement architecture has five layers (ADR-EPIC002-002 [E-001]). The iteration 1 derivation focused on L1 and L2 but did not analyze how L3, L4, and L5 compensate for L1/L2 limitations. This is relevant because a rule enforced by L3 or L5 may be effectively "HARD" even without L2 re-injection.

| Layer | Timing | Context Rot Vulnerability | Applicable Rules | Mechanism |
|-------|--------|---------------------------|-----------------|-----------|
| L1 | Session start | VULNERABLE (CRR 1-2) | All 31 H-rules | Auto-loaded rule files |
| L2 | Every prompt | IMMUNE | 10 H-rules (engine-processed) | Prompt reinforcement engine |
| L3 | Before tool calls | IMMUNE | H-05, H-06 (UV gating), H-10 (file structure) | AST/deterministic gating |
| L4 | After tool calls | MIXED | H-11, H-12 (type hints/docstrings via linting) | Output inspection |
| L5 | Commit/CI | IMMUNE | H-20, H-21 (test/coverage), H-11, H-12 (mypy/ruff) | Post-hoc verification |

**Key insight:** Rules enforced by L3 or L5 are protected against context rot regardless of L1/L2 status, because these layers use deterministic checks that do not depend on the LLM's context window. The "effectively MEDIUM" characterization of L1-only rules (iteration 1, line 140) is **overstated** for rules that have L3/L5 coverage.

**Revised enforcement reliability tiers:**

| Enforcement Profile | Rules | Rot Resistance |
|---------------------|-------|----------------|
| L2 + L1 + (L3/L4/L5 where applicable) | 10 H-rules | Highest -- survives full context rot |
| L1 + L3/L5 (no engine L2, but deterministic backup) | H-05, H-06, H-10, H-11, H-12, H-20, H-21 (7 rules) | High -- deterministic enforcement even if LLM forgets |
| L1 + structural L2 emphasis (no engine L2, no L3/L5) | Remaining Tier B rules | Moderate -- L1 session-start + structural emphasis, degrades under context pressure |
| L1 only (no L2 marker, no L3/L5) | H-04, H-16, H-17, H-18 (4 rules) | Lowest -- fully vulnerable to context rot |

### Family B Verdict

**If all HARD rules require engine-processed L2 protection:** Upper bound is **~14 rules** (10 current + ~4 additional within L2 budget).

**If a tiered model is acceptable:** The architecture supports meaningful enforcement for **25+ rules** through a combination of engine-processed L2 (10 rules), structural L2 + L3/L5 deterministic backup (7 rules), and structural L2 emphasis (remaining rules). The four rules with no L2 marker at all (H-04, H-16, H-17, H-18) are the genuinely vulnerable set -- and all four are candidates for either L2 marker addition or MEDIUM reclassification.

**This is the binding constraint for Tier A allocation** (12-14 rules maximum with engine-processed L2), but **not the binding constraint for total HARD rule count** when compensating controls are considered.

---

## Constraint Family C: Instruction-Following Capacity

> Constituent analyses: Instruction-Following Research (formerly Constraint 3) + Rule Conflict Probability (formerly Constraint 5)

### Instruction-Following Research

#### Data

| Study | Finding | Confidence |
|-------|---------|------------|
| ManyIFEval (arXiv:2509.21051, 2025) [E-004] | 5 simultaneous instructions: 32-72% accuracy. 10 instructions: 2-39% accuracy. | High (peer-reviewed) |
| AGENTIF (arXiv:2505.16944, NeurIPS 2025) [E-005] | 11.9 constraints avg: <30% perfect compliance across all models. Best model (o1-mini): 59.8% constraint success rate. | High (NeurIPS Spotlight) |
| Control Illusion (arXiv:2502.15851, 2025) [E-006] | Claude 3.5 system prompt adherence under conflict: 29.9%. Larger models show no consistent advantage. | High (peer-reviewed) |
| Lost in the Middle (Liu et al., TACL 2024) [E-007] | Middle-positioned information in long contexts degrades significantly. U-shaped recall curve. | High (TACL publication) |

#### Analysis

These studies measure instruction-following fidelity in general-purpose tasks. A critical distinction for Jerry:

- **31 HARD rules in rule files** does NOT equal 31 simultaneously active constraints per interaction
- In practice, a given interaction activates a subset of rules based on task type (see [Rule Activation Profiles](#rule-activation-profiles) below)
- The L2 re-injection architecture selectively emphasizes the most critical 8 markers per prompt
- The Jerry enforcement architecture has structural mitigations (L2 re-injection, L3 deterministic gating, domain partitioning) specifically designed to overcome the limitations these studies document

**Applicability caveat (PM-004):** The ManyIFEval and AGENTIF data measure general-purpose instruction following, not compliance within a purpose-built enforcement system with L2 re-injection and L3 deterministic gating. The Jerry architecture partially compensates for the limitations these studies identify. The research data therefore represents a **conservative lower bound** on Jerry's effective constraint capacity, not a direct measurement. We use it as such -- as a constraint rather than a prediction.

**Implication for L2-protected rules:** The 10-12 rules with engine-processed L2 re-injection are within the 5-10 range where compliance is still meaningful (32-72% per ManyIFEval). The L2 re-injection mechanism re-injects compressed summaries (~50 tokens each), not full constraint specifications. Whether compressed re-injections achieve the same compliance as full specifications is untested (DA-002), but the compression preserves the critical trigger words (MUST, NEVER, REQUIRED) that drive compliance.

**Implication for L1-only rules:** Rules without engine-processed L2 re-injection compete for attention with the entire context. As context fills toward 200K, these rules experience attention dilution [E-011] and positional degradation [E-007]. Their effective enforcement probability degrades from "high" (early session) to "moderate" (late session under context pressure) -- but this is partially offset by L3/L5 compensating controls for applicable rules, and by structural L2 emphasis in auto-loaded files.

### Rule Conflict Probability

The number of potential pairwise interactions between N rules is N(N-1)/2:

| Rule Count | Pairwise Interactions | Relative to 20 rules |
|------------|----------------------|---------------------|
| 15 | 105 | 0.55x |
| 20 | 190 | 1.0x (baseline) |
| 25 | 300 | 1.58x |
| 30 | 435 | 2.29x |
| 35 | 595 | 3.13x |

**Qualification (SR-003):** This combinatorial analysis is theoretical. The three observed conflicts (H-16/H-14 tension, H-20/rapid-prototyping tension, H-25..H-30 internal overlap) are anecdotal rather than systematic. The formula overstates actual conflict risk because rules in the same domain file are more likely to interact than rules across domains, and most rule pairs are semantically non-overlapping. However, the combinatorial growth rate is real: at 35 rules the interaction surface (595 pairs) is 3.1x larger than at 20, and no formal conflict resolution mechanism exists.

### Family C Verdict

Research supports **10-12 simultaneously-enforced constraints** as the practical ceiling for reliable compliance in general-purpose LLM tasks. With Jerry-specific mitigations (L2 re-injection, domain partitioning, L3/L5 deterministic checks), the effective ceiling is higher but not unbounded. Total HARD rule count can exceed the simultaneous-enforcement ceiling if rules are domain-partitioned (not all active simultaneously), but **beyond ~25 total rules, even domain partitioning cannot prevent attention dilution from degrading the full set.** Rule conflict probability reinforces this: the conflict surface at 25 rules (300 pairs) is manageable; at 35 (595 pairs) it is not, absent formal conflict resolution.

---

## Synthesis: Binding Constraint Analysis

| Constraint Family | Derived Ceiling | Binding? |
|-------------------|-----------------|----------|
| A: Token/Resource Budget | 25-40 (with consolidation) | No -- manageable through optimization |
| B: Enforcement Coverage | 14 (engine-processed L2) / 25+ (with compensating controls) | **Yes -- for Tier A allocation (12-14 rules)** |
| C: Instruction-Following Capacity | 10-12 simultaneous, ~25 total with partitioning | **Yes -- for total count** |

**Two ceilings emerge:**

1. **Tier A ceiling (engine-processed L2, highest enforcement reliability): 12-14 rules.** These are the rules that survive full context rot because they are re-injected every prompt by the engine. This is determined by the L2 token budget (600 tokens, 415 currently used, ~185 remaining = ~3-4 additional slots).

2. **Total ceiling (all HARD rules including Tier B): 25 rules.** This is the convergence point of Family A (token budget: 25-40), Family B (compensating controls: 25+), and Family C (partitioned instruction-following: ~25). Beyond this number, enforcement quality degrades across all three families simultaneously.

**Resolution of the 14-vs-25 gap (DA-001):** The binding constraint of ~14 gives us the **Tier A count** -- the number of rules with the highest enforcement guarantee (engine-processed L2 re-injection). This does not mean rules 15-25 are "effectively MEDIUM." Tier B rules are enforced through a different mechanism portfolio:

| Enforcement Mechanism | Tier A | Tier B |
|----------------------|--------|--------|
| L1 session-start loading | Yes | Yes |
| Engine-processed L2 re-injection (per-prompt) | **Yes** | No |
| Structural L2 emphasis in auto-loaded file | Yes (redundant) | **Yes** (17 of ~13 Tier B rules) |
| L3 deterministic gating (where applicable) | Some | **Some** (H-05/H-06 UV, H-10 file structure) |
| L4 output inspection (where applicable) | Some | **Some** (H-11/H-12 linting) |
| L5 commit/CI verification (where applicable) | Some | **Some** (H-20/H-21 tests/coverage) |

Tier B rules are not "MEDIUM relabeled as HARD." They are HARD rules with a different -- and for some rules, equally robust -- enforcement profile. A Tier B rule with L3 deterministic gating (e.g., H-05 UV-only Python) is arguably MORE reliably enforced than a Tier A rule with only L2 re-injection, because L3 gating is immune to context rot and operates deterministically.

The honest statement is: Tier A rules have the broadest enforcement coverage (L1+L2+L3/L4/L5). Tier B rules have narrower but still meaningful enforcement (L1+structural-L2+L3/L5 where applicable). Only the 4 rules with no L2 marker and no L3/L5 coverage (H-04, H-16, H-17, H-18) are genuinely vulnerable -- and these should be prioritized for either L2 marker addition or reclassification.

---

## Sensitivity Analysis

The derived ceiling of 25 depends on several key assumptions. This section tests robustness by varying each assumption by +/-20%.

### Parameter Sensitivity

| Parameter | Base Value | -20% | +20% | Ceiling Impact |
|-----------|-----------|------|------|----------------|
| HARD content ratio (Constraint A) | 60% | 48% | 72% | At 48%: ~14.6 rules (token budget becomes binding at ~15). At 72%: ~22 rules. **Sensitive.** |
| Mean per-rule L1 cost | 410 tokens | 328 tokens | 492 tokens | At 328: ~22.8 rules. At 492: ~15.2 rules. **Sensitive** (but offset by consolidation). |
| L2 per-marker cost | ~50 tokens | 40 tokens | 60 tokens | At 40: ~4-5 additional Tier A slots. At 60: ~3 additional Tier A slots. **Low sensitivity** (changes Tier A by +/-1). |
| L2 total budget | 600 tokens | 480 tokens | 720 tokens | At 480: ~1-2 additional Tier A slots. At 720: ~6 additional Tier A slots (up to 16 Tier A). **Moderate sensitivity.** |
| Simultaneous active rules per task | 5-8 | 4-6 | 6-10 | At 4-6: more headroom, total ceiling could increase to ~28. At 6-10: ceiling decreases to ~22. **Moderate sensitivity.** |

### Scenario Analysis

| Scenario | Assumptions | Derived Ceiling |
|----------|-------------|-----------------|
| **Conservative** (-20% on favorable assumptions) | 48% HARD ratio, 492 tokens/rule, 6-10 co-active | **20 rules** (token budget becomes binding) |
| **Base Case** | 60% HARD ratio, 410 tokens/rule, 5-8 co-active | **25 rules** |
| **Optimistic** (+20% on favorable assumptions) | 72% HARD ratio, 328 tokens/rule, 4-6 co-active | **28 rules** |
| **Engine L2 expansion** (all 16 markers processed) | Base + L2 reads all 9 files, budget 840 tokens | **25 rules** (total unchanged, but Tier A expands to ~20) |

**Interpretation:** The derived ceiling is robust within the **20-28 range**. The base case of 25 is the center of this range. The conservative scenario (20) would require more aggressive consolidation. The optimistic scenario (28) would provide more headroom. The recommendation of 25 is defensible under all but the most conservative parameter assumptions.

**Key finding:** The ceiling is most sensitive to the HARD content ratio and per-rule L1 cost. Both of these can be reduced through rule consolidation (which reduces per-rule overhead) and file optimization (which increases the HARD content ratio). This means the ceiling is partially within engineering control, not a fixed external constraint.

---

## Rule Activation Profiles

The instruction-following research (Family C) establishes that **simultaneously active** constraints, not total defined constraints, determine compliance quality. This section profiles which rules co-activate by task type.

| Task Type | Activated Rules | Co-Active Count | Within 10-12 Ceiling? |
|-----------|----------------|-----------------|----------------------|
| **Coding (Python implementation)** | H-05, H-06 (UV), H-07..H-10 (architecture), H-11, H-12 (code quality), H-20, H-21 (testing) | 10 | Yes (at ceiling) |
| **Governance (rule/ADR change)** | H-01..H-03 (constitutional), H-13..H-15 (quality), H-16 (steelman), H-17 (scoring), H-18 (compliance), H-19 (escalation), H-31 (ambiguity) | 10 | Yes (at ceiling) |
| **Skill development** | H-23, H-24 (navigation), H-25..H-30 (skill standards), H-11, H-12 (code quality) | 10 | Yes (at ceiling) |
| **Document/analysis writing** | H-13..H-15 (quality), H-23, H-24 (navigation), H-31 (ambiguity) | 6 | Yes (well within) |
| **Orchestration/workflow** | H-01..H-03 (constitutional), H-13, H-14 (quality), H-22 (skill invocation), H-31 (ambiguity) | 7 | Yes (within) |

**Observations:**
1. Maximum co-activation is **10 rules** across all profiled task types -- at the ceiling identified by ManyIFEval/AGENTIF research.
2. No task type activates more than 10 rules, confirming that domain partitioning keeps co-activation within the research-supported range.
3. The 25 total rules can be organized so that no single task type exceeds the 10-12 simultaneous constraint ceiling.
4. The Tier A rules (constitutional + quality: H-01..H-03, H-13..H-15, H-19, H-31) appear across multiple task types, justifying their L2 protection priority.

---

## Recommendation

### Derived Budget: 25 HARD Rules (Two-Tier Allocation)

| Tier | Allocation | Enforcement Profile | Purpose |
|------|-----------|---------------------|---------|
| **Tier A: Constitutional** | 12 rules | Engine-processed L2 re-injection + L1 + L3/L4/L5 where applicable | Rules whose violation causes irreversible or systemic harm (P-003, P-020, P-022, quality gates, governance escalation) |
| **Tier B: Operational** | 13 rules | L1 session-start + structural L2 emphasis + L3/L5 where applicable | Rules whose violation is costly but recoverable, and/or are enforced by deterministic L3/L5 controls (coding standards, testing standards, skill standards) |
| **Total** | **25** | | |

### Tier Assignment Criteria

| Criterion | Tier A | Tier B |
|-----------|--------|--------|
| Violation reversibility | Irreversible or systemic cascade | Costly but recoverable within 1 day |
| Enforcement dependency | Requires per-prompt LLM awareness (no L3/L5 backup) | Has L3/L5 deterministic backup OR is domain-specific |
| Cross-task activation | Activated across 3+ task types | Activated in 1-2 task types |
| Constitutional reference | References P-series principles | References operational standards |

### What This Means for the Current 31 Rules

A net reduction of 6 rules is required, achievable through consolidation:

| Consolidation | Before | After | Savings | L3 Impact |
|---------------|--------|-------|---------|-----------|
| H-25..H-30 (skill standards) | 6 | 2 compound rules | -4 | **No L3 impact** -- skill standards are enforced via L1/L2/L4 (structural review), not L3 AST checks |
| H-07..H-09 (architecture layers) | 3 | 1 compound rule | -2 | **No L3 impact** -- architecture layer rules are enforced via L1/L2/L4 (import review), not L3 AST checks. Note: if L3 AST gating is added for import enforcement in the future, individual rules should be un-consolidated. |
| **Net** | | | **-6 (31 -> 25)** | |

**(PM-001 resolution):** Consolidation is proposed ONLY for rules that are NOT enforced via L3 AST gating. The H-25..H-30 skill standards and H-07..H-09 architecture layer rules are enforced through L1 loading (LLM reads and follows them), L2 structural emphasis (markers in auto-loaded files), and L4 output inspection (structural review). They do not have L3 AST enforcement today. Compound rules are compatible with L1/L2/L4 enforcement because the LLM reads the full rule text regardless of whether it is one rule or six.

Rules that ARE enforced by L3 deterministic gating (e.g., H-05/H-06 UV checks) MUST remain as individual HARD rules, because L3 checks operate on specific patterns and cannot parse compound English sentences.

### What This Means for PROJ-007's H-32..H-35

H-32..H-35 cannot be added without first consolidating to create headroom. The sequence:
1. Consolidate H-25..H-30 (save 4 slots)
2. Consolidate H-07..H-09 (save 2 slots)
3. Current count: 25 (6 freed)
4. Add H-32..H-35 (consume 4 slots)
5. Post-addition count: 29 -- **over the 25 ceiling by 4**

**Resolution (selected option):** Consolidate H-32..H-35 into 2 compound rules (4 -> 2), yielding a final count of **27**. Apply the [Exception Mechanism](#exception-mechanism) for a temporary ceiling expansion of 25 + 2 = 27 for a 3-month consolidation period, during which additional consolidation elsewhere must reduce the total back to 25. Alternatively, classify 2 of the 4 proposed rules as MEDIUM with documented justification if they do not meet Tier A or Tier B criteria. **The specific resolution should be decided during PROJ-007 implementation based on the actual content of H-32..H-35.**

### What This Means for the "35 Slot" Ceiling

**The 35 ceiling should be replaced with the 25 ceiling**, with explicit two-tier allocation documented in `quality-enforcement.md`. The Tier Vocabulary table should read:

| Tier | Max Count | Enforcement Profile |
|------|-----------|---------------------|
| **HARD (Tier A)** | <= 12 | Engine-processed L2 + L1 + L3/L4/L5 |
| **HARD (Tier B)** | <= 13 | L1 + structural L2 + L3/L5 where applicable |
| **HARD (Total)** | <= 25 | (subject to [Exception Mechanism](#exception-mechanism)) |
| **MEDIUM** | Unlimited | None |
| **SOFT** | Unlimited | None |

---

## Draft Tier A/B Classification

Based on the tier assignment criteria above, here is the proposed classification of the 25 post-consolidation rules:

### Tier A: Constitutional (12 rules) -- Engine-Processed L2

| # | Rule | Rationale | Current L2 Status |
|---|------|-----------|-------------------|
| 1 | H-01 (No recursive subagents) | Constitutional (P-003), irreversible hierarchy violation | Has L2 (rank 1) |
| 2 | H-02 (User authority) | Constitutional (P-020), irreversible trust violation | Has L2 (rank 1) |
| 3 | H-03 (No deception) | Constitutional (P-022), irreversible trust violation | Has L2 (rank 1) |
| 4 | H-04 (Active project required) | Session-level gate, no L3/L5 backup, cross-task | Needs L2 marker added |
| 5 | H-05 (UV for execution) | Constitutional tool constraint, cross-task; note: also has L3 backup | Has L2 (rank 3) |
| 6 | H-06 (UV for deps) | Constitutional tool constraint, cross-task; note: also has L3 backup | Has L2 (rank 3) |
| 7 | H-13 (Quality threshold) | Quality framework foundation, cross-task | Has L2 (rank 2) |
| 8 | H-14 (Creator-critic cycle) | Quality framework foundation, cross-task | Has L2 (rank 2) |
| 9 | H-15 (Self-review) | Quality framework foundation, cross-task | Has L2 (rank 5) |
| 10 | H-19 (Governance escalation) | Governance gate, irreversible if missed | Has L2 (rank 8) |
| 11 | H-22 (Proactive skill invocation) | Cross-task workflow, no L3/L5 backup | Needs L2 marker added (uses structural L2 in mandatory-skill-usage.md) |
| 12 | H-31 (Clarify when ambiguous) | Cross-task quality, irreversible wrong-direction work | Has L2 (rank 2) |

**L2 budget impact:** 10 of 12 Tier A rules already have engine-processed L2 markers. Adding H-04 and H-22 requires ~100 additional tokens, bringing the L2 budget to ~515 of 600 tokens (86% utilization). This is within budget.

### Tier B: Operational (13 rules) -- Structural L2 + L3/L5

| # | Rule | Enforcement Backup | Structural L2? |
|---|------|--------------------|----------------|
| 1 | H-07+H-08+H-09 (Architecture layers -- consolidated) | L4 import review | Yes (architecture-standards.md) |
| 2 | H-10 (One class per file) | L3/L4 (file structure check) | Yes (architecture-standards.md) |
| 3 | H-11 (Type hints) | L5 (mypy) | Yes (coding-standards.md) |
| 4 | H-12 (Docstrings) | L5 (ruff) | Yes (coding-standards.md) |
| 5 | H-16 (Steelman before critique) | L1 only | No -- **candidate for L2 marker** |
| 6 | H-17 (Quality scoring) | L1 only | No -- **candidate for L2 marker** |
| 7 | H-18 (Constitutional compliance check) | L1 only | No -- **candidate for L2 marker** |
| 8 | H-20 (Test before implement) | L5 (pytest) | Yes (testing-standards.md) |
| 9 | H-21 (90% line coverage) | L5 (coverage) | Yes (testing-standards.md) |
| 10 | H-23 (Navigation table) | L4 (structural review) | Yes (markdown-navigation-standards.md) |
| 11 | H-24 (Anchor links) | L4 (structural review) | Yes (markdown-navigation-standards.md) |
| 12 | H-25+H-26+H-27 (Skill naming/structure -- consolidated) | L4 (structural review) | Yes (skill-standards.md) |
| 13 | H-28+H-29+H-30 (Skill description/paths/registration -- consolidated) | L4 (structural review) | Yes (skill-standards.md) |

**Vulnerability assessment:** Only 3 Tier B rules (H-16, H-17, H-18) have no L2 marker AND no L3/L5 deterministic backup. These are the genuinely vulnerable rules. All three relate to quality process compliance (steelman ordering, scoring requirement, constitutional check) -- they are procedural rules that could benefit from either L2 marker addition or consolidation into a single "quality process" compound rule.

---

## Exception Mechanism

> Resolves RT-001: ceiling weaponization risk

A hard ceiling without an override creates a governance vulnerability where the ceiling can be used to indefinitely block legitimate new HARD rules. The following exception mechanism provides a controlled escape valve.

### Temporary Ceiling Expansion

| Element | Specification |
|---------|---------------|
| **Trigger** | A C4 governance review determines that a new HARD rule is necessary AND no consolidation or demotion can create headroom within the current ceiling |
| **Authorization** | Requires explicit approval from the governance authority (P-020 user authority) via a C4-reviewed ADR |
| **Expansion Limit** | Ceiling + N (where N <= 3) for a maximum of 3 months |
| **Consolidation Deadline** | The expansion ADR MUST include a specific consolidation plan to return to the base ceiling within the 3-month window |
| **Enforcement** | If the deadline passes without consolidation, the expansion ADR is revoked and the expanded rules must be consolidated or demoted to MEDIUM |
| **Tracking** | Expansion status tracked in `quality-enforcement.md` Tier Vocabulary table with expiration date |
| **Non-Stacking** | Only one expansion can be active at a time. A new expansion requires first resolving the existing one. |

### Permanent Ceiling Revision

If the constraint analysis fundamentally changes (e.g., the L2 engine is expanded to read all 9 files, or the context window doubles to 400K), the ceiling itself should be re-derived via a new C4 analysis using this same methodology. The ceiling is derived from system constraints, not policy preference -- if the constraints change, the ceiling should change.

---

## Implementation Path

| Step | Action | Criticality | Dependencies |
|------|--------|-------------|--------------|
| 1 | Consolidate H-25..H-30 into 2 compound rules (naming/structure + description/paths/registration) | C3 (AE-002) | None |
| 2 | Consolidate H-07..H-09 into 1 compound rule (architecture layer isolation) | C3 (AE-002) | None |
| 3 | Classify all 25 remaining rules into Tier A / Tier B per the draft classification above | C3 (AE-002) | Steps 1-2 |
| 4 | Add L2-REINJECT markers for H-04 and H-22 in quality-enforcement.md | C3 | Step 3 |
| 5 | Update quality-enforcement.md: ceiling 35 -> 25, add two-tier table with exception mechanism | C3 (AE-002) | Steps 3-4 |
| 6 | Add PROJ-007 rules (H-32..H-35) within the new budget, using consolidation + exception mechanism as needed | C3 (AE-002) | Step 5 |
| 7 | Update HARD rule index to reflect consolidation and new tier assignments | C3 (AE-002) | Step 6 |

**Rollback path (PM-006):** If the 25-rule ceiling proves too restrictive after adoption, the Exception Mechanism provides the first safety valve (temporary expansion). If the exception mechanism is exercised more than twice in 6 months, this signals that the ceiling should be re-derived with updated parameters (likely raising it to ~28 based on the optimistic sensitivity scenario). The consolidation steps (1-2) are reversible by un-consolidating compound rules back to individual rules, though this would require a ceiling adjustment.

---

## Evidence Index

| ID | Source | Content | Confidence | File Path |
|----|--------|---------|------------|-----------|
| E-001 | ADR-EPIC002-002 | Token budget: L1=12,476, L2=600, total=~15,100 | High (baselined ADR) | `docs/design/adr/ADR-EPIC002-002-enforcement-architecture.md` |
| E-002 | prompt_reinforcement_engine.py | Engine reads only quality-enforcement.md L2 markers (line 243, `_find_rules_path` method) | High (source code) | `src/infrastructure/internal/enforcement/prompt_reinforcement_engine.py` |
| E-003 | L2-REINJECT marker inventory | 16 markers across 9 files: 8 engine-processed (quality-enforcement.md, covering 10 H-rules) + 8 structurally-emphasized (8 other files, covering 17 additional H-rules) | High (file scan, verified 2026-02-21) |
| E-004 | ManyIFEval (arXiv:2509.21051, 2025) | 5 instructions: 32-72%, 10 instructions: 2-39% | High (peer-reviewed) |
| E-005 | AGENTIF (arXiv:2505.16944, NeurIPS 2025) | 11.9 constraints: <30% perfect compliance | High (NeurIPS Spotlight) |
| E-006 | Control Illusion (arXiv:2502.15851, 2025) | Claude 3.5 system prompt adherence: 29.9% under conflict | High (peer-reviewed) |
| E-007 | Lost in the Middle (Liu et al., TACL 2024) | Middle-positioned information degrades in long contexts | High (TACL publication) |
| E-008 | nse-risk-001-risk-assessment.md | "20-25 sweet spot" diminishing returns curve | Medium (agent judgment, same-project, potential epistemic correlation) |
| E-009 | EN-404 deliverable-003 | Original `<= 25` ceiling with "scarcity preserves signal" rationale | Medium (design intent, subsequently overridden) |
| E-010 | Commit 936d61c | Ceiling update from 25 to 35 associated with H-31 addition | High (git evidence) |
| E-011 | ADOR (Xiao et al., OpenReview 2024) | Attention dilution: softmax normalization distributes weight across all tokens | Emerging (formal literature) |
| E-012 | ADR-EPIC002-002 R-SYS-004 | 82.5% of enforcement budget in L1 (VULNERABLE layer) = RED risk score 16 | High (baselined ADR) |
| E-013 | L2-REINJECT structural analysis (new) | 8 non-engine L2 markers in auto-loaded files provide structural emphasis for 17 H-rules not covered by engine-processed L2 | High (file scan, verified 2026-02-21) |
| E-014 | L3-L5 enforcement layer analysis (new) | L3 (AST gating) covers H-05, H-06, H-10; L5 (CI) covers H-11, H-12, H-20, H-21 -- all immune to context rot | High (architecture analysis) |

---

## Revision Log

| Iteration | Date | Score | Key Changes |
|-----------|------|-------|-------------|
| 1 | 2026-02-21 | 0.90 (REVISE) | Initial derivation with 5-constraint methodology |
| 2 | 2026-02-21 | *(pending scoring)* | Resolved 7 CRITICAL findings: reframed constraint independence (IN-001), justified 14-vs-25 gap with compensating controls analysis (DA-001), added L2 marker precision tables (CV-001/CV-002/FM-001), distinguished engine-processed vs. structural L2 (CV-002), added consolidation L3 feasibility analysis (PM-001), added exception mechanism (RT-001). Added sensitivity analysis, rule activation profiles, draft Tier A/B classification, L3-L5 compensating controls, P-020 reference, implementation path resolution. |
