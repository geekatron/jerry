# TASK-001: Evaluation Criteria and Weighting Methodology for Adversarial Strategy Selection

<!--
DOCUMENT-ID: FEAT-004:EN-302:TASK-001
AUTHOR: ps-analyst agent
DATE: 2026-02-13
STATUS: Complete
PARENT: EN-302 (Strategy Selection & Decision Framework)
FEATURE: FEAT-004 (Adversarial Strategy Research & Skill Enhancement)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
PS-ID: EN-302
ENTRY-ID: TASK-001
INPUT: TASK-006 revised catalog (EN-301), TASK-004 unified catalog (EN-301)
-->

> **Version:** 1.1.0
> **Agent:** ps-analyst
> **Quality Target:** >= 0.92
> **Input Artifacts:** EN-301 TASK-006 (revised catalog, v1.1.0), EN-301 TASK-004 (unified catalog, v1.0.0)
> **Purpose:** Define evaluation dimensions, weighting methodology, and scoring rubric for selecting the best 10 adversarial strategies from the 15-strategy catalog

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | Overview of the evaluation framework and its role in the selection pipeline |
| [Evaluation Dimensions](#evaluation-dimensions) | Definition of 6 weighted criteria with rationale |
| [Weighting Methodology](#weighting-methodology) | Percentage weights, justification, and sensitivity analysis guidance |
| [Scoring Scale and Rubric](#scoring-scale-and-rubric) | 1-5 scoring scale with per-criterion descriptors and anchoring examples |
| [Jerry-Specific Considerations](#jerry-specific-considerations) | How P-003, context rot, 3-iteration loops, and portability are factored in |
| [Composite Score Calculation](#composite-score-calculation) | Formula, normalization, and tie-breaking procedure |
| [Sensitivity Analysis Guidance](#sensitivity-analysis-guidance) | How to test robustness of selections to weight shifts |
| [Framework Validation](#framework-validation) | How this framework itself should be validated |
| [References](#references) | Sources and citations |

---

## Executive Summary

This document defines the evaluation framework used to score all 15 adversarial strategies from the EN-301 catalog and select the best 10 for integration into Jerry. The framework consists of six evaluation dimensions, each with a defined weight, a 1-5 scoring rubric with per-criterion descriptors, and anchoring examples tied to specific strategies from the catalog for calibration purposes.

The framework is designed around three principles:

1. **Transparency**: Every weight and score has a documented rationale. No subjective "gut feel" decisions are hidden behind composite numbers.
2. **Reproducibility**: A different evaluator applying the same rubric to the same strategy catalog should produce scores within +/- 0.5 points of the original evaluation.
3. **Sensitivity-aware**: The weighting is designed so that the selection of the top 10 is robust to +/- 10% weight shifts in any single criterion. Strategies near the cutoff boundary are explicitly identified for closer scrutiny.

The six evaluation dimensions are:

| # | Dimension | Weight | Rationale Summary |
|---|-----------|--------|-------------------|
| D1 | Effectiveness | 25% | Empirical evidence of quality improvement is the primary purpose |
| D2 | LLM Applicability | 25% | Strategies must translate well to LLM-based agent review |
| D3 | Complementarity | 15% | Redundancy wastes context budget; diversity maximizes coverage |
| D4 | Implementation Complexity | 15% | Feasibility within Jerry's current architecture |
| D5 | Cognitive Load | 10% | User comprehension required when strategies are invoked |
| D6 | Differentiation | 10% | Uniqueness justifies the strategy's slot in the final 10 |

These weights reflect Jerry's operational priorities: quality outcomes and LLM fitness are paramount (50% combined), practical concerns of integration and portfolio diversity are important (30% combined), and user experience and uniqueness are secondary but non-negligible (20% combined).

---

## Evaluation Dimensions

### D1: Effectiveness (Weight: 25%)

**Definition:** The degree to which the strategy has demonstrated, through empirical evidence or established practice, measurable improvement in artifact quality, defect detection, or decision-making outcomes.

**What this measures:**
- Strength of empirical evidence (peer-reviewed studies, replicated results, industry adoption at scale)
- Breadth of evidence (validated across multiple domains, tasks, or contexts)
- Magnitude of observed improvement (effect size, not just statistical significance)
- Maturity of the technique (years of application, standardization)

**Why 25%:** Jerry's quality gates require a threshold of >= 0.92. Selecting strategies without strong effectiveness evidence would undermine the credibility of the quality framework. This criterion ensures the foundation is built on strategies with proven track records, not speculative potential. The 25% weight makes effectiveness the joint-highest criterion, reflecting that Jerry's purpose is to improve quality, not merely to review artifacts.

**What this does NOT measure:** Effectiveness in an LLM context specifically (that is D2). A strategy may be highly effective in human teams but poorly suited to LLM agents. Both dimensions are needed.

---

### D2: LLM Applicability (Weight: 25%)

**Definition:** The degree to which the strategy can be effectively implemented and executed by LLM-based agents within the constraints of current LLM capabilities, including prompt engineering, context window limitations, and single-model architectures.

**What this measures:**
- Naturalness of LLM implementation (does the strategy align with what LLMs do well: generation, classification, structured reasoning?)
- Empirical validation in LLM contexts specifically (tested with LLM agents, not only human teams)
- Robustness to single-model architecture (does the strategy degrade when creator and critic are the same model?)
- Context window fit (can the strategy be executed within typical context budgets without triggering context rot?)
- Prompt engineering tractability (can the strategy be reliably elicited through well-structured prompts?)

**Why 25%:** Jerry is an LLM-agent framework. A strategy that works brilliantly with human teams but cannot be effectively implemented by LLM agents has zero operational value in Jerry. This criterion is weighted equally with effectiveness because it acts as a hard feasibility filter: strategies scoring 1 on D2 should be eliminated regardless of their effectiveness score. The joint-highest weight reflects the fundamental constraint that all strategies must work in an LLM context.

**D2 Floor Rule (Qualifying Gate):** D2 functions as both a weighted dimension and a qualifying gate. Any strategy scoring D2 <= 1 is automatically excluded from the selection regardless of its composite score. This floor rule prevents the mathematical possibility of a fundamentally LLM-incompatible strategy achieving a marginal composite score through high scores on other dimensions. In the current 15-strategy catalog, no strategy scores D2=1, so this rule does not affect the current selection. However, it ensures framework integrity if the catalog is extended in the future. The floor rule is applied as Step 0 in the Selection Procedure (before composite calculation), making D2's gate-like character explicit rather than relying solely on the weighted formula.

**What this does NOT measure:** Implementation effort (that is D4). A strategy may be highly applicable to LLMs in principle but require significant engineering to integrate into Jerry's specific architecture.

---

### D3: Complementarity (Weight: 15%)

**Definition:** The degree to which the strategy contributes unique coverage to the overall strategy portfolio, addressing failure modes, cognitive biases, or review dimensions not covered by other strategies in the catalog.

**What this measures:**
- Unique failure mode coverage (does the strategy catch defect types that other strategies miss?)
- Unique cognitive bias mitigation (does it address biases not addressed by other strategies? -- reference Appendix B of TASK-006)
- Mechanistic family diversity (does inclusion increase the representation across the four mechanistic families: Role-Based, Structured Decomposition, Dialectical Synthesis, Iterative Self-Correction?)
- Architectural layer diversity (does inclusion ensure coverage across all five layers of the composition model: L0-L4?)
- Non-redundancy with other high-scoring strategies (if two strategies provide similar coverage, the second one's complementarity score decreases)

**Why 15%:** The goal is to select 10 from 15 -- a 67% retention rate. With such high retention, complementarity is less decisive than in, say, a 5-from-30 selection. However, it remains important because Jerry's context budget is finite. Including two strategies that catch the same defects wastes context window space that could be allocated to a strategy covering a different failure mode. The 15% weight reflects that complementarity is a portfolio-level concern that matters but is subordinate to the individual-strategy quality criteria (D1, D2).

**Evaluation note:** Complementarity is inherently relative -- a strategy's complementarity score depends on which other strategies are selected. For the initial scoring pass, complementarity is evaluated against the full 15-strategy catalog. After the initial top-10 cut, a complementarity re-check is performed to ensure the selected set provides adequate coverage across all four mechanistic families, all five composition layers, and the cognitive bias map from TASK-006 Appendix B.

**Known Limitation -- Sequential Scoring Approximation (F-002):** Scoring D3 against the full 15-strategy catalog and then selecting the top 10 is a methodological approximation. Ideally, D3 would be scored against the evolving selection set, but this creates a circular dependency (the selection depends on D3 scores, which depend on the selection). The sequential approach (score against full catalog -> select top 10 -> re-check complementarity) is adopted as a pragmatic resolution. The post-hoc complementarity re-check in TASK-004 serves as validation: if the re-check reveals that the selected 10 have adequate coverage and no critical complementarity gaps require a swap, then the approximation is valid post-hoc. In the actual TASK-004 evaluation, the re-check confirmed portfolio adequacy without requiring any score revisions or swaps, validating the sequential approach for this catalog. If future catalog extensions significantly change the portfolio composition, D3 should be re-scored for the selected subset.

---

### D4: Implementation Complexity (Weight: 15%)

**Definition:** The degree of engineering effort, architectural modification, and ongoing maintenance required to integrate the strategy into Jerry's agent architecture, skill system, and orchestration framework.

**What this measures:**
- Agent count required (1-agent strategies are simpler than 3+ agent strategies)
- Number of agent passes (cost per invocation: 1 pass vs. 6+ passes)
- Orchestration complexity (does the strategy require sync barriers, debate management, or multi-round coordination?)
- Template and prompt engineering effort (can the strategy be implemented with a well-structured prompt, or does it require new infrastructure?)
- Integration with existing Jerry components (does it leverage existing `.claude/rules/` files, existing skills, or existing agent roles?)
- Maintenance burden (does the strategy require ongoing calibration, rubric updates, or threshold tuning?)

**Why 15%:** Jerry is an operational framework, not a research prototype. Strategies that require extensive engineering to implement will delay the quality framework's deployment and increase maintenance costs. However, implementation complexity is weighted below effectiveness and LLM applicability because a highly effective, highly applicable strategy is worth extra implementation effort. The 15% weight ensures complexity is a meaningful tiebreaker between similarly effective strategies but does not cause the framework to prefer mediocre-but-easy strategies over excellent-but-harder ones.

**Scoring direction:** This criterion is scored INVERSELY -- a score of 5 means LOW complexity (easy to implement), and a score of 1 means HIGH complexity (hard to implement). This ensures that all dimension scores use the same polarity (higher = better).

---

### D5: Cognitive Load (Weight: 10%)

**Definition:** The degree of conceptual overhead imposed on Jerry users when a strategy is invoked, its outputs are presented, and its results need to be interpreted or acted upon.

**What this measures:**
- Conceptual simplicity (can a user understand what the strategy does from a one-sentence description?)
- Output interpretability (are the strategy's outputs self-explanatory, or do they require specialized knowledge to interpret?)
- Actionability of findings (does the strategy produce clear, actionable feedback, or does it require translation?)
- Familiarity (is the strategy a well-known technique that most engineers would recognize?)
- Volume of output (does the strategy produce focused, concise findings, or does it generate voluminous output that requires triage?)

**Why 10%:** Jerry's primary users are developers and engineers using Claude Code. While they are technically sophisticated, they should not need to understand the theoretical basis of every adversarial strategy to benefit from it. However, cognitive load is weighted lower than effectiveness and applicability because Jerry's skill system abstracts most of the strategy mechanics from the user -- the user invokes `/problem-solving` or the quality gate, not "S-003 Steelman Technique" directly. The abstraction layer reduces the user-facing cognitive burden, making this criterion less decisive. The 10% weight reflects its role as a meaningful but secondary concern.

---

### D6: Differentiation (Weight: 10%)

**Definition:** The degree to which the strategy is mechanistically unique from all other strategies in the catalog, offering a genuinely distinct adversarial mechanism rather than a variation on another strategy's approach.

**What this measures:**
- Mechanism uniqueness (does the strategy use a fundamentally different adversarial mechanism than all other strategies?)
- Output type uniqueness (does the strategy produce a distinctive type of output? -- reference the Redundancy Check table from TASK-004)
- Agent pattern uniqueness (does the strategy require a distinctive agent configuration?)
- Non-subsumption (is the strategy's mechanism NOT a subset of another strategy's mechanism?)
- Replaceability (if removed, would its function be entirely covered by the remaining strategies?)

**Why 10%:** Differentiation is partially captured by D3 (Complementarity), which measures portfolio-level coverage. D6 adds a strategy-level uniqueness check: even if a strategy scores well on complementarity because it covers a needed bias or failure mode, it should still be mechanistically distinct from other selected strategies. The 10% weight reflects that differentiation is a guard against subtle redundancy not fully captured by complementarity analysis. It is weighted lowest because the TASK-004 Redundancy Check already verified that all 15 strategies have unique mechanism x agent pattern x output type combinations -- differentiation is therefore unlikely to be a decisive factor for most strategies.

---

## Weighting Methodology

### Weight Assignment Summary

| Dimension | Code | Weight | Category |
|-----------|------|--------|----------|
| Effectiveness | D1 | 25% | Quality Outcome |
| LLM Applicability | D2 | 25% | Quality Outcome |
| Complementarity | D3 | 15% | Portfolio Fitness |
| Implementation Complexity | D4 | 15% | Portfolio Fitness |
| Cognitive Load | D5 | 10% | User Experience |
| Differentiation | D6 | 10% | User Experience |
| **Total** | | **100%** | |

### Weight Justification by Jerry Priority

The weights are justified by mapping each dimension to Jerry's operational priorities:

**Priority 1: Quality gates >= 0.92 (drives D1 + D2 = 50%)**

Jerry's quality framework requires artifacts to pass a 0.92 threshold. This threshold is only meaningful if the adversarial strategies producing the scores are themselves effective (D1) and work reliably in LLM contexts (D2). A strategy that is theoretically brilliant but produces unreliable results in LLM agents would undermine the entire quality gate system. Allocating 50% of the total weight to these two dimensions ensures that the selected strategies are, first and foremost, strategies that actually work in Jerry's execution environment.

**Priority 2: Creator-critic-revision cycles (drives D3 + D4 = 30%)**

Jerry's review architecture uses creator-critic-revision cycles with a 3-iteration cap. This imposes two constraints: (a) the strategy portfolio must provide comprehensive coverage within a limited number of cycles (D3: complementarity ensures no redundant strategies waste cycles), and (b) each strategy must be implementable within the 1-agent-or-2-agent patterns that the cycle supports (D4: complexity ensures strategies fit the architecture). The 30% allocation ensures that practical fit within Jerry's operational model is a significant selection factor.

**Priority 3: Multi-agent orchestration usability (drives D5 + D6 = 20%)**

Jerry's orchestration skill coordinates multi-agent workflows. Users interact with strategies indirectly through quality gate invocations and review workflows. While the skill system abstracts most strategy mechanics, users still see strategy outputs (quality scores, critique findings, recommendations) and must understand and act on them. D5 ensures outputs are interpretable, and D6 ensures each strategy in the final 10 earns its place through genuine uniqueness. The 20% allocation reflects that user experience is important but secondary to quality outcomes and architectural fitness.

### Weight Validation Checks

The following cross-checks validate the weight assignment:

1. **No single dimension is decisive:** The maximum weight is 25%. Even a perfect score (5) on the highest-weighted dimension contributes only 1.25 to the composite score (out of 5.0 maximum). No strategy can be selected on the strength of a single dimension alone.

2. **Quality outcome dimensions dominate:** D1 + D2 = 50%. A strategy must score well on at least one quality outcome dimension to be competitive. This prevents selection of strategies that are easy to implement but ineffective.

3. **Portfolio dimensions are meaningful tiebreakers:** D3 + D4 = 30%. For strategies that are similarly effective and applicable, portfolio fit determines the selection. This prevents selecting two highly effective strategies that do the same thing.

4. **User experience dimensions prevent pathological selections:** D5 + D6 = 20%. Even if a strategy scores well on all other dimensions, extreme cognitive load or pure redundancy can bring its composite score below the cutoff.

5. **Sum is exactly 100%:** 25 + 25 + 15 + 15 + 10 + 10 = 100%.

---

## Scoring Scale and Rubric

### Scale Definition

All dimensions use a 1-5 integer scale:

| Score | Label | General Meaning |
|-------|-------|-----------------|
| 5 | **Exceptional** | Best possible performance on this dimension; no meaningful improvement possible |
| 4 | **Strong** | Clear strength on this dimension with minor limitations |
| 3 | **Adequate** | Acceptable performance; neither a strength nor a weakness |
| 2 | **Limited** | Notable weaknesses on this dimension that create risk |
| 1 | **Poor** | Fundamental problems on this dimension; significant barrier to selection |

### D1: Effectiveness Rubric

| Score | Descriptor | Evidence Standard |
|-------|------------|-------------------|
| 5 | Multiple peer-reviewed empirical studies demonstrating consistent quality improvement; replicated across domains; standardized by industry or government bodies; decades of proven practice | Peer-reviewed publications with replication; industry standards (ISO, MIL-STD, IEC); government adoption |
| 4 | At least one peer-reviewed empirical study with positive results; broad adoption in practice; strong theoretical foundation with empirical support | Published empirical results (e.g., arXiv with conference acceptance); widespread adoption |
| 3 | Theoretical basis is sound and well-cited; limited empirical validation but consistent positive anecdotal evidence; moderate adoption | Well-cited theoretical papers; limited or indirect empirical evidence; adopted by recognizable organizations |
| 2 | Theoretical basis exists but is disputed or narrow; minimal empirical evidence; limited adoption | Theoretical papers without empirical validation; anecdotal evidence only |
| 1 | No empirical evidence; purely speculative; novel and untested; no adoption history | No published evidence; no known adoption |

**Anchoring Examples:**

| Strategy | Expected D1 Score | Rationale |
|----------|-------------------|-----------|
| S-012 FMEA | 5 | 70+ years of standardized practice across aerospace, automotive, medical devices. MIL-STD-1629A, IEC 60812. Government and industry standard. |
| S-002 Devil's Advocate | 5 | CIA-formalized structured analytic technique (Heuer & Pherson, 2014). Decades of intelligence community use. Multiple empirical studies including Schweiger et al. (1986). |
| S-010 Self-Refine | 4 | Peer-reviewed at NeurIPS 2023 (Madaan et al., 2023). Demonstrated improvement across multiple tasks. Single study, but conference-accepted with empirical results. |
| S-015 PAE | 2 | Novel composite with no direct empirical validation. Component strategies are individually validated, but the graduated composition is untested. Provisional status acknowledged in TASK-006. |

---

### D2: LLM Applicability Rubric

| Score | Descriptor | LLM Fitness Standard |
|-------|------------|----------------------|
| 5 | Designed specifically for LLM agents; empirically validated in LLM contexts; naturally aligns with LLM capabilities (generation, classification, structured reasoning); works with single-model architecture; fits within standard context windows | LLM-native design with published LLM benchmarks |
| 4 | Highly compatible with LLM implementation; can be reliably elicited through prompt engineering; works with single-model architecture with minor limitations; moderate context footprint | Strong LLM fit with demonstrated prompt-based implementation |
| 3 | Compatible with LLM implementation but requires careful prompt engineering; some aspects degrade in single-model context; moderate-to-large context footprint | Feasible LLM implementation with known limitations |
| 2 | Partially compatible; significant aspects rely on capabilities LLMs lack (genuine domain expertise, physical simulation, persistent memory across sessions); requires workarounds | Limited LLM compatibility requiring significant adaptation |
| 1 | Fundamentally incompatible with LLM agent execution; requires human judgment, physical interaction, real-time collaboration, or capabilities beyond current LLMs | Incompatible with LLM implementation |

**Anchoring Examples:**

| Strategy | Expected D2 Score | Rationale |
|----------|-------------------|-----------|
| S-010 Self-Refine | 5 | Designed for LLMs. Published LLM benchmarks (Madaan et al., 2023). Single-agent, single-model. Minimal context footprint. Naturally aligns with LLM generation-feedback-refine capability. |
| S-007 Constitutional AI Critique | 5 | Designed for LLMs (Bai et al., 2022, Anthropic). Jerry already has constitutions (`.claude/rules/`). Principle-by-principle evaluation is natural for LLMs. |
| S-004 Pre-Mortem | 4 | Not LLM-native, but temporal reframing ("it has failed") maps naturally to LLM prompting. The "narrator persona" is easily elicited. Minor limitation: LLMs lack genuine domain experience for identifying non-obvious failure modes. |
| S-006 ACH | 3 | Matrix construction is feasible for LLMs, but the quality of hypothesis generation depends on domain knowledge. Evidence assessment (C/I/N/A) involves subjective judgment that LLMs may not calibrate well. |

---

### D3: Complementarity Rubric

| Score | Descriptor | Portfolio Contribution Standard |
|-------|------------|-------------------------------|
| 5 | Addresses failure modes or cognitive biases that NO other strategy in the catalog targets; represents an otherwise-uncovered mechanistic family; fills a gap in the L0-L4 composition model that no other strategy can fill | Unique and irreplaceable portfolio contribution |
| 4 | Addresses failure modes or biases that at most one other strategy partially covers; strong contribution to mechanistic family diversity or composition layer coverage | Highly valuable portfolio contribution with minimal overlap |
| 3 | Some overlap with 1-2 other strategies but provides distinct coverage in at least one significant area (different bias, different failure mode class, or different composition layer) | Meaningful portfolio contribution with moderate overlap |
| 2 | Substantial overlap with 2+ other strategies; its coverage is mostly subsumed by others; provides only marginal incremental coverage | Limited incremental contribution; mostly redundant |
| 1 | Fully subsumed by another strategy or combination of strategies; removal would not create any coverage gap | No unique contribution; fully redundant |

**Anchoring Examples:**

| Strategy | Expected D3 Score | Rationale |
|----------|-------------------|-----------|
| S-011 CoVe | 5 | Only strategy targeting factual accuracy and hallucination specifically. No other strategy provides independent factual verification. Removing it creates an unaddressed failure mode class. |
| S-013 Inversion | 4 | Unique "generative" strategy -- produces checklists for other strategies to consume. Complements all other strategies rather than duplicating any. Minor overlap with FMEA's failure enumeration, but mechanism is distinct (problem reversal vs. bottom-up enumeration). |
| S-002 Devil's Advocate | 3 | Core adversarial strategy, but overlaps with Red Team (S-001) in providing oppositional critique. DA challenges conclusions; RT simulates adversaries. Distinct but related mechanisms. Both address confirmation bias. |
| S-010 Self-Refine | 2 | Self-critique mechanism partially overlapped by Constitutional AI Critique (S-007), which also involves self-review. Self-Refine is simpler but less structured. Its unique contribution is the low-cost pre-critic self-check role. |

---

### D4: Implementation Complexity Rubric (INVERSE: 5 = easy, 1 = hard)

| Score | Descriptor | Complexity Standard |
|-------|------------|---------------------|
| 5 | Single agent, 1 pass; implementable with a single well-structured prompt; leverages existing Jerry infrastructure directly; no orchestration required; minimal maintenance | Trivial integration effort |
| 4 | 1-2 agents, 2 passes; standard prompt engineering; minor template creation; uses existing agent roles; simple orchestration (sequential) | Low integration effort |
| 3 | 2 agents, 2-3 passes; moderate prompt engineering; new templates needed; may require new agent mode configuration; standard orchestration with sync barriers | Moderate integration effort |
| 2 | 2-3 agents, 3-4 passes; significant prompt engineering; new infrastructure components needed (e.g., matrix templates, debate management); complex orchestration | High integration effort |
| 1 | 3+ agents, 4+ passes; requires new architectural components; multi-round management with state tracking; extensive calibration and maintenance; orchestration infrastructure changes | Very high integration effort |

**Anchoring Examples:**

| Strategy | Expected D4 Score | Rationale |
|----------|-------------------|-----------|
| S-010 Self-Refine | 5 | Single agent, 1 additional pass. A prompt suffix is the entire implementation. No orchestration, no templates, no new infrastructure. |
| S-003 Steelman | 5 | Adds one prompt phase to existing critic invocation ("first, steelman the argument"). Minimal overhead. No new agents or infrastructure. |
| S-007 Constitutional AI Critique | 4 | 1-2 agents, 2-4 passes. Jerry already has constitutions -- the strategy leverages existing `.claude/rules/` files. Templates needed for principle-by-principle evaluation format. |
| S-009 Multi-Agent Debate | 1 | 3+ agents, 4-6+ passes. Requires debate round management, sync barriers, convergence detection or judge agent, and response sharing infrastructure. Most complex strategy in the catalog. |

---

### D5: Cognitive Load Rubric

| Score | Descriptor | User Comprehension Standard |
|-------|------------|----------------------------|
| 5 | Strategy is intuitively understood from its name; outputs are self-explanatory; findings are immediately actionable without translation; most engineers would recognize the technique | Minimal cognitive overhead |
| 4 | Strategy concept is easily explained in one sentence; outputs require minimal interpretation; findings include clear action items; technique is moderately well-known | Low cognitive overhead |
| 3 | Strategy requires a brief explanation for most users; outputs require some interpretation; findings may need translation to actionable items; technique is recognized by domain specialists | Moderate cognitive overhead |
| 2 | Strategy requires background knowledge to understand; outputs require significant interpretation; findings need substantial translation to be actionable; technique is specialized | High cognitive overhead |
| 1 | Strategy requires expert knowledge to understand; outputs are opaque without training; findings require specialist interpretation; technique is obscure or requires formal training | Very high cognitive overhead |

**Anchoring Examples:**

| Strategy | Expected D5 Score | Rationale |
|----------|-------------------|-----------|
| S-002 Devil's Advocate | 5 | Universally understood concept. "Here is why you might be wrong." Findings are direct critiques -- no translation needed. Every engineer has encountered this. |
| S-014 LLM-as-Judge | 4 | Concept is simple ("give it a score with reasons"). Output is a number + explanation. Requires understanding what the rubric dimensions mean, but the score itself is self-explanatory. |
| S-006 ACH | 2 | Requires understanding of hypothesis matrices, diagnosticity, and the "least rejected" (not "most confirmed") paradigm. The matrix output requires interpretation to extract actionable conclusions. Specialized intelligence analysis technique. |
| S-015 PAE | 2 | Meta-strategy with 5 escalation levels, gate criteria, and strategy composition. Understanding why the system chose a particular level requires knowledge of the full strategy catalog. Output spans multiple strategies, each with its own interpretation requirements. |

---

### D6: Differentiation Rubric

| Score | Descriptor | Uniqueness Standard |
|-------|------------|---------------------|
| 5 | No other strategy in the catalog uses a similar mechanism, produces a similar output type, or serves a similar function. Removal would leave a unique-in-kind gap. | Wholly unique -- no substitute exists |
| 4 | Mechanism is distinct from all others, though one strategy may share a superficial resemblance. Differentiation is clear at the mechanism level. | Clearly distinct -- resemblance is superficial |
| 3 | Mechanism is distinct but belongs to the same mechanistic family as 1-2 other strategies. Differentiation is real but requires explanation. | Distinct within family -- requires explanation |
| 2 | Mechanism has significant overlap with another strategy; differentiation exists but is subtle and debatable. The TASK-006 differentiation clarifications were needed to justify inclusion. | Subtle distinction -- debatable uniqueness |
| 1 | Mechanism is essentially a variant or subset of another strategy. Could be implemented as a configuration option of another strategy rather than a standalone entry. | Minimal distinction -- variant of another |

**Anchoring Examples:**

| Strategy | Expected D6 Score | Rationale |
|----------|-------------------|-----------|
| S-011 CoVe | 5 | Only factual verification strategy. No other strategy uses independent, context-isolated verification of claims. Wholly unique mechanism. |
| S-004 Pre-Mortem | 5 | Only strategy using temporal reframing ("it has failed"). No other strategy uses prospective hindsight as its primary mechanism. |
| S-003 Steelman | 3 | Belongs to the Dialectical Synthesis family. TASK-006 differentiation clarifications were needed to distinguish it from Self-Refine (S-010). The distinction (charitable reconstruction vs. self-improvement) is real but required explicit mechanism-level analysis. |
| S-008 Socratic Method | 3 | TASK-006 differentiation clarifications were needed to distinguish from Devil's Advocate (S-002). The distinction (questions vs. assertions) is operationally significant but both deliver verbal adversarial challenge. |

---

## Anchoring Risk Acknowledgment

**Anchoring examples** are provided in each rubric dimension to calibrate scorers. These examples represent expected scores based on the rubric descriptor analysis, but they are **calibration aids, not prescriptive scores**. The TASK-004 evaluator should treat them as baselines and independently evaluate each strategy against the rubric descriptors. Where the TASK-004 scorer assigns a score that diverges from an anchoring example, the divergence should be noted and explained, demonstrating independent evaluation.

**Circularity risk:** Because the same analytical team (ps-analyst) designed the rubric anchoring examples (TASK-001) and scored the strategies (TASK-004), there is a risk that scores are anchored by the examples rather than independently derived. This risk is mitigated by: (a) the adversarial review process (TASK-006, ps-critic) which independently evaluates the scores, (b) the sensitivity analysis which tests robustness of the selection to score variations, and (c) explicit documentation of divergences in TASK-004 where scores differ from what anchoring examples might suggest.

---

## Jerry-Specific Considerations

### P-003: No Recursive Subagents

**Constraint:** Jerry's constitution (P-003) enforces a hard limit of one level of agent spawning: orchestrator -> worker. Workers MUST NOT invoke sub-workers.

**Impact on Evaluation:**

- **D2 (LLM Applicability):** Strategies requiring hierarchical agent spawning (e.g., a debate agent that spawns sub-agents for research) score lower on D2 because they cannot be implemented as designed. They must be flattened to the orchestrator -> worker pattern.
- **D4 (Implementation Complexity):** Strategies requiring 3+ distinct agent roles (e.g., S-009 Multi-Agent Debate: debater A + debater B + judge) must all be orchestrated by the top-level orchestrator, not by each other. This increases orchestration complexity but does not prohibit the strategy -- it is an implementation constraint, not a mechanism constraint.
- **Specific strategy impacts:**
  - S-009 (Multi-Agent Debate): All debater and judge agents are invoked by the orchestrator. Debaters do not invoke each other. This is compliant but requires careful orchestration design. D4 score penalized accordingly.
  - S-005 (Dialectical Inquiry): Three agents (thesis, antithesis, synthesizer) invoked by orchestrator. Compliant. Moderate D4 impact.
  - S-015 (PAE): Escalation between levels is managed by the orchestrator, not by the strategies themselves. Compliant. Each level invokes its strategy agents directly from the orchestrator.

**Rubric integration:** P-003 compliance is evaluated within D2 and D4. No separate dimension is needed because P-003 is a binary constraint (compliant or not), and all 15 strategies are structurally P-003-compliant per the L2 architecture section of TASK-004. The impact on scoring is through the implementation complexity required to achieve compliance.

---

### Context Window Constraints (Context Rot)

**Constraint:** Jerry's core problem is context rot -- LLM performance degrades as context fills. Strategies that consume large amounts of context window space or generate voluminous intermediate artifacts contribute to context rot.

**Impact on Evaluation:**

- **D2 (LLM Applicability):** Strategies with large context footprints score lower. Specifically:
  - Multi-round strategies that accumulate debate transcripts (S-009) consume more context than single-pass strategies (S-010).
  - Matrix-producing strategies (S-006 ACH, S-012 FMEA) generate structured outputs that consume context space proportional to the number of hypotheses/components evaluated.
  - Multi-pass strategies (S-007 Constitutional AI with 3 critique passes) consume more context than single-pass strategies, but can mitigate this by summarizing previous passes.

- **D5 (Cognitive Load):** Strategies that produce voluminous output (S-012 FMEA tables, S-006 ACH matrices) increase the user's cognitive burden and also risk pushing useful information out of the LLM's effective context window when that output is consumed by downstream agents.

- **Mitigation acknowledgment:** Jerry's architecture mitigates context rot through filesystem persistence (persisting intermediate artifacts to `.jerry/data/` rather than keeping them in context). Strategies that naturally produce persistable, structured outputs (FMEA tables, ACH matrices, rubric scores) are partially shielded from context rot concerns because their outputs can be persisted and selectively loaded. This mitigation is factored into D2 scoring: strategies with naturally persistable outputs receive less D2 penalty for context consumption.

---

### 3-Iteration Adversarial Feedback Loop

**Constraint:** Jerry's creator-critic-revision cycle has a 3-iteration cap. After 3 rounds of critique and revision, the artifact is either accepted, escalated, or abandoned. Strategies must deliver value within this budget.

**Impact on Evaluation:**

- **D2 (LLM Applicability):** Strategies that require more than 3 iterations to converge score lower. Specifically:
  - S-010 (Self-Refine): Explicitly designed with diminishing returns after 2-3 iterations. Well-aligned with the 3-iteration constraint. D2 score benefits.
  - S-009 (Multi-Agent Debate): Typically requires 2-4 debate rounds. At the upper end, this consumes the entire iteration budget. D2 score penalized.
  - S-007 (Constitutional AI Critique): Multi-pass structure (structural -> semantic -> holistic) requires 2-3 passes. Fits within the 3-iteration budget. D2 score neutral.

- **D4 (Implementation Complexity):** Strategies that cannot complete within 3 iterations require either: (a) compression of their mechanism to fit the budget, which may reduce effectiveness, or (b) consuming all 3 iterations for a single strategy, leaving no room for other strategies in the same review cycle. Both increase implementation complexity.

- **Rubric integration:** The 3-iteration constraint is evaluated within D2 (does the strategy converge within 3 iterations?) and D4 (what is the cost of fitting the strategy within the budget?). Strategies scoring high on both D2 and D4 are those that deliver their value in 1-2 iterations, leaving budget for additional strategies or revision.

---

### Cross-Platform Portability (macOS, Windows, Linux)

**Constraint:** Jerry must run on macOS, Windows, and Linux. Strategies must not depend on platform-specific capabilities.

**Impact on Evaluation:**

- **D4 (Implementation Complexity):** This consideration has minimal impact on most strategies because adversarial strategies operate at the prompt and reasoning level, not at the operating system level. The relevant portability concerns are:
  - File path handling for persisted artifacts (Windows backslashes vs. Unix forward slashes) -- this is an infrastructure concern, not a strategy concern
  - External tool invocation for tool-augmented strategies (S-011 CoVe with link checkers, S-007 CRITIC enhancement with linters) -- tools must be cross-platform
  - Shell command execution for any strategy that triggers external validation -- commands must be portable

- **Rubric integration:** Cross-platform portability is a minor factor in D4. Strategies that rely on external tools for their core mechanism (S-011 with tool-augmented verification) receive a small D4 penalty if those tools are not universally available. Pure prompt-based strategies (S-002, S-003, S-004, S-008, S-010, S-013) are fully platform-independent and receive no portability penalty.

---

## Composite Score Calculation

### Formula

The composite score for each strategy is calculated as:

```
Composite Score = (D1 * 0.25) + (D2 * 0.25) + (D3 * 0.15) + (D4 * 0.15) + (D5 * 0.10) + (D6 * 0.10)
```

Where each D_i is an integer from 1 to 5.

**Score Range:** Minimum = 1.00 (all 1s), Maximum = 5.00 (all 5s).

### Interpretation Scale

| Composite Score | Interpretation | Selection Likelihood |
|-----------------|----------------|---------------------|
| 4.00 - 5.00 | Exceptional candidate | Almost certain selection |
| 3.50 - 3.99 | Strong candidate | Likely selection |
| 3.00 - 3.49 | Viable candidate | Selection depends on portfolio fit |
| 2.50 - 2.99 | Marginal candidate | Selection only if portfolio gap requires it |
| 1.00 - 2.49 | Weak candidate | Likely exclusion |

### Selection Procedure

0. **D2 floor gate:** Eliminate any strategy with D2 <= 1 (fundamentally incompatible with LLM execution). These strategies are excluded regardless of their scores on other dimensions.
1. **Initial scoring:** Score all remaining strategies on all 6 dimensions using the rubrics above.
2. **Composite calculation:** Calculate composite scores using the weighted formula.
3. **Rank ordering:** Sort strategies by composite score, descending.
4. **Top-10 cut:** Select the top 10 strategies by composite score.
5. **Boundary analysis:** For strategies ranked 9-12 (near the cutoff), perform sensitivity analysis (see next section) to assess robustness.
6. **Complementarity re-check:** Verify that the selected 10 provide coverage across all four mechanistic families and all five composition layers. If a critical gap exists, consider swapping the lowest-ranked selected strategy for a lower-ranked strategy that fills the gap, with documented justification.
7. **Document:** Record all scores, rationale, and any post-scoring adjustments with full justification.

### Tie-Breaking Rules

When two or more strategies have identical composite scores, apply the following tiebreakers in order:

1. **D1 (Effectiveness):** Higher D1 score wins. Rationale: effectiveness is the most fundamental quality of an adversarial strategy.
2. **D2 (LLM Applicability):** Higher D2 score wins. Rationale: in Jerry's context, LLM fitness is a hard feasibility constraint.
3. **D3 (Complementarity):** Higher D3 score wins. Rationale: portfolio diversity is the next priority.
4. **If still tied:** Both strategies are included if both are within the top 10. If the tie is at the cutoff boundary (rank 10-11), the evaluator provides a qualitative justification for the selection.

---

## Sensitivity Analysis Guidance

### Purpose

Sensitivity analysis determines how robust the top-10 selection is to changes in the weight assignments. A robust selection is one where the same 10 strategies are selected under plausible alternative weightings.

### Methodology

For each dimension D_i, test two scenarios:

1. **Increase D_i weight by 10 percentage points** (e.g., D1 from 25% to 35%), reducing all other dimensions proportionally to maintain a 100% total.
2. **Decrease D_i weight by 10 percentage points** (e.g., D1 from 25% to 15%), increasing all other dimensions proportionally to maintain a 100% total.

This produces 12 alternative weight configurations (6 dimensions x 2 directions).

### Proportional Rebalancing

When adjusting weight for dimension D_i by +/- delta:

```
New weight for D_i = Original weight +/- delta
New weight for D_j (j != i) = Original weight for D_j * (1 - New D_i weight) / (1 - Original D_i weight)
```

**Example:** Increasing D1 from 25% to 35%:
- D2: 25% * (1 - 0.35) / (1 - 0.25) = 25% * 0.867 = 21.7%
- D3: 15% * 0.867 = 13.0%
- D4: 15% * 0.867 = 13.0%
- D5: 10% * 0.867 = 8.7%
- D6: 10% * 0.867 = 8.7%
- Total: 35.0 + 21.7 + 13.0 + 13.0 + 8.7 + 8.7 = 100.1% (rounding, adjust to 100%)

### Analysis Procedure

1. For each of the 12 alternative weight configurations, recalculate all 15 composite scores.
2. Re-rank strategies.
3. Identify which strategies change position relative to the top-10 cutoff.
4. Report:
   - **Stable selections:** Strategies that remain in the top 10 under all 12 configurations. These are confidently selected.
   - **Stable exclusions:** Strategies that remain outside the top 10 under all 12 configurations. These are confidently excluded.
   - **Sensitive strategies:** Strategies that cross the cutoff boundary under one or more configurations. These require qualitative justification for their final inclusion/exclusion decision.

### Robustness Threshold

The selection is considered **robust** if:
- At least 8 of the 10 selected strategies are stable (remain selected under all 12 configurations)
- At most 2 strategies are sensitive (cross the boundary under some configurations)
- No strategy crosses the boundary under more than 4 of the 12 configurations

If the robustness threshold is not met, the evaluator should:
1. Review whether the weight assignments adequately reflect Jerry's priorities
2. Consider whether the sensitive strategies require qualitative override (documented justification for inclusion/exclusion regardless of weight sensitivity)
3. Document the sensitivity findings in the final ADR (TASK-005)

---

## Framework Validation

This evaluation framework is itself subject to quality validation. The following checks should be performed before applying the framework to the 15 strategies:

### Internal Consistency Checks

| Check | Expected Result | Status |
|-------|-----------------|--------|
| Weights sum to 100% | 25 + 25 + 15 + 15 + 10 + 10 = 100 | PASS |
| All dimensions have rubrics | 6 dimensions, 6 rubrics defined | PASS |
| All rubric levels have descriptors | 5 levels per rubric, all described | PASS |
| All dimensions have anchoring examples | At least 3 anchoring examples per dimension | PASS |
| Scoring scale is consistent across dimensions | All use 1-5, higher = better (D4 is inverse-scored) | PASS |
| Jerry-specific constraints are addressed | P-003, context rot, 3-iteration, portability documented | PASS |
| Tie-breaking procedure is deterministic | 3-level tiebreaker + qualitative fallback defined | PASS |
| Sensitivity analysis methodology is specified | 12 alternative configurations, proportional rebalancing | PASS |

### External Validation

- **TASK-006 adversarial review (ps-critic):** This document will be reviewed by ps-critic for internal consistency, blind spots, and potential gaming vectors.
- **TASK-004 scoring (ps-analyst):** This framework will be applied by ps-analyst to score all 15 strategies. Any rubric ambiguities discovered during scoring will be documented and resolved.
- **Cross-reference with TASK-002 (risk assessment) and TASK-003 (architecture trade study):** The evaluation framework should be consistent with the risk and architecture findings from the parallel tasks. Discrepancies will be documented in the ADR (TASK-005).

---

## References

### Primary Sources

| # | Citation | Relevance |
|---|----------|-----------|
| 1 | EN-301 TASK-004: Unified Catalog of 15 Adversarial Review Strategies (v1.0.0) | Full strategy catalog with mechanisms, strengths, weaknesses, and Jerry applicability |
| 2 | EN-301 TASK-006: Revised Catalog (v1.1.0) | Revision addressing adversarial review findings; contraindications, systemic risk, differentiation clarifications |
| 3 | EN-302: Strategy Selection & Decision Framework (enabler document) | Parent enabler defining the selection task, acceptance criteria, and task dependencies |
| 4 | Jerry Constitution (docs/governance/JERRY_CONSTITUTION.md) | P-003 (No Recursive Subagents), P-020 (User Authority), P-022 (No Deception) |

### Methodological Sources

| # | Citation | Relevance |
|---|----------|-----------|
| 5 | Keeney, R. L., & Raiffa, H. (1993). *Decisions with Multiple Objectives: Preferences and Value Trade-offs*. Cambridge University Press. ISBN: 978-0521438834. | Multi-criteria decision analysis (MCDA) methodology underlying the weighted scoring approach |
| 6 | Saaty, T. L. (1980). *The Analytic Hierarchy Process*. McGraw-Hill. ISBN: 978-0070543713. | AHP weight assignment methodology; pairwise comparison as a weight validation technique |
| 7 | Goodwin, P., & Wright, G. (2004). *Decision Analysis for Management Judgment* (3rd ed.). Wiley. ISBN: 978-0470861080. | Sensitivity analysis methodology and robustness testing for multi-criteria decisions |

### Jerry Architecture Sources

| # | Citation | Relevance |
|---|----------|-----------|
| 8 | CLAUDE.md (project root) | Jerry identity, navigation, critical constraints including P-003 |
| 9 | `.claude/rules/architecture-standards.md` | Hexagonal architecture, layer dependencies, composition root pattern |
| 10 | `skills/orchestration/SKILL.md` | Orchestration skill capabilities and constraints relevant to strategy implementation |

---

*Document ID: FEAT-004:EN-302:TASK-001*
*PS ID: EN-302*
*Entry ID: TASK-001*
*Agent: ps-analyst*
*Created: 2026-02-13*
*Status: Complete*
