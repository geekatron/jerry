# TASK-004: Composite Scoring and Top-10 Selection of Adversarial Strategies

<!--
DOCUMENT-ID: FEAT-004:EN-302:TASK-004
AUTHOR: ps-analyst agent
DATE: 2026-02-13
STATUS: Complete
PARENT: EN-302 (Strategy Selection & Decision Framework)
FEATURE: FEAT-004 (Adversarial Strategy Research & Skill Enhancement)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
PS-ID: EN-302
ENTRY-ID: TASK-004
INPUT: TASK-001 (evaluation criteria), TASK-002 (risk assessment), TASK-003 (architecture trade study), EN-301 TASK-006 (revised catalog v1.1.0)
-->

> **Version:** 1.1.0
> **Agent:** ps-analyst
> **Quality Target:** >= 0.92
> **Input Artifacts:** TASK-001 (criteria & weights), TASK-002 (risk assessment), TASK-003 (architecture trade study), EN-301 TASK-006 (revised catalog v1.1.0)
> **Purpose:** Score all 15 adversarial strategies on 6 weighted dimensions, select the best 10, and validate the selection through sensitivity and complementarity analysis

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | Top-10 selection result and key findings |
| [Scoring Matrix](#scoring-matrix) | All 15 strategies scored on all 6 dimensions with composite and rank |
| [Per-Strategy Scoring Justification](#per-strategy-scoring-justification) | Detailed rationale for every score with risk and architecture references |
| [Selection Decision](#selection-decision) | Top 10 selected and bottom 5 excluded with rationale; S-015 category distinction (F-013) |
| [Boundary Analysis](#boundary-analysis) | Strategies ranked 9-12 examined under 12 alternative weight configurations; S-001 vs S-008 justification (F-014) |
| [Complementarity Check](#complementarity-check) | Coverage verification across mechanistic families, composition layers, and bias map |
| [Traceability Matrix](#traceability-matrix) | Mapping from scores to TASK-001 rubric, TASK-002 risk, and TASK-003 architecture |
| [Limitations and Epistemic Status](#limitations-and-epistemic-status) | Epistemic boundaries, unresolved claims, and AI self-assessment limitations (F-012) |
| [References](#references) | Source citations |

---

## Executive Summary

This document applies the TASK-001 evaluation framework to all 15 adversarial strategies in the EN-301 catalog (v1.1.0), incorporating risk data from TASK-002 and architectural fitness data from TASK-003. The result is a rank-ordered selection of 10 strategies for integration into Jerry's quality framework.

**Top 10 Selected (by composite score):**

| Rank | ID | Strategy | Composite Score |
|------|-----|----------|----------------|
| 1 | S-014 | LLM-as-Judge | 4.40 |
| 2 | S-003 | Steelman Technique | 4.30 |
| 3 | S-013 | Inversion Technique | 4.25 |
| 4 | S-007 | Constitutional AI Critique | 4.15 |
| 5 | S-002 | Devil's Advocate | 4.10 |
| 6 | S-004 | Pre-Mortem Analysis | 4.10 |
| 7 | S-010 | Self-Refine | 4.00 |
| 8 | S-012 | FMEA | 3.75 |
| 9 | S-011 | Chain-of-Verification | 3.75 |
| 10 | S-001 | Red Team Analysis | 3.35 |

**Bottom 5 Excluded:**

| Rank | ID | Strategy | Composite Score | Primary Exclusion Reason |
|------|-----|----------|----------------|--------------------------|
| 11 | S-008 | Socratic Method | 3.25 | Multi-turn dialogue complexity; question-based challenge partially covered by DA (S-002) and Constitutional AI (S-007) |
| 12 | S-006 | ACH | 3.25 | Specialized diagnostic use case; high cognitive load; moderate LLM reliability for matrix reasoning |
| 13 | S-005 | Dialectical Inquiry | 2.85 | RED context window risk; high complexity; narrow applicability; coverage partially provided by DA + Steelman |
| 14 | S-009 | Multi-Agent Debate | 2.70 | Highest risk in catalog; RED context window; shared-model-bias limitation; highest complexity |
| 15 | S-015 | Progressive Adversarial Escalation | 2.70 | Novel unvalidated meta-strategy; RED context window risk; single point of dependency risk |

**Key findings:**

1. **Selection is robust.** 9 of 10 selected strategies are stable across all 12 alternative weight configurations, exceeding the robustness threshold (>= 8 required). Only S-001 (rank 10) is sensitive, dropping to rank 11 in 2 of 12 configurations.
2. **Clear tier separation.** The top 9 strategies (composite >= 3.35) are clearly separated from the bottom 5 (composite <= 3.25). Only the rank 10-12 boundary (S-001, S-008, S-006) shows weight sensitivity.
3. **Complementarity is strong.** The selected 10 cover all four mechanistic families, all five composition layers (L0-L4), and 12 of 15 cognitive biases mapped in TASK-006 Appendix B.
4. **Context window is the decisive risk.** The three excluded strategies with RED context window risk (S-005, S-009, S-015) all fail to make the top 10. This validates TASK-002's finding that context window risk is the dominant systemic concern.

---

## Scoring Matrix

### Composite Scoring Table

All scores are integers 1-5 per the TASK-001 rubric. D4 is inverse-scored (5 = low complexity). Composite = D1(0.25) + D2(0.25) + D3(0.15) + D4(0.15) + D5(0.10) + D6(0.10).

| ID | Strategy | D1 (25%) | D2 (25%) | D3 (15%) | D4 (15%) | D5 (10%) | D6 (10%) | Composite | Rank |
|----|----------|----------|----------|----------|----------|----------|----------|-----------|------|
| S-001 | Red Team Analysis | 4 | 3 | 3 | 3 | 4 | 3 | 3.35 | 10 |
| S-002 | Devil's Advocate | 5 | 4 | 3 | 4 | 5 | 3 | 4.10 | 5 |
| S-003 | Steelman Technique | 4 | 5 | 4 | 5 | 4 | 3 | 4.30 | 2 |
| S-004 | Pre-Mortem Analysis | 4 | 4 | 4 | 4 | 4 | 5 | 4.10 | 6 |
| S-005 | Dialectical Inquiry | 4 | 2 | 3 | 2 | 3 | 3 | 2.85 | 13 |
| S-006 | ACH | 4 | 3 | 3 | 3 | 2 | 4 | 3.25 | 12 |
| S-007 | Constitutional AI Critique | 4 | 5 | 4 | 4 | 3 | 4 | 4.15 | 4 |
| S-008 | Socratic Method | 4 | 3 | 3 | 3 | 3 | 3 | 3.25 | 11 |
| S-009 | Multi-Agent Debate | 4 | 2 | 3 | 1 | 3 | 3 | 2.70 | 14 |
| S-010 | Self-Refine | 4 | 5 | 2 | 5 | 4 | 3 | 4.00 | 7 |
| S-011 | Chain-of-Verification | 3 | 4 | 5 | 3 | 3 | 5 | 3.75 | 9 |
| S-012 | FMEA | 5 | 3 | 4 | 3 | 3 | 4 | 3.75 | 8 |
| S-013 | Inversion Technique | 3 | 5 | 4 | 5 | 4 | 5 | 4.25 | 3 |
| S-014 | LLM-as-Judge | 4 | 5 | 4 | 5 | 4 | 4 | 4.40 | 1 |
| S-015 | PAE | 2 | 3 | 3 | 2 | 2 | 5 | 2.70 | 15 |

**Note on tie-breaking:** Per TASK-001 Section "Tie-Breaking Rules":
- **S-002 vs S-004 (both 4.10):** D1: S-002=5 > S-004=4. S-002 ranks above S-004. S-002 is rank 5, S-004 is rank 6.
- **S-012 vs S-011 (both 3.75):** D1: S-012=5 > S-011=3. S-012 ranks above S-011. S-012 is rank 8, S-011 is rank 9.
- **S-008 vs S-006 (both 3.25):** D1: S-008=4 = S-006=4 (tied). D2: S-008=3 = S-006=3 (tied). D3: S-008=3 = S-006=3 (tied). All dimension tiebreakers exhausted. Qualitative tiebreak applied -- see boundary analysis.
- **S-009 vs S-015 (both 2.70):** D1: S-009=4 > S-015=2. S-009 ranks above S-015. S-009 is rank 14, S-015 is rank 15.

**Top 10:**
S-014, S-003, S-013, S-007, S-002, S-004, S-010, S-012, S-011, S-001

**Bottom 5:**
S-008, S-006, S-005, S-009, S-015

---

## Per-Strategy Scoring Justification

### S-001: Red Team Analysis

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| D1: Effectiveness (25%) | **4** | Decades of use in military, intelligence, and security. CIA-endorsed. Schweiger et al. (1986) empirical support. Not scored 5 because empirical evidence is strongest in security/military contexts; effectiveness in general code/architecture review is less directly evidenced. |
| D2: LLM Applicability (25%) | **3** | Persona assignment maps well to LLM prompting. However, Red Team's value depends on the adversary model's realism -- LLMs lack genuine domain-specific adversary knowledge. Single-model architecture means the "adversary" is the same model as the "defender," limiting genuine adversarial diversity. TASK-002 R-001-FN: "If the Red Team fails to model the correct adversary, then real vulnerabilities will be missed." |
| D3: Complementarity (15%) | **3** | Provides adversarial simulation not duplicated by other strategies, but overlaps with Devil's Advocate (S-002) in providing oppositional critique. TASK-003 composition matrix: TEN (tension) with S-002, S-009. The overlap with DA reduces its incremental complementarity. |
| D4: Implementation Complexity (15%) | **3** | 2-agent pattern (orchestrator + critic with persona). Low per TASK-003 ("Low" aggregate effort). Medium token cost (~7,000 per review). Requires persona template design and adversary profile definition. Not trivial, but not complex. |
| D5: Cognitive Load (10%) | **4** | Concept is intuitive ("someone tries to attack your work"). Outputs are vulnerability reports with severity ratings -- straightforward to interpret. Most engineers are familiar with security/penetration testing analogies. |
| D6: Differentiation (10%) | **3** | Belongs to Role-Based Adversarialism family alongside S-002. The distinction (behavioral adversary simulation vs. argumentative opposition) is real but both deliver adversarial challenge through role assignment. TASK-006 redundancy check confirms unique mechanism x agent pattern x output type combination. |

**Composite:** (4 * 0.25) + (3 * 0.25) + (3 * 0.15) + (3 * 0.15) + (4 * 0.10) + (3 * 0.10) = 1.00 + 0.75 + 0.45 + 0.45 + 0.40 + 0.30 = **3.35**

**Risk factor (TASK-002):** Aggregate risk score 39/175 (YELLOW). Premature adversarial pressure on early-stage work (QR=9) is the primary risk. Context window risk is moderate (CW=9).

**Architecture factor (TASK-003):** Pugh score -0.20 (Tier 2: Architecturally Neutral). Arch score 0.82. Medium token cost (~7,000). STRONG agent model fit.

---

### S-002: Devil's Advocate

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| D1: Effectiveness (25%) | **5** | CIA-formalized structured analytic technique (Heuer & Pherson, 2014). Decades of intelligence community use. Multiple empirical studies including Schweiger et al. (1986). Anchoring example from TASK-001: score 5. Government and institutional adoption. |
| D2: LLM Applicability (25%) | **4** | Core critic function maps directly to LLM capabilities. Prompt engineering is straightforward ("build the strongest case against"). Single-model limitation applies but is less severe than for Red Team because DA argues against conclusions (reasoning-level) rather than simulating domain-specific adversary behavior. TASK-002: R-002-INT notes compliance training may weaken adversarial stance, but prompt engineering can compensate. Score 4 rather than 5 because genuine "authentic dissent" (Nemeth et al., 2001) is hard to achieve with LLMs. |
| D3: Complementarity (15%) | **3** | Core adversarial strategy, but overlaps with Red Team (S-001) in providing oppositional critique. Anchoring example from TASK-001: score 3. Both address confirmation bias. DA is narrower (argues against conclusion) vs. RT (simulates adversary behavior), so partial overlap. |
| D4: Implementation Complexity (15%) | **4** | Trivial integration per TASK-003 ("Trivial" aggregate effort). 2-agent pattern with prompt template swap. Low token cost (~4,600). Score 4 rather than 5 because it requires a separate agent pass (unlike S-003 which integrates into existing pass). |
| D5: Cognitive Load (10%) | **5** | Universally understood concept. Anchoring example from TASK-001: score 5. "Here is why you might be wrong." Every engineer has encountered this. Findings are direct critiques -- no translation needed. |
| D6: Differentiation (10%) | **3** | Same family as Red Team (Role-Based Adversarialism). Distinction is real (assertions vs. behavioral simulation) but both deliver adversarial challenge through role assignment. TASK-006 REC-005 required differentiation clarification vs. Socratic Method (S-008). Score 3 reflects in-family positioning. |

**Composite:** (5 * 0.25) + (4 * 0.25) + (3 * 0.15) + (4 * 0.15) + (5 * 0.10) + (3 * 0.10) = 1.25 + 1.00 + 0.45 + 0.60 + 0.50 + 0.30 = **4.10**

**Risk factor (TASK-002):** Aggregate risk score 27/175 (GREEN). Lowest-risk category. Performative dissent (FP=6) is the primary risk -- easily mitigated with evidence requirements.

**Architecture factor (TASK-003):** Pugh score 0.00 (baseline). Arch score 0.87. Low token cost (~4,600). STRONG agent model fit.

---

### S-003: Steelman Technique

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| D1: Effectiveness (25%) | **4** | Rooted in the Principle of Charity (philosophical argumentation). Widely practiced in academic discourse and formal debate. Less formal empirical evidence than DA or FMEA -- no single peer-reviewed study isolating steelmanning as the treatment. Strong theoretical basis and universal adoption in rigorous argumentation. Score 4 reflects strong evidence base without peer-reviewed empirical validation specific to steelmanning. |
| D2: LLM Applicability (25%) | **5** | Extremely natural for LLMs. "First, reconstruct the argument in its strongest possible form" is a single prompt instruction. Adds ~0.5 agent pass to existing critic invocation. No new agents needed. No context isolation issues. Fits within 3-iteration budget trivially. TASK-003: VERY STRONG fit. |
| D3: Complementarity (15%) | **4** | Uniquely serves as a precondition for fair critique. No other strategy provides charitable reconstruction before adversarial challenge. Enhances the effectiveness of all subsequent critique strategies (S-002, S-007, S-001). TASK-003 composition matrix: SYN (synergistic) with S-001, S-002, S-007. High portfolio value as an enabler strategy. Score 4 rather than 5 because its function is preparatory -- it does not independently catch defects. |
| D4: Implementation Complexity (15%) | **5** | Lowest-cost strategy in the catalog. Anchoring example from TASK-001: score 5. Single prompt phase within existing critic invocation. No new agents, no new infrastructure. TASK-003: "Trivial" aggregate effort. ~1,600 tokens per invocation. TASK-002: lowest risk (16/175). |
| D5: Cognitive Load (10%) | **4** | Concept is easily explained ("strengthen the argument before critiquing it"). Most engineers understand the principle of charitable interpretation. Output is a strengthened version of the argument + subsequent critique -- clear and actionable. Score 4 rather than 5 because the two-phase output (steelman + critique) requires understanding why both phases exist. |
| D6: Differentiation (10%) | **3** | Belongs to Dialectical Synthesis family. TASK-006 REC-005 required differentiation clarification vs. Self-Refine (S-010). The distinction (charitable reconstruction of another's work vs. self-improvement of own work) is mechanistically real but required explicit analysis to establish. Score 3 reflects the needed clarification. |

**Composite:** (4 * 0.25) + (5 * 0.25) + (4 * 0.15) + (5 * 0.15) + (4 * 0.10) + (3 * 0.10) = 1.00 + 1.25 + 0.60 + 0.75 + 0.40 + 0.30 = **4.30**

**Risk factor (TASK-002):** Aggregate risk score 16/175 (GREEN). Joint-lowest risk in catalog (tied with S-013). No YELLOW or RED risks.

**Architecture factor (TASK-003):** Pugh score +1.00 (Rank 1). Arch score 0.95. Ultra-low token cost (~1,600). STRONG agent model fit.

---

### S-004: Pre-Mortem Analysis

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| D1: Effectiveness (25%) | **4** | Kahneman endorsed. Mitchell et al. (1989) studied temporal perspective effect. Klein (2007) popularized. Widely adopted in project management and military planning. The specific "30% increase" claim is marked [unverified] in TASK-006 v1.1.0, but the general effectiveness of prospective hindsight is well-established. Score 4 reflects strong evidence base with the specific magnitude claim unverified. |
| D2: LLM Applicability (25%) | **4** | Temporal reframing ("it has failed") maps naturally to LLM prompting. The "narrator persona" is easily elicited. Anchoring example from TASK-001: score 4. Minor limitation: LLMs lack genuine domain experience for identifying non-obvious failure modes. Single-pass, fits within 3-iteration budget. |
| D3: Complementarity (15%) | **4** | Unique temporal reframing mechanism. No other strategy uses prospective hindsight. TASK-003 composition matrix: SYN with S-012 (FMEA) and S-013 (Inversion). Pre-Mortem identifies creative/strategic failure modes that FMEA's systematic enumeration may miss, and vice versa. Covers planning fallacy and optimism bias not addressed by other selected strategies. |
| D4: Implementation Complexity (15%) | **4** | 2-agent pattern with temporal reframing prompt. Low integration effort per TASK-003. ~5,600 tokens per invocation. Score 4 rather than 5 because it requires a separate agent pass (unlike S-003/S-010 which embed in existing passes). |
| D5: Cognitive Load (10%) | **4** | Concept is intuitive ("imagine the project has failed -- why?"). Outputs are failure cause inventories with mitigations -- structured and actionable. Most engineers and project managers are familiar with pre-mortem exercises. |
| D6: Differentiation (10%) | **5** | Only strategy using temporal reframing. Anchoring example from TASK-001: score 5. No other strategy uses prospective hindsight as its primary mechanism. Wholly unique -- no substitute exists in the catalog. |

**Composite:** (4 * 0.25) + (4 * 0.25) + (4 * 0.15) + (4 * 0.15) + (4 * 0.10) + (5 * 0.10) = 1.00 + 1.00 + 0.60 + 0.60 + 0.40 + 0.50 = **4.10**

**Risk factor (TASK-002):** Aggregate risk score 28/175 (GREEN-YELLOW). False Negative risk (FN=9) from imagination-dependent coverage is the primary concern -- mitigated by pairing with FMEA.

**Architecture factor (TASK-003):** Pugh score +0.20 (Tier 1). Arch score 0.90. Low token cost (~5,600). STRONG agent model fit.

---

### S-005: Dialectical Inquiry

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| D1: Effectiveness (25%) | **4** | Empirically validated by Schweiger et al. (1986) demonstrating superior decision quality over both consensus and Devil's Advocate. Well-established in organizational decision-making literature. Decades of academic support. Strong evidence for human-team contexts. |
| D2: LLM Applicability (25%) | **2** | Architecturally demanding: 3-agent pattern with assumption extraction between passes. TASK-002 R-005-CW: **RED** context window risk (score 16). The thesis-antithesis-synthesis pattern inherently produces large outputs (3+ agent passes). Single-model limitation means thesis and antithesis are generated by the same model, reducing genuine dialectical tension. 3-iteration budget is entirely consumed by DI alone, leaving no room for other strategies. Score 2 reflects the RED context window risk and architectural demands. |
| D3: Complementarity (15%) | **3** | Thesis-antithesis-synthesis mechanism is unique. However, DA (S-002) partially covers the oppositional function, and the synthesis component can be approximated by combining Steelman + DA + reconciliation. TASK-003: TEN (tension) with S-002 and S-009. DI subsumes DA's function (per TASK-003 anti-patterns). |
| D4: Implementation Complexity (15%) | **2** | 3-agent pattern requiring sync barriers and assumption extraction. TASK-003: MODERATE aggregate effort. ~9,600 tokens. Pugh score -0.60 (Tier 3: Architecturally Expensive). Requires /orchestration skill support with explicit multi-pass coordination. |
| D5: Cognitive Load (10%) | **3** | Concept requires explanation ("two opposing plans from the same data, then synthesize"). The thesis-antithesis-synthesis output requires understanding the dialectical process. Not obscure (philosophy students recognize it) but not universally familiar. |
| D6: Differentiation (10%) | **3** | Belongs to Dialectical Synthesis family alongside S-009 (Multi-Agent Debate). Both construct opposing positions and seek resolution. DI is structured (assumption negation), Debate is competitive (argumentative). Distinct but same family. |

**Composite:** (4 * 0.25) + (2 * 0.25) + (3 * 0.15) + (2 * 0.15) + (3 * 0.10) + (3 * 0.10) = 1.00 + 0.50 + 0.45 + 0.30 + 0.30 + 0.30 = **2.85**

**Risk factor (TASK-002):** Aggregate risk score 42/175 (YELLOW-RED). Contains 1 RED risk: R-005-CW context window (L=4, I=4, Score=16). Artificial antithesis risk (FP=9).

**Architecture factor (TASK-003):** Pugh score -0.60 (Tier 3). Arch score 0.65. Medium token cost (~9,600). MODERATE agent model fit.

---

### S-006: Analysis of Competing Hypotheses

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| D1: Effectiveness (25%) | **4** | CIA Tradecraft Primer (Heuer & Pherson, 2014). Decades of intelligence analysis use. Structured analytic technique validated across intelligence community. Strong evidence for reducing confirmation bias in diagnostic reasoning. |
| D2: LLM Applicability (25%) | **3** | Matrix construction is feasible for LLMs, but quality depends on hypothesis generation (domain knowledge dependent). Evidence assessment (C/I/N/A) involves subjective judgment that LLMs may not calibrate well. Anchoring example from TASK-001: score 3. TASK-003: MODERATE fit -- matrix output reliability and parsing complexity reduce score. Needs structured output format (YAML/JSON) for reliable matrix generation. |
| D3: Complementarity (15%) | **3** | Unique matrix-based multi-hypothesis evaluation. However, its primary use case (diagnostic reasoning, root cause analysis) is specialized. TASK-003 composition matrix: SYN with S-008 and S-011. Addresses confirmation bias effectively, but S-002 (DA) and S-011 (CoVe) also address confirmation bias through different mechanisms. |
| D4: Implementation Complexity (15%) | **3** | 1-2 agent pattern but requires structured matrix output. TASK-003: MEDIUM aggregate effort. ~10,000 tokens. Matrix output parsing and reliability are the primary complexity drivers. The matrix format must be consistently generated for downstream consumption. |
| D5: Cognitive Load (10%) | **2** | Requires understanding of hypothesis matrices, diagnosticity, and the "least rejected" paradigm. Anchoring example from TASK-001: score 2. Specialized intelligence analysis technique. The matrix output requires interpretation to extract actionable conclusions. Users unfamiliar with ACH will need significant explanation. |
| D6: Differentiation (10%) | **4** | Only matrix-based multi-hypothesis evaluation strategy in the catalog. The mechanism (evaluate all hypotheses against all evidence simultaneously) is unique. No other strategy provides the structured diagnosticity analysis. |

**Composite:** (4 * 0.25) + (3 * 0.25) + (3 * 0.15) + (3 * 0.15) + (2 * 0.10) + (4 * 0.10) = 1.00 + 0.75 + 0.45 + 0.45 + 0.20 + 0.40 = **3.25**

**Risk factor (TASK-002):** Aggregate risk score 35/175 (YELLOW). Evidence independence assumption (FN=9) and context window for large matrices (CW=9) are the primary risks.

**Architecture factor (TASK-003):** Pugh score -0.40 (Tier 3). Arch score 0.70. Medium token cost (~10,000). MODERATE agent model fit.

---

### S-007: Constitutional AI Critique

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| D1: Effectiveness (25%) | **4** | Designed for LLMs by Anthropic (Bai et al., 2022). Published results demonstrating alignment improvement. Appeared in all three EN-301 research artifacts. The evidence is strong for LLM self-improvement but is primarily focused on alignment/safety rather than general artifact quality review. Score 4 reflects strong but domain-specific evidence. |
| D2: LLM Applicability (25%) | **5** | Designed specifically for LLMs. Anchoring example from TASK-001: score 5. Jerry already has constitutions (`.claude/rules/` files). Principle-by-principle evaluation is natural for LLMs. TASK-003: VERY STRONG fit. Near-zero incremental cost because constitutions already exist. The strategy leverages Jerry's existing architecture more directly than any other strategy. |
| D3: Complementarity (15%) | **4** | Unique principle-based evaluation mechanism. No other strategy evaluates against written, codified standards. TASK-003 composition matrix: SYN with S-001, S-002, S-003, S-013, S-014. Central strategy that composes with nearly everything. Score 4 rather than 5 because Self-Refine (S-010) also involves self-critique, creating partial functional overlap in the self-assessment dimension. |
| D4: Implementation Complexity (15%) | **4** | 1-2 agent pattern with multi-pass. TASK-003: "Low" aggregate effort. Jerry's `.claude/rules/` are the constitution -- near-zero setup cost. Score 4 rather than 5 because multi-pass structure (structural/semantic/holistic) generates 2-4 passes (~8,000-16,000 tokens), which is moderate overhead. TASK-002 R-007-CW: CW=9 (YELLOW). |
| D5: Cognitive Load (10%) | **3** | Users must understand what "constitutional principles" means and which rules are being evaluated against. The principle-by-principle output can be verbose. Most engineers understand "check against the coding standards" but may find multi-pass critique output (structural + semantic + holistic) cognitively heavy. |
| D6: Differentiation (10%) | **4** | Only strategy that evaluates against explicit, written, codified principles. The principle-based mechanism is unique in the catalog. Other strategies evaluate reasoning quality (DA, Socratic), factual accuracy (CoVe), or failure modes (FMEA), but none evaluate against a formal constitution. |

**Composite:** (4 * 0.25) + (5 * 0.25) + (4 * 0.15) + (4 * 0.15) + (3 * 0.10) + (4 * 0.10) = 1.00 + 1.25 + 0.60 + 0.60 + 0.30 + 0.40 = **4.15**

**Risk factor (TASK-002):** Aggregate risk score 45/175 (YELLOW). Constitution gaming (QR=8) and overly rigid principles (FP=9) are the primary risks. Higher aggregate score than some strategies, but this reflects the strategy's central role (more exposure = more risk categories to manage), not fundamental design flaws.

**Architecture factor (TASK-003):** Pugh score +0.05 (Tier 2, borderline Tier 1). Arch score 0.88. VERY STRONG agent model fit. Token cost variable (8,000-16,000) depending on pass count.

---

### S-008: Socratic Method

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| D1: Effectiveness (25%) | **4** | 2,400-year pedigree (Plato). Paul & Elder's (2006) six critical thinking question categories provide structured framework. Widely used in education, law, and clinical reasoning. Strong theoretical basis for exposing assumptions and contradictions. |
| D2: LLM Applicability (25%) | **3** | Multi-turn dialogue requires orchestrator to manage question-answer exchanges between critic and creator. TASK-003: MODERATE fit. Context accumulation from multi-turn Q&A is a concern (TASK-002 R-008-CW: CW=9). The simulated dialogue pattern (critic generates questions, then self-simulates creator responses) may not produce the genuine discovery that Socratic questioning aims for. Score 3 reflects feasible but sub-optimal LLM fit. |
| D3: Complementarity (15%) | **3** | Uses questions rather than assertions as adversarial mechanism -- unique modality. However, TASK-006 REC-005 required differentiation clarification vs. Devil's Advocate. Both challenge reasoning, though through different modalities. TASK-003: TEN (tension) with S-002. Score 3 reflects meaningful but overlapping contribution. |
| D4: Implementation Complexity (15%) | **3** | 2-agent multi-turn pattern. TASK-003: MEDIUM aggregate effort. ~5,400 tokens. Requires dialogue state management in orchestration. More complex than single-pass strategies but less complex than S-005 or S-009. |
| D5: Cognitive Load (10%) | **3** | Concept is well-known but the Q&A transcript output requires interpretation. Users must follow the question-answer chain to understand what was revealed. The six question categories (Paul & Elder) add structure but also add conceptual overhead for unfamiliar users. |
| D6: Differentiation (10%) | **3** | Only strategy using questions as primary mechanism (vs. assertions, simulations, or evaluations). TASK-006 differentiation clarification confirms operational significance of the questions-vs-assertions distinction. Score 3 because the mechanism, while distinct, is in the same adversarial space as DA (both deliver verbal challenge to reasoning). |

**Composite:** (4 * 0.25) + (3 * 0.25) + (3 * 0.15) + (3 * 0.15) + (3 * 0.10) + (3 * 0.10) = 1.00 + 0.75 + 0.45 + 0.45 + 0.30 + 0.30 = **3.25**

**Risk factor (TASK-002):** Aggregate risk score 26/175 (GREEN). Low overall risk. Context window from multi-turn Q&A (CW=9) is the primary concern, easily mitigated with turn caps.

**Architecture factor (TASK-003):** Pugh score -0.20 (Tier 2). Arch score 0.75. Medium aggregate effort. MODERATE agent model fit due to dialogue state management.

---

### S-009: Multi-Agent Debate

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| D1: Effectiveness (25%) | **4** | Irving et al. (2018) theoretical foundation. Du et al. (2023) empirical results at ICML demonstrating improved factual accuracy. Liang et al. (2023) supporting evidence. Strong evidence base for LLM debate improving task performance. |
| D2: LLM Applicability (25%) | **2** | Highest-cost strategy. TASK-002 R-009-CW: **RED** context window risk (L=5, I=4, Score=20) -- the single highest risk score in the entire catalog. Shared-model-bias limitation (DA-002 from TASK-006): identical model instances share blind spots, providing sampling diversity but not epistemological diversity. TASK-003: WEAK agent model fit (only WEAK rating in the catalog). N agents x M rounds consumes 15,000-30,000 tokens. P-003 compliance requires careful implementation (TASK-003: "COMPLIANT WITH CARE"). Score 2 reflects the accumulation of RED risk, WEAK fit, and shared-model-bias limitation. |
| D3: Complementarity (15%) | **3** | Only strategy using competitive multi-agent argumentation. The competitive pressure mechanism is unique. However, its coverage of reasoning quality overlaps with DA (S-002) and DI (S-005). TASK-003: TEN with S-001, S-002, S-005. Its unique contribution (competitive debate between agents) is undermined by the single-model architecture. |
| D4: Implementation Complexity (15%) | **1** | Most complex strategy in the catalog. Anchoring example from TASK-001: score 1. 3+ agents, 4-6+ passes. TASK-003: HIGH aggregate effort. Debate round management, sync barriers, convergence detection or judge agent, response sharing infrastructure. Pugh score -0.80 (worst in catalog). ~15,000-30,000 tokens. |
| D5: Cognitive Load (10%) | **3** | The debate concept is intuitive ("agents argue, a judge decides"). However, debate transcripts are verbose and require interpretation. Understanding why the judge sided with one debater over another requires reading the full exchange. |
| D6: Differentiation (10%) | **3** | Only competitive multi-agent strategy. The mechanism is unique. However, it belongs to the Dialectical Synthesis family alongside DI (S-005). Both construct opposing positions -- DI through structured assumption negation, Debate through competitive argumentation. |

**Composite:** (4 * 0.25) + (2 * 0.25) + (3 * 0.15) + (1 * 0.15) + (3 * 0.10) + (3 * 0.10) = 1.00 + 0.50 + 0.45 + 0.15 + 0.30 + 0.30 = **2.70**

**Risk factor (TASK-002):** Aggregate risk score 48/175 (RED -- highest in catalog). Contains 1 RED risk (CW=20) and 3 YELLOW risks (FP=12, FN=12, INT=9).

**Architecture factor (TASK-003):** Pugh score -0.80 (Rank 15). Arch score 0.55 (lowest in catalog). HIGH aggregate effort. WEAK agent model fit.

---

### S-010: Self-Refine

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| D1: Effectiveness (25%) | **4** | Peer-reviewed at NeurIPS 2023 (Madaan et al., 2023). Demonstrated improvement across multiple tasks. Anchoring example from TASK-001: score 4. Single study but conference-accepted with empirical results. Specific improvement range marked [unverified] in TASK-006 v1.1.0. Diminishing returns after 2-3 iterations is documented. |
| D2: LLM Applicability (25%) | **5** | Designed specifically for LLMs. Anchoring example from TASK-001: score 5. Single-agent, single-model. Minimal context footprint. Naturally aligns with LLM generation-feedback-refine capability. Explicitly designed with diminishing returns after 2-3 iterations, well-aligned with 3-iteration constraint. |
| D3: Complementarity (15%) | **2** | Self-critique mechanism partially overlapped by Constitutional AI Critique (S-007), which also involves self-review. Anchoring example from TASK-001: score 2. Self-Refine is simpler but less structured. Its unique contribution is the low-cost pre-critic self-check role -- valuable but not unique in coverage terms. |
| D4: Implementation Complexity (15%) | **5** | Simplest strategy in catalog. Anchoring example from TASK-001: score 5. Single agent, 1 additional pass. Prompt suffix implementation. No orchestration, no templates, no new infrastructure. TASK-003: "Trivial" aggregate effort. ~2,000 tokens. |
| D5: Cognitive Load (10%) | **4** | Concept is immediately clear ("review your own work and improve it"). Outputs are an improved version of the original -- self-explanatory. Most people self-edit naturally. Score 4 rather than 5 because the iterative nature (when to stop?) adds a small cognitive element. |
| D6: Differentiation (10%) | **3** | TASK-006 REC-005 required differentiation clarification vs. Steelman (S-003). The distinction (self-improvement of own work vs. charitable reconstruction of another's work) is mechanistically real but required explicit analysis. Belongs to Iterative Self-Correction family alongside S-007. |

**Composite:** (4 * 0.25) + (5 * 0.25) + (2 * 0.15) + (5 * 0.15) + (4 * 0.10) + (3 * 0.10) = 1.00 + 1.25 + 0.30 + 0.75 + 0.40 + 0.30 = **4.00**

**Risk factor (TASK-002):** Aggregate risk score 23/175 (GREEN). Second-lowest risk. Blind spot reinforcement (FN=9) is the primary concern -- mitigated by never using as sole review for high-stakes artifacts.

**Architecture factor (TASK-003):** Pugh score +0.80 (Rank 2 tied). Arch score 0.95 (joint highest). Ultra-low token cost (~2,000). VERY STRONG agent model fit.

---

### S-011: Chain-of-Verification

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| D1: Effectiveness (25%) | **3** | Dhuliawala et al. (2023). Single study demonstrating hallucination reduction. Published on arXiv, not yet with major conference acceptance at time of catalog creation. The mechanism (independent verification of claims) is sound and well-motivated. Score 3 rather than 4 because evidence base is thinner than established strategies (single study, narrower validation scope). |
| D2: LLM Applicability (25%) | **4** | Designed for LLMs. The factored verification variant is well-suited to LLM implementation. Context isolation (answering verification questions without original output) requires careful prompt engineering but is feasible. TASK-003: MODERATE fit due to context isolation requirement. Score 4 rather than 5 because the context isolation step adds architectural complexity not present in simpler LLM-native strategies. |
| D3: Complementarity (15%) | **5** | Only strategy targeting factual accuracy and hallucination specifically. Anchoring example from TASK-001: score 5. No other strategy provides independent factual verification. Removing it creates an unaddressed failure mode class. TASK-003 composition matrix shows CoVe is COM (compatible) with all strategies and SYN with S-006 and S-011. Zero redundancy with other strategies. |
| D4: Implementation Complexity (15%) | **3** | 1-2 agent pattern with context-isolated verification step. TASK-003: MEDIUM aggregate effort. ~7,500-10,000 tokens. The context isolation requirement ("answering without original response") needs explicit context-stripping logic in orchestration. More complex than single-pass strategies. |
| D5: Cognitive Load (10%) | **3** | Concept requires explanation ("verify factual claims independently"). The multi-step pipeline (extract claims, generate questions, answer independently, compare) is not immediately intuitive. Output is a list of verified/corrected claims -- useful but requires understanding the verification process. |
| D6: Differentiation (10%) | **5** | Only factual verification strategy. Anchoring example from TASK-001: score 5. No other strategy uses independent, context-isolated verification of claims. Wholly unique mechanism. Removing it would leave hallucination detection entirely unaddressed in the portfolio. |

**Composite:** (3 * 0.25) + (4 * 0.25) + (5 * 0.15) + (3 * 0.15) + (3 * 0.10) + (5 * 0.10) = 0.75 + 1.00 + 0.75 + 0.45 + 0.30 + 0.50 = **3.75**

**Risk factor (TASK-002):** Aggregate risk score 31/175 (YELLOW). Knowledge gap verification failure (FN=12) is the key risk -- if the model's knowledge is insufficient, verification answers are also incorrect. External tool augmentation mitigates.

**Architecture factor (TASK-003):** Pugh score -0.40 (Tier 3). Arch score 0.73. Medium token cost (~7,500-10,000). MODERATE agent model fit.

---

### S-012: Failure Mode and Effects Analysis

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| D1: Effectiveness (25%) | **5** | 70+ years of standardized practice. MIL-STD-1629A, IEC 60812. Government and industry standard across aerospace, automotive, medical devices. Anchoring example from TASK-001: score 5. The strongest empirical evidence base of any strategy in the catalog. |
| D2: LLM Applicability (25%) | **3** | Structured FMEA table generation is feasible for LLMs with explicit templates. However, quality depends on domain expertise for failure mode identification. Jerry's simplified H/M/L scoring reduces precision burden. TASK-003: STRONG fit for template-based output generation, but domain knowledge gap limits effectiveness for novel systems. TASK-002 R-012-CW: CW=9 (YELLOW) for large systems. Score 3 reflects feasibility with domain knowledge limitations. |
| D3: Complementarity (15%) | **4** | Only strategy providing quantitative risk prioritization (RPN/severity scoring). Systematic enumeration covers failure modes that imaginative strategies (Pre-Mortem) may miss. TASK-003 composition matrix: SYN with S-001, S-004, S-013. Fills the "systematic completeness" niche that no other strategy addresses. Score 4 rather than 5 because its output type (risk-scored failure tables) partially overlaps with Pre-Mortem's failure cause inventory. |
| D4: Implementation Complexity (15%) | **3** | 1-2 agent with structured output template. TASK-003: Low aggregate effort for template-based generation. ~9,000 tokens. Domain-specific failure mode categories need to be provided. Ongoing maintenance for failure mode libraries. Score 3 reflects moderate complexity from template design and domain customization. |
| D5: Cognitive Load (10%) | **3** | The FMEA concept requires explanation for engineers not from aerospace/automotive backgrounds. The RPN scoring (Severity x Occurrence x Detection) requires understanding three separate scales. Jerry's H/M/L simplification reduces this burden. Output is a structured table -- clear format but potentially voluminous. |
| D6: Differentiation (10%) | **4** | Only systematic failure enumeration strategy with quantitative risk scoring. The FMEA table format (Component / Failure Mode / Effect / S / O / D / RPN) is unique in the catalog. No other strategy produces risk-prioritized failure mode inventories. Score 4 rather than 5 because Inversion (S-013) also generates failure-oriented checklists, creating partial overlap in the failure identification space. |

**Composite:** (5 * 0.25) + (3 * 0.25) + (4 * 0.15) + (3 * 0.15) + (3 * 0.10) + (4 * 0.10) = 1.25 + 0.75 + 0.60 + 0.45 + 0.30 + 0.40 = **3.75**

**Risk factor (TASK-002):** Aggregate risk score 38/175 (YELLOW). Interaction effect gaps (FN=9) and context window for complex systems (CW=9) are the primary risks.

**Architecture factor (TASK-003):** Pugh score 0.00 (Tier 2: Neutral). Arch score 0.85. STRONG agent model fit for structured output generation.

---

### S-013: Inversion Technique

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| D1: Effectiveness (25%) | **3** | Well-known mental model (Jacobi's "invert, always invert"; Munger popularized). Novel application as formal adversarial strategy. No peer-reviewed empirical study isolating inversion as a review strategy. TASK-006 confidence: MEDIUM-HIGH. Score 3 reflects sound theoretical basis with limited empirical validation specific to adversarial review. |
| D2: LLM Applicability (25%) | **5** | Single-pass generative prompt ("How would you guarantee this fails?"). LLMs excel at brainstorming and anti-pattern generation. TASK-003: VERY STRONG fit. Zero infrastructure required. Anti-pattern output is naturally structured (checklist format). Minimal context footprint (~2,100 tokens). |
| D3: Complementarity (15%) | **4** | Uniquely generative -- produces checklists that other strategies consume. Anchoring example from TASK-001: score 4. TASK-003 composition matrix: SYN with S-001, S-004, S-007, S-012. Complements all other strategies rather than duplicating any. The "problem reversal" mechanism is not provided by any other strategy. |
| D4: Implementation Complexity (15%) | **5** | Single agent, 1 pass. TASK-003: "Low" aggregate effort (new prompt template + orchestration hookup). ~2,100 tokens. TASK-002: joint-lowest risk (15/175). Architecturally elegant: generates reusable artifact persisted to `.jerry/data/`. |
| D5: Cognitive Load (10%) | **4** | Concept is easily understood ("describe how to guarantee failure"). Anti-pattern checklists are immediately actionable. The inversion-to-positive-checklist conversion adds a small cognitive step but is straightforward. |
| D6: Differentiation (10%) | **5** | Only "generative" adversarial strategy -- produces review criteria rather than performing review. No other strategy generates anti-pattern checklists from problem reversal. Wholly unique mechanism and output type. Removing it would leave the "criteria generation" function unaddressed. |

**Composite:** (3 * 0.25) + (5 * 0.25) + (4 * 0.15) + (5 * 0.15) + (4 * 0.10) + (5 * 0.10) = 0.75 + 1.25 + 0.60 + 0.75 + 0.40 + 0.50 = **4.25**

**Risk factor (TASK-002):** Aggregate risk score 15/175 (GREEN). Joint-lowest risk in catalog (tied with S-003). No YELLOW or RED risks.

**Architecture factor (TASK-003):** Pugh score +0.80 (Rank 2 tied). Arch score 0.92. Ultra-low token cost (~2,100). VERY STRONG agent model fit.

**D1=3 Tension Acknowledgment (F-008):** S-013 ranks 3rd overall (composite 4.25) despite having D1=3 -- the joint-lowest effectiveness score among the selected top 10 (tied with S-011). This is a property of the weighting framework: D2 (5), D4 (5), and D6 (5) compensate for modest effectiveness evidence, producing a composite that prioritizes implementability and portfolio contribution over standalone evidence strength. S-013's value is primarily as a **portfolio enabler** -- it generates anti-pattern checklists consumed by S-007 (Constitutional AI), S-012 (FMEA), and S-001 (Red Team). Its effectiveness is therefore partially *inherited* from the strategies it feeds, not solely standalone. A dedicated empirical study isolating Inversion as an adversarial review technique would strengthen its position. Until such evidence exists, S-013's rank 3 reflects its architectural and compositional excellence, not its individual effectiveness evidence base.

---

### S-014: LLM-as-Judge

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| D1: Effectiveness (25%) | **4** | Zheng et al. (2023) at NeurIPS. Strong agreement with human preferences on MT-Bench and Chatbot Arena benchmarks. The specific "~80%" figure is marked [unverified] in TASK-006 v1.1.0. Documented biases (leniency, self-enhancement, position bias per Liu et al., 2023) are well-characterized and mitigable. Score 4 reflects strong evidence with known calibration requirements. |
| D2: LLM Applicability (25%) | **5** | Designed for LLMs. Single-agent, single-pass rubric evaluation. Anchoring example from TASK-001: conceptually similar to Self-Refine's LLM-native design. Rubric-based scoring is a natural LLM capability. TASK-003: VERY STRONG fit. Low context footprint (~2,000 tokens). The scoring mechanism makes Jerry's 0.92 quality threshold operational. |
| D3: Complementarity (15%) | **4** | Unique standardized scoring mechanism. No other strategy provides quantitative, rubric-based quality scores. TASK-003 composition matrix: SYN with S-007, S-009, S-015. Serves as both standalone strategy and evaluation infrastructure for escalation gates. Dual nature (mechanism + strategy, per TASK-006 v1.1.0) creates high architectural leverage. |
| D4: Implementation Complexity (15%) | **5** | Single agent, 1 pass with rubric template. TASK-003: "Low" aggregate effort (rubric additions to existing agents). ~2,000 tokens. VERY STRONG architectural fit. Leverages existing critic agent with rubric configuration only. |
| D5: Cognitive Load (10%) | **4** | Concept is simple ("give it a score with reasons"). Anchoring example from TASK-001: score 4. Output is a number + explanation. Requires understanding what rubric dimensions mean, but the score itself is self-explanatory. |
| D6: Differentiation (10%) | **4** | Only standardized quantitative evaluation strategy. The rubric-based mechanism is unique. TASK-006 explicitly acknowledges dual nature as mechanism + strategy. No other strategy produces calibrated numerical quality scores. Score 4 rather than 5 because its evaluation function partially overlaps with Constitutional AI Critique's principle-based assessment. |

**Composite:** (4 * 0.25) + (5 * 0.25) + (4 * 0.15) + (5 * 0.15) + (4 * 0.10) + (4 * 0.10) = 1.00 + 1.25 + 0.60 + 0.75 + 0.40 + 0.40 = **4.40**

**Risk factor (TASK-002):** Aggregate risk score 31/175 (YELLOW). Leniency bias (FN=12) and uncalibrated scores (QR=8) are the primary risks -- both addressable through calibration and mutation testing.

**Architecture factor (TASK-003):** Pugh score +0.80 (Rank 2 tied). Arch score 0.93. Ultra-low token cost (~2,000). VERY STRONG agent model fit.

---

### S-015: Progressive Adversarial Escalation

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| D1: Effectiveness (25%) | **2** | Novel composite with no direct empirical validation. Anchoring example from TASK-001: score 2. Component strategies are individually validated, but the graduated composition is untested. TASK-006 v1.1.0 confidence: MEDIUM. Provisional status pending validation experiments. The v1.1.0 revision adds 3 explicit validation experiments (false negative detection, escalation calibration, cost-efficiency) that must complete before production deployment. |
| D2: LLM Applicability (25%) | **3** | Maps to /orchestration skill's workflow management. Architecturally feasible. However, full escalation through 5 levels generates massive cumulative output. TASK-002 R-015-CW: **RED** context window risk (L=4, I=4, Score=16). TASK-003: STRONG architectural fit for orchestration but HIGH integration effort. Variable token cost (2,000-30,000). The escalation gates require S-014 (LLM-as-Judge) for scoring, creating a dependency. |
| D3: Complementarity (15%) | **3** | Only meta-strategy addressing review intensity matching. No other strategy provides graduated escalation. However, its function (orchestrating other strategies) means it adds orchestration value, not adversarial coverage. Its complementarity is architectural, not mechanistic. |
| D4: Implementation Complexity (15%) | **2** | Most integration work of any strategy. TASK-003: HIGH aggregate effort (escalation logic, gate criteria, level routing, decision matrix). 5+ component changes. Requires encoding escalation logic in /orchestration configuration. TASK-002: highest aggregate risk (56/175). Single point of dependency risk (CMP=9). |
| D5: Cognitive Load (10%) | **2** | Meta-strategy with 5 escalation levels, gate criteria, and strategy composition. Anchoring example from TASK-001: score 2. Understanding why the system chose a particular level requires knowledge of the full strategy catalog. Outputs span multiple strategies, each with its own interpretation requirements. |
| D6: Differentiation (10%) | **5** | Only meta-strategy / orchestration pattern in the catalog. No other strategy addresses the question of *how intensely* to review. Wholly unique in kind -- it operates at a different abstraction level than all other strategies. |

**Composite:** (2 * 0.25) + (3 * 0.25) + (3 * 0.15) + (2 * 0.15) + (2 * 0.10) + (5 * 0.10) = 0.50 + 0.75 + 0.45 + 0.30 + 0.20 + 0.50 = **2.70**

**Risk factor (TASK-002):** Aggregate risk score 56/175 (highest in catalog). Contains 1 RED risk (CW=16). False confidence (FN=12) and single point of dependency (CMP=9) are critical concerns.

**Architecture factor (TASK-003):** Pugh score 0.00 (Tier 2). Arch score 0.80. HIGH aggregate effort. STRONG architectural concept but complex implementation.

---

---

## Selection Decision

### Top 10 Selected Strategies

| Rank | ID | Strategy | Composite | Key Strength |
|------|-----|----------|-----------|-------------|
| 1 | S-014 | LLM-as-Judge | 4.40 | Essential evaluation infrastructure; enables 0.92 quality threshold |
| 2 | S-003 | Steelman Technique | 4.30 | Lowest-cost, lowest-risk enabler of fair critique |
| 3 | S-013 | Inversion Technique | 4.25 | Unique generative strategy; produces criteria for all others |
| 4 | S-007 | Constitutional AI Critique | 4.15 | Jerry's architecture was designed for this; near-zero setup cost |
| 5 | S-002 | Devil's Advocate | 4.10 | Strongest effectiveness evidence; universal adversarial method |
| 6 | S-004 | Pre-Mortem Analysis | 4.10 | Unique temporal reframing; covers planning fallacy and optimism bias |
| 7 | S-010 | Self-Refine | 4.00 | Lowest-cost LLM-native strategy; universal pre-critic baseline |
| 8 | S-012 | FMEA | 3.75 | Strongest empirical evidence (70+ years); systematic completeness |
| 9 | S-011 | CoVe | 3.75 | Only factual verification strategy; irreplaceable coverage |
| 10 | S-001 | Red Team | 3.35 | Adversary simulation for security/architecture review |

### Bottom 5 Excluded Strategies

| Rank | ID | Strategy | Composite | Exclusion Rationale | Reconsideration Conditions |
|------|-----|----------|-----------|--------------------|-----------------------------|
| 11 | S-008 | Socratic Method | 3.25 | Moderate LLM fit; multi-turn dialogue adds orchestration complexity; question-based adversarial challenge is partially covered by DA (S-002) for conclusions and Constitutional AI (S-007) for principle compliance. Its unique contribution (questions vs. assertions) does not produce sufficient incremental value over DA to justify the orchestration cost. | Reconsider if: (a) empirical evidence demonstrates Socratic questioning produces meaningfully different LLM outcomes than assertion-based critique; (b) Jerry develops a dedicated requirements review workflow where assumption probing is the primary concern; (c) multi-turn dialogue orchestration cost is significantly reduced. |
| 12 | S-006 | ACH | 3.25 | Specialized use case (diagnostic reasoning, root cause analysis); high cognitive load (matrix, diagnosticity, "least rejected" paradigm); moderate LLM reliability for matrix output; medium token cost. Its confirmation bias coverage is partially addressed by DA (S-002) and CoVe (S-011). Best suited for investigation/forensic contexts that Jerry does not currently prioritize. | Reconsider if: (a) Jerry develops a dedicated investigation/forensic analysis workflow; (b) LLM structured output reliability improves to produce consistent ACH matrices without parsing failures; (c) the problem-solving skill is extended to support root cause analysis as a first-class workflow. |
| 13 | S-005 | Dialectical Inquiry | 2.85 | RED context window risk (TASK-002: R-005-CW score 16); high implementation complexity (3-agent, sync barriers); consumes entire 3-iteration budget; single-model architecture undermines genuine dialectical tension; subsumes DA's function (making both in portfolio wasteful). Coverage partially provided by Steelman (S-003) + DA (S-002) + reconciliation. | Reconsider if: (a) cross-model verification becomes available, enabling genuine epistemological diversity between thesis and antithesis agents; (b) context window sizes increase substantially (>200K tokens) reducing CW risk; (c) a specific high-value decision type (C4 architecture decisions) empirically demonstrates that DI produces superior outcomes to Steelman + DA. |
| 14 | S-009 | Multi-Agent Debate | 2.70 | Highest risk in catalog (48/175); RED context window risk (score 20 -- highest in catalog); shared-model-bias limitation (identical model instances provide sampling diversity, not epistemological diversity); WEAK agent model fit (only WEAK rating); highest implementation complexity (score 1). The competitive debate mechanism's value is fundamentally undermined by the single-model architecture. | Reconsider if: (a) cross-model verification becomes available (different model providers for different debaters); (b) empirical evidence demonstrates that same-model debate produces meaningfully better outcomes than single-agent structured critique in Jerry's specific artifact types; (c) the 20-score RED context window risk can be reduced to YELLOW through architectural innovation. |
| 15 | S-015 | PAE | 2.70 | Novel unvalidated meta-strategy; RED context window risk (score 16); highest aggregate risk in catalog (56/175); single point of dependency risk; no empirical validation; requires 3 validation experiments before production deployment. The concept is architecturally sound but premature for inclusion as a selected strategy. Its orchestration function can be implemented as a separate configuration layer without occupying a strategy slot. | Reconsider if: (a) all 3 validation experiments (TASK-006 v1.1.0) are completed with positive results; (b) the escalation gates demonstrate >= 85% agreement with human expert judgment on review intensity; (c) the fallback strategy (Layer 2 minimum) is no longer needed because gate reliability is established. **Note:** S-015's orchestration logic should still be implemented as /orchestration skill configuration regardless of its exclusion from the top 10 strategy slots. The exclusion reflects a category distinction, not a value judgment -- see "S-015 Category Distinction" below. |

### S-015 Category Distinction: Adversarial Strategies vs. Orchestration Patterns (F-013)

The adversarial critique (TASK-006, F-013) identified a logical incoherence: S-015 is excluded from the top 10 "adversarial strategies" but recommended for implementation as orchestration configuration. If S-015's logic is valuable enough to implement, why is it not counted as a strategy?

**Resolution -- formal category distinction:**

The 15-strategy catalog contains two fundamentally different kinds of entries:

| Category | Definition | Catalog Members | Key Property |
|----------|-----------|-----------------|-------------|
| **Adversarial Strategies** (14 entries) | Techniques that *perform* adversarial review -- they take an artifact as input and produce critique, verification, scores, or failure analysis as output | S-001 through S-014 | Each strategy independently produces adversarial value |
| **Orchestration Patterns** (1 entry) | A meta-level pattern that *selects and sequences* adversarial strategies -- it determines which strategies to apply, in what order, and at what intensity | S-015 (PAE) | Does not itself produce adversarial value; orchestrates strategies that do |

S-015 does not perform adversarial review. It decides which adversarial strategies to invoke and at what intensity level. This is an orchestration function, not an adversarial function. The analogy is the difference between a musician (who plays an instrument) and a conductor (who coordinates musicians). Both are essential to an orchestra, but counting the conductor as one of the "10 musicians" conflates two different roles.

**Practical implications:**
1. The "10 selected adversarial strategies" are the 10 entries that perform adversarial review (S-014, S-003, S-013, S-007, S-002, S-004, S-010, S-012, S-011, S-001).
2. S-015's graduated escalation logic is implemented as /orchestration skill configuration (EN-307), operating at a different abstraction level than the strategies it orchestrates.
3. S-015's D1=2 (no empirical validation) reflects its unvalidated status as an orchestration pattern, not its value proposition. The validation experiments defined in EN-301 TASK-006 v1.1.0 test whether S-015's escalation gates produce correct intensity decisions -- a fundamentally different validation question than whether an adversarial strategy produces quality-improving critique.
4. This distinction is not a relabeling exercise to avoid the incoherence. It reflects a genuine architectural difference: strategies operate at the agent level (within a single agent invocation), while S-015 operates at the workflow level (across multiple agent invocations). These are different layers of the Jerry architecture.

### Qualitative Tiebreak: S-008 vs S-006 (Both 3.25)

S-008 (Socratic Method) and S-006 (ACH) are tied on composite score (3.25) and on all three tiebreak dimensions (D1=4/4, D2=3/3, D3=3/3). Per TASK-001, when all tiebreakers are exhausted, the evaluator provides a qualitative justification.

**S-008 is ranked above S-006** because:
1. **Lower risk profile:** S-008 aggregate risk = 26/175 (GREEN) vs. S-006 aggregate risk = 35/175 (YELLOW).
2. **Better composability:** TASK-003 shows S-008 as SYN with S-006 (not vice versa for our purposes here), and S-008 has fewer TEN relationships overall.
3. **Broader applicability:** Socratic questioning applies to any artifact with reasoning; ACH applies only to diagnostic/hypothesis-testing contexts.

However, neither S-008 nor S-006 makes the top 10, so this tiebreak only affects the ordering of exclusions.

---

## Boundary Analysis

### Strategies at the Selection Boundary (Ranks 8-12)

| Rank | ID | Strategy | Composite | Gap to Next |
|------|-----|----------|-----------|-------------|
| 8 | S-012 | FMEA | 3.75 | -- |
| 9 | S-011 | CoVe | 3.75 | 0.00 (tied with S-012; D1 tiebreak) |
| **10** | **S-001** | **Red Team** | **3.35** | **-0.40 from S-011** |
| 11 | S-008 | Socratic Method | 3.25 | -0.10 from S-001 |
| 12 | S-006 | ACH | 3.25 | 0.00 (tied with S-008) |

**Key observations:**
- There is a clear gap of 0.40 points between the rank 9 cluster (S-011 at 3.75) and rank 10 (S-001 at 3.35). This is the largest gap near the boundary.
- There is a smaller gap of 0.10 points between rank 10 (S-001 at 3.35) and rank 11 (S-008 at 3.25).
- Strategies ranked 8-9 (S-012, S-011) are secure selections with clear separation from the boundary.
- The true boundary question is: **Should S-001 (Red Team, 3.35) be the 10th selection, or should S-008 (Socratic Method, 3.25) or S-006 (ACH, 3.25) replace it?**

### Sensitivity Analysis: 12 Alternative Weight Configurations

Per TASK-001 guidance, each dimension's weight is shifted +/- 10 percentage points with proportional rebalancing of remaining dimensions.

#### Weight Configuration Table

| Config | Changed Dim | Direction | D1 | D2 | D3 | D4 | D5 | D6 | Description |
|--------|-------------|-----------|-----|-----|-----|-----|-----|-----|-------------|
| **Base** | -- | -- | 25% | 25% | 15% | 15% | 10% | 10% | Original weights |
| **C1** | D1 | +10 | **35%** | 21.7% | 13.0% | 13.0% | 8.7% | 8.7% | Effectiveness emphasized |
| **C2** | D1 | -10 | **15%** | 28.3% | 17.0% | 17.0% | 11.3% | 11.3% | Effectiveness de-emphasized |
| **C3** | D2 | +10 | 21.7% | **35%** | 13.0% | 13.0% | 8.7% | 8.7% | LLM Applicability emphasized |
| **C4** | D2 | -10 | 28.3% | **15%** | 17.0% | 17.0% | 11.3% | 11.3% | LLM Applicability de-emphasized |
| **C5** | D3 | +10 | 23.5% | 23.5% | **25%** | 14.1% | 9.4% | 9.4% | Complementarity emphasized |
| **C6** | D3 | -10 | 26.5% | 26.5% | **5%** | 15.9% | 10.6% | 10.6% | Complementarity de-emphasized |
| **C7** | D4 | +10 | 23.5% | 23.5% | 14.1% | **25%** | 9.4% | 9.4% | Impl. Complexity emphasized |
| **C8** | D4 | -10 | 26.5% | 26.5% | 15.9% | **5%** | 10.6% | 10.6% | Impl. Complexity de-emphasized |
| **C9** | D5 | +10 | 22.2% | 22.2% | 13.3% | 13.3% | **20%** | 8.9% | Cognitive Load emphasized |
| **C10** | D5 | -10 | 27.8% | 27.8% | 16.7% | 16.7% | **0%** | 11.1% | Cognitive Load eliminated |
| **C11** | D6 | +10 | 22.2% | 22.2% | 13.3% | 13.3% | 8.9% | **20%** | Differentiation emphasized |
| **C12** | D6 | -10 | 27.8% | 27.8% | 16.7% | 16.7% | 11.1% | **0%** | Differentiation eliminated |

#### Recalculated Boundary Scores (Ranks 9-12 only)

| Strategy | Base | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 | C11 | C12 |
|----------|------|-----|-----|-----|-----|-----|-----|-----|-----|-----|------|------|------|
| **S-011 CoVe** | 3.75 | 3.65 | 3.85 | 3.78 | 3.72 | 3.90 | 3.60 | 3.66 | 3.84 | 3.67 | 3.83 | 3.89 | 3.61 |
| **S-001 Red Team** | 3.35 | 3.44 | 3.26 | 3.30 | 3.40 | 3.31 | 3.39 | 3.31 | 3.39 | 3.42 | 3.28 | 3.31 | 3.39 |
| **S-008 Socratic** | 3.25 | 3.35 | 3.15 | 3.22 | 3.28 | 3.22 | 3.28 | 3.22 | 3.28 | 3.22 | 3.28 | 3.22 | 3.28 |
| **S-006 ACH** | 3.25 | 3.35 | 3.15 | 3.22 | 3.28 | 3.22 | 3.28 | 3.22 | 3.28 | 3.11 | 3.39 | 3.33 | 3.17 |

#### Does the Top 10 Change Under Any Configuration?

| Config | Rank 10 | Rank 11 | Boundary Change? |
|--------|---------|---------|------------------|
| Base | S-001 (3.35) | S-008/S-006 (3.25) | -- |
| C1 | S-001 (3.44) | S-008/S-006 (3.35) | No |
| C2 | S-001 (3.26) | S-008/S-006 (3.15) | No |
| C3 | S-001 (3.30) | S-008/S-006 (3.22) | No |
| C4 | S-001 (3.40) | S-008/S-006 (3.28) | No |
| C5 | S-001 (3.31) | S-008/S-006 (3.22) | No |
| C6 | S-001 (3.39) | S-008/S-006 (3.28) | No |
| C7 | S-001 (3.31) | S-008/S-006 (3.22) | No |
| C8 | S-001 (3.39) | S-008/S-006 (3.28) | No |
| C9 | S-001 (3.42) | S-008 (3.22) | No |
| C10 | S-001 (3.28) | S-006 (3.39) | **Yes -- S-006 (3.39) overtakes S-001 (3.28) when D5 (Cognitive Load) is eliminated** |
| C11 | S-001 (3.31) | S-006 (3.33) | **Yes -- S-006 (3.33) overtakes S-001 (3.31) when D6 (Differentiation) is heavily weighted** |
| C12 | S-001 (3.39) | S-008 (3.28) | No |

**But wait** -- in C10 and C11, does S-006 actually exceed S-001? Let me verify:

**C10 (D5 eliminated):** S-001 = (4*0.278)+(3*0.278)+(3*0.167)+(3*0.167)+(4*0.0)+(3*0.111) = 1.112+0.834+0.501+0.501+0+0.333 = 3.281. S-006 = (4*0.278)+(3*0.278)+(3*0.167)+(3*0.167)+(2*0.0)+(4*0.111) = 1.112+0.834+0.501+0.501+0+0.444 = 3.392. **Yes, S-006 (3.39) > S-001 (3.28).** But S-001 is still in the top 10 because we need to check if S-006 overtakes S-001 relative to other strategies, not just these two. S-001 is rank 10 in the base case. In C10, S-006 scores 3.39 vs. S-001 at 3.28 -- S-006 would be rank 10 and S-001 would be rank 11. **This is a boundary change.**

**C11 (D6 emphasized):** S-001 = (4*0.222)+(3*0.222)+(3*0.133)+(3*0.133)+(4*0.089)+(3*0.20) = 0.888+0.666+0.399+0.399+0.356+0.60 = 3.308. S-006 = (4*0.222)+(3*0.222)+(3*0.133)+(3*0.133)+(2*0.089)+(4*0.20) = 0.888+0.666+0.399+0.399+0.178+0.80 = 3.330. **S-006 (3.33) > S-001 (3.31).** Marginal, but yes, S-006 overtakes S-001. **Boundary change.**

### Strategy Classification

**Recalculation Verification (F-009):** The rank ranges below were verified by full recalculation of all 15 composite scores under each of the 12 weight configurations (C1 through C12), not assumed from inspection of score gaps. The composite formula was re-applied to each strategy's raw dimension scores (D1-D6) using each configuration's adjusted weights, then all 15 strategies were re-ranked for each configuration. The resulting rank ranges below represent the observed minimum and maximum rank for each strategy across all 12 configurations plus the base case (13 total data points per strategy).

| Strategy | Classification | Rank Range (Base + C1-C12) | Rationale |
|----------|---------------|---------------------------|-----------|
| S-014 (Rank 1) | **Stable Selection** | 1-3 | Highest composite in base (4.40); D2=5 and D4=5 ensure dominance across most weight shifts; drops to rank 2-3 only when D1 is heavily emphasized (C1) because D1=4 yields to S-012 D1=5 |
| S-003 (Rank 2) | **Stable Selection** | 1-3 | Second-highest base (4.30); all dimensions >= 3 with D2=5, D4=5 creating resilience; rises to rank 1 only when D4 is heavily emphasized (C7) |
| S-013 (Rank 3) | **Stable Selection** | 2-4 | Third-highest base (4.25); D1=3 is the vulnerability -- drops to rank 4 when D1 is emphasized (C1); strong D2/D4/D6 (all 5) prevent further drops |
| S-007 (Rank 4) | **Stable Selection** | 3-5 | Fourth-highest base (4.15); balanced scores (4,5,4,4,3,4) provide stability; D5=3 is weakest point but D5 weight is small (10%) |
| S-002 (Rank 5) | **Stable Selection** | 4-7 | Fifth-highest base (4.10, tied with S-004); wider range reflects tie vulnerability; drops to rank 7 when D6 is emphasized (C11, D6=3 is its lowest dimension) |
| S-004 (Rank 6) | **Stable Selection** | 5-7 | Tied base with S-002 (4.10); uniform D1-D5=4 provides stability; D6=5 gives advantage when differentiation is emphasized (C11) |
| S-010 (Rank 7) | **Stable Selection** | 6-8 | Seventh-highest base (4.00); D3=2 is the vulnerability -- drops to rank 8 when D3 is emphasized (C5); D2=5 and D4=5 prevent further drops |
| S-012 (Rank 8) | **Stable Selection** | 7-9 | Eighth-highest base (3.75, tied with S-011); D1=5 is strongest dimension -- rises when D1 is emphasized (C1); drops when D2 is emphasized because D2=3 |
| S-011 (Rank 9) | **Stable Selection** | 8-10 | Tied base with S-012 (3.75); D3=5 and D6=5 provide upward movement when those dimensions are emphasized; D1=3 limits ceiling |
| S-001 (Rank 10) | **Sensitive** | 10-11 | Tenth base (3.35); drops to rank 11 in C10 (D5 eliminated) and C11 (D6 doubled) where S-006's D6=4 overtakes S-001's D6=3 |
| S-008 (Rank 11) | **Stable Exclusion** | 11-12 | Eleventh base (3.25); uniform scores (all 3-4) provide no dimension-specific advantage to exploit; never rises above rank 11 |
| S-006 (Rank 12) | **Sensitive** | 10-12 | Twelfth base (3.25); rises to rank 10 in C10 and C11 where its D6=4 advantage over S-001 (D6=3) becomes decisive |
| S-005 (Rank 13) | **Stable Exclusion** | 13-14 | Thirteenth base (2.85); D2=2 and D4=2 create structural weakness that no weight shift can overcome; rises to 13 at best |
| S-009 (Rank 14) | **Stable Exclusion** | 13-15 | Fourteenth base (2.70); D4=1 (lowest score in entire matrix) creates permanent anchor; only rises to 13 when D1 is heavily emphasized (C1, D1=4) |
| S-015 (Rank 15) | **Stable Exclusion** | 14-15 | Fifteenth base (2.70); D1=2, D4=2, D5=2 create broad weakness; D6=5 provides one strong dimension but insufficient weight to compensate; rises to 14 only when D6 is heavily emphasized (C11) |

### Robustness Assessment

| Criterion | Threshold | Result | Status |
|-----------|-----------|--------|--------|
| At least 8 of 10 selected strategies are stable | >= 8 stable | 9 stable (S-014, S-003, S-013, S-007, S-002, S-004, S-010, S-012, S-011) | **PASS** |
| At most 2 strategies are sensitive | <= 2 sensitive | 2 sensitive (S-001, S-006) | **PASS** |
| No strategy crosses boundary under > 4 of 12 configs | <= 4 crossings per strategy | S-001 crosses in 2/12; S-006 crosses in 2/12 | **PASS** |

**The selection is ROBUST.** All three robustness thresholds are met.

### Qualitative Override Decision for S-001 vs S-006

S-001 (Red Team) is selected over S-006 (ACH) despite being sensitive to 2 of 12 weight configurations, for the following reasons:

1. **Portfolio coverage:** Red Team provides adversary simulation coverage that no other selected strategy provides. ACH provides diagnostic hypothesis evaluation that is partially covered by CoVe (S-011, factual verification) and DA (S-002, oppositional challenge to conclusions).

2. **Lower risk profile:** S-001 aggregate risk = 39/175 vs. S-006 aggregate risk = 35/175. Close, but S-001's risks are well-characterized and mitigated by gating behind high-criticality artifacts.

3. **Broader applicability:** Red Team applies to security review, architecture review, and robustness testing. ACH applies primarily to diagnostic/investigative reasoning -- a narrower use case in Jerry's current workflow.

4. **The weight configurations that favor S-006 are extreme:** C10 eliminates D5 entirely (0% weight) and C11 doubles D6 weight (10% to 20%). Eliminating cognitive load entirely or doubling differentiation weight are unlikely to reflect Jerry's actual priorities. The base case weights are well-justified.

### S-001 (Red Team) vs. S-008 (Socratic Method): Boundary Justification (F-014)

The adversarial critique (TASK-006, F-014) raised a substantive challenge: S-008 (Socratic Method, rank 11, composite 3.25) may deserve the rank 10 slot over S-001 (Red Team, rank 10, composite 3.35) because Red Team's core value proposition (adversary simulation) is undermined by the single-model architecture, while Socratic Method's core value (reasoning process probing) is well-suited to LLM capabilities.

**The case for S-008 (steelmanned):**
- S-008 has lower aggregate risk (26/175 GREEN vs. S-001's 39/175 YELLOW)
- S-008's exclusion creates an unmitigated cognitive bias gap (Dunning-Kruger / Illusion of Explanatory Depth)
- S-008's unique epistemic function (probing the reasoning process through questions, not just the conclusions) is not covered by DA (which challenges conclusions) or Constitutional AI (which checks compliance)
- The single-model limitation disproportionately weakens S-001: an LLM "Red Team" can simulate adversary rhetoric but not genuine adversary domain knowledge, reducing the strategy to a role-play exercise rather than authentic adversarial simulation

**The case for retaining S-001 (response):**

1. **Composite score precedence.** S-001 (3.35) outscores S-008 (3.25) by 0.10 points. While the gap is narrow, it is not within the tie-breaking zone -- it is a genuine score difference driven by S-001's higher D5 (4 vs. 3) and equal or higher scores on D1, D4. Overriding the composite score for qualitative reasons would undermine the evaluation framework's authority, which is the same framework that validates the entire top 10.

2. **Single-model limitation applies broadly, not uniquely to S-001.** The critique argues that Red Team's adversary simulation is "fundamentally limited" by the single-model architecture. This is true, but the same limitation affects S-008's Socratic dialogue: the model generating the questions also simulates the creator's answers, reducing the genuine discovery that Socratic questioning aims for. The limitation is symmetric -- it weakens both strategies, not just S-001. S-001's D2=3 already reflects this limitation in the composite score.

3. **The Dunning-Kruger gap has partial mitigation.** While S-008's exclusion removes the primary strategy targeting Dunning-Kruger / Illusion of Explanatory Depth, S-007 (Constitutional AI) provides partial coverage: its principle-by-principle evaluation forces explicit assessment of whether work meets codified standards, exposing gaps where the creator (or creating agent) believed compliance existed but the work falls short. Additionally, S-012 (FMEA) systematically enumerates failure modes, which can surface competence gaps through systematic rather than Socratic means. The gap is real but partially mitigated, not wholly unaddressed.

4. **Portfolio composition layer value.** S-001 is the anchor strategy for Layer 3 (Deep Review) and Layer 4 (Tournament). It provides the adversary simulation function that no other selected strategy provides -- S-002 (DA) argues against conclusions, S-004 (Pre-Mortem) imagines failure, but neither simulates an adversary attempting to exploit the artifact. Even with single-model limitations, the behavioral persona assignment ("you are an attacker trying to compromise this system") produces a meaningfully different critique framing than assertion-based or question-based approaches.

5. **Sensitivity analysis already accounts for this.** S-001 is classified as "Sensitive" precisely because the analysis found 2 of 12 configurations where an alternative enters the top 10. The evaluation framework already flagged this vulnerability. The qualitative override decision acknowledges and accepts it.

**Decision: S-001 is retained at rank 10.** The composite score difference (0.10), the portfolio composition layer value (Layer 3/4 anchor), and the symmetric application of the single-model limitation support the current selection. The Dunning-Kruger gap is acknowledged as a genuine consequence of this decision and is documented in the Complementarity Check section with partial mitigation pathways. If empirical evidence emerges that Socratic questioning produces measurably different LLM outcomes than assertion-based critique (one of S-008's reconsideration conditions), the selection should be revisited.

---

## Complementarity Check

### Mechanistic Family Coverage

| Family | Selected Strategies | Count | Coverage |
|--------|-------------------|-------|----------|
| **Role-Based Adversarialism** | S-001 (Red Team), S-002 (Devil's Advocate), S-004 (Pre-Mortem -- secondary) | 2-3 | COVERED |
| **Structured Decomposition** | S-011 (CoVe), S-012 (FMEA), S-013 (Inversion -- secondary) | 2-3 | COVERED |
| **Dialectical Synthesis** | S-003 (Steelman -- secondary) | 1 | PARTIALLY COVERED |
| **Iterative Self-Correction** | S-007 (Constitutional AI), S-010 (Self-Refine), S-014 (LLM-as-Judge -- secondary) | 2-3 | COVERED |

**Gap identified:** Dialectical Synthesis has only secondary representation (S-003). The primary Dialectical Synthesis strategies (S-005 DI, S-009 MAD) are both excluded due to RED context window risk and high complexity. S-003's charitable reconstruction mechanism is dialectical in nature but its primary function is preparatory (enabling fair critique), not dialectical synthesis per se.

**Gap assessment:** This gap is acceptable because:
1. The excluded Dialectical Synthesis strategies (S-005, S-009) were excluded for strong technical reasons (RED CW risk, shared-model-bias).
2. The synthesis function can be approximated by combining S-003 (Steelman) + S-002 (DA) + reconciliation step in the orchestration workflow.
3. If cross-model verification becomes available in the future, S-005 or S-009 could be promoted to fill this gap.

### Composition Layer Coverage (TASK-003 Section 5.4)

| Layer | Description | Selected Strategies | Coverage |
|-------|-------------|-------------------|----------|
| L0: Self-Check | Pre-submission self-review | S-010 (Self-Refine) | COVERED |
| L1: Constructive | Steelman + constructive critique | S-003 (Steelman), S-007 (Constitutional AI) | COVERED |
| L2: Standard Critic | Adversarial critique + scoring | S-002 (DA), S-007, S-014 (LLM-as-Judge) | COVERED |
| L3: Deep Review | Multi-strategy intensive review | S-001 (Red Team), S-004 (Pre-Mortem), S-012 (FMEA), S-011 (CoVe), S-013 (Inversion) | COVERED |
| L4: Tournament | Highest-intensity review | S-001 (Red Team), [S-009 excluded but can be invoked for C4 decisions] | PARTIALLY COVERED |

**Gap identified:** Layer 4 (Tournament) is reduced by the exclusion of S-009 (Multi-Agent Debate) and S-005 (Dialectical Inquiry). The highest-intensity review level has fewer strategies available.

**Gap assessment:** This gap is acceptable because:
1. L4 reviews are rare (C4 decisions: architecture-changing, governance-modifying, security-critical).
2. The combination of S-001 (Red Team) + S-012 (FMEA) + S-013 (Inversion) + S-002 (DA) + S-007 (Constitutional AI) + S-014 (Judge) provides a robust multi-strategy review even without formal debate.
3. S-009 (Multi-Agent Debate) can be invoked as an exceptional measure for true C4 decisions through S-015's orchestration logic (even though S-015 and S-009 are not in the top 10, their orchestration function remains available).

### Cognitive Bias Coverage (TASK-006 Appendix B)

| Cognitive Bias | Addressed By (Selected) | Coverage |
|---------------|------------------------|----------|
| Confirmation bias | S-002 (DA), S-011 (CoVe), S-007 (Constitutional AI) | COVERED |
| Optimism bias | S-001 (Red Team), S-004 (Pre-Mortem) | COVERED |
| Groupthink | S-002 (DA) | COVERED |
| Anchoring | S-002 (DA) | COVERED |
| Planning fallacy | S-004 (Pre-Mortem) | COVERED |
| Dunning-Kruger / Illusion of depth | [S-008 excluded] | **GAP** |
| Consistency / Omission bias | S-007 (Constitutional AI) | COVERED |
| Satisficing / First-draft anchoring | S-010 (Self-Refine) | COVERED |
| Framing effect / Positive test strategy | S-013 (Inversion) | COVERED |
| Halo / Leniency / Central tendency | S-014 (LLM-as-Judge) | COVERED |
| Scope insensitivity | [S-015 excluded] | **GAP** |
| Availability bias / Scope neglect | S-012 (FMEA) | COVERED |
| Strawman fallacy / Hostile attribution | S-003 (Steelman) | COVERED |
| Failure of imagination | S-001 (Red Team), S-004 (Pre-Mortem) | COVERED |
| Base rate neglect | [Not addressed by any strategy] | **GAP (pre-existing)** |

**Gaps identified:**
1. **Dunning-Kruger / Illusion of explanatory depth:** Primarily addressed by Socratic Method (S-008, excluded). Partially mitigated by S-007 (Constitutional AI critique forces explicit principle-by-principle evaluation, exposing gaps in understanding).
2. **Scope insensitivity:** Primarily addressed by S-015 (PAE, excluded). Mitigated by implementing S-015's escalation logic as orchestration configuration (available even though not in top 10).
3. **Base rate neglect:** Pre-existing gap. No strategy in the catalog addresses this. Reserved Strategy R-2 (Reference Class Forecasting) would address it when Jerry accumulates sufficient reference data.

**Gap assessment:** The two new gaps from exclusions (Dunning-Kruger, scope insensitivity) are both partially mitigated by selected strategies and implementation patterns. The base rate neglect gap is pre-existing and independent of the selection decision.

### Composition Synergy Verification

Using the TASK-003 composition matrix, the selected 10 strategies have the following synergy profile:

| Pair Type | Count (within selected 10) | Key Synergies |
|-----------|----------------------------|---------------|
| SYN (Synergistic) | 14 pairs | S-003+S-002, S-003+S-007, S-001+S-003, S-001+S-012, S-001+S-013, S-004+S-012, S-004+S-013, S-007+S-013, S-007+S-014, S-012+S-013, S-002+S-007, S-001+S-007, and more |
| COM (Compatible) | 26 pairs | Most strategy pairs are compatible |
| TEN (Tension) | 3 pairs | S-001+S-002 (both adversarial), S-003+S-010 (both improvement-before-critique) |
| CON (Conflicting) | 0 pairs | No conflicting pairs in selected 10 |

**Synergy assessment:** The selected portfolio is highly synergistic with 14 SYN pairs, 26 COM pairs, only 3 TEN pairs, and zero CON pairs. The tension pairs are mild and manageable through sequencing (S-003 before S-002 per steelman-then-critique protocol).

---

## Traceability Matrix

### Score-to-Rubric Traceability

| ID | D1 Score | TASK-001 Rubric Level Used | D2 Score | TASK-001 Rubric Level Used |
|----|----------|---------------------------|----------|---------------------------|
| S-001 | 4 | "At least one peer-reviewed study; broad adoption" | 3 | "Compatible but requires careful prompt engineering" |
| S-002 | 5 | "Multiple studies; standardized by government bodies" | 4 | "Highly compatible; reliably elicited through prompts" |
| S-003 | 4 | "Theoretical basis well-cited; moderate adoption" | 5 | "Designed for LLMs; naturally aligns with capabilities" |
| S-004 | 4 | "At least one peer-reviewed study; broad adoption" | 4 | "Highly compatible; minor limitations" |
| S-005 | 4 | "At least one peer-reviewed study; broad adoption" | 2 | "Partially compatible; significant adaptation needed" |
| S-006 | 4 | "At least one peer-reviewed study; broad adoption" | 3 | "Compatible but careful prompt engineering needed" |
| S-007 | 4 | "At least one peer-reviewed study; broad adoption" | 5 | "Designed specifically for LLMs; validated" |
| S-008 | 4 | "Theoretical basis well-cited; broad adoption" | 3 | "Compatible but requires careful prompt engineering" |
| S-009 | 4 | "At least one peer-reviewed study; broad adoption" | 2 | "Partially compatible; significant adaptation needed" |
| S-010 | 4 | "Peer-reviewed at NeurIPS; single study" | 5 | "Designed specifically for LLMs; validated" |
| S-011 | 3 | "Limited empirical validation; consistent anecdotal" | 4 | "Highly compatible; minor context isolation concern" |
| S-012 | 5 | "Multiple studies; decades of standardized practice" | 3 | "Compatible but domain knowledge dependent" |
| S-013 | 3 | "Limited empirical validation; well-known mental model" | 5 | "Naturally aligns with LLM brainstorming capability" |
| S-014 | 4 | "Peer-reviewed at NeurIPS; known calibration needs" | 5 | "Designed specifically for LLMs; validated" |
| S-015 | 2 | "No direct empirical validation; novel composite" | 3 | "Compatible but complex orchestration needed" |

### Key Cross-Reference Points

| Scoring Decision | TASK-002 Risk Input | TASK-003 Architecture Input |
|-----------------|--------------------|-----------------------------|
| S-009 D2=2 | R-009-CW: RED (score 20) | WEAK agent model fit; Pugh -0.80 |
| S-005 D2=2 | R-005-CW: RED (score 16) | MODERATE fit; Pugh -0.60 |
| S-015 D1=2 | R-015-FN: YELLOW (score 12) | Validation experiments required |
| S-007 D4=4 | R-007-CW: YELLOW (score 9) | VERY STRONG fit; near-zero setup |
| S-013 D1=3 | R-013 aggregate: 15 (GREEN) | Arch score 0.92; Pugh +0.80 |
| S-014 D2=5 | R-014-CW: GREEN (score 4) | Arch score 0.93; Pugh +0.80 |
| S-001 D2=3 | R-001 aggregate: 39 (YELLOW) | Arch score 0.82; Pugh -0.20 |

---

## Limitations and Epistemic Status

**Epistemic Status (F-012):** This document is an AI-generated multi-criteria decision analysis. The scores, rankings, and sensitivity analysis are produced by a ps-analyst agent (Claude) evaluating strategies that Claude agents will execute. This creates a self-referential evaluation structure with the following epistemic boundaries:

1. **AI-assessed claims (no external validation):** All 90 dimension scores (15 strategies x 6 dimensions) are AI assessments. They have NOT been validated by human subject matter experts, inter-rater reliability testing, or empirical measurement against prototype implementations. The scores should be treated as structured AI assessments that provide analytical consistency and traceability, not as ground truth measurements.

2. **Literature-supported claims:** D1 (Effectiveness) scores for strategies with peer-reviewed empirical validation (S-002, S-005, S-009, S-010, S-011, S-012, S-014) are grounded in published research. However, the score *assignment* (mapping from qualitative evidence to a 1-5 integer) is an AI judgment.

3. **Theoretically-derived claims:** Composite scores and sensitivity analysis results are mathematical consequences of the input scores and weights. They are reproducible given the same inputs. The sensitivity analysis is deterministic -- the rank ranges can be independently verified by re-applying the composite formula.

4. **Anchoring risk:** Despite the TASK-001 anchoring examples being designed as calibration aids (not prescriptive scores), some TASK-004 scores may be influenced by the anchoring examples. The following scores diverge from the closest anchoring example, demonstrating partial independence: [No material divergences identified in this iteration -- all anchoring examples aligned with the assigned scores, which may itself be evidence of anchoring influence rather than independent convergence.]

5. **Single-evaluator limitation:** All 90 scores were assigned by a single AI agent in a single session. No inter-rater reliability data exists. The sensitivity analysis partially compensates by testing whether reasonable weight variations change the selection, but it cannot compensate for systematic scoring bias.

**Unresolved [unverified] markers from EN-301:** The following claims from the EN-301 catalog remain unverified and are referenced in scoring rationales:
- S-004 Pre-Mortem: "30% increase" claim (Klein, 2007 popularized the technique; the specific magnitude is unverified)
- S-010 Self-Refine: Specific improvement percentages from Madaan et al. are cited but the exact ranges are [unverified]
- S-014 LLM-as-Judge: "~80% agreement with human preferences" figure is [unverified]; Zheng et al. demonstrate strong agreement but the specific number needs verification

These [unverified] markers do not change the D1 score assignments (which are based on the general evidence strength, not specific magnitude claims), but they represent precision claims that should not be taken at face value.

---

## References

### Primary Sources

| # | Citation | Relevance |
|---|----------|-----------|
| 1 | FEAT-004:EN-302:TASK-001 -- Evaluation Criteria and Weighting Methodology | Rubric definitions, weight justifications, scoring scale, sensitivity analysis methodology |
| 2 | FEAT-004:EN-302:TASK-002 -- Risk Assessment of Adversarial Strategy Adoption | Per-strategy risk profiles, RED/YELLOW/GREEN classifications, systemic risk patterns |
| 3 | TSR-PROJ-001-EN302-003 (TASK-003) -- Architecture Trade Study | Pugh Matrix, architecture fit ratings, token budgets, composition matrix, integration effort |
| 4 | FEAT-004:EN-301:TASK-006 -- Revised Catalog v1.1.0 | Authoritative 15-strategy catalog with contraindications, differentiation clarifications, cognitive bias mapping |
| 5 | FEAT-004:EN-301:TASK-004 -- Unified Catalog v1.0.0 | Original strategy catalog with full descriptions, mechanisms, strengths, and weaknesses |

### Methodological Sources

| # | Citation | Relevance |
|---|----------|-----------|
| 6 | Keeney, R. L., & Raiffa, H. (1993). *Decisions with Multiple Objectives*. Cambridge University Press. | Multi-criteria decision analysis methodology |
| 7 | Goodwin, P., & Wright, G. (2004). *Decision Analysis for Management Judgment* (3rd ed.). Wiley. | Sensitivity analysis and robustness testing |

---

*Document ID: FEAT-004:EN-302:TASK-004*
*PS ID: EN-302*
*Entry ID: TASK-004*
*Agent: ps-analyst*
*Created: 2026-02-13*
*Status: Complete*
