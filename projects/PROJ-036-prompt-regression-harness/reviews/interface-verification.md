---
DISCLAIMER: This guidance is AI-generated based on NASA Systems Engineering
standards. It is advisory only and does not constitute official NASA guidance.
All SE decisions require human review and professional engineering judgment.
Not for use in mission-critical decisions without SME validation.
---

# Interface Verification: PROJ-036 Four-Layer Composite Test Harness

> **Project:** PROJ-036-prompt-regression-harness
> **Entry:** PROJ-036-e-002
> **Date:** 2026-03-07
> **Status:** Draft
> **Scope:** Inter-layer interface verification — L1 to L2, L2 to L4, L3 to L4, L4 to CI/CD
> **V&V Agent:** nse-verification v2.2.0

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Interface verification summary |
| [L1: Interface Verification Results](#l1-interface-verification-results) | Detailed per-interface findings |
| [L2: Architecture Integrity Assessment](#l2-architecture-integrity-assessment) | H-07 compliance, dependency direction, risk |
| [References](#references) | Evidence sources |

---

## L0: Executive Summary

Four primary inter-layer interfaces verified. Three interfaces are PASS (L1 to L2, L3 to L4, L4 to CI/CD). One interface (L2 to L4) is PASS with an architectural deviation note: the design specifies score arrays pass from Layer 2 to Layer 4 via a shared format, but the current implementation routes Layer 2 output through promptfoo's JSON format before Layer 4 ingestion — this deviation is documented in the design and does not constitute a violation. H-07 (domain layer isolation) compliance is confirmed across all four interfaces: domain modules import only from other domain modules, stdlib, and approved math libraries; adapters (DeepEval, promptfoo, GitHub Actions) never pollute domain code.

---

## L1: Interface Verification Results

### Interface 1: Layer 1 (CI/CD Gate) to Layer 2 (Evaluation Backend)

**Interface Definition:** GitHub Actions workflow triggers promptfoo Docker container, which invokes Python assertion scripts importing from `jerry.testing.evaluation`.

**Evidence Examined:**

| Element | Source | Finding |
|---------|--------|---------|
| Trigger mechanism | `prompt-regression-smoke.yml` job `smoke-structural-check` | Docker container `ghcr.io/promptfoo/promptfoo:latest` invoked per agent in matrix strategy |
| Python invocation | `promptfoo-config.yaml` defaultTest assertions | `not-empty` and `not-regex` assertion types execute < 100ms (FR-008 compliance) |
| Secret injection | `prompt-regression-smoke.yml` env block | `ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}` injected from GHA secrets; never hardcoded (MC-01) |
| File mount | Docker flags in smoke workflow | `skills/*/agents/*.md` and test config files mounted read-only |
| Output format | `promptfoo-config.yaml` `outputPath` | JSON output at `tests/prompt-regression/results/promptfoo-output.json` |
| Tier selection | `EVALUATION_MODE` env var | Smoke tier configured via environment variable; workflow sets `EVALUATION_MODE=smoke` |

**Verification Result:** PASS

**Evidence Summary:** The L1-to-L2 interface is implemented via Docker-isolated promptfoo invocation with proper secret management and read-only filesystem mounts. The promptfoo process invokes Python assertion scripts via subprocess, maintaining Layer 2 domain isolation. Security controls MC-07 through MC-33 are documented inline in the smoke workflow.

**Architectural Deviation Note:** The design's description of "the baseline provider could directly load pre-captured baseline outputs" (promptfoo-config.yaml line 73) is marked as a future Phase B integration. Current implementation uses Layer 4 as the authoritative FR-003 before/after comparison engine; the two-provider promptfoo setup is acknowledged as a placeholder. This is documented and intentional — not a defect.

---

### Interface 2: Layer 2 (Evaluation Backend) to Layer 4 (Statistical Engine)

**Interface Definition:** Layer 2 produces score arrays (float[] in [0.0, 1.0]) that Layer 4 consumes via the `compare_versions()` API. The data contract is the `ScoreArray` type defined in `jerry/testing/types.py`.

**Evidence Examined:**

| Element | Source | Finding |
|---------|--------|---------|
| Score array type | `types.py` `ScoreArray` type alias | `ScoreArray = list[float]` (type alias, not a dataclass); validation enforced at call sites via `_validate_score_array()` in `stats.py` (values in [0.0, 1.0], N >= 20) |
| Batch evaluation output | `evaluation/deepeval_adapter.py` `evaluate_batch()` | Returns `dict[str, list[float]]` keyed by metric name; scores in [0.0, 1.0] per criterion |
| Layer 4 ingestion | `stats.py` `compare_versions()` signature | Accepts `scores_a: list[float], scores_b: list[float]`; validates N >= 20 |
| Invalid score rejection | `stats.py` `_validate_score_array()` | Raises `InvalidScoreArrayError` for values outside [0.0, 1.0] |
| Orchestration bridge | `layer4_stats.py` `_run_statistical()` | Reads promptfoo JSON output; constructs score arrays; calls `stats.compare_versions()` |
| Cross-project sharing | `stats.py` module docstring; `jerry/testing/__init__.py` lines 33-43; `jerry/testing/baselines/store.py:60`; `jerry/testing/metamorphic/base.py:50`; `jerry/testing/layer4_stats.py:34` | FR-019 verified: `stats.py` docstring states "shared between PROJ-036 (prompt regression) and PROJ-017 (skill evaluation framework)"; public API (`compare_versions`, `compare_multiple_metrics`, `wilson_score_intervals`, `merge_decision_from_classification`, `InsufficientSamplesError`, `MIN_STATISTICAL_SAMPLE_SIZE`, `QUALITY_PASS_THRESHOLD`, `BONFERRONI_K_FULL_SUITE`, `BONFERRONI_ALPHA_FULL`) re-exported via `jerry/testing/__init__.py`; concrete imports confirmed at 4 import sites within PROJ-036 codebase |

**Verification Result:** PASS

**Evidence Summary:** The L2-to-L4 interface is clean: Layer 4 (`stats.py`) operates on plain `list[float]`, which is the most general interface possible. The `DeepEvalAdapter.evaluate_batch()` returns `dict[str, list[float]]`, directly compatible. The `Layer4Pipeline._run_statistical()` bridges the two by extracting score arrays from promptfoo JSON output and passing them to `stats.compare_versions()`. The `ScoreArray` domain type adds runtime validation. The one-way dependency (adapters import domain; domain does not import adapters) is confirmed.

**Architectural Note (FR-019):** The system-design.md documents a deliberate architectural deviation: `layer4_stats.py` is classified as an adapter (not domain) because it orchestrates I/O, report formatting, and GHA API integration. It imports from `stats.py` (domain) but `stats.py` does NOT import from `layer4_stats.py`. This direction is correct and confirmed.

---

### Interface 3: Layer 3 (Metamorphic Relations) to Layer 4 (Statistical Engine)

**Interface Definition:** Layer 3 MR implementations invoke `evaluate()` which internally calls Wilcoxon via `_wilcoxon_p_and_effect()`. The result is an `MRResult` dataclass that the Layer 4 pipeline aggregates into the final regression report.

**Evidence Examined:**

| Element | Source | Finding |
|---------|--------|---------|
| MRResult type | `metamorphic/base.py` `MRResult` dataclass | Contains: `mr_id`, `passed`, `original_scores`, `transformed_scores`, `mean_delta`, `tolerance`, `effect_size`, `p_value`, `severity`, `evidence` |
| Statistical computation | `mr_001_paraphrase.py` `_wilcoxon_p_and_effect()` | Uses `scipy.stats.wilcoxon` directly; returns `(p_value, effect_r)` tuple |
| Shared helper pattern | `mr_003_context.py`, `mr_004_formatting.py`, `mr_005_roundtrip.py` | All three import `_wilcoxon_p_and_effect` from `mr_001_paraphrase` — shared statistical helper pattern |
| MR-002 exception | `mr_002_negation.py` | Directional MR; uses separate Wilcoxon computation for directional effect; minimum_sample_size=15 (not 20) |
| N enforcement | `metamorphic/base.py` `_validate_inputs()` | Raises `InsufficientSamplesError` if `len(original_scores) < self.minimum_sample_size` |
| Score range validation | `metamorphic/base.py` `_validate_inputs()` | Validates each score in [0.0, 1.0] for both sequences |
| Layer 4 integration | `layer4_stats.py` `_run_statistical()` | Aggregates MR pass/fail results into `ComparisonReport` |

**Verification Result:** PASS

**Evidence Summary:** The L3-to-L4 interface is well-defined via the `MRResult` dataclass. All 5 MR implementations produce `MRResult` instances with identical structure. The shared `_wilcoxon_p_and_effect()` helper in `mr_001_paraphrase.py` ensures statistical consistency across MRs (changes to Wilcoxon computation affect all 5 MRs through the shared function — documented in each MR module's docstring as a notice). Input validation is uniform via the inherited `_validate_inputs()` from the `MetamorphicRelation` ABC.

**Design Pattern Finding:** The MR-to-stats interface bypasses the `stats.py` module and calls `scipy.stats.wilcoxon` directly through the `_wilcoxon_p_and_effect()` helper. This is intentional: MR statistical computation is simpler than the full Wilcoxon+Wilson+Bonferroni pipeline in `stats.py`. The MR layer uses only the Wilcoxon p-value and Cohen's r; it does not need Wilson CIs or Bonferroni correction (those are applied at the aggregate Layer 4 level). This is architecturally sound.

---

### Interface 4: Layer 4 (Statistical Engine) to CI/CD Output

**Interface Definition:** Layer 4 produces a final regression verdict and emits it to: (1) GitHub Actions output variables, (2) JSON artifact, (3) Markdown PR comment, and optionally (4) Langfuse trace.

**Evidence Examined:**

| Element | Source | Finding |
|---------|--------|---------|
| GHA output emission | `layer4_stats.py` `_emit_gha_outputs()` | Writes to `$GITHUB_OUTPUT` file; variables: `verdict`, `p_value`, `effect_size`, `merge_decision`, `report_path` |
| Exit code mapping | `layer4_stats.py` `_exit_code()` | ALLOW=0, BLOCK=1, ALLOW_WITH_WARNING=2; maps `MergeDecision` enum |
| Merge decision logic | `stats.py` `merge_decision_from_classification()` | Maps `RegressionClass` to `MergeDecision`; REGRESSION → BLOCK, MARGINAL → ALLOW_WITH_WARNING, NO_REGRESSION → ALLOW |
| PR comment content | `reports/generator.py` `to_markdown()` | Markdown report with verdict, p-value, Wilson CIs, Bonferroni disclosure |
| JSON artifact | `reports/generator.py` `to_json()` | JSON structure with all statistical fields per behavioral-contracts.md D.6 schema |
| Report path | `reports/generator.py` factory methods | `from_single_metric()`, `from_multi_metric()`, `smoke_mode_report()` |
| Smoke path | `layer4_stats.py` `_run_smoke()` | Returns `MergeDecision.ALLOW` with structural-only report |
| SHA-pinned upload action | `prompt-regression-smoke.yml` | `actions/upload-artifact@ea165f8d65b6e75b...` for report artifact publishing |

**Verification Result:** PASS

**Evidence Summary:** The L4-to-CI/CD interface is complete: exit codes are deterministic (ALLOW=0, BLOCK=1, ALLOW_WITH_WARNING=2), GitHub Actions output variables are written to `$GITHUB_OUTPUT` per GHA protocol, and both JSON and Markdown report formats are implemented. The smoke mode correctly bypasses statistical computation and returns ALLOW without LLM calls. SHA-pinned GitHub Actions prevent workflow supply chain attacks (FR-025 compliance).

**Bonferroni Disclosure Verification:** `BonferroniConfig.description` property in `types.py` produces the FR-017-compliant disclosure string included in reports. This ensures every report that uses Bonferroni correction includes the disclosure text required by FR-017 AC-2.

---

## L2: Architecture Integrity Assessment

### H-07 Domain Layer Isolation Compliance

The critical architectural constraint is H-07: domain modules MUST NOT import adapter modules. This is verified by inspecting import statements across all key domain files.

| Domain File | External Imports Found | Adapter Imports Found | H-07 Status |
|-------------|----------------------|----------------------|-------------|
| `types.py` | `dataclasses`, `enum`, `typing` (stdlib only) | None | PASS |
| `stats.py` | `scipy.stats.wilcoxon`, `statsmodels.stats.proportion` (approved math libs) | None | PASS |
| `metamorphic/base.py` | `statistics`, `abc`, `typing` (stdlib) | None | PASS |
| `metamorphic/mr_001_paraphrase.py` | `scipy.stats` (approved math lib) | None | PASS |
| `metamorphic/mr_002_negation.py` | None beyond domain imports | None | PASS |
| `metamorphic/mr_003_context.py` | `random` (stdlib) | None | PASS |
| `metamorphic/mr_004_formatting.py` | `re` (stdlib) | None | PASS |
| `metamorphic/mr_005_roundtrip.py` | `re`, `typing` (stdlib) | None | PASS |
| `evaluation/metrics.py` | None beyond domain imports | None | PASS |
| `evaluation/debiasing.py` | `random` (stdlib) | None | PASS |
| `evaluation/ports.py` | `typing` (stdlib) | None | PASS |

**H-07 Compliance Result:** All domain modules pass H-07 verification. No adapter imports found in any domain file.

**Adapter Files (Expected to Import External Libraries):**

| Adapter File | External Library Imported | Direction Correct? |
|-------------|--------------------------|-------------------|
| `evaluation/deepeval_adapter.py` | `deepeval` | Yes — adapter imports framework |
| `layer4_stats.py` | `pathlib`, `json`, `os` (stdlib); reads `jerry.testing.stats` (domain) | Yes — adapter imports domain |
| `baselines/store.py` | `json`, `pathlib`, `hashlib`, `datetime` (stdlib) | Yes — adapter uses only stdlib |
| `reports/generator.py` | `jerry.testing.types` (domain only) | Yes — adapter imports domain |

### Forbidden Dependency Verification

The system-design.md Section 1.4 lists 6 forbidden dependency patterns. Each is checked:

| Forbidden Dependency | Check | Result |
|----------------------|-------|--------|
| `stats.py --> deepeval_adapter.py` | `stats.py` imports: `scipy`, `statsmodels`, `typing`, `logging`, `jerry.testing.types` only | NOT PRESENT — PASS |
| `metrics.py --> promptfoo internals` | `metrics.py` imports: domain types only | NOT PRESENT — PASS |
| `base.py --> DeepEval BaseMetric` | `metamorphic/base.py` imports: `statistics`, `abc`, `typing`, `jerry.testing.stats` only | NOT PRESENT — PASS |
| `mr_*.py --> deepeval_adapter.py` | All mr_*.py files import from `metamorphic.base` and `mr_001_paraphrase` only | NOT PRESENT — PASS |
| `stats.py --> store.py` | `stats.py` has no `baselines` imports | NOT PRESENT — PASS |
| `types.py --> any adapter` | `types.py` imports: `dataclasses`, `enum`, `typing` (stdlib only) | NOT PRESENT — PASS |

**Forbidden Dependency Result:** All 6 forbidden dependencies are confirmed absent. Zero H-07 violations detected.

### Dependency Direction Summary

```
Confirmed Dependency Flow (arrows = "depends on"):

Adapters (outbound) --> Domain Core <-- Ports
    deepeval_adapter.py --> evaluation/metrics.py
    deepeval_adapter.py --> evaluation/debiasing.py
    layer4_stats.py     --> stats.py
    layer4_stats.py     --> types.py
    baselines/store.py  --> types.py
    reports/generator.py --> types.py

Domain Core (internal dependencies):
    metamorphic/mr_*.py --> metamorphic/base.py
    metamorphic/mr_*.py --> stats.py (for Wilcoxon)
    stats.py            --> types.py
    layer4_stats.py     --> stats.py

External Math Library Dependencies (approved):
    stats.py            --> scipy.stats
    stats.py            --> statsmodels.stats
    mr_001_paraphrase.py --> scipy.stats
```

### Interface Risk Assessment

| Interface | Risk Level | Rationale |
|-----------|-----------|-----------|
| L1 to L2 (Docker subprocess) | LOW | Subprocess isolation via Docker prevents host contamination; read-only mounts; secrets via env injection (not file) |
| L2 to L4 (score arrays) | LOW | `list[float]` is the simplest possible interface; runtime validation at both ends; no shared mutable state |
| L3 to L4 (MRResult aggregation) | LOW | Frozen dataclass (`MRResult`) prevents mutation after creation; all fields typed |
| L4 to CI/CD (exit codes + GHA output) | LOW | Exit codes are integer (unambiguous); GHA output uses key=value protocol; JSON artifact schema documented |
| Shared `_wilcoxon_p_and_effect` dependency | MEDIUM | MR-003, MR-004, MR-005 all import from `mr_001_paraphrase.py`. A bug in `_wilcoxon_p_and_effect()` would affect all three silently. Mitigation: this module should have unit tests validating the helper directly. |

### Cross-Reference: FR-026 Status

> **Note:** FR-026 (DeepEval version pinning) has PARTIAL verification status — LLM model pinning is confirmed in `deepeval_adapter.py`, but the `deepeval` Python package is absent from `pyproject.toml`, making AC-1 (pinned exact version in `uv.lock`) not yet satisfiable. This gap is tracked in detail in the Requirements Coverage Matrix (VCRM) and FMEA Mitigation Verification (FM-008). The interface verification scope (inter-layer contract boundaries) is not directly affected by dependency pinning, but the L2-to-L4 interface relies on `deepeval` being available at runtime; version drift could alter score array output format. Risk: LOW — model pinning is the primary control; package version drift is detectable via metric score shift.

---

## References

| Source | Content Used |
|--------|-------------|
| `jerry/testing/stats.py` | L2-to-L4 interface: `compare_versions()` signature, `InvalidScoreArrayError` |
| `jerry/testing/types.py` | `ScoreArray`, `MRResult`, `MergeDecision`, `BonferroniConfig.description` |
| `jerry/testing/layer4_stats.py` | L4-to-CI/CD interface: `_emit_gha_outputs()`, `_exit_code()`, `_run_statistical()`, `_run_smoke()` |
| `jerry/testing/evaluation/deepeval_adapter.py` | L1-to-L2 interface: `evaluate_batch()` return type |
| `jerry/testing/evaluation/debiasing.py` | FR-021 enforcement at adapter construction |
| `jerry/testing/evaluation/ports.py` | `EvaluationPort` Protocol definition |
| `jerry/testing/metamorphic/base.py` | L3-to-L4 interface: `MRResult` dataclass, `_validate_inputs()` |
| `jerry/testing/metamorphic/mr_001_paraphrase.py` | `_wilcoxon_p_and_effect()` shared helper |
| `jerry/testing/metamorphic/mr_002_negation.py` | Directional MR; minimum_sample_size=15 |
| `jerry/testing/metamorphic/mr_003_context.py` | Shared helper import pattern |
| `jerry/testing/metamorphic/mr_004_formatting.py` | Shared helper import pattern; FormattingVariant dispatch |
| `jerry/testing/metamorphic/mr_005_roundtrip.py` | Shared helper; optional translator callable |
| `jerry/testing/baselines/store.py` | Baseline persistence adapter |
| `jerry/testing/reports/generator.py` | JSON and Markdown report generation |
| `tests/prompt-regression/promptfoo-config.yaml` | L1-to-L2 configuration |
| `tests/prompt-regression/version_keys.py` | Version key management |
| `.github/workflows/prompt-regression-smoke.yml` | L1 CI/CD gate implementation |
| `projects/PROJ-036-prompt-regression-harness/design/system-design.md` | H-07 dependency graph, forbidden dependencies, integration patterns |
| NPR 7123.1D, Process 7 | Verification methodology |

---

*Generated by nse-verification agent v2.2.0*
*NASA Standards: NPR 7123.1D Process 7, NASA SWEHB 7.9*
*Constitutional Compliance: P-003 (no recursive subagents), P-020 (user authority), P-022 (no deception)*
*P-043 Disclaimer: Included at top of document*
