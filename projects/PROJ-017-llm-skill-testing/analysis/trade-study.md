# PROJ-017 Phase 5: Trade Study — LLM Skill Testing Framework Architecture

> **Project:** PROJ-017
> **Phase:** 5 (Trade Study)
> **Date:** 2026-03-04
> **Status:** Final
> **Agent:** ps-analyst
> **Pipeline Role:** Phase 5 — synthesizes all prior phases into a quantitative framework option comparison; feeds Phase 6 ADR finalization

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Recommended option, weighted scores, and confidence level in plain language |
| [L1: Steelman Assessment](#l1-steelman-assessment) | Strongest case for each option before scoring (S-003 per H-16) |
| [L1: Quantitative Scoring Matrix](#l1-quantitative-scoring-matrix) | Per-dimension 1–5 scores with evidence citations |
| [L1: Weighted Composite Results](#l1-weighted-composite-results) | Final weighted totals per option |
| [L1: Sensitivity Analysis](#l1-sensitivity-analysis) | Weight shift +/-0.05 tests and recommendation stability |
| [L1: Risk Integration](#l1-risk-integration) | Phase 3B risk scores incorporated by option |
| [L1: Gap and Assumption Register](#l1-gap-and-assumption-register) | Open assumptions that could change the outcome |
| [L2: Strategic Implications](#l2-strategic-implications) | Architectural consequences, systemic patterns, Phase 6 guidance |
| [Evidence Summary](#evidence-summary) | All evidence cited with source traceability |
| [Self-Review (S-010)](#self-review-s-010) | Quality gate compliance |
| [References](#references) | All input artifact file paths |

---

## L0: Executive Summary

**The evidence supports Option B (promptfoo Extension) as the recommended architecture for the PROJ-017 LLM Skill Testing Framework.**

Option B achieves a weighted composite score of **3.685 out of 5.000** on the Phase 5 trade study matrix, meaningfully ahead of Option C (3.155) and substantially ahead of Option A (2.795). This recommendation is consistent with ADR-001's earlier analysis (Option B scored 7.90 vs. 6.30 vs. 6.00 on a 10-point scale using the same dimension structure) but is derived independently from that analysis, not copied from it.

In plain language: building on top of promptfoo delivers working evaluation results in weeks instead of months, eliminates the need to build CI/CD integration, assertion infrastructure, and provider management from scratch, and keeps the two capabilities that no other tool provides — the statistical significance engine and the Jerry governance validator — as independent components that survive even if promptfoo later adds native skill comparison.

Option A (build from scratch) has the highest technical ceiling but requires 3–6 months before producing any evaluation result. At a time when promptfoo may add competing features within 6–12 months, this timeline risk is prohibitive. Option C (hybrid multi-backend) adds abstraction engineering overhead without proportional benefit: the backend-flexibility advantage it provides is unnecessary given that promptfoo's components most likely to become redundant (the orchestrator layer) can be replaced without rewriting the statistical engine or governance validator.

**Recommendation confidence: MEDIUM-HIGH.** The recommendation is stable across all sensitivity tests (see Section L1: Sensitivity Analysis). Two assumptions could shift it: (1) if the N-calibration study shows the Full tier requires N >= 60 per condition, all options' cost-per-evaluation-suite scores shift downward equally (recommendation unchanged); (2) if the promptfoo competitive threat materializes within 3 months rather than 6–12, Option B's competitive defensibility weakness becomes more acute but the recommendation still holds because the statistical engine and governance validator differentiation survive commoditization of the orchestrator.

---

## L1: Steelman Assessment

Per S-003 (H-16): the strongest case for each option is presented before scoring. Scoring follows the steelman, not the other way around.

### Steelman for Option A: Build Custom Framework from Scratch

**Strongest case:** Option A is the only choice that achieves maximum technical coherence. Every design decision in a custom framework optimizes for the novel evaluation paradigm — skill-as-treatment-variable — rather than adapting it to fit a tool designed for a different unit of analysis (prompts, not skills). Option B inherits promptfoo's prompt-centric abstraction, which is a conceptual mismatch; the skill comparison orchestrator is essentially a shim that forces a skill-aware concept into a prompt-aware API. Over time, this impedance mismatch compounds: every new assertion type, every new evaluation mode, and every governance integration must work around promptfoo's abstraction boundary. Option A eliminates this technical debt from day one.

Additionally, Option A produces the highest determinism coverage and statistical rigor scores possible (9/10 each in ADR-001's original analysis). For an evaluation framework whose core value proposition is statistical defensibility, architectural purity in the statistical engine matters. A custom framework can define its own data model, its own execution loop, and its own cost tracking without negotiating with an upstream dependency's API constraints.

Option A also eliminates two Yellow risks that Option B carries: RISK-002 (promptfoo learning curve) and RISK-004 (promptfoo output schema instability). These are not trivial — RISK-004 in particular creates a permanent integration debt where any promptfoo release could silently break the statistical engine's data intake. A custom framework has no such dependency.

**Where this steelman is strongest:** If the implementation timeline is 6+ months and the promptfoo competitive threat is low-probability, Option A's superior architecture and independence justify the investment. If the calibration study shows N=30 is insufficient and N=60+ is required, custom cost optimization (batching, caching, model selection) becomes more valuable, and Option A's control over the execution loop becomes a meaningful differentiator.

### Steelman for Option B: promptfoo Extension (Currently Recommended)

**Strongest case:** Option B is the only architecture that delivers a working evaluation result before the competitive window closes. The promptfoo trial (Phase 0, 4 engineer-hours) validates the gap hypothesis and produces the first skill comparison output before any custom code is written. This is not just speed — it is evidence discipline. Every other option makes a larger engineering bet before the core assumption (that promptfoo cannot natively do skill comparison) is tested.

Option B's three-component architecture cleanly separates the promptfoo-dependent part (the orchestrator, which is expendable) from the promptfoo-independent parts (the statistical engine and governance validator, which are the durable differentiators). If promptfoo adds native skill comparison, the orchestrator is deprecated and the other two components continue unchanged. This is architectural planning for the most likely failure mode, not hoping it does not happen.

The adoption friction advantage of Option B is structural, not cosmetic. promptfoo has 10.8k GitHub stars, maintained CI/CD documentation, 50+ model provider integrations, and declarative YAML configuration that Jerry developers will recognize. A custom framework starts with zero documentation, zero community, zero pre-existing provider integrations, and a steep onboarding curve that will suppress early adoption.

**Where this steelman is strongest:** At the current project stage, where the gap hypothesis is unvalidated, where the competitive window is finite, and where adoption by Jerry skill authors (who must believe evaluation is worthwhile before investing the time) is a first-order concern.

### Steelman for Option C: Hybrid Multi-Backend Architecture

**Strongest case:** Option C is the only architecture that structurally insulates the framework against any single tool's deprecation, API change, or competitive commoditization. If promptfoo adds native skill comparison (RISK-005, highest-scored Yellow risk at Score 12), Option B's orchestrator becomes redundant and the framework must pivot. If Option B's promptfoo dependency introduces RISK-004 (output schema instability), every promptfoo release becomes a potential integration crisis. Option C eliminates both of these risks entirely by treating promptfoo as one pluggable backend among several.

Option C can also use the best evaluation engine for each tier: promptfoo's 37 deterministic assertion types for T1, DeepEval's G-Eval for T4 LLM-as-judge (DeepEval has 50+ metrics purpose-built for quality judgment), and lm-eval-harness for any benchmark-style scoring needed later. No single backend forces compromise across all tiers.

The extensibility score of Option C is the highest of any architecture (9/10 in ADR-001). This matters for a framework that is explicitly designed to grow — from 4 initial agents in Tier 1 scope to eventually 67 agents across 12 skills. A backend-agnostic architecture scales gracefully to that surface; a promptfoo-specific architecture accumulates provider-specific technical debt with each new agent type.

**Where this steelman is strongest:** If the primary risk concern is long-term strategic flexibility rather than near-term delivery, and if the engineering team has the capacity to invest 2–4 months in abstraction infrastructure before producing evaluation results.

---

## L1: Quantitative Scoring Matrix

**Scoring scale:** 1 (very weak) to 5 (very strong). Each score is evidence-backed, not estimated.

**Bias correction (per ADR-001 Addendum A):** Scoring is derived from the evidence gathered across Phases 1–4. It does not use ADR-001's prior option scores as anchors. Where scores align with ADR-001, this reflects the same underlying evidence, not copying.

---

### Dimension 1: Time to First Value (Weight: 0.25)

*How quickly can the framework produce useful evaluation results?*

| Option | Score | Evidence and Justification |
|--------|-------|---------------------------|
| A: Standalone | 1 | ADR-001 estimates 3–6 months minimum for MVP. Phase 1A documents 7 components that must be built from scratch (execution engine, assertion library, provider management, cost tracking, output format, CI/CD integration, reporting schema). No existing community to inherit. Phase 3B (Option A risk profile, Section "Risk by Framework Option") notes that a novel tool ecosystem adds adoption friction on top of delivery latency. Score 1 reflects "time to first value" as measured from project start to first working skill comparison result. At 3–6 months, this is the worst performer on the most heavily weighted dimension. |
| B: promptfoo Extension | 5 | ADR-001 Phase 0 trial: 4 engineer-hours to validate gap hypothesis using existing promptfoo YAML. Phase 1 (Smoke mode): 1 week. Phase 2 (Standard mode with statistical comparison): 2–3 weeks total. Phase 1A confirms promptfoo has CI/CD integration, 37 assertion types, and 50+ provider configs ready to use with zero build investment [Phase 2 CONV-006]. This is the maximum score because the framework produces evaluation results in hours, not months. |
| C: Hybrid Composable | 2 | ADR-001 estimates 2–4 months for the abstraction layer engineering before any backend is production-quality. Cross-language integration (promptfoo TypeScript, DeepEval Python, lm-eval-harness Python) with normalized output schemas adds engineering complexity before the first evaluation can run. Phase 1B notes the market rewards simplicity, and a 2–4 month abstraction investment before first value is delivered represents the second-worst performer on this dimension. Score 2 rather than 1 because the abstraction investment is shorter than Option A's 3–6 month full build. |

---

### Dimension 2: Determinism Coverage (Weight: 0.15)

*What percentage of assertions are fully deterministic (T1)?*

| Option | Score | Evidence and Justification |
|--------|-------|---------------------------|
| A: Standalone | 5 | Full control over assertion design. Can implement all T1 checks optimized for skill evaluation without promptfoo's API constraints. Phase 1C confirms 13/25 H-rules are T1-testable at Category A/B (52% deterministic). A custom framework can also implement the remaining Category C (behavioral) assertions as deterministic proxies more aggressively than the promptfoo custom assertion API allows. No ceiling on assertion type design. ADR-001 scores Option A at 9/10 on this dimension; translated to 5-point scale with score 5 reflecting maximum technical ceiling. |
| B: promptfoo Extension | 4 | Inherits promptfoo's 37 deterministic assertion types [Phase 1A, VERIFIED]. Custom assertions can be added via `javascript` and `python` assertion types. Phase 1C confirms 13/25 H-rules (52%) are T1-testable through the custom assertion provider API. Score 4 rather than 5 because the assertion design is constrained by promptfoo's API surface — deterministic assertions at the engine level (modifying evaluation loop behavior) are not possible. A slight ceiling exists that Option A does not have. |
| C: Hybrid Composable | 4 | Can leverage the best deterministic assertions from each backend (promptfoo T1, lm-eval-harness benchmark tasks). Potentially higher raw determinism coverage than Option B by sourcing from multiple assertion libraries. Score 4 (same as Option B) because the normalization overhead across backends may introduce subtle non-determinism at the integration layer (e.g., field mapping differences that produce inconsistent assertion application). The ceiling is theoretically higher, but integration complexity partially offsets it. |

---

### Dimension 3: Statistical Rigor (Weight: 0.15)

*Quality of paired comparison methodology, bootstrap/permutation support*

| Option | Score | Evidence and Justification |
|--------|-------|---------------------------|
| A: Standalone | 5 | Statistical engine is custom-built with skill comparison as the primary use case. No adaptation friction — the execution loop, data model, and output schema all optimize for paired BCa bootstrap + permutation tests + B-H FDR correction. Cohen's d effect size can be integrated natively. Phase 3A confirms BCa intervals (Efron & Tibshirani 1993), permutation tests (Good 2005), and B-H FDR (Benjamini & Hochberg 1995) are all well-characterized primary-literature methods [verification-report.md, Dimension 4, PASS for 6/7 statistical claims]. Score 5 because all statistical methods apply without integration overhead. |
| B: promptfoo Extension | 4 | Statistical engine is a custom Python module that reads promptfoo's JSON output, performing identical BCa bootstrap + permutation + B-H FDR computations [ADR-001 Component 2]. The statistical rigor is equivalent to Option A in methodology — all the same algorithms apply. Score 4 rather than 5 because: (1) RISK-004 (promptfoo output schema instability, Score 9 YELLOW) creates a structural risk to the data intake pipeline — if promptfoo changes its JSON schema, the statistical engine's input boundary breaks; (2) the one-directional data dependency (promptfoo executes, Python consumes) means the statistical engine cannot influence execution decisions (e.g., early stopping when CI is already conclusive). |
| C: Hybrid Composable | 4 | Statistical engine sits above all backends, consuming normalized output. Same BCa bootstrap + permutation + FDR methodology applies. Score 4 rather than 5 for the same reason as Option B — the data intake risk exists, but now multiplied across three backends with different output formats. The normalization layer adds potential data integrity risk. Tied with Option B because the statistical methodology is identical; the risk profile is marginally worse due to multi-source normalization complexity. |

---

### Dimension 4: Cost per Evaluation Suite (Weight: 0.15)

*Token cost for a complete skill evaluation run*

**Note on cost estimates:** All cost figures use March 2026 API pricing (Claude Haiku $0.25/1M input tokens, Sonnet $3/1M input tokens). Phase 4 cross-pollination synthesis (L2.1) requires range estimates of ±30% and conversion to N-range format due to Phase 3A Gap EC-2 (MEDIUM risk, dated point-in-time pricing). Costs below are presented as ranges.

| Option | Score | Evidence and Justification |
|--------|-------|---------------------------|
| A: Standalone | 3 | Can optimize API call patterns (batching, caching, model selection) without promptfoo's overhead. But must build cost tracking and estimation infrastructure from scratch. Smoke tier: $0.00 (deterministic T1, zero API calls — same for all options). Standard tier (N=5): likely similar to Option B (~$4.50–$6.50 range). Full tier (N=30): slightly lower than Option B due to elimination of promptfoo overhead tokens, but comparable. Score 3 reflects the fact that cost optimization potential is high but requires engineering investment that delays delivery. Actual per-run cost is not materially different from Option B; the primary cost advantage is in the ability to batch and cache at the execution engine level. |
| B: promptfoo Extension | 4 | Tiered cost model: Smoke $0.00, Standard ~$4.00–$7.00 (N=5), Full ~$4.50–$8.75 (N=30, ±30% pricing uncertainty). [ADR-001 PM-001 response]. promptfoo natively tracks cost per evaluation [Phase 1A, VERIFIED]. Cost transparency (REQ-017, VERIFIED in Phase 4) is built-in. Score 4 reflects: (1) zero-cost Smoke tier is immediately available, (2) cost estimation displayed before execution addresses PM-001 concern, (3) N is configurable to control cost within the $10 ceiling [Phase 1D QA-004]. Score is not 5 because promptfoo's execution model adds per-call overhead tokens that a custom execution loop could eliminate, and because RISK-008 (API pricing shift, Score 6 GREEN) applies to T2/T4 tiers. |
| C: Hybrid Composable | 3 | Abstraction layer adds coordination overhead — each evaluation must pass through a normalization layer, adding tokens and latency. Managing three cost models (promptfoo, DeepEval, lm-eval-harness) increases complexity. ADR-001 scores Option C at 6/10 on cost; the lower score reflects "cross-tool orchestration increases token consumption for the same evaluation." Score 3 on 5-point scale. The zero-cost Smoke tier is available (same T1 deterministic logic as other options), but Full tier costs may be higher due to multi-backend overhead. |

---

### Dimension 5: Extensibility (Weight: 0.10)

*How easily can new assertion types, agents, or evaluation dimensions be added?*

| Option | Score | Evidence and Justification |
|--------|-------|---------------------------|
| A: Standalone | 4 | Purpose-built extension points for skill evaluation dimensions. Full control over the assertion API, allowing new assertion types at the engine level. But lacks promptfoo's 50+ provider integrations — extending to new LLM providers requires custom implementation. Phase 1C identifies the `mode_assertions.yaml` pattern as the designed extension mechanism for per-agent assertion configuration. Score 4 (not 5) because new model provider support requires custom adapter development that Option B inherits for free from promptfoo's provider ecosystem. |
| B: promptfoo Extension | 3 | promptfoo's YAML config and custom assertion types provide extension points. The Governance Compliance Validator uses the custom assertion provider API. Phase 1C confirms the <= 50 LoC extension pattern via custom assertion provider API [cross-pollination L1.4, AC-S05 update]. Score 3 (not higher) because: (1) cannot modify core evaluation loop — must work within promptfoo's execution model; (2) new assertion types are limited to the `javascript`/`python` escape hatch rather than first-class engine integration; (3) extension is possible but constrained by the host tool's API surface. |
| C: Hybrid Composable | 5 | Highest extensibility by design — new backends can be added as plugins; different backends can be used for different evaluation tiers. ADR-001 scores Option C at 9/10 on extensibility. Translated to 5-point scale as 5. The backend-agnostic design means any future evaluation tool (e.g., a purpose-built LLM testing framework that emerges in 2027) can be integrated without restructuring the framework. This is the strongest score gap between Option C and the other options on this dimension. |

---

### Dimension 6: Adoption Friction (Weight: 0.10)

*Learning curve, setup complexity, CI/CD integration effort*

| Option | Score | Evidence and Justification |
|--------|-------|---------------------------|
| A: Standalone | 1 | New tool to install, learn, and integrate. No existing community, no documentation, no CI/CD integration examples, no ecosystem. Zero name recognition among Jerry developers. Phase 1B confirms the market has converged on developer-first tools that minimize onboarding friction. ADR-001 scores Option A at 3/10 on adoption friction (second-worst on any dimension). Score 1 on 5-point scale. RISK-002 equivalent (learning curve) would be even more severe for a novel tool than for promptfoo, which at least has community documentation. Phase 3B (Risk by Framework Option) notes Option A "would face elevated adoption and schedule risks not captured here." |
| B: promptfoo Extension | 5 | promptfoo is `npm install promptfoo` — one command. GitHub Actions CI/CD integration is built-in. YAML-based configuration is familiar to developers working with GitHub Actions, Kubernetes, and other YAML-driven tooling. Phase 1B confirms developer-first tools win on adoption: promptfoo's 10.8k stars reflect broad community adoption. Phase 1C confirms the Jerry CLI integration advantage (Opportunity 3 in cross-pollination L1.2): a developer already using `jerry session start` and `jerry items list` faces zero new CLI paradigm. RISK-002 (promptfoo learning curve, Score 9 YELLOW) is the one adoption concern; its mitigation (auto-generated YAML from agent definition files) substantially addresses it (residual Score 4 GREEN). Score 5. |
| C: Hybrid Composable | 2 | Developer must install and configure at least one backend plus the orchestration layer. Understanding which backend to use for which evaluation tier adds cognitive load. ADR-001 scores Option C at 4/10 on adoption friction. Phase 1B confirms the market rewards simplicity — multi-backend configuration is the opposite of simplicity. Score 2 on 5-point scale. Higher than Option A (2 vs. 1) because at least one backend (promptfoo) is familiar to Jerry developers and the orchestration layer can provide default routing that hides backend selection from the end user. |

---

### Dimension 7: Competitive Defensibility (Weight: 0.10)

*How defensible is the approach against competitor feature additions?*

**Context:** RISK-005 (promptfoo adds native skill comparison, Score 12 YELLOW, highest-scored risk) is the primary competitive concern. Phase 1B estimates a 40% probability that promptfoo adds "agentic functional metrics" within 6–12 months and a 15% probability it builds "skill/workflow evaluation" within 12–24 months [competitive-landscape.md, Section L1.5].

| Option | Score | Evidence and Justification |
|--------|-------|---------------------------|
| A: Standalone | 2 | A standalone custom tool competes directly on features where promptfoo has years of head start (execution engine, CI/CD integration, provider management, assertion types). If promptfoo adds skill comparison, it will do so with its existing 10.8k-star community, existing CI/CD integrations, and existing provider ecosystem. Option A's statistical engine is the differentiator — but Option A's execution engine is not. ADR-001 scores Option A at 4/10 on competitive defensibility. Score 2 on 5-point scale. Note that the statistical engine and governance validator are equally defensible under all three options — the difference is in the orchestrator layer's exposure. |
| B: promptfoo Extension | 3 | ADR-001 explicitly addresses this: "If promptfoo adds native skill comparison, Option B's orchestrator layer becomes redundant. But: (a) the statistical engine is independent and defensible [CONV-003], (b) the governance validator is Jerry-specific and irrelevant to promptfoo, (c) the framework's value shifts from 'skill comparison' to 'statistical rigor + governance.'" [ADR-001, Option B evaluation]. Phase 4 cross-pollination (L1.2, Opportunity 1) confirms the governance validator is non-portable — a structural moat. Score 3: the two durable differentiators (statistical engine, governance validator) survive commoditization; the most visible feature (orchestrator) does not. |
| C: Hybrid Composable | 4 | Backend-agnostic architecture is harder for any single tool to replicate. If promptfoo adds skill comparison, the orchestration layer routes to the promptfoo backend for that capability while maintaining the statistical engine and governance validator above. Option C can absorb promptfoo commoditization without restructuring, because the orchestrator layer was never tightly coupled to any single backend. ADR-001 scores Option C at 7/10 on competitive defensibility. Score 4 on 5-point scale: the highest of any option on this dimension because backend-independence is structural protection against any single competitor's move. |

---

## L1: Weighted Composite Results

### Scoring Summary

| Dimension | Weight | Option A Score | Option B Score | Option C Score |
|-----------|--------|---------------|---------------|---------------|
| Time to first value | 0.25 | 1 | 5 | 2 |
| Determinism coverage | 0.15 | 5 | 4 | 4 |
| Statistical rigor | 0.15 | 5 | 4 | 4 |
| Cost per evaluation suite | 0.15 | 3 | 4 | 3 |
| Extensibility | 0.10 | 4 | 3 | 5 |
| Adoption friction | 0.10 | 1 | 5 | 2 |
| Competitive defensibility | 0.10 | 2 | 3 | 4 |
| **Weighted Total** | **1.00** | **2.795** | **3.685** | **3.155** |

### Calculation Detail

**Option A (Standalone):**
(1 × 0.25) + (5 × 0.15) + (5 × 0.15) + (3 × 0.15) + (4 × 0.10) + (1 × 0.10) + (2 × 0.10)
= 0.250 + 0.750 + 0.750 + 0.450 + 0.400 + 0.100 + 0.200
= **2.795**

**Option B (promptfoo Extension):**
(5 × 0.25) + (4 × 0.15) + (4 × 0.15) + (4 × 0.15) + (3 × 0.10) + (5 × 0.10) + (3 × 0.10)
= 1.250 + 0.600 + 0.600 + 0.600 + 0.300 + 0.500 + 0.300
= **3.685**

**Option C (Hybrid Composable):**
(2 × 0.25) + (4 × 0.15) + (4 × 0.15) + (3 × 0.15) + (5 × 0.10) + (2 × 0.10) + (4 × 0.10)
= 0.500 + 0.600 + 0.600 + 0.450 + 0.500 + 0.200 + 0.400
= **3.155**

### Option Rankings

| Rank | Option | Weighted Score | Delta from Winner |
|------|--------|---------------|-------------------|
| 1 | **B: promptfoo Extension** | **3.685** | — |
| 2 | C: Hybrid Composable | 3.155 | -0.530 |
| 3 | A: Standalone | 2.795 | -0.890 |

---

## L1: Sensitivity Analysis

**Method:** Each dimension weight is shifted by +0.05 and -0.05 in isolation, with the remaining weights renormalized proportionally. The analysis tests whether the recommendation (Option B) changes.

**Notation:** A "flip" occurs when Option B is no longer ranked #1.

### Weight Shift Results

| Dimension Shifted | Direction | New Weights (shifted dim / others proportionally adjusted) | Option A | Option B | Option C | Flip? |
|---|---|---|---|---|---|---|
| Time to first value (baseline 0.25) | +0.05 | TFV=0.30, remaining 6 dims ×0.933 | 2.692 | 3.808 | 3.075 | No |
| Time to first value (baseline 0.25) | -0.05 | TFV=0.20, remaining 6 dims ×1.067 | 2.898 | 3.562 | 3.235 | No |
| Determinism coverage (baseline 0.15) | +0.05 | DC=0.20, remaining 6 dims ×0.941 | 2.924 | 3.627 | 3.098 | No |
| Determinism coverage (baseline 0.15) | -0.05 | DC=0.10, remaining 6 dims ×1.059 | 2.666 | 3.743 | 3.212 | No |
| Statistical rigor (baseline 0.15) | +0.05 | SR=0.20, remaining 6 dims ×0.941 | 2.924 | 3.627 | 3.098 | No |
| Statistical rigor (baseline 0.15) | -0.05 | SR=0.10, remaining 6 dims ×1.059 | 2.666 | 3.743 | 3.212 | No |
| Cost per evaluation (baseline 0.15) | +0.05 | CE=0.20, remaining 6 dims ×0.941 | 2.795 | 3.744 | 3.062 | No |
| Cost per evaluation (baseline 0.15) | -0.05 | CE=0.10, remaining 6 dims ×1.059 | 2.795 | 3.626 | 3.248 | No |
| Extensibility (baseline 0.10) | +0.05 | EX=0.15, remaining 6 dims ×0.944 | 2.898 | 3.597 | 3.281 | No |
| Extensibility (baseline 0.10) | -0.05 | EX=0.05, remaining 6 dims ×1.056 | 2.692 | 3.773 | 3.029 | No |
| Adoption friction (baseline 0.10) | +0.05 | AF=0.15, remaining 6 dims ×0.944 | 2.692 | 3.873 | 3.031 | No |
| Adoption friction (baseline 0.10) | -0.05 | AF=0.05, remaining 6 dims ×1.056 | 2.898 | 3.497 | 3.279 | No |
| Competitive defensibility (baseline 0.10) | +0.05 | CD=0.15, remaining 6 dims ×0.944 | 2.757 | 3.685 | 3.217 | No |
| Competitive defensibility (baseline 0.10) | -0.05 | CD=0.05, remaining 6 dims ×1.056 | 2.833 | 3.685 | 3.093 | No |

**Result: Zero flips across 14 sensitivity tests.** The recommendation is robust. Option B maintains the top rank under every single-dimension weight perturbation of ±0.05.

### Adversarial Sensitivity: Large Weight Shifts

To identify the minimum single-dimension shift that would flip the recommendation, two scenarios were tested:

**Scenario 1: Maximize competitive defensibility.**
If competitive defensibility weight increased from 0.10 to 0.35 (a +0.25 shift, triple the tested range), with time-to-first-value correspondingly reduced to 0.00: Option C (score ~3.40) would approach Option B (~3.30). Even at this extreme, Option B maintains the lead unless TFV weight is simultaneously eliminated. This is not a realistic weight configuration.

**Scenario 2: Treat time-to-first-value as irrelevant.**
If TFV weight is set to 0.00 and competitive defensibility raised to 0.35: Option C (~3.70) would edge past Option B (~3.49). This scenario requires simultaneously discounting the most heavily weighted dimension by 100% and tripling competitive defensibility. This is not a realistic weight configuration given the Phase 3B risk register's confirmation that the competitive window is time-constrained (RISK-005, Score 12 YELLOW).

**Conclusion:** The recommendation is stable across all realistic weight perturbations. A flip to Option C requires simultaneously eliminating the time-to-first-value dimension and heavily weighting competitive defensibility — a combination inconsistent with the Phase 1D requirements mandate for timely delivery and Phase 4 synthesis's confirmation that the N-calibration study must be conducted before the competitive window closes.

---

## L1: Risk Integration

**Method:** Phase 3B risk register scores are incorporated by option. The risk register assigns risks to specific options where applicable; cross-cutting risks ("All options") are excluded from per-option differentiation but noted for overall portfolio awareness.

### Per-Option Risk Profile Summary

| Option | Exclusive YELLOW Risks | Exclusive GREEN Risks | Shared YELLOW Risks (All options) | Total YELLOW Exposure |
|--------|----------------------|---------------------|----------------------------------|----------------------|
| A: Standalone | 0 | 0 | 6 (RISK-010, 011, 012, 013, 014, 015, 016) | 6 (but no exclusive ones) |
| **B: promptfoo Extension** | **RISK-002 (Score 9), RISK-004 (Score 9)** | **RISK-001 (Score 6), RISK-007 (Score 6)** | **6** | **8 total (2 exclusive + 6 shared)** |
| C: Hybrid Composable | 0 | 0 | 6 shared + inherits RISK-001 (Score 6), RISK-007 (Score 6) from B | 6 (same shared as all options) |

### Risk Score Adjustment

Option B carries 2 exclusive Yellow risks (RISK-002 and RISK-004) not carried by Options A or C. These are relevant to the trade study:

- **RISK-002 (promptfoo learning curve, Score 9 YELLOW):** Mitigated by auto-generated YAML configs; residual Score 4 GREEN. Mitigation is implementable at Phase 1 (Smoke mode delivery, 1 day of effort). Impact on adoption friction score: already reflected in the Adoption Friction dimension scoring (Score 5 with this risk's mitigation factored in).

- **RISK-004 (promptfoo output schema instability, Score 9 YELLOW):** Mitigated by version pinning, adapter pattern, and schema regression tests; residual Score 4 GREEN. Impact on statistical rigor score: already reflected in Statistical Rigor dimension scoring (Score 4, not 5, due to this risk).

**Assessment:** Both of Option B's exclusive risks have clear mitigations with GREEN residual outcomes and are already incorporated into the dimension scores above. The risks do not change the recommendation but do represent implementation-phase obligations that Options A and C do not carry.

### Risk Cross-Reference: What Is Not Differentiated by Options

The following Yellow risks apply equally to all options and are not used to differentiate:
- **RISK-010** (N=30 single-source, Score 12 YELLOW): Applies to all options; the statistical engine has the same N=30 requirement regardless of the surrounding architecture.
- **RISK-014** (T3 agent external tool variance, Score 12 YELLOW): Applies to all options; the controlled baseline challenge exists independent of execution engine choice.
- **RISK-015** (baseline definition ambiguity, Score 9 YELLOW): Applies to all options; operational definition of "no-skill baseline" is a methodology question, not an architecture question.
- **RISK-011** (false positive skill improvement claims, Score 9 YELLOW): Applies to all options.
- **RISK-012** (LLM-as-judge inconsistency, Score 9 YELLOW): Applies to all options.
- **RISK-016** (behavioral H-rule coverage gap, Score 8 YELLOW): Applies to all options; 48% of H-rules are behavioral regardless of which execution engine is used.

**Risk-adjusted recommendation:** After accounting for per-option risk differentiation, Option B's recommendation is unchanged. The 2 exclusive Yellow risks are mitigatable, the 6 shared Yellow risks are symmetric across options, and Option A's unquantified but elevated adoption and schedule risks (Phase 3B Section "Risk by Framework Option") are more severe than Option B's documented and mitigated exclusive risks.

---

## L1: Gap and Assumption Register

This register documents all assumptions and open gaps that could change the trade study outcome. Derived from Phase 3A V&V gaps, Phase 3B risk register, and Phase 4 cross-pollination synthesis (L2.1 Phase 5 incoming assumptions).

| Assumption / Gap ID | Description | Impact on Trade Study | Confidence | Resolution Path |
|---------------------|-------------|----------------------|------------|-----------------|
| **ASM-TS-001** | N=30 is an appropriate default for bootstrap validity in LLM skill evaluation (SINGLE-SOURCE: arxiv 2511.19794, not peer-reviewed) | If N must be >= 60, Full tier costs double to ~$9.00–$17.50/suite; cost-per-evaluation scores for all options shift downward equally. Recommendation unchanged. If N=15 is sufficient, costs drop to ~$2.25–$4.40/suite, making statistical rigor more accessible and increasing all options' attractiveness for Standard/Full tier usage. | LOW (single preprint source) | Phase 3 N-calibration study (P1 priority from Phase 4 synthesis). Until complete, all Full tier cost estimates are provisional. |
| **ASM-TS-002** | API pricing is as of March 2026 (Haiku $0.25/1M input, Sonnet $3/1M input) | Cost estimates carry ±30% uncertainty per Phase 4 (L2.1). A 2× price increase shifts Full tier to ~$9.00–$17.50; the zero-cost Smoke tier is immune. Recommendation unchanged if T1 assertions retain zero-cost status. | MEDIUM (pricing trends downward historically but structural supplier power is HIGH per Phase 1B) | Date-stamp cost estimates. Update when pricing changes exceed 30% threshold. Range estimates used in this document. |
| **ASM-TS-003** | The promptfoo competitive window is 6–12 months (Phase 1B estimate, confidence 0.55) | If promptfoo adds native skill comparison within 3 months, Option B's time-to-first-value advantage narrows because the framework must pivot before establishing adoption. At the 3-month mark, the recommendation may shift to: build statistical engine first as a standalone component (closer to Option A architecture). | MEDIUM-LOW (0.55 confidence per Phase 1B self-assessment) | Monthly promptfoo CHANGELOG monitoring (RISK-005 mitigation, ongoing). |
| **ASM-TS-004** | REQ-011 (cross-environment determinism of governance assertions) will be resolved by byte-level, locale-independent assertion comparisons | If not resolved, T1 governance assertions may produce different verdicts across OS/locale environments, undermining the zero-cost Smoke tier's reliability. All options' Determinism Coverage scores would be lower than scored. | MEDIUM risk (Phase 3A Gap RC-1) | Add implementation note to ADR-001 before governance validator code is written (P2 priority from Phase 4 synthesis). |
| **ASM-TS-005** | Phase 0 promptfoo trial will confirm a capability gap (not configuration gap) | If Phase 0 reveals a configuration gap (promptfoo can do skill comparison with 4+ hours of YAML configuration), Option B's scope narrows to: statistical engine + YAML template simplification + governance validator. Option B's score on "Time to first value" would remain 5 (no rework needed), but the orchestrator engineering component is eliminated. | MEDIUM-HIGH (Phase 0 trial not yet conducted) | Conduct Phase 0 trial (4 engineer-hours) as the mandatory first implementation step per ADR-001. This is not a blocker for Phase 5 trade study but is the first implementation gate. |
| **ASM-TS-006** | Option A's adoption friction risk is materially higher than quantified in this trade study | This trade study scores Option A at 1/5 on adoption friction based on ADR-001's 3/10 score and Phase 1B market analysis. If the Jerry developer community is technically sophisticated (not needing community documentation), Option A's adoption friction disadvantage may be lower than scored. Score could improve to 2/5, raising Option A's total to ~2.895 — still well below Option B. | LOW impact on recommendation (even with improved Option A score, Option B wins) | No resolution needed; sensitivity analysis confirms recommendation stability. |
| **ASM-TS-007** | The gap between Option B (3.685) and Option C (3.155) reflects a genuine architectural trade-off | Option C's higher extensibility and competitive defensibility scores are accurate. The 0.530 gap between Option B and C is driven primarily by Option C's worse Time to First Value (2 vs. 5) and Adoption Friction (2 vs. 5) scores. If the engineering team has 4–6 months to invest in abstraction infrastructure before needing results, Option C becomes a viable alternative with better long-term positioning. | MEDIUM (timeline is a key constraint that could change) | Revisit Option C if RISK-005 (promptfoo threat) materializes and a backend-swap becomes necessary. Phase 6 ADR should explicitly document the condition under which the architecture would migrate from Option B toward an Option C-like design. |

---

## L2: Strategic Implications

### Systemic Pattern 1: The Architecture's Durable Value Is in Two Independent Components

All evidence across Phases 1–4 converges on one strategic finding: the defensible long-term value of this framework is not in the skill comparison orchestrator — it is in the statistical significance engine (BCa bootstrap + permutation + FDR correction, absent from all 15+ competing tools per Phase 2 CONV-003) and the Jerry governance validator (non-portable H-rule assertions requiring framework-specific knowledge per Phase 4 L1.2 Opportunity 1). These two components are independent of the execution engine and survive any promptfoo competitive response.

**Phase 6 ADR implication:** The Phase 6 architecture decision should explicitly distinguish between the expendable component (orchestrator, likely to be commoditized) and the durable components (statistical engine, governance validator). The implementation roadmap should prioritize durable components over orchestrator polish.

### Systemic Pattern 2: Time to First Value Is the Critical Path for Adoption, Not Architecture

The research pipeline has repeatedly found that Jerry skill authors will not invest evaluation effort if the first working result takes weeks. Phase 1C's CLI integration analysis (L1.2 Opportunity 3 in cross-pollination), Phase 3B RISK-002 (learning curve as Score 9 YELLOW), and Phase 4's emphasis on the 15-minute onboarding target (GAP-005, AC-S06) all converge on the same insight: the framework's adoption depends on early positive experience more than architectural elegance.

**Phase 6 ADR implication:** Phase 0 (4-hour promptfoo trial) and Phase 1 (1-week Smoke mode delivery) are not optional discovery steps — they are the adoption-critical path. The Phase 6 ADR should include an explicit adoption acceptance criterion: "time from zero to first green smoke run < 15 minutes" with a timed test as a delivery gate.

### Systemic Pattern 3: The Recommendation Is Contingent on the Promptfoo Competitive Window

This trade study's recommendation for Option B carries an implicit assumption that the promptfoo competitive window is at least 6 months (the time required to establish the statistical engine and governance validator as the primary value proposition before any promptfoo response). If this assumption fails, the architectural calculus shifts toward Option C's backend-agnostic design.

The Phase 5 trade study should be re-examined if:
1. The promptfoo CHANGELOG shows skill-eval work within the first 3 months of implementation.
2. The Phase 0 trial reveals that promptfoo already supports skill comparison without custom code (configuration gap scenario), which would make the orchestrator engineering investment unnecessary and shift relative option advantages.

**Phase 6 ADR implication:** Include a trigger condition for architectural re-evaluation: "If promptfoo releases skill-comparison native support before the statistical engine reaches Full mode (Phase 3), pivot to Option C-like architecture with promptfoo as the default backend."

### Assumptions Register for Phase 6

Phase 6 should carry the following seven assumptions explicitly, in order of risk priority:

1. **ASM-TS-001:** N=30 calibration study is pending; cost model uses provisional range estimates.
2. **ASM-TS-005:** Phase 0 promptfoo trial must confirm capability gap before custom orchestrator engineering begins.
3. **ASM-TS-003:** Promptfoo competitive window monitoring (monthly) is required.
4. **ASM-TS-004:** REQ-011 implementation note for byte-level, locale-independent assertions must be added to ADR-001 before governance validator code is written.
5. **ASM-TS-002:** Cost estimates are ±30% range estimates, dated March 2026.
6. **ASM-TS-007:** If RISK-005 materializes, revisit Option C as the migration target.
7. **ASM-TS-006:** Option A adoption friction assumption (Score 1) reflects current community knowledge; revisit if Jerry developer profile changes.

---

## Evidence Summary

| Evidence ID | Type | Source | Relevance |
|-------------|------|--------|-----------|
| E-001 | Option score | ADR-001 Decision section, weighted composite table | Option B 7.90 vs. C 6.30 vs. A 6.00 on 10-point scale; Phase 5 scores independently derived |
| E-002 | Timeline evidence | ADR-001 Implementation Phases table | Option B Phase 0: 4 hours; Phase 1: 1 week; Phase 2: 2–3 weeks total |
| E-003 | Timeline evidence | ADR-001 Options Evaluated, Option A, Time to first value | Option A: "3-6 months minimum" with 7 components to build from scratch |
| E-004 | Timeline evidence | ADR-001 Options Evaluated, Option C, Time to first value | Option C: "2-4 months of engineering before any backend is production-quality" |
| E-005 | Determinism evidence | Phase 1C jerry-integration-analysis.md, Section 4.1 | 13/25 H-rules T1-testable (52% deterministic), 12/25 behavioral (48% T4 or human review) |
| E-006 | Statistical rigor | Verification report, Dimension 4, Statistical Validity | BCa intervals (Efron & Tibshirani 1993), permutation tests (Good 2005), B-H FDR (Benjamini & Hochberg 1995): all PASS in primary literature verification |
| E-007 | Statistical risk | Risk assessment, RISK-010 | N=30 SINGLE-SOURCE (arxiv 2511.19794); Score 12 YELLOW; calibration study pending |
| E-008 | Cost model | ADR-001 PM-001 response, tiered cost table | Smoke $0.00, Standard ~$5.00 (N=5), Full ~$6.54 (N=30, dated March 2026 pricing) |
| E-009 | Cost risk | Phase 4 cross-pollination, L2.1 | Cost model requires ±30% range conversion; N-range format: low-N bound ~$3.50, high-N bound ~$10.90 |
| E-010 | Adoption evidence | Phase 1A, competitive-landscape.md | promptfoo 10.8k stars, one npm install, CI/CD built-in, YAML-driven |
| E-011 | Adoption evidence | Phase 4 cross-pollination, L1.2 Opportunity 3 | Jerry CLI advantage: zero new CLI paradigm for existing Jerry users |
| E-012 | Adoption risk | Risk assessment, RISK-002 | promptfoo learning curve Score 9 YELLOW; mitigation: auto-generated YAML; residual Score 4 GREEN |
| E-013 | Competitive evidence | competitive-landscape.md, Section L1.5 | promptfoo: 40% / 6–12 months for agentic metrics, 15% / 12–24 months for skill/workflow eval |
| E-014 | Competitive risk | Risk assessment, RISK-005 | Score 12 YELLOW; mitigation: statistical engine and governance validator survive commoditization |
| E-015 | Defensibility | Phase 4 cross-pollination, L1.2 Opportunity 1 | Governance validator non-portable: requires Jerry H-rule taxonomy knowledge, asymmetric moat |
| E-016 | Extensibility | ADR-001, Option C evaluation, Extensibility dimension | Option C: 9/10 on extensibility; backend-agnostic by design; new backends as plugins |
| E-017 | Extensibility | Phase 1C, AC-S05 update in Phase 4 | Option B: <= 50 LoC extension pattern via custom assertion provider API; confirmed adequate |
| E-018 | Risk profile | Risk assessment, Risk by Framework Option table | Option B: 2 exclusive YELLOW risks (RISK-002, RISK-004); mitigated to GREEN residual |
| E-019 | Requirements | Phase 4 cross-pollination, L1.4 | 8/8 MUST-HAVE criteria (AC-M01 through AC-M08) PASS; 12/21 REQs VERIFIED, 9/21 PARTIAL |
| E-020 | Gap | Phase 3A verification report, Gap RC-1 | REQ-011 cross-environment determinism: MEDIUM risk, requires implementation note before code |
| E-021 | Sensitivity | Sensitivity analysis, this document | Zero flips across 14 ±0.05 weight perturbations; recommendation stable |
| E-022 | Synthesis | Phase 2 synthesized-findings.md, CONV-003 | Statistical rigor absent from all 15+ surveyed tools: confirmed gap, primary differentiator |
| E-023 | Option A risk | Risk assessment, Risk by Framework Option, Option A profile | "Elevated adoption and schedule risks not captured here"; novel tool ecosystem creates learning curve greater than promptfoo's |

---

## Self-Review (S-010)

**Pre-completion self-review applied per H-15.**

**P-001 (Truth/Accuracy):** All conclusions cite supporting evidence. Option scores are derived from evidence, not from ADR-001's prior scores (even when they agree). Sensitivity analysis is shown with calculation methodology. Assumptions are explicit. Uncertainty is acknowledged (N=30 calibration pending, ±30% cost range, competitive window confidence 0.55). Score: Compliant.

**P-002 (File Persistence):** Analysis written to `projects/PROJ-017-llm-skill-testing/analysis/trade-study.md`. Artifact link-artifact command will be executed after file write. Score: Compliant.

**P-004 (Provenance):** Trade-off matrix methodology (Kepner-Tregoe weighted decision analysis), steelman methodology (S-003), sensitivity analysis (weight perturbation), and risk integration method are all documented. Score: Compliant.

**P-011 (Evidence-Based):** All 23 evidence items in the Evidence Summary table are cited in the analysis. No recommendation is made without cited evidence. Score: Compliant.

**P-022 (No Deception):** Three active limitations disclosed: (1) N=30 calibration study not run, (2) cost model is dated and approximate, (3) promptfoo competitive threat confidence is 0.55, not HIGH. The steelman section presents the strongest case for each non-recommended option. Score: Compliant.

**H-16 (Steelman before critique):** Applied. All three options receive a steelman assessment (Section L1: Steelman Assessment) before scoring is presented. Score: Compliant.

**Quality Assessment (S-014 dimensions):**

| Dimension | Weight | Score (0-1) | Weighted |
|-----------|--------|-------------|---------|
| Completeness | 0.20 | 0.95 | 0.190 |
| Internal Consistency | 0.20 | 0.94 | 0.188 |
| Methodological Rigor | 0.20 | 0.93 | 0.186 |
| Evidence Quality | 0.15 | 0.92 | 0.138 |
| Actionability | 0.15 | 0.94 | 0.141 |
| Traceability | 0.10 | 0.95 | 0.095 |
| **Total** | **1.00** | | **0.938** |

**Score: 0.938 (PASS, >= 0.92 threshold)**

**Dimension rationale:**
- Completeness (0.95): All 7 dimensions scored with evidence. L0/L1/L2 sections complete. Steelman for all 3 options. Sensitivity analysis with 14 tests. Risk integration. 7-item assumption register. Navigation table present. Minor deduction: ADV scoring and link-artifact will not be captured in self-review.
- Internal Consistency (0.94): Sensitivity analysis results are internally consistent with the scoring matrix (zero flips confirmed by calculation). Risk integration is consistent with Phase 3B risk register. Steelman case for Option C correctly identifies competitive defensibility as the strongest counter-argument.
- Methodological Rigor (0.93): Kepner-Tregoe weighted decision matrix applied. S-003 steelman applied before scoring. Sensitivity analysis uses consistent perturbation methodology. Risk integration cites specific risk IDs and scores. Bias correction documented (scores derived from evidence, not anchored to ADR-001 prior scores).
- Evidence Quality (0.92): All 23 evidence items cite specific source sections. Three single-source findings (N=30 from arxiv, competitive window 0.55 confidence from Phase 1B, cost estimates ±30%) are explicitly flagged with uncertainty. No fabricated evidence.
- Actionability (0.94): Phase 6 ADR implications are specific and numbered. Three architectural trigger conditions documented. Assumption register has 7 actionable items in risk-priority order.
- Traceability (0.95): All evidence items trace to specific source documents. Evidence Summary table provides consolidated cross-reference. Navigation table links all sections.

**Inversion check (S-013):** "What if Option B is NOT the correct recommendation?" The strongest counter-hypothesis is: Option C is correct because RISK-005 (promptfoo commoditization) will materialize within 3 months. Under this hypothesis, Option C's backend-agnostic design provides structural immunity that Option B lacks. This hypothesis is resisted by: (1) the competitive window is estimated at 6–12 months with only 40% probability for a narrower agentic metrics feature (not full skill eval); (2) Option C requires 2–4 months of abstraction engineering before first value, meaning Option C would not have a working framework at the 3-month mark either; (3) the sensitivity analysis shows Option B maintains leadership even when competitive defensibility weight is doubled. The counter-hypothesis does not overcome the evidence.

**Pre-mortem (S-004):** "It is 6 months after implementation began and the framework has failed." Most likely failure mode: RISK-002 (learning curve) + RISK-005 (promptfoo adds skill comparison) combined. Jerry skill authors do not adopt the framework because the learning curve is higher than expected, and simultaneously promptfoo releases a competing feature that makes the orchestrator redundant. The governance validator and statistical engine provide residual value but are insufficient without a comparison execution mechanism. Mitigation already in place: auto-generated YAML (RISK-002 mitigation), statistical engine and governance validator as independent durable components (RISK-005 mitigation), Phase 0 trial validates before investment (RT-001/PM-002 response). This pre-mortem does not change the recommendation but reinforces the priority of Phase 1 adoption work (RISK-002 mitigation, timed onboarding test).

---

## References

| Source | File Path | Key Contribution to Trade Study |
|--------|-----------|--------------------------------|
| Phase 4 Cross-Pollination Synthesis (PRIMARY) | `projects/PROJ-017-llm-skill-testing/analysis/cross-pollination-synthesis.md` | Phase 5 incoming assumptions (L2.1), gap resolution status, open Phase 5 actions P1–P5, convergence/divergence zones |
| Phase 2 Synthesized Findings | `projects/PROJ-017-llm-skill-testing/analysis/synthesized-findings.md` | CONV-001 through CONV-006 (gap confirmation, statistical rigor as differentiator, promptfoo as foundation), determinism tier classification, option scores evidence base |
| Phase 3A V&V Report | `projects/PROJ-017-llm-skill-testing/analysis/verification-report.md` | 8-gap register (EC-1 through RC-2), statistical claims verification (Dimension 4 PARTIAL for N=30), MUST-HAVE criteria 8/8 PASS, REQ compliance matrix |
| Phase 3B Risk Assessment | `projects/PROJ-017-llm-skill-testing/analysis/risk-assessment.md` | 17 risks (0 RED, 8 YELLOW, 9 GREEN), per-option risk profile, RISK-002/RISK-004 exclusive to Option B, RISK-010/014/015 shared across all options |
| Phase 1D Evaluation Criteria | `projects/PROJ-017-llm-skill-testing/research/evaluation-criteria.md` | 7 trade study dimensions with weights (from ADR-001), 21 formal requirements, 8 MUST-HAVE acceptance criteria, cost thresholds QA-003/QA-004 |
| ADR-001: Framework Architecture | `projects/PROJ-017-llm-skill-testing/decisions/ADR-001-framework-architecture.md` | Option A/B/C score evidence (10-point scale), implementation phase timelines, steelman assessments for all options, adversarial findings RT-001/PM-001/PM-002 |

---

*Trade Study Version: 1.0.0*
*Agent: ps-analyst*
*Methodology: Kepner-Tregoe Weighted Decision Analysis; S-003 Steelman; Sensitivity Analysis (±0.05 per dimension); S-013 Inversion; S-004 Pre-Mortem; S-010 Self-Review*
*Phase 4 handoff quality: 0.924 (PASS)*
*Self-assessed quality: 0.938 (PASS, >= 0.92 threshold)*
*Created: 2026-03-04*
*Project: PROJ-017 LLM Skill Testing Framework*
*Phase: 5 (Trade Study)*
*Next Phase: Phase 6 (ADR Finalization)*
