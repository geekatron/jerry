# Quality Gate 2 — Implementation Consistency Barrier Score (Iter 2)

## L0 Executive Summary

**Gate:** QG-2 — Implementation Consistency | **Verdict:** REVISE | **Threshold:** 0.95
**Composite Score:** 0.940/1.00 | **Weakest Dimension:** Structural Alignment (0.905)
**One-line assessment:** All four iter1 critical gaps are resolved — single `InsufficientSamplesError`
class, `version_keys.py` exists and fully implements FR-004, three mode-specific CI/CD workflow files
present and coherent, STANDARD N accumulation protocol documented — raising the score from 0.882 to
0.940; the remaining gap below the 0.95 barrier threshold is residual structural debt (peer module
coupling, H-10 multi-type grouping in `base.py`) and one architectural wire-up gap (Layer 3 → Layer 4
MR-to-ScoreArray conversion path not visible in delivered files).

---

## Scoring Context

- **Deliverable:** `projects/PROJ-036-prompt-regression-harness/` (all five implementation streams)
- **Deliverable Type:** Implementation (multi-stream)
- **Criticality Level:** C4
- **Threshold:** 0.95 (barrier gate — stricter than S-014's 0.92 for cross-stream consistency)
- **Gate Pattern:** sync_barrier (cross-deliverable consistency scoring)
- **Scoring Strategy:** S-014 LLM-as-Judge with 4-dimension barrier rubric
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-03-07T00:00:00Z
- **Prior Score:** iter1 = 0.882 REVISE (2026-03-07)
- **Debiasing applied:** Yes — each dimension scored independently before composite computed

---

## Iter2 Gap Resolution Status

| Gap | Iter1 Finding | Iter2 Status | Evidence |
|-----|--------------|--------------|---------|
| Gap 1 — `InsufficientSamplesError` dual class | Two incompatible classes in `stats.py` and `base.py` with different constructors | **RESOLVED** | `base.py` line 50: `from jerry.testing.stats import InsufficientSamplesError`. No `class InsufficientSamplesError` definition in `base.py`. Single canonical class confirmed in `stats.py` lines 99-108. |
| Gap 2 — `version_keys.py` absent | File cited in `promptfoo-config.yaml` but did not exist | **RESOLVED** | `tests/prompt-regression/version_keys.py` exists — 671 lines implementing FR-004 fully: `VersionKey`, `VersionKeyRegistry`, `build_version_key()`, `validate_baseline_version_key()`, `get_current_commit_hash()`, `get_file_last_commit_hash()`, `compute_prompt_content_hash()`, `BaselineMismatchError`. |
| Gap 3 — CI/CD workflow absent | `.github/workflows/prompt-regression.yml` not found | **RESOLVED** | Three mode-specific files delivered: `prompt-regression-smoke.yml` (Tier 1, 376 lines), `prompt-regression-standard.yml` (Tier 2, 600 lines), `prompt-regression-full.yml` (Tier 3, 509 lines). `promptfoo-config.yaml` updated to reference all three. |
| Gap 4 — N accumulation protocol undocumented | How STANDARD N=10 batches accumulate to N≥20 not specified anywhere | **RESOLVED** | Protocol documented in `baselines/store.py` module docstring (lines 26-42, 5-step protocol) and in `stats.py` `compare_versions()` docstring (lines 547-554). |

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.940 |
| **Threshold** | 0.95 (barrier gate) |
| **Verdict** | REVISE |
| **Iter1 Score** | 0.882 |
| **Score Delta** | +0.058 |
| **Stream scores incorporated** | Yes — 5 streams read in full |
| **Missing deliverables detected** | 0 (all iter1 missing deliverables now present) |
| **Remaining gaps** | 3 (structural debt, H-10 multi-type grouping, Layer 3→4 wire-up gap) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Terminological Consistency | 0.25 | 0.960 | 0.240 | Single `InsufficientSamplesError` in `stats.py`; `version_keys.py` now exists implementing FR-004 with `VersionKey`, `VersionKeyRegistry`, format `{hash}:{path}` consistently; all terminology from iter1 still consistent |
| Structural Alignment | 0.25 | 0.905 | 0.226 | H-07/H-10/H-11 compliance strong; `mr_001_paraphrase.py` peer-import of `_wilcoxon_p_and_effect` still present; `base.py` still contains multi-type grouping (`MRViolationSeverity`, `MRResult`, `MetamorphicRelation`); `version_keys.py` introduces second `EvaluationMode` enum alongside `types.py`'s |
| Quantitative Consistency | 0.25 | 0.950 | 0.238 | N accumulation protocol now documented; all numeric constants consistent across streams; STANDARD N=10 → N≥20 accumulation path specified in both `store.py` and `stats.py` docstrings; three CI/CD workflows reference `QUALITY_PASS_THRESHOLD: "0.92"` consistently |
| Architectural Coherence | 0.25 | 0.945 | 0.236 | Three CI/CD workflows (3E) fully present with correct FR traceability; `version_keys.py` FR-004 chain complete; `store.py` imports `InsufficientSamplesError` from `stats.py`; Layer 3→4 MR-to-ScoreArray conversion path still not visible in delivered files (deepeval_adapter.py absent) |
| **TOTAL** | **1.00** | | **0.940** | |

**Arithmetic verification:**
- Terminological: 0.960 × 0.25 = 0.240
- Structural: 0.905 × 0.25 = 0.226
- Quantitative: 0.950 × 0.25 = 0.238 (rounding: 0.2375 → 0.238)
- Architectural: 0.945 × 0.25 = 0.236 (rounding: 0.23625 → 0.236)
- Sum: 0.240 + 0.226 + 0.238 + 0.236 = **0.940**
- Threshold: 0.95. Deficit: 0.010. Verdict: **REVISE**

---

## Detailed Dimension Analysis

### Terminological Consistency (0.960/1.00)

**Evidence — Resolved gaps from iter1:**

**Gap 1 RESOLVED — Single `InsufficientSamplesError`:** `stats.py` lines 99-108 defines the single canonical `class InsufficientSamplesError(ValueError)`. `base.py` line 50 imports it: `from jerry.testing.stats import InsufficientSamplesError`. The `base.py` module docstring explicitly states: "InsufficientSamplesError is imported from `jerry.testing.stats` (consolidated per QG-2 cross-stream consistency)." Grep across `jerry/testing/` confirms only one `class InsufficientSamplesError` definition. `mr_001_paraphrase.py` imports `InsufficientSamplesError` from `jerry.testing.metamorphic.base` — since `base.py` now re-exports the `stats.py` class rather than defining its own, this import chain resolves to the same canonical class. `store.py` imports from `jerry.testing.stats` directly (line 60). The metamorphic `__init__.py` re-exports `InsufficientSamplesError` from `base`, which in turn re-exports from `stats`. All callers are now using the same class.

**Gap 2 RESOLVED — `version_keys.py` now exists:** `tests/prompt-regression/version_keys.py` is a 671-line implementation of FR-004. It implements: `VersionKey` dataclass with `commit_hash` + `file_path` fields; `build_version_key()` and `get_current_commit_hash()` and `get_file_last_commit_hash()` for git integration; `validate_baseline_version_key()` for FR-004 AC-2 mismatch detection; `VersionKeyRegistry` for agent-ID-to-VersionKey caching; `BaselineMismatchError` for typed error signaling; `compute_prompt_content_hash()` as secondary integrity check. The FR-004 format `{git_commit_hash}:{file_path}` is fully implemented with path traversal protection and OWASP alignment. `promptfoo-config.yaml` now references `tests/prompt-regression/version_keys.py` (full path) — consistent with actual location.

**Evidence — Continued consistency from iter1:**
- `EvaluationMode` enum values (`SMOKE`, `STANDARD`, `FULL`) consistent across `types.py`, `stats.py`, `store.py`, `layer4_stats.py`, CI/CD workflows, and `promptfoo-config.yaml`.
- `RegressionClass` names consistent across `types.py`, `stats.py`, `layer4_stats.py`, `generator.py`.
- Version key format `"{hash}:{path}"` consistent across `types.py`, `stats.py`, `store.py`, `layer4_stats.py`, and now `version_keys.py`.
- Quality gate `0.92` consistent across `stats.py`, `store.py`, `metrics.py`, `adv-scorer.yaml`, and all three CI/CD workflows (`QUALITY_PASS_THRESHOLD: "0.92"`).

**Residual gap — Second `EvaluationMode` enum in `version_keys.py` (minor):**
`version_keys.py` defines its own `EvaluationMode(str, Enum)` with values `SMOKE = "smoke"`, `STANDARD = "standard"`, `FULL = "full"` (lines 87-97). This is a second definition of `EvaluationMode` — `types.py` already defines the canonical enum with the same values. The `version_keys.py` module does not import from `jerry.testing.types`. This creates a terminological duplication: two `EvaluationMode` classes with identical values but different identity (they are not the same object). Code that imports from both would receive different type objects. The duplication is documented (the module is in `tests/` not `jerry/testing/`, which may justify the independence), but it creates a maintainability risk if the values diverge. Score impact: -0.04.

**Improvement Path:** Import `EvaluationMode` from `jerry.testing.types` in `version_keys.py` rather than redefining it, or document explicitly why the independent definition is intentional (e.g., tests-directory module does not depend on production package at import time).

---

### Structural Alignment (0.905/1.00)

**Evidence — Continued compliance from iter1:**
- **H-07 domain isolation:** `version_keys.py` (in `tests/`) imports only stdlib (hashlib, re, subprocess, dataclasses, enum, pathlib, typing). No cross-contamination into domain layer.
- All three CI/CD workflow files use `uv run` exclusively (H-05 compliance) — verified in smoke, standard, and full workflows.
- **H-10 one class per file:** `version_keys.py` contains `VersionKey`, `BaselineVersionRecord`, `VersionKeyError`, `BaselineMismatchError`, `EvaluationMode`, `VersionKeyRegistry` in one file. For a `tests/` utility module, this is more acceptable than production code, but represents a deviation from strict H-10 interpretation. Score impact: -0.03 (tests-directory context partially mitigates; primary concern is the `VersionKeyRegistry` class which is substantial).
- **H-11 type hints + docstrings:** All public functions in `version_keys.py` carry type annotations and docstrings. All new CI/CD workflow steps are documented.

**Persistent gap — MR peer-module cross-import (same as iter1):**
`mr_003_context.py`, `mr_004_formatting.py`, and `mr_005_roundtrip.py` still import `_wilcoxon_p_and_effect` from `mr_001_paraphrase` (a private function). No fix was applied. This structural debt persists. Score impact: -0.03 (unchanged from iter1).

**Persistent gap — `base.py` multi-type grouping (same as iter1):**
`base.py` continues to define `MRViolationSeverity`, `MRResult`, and `MetamorphicRelation` in one file (plus it now imports rather than defines `InsufficientSamplesError`). Stream 3B's `evaluation/__init__.py` has separate files for each type — the metamorphic package remains less rigorous here. Score impact: -0.04 (unchanged from iter1; but base.py consolidation is now improved by removing the duplicate class definition).

**Improvement Path:** (1) Extract `_wilcoxon_p_and_effect` to `jerry/testing/metamorphic/_wilcoxon_helpers.py`. (2) Split `base.py` into per-type files per H-10 strict interpretation. (3) Consolidate `EvaluationMode` to `jerry.testing.types` import in `version_keys.py`. Lower priority than functional completeness gaps.

---

### Quantitative Consistency (0.950/1.00)

**Evidence — Gap 4 RESOLVED:**

**STANDARD mode N accumulation protocol documented:** `baselines/store.py` module docstring now contains a 5-step protocol (lines 26-42):
1. Each STANDARD invocation stores N=10 scores; FULL N≥30 guard does NOT apply to STANDARD batches.
2. Subsequent STANDARD invocations for the same key append, accumulating scores.
3. Once accumulated N ≥ 20, `compare_versions()` can perform Wilcoxon comparison.
4. If accumulated N < 20, `compare_versions()` raises `InsufficientSamplesError`, signalling caller to run additional batches.
5. FULL mode (N=30 per invocation) always satisfies the minimum in one pass.

`stats.py` `compare_versions()` docstring (lines 547-554) cross-references this protocol: "STANDARD mode produces N=10 scores per invocation. This function requires N >= 20. The caller (Layer 4 pipeline or CI workflow) MUST accumulate multiple STANDARD batches via BaselineStore before invoking this function."

The CI/CD `standard-regression` workflow handles the `INSUFFICIENT_SAMPLES` verdict at the enforcement gate step (lines 445-449): logs a warning, exits 0 (does not block merge), instructs the caller to run Full tier for statistically valid comparison. This matches the documented protocol.

**Evidence — Continued consistency from iter1:**
- N≥20 (`MIN_STATISTICAL_SAMPLE_SIZE = 20`) consistent across `stats.py`, `base.py` (inherited via ABC), all five MR implementations.
- N=30 for FULL mode (`MIN_FULL_SAMPLES = 30`) consistent in `store.py`, `baselines/ports.py`, and Full workflow env var `N_RUNS_PER_VERSION: "30"`.
- Bonferroni K=13 consistent: `stats.py` constant, `layer4_stats.py` import, Full workflow env var `BONFERRONI_K_FULL: "13"`.
- Alpha=0.05/0.004 consistent across `stats.py`, MR implementations, Standard workflow env var `STATISTICAL_ALPHA: "0.05"`.
- Quality gate 0.92 consistent: Standard workflow `QUALITY_PASS_THRESHOLD: "0.92"`, Full workflow same, `stats.py` `QUALITY_PASS_THRESHOLD`, `store.py` `_BASELINE_QUALITY_GATE`, `metrics.py` classify logic.

**Residual gap — `BaselineVersionRecord.validate_minimum_runs()` N=10 vs. STANDARD accumulation protocol (minor):**
`version_keys.py` `BaselineVersionRecord.validate_minimum_runs()` applies minimums `{SMOKE: 1, STANDARD: 10, FULL: 30}` (lines 209-213). This enforces N=10 per STANDARD invocation at the record level — consistent with the per-invocation count. The accumulation to N≥20 happens at the comparison step via `compare_versions()`. The two-level enforcement (per-record N=10 minimum, per-comparison N≥20 minimum) is coherent and consistent with the documented protocol. Not a scoring gap.

**Improvement Path:** No additional quantitative changes needed beyond what is implemented.

---

### Architectural Coherence (0.945/1.00)

**Evidence — Gaps 2, 3, 4 RESOLVED:**

**Gap 2 RESOLVED (FR-004 chain complete):** `version_keys.py` now fully implements the FR-004 validation chain. `validate_baseline_version_key()` compares `baseline_key.commit_hash` with `current_branch_key.commit_hash` and raises `BaselineMismatchError` on mismatch (FR-004 AC-2). The `VersionKeyRegistry` caches per-agent `VersionKey` objects. The full architectural chain from git hash to baseline retrieval to mismatch detection is implemented.

**Gap 3 RESOLVED (Stream 3E complete):** Three CI/CD workflows are present:
- `prompt-regression-smoke.yml`: PR-triggered structural gate, matrix strategy per changed agent, Docker hardening, no API key required, 4 jobs.
- `prompt-regression-standard.yml`: Statistical regression gate, N=10, fork detection with MC-28 fallback, Layer 4 statistical analysis invocation via `uv run python -m jerry.testing.layer4_stats`, verdict-to-CI-exit-code mapping, 5 jobs.
- `prompt-regression-full.yml`: N=30 baseline refresh, weekly schedule + tag trigger + manual dispatch, model migration mode, baseline store update step conditioned on NO_REGRESSION + `update_baselines=true`, 3 jobs.

All three workflows correctly reference FR traceability chains, security controls (MC-07 through MC-33), and use `uv run` exclusively (H-05/FR-023). The Standard workflow invokes `uv run python -m jerry.testing.layer4_stats` with correct arguments including `--bonferroni-k`, `--base-sha`, `--head-sha`, and `--agent`.

**FR traceability completeness:** FR-001 through FR-028 coverage verified across streams:
- FR-002 (PR gate): smoke + standard workflows — verified.
- FR-003 (before/after): standard workflow "Checkout base branch agent definition" step + Layer 4 invocation — verified.
- FR-004 (version keys): `version_keys.py` + `store.py` + `promptfoo-config.yaml` — verified.
- FR-005 (tiered modes): all three workflows + `types.py` `EvaluationMode` — verified.
- FR-010 (five MRs): `metamorphic/__init__.py` `all_relations()` + full workflow `ENABLE_METAMORPHIC_RELATIONS=true` — verified.
- FR-014 (N≥20): `stats.py` `MIN_STATISTICAL_SAMPLE_SIZE` + `base.py` `minimum_sample_size` + full workflow comment — verified.
- FR-015-017 (Wilcoxon/Wilson/Bonferroni): `stats.py` implementations + layer4_stats invocation in both standard and full workflows — verified.
- FR-020 (baseline audit): `store.py` `audit()` method + full workflow baseline update step — verified.

**Residual gap — Layer 3 → Layer 4 MR-to-ScoreArray conversion path (same as iter1):**
The full workflow passes `ENABLE_METAMORPHIC_RELATIONS=true` to Docker, which tells promptfoo to run MRs. But the mechanism by which MR `MRResult` objects (with `p_value`, `passed`, score sequences) are converted into `ScoreArray` tuples consumable by `compare_multiple_metrics()` is not visible. `metamorphic/__init__.py` notes "Fisher's aggregation is an adapter-layer concern and is NOT implemented in this domain package." The `deepeval_adapter.py` file (referenced in `evaluation/__init__.py` H-10 compliance table) remains absent from the deliverable set. The gap has not been resolved in iter2. Score impact: -0.04 (same as iter1; partial improvement because the workflow now has the infrastructure, but the adapter wire-up still cannot be verified).

**Minor gap — `version_keys.py` location vs. import path:**
`promptfoo-config.yaml` comments reference `tests/prompt-regression/version_keys.py` (correct path). However, `version_keys.py` defines `EvaluationMode` independently rather than importing from `jerry.testing.types` — this creates a subtle architectural inconsistency where the test-layer utility does not depend on the production package's type definitions. The file is in `tests/` which justifies some independence, but the type duplication creates an import-time inconsistency if code tries to compare `version_keys.EvaluationMode` values with `jerry.testing.types.EvaluationMode` values. Score impact: -0.01 (minor; tests-directory context mitigates).

**Improvement Path:** (1) Implement `jerry/testing/evaluation/deepeval_adapter.py` to complete the Layer 3 → Layer 4 MR-to-ScoreArray wire-up and resolve the most significant remaining architectural gap. (2) Import `EvaluationMode` from `jerry.testing.types` in `version_keys.py`.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Architectural Coherence | 0.945 | 0.970 | Implement `jerry/testing/evaluation/deepeval_adapter.py` to wire MR `MRResult` objects into `ScoreArray` tuples for Layer 4 consumption. This is the single largest remaining architectural gap. |
| 2 | Terminological Consistency | 0.960 | 0.975 | Import `EvaluationMode` from `jerry.testing.types` in `tests/prompt-regression/version_keys.py` rather than defining a second independent enum with identical values. Add a comment explaining the dependency direction if tests-layer independence is intentional. |
| 3 | Structural Alignment | 0.905 | 0.940 | Extract `_wilcoxon_p_and_effect` to `jerry/testing/metamorphic/_wilcoxon_helpers.py` to eliminate peer module coupling. Split `base.py` per H-10 strict interpretation: `base.py` (MetamorphicRelation ABC only), `mr_result.py` (MRResult), `mr_violation_severity.py` (MRViolationSeverity). |
| 4 | All | — | 0.95+ | After implementing `deepeval_adapter.py` and resolving `EvaluationMode` duplication, re-score at iter3. Expected composite: 0.955-0.960 (above the 0.95 barrier threshold). |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score with specific file, line, and content references
- [x] Uncertain scores resolved downward: Structural Alignment held at 0.905 (same as iter1) because peer-import and H-10 multi-type grouping remain unresolved despite other improvements
- [x] Calibration anchors applied: 0.940 is between 0.92 (strong with minor gaps) and 0.95 (barrier threshold); composite reflects resolved critical gaps but persistent structural debt
- [x] No dimension scored above 0.96 — Terminological Consistency at 0.960 is justified by all four iter1 gaps resolved with one residual minor duplication; Quantitative at 0.950 reflects the documented N accumulation protocol as genuinely resolving the gap
- [x] Score delta from iter1 (+0.058) is proportional to the 4 gaps resolved — two were critical (missing files) and two were documentation gaps; the improvement is material and measurable
- [x] Arithmetic verified: 0.240 + 0.226 + 0.238 + 0.236 = 0.940
- [x] Barrier gate threshold 0.95 deliberately stricter than S-014 deliverable threshold 0.92; the 0.010 deficit is real and addressable in one targeted iter3

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.940
threshold: 0.95
weakest_dimension: structural_alignment
weakest_score: 0.905
critical_findings_count: 0
high_findings_count: 1
high_findings:
  - "deepeval_adapter.py absent — Layer 3 to Layer 4 MR-to-ScoreArray conversion path unverified"
medium_findings_count: 2
medium_findings:
  - "version_keys.py defines second EvaluationMode enum independent from types.py"
  - "mr_001_paraphrase.py peer-import structural debt unresolved (mr_003, mr_004, mr_005 still import _wilcoxon_p_and_effect from mr_001)"
iteration: 2
iter1_score: 0.882
iter2_score: 0.940
score_delta: +0.058
iter1_gaps_resolved:
  - "InsufficientSamplesError consolidated to single class in stats.py"
  - "version_keys.py implemented at tests/prompt-regression/version_keys.py (671 lines, FR-004 complete)"
  - "Three CI/CD workflow files delivered (smoke/standard/full)"
  - "STANDARD N accumulation protocol documented in store.py and stats.py"
improvement_recommendations:
  - "Implement jerry/testing/evaluation/deepeval_adapter.py (Layer 3 to Layer 4 wire-up)"
  - "Import EvaluationMode from jerry.testing.types in version_keys.py"
  - "Extract _wilcoxon_p_and_effect to metamorphic/_wilcoxon_helpers.py"
  - "Split base.py per H-10 strict interpretation"
```

---

*Gate: QG-2 — Implementation Consistency*
*Pattern: sync_barrier*
*SSOT: `.context/rules/quality-enforcement.md`*
*Scored: 2026-03-07*
*Agent: adv-scorer*
*Iteration: 2 of N (prior: 0.882 REVISE → current: 0.940 REVISE)*
