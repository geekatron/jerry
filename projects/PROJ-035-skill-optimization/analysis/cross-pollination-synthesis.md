# Cross-Pollination Synthesis: LLM Prompt Test Harness

> Phase 3 synthesis artifact for PROJ-035 FEAT-035-001. Combines all four Phase 1 research outputs to identify convergence patterns, gaps, and the optimal combination of approaches for building a prompt regression test harness.

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | 5-7 bullet cross-stream findings for non-technical stakeholders |
| [L1: Technical Synthesis](#l1-technical-synthesis) | All 6 synthesis tasks with tables, matrices, and gap analysis |
| [L1.1: Historical-to-LLM Methodology Mapping](#l11-historical-to-llm-methodology-mapping) | Task 1: classical methods → current frameworks and innovations |
| [L1.2: Framework Capability Matrix](#l12-framework-capability-matrix) | Task 2: side-by-side evaluation needs coverage |
| [L1.3: SDK Testing Gap Analysis](#l13-sdk-testing-gap-analysis) | Task 3: what Agent SDKs are missing for prompt regression |
| [L1.4: Innovation Readiness Assessment](#l14-innovation-readiness-assessment) | Task 4: production-ready vs. experimental with evidence |
| [L1.5: Convergence Patterns](#l15-convergence-patterns) | Task 5: themes appearing across 3+ research streams |
| [L2: Strategic Synthesis](#l2-strategic-synthesis) | Task 6: optimal combination recommendation with evidence tracing |
| [Source Summary](#source-summary) | All sources with contribution summary |

---

## L0: Executive Summary

- **The oracle problem is the central challenge, and it has a known solution.** Classical testing literature identified this problem 25+ years ago -- when there is no single "correct" expected output, traditional assertions break down. Metamorphic testing (Chen, 1998) and property-based testing (Claessen & Hughes, 2000) were invented specifically to address this. The 2024-2025 LLM testing research community has independently converged on exactly these two approaches: LLMORPH implemented 36 metamorphic relations across 560,000 automated LLM tests, and agentic property-based testing achieved a 56% valid bug rate across 100 Python packages. [Sources: 1A, 1D]

- **No existing Agent SDK provides what PROJ-035 needs.** Every evaluated SDK (LangGraph, CrewAI, OpenAI Agents SDK, Google ADK, Microsoft Agent Framework, Pydantic AI, Strands Agents) focuses on evaluating whether agent outputs are currently good -- not whether a prompt change caused a regression. This specific gap -- prompt version comparison with regression detection -- is universally absent. It is the novel contribution the harness must make. [Source: 1C]

- **The best combination already exists in open-source tools, but no one has wired them together for prompt regression.** promptfoo (MIT, 10.8K stars) provides CI/CD-native regression detection with GitHub Action PR comments. DeepEval (Apache 2.0, 14K stars) provides 50+ pytest-compatible evaluation metrics. Neither alone is sufficient; both together cover the regression detection plus quality measurement gap. [Source: 1B]

- **LLM-as-a-Judge is production-ready but requires debiasing to be trustworthy.** The innovation research documents 80-87% correlation with human evaluation -- but only when combined with position randomization, rubric shuffling, and ensemble calibration techniques. Vanilla LLM-as-Judge (which Jerry's S-014 currently implements) introduces systematic bias that can invalidate comparison across prompt versions. [Source: 1D]

- **Statistical rigor is absent from current LLM evaluation practice and this gap is critical for regression testing.** CLT-based point estimates (the current norm, including Jerry's >= 0.92 threshold) dramatically underestimate uncertainty with fewer than several hundred data points. For regression testing -- where the question is "did quality change significantly?" rather than "is quality above threshold?" -- proper hypothesis tests (Wilson score intervals, Wilcoxon signed-rank, Fisher exact) are required to avoid false regression alarms and missed regressions. Note: this CLT limitation applies specifically to small evaluation sets (N < 100), which is the typical context for per-PR regression testing; the threshold concern does not apply to evaluation regimes with several hundred or more samples. [Source: 1D]

- **Six convergence patterns emerge across the research streams, with varying breadth:** (1) the oracle problem and property-based solutions (all four streams: 1A, 1B, 1C, 1D), (2) pytest as the integration backbone (1B, 1C, 1D), (3) LLM-as-Judge as the adopted evaluation mechanism (1B, 1C, 1D), (4) CI/CD gate as the required delivery format (1B, 1C, 1D), (5) declarative test case configuration over imperative code (1B, 1C, 1D), and (6) statistical rigor universally absent from current practice (1A, 1D). These are not opinions -- they emerge independently from historical methodology research, current framework adoption data, SDK gap analysis, and innovation literature. [Sources: 1A, 1B, 1C, 1D]

- **The optimal harness combines four layers:** (1) promptfoo declarative YAML for test case definition and CI/CD regression gates, (2) DeepEval pytest-compatible metrics as the scoring backend, (3) metamorphic relations for oracle-problem-safe assertions, and (4) statistical hypothesis testing (Wilson/Wilcoxon) instead of point-estimate thresholds. This combination is evidence-derived from findings across all four Phase 1 streams.

---

## L1: Technical Synthesis

### L1.1: Historical-to-LLM Methodology Mapping

**Approach:** This mapping uses the LLM applicability ratings and current-implementation cross-references documented in Stream 1A (historical-testing-methodologies.md), then traces each method to the frameworks (1B) and innovations (1D) that implement it. No new analogies are introduced.

#### HIGH applicability methods and their LLM framework implementations

| Classical Methodology | 1A Applicability | What Implements It | Where Found |
|----------------------|------------------|--------------------|-------------|
| **Metamorphic Testing** (Chen, 1998) | HIGHEST | LLMORPH (ASE 2025): 36 MRs, 560K tests. Giskard incorporates MT principles. | 1D Innovation #2; 1B Giskard |
| **Property-Based Testing** (Claessen & Hughes, 2000) | HIGH | Hypothesis library (BSD): used by agentic PBT research. DeepEval's custom metric framework supports invariant specification. | 1D Innovation #4; 1B DeepEval |
| **Mutation Testing** (DeMillo et al., 1978) | HIGH | promptfoo: tests across multiple prompt variants to verify test suite sensitivity. Manual prompt mutation patterns documented in 1A but no framework implements full mutation scoring. | 1B promptfoo (partial); 1A identified gap |
| **Design by Contract** (Meyer, 1986) | HIGH | DeepEval assertion system: preconditions (input format checks), postconditions (output constraint metrics). Google ADK `.test.json` expected tool trajectory = contract specification. | 1B DeepEval, 1C Google ADK |
| **Behavior-Driven Development** (North, 2003) | MEDIUM-HIGH | pytest-bdd (Jerry's current H-20 standard). DeepEval test cases follow Given/When/Then-compatible structure. promptfoo YAML configs are BDD-adjacent. | 1B pytest, DeepEval, promptfoo |
| **Fuzz Testing** (Miller, 1988) | MEDIUM-HIGH | promptfoo red teaming: 40+ attack types as structured adversarial prompt injection. Giskard vulnerability scanning: automated adversarial test generation. | 1B promptfoo, Giskard |
| **Exploratory Testing** (Kaner, 1984) | MEDIUM-HIGH | No current framework formalizes this for LLMs. The 1A finding stands: no Session-Based Test Management equivalent exists for LLM prompts. | 1A identified gap |

#### MEDIUM applicability methods with partial implementations

| Classical Methodology | 1A Applicability | Current Implementation Status |
|----------------------|------------------|-------------------------------|
| **Equivalence Partitioning** (Myers, 1979) | MEDIUM | DeepEval `@pytest.mark.parametrize` enables partition testing. promptfoo test case variables serve as partition representatives. No tool automatically partitions the prompt input space. |
| **Model-Based Testing** (Chow, mid-1970s) | MEDIUM | Google ADK `.evalset.json` for multi-turn conversation flows approaches MBT for structured interactions. Strands User Simulator similarly. |
| **TDD** (Beck, 1994-2003) | LOW-MEDIUM | Conceptually present in DeepEval (write failing test, modify prompt, verify pass) but the non-determinism problem 1A identified remains: no framework solves the "Green" step deterministically. |

#### Gap identified in 1A that no framework closes

**Non-Determinism Gap** (1A L2: Identified Gaps #2): The most critical gap is the absence of statistical assertion frameworks. Every classical methodology assumes deterministic outputs. LLM outputs are stochastic. The 1D research directly addresses this via Innovation #6 (Statistical Rigor / CLT Alternatives) and Innovation #3 (PPI), but no currently surveyed framework in 1B implements these methods. This is the primary gap the harness must fill.

---

### L1.2: Framework Capability Matrix

**Source:** 1B industry-frameworks-survey.md (L1C Capability Comparison Matrix, L2 Strategic Assessment). All scores and ratings are from the 1B research findings.

#### LLM/AI Framework Coverage Matrix (from 1B)

| Evaluation Need | promptfoo | DeepEval | Langfuse | Opik | RAGAS | lm-eval-harness | Giskard |
|-----------------|-----------|----------|----------|------|-------|-----------------|---------|
| **Regression testing** | VERY HIGH (before/after PR diff, GitHub Action) | VERY HIGH (pytest-native, metrics library) | HIGH (prompt versioning, dataset evals) | HIGH (experiment tracking) | MED-HIGH (RAG-specific) | MEDIUM (task comparison) | HIGH (vulnerability regression) |
| **Behavioral evaluation** | HIGH (assertion types: exact, contains, LLM-graded, JS/Python) | HIGH (G-Eval, custom criteria) | MEDIUM (LLM-as-judge via API) | HIGH (built-in + custom) | MEDIUM (RAG behaviors) | LOW (benchmark-oriented) | HIGH (bias, safety behaviors) |
| **Statistical rigor** | LOW (assertions are binary; no confidence intervals) | LOW (point-estimate thresholds) | LOW (custom only) | LOW (custom only) | LOW | MEDIUM (benchmark statistics) | LOW |
| **CI/CD integration** | VERY HIGH (native GitHub Action, PR comments) | HIGH (pytest plugin, any CI) | MEDIUM (API-driven) | HIGH (pytest plugin) | MEDIUM (script-based) | HIGH (CLI-based) | MEDIUM (script-based) |
| **Determinism control** | MEDIUM (caching; no statistical aggregation) | MEDIUM (threshold per metric; no aggregation) | LOW | LOW | LOW | MEDIUM | LOW |
| **Multi-model support** | VERY HIGH (OpenAI, Anthropic, Azure, Bedrock, Ollama, 100+ providers) | HIGH (multi-provider) | HIGH (via integrations) | HIGH (70+ integrations) | MEDIUM | VERY HIGH (HF, vLLM, SGLang, APIs) | MEDIUM |

**Critical observation from 1B L2:** "The convergence point for LLM prompt regression testing lies at the intersection of promptfoo's CI/CD-native design and DeepEval's pytest-compatible metric system." No single framework is complete. The gap universally absent from the matrix is the statistical rigor row -- all frameworks use point estimates, not confidence intervals or hypothesis tests.

#### Traditional Framework Contribution (from 1B)

| Framework | Contribution to Prompt Regression Harness |
|-----------|------------------------------------------|
| **pytest** | Test runner backbone. DeepEval, Opik, Google ADK all integrate via pytest. Jerry already uses this (H-20). HIGH compatibility. |
| **Jest/Vitest** | Alternative backbone for TypeScript prompt tests. Snapshot testing paradigm (capture/compare) conceptually maps to prompt regression. MEDIUM fit; not Jerry's existing stack. |
| **Playwright/Cypress/Selenium** | Not applicable to LLM output evaluation. Only useful for E2E testing of LLM-powered UIs. |

---

### L1.3: SDK Testing Gap Analysis

**Source:** 1C agent-sdk-evaluation.md (L2 Gap Analysis). Cross-referenced against 1A and 1B needs.

#### The central gap finding (from 1C)

"No evaluated SDK provides native prompt regression testing capabilities." (1C L0: Executive Summary) The critical question -- "Did this prompt change cause a regression in output quality across a defined test suite?" -- is answered by zero of the seven evaluated SDKs.

#### Five specific gaps identified in 1C, cross-referenced to 1A and 1B needs

| Gap (1C) | Description | Cross-Reference to Testing Need |
|----------|-------------|--------------------------------|
| **Gap 1: Prompt Version Management** | No SDK tracks prompt versions, maintains a prompt changelog, or supports comparing outputs between versions. | 1A: Mutation testing requires knowing what changed. 1B: promptfoo's "before/after diff" partially addresses this but requires external git integration. |
| **Gap 2: Regression Comparison Logic** | Closest capability is snapshot testing (Pydantic AI with `inline-snapshot`, Strands with `.to_file()`), but these capture point-in-time output without version comparison workflow. No SDK provides: automatic baseline capture, side-by-side version N vs. N+1 comparison, or regression severity classification. | 1A: This is the oracle problem applied to regression: "How do I know if quality degraded?" 1D: PPI (Innovation #3) would provide the statistical framework to answer this. |
| **Gap 3: Non-Determinism-Aware Assertions** | Only Google ADK and Strands acknowledge non-determinism. ADK uses ROUGE-1 similarity; Strands uses LLM-as-Judge with statistical baselines. No SDK provides: combined similarity + LLM-judge + statistical testing as a unified regression assertion. | 1A: Non-Determinism Gap directly corresponds. 1D: Innovation #6 (CLT Alternatives) provides the statistical methods. |
| **Gap 4: CI/CD Prompt Regression Gates** | Google ADK comes closest: pytest bridge that blocks deployment when absolute quality drops. Gap: no relative regression gate (compare PR vs. main branch baseline). | 1B: promptfoo's GitHub Action provides relative before/after comparison -- this is the bridge between the ADK pattern and the regression gate. |
| **Gap 5: Test Case Generation from Prompt Changes** | Strands `ExperimentGenerator` creates test suites from context descriptions, but not in response to specific prompt modifications. | 1D: Innovation #11 (Prompt Perturbation Testing) maps to this; 1D Innovation #4 (Agentic PBT) could generate tests from prompt changes. |

#### SDK capability map against 1A methodologies

| SDK Capability | Best SDK Example | 1A Methodology It Approximates | Gap |
|----------------|------------------|---------------------------------|-----|
| Test model / deterministic mock | Pydantic AI `TestModel` | TDD (Red-Green-Refactor): enables deterministic "Green" step | Gap: TestModel bypasses LLM entirely; cannot test actual prompt quality |
| Evaluation framework | Google ADK (6+ evaluators), Strands (7+ evaluators) | Property-based testing: invariant specification per evaluator | Gap: evaluators test output quality, not regression from a baseline |
| Trajectory testing | Google ADK `tool_trajectory_avg_score`, Pydantic AI `capture_run_messages()` | Design by Contract: postcondition verification of tool call sequence | Gap: no version comparison; only absolute compliance |
| Tracing | OpenAI Agents SDK (comprehensive), Strands (OpenTelemetry) | Exploratory testing: captures what happened | Gap: tracing is data capture, not comparison logic |
| Auto test generation | Strands `ExperimentGenerator` | Model-based testing: automated test derivation | Gap: generates from context, not from prompt changes |

#### Architectural recommendations from 1C

1C L2 recommends the harness adopt the following SDK-derived patterns as design inspiration (not as direct dependencies):
- **Pydantic AI patterns:** `TestModel`, `FunctionModel`, `ALLOW_MODEL_REQUESTS`, `Agent.override()` -- the best-in-class testing ergonomics model.
- **Google ADK evaluation format:** `.test.json`, `.evalset.json` as structured test case definition patterns.
- **Strands Evals extensibility:** The base `Evaluator` class pattern with custom evaluators.
- **OpenTelemetry tracing:** Supported by Strands, Microsoft Agent Framework, and adapters for most SDKs -- the common data format for execution capture.

---

### L1.4: Innovation Readiness Assessment

**Source:** 1D innovation-frameworks.md (L2 Strategic Assessment, Maturity Assessment Matrix). All maturity classifications and evidence cited are from 1D research findings.

#### Production-Ready Innovations (immediate integration candidates)

| Innovation (1D #) | Maturity Evidence (from 1D) | Feasibility for PROJ-035 | Integration Path |
|-------------------|----------------------------|--------------------------|-----------------|
| **#1: LLM-as-Judge with Debiasing** | 80-87% human correlation; multiple production frameworks (1D cites Zheng et al., 2023, "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena"; Wang et al., 2023, "Large Language Models are not Fair Evaluators"); ACL, NeurIPS published debiasing techniques | HIGH | Add position randomization and rubric shuffling to harness evaluation pipeline. Jerry's S-014 already implements vanilla LLM-as-Judge; debiasing is an enhancement, not a replacement. |
| **#7: Chain-of-Verification (CoVe)** | ACL 2024 published (Dhuliawala et al., 2024, "Chain-of-Verification Reduces Hallucination in Large Language Models"); 50-70% hallucination reduction; CISC (ACL 2025, "Concise Chain-of-Verification") reduces required paths by 40% | HIGH | Jerry already has S-011 in its strategy catalog. CoVe implementation requires context isolation for verification questions -- consistent with Jerry's FC-M-001 (Fresh Context Reviewer). |
| **#8: Open-Source Eval Frameworks** | promptfoo 10.8K stars, MIT (github.com/promptfoo/promptfoo); DeepEval 14K stars, Apache 2.0 (github.com/confident-ai/deepeval); Langfuse 22.7K stars, MIT (github.com/langfuse/langfuse) | VERY HIGH | These are the direct tools for the harness. OSI-licensed, pytest-compatible, CI/CD-integrated. |
| **#6: Statistical Rigor (CLT Alternatives)** | ICML 2025 position paper (Baan et al., "Stop! In the Name of Flawed Evaluation: Revisiting the Metric Zoo for Language Generation"); ICLR 2025 blogpost on evaluation confidence; Python library released (1D cites `lm-evaluation-harness` statistical extensions) | HIGH | Replace Jerry's point-estimate threshold (>= 0.92) with Wilson score intervals for regression comparison. Straightforward Python implementation. |

#### Emerging Innovations (next quarter prototyping candidates)

| Innovation (1D #) | Maturity Evidence (from 1D) | What Needs Adaptation | Risk Level |
|-------------------|-----------------------------|----------------------|------------|
| **#2: Metamorphic Testing** | ASE 2025 peer-reviewed (LLMORPH: "Metamorphic Testing of Large Language Models"); ICSME 2025 NLP study; Giskard OSS incorporates MT principles (github.com/Giskard-AI/giskard) | Define Jerry-specific metamorphic relations (e.g., "paraphrasing a system prompt should not change quality score by more than +/- 0.05") | LOW -- well-understood theory, high-value for oracle problem |
| **#3: Prediction-Powered Inference (PPI)** | Published in Science (2023, Angelopoulos et al., "Prediction-Powered Inference"); NeurIPS 2024 Stratified PPI extension (Angelopoulos et al., 2024) | Build calibration dataset of human-scored Jerry outputs | MEDIUM -- requires human annotation effort |
| **#11: Prompt Perturbation Testing** | Multiple 2025 papers; partially implemented in promptfoo red teaming module (promptfoo.dev/docs/red-team); 10-40% accuracy degradation under perturbation documented across studies | Build perturbation generator for agent definitions | LOW -- existing frameworks available |

#### Experimental Innovations (watch and evaluate)

| Innovation (1D #) | Maturity Evidence | Blocker | Watch Condition |
|-------------------|-------------------|---------|-----------------|
| **#4: Agentic Property-Based Testing** | arXiv preprint (2510.09907, "Automated Property-Based Testing of LLM-powered Agents"); 56% valid bug rate; $9.93/bug | Requires Claude Opus API; cost may not scale for CI | When Jerry's codebase grows beyond current test coverage |
| **#5: Creative Adversarial Testing (CAT)** | KDD 2025 Workshop paper; validated on synthetic data only | Only synthetic validation; real-world fidelity unknown | When multi-goal orchestration evaluation is needed |
| **#9: LLM Observability/Drift** | Langfuse 22.7K stars; production-ready platform (github.com/langfuse/langfuse, MIT license) | Jerry is CLI-only (no persistent service) | When Jerry adds session-level analytics |
| **#10: Chatbot Arena / Bradley-Terry** | 240K+ votes (LMSYS Chatbot Arena, Chiang et al., 2024, "Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference"); very high statistical rigor | Requires pairwise comparison infrastructure; crowdsourcing not applicable | When multiple agent definition versions need ranking |

---

### L1.5: Convergence Patterns

Patterns identified as appearing across 3 or more independent research streams (1A, 1B, 1C, 1D). The threshold of 3 out of 4 streams was chosen because it requires independent corroboration from a majority of sources: a theme appearing in only 1 or 2 streams could reflect a single research community's bias or a framework vendor's positioning, whereas appearance in 3 or more streams indicates convergence across distinct methodological traditions (historical analysis, current framework adoption, SDK evaluation, and innovation research). PAT-006 (Statistical Rigor Absent) is the only pattern that meets only 2-stream explicit citation; it is included because its implicit presence across all four streams is documented in its entry and its critical relevance to the synthesis task warrants explicit identification despite lower citation breadth.

#### PAT-001: The Oracle Problem Dominates LLM Testing

**Appears in:** 1A, 1B, 1C, 1D (all four streams)

| Stream | How It Appears |
|--------|---------------|
| 1A (Historical) | "The oracle problem -- the inability to specify exact expected outputs -- is the central challenge for LLM prompt testing." (1A L2: Identified Gaps #1). Metamorphic testing and PBT were invented for this. |
| 1B (Frameworks) | Every LLM framework uses either LLM-as-Judge or similarity scoring instead of exact assertions, precisely because exact oracles are impossible. |
| 1C (SDKs) | "Gap 3: Non-Determinism-Aware Assertions" -- all SDKs struggle with the same problem; Google ADK and Strands use ROUGE-1 and LLM-Judge as substitutes. |
| 1D (Innovations) | Innovation #2 (Metamorphic Testing) is explicitly motivated as "solving the oracle problem" for LLMs. Innovation #3 (PPI) provides statistical rigor in the absence of a ground truth oracle. |

**Implication:** The harness must not require exact expected outputs. Assertions must be property-based (constraints), metamorphic (relational), or statistical.

---

#### PAT-002: pytest as the Convergence Point for Python LLM Testing

**Appears in:** 1A (implied), 1B, 1C, 1D (three explicit streams)

| Stream | How It Appears |
|--------|---------------|
| 1B (Frameworks) | pytest: "504M+ monthly PyPI downloads; 12,500+ enterprise users." DeepEval is a pytest plugin. Opik has pytest integration. (1B L1A #5, L2 Tier 3) |
| 1C (SDKs) | Google ADK: "Native pytest integration for CI/CD pipelines." (1C L1.4). Pydantic AI: "Designed for standard pytest workflows with `pytest.mark.anyio`." (1C L1.6). Strands: "Pytest-compatible through standard Python test patterns." (1C L1.7) |
| 1D (Innovations) | DeepEval (Innovation #8): "pytest-compatible LLM unit testing; deepeval test run works like pytest." (1D Innovation #8). Google ADK codelab uses pytest bridge for CI/CD. |

**Implication:** pytest is the de facto standard integration point. The harness must be pytest-native, not pytest-adjacent.

---

#### PAT-003: LLM-as-Judge is the Adopted Evaluation Mechanism

**Appears in:** 1B, 1C, 1D (three explicit streams, implicit in 1A's discussion of evaluation metrics gap)

| Stream | How It Appears |
|--------|---------------|
| 1B (Frameworks) | All 7 LLM frameworks support LLM-as-Judge. DeepEval's G-Eval, promptfoo's LLM-graded assertions, Langfuse's LLM-as-judge, Opik built-in, RAGAS metrics, lm-eval (task-based), Giskard adversarial. (1B L1B, L1C Key Metrics table) |
| 1C (SDKs) | Google ADK: `final_response_match_v2` (LLM-judged semantic match). Strands: "Built-in LLM-as-a-Judge scoring via Amazon Bedrock Claude 4." (1C L1.4, L1.7) |
| 1D (Innovations) | Innovation #1 (LLM-as-Judge Debiasing) documents the maturity and limitations of the approach; 80-87% correlation. Critically: "vanilla LLM-as-judge works fine for cheap filtering and initial screening, but cannot replace human expert verification for high-stakes evaluation." (1D Innovation #1) |

**Tension Identified:** LLM-as-Judge is universally adopted but universally applied without the debiasing techniques that 1D documents as required for reliability. The harness must implement debiasing as a first-class concern, not an afterthought.

---

#### PAT-004: CI/CD Gate is the Required Delivery Format

**Appears in:** 1B, 1C, 1D (three explicit streams)

| Stream | How It Appears |
|--------|---------------|
| 1B (Frameworks) | promptfoo's GitHub Action for PR-triggered evaluation with before/after comments is the standout CI/CD feature. DeepEval: "Integrates with any CI/CD environment via pytest." (1B L1B #1, #2) |
| 1C (SDKs) | Google ADK: "pytest bridge: CI/CD runner invokes pytest, which calls the ADK evaluator, which blocks deployment if the agent degrades." (1C L1.4). 1C Gap #4: "No SDK provides: a GitHub Action that detects prompt file changes in a PR and triggers regression tests." |
| 1D (Innovations) | Innovation #8: "promptfoo: CLI-first, declarative YAML configs, CI/CD native (GitHub Actions)." (1D Innovation #8 Framework table). |

**Implication:** The harness must ship with a GitHub Action as a first-class deliverable. Local testing is insufficient -- the regression gate must fire automatically on prompt changes in PRs.

---

#### PAT-005: Declarative Test Case Configuration Fits Prompt Testing Better than Imperative Code

**Appears in:** 1B, 1C, 1D (three streams)

| Stream | How It Appears |
|--------|---------------|
| 1B (Frameworks) | promptfoo's YAML declarative config: "Declarative YAML test configuration (prompts + test cases + assertions). Side-by-side model comparison." (1B L1B #1). lm-evaluation-harness: "YAML-based task configuration with Jinja2 templating." (1B L1B #6) |
| 1C (SDKs) | Google ADK `.test.json` and `.evalset.json` formats: structured test case definitions. 1C recommends "Use Google ADK's evaluation approach as a reference for structured test case formats." (1C L2 Architectural Recommendations) |
| 1D (Innovations) | DeepEval (Innovation #8) provides both pytest imperative and declarative patterns. promptfoo YAML: "prompts, providers, tests vars, assert type." (1D Innovation #8 code example) |

**Implication:** Test cases should be defined as YAML/JSON files version-controlled alongside prompt files -- not as Python test functions. This enables non-Python users to contribute tests and enables clean before/after diffing of test case evolution.

---

#### PAT-006: Statistical Rigor is Universally Absent

**Appears in:** 1A, 1D (two streams -- but with critical relevance to all four)

| Stream | How It Appears |
|--------|---------------|
| 1A (Historical) | "Evaluation Metric Gap: Classical testing uses binary pass/fail oracles. LLM output quality is multi-dimensional." (1A L2 Identified Gaps #4). "Non-Determinism Gap: Most classical methodologies assume deterministic execution. Adapting them requires distributional checks." (1A L2 Identified Gaps #2) |
| 1D (Innovations) | Innovation #6: "CLT-based methods perform very poorly, usually dramatically underestimating uncertainty." (1D Innovation #6). Wilson score intervals, Wilcoxon signed-rank, Fisher exact tests are the evidence-based alternatives. |

**Note:** While only two streams explicitly identify this as a gap, it is implicitly present across all four. The 1B matrix shows no framework provides confidence intervals. The 1C SDK matrix shows no SDK provides statistical significance testing. The harness must fill this gap regardless of which other components it adopts.

---

## L2: Strategic Synthesis

### Task 6: Optimal Combination Recommendation

**Evidence-based derivation:** This recommendation traces every design decision to specific findings in the Phase 1 research. No decision is introduced without a source.

#### The Four-Layer Architecture

```
Layer 1: Test Case Definition (CI/CD-native, declarative)
    promptfoo YAML + custom Python validators
    Source: 1B (promptfoo VERY HIGH regression fit, GitHub Action),
            1C (Google ADK .test.json format as design reference),
            PAT-005 (declarative config convergence)

Layer 2: Evaluation Backend (pytest-native, extensible metrics)
    DeepEval pytest plugin + custom evaluators
    Source: 1B (DeepEval VERY HIGH regression fit, 50+ metrics, G-Eval),
            1C (Pydantic AI patterns: TestModel, ALLOW_MODEL_REQUESTS),
            PAT-002 (pytest convergence)

Layer 3: Oracle-Safe Assertions (metamorphic + property-based)
    Metamorphic relations (paraphrase, negation, perturbation invariants)
    Source: 1A (Metamorphic Testing HIGHEST applicability),
            1D (Innovation #2: LLMORPH, Giskard MT principles),
            PAT-001 (oracle problem dominance)

Layer 4: Statistical Comparison Engine (regression-specific)
    Wilson score intervals + Wilcoxon signed-rank test
    Source: 1D (Innovation #6: CLT Alternatives, ICML/ICLR 2025),
            PAT-006 (statistical rigor universally absent),
            1C (Gap 3: non-determinism-aware assertions)
```

#### What the Harness Adds That Does Not Exist (the novel contribution)

From 1C Gap #2: "Regression Comparison Logic is the core value proposition of the harness. The comparison logic is the novel contribution." The following table shows what exists today vs. what the harness must build:

| Component | What Exists (source) | What the Harness Adds |
|-----------|---------------------|----------------------|
| Test case execution | promptfoo, DeepEval (1B) | Prompt version tagging for each test run |
| Quality measurement | G-Eval, DeepEval metrics, ROUGE-1 (1B, 1C) | Statistical comparison of metric scores across versions using Wilcoxon/Wilson |
| CI/CD integration | promptfoo GitHub Action (1B) | Git-diff-triggered test selection (only re-run tests affected by changed prompts) |
| Assertion types | Binary assertions, LLM-judge (1B) | Metamorphic relation assertions (consistency between related prompt pairs) |
| Debiasing | Not implemented in any framework (1D gap) | Position randomization + rubric shuffling per 1D Innovation #1 |
| Snapshot baseline | Pydantic AI `inline-snapshot`, Strands `.to_file()` (1C) | Version-keyed baseline store with statistical drift detection |

#### Component Selection Justification (with source traces)

**Component 1: promptfoo as CI/CD layer**

Justification:
- "Purpose-built for this exact use case [prompt regression]." (1B L1B #1)
- "GitHub Action enables automated regression checks on prompt changes. The 'before/after' PR comparison directly supports regression detection." (1B L1B #1)
- "VERY HIGH" regression testing suitability score in 1B capability matrix. (1B L1C)
- CI/CD integration pattern identified as convergence theme across 1B, 1C, 1D. (PAT-004)

Counter-argument addressed: promptfoo is TypeScript-native, not Python. 1B L2 addresses this: "A hybrid approach (promptfoo for CI gates, DeepEval for in-depth metric evaluation) is architecturally viable." (1B L2)

**Component 2: DeepEval as evaluation metric backend**

Justification:
- "pytest-native (aligns with Jerry's Python infrastructure); 50+ research-backed metrics; most comprehensive evaluation coverage." (1B L2 Tier 1 table)
- DeepEval's G-Eval enables custom evaluation criteria matching Jerry's prompt quality needs. (1B L1B #2)
- "Synthetic dataset generation supports systematic regression test creation." (1B L1B #2)
- Jerry already uses pytest (H-20 BDD test-first), so DeepEval's pytest plugin creates zero new infrastructure. (1B L2 #1)

**Component 3: Metamorphic relations as oracle-safe assertions**

Justification:
- "Metamorphic testing is the single most applicable classical methodology to LLM prompt testing" because LLMs present the oracle problem by definition. (1A #9 LLM Applicability)
- Active 2024-2025 research: "LLMORPH implements 36 metamorphic relations for LLM testing; metamorphic prompt testing detected 75% of erroneous GPT-4 programs with 8.6% false positive rate." (1A #9)
- 1D Innovation #2: MEDIUM-HIGH integration feasibility for Jerry. "Requires defining domain-specific metamorphic relations for agent outputs." (1D Innovation #2)
- Example Jerry-specific metamorphic relations (from 1D Integration Feasibility):
  - "If the system prompt is paraphrased, quality score should remain within +/- 0.05"
  - "If the user prompt is translated to another language and back, factual content should be preserved"
  - "If irrelevant context is appended to the prompt, the output should not change substantively"

**Component 4: Statistical hypothesis testing for regression comparison**

Justification:
- "CLT-based methods perform very poorly, usually dramatically underestimating uncertainty (i.e., producing error bars that are too small) in small-data contexts." (1D Innovation #6, citing ICML 2025)
- For regression testing specifically, the question is "did quality change significantly?" -- a hypothesis test, not a threshold comparison. Wilcoxon signed-rank is the appropriate test for paired before/after scores. (1D Innovation #6 recommended methods table)
- "Wilson score intervals are straightforward to implement in Python." (1D Innovation #6 Integration Feasibility)
- Jerry's current >= 0.92 threshold is a point estimate with no confidence interval. With typical evaluation sets (N < 100), CLT-based intervals underestimate uncertainty. (1D Innovation #6)

**Component 5: LLM-as-Judge with debiasing (not vanilla)**

Justification:
- LLM-as-Judge is production-ready at 80-87% human correlation (1D Innovation #1) and is the convergent evaluation mechanism across all frameworks (PAT-003).
- However: "vanilla LLM-as-judge works fine for cheap filtering and initial screening, but cannot replace human expert verification for high-stakes evaluation." (1D Innovation #1)
- The specific debiasing techniques required: position randomization, rubric shuffling, ensemble calibration. (1D Innovation #1 Key Debiasing Techniques table)
- "Integration Feasibility for Jerry: HIGH. Jerry already uses S-014 (LLM-as-Judge). The debiasing techniques can be implemented as enhancements to the existing `adv-scorer` agent without architectural changes." (1D Innovation #1)

#### What NOT to include (and why)

| Excluded Component | Reason | Source |
|-------------------|--------|--------|
| Langfuse as primary tool | Langfuse is an observability platform, not a testing tool. "Best used in combination with a dedicated testing tool for structured regression testing." | 1B L1B #3 |
| Google ADK evaluation framework | Google ADK evaluates agent behavior quality, not prompt stability. "No prompt versioning or diff capabilities." | 1C L1.4 Gaps |
| Agentic PBT (Innovation #4) | "Experimental. Requires Claude Opus API access; cost per bug may be high." | 1D L2 Experimental table |
| CLT-based point estimates | "CLT dramatically underestimates uncertainty in small-data contexts" -- the exact context of per-PR regression testing. | 1D Innovation #6 |
| Crowdsourced BT models (Innovation #10) | "Integration Feasibility for Jerry: LOW-MEDIUM. Jerry's single-user context makes crowdsourced evaluation impractical." | 1D Innovation #10 |

#### Integration Architecture Summary

```
PROMPT CHANGE (git diff detects modified agent definition file)
    |
    v
promptfoo GitHub Action (triggers on PR)
    |
    +--> Load test cases from .yaml test suite
    +--> Run prompts against target LLM
    +--> Collect raw outputs
    |
    v
DeepEval Metric Evaluation
    |
    +--> G-Eval with debiased LLM-as-Judge
    |     (position randomization, rubric shuffling)
    +--> Metamorphic relation checks
    |     (paraphrase consistency, negation handling)
    +--> Custom property assertions
    |     (output constraints, format compliance)
    |
    v
Statistical Comparison Engine (novel layer)
    |
    +--> Retrieve baseline scores for this prompt version
    +--> Run Wilcoxon signed-rank test (before vs. after)
    +--> Compute Wilson score intervals
    +--> Classify: NO_REGRESSION | MARGINAL | REGRESSION
    |
    v
CI/CD Gate Decision
    |
    +--> PASS: no statistically significant regression detected
    +--> FAIL: regression detected with confidence interval
    |     (blocks merge; posts detailed report to PR)
    v
Langfuse (optional, observability layer)
    Log prompt version, scores, and comparison results for trend tracking
```

#### Phased Implementation Plan

Based on innovation readiness assessment (1D L2) and gap prioritization (1C L2, 1B L2):

| Phase | Components | Evidence Basis | Estimated Effort |
|-------|-----------|----------------|-----------------|
| **Phase A: Foundation** | pytest + DeepEval + promptfoo integration; basic LLM-as-Judge assertions | 1B convergence finding; PAT-002, PAT-004 | Low (all frameworks have existing integration docs) |
| **Phase B: Statistical layer** | Replace point estimates with Wilson score intervals; Wilcoxon for version comparison | 1D Innovation #6; PAT-006 | Low-Medium (Python stdlib + scipy) |
| **Phase C: Debiasing** | Add position randomization and rubric shuffling to LLM-as-Judge | 1D Innovation #1; PAT-003 | Low (algorithmic; no new dependencies) |
| **Phase D: Metamorphic** | Define Jerry-specific MRs; implement MT assertion type in DeepEval | 1A HIGHEST applicability; 1D Innovation #2; PAT-001 | Medium (domain MR definition is intellectual work) |
| **Phase E: PPI calibration** | Build human annotation calibration dataset; implement bias-corrected intervals | 1D Innovation #3 | High (requires human annotation effort) |

**Effort estimate caveat:** The effort classifications above (Low / Low-Medium / Medium / High) are qualitative estimates derived from framework complexity assessment -- specifically, the number of new dependencies, the amount of custom code required, and the maturity of existing integration documentation as documented in the Phase 1 research. They are not derived from measured implementation data and should be treated as directional guidance rather than planning-grade estimates until a prototype sprint validates them.

---

## Source Summary

| Source | Type | Key Contribution | Patterns Contributed |
|--------|------|------------------|---------------------|
| `research/historical-testing-methodologies.md` (1A) | Historical survey | 12 methodology catalog with LLM applicability ratings; oracle problem and non-determinism gaps formally identified | PAT-001, PAT-006 |
| `research/industry-frameworks-survey.md` (1B) | Framework survey | 14 frameworks (7 traditional, 7 LLM-specific) with capability matrix; promptfoo + DeepEval identified as primary candidates | PAT-002, PAT-003, PAT-004, PAT-005 |
| `research/agent-sdk-evaluation.md` (1C) | SDK evaluation | 7 Agent SDKs evaluated; 5 specific gaps for prompt regression testing documented; Pydantic AI and Google ADK identified as design references | PAT-002, PAT-003, PAT-004 |
| `research/innovation-frameworks.md` (1D) | Innovation survey | 11 innovations cataloged with maturity assessment; LLM-as-Judge debiasing, metamorphic testing, PPI, statistical rigor alternatives documented | PAT-001, PAT-003, PAT-006 |

---

## Self-Review Verification (S-010)

- [x] All 6 synthesis tasks addressed: Tasks 1-6 in L1.1-L1.5 and L2 respectively
- [x] Cross-references trace to specific input artifacts: Every claim cites stream (1A/1B/1C/1D) and section
- [x] No new ungrounded claims introduced: All framework choices, gap identifications, and pattern attributions cite Phase 1 sources
- [x] L0/L1/L2 structure complete: Executive Summary, Technical Synthesis, Strategic Synthesis all present
- [x] Navigation table present: Document Sections table at top
- [x] Capability matrix covers all discovered frameworks: L1.2 covers all 7 LLM frameworks from 1B

---

*Synthesis conducted: 2026-03-06*
*Agent: ps-synthesizer (Phase 3, PROJ-035 FEAT-035-001)*
*Sources synthesized: 4 Phase 1 research documents (1A, 1B, 1C, 1D)*
*Methodology: Thematic analysis (Braun & Clarke, 2006); cross-reference matrix; convergence pattern extraction*
*Confidence: HIGH -- all synthesis claims trace to Phase 1 research findings; no ungrounded claims introduced*
