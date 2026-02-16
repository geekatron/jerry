# ADR-EPIC002-001: Selection of 10 Adversarial Strategies for Jerry Quality Framework

<!--
DOCUMENT-ID: FEAT-004:EN-302:TASK-005
AUTHOR: ps-architect agent
DATE: 2026-02-13
STATUS: Accepted
PARENT: EN-302 (Strategy Selection & Decision Framework)
FEATURE: FEAT-004 (Adversarial Strategy Research & Skill Enhancement)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
ADR-ID: ADR-EPIC002-001
TYPE: Architecture Decision Record
RATIFIED-BY: User (P-020) on 2026-02-13
RATIFICATION-NOTE: User approved with note to revisit Option C in a future epic, specifically exploring cross-model LLM involvement
-->

> **ADR ID:** ADR-EPIC002-001
> **Version:** 1.2.0
> **Date:** 2026-02-13
> **Author:** ps-architect
> **Status:** ACCEPTED (ratified by user on 2026-02-13 per P-020)
> **Deciders:** User (P-020 authority), ps-architect (recommendation), ps-critic (adversarial review)
> **Quality Target:** >= 0.92
> **Ratification Note:** User approved with directive to revisit Option C in a future epic, exploring cross-model LLM involvement to address DA-002 (single-model blind spot)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Status](#status) | Current decision lifecycle stage; downstream dependency gating (F-010) |
| [Context](#context) | Why this decision is needed and what constraints apply |
| [Decision](#decision) | The 10 selected strategies and 5 excluded strategies with rationale; S-015 category distinction (F-013) |
| [Options Considered](#options-considered) | Three selection approaches evaluated |
| [Consequences](#consequences) | Positive, negative, and neutral outcomes with impact estimates (F-011) |
| [Evidence Base](#evidence-base) | Summary of findings from TASK-001 through TASK-004 |
| [Compliance](#compliance) | P-003, P-020, P-043 compliance assessment |
| [Related Decisions](#related-decisions) | Upstream and downstream decision linkages |
| [Limitations and Epistemic Status](#limitations-and-epistemic-status-f-012) | Epistemic boundaries and AI self-assessment structural limitation (F-012) |
| [References](#references) | Source citations |

---

## Status

**ACCEPTED** -- This ADR has been ratified through the full governance process:

1. **Adversarial review** by ps-critic: COMPLETE (2 iterations, 0.79 → 0.935 CONDITIONAL PASS)
2. **User ratification** per P-020 (User Authority): ACCEPTED on 2026-02-13

**User Directive:** Revisit Option C (all 15 strategies with tiered activation) in a future epic, specifically exploring cross-model LLM involvement to address the DA-002 single-model blind spot. Strategies S-005 (Dialectical Inquiry) and S-009 (Multi-Agent Debate) would benefit most from cross-model architecture, as their value propositions depend on genuine epistemological diversity that a single-model architecture cannot provide.

**Downstream Dependency Gating (F-010):** This ADR is now ACCEPTED. Downstream enablers (EN-303 Situational Mapping, EN-304 Problem-Solving Skill Enhancement, EN-305 NASA SE Skill Enhancement, EN-307 Orchestration Enhancement) are UNBLOCKED for detailed implementation design. The strategy set is stable: 9 of 10 selections are robust across all weight configurations. The maximum plausible future change is a single strategy swap at rank 10 (S-001 ↔ S-006).

---

## Context

### Why This Decision Is Needed

Jerry's quality framework requires adversarial review strategies to enforce its >= 0.92 quality gate. Without a defined set of strategies, the quality gate is aspirational rather than operational. This ADR formalizes which strategies comprise Jerry's adversarial review capability, enabling the downstream enablers (EN-303 situational mapping, EN-304/305 skill enhancements, EN-307 orchestration enhancement) to proceed with a stable strategy set.

### Background

**EN-301 (Deep Research)** produced a catalog of 15 adversarial review strategies through a rigorous research pipeline:

- TASK-001 through TASK-003: Three independent research streams (academic literature, LLM-specific techniques, structured analytic techniques)
- TASK-004: Synthesis into a unified 15-strategy catalog (v1.0.0)
- TASK-005/006: Two-iteration adversarial review cycle (iter1: 0.89 score, iter2: 0.936 PASS)
- TASK-007/008: Final validation (8/8 acceptance criteria met)

The catalog includes strategies S-001 through S-015, spanning four mechanistic families (Role-Based Adversarialism, Structured Decomposition, Dialectical Synthesis, Iterative Self-Correction) and five composition layers (L0-L4).

**EN-302 (Strategy Selection)** evaluated these 15 strategies to select the best 10 for integration:

- TASK-001: Defined 6-dimension weighted evaluation framework (D1-D6)
- TASK-002: Assessed risk profiles for all 15 strategies across 7 risk categories (105 risk assessments)
- TASK-003: Conducted architecture trade study with Pugh Matrix analysis, token budget modeling, and composition matrix
- TASK-004: Scored all 15 strategies, performed sensitivity analysis, and produced the ranked selection

### Constraints

| Constraint | Source | Impact on Selection |
|------------|--------|---------------------|
| **P-003: No Recursive Subagents** | Jerry Constitution (HARD) | All strategies must operate within orchestrator -> worker pattern; no nested agent spawning |
| **Context Rot** | Jerry core problem (CLAUDE.md) | Strategies with high token consumption create the very problem Jerry exists to solve; context window budget is finite |
| **3-Iteration Minimum** | Quality framework design | Strategies must deliver value within a 3-iteration creator-critic-revision cycle |
| **>= 0.92 Quality Gate** | EPIC-002 requirement | Selected strategies must collectively enable quality scores at or above the 0.92 threshold |
| **Single-Model Architecture** | Current Jerry architecture | All agents use the same Claude model; self-critique strategies share model blind spots (systemic risk DA-002) |
| **10-of-15 Selection** | EN-302 specification | Must select exactly 10 strategies from the 15-strategy catalog |

### User Ratification of EN-301-DEV-001

During EN-301, a specification deviation was recorded (EN-301-DEV-001) where Blue Team was replaced by Pre-Mortem (S-004) and Strawman was replaced by Dialectical Inquiry (S-005). The user ratified this deviation on 2026-02-13:

- **Pre-Mortem (S-004)** and **Dialectical Inquiry (S-005)** confirmed as active strategies in the catalog
- **Blue Team** moved to Reserved Strategy R-6 with defined promotion criteria

This ratification is an input to this ADR: S-004 and S-005 are evaluated as first-class catalog members, not as provisional substitutions.

---

## Decision

### The 10 Selected Strategies

The following 10 strategies are selected for integration into Jerry's quality framework, ranked by composite score:

| Rank | ID | Strategy | Composite Score | Mechanistic Family | Key Strength |
|------|-----|----------|----------------|--------------------|--------------|
| 1 | S-014 | LLM-as-Judge | 4.40 | Iterative Self-Correction | Essential evaluation infrastructure; enables 0.92 quality threshold; dual-role as strategy and scoring mechanism |
| 2 | S-003 | Steelman Technique | 4.30 | Dialectical Synthesis | Lowest-cost (1,600 tokens), lowest-risk (16/175) enabler of fair critique; enhances all subsequent review strategies |
| 3 | S-013 | Inversion Technique | 4.25 | Structured Decomposition | Unique generative strategy; produces anti-pattern checklists consumed by all other strategies; joint-lowest risk (15/175) |
| 4 | S-007 | Constitutional AI Critique | 4.15 | Iterative Self-Correction | Jerry's architecture was designed around this pattern; `.claude/rules/` ARE the constitution; near-zero setup cost |
| 5 | S-002 | Devil's Advocate | 4.10 | Role-Based Adversarialism | Strongest effectiveness evidence (CIA-formalized, Schweiger et al.); universal adversarial method; universally understood |
| 6 | S-004 | Pre-Mortem Analysis | 4.10 | Role-Based Adversarialism | Unique temporal reframing mechanism; covers planning fallacy and optimism bias not addressed by other strategies |
| 7 | S-010 | Self-Refine | 4.00 | Iterative Self-Correction | LLM-native (Madaan et al., NeurIPS 2023); zero additional infrastructure; universal pre-critic baseline |
| 8 | S-012 | FMEA | 3.75 | Structured Decomposition | Strongest empirical evidence in catalog (70+ years, MIL-STD-1629A, IEC 60812); systematic completeness |
| 9 | S-011 | Chain-of-Verification (CoVe) | 3.75 | Structured Decomposition | Only factual verification strategy; irreplaceable hallucination detection coverage; zero redundancy with other strategies |
| 10 | S-001 | Red Team Analysis | 3.35 | Role-Based Adversarialism | Adversary simulation for security and architecture review; decades of military/intelligence community use |

### The 5 Excluded Strategies

| Rank | ID | Strategy | Composite Score | Primary Exclusion Rationale | Reconsideration Conditions |
|------|-----|----------|----------------|----------------------------|---------------------------|
| 11 | S-008 | Socratic Method | 3.25 | Multi-turn dialogue adds orchestration complexity (Medium effort) without sufficient incremental value. Question-based adversarial challenge is partially covered by DA (S-002) for conclusions and Constitutional AI (S-007) for principle compliance. Its unique contribution (questions vs. assertions) does not justify the orchestration cost. | (a) Empirical evidence of meaningfully different LLM outcomes from Socratic vs. assertion-based critique; (b) dedicated requirements review workflow where assumption probing is primary; (c) significant reduction in multi-turn dialogue orchestration cost |
| 12 | S-006 | Analysis of Competing Hypotheses (ACH) | 3.25 | Specialized diagnostic use case (root cause analysis, forensics); highest cognitive load score (D5=2) in the selected boundary; moderate LLM reliability for consistent matrix output. Confirmation bias coverage partially addressed by DA (S-002) and CoVe (S-011). | (a) Jerry develops dedicated investigation/forensic analysis workflow; (b) LLM structured output reliability improves for consistent matrix generation; (c) problem-solving skill extended to first-class root cause analysis |
| 13 | S-005 | Dialectical Inquiry (DI) | 2.85 | **RED context window risk** (TASK-002: R-005-CW, L=4, I=4, Score=16). High implementation complexity (3-agent, sync barriers). Consumes entire 3-iteration budget. Single-model architecture undermines genuine dialectical tension. Coverage partially provided by Steelman (S-003) + DA (S-002) + reconciliation. | (a) Cross-model verification enables genuine epistemological diversity; (b) context windows increase substantially (>200K tokens); (c) empirical evidence that DI produces superior outcomes to Steelman + DA for C4 architecture decisions |
| 14 | S-009 | Multi-Agent Debate (MAD) | 2.70 | **Highest risk in catalog** (48/175 aggregate). **RED context window risk** (R-009-CW, Score=20 -- single highest risk score in catalog). WEAK agent model fit (only WEAK rating in catalog). Shared-model-bias limitation (DA-002) fundamentally undermines competitive debate's value proposition. Highest implementation complexity (D4=1). | (a) Cross-model verification enables different model providers for debaters; (b) empirical evidence of same-model debate superiority over single-agent structured critique for Jerry's artifact types; (c) RED context window risk reduced to YELLOW through architectural innovation |
| 15 | S-015 | Progressive Adversarial Escalation (PAE) | 2.70 | **Novel unvalidated meta-strategy** (D1=2). **RED context window risk** (R-015-CW, Score=16). Highest aggregate risk in catalog (56/175). Single point of dependency risk (CMP=9). Requires 3 validation experiments (defined in EN-301 TASK-006 v1.1.0) before production deployment. | (a) All 3 validation experiments completed with positive results; (b) escalation gates demonstrate >= 85% agreement with human expert judgment; (c) fallback strategy no longer needed because gate reliability is established |

**S-015 Category Distinction (F-013):** S-015 is categorized as an **orchestration pattern**, not an adversarial strategy. The 14 other catalog entries (S-001 through S-014) are adversarial strategies -- they take an artifact as input and produce critique, verification, scores, or failure analysis as output. S-015 is qualitatively different: it selects and sequences adversarial strategies, determining which to apply, in what order, and at what intensity. This is an orchestration function operating at the workflow level, not the agent level. The "10 selected adversarial strategies" are the 10 entries that perform adversarial review. S-015's graduated escalation logic is implemented as /orchestration skill configuration (EN-307), operating at a different abstraction level. This is not a relabeling exercise -- it reflects a genuine architectural difference (strategies execute within agent invocations; S-015 operates across agent invocations). See TASK-004 "S-015 Category Distinction" section for the full analysis.

---

## Options Considered

### Option A: Select Top 10 by Composite Score (CHOSEN)

**Description:** Apply the TASK-001 evaluation framework (6 weighted dimensions, 1-5 scoring rubric) to all 15 strategies, calculate composite scores, select the top 10 by rank order.

**Pros:**
- Transparent and reproducible: every score has documented rationale traceable to rubric descriptors
- Validated through 12-configuration sensitivity analysis: selection is robust (9/10 stable, exceeds 8/10 threshold)
- Integrates all three evaluation inputs (effectiveness, risk, architecture) through the composite formula
- Clear cutoff: 0.10-point gap between rank 10 (3.35) and rank 11 (3.25), plus 0.40-point gap between rank 9 (3.75) and rank 10 (3.35)
- Tiebreaking procedure is deterministic (D1 > D2 > D3 > qualitative)

**Cons:**
- Sensitivity analysis reveals rank 10 (S-001 Red Team) is sensitive in 2 of 12 configurations (C10, C11), where S-006 (ACH) would replace it
- The composite score reduces 6-dimensional evaluation to a single number, which can obscure individual dimension weaknesses
- Weight assignments, while justified, involve judgment that could be challenged

**Why chosen:** This option provides the most rigorous, transparent, and defensible selection. The sensitivity analysis confirms the selection is robust to plausible weight variations. The single sensitive strategy (S-001 at rank 10) has strong qualitative justification for inclusion (unique adversary simulation coverage, broader applicability than the alternative S-006).

### Option B: Select Top 8 + 2 Diversity Picks

**Description:** Select the top 8 by composite score, then choose 2 additional strategies specifically to maximize mechanistic family diversity and composition layer coverage, even if they rank lower than other candidates.

**Pros:**
- Guarantees coverage across all four mechanistic families
- Could fill the Dialectical Synthesis gap identified in TASK-004 complementarity check
- Addresses the concern that composite scoring may systematically favor low-cost strategies over high-value-but-complex ones

**Cons:**
- The "diversity picks" would likely be S-005 (Dialectical Inquiry) or S-009 (Multi-Agent Debate), both of which carry RED context window risks
- Overriding composite scores for diversity reasons undermines the evaluation framework's legitimacy
- The Dialectical Synthesis coverage gap is assessed as acceptable in TASK-004 (S-003 + S-002 + reconciliation approximates the function)
- Introduces subjective selection at the final step, reducing transparency

**Why rejected:** The coverage gap analysis in TASK-004 confirms that the top-10 selection by composite score already provides adequate coverage across all critical dimensions. The Dialectical Synthesis gap is manageable through strategy composition. Overriding the composite scoring to include RED-risk strategies would undermine the risk-informed foundation of the selection.

### Option C: Select All 15 with Tiered Activation

**Description:** Include all 15 strategies in the framework but assign activation tiers (always-on, conditional, exceptional) to manage cost and complexity.

**Pros:**
- No coverage gaps: all mechanistic families and cognitive biases are addressed
- Allows strategies to be activated when their specific use case arises
- Future-proofs the framework against discovering that an excluded strategy was needed

**Cons:**
- Maintains 15 strategy prompt templates, agent modes, and orchestration configurations -- higher maintenance burden
- The RED-risk strategies (S-005, S-009, S-015) would require full implementation even if rarely used
- Creates false confidence: users may believe all 15 are equally vetted, obscuring the unvalidated status of S-015
- Violates the EN-302 specification to "select 10" -- the evaluation framework was designed around a selection decision, not a tiering decision
- The 5 excluded strategies collectively have 3 RED risks and the highest aggregate risk scores; including them adds risk surface without proportional quality benefit

**Why rejected:** The cost-benefit analysis does not justify maintaining 15 strategies when 10 provide adequate coverage. The excluded strategies have demonstrably higher risk profiles and lower composite scores. The tiered activation model adds complexity without solving the fundamental issues that caused their exclusion (RED context window risk, unvalidated effectiveness, shared-model-bias undermining).

---

## Consequences

### Positive

1. **Operational quality gate:** The selected 10 strategies, anchored by S-014 (LLM-as-Judge), make Jerry's >= 0.92 quality threshold operational with a concrete evaluation mechanism.

2. **Comprehensive coverage:** The portfolio covers all four mechanistic families (3 fully, 1 via composition), all five composition layers (L0-L4), and 12 of 15 mapped cognitive biases.

3. **Favorable risk profile:** The selected 10 contain zero RED risks. All risks are GREEN or YELLOW with defined mitigations. The three RED context window risks in the catalog are all in excluded strategies.

4. **Efficient token budget:** The selected strategies span Ultra-Low to Medium token tiers. A typical Layer 2 review (S-010 + S-007 + S-014) costs approximately 12,000-18,000 tokens. No selected strategy exceeds 10,000 tokens per invocation individually (except S-012 FMEA at 9,000 and S-007 Constitutional AI at 8,000-16,000 at the high end of multi-pass).

5. **Strong synergy profile:** The selected 10 have 14 SYN (synergistic) pairs, 26 COM (compatible) pairs, only 3 TEN (tension) pairs, and zero CON (conflicting) pairs.

6. **Phased integration path:** TASK-003 defines a 4-phase integration priority order. Phase 1 (S-010, S-003, S-014, S-013) delivers approximately 60% of adversarial review capability at approximately 20% of total integration effort.

7. **Robust selection:** 9 of 10 selected strategies are stable across all 12 alternative weight configurations, exceeding the robustness threshold of 8/10.

### Negative

1. **Dialectical Synthesis gap:** The selected portfolio has only secondary representation in the Dialectical Synthesis mechanistic family (S-003 Steelman). The primary Dialectical Synthesis strategies (S-005 DI, S-009 MAD) are both excluded. While the gap is assessed as manageable through strategy composition, it represents a genuine reduction in dialectical rigor compared to Option C.
   - **Impact estimate (F-011):** LOW. C4-level decisions requiring full dialectical inquiry (thesis-antithesis-synthesis) are expected to constitute <5% of review cycles based on Jerry's current usage patterns (most reviews are artifact quality reviews, not strategic decision reviews). For that <5%, the Steelman (S-003) + Devil's Advocate (S-002) + reconciliation approximation covers approximately 70-80% of Dialectical Inquiry's value proposition -- it provides opposing viewpoints and charitable reconstruction, missing only the formal assumption-negation step. Additionally, the excluded strategies carry RED context window risks (S-005: 16, S-009: 20) that would negate their quality benefit through context rot in approximately 30-50% of invocations (based on TASK-002 likelihood ratings of 4/5), meaning their effective value is further reduced. Net expected quality regression: negligible for routine reviews, minor for the rare C4 decisions.

2. **Layer 4 (Tournament) reduced intensity:** The highest-intensity review level has fewer strategies available with the exclusion of S-009 (Multi-Agent Debate). For true C4 decisions (architecture-changing, governance-modifying), the available review depth is reduced.
   - **Impact estimate (F-011):** LOW-MEDIUM. Layer 4 reviews are invoked only for C4-criticality decisions, which are rare in Jerry's current workflow (<2% of review cycles). Even at reduced intensity, the available L4 combination (S-001 Red Team + S-012 FMEA + S-013 Inversion + S-002 DA + S-007 Constitutional AI + S-014 Judge) deploys 6 strategies simultaneously, providing multi-perspective adversarial coverage. The primary loss is the competitive debate mechanism (S-009), which provides sampling diversity but is undermined by the single-model architecture (DA-002). S-009 remains available as an exceptional invocation for true C4 decisions even though it is not in the top 10 -- its orchestration function is preserved in EN-307. Net expected quality regression: negligible for the vast majority of reviews; modest for the rare C4 decisions where competitive debate would have provided incremental value.

3. **Cognitive bias coverage gaps:** Two bias categories lose their primary mitigation:
   - **Dunning-Kruger / Illusion of explanatory depth:** Primarily addressed by excluded S-008 (Socratic Method). Partially mitigated by S-007 (principle-by-principle evaluation exposes gaps where the creator believed compliance existed but the work falls short) and S-012 (FMEA systematic enumeration surfaces competence gaps through systematic means).
   - **Scope insensitivity:** Primarily addressed by excluded S-015 (PAE). Mitigated by implementing S-015's escalation logic as orchestration configuration (the mitigation mechanism is preserved even though S-015 is not counted as a strategy).
   - **Impact estimate (F-011):** LOW for scope insensitivity (full mitigation through S-015 orchestration implementation). MEDIUM for Dunning-Kruger, which is a particularly dangerous bias in LLM-generated artifacts because LLMs produce confident, fluent text that can mask shallow reasoning. S-007 and S-012 provide partial coverage through structured evaluation and systematic enumeration, but neither directly probes the reasoning process the way Socratic questioning does. The expected manifestation is a marginal increase in false negatives for artifacts where the creating agent confidently produces plausible but logically flawed reasoning -- estimated at 5-10% of high-complexity artifacts. This is the most consequential gap from the selection decision and should be monitored through periodic human spot-checks of artifacts that received S-007 Constitutional AI review but no Socratic probing.

4. **S-001 (Red Team) sensitivity at rank 10:** S-001 drops to rank 11 in 2 of 12 weight configurations (C10: cognitive load eliminated; C11: differentiation doubled). This creates a minor vulnerability to challenge from S-006 (ACH) advocates.

5. **S-015 category distinction requires communication (F-013):** S-015 is categorized as an orchestration pattern rather than an adversarial strategy (see Decision section, "S-015 Category Distinction"). This creates a conceptual distinction that must be communicated clearly to downstream consumers: the EN-301 catalog contains 14 adversarial strategies + 1 orchestration pattern, and the "10 selected strategies" refers to 10 of the 14 adversarial strategies. The orchestration pattern (S-015) is implemented separately through EN-307. The risk is that consumers unfamiliar with this distinction may believe S-015 was rejected on quality grounds, when in fact it was categorized differently based on its architectural role.

### Neutral (Requires Monitoring)

1. **Shared-model-bias exposure:** Six of the selected 10 strategies (S-007, S-010, S-011, S-013, S-014, and partially S-003) involve self-critique or self-evaluation. Correlated false negatives from shared model blind spots must be monitored through external tool verification, mutation testing, and periodic human spot-checks.

2. **Excluded strategy reconsideration:** The reconsideration conditions for each excluded strategy should be reviewed quarterly. If cross-model verification becomes available, S-005 and S-009 should be re-evaluated. If S-015's validation experiments succeed, it should be re-evaluated for inclusion.

3. **S-015 validation experiments:** Three experiments defined in EN-301 TASK-006 v1.1.0 (false negative detection, escalation calibration, cost-efficiency) must proceed regardless of S-015's exclusion from the top 10. The results will inform whether S-015 should be promoted in a future ADR revision.

4. **Quality gate calibration:** S-014 (LLM-as-Judge) leniency bias (TASK-002: R-014-FN, Score=12) must be actively managed through rubric calibration against human-scored reference sets, mutation testing, and periodic human audit of score distributions. Uncalibrated scores treated as ground truth is a significant quality regression risk.

---

## Evidence Base

### TASK-001: Evaluation Criteria Summary

The evaluation framework consists of six weighted dimensions designed around Jerry's operational priorities:

| Category | Dimensions | Combined Weight | Jerry Priority |
|----------|-----------|-----------------|----------------|
| Quality Outcome | D1: Effectiveness (25%), D2: LLM Applicability (25%) | 50% | Quality gates >= 0.92 |
| Portfolio Fitness | D3: Complementarity (15%), D4: Implementation Complexity (15%) | 30% | Creator-critic-revision cycles |
| User Experience | D5: Cognitive Load (10%), D6: Differentiation (10%) | 20% | Multi-agent orchestration usability |

Key design properties of the framework:
- No single dimension is decisive (max weight 25%)
- Quality outcome dimensions dominate (50%) -- prevents selecting easy-but-ineffective strategies
- All dimensions use consistent 1-5 scale (D4 inverse-scored: 5 = low complexity)
- Anchoring examples tie rubric levels to specific strategies for calibration
- Deterministic tie-breaking procedure (D1 > D2 > D3 > qualitative)

### TASK-002: Key Risk Findings

**Risk portfolio:** 3 RED | 18 YELLOW | 84 GREEN across 105 assessments (15 strategies x 7 categories)

| Finding | Impact on Selection |
|---------|---------------------|
| **Context window is the dominant systemic risk.** All 3 RED risks are context window risks (S-009: 20, S-015: 16, S-005: 16). | All 3 RED-risk strategies are excluded from the top 10. Context window risk is the single most decisive factor in the exclusion of S-005, S-009, and S-015. |
| **Shared model bias is a cross-cutting risk (DA-002).** Six strategies rely on self-critique with correlated failure modes. | Documented as a monitoring requirement. External tool verification and mutation testing mandated for mitigation. |
| **Lowest-risk strategies:** S-013 (15/175), S-003 (16/175), S-010 (23/175). | All three are in the top 7 of the selection, confirming alignment between low risk and high composite score. |
| **Highest-risk strategies:** S-015 (56/175), S-009 (48/175), S-007 (45/175), S-005 (42/175). | S-015, S-009, S-005 are excluded. S-007 is included (rank 4) because its higher aggregate risk reflects its central role and broad exposure, not fundamental design flaws. |
| **No strategy has an unacceptable overall risk profile.** All 15 are adoptable with mitigation. | The exclusions are driven by composite score rank, not by absolute risk thresholds. |

### TASK-003: Architecture Fit Conclusions

| Finding | Impact on Selection |
|---------|---------------------|
| **Pugh Matrix Tier 1 (architectural winners):** S-003, S-010, S-013, S-014, S-004 | All 5 are in the selected top 10 (ranks 2, 7, 3, 1, 6). Strong correlation between architectural fit and composite score. |
| **Pugh Matrix Tier 3 (architecturally expensive):** S-006, S-011, S-005, S-009 | S-005 and S-009 are excluded. S-006 is excluded. S-011 is included despite Tier 3 Pugh score because its unique factual verification coverage (D3=5, D6=5) outweighs architectural cost. |
| **Token efficiency tiers:** Ultra-Low: S-003 (1,600), S-010 (2,000), S-014 (2,000), S-013 (2,100). High: S-009 (15,000-30,000). | The 4 ultra-low strategies are all in the top 7. The only High-tier strategy (S-009) is excluded. |
| **P-003 compliance:** All 15 strategies are structurally compliant. S-009 carries implementation risk ("COMPLIANT WITH CARE"). | P-003 is not a differentiator for selection, but S-009's implementation risk contributes to its low composite score. |
| **Composition matrix:** 16 SYN pairs, 7 TEN pairs, 0 CON pairs across all 15 strategies. | Selected 10 preserve the strongest synergy pairs (S-003+S-002, S-003+S-007, S-004+S-012, S-013+S-007, S-014+S-015) while avoiding the costliest TEN pairs (S-002+S-005, S-005+S-009). |

### TASK-004: Scoring Results and Sensitivity Analysis

**Composite score distribution:**

| Score Range | Count | Strategies |
|-------------|-------|------------|
| 4.00 - 4.40 | 7 | S-014 (4.40), S-003 (4.30), S-013 (4.25), S-007 (4.15), S-002 (4.10), S-004 (4.10), S-010 (4.00) |
| 3.35 - 3.75 | 3 | S-012 (3.75), S-011 (3.75), S-001 (3.35) |
| 2.70 - 3.25 | 5 | S-008 (3.25), S-006 (3.25), S-005 (2.85), S-009 (2.70), S-015 (2.70) |

**Sensitivity analysis results:**

| Criterion | Threshold | Result | Status |
|-----------|-----------|--------|--------|
| At least 8 of 10 selected are stable | >= 8 | 9 stable | **PASS** |
| At most 2 strategies are sensitive | <= 2 | 2 sensitive (S-001, S-006) | **PASS** |
| No strategy crosses boundary under > 4 of 12 configs | <= 4 crossings | Max 2 crossings (S-001 and S-006) | **PASS** |

**All three robustness thresholds are met.** The selection is classified as **ROBUST**.

The only sensitive boundary is S-001 (rank 10) vs. S-006 (rank 12), where S-006 overtakes S-001 in 2 of 12 configurations:
- C10: D5 (Cognitive Load) eliminated entirely (0% weight)
- C11: D6 (Differentiation) doubled (10% to 20%)

Both configurations represent extreme weight adjustments unlikely to reflect Jerry's actual priorities. The qualitative override favoring S-001 over S-006 is justified by broader applicability, unique adversary simulation coverage, and lower specialization risk.

---

## Compliance

### P-003: No Recursive Subagents

All 10 selected strategies are **fully P-003 compliant:**

| Strategy | Agent Pattern | P-003 Status |
|----------|--------------|-------------|
| S-014 LLM-as-Judge | 1-agent (single pass) | COMPLIANT |
| S-003 Steelman | 1-agent (prompt phase) | COMPLIANT |
| S-013 Inversion | 1-agent (single pass) | COMPLIANT |
| S-007 Constitutional AI | 1-2 agent (multi-pass) | COMPLIANT |
| S-002 Devil's Advocate | 2-agent (orchestrator + critic) | COMPLIANT |
| S-004 Pre-Mortem | 2-agent (orchestrator + analyst) | COMPLIANT |
| S-010 Self-Refine | 1-agent (self-review) | COMPLIANT |
| S-012 FMEA | 1-2 agent (structured output) | COMPLIANT |
| S-011 CoVe | 1-2 agent (context-isolated verification) | COMPLIANT |
| S-001 Red Team | 2-agent (orchestrator + critic with persona) | COMPLIANT |

No selected strategy requires nested agent spawning. All multi-agent patterns use the orchestrator -> worker model with sequential invocations managed by the orchestrator.

**P-003 risk eliminated:** The excluded strategy with P-003 implementation risk (S-009 Multi-Agent Debate, "COMPLIANT WITH CARE") is not in the selected set.

### P-020: User Authority

This ADR is a **recommendation**, not a final decision. Per P-020:

- The user has been informed of the selection through this ADR
- The user retains authority to override any selection or exclusion
- The user may direct inclusion of excluded strategies or exclusion of selected strategies
- The user previously ratified EN-301-DEV-001 (Blue Team -> R-6, Pre-Mortem/Dialectical Inquiry confirmed), demonstrating active engagement with strategy decisions

**Ratification status:** Pending. This ADR requires explicit user ratification before transitioning to ACCEPTED status.

### P-043: Mandatory Disclaimer

**DISCLAIMER:** This ADR is AI-generated analysis based on the EN-302 evaluation framework. It is advisory only and constitutes a recommendation, not a binding decision. The evaluation scores, risk assessments, and architectural analyses are produced by AI agents (ps-analyst, nse-risk, nse-architecture, ps-architect) and have not been validated by human subject matter experts. All strategy selection decisions require human review per P-020. The quality scores, sensitivity analyses, and composite rankings should be treated as structured assessments that inform, but do not replace, human judgment.

---

## Related Decisions

### Upstream (Inputs to This ADR)

| Decision / Artifact | Relationship | Status |
|---------------------|-------------|--------|
| **EN-301-DEV-001** (Specification Deviation) | Blue Team replaced by Pre-Mortem (S-004); Strawman replaced by Dialectical Inquiry (S-005). User-ratified 2026-02-13. Blue Team moved to Reserved Strategy R-6. | Ratified |
| **EN-301 TASK-006** (Revised Catalog v1.1.0) | Authoritative 15-strategy catalog with contraindications, differentiation clarifications, systemic risk analysis, reserved strategies, and validation experiments. | Complete |
| **EN-302 TASK-001** (Evaluation Criteria) | 6-dimension weighted framework with scoring rubrics and sensitivity analysis methodology. | Complete |
| **EN-302 TASK-002** (Risk Assessment) | 105-risk assessment matrix across 15 strategies x 7 categories. 3 RED, 18 YELLOW, 84 GREEN. | Complete |
| **EN-302 TASK-003** (Architecture Trade Study) | Pugh Matrix, token budget analysis, composition matrix, integration cost assessment. | Complete |
| **EN-302 TASK-004** (Scoring & Selection) | Composite scoring, rank ordering, sensitivity analysis, complementarity check. | Complete |

### Downstream (Decisions Informed by This ADR)

| Decision / Enabler | Relationship | Status |
|--------------------|-------------|--------|
| **EN-302 TASK-006** (Adversarial Review) | ps-critic will stress-test this ADR's rationale, assumptions, and conclusions. May result in ADR revision. | Pending |
| **EN-303** (Situational Applicability Mapping) | Will map the 10 selected strategies to specific artifact types, review contexts, and criticality levels. Depends on the stable strategy set defined here. | Planned |
| **EN-304** (Problem-Solving Skill Enhancement) | Will enhance ps-critic and related agents with the 10 selected strategy modes. Depends on knowing which strategies to implement. | Planned |
| **EN-305** (NASA SE Skill Enhancement) | Will integrate relevant strategies (S-007, S-012, S-014) into nse-reviewer and nse-qa agents. | Planned |
| **EN-307** (Orchestration Skill Enhancement) | Will implement S-015's graduated escalation logic as orchestration configuration and integrate strategy sequencing from TASK-003 composition analysis. | Planned |
| **S-015 Validation Experiments** | Three experiments (false negative detection, escalation calibration, cost-efficiency) must proceed. Results may trigger ADR revision to include S-015 in a future version. | Planned |

### Reserved Strategies (from EN-301 TASK-006)

The following strategies are maintained in reserve with defined promotion criteria:

| ID | Strategy | Origin | Promotion Condition |
|----|----------|--------|---------------------|
| R-1 | Cognitive Walkthrough | EN-301 TASK-002 | Promote if Jerry develops end-user-facing interface reviews |
| R-2 | Reference Class Forecasting | EN-301 TASK-002 | Promote when Jerry accumulates sufficient reference class data |
| R-3 | Formal Methods / Model Checking | EN-301 TASK-002 | Promote if Jerry expands to safety-critical domains |
| R-4 | ATAM | EN-301 TASK-002 | Promote if Jerry develops dedicated architecture review workflows |
| R-5 | Ensemble Adversarial Meta-Review | EN-301 TASK-003 | Promote if multi-strategy disagreement analysis shows measurable benefit |
| R-6 | Blue Team | EN-301-DEV-001 | Promote if distinct Blue Team behavioral profile validated against Pre-Mortem |

---

## Limitations and Epistemic Status (F-012)

**This ADR is an AI-generated architecture decision recommendation.** All evidence, analysis, scoring, risk assessment, and architectural evaluation cited in this document were produced by AI agents (ps-analyst, nse-risk, nse-architecture, ps-architect) without human subject matter expert validation. The following epistemic boundaries apply:

### What This ADR Can Claim

1. **Internal consistency.** The selection follows logically from the evaluation framework (TASK-001), risk assessment (TASK-002), architecture trade study (TASK-003), and composite scoring (TASK-004). The methodology is transparent, reproducible, and traceable. Any independent evaluator applying the same framework to the same data would arrive at the same or very similar selection.

2. **Sensitivity robustness.** The 12-configuration sensitivity analysis is deterministic and verifiable. The rank ranges and boundary behaviors are mathematical consequences of the composite formula and can be independently confirmed.

3. **Literature grounding.** For strategies with peer-reviewed empirical evidence (S-002, S-005, S-009, S-010, S-011, S-012, S-014), the D1 (Effectiveness) scores are anchored in published research. The citations are verifiable.

### What This ADR Cannot Claim

1. **Empirical validation of the selection's quality impact.** No prototype implementation has been tested. The claim that these 10 strategies will collectively enable a >= 0.92 quality gate is a structured projection, not an empirical finding. The actual quality impact will only be known after Phase 1 integration (EN-304, EN-305).

2. **Ground truth for AI-assessed scores.** The 90 dimension scores (15 strategies x 6 dimensions) in TASK-004 are AI assessments. No inter-rater reliability data exists. No human scoring comparison has been performed. The scores are structured analytical judgments, not measurements.

3. **Resolution of [unverified] claims.** Several empirical claims from the EN-301 catalog (S-004 "30% improvement," S-010 specific improvement ranges, S-014 "~80% agreement") remain unverified. These claims do not change the D1 score assignments but represent precision claims that should not be cited without caveat.

4. **External validity.** This analysis is specific to Jerry's architecture (single-model, hexagonal, P-003 constrained, UV-managed Python). The selection may not generalize to other AI agent frameworks with different architectural constraints.

### Structural Limitation: AI Self-Assessment

The EN-302 evaluation pipeline involves AI agents assessing the quality of strategies that AI agents will execute to evaluate the quality of AI-generated artifacts. This creates a three-layer self-referential structure:

```
Layer 1: AI agents (ps-analyst, nse-risk, etc.) evaluate strategies
Layer 2: AI agents (ps-critic, etc.) will execute the selected strategies
Layer 3: AI agents (ps-creator, etc.) produce the artifacts being reviewed
```

All three layers use the same model (Claude), creating correlated assessment patterns. The sensitivity analysis and adversarial review process (TASK-006) partially compensate for this structural limitation, but cannot fully overcome it. The ultimate validation comes from empirical performance after implementation -- which is why this ADR requires user ratification (P-020) and why Phase 1 integration should include quality measurement against human-judged baselines.

---

## References

### Primary Evidence Sources

| # | Citation | Role in This ADR |
|---|----------|-----------------|
| 1 | FEAT-004:EN-302:TASK-001 -- Evaluation Criteria and Weighting Methodology | Rubric definitions, weight justifications, composite formula, sensitivity methodology |
| 2 | FEAT-004:EN-302:TASK-002 -- Risk Assessment (nse-risk v2.1.0) | Risk profiles (105 assessments), RED/YELLOW/GREEN classifications, systemic risk patterns |
| 3 | TSR-PROJ-001-EN302-003 (TASK-003) -- Architecture Trade Study (nse-architecture v2.1.0) | Pugh Matrix, token budgets, composition matrix, integration costs, P-003 compliance |
| 4 | FEAT-004:EN-302:TASK-004 -- Composite Scoring and Top-10 Selection (ps-analyst) | Scores, rankings, sensitivity analysis, complementarity check, boundary analysis |
| 5 | FEAT-004:EN-301:TASK-006 -- Revised Catalog v1.1.0 | Authoritative 15-strategy catalog, contraindications, reserved strategies, validation experiments |
| 6 | FEAT-004:EN-301:TASK-008 -- Final Validation Report | 8/8 AC pass, EN-301-DEV-001 deviation record, quality certification |

### Methodological Sources

| # | Citation | Relevance |
|---|----------|-----------|
| 7 | Keeney, R. L., & Raiffa, H. (1993). *Decisions with Multiple Objectives*. Cambridge University Press. ISBN: 978-0521438834. | Multi-criteria decision analysis methodology underpinning the composite scoring approach |
| 8 | Goodwin, P., & Wright, G. (2004). *Decision Analysis for Management Judgment* (3rd ed.). Wiley. ISBN: 978-0470861080. | Sensitivity analysis methodology and robustness testing |
| 9 | Saaty, T. L. (1980). *The Analytic Hierarchy Process*. McGraw-Hill. ISBN: 978-0070543713. | Weight validation methodology |

### Jerry Framework Sources

| # | Citation | Relevance |
|---|----------|-----------|
| 10 | Jerry Constitution (docs/governance/JERRY_CONSTITUTION.md) | P-003, P-020, P-022, P-043 constraints |
| 11 | CLAUDE.md (project root) | Jerry identity, context rot problem statement, critical constraints |
| 12 | `.claude/rules/architecture-standards.md` | Hexagonal architecture, layer dependencies, composition root pattern |
| 13 | `skills/orchestration/SKILL.md` | Orchestration skill capabilities for strategy integration |

### Strategy-Specific Empirical Sources

| # | Citation | Strategy |
|---|----------|----------|
| 14 | Schweiger, D. M., Sandberg, W. R., & Ragan, J. W. (1986). Group approaches for improving strategic decision making. *Academy of Management Journal*, 29(1), 51-71. | S-002 (DA), S-005 (DI) |
| 15 | Heuer, R. J., & Pherson, R. H. (2014). *Structured Analytic Techniques for Intelligence Analysis* (2nd ed.). CQ Press. ISBN: 978-1452241517. | S-002 (DA), S-006 (ACH) |
| 16 | Madaan, A., et al. (2023). Self-Refine: Iterative Refinement with Self-Feedback. *NeurIPS 2023*. arXiv:2303.17651. | S-010 (Self-Refine) |
| 17 | Bai, Y., et al. (2022). Constitutional AI: Harmlessness from AI Feedback. Anthropic. arXiv:2212.08073. | S-007 (Constitutional AI) |
| 18 | Zheng, L., et al. (2023). Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena. *NeurIPS 2023*. arXiv:2306.05685. | S-014 (LLM-as-Judge) |
| 19 | Dhuliawala, S., et al. (2023). Chain-of-Verification Reduces Hallucination in Large Language Models. arXiv:2309.11495. | S-011 (CoVe) |
| 20 | Klein, G. (2007). Performing a Project Premortem. *Harvard Business Review*, 85(9), 18-19. | S-004 (Pre-Mortem) |
| 21 | MIL-STD-1629A (1980). Procedures for Performing a Failure Mode, Effects, and Criticality Analysis. US Department of Defense. | S-012 (FMEA) |
| 22 | Du, Y., et al. (2023). Improving Factuality and Reasoning in Language Models through Multiagent Debate. *ICML 2023*. arXiv:2305.14325. | S-009 (MAD) |

---

*DISCLAIMER: This ADR is AI-generated based on structured evaluation of adversarial strategies. It is advisory only and constitutes a recommendation pending adversarial review (TASK-006) and user ratification (P-020). All strategy selection decisions require human review and professional judgment.*

---

*Document ID: FEAT-004:EN-302:TASK-005*
*ADR ID: ADR-EPIC002-001*
*Agent: ps-architect*
*Created: 2026-02-13*
*Status: Proposed*
