# Quality Gate 2 — Implementation Consistency Barrier Score

## L0 Executive Summary

**Gate:** QG-2 — Implementation Consistency | **Verdict:** REVISE | **Threshold:** 0.95
**Composite Score:** 0.882/1.00 | **Weakest Dimension:** Terminological Consistency (0.830)
**One-line assessment:** The five implementation streams form a coherent, well-structured architecture
with strong H-07/H-10/H-11 compliance and internally consistent numeric constants, but two substantive
consistency gaps prevent acceptance: (1) `version_keys.py` is cited by Stream 3A and the overall
design but does not exist in the codebase, and (2) the `InsufficientSamplesError` in `stats.py`
uses a free-form string constructor while `base.py` defines a structured constructor with positional
`(n, minimum, mr_id)` arguments — the two exception classes share a name but are different types,
creating a terminology and interface mismatch across layers.

---

## Scoring Context

- **Gate ID:** QG-2
- **Gate Name:** Quality Gate 2 — Implementation Consistency
- **Pattern:** sync_barrier (cross-deliverable consistency scoring)
- **Criticality Level:** C4
- **Threshold:** 0.95
- **Streams Evaluated:**
  - 3A (Layer 1 — promptfoo CI/CD): `tests/prompt-regression/promptfoo-config.yaml` + 5 test case YAMLs
  - 3B (Layer 2 — DeepEval): `jerry/testing/evaluation/__init__.py`, `metrics.py`, `debiasing.py`
  - 3C (Layer 3 — Metamorphic Relations): `jerry/testing/metamorphic/` (7 files)
  - 3D (Layer 4 — Statistical Engine): `jerry/testing/types.py`, `stats.py`, `layer4_stats.py`,
    `baselines/store.py`, `baselines/ports.py`, `baselines/__init__.py`, `reports/generator.py`,
    `reports/ports.py`, `reports/__init__.py`, `__init__.py`
  - 3E (CI/CD Pipeline): No `.github/workflows/prompt-regression.yml` found; no `jerry/testing/evaluation/criteria/` found
- **Scoring Strategy:** S-014 LLM-as-Judge with 4-dimension barrier rubric
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-03-07T00:00:00Z
- **Debiasing applied:** Yes — each dimension scored independently before composite computed

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.882 |
| **Threshold** | 0.95 (barrier gate) |
| **Verdict** | REVISE |
| **Stream scores incorporated** | Yes — 5 streams read in full |
| **Missing deliverables detected** | 2 (version_keys.py absent; GitHub Actions workflow absent) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Terminological Consistency | 0.25 | 0.830 | 0.208 | EvaluationMode values consistent; RegressionClass enum consistent; two `InsufficientSamplesError` classes with incompatible constructors; version key format cited but module missing |
| Structural Alignment | 0.25 | 0.905 | 0.226 | H-07 domain isolation cleanly enforced; H-10 one-class-per-file compliant; H-11 type hints and docstrings present; MR statistical helper cross-import (3C importing from mr_001_paraphrase) is a minor structural coupling but documented |
| Quantitative Consistency | 0.25 | 0.920 | 0.230 | N>=20 in stats.py; N=30 for FULL in store.py; Bonferroni k=13 consistent; alpha=0.05 uncorrected and 0.004 corrected both consistent; quality gate 0.92 uniform; MR tolerances (0.05, 0.03, 0.06) internally consistent and referenced from contracts |
| Architectural Coherence | 0.25 | 0.875 | 0.219 | FR traceability present throughout; hexagonal port/adapter pattern cleanly applied; Layer 1 → Layer 2 data flow consistent; debiasing in 3B consistent with MR domain isolation in 3C; CI/CD stream (3E) partially absent — workflow file not present |
| **TOTAL** | **1.00** | | **0.882** | |

**Arithmetic verification:**
- Terminological: 0.830 × 0.25 = 0.2075
- Structural: 0.905 × 0.25 = 0.2263
- Quantitative: 0.920 × 0.25 = 0.2300
- Architectural: 0.875 × 0.25 = 0.2188
- Sum: 0.2075 + 0.2263 + 0.2300 + 0.2188 = 0.8826 → rounded to **0.882**
- Threshold: 0.95. Deficit: 0.068. Verdict: **REVISE**

---

## Detailed Dimension Analysis

### Terminological Consistency (0.830/1.00)

**Evidence — Consistent:**
- `EvaluationMode` enum values: `SMOKE = "Smoke"`, `STANDARD = "Standard"`, `FULL = "Full"` appear uniformly across `types.py` (definition), `stats.py` (compare_versions signature), `store.py` (FULL mode guard), `layer4_stats.py` (run method dispatch), and `promptfoo-config.yaml` (comment referencing Smoke=1, Standard=10, Full=30).
- `RegressionClass` enum names (`NO_REGRESSION`, `MARGINAL`, `REGRESSION`, `IMPROVEMENT`, `QUALITY_FLOOR_BREACH`, `STRUCTURAL_FAIL`) defined once in `types.py` and referenced consistently in `stats.py`, `layer4_stats.py`, `generator.py`, and test case comments.
- `metric_id` string identifiers: `composite_score`, `completeness`, `evidence_quality`, `actionability` used consistently across `stats.py` (compare_versions default), `layer4_stats.py` (run example), and test case YAML files (`quality/completeness`, `quality/evidence_quality`, `quality/actionability` metrics). Minor difference in metric naming convention — Python code uses snake_case (`composite_score`), YAML test cases use slash-separated (`quality/completeness`) — but this is a layer separation, not a contradiction.
- Version key format `"{hash}:{path}"`: cited in `types.py` (`BaselineRecord.version_key` docstring: `"Composite key '{git_commit_hash}:{file_path}'"` per FR-004), `stats.py` (compare_versions `version_key_a` docstring: `"{hash}:{path}"`), `store.py` (_validate_version_key docstring: `"'{git_hash}:{file_path}'"` per FR-004), and `layer4_stats.py` (Layer4Pipeline.run version_key_a docstring: `"{hash}:{path}"`). All four are consistent.
- Quality gate threshold: `QUALITY_PASS_THRESHOLD = 0.92` in `stats.py`; `_BASELINE_QUALITY_GATE = 0.92` in `store.py` (with a comment explaining why it is duplicated rather than imported); `classify_composite` in `metrics.py` (3B) uses `>= 0.92` for PASS; test case YAML SI-SCOR-005 states "PASS only when composite >= 0.92". All four independently consistent.

**Gaps — Score Deductions:**

**Gap 1 — Missing `version_keys.py` module (significant):** `promptfoo-config.yaml` explicitly references `jerry/testing/version_keys.py` four times (lines 82, 134, 136, 139): "The version_keys.py module validates that baseline version keys match the target branch git commit hash" and "version_keys.py uses these to validate baseline vs. candidate alignment (FR-004)". The `adv-scorer.yaml` test case header also lists `jerry/testing/version_keys.py` as a Stream 3A deliverable. Glob search on `jerry/testing/version_keys.py` returns no results — the file does not exist. The referenced FR-004 version key validation logic has no implementation. This is a concrete terminological and functional gap: a module cited as the "authoritative implementation of FR-004" is absent. Score impact: -0.07.

**Gap 2 — Dual `InsufficientSamplesError` classes with incompatible constructors (moderate):** `stats.py` (3D) defines `InsufficientSamplesError(ValueError)` with the standard message format: `"Wilcoxon requires N >= {MIN_STATISTICAL_SAMPLE_SIZE} per version (got {n_a}, {n_b}). Use Smoke mode..."` — a plain string passed directly to `super().__init__()`. `base.py` (3C) defines a second `InsufficientSamplesError(ValueError)` with a structured constructor `__init__(self, n: int, minimum: int, mr_id: str)` that formats its own message. The name is identical but the type signature, message format, and semantic context differ. `store.py` imports `InsufficientSamplesError` from `stats.py` and uses it with a free-form string: `raise InsufficientSamplesError("FULL mode baseline requires N >= ...")`. The two classes cannot be treated interchangeably by a caller. The `jerry.testing.__init__.py` re-exports only the `stats.py` version. Code in 3C metamorphic layer raises `base.InsufficientSamplesError` with positional args; code in 3D raises `stats.InsufficientSamplesError` with string constructor. Score impact: -0.07.

**Gap 3 — Bonferroni k=6 in test fixture vs. k=13 in system (minor):** `adv-scorer.yaml` fixture P-ADVS-004 (line 394) contains a comment `# Bonferroni correction for K=6 quality dimensions` with code `alpha_corrected = 0.05 / 6  # = 0.0083`. The system's authoritative constant is `BONFERRONI_K_FULL_SUITE = 13` (6 dimensions + composite + 5 MRs + pass rate = 13). The k=6 figure in the test fixture is an artifact of the fictional test scenario (a simplified code snippet shown to the agent being scored) and is explicitly commented as part of a user-provided artifact, not a system constant. On close reading, k=6 in the artifact is correct for that scenario description (6 quality dimensions only), while the harness itself uses k=13. This is not a true inconsistency — the test fixture intentionally presents simplified code to test the adv-scorer's analytical ability. Score impact: 0 (artifact content, not system constant).

**Improvement Path:** (1) Implement `jerry/testing/version_keys.py` to satisfy FR-004 per the documented API. (2) Consolidate `InsufficientSamplesError` to a single definition in `jerry/testing/types.py` or `jerry/testing/stats.py` with backward-compatible constructor; update `base.py` to import from there rather than defining its own.

---

### Structural Alignment (0.905/1.00)

**Evidence — Consistent:**
- **H-07 domain isolation:** `types.py` imports only stdlib. `stats.py` imports only stdlib, scipy, statsmodels, and `jerry.testing.types`. `evaluation/metrics.py` imports only stdlib and sibling evaluation modules (no DeepEval). `evaluation/debiasing.py` imports only stdlib and sibling modules. `metamorphic/base.py`, `mr_001_paraphrase.py` through `mr_005_roundtrip.py` import only stdlib (scipy conditionally) and parent base module. `baselines/ports.py` imports only stdlib and `jerry.testing.types`. `baselines/store.py` imports stdlib, `jerry.testing.types`, and `jerry.testing.stats.InsufficientSamplesError` (legitimate adapter → domain dependency). `reports/ports.py` imports only stdlib and types. `reports/generator.py` imports only stdlib and types. `layer4_stats.py` imports from `stats`, `types`, `baselines.ports`, `reports.ports` — legitimate adapter-to-adapter-via-port imports. No cross-layer violations detected.
- **H-10 one class per file:** Verified across all Python files read: `metrics.py` (JerryGEvalMetric), `debiasing.py` (DebiasingStrategy), `base.py` (MetamorphicRelation ABC + MRResult dataclass + MRViolationSeverity enum, which are support types not primary classes — the one-class rule applies to primary domain classes), `mr_001_paraphrase.py` (ParaphraseConsistency), `mr_002_negation.py` (NegationHandling), `mr_003_context.py` (IrrelevantContextAppendation), `mr_004_formatting.py` (FormattingPerturbation), `mr_005_roundtrip.py` (LanguageRoundTrip), `store.py` (BaselineStore), `ports.py` (BaselinePersistencePort / ReportOutputPort), `generator.py` (ReportGenerator), `layer4_stats.py` (Layer4Pipeline), `calibration.py` (CalibrationRunner + `apply_calibrated_tolerances` function). All comply. `types.py` contains multiple grouped dataclasses — this is the SSOT domain type file, grouped by concern per H-10 docstring note: "One primary class/enum grouping per file (grouped by concern)." Compliant.
- **H-11 type hints + docstrings:** All public functions and classes examined carry both. Spot-checked: `compare_versions()` in `stats.py` (full Args/Returns/Raises), `JerryGEvalMetric.score_composite()` (full docstring with example), `BaselineStore.store()` (detailed Args/Returns/Raises), `LanguageRoundTrip.evaluate()` (full docstring). No public functions found without type annotations or docstrings.
- **Layer boundary discipline:** Layer 1 (promptfoo YAML) outputs to `tests/prompt-regression/results/promptfoo-output.json`. The comment in `promptfoo-config.yaml` (line 146-148) correctly describes consumption: "JSON output is consumed by Layer 2 (DeepEval), Layer 3 (MR checks), and Layer 4 (statistical engine) — this is the inter-layer interface." `layer4_stats.py` imports from `baselines.ports` and `reports.ports` (not concrete adapters at top level), consistent with hexagonal architecture. Lazy import of `ReportGenerator` in `Layer4Pipeline.__init__` (line 102-104) explicitly preserves H-07 compliance.
- **Port/adapter boundaries:** `BaselinePersistencePort` (Protocol) in `baselines/ports.py` matched by `BaselineStore` in `store.py`. `ReportOutputPort` (Protocol) in `reports/ports.py` matched by `ReportGenerator` in `generator.py`. `EvaluationPort` exported from `evaluation/__init__.py`. All hexagonal ports defined in domain-layer modules.

**Gaps:**

**Gap 1 — MR statistical helper cross-import (minor, documented):** `mr_003_context.py`, `mr_004_formatting.py`, and `mr_005_roundtrip.py` all import `_wilcoxon_p_and_effect` from `jerry.testing.metamorphic.mr_001_paraphrase` (a private module-level function). This creates a coupling between sibling modules within the same package. It is structurally preferable to extract `_wilcoxon_p_and_effect` to a shared module (e.g., `metamorphic/_stats_helpers.py`) to avoid this peer coupling. However, the docstring in `mr_001_paraphrase.py` acknowledges this: "Used by MR-001, MR-003, MR-004, and MR-005 for two-sided testing." The coupling is intentional, documented, and confined to within the metamorphic domain package — no H-07 violation. Score impact: -0.03 (structural debt, not a violation).

**Gap 2 — `base.py` contains multiple types (minor):** `base.py` defines `InsufficientSamplesError`, `MRViolationSeverity`, `MRResult`, and `MetamorphicRelation` in one file. For H-10 strict interpretation, `MRResult` and `MRViolationSeverity` should be in separate files. The `evaluation/__init__.py` H-10 compliance table does list separate files for `ScoringResult`, `PositionRandomizationResult`, `QualityCriterion` — demonstrating stream 3B's more rigorous application of H-10. The metamorphic package (3C) is less rigorous here. Score impact: -0.04.

**Improvement Path:** (1) Extract `_wilcoxon_p_and_effect` to `jerry/testing/metamorphic/_wilcoxon_helpers.py` to eliminate peer module coupling. (2) Split `base.py` into `base.py` (MetamorphicRelation ABC only), `mr_result.py` (MRResult), `mr_violation_severity.py` (MRViolationSeverity), and `insufficient_samples_error.py` per H-10 strict interpretation. Lower priority than the terminological gaps above.

---

### Quantitative Consistency (0.920/1.00)

**Evidence — Consistent:**

**N>=20 minimum sample size:**
- `stats.py`: `MIN_STATISTICAL_SAMPLE_SIZE: int = 20` (named constant per FR-014, line 63). `compare_versions()` raises `InsufficientSamplesError` when `n_a < MIN_STATISTICAL_SAMPLE_SIZE or n_b < MIN_STATISTICAL_SAMPLE_SIZE`.
- `metamorphic/base.py`: `minimum_sample_size: int = 20` class attribute on `MetamorphicRelation`.
- `metamorphic/mr_001_paraphrase.py`: `minimum_sample_size: int = 20`, raises `InsufficientSamplesError` via `_validate_inputs()` when `n < self.minimum_sample_size`.
- `metamorphic/mr_002_negation.py`: `minimum_sample_size: int = 15` (explicitly reduced from 20 for large-effect detection — documented in docstring: "Reduced from 20; detecting presence of large effect requires fewer samples"). This is a deliberate and documented deviation, not an inconsistency.
- `metamorphic/mr_003_context.py` through `mr_005_roundtrip.py`: all `minimum_sample_size: int = 20`.
- `jerry/testing/__init__.py` re-exports `MIN_STATISTICAL_SAMPLE_SIZE`.

**N=30 for FULL mode:**
- `store.py`: `MIN_FULL_SAMPLES: int = 30` (class attribute, line 114), enforced in `store()` for `EvaluationMode.FULL`.
- `stats.py` docstring for `compare_versions()`: "N >= MIN_STATISTICAL_SAMPLE_SIZE for both arrays". Consistent — N=30 > N=20; FULL mode applies stricter gate.
- `promptfoo-config.yaml` comment: "Standard: N=10, Full: N=30" (line 20, usage comment). Consistent.
- `baselines/ports.py`: `min_samples: int = 30` default in `BaselinePersistencePort.store()` signature.
- `debiasing.py` method docstring: "Over N=30 runs, each candidate will appear first approximately N/2 = 15 times" (line 117). Consistent.

**Bonferroni k=13:**
- `stats.py`: `BONFERRONI_K_FULL_SUITE: int = 13` with docstring: "6 S-014 dimensions + 1 composite score + 5 MRs + 1 pass rate = 13."
- `layer4_stats.py` imports `BONFERRONI_K_FULL_SUITE` from `stats.py` and uses it in `_run_statistical()`.
- `jerry/testing/__init__.py` re-exports `BONFERRONI_K_FULL_SUITE`.
- Arithmetic check: 6 + 1 + 5 + 1 = 13. Correct.

**Alpha values:**
- `stats.py`: `_ALPHA_REGRESSION: float = 0.05` (uncorrected), `BONFERRONI_ALPHA_FULL: float = 0.004`.
- 0.05/13 = 0.003846... → spec rounds to 0.004 (conservative). `stats.py` docstring: "0.05/13 = 0.003846..., rounded to 0.004 per contract convention." Explicitly verified.
- `mr_001_paraphrase.py`: `P_ALPHA: float = 0.05` (Wilcoxon significance level). Consistent.
- `mr_002_negation.py`: `P_NON_SIGNIFICANT_THRESHOLD: float = 0.10` (different threshold for directional test — documented in contracts C.2). Consistent by design.
- `mr_003_context.py`: `P_ALPHA: float = 0.05`. `mr_004_formatting.py`: `P_ALPHA: float = 0.05`. `mr_005_roundtrip.py`: `P_ALPHA: float = 0.05`. All consistent.

**MR tolerance values:**
- MR-001: `TOLERANCE = 0.05`. MR-003: `TOLERANCE = 0.03` (tighter, documented in C.3). MR-004: `TOLERANCE = 0.05`. MR-005: `TOLERANCE = 0.06` (looser, for translation noise, documented in C.5). MR-002 uses `MIN_DELTA_REQUIRED = 0.05` (directional semantics). Each value is consistent with its corresponding behavioral-contracts.md citation.

**Quality gate 0.92:**
- `stats.py`: `QUALITY_PASS_THRESHOLD = 0.92`.
- `store.py`: `_BASELINE_QUALITY_GATE: float = 0.92`.
- `metrics.py` `classify_composite()`: `if composite_score >= 0.92: return "PASS"`.
- `adv-scorer.yaml` test assertions: SI-SCOR-005 "PASS only when composite >= 0.92".
- `ps-researcher.yaml` LLM-rubric thresholds: 0.82, 0.75, 0.65, 0.78 per-dimension floors — all below 0.92, consistent.
- `jerry/testing/__init__.py` re-exports `QUALITY_PASS_THRESHOLD`.

**Gaps:**

**Gap 1 — `BONFERRONI_ALPHA_FULL = 0.004` vs. computed 0.003846 (precision note):** The stored constant 0.004 is documented as a conservative 3-significant-figure rounding in `stats.py`. The comment explains: "round(0.05/13, 4) = 0.0038, which would be a 5% relative error from the specified threshold." The chosen 0.004 is conservative (higher than actual 0.003846), which makes the gate stricter, not looser. This is intentional and documented. Not a scoring gap.

**Gap 2 — STANDARD mode N validation gap (minor):** `stats.py` enforces only N >= 20 (MIN_STATISTICAL_SAMPLE_SIZE = 20) for all modes, while `store.py` applies N=30 only for FULL mode baselines. This means STANDARD mode accepts N=10 (per promptfoo comments) from promptfoo but stats.py would reject N=10 with InsufficientSamplesError at the Wilcoxon comparison step. The resolution: STANDARD mode N=10 is the per-run count during evaluation, while stats.py's N=20 minimum applies at comparison time (requiring accumulation of 20+ STANDARD runs before comparison). This is plausible but the inter-layer handoff protocol for accumulating STANDARD runs to reach N=20 is not documented in any of the five streams. Score impact: -0.04.

**Gap 3 — Effect size thresholds not unified:** MR-001 uses `EFFECT_R_THRESHOLD = 0.30`; MR-002 uses `EFFECT_R_THRESHOLD = 0.40`; MR-003 uses `EFFECT_R_THRESHOLD = 0.25`; MR-004 uses `EFFECT_R_THRESHOLD = 0.30`; MR-005 uses `EFFECT_R_THRESHOLD = 0.35`. These intentional differences per contracts C.1-C.5 are documented and consistent with the contracts. Not a scoring gap.

**Improvement Path:** Document the STANDARD mode N accumulation protocol — specifically, how 10 runs per evaluation accumulate to the N>=20 required by stats.py before statistical comparison can be performed. This protocol gap is the only material quantitative consistency issue.

---

### Architectural Coherence (0.875/1.00)

**Evidence — Consistent:**

**FR traceability chain:**
- FR-001 (declarative YAML test cases): `promptfoo-config.yaml` header and each test case YAML cite FR-001. Test cases have assertion blocks with metric labels (structural/non_empty, quality/completeness). Direct traceability.
- FR-003 (before/after comparison): `promptfoo-config.yaml` contains an extended comment (lines 59-76) explicitly explaining how the two-provider setup relates to FR-003 and why the actual before/after comparison is performed by Layer 4 (statistical engine), not by promptfoo. This is architecturally coherent documentation of the layer division.
- FR-005 (tiered evaluation modes): EvaluationMode enum in `types.py` maps directly to FR-005 tier definitions. `promptfoo-config.yaml` references FR-005 in comment on `repeat: 1`. `layer4_stats.py` dispatches on `EvaluationMode.SMOKE` vs. others. Consistent.
- FR-010 (five universal MRs): All five MRs (MR-001 through MR-005) implemented in dedicated files matching FR-010 requirements. `metamorphic/__init__.py` maps canonical system-design.md names (`ContextWindowStability`, `FormatInvariance`, `PromptRoundTrip`) to implementation names.
- FR-014 (N>=20): Named constant `MIN_STATISTICAL_SAMPLE_SIZE = 20` in `stats.py`, enforced in `base.py` `_validate_inputs`, re-exported from package `__init__.py`.
- FR-019 (stats.py as SSOT): `layer4_stats.py` imports all statistical functions from `stats.py` and does not re-implement any. `jerry/testing/__init__.py` re-exports from `stats.py`. One-way dependency enforced.
- FR-020 (baseline audit): `BaselineStore.audit()` implemented and documented. `BaselinePersistencePort.audit()` in port contract.

**Debiasing (3B) consistent with MR methodology (3C):**
- 3B's `DebiasingStrategy` (position randomization + rubric shuffling) applies to G-Eval single-output scoring. It is domain-layer, H-07 compliant.
- 3C's `MetamorphicRelation` family applies dual-condition violation checks (statistical significance + practical significance) — a different debiasing approach for comparative evaluation.
- Both approaches are orthogonal: 3B debiases the LLM judge; 3C debiases statistical interpretation. They compose without contradiction. `evaluation/__init__.py` explicitly states "Fisher's aggregation is an adapter-layer concern and is NOT implemented in this domain package" — consistent with 3C's statement that Fisher's method aggregates MR p-values at the adapter layer.

**Layer 1 → Layer 2 interface:**
- `promptfoo-config.yaml` outputs to `tests/prompt-regression/results/promptfoo-output.json` (line 149).
- `evaluation/__init__.py` references "Layer 2 DeepEval evaluation backend" and imports from `jerry.testing.evaluation.criteria.ps_researcher`.
- `metrics.py` defines `DIMENSION_WEIGHTS` and `JerryGEvalMetric.score_composite()` returning float in [0.0, 1.0]. The interface for feeding Layer 1 (promptfoo) outputs into Layer 2 (JerryGEvalMetric) is architecturally defined but not explicitly wired — the `deepeval_adapter.py` file is referenced in `evaluation/__init__.py` H-10 compliance table but was not in the deliverable list and was not read. The design intent is coherent; the concrete wiring exists per the H-10 table.

**Layer 4 pipeline integration:**
- `Layer4Pipeline.run()` accepts `metric_scores: dict[str, tuple[ScoreArray, ScoreArray]]`, calls `compare_multiple_metrics()` from `stats.py`, generates `ComparisonReport`, persists via `ReportOutputPort`, and emits GitHub Actions outputs. Clean pipeline from score arrays to CI/CD gate.
- `BaselineStore` stores scores with `version_key = "{hash}:{path}"`. `layer4_stats.py` uses `version_key_a` and `version_key_b` parameters of the same format in its `run()` signature. Consistent.

**Gaps:**

**Gap 1 — CI/CD pipeline (Stream 3E) partially absent (significant):** No `.github/workflows/prompt-regression.yml` exists (glob returned no results). `promptfoo-config.yaml` references it repeatedly ("AGENT_ID is set by the GitHub Actions workflow (.github/workflows/prompt-regression.yml)"). `evaluation/__init__.py` also references it. The Stream 3E score of 0.943 was assigned for CI/CD pipeline work, but the primary deliverable (the workflow file) is not present. The existing `evaluation/criteria/` directory was also not found. This means the architectural coherence of the CI/CD integration layer cannot be verified. Score impact: -0.06.

**Gap 2 — FR-004 validation absent (carried from terminological gap):** The absence of `version_keys.py` means that although the version key format is architecturally consistent, the validation mechanism (described as ensuring "baseline version keys match the target branch git commit hash before comparison") has no implementation. This is an architectural gap in the FR-004 compliance chain. Score impact: -0.04 (partially overlapping with terminological gap above).

**Gap 3 — Layer 3 → Layer 4 interface under-specified (minor):** The MR evaluation produces `MRResult` objects (from `metamorphic/base.py`). Layer 4's `Layer4Pipeline.run()` accepts `metric_scores: dict[str, tuple[ScoreArray, ScoreArray]]`. The mechanism for converting `MRResult` objects (which contain `p_value`, `passed`, and score sequences) into the `ScoreArray` format consumed by Layer 4 is the role of the DeepEval adapter (`deepeval_adapter.py`) mentioned in the evaluation package — but this adapter was not in the deliverable set. The interface specification exists (Fisher's aggregation mentioned in `metamorphic/__init__.py`) but the wiring is not visible in the read files. Score impact: -0.04.

**Improvement Path:** (1) Create `.github/workflows/prompt-regression.yml` with agent matrix strategy, evaluation mode dispatch, and artifact upload to complete Stream 3E. (2) Implement `jerry/testing/version_keys.py` per FR-004. (3) Document or implement the Layer 3 → Layer 4 score conversion path.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Terminological Consistency | 0.830 | 0.900 | Implement `jerry/testing/version_keys.py` per FR-004 spec. Consolidate `InsufficientSamplesError` to a single class in `jerry/testing/stats.py`; update `base.py` to import from there rather than defining its own incompatible constructor. |
| 2 | Architectural Coherence | 0.875 | 0.940 | Create `.github/workflows/prompt-regression.yml` with agent matrix strategy, evaluation mode env vars, and promptfoo Docker invocation per ADR-001 constraint. Create `jerry/testing/evaluation/criteria/` with per-agent criteria files. |
| 3 | Quantitative Consistency | 0.920 | 0.960 | Document STANDARD mode N accumulation protocol: specify how N=10-run batches accumulate to N>=20 before Wilcoxon comparison can be invoked. Add a protocol note to `baselines/protocol.md`. |
| 4 | Structural Alignment | 0.905 | 0.940 | Extract `_wilcoxon_p_and_effect` to `metamorphic/_wilcoxon_helpers.py`. Consider splitting `base.py` per H-10 strict interpretation. Lower priority than gaps 1-3. |

---

## Missing Deliverables Summary

| Stream | Expected File | Status | Impact |
|--------|--------------|--------|--------|
| 3A | `jerry/testing/version_keys.py` | ABSENT — no file at this path | High: FR-004 validation unimplemented |
| 3E | `.github/workflows/prompt-regression.yml` | ABSENT — no file at this path | High: CI/CD gate incomplete |
| 3E | `jerry/testing/evaluation/criteria/` | ABSENT — directory not found | Medium: per-agent criteria not verified |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score with specific file and line references
- [x] Uncertain scores resolved downward: Terminological Consistency assigned 0.830 not 0.870 due to the missing module being a concrete deliverable gap, not a documentation gap
- [x] Calibration anchors applied: 0.830 is between 0.70 (significant gaps) and 0.85 (minor refinements); reflects two material gaps but strong overall consistency in present code
- [x] No dimension scored above 0.95 — highest is Quantitative Consistency at 0.920 (genuine strength with one undocumented protocol gap)
- [x] Arithmetic verified by hand: 0.2075 + 0.2263 + 0.2300 + 0.2188 = 0.8826 ≈ 0.882
- [x] Barrier gate threshold 0.95 is above the S-014 deliverable threshold 0.92 — deliberate; cross-stream consistency is harder to achieve than single-stream quality

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.882
threshold: 0.95
weakest_dimension: terminological_consistency
weakest_score: 0.830
critical_findings_count: 2
critical_findings:
  - "jerry/testing/version_keys.py does not exist (FR-004 validation absent)"
  - "Two InsufficientSamplesError classes with incompatible constructors in stats.py vs base.py"
high_findings_count: 1
high_findings:
  - ".github/workflows/prompt-regression.yml does not exist (Stream 3E CI/CD incomplete)"
iteration: 1
improvement_recommendations:
  - "Implement jerry/testing/version_keys.py per FR-004 specification"
  - "Consolidate InsufficientSamplesError to single class in stats.py; update base.py import"
  - "Create .github/workflows/prompt-regression.yml with agent matrix strategy"
  - "Document STANDARD mode N accumulation protocol in baselines/protocol.md"
  - "Extract _wilcoxon_p_and_effect to metamorphic/_wilcoxon_helpers.py"
```

---

*Gate: QG-2 — Implementation Consistency*
*Pattern: sync_barrier*
*SSOT: `.context/rules/quality-enforcement.md`*
*Scored: 2026-03-07*
*Agent: adv-scorer*
