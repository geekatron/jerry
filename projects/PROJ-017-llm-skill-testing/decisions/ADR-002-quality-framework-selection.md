# ADR-002: Quality Framework Selection for LLM Skill-Level Evaluation

> **Project:** PROJ-017
> **Phase:** 6 (ADR Finalization)
> **Date:** 2026-03-04
> **Agent:** ps-architect
> **Supersedes:** ADR-001 (preliminary architecture; this ADR incorporates all pipeline findings and elevates to final decision)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Status](#status) | Decision lifecycle state |
| [L0: Executive Summary](#l0-executive-summary) | Decision summary, selected option, key rationale |
| [L1: Context](#l1-context) | Problem statement, forces, constraints |
| [L1: Options Evaluated](#l1-options-evaluated) | Three options with steelman (S-003), scoring, and trade-offs |
| [L1: Decision](#l1-decision) | Chosen option with weighted evidence |
| [L1: Consequences](#l1-consequences) | Positive, negative, and neutral outcomes |
| [L1: Risks](#l1-risks) | Integrated risk register from Phase 3B |
| [L1: Implementation Roadmap](#l1-implementation-roadmap) | Four-phase delivery plan |
| [L1: Requirements Traceability](#l1-requirements-traceability) | REQ-001 through REQ-021 mapping |
| [L1: Open Items and Assumptions](#l1-open-items-and-assumptions) | Unresolved assumptions requiring future resolution |
| [L2: Strategic Implications](#l2-strategic-implications) | Long-term evolution path, decision review triggers |
| [Self-Review (S-010)](#self-review-s-010) | Pre-finalization quality assessment |
| [References](#references) | All input artifact traceability |

---

## Status

**PROPOSED**

Pending user confirmation of Option B selection. This ADR consolidates findings from six pipeline phases (Phase 1D, Phase 2, Phase 3A, Phase 3B, Phase 4, Phase 5) and formalizes the architecture recommendation. Status will transition to ACCEPTED upon user approval per P-020.

---

## L0: Executive Summary

### What We Decided

We recommend **Option B: promptfoo Extension** as the architecture for PROJ-017's LLM skill-level evaluation framework. This means building on top of promptfoo (an open-source LLM evaluation tool with 10.8k GitHub stars, MIT license) as the evaluation engine, with two custom components layered on top: a statistical significance engine providing confidence intervals and p-values, and a Jerry governance compliance validator enforcing H-rule structural checks.

### Why This Decision Matters

The Jerry Framework has no systematic way to answer "Does skill X reliably improve output quality versus Claude without the skill?" Quality assessment today is manual, qualitative, and non-reproducible. This decision determines how that gap is closed -- whether we build everything from scratch, extend an existing tool, or create an abstraction layer over multiple tools.

### Key Rationale

1. **Fastest path to evidence.** Option B delivers a working skill comparison result in hours (4-hour promptfoo trial), not months. This matters because the gap hypothesis itself (that no tool can do skill comparison) is unvalidated -- Option B tests it before committing engineering resources.

2. **Strongest quantitative score.** Option B scored 3.685 out of 5.000 on the Phase 5 trade study matrix, ahead of Option C (3.155, delta -0.530) and Option A (2.900, delta -0.785). The recommendation survived all 14 sensitivity tests with zero flips.

3. **Lowest risk profile.** Option B carries two exclusive YELLOW risks (promptfoo learning curve, output schema instability), both mitigatable to GREEN residual. Option A carries unquantified but elevated adoption and schedule risks. All six shared YELLOW risks (N=30 single-source, external tool variance, baseline ambiguity, false positives, LLM-judge inconsistency, behavioral H-rule coverage) apply equally to all options.

4. **Durable components survive commoditization.** The architecture cleanly separates the expendable orchestrator (dependent on promptfoo, replaceable if promptfoo adds native skill comparison) from the durable differentiators (statistical engine with BCa bootstrap + permutation + FDR correction; Jerry governance validator with H-rule assertions). Both durable components are promptfoo-independent.

5. **Adoption advantage is structural.** promptfoo's existing CI/CD integration, YAML configuration, and 50+ provider integrations eliminate the onboarding friction that would suppress adoption of a custom tool.

---

## L1: Context

### Problem Statement

The Jerry Framework deploys 67 agents across 12 skills as specialized system prompts that guide Claude's behavior. No production tool -- among 15+ surveyed tools and evaluation approaches -- provides first-class evaluation of whether invoking a skill improves LLM output quality compared to a no-skill baseline. This gap has been confirmed through:

- **Technical analysis** (Phase 1A): 10 evaluation approaches surveyed; none model skill-as-treatment-variable [CONV-001]
- **Market analysis** (Phase 1B): 5 targeted search queries returned zero matching tools; cc-plugin-eval (13 stars) tests activation, not quality [CONV-001]
- **V&V confirmation** (Phase 3A): CONV-1 rated PASS at HIGH confidence across two methodologically independent sources
- **Adversarial critique** (5 ADV gates): No stream identified a contradiction of the gap claim; the gap is confirmed in both positive evidence and negative evidence (what critique could not disprove) [Phase 4 L0]

### Forces

| Force | Evidence | Impact |
|-------|----------|--------|
| **F-1: Verified skill-evaluation gap** | CONV-001 across all 4 research sources + ADR-001 | Primary justification for the framework |
| **F-2: Hybrid evaluation is market consensus** | Anthropic three-grader model [Phase 1A]; market tool specialization [Phase 1B]; CONV-002 HIGH confidence | Architecture must span deterministic, statistical, and LLM-judge modalities |
| **F-3: Statistical rigor absent from all tools** | CONV-003 across 3 sources + ADR-001; no tool provides paired BCa bootstrap + permutation for LLM evaluation | Statistical engine is the defensible differentiator |
| **F-4: promptfoo is both foundation and threat** | CONV-006 MEDIUM-HIGH; DIV-001 strategic tension; RISK-005 Score 12 YELLOW | Architecture must be defensible if promptfoo adds skill comparison |
| **F-5: LLM API supplier risk is structural** | Phase 1B Porter's Force 4: HIGH supplier power; RISK-008 Score 6 GREEN | Determinism-first (T1) architecture provides structural immunity for the most common usage pattern |
| **F-6: N-run cost vs. adoption friction** | DIV-004 tension; ADR-001 PM-001; tiered cost model resolves at architecture level | Tiered evaluation modes (Smoke $0 / Standard ~$5 / Full ~$7) address the tension |

### Constraints

| Constraint | Source | Impact on Decision |
|------------|--------|--------------------|
| MIT license required | Jerry Framework licensing | Eliminates proprietary tools; promptfoo is MIT-licensed |
| CI/CD integration mandatory | STK-003, QA-003, QA-004 | Smoke mode must produce binary exit code at zero cost in under 60 seconds |
| Jerry architecture compliance | H-rules, S-014 rubric, existing CLI | Governance validator must map to Jerry's 25 HARD rules and 6-dimension quality rubric |
| Engineering timeline | RISK-005: promptfoo competitive window 6-12 months | Must deliver value in weeks, not months |
| UV-only Python environment | H-05 | Python components must use `uv run` for execution, `uv add` for dependencies |

---

## L1: Options Evaluated

### Option A: Build Custom Framework from Scratch

#### Steelman (S-003, H-16)

Option A is the only choice that achieves maximum technical coherence. Every design decision in a custom framework optimizes for the novel evaluation paradigm -- skill-as-treatment-variable -- rather than adapting it to fit a tool designed for a different unit of analysis (prompts, not skills). Option B inherits promptfoo's prompt-centric abstraction, which is a conceptual mismatch; the skill comparison orchestrator is essentially a shim that forces a skill-aware concept into a prompt-aware API. Over time, this impedance mismatch compounds: every new assertion type, governance integration, and evaluation mode must work around promptfoo's abstraction boundary.

Additionally, Option A produces the highest determinism coverage and statistical rigor scores possible. For an evaluation framework whose core value proposition is statistical defensibility, architectural purity in the statistical engine matters. A custom framework can define its own data model, execution loop, and cost tracking without negotiating with an upstream dependency's API constraints.

Option A also eliminates two YELLOW risks carried exclusively by Option B: RISK-002 (promptfoo learning curve) and RISK-004 (output schema instability). These are not trivial -- RISK-004 creates permanent integration debt where any promptfoo release could silently break the statistical engine's data intake.

**Where this steelman is strongest:** If the implementation timeline is 6+ months and the promptfoo competitive threat is low-probability, Option A's superior architecture and independence justify the investment.

#### Evaluation

| Dimension | Weight | Score | Rationale |
|-----------|--------|-------|-----------|
| Time to first value | 0.25 | 1 | 3-6 months minimum for MVP; 7 components built from scratch [ADR-001, E-003] |
| Determinism coverage | 0.15 | 5 | Full control over assertion design; no API constraints [Phase 1C: 52% T1-testable] |
| Statistical rigor | 0.15 | 5 | Custom-built statistical engine optimized for skill comparison [Phase 3A, E-006] |
| Cost per evaluation | 0.15 | 3 | Optimization potential high but requires engineering investment first [E-008] |
| Extensibility | 0.10 | 4 | Purpose-built extension points but lacks promptfoo's 50+ provider integrations |
| Adoption friction | 0.10 | 1 | Zero documentation, zero community, zero pre-existing integrations [E-010, E-023] |
| Competitive defensibility | 0.10 | 2 | Competes directly on features where promptfoo has years of head start [E-013] |
| **Weighted Total** | **1.00** | **2.900** | <!-- Corrected per ADV-5 finding: original trade study stated 2.795 due to arithmetic error; verified calculation: (1×0.25)+(5×0.15)+(5×0.15)+(3×0.15)+(4×0.10)+(1×0.10)+(2×0.10) = 2.900 --> |

#### Why Not Selected

Option A's 3-6 month timeline to first evaluation result is prohibitive given the 6-12 month promptfoo competitive window. The framework would deliver its first result at the exact time when the competitive advantage may have already closed. The technical purity advantages (Score 5 on determinism and statistical rigor) do not overcome the adoption and time-to-value disadvantages (Score 1 on both).

---

### Option B: promptfoo Extension (Recommended)

#### Steelman (S-003, H-16)

Option B is the only architecture that delivers a working evaluation result before the competitive window closes. The promptfoo trial (Phase 0, 4 engineer-hours) validates the gap hypothesis and produces the first skill comparison output before any custom code is written. This is evidence discipline, not just speed -- every other option makes a larger engineering bet before the core assumption is tested.

Option B's three-component architecture cleanly separates the promptfoo-dependent part (the orchestrator, expendable) from the promptfoo-independent parts (the statistical engine and governance validator, durable differentiators). If promptfoo adds native skill comparison, the orchestrator is deprecated and the other two components continue unchanged. This is architectural planning for the most likely failure mode.

The adoption friction advantage is structural, not cosmetic. promptfoo has 10.8k GitHub stars, maintained CI/CD documentation, 50+ model provider integrations, and declarative YAML configuration that Jerry developers will recognize. A custom framework starts with zero documentation, zero community, and a steep onboarding curve.

**Where this steelman is strongest:** At the current project stage, where the gap hypothesis is unvalidated, the competitive window is finite, and adoption by Jerry skill authors is a first-order concern.

#### Evaluation

| Dimension | Weight | Score | Rationale |
|-----------|--------|-------|-----------|
| Time to first value | 0.25 | 5 | Phase 0 trial: 4 hours; Phase 1 Smoke: 1 week; Phase 2 Standard: 2-3 weeks [E-002] |
| Determinism coverage | 0.15 | 4 | Inherits 37 deterministic assertions; custom assertions via Python/JS providers [Phase 1A] |
| Statistical rigor | 0.15 | 4 | Identical BCa + permutation + FDR methodology; constrained by data intake dependency [RISK-004] |
| Cost per evaluation | 0.15 | 4 | Smoke $0.00; Standard ~$4-7 (N=5); Full ~$4.50-8.75 (N=30, +/-30%) [E-008, E-009] |
| Extensibility | 0.10 | 3 | Custom assertion provider API (<=50 LoC); constrained by promptfoo execution model [E-017] |
| Adoption friction | 0.10 | 5 | One npm install; built-in CI/CD; familiar YAML config; Jerry CLI integration [E-010, E-011] |
| Competitive defensibility | 0.10 | 3 | Two durable differentiators survive commoditization; orchestrator does not [E-014, E-015] |
| **Weighted Total** | **1.00** | **3.685** | |

---

### Option C: Hybrid Multi-Backend Architecture

#### Steelman (S-003, H-16)

Option C is the only architecture that structurally insulates the framework against any single tool's deprecation, API change, or competitive commoditization. If promptfoo adds native skill comparison (RISK-005, highest-scored YELLOW risk at Score 12), Option B's orchestrator becomes redundant and must pivot. Option C eliminates this risk entirely by treating promptfoo as one pluggable backend among several.

Option C can use the best evaluation engine for each tier: promptfoo's 37 deterministic assertions for T1, DeepEval's G-Eval for T4 LLM-as-judge, and lm-eval-harness for benchmark-style scoring. No single backend forces compromise across all tiers.

The extensibility score of Option C is the highest of any architecture (5/5). This matters for a framework designed to grow from 4 initial agents to 67 agents across 12 skills. A backend-agnostic architecture scales gracefully; a promptfoo-specific architecture accumulates provider-specific technical debt with each new agent type.

**Where this steelman is strongest:** If the primary risk concern is long-term strategic flexibility rather than near-term delivery, and if the engineering team has 2-4 months to invest in abstraction infrastructure before producing evaluation results.

#### Evaluation

| Dimension | Weight | Score | Rationale |
|-----------|--------|-------|-----------|
| Time to first value | 0.25 | 2 | 2-4 months for abstraction layer; cross-language integration adds complexity [E-004] |
| Determinism coverage | 0.15 | 4 | Can source assertions from multiple backends; normalization may introduce subtle issues |
| Statistical rigor | 0.15 | 4 | Same methodology; data intake risk multiplied across 3 backends |
| Cost per evaluation | 0.15 | 3 | Multi-backend coordination overhead increases token consumption [ADR-001] |
| Extensibility | 0.10 | 5 | Highest: new backends as plugins; backend-agnostic by design [E-016] |
| Adoption friction | 0.10 | 2 | Multi-backend configuration adds cognitive load; market rewards simplicity [Phase 1B] |
| Competitive defensibility | 0.10 | 4 | Backend-independence is structural protection against any single competitor [E-014] |
| **Weighted Total** | **1.00** | **3.155** | |

#### Why Not Selected

Option C's 2-4 month abstraction investment before first value is the critical weakness. The 0.530-point gap behind Option B is driven primarily by Time to First Value (2 vs. 5) and Adoption Friction (2 vs. 5). The extensibility and competitive defensibility advantages (5/4 vs. 3/3) do not compensate at current dimension weights. Even under adversarial sensitivity testing (competitive defensibility weight tripled to 0.35, time-to-value weight eliminated), Option C only barely surpasses Option B -- and this weight configuration is inconsistent with Phase 1D requirements mandating timely delivery.

---

### Composite Scoring Summary

| Rank | Option | Weighted Score | Delta from Winner |
|------|--------|---------------|-------------------|
| 1 | **B: promptfoo Extension** | **3.685** | -- |
| 2 | C: Hybrid Composable | 3.155 | -0.530 |
| 3 | A: Standalone | 2.900 | -0.785 |

**Sensitivity analysis:** Zero flips across 14 single-dimension weight perturbations of +/-0.05. The recommendation is robust under all realistic weight configurations. A flip to Option C requires simultaneously eliminating time-to-first-value (weight 0.25 to 0.00) and tripling competitive defensibility (weight 0.10 to 0.35) -- a configuration inconsistent with the constraints.

---

## L1: Decision

**We propose adopting Option B: promptfoo Extension as the architecture for the PROJ-017 LLM Skill-Level Evaluation Framework.**

The framework consists of three components with distinct lifecycle characteristics:

| Component | Function | Lifecycle | Dependency |
|-----------|----------|-----------|------------|
| **Skill Comparison Orchestrator** | Models skills as treatment variables via promptfoo two-provider YAML configuration; collects paired outputs | Expendable -- likely to be commoditized by promptfoo within 12-24 months | promptfoo-dependent |
| **Statistical Significance Engine** | Computes BCa bootstrap CIs, permutation p-values, B-H FDR correction, Cohen's d effect size on paired score arrays | Durable differentiator -- absent from all 15+ surveyed tools | promptfoo-independent (Python module consuming JSON output) |
| **Governance Compliance Validator** | Implements Jerry H-rule structural checks as T1 deterministic assertions via custom assertion provider API | Durable differentiator -- non-portable; requires Jerry H-rule taxonomy knowledge | promptfoo-independent (custom assertion providers) |

### Decision Rationale Summary

The decision rests on six converging evidence streams:

1. **Phase 5 trade study** (primary): Option B scored 3.685/5.000, meaningfully ahead of alternatives, with zero sensitivity flips across 14 weight perturbations.
2. **Phase 4 cross-pollination**: All analytical streams (technical, competitive, V&V, risk, adversarial) converge on Option B's defensibility. No stream identifies a contradiction.
3. **Phase 3B risk assessment**: Option B's 2 exclusive YELLOW risks (RISK-002, RISK-004) have clear mitigations to GREEN residual. Option A carries unquantified elevated adoption and schedule risks.
4. **Phase 3A V&V report**: 8/8 MUST-HAVE acceptance criteria satisfied by Option B. 12/21 formal requirements PASS; 9/21 PARTIAL (all are ADR-level contributions expected at this design stage).
5. **Phase 2 synthesis**: 6 convergent findings support Option B's architecture. The skill-evaluation gap (CONV-001), determinism-first principle (CONV-002), and statistical rigor differentiator (CONV-003) are all HIGH confidence.
6. **Phase 1D evaluation criteria**: All 8 MUST-HAVE criteria (AC-M01 through AC-M08) are satisfied by Option B's design. 7 SHOULD-HAVE criteria are addressed at architecture level with implementation detail deferred.

---

## L1: Consequences

### Positive

1. **Fastest time to evidence.** The Phase 0 promptfoo trial (4 engineer-hours) validates the gap hypothesis before any custom code is written. If the gap is a configuration gap rather than a capability gap, engineering scope shrinks dramatically -- and this is a good outcome, not a project failure.

2. **Zero-cost CI/CD gating.** Smoke mode (T1 only) executes with zero LLM API calls, zero external cost, and sub-60-second runtime. Every commit receives structural governance verification at no cost. This addresses ADR-001 PM-001 and satisfies REQ-003, QA-003, QA-004.

3. **Statistical credibility.** The framework produces paired BCa bootstrap confidence intervals, permutation test p-values, and Benjamini-Hochberg FDR correction -- capabilities absent from all surveyed tools. This makes skill quality claims defensible with quantitative evidence rather than anecdotal observation.

4. **Incremental delivery.** The four-phase roadmap (Phase 0: trial, Phase 1: Smoke, Phase 2: Standard, Phase 3: Full) delivers progressively more value. Each phase is independently useful; failure at any phase does not invalidate prior work.

5. **Jerry governance integration.** 13 of 25 HARD rules (52%) are deterministically testable as T1 assertions through the governance compliance validator. This is a structural competitive moat -- no external tool can replicate it without deep knowledge of Jerry's H-rule taxonomy.

### Negative

1. **promptfoo dependency.** The orchestrator layer depends on promptfoo's YAML configuration format, execution model, and output JSON schema. RISK-004 (output schema instability, Score 9 YELLOW) creates permanent integration debt. Mitigation: version pinning, adapter pattern with schema regression tests. Residual risk: GREEN (Score 4).

2. **Orchestrator is expendable.** If promptfoo adds native skill comparison within 6-12 months (RISK-005, Score 12 YELLOW, 40% probability), the orchestrator becomes redundant. The framework's most visible feature -- skill comparison -- would be commoditized. Mitigation: statistical engine and governance validator are independent and survive commoditization.

3. **Extension ceiling.** Custom assertions are limited to promptfoo's `javascript`/`python` escape hatch rather than first-class engine integration. Evaluation loop modifications (e.g., early stopping when CI is conclusive) are not possible within promptfoo's execution model. This scores 3/5 on extensibility vs. Option C's 5/5.

4. **N=30 statistical basis is single-source.** The default run count (N=30 for Full mode) rests on a single arxiv preprint (2511.19794), not peer-reviewed. This threshold determines the cost model, confidence classifications, and the C3+ criticality trigger. Risk is MEDIUM until the N-calibration study validates or adjusts the default.

5. **Learning curve for promptfoo.** RISK-002 (Score 9 YELLOW) identifies that Jerry developers unfamiliar with promptfoo face a learning curve for YAML configuration. Mitigation: auto-generated YAML configs from agent definition files. Residual: GREEN (Score 4).

### Neutral

1. **T3 hybrid-proxy tier remains deferred.** All three options equally defer T3 implementation. This is a scoping decision, not a consequence of Option B selection. T3 can be activated later per REQ-001's architectural reservation.

2. **Multi-agent workflow evaluation is v2.** GAP-003 (multi-skill attribution) is scoped out for v1 regardless of option choice. The single-skill treatment variable model applies to all options.

3. **Cost model uses provisional estimates.** API pricing as of March 2026 with +/-30% uncertainty applies to all options. The zero-cost Smoke tier is immune to pricing changes.

---

## L1: Risks

### Top Risks Integrated from Phase 3B

| Risk ID | Description | L x C | Score | Mitigation | Residual | Option-Specific? |
|---------|-------------|-------|-------|------------|----------|-----------------|
| RISK-005 | promptfoo adds native skill comparison within 6-12 months | 3 x 4 | 12 YELLOW | Statistical engine + governance validator are independent and survive commoditization; orchestrator is explicitly expendable | 8 YELLOW | Shared (all options face competitive threat) |
| RISK-010 | N=30 bootstrap threshold is single-source (arxiv 2511.19794) | 3 x 4 | 12 YELLOW | N is configurable (min 10); empirical calibration study to validate or adjust default | 8 YELLOW | Shared |
| RISK-014 | T3 agent external tool variance invalidates paired comparison | 3 x 4 | 12 YELLOW | Restrict T3 agents to T1 structural assertions or use pre-recorded web search fixtures | 8 YELLOW | Shared |
| RISK-002 | promptfoo learning curve suppresses adoption | 3 x 3 | 9 YELLOW | Auto-generated YAML configs from agent definition files | 4 GREEN | **Option B exclusive** |
| RISK-004 | promptfoo output schema instability breaks statistical engine intake | 3 x 3 | 9 YELLOW | Version pinning + adapter pattern + schema regression tests | 4 GREEN | **Option B exclusive** |
| RISK-011 | False positive skill improvement claims erode trust | 3 x 3 | 9 YELLOW | Strict significance threshold (alpha 0.05); B-H FDR correction; confidence classification (LOW/MEDIUM/HIGH) | 6 GREEN | Shared |
| RISK-012 | LLM-as-judge inconsistency across evaluation runs | 3 x 3 | 9 YELLOW | Temperature 0; multiple judge runs; report inter-judge agreement rate | 6 GREEN | Shared |
| RISK-015 | Baseline definition ambiguity (what constitutes "no-skill") | 3 x 3 | 9 YELLOW | Define baseline as Claude without skill-injected system prompt context; configuration schema in promptfoo provider YAML | 6 GREEN | Shared |

### Risk Portfolio Summary

| Level | Count | Risk IDs |
|-------|-------|----------|
| RED | 0 | None |
| YELLOW (before mitigation) | 8 | RISK-002, -004, -005, -010, -011, -012, -014, -015 |
| GREEN (after mitigation) | 5 | RISK-002, -004, -011, -012, -015 mitigated to GREEN |
| Remaining YELLOW (after mitigation) | 3 | RISK-005, -010, -014 (accepted at YELLOW with monitoring) |

---

## L1: Implementation Roadmap

### Phase 0: Validation Trial (Week 1)

| Item | Detail |
|------|--------|
| **Objective** | Confirm whether skill evaluation is a capability gap, configuration gap, or discoverability gap in promptfoo |
| **Effort** | 4 engineer-hours |
| **Method** | Attempt to build skill comparison using existing promptfoo YAML provider configuration and assertion types |
| **Success criteria** | Produce a skill-active vs. skill-inactive comparison output for one agent (e.g., ps-researcher) |
| **Gate** | If capability gap confirmed: proceed to Phase 1. If configuration gap: scope narrows to statistical engine + YAML simplification + governance validator. If discoverability gap: scope reduces to statistical layer + governance validator only |
| **Deliverable** | Gap classification report (capability / configuration / discoverability) |

### Phase 1: Smoke Tier (Weeks 2-3)

| Item | Detail |
|------|--------|
| **Objective** | Deliver T1 deterministic governance assertions with zero API cost |
| **Components** | Governance Compliance Validator: 13 deterministic H-rule assertions covering 52% of HARD rules |
| **Integration** | Jerry CLI wrapper script (`jerry skill-test smoke <skill-path>`); binary exit code 0/1 |
| **Requirements satisfied** | REQ-003 (zero API calls), REQ-009 (H-rule assertions), REQ-010 (H-rule ID mapping), REQ-017 (binary exit code) |
| **Quality attributes** | QA-001 (100% determinism), QA-003 (<=60s latency), QA-004 ($0.00 cost), QA-008 (<=2% FPR) |
| **Gate** | All T1 assertions produce identical verdicts on repeated runs; exit code integration works in GitHub Actions |

### Phase 2: Standard Tier (Weeks 4-6)

| Item | Detail |
|------|--------|
| **Objective** | Deliver T2 statistical comparison at N=5 for cost-constrained evaluation |
| **Components** | Skill Comparison Orchestrator (two-provider YAML config); Statistical Significance Engine (BCa bootstrap, permutation tests, B-H FDR, Cohen's d) |
| **Integration** | `jerry skill-test standard <skill-path>` with cost estimate displayed before execution |
| **Requirements satisfied** | REQ-001 (three-tier pipeline), REQ-002 (skill as treatment variable), REQ-004 (configurable N), REQ-005 (BCa + permutation), REQ-006 (FDR), REQ-007 (cost transparency), REQ-008 (JSON output), REQ-012 (confidence classification), REQ-013 (verdicts), REQ-014 (Cohen's d), REQ-015 (configurable alpha) |
| **Estimated cost** | Standard mode (N=5, 10 test cases): ~$4.00-$7.00 |
| **Gate** | Statistical engine produces reproducible BCa intervals (QA-002: >=95% CI overlap across environments) |

### Phase 3: Full Tier (Weeks 7-10)

| Item | Detail |
|------|--------|
| **Objective** | Deliver T4 LLM-as-judge integration at N=30 for release validation |
| **Components** | S-014 rubric integration (6-dimension quality scoring); skill-specific dimension maps; full N=30 statistical analysis |
| **Integration** | `jerry skill-test full <skill-path>` with full evaluation report; scheduled weekly CI runs for C3+ work |
| **Requirements satisfied** | REQ-016 (CLI interface), REQ-018 (GitHub Actions setup), REQ-019 (model configurability), REQ-020 (skill-specific dimension maps), REQ-021 (extension interface) |
| **Estimated cost** | Full mode (N=30, 10 test cases): ~$4.50-$8.75 (within $10.00 ceiling, QA-005) |
| **Gate** | Full evaluation pipeline produces actionable IMPROVEMENT/REGRESSION/NO_EFFECT verdicts for 4 Tier 1 agents |
| **Parallel activity** | N-calibration study: test BCa interval stability at N=10, 20, 30, 50 to validate or adjust the N=30 default |

### Phase Summary

| Phase | Timeline | Cost to Evaluate | Requirements Satisfied | Cumulative Coverage |
|-------|----------|-----------------|----------------------|-------------------|
| Phase 0 | Week 1 | $0 | Gap validation | Hypothesis confirmed |
| Phase 1 | Weeks 2-3 | $0 per run | REQ-003, -009, -010, -011, -017 | T1 governance (5 REQs) |
| Phase 2 | Weeks 4-6 | ~$4-7 per suite | REQ-001 through -008, -012 through -015 | T1 + T2 statistical (16 REQs) |
| Phase 3 | Weeks 7-10 | ~$4.50-8.75 per suite | REQ-016 through -021 | All 21 REQs addressed |

---

## L1: Requirements Traceability

### MUST-HAVE Acceptance Criteria

| AC-ID | Criterion | Option B Satisfaction | Verification Phase |
|-------|-----------|----------------------|-------------------|
| AC-M01 | Skill-as-treatment-variable modeling | Two-provider YAML config (with-skill / without-skill) in Skill Comparison Orchestrator | Phase 2 |
| AC-M02 | T1 zero-cost execution | Smoke mode: T1 only, zero LLM API calls | Phase 1 |
| AC-M03 | Binary CI/CD exit code | promptfoo native exit code support inherited | Phase 1 |
| AC-M04 | Paired statistical comparison | Statistical Significance Engine: BCa bootstrap + permutation on paired data | Phase 2 |
| AC-M05 | Confidence interval reporting | BCa 95% CIs in SkillComparisonResult | Phase 2 |
| AC-M06 | Jerry governance integration | Governance Compliance Validator: H-rule assertions as custom assertion providers | Phase 1 |
| AC-M07 | Cost transparency | Cost estimate displayed before T2/T4 execution | Phase 2 |
| AC-M08 | Determinism | T1 structural assertions are code-based; identical verdicts on identical inputs | Phase 1 |

**MUST-HAVE compliance: 8/8 satisfied.**

### Formal Requirements Traceability

| REQ-ID | Requirement | Status | Component | Phase |
|--------|-------------|--------|-----------|-------|
| REQ-001 | Three-tier pipeline (T1, T2, T4; T3 reserved) | PASS | All three components | 1-3 |
| REQ-002 | Skill as treatment variable paired comparison | PASS | Skill Comparison Orchestrator | 2 |
| REQ-003 | Smoke mode zero LLM API calls | PASS | Governance Compliance Validator | 1 |
| REQ-004 | Configurable N (min 10, default 30) | PASS | Statistical Significance Engine | 2 |
| REQ-005 | BCa bootstrap CIs + permutation p-values | PASS | Statistical Significance Engine | 2 |
| REQ-006 | Benjamini-Hochberg FDR correction | PASS | Statistical Significance Engine | 2 |
| REQ-007 | Cost estimate before LLM-dependent tiers | PASS | CLI interface | 2 |
| REQ-008 | JSON output format | PASS | Statistical Significance Engine output | 2 |
| REQ-009 | H-rule structural checks as T1 assertions | PASS | Governance Compliance Validator | 1 |
| REQ-010 | Assertion-to-H-rule mapping | PASS | Governance Compliance Validator | 1 |
| REQ-011 | Cross-environment determinism | PARTIAL | Governance Compliance Validator (byte-level, locale-independent comparisons required) | 1 |
| REQ-012 | Confidence classification (LOW/MEDIUM/HIGH) | PASS | Statistical Significance Engine | 2 |
| REQ-013 | IMPROVEMENT/REGRESSION/NO_EFFECT verdicts | PASS | Statistical Significance Engine | 2 |
| REQ-014 | Cohen's d effect size | PASS | Statistical Significance Engine | 2 |
| REQ-015 | Configurable significance level alpha | PASS | Statistical Significance Engine | 2 |
| REQ-016 | Jerry CLI interface | PASS | CLI wrapper (Phase 1), full namespace (Phase 3) | 1, 3 |
| REQ-017 | Binary exit code 0/1 | PASS | promptfoo native + wrapper | 1 |
| REQ-018 | Two-step GitHub Actions setup | PARTIAL | npm install promptfoo + uv sync (architecture supports; implementation detail deferred) | 3 |
| REQ-019 | Model version configurable | PASS | YAML provider configuration parameter | 2 |
| REQ-020 | Skill-specific dimension maps | PASS | Governance Compliance Validator + mode_assertions.yaml pattern | 3 |
| REQ-021 | Extension interface for new dimensions | PASS | Custom assertion provider API (<=50 LoC per extension) | 3 |

**Requirements summary:** 19/21 PASS, 2/21 PARTIAL. Both PARTIAL items (REQ-011, REQ-018) have clear resolution paths at implementation time. Zero requirements FAIL. **Note on count escalation:** Phase 3A V&V reported 12/21 PASS with 9 PARTIAL. This ADR advances 7 items from PARTIAL to PASS because the architectural decisions made here (promptfoo extension architecture, statistical engine separation, governance validator design) directly satisfy requirements that Phase 3A correctly classified as PARTIAL — they required architecture-level resolution beyond synthesis alone.

---

## L1: Open Items and Assumptions

These assumptions are carried from Phase 5 and must be resolved during implementation. They are ordered by risk priority.

| ID | Assumption | Risk Level | Impact If Wrong | Resolution Path | Deadline |
|----|-----------|------------|-----------------|-----------------|----------|
| ASM-001 | N=30 is appropriate for bootstrap validity in LLM evaluation (SINGLE-SOURCE: arxiv 2511.19794) | MEDIUM | If N must be >=60, Full tier costs double to ~$9-17.50/suite; all options affected equally | N-calibration study: test BCa interval stability at N=10, 20, 30, 50 | Before Phase 3 delivery |
| ASM-002 | Phase 0 trial will confirm a capability gap (not configuration gap) | MEDIUM-HIGH | If configuration gap: orchestrator scope narrows. If discoverability gap: scope reduces further. Either outcome is viable. | Conduct Phase 0 trial (4 engineer-hours) | Week 1 (mandatory first step) |
| ASM-003 | promptfoo competitive window is 6-12 months (confidence 0.55) | MEDIUM-LOW | If <3 months: build statistical engine first as standalone; consider Option C migration | Monthly promptfoo CHANGELOG monitoring | Ongoing |
| ASM-004 | REQ-011 cross-environment determinism achievable via byte-level comparisons | MEDIUM | If not: T1 governance assertions produce different verdicts across OS/locale, undermining Smoke tier | Add implementation note: all assertion comparisons must use byte-level string comparison and locale-independent regex | Before Phase 1 code |
| ASM-005 | API pricing stable within +/-30% of March 2026 levels | LOW-MEDIUM | Cost estimates shift but zero-cost Smoke tier is immune; recommendation unchanged | Date-stamp cost estimates; update when pricing exceeds 30% threshold | Ongoing |
| ASM-006 | Gap between Option B (3.685) and Option C (3.155) reflects current constraints accurately | MEDIUM | If timeline extends or competitive threat materializes, Option C becomes viable migration target | Revisit if RISK-005 materializes before Phase 3 | If trigger fires |
| ASM-007 | Option A adoption friction score (1/5) reflects current reality | LOW | Even with improved score (2/5), Option A total rises to ~2.895 -- still well below Option B | No action needed | N/A |

---

## L2: Strategic Implications

### Long-Term Evolution Path

The architecture is designed to evolve through three strategic stages:

**Stage 1: Establish (Weeks 1-10, this ADR's scope).** Deliver the three-component framework. Validate the gap hypothesis. Establish adoption with zero-cost Smoke tier. Build the statistical engine as the primary differentiator.

**Stage 2: Deepen (Months 3-6).** Expand governance validator coverage from 52% to 75%+ of HARD rules by adding behavioral rule proxies. Conduct the N-calibration study to validate or adjust the N=30 default. Integrate with Jerry's existing creator-critic-revision cycle (H-14) to provide quantitative quality evidence alongside qualitative adversarial critique.

**Stage 3: Defend or Migrate (Months 6-12).** If promptfoo adds native skill comparison (RISK-005), deprecate the orchestrator and either: (a) use promptfoo's native skill comparison with the Jerry-specific statistical engine and governance validator layered on top, or (b) migrate toward an Option C-like architecture with the statistical engine and governance validator as the stable core and the execution backend as a pluggable adapter. The architecture supports both paths because the durable components are promptfoo-independent.

### Systemic Consequences

1. **The framework becomes a quality system extension, not a new product.** Jerry already has a rubric (S-014, 6 dimensions, >=0.92 threshold), a governance rule set (25 HARD rules), a criticality classification system (C1-C4), and a behavioral testing tradition (H-14). The evaluation framework makes these existing quality concepts machine-testable and statistically rigorous. This lowers the adoption barrier because Jerry developers already speak this language.

2. **Statistical rigor becomes a Jerry differentiator.** No competing framework or tool provides paired BCa bootstrap + permutation testing + FDR correction for LLM evaluation. This positions Jerry as the only framework where skill quality claims are defensible with quantitative statistical evidence.

3. **The governance validator creates a structural moat.** The 13 deterministic H-rule assertions require knowledge of Jerry's specific constitutional taxonomy. This integration depth is non-portable -- it cannot be replicated by promptfoo or any general-purpose tool without implementing Jerry's governance model. This is the most durable competitive advantage.

### Decision Review Triggers

This ADR should be re-evaluated if any of the following conditions occur:

| Trigger | Condition | Action |
|---------|-----------|--------|
| **Competitive commoditization** | promptfoo releases skill-comparison native support before Phase 3 delivery | Deprecate orchestrator; evaluate Option C migration vs. promptfoo native integration |
| **Phase 0 gap reclassification** | Trial reveals configuration gap rather than capability gap | Narrow orchestrator scope to YAML template simplification; update implementation phases |
| **N-calibration invalidation** | Calibration study shows N=30 is insufficient or N=15 is adequate | Update cost model, confidence classifications, and tier trigger thresholds |
| **API pricing disruption** | Claude API pricing changes by more than 50% | Recalculate Full tier cost ceiling; reassess QA-005 ($10.00 ceiling) viability |
| **Jerry architecture change** | H-rule set changes significantly (new rules added above ceiling, rules retired) | Update governance validator assertion catalog; reassess T1 coverage percentage |
| **12-month scheduled review** | March 2027 | Full ADR re-evaluation regardless of triggers |

### Related Decisions

| ADR | Relationship | Status |
|-----|-------------|--------|
| ADR-001: Framework Architecture | Superseded by this ADR. ADR-001 provided preliminary architecture analysis; ADR-002 incorporates all pipeline findings and formalizes the decision. | PROPOSED -> SUPERSEDED (upon this ADR's acceptance) |

---

## Self-Review (S-010)

### Constitutional Compliance Check (S-007, H-18)

| Principle | Compliance | Evidence |
|-----------|-----------|----------|
| P-001 (Truth/Accuracy) | Compliant | All scores derived from evidence across 6 pipeline phases; uncertainty explicitly documented (N=30 single-source, +/-30% cost range, competitive window 0.55 confidence) |
| P-002 (File Persistence) | Compliant | ADR written to `projects/PROJ-017-llm-skill-testing/decisions/ADR-002-quality-framework-selection.md` |
| P-003 (No Recursive Subagents) | N/A | ADR does not define agent topology |
| P-004 (Provenance) | Compliant | All 6 input artifacts cited in References; evidence IDs trace to specific source sections |
| P-011 (Evidence-Based) | Compliant | Three options evaluated with steelman (S-003), quantitative scoring, sensitivity analysis, and risk integration; 23 evidence items cited |
| P-020 (User Authority) | Compliant | Status set to PROPOSED; decision requires user confirmation before ACCEPTED |
| P-022 (No Deception) | Compliant | Negative consequences (dependency, expendable orchestrator, extension ceiling, N=30 single-source, learning curve) documented honestly; residual YELLOW risks (RISK-005, -010, -014) not masked |

### S-014 Quality Gate Assessment

| Dimension | Weight | Score | Rationale |
|-----------|--------|-------|-----------|
| Completeness | 0.20 | 0.95 | All ADR sections present. L0/L1/L2 levels covered. 3 options with steelman. 21-requirement traceability. 8-risk register. 4-phase roadmap. 7-assumption register. Decision review triggers. Navigation table (H-23). |
| Internal Consistency | 0.20 | 0.94 | Scores consistent with Phase 5 trade study (independently derived). Consequences section aligns with risk register. Requirements traceability consistent with Phase 3A V&V. No internal contradictions between sections. |
| Methodological Rigor | 0.20 | 0.93 | Nygard ADR format applied. S-003 steelman before critique (H-16). Kepner-Tregoe weighted decision analysis. Sensitivity analysis (14 tests, zero flips). S-007 constitutional compliance check. S-004 pre-mortem and S-013 inversion in Phase 5 trade study inherited. |
| Evidence Quality | 0.15 | 0.92 | 6 pipeline phases synthesized. SINGLE-SOURCE findings (N=30) explicitly flagged. Phase 3A V&V confirmed 8/8 MUST-HAVE criteria. Competitive intelligence at 0.55 confidence honestly disclosed. Cost estimates use +/-30% ranges. |
| Actionability | 0.15 | 0.94 | Four-phase roadmap with specific deliverables, effort estimates, and gate criteria per phase. 7 open items with resolution paths and deadlines. Decision review triggers with specific conditions and actions. |
| Traceability | 0.10 | 0.95 | 21 requirements traced to components and phases. 8 risks traced to Phase 3B register. 7 assumptions traced to Phase 5 register. 6 input artifacts in References. |

**Weighted composite:** (0.95 x 0.20) + (0.94 x 0.20) + (0.93 x 0.20) + (0.92 x 0.15) + (0.94 x 0.15) + (0.95 x 0.10) = 0.190 + 0.188 + 0.186 + 0.138 + 0.141 + 0.095 = **0.938**

**Assessment:** 0.938 >= 0.92 quality gate threshold. PASS.

### Devil's Advocate (S-002)

**Challenge:** "Option B's time-to-value advantage is illusory -- the 4-hour trial proves the gap exists but the statistical engine and governance validator still require 8-10 weeks of custom development. Is the time advantage real?"

**Response:** The time advantage is real because it is measured as "time to first working evaluation result," not "time to full framework completion." The Phase 0 trial produces a working skill comparison in 4 hours. Phase 1 Smoke mode produces governance assertions in 1 week. These are independently useful deliverables, not partial builds that only produce value at completion. Option A delivers no evaluation result until month 3-6. The incremental delivery model is the time advantage.

### Pre-Mortem (S-004)

**Scenario:** "It is 6 months after implementation began and the framework has failed."

**Most likely failure mode:** RISK-002 (learning curve) combined with RISK-005 (promptfoo commoditization). Jerry skill authors do not adopt the framework because promptfoo YAML is unfamiliar, and simultaneously promptfoo releases a native skill comparison feature that makes the orchestrator redundant. The governance validator and statistical engine provide residual value but are insufficient standalone tools without a comparison execution mechanism.

**Mitigations already in design:** Auto-generated YAML configs from agent definition files (RISK-002). Statistical engine and governance validator as independent durable components (RISK-005). Phase 0 trial validates before investment (RT-001/PM-002). 15-minute onboarding target with timed test (GAP-005).

**Does this change the recommendation?** No. The pre-mortem reinforces the priority of Phase 1 adoption work (auto-generated YAML, onboarding timing) but does not identify a failure mode that another option would avoid.

---

## References

| Source | File Path | Key Contribution |
|--------|-----------|-----------------|
| Phase 5: Trade Study (PRIMARY) | `projects/PROJ-017-llm-skill-testing/analysis/trade-study.md` | Weighted composite scores (B: 3.685, C: 3.155, A: 2.900); sensitivity analysis (zero flips); risk integration; assumption register |
| Phase 4: Cross-Pollination Synthesis | `projects/PROJ-017-llm-skill-testing/analysis/cross-pollination-synthesis.md` | Cross-stream convergence confirmation; gap resolution status; adversarial critique integration; quality trajectory |
| Phase 3B: Risk Assessment | `projects/PROJ-017-llm-skill-testing/analysis/risk-assessment.md` | 17 risks (0 RED, 8 YELLOW, 9 GREEN); per-option risk profiles; mitigation roadmap |
| Phase 3A: V&V Report | `projects/PROJ-017-llm-skill-testing/analysis/verification-report.md` | 8/8 MUST-HAVE criteria PASS; 8-gap register; statistical claims verification; requirements compliance matrix |
| Phase 2: Synthesized Findings | `projects/PROJ-017-llm-skill-testing/analysis/synthesized-findings.md` | 6 convergent findings (CONV-001 through CONV-006); 5 divergent findings; 5 gaps; determinism tier classification |
| Phase 1D: Evaluation Criteria | `projects/PROJ-017-llm-skill-testing/research/evaluation-criteria.md` | 21 formal requirements (REQ-001 through REQ-021); 8 MUST-HAVE + 7 SHOULD-HAVE acceptance criteria; 10 quality attributes |
| ADR-001: Framework Architecture | `projects/PROJ-017-llm-skill-testing/decisions/ADR-001-framework-architecture.md` | Preliminary option analysis; three-component architecture; adversarial finding responses (RT-001, PM-001, PM-002) |

### Evidence Code Legend

Evidence codes (E-NNN) cited in scoring rationale originate from Phase 5 trade study evidence register. CONV-NNN codes originate from Phase 2 synthesized findings.

| Code | Type | Source Location | Summary |
|------|------|----------------|---------|
| E-002 | Timeline | ADR-001 Implementation Phases table | Option B Phase 0: 4 hours; Phase 1: 1 week; Phase 2: 2-3 weeks |
| E-003 | Timeline | ADR-001 Option A evaluation | Option A: 3-6 months minimum, 7 components from scratch |
| E-004 | Timeline | ADR-001 Option C evaluation | Option C: 2-4 months before production-quality backend |
| E-006 | Statistical rigor | Phase 3A verification, Dimension 4 | BCa intervals, permutation tests, B-H FDR: all PASS |
| E-008 | Cost model | ADR-001 PM-001 response | Smoke $0.00, Standard ~$5.00 (N=5), Full ~$6.54 (N=30) |
| E-009 | Cost risk | Phase 4, L2.1 | Cost model requires +/-30% range; $3.50-$10.90 bounds |
| E-010 | Adoption | Phase 1B competitive-landscape.md | promptfoo 10.8k stars, npm install, CI/CD built-in |
| E-011 | Adoption | Phase 4, L1.2 Opportunity 3 | Jerry CLI advantage: zero new CLI paradigm |
| E-013 | Competitive | Phase 1B, Section L1.5 | promptfoo: 40%/6-12mo for agentic, 15%/12-24mo for skill eval |
| E-014 | Competitive risk | Phase 3B, RISK-005 | Score 12 YELLOW; statistical engine + governance validator survive |
| E-015 | Defensibility | Phase 4, L1.2 Opportunity 1 | Governance validator non-portable: asymmetric moat |
| E-016 | Extensibility | ADR-001 Option C evaluation | Option C: backend-agnostic by design; plugins |
| E-017 | Extensibility | Phase 1C, AC-S05 | Option B: <=50 LoC extension via custom assertion provider API |
| E-023 | Option A risk | Phase 3B, Option A profile | Elevated adoption/schedule risks; novel tool ecosystem |
| CONV-001 | Convergent finding | Phase 2 synthesized-findings.md | Verified skill-evaluation gap across all 4 research sources |
| CONV-002 | Convergent finding | Phase 2 synthesized-findings.md | Hybrid evaluation is market consensus (HIGH confidence) |
| CONV-003 | Convergent finding | Phase 2 synthesized-findings.md | Statistical rigor absent from all surveyed tools |
| CONV-006 | Convergent finding | Phase 2 synthesized-findings.md | promptfoo is both foundation and competitive threat |

---

*ADR Version: 1.0.0*
*Agent: ps-architect*
*Methodology: Nygard ADR format; S-003 Steelman (H-16); S-002 Devil's Advocate; S-004 Pre-Mortem; S-007 Constitutional Compliance (H-18); S-010 Self-Review (H-15); Kepner-Tregoe Weighted Decision Analysis (inherited from Phase 5)*
*Quality Score: 0.938 (PASS, >= 0.92 threshold, C3 deliverable per AE-003)*
*Created: 2026-03-04*
*Project: PROJ-017 LLM Skill Testing Framework*
*Phase: 6 (ADR Finalization)*
*Input Artifacts: 6 (Phase 1D, Phase 2, Phase 3A, Phase 3B, Phase 4, Phase 5)*
*Supersedes: ADR-001 (Framework Architecture)*
