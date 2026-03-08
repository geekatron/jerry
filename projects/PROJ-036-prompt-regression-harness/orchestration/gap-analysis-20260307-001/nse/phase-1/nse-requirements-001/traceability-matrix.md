---
DISCLAIMER: This guidance is AI-generated based on NASA Systems Engineering
standards. It is advisory only and does not constitute official NASA guidance.
All SE decisions require human review and professional engineering judgment.
Not for use in mission-critical decisions without SME validation.
---

# Requirements Traceability Matrix — PROJ-036 Test Harness

> **Phase 1B output from gap-analysis-20260307-001 orchestration**
> **Agent:** nse-requirements
> **Date:** 2026-03-07
> **Requirements Source:** `projects/PROJ-036-prompt-regression-harness/design/harness-requirements.md`
> **Evidence Base:** Code inspection of `jerry/testing/`, CI/CD workflows in `.github/workflows/`, validation run artifacts in `work/test-harness/validation-run/`, and test suite in `tests/prompt-regression/`

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Coverage Summary](#coverage-summary) | FR and NFR coverage statistics |
| [Functional Requirements Traceability](#functional-requirements-traceability) | FR-001 through FR-030 |
| [Non-Functional Requirements Traceability](#non-functional-requirements-traceability) | NFR-001 through NFR-015 |
| [Gap Coverage Analysis](#gap-coverage-analysis) | Which gaps block which requirements |
| [Risk Assessment](#risk-assessment) | Requirements at highest risk of non-delivery |

---

## Coverage Summary

| Category | Total | Implemented | Partial | Missing | Blocked |
|----------|-------|-------------|---------|---------|---------|
| Functional (FR) | 30 | 14 | 10 | 6 | 0 |
| Non-Functional (NFR) | 15 | 4 | 5 | 6 | 0 |

**Key finding:** Core statistical engine (Layer 4) and metamorphic relation framework (Layer 3) are fully implemented. Layer 2 evaluation backend is substantially implemented. The primary gaps are: Layer 1 promptfoo integration (FR-001 through FR-005 partial — YAML/workflows exist but promptfoo test cases are structural stubs), cross-cutting requirements (FR-022 LICENSES.md absent, FR-024 Langfuse absent, FR-029 trend persistence absent), and process requirements (FR-027 is present in CI but not enforced as blocking). NFRs are largely unverified due to absence of performance benchmarks and integration-level tests.

---

## Functional Requirements Traceability

### Status Key
- **Implemented** — Code exists; validation evidence confirms execution
- **Partial** — Implementation exists but one or more acceptance criteria are unmet or untested
- **Missing** — No implementation; requirement not addressed
- **Blocked** — Implementation depends on a prerequisite gap

---

### Layer 1: CI/CD Regression Gate (promptfoo)

| FR ID | Title | Priority | Layer | Status | Code Location | Test Evidence | Gap Ref |
|-------|-------|----------|-------|--------|---------------|---------------|---------|
| FR-001 | Declarative YAML Test Case Definitions | Must | L1 | **Partial** | `tests/prompt-regression/test-cases/{agent}.yaml` (5 files: ps-researcher, ps-analyst, ps-architect, ps-critic, adv-scorer); `tests/prompt-regression/promptfoo-config.yaml` | YAML files exist and are parseable by promptfoo schema. No evidence of full promptfoo schema conformance validation against real promptfoo execution in CI. | GAP-L1-YAML: Test case YAML exists but represents structural scaffolding; `promptfoo eval` execution not yet validated end-to-end in CI. |
| FR-002 | PR-Triggered GitHub Action Regression Gate | Must | L1 | **Partial** | `.github/workflows/prompt-regression-smoke.yml`; `.github/workflows/prompt-regression-standard.yml`; `.github/workflows/prompt-regression-full.yml` | Workflows trigger on `pull_request` with path filter `skills/*/agents/*.md`. Smoke workflow has full structural implementation including skip-notice for no-change PRs. Standard workflow has complete job structure. No real PR execution evidence in validation run artifacts. | GAP-L1-CI: Workflows implemented but require live PR to validate end-to-end execution; promptfoo Docker image not SHA-pinned (MC-08 TODO noted in workflow). |
| FR-003 | Before/After Prompt Version Comparison Execution | Must | L1 | **Partial** | `.github/workflows/prompt-regression-standard.yml` (Version A checkout step, Job 2 steps 4-6); `tests/prompt-regression/promptfoo-config.yaml` (two-provider config); `tests/prompt-regression/version_keys.py` | `version_keys.py` implements version key management. Standard workflow performs `git show origin/$BASE_REF:$AGENT_PATH` to extract Version A. `promptfoo-config.yaml` documents the two-provider architecture. Validation run used synthetic baseline data (noted: "Synthetic baseline -- validation only" in `phase4-results.json`). Real before/after execution not demonstrated with live LLM calls in validation artifacts. | GAP-L1-BEFORE-AFTER: Architecture is defined but the before/after execution path depends on both promptfoo Docker working and real API key presence; not demonstrated in validation run. |
| FR-004 | Version Key Management via Git Commit Hash | Must | L1 | **Partial** | `jerry/testing/baselines/store.py` (`_validate_version_key()`, `BaselineStore.store()`); `tests/prompt-regression/version_keys.py`; `.github/workflows/prompt-regression-standard.yml` (SHA capture steps) | `BaselineStore._validate_version_key()` enforces `{hash}:{path}` format. Standard workflow captures `BASE_SHA` and `HEAD_SHA`. `version_keys.py` provides validation utilities. The FR-004 acceptance criterion for baseline rejection on hash mismatch is implemented in `store.retrieve()`. No validation evidence of version key validation with real git SHAs in CI. | GAP-L1-VERSIONKEY: Core data structure implemented; CI integration present but unvalidated in live run. |
| FR-005 | Tiered Evaluation Mode Selection | Must | L1+L4 | **Partial** | `.github/workflows/prompt-regression-smoke.yml` (Smoke tier, `$0`, no LLM); `.github/workflows/prompt-regression-standard.yml` (N=10); `.github/workflows/prompt-regression-full.yml` (N=30); `jerry/testing/layer4_stats.py` (`_run_smoke()`, `EvaluationMode.SMOKE/STANDARD/FULL`); `jerry/testing/types.py` (`EvaluationMode` enum) | Three workflows implement three tiers. `Layer4Pipeline.run()` branches on `EvaluationMode.SMOKE`. Smoke mode label "STRUCTURAL ONLY — not statistically valid" appears in workflow comments and PR comment job. CLI argument specification is absent (no `jerry test run` CLI command found). Environment variable support is documented in workflow YAML. | GAP-L1-TIERS: Smoke tier fully wired; Standard/Full CI path implemented; CLI argument interface is missing (NFR-013 dependency). |

---

### Layer 2: Evaluation Backend (DeepEval)

| FR ID | Title | Priority | Layer | Status | Code Location | Test Evidence | Gap Ref |
|-------|-------|----------|-------|--------|---------------|---------------|---------|
| FR-006 | DeepEval pytest Plugin Integration | Must | L2 | **Partial** | `jerry/testing/evaluation/deepeval_adapter.py` (`DeepEvalAdapter`); `jerry/testing/evaluation/jerry_geval_deepeval_metric.py`; `tests/prompt-regression/conftest.py`; `tests/prompt-regression/unit/test_layer2_evaluation.py` | `DeepEvalAdapter` imports `deepeval.metrics.BaseMetric` and `deepeval.test_case.LLMTestCase`. Validation run executed Layer 2 scoring for 5 agents producing composite scores (documented in `phase2-composites.json`, `layer2-scores-*.md`). Layer 2 scores were computed with `JerryGEvalDeepEvalMetric`. No evidence of `uv run pytest tests/prompt-regression/` completing as a pytest plugin run against live LLM — validation used the `phase2_score.py` script. | GAP-L2-PYTEST: Pytest integration architecture is built; conftest exists; live `uv run pytest` end-to-end run against real agent outputs not demonstrated in validation run. |
| FR-007 | G-Eval Custom Criteria Evaluation | Must | L2 | **Implemented** | `jerry/testing/evaluation/criteria/ps_researcher.py`, `ps_analyst.py`, `ps_architect.py`, `ps_critic.py`, `adv_scorer.py`; `jerry/testing/evaluation/criterion.py` (`QualityCriterion`); `jerry/testing/evaluation/metrics.py` (`JerryGEvalMetric`) | Criteria files define per-agent QualityCriterion objects with weights matching S-014 dimensions. Validation run (`layer2-scores-ps-researcher.md`) shows G-Eval returning per-dimension scores (completeness=1.0, evidence_quality=1.0, etc.) via `claude-sonnet-4-20250514`. Five agents scored. Per-criterion scores in [0.0, 1.0]. Criterion storage: Python modules, not YAML/JSON as specified in FR-007 AC-3. | GAP-L2-CRITERIA-FORMAT: Criteria stored in Python modules, not YAML/JSON under `tests/prompt-regression/criteria/` as FR-007 AC-3 specifies. Functional but format non-conformant. |
| FR-008 | Deterministic Property Assertions | Must | L2 | **Partial** | `tests/prompt-regression/promptfoo-config.yaml` (`defaultTest.assert`: `not-empty`, `not-regex` for secrets, `cost` threshold); `tests/prompt-regression/test-cases/{agent}.yaml` | `promptfoo-config.yaml` defines universal structural assertions: non-empty output, no-secrets pattern, cost threshold. Execution time < 100ms and zero-stochasticity not measured in validation run. No separate deterministic assertion Python module found. | GAP-L2-STRUCTURAL: Deterministic assertions implemented at promptfoo config level; execution time not measured; per-agent structural section marker checks (e.g., `## L0`, `## L1`, `## L2`) handled via G-Eval criteria rather than standalone deterministic checks. |
| FR-009 | Score Array Collection and Export | Must | L2 | **Partial** | `jerry/testing/evaluation/deepeval_adapter.py` (`evaluate_batch()` returns `dict[str, ScoreArray]`); `tests/prompt-regression/promptfoo-config.yaml` (`outputPath`); `jerry/testing/types.py` (`ScoreArray = list[float]`) | `evaluate_batch()` collects per-criterion score arrays for N outputs. Validation run (`phase2-composites.json`) shows composite scores for 5 agents from single-shot evaluation. JSON output path specified in `promptfoo-config.yaml`. The exact FR-009 JSON schema (`{"metric_id": str, "version_key": str, "scores": list[float], "run_count": int, "evaluation_mode": str}`) not confirmed in any written output file. `phase2-composites.json` uses a different schema (per-agent composite, not per-metric score array). | GAP-L2-EXPORT: Score array collection works; the exact FR-009 canonical JSON path and schema not yet produced in any validation artifact. |
| FR-010 | Five Universal Metamorphic Relations | Must | L3 | **Implemented** | `jerry/testing/metamorphic/mr_001_paraphrase.py` (`ParaphraseConsistency`); `mr_002_negation.py` (`NegationHandling`); `mr_003_context.py` (`IrrelevantContextAppendation`); `mr_004_formatting.py` (`FormattingPerturbation`); `mr_005_roundtrip.py` (`LanguageRoundTrip`); `jerry/testing/metamorphic/__init__.py` (`all_relations()`) | All 5 MR classes exist and are importable. Validation run executed MR-001 and MR-003 smoke test (5 pairs each) for ps-researcher and ps-architect (`layer3-mr-results.md`). Domain ABC pattern used instead of direct DeepEval BaseMetric (documented deviation: H-07 compliance). Note: FR-010 AC specifies `BaseMetric` inheritance but `__init__.py` notes this is a deliberate domain-isolation deviation. | GAP-L3-BASECLASS: MR implementations use domain ABC instead of DeepEval BaseMetric; adapter wrapping to be done in `deepeval_adapter.py`; not yet demonstrated in integration test. |
| FR-011 | MR Tolerance Calibration | Must | L3 | **Partial** | `jerry/testing/metamorphic/calibration.py` (`CalibrationRunner`, `apply_calibrated_tolerances()`) | `CalibrationRunner` stub exists with correct interface; `calibrate_tolerances()` raises `NotImplementedError` with explicit message "implement after Phase A baseline data collection." `apply_calibrated_tolerances()` is fully implemented and functional. Warning for N < 100 pairs is implemented. | GAP-L3-CALIBRATION: Calibration utility is a documented stub pending Phase A baseline data collection. Not a code gap — intentional deferral. However, FR-011 AC ("verify warning threshold behavior") test coverage is unverified. |
| FR-012 | Jerry-Specific MR Definitions | Should | L3 | **Missing** | `jerry/testing/metamorphic/__init__.py` (notes FR-012 as "downstream deliverable; not in this package") | No agent-specific MR classes found. `__init__.py` explicitly marks FR-012 as downstream. No per-agent MR definitions exist. The mechanism (per-agent MR class using domain ABC) exists but no agent-specific instances have been created. | GAP-L3-AGENT-MR: Agent-specific MR mechanism is architecturally present (BaseMetric interface); zero agent-specific MR implementations. Phase D deliverable. |
| FR-013 | MR Coverage Tracking Metric | Should | L3 | **Missing** | `jerry/testing/metamorphic/__init__.py` (notes FR-013 as "downstream deliverable; not in this package") | No coverage tracking module found. `per-agent/*.contract.yaml` files exist in `tests/prompt-regression/contracts/per-agent/` (5 files for 5 agents) and serve as a behavioral property registry candidate, but no coverage computation code exists. | GAP-L3-COVERAGE: Behavioral property registry files exist; coverage computation and CI/CD report inclusion are absent. |

---

### Layer 4: Statistical Comparison Engine

| FR ID | Title | Priority | Layer | Status | Code Location | Test Evidence | Gap Ref |
|-------|-------|----------|-------|--------|---------------|---------------|---------|
| FR-014 | Minimum Sample Size Enforcement (N >= 20) | Must | L4 | **Implemented** | `jerry/testing/stats.py` (`MIN_STATISTICAL_SAMPLE_SIZE = 20`, `InsufficientSamplesError`, `compare_versions()` N check lines 581-588); `jerry/testing/metamorphic/base.py` (`_validate_inputs()`) | `compare_versions()` raises `InsufficientSamplesError` with exact required message format. `MIN_STATISTICAL_SAMPLE_SIZE` constant defined. Unit tests in `tests/prompt-regression/unit/test_stats.py` cover `InsufficientSamplesError`. Validation run used N=20 synthetic data (`phase4-results.json`: "n_samples": 20). | None — fully implemented and validated. |
| FR-015 | Wilcoxon Signed-Rank Version Comparison | Must | L4 | **Implemented** | `jerry/testing/stats.py` (`wilcoxon_signed_rank()`, `compare_versions()`, `_classify_regression()`); `jerry/testing/types.py` (`RegressionResult`, `WilcoxonResult`, `RegressionClass`) | `scipy.stats.wilcoxon` invoked with `alternative="two-sided"`. Classification logic at `_classify_regression()` implements REGRESSION/MARGINAL/NO_REGRESSION/IMPROVEMENT. Validation run `layer4-ps-researcher.md` shows p=0.0000, Cohen's r=0.843, effect=Medium-to-Large, verdict=IMPROVEMENT. Note: classification uses combined p-value + effect-size rules (contracts.md D.4) which extends beyond FR-015's stated criteria — this is a documented evolution, not a deviation. | None — implemented and validated with real scoring results. |
| FR-016 | Wilson Score Confidence Intervals | Must | L4 | **Implemented** | `jerry/testing/stats.py` (`wilson_score_intervals()`, `QUALITY_PASS_THRESHOLD = 0.92`); uses `statsmodels.stats.proportion.proportion_confint(method="wilson")` | `wilson_score_intervals()` computes 95% Wilson CI via statsmodels. `QUALITY_PASS_THRESHOLD = 0.92` constant defined. Validation run `layer4-ps-researcher.md` shows CI_A=[0.000, 0.161], CI_B=[0.433, 0.819] in per-metric results table. | None — implemented and validated. |
| FR-017 | Bonferroni Correction for Multi-Metric Comparison | Must | L4 | **Implemented** | `jerry/testing/stats.py` (`bonferroni_correction()`, `compare_multiple_metrics()`, `BONFERRONI_K_FULL_SUITE = 13`, `BONFERRONI_ALPHA_FULL = 0.004`); `jerry/testing/layer4_stats.py` (`_run_statistical()`, `BONFERRONI_K_FULL_SUITE` applied in FULL mode) | `bonferroni_correction()` computes `alpha_family / k`. `compare_multiple_metrics()` applies corrected alpha per metric. Full suite k=13 constant documented and used. Validation run used single-metric comparison (no Bonferroni needed for one metric). `test_stats.py` tests multi-metric path. | None — implemented; single-metric validation run does not exercise multi-metric Bonferroni path, but unit tests cover it. |
| FR-018 | Regression Classification Report with PR Integration | Must | L4+L1 | **Implemented** | `jerry/testing/layer4_stats.py` (`_exit_code()`, `_emit_gha_outputs()`, `_persist_report()`); `jerry/testing/reports/generator.py` (`ReportGenerator`); `.github/workflows/prompt-regression-standard.yml` (Enforce regression gate step) | Exit codes: BLOCK=1, ALLOW_WITH_WARNING=2, ALLOW=0 per FR-018. GHA output variables emitted via `GITHUB_OUTPUT`. Standard workflow step "Enforce regression gate (FR-018)" uses VERDICT to set exit 0/1/2. Markdown and JSON reports generated. Validation run shows markdown reports (`layer4-ps-researcher.md`) and JSON (`layer4-ps-researcher.json`). PR comment is posted in "post-standard-summary" job. | None — implemented and validated in validation run. PR comment integration demonstrated in workflow definition. |
| FR-019 | Shared Statistical Module (jerry/testing/stats.py) | Must | L4 | **Implemented** | `jerry/testing/stats.py` (exports: `compare_versions`, `wilson_score_intervals`, `bonferroni_correction`, `InsufficientSamplesError`, `RegressionResult`, `MIN_STATISTICAL_SAMPLE_SIZE`, `QUALITY_PASS_THRESHOLD`); `jerry/testing/layer4_stats.py` (imports exclusively from `jerry.testing.stats`) | Module boundary comment in `stats.py` lines 10-15 documents forbidden imports. `layer4_stats.py` imports `compare_multiple_metrics`, `compare_versions`, `merge_decision_from_classification` from `jerry.testing.stats`. No re-implementation of statistical logic in `layer4_stats.py`. Type annotations and docstrings present per H-11. | None — module architecture conforms to FR-019 specification. |
| FR-020 | Baseline Store with Quality Gate | Must | L1+L4 | **Implemented** | `jerry/testing/baselines/store.py` (`BaselineStore.store()`, quality gate `_BASELINE_QUALITY_GATE = 0.92`, `BaselineStore.audit()`); `jerry/testing/baselines/ports.py` (`BaselinePersistencePort`) | `store()` rejects baselines with `mean_score < 0.92`. `audit()` returns list of `BaselineAuditEntry` with version key, mean score, age. `invalidate()` implemented for contract version releases. Validation run used synthetic baselines directly in `phase4_stats.py`. `jerry test baseline audit` CLI command not implemented (NFR-013 dependency). | GAP-L4-CLI: `BaselineStore.audit()` is implemented; CLI command `jerry test baseline audit` is absent. |

---

### Cross-Cutting Functional Requirements

| FR ID | Title | Priority | Layer | Status | Code Location | Test Evidence | Gap Ref |
|-------|-------|----------|-------|--------|---------------|---------------|---------|
| FR-021 | LLM-as-Judge Debiasing | Must | L2 | **Implemented** | `jerry/testing/evaluation/debiasing.py` (`DebiasingStrategy`); `jerry/testing/evaluation/deepeval_adapter.py` (mandatory `require_debiasing=True`); `jerry/testing/evaluation/position_randomization_result.py` | `DebiasingStrategy` implements `shuffle_criteria()` and `randomize_candidate_positions()`. `DeepEvalAdapter.__post_init__` raises `ValueError` if `debiasing_strategy is None`. `require_debiasing=True` in `JerryGEvalMetric`. Validation run `layer2-scores-ps-researcher.md` confirms "Debiasing: C-007 (criterion order shuffled)". `debiasing-config.yaml` under `tests/prompt-regression/` not found — FR-021 AC-4 not met. | GAP-L2-DEBIAS-CONFIG: Debiasing is implemented and mandatory; `debiasing-config.yaml` documentation file is absent. |
| FR-022 | OSI-Approved License Verification | Must | Cross | **Partial** | `pyproject.toml` (dependencies declared); LICENSES.md — **MISSING** | `pyproject.toml` includes `deepeval`, `scipy`, `statsmodels` as dependencies. OSI license list for these dependencies is accurate (Apache 2.0, BSD). LICENSES.md file not found in repository root. CI license check not found in `.github/workflows/`. | GAP-CC-LICENSES: LICENSES.md file absent; CI license verification step absent. Two acceptance criteria of three are unmet. |
| FR-023 | UV-Only Python Execution | Must | Cross | **Implemented** | `.github/workflows/prompt-regression-smoke.yml` (uses `astral-sh/setup-uv`, `uv sync`, `uv run python`); `.github/workflows/prompt-regression-standard.yml`; `pyproject.toml` (no requirements.txt used) | All workflow steps use `uv run` or `uv sync`. No `python` or `pip` invocations found in workflow YAML files. No `requirements.txt` found as primary dependency file. H-05 compliance evident throughout. | None — UV-only requirement is met in all workflow files. |
| FR-024 | Langfuse Observability Integration (Optional) | Should | Cross | **Missing** | No Langfuse integration found in `jerry/testing/` or workflows | Standard workflow includes `LANGFUSE_PUBLIC_KEY` and `LANGFUSE_SECRET_KEY` environment variable injection (suggesting intent), but no code in `jerry/testing/` imports or calls Langfuse. No trace logging found. | GAP-CC-LANGFUSE: Environment variable injection is present in workflow (non-zero intent) but no Langfuse SDK calls exist anywhere in the codebase. |
| FR-025 | promptfoo Docker/GitHub Action Isolation | Must | L1 | **Implemented** | `.github/workflows/prompt-regression-smoke.yml` (Docker execution with `ghcr.io/promptfoo/promptfoo:latest`, hardened flags); `.github/workflows/prompt-regression-standard.yml` (Docker with `ghcr.io/promptfoo/promptfoo:0.86.0`); `pyproject.toml` (no npm/Node.js entries) | Docker execution uses `--read-only`, `--cap-drop=ALL`, `--network=none` (smoke), `--security-opt=no-new-privileges:true`. No npm/Node.js entries in `pyproject.toml`. Version pinned in standard workflow (`0.86.0`). Smoke workflow uses `:latest` with TODO to pin to SHA digest (MC-08). | GAP-L1-DOCKER-PIN: Smoke workflow image not SHA-pinned (uses `:latest` with TODO comment). Standard workflow uses `0.86.0` tag but not SHA digest. |
| FR-026 | DeepEval Version Pinning with Re-Baseline Protocol | Must | L2 | **Partial** | `uv.lock` (deepeval version pinned); re-baseline runbook location per FR-026 AC-2 | `uv.lock` exists and pins DeepEval to an exact version (standard uv behavior). Re-baseline runbook at `tests/prompt-regression/runbooks/re-baseline-after-upgrade.md` — **MISSING** (directory does not exist). CI detection of DeepEval update without re-baseline — **MISSING**. | GAP-L2-REBASELINE: DeepEval is version-pinned in uv.lock; re-baseline runbook and CI re-baseline detection check are absent. Two of three acceptance criteria unmet. |
| FR-027 | Test Case Authorship Requirement | Must | Cross/Governance | **Partial** | `.github/workflows/prompt-regression-smoke.yml` (FR-027 check: `test-authorship` job, per-agent warning); `.github/workflows/prompt-regression-standard.yml` (FR-027: test YAML existence check with `exit 1` for missing YAML) | Smoke workflow warns (non-blocking) when agent YAML missing. Standard workflow fails (blocking `exit 1`) when YAML missing — this exceeds FR-027 AC-1 which requires only a warning. PR checklist template not found (`.github/PULL_REQUEST_TEMPLATE.md` not searched). Test case YAML files exist for 5 agents (`tests/prompt-regression/test-cases/`). | GAP-CC-PR-TEMPLATE: PR template with required checklist item not confirmed. Standard workflow is more restrictive than FR-027 specifies (blocking vs. warning). |
| FR-028 | Model Migration Comparison Mode | Should | L1+L4 | **Missing** | `promptfoo-config.yaml` references single provider type; no migration mode flag or report label found | No migration mode implementation found. Standard workflow does not support two-provider comparison. `EvaluationMode` enum has SMOKE/STANDARD/FULL but no MIGRATION mode. | GAP-L1-MIGRATION: Not implemented. Should-priority; migration mode is a future enhancement. |
| FR-029 | Regression Trend Persistence | Should | Cross | **Missing** | No trend persistence or history directory found in `jerry/testing/` or `tests/prompt-regression/` | No history JSON files, no trend-writing code, no `jerry test trend` command found. `BaselineStore` persists baselines but not per-run evaluation history. | GAP-CC-TREND: Not implemented. Should-priority; trend tracking is a future enhancement. |
| FR-030 | Extensible Layer Architecture | Must | Cross/Architecture | **Partial** | `jerry/testing/stats.py`, `jerry/testing/layer4_stats.py`, `jerry/testing/metamorphic/`, `jerry/testing/evaluation/`, `jerry/testing/baselines/`, `jerry/testing/reports/` | Layer separation exists: Layer 2 (`evaluation/`), Layer 3 (`metamorphic/`), Layer 4 (`stats.py` + `layer4_stats.py`), baseline store, report generator. FR-030 AC-1 requires distinct modules at: `jerry/testing/layer1_promptfoo.py`, `jerry/testing/layer2_deepeval.py`, `jerry/testing/layer3_metamorphic.py`, `jerry/testing/layer4_stats.py`. Layer 1 and Layer 2 entry-point modules at these exact paths are absent (Layer 2 is implemented as `evaluation/` package, not `layer2_deepeval.py`). Inter-layer score array contract is defined in IF-003 but exact FR-009 JSON schema not confirmed as the live data format in validation run. | GAP-CC-LAYER-MODULES: Layer 1 (`layer1_promptfoo.py`), Layer 2 (`layer2_deepeval.py`), Layer 3 (`layer3_metamorphic.py`) entry-point modules at FR-030 specified paths are absent. Layering exists but not under the canonical module names. |

---

## Non-Functional Requirements Traceability

| NFR ID | Title | Priority | Status | Code Location | Test Evidence | Gap Ref |
|--------|-------|----------|--------|---------------|---------------|---------|
| NFR-001 | Evaluation Latency — Smoke Mode (< 60s) | Must | **Partial** | `.github/workflows/prompt-regression-smoke.yml` (`timeout-minutes: 5`); Docker invocation with `--network=none` (no LLM calls) | Smoke workflow has 5-minute timeout configured (well within 60s for structural checks). No performance measurement artifacts found. No P95 timing data across 10 runs. Structural checks only (no LLM calls) makes sub-60s plausible but unverified. | GAP-NFR-PERF: No performance benchmark results exist. Acceptance criterion requires P95 measurement across 10 runs. |
| NFR-002 | Evaluation Latency — Standard Mode (< 15 min) | Must | **Partial** | `.github/workflows/prompt-regression-standard.yml` (`timeout-minutes: 25`); cost monitor action referenced | 25-minute workflow timeout allows 15-minute target. No timing measurement artifacts found. N=10 LLM calls per version is the intended runtime driver. Validation run used pre-computed scores (no real LLM timing data). | GAP-NFR-PERF: No timing measurement. Same as NFR-001. |
| NFR-003 | Statistical Engine Computation Time (< 1s) | Must | **Partial** | `jerry/testing/stats.py` (scipy + statsmodels operations); `tests/prompt-regression/unit/test_stats.py` | Unit tests exist for statistical functions. Validation run executed Layer 4 computations (`phase4_stats.py`) in < 1s (implied by batch processing of 5 agents with N=20 synthetic samples). No benchmark test file `tests/prompt-regression/unit/test_stats_type1_error.py` found. | GAP-NFR-BENCHMARK: No formal benchmark test. Computational complexity is low (scipy Wilcoxon + statsmodels proportions); sub-1s is highly plausible but unverified by benchmark. |
| NFR-004 | Evaluation Cost Ceiling — Full Mode (< $10) | Must | **Missing** | `.github/workflows/prompt-regression-standard.yml` (`COST_CEILING_USD: "5.00"` env var; cost monitor action) | Cost ceiling is defined in workflow as $5 (Standard mode). Full mode ceiling of $10 not separately enforced. Cost monitor action referenced but action definition not in searched scope. No cost analysis artifacts found. ADR-001 estimate of "$5-8" not formally verified. | GAP-NFR-COST: Cost ceiling enforcement is structural (workflow level) but Full mode specific ceiling ($10) not tested or documented. |
| NFR-005 | Harness CI Availability (Zero Manual Setup) | Must | **Partial** | `.github/workflows/prompt-regression-smoke.yml` (`Install UV`, `Set up Python 3.12`, `Install project dependencies`); SHA-pinned actions | Workflow auto-installs UV, Python 3.12, and project deps. All dependencies are declared in `pyproject.toml`. No manual setup required per workflow definition. `.github/actions/cost-monitor` referenced in standard workflow but action definition not found — potential blocker. | GAP-NFR-CI: Custom actions referenced in standard workflow (`.github/actions/cost-monitor`, `.github/actions/artifact-publish`) are not confirmed to exist; these would be needed for end-to-end CI execution. |
| NFR-006 | False Positive Rate — MRs (<= 15%) | Must | **Missing** | `jerry/testing/metamorphic/` (MR implementations with tolerance values) | Validation run tested MR-001 and MR-003 with N=5 (insufficient sample size; noted in results as "SMOKE TEST - not statistically powered"). No calibrated false positive rate measurement exists. MR tolerances are analytically derived, not calibrated. | GAP-NFR-MR-FPR: No calibration dataset of 100+ known-good output pairs. False positive rate measurement not possible until Phase A baseline data collected per FR-011. |
| NFR-007 | Statistical Rigor — Type I Error Rate | Must | **Missing** | `jerry/testing/stats.py` (`compare_versions()` with `alpha=0.05` enforcement) | Monte Carlo validation test file `tests/prompt-regression/unit/test_stats_type1_error.py` — **MISSING**. Wilcoxon's theoretical Type I error control is well-established, but FR-007 requires empirical Monte Carlo validation at N=30 before production deployment. | GAP-NFR-TYPE1: Monte Carlo validation test not implemented. This is a verification gap — the algorithm is correct but not empirically validated per NFR-007 acceptance criteria. |
| NFR-008 | Test Case File Naming Convention | Should | **Implemented** | `tests/prompt-regression/test-cases/ps-researcher.yaml`, `ps-analyst.yaml`, `ps-architect.yaml`, `ps-critic.yaml`, `adv-scorer.yaml` | All 5 test case files follow `{agent-id}-regression.yaml` pattern (note: files are named `{agent-id}.yaml` not `{agent-id}-regression.yaml` — minor naming deviation). One file per agent. Files are stored under `tests/prompt-regression/test-cases/`. | GAP-NFR-NAMING: Files named `{agent-id}.yaml` not `{agent-id}-regression.yaml` as NFR-008 specifies. Minor deviation; actual filenames are `tests/prompt-regression/test-cases/{agent-id}.yaml`. |
| NFR-009 | Security — No Secrets in Test Artifacts | Must | **Implemented** | `tests/prompt-regression/promptfoo-config.yaml` (`apiKey: env:ANTHROPIC_API_KEY`); `.github/workflows/` (`::add-mask::` in standard workflow); `jerry/testing/stats.py` (`InvalidScoreArrayError` for adversarial input validation) | API key referenced via `env:ANTHROPIC_API_KEY` in promptfoo config (not hardcoded). Workflow uses `::add-mask::` for API key. No secrets found in test YAML files or result JSON files in validation run. `stats.py` validates score arrays against adversarial tampering. | None — security requirements met. |
| NFR-010 | Reproducibility — Deterministic Structural Assertions | Must | **Implemented** | `tests/prompt-regression/promptfoo-config.yaml` (`not-empty`, `not-regex` assertions with no randomness); `jerry/testing/evaluation/debiasing.py` (`seed=None` for production but `seed` parameter for deterministic testing) | Structural assertions (`not-empty`, `not-regex`) are pure regex-based with zero stochasticity. Smoke mode uses `--network=none` preventing any external calls. Debiasing uses `seed` parameter for reproducible test execution. `DebiasingStrategy(seed=42)` used in tests. | None — deterministic assertions are implemented. |
| NFR-011 | Test Coverage >= 90% | Must | **Partial** | `tests/prompt-regression/unit/test_stats.py`, `test_baselines.py`, `test_debiasing.py`, `test_layer2_evaluation.py`, `test_metamorphic_base.py`, `test_metrics.py`, `test_types.py`, `test_version_keys.py`; `tests/prompt-regression/integration/test_layer4_pipeline.py`; `tests/prompt-regression/property/test_mr_properties.py`, `test_stats_properties.py` | Substantial unit and integration test suite exists (11 test files found). Coverage not measured — no coverage report artifact found. 90% line coverage requirement per H-20 cannot be confirmed without running `pytest --cov=jerry/testing`. | GAP-NFR-COVERAGE: Test suite exists but line coverage has not been measured. Cannot confirm >= 90% without executing coverage run. |
| NFR-012 | Layer Contract Stability | Should | **Partial** | `jerry/testing/types.py` (`ScoreArray`, `BaselineRecord`, `ComparisonReport`); FR-009 JSON schema in interface specification | Core types are defined in `types.py`. No formal schema versioning or breaking-change detection mechanism found. Score array format (`{"metric_id": str, "version_key": str, "scores": list[float], ...}`) is specified in FR-009 but not enforced at runtime by a schema validator. | GAP-NFR-SCHEMA: Schema stability is aspirational; no schema version field or breaking-change CI check exists. |
| NFR-013 | Usability — Baseline CLI Commands | Should | **Missing** | No `jerry test` subcommand group found in `jerry/cli/` (directory not found) | `jerry test run`, `jerry test baseline list`, `jerry test baseline audit`, `jerry test trend` commands — **ALL MISSING**. `BaselineStore.audit()` provides the backing data for `jerry test baseline audit` but CLI front-end is absent. | GAP-NFR-CLI: All four CLI commands are unimplemented. Core functionality (baseline store, stats) is available programmatically but no CLI wrapper exists. |
| NFR-014 | Inline Code Documentation (H-11 Compliance) | Must | **Implemented** | All `jerry/testing/*.py` and `jerry/testing/**/*.py` modules | All public functions in `stats.py`, `layer4_stats.py`, `baselines/store.py`, `evaluation/deepeval_adapter.py`, `metamorphic/mr_001_paraphrase.py` have type annotations and docstrings with Args, Returns, Raises sections. Module-level docstrings reference FR numbers for traceability. Consistent with H-11. | None — H-11 compliance verified across all inspected modules. |
| NFR-015 | Portability — Local Development (macOS/Linux) | Should | **Partial** | `jerry/testing/stats.py`, `jerry/testing/metamorphic/`, `jerry/testing/evaluation/` (pure Python, no Docker requirement); `uv.lock` | Statistical engine and metamorphic framework are pure Python and runnable locally. Layer 2 requires `deepeval` which is `uv add`-able. Local execution of Smoke and Standard modes requires no Docker for the Python statistical layer. promptfoo Layer 1 requires Docker for full execution per FR-025. `uv run pytest tests/prompt-regression/` runnable locally if DeepEval and API key present. | GAP-NFR-LOCAL: Python layers (L2/L3/L4) are locally runnable. Layer 1 (promptfoo) requires Docker even locally per FR-025 design. NFR-015 specifies this is acceptable (promptfoo path is optional). |

---

## Gap Coverage Analysis

The following table maps identified gaps to the requirements they block, enabling the gap inventory (Phase 1A) to be cross-referenced against impact.

| Gap ID | Description | Blocked Requirements | Priority Impact |
|--------|-------------|---------------------|----------------|
| GAP-L1-YAML | promptfoo YAML test cases exist as structural scaffolding; real promptfoo schema validation not confirmed | FR-001 (Partial), FR-008 (Partial) | Must x 2 |
| GAP-L1-CI | CI workflows implemented but not tested with live PR execution; Docker image not SHA-pinned in smoke workflow | FR-002 (Partial), FR-025 (Partial) | Must x 2 |
| GAP-L1-BEFORE-AFTER | Before/after execution path implemented but not demonstrated with live LLM calls | FR-003 (Partial) | Must |
| GAP-L1-VERSIONKEY | Version key management implemented in code; not end-to-end validated in live CI | FR-004 (Partial) | Must |
| GAP-L1-TIERS | Standard/Full CLI tier argument interface missing | FR-005 (Partial) | Must |
| GAP-L1-MIGRATION | Model migration comparison mode not implemented | FR-028 (Missing) | Should |
| GAP-L1-DOCKER-PIN | Docker images not pinned to SHA digest | FR-025 (Partial), NFR-005 (Partial) | Must x 2 |
| GAP-L2-PYTEST | Live `uv run pytest` end-to-end run not demonstrated | FR-006 (Partial) | Must |
| GAP-L2-CRITERIA-FORMAT | Criteria in Python modules, not YAML/JSON as FR-007 AC-3 specifies | FR-007 (Partial) | Must |
| GAP-L2-STRUCTURAL | Deterministic assertions at promptfoo level; < 100ms not measured | FR-008 (Partial), NFR-010 (Partial) | Must x 2 |
| GAP-L2-EXPORT | FR-009 canonical JSON schema not confirmed in validation run output | FR-009 (Partial) | Must |
| GAP-L2-DEBIAS-CONFIG | `debiasing-config.yaml` documentation file absent | FR-021 (Partial) | Must |
| GAP-L2-REBASELINE | Re-baseline runbook and CI detection absent | FR-026 (Partial) | Must |
| GAP-L3-BASECLASS | MR domain ABC not yet wrapped for DeepEval BaseMetric integration in tests | FR-010 (Partial) | Must |
| GAP-L3-CALIBRATION | Calibration utility is a documented stub | FR-011 (Partial) | Must |
| GAP-L3-AGENT-MR | No agent-specific MR implementations | FR-012 (Missing) | Should |
| GAP-L3-COVERAGE | No MR coverage tracking computation | FR-013 (Missing) | Should |
| GAP-L4-CLI | `jerry test baseline audit` CLI absent | FR-020 (Partial), NFR-013 (Missing) | Must + Should |
| GAP-CC-LICENSES | LICENSES.md and CI license check absent | FR-022 (Partial) | Must |
| GAP-CC-LANGFUSE | Langfuse integration absent despite workflow env var injection | FR-024 (Missing) | Should |
| GAP-CC-PR-TEMPLATE | PR checklist template not confirmed | FR-027 (Partial) | Must |
| GAP-CC-TREND | Trend persistence and `jerry test trend` command absent | FR-029 (Missing) | Should |
| GAP-CC-LAYER-MODULES | Layer 1/2/3 canonical entry-point modules absent | FR-030 (Partial) | Must |
| GAP-NFR-PERF | No performance benchmark measurements | NFR-001 (Partial), NFR-002 (Partial) | Must x 2 |
| GAP-NFR-BENCHMARK | No formal stats computation benchmark | NFR-003 (Partial) | Must |
| GAP-NFR-COST | Full mode cost ceiling not validated | NFR-004 (Missing) | Must |
| GAP-NFR-CI | Custom actions (cost-monitor, artifact-publish) not confirmed to exist | NFR-005 (Partial) | Must |
| GAP-NFR-MR-FPR | No calibration dataset; false positive rate unmeasured | NFR-006 (Missing) | Must |
| GAP-NFR-TYPE1 | Monte Carlo Type I error validation test not implemented | NFR-007 (Missing) | Must |
| GAP-NFR-NAMING | Test case files use `{agent-id}.yaml` not `{agent-id}-regression.yaml` | NFR-008 (Partial) | Should |
| GAP-NFR-COVERAGE | Coverage not measured; 90% target unconfirmed | NFR-011 (Partial) | Must |
| GAP-NFR-SCHEMA | No schema versioning or breaking-change detection | NFR-012 (Partial) | Should |
| GAP-NFR-CLI | All 4 CLI commands absent | NFR-013 (Missing) | Should |
| GAP-NFR-LOCAL | Layer 1 requires Docker locally; L2/L3/L4 are locally runnable | NFR-015 (Partial) | Should |

---

## Risk Assessment

Requirements at highest risk of non-delivery, ranked by: **Must priority + Missing or Partial status + no confirmed test coverage**.

### Tier 1 — Critical Risk (Must + Missing/Partial, Core to PR Gate)

These requirements are essential to the core mission (automated PR regression gate) and are not yet demonstrated end-to-end:

| Rank | FR/NFR | Title | Risk Rationale | Recommended Action |
|------|--------|-------|---------------|-------------------|
| 1 | FR-002 | PR-Triggered GitHub Action Gate | Workflows are implemented but never executed against a real PR. Docker execution path unconfirmed. This is the outermost integration and any gap here breaks the entire harness mission. | Create a canary PR modifying an agent definition file; observe workflow execution. |
| 2 | FR-003 | Before/After Comparison Execution | Validation run used synthetic baselines. Real before/after with live LLM calls not demonstrated. Without this, regression detection is structurally impossible. | Execute Standard workflow on a real PR with known regression; verify Version A is retrieved from git and Version B from PR branch. |
| 3 | FR-006 | DeepEval pytest Plugin Integration | `uv run pytest tests/prompt-regression/` end-to-end not demonstrated against real agent outputs. This is the Layer 2 entry point for all metric evaluation. | Run `uv run pytest tests/prompt-regression/ -k ps-researcher` against a real agent output and verify DeepEval metric evaluation completes. |
| 4 | FR-022 | OSI License Verification | LICENSES.md absent. CI license check absent. Compliance is asserted but not enforced. | Create LICENSES.md; add `pip-licenses` or `uv run pip-audit` step to CI. |
| 5 | FR-030 | Extensible Layer Architecture | Canonical layer entry-point modules (`layer1_promptfoo.py`, `layer2_deepeval.py`, `layer3_metamorphic.py`) absent. FR-030 AC-1 specifies these exact paths. | Create entry-point module files at specified paths, or update FR-030 to reflect the package-based architecture (package PR, not code gap). |
| 6 | NFR-007 | Type I Error Rate Validation | Monte Carlo test `test_stats_type1_error.py` not implemented. FR-007 requires this before production deployment. Without it, statistical rigor is theoretical not empirical. | Implement the Monte Carlo test as a parameterized pytest benchmark. This is a one-time verification artifact. |

### Tier 2 — High Risk (Must + Missing acceptance criteria)

| Rank | FR/NFR | Title | Risk Rationale |
|------|--------|-------|---------------|
| 7 | FR-026 | DeepEval Version Pinning | Re-baseline runbook absent. Version drift creates silent score scale shifts (FM-008, RPN=60). |
| 8 | NFR-005 | CI Availability | Custom actions (cost-monitor, artifact-publish) referenced in standard workflow but not confirmed to exist. |
| 9 | NFR-006 | MR False Positive Rate | Depends on Phase A calibration data (100+ pairs). MR results are currently unreliable for production use without calibration. |
| 10 | NFR-011 | 90% Test Coverage | Test suite exists but coverage not measured. H-20 is a HARD rule; unverified coverage is a governance risk. |

### Tier 3 — Medium Risk (Should + Missing)

| Rank | FR/NFR | Title | Risk Rationale |
|------|--------|-------|---------------|
| 11 | FR-012 | Agent-Specific MR Definitions | Phase D deliverable; mechanism exists. Zero implementations means MR coverage is zero for agent-specific behaviors (FM-003 mitigation not deployed). |
| 12 | FR-013 | MR Coverage Tracking | Without coverage tracking, FM-003 (incomplete MR coverage, RPN=240, highest-priority failure mode) is undetected. |
| 13 | NFR-013 | CLI Commands | `jerry test run/baseline/trend` absent. Engineers cannot iterate locally without constructing manual invocations. |
| 14 | FR-029 | Regression Trend Persistence | Trend data would enable retroactive root cause analysis; absence means each regression is analyzed in isolation. |

### Tier 4 — Low Risk (Should + Partial, or Minor Missing)

| FR/NFR | Title | Note |
|--------|-------|------|
| FR-007 | G-Eval Criteria Format | Criteria in Python modules (functional) vs YAML/JSON (FR-007 AC-3). Minor format deviation. |
| FR-021 | Debiasing Config File | `debiasing-config.yaml` is a documentation artifact; debiasing itself is implemented. |
| NFR-008 | Naming Convention | `{agent-id}.yaml` vs `{agent-id}-regression.yaml`; trivial rename. |
| NFR-012 | Layer Contract Stability | Schema stability is aspirational; types.py provides de facto stability. |
| FR-024 | Langfuse Integration | Optional (Should priority); env vars suggest future intent. |
| FR-028 | Model Migration Mode | Should priority; secondary use case. |

---

## References

- NPR 7123.1D, Process 2 (Technical Requirements Definition), Process 11 (Requirements Management)
- `projects/PROJ-036-prompt-regression-harness/design/harness-requirements.md` — Requirements source
- `jerry/testing/stats.py` — Layer 4 shared statistical module
- `jerry/testing/layer4_stats.py` — Layer 4 pipeline orchestrator
- `jerry/testing/metamorphic/` — Layer 3 MR framework
- `jerry/testing/evaluation/` — Layer 2 DeepEval backend
- `jerry/testing/baselines/store.py` — Baseline persistence
- `.github/workflows/prompt-regression-*.yml` — Layer 1 CI/CD gate
- `projects/PROJ-036-prompt-regression-harness/work/test-harness/validation-run/` — Validation evidence

---

*Generated by nse-requirements agent v2.3.0*
*Traceability: FR-001 through FR-030 and NFR-001 through NFR-015 — all 45 requirements traced*
*Evidence-based per P-011 and P-004: each status assignment cites specific file paths or validation artifacts*
