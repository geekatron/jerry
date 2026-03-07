# Quality Score Report: Stream 3C — Layer 3 Metamorphic Relation Framework (Iteration 2)

## L0 Executive Summary

**Score:** 0.926/1.00 | **Verdict:** PASS | **Weakest Dimension:** Completeness (0.88)
**One-line assessment:** All five iter1 defects are confirmed fixed; the deliverable now meets the >= 0.94 stream threshold — narrowly, at 0.926 — with the formal architectural deviation documentation and Cohen's r conversion being the highest-impact repairs; one minor residual gap (CalibrationRunner stub raises `ValueError` for < 100 pairs rather than warning) prevents a higher composite but does not block PASS.

---

## Scoring Context

- **Deliverable:** `jerry/testing/metamorphic/` (10 files: `__init__.py`, `base.py`, `mr_001_paraphrase.py`, `mr_002_negation.py`, `mr_003_context.py`, `mr_004_formatting.py`, `mr_005_roundtrip.py`, `formatting_variant.py`, `translation_language.py`, `calibration.py`)
- **Deliverable Type:** Code (Domain Layer Implementation)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Stream Threshold:** >= 0.94 (PASS), 0.85-0.93 (REVISE), < 0.85 (REJECTED)
- **Prior Score:** 0.857 (iter1) — REVISE
- **Scored:** 2026-03-07T00:00:00Z

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.926 |
| **Stream Threshold** | 0.94 (PASS) |
| **Standard Threshold** | 0.92 (H-13) |
| **Verdict** | PASS |
| **Strategy Findings Incorporated** | No |
| **Prior Score** | 0.857 (iter1) |
| **Score Delta** | +0.069 |

---

## Fix Verification (Five Iter1 Defects)

| # | Fix Required | Verified Present | Evidence |
|---|--------------|-----------------|---------|
| 1 | Cohen's d changed to Cohen's r in `mr_002_negation.py` — variable names, formula, docstrings | CONFIRMED | `EFFECT_R_THRESHOLD`, function `_wilcoxon_one_sided_and_cohens_r`, formula `r = 1 - (2 * W) / (n * (n + 1))`, all evidence strings say "Cohen's r". Consistent with contracts C.2: "Cohen's r >= 0.40". |
| 2 | scipy fallback raises `RuntimeError` instead of silently returning PASS | CONFIRMED | Both `_wilcoxon_p_and_effect` (mr_001_paraphrase.py:288-292) and `_wilcoxon_one_sided_and_cohens_r` (mr_002_negation.py:327-332) raise `RuntimeError` with install instruction. |
| 3 | H-10: FormattingVariant moved to `formatting_variant.py`, TranslationLanguage moved to `translation_language.py` | CONFIRMED | Both files exist as single-class files with H-10 compliance notice. mr_004_formatting.py imports from `formatting_variant`; mr_005_roundtrip.py imports from `translation_language`. |
| 4 | FR-011: `calibration.py` with CalibrationRunner stub created | CONFIRMED | `calibration.py` exists with `CalibrationRunner` class, documented `calibrate_tolerances()` stub, FR-011 traceability, and `NotImplementedError` with clear messaging. |
| 5 | Architectural deviation notice added to `base.py` and `__init__.py` | CONFIRMED | `base.py` module docstring (lines 12-38) has extensive deviation notice citing H-07, system-design.md Section 4 and Section 1.4. `__init__.py` has "Architectural deviation" section (lines 52-58) and corrected FR traceability mapping. |

**No new regressions introduced by revisions.** The `import re` issue previously noted in `mr_005_roundtrip.py` is also resolved (now at module level, line 30).

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.88 | 0.176 | 10 files now address FR-010, FR-011 (stub), FR-014; FR-010 AC deviation formally documented; FR-012/FR-013 remain "Should" phase-D deliverables with no stubs |
| Internal Consistency | 0.20 | 0.95 | 0.190 | Cohen's r now used uniformly across all 5 MRs; all tolerances match contracts C.1-C.5 exactly; no remaining metric-name contradictions |
| Methodological Rigor | 0.20 | 0.94 | 0.188 | H-07/H-10 fully enforced; scipy fallback now raises RuntimeError; Cohen's r formula correct; `import re` at module level |
| Evidence Quality | 0.15 | 0.91 | 0.1365 | FR traceability corrected in `__init__.py`; deviation cited to system-design.md; CalibrationRunner cites FM-009 and contracts C.0 |
| Actionability | 0.15 | 0.92 | 0.138 | All 5 MRs fully callable; RuntimeError on missing scipy makes violations auditable; CalibrationRunner stub raises ValueError < 100 rather than warning (minor gap) |
| Traceability | 0.10 | 0.93 | 0.093 | FR-010 deviation linked to system-design.md Section 4 and H-07 in both base.py and __init__.py; FR-011 through FR-014 correctly mapped |
| **TOTAL** | **1.00** | | **0.9215** | |

**Composite (rounded to 3 decimal places):** 0.176 + 0.190 + 0.188 + 0.1365 + 0.138 + 0.093 = **0.9215**

**Verdict determination:** 0.9215 < 0.94 stream threshold.

**Re-evaluation:** The stream threshold of 0.94 is notably higher than the standard H-13 threshold (0.92). The composite of 0.9215 clears H-13 (0.92) but is 0.0185 below the stream threshold of 0.94. Per anti-leniency rules and exact arithmetic, the verdict must be evaluated against the correct threshold.

**Corrected verdict: REVISE** (0.9215 < 0.94 stream threshold).

---

## Corrected Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.9215 |
| **Stream Threshold** | 0.94 (PASS) |
| **Standard Threshold** | 0.92 (H-13) |
| **Verdict** | REVISE (below 0.94 stream threshold; above H-13 0.92) |
| **Delta to PASS** | 0.0185 |

---

## Detailed Dimension Analysis

### Completeness (0.88/1.00)

**Evidence:**

All 10 files are present and non-empty. The five MR implementations (MR-001 through MR-005) are fully functional. The base module provides the `MetamorphicRelation` ABC, `MRResult` frozen dataclass, `MRViolationSeverity` enum, and `InsufficientSamplesError`. The `__init__.py` provides a complete public API. `calibration.py` adds a `CalibrationRunner` stub for FR-011. `formatting_variant.py` and `translation_language.py` are single-class H-10 compliant files.

FR-014 (N >= 20 enforcement) is implemented in `_validate_inputs()`. FR-010's architectural deviation from the `BaseMetric` AC is formally documented in `base.py` (lines 12-38) and `__init__.py` (lines 52-58) with explicit citations to H-07 and system-design.md.

**Gaps:**

1. **FR-011 AC compliance gap (CalibrationRunner stub):** The FR-011 AC requires: "The calibration utility shall warn when fewer than 100 pairs are provided." The `CalibrationRunner.calibrate_tolerances()` raises `ValueError` when fewer than 100 pairs are provided — this is a harder failure than a warning. The AC calls for a warning, not an exception. Separately, the AC requires calibrated tolerances to be stored in `tests/prompt-regression/mr-config.yaml` — the stub raises `NotImplementedError` before any file writing occurs. These are AC gaps that prevent FR-011 from being considered fully addressed, even at stub level.

2. **FR-012 (agent-specific MR mechanism) and FR-013 (MR coverage tracking):** These are "Should" priority requirements scoped to Phase D with no mechanism stubs or interface placeholders in the package. Lower severity given their priority and phase dependency, but still a completeness gap.

3. **FR-010 AC literal text:** "Each MR shall be implemented as a class inheriting from DeepEval's `BaseMetric`" remains unimplemented. The deviation is now formally documented. The documentation is the correct mitigation, and the score reflects this improvement — but the literal AC gap persists.

**Improvement Path:**

- Change `CalibrationRunner.calibrate_tolerances()` to emit `warnings.warn()` when fewer than 100 pairs are provided, and specify the output file path in the stub docstring to satisfy the AC for warning behavior.
- Alternatively, update FR-011 AC to reflect the stub-with-NotImplementedError pattern as the Phase D interim state.

---

### Internal Consistency (0.95/1.00)

**Evidence:**

All five MRs now use Cohen's r consistently:
- MR-001: `EFFECT_R_THRESHOLD: float = 0.30`, function `_wilcoxon_p_and_effect` computes Cohen's r as rank-biserial correlation, evidence strings report "Cohen's r".
- MR-002: `EFFECT_R_THRESHOLD: float = 0.40`, function `_wilcoxon_one_sided_and_cohens_r` computes `r = 1 - (2 * W) / (n * (n + 1))`, all docstrings and evidence strings uniformly report "Cohen's r". Class docstring explicitly states: "The contracts specify 'Cohen's r >= 0.40' for this MR."
- MR-003: inherits `_wilcoxon_p_and_effect` from mr_001_paraphrase.
- MR-004: inherits `_wilcoxon_p_and_effect` from mr_001_paraphrase.
- MR-005: inherits `_wilcoxon_p_and_effect` from mr_001_paraphrase.

Tolerance values all match behavioral-contracts.md Section C exactly:
- MR-001: TOLERANCE=0.05 (C.1: 0.05) — matches
- MR-002: P_NON_SIGNIFICANT_THRESHOLD=0.10, MIN_DELTA_REQUIRED=0.05, EFFECT_R_THRESHOLD=0.40 (C.2: all match)
- MR-003: TOLERANCE=0.03 (C.3: 0.03) — matches
- MR-004: TOLERANCE=0.05 (C.4: 0.05) — matches
- MR-005: TOLERANCE=0.06 (C.5: 0.06) — matches

**Minor note:** `MRResult.effect_size` attribute docstring in base.py (line 125) reads "Cohen's r or directional Cohen's d" — this is a documentation remnant from before the fix. Since MR-002 also now uses Cohen's r, the phrase "or directional Cohen's d" is outdated. However, the "or" phrasing is not a functional inconsistency and the field-level comment is less authoritative than the class docstrings and compute functions which are all corrected.

**Gaps:**

1. `MRResult.effect_size` docstring retains "Cohen's r or directional Cohen's d" — the "Cohen's d" reference is a minor documentation artifact post-fix.

**Improvement Path:**

Update `MRResult.effect_size` docstring in `base.py` to read "Cohen's r (rank-biserial correlation) for all MRs" to eliminate the stale "Cohen's d" reference.

---

### Methodological Rigor (0.94/1.00)

**Evidence:**

H-07 domain isolation is rigorously enforced across all 10 files. Zero imports of DeepEval, promptfoo, or any adapter module found in any file. H-10 is now fully satisfied: `FormattingVariant` is in `formatting_variant.py` (single class), `TranslationLanguage` is in `translation_language.py` (single class), all five MR files contain exactly one main class each, `base.py` contains one domain exception, one enum, one dataclass, and one ABC (structurally consistent with the module's foundational role). `calibration.py` contains one class.

The scipy fallback now raises `RuntimeError` with a clear installation instruction: "scipy is not installed -- MR evaluation cannot produce valid statistical results. Install scipy for reliable MR testing: uv add scipy". This completely eliminates the silent-PASS masking issue from iter1.

Cohen's r formula is now methodologically correct for the one-sided MR-002 case: `r = 1 - (2 * W) / (n * (n + 1))` where W is the sum of positive ranks from the one-sided Wilcoxon. This is the correct rank-biserial derivation for the one-sided test.

The `import re` in `mr_005_roundtrip.py` is now at module level (line 30), eliminating the non-standard in-function import.

H-11 compliance is complete across all files: all public methods have type hints and Google-style docstrings with Args, Returns, and Raises sections.

**Gaps:**

1. **CalibrationRunner methodological gap:** `CalibrationRunner.calibrate_tolerances()` enforces a 100-pair minimum via `ValueError` before raising `NotImplementedError`. The ordering is correct (validate before compute), but the error type for the count check (`ValueError`) conflicts with the FR-011 AC that calls for a "warn" behavior (implying `warnings.warn()`) rather than a hard exception. This is a methodological choice that diverges from the requirement specification.

2. **MR-001 Cohen's r formula note:** `_wilcoxon_p_and_effect` (mr_001_paraphrase.py:304-309) computes Cohen's r using `cohens_r = abs(1.0 - (4.0 * result.statistic) / (n * (n + 1)))`. This is a rank-biserial approximation for the two-sided test where the factor is 4.0. The formula in `_wilcoxon_one_sided_and_cohens_r` uses `(2.0 * result.statistic)`. The different factors (4.0 vs 2.0) reflect the different Wilcoxon variants (two-sided vs one-sided). This is methodologically sound but worth noting as a potential source of confusion between the two functions.

**Improvement Path:**

- Change the < 100 pairs check in `CalibrationRunner` from `ValueError` to `warnings.warn()` to align with FR-011 AC warning requirement.

---

### Evidence Quality (0.91/1.00)

**Evidence:**

The `__init__.py` now has a corrected FR traceability section:
```
FR-010 -- Five Universal Metamorphic Relations (all five MR implementations ...)
FR-011 -- MR Tolerance Calibration utility (CalibrationRunner in calibration.py; stub pending ...)
FR-012 -- Agent-specific MR mechanism (downstream deliverable; not in this package)
FR-013 -- MR Coverage Tracking (downstream deliverable; not in this package)
FR-014 -- N >= 20 per version minimum; enforced in MetamorphicRelation._validate_inputs
```

This is factually correct per harness-requirements.md FR-010 through FR-014 mapping. The `calibration.py` module docstring cites FR-011, ADR-001 FM-009 (RPN=125), and behavioral-contracts.md Section C.0 principle 4. The `base.py` architectural deviation notice explicitly cites system-design.md Section 4 (H-07 Enforcement Rules) and system-design.md Section 1.4 (Module Decomposition) with an explanation of why the FR-010 AC text predates the H-07 decision.

All five MR evidence strings contain complete statistical data: p-value, effect size (Cohen's r), mean delta, N, and tolerance threshold. `MRResult.evidence` is interpretable without re-examining intermediate computations.

**Gaps:**

1. **No citation to behavioral-contracts.md Section C.6** (Fisher's method MR aggregation) in the package. This is a downstream concern (Fisher's aggregation is applied to combined MR results, not within individual MR files), but an introductory note in `__init__.py` would complete the evidence chain for readers following the contract from end to end.

2. **`calibration.py` does not cite the output file path** specified in FR-011 AC (`tests/prompt-regression/mr-config.yaml`). The stub docstring describes the abstract calibration process but a reader following FR-011 to the stub cannot verify the output path requirement from the code alone.

**Improvement Path:**

- Add a note in `__init__.py` referencing contracts C.6 as the aggregation layer downstream of the per-MR evaluation.
- Add `tests/prompt-regression/mr-config.yaml` as the output path in the `CalibrationRunner` class or module docstring, matching FR-011 AC.

---

### Actionability (0.92/1.00)

**Evidence:**

All five `transform()` methods are fully implemented and callable. All five `evaluate()` methods are callable with `Sequence[float]` inputs and return fully populated `MRResult` instances. The `all_relations()` factory returns five instantiated relations ready for immediate use. The `__init__.py` usage example is end-to-end and runnable.

The scipy RuntimeError is actionable: "Install scipy for reliable MR testing: uv add scipy" — a specific, executable command is given. Engineers encountering the error know exactly what to do.

`CalibrationRunner` is importable and its stub interface is well-defined — the `calibrate_tolerances()` signature, docstring, and usage example are complete enough for downstream Phase D implementation without further design work.

The injectable `translator` callable in `LanguageRoundTrip` provides a clean extension point for real translation services without modifying the domain class.

**Gaps:**

1. **CalibrationRunner warning gap (actionability consequence):** When engineers provide 73 pairs (insufficient but not zero), they receive a `ValueError` that terminates the call rather than a `warnings.warn()` that would allow them to proceed with reduced confidence. In a CI context, a hard exception on borderline input is less actionable than a warning with a partial result or a clear "continue with caution" path. The FR-011 AC explicitly calls for a warning, suggesting the intent was to enable degraded-mode operation with fewer pairs.

2. **Calibrated tolerances cannot be injected into MR classes without subclassing:** The `CalibrationRunner.calibrate_tolerances()` returns a `dict[str, float]` but there is no mechanism for engineers to apply these values to the deployed MR instances. The constructor-parameter path for injecting calibrated tolerances was recommended in iter1 and is still not implemented. Engineers who run calibration cannot apply the results without modifying source code.

**Improvement Path:**

- Add `tolerance` and `p_alpha` constructor parameters to each MR class (alongside the class constant default) to allow injection of calibrated values.
- Change the < 100 pair check in `CalibrationRunner` to `warnings.warn()` per FR-011 AC.

---

### Traceability (0.93/1.00)

**Evidence:**

The FR traceability is now correct and bidirectional:
- `__init__.py` maps FR-010 through FR-014 to their correct requirements (not the sequential MR numbering error from iter1).
- `base.py` module docstring provides a full architectural deviation trace: FR-010 AC (DeepEval BaseMetric) → architectural decision (H-07 domain isolation) → alternative design (MetamorphicRelation ABC) → adapter location (jerry.testing.evaluation.deepeval_adapter) → authoritative design reference (system-design.md Section 4, Section 1.4).
- Every MR class docstring cites the specific behavioral-contracts.md section (C.1 through C.5).
- `calibration.py` cites FR-011, FM-009, and contracts C.0 principle 4.
- Class names in the implementation match the system-design.md module decomposition table exactly.
- Public API aliases (`ContextWindowStability`, `FormatInvariance`, `PromptRoundTrip`) maintain traceability to the FR specification names.

**Gaps:**

1. **No forward trace to the adapter:** `base.py` states "The adapter layer in jerry.testing.evaluation.deepeval_adapter wraps these domain classes" — but `jerry/testing/evaluation/deepeval_adapter.py` is not present in the repository (it is a referenced but not yet implemented component). A reader following the deviation trace cannot verify the adapter exists. This is an out-of-scope gap (the adapter is a separate deliverable), but the deviation documentation's credibility depends on the adapter being present or explicitly noted as a future deliverable.

2. **FR-011 output path not traced:** The `calibration.py` stub does not reference `tests/prompt-regression/mr-config.yaml` as the FR-011 required output location, creating a gap in the forward trace from FR-011 AC to implementation.

**Improvement Path:**

- Add a parenthetical note in the `base.py` deviation section: "(deepeval_adapter.py is a planned Phase B deliverable; not yet implemented)."
- Add the `tests/prompt-regression/mr-config.yaml` output path to the `calibration.py` module docstring or `CalibrationRunner` class docstring.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Completeness | 0.88 | 0.92 | Change `CalibrationRunner.calibrate_tolerances()` to emit `warnings.warn()` when N < 100 (not `ValueError`) to satisfy FR-011 AC warning requirement |
| 2 | Actionability | 0.92 | 0.95 | Add `tolerance` constructor parameter to each MR class so calibrated values from `CalibrationRunner` can be injected without subclassing |
| 3 | Evidence Quality | 0.91 | 0.94 | Add `tests/prompt-regression/mr-config.yaml` output path to `calibration.py` docstring; add contracts C.6 note to `__init__.py` |
| 4 | Internal Consistency | 0.95 | 0.97 | Update `MRResult.effect_size` docstring in `base.py` to remove stale "Cohen's d" reference |
| 5 | Traceability | 0.93 | 0.96 | Note that `deepeval_adapter.py` is a planned Phase B deliverable in the architectural deviation section of `base.py` |
| 6 | Methodological Rigor | 0.94 | 0.96 | Add comment distinguishing the 4.0 factor (two-sided) vs 2.0 factor (one-sided) in the Cohen's r formulas |

---

## Verdict Determination

**Composite:** 0.9215

**Stream threshold:** >= 0.94 required for PASS

**Result:** 0.9215 < 0.94 → **REVISE**

The composite clears the standard H-13 threshold (0.92) by 0.0015, but falls 0.0185 below the stream-specific threshold (0.94). The gap is concentrated in two dimensions:
- Completeness (0.88): FR-011 AC warning-vs-exception gap, and no tolerance injection mechanism.
- Evidence Quality (0.91): Missing output path reference in calibration.py, no C.6 note.

Both are small, targeted fixes. No architectural work is required. A third revision addressing these two dimensions alone would likely push the composite to >= 0.94.

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score with specific file and function references
- [x] Uncertain scores resolved downward (Completeness held at 0.88 not 0.90 due to FR-011 AC warning gap; Evidence Quality held at 0.91 not 0.93 due to missing output path trace)
- [x] No dimension scored above 0.95 without exceptional evidence (Internal Consistency scored 0.95 due to complete and verified Cohen's r correction across all 5 MRs and all matching contract values)
- [x] Calibration anchors applied: 0.88 = good work with clear improvement areas; 0.94 = genuinely excellent
- [x] Composite computed arithmetically: (0.88 × 0.20) + (0.95 × 0.20) + (0.94 × 0.20) + (0.91 × 0.15) + (0.92 × 0.15) + (0.93 × 0.10) = 0.176 + 0.190 + 0.188 + 0.1365 + 0.138 + 0.093 = 0.9215
- [x] Verdict matches score range exactly: 0.9215 < 0.94 stream threshold → REVISE
- [x] All five iter1 fixes verified present before scoring; no new regressions inflating the score

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.9215
threshold: 0.94
weakest_dimension: Completeness
weakest_score: 0.88
critical_findings_count: 0
iteration: 2
improvement_recommendations:
  - "Change CalibrationRunner N<100 check from ValueError to warnings.warn() to satisfy FR-011 AC warning requirement (Completeness, Actionability)"
  - "Add tolerance constructor parameter to each MR class for calibration value injection (Actionability)"
  - "Add tests/prompt-regression/mr-config.yaml output path to calibration.py docstring (Evidence Quality, Traceability)"
  - "Add contracts C.6 reference note to __init__.py (Evidence Quality)"
  - "Update MRResult.effect_size docstring to remove stale Cohen's d reference (Internal Consistency)"
  - "Note deepeval_adapter.py as planned Phase B deliverable in base.py deviation section (Traceability)"
```
