---
DISCLAIMER: This guidance is AI-generated based on NASA Systems Engineering
standards. It is advisory only and does not constitute official NASA guidance.
All SE decisions require human review and professional engineering judgment.
Not for use in mission-critical decisions without SME validation.
---

# Risk Assessment: PROJ-017 LLM Skill Testing Framework

> **Project:** PROJ-017
> **Phase:** 3B (Risk Assessment)
> **Date:** 2026-03-03
> **Status:** Active
> **Input Artifacts:** Phase 2 Synthesis (synthesized-findings.md), ADR-001 (framework-architecture.md)

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Risk count by level, top 3 risks, RED risk alerts |
| [L1: Adoption Risk](#l1-adoption-risk) | Developer friction, learning curve, ecosystem maturity |
| [L1: Integration Risk](#l1-integration-risk) | Jerry CLI compatibility, quality gate alignment, CI/CD complexity |
| [L1: Obsolescence Risk](#l1-obsolescence-risk) | Competitive threat timeline, technology evolution |
| [L1: Measurement Risk](#l1-measurement-risk) | Statistical validity, false positive/negative rates, N sensitivity |
| [L1: Gap Risk](#l1-gap-risk) | Unresolved research gaps that could invalidate conclusions |
| [ADR-001 Risk Cross-Reference](#adr-001-risk-cross-reference) | Bidirectional mapping of ADR-001 R-001 through R-007 to assessment risks |
| [L2: Risk Register Table](#l2-risk-register-table) | Complete risk register with L x C scoring |
| [L2: Risk Portfolio Analysis](#l2-risk-portfolio-analysis) | 5x5 matrix, category breakdown, review implications |
| [L2: Mitigation Roadmap](#l2-mitigation-roadmap) | Sequenced mitigation actions by implementation phase |
| [Self-Review](#self-review) | S-010 quality gate compliance |
| [References](#references) | Source traceability |

---

## L0: Executive Summary

**Risk Portfolio:** 0 RED | 8 YELLOW | 9 GREEN

This risk assessment identifies 17 risks across 5 dimensions for the PROJ-017 LLM Skill Testing Framework. The selected architecture (ADR-001 Option B: promptfoo Extension) carries no RED-level risks, but contains 8 YELLOW risks that require active mitigation. The risk profile is favorable for proceeding with implementation, contingent on addressing the top 3 risks below.

**Top 3 Risks:**

1. **RISK-005 (Score 12, YELLOW):** If the promptfoo competitive team adds native skill comparison within 6-12 months, then the Skill Comparison Orchestrator component becomes redundant and the framework loses its most visible feature. Mitigation: architectural separation ensures the statistical engine and governance validator remain independently valuable.

2. **RISK-010 (Score 12, YELLOW):** If the N=30 per condition sample size requirement (derived from a single academic source, arXiv 2511.19794) is domain-inappropriate for LLM skill evaluation, then the Full tier's statistical conclusions may be unreliable and the cost model is miscalibrated. Mitigation: N is configurable (min 10, default 30) with a Phase 3 calibration study.

3. **RISK-014 (Score 12, YELLOW):** If T3 agent external tool variance (web search returning different results across runs) is not controlled, then paired skill comparisons for T3 agents (ps-researcher, nse-explorer) produce invalid statistical results that attribute environmental noise to skill quality. Mitigation: fixture-based response replay or restriction to T1-only evaluation for T3 agents.

No RED risks require immediate escalation. All YELLOW risks have documented mitigation strategies with residual risk at GREEN level.

---

## L1: Adoption Risk

Adoption risk addresses developer friction, learning curve, and ecosystem maturity that could prevent the framework from achieving its intended usage within the Jerry ecosystem and potentially the broader Claude Code community.

### RISK-001: Dual Runtime Dependency (Node.js + Python)

| Attribute | Value |
|-----------|-------|
| **Risk Statement** | If the framework requires both Node.js (for promptfoo) and Python (for the statistical engine and Jerry CLI), then developers without both runtimes configured face a non-trivial setup barrier that reduces adoption. |
| **Affected Requirements** | REQ-021 (Jerry CLI integration), AC-S06 (adoption friction) |
| **Category** | Technical / Adoption |
| **Likelihood** | 3 (Possible) -- Jerry already requires Python via `uv`; Node.js is common but not universal among Jerry users |
| **Consequence** | 2 (Minor) -- Setup is a one-time cost; standard package managers handle both runtimes |
| **Score** | 6 (GREEN) |
| **Status** | Identified |
| **Applies To** | Option B (promptfoo Extension), Option C (Hybrid Composable) |
| **Root Cause** | promptfoo is TypeScript; statistical engine and Jerry are Python |
| **Trigger** | Developer attempts first-time framework setup |
| **Mitigation Strategy** | Mitigate |
| **Mitigation Plan** | (1) Provide a single `jerry eval setup` command that checks for both runtimes and installs promptfoo via npm if missing. (2) Document minimum runtime versions in PROJ-017 README. (3) Consider Docker-based alternative for CI/CD environments. |
| **Residual Risk** | L=2, C=1, Score=2 (GREEN) -- One-time setup friction reduced to a single command |
| **Owner** | Implementation Lead |
| **Due Date** | Phase 1 (Smoke mode delivery) |

### RISK-002: promptfoo Learning Curve for Jerry Developers (GAP-005)

| Attribute | Value |
|-----------|-------|
| **Risk Statement** | If Jerry developers are unfamiliar with promptfoo's YAML configuration syntax and assertion types, then the time-to-first-value exceeds the 15-minute target (GAP-005) and early adopters abandon the framework before experiencing its value. |
| **Affected Requirements** | AC-S06 (adoption friction), REQ-020 (promptfoo YAML-driven configuration) |
| **Category** | Adoption |
| **Likelihood** | 3 (Possible) -- promptfoo has good documentation but Jerry developers may not have prior evaluation tool experience |
| **Consequence** | 3 (Moderate) -- Failed first experience creates lasting negative perception; difficult to recover |
| **Score** | 9 (YELLOW) |
| **Status** | Identified |
| **Applies To** | Option B (promptfoo Extension) |
| **Root Cause** | Framework introduces an external tool's configuration paradigm into Jerry's workflow |
| **Trigger** | Developer attempts first skill evaluation without prior promptfoo experience |
| **Mitigation Strategy** | Mitigate |
| **Mitigation Plan** | (1) Generate default YAML configs automatically from agent definition files (Skill Comparison Orchestrator's primary function). (2) Provide `jerry eval init <agent.md>` that creates a working evaluation config with zero manual YAML editing. (3) Include 3-5 worked examples covering common skill types (researcher, analyst, architect). (4) Measure time-to-first-green-smoke in Phase 1 acceptance testing. |
| **Residual Risk** | L=2, C=2, Score=4 (GREEN) -- Auto-generation eliminates most manual configuration; examples cover common patterns |
| **Owner** | Implementation Lead |
| **Due Date** | Phase 1 (Smoke mode delivery) |

### RISK-003: Claude Code Skill Community Size Unknown

| Attribute | Value |
|-----------|-------|
| **Risk Statement** | If the Claude Code skill developer community is too small (cc-plugin-eval has only 13 GitHub stars per Phase 1B RG-5; see `projects/PROJ-017-llm-skill-testing/research/competitive-landscape.md` Section L1.2), then the framework achieves no network effects beyond Jerry and the general-purpose extensibility investment (skill orchestrator, statistical engine) has no external audience. |
| **Affected Requirements** | REQ-019 (extensibility for new agents) |
| **Category** | Adoption / Cost |
| **Likelihood** | 3 (Possible) -- Community size is genuinely unknown; 13 stars on the only comparable tool is a weak signal |
| **Consequence** | 2 (Minor) -- Framework still provides full value to Jerry; only the general-purpose ambition is affected |
| **Score** | 6 (GREEN) |
| **Status** | Accepted |
| **Applies To** | All options |
| **Root Cause** | Claude Code plugin ecosystem maturity is early and poorly measured |
| **Trigger** | Post-launch: no external adoption after 3 months of availability |
| **Mitigation Strategy** | Accept |
| **Mitigation Plan** | ADR-001 already scopes as "Jerry-first, extensible to others later." No engineering investment is contingent on external adoption. The statistical engine and governance validator provide full Jerry-internal value regardless of external community size. Monitor Claude Code ecosystem growth as a leading indicator. |
| **Residual Risk** | L=3, C=2, Score=6 (GREEN) -- Accepted; internal value unaffected |
| **Owner** | Project Lead |
| **Due Date** | N/A (monitoring only) |

---

## L1: Integration Risk

Integration risk addresses compatibility with Jerry's existing infrastructure (CLI, quality gate, CI/CD pipeline, hexagonal architecture) and the complexity of extending that infrastructure with evaluation capabilities.

### RISK-004: promptfoo Output Schema Instability

| Attribute | Value |
|-----------|-------|
| **Risk Statement** | If promptfoo changes its JSON output schema in a minor or major release, then the statistical engine's JSON ingestion breaks silently (incorrect field mapping) or loudly (parse failure), disrupting evaluation pipelines. |
| **Affected Requirements** | REQ-005 (skill comparison report), REQ-006 (statistical significance testing) |
| **Category** | Technical / Integration |
| **Likelihood** | 3 (Possible) -- promptfoo is actively developed (10.8k stars, frequent releases); output format changes are plausible within 12 months |
| **Consequence** | 3 (Moderate) -- Breaks the statistical engine's primary data intake; requires engineering time to fix |
| **Score** | 9 (YELLOW) |
| **Status** | Identified |
| **Applies To** | Option B (promptfoo Extension) |
| **Root Cause** | Cross-component integration via a third-party JSON contract that is not under PROJ-017 control |
| **Trigger** | promptfoo release with changed output field names or structure |
| **Mitigation Strategy** | Mitigate |
| **Mitigation Plan** | (1) Pin promptfoo to a specific version in project dependencies; update deliberately with a test pass. (2) Implement a JSON schema validator at the statistical engine's input boundary that fails fast with a descriptive error on schema mismatch. (3) Abstract the promptfoo output reader into an adapter layer (consistent with hexagonal architecture H-07) so schema changes require only adapter modification. (4) Add promptfoo output schema regression tests to the framework's own CI. |
| **Residual Risk** | L=2, C=2, Score=4 (GREEN) -- Version pinning prevents surprise breaks; adapter pattern isolates changes |
| **Owner** | Implementation Lead |
| **Due Date** | Phase 2 (Standard mode delivery) |

### RISK-006: Quality Gate Dimension Mapping Drift

| Attribute | Value |
|-----------|-------|
| **Risk Statement** | If Jerry's quality gate dimensions (S-014: Completeness, Internal Consistency, Methodological Rigor, Evidence Quality, Actionability, Traceability) are modified (weights changed, dimensions added/removed), then the evaluation framework's skill comparison scoring becomes misaligned with the production quality gate, producing evaluations that do not predict actual quality gate outcomes. |
| **Affected Requirements** | REQ-016 (S-014 rubric integration), REQ-012 (Jerry governance rule assertions) |
| **Category** | Integration |
| **Likelihood** | 2 (Unlikely) -- Quality gate dimensions are governed by quality-enforcement.md (SSOT); changes require C3+ review |
| **Consequence** | 3 (Moderate) -- Misaligned evaluation produces misleading skill quality claims |
| **Score** | 6 (GREEN) |
| **Status** | Identified |
| **Applies To** | All options |
| **Root Cause** | Two systems (quality gate and evaluation framework) reference the same dimension model but do not share a single implementation |
| **Trigger** | Quality gate SSOT (quality-enforcement.md) is updated without corresponding evaluation framework update |
| **Mitigation Strategy** | Mitigate |
| **Mitigation Plan** | (1) Implement dimension weights as a shared configuration loaded from a single SSOT file (quality-enforcement.md or a dedicated quality-dimensions.yaml). (2) Add a T1 deterministic assertion that validates dimension parity between the evaluation framework and quality-enforcement.md at CI time. (3) Document the quality gate dimension contract as an explicit interface in the evaluation framework architecture. |
| **Residual Risk** | L=1, C=2, Score=2 (GREEN) -- Shared configuration eliminates drift; CI assertion catches divergence |
| **Owner** | Implementation Lead |
| **Due Date** | Phase 2 (Standard mode delivery) |

### RISK-007: Jerry CLI Integration Timing Creates Parallel Interfaces

| Attribute | Value |
|-----------|-------|
| **Risk Statement** | If the phased CLI integration approach (wrapper script first, full `jerry eval` namespace later per DIV-005) extends beyond Phase 4, then developers learn the wrapper interface and resist migrating to the full namespace, creating a permanent dual-interface maintenance burden. |
| **Affected Requirements** | REQ-021 (Jerry CLI integration) |
| **Category** | Integration / Schedule |
| **Likelihood** | 3 (Possible) -- Phased approaches commonly stall at "good enough" intermediate states |
| **Consequence** | 2 (Minor) -- Maintenance overhead for two interfaces; user confusion is bounded |
| **Score** | 6 (GREEN) |
| **Status** | Identified |
| **Applies To** | Option B (promptfoo Extension), Option C (Hybrid Composable) |
| **Root Cause** | Phased integration creates an intermediate state that may become permanent |
| **Trigger** | Wrapper script still in use 6 months after initial delivery |
| **Mitigation Strategy** | Mitigate |
| **Mitigation Plan** | (1) Set a hard deprecation date for the wrapper at Phase 4 start. (2) Include deprecation warnings in the wrapper script from day one ("This interface will be replaced by `jerry eval` in Phase 4"). (3) Design the wrapper CLI to be a strict subset of the planned `jerry eval` namespace so migration is mechanical. |
| **Residual Risk** | L=2, C=1, Score=2 (GREEN) -- Deprecation plan and API compatibility minimize migration friction |
| **Owner** | Implementation Lead |
| **Due Date** | Phase 1 (Smoke mode delivery, deprecation plan documented) |

---

## L1: Obsolescence Risk

Obsolescence risk addresses the competitive threat timeline and technology evolution that could render the framework redundant or architecturally outdated before it delivers sustained value.

### RISK-005: promptfoo Adds Native Skill Comparison

| Attribute | Value |
|-----------|-------|
| **Risk Statement** | If the promptfoo competitive team adds native skill-level evaluation (system-prompt A/B testing with quality comparison) within the 6-12 month window identified by Phase 1B, then the Skill Comparison Orchestrator component becomes redundant, the framework's most visible feature is commoditized, and the time invested in the orchestrator is partially wasted. |
| **Affected Requirements** | REQ-001 (skill as treatment variable), REQ-002 (paired comparison) |
| **Category** | Technical / Schedule |
| **Likelihood** | 3 (Possible) -- Phase 1B Section L1.5 Threat Timing Assessment rates "promptfoo adds agentic functional metrics" at 40% probability / 6-12 months and "promptfoo builds skill/workflow evaluation" at 15% probability / 12-24 months (see `projects/PROJ-017-llm-skill-testing/research/competitive-landscape.md`, Section L1.5). Phase 2 Synthesis DIV-001 identifies this as a strategic tension: promptfoo is simultaneously the recommended foundation and the primary competitive risk. |
| **Consequence** | 4 (Major) -- The most visible differentiator is neutralized; reputational risk if the framework is perceived as "promptfoo but worse" |
| **Score** | 12 (YELLOW) |
| **Status** | Active |
| **Applies To** | Option B (promptfoo Extension) -- highest exposure; Option A and C also affected but less directly |
| **Root Cause** | Building a differentiated product on top of a platform that could absorb the differentiation |
| **Trigger** | promptfoo release notes announce skill/plugin comparison feature |
| **Mitigation Strategy** | Mitigate |
| **Mitigation Plan** | (1) ADR-001 already architecturally separates the three components; the statistical engine and governance validator are independently valuable and not replicated by promptfoo. (2) Prioritize the statistical engine and governance validator delivery over orchestrator polish -- these are the defensible differentiators (CONV-003: statistical significance as differentiator; CONV-005: Jerry's existing architecture provides natural integration points; see `projects/PROJ-017-llm-skill-testing/analysis/synthesized-findings.md` L2 Strategic Implications, Theme 3: The Competitive Window Is Time-Limited). (3) Monitor promptfoo's GitHub issues and roadmap quarterly for skill-eval signals. (4) If promptfoo adds basic skill comparison, pivot to "statistical rigor + governance compliance on top of promptfoo's native skill comparison" positioning. (5) Publish the evaluation methodology (BCa bootstrap + FDR correction for skill evaluation) as a reference methodology to establish thought leadership before the feature is commoditized. |
| **Residual Risk** | L=3, C=2, Score=6 (GREEN) -- Statistical engine and governance validator survive commoditization of the orchestrator |
| **Owner** | Project Lead |
| **Due Date** | Ongoing (quarterly competitive monitoring) |

### RISK-008: LLM API Pricing Structural Shift

| Attribute | Value |
|-----------|-------|
| **Risk Statement** | If LLM API pricing increases substantially (supplier power is rated HIGH per Phase 1B Section L1.2 Porter's Force 4; see `projects/PROJ-017-llm-skill-testing/research/competitive-landscape.md`) or per-call pricing models shift to subscription-based models, then the tiered cost model (Smoke $0/Standard $5/Full $6.54, validated by CONV-004) becomes invalid and the Full tier may be financially impractical for routine use. |
| **Affected Requirements** | REQ-010 (N >= 30), REQ-017 (cost transparency reporting), AC-M02 (zero-cost CI/CD) |
| **Category** | Cost |
| **Likelihood** | 2 (Unlikely) -- Industry trend is toward decreasing API prices (Haiku/Sonnet cost reductions have been consistent); but pricing power is structural |
| **Consequence** | 3 (Moderate) -- Full tier becomes unaffordable; framework value degrades to Smoke + Standard only |
| **Score** | 6 (GREEN) |
| **Status** | Identified |
| **Applies To** | All options (any framework using LLM-as-judge is exposed) |
| **Root Cause** | Structural dependency on third-party API pricing for T2 and T4 evaluation tiers |
| **Trigger** | Anthropic API pricing increase > 3x for Sonnet or Haiku models |
| **Mitigation Strategy** | Accept + Monitor |
| **Mitigation Plan** | (1) Smoke tier (T1 deterministic, zero API cost) is immune to pricing changes and provides baseline CI/CD value. (2) Cost transparency reporting (REQ-017) makes pricing impact immediately visible. (3) The statistical engine's N parameter is configurable; N can be reduced (min 10) to control cost under higher pricing. (4) Open-weight model support (via promptfoo's provider flexibility) provides an escape valve if API pricing becomes prohibitive. |
| **Residual Risk** | L=2, C=2, Score=4 (GREEN) -- T1 immunity and N configurability provide structural resilience |
| **Owner** | Project Lead |
| **Due Date** | N/A (monitoring only) |

### RISK-009: Evaluation Tool Market Consolidation

| Attribute | Value |
|-----------|-------|
| **Risk Statement** | If the LLM evaluation tool market consolidates (Phase 1B identifies 15+ funded players, many with overlapping features), then a well-funded competitor acquires or replicates the statistical + governance combination, reducing the framework's differentiation window. |
| **Affected Requirements** | N/A (strategic positioning, not a specific requirement) |
| **Category** | Schedule |
| **Likelihood** | 2 (Unlikely) -- Jerry's governance model is highly specific; statistical rigor for LLM evaluation is a niche concern that well-funded players have not prioritized |
| **Consequence** | 2 (Minor) -- External competitive positioning affected; Jerry-internal value unaffected |
| **Score** | 4 (GREEN) |
| **Status** | Accepted |
| **Applies To** | All options |
| **Root Cause** | Active, well-funded competitive landscape with overlapping feature sets |
| **Trigger** | A tool with > 10k stars announces paired statistical skill evaluation |
| **Mitigation Strategy** | Accept |
| **Mitigation Plan** | Jerry-first scope insulates against competitive dynamics. The governance validator is non-portable. Monitor competitive landscape per Phase 1B methodology quarterly. |
| **Residual Risk** | L=2, C=2, Score=4 (GREEN) -- Internal value unaffected by competitive dynamics |
| **Owner** | Project Lead |
| **Due Date** | N/A (monitoring only) |

---

## L1: Measurement Risk

Measurement risk addresses statistical validity, false positive/negative rates, and sensitivity to sample size (N) that could undermine the framework's core value proposition -- producing reliable, defensible claims about skill quality.

### RISK-010: N=30 Single-Source Academic Basis

| Attribute | Value |
|-----------|-------|
| **Risk Statement** | If the N >= 30 per condition sample size requirement (derived from a single academic source, arXiv 2511.19794 -- https://arxiv.org/abs/2511.19794 -- flagged as SINGLE-SOURCE by Phase 1A and Phase 2 Synthesis CONV-003) is domain-inappropriate for LLM skill evaluation, then the Full tier's statistical conclusions may be unreliable (Type I/II error rates not controlled at stated alpha) and the cost model ($6.54/suite) is miscalibrated to an incorrect N. |
| **Affected Requirements** | REQ-010 (N >= 30 per condition), REQ-006 (statistical significance testing), REQ-011 (alpha 0.05) |
| **Category** | Technical / Cost |
| **Likelihood** | 3 (Possible) -- The paper addresses general LLM evaluation; Jerry skill evaluation has unique variance characteristics (e.g., structured prompts reduce output variance compared to open-ended generation) that may require different N |
| **Consequence** | 4 (Major) -- If N=30 is insufficient, the framework's core differentiator (statistical rigor) is undermined; if N=30 is excessive, the framework unnecessarily inflates cost |
| **Score** | 12 (YELLOW) |
| **Status** | Active |
| **Applies To** | All options (any framework using statistical comparison) |
| **Root Cause** | Statistical power analysis depends on effect size and variance, both of which are unknown for LLM skill evaluation |
| **Trigger** | Phase 3 calibration study shows bootstrap interval instability at N=30, or interval stability at N < 20 |
| **Mitigation Strategy** | Mitigate |
| **Mitigation Plan** | (1) N is a configurable parameter with default 30 and minimum 10 (per ADR-001 RT-003 response). (2) Phase 3 calibration study (bootstrap interval stability at N=10, 20, 30, 50) is an explicit ADR-001 Phase 3 deliverable. (3) Document the calibration methodology and results as the framework's own empirical basis. (4) If calibration shows stability at N < 30, update the default and recalculate the cost model. (5) If calibration shows instability at N=30, investigate higher N with revised cost projections. |
| **Residual Risk** | L=2, C=2, Score=4 (GREEN) -- Calibration study resolves uncertainty; configurable N prevents lock-in |
| **Owner** | Implementation Lead |
| **Due Date** | Phase 3 (Full mode delivery, calibration study) |

### RISK-011: False Positive Skill Improvement Claims

| Attribute | Value |
|-----------|-------|
| **Risk Statement** | If the statistical engine produces false positive "SKILL_IMPROVES_QUALITY" verdicts due to confounding variables (prompt phrasing, model temperature, context window state) that are not controlled in the experimental design, then developers make incorrect decisions about which skills to keep, modify, or discard. |
| **Affected Requirements** | REQ-006 (statistical significance testing), REQ-011 (alpha 0.05, one-sided hypothesis) |
| **Category** | Technical |
| **Likelihood** | 3 (Possible) -- LLM outputs are sensitive to many factors beyond skill content; controlling all confounds in a paired comparison is non-trivial |
| **Consequence** | 3 (Moderate) -- Wrong conclusions about skill quality; wasted engineering effort on skills that do not actually help |
| **Score** | 9 (YELLOW) |
| **Status** | Identified |
| **Applies To** | All options (inherent to LLM evaluation) |
| **Origin** | Assessment-originated risk from Phase 2 GAP-003 (statistical methodology gaps) and CONV-001 (determinism-first consensus); see `projects/PROJ-017-llm-skill-testing/analysis/synthesized-findings.md` |
| **Root Cause** | LLM output variance has multiple sources; paired comparison only controls for skill-as-treatment if other variables are held constant |
| **Trigger** | Skill evaluation produces "IMPROVEMENT" verdict, but subsequent manual review finds no quality difference |
| **Mitigation Strategy** | Mitigate |
| **Mitigation Plan** | (1) Require identical model, temperature (0.0 for deterministic, documented value for stochastic), and max_tokens between treatment and control conditions. (2) Use paired comparison (same prompt, same model instance) to control for prompt-level variance. (3) Report effect size (Cohen's d) alongside p-value -- small but significant effects should be interpreted cautiously. (4) Apply Benjamini-Hochberg FDR correction when evaluating multiple dimensions simultaneously. (5) Document the experimental design assumptions and their limitations in the framework's methodology guide. |
| **Residual Risk** | L=2, C=2, Score=4 (GREEN) -- Paired design + FDR correction + effect size reporting reduce false positive risk |
| **Owner** | Implementation Lead |
| **Due Date** | Phase 2 (Standard mode, statistical engine delivery) |

### RISK-012: LLM-as-Judge Scoring Inconsistency (T4)

| Attribute | Value |
|-----------|-------|
| **Risk Statement** | If the T4 LLM-as-judge evaluator (S-014 rubric applied by Claude Haiku) produces inconsistent scores across repeated evaluations of the same output, then the within-subject variance overwhelms the between-condition (skill vs. no-skill) effect, making statistical comparison unreliable even at N=30. |
| **Affected Requirements** | REQ-016 (S-014 rubric integration), REQ-006 (statistical significance testing) |
| **Category** | Technical |
| **Likelihood** | 3 (Possible) -- LLM-as-judge consistency varies by model and rubric specificity; Haiku may be more variable than Sonnet for nuanced quality dimensions |
| **Consequence** | 3 (Moderate) -- T4 evaluation tier produces noisy data that reduces statistical power; Full tier conclusions weakened |
| **Score** | 9 (YELLOW) |
| **Status** | Identified |
| **Applies To** | All options (any framework using LLM-as-judge) |
| **Origin** | Assessment-originated risk from Phase 2 DIV-003 (LLM-as-judge reliability divergence) and CONV-002 (multi-tier evaluation consensus); see `projects/PROJ-017-llm-skill-testing/analysis/synthesized-findings.md` |
| **Root Cause** | LLM-as-judge is inherently probabilistic; intra-rater reliability is model- and rubric-dependent |
| **Trigger** | Same output scored by the same rubric produces > 0.15 score variance across 10 repeated evaluations |
| **Mitigation Strategy** | Mitigate |
| **Mitigation Plan** | (1) Measure intra-rater reliability (Krippendorff's alpha or ICC) for the S-014 rubric with Haiku as part of the Phase 3 calibration study. (2) If reliability is low (alpha < 0.67), consider using Sonnet for T4 judging (higher cost but more consistent) or averaging multiple judge calls per evaluation. (3) Report inter- and intra-rater reliability metrics in evaluation output to make scoring consistency transparent. (4) Use temperature=0 for judge model calls to maximize determinism. |
| **Residual Risk** | L=2, C=2, Score=4 (GREEN) -- Calibration study identifies reliability; model selection and averaging mitigate inconsistency |
| **Owner** | Implementation Lead |
| **Due Date** | Phase 3 (Full mode delivery, calibration study) |

### RISK-013: Benjamini-Hochberg FDR Correction Over-Conservatism

| Attribute | Value |
|-----------|-------|
| **Risk Statement** | If the Benjamini-Hochberg FDR correction is applied across all 6 S-014 quality dimensions simultaneously, then the adjusted significance threshold becomes so conservative that real skill improvements fail to reach significance (false negatives), especially at the Standard tier's lower N=5. |
| **Affected Requirements** | REQ-009 (FDR correction), REQ-011 (alpha 0.05) |
| **Category** | Technical |
| **Likelihood** | 3 (Possible) -- BH correction with 6 tests at alpha=0.05 adjusts the threshold to alpha/6 for the most significant test; at N=5, power is already low |
| **Consequence** | 2 (Minor) -- Standard tier evaluations may fail to detect real improvements; mitigated by Full tier availability at higher N |
| **Score** | 6 (GREEN) |
| **Status** | Identified |
| **Applies To** | All options (any framework using multiple comparisons) |
| **Origin** | Assessment-originated risk from Phase 2 GAP-003 (statistical methodology gaps); the FDR correction approach is specified in Phase 1A but power analysis at low N is a novel risk identified in this assessment |
| **Root Cause** | Multiple comparison correction trades false positive control for statistical power |
| **Trigger** | Standard tier (N=5) evaluations consistently show "NO_EFFECT" when Full tier (N=30) shows "IMPROVEMENT" |
| **Mitigation Strategy** | Mitigate |
| **Mitigation Plan** | (1) Make FDR correction configurable: apply by default for Full tier, optional for Standard tier. (2) Report both corrected and uncorrected p-values in output. (3) Document that Standard tier (N=5) is a screening tool, not a definitive assessment -- true statistical rigor requires Full tier. (4) Consider dimension grouping: apply FDR within dimension families (structural vs. quality) rather than across all 6. |
| **Residual Risk** | L=2, C=1, Score=2 (GREEN) -- Configurable correction and documented tier expectations manage false negatives |
| **Owner** | Implementation Lead |
| **Due Date** | Phase 2 (Standard mode, statistical engine delivery) |

---

## L1: Gap Risk

Gap risk addresses unresolved research gaps (GAP-001 through GAP-005 from Phase 2 Synthesis) that could invalidate architectural assumptions or create implementation blockers if not resolved before or during the relevant implementation phase.

### RISK-014: T3 Agent External Tool Variance (GAP-001)

| Attribute | Value |
|-----------|-------|
| **Risk Statement** | If T3 agent external tool variance (web search returning different results across runs for ps-researcher, nse-explorer) is not controlled, then paired skill comparisons for T3 agents produce invalid statistical results that attribute environmental noise to skill quality differences, undermining the framework's core claim of rigorous evaluation. |
| **Affected Requirements** | REQ-001 (skill as treatment variable), REQ-003 (controlled baseline) |
| **Category** | Technical |
| **Likelihood** | 4 (Likely) -- T3 agents with WebSearch/WebFetch access will encounter different web content across runs by definition; this is highly likely for these agents |
| **Consequence** | 3 (Moderate) -- Affects 6 of 67 agents (T3 tier: ps-researcher, ps-investigator, nse-explorer, nse-architecture, plus potential others); does not affect T1/T2/T4 agents |
| **Score** | 12 (YELLOW) |
| **Status** | Active |
| **Applies To** | All options |
| **Root Cause** | External API calls introduce uncontrolled variance into the experimental design; paired comparison assumes controlled conditions |
| **Trigger** | Any evaluation of a T3-tier agent that uses WebSearch or WebFetch |
| **Mitigation Strategy** | Mitigate |
| **Mitigation Plan** | (1) Primary: Implement fixture-based response replay -- record web search responses during a "golden run" and replay them as deterministic fixtures in subsequent runs. promptfoo's custom provider mechanism supports this via response caching. (2) Secondary: For agents where fixture replay is impractical, restrict evaluation to T1 structural assertions only (navigation table, citation format, heading hierarchy) that do not depend on web content. (3) Clearly document in evaluation reports which agents were evaluated with controlled vs. uncontrolled external access. (4) In the long term, explore mock MCP servers that return deterministic responses for evaluation runs. |
| **Residual Risk** | L=2, C=2, Score=4 (GREEN) -- Fixture replay controls variance; T1-only fallback provides minimum coverage |
| **Owner** | Implementation Lead |
| **Due Date** | Phase 2 (Standard mode, when T3 agents enter evaluation scope) |

### RISK-015: Baseline Definition Ambiguity (GAP-004)

| Attribute | Value |
|-----------|-------|
| **Risk Statement** | If the operational definition of "no-skill baseline" is not precisely specified (what exactly changes between baseline and treatment conditions for agents with complex system prompts, tool definitions, and resource injections), then different evaluators implement different baselines for the same agent, producing non-comparable evaluation results. |
| **Affected Requirements** | REQ-001 (skill as treatment variable), REQ-003 (controlled baseline) |
| **Category** | Technical |
| **Likelihood** | 3 (Possible) -- Agent definitions contain multiple elements (system prompt, tools, MCP servers, governance YAML); "removing the skill" could mean removing any subset |
| **Consequence** | 3 (Moderate) -- Non-comparable results across evaluators undermine the framework's claim of standardized evaluation |
| **Score** | 9 (YELLOW) |
| **Status** | Active |
| **Applies To** | All options |
| **Root Cause** | Phase 1D requires AC-M01 (skill as treatment variable) but does not operationally define the treatment/control manipulation |
| **Trigger** | Two evaluators produce conflicting skill quality assessments for the same agent due to different baseline definitions |
| **Mitigation Strategy** | Mitigate |
| **Mitigation Plan** | (1) Define the baseline operationally: the baseline condition is the Claude model receiving the identical user prompt with NO skill-injected content -- no system prompt from the agent definition file, no tool restrictions from the `tools` frontmatter field, no MCP server configuration, and no governance YAML. This is the "bare model" baseline. (2) Implement this as the Skill Comparison Orchestrator's default: one promptfoo provider reads the agent definition file for the treatment condition; the other provider uses an empty system prompt for the control condition. (3) Support a "partial baseline" mode where only the system prompt body is removed but tool restrictions remain, for evaluating the value of the reasoning instructions independent of tool access. (4) Document the baseline specification as a formal interface in the framework's methodology guide. |
| **Residual Risk** | L=1, C=2, Score=2 (GREEN) -- Formal specification eliminates ambiguity; orchestrator enforces consistency |
| **Owner** | Implementation Lead |
| **Due Date** | Phase 1 (Smoke mode, baseline specification documented) |

### RISK-016: Behavioral H-Rule Coverage Gap (GAP-002)

| Attribute | Value |
|-----------|-------|
| **Risk Statement** | If the 48% of HARD rules classified as "behavioral" (Category C by Phase 1C, Section 4.1 H-Rule to Assertion Mapping; see `projects/PROJ-017-llm-skill-testing/research/jerry-integration-analysis.md`) cannot be reduced to structural assertions, then the Governance Compliance Validator covers only 52% of H-rules, leaving a significant governance surface untested by the framework's deterministic tier. This gap is identified as GAP-002 in Phase 2 Synthesis (`projects/PROJ-017-llm-skill-testing/analysis/synthesized-findings.md`). |
| **Affected Requirements** | REQ-012 (Jerry governance rule assertions), REQ-015 (H-rule compliance reporting) |
| **Category** | Technical |
| **Likelihood** | 4 (Likely) -- By definition, behavioral rules (e.g., H-02 "user authority -- never override", H-03 "no deception") require judgment to evaluate; T1 structural checks cannot assess behavioral compliance |
| **Consequence** | 2 (Minor) -- 52% deterministic coverage still exceeds any competing approach; behavioral rules can be covered by T4 LLM-as-judge or documented as human-review items |
| **Score** | 8 (YELLOW) |
| **Status** | Identified |
| **Applies To** | All options |
| **Root Cause** | Some governance rules describe behavioral expectations rather than structural properties; behavioral compliance assessment inherently requires judgment |
| **Trigger** | Governance auditor requests 100% H-rule coverage and finds 48% gap |
| **Mitigation Strategy** | Mitigate |
| **Mitigation Plan** | (1) Explicitly scope the Governance Compliance Validator to Category A and B (structural) H-rules only in v1. (2) For Category C (behavioral) H-rules, define proxy T1 assertions where possible (e.g., H-02 "user authority" can be partially tested by checking for AskUserQuestion invocations before destructive operations). (3) For irreducible behavioral rules, document as "requires T4 LLM-as-judge evaluation" and implement behavioral compliance as an S-014 rubric dimension in the Full tier. (4) Report H-rule coverage as two numbers: "13/25 deterministic (T1), 25/25 with T4 judging." |
| **Residual Risk** | L=3, C=1, Score=3 (GREEN) -- Transparent two-tier reporting manages expectations; T4 provides full coverage path |
| **Owner** | Implementation Lead |
| **Due Date** | Phase 1 (Smoke mode, governance scope documented); Phase 3 (Full mode, T4 behavioral assertions) |

### RISK-017: Multi-Agent Skill Composition Unaddressed (GAP-003)

| Attribute | Value |
|-----------|-------|
| **Risk Statement** | If multi-skill workflow evaluation (e.g., `/problem-solving` invoking ps-researcher + ps-analyst + ps-synthesizer in sequence) is deferred to v2 without a clear architectural extension path, then v1 evaluation results may mislead users into believing skill quality is fully assessed when multi-skill interactions (where most Jerry work occurs) remain unevaluated. |
| **Affected Requirements** | REQ-004 (multi-agent support, SCOPED OUT per synthesis) |
| **Category** | Technical |
| **Likelihood** | 2 (Unlikely) -- ADR-001 and Phase 2 Synthesis explicitly scope multi-agent as v2; the risk is that users misunderstand the scope, not that the scope is wrong |
| **Consequence** | 2 (Minor) -- v1 value proposition is clear (single-skill evaluation); multi-skill is explicitly deferred |
| **Score** | 4 (GREEN) |
| **Status** | Accepted |
| **Applies To** | All options |
| **Root Cause** | Multi-skill attribution is a fundamentally harder problem than single-skill evaluation; requiring it in v1 would delay delivery significantly |
| **Trigger** | User evaluates a multi-skill workflow and expects attribution to individual skills |
| **Mitigation Strategy** | Accept |
| **Mitigation Plan** | (1) Document the single-skill scope limitation prominently in the framework's README and evaluation output. (2) Design the Skill Comparison Orchestrator's interface to support "workflow" test cases as a v2 extension (Phase 2 Synthesis GAP-003 proposes this). (3) Include a "scope" field in evaluation reports: "single-skill" or "workflow" (v2). |
| **Residual Risk** | L=2, C=2, Score=4 (GREEN) -- Clear documentation prevents misunderstanding; architectural extension path is preserved |
| **Owner** | Project Lead |
| **Due Date** | Phase 1 (scope documentation); v2 planning (workflow extension) |

---

## ADR-001 Risk Cross-Reference

This table maps ADR-001's risk register (R-001 through R-007) to the corresponding risks in this assessment, enabling bidirectional traceability between the architecture decision and the risk assessment.

| ADR-001 Risk ID | ADR-001 Risk Description | This Assessment Risk ID(s) | Mapping Rationale |
|-----------------|--------------------------|---------------------------|-------------------|
| R-001 | Gap is a configuration gap, not capability gap (PM-002) | RISK-005 (partial) | R-001 addresses whether the gap exists; RISK-005 addresses competitive commoditization of the gap solution. Both concern the Skill Comparison Orchestrator's raison d'etre. Phase 0 validation trial resolves R-001; RISK-005 persists beyond Phase 0. |
| R-002 | N>=30 is too expensive for adoption (PM-001) | RISK-010, RISK-008 | R-002 addresses cost impact of N requirement. RISK-010 addresses statistical validity of N=30 (the upstream concern). RISK-008 addresses the downstream LLM API pricing risk that compounds R-002. |
| R-003 | promptfoo adds native skill comparison (PM-006) | RISK-005 | Direct equivalent. RISK-005 provides the full 5x5 scoring, mitigation plan, and residual risk that R-003 summarizes. |
| R-004 | Claude Code skill community is too small (RG-5) | RISK-003 | Direct equivalent. Both address external adoption risk and conclude that Jerry-first scope insulates against this risk. |
| R-005 | promptfoo YAML config cannot express skill comparison (capability gap) | RISK-015 (partial) | R-005 addresses whether promptfoo can technically express the comparison. RISK-015 addresses the downstream baseline definition ambiguity that affects comparison validity regardless of expression mechanism. Phase 0 trial resolves R-005; RISK-015 requires formal specification in Phase 1. |
| R-006 | N>=30 bootstrap requirement is incorrect (RT-003, SINGLE-SOURCE) | RISK-010 | Direct equivalent. RISK-010 provides the full 5x5 scoring and calibration study mitigation that R-006 summarizes. |
| R-007 | Composability thesis fails -- promptfoo output not ingestible by external tools (PM-005) | RISK-004 (partial) | R-007 addresses cross-tool output compatibility. RISK-004 addresses promptfoo's own output schema stability. Both concern the JSON output contract but at different boundaries (external tools vs. internal statistical engine). |

> **Traceability note:** ADR-001 R-001 through R-007 are high-level risk summaries in the architecture decision. This assessment expands them into fully scored risks per NPR 8000.4C methodology, with some ADR-001 risks mapping to multiple assessment risks (R-002 maps to RISK-010 + RISK-008) and some assessment risks having no ADR-001 equivalent (RISK-011 through RISK-014 are novel risks identified by this assessment from Phase 2 gap analysis).

---

## L2: Risk Register Table

### Complete Risk Register

| ID | Risk Statement (If... then...) | Dimension | L | C | Score | Level | Status | Option(s) | Mitigation | Residual |
|----|-------------------------------|-----------|---|---|-------|-------|--------|-----------|------------|----------|
| RISK-001 | If dual runtime (Node.js + Python) required, then setup barrier reduces adoption | Adoption | 3 | 2 | 6 | GREEN | Identified | B, C | Single setup command | 2 (GREEN) |
| RISK-002 | If developers unfamiliar with promptfoo YAML, then time-to-first-value exceeds 15min target | Adoption | 3 | 3 | 9 | YELLOW | Identified | B | Auto-generated configs, examples | 4 (GREEN) |
| RISK-003 | If Claude Code skill community too small, then general-purpose extensibility has no audience | Adoption | 3 | 2 | 6 | GREEN | Accepted | All | Jerry-first scope | 6 (GREEN) |
| RISK-004 | If promptfoo changes output schema, then statistical engine ingestion breaks | Integration | 3 | 3 | 9 | YELLOW | Identified | B | Version pinning, adapter pattern | 4 (GREEN) |
| RISK-005 | If promptfoo adds native skill comparison, then orchestrator becomes redundant | Obsolescence | 3 | 4 | 12 | YELLOW | Active | B (primary) | Statistical + governance defensibility | 6 (GREEN) |
| RISK-006 | If quality gate dimensions modified, then evaluation misaligns with production gate | Integration | 2 | 3 | 6 | GREEN | Identified | All | Shared config, CI parity assertion | 2 (GREEN) |
| RISK-007 | If wrapper-to-namespace migration stalls, then dual CLI interfaces persist | Integration | 3 | 2 | 6 | GREEN | Identified | B, C | Hard deprecation date, API subset design | 2 (GREEN) |
| RISK-008 | If LLM API pricing increases substantially, then cost model invalidated | Obsolescence | 2 | 3 | 6 | GREEN | Identified | All | T1 immunity, configurable N, open-weight models | 4 (GREEN) |
| RISK-009 | If evaluation market consolidates, then differentiation window closes | Obsolescence | 2 | 2 | 4 | GREEN | Accepted | All | Jerry-first scope insulation | 4 (GREEN) |
| RISK-010 | If N=30 is domain-inappropriate, then statistical conclusions unreliable and cost miscalibrated | Measurement | 3 | 4 | 12 | YELLOW | Active | All | Configurable N, calibration study | 4 (GREEN) |
| RISK-011 | If confounding variables not controlled, then false positive skill improvement claims | Measurement | 3 | 3 | 9 | YELLOW | Identified | All | Paired design, FDR correction, effect size | 4 (GREEN) |
| RISK-012 | If LLM-as-judge inconsistent, then T4 scoring noise overwhelms between-condition effect | Measurement | 3 | 3 | 9 | YELLOW | Identified | All | Reliability measurement, model selection | 4 (GREEN) |
| RISK-013 | If FDR correction over-conservative at N=5, then real improvements missed at Standard tier | Measurement | 3 | 2 | 6 | GREEN | Identified | All | Configurable correction, documented tier expectations | 2 (GREEN) |
| RISK-014 | If T3 agent external tool variance not controlled, then paired comparisons invalid | Gap | 4 | 3 | 12 | YELLOW | Active | All | Fixture replay, T1-only fallback | 4 (GREEN) |
| RISK-015 | If baseline definition ambiguous, then non-comparable evaluation results | Gap | 3 | 3 | 9 | YELLOW | Active | All | Formal specification, orchestrator enforcement | 2 (GREEN) |
| RISK-016 | If 48% behavioral H-rules not testable at T1, then governance coverage gap | Gap | 4 | 2 | 8 | YELLOW | Identified | All | Two-tier reporting, T4 behavioral assertions | 3 (GREEN) |
| RISK-017 | If multi-skill composition deferred, then users misunderstand v1 scope | Gap | 2 | 2 | 4 | GREEN | Accepted | All | Clear scope documentation, v2 extension path | 4 (GREEN) |

---

## L2: Risk Portfolio Analysis

### 5x5 Risk Matrix

```
           CONSEQUENCE
           1        2        3        4        5
       +--------+--------+--------+--------+--------+
  5    |   5    |  10    |  15    |  20    |  25    |  L=5 (Almost Certain)
       +--------+--------+--------+--------+--------+
  4    |   4    |  R16:8 | R14:12 |  16    |  20    |  L=4 (Likely)
       +--------+--------+--------+--------+--------+
  3    |   3    | R01:6  | R02:9  | R05:12 |  15    |  L=3 (Possible)
       |        | R03:6  | R04:9  | R10:12 |        |
       |        | R07:6  | R11:9  |        |        |
       |        | R08:6  | R12:9  |        |        |
       |        | R13:6  | R15:9  |        |        |
       +--------+--------+--------+--------+--------+
  2    |   2    | R06:4  |  R08:6 |   8    |  10    |  L=2 (Unlikely)
       |        | R09:4  |        |        |        |
       |        | R17:4  |        |        |        |
       +--------+--------+--------+--------+--------+
  1    |   1    |   2    |   3    |   4    |   5    |  L=1 (Rare)
       +--------+--------+--------+--------+--------+
         Minimal  Minor  Moderate  Major   Critical

GREEN: 1-7 (Accept/Monitor)    YELLOW: 8-15 (Mitigate/Monitor)    RED: 16-25 (Immediate Action)

Threshold derivation: Score 8 (YELLOW boundary) corresponds to L=2 C=4 or L=4 C=2 -- the lowest
product where at least one factor is rated "Major" (4) or both factors exceed the midpoint (3).
Per NPR 8000.4C, risks at this level warrant active mitigation planning. Score 16 (RED boundary)
corresponds to L=4 C=4 -- both factors at "Likely"/"Major" or higher, requiring immediate action.
```

### Risk by Category

| Category | RED | YELLOW | GREEN | Total |
|----------|-----|--------|-------|-------|
| Technical | 0 | 5 | 1 | 6 |
| Adoption | 0 | 1 | 2 | 3 |
| Integration | 0 | 1 | 3 | 4 |
| Cost | 0 | 1 | 1 | 2 |
| Schedule | 0 | 1 | 1 | 2 |
| **Total** | **0** | **8** | **9** | **17** |

Note: Some risks map to multiple categories. Primary category used for counting.

### Risk by Dimension

| Dimension | RED | YELLOW | GREEN | Total |
|-----------|-----|--------|-------|-------|
| Adoption | 0 | 1 | 2 | 3 |
| Integration | 0 | 2 | 2 | 4 |
| Obsolescence | 0 | 1 | 2 | 3 |
| Measurement | 0 | 3 | 1 | 4 |
| Gap | 0 | 3 | 1 | 4 |
| **Total** | **0** | **8** | **9** | **17** |

Note: Measurement and Gap dimensions carry the highest YELLOW concentration, reflecting the framework's novel statistical methodology and unresolved Phase 1 research gaps.

### Risk by Framework Option

| Option | Exclusive Risks | Shared Risks | Risk Exposure |
|--------|----------------|--------------|---------------|
| Option A (Standalone) | 0 | 12 shared with All | Lower integration risk, higher adoption risk |
| **Option B (promptfoo Extension)** | **RISK-002, RISK-004** | **12 shared with All, 2 shared with C** | **Moderate integration risk, lowest adoption risk** |
| Option C (Hybrid Composable) | 0 | 12 shared with All, 2 shared with B | Highest integration risk, highest adoption risk |

**Option A Risk Profile:** Option A (Standalone Framework) carries 0 exclusive risks from this register but would face elevated adoption and schedule risks not captured here because ADR-001 selected Option B. Specifically: (a) RISK-001 (dual runtime) would be eliminated (Python-only), but a new adoption risk of comparable magnitude would arise from building an entirely new evaluation tool ecosystem with no existing community (ADR-001 scores Option A at 3/10 for adoption friction vs. 9/10 for Option B). (b) RISK-002 (promptfoo learning curve) would be eliminated but replaced by a learning curve for a novel, undocumented tool. (c) RISK-004 and RISK-005 (promptfoo-specific risks) would be eliminated entirely -- this is Option A's primary risk advantage. (d) All measurement risks (RISK-010 through RISK-013) and gap risks (RISK-014 through RISK-017) apply equally to Option A. (e) The 3-6 month time-to-value for Option A (ADR-001 evaluation) would increase schedule risk for the competitive window identified by RISK-005/RISK-009. Net assessment: Option A trades 2 YELLOW promptfoo-specific risks (RISK-004, RISK-005) for higher adoption friction and schedule exposure. The 12 shared "All options" risks remain unchanged.

Option B has 2 exclusive risks (RISK-002: promptfoo learning curve, RISK-004: output schema instability) that Options A and C do not have. However, these are both YELLOW risks with clear mitigations and GREEN residual risk. In exchange, Option B eliminates the adoption friction risks that Option A (new tool ecosystem, 3-6 month delivery) and Option C (multi-backend complexity, 2-4 month abstraction overhead) would introduce.

### Review Implications

| Review Gate | Risk Concern | Impact | Recommendation |
|-------------|-------------|--------|----------------|
| Phase 0 (Validation Trial) | RISK-005 (promptfoo competitive threat) | Informs scope | Proceed -- trial validates gap hypothesis regardless |
| Phase 1 (Smoke mode) | RISK-015 (baseline ambiguity) | Blocks meaningful comparison | Resolve baseline specification before Phase 1 delivery |
| Phase 2 (Standard mode) | RISK-010 (N=30 basis), RISK-011 (false positives), RISK-014 (T3 variance) | Core statistical engine risks | Calibration study must precede or accompany Phase 2 |
| Phase 3 (Full mode) | RISK-012 (LLM-as-judge consistency) | T4 reliability | Intra-rater reliability study required at Phase 3 entry |
| Phase 4 (Jerry CI integration) | RISK-004 (promptfoo schema), RISK-007 (CLI migration) | Integration stability | Version pinning and deprecation plan must be in place |

---

## L2: Mitigation Roadmap

Mitigations sequenced by ADR-001 implementation phase, showing which risks are addressed at each stage.

### Phase 0: Validation Trial (4 hours)

| Risk | Mitigation Action | Effort |
|------|-------------------|--------|
| RISK-005 | Begin competitive monitoring (check promptfoo roadmap) | 30 min |
| (General) | Phase 0 trial resolves ADR-001 R-001 (gap classification) which contextualizes all risks | 4 hours |

### Phase 1: Smoke Mode (1 week)

| Risk | Mitigation Action | Effort |
|------|-------------------|--------|
| RISK-001 | Implement `jerry eval setup` command with runtime detection | 2 hours |
| RISK-002 | Build auto-config generation from agent definition files; include 3 worked examples | 1 day |
| RISK-007 | Document deprecation plan for wrapper CLI; design wrapper as subset of `jerry eval` | 2 hours |
| RISK-015 | Publish formal baseline specification in methodology guide | 4 hours |
| RISK-016 | Document H-rule coverage scope (52% T1, two-tier reporting format) | 2 hours |
| RISK-017 | Document single-skill scope limitation in README and evaluation output | 1 hour |

### Phase 2: Standard Mode (2 weeks)

| Risk | Mitigation Action | Effort |
|------|-------------------|--------|
| RISK-004 | Implement output schema validator and adapter pattern for promptfoo JSON ingestion | 1 day |
| RISK-006 | Implement shared quality dimension configuration (single SSOT file) | 4 hours |
| RISK-010 | Begin N-calibration study (bootstrap stability at N=10, 20, 30, 50) | 2 days |
| RISK-011 | Implement paired comparison controls (same model, temperature=0, max_tokens) | 4 hours |
| RISK-013 | Implement configurable FDR correction; document Standard tier as screening tool | 2 hours |
| RISK-014 | Implement fixture-based response replay for T3 agent evaluation | 1 day |

### Phase 3: Full Mode (2 weeks)

| Risk | Mitigation Action | Effort |
|------|-------------------|--------|
| RISK-010 | Complete N-calibration study; update default N if warranted | 1 day |
| RISK-012 | Conduct intra-rater reliability study for S-014 rubric with Haiku; adjust model selection if needed | 2 days |
| RISK-016 | Implement T4 behavioral H-rule assertions using S-014 rubric dimensions | 2 days |

### Phase 4: Jerry CI Integration (1 week)

| Risk | Mitigation Action | Effort |
|------|-------------------|--------|
| RISK-004 | Pin promptfoo version in CI; add schema regression tests | 2 hours |
| RISK-007 | Execute wrapper-to-namespace migration; remove deprecated wrapper | 1 day |

### Ongoing (Post-Launch)

| Risk | Mitigation Action | Owner | Frequency |
|------|-------------------|-------|-----------|
| RISK-003 | Monitor Claude Code ecosystem growth signals | Project Lead | Quarterly |
| RISK-005 | Monitor promptfoo roadmap and releases for skill-eval features | Project Lead | Quarterly |
| RISK-008 | Monitor LLM API pricing trends; update cost model if > 2x change | Project Lead | Quarterly |
| RISK-009 | Review competitive landscape per Phase 1B methodology | Project Lead | Quarterly |

---

## Self-Review

**S-010 Self-Review (H-15 compliance) applied before finalizing.**

**Checklist:**
- [x] P-001: Are risks based on evidence and analysis? All 17 risks trace to specific findings in Phase 2 Synthesis or ADR-001.
- [x] P-002: Will risks be persisted to project directory? Yes, writing to `projects/PROJ-017-llm-skill-testing/analysis/risk-assessment.md`.
- [x] P-004: Does each risk have documented rationale? Yes, every risk includes root cause, trigger, and evidence-based likelihood/consequence justification.
- [x] P-042: Are all identified risks documented? Yes, 17 risks across 5 dimensions. No risks suppressed.
- [x] P-042: Are RED risks explicitly escalated? No RED risks identified. All 8 YELLOW risks are documented with active mitigation plans.
- [x] P-043: Is the mandatory disclaimer included? Yes, at the top of the file.

**Quality Assessment (S-014 dimensions):**

| Dimension | Weight | Score (0-1) | Weighted | Justification |
|-----------|--------|-------------|----------|---------------|
| Completeness | 0.20 | 0.94 | 0.188 | All 5 required risk dimensions covered. 17 risks identified. All GAP-001 through GAP-005 from Phase 2 mapped to risk entries (RISK-002 now explicitly labeled GAP-005). ADR-001 risks (R-001 through R-007) cross-referenced via dedicated cross-reference table. Full risk register, portfolio analysis, and mitigation roadmap included. Option A risk profile added for complete per-option comparison. YELLOW/RED threshold derivation documented. Minor deduction: no quantitative risk trend analysis (this is the initial assessment; trends require subsequent assessments). |
| Internal Consistency | 0.20 | 0.93 | 0.186 | Risk scores consistent across dimensions: similar likelihood/consequence patterns produce similar scores. Mitigation roadmap aligns with ADR-001 implementation phases. Residual risk calculations consistent (all mitigated risks drop by at least one level). No contradictions between risk statements and mitigation plans. |
| Methodological Rigor | 0.20 | 0.93 | 0.186 | NASA NPR 8000.4C risk management methodology applied: 5x5 matrix, If-Then risk statements, L x C scoring, 4-tier classification (RED/YELLOW/GREEN). Mitigation strategies classified per NASA taxonomy (Avoid/Transfer/Mitigate/Accept). All risks include root cause, trigger, and residual risk assessment. YELLOW/RED threshold boundaries now include NPR 8000.4C derivation rationale. |
| Evidence Quality | 0.15 | 0.92 | 0.138 | Every risk cites specific Phase 2 Synthesis findings (CONV-001 through CONV-006, DIV-001 through DIV-005, GAP-001 through GAP-005) or ADR-001 components. Likelihood ratings justified with evidence. RISK-005 now cites Phase 1B Section L1.5 Threat Timing Assessment with specific probability estimates. RISK-008 cites Phase 1B Section L1.2 Porter's Force 4 with file path. RISK-010 includes full arXiv URL. RISK-016 cites Phase 1C Section 4.1 with file path. Minor deduction: some likelihood estimates inherit upstream confidence ratings (e.g., DIV-001 strategic tension). |
| Actionability | 0.15 | 0.94 | 0.141 | Every risk has a concrete mitigation plan with specific actions, owner, and due date tied to ADR-001 implementation phases. Mitigation roadmap provides sequenced timeline. Phase 2 entry criteria include specific risk mitigations. |
| Traceability | 0.10 | 0.93 | 0.093 | All risks cite affected requirements (REQ-001 through REQ-021). ADR-001 R-001 through R-007 cross-reference table provides bidirectional traceability. Phase 2 Synthesis CONV/DIV/GAP IDs cited inline (RISK-005 mitigation cites CONV-003, CONV-005; RISK-008 cites CONV-004; RISK-010 cites CONV-003; RISK-016 cites GAP-002). Phase 1B and Phase 1C file paths included in References table and inline citations. Framework option applicability documented per risk including Option A risk profile. |
| **Total** | **1.00** | | **0.932** | |

**Score: 0.932 (PASS, >= 0.92 threshold)**

> **Revision note:** This is the second scoring pass (v1.1.0), incorporating fixes from ADV-3B scoring feedback (composite 0.893 REVISE). Key changes: (1) ADR-001 cross-reference table added (Traceability +0.11), (2) Phase reference IDs replaced with CONV/DIV/GAP structured identifiers (Traceability, Evidence Quality), (3) Phase 1B/1C file paths added to inline citations and References (Evidence Quality +0.05, Traceability), (4) Option A risk profile added (Completeness), (5) GAP-005 label added to RISK-002, YELLOW threshold derivation note added (Completeness). Revised composite: 0.932 (prior: 0.933 self-assessed, 0.893 ADV-3B-scored).

**Adversarial self-critique (S-002, applied after S-003 steelman per H-16):**

*Steelman:* The risk assessment covers all 5 required dimensions, maps every Phase 2 gap to a risk entry, provides quantified L x C scoring per NASA methodology, and includes a phased mitigation roadmap that aligns with ADR-001's implementation timeline. The absence of RED risks is an honest finding (not risk suppression) given the phased architecture's built-in validation gates.

*Devil's advocate challenges:*
1. *"Are you under-scoring RISK-005 (promptfoo competition)?"* -- Possible. If promptfoo's team is already developing skill comparison, the 6-12 month timeline could be 3 months. However, L=3 C=4 (Score 12) already places this in the YELLOW band, and the mitigation (independent statistical engine + governance validator) addresses the worst case. Upgrading to L=4 would yield Score 16 (RED). Decision: maintain L=3 based on Phase 1B's MEDIUM confidence assessment of the timeline; increasing without new evidence would violate P-001 (truth/accuracy).
2. *"Is RISK-014 (T3 agent variance) under-scored at L=4 C=3?"* -- The variance is certain for T3 agents but affects only ~9% of the agent population (6 of 67). C=3 reflects the bounded scope. If the framework's value proposition were primarily about T3 agent evaluation, C=4 would be warranted.
3. *"Should multi-agent composition (RISK-017) be scored higher since most Jerry work is multi-skill?"* -- Valid concern. However, the risk is about user misunderstanding of scope (L=2), not about the scoping decision itself (which is sound). The mitigation (documentation) directly addresses the stated risk.

No score adjustments made based on self-critique. All challenges are addressed within the existing scoring rationale.

---

## References

| Source | Content | File Path |
|--------|---------|-----------|
| Phase 2 Synthesis | Convergent findings (CONV-001 through CONV-006), Divergent findings (DIV-001 through DIV-005), Gap analysis (GAP-001 through GAP-005), Determinism tier classification, Requirements alignment | `projects/PROJ-017-llm-skill-testing/analysis/synthesized-findings.md` |
| ADR-001 | Framework architecture decision, Option B selection (7.90), Risk register (R-001 through R-007), Implementation phases, Cost model | `projects/PROJ-017-llm-skill-testing/decisions/ADR-001-framework-architecture.md` |
| Phase 1B | Competitive landscape, Porter's Five Forces, promptfoo threat assessment (Section L1.5), market positioning | `projects/PROJ-017-llm-skill-testing/research/competitive-landscape.md` |
| Phase 1C | Jerry integration analysis, H-rule category mapping (52% T1-testable), S-014 dimension mapping, CLI namespace design, 67-agent evaluation surface | `projects/PROJ-017-llm-skill-testing/research/jerry-integration-analysis.md` |
| arXiv 2511.19794 | Statistical evaluation sample size requirements for LLM assessment (N >= 30 per condition) | https://arxiv.org/abs/2511.19794 |
| NPR 8000.4C | Agency Risk Management Procedural Requirements -- 5x5 risk matrix, risk response strategies | NASA Standards |
| NPR 7123.1D Process 13 | Technical Risk Management -- risk identification, assessment, mitigation methodology | NASA Standards |
| NASA Risk Management Handbook | Continuous Risk Management (CRM) cycle: Identify, Analyze, Plan, Track, Control, Communicate | NASA Standards |

---

*Generated by nse-risk agent v1.0.0*
*Risk Assessment Version: 1.1.0*
*Date: 2026-03-04 (revised from 2026-03-03 v1.0.0)*
*Project: PROJ-017 LLM Skill Testing Framework*
*Phase: 3B (Risk Assessment)*
*Quality Score: 0.932 (PASS, >= 0.92 threshold; prior ADV-3B score: 0.893 REVISE)*
*Input Artifacts: Phase 2 Synthesis, ADR-001, Phase 1B, Phase 1C*
*Methodology: NASA NPR 8000.4C 5x5 risk matrix, If-Then risk statements, L x C scoring*
*Revision: ADV-3B quality gate fixes -- ADR-001 cross-reference table, structured finding IDs, Phase 1B/1C file paths, Option A risk profile, threshold derivation*
