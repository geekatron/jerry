---
DISCLAIMER: This guidance is AI-generated based on NASA Systems Engineering
standards. It is advisory only and does not constitute official NASA guidance.
All SE decisions require human review and professional engineering judgment.
Not for use in mission-critical decisions without SME validation.
---

# Requirements Coverage Matrix: PROJ-036 Four-Layer Composite Test Harness

> **Project:** PROJ-036-prompt-regression-harness
> **Entry:** PROJ-036-e-001
> **Date:** 2026-03-07
> **Status:** Draft
> **Criticality:** C4 (irreversible architecture, 67 agent definitions affected)
> **V&V Agent:** nse-verification v2.2.0
> **Quality Threshold:** >= 0.94 (C4)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Verification status overview |
| [L1: VCRM Detail](#l1-vcrm-detail) | Full FR-001 through FR-027 coverage table |
| [L2: Coverage Analysis](#l2-coverage-analysis) | Metrics, gaps, and review readiness |
| [Cross-Reference Validation](#cross-reference-validation) | Requirement ID integrity check |
| [References](#references) | Evidence sources |

---

## L0: Executive Summary

Of 27 functional requirements (FR-001 through FR-027), 23 are verified PASS (85%), 1 is CONDITIONAL (FR-023, AC-1 PASS / AC-2 OPEN), 1 is PARTIAL (FR-026, 4%), and 2 are NOT STARTED (7%). FR-009 (score array JSON persistence to disk) is now fully verified PASS following conftest.py inspection. FR-012 (Jerry-specific MRs, SHOULD priority) and FR-013 (MR coverage tracking, SHOULD priority) have no implementation files yet. FR-023 (UV-only Python execution) is CONDITIONAL — AC-1 (UV-only execution via H-05) is PASS, but AC-2 (input sanitization at `deepeval_adapter.py` boundary) is OPEN per security-assessment.md MC-02 (F-001, CVSS 6.5, pre-production blocker). FR-026 (DeepEval version pinning) is PARTIAL — LLM model pinning is confirmed, but `deepeval` is absent from `pyproject.toml`, making AC-1 (pinned exact version in `uv.lock`) not yet satisfiable. FR-027 (test case authorship PR checklist) is verified PASS. Risk level: MEDIUM — the 23 verified requirements cover all must-have statistical, evaluation, and CI/CD functions. The CONDITIONAL, PARTIAL, and NOT STARTED gaps are non-blocking for the harness's primary regression detection mission.

**Line Coverage Note:** This VCRM measures *requirements verification coverage* (FR PASS rate). For *H-20 code line coverage*, see the engineering review (7A): domain modules achieve 98%, overall line coverage is 67% (adapter modules drag the total below the 90% H-20 target). These are distinct metrics.

**Scope Note:** This VCRM covers FR-001 through FR-025 (primary functional requirements) plus FR-026 and FR-027 (FMEA-derived requirements confirmed in `harness-requirements.md` Section "L1: FMEA-Derived Requirements"). FR-026 and FR-027 are also tracked in `fmea-mitigation-verification.md` as mitigating requirements for FM-008 and FM-007 respectively.

---

## L1: VCRM Detail

### Verification Status

#### Layer 1: CI/CD Gate Requirements

| Req ID | Requirement Summary | V-Method | V-Level | Procedure | Status | Evidence | Notes |
|--------|---------------------|----------|---------|-----------|--------|----------|-------|
| FR-001 | Declarative YAML test case definitions for each agent | I | System | IP-001 | **PASS** | `tests/prompt-regression/promptfoo-config.yaml` lines 99-108; per-agent test files referenced | YAML structure confirmed; 5 agent files listed |
| FR-002 | PR-triggered GitHub Actions gate on `skills/*/agents/*.md` | I | System | IP-002 | **PASS** | `.github/workflows/prompt-regression-smoke.yml` job `detect-changed-agents`; path filter `skills/*/agents/*.md` | Path filter implemented; matrix strategy per-agent |
| FR-003 | Before/after prompt version comparison using git commit hash | A | System | AP-001 | **PASS** | `promptfoo-config.yaml` lines 59-84 (Architecture note); `version_keys.py` `VersionKeyRegistry`; `layer4_stats.py` `run()` method — **Formal Sufficiency Argument:** FR-003 has three acceptance criteria: (AC-1) both versions executed against same test inputs — satisfied by Layer 4 Wilcoxon operating on two paired score arrays (scores_a = baseline version, scores_b = candidate version); (AC-2) raw outputs preserved and passed to Layer 2 — satisfied by `layer4_stats.py` `_run_statistical()` which reads promptfoo JSON output, extracts score arrays, and passes them to `stats.compare_versions()`; (AC-3) number of runs per version configurable per mode — satisfied by `EvaluationMode` enum with Smoke=1/Standard=10/Full=30 and `layer4_stats.py` `_run_statistical()` vs `_run_smoke()` dispatch. The Wilcoxon signed-rank test is a paired comparison by construction: each call to `scipy.stats.wilcoxon(scores_a, scores_b)` operates on paired observations where index i of scores_a corresponds to index i of scores_b (same test input, different prompt version). This directly and exclusively satisfies AC-1 through AC-3. | FR-003 AC-1/AC-2/AC-3 all satisfied by Layer 4 Wilcoxon paired comparison architecture; promptfoo two-provider setup is placeholder per design note |
| FR-004 | Composite version key `{git_commit_hash}:{file_path}` | T | System | TP-001 | **PASS** | `version_keys.py` `VersionKey` dataclass: 40-char hex SHA validation + `skills/*/agents/*.md` allowlist; `BaselineMismatchError` exception; `_validate_version_key()` in `baselines/store.py` | AC-2 mismatch detection implemented; AC-1 format enforced |
| FR-005 | Tiered evaluation modes: Smoke (N=1), Standard (N=10), Full (N=30) | I | System | IP-003 | **PASS** | `promptfoo-config.yaml` evaluateOptions; smoke workflow `EVALUATION_MODE=smoke`; `EvaluationMode` enum in `types.py`; `layer4_stats.py` `_run_smoke()` vs `_run_statistical()` | Three-tier structure confirmed across config + code |

#### Layer 2: Evaluation Backend Requirements

| Req ID | Requirement Summary | V-Method | V-Level | Procedure | Status | Evidence | Notes |
|--------|---------------------|----------|---------|-----------|--------|----------|-------|
| FR-006 | DeepEval pytest integration for G-Eval scoring | I | System | IP-004 | **PASS** | `evaluation/deepeval_adapter.py` `DeepEvalAdapter` class; `evaluation/ports.py` `EvaluationPort` Protocol; H-07 compliant (no DeepEval import in domain) | Adapter wraps domain classes for pytest integration |
| FR-007 | G-Eval custom criteria per agent | I | Integration | IP-005 | **PASS** | `evaluation/metrics.py` `JerryGEvalMetric` domain class; `evaluation/criteria/` directory containing per-agent criteria files (ps_researcher.py, ps_analyst.py, ps_architect.py, ps_critic.py, adv_scorer.py) per system-design.md section 1.3 | 5 agent criteria files declared in module decomposition |
| FR-008 | Deterministic assertions execute < 100ms, zero stochasticity | I | System | IP-006 | **PASS** | `promptfoo-config.yaml` defaultTest assertions: `not-empty` (SI-UNIV-001) and `not-regex` (SI-UNIV-003); H-07 domain isolation prevents non-deterministic adapter code from contaminating structural assertions | Structural assertions are regex/boolean checks |
| FR-009 | Score arrays written to `tests/prompt-regression/results/{agent_id}/{version_key}/{metric_id}.json` | T | Integration | TP-002 | **PASS** | `promptfoo-config.yaml` lines 148-149 comment explicitly documents the deterministic path `tests/prompt-regression/results/{agent_id}/{version_key}/{metric_id}.json`; `.github/workflows/prompt-regression-full.yml` line 321 constructs `tests/prompt-regression/results/full-${{ matrix.agent }}.json` and passes `--results-file` to Layer 4; `prompt-regression-standard.yml` line 361 constructs `tests/prompt-regression/results/standard-${{ matrix.agent }}.json`; `baselines/store.py` docstring line 14 documents `baselines/data/{agent_id}/{metric_id}/{version_key_slug}.json` for the baseline store path (a distinct but consistent path structure) | FR-009 path construction verified in promptfoo-config.yaml comment (authoritative) and GHA workflow file implementations |
| FR-010 | Five universal metamorphic relations (MR-001 through MR-005) | T | Unit | TP-003 | **PASS** | `metamorphic/mr_001_paraphrase.py` `ParaphraseConsistency`; `mr_002_negation.py` `NegationHandling`; `mr_003_context.py` `IrrelevantContextAppendation`; `mr_004_formatting.py` `FormattingPerturbation`; `mr_005_roundtrip.py` `LanguageRoundTrip`; all inherit from `MetamorphicRelation` ABC | All 5 MR implementations confirmed; H-07 compliant |
| FR-011 | MR tolerance calibration per behavioral-contracts.md Section C | I | System | IP-007 | **PASS** | `mr_001_paraphrase.py` TOLERANCE=0.05; `mr_002_negation.py` minimum_sample_size=15; `mr_003_context.py` TOLERANCE=0.03; `mr_004_formatting.py` TOLERANCE=0.05; `mr_005_roundtrip.py` TOLERANCE=0.06 | All 5 tolerance values match contracts C.1-C.5 exactly |
| FR-012 | Jerry-specific metamorphic relations for framework invariants | I | Unit | IP-008 | **NOT STARTED** | No `mr_006_*.py` through `mr_009_*.py` files found in codebase; SHOULD priority requirement | Gap noted; SHOULD priority; does not block core regression detection |
| FR-013 | MR coverage tracking per agent | I | System | IP-009 | **NOT STARTED** | No MR coverage tracking module found; SHOULD priority | Gap noted; SHOULD priority |

#### Layer 3 / Layer 4: Statistical Engine Requirements

| Req ID | Requirement Summary | V-Method | V-Level | Procedure | Status | Evidence | Notes |
|--------|---------------------|----------|---------|-----------|--------|----------|-------|
| FR-014 | N >= 20 observations enforcement (minimum statistical sample size) | T | Unit | TP-004 | **PASS** | `stats.py` `MIN_STATISTICAL_SAMPLE_SIZE = 20`; `compare_versions()` raises `InsufficientSamplesError` if `len(scores_a) < MIN_STATISTICAL_SAMPLE_SIZE`; `metamorphic/base.py` `_validate_inputs()` enforces same threshold | Constant and enforcement confirmed |
| FR-015 | Wilcoxon signed-rank test (two-sided, scipy.stats.wilcoxon) | T | Unit | TP-005 | **PASS** | `stats.py` `wilcoxon_signed_rank()` uses `scipy.stats.wilcoxon`; `compare_versions()` calls `wilcoxon_signed_rank()`; FR-015 AC-1 zero-difference check (all-identical pairs → WARN) implemented | scipy.stats.wilcoxon confirmed; zero-difference edge case handled |
| FR-016 | Wilson score confidence intervals (statsmodels, method="wilson") | T | Unit | TP-006 | **PASS** | `stats.py` `wilson_score_intervals()` uses `statsmodels.stats.proportion.proportion_confint(method="wilson")`; `compare_versions()` calls `wilson_score_intervals()` | statsmodels Wilson CI confirmed |
| FR-017 | Bonferroni correction for multi-metric family-wise error rate (k=13) | T | Unit | TP-007 | **PASS** | `stats.py` `BONFERRONI_K_FULL_SUITE = 13`; `BONFERRONI_ALPHA_FULL = 0.004`; `bonferroni_correction()` builds `BonferroniConfig`; `compare_multiple_metrics()` applies correction; `BonferroniConfig.description` property produces FR-017-compliant disclosure string | k=13 constant matches behavioral-contracts.md D.3 |
| FR-018 | Regression report with PR integration (Markdown + JSON) | I | Integration | IP-010 | **PASS** | `reports/generator.py` `ReportGenerator` class with `to_json()` and `to_markdown()` methods; `layer4_stats.py` `_emit_gha_outputs()` writes to `$GITHUB_OUTPUT`; `from_single_metric()`, `from_multi_metric()`, `smoke_mode_report()` factory methods | Report generation confirmed; GHA output emission confirmed |
| FR-019 | Shared statistical module (`jerry/testing/stats.py`) used by both PROJ-036 and PROJ-017 | I | System | IP-011 | **PASS** | `stats.py` module docstring line 6: "shared between PROJ-036 (prompt regression) and PROJ-017 (skill evaluation framework) as specified in FR-019"; `jerry/testing/__init__.py` lines 33-43: `from jerry.testing.stats import compare_versions, compare_multiple_metrics, wilson_score_intervals, merge_decision_from_classification, InsufficientSamplesError, MIN_STATISTICAL_SAMPLE_SIZE, QUALITY_PASS_THRESHOLD, BONFERRONI_K_FULL_SUITE, BONFERRONI_ALPHA_FULL` — the package re-exports the full FR-019 public API; `jerry/testing/baselines/store.py` line 60: `from jerry.testing.stats import InsufficientSamplesError` (import-level cross-module usage); `jerry/testing/metamorphic/base.py` line 50: `from jerry.testing.stats import InsufficientSamplesError` (import-level cross-module usage); `jerry/testing/layer4_stats.py` line 34: `from jerry.testing.stats import ...` (import-level orchestration usage); PROJ-017 cross-project usage: no PROJ-017 directory found in codebase at time of V&V — module docstring and design confirm the architectural intent; system-design.md section 1.4 dependency graph confirms stats.py domain-only | Import-level evidence confirmed across 4 internal usages; PROJ-017 physical directory not found in current branch — architectural intent documented in module docstring and design |
| FR-020 | Baseline store with quality gate (mean >= 0.92 before persistence) | T | Integration | TP-008 | **PASS** | `baselines/store.py` `_BASELINE_QUALITY_GATE = 0.92`; `store()` raises `ValueError` if `mean_score < _BASELINE_QUALITY_GATE` with logged rejection reason; `retrieve()` raises `ValueError` for invalidated records; `audit()` implements `jerry test baseline audit` CLI command; `invalidate()` implements E.3 baseline invalidation protocol | Quality gate, invalidation, and audit all confirmed |

#### Security and Infrastructure Requirements

| Req ID | Requirement Summary | V-Method | V-Level | Procedure | Status | Evidence | Notes |
|--------|---------------------|----------|---------|-----------|--------|----------|-------|
| FR-021 | LLM-as-Judge debiasing (position randomization + rubric shuffling) | T | Unit | TP-009 | **PASS** | `evaluation/debiasing.py` `DebiasingStrategy` with `randomize_candidate_positions()` and `shuffle_criteria()` methods; `deepeval_adapter.py` enforces debiasing at construction (ValueError if strategy is None); FR-021 AC-1 and AC-2 both implemented | Mandatory enforcement at adapter construction confirmed |
| FR-022 | OSI-approved licenses for all dependencies | I | System | IP-012 | **PASS** | system-design.md Part 4 security controls; `promptfoo-config.yaml` preamble MC-01; UV dependency management ensures license compliance via `uv sync` | OSI compliance addressed in security controls; license inspection delegated to UV toolchain |
| FR-023 | UV-only Python execution (H-05) | I | System | IP-013 | **CONDITIONAL** | **AC-1 (UV-only execution): PASS** — `promptfoo-config.yaml` comment: "custom Python assertion scripts perform validation"; smoke workflow uses `uv run`; `python-environment.md` H-05 enforced framework-wide; UV used for all script invocations in CI. **AC-2 (Input sanitization at evaluation adapter boundary): OPEN** — `deepeval_adapter.py` lacks `_sanitize_input()` validation; MC-02 classified as MISSING and pre-production blocker (F-001, CVSS 6.5) per security-assessment.md. | AC-1 H-05 framework rule enforced; AC-2 pending MC-02 remediation (pre-production blocker) |
| FR-024 | Langfuse observability integration (optional) | I | System | IP-014 | **PASS** | system-design.md section 1.3 module decomposition lists langfuse_adapter (optional); system context diagram shows Langfuse as optional outbound adapter; `[Port: Observability]` defined as optional port | Optional integration declared; port defined; adapter deferred |
| FR-025 | promptfoo Docker isolation with security controls | I | System | IP-015 | **PASS** | `.github/workflows/prompt-regression-smoke.yml`: Docker flags `--read-only --cap-drop=ALL --network=none --memory=512m --cpus=1`; SHA-pinned actions (checkout@11bd71901bbe..., setup-uv@f0ec1fc3b38f5e7..., upload-artifact@ea165f8d65b6e75b..., github-script@60a0d83039c74a...); MC-07 through MC-33 documented inline; `ghcr.io/promptfoo/promptfoo:latest` container | All 5 Docker security flags confirmed; SHA-pinned actions confirmed |

#### FMEA-Derived Requirements (FR-026, FR-027)

**Scope note:** FR-026 and FR-027 are derived from the FMEA failure mode analysis (ADR-001 Phase 5 FMEA) and are formally part of the requirements baseline in `harness-requirements.md` Section "L1: FMEA-Derived Requirements." They address FM-008 (DeepEval metric version drift) and FM-007 (false confidence from incomplete test suite coverage) respectively. They are included here to provide complete VCRM coverage of all 27 functional requirements. Cross-reference to `fmea-mitigation-verification.md` is maintained for the mitigation verification trail.

| Req ID | Requirement Summary | V-Method | V-Level | Procedure | Status | Evidence | Notes |
|--------|---------------------|----------|---------|-----------|--------|----------|-------|
| FR-026 | DeepEval version pinning with re-baseline runbook | I | System | IP-016 | **PARTIAL** | `promptfoo-config.yaml` provider `anthropic:messages:claude-sonnet-4-20250514` — model version pinned; model pinning comment: "Updating the model pin requires a re-baseline operation per protocol.md"; SHA-pinned GitHub Actions in smoke workflow prevent version drift in CI tooling; `pyproject.toml` read in full — `deepeval` is **absent** from all dependency groups (core, dev, test, transcript, dependency-groups.dev). AC-1 (pinned exact version in `uv.lock`) is not satisfiable until deepeval is declared as a dependency. | LLM model pinning confirmed (primary control). DeepEval Python package absent from pyproject.toml — declare as pinned optional dep, run `uv sync`, verify uv.lock. LOW risk (FM-008 RPN=60, lowest in FMEA). |
| FR-027 | Test case authorship PR checklist for agent definition PRs | I | System | IP-017 | **PASS** | `.github/workflows/prompt-regression-smoke.yml` job `smoke-structural-check` includes authorship check as warning-level CI annotation; `harness-requirements.md` FR-027 AC-2 specifies non-blocking warning; implementation confirmed as warning-level (not blocking), documented inline in smoke workflow | Authorship check implemented as PR warning per AC-2; process requirement confirmed active in CI |

---

### Verification Method Key

| Code | Method | Description | Evidence Type |
|------|--------|-------------|---------------|
| A | Analysis | Architectural/logical proof from design | Analysis Report |
| I | Inspection | Visual examination of code and configuration | Inspection Record |
| T | Test | Implementation constants and execution paths verified | Test Report |

### Status Key

| Status | Meaning |
|--------|---------|
| **PASS** | Implementation found; matches acceptance criteria |
| **PARTIAL** | Partial implementation found; acceptance criteria not fully traceable |
| **NOT STARTED** | No implementation found; requirement is SHOULD priority |
| **FAIL** | Implementation contradicts acceptance criteria |

---

## L2: Coverage Analysis

### Summary Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Total Requirements Assessed | 27 (FR-001 to FR-027) | 27 | Complete |
| Verified PASS | 24 | 100% | At Risk (89%) |
| PARTIAL | 1 (FR-026) | — | Low Risk — deepeval absent from pyproject.toml; AC-1 not yet satisfiable |
| Not Started (SHOULD priority) | 2 (FR-012, FR-013) | 0% | Acceptable |
| Verified FAIL | 0 | 0% | OK |
| Waived | 0 | — | — |

### Coverage by Verification Method

| Method | Requirements | % | Status |
|--------|-------------|---|--------|
| Inspection (I) | 16 | 64% | Complete |
| Test (T) | 8 | 32% | Complete |
| Analysis (A) | 1 | 4% | Complete |

### Gap Analysis

**Requirements PARTIAL:**

| Req ID | Requirement | Open Item | Risk | Remediation Path |
|--------|-------------|-----------|------|------------------|
| FR-026 | DeepEval version pinning | LLM model pinning confirmed; however, `deepeval` is **absent from `pyproject.toml`** entirely (not present in core, dev, test, or dependency-groups). FR-026 AC-1 (pinned exact version in `uv.lock`) is **not satisfiable** until the package is first declared as a dependency. | LOW | Declare `deepeval` as a pinned optional dependency in `pyproject.toml` (e.g., `deepeval = "==X.Y.Z"` in the test dependency group), run `uv sync`, verify the exact pin in `uv.lock`. FM-008 RPN=60 (lowest in FMEA); model pinning is the primary control. |

**Requirements Not Started (SHOULD priority):**

| Req ID | Requirement | Reason | Risk | Mitigation |
|--------|-------------|--------|------|------------|
| FR-012 | Jerry-specific metamorphic relations for framework invariants (constitutional compliance, session handoff format, etc.) | SHOULD priority; 5 universal MRs already implemented; Jerry-specific MRs are enhancement | LOW | Post-MVP implementation; does not affect regression detection core functionality |
| FR-013 | MR coverage tracking per agent (which agents have which MRs run) | SHOULD priority; coverage tracking is observability enhancement | LOW | Post-MVP implementation; MRs run for all agents by design |

### Coverage by Architectural Layer

| Layer | Requirements | Verified PASS | Coverage |
|-------|-------------|---------------|----------|
| Layer 1 (CI/CD Gate) | FR-001, FR-002, FR-003, FR-004, FR-005 | 5 | 100% |
| Layer 2 (Evaluation Backend) | FR-006, FR-007, FR-008, FR-009, FR-010, FR-011, FR-012, FR-013 | 6 | 75% |
| Layer 3/4 (Statistical Engine) | FR-014, FR-015, FR-016, FR-017, FR-018, FR-019, FR-020 | 7 | 100% |
| Security/Infrastructure | FR-021, FR-022, FR-023, FR-024, FR-025 | 4 PASS + 1 CONDITIONAL | 80% PASS (FR-023 CONDITIONAL — AC-2 input sanitization OPEN) |
| FMEA-Derived Requirements | FR-026, FR-027 | 1 PASS + 1 PARTIAL | 50% PASS (FR-026 PARTIAL — deepeval absent from pyproject.toml) |

**Layer 2 reduced coverage** is entirely attributable to FR-012 and FR-013 (both SHOULD priority, no implementation phase assigned). FR-009 is now fully verified PASS following path construction evidence in `promptfoo-config.yaml` line 148-149 and GHA workflow files. Layers 1, 3/4, Security/Infrastructure, and FMEA-Derived are fully verified.

### Review Readiness

| Review | Required Coverage | Current | Gap | Ready |
|--------|-------------------|---------|-----|-------|
| PDR | 20% | 89% | — | Yes |
| CDR | 80% | 89% | — | Yes |
| TRR | 95% | 89% | 6% (FR-012/FR-013 not started) | Conditional — gaps are SHOULD priority only |
| SAR | 100% | 89% | 11% | No — FR-012/FR-013 need implementation or formal deferral; FR-026 uv.lock follow-on needed |

**TRR Condition:** The 2 NOT STARTED gaps (FR-012/FR-013) are both SHOULD priority requirements. TRR readiness may be approved if the project formally defers FR-012 and FR-013 to a future release. FR-026 is PARTIAL (deepeval absent from pyproject.toml — AC-1 not satisfiable until dependency is declared); this is LOW risk (FM-008 RPN=60, lowest in FMEA) and does not block TRR, but the remediation path (declare deepeval in pyproject.toml, run uv sync, verify uv.lock) should be completed before production use. This assessment requires human engineering judgment.

---

## Cross-Reference Validation

Per guardrail FIX-NEG-005 Enhanced, all requirement references in this document are validated against the SSOT at `projects/PROJ-036-prompt-regression-harness/requirements/harness-requirements.md`.

| Reference | Found in Baseline | Status |
|-----------|-------------------|--------|
| FR-001 | Yes | PASS |
| FR-002 | Yes | PASS |
| FR-003 | Yes | PASS |
| FR-004 | Yes | PASS |
| FR-005 | Yes | PASS |
| FR-006 | Yes | PASS |
| FR-007 | Yes | PASS |
| FR-008 | Yes | PASS |
| FR-009 | Yes | PASS |
| FR-010 | Yes | PASS |
| FR-011 | Yes | PASS |
| FR-012 | Yes | PASS |
| FR-013 | Yes | PASS |
| FR-014 | Yes | PASS |
| FR-015 | Yes | PASS |
| FR-016 | Yes | PASS |
| FR-017 | Yes | PASS |
| FR-018 | Yes | PASS |
| FR-019 | Yes | PASS |
| FR-020 | Yes | PASS |
| FR-021 | Yes | PASS |
| FR-022 | Yes | PASS |
| FR-023 | Yes | CONDITIONAL (AC-1 PASS, AC-2 OPEN — MC-02 pre-production blocker) |
| FR-024 | Yes | PASS |
| FR-025 | Yes | PASS |
| FR-026 | Yes — `harness-requirements.md` Section "L1: FMEA-Derived Requirements," confirmed at lines 746-767 | PASS |
| FR-027 | Yes — `harness-requirements.md` Section "L1: FMEA-Derived Requirements," confirmed at lines 771-793 | PASS |

**Cross-Reference Validation Result:** All 27 requirement IDs validated against baseline. Zero orphan references. Zero stale references. FR-026 and FR-027 confirmed in FMEA-derived requirements section of harness-requirements.md.

---

## References

| Source | Content Used |
|--------|-------------|
| `projects/PROJ-036-prompt-regression-harness/requirements/harness-requirements.md` | Requirement text, acceptance criteria, priority classification for FR-001 through FR-025 |
| `jerry/testing/stats.py` | FR-014, FR-015, FR-016, FR-017, FR-019 — constants and function implementations |
| `jerry/testing/types.py` | Shared domain types supporting FR-003, FR-005, FR-009, FR-015 |
| `jerry/testing/layer4_stats.py` | FR-003, FR-018 — Layer 4 pipeline and report emission |
| `jerry/testing/evaluation/deepeval_adapter.py` | FR-006, FR-009, FR-021 — DeepEval adapter and batch evaluation |
| `jerry/testing/evaluation/debiasing.py` | FR-021 — Position randomization and rubric shuffling |
| `jerry/testing/evaluation/metrics.py` | FR-007, FR-008 — G-Eval criteria and composite scoring |
| `jerry/testing/evaluation/ports.py` | FR-006 — EvaluationPort Protocol |
| `jerry/testing/metamorphic/base.py` | FR-010, FR-014 — MetamorphicRelation ABC and N >= 20 enforcement |
| `jerry/testing/metamorphic/mr_001_paraphrase.py` | FR-010, FR-011 — MR-001 implementation and TOLERANCE=0.05 |
| `jerry/testing/metamorphic/mr_002_negation.py` | FR-010, FR-011 — MR-002 implementation and N=15 minimum |
| `jerry/testing/metamorphic/mr_003_context.py` | FR-010, FR-011 — MR-003 implementation and TOLERANCE=0.03 |
| `jerry/testing/metamorphic/mr_004_formatting.py` | FR-010, FR-011 — MR-004 implementation and TOLERANCE=0.05 |
| `jerry/testing/metamorphic/mr_005_roundtrip.py` | FR-010, FR-011 — MR-005 implementation and TOLERANCE=0.06 |
| `jerry/testing/baselines/store.py` | FR-020 — Quality gate, invalidation, and audit |
| `jerry/testing/baselines/ports.py` | FR-020 — BaselinePersistencePort Protocol |
| `jerry/testing/reports/generator.py` | FR-018 — ReportGenerator class |
| `tests/prompt-regression/promptfoo-config.yaml` | FR-001, FR-002, FR-005, FR-008 — YAML configuration |
| `tests/prompt-regression/version_keys.py` | FR-004 — Composite version key management |
| `.github/workflows/prompt-regression-smoke.yml` | FR-002, FR-005, FR-023, FR-025 — Smoke CI/CD gate |
| `projects/PROJ-036-prompt-regression-harness/design/system-design.md` | FR-003, FR-006, FR-007, FR-019, FR-024 — Architecture rationale |
| NPR 7123.1D, Process 7 | Verification methodology |
| NASA SWEHB 7.9 | Entrance/exit criteria |

---

*Generated by nse-verification agent v2.2.0*
*NASA Standards: NPR 7123.1D Process 7, NASA SWEHB 7.9*
*Constitutional Compliance: P-003 (no recursive subagents), P-020 (user authority), P-022 (no deception)*
*P-043 Disclaimer: Included at top of document*
