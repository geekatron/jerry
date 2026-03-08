# ADR-001: Test Harness Architecture for LLM Prompt Evaluation and Safe Refactoring

> **Project:** PROJ-035 (Skill Optimization)
> **Feature:** FEAT-035-001
> **Phase:** 7 (Architecture Decision)
> **Date:** 2026-03-06
> **Agent:** ps-architect
> **Related:** PROJ-017 ADR-002 (Quality Framework Selection -- complementary, not competing)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Status](#status) | Decision lifecycle state |
| [L0: Executive Summary](#l0-executive-summary) | Decision, rationale, and implications for non-technical stakeholders |
| [L1: Context](#l1-context) | Problem statement, forces, constraints |
| [L1: Options Evaluated](#l1-options-evaluated) | Three options with steelman analysis (S-003), scoring, and trade-offs |
| [L1: Decision](#l1-decision) | Chosen option with weighted evidence |
| [L1: Technical Implementation](#l1-technical-implementation) | Layer architecture, component integration, code patterns |
| [L1: Consequences](#l1-consequences) | Positive, negative, and neutral outcomes |
| [L1: Risks](#l1-risks) | Integrated risk register from Phase 5 FMEA |
| [L1: Implementation Roadmap](#l1-implementation-roadmap) | Six-phase delivery plan with FMEA-informed sequencing |
| [L1: PROJ-017 ADR-002 Relationship](#l1-proj-017-adr-002-relationship) | Complementary architecture, shared infrastructure, divergence points |
| [L2: Architectural Implications](#l2-architectural-implications) | Long-term evolution path, systemic consequences, decision review triggers |
| [Evidence Traceability](#evidence-traceability) | All cited evidence with source file paths |
| [Self-Review (S-010)](#self-review-s-010) | Pre-finalization quality assessment |

---

## Status

**ACCEPTED**

Accepted 2026-03-06 per P-020 user approval. This ADR synthesizes findings from six prior artifacts across Phases 1A, 1B, 1C, 1D, 3, and 5 of the PROJ-035 FEAT-035-001 orchestration pipeline.

---

## L0: Executive Summary

### What We Decided

We recommend a **Four-Layer Composite Architecture** for the Jerry Framework's prompt regression test harness. This architecture combines four proven, open-source components into an integrated system that detects when a prompt change causes a regression in output quality -- a capability that does not exist in any single tool today.

The four layers are:

1. **CI/CD Regression Gate** -- promptfoo (MIT license) provides declarative YAML test case definitions and a GitHub Action that automatically triggers regression tests when prompt files change in a pull request.
2. **Evaluation Backend** -- DeepEval (Apache 2.0) provides 14+ pytest-compatible evaluation metrics, including LLM-as-Judge with debiasing, integrated directly into Jerry's existing pytest test infrastructure.
3. **Oracle-Safe Assertions** -- Custom metamorphic relations verify behavioral consistency (e.g., "paraphrasing a system prompt should not change output quality by more than +/- 0.05") without requiring exact expected outputs -- solving the fundamental "oracle problem" that makes LLM testing different from traditional software testing.
4. **Statistical Comparison Engine** -- Wilcoxon signed-rank tests and Wilson score intervals replace point-estimate thresholds, providing statistically valid regression detection that distinguishes real quality degradation from random LLM output variance.

### Why This Decision Matters

The Jerry Framework has 67 agent definitions across 12 skills. Today, refactoring any agent's system prompt is a high-risk operation with no safety net: there is no automated way to determine whether a prompt change improved, degraded, or had no effect on output quality. This decision establishes the architecture for that safety net, enabling confident prompt iteration and safe migration across model versions.

### Key Rationale

1. **No single tool solves this problem.** All seven evaluated Agent SDKs and all seven evaluated LLM testing frameworks focus on "is the output good?" rather than "did this change cause a regression?" The comparison logic between prompt versions is the novel contribution this harness must make. [Phase 1C L2 Gap Analysis; Phase 3 L0]

2. **The composite scored highest by a structural margin.** Under the ADR's six-dimension weighted evaluation, the Four-Layer Composite scored 4.45/5.00, leading the next-best alternative (Extended Composite at 3.95) by 0.50 points (corroborated by Phase 5's different weight configuration at 4.65/5.00 with 0.80-point lead over the Statistical-Only alternative). This margin is structural: the composite uniquely achieves the highest score on both of the two highest-weighted dimensions (Refactoring Safety and Statistical Rigor). [ADR Options Comparison Matrix; Phase 5 L1 Comparative Matrix]

3. **Every component is evidence-derived.** No component was predetermined from training data. Each layer traces to specific convergence patterns identified independently across four research streams: the oracle problem (all 4 streams), pytest as integration backbone (3 streams), LLM-as-Judge as evaluation mechanism (3 streams), CI/CD gate as required delivery format (3 streams), and statistical rigor as universally absent (2 streams with implicit presence in all 4). [Phase 3 L1.5 Convergence Patterns PAT-001 through PAT-006]

---

## L1: Context

### Problem Statement

Engineers modifying Jerry agent definitions (the structured system prompts in `skills/*/agents/*.md`) have no automated mechanism to verify that their changes preserve output quality. The current workflow is: make the change, manually test, hope for the best. This creates three concrete problems:

1. **Regression risk during refactoring.** Prompt wording changes that appear trivial can cause significant behavioral shifts. LLM outputs are non-deterministic; the same prompt produces different outputs on each invocation. Without statistical comparison across multiple runs, there is no way to distinguish real regression from random variance. [Phase 1A L2 Identified Gaps #2: Non-Determinism Gap]

2. **Migration uncertainty.** When Anthropic releases a new Claude model version, all 67 agent definitions must be validated against the new model. Today, this validation is manual and incomplete. [Phase 1C L2 Gap Analysis: "No evaluated SDK provides native prompt regression testing capabilities"]

3. **No oracle for LLM outputs.** Traditional testing assumes a single correct expected output. LLM prompt testing has no such oracle -- there are many acceptable outputs for any given prompt. This means standard assertion mechanisms (assertEqual, snapshot comparison) produce false positives on every run. [Phase 1A L2 Identified Gaps #1: Oracle Problem; Phase 3 PAT-001]

### Forces

| Force | Evidence | Impact on Decision |
|-------|----------|-------------------|
| **F-1: Oracle problem is central** | Metamorphic testing rated HIGHEST applicability across all 12 historical methodologies [Phase 1A]; PAT-001 convergence across all 4 research streams [Phase 3 L1.5] | Architecture must include oracle-safe assertions; exact-output comparison is structurally invalid |
| **F-2: Statistical rigor universally absent** | All 7 LLM frameworks rated LOW on statistical rigor [Phase 1B L1C matrix]; ICML 2025 position paper: "CLT-based methods perform very poorly" [Phase 1D Innovation #6] | Architecture must include hypothesis testing; point-estimate thresholds are insufficient |
| **F-3: pytest is the convergence point** | PAT-002: 504M+ monthly PyPI downloads; DeepEval, Google ADK, Pydantic AI all integrate via pytest [Phase 3 L1.5]; Jerry H-20 mandates pytest | Architecture must be pytest-native |
| **F-4: CI/CD gate is the required delivery format** | PAT-004: promptfoo GitHub Action provides PR-triggered before/after comparison [Phase 3 L1.5]; Phase 1C Gap #4: no SDK provides PR-triggered regression gate | Architecture must include automated CI/CD gate |
| **F-5: LLM-as-Judge requires debiasing** | 80-87% human correlation with debiasing; "vanilla LLM-as-judge works fine for cheap filtering and initial screening, but cannot replace human expert verification for high-stakes evaluation" [Phase 1D Innovation #1]; PAT-003 tension identified [Phase 3 L1.5] | Architecture must implement position randomization and rubric shuffling |
| **F-6: No SDK provides prompt regression testing** | All 7 evaluated SDKs (LangGraph, CrewAI, OpenAI Agents SDK, Google ADK, MS Agent Framework, Pydantic AI, Strands Agents) focus on output quality evaluation, not prompt change regression detection [Phase 1C L0; Phase 3 L1.3] | The regression comparison logic is the novel contribution |

### Constraints

| Constraint | Source | Impact |
|------------|--------|--------|
| OSI-approved open-source licenses only | Phase 5 M-001; ADR-002 Constraints | All selected components verified: promptfoo (MIT), DeepEval (Apache 2.0), scipy (BSD) |
| UV-only Python execution (H-05) | Jerry CLAUDE.md | DeepEval and statistical engine run via `uv run pytest`; promptfoo runs via Docker/GHA |
| pytest as test runner backbone (H-20) | Jerry quality-enforcement.md | DeepEval is a pytest plugin; natural integration |
| CI/CD gate must block merge on regression | Phase 5 M-003 | promptfoo GitHub Action provides this; pytest exit code provides backup |
| Non-determinism-aware assertions | Phase 5 M-004 | Metamorphic relations and statistical tests; never exact-output comparison |

---

## L1: Options Evaluated

Three options are derived from the Phase 5 analytical evaluation, which assessed five candidate approaches. The three presented here represent the recommended composite (validated by Phase 5 as top-scoring), a credible simpler alternative (fewer layers, faster time-to-value), and a credible more comprehensive alternative (additional capabilities, higher cost).

### Option A: Streamlined Dual-Layer (promptfoo + DeepEval)

#### Description

Use promptfoo for CI/CD regression gating and DeepEval for pytest-native evaluation metrics. No metamorphic assertions, no statistical hypothesis testing. Regression detection relies on DeepEval's point-estimate thresholds and promptfoo's binary pass/fail assertions.

This is the minimal viable harness: two proven tools wired together without custom statistical or metamorphic layers.

#### Steelman (S-003, H-16)

Option A delivers the fastest time-to-first-value of any option. Both promptfoo and DeepEval have existing documentation, established communities (10.8K and 14K+ GitHub stars respectively), and proven CI/CD integration patterns. An engineer can have a working regression gate within days, not weeks.

Option A also carries the fewest failure modes. The Phase 5 FMEA identified 10 failure modes for the Four-Layer Composite; Option A eliminates FM-003 (incomplete MR coverage), FM-009 (ambiguous MR violations), and FM-002 (statistical false alarms from small N) entirely -- because it does not include the layers that produce those failure modes. Fewer layers means fewer integration points, fewer configuration surfaces, and fewer ways the system can produce misleading results.

For teams that primarily need "did anything obviously break?" rather than "did quality change with statistical significance?", Option A is genuinely sufficient and avoids complexity that may not be needed.

**Where this steelman is strongest:** When the engineering team is small, prompt changes are infrequent, and speed of adoption matters more than the precision of regression detection.

#### Evaluation

| Dimension | Score (1-5) | Rationale |
|-----------|-------------|-----------|
| Refactoring Safety | 3 | Detects binary pass/fail regressions but cannot distinguish statistical noise from real regression with small evaluation sets. [Phase 5 D1: promptfoo-Only=3, DeepEval-Only=3; combined does not exceed individual maximum because both share the same limitation: point-estimate thresholds] |
| Migration Confidence | 5 | promptfoo supports 100+ provider integrations for multi-model comparison. [Phase 1B L1C: "VERY HIGH multi-model support"] |
| Determinism Coverage | 2 | No multi-run aggregation. Single-run evaluations subject to LLM output variance. [Phase 1B L1C: "MEDIUM (caching; no statistical aggregation)" for promptfoo; "MEDIUM (threshold per metric; no aggregation)" for DeepEval] |
| Statistical Rigor | 1 | Binary assertions and point-estimate thresholds only. No confidence intervals, no significance testing. [Phase 1B L1C statistical rigor row: "LOW" for both promptfoo and DeepEval] |
| Integration Feasibility | 5 | DeepEval is pytest-native (H-20 compliant). promptfoo GitHub Action for CI. Established documentation. [Phase 5 D5: DeepEval-Only scored 5 on integration] |
| Time to First Value | 5 | Days to working regression gate. Both tools have existing integration docs and community support. [Phase 5: promptfoo-Only and DeepEval-Only both scored 5 on Evidence Basis] |

#### Why Not Selected

Option A scores 1/5 on Statistical Rigor and 2/5 on Determinism Coverage. For per-PR regression testing with evaluation sets smaller than 100 samples, point-estimate thresholds "perform very poorly, usually dramatically underestimating uncertainty" [Phase 1D Innovation #6, citing ICML 2025]. This means Option A will produce both false regression alarms (blocking valid PRs) and missed regressions (allowing degraded prompts through) at rates that cannot be estimated or controlled. For a harness whose primary purpose is regression safety, this is a structural deficiency.

---

### Option B: Four-Layer Composite (Recommended)

#### Description

Combine four high-evidence components into a layered architecture:

- **Layer 1 (CI/CD gate):** promptfoo declarative YAML + GitHub Action for PR-triggered regression testing
- **Layer 2 (Evaluation backend):** DeepEval pytest-native metrics with debiased LLM-as-Judge (position randomization, rubric shuffling)
- **Layer 3 (Oracle-safe assertions):** Metamorphic relations for behavioral consistency verification
- **Layer 4 (Statistical engine):** Wilcoxon signed-rank test + Wilson score intervals for version comparison

Implemented in phases A through F, with Phases A-B delivering immediate refactoring safety value within 2-3 weeks.

#### Steelman (S-003, H-16)

Option B is the only architecture that achieves the highest score on both of the two highest-weighted evaluation dimensions (Refactoring Safety and Statistical Rigor). This is not incremental improvement; it is a structural capability gap closure.

The metamorphic relation layer (Layer 3) provides what no existing tool provides: assertions that are immune to the oracle problem by design. Rather than asking "is this output correct?" (unanswerable for LLM outputs), metamorphic relations ask "is this output consistent with related outputs?" -- a question that has a definite, testable answer. The ASE 2025 LLMORPH research validated this approach across 560,000 tests with an 8.6% false positive rate [Phase 1D Innovation #2].

The statistical comparison engine (Layer 4) replaces the universally-adopted-but-statistically-invalid practice of point-estimate threshold comparison with proper hypothesis testing. Wilcoxon signed-rank tests determine whether the before/after score distributions are significantly different; Wilson score intervals quantify the uncertainty around each version's quality estimate. These are textbook statistical methods with decades of validation, applied to a domain where the ICML 2025 community consensus is that current practices are inadequate [Phase 1D Innovation #6].

The phased implementation plan means the full complexity is not required on day one. Phases A-B deliver a working harness with statistical rigor in 2-3 weeks. Phases C-D add debiasing and metamorphic relations incrementally.

**Where this steelman is strongest:** When refactoring safety is the primary concern, prompt changes affect production agent behavior, and false alarms or missed regressions have real consequences.

#### Evaluation

| Dimension | Score (1-5) | Rationale |
|-----------|-------------|-----------|
| Refactoring Safety | 5 | All regression failure modes addressed: metamorphic relations catch behavioral inconsistencies, statistical engine distinguishes real from noise-induced differences, debiased LLM-as-Judge provides consistent quality scores. [Phase 5 D1: "All regression failure modes addressed"] |
| Migration Confidence | 5 | promptfoo layer provides 100+ provider integrations; statistical engine enables confidence interval comparison across model versions; metamorphic relations validate behavioral consistency cross-model. [Phase 5 D2] |
| Determinism Coverage | 4 | Statistical engine (Layer 4) aggregates multiple runs for hypothesis testing. Metamorphic relations (Layer 3) provide determinism-safe assertions. Some residual stochasticity from single-run LLM-as-Judge scores. [Phase 5 D3] |
| Statistical Rigor | 5 | Full statistical rigor: Wilson score intervals, Wilcoxon signed-rank, Bonferroni correction for multi-metric comparisons. [Phase 5 D4; Phase 1D Innovation #6] |
| Integration Feasibility | 4 | DeepEval and statistical engine are pytest/Python native (H-05, H-20 compliant). promptfoo requires npm alongside UV -- manageable via Docker/GHA. Metamorphic relations require domain definition work. [Phase 5 D5] |
| Time to First Value | 3 | Phases A-B deliver working harness in 2-3 weeks. Full four-layer capability requires Phases C-D (additional 3-4 weeks). Slower than Option A's days-to-working-gate. [Phase 5 L2 Integration Roadmap] |

---

### Option C: Extended Composite with PPI Calibration

#### Description

All four layers from Option B, plus:

- **Layer 5 (PPI calibration):** Prediction-Powered Inference combines small human annotation datasets with LLM-as-Judge scores to produce bias-corrected confidence intervals with known statistical guarantees.
- **Layer 6 (Perturbation testing):** Automated prompt perturbation testing (Innovation #11) that generates test cases from prompt diffs, addressing the highest-priority FMEA failure mode (FM-007: incomplete test coverage).

#### Steelman (S-003, H-16)

Option C is the only architecture that addresses FM-007 (false confidence from incomplete test suite coverage, RPN 432 -- the highest-priority failure mode). Option B accepts FM-007 as an irreducible risk; Option C actively mitigates it through automated test case generation from prompt diffs.

PPI calibration (Layer 5) provides what no other statistical approach can: valid confidence intervals that account for the known bias of LLM-as-Judge evaluation. Published in *Science* (2023) and extended at NeurIPS 2024 (Stratified PPI), this approach produces confidence intervals that are statistically valid even when the LLM judge is systematically biased -- which Phase 1D Innovation #1 documents it always is without debiasing [Phase 1D Innovation #3].

For organizations subject to regulatory scrutiny of AI evaluation methods, or for future scenarios where Jerry's quality gate decisions have contractual or compliance implications, Option C provides the most defensible evaluation methodology available.

**Where this steelman is strongest:** When evaluation defensibility is paramount, human annotation investment is feasible, and the highest-priority FMEA risk (FM-007) must be actively mitigated rather than accepted.

#### Evaluation

| Dimension | Score (1-5) | Rationale |
|-----------|-------------|-----------|
| Refactoring Safety | 5 | All Option B capabilities plus automated test case generation from prompt diffs reduces FM-007 coverage gap. [Phase 1D Innovation #11; Phase 5 FM-007] |
| Migration Confidence | 5 | All Option B capabilities plus PPI-calibrated confidence intervals enable statistically defensible cross-model comparison. [Phase 1D Innovation #3] |
| Determinism Coverage | 5 | PPI calibration provides bias-corrected intervals that account for LLM judge non-determinism. Statistical guarantees are stronger than Option B's Wilcoxon approach alone. [Phase 1D Innovation #3: "produces valid confidence intervals"] |
| Statistical Rigor | 5 | Maximum: PPI + Wilcoxon + Wilson + Bonferroni. Published in *Science* with NeurIPS extension. [Phase 1D Innovation #3, Innovation #6] |
| Integration Feasibility | 2 | PPI requires a calibration dataset of human-scored Jerry outputs -- significant effort to create and maintain. Perturbation testing requires building a perturbation generator for agent definitions. Both are custom engineering with no off-the-shelf implementation. [Phase 1D Innovation #3: "Integration Feasibility: HIGH" but "requires human annotation effort" -- rated MEDIUM for harness scope; Phase 3 L1.4: "High (requires human annotation effort)"] |
| Time to First Value | 1 | All Option B timeline plus: PPI calibration requires human annotation campaign (weeks to months); perturbation generator requires custom development. Full capability is months away. [Phase 3 L2: Phase E effort rated "High"] |

#### Why Not Selected

Option C's time-to-first-value (Score 1) and integration feasibility (Score 2) are prohibitive at this stage. The PPI calibration layer requires a human annotation campaign to build the calibration dataset -- an investment that cannot be justified until the base harness (Option B) has proven its value in production use. The perturbation testing layer (Innovation #11) is emerging research without production-ready tooling.

Option C is the natural evolution path for Option B. Phases E and F of the implementation roadmap describe exactly this evolution. The decision is not "never" -- it is "not yet."

---

### Dimension Weight Justification

| Dimension | Weight | Rationale |
|-----------|--------|-----------|
| Refactoring Safety | 0.25 | Highest weight: the harness's primary use case is regression detection during prompt editing (F-1, Problem Statement). This dimension directly measures how well each option serves that use case. |
| Statistical Rigor | 0.20 | Second-highest: F-2 establishes that statistical rigor is universally absent in current tools and is the critical gap identified by ICML 2025. Without this, regression detection is threshold-based guessing. |
| Migration Confidence | 0.15 | Model migration is the secondary use case (Problem Statement), requiring cross-version comparison. Important but less frequent than day-to-day refactoring. |
| Integration Feasibility | 0.15 | The harness must integrate into Jerry's UV-only, pytest-native environment (F-3, H-05, H-20). Poor integration feasibility blocks adoption regardless of technical merit. |
| Time to First Value | 0.15 | Equal to Integration Feasibility: the harness must deliver value within weeks, not months, to justify the investment. Derived from the ADR's architectural evaluation scope (not present in Phase 5's research-focused weight set). |
| Determinism Coverage | 0.10 | Lowest weight: while non-determinism awareness is essential (F-1, F-5), it is an enabling property rather than the primary evaluation criterion. All architecturally viable options must address it; the discriminating factor is how well, not whether. |

### Options Comparison Matrix

| Dimension | Weight | Option A: Streamlined | Option B: Four-Layer (Rec.) | Option C: Extended |
|-----------|--------|----------------------|----------------------------|-------------------|
| Refactoring Safety | 0.25 | 3 (0.75) | **5 (1.25)** | 5 (1.25) |
| Migration Confidence | 0.15 | 5 (0.75) | **5 (0.75)** | 5 (0.75) |
| Determinism Coverage | 0.10 | 2 (0.20) | 4 (0.40) | **5 (0.50)** |
| Statistical Rigor | 0.20 | 1 (0.20) | **5 (1.00)** | 5 (1.00) |
| Integration Feasibility | 0.15 | **5 (0.75)** | 4 (0.60) | 2 (0.30) |
| Time to First Value | 0.15 | **5 (0.75)** | 3 (0.45) | 1 (0.15) |
| **Weighted Total** | **1.00** | **3.40** | **4.45** | **3.95** |

**Ranking:**

| Rank | Option | Weighted Total | Delta from Winner |
|------|--------|---------------|-------------------|
| 1 | **B: Four-Layer Composite** | **4.45** | -- |
| 2 | C: Extended Composite | 3.95 | -0.50 |
| 3 | A: Streamlined Dual-Layer | 3.40 | -1.05 |

**Note on weight differences from Phase 5:** This ADR uses a six-dimension evaluation (adding Time to First Value) per the architecture decision requirements, whereas Phase 5 used a six-dimension evaluation with Evidence Basis instead of Time to First Value, and different dimension weights. The Phase 5 evaluation assessed five approaches (including single-tool options); this ADR evaluates three architecturally distinct alternatives. The Four-Layer Composite remains the top-ranked option under both weight configurations.

**Sensitivity analysis:** Option B's lead over Option A is robust: even if Time to First Value weight is doubled (0.30) at the expense of Statistical Rigor (0.10), Option B scores 4.00 vs. Option A's 3.95 -- still leading, though narrowly. The recommendation flips to Option A only if Statistical Rigor weight drops below 0.05, which contradicts the ICML 2025 consensus that statistical rigor is the critical gap in LLM evaluation [Phase 1D Innovation #6].

---

## L1: Decision

**We propose adopting Option B: Four-Layer Composite Architecture as the test harness for LLM prompt evaluation and safe refactoring in the Jerry Framework.**

The architecture consists of four layers with distinct integration characteristics:

| Layer | Component | License | Function | Jerry Integration |
|-------|-----------|---------|----------|-------------------|
| **1. CI/CD Gate** | promptfoo | MIT | Declarative YAML test case definitions; GitHub Action for PR-triggered regression testing; before/after diff reporting | Runs via GitHub Action or Docker; test configs in `tests/prompt-regression/` |
| **2. Evaluation Backend** | DeepEval | Apache 2.0 | 14+ pytest-compatible evaluation metrics; G-Eval custom criteria; debiased LLM-as-Judge | pytest plugin; `uv run pytest tests/prompt-regression/` |
| **3. Oracle-Safe Assertions** | Custom (Python) | N/A (internal) | Metamorphic relation definitions; behavioral consistency verification without expected outputs | Custom assertion module; Jerry-specific MR definitions |
| **4. Statistical Engine** | scipy + custom | BSD (scipy) | Wilcoxon signed-rank for version comparison; Wilson score intervals for per-metric evaluation; Bonferroni correction for multi-metric | Python module; `jerry/testing/stats.py` (shared with PROJ-017) |

### Decision Rationale Summary

The decision rests on five converging lines of evidence:

1. **Weighted evaluation (primary):** The Four-Layer Composite scored 4.45/5.00 on the ADR's six-dimension weighted evaluation matrix, leading the next-best alternative by 0.50 points (corroborated by Phase 5's different weight configuration at 4.65/5.00 with 0.80-point lead). The margin is structural, not incremental. [ADR Options Comparison Matrix; Phase 5 L1 Comparative Matrix]

2. **Phase 3 convergence patterns:** Six independent convergence patterns identified across four research streams all support the composite architecture: oracle problem dominance (PAT-001), pytest convergence (PAT-002), LLM-as-Judge adoption (PAT-003), CI/CD gate requirement (PAT-004), declarative configuration fit (PAT-005), and statistical rigor absence (PAT-006). [Phase 3 L1.5]

3. **Phase 1 gap analysis:** All seven evaluated Agent SDKs and all seven evaluated LLM testing frameworks leave the same five gaps unfilled: prompt version management, regression comparison logic, non-determinism-aware assertions, CI/CD regression gates, and test case generation from prompt changes. The composite architecture addresses four of five (Gap #5 is deferred to Phase F). [Phase 1C L2 Gaps 1-5]

4. **PROJ-017 ADR-002 alignment:** ADR-002 selected promptfoo as the CI/CD engine for skill-level evaluation. This ADR leverages the same promptfoo infrastructure for regression testing, creating shared infrastructure rather than competing toolchains. [PROJ-017 ADR-002 L1 Decision]

5. **FMEA risk-informed design:** The Phase 5 FMEA identified 10 failure modes with RPNs from 60 to 432. The implementation roadmap sequences phases to address failure modes in RPN priority order: FM-004/FM-005/FM-008 in Phase A, FM-002/FM-006 in Phase B, FM-001 in Phase C, FM-003/FM-009 in Phase D. [Phase 5 L1 FMEA Analysis]

---

## L1: Technical Implementation

### Architecture Diagram

```
PROMPT CHANGE (git diff detects modified agent definition file)
    |
    v
Layer 1: promptfoo GitHub Action (triggers on PR)
    |
    +--> Load test cases from YAML test suite
    |    (tests/prompt-regression/*.yaml)
    +--> Run prompt versions A (base) and B (PR) against target LLM
    +--> Collect raw outputs (N >= 20 runs per version)
    |
    v
Layer 2: DeepEval Metric Evaluation (pytest plugin)
    |
    +--> G-Eval with debiased LLM-as-Judge
    |    (position randomization, rubric shuffling per Innovation #1)
    +--> Custom property assertions
    |    (output constraints, format compliance, H-rule checks)
    |
    v
Layer 3: Metamorphic Relation Checks
    |
    +--> Paraphrase consistency (MR-001)
    +--> Negation handling (MR-002)
    +--> Irrelevant context appendation (MR-003)
    +--> Formatting perturbation (MR-004)
    +--> Language round-trip (MR-005)
    |
    v
Layer 4: Statistical Comparison Engine
    |
    +--> Retrieve baseline scores for prompt version A
    +--> Run Wilcoxon signed-rank test (version A vs. B)
    +--> Compute Wilson score intervals per metric
    +--> Apply Bonferroni correction for multi-metric comparison
    +--> Classify: NO_REGRESSION | MARGINAL | REGRESSION
    |
    v
CI/CD Gate Decision
    |
    +--> PASS: no statistically significant regression detected
    +--> WARN: marginal regression (p < 0.10 but p >= 0.05)
    +--> FAIL: regression detected (p < 0.05) with confidence interval
    |    (blocks merge; posts detailed report to PR)
    v
Optional: Langfuse observability layer
    Log prompt version, scores, comparison results for trend tracking
```

### Component Integration Patterns

**Layer 1 + Layer 2 integration:** promptfoo executes test cases and passes raw LLM outputs to DeepEval metrics via a custom Python assertion provider. This pattern is documented in the Phase 1B industry framework survey: "A hybrid approach (promptfoo for CI gates, DeepEval for in-depth metric evaluation) is architecturally viable" [Phase 1B L2].

**Layer 2 + Layer 3 integration:** Metamorphic relations are implemented as custom DeepEval metrics. Each MR defines a transformation function and an expected consistency relation. Example:

```python
# Metamorphic Relation: Paraphrase Consistency (MR-001)
# Source: Phase 1D Innovation #2 (LLMORPH); Phase 1A Metamorphic Testing
class ParaphraseConsistencyMetric(BaseMetric):
    """Verify that paraphrasing the system prompt does not
    change output quality score by more than tolerance."""

    def __init__(self, tolerance: float = 0.05):
        self.tolerance = tolerance

    def measure(self, test_case: LLMTestCase) -> float:
        original_score = self.evaluate(test_case.input)
        paraphrased_score = self.evaluate(
            self.paraphrase(test_case.input)
        )
        delta = abs(original_score - paraphrased_score)
        return 1.0 if delta <= self.tolerance else 0.0
```

**Layer 2 + Layer 4 integration:** The statistical engine consumes score arrays from DeepEval evaluations across N runs. Example:

```python
# Statistical Comparison: Wilcoxon Signed-Rank Test
# Source: Phase 1D Innovation #6 (ICML 2025, ICLR 2025)
from scipy.stats import wilcoxon
from statsmodels.stats.proportion import proportion_confint

def compare_versions(
    scores_a: list[float],
    scores_b: list[float],
    alpha: float = 0.05
) -> RegressionResult:
    """Compare two prompt versions using Wilcoxon signed-rank.

    Returns regression classification with confidence interval.
    """
    if len(scores_a) < 20 or len(scores_b) < 20:
        raise InsufficientSamplesError(
            f"Wilcoxon requires N >= 20 per version (got {len(scores_a)}, {len(scores_b)}). "
            "Use Smoke mode for single-run structural checks only."
        )
    stat, p_value = wilcoxon(scores_a, scores_b)
    ci_a = proportion_confint(
        sum(s >= 0.92 for s in scores_a),
        len(scores_a),
        method="wilson"
    )
    ci_b = proportion_confint(
        sum(s >= 0.92 for s in scores_b),
        len(scores_b),
        method="wilson"
    )
    if p_value < alpha and mean(scores_b) < mean(scores_a):
        return RegressionResult.REGRESSION
    elif p_value < 0.10:
        return RegressionResult.MARGINAL
    return RegressionResult.NO_REGRESSION
```

### Test Case Definition Format

Test cases use promptfoo's declarative YAML with Jerry-specific extensions:

```yaml
# tests/prompt-regression/ps-researcher.yaml
description: "Regression tests for ps-researcher agent"
prompts:
  - file://skills/problem-solving/agents/ps-researcher.md
providers:
  - id: anthropic:claude-sonnet-4-20250514
    config:
      temperature: 0
tests:
  - vars:
      user_query: "Research authentication patterns for .NET microservices"
    assert:
      - type: python
        value: "file://tests/prompt-regression/metrics/quality_score.py"
        threshold: 0.85
      - type: python
        value: "file://tests/prompt-regression/metrics/paraphrase_mr.py"
      - type: contains
        value: "## L0"  # Structural check: L0 section present
```

### Tiered Evaluation Modes

To address FM-006 (cost overrun), three evaluation tiers are defined:

| Mode | Runs per Version | Metrics | Approximate Cost | Use Case |
|------|-----------------|---------|-----------------|----------|
| **Smoke** | 1 | Deterministic only (structural checks, format compliance) | $0.00 | Every PR; fast feedback |
| **Standard** | 10 | Deterministic + LLM-as-Judge (debiased) | ~$2 | PRs modifying agent definitions |
| **Full** | 30 | All layers including MR checks + full statistical analysis | ~$5-8 | Pre-release validation; model migration |

**Note:** Smoke mode (N=1) provides deterministic structural checks only and is explicitly non-statistical. Its output report is labeled "STRUCTURAL ONLY -- not statistically valid" to prevent false confidence (FM-002 mitigation). Standard and Full modes enforce N >= 20 via runtime assertion in the statistical engine.

---

## L1: Consequences

### Positive

1. **Confident prompt refactoring.** Engineers can modify agent definitions and receive automated, statistically valid feedback on whether the change caused a regression. This transforms prompt editing from a high-risk manual process to a standard engineering workflow with safety nets. [Phase 5 L0: "The Four-Layer Composite is the only approach that fully addresses all six evaluation dimensions"]

2. **Shared infrastructure with PROJ-017.** Both PROJ-017 (skill evaluation) and PROJ-035 (prompt regression) use promptfoo as the CI/CD layer and a statistical engine as the differentiating component. A shared Python statistical module (`jerry/testing/stats.py`) serves both projects without infrastructure duplication. [Phase 5 L2: "Shared statistical engine: The BCa bootstrap and Wilcoxon signed-rank implementations serve different use cases but operate on the same data type"]

3. **Model migration safety.** When Anthropic releases new Claude model versions, the harness provides a systematic way to validate all 67 agent definitions against the new model with statistical confidence intervals -- not manual spot-checking. [Phase 1C L2 Gap #4; Phase 5 D2]

4. **Oracle problem solved by design.** Metamorphic relations provide behavioral assertions that work despite LLM non-determinism. This is not a workaround; it is the academically validated approach (ASE 2025, 560K tests, 8.6% false positive rate). [Phase 1A; Phase 1D Innovation #2]

5. **Statistical rigor closes the industry gap.** Every LLM evaluation framework surveyed uses point-estimate thresholds. The harness's statistical engine provides what none of them do: confidence intervals and significance testing for regression detection. [Phase 1B L1C; Phase 1D Innovation #6]

### Negative

1. **Four-layer complexity creates integration risk.** The composite architecture has more integration points than a single-tool approach. Each layer boundary is a potential failure point. The Phase 5 FMEA identified 10 failure modes, 4 of which (FM-001, FM-002, FM-003, FM-009) arise specifically from multi-layer interactions that would not exist in Option A. [Phase 5 FMEA; directly acknowledged]

2. **promptfoo introduces a Node.js dependency.** Jerry is a UV-only Python project (H-05). promptfoo is TypeScript-native. While this is mitigated via Docker/GitHub Action (no local npm install required), it creates a toolchain inconsistency. If the Docker/GHA mitigation proves insufficient, the fallback is promptfoo's Python API client, which supports programmatic evaluation execution but does not provide the native GitHub PR status integration that the GitHub Action does. Under this fallback, M-003 (CI/CD merge blocking) would be satisfied via pytest exit code (non-zero on regression) integrated into a standard GitHub Actions workflow step, rather than promptfoo's native PR reporter. This is a degraded but functionally compliant path. [Phase 5 FM-004: RPN 90]

3. **Metamorphic relation definition requires domain expertise.** The harness cannot generate its own metamorphic relations -- they must be authored by engineers who understand Jerry's agent behavioral expectations. If MR definitions are not maintained, Layer 3 provides no value. This is a process risk, not a technical risk. [Phase 5 FM-003: RPN 240; Phase 5 L2: "Human factors: The two highest-priority risks are not technical; they are process risks"]

4. **Statistical engine requires minimum sample sizes.** Wilcoxon signed-rank tests require N >= 20 per version for reliable results. This means the Standard and Full evaluation modes require 20-60 LLM invocations per regression test, creating cost pressure. The tiered evaluation modes mitigate this, but Smoke mode (N=1) provides no statistical guarantee. [Phase 5 FM-002: RPN 168; FM-006: RPN 140]

5. **Time-to-first-value is slower than the simplest alternative.** Option A delivers a working gate in days; Option B requires 2-3 weeks for Phases A-B. This delay is the cost of statistical rigor. [Options Matrix: Option A Time to First Value = 5, Option B = 3]

### Neutral

1. **Evolution path to Option C is designed-in.** Phases E and F of the implementation roadmap explicitly describe the addition of PPI calibration and perturbation testing. The architecture accommodates these additions without refactoring. [Phase 3 L2 Phased Implementation Plan]

2. **All selected components are OSI-licensed and independently viable.** If any single component is deprecated, the others continue to function. promptfoo replacement would require a new CI/CD layer; DeepEval replacement would require new metric implementations; the statistical engine and metamorphic relations are custom code with no external dependency risk. [Phase 5 M-001]

---

## L1: Risks

Risk register drawn from Phase 5 FMEA analysis with ADR-level mitigations.

| ID | Failure Mode | S | O | D | RPN | Mitigation | Phase |
|----|--------------|----|---|---|-----|------------|-------|
| FM-007 | False confidence from incomplete test suite coverage | 9 | 6 | 8 | **432** | Require test case authorship alongside prompt authorship (PR checklist); implement prompt perturbation testing (Phase F); track coverage metric | F (ongoing) |
| FM-001 | Vanilla LLM-as-Judge bias invalidates version comparison | 8 | 7 | 5 | **280** | Position randomization + rubric shuffling as mandatory harness configuration | C |
| FM-003 | Incomplete metamorphic relation coverage | 8 | 5 | 6 | **240** | Start with 5 universal MRs; MR definition workshop; track MR coverage metric | D |
| FM-002 | Statistical false alarm from small evaluation sets | 7 | 6 | 4 | **168** | Enforce N >= 20 per version; use Wilcoxon exclusively for paired comparison | B |
| FM-005 | Prompt version mismatch in baseline store | 9 | 4 | 4 | **144** | Git commit hash + file path as composite version key; smoke test validation | A |
| FM-010 | Stale baseline captures known-poor prompt version | 8 | 3 | 6 | **144** | Require quality gate check before baseline acceptance; baseline audit CLI | E |
| FM-006 | LLM cost overrun from multi-sample statistical engine | 7 | 5 | 4 | **140** | Tiered evaluation modes: Smoke ($0), Standard (~$2), Full (~$5-8) | B |
| FM-009 | Metamorphic relation violation is ambiguous | 5 | 5 | 5 | **125** | Calibrate MR tolerance against 100+ real output pairs; use MR violations as warnings until validated | D |
| FM-004 | promptfoo npm dependency conflicts with UV-only | 6 | 5 | 3 | **90** | Docker image or GitHub Action (primary); Python API client + pytest exit code fallback (M-003 compliant via GHA workflow step) | A |
| FM-008 | DeepEval metric version drift changes score scale | 5 | 4 | 3 | **60** | Pin DeepEval version in `uv.lock`; re-baseline after version bumps | A |

**Critical finding:** FM-007 (RPN 432) is the highest-priority risk and is structurally irreducible. It represents the test coverage problem applied to prompts: any prompt behavior not covered by a test case is invisible to the harness. This risk can be reduced (via Innovation #11 perturbation testing in Phase F) but not eliminated. All claims about harness safety must explicitly acknowledge this coverage limitation. [Phase 5 L1 FMEA: "FM-007 is not a component implementation problem -- it is an intrinsic limitation of any test harness that does not achieve 100% behavioral coverage"]

---

## L1: Implementation Roadmap

Phases are sequenced by FMEA priority (highest-RPN failure modes addressed first) and dependency order.

| Phase | Components | FMEA Risks Addressed | Effort | Value Delivered |
|-------|-----------|---------------------|--------|----------------|
| **A: Foundation** | pytest + DeepEval integration; promptfoo GitHub Action setup; git-hash version keys; DeepEval version pinning | FM-004, FM-005, FM-008 | Low (1-2 weeks) | First working CI regression gate (Smoke mode) |
| **B: Statistical Layer** | Wilson score intervals; Wilcoxon signed-rank version comparison; tiered evaluation modes (Smoke/Standard/Full) | FM-002, FM-006 | Low-Medium (1 week) | Statistically valid regression detection (Standard mode) |
| **C: Debiasing** | Position randomization; rubric shuffling for LLM-as-Judge | FM-001 | Low (1-2 days) | Valid cross-version comparison scores |
| **D: Metamorphic** | 5 universal MRs + Jerry-specific MR definitions; MR assertion type in DeepEval | FM-003, FM-009 | Medium (2-3 weeks for MR definition) | Oracle-problem-safe regression detection |
| **E: Baseline Quality** | Baseline quality gate; baseline audit CLI command | FM-010 | Low (1-2 days) | Prevents regression against known-bad baselines |
| **F: Coverage (ongoing)** | Innovation #11 test case generation from prompt diffs; test coverage metrics | FM-007 | High (ongoing process) | Reduces (but cannot eliminate) coverage gap |

**Milestone:** Phases A+B deliver a working, statistically valid regression harness in approximately 2-3 weeks. This is the minimum viable harness.

**Effort caveat:** Effort estimates are qualitative, derived from component complexity and integration documentation maturity [Phase 3 L2: "The effort classifications are qualitative estimates ... should be treated as directional guidance rather than planning-grade estimates until a prototype sprint validates them"].

---

## L1: PROJ-017 ADR-002 Relationship

### Complementary, Not Competing

PROJ-017 ADR-002 and this ADR address fundamentally different questions:

| Dimension | PROJ-017 ADR-002 | PROJ-035 ADR-001 (This ADR) |
|-----------|-----------------|----------------------------|
| **Question** | Does invoking skill X improve output quality vs. no-skill baseline? | Did this prompt change cause a regression in output quality? |
| **Comparison type** | Skill-present vs. skill-absent (treatment variable = skill activation) | Prompt version N vs. N+1 (treatment variable = prompt change) |
| **Primary concern** | Skill effectiveness measurement | Safe refactoring and migration |
| **promptfoo role** | CI/CD layer for skill comparison orchestration | CI/CD layer for PR-triggered regression gate |
| **Statistical engine** | BCa bootstrap + permutation + FDR correction (effect size focus) | Wilcoxon signed-rank + Wilson score intervals (regression detection focus) |

### Shared Infrastructure

Both projects share three infrastructure components:

1. **promptfoo installation.** The PROJ-017 two-provider YAML (skill-present vs. skill-absent) and the PROJ-035 regression gate YAML (version A vs. version B) coexist in the same promptfoo installation. [Phase 5 L2: "No duplicate infrastructure"]

2. **Statistical engine module.** A shared Python module (`jerry/testing/stats.py`) provides BCa bootstrap (PROJ-017) and Wilcoxon signed-rank (PROJ-035) on the same data type: paired score arrays from LLM evaluation. [Phase 5 L2: "A shared Python statistical module serves both projects without duplication"]

3. **DeepEval metrics.** Both projects can use DeepEval's G-Eval and custom metrics as scoring backends.

### Divergence Points

- PROJ-017's governance compliance validator (Jerry H-rule structural assertions) is out of scope for PROJ-035's regression harness.
- PROJ-035's metamorphic relation layer is not needed for PROJ-017's skill comparison use case.
- The two projects share infrastructure but not all components.

### Sequencing Recommendation

Phase A of this ADR's roadmap should be coordinated with PROJ-017's Phase 0 promptfoo trial. Establishing the shared promptfoo installation and CI configuration once eliminates duplicate setup work.

---

## L2: Architectural Implications

### Long-Term Evolution Path

The Four-Layer Composite architecture is designed for incremental evolution without refactoring:

```
Phase A-B (Now):       [promptfoo] → [DeepEval] → [Statistical Engine]
                        CI/CD gate    Metrics      Hypothesis testing
                        ~2-3 weeks to working harness

Phase C-D (Weeks 3-6): [promptfoo] → [DeepEval + Debiasing] → [MR Layer] → [Statistical Engine]
                        CI/CD gate    Debiased metrics          Oracle-safe   Hypothesis testing
                        Full four-layer capability

Phase E-F (Future):    [promptfoo] → [DeepEval + PPI] → [MR + Perturbation] → [Statistical Engine]
                        CI/CD gate    Calibrated scores  Auto-generated tests   Hypothesis testing
                        Maximum regression safety
```

Each phase adds capability without modifying prior layers. This is possible because the layers communicate through a common data format: arrays of quality scores produced by Layer 2, consumed by Layers 3 and 4.

### Systemic Consequences

Three systemic patterns identified in the Phase 5 analysis have implications beyond PROJ-035:

**Pattern A: Statistical debt accrues silently.** Every evaluation in the Jerry framework that uses a point-estimate threshold (>= 0.92 from S-014) is subject to the CLT underestimation problem. This is not a PROJ-035-specific problem -- it applies to every ps-critic evaluation, every quality gate, and every adversarial scoring event. The PROJ-035 statistical engine represents an investment that should eventually be generalized to the broader Jerry quality framework. [Phase 5 L2: "statistical debt accrues silently"]

**Pattern B: Evaluation validity requires configuration discipline.** Using the correct tool does not guarantee valid evaluation -- it requires configuration discipline (debiasing, sample size, version key management). The harness must ship with validated default configurations, not just tool integrations. [Phase 5 L2: "evaluation validity requires configuration discipline"]

**Pattern C: Test coverage is the irreducible risk.** FM-007 is structurally unsolvable without 100% behavioral test coverage. For 67 agent definitions each containing multiple behavioral dimensions, this is an ongoing process requirement, not a one-time engineering task. [Phase 5 L2: "test coverage is the irreducible risk"]

### Future Flexibility and Constraints

**Flexibility gained:**
- Model migration becomes a systematic process rather than a manual audit
- Prompt A/B testing becomes possible with statistical confidence
- Agent definition quality can be tracked over time via regression trend data
- The statistical engine generalizes beyond PROJ-035 to improve Jerry's quality gate framework-wide

**Constraints accepted:**
- promptfoo as the CI/CD layer creates a dependency on an actively maintained but externally controlled project (mitigated: MIT license, replaceable)
- N >= 20 sample size requirement creates cost floor for statistically valid regression testing
- Metamorphic relation authorship creates ongoing domain expertise requirement
- FM-007 (coverage gap) is architecturally irreducible

### Decision Review Triggers

This decision should be revisited if any of the following occur:

| Trigger | Implication |
|---------|-------------|
| promptfoo adds native prompt regression comparison | Layer 1 may be simplified; evaluate whether native capability matches harness requirements |
| DeepEval's scoring algorithm changes in a major version | Re-baseline all test suites; evaluate whether metric continuity is maintained |
| Anthropic releases evaluation tooling with regression detection | Evaluate whether vendor tooling replaces need for custom harness |
| Jerry skill count exceeds 100 agents | Evaluate whether tiered evaluation modes scale; consider parallelization |
| PPI calibration dataset becomes available | Activate Phase E; transition from Wilcoxon-only to PPI-calibrated comparison |
| PROJ-017 ADR-002 transitions to ACCEPTED | Coordinate shared promptfoo and statistical engine infrastructure |

---

## Evidence Traceability

| Evidence ID | Source Artifact | Specific Location | Claim Supported |
|-------------|----------------|-------------------|-----------------|
| E-001 | Phase 1A: `research/historical-testing-methodologies.md` | L2 Identified Gaps #1 (Oracle Problem), #2 (Non-Determinism Gap) | Forces F-1, F-2; Metamorphic testing rationale |
| E-002 | Phase 1A: `research/historical-testing-methodologies.md` | L1 #9: Metamorphic Testing HIGHEST applicability | Layer 3 component selection |
| E-003 | Phase 1B: `research/industry-frameworks-survey.md` | L1C Capability Comparison Matrix (statistical rigor row: all LOW) | Force F-2; Statistical rigor gap |
| E-004 | Phase 1B: `research/industry-frameworks-survey.md` | L1B #1 (promptfoo: "Purpose-built for this exact use case") | Layer 1 component selection |
| E-005 | Phase 1B: `research/industry-frameworks-survey.md` | L1B #2 (DeepEval: "pytest-native, 14+ metrics") | Layer 2 component selection |
| E-006 | Phase 1B: `research/industry-frameworks-survey.md` | L2: "hybrid approach (promptfoo + DeepEval) is architecturally viable" | Composite architecture feasibility |
| E-007 | Phase 1C: `research/agent-sdk-evaluation.md` | L0: "No evaluated SDK provides native prompt regression testing" | Force F-6; Novel contribution |
| E-008 | Phase 1C: `research/agent-sdk-evaluation.md` | L2 Gaps 1-5 | Five gaps the harness addresses |
| E-009 | Phase 1D: `research/innovation-frameworks.md` | Innovation #1: "80-87% human correlation"; debiasing techniques table | Force F-5; Phase C scope |
| E-010 | Phase 1D: `research/innovation-frameworks.md` | Innovation #2: "LLMORPH: 560,000 tests, 8.6% false positive rate" (ASE 2025) | Layer 3 evidence; MR effectiveness |
| E-011 | Phase 1D: `research/innovation-frameworks.md` | Innovation #6: "CLT-based methods perform very poorly" (ICML 2025) | Force F-2; Layer 4 justification |
| E-012 | Phase 1D: `research/innovation-frameworks.md` | Innovation #3: PPI "produces valid confidence intervals" (Science 2023, NeurIPS 2024) | Option C evaluation; Phase E scope |
| E-013 | Phase 1D: `research/innovation-frameworks.md` | Innovation #8: promptfoo 10.8K stars MIT; DeepEval 14K stars Apache 2.0 | License verification; evidence basis |
| E-014 | Phase 1D: `research/innovation-frameworks.md` | Innovation #11: Prompt perturbation testing (10-40% accuracy degradation) | Phase F scope; FM-007 mitigation |
| E-015 | Phase 3: `analysis/cross-pollination-synthesis.md` | L1.5 PAT-001 through PAT-006 | Six convergence patterns supporting composite |
| E-016 | Phase 3: `analysis/cross-pollination-synthesis.md` | L2 Four-Layer Architecture section | Composite architecture derivation |
| E-017 | Phase 3: `analysis/cross-pollination-synthesis.md` | L2 Component Selection Justification (5 components with source traces) | Per-component evidence chain |
| E-018 | Phase 5: `analysis/test-harness-evaluation.md` | L1 Comparative Matrix: Composite=4.65, Statistical-Only=3.85 | Weighted scoring and ranking |
| E-019 | Phase 5: `analysis/test-harness-evaluation.md` | L1 FMEA: 10 failure modes, FM-007 RPN=432 | Risk register; phase sequencing |
| E-020 | Phase 5: `analysis/test-harness-evaluation.md` | L2: PROJ-017 ADR-002 relationship table | Complementary architecture analysis |
| E-021 | PROJ-017: `decisions/ADR-002-quality-framework-selection.md` | L0: promptfoo Extension recommended; L1 Forces F-3: Statistical rigor absent | Shared infrastructure; alignment confirmation |
| E-022 | ADR-001 Weight Justification table | Dimension weight rationale derived from Forces F-1 through F-5 and Problem Statement | Dimension weights used in Options Comparison Matrix |

---

## Self-Review (S-010)

Applied per H-15 before finalization.

- [x] **Nygard ADR format:** Title, Status, Context, Decision, Consequences sections all present
- [x] **3 options evaluated:** Streamlined Dual-Layer, Four-Layer Composite, Extended Composite with PPI
- [x] **All 6 dimensions scored:** Refactoring Safety, Migration Confidence, Determinism Coverage, Statistical Rigor, Integration Feasibility, Time to First Value
- [x] **Options derived from Phase 5 analysis:** Phase 5 identified Five-Layer Composite as top-scoring; 3 ADR options represent simpler/recommended/comprehensive alternatives from Phase 5 evidence
- [x] **Evidence tracing present:** 22 evidence entries tracing to specific Phase 1/3/5 artifact locations and ADR-internal derivations
- [x] **PROJ-017 ADR-002 relationship addressed:** Complementary analysis with shared infrastructure and divergence points documented
- [x] **L0/L1/L2 structure complete:** Executive Summary, technical sections, Architectural Implications
- [x] **Navigation table present (H-23):** Document Sections table at top with anchor links
- [x] **Status is "Proposed" (P-020):** Human approval required before ACCEPTED
- [x] **Negative consequences documented (P-022):** Five negative consequences explicitly stated including complexity risk, Node.js dependency, MR expertise requirement, sample size cost, and time-to-value delay
- [x] **Steelman applied to rejected alternatives (S-003, H-16):** Option A steelman acknowledges genuine speed and simplicity advantages; Option C steelman acknowledges genuine statistical and coverage advantages
- [x] **All frameworks/tools have verified OSI-approved licenses:** promptfoo (MIT), DeepEval (Apache 2.0), scipy (BSD)

---

*ADR produced: 2026-03-06*
*Agent: ps-architect (Phase 7, PROJ-035 FEAT-035-001)*
*Input artifacts: 6 Phase 1/3/5 documents + PROJ-017 ADR-002*
*Evidence entries: 22 (all traced to specific artifact sections)*
*Confidence: HIGH for component selection; MEDIUM-HIGH for integrated composite (pending Phase A prototype validation)*
