# Quality Score Report: Stream 3C — Layer 3 Metamorphic Relation Framework

## L0 Executive Summary

**Score:** 0.857/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Completeness (0.82)

**One-line assessment:** The five MR implementations are structurally solid with correct tolerance values, strong H-07 domain isolation, and thorough traceability — but two deficiencies block PASS: FR-010 acceptance criteria literally require DeepEval `BaseMetric` inheritance (the domain-ABC approach is architecturally justified but creates a gap), and MR-002 uses Cohen's d where behavioral-contracts.md Section C.2 specifies Cohen's r, a metric-type mismatch that must be resolved or explicitly documented as an architectural deviation.

---

## Scoring Context

- **Deliverable:** `jerry/testing/metamorphic/` (7 files: `__init__.py`, `base.py`, `mr_001_paraphrase.py`, `mr_002_negation.py`, `mr_003_context.py`, `mr_004_formatting.py`, `mr_005_roundtrip.py`)
- **Deliverable Type:** Code (Domain Layer Implementation)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Stream Threshold:** >= 0.94 (PASS), 0.85-0.93 (REVISE), < 0.85 (REJECTED)
- **Scored:** 2026-03-07T00:00:00Z

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.857 |
| **Stream Threshold** | 0.94 (PASS) |
| **Standard Threshold** | 0.92 (H-13) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.82 | 0.164 | All 5 MRs and base ABC present; FR-010 AC requires DeepEval BaseMetric inheritance which is not implemented; FR-011 calibration utility absent from these 7 files |
| Internal Consistency | 0.20 | 0.83 | 0.166 | Tolerances match contracts exactly for MR-001, 003, 004, 005; MR-002 uses Cohen's d where contracts C.2 specifies Cohen's r |
| Methodological Rigor | 0.20 | 0.87 | 0.174 | H-07 domain isolation enforced throughout; Wilcoxon correctly applied; mr_004 and mr_005 each contain two classes (Enum + main class), a mild H-10 concern |
| Evidence Quality | 0.15 | 0.89 | 0.1335 | FR-xxx traceability in `__init__.py`, contracts section citations in every file, ADR-001 and LLMORPH references, complete evidence strings in MRResult |
| Actionability | 0.15 | 0.88 | 0.132 | All transform() and evaluate() methods fully implemented and callable; scipy fallback silently returns p=1.0 masking violations without user warning |
| Traceability | 0.10 | 0.87 | 0.087 | FR-010 through FR-014 mapped in `__init__.py`; all class names match system-design.md module decomposition; H-07/H-10 referenced in every module |
| **TOTAL** | **1.00** | | **0.857** | |

---

## Detailed Dimension Analysis

### Completeness (0.82/1.00)

**Evidence:**

All seven files specified in the task are present and non-empty. All five MR implementations (MR-001 through MR-005) are delivered with both `transform()` and `evaluate()` methods fully implemented. The base module (`base.py`) provides the `MetamorphicRelation` ABC, `MRResult` frozen dataclass, `MRViolationSeverity` enum, and `InsufficientSamplesError` domain exception. The `__init__.py` provides a complete public API with `__all__`, an `all_relations()` factory, public API aliases (`ContextWindowStability`, `FormatInvariance`, `PromptRoundTrip`), and usage examples. FR-014 (N >= 20 enforcement) is implemented in `_validate_inputs()` raising `InsufficientSamplesError`.

**Gaps:**

1. **FR-010 AC literal deviation:** FR-010 acceptance criteria state "Each MR shall be implemented as a class inheriting from DeepEval's `BaseMetric` with a `measure(test_case: LLMTestCase) -> float` method returning 0.0 (violation) or 1.0 (pass)." The implementation uses a custom `MetamorphicRelation` ABC and returns `MRResult` objects — not `BaseMetric` + `measure()`. The system-design.md explicitly justifies this as H-07 domain isolation (adapter layer wraps domain classes for DeepEval integration). This is architecturally sound, but the gap between the FR-010 acceptance criteria letter and the implementation is not documented as a formal deviation or accepted requirement waiver within the deliverable itself. A grader applying the rubric literally must count this as a completeness gap.

2. **FR-011 calibration utility absent:** FR-011 (MR Tolerance Calibration from Real Output Pairs, "Must" priority) requires a calibration utility that accepts 100+ output pairs and computes empirical tolerance values. No calibration function, module, or stub is present in the 7 delivered files. FR-011 is explicitly in the Layer 3 requirement scope (lines 349-367 of harness-requirements.md). This is a gap even if FR-011 implementation is deferred to a later phase.

3. **FR-012 (agent-specific MR mechanism) and FR-013 (MR coverage tracking):** Both are "Should" priority and are downstream deliverables, but neither has a stub or interface placeholder in the delivered files. These are lower severity gaps.

**Improvement Path:**

- Either add a formal deviation note in `__init__.py` acknowledging that `MetamorphicRelation` + `MRResult` is the domain interface and the DeepEval `BaseMetric` adapter lives in `evaluation/deepeval_adapter.py` (and verify that adapter exists), or update FR-010 AC text to reflect the architecture.
- Add a calibration module stub (`calibration.py`) to the package with the interface signature for FR-011, even if unimplemented.

---

### Internal Consistency (0.83/1.00)

**Evidence:**

Tolerance values for MR-001, MR-003, MR-004, and MR-005 match behavioral-contracts.md Section C exactly:
- MR-001: `TOLERANCE = 0.05` (contracts C.1: 0.05) — matches
- MR-003: `TOLERANCE = 0.03` (contracts C.3: 0.03) — matches
- MR-004: `TOLERANCE = 0.05` (contracts C.4: 0.05) — matches
- MR-005: `TOLERANCE = 0.06` (contracts C.5: 0.06) — matches

MR-002 `minimum_sample_size = 15` (contracts C.2: "15 pairs") — matches. MR-002 violation conditions (`p >= 0.10 AND mean_delta < 0.05`) match contracts C.2. All class names, `mr_id` values, and `mr_name` strings are internally consistent across `__init__.py`, `base.py`, and the five MR files. The `MRResult` fields used in each `evaluate()` method are consistent with the dataclass definition in `base.py`.

**Gaps:**

**Cohen's r vs. Cohen's d for MR-002:** behavioral-contracts.md Section C.2 states the effect size metric as "Cohen's r >= 0.40 (large effect expected for constraint negation)". The `NegationHandling` class uses `EFFECT_D_THRESHOLD: float = 0.40` and the `_wilcoxon_and_cohens_d()` function computes Cohen's d (standardized mean difference using pooled standard deviation). These are different metrics: Cohen's r is the rank-biserial correlation coefficient derived from the Wilcoxon statistic; Cohen's d is the standardized mean difference using standard deviations. The implementation choice of d is statistically defensible (Cohen's d is the more natural effect size for a directional comparison of means), but it creates a named inconsistency between the contracts document and the implementation. The evidence strings in `evaluate()` report "Cohen's d" when the contracts specify "Cohen's r". This inconsistency means the calibrated threshold (0.40) cannot be directly compared across MRs without knowing which effect size metric each uses.

The task specification's own description says "MR-002=Cohen's d>=0.40" which aligns with the code, but the behavioral contracts document says "Cohen's r >= 0.40". The inconsistency between the reference documents and between the reference document and the code must be flagged here even if the code is self-consistent.

**Improvement Path:**

Either update behavioral-contracts.md Section C.2 to read "Cohen's d >= 0.40" with a rationale note explaining why d is more appropriate for MR-002's directional test, or update the implementation to use Cohen's r (rank-biserial correlation) for consistency with the other four MRs and the contracts document.

---

### Methodological Rigor (0.87/1.00)

**Evidence:**

H-07 domain isolation is rigorously enforced. A search across all 7 files finds zero imports of DeepEval, promptfoo, or any adapter module. The only external dependency is `scipy.stats.wilcoxon`, imported conditionally with a `try/except ImportError` fallback. The Wilcoxon signed-rank test is applied correctly throughout:
- Two-sided alternative for symmetric MRs (001, 003, 004, 005): `alternative="two-sided"` — correct per contracts C.1/C.3/C.4/C.5.
- One-sided alternative for directional MR-002: `alternative="greater"` — correct per contracts C.2 ("tests for presence of effect, not absence").
- `zero_method="wilcox"` used consistently, matching the contracts D.1 "scipy default" specification.

H-11 compliance is complete: all public methods have type hints and Google-style docstrings with Args, Returns, and Raises sections. H-10 compliance (one class per file) holds for the primary classes. H-20 BDD test-first: test infrastructure is not part of this deliverable but the domain classes are written with testability in mind (deterministic transforms, injectable translator in MR-005).

Effect size computations are methodologically sound: Cohen's r via rank-biserial approximation for MR-001/003/004/005; Cohen's d via pooled standard deviation for MR-002. The dual-condition violation requirement (both statistical AND practical significance) is correctly implemented in all five MRs, reducing false positive rate as documented in the LLMORPH study citation.

**Gaps:**

1. **H-10 mild concern:** `mr_004_formatting.py` contains two classes: `FormattingVariant(str, Enum)` and `FormattingPerturbation(MetamorphicRelation)`. Similarly, `mr_005_roundtrip.py` contains `TranslationLanguage(str, Enum)` and `LanguageRoundTrip(MetamorphicRelation)`. H-10 states "One class per file." Having an Enum (which is a class) plus a main class in the same file is a mild violation. The Enums could be moved to a shared `enums.py` or `types.py` within the metamorphic package.

2. **scipy fallback behavior:** When scipy is unavailable, `_wilcoxon_p_and_effect` returns `(1.0, 0.0)`, which causes `evaluate()` to always return PASS (p=1.0 is never < 0.05, so no violation is ever declared). This silent masking is methodologically dangerous: users running in environments without scipy will receive all-PASS results with no indication that statistical testing was skipped. The fallback should log a warning or raise an informational exception.

3. **`import re` inside function body:** In `mr_005_roundtrip.py`, `_apply_vocabulary_substitution()` contains `import re` inside the function. While functionally harmless (Python caches imports), this is non-standard and would be flagged by linting tools.

**Improvement Path:**

- Move `FormattingVariant` and `TranslationLanguage` to a shared `enums.py` within the metamorphic package to satisfy H-10 strictly.
- Add a `logging.warning()` call in the scipy fallback path to alert users that statistical testing is disabled.
- Move `import re` to module level in `mr_005_roundtrip.py`.

---

### Evidence Quality (0.89/1.00)

**Evidence:**

The `__init__.py` module docstring provides explicit FR traceability:
```
FR-010  -- five universal MRs; ParaphraseConsistency (MR-001) is the first
FR-011  -- NegationHandling (MR-002 Negation Sensitivity)
FR-012  -- ContextWindowStability / IrrelevantContextAppendation (MR-003)
FR-013  -- FormatInvariance / FormattingPerturbation (MR-004)
FR-014  -- PromptRoundTrip / LanguageRoundTrip (MR-005)
FR-014 also requires N>=20 per version minimum; enforced in MetamorphicRelation base
```

Each MR file header cites the specific behavioral contracts section (C.1 through C.5) and includes exact tolerance values, statistical parameters, and violation conditions. The `base.py` module explicitly references "ADR-001 FM-002" for the N>=20 rationale. The `__init__.py` cites the LLMORPH study (ASE 2024, 560,000 tests, 8.6% false positive rate). Evidence strings in `MRResult.evidence` include all relevant statistical values (p-value, effect size, mean delta, N) making results interpretable without requiring re-examination of intermediate computations.

**Gaps:**

1. The FR-010 through FR-014 mapping in `__init__.py` has a minor confusion: the docstring maps FR-011 to "NegationHandling (MR-002)" and FR-012 to "ContextWindowStability / IrrelevantContextAppendation (MR-003)". However, FR-011 is the calibration utility requirement, not the MR-002 implementation. FR-012 is the agent-specific MR mechanism, not MR-003. The traceability comment appears to map requirement IDs to MR IDs sequentially (FR-010=MR-001, FR-011=MR-002, etc.) which is incorrect. The correct mapping from harness-requirements.md is: FR-010 covers all five universal MRs; FR-011 is calibration utility; FR-012 is agent-specific MR; FR-013 is coverage tracking; FR-014 is N>=20 enforcement.

2. No explicit citation of behavioral-contracts.md Section C.6 (Fisher's method MR aggregation) — this is downstream of the delivered files but noting it as a gap for completeness of the evidence chain.

**Improvement Path:**

Correct the FR traceability mapping in `__init__.py` to accurately reflect what each requirement covers rather than sequential MR-to-FR mapping.

---

### Actionability (0.88/1.00)

**Evidence:**

All five `transform()` methods produce actual transformed strings using deterministic, dependency-free logic (regex substitution, vocabulary tables, random with seeded RNG). None are abstract stubs. All five `evaluate()` methods are callable with `Sequence[float]` inputs and return fully populated `MRResult` instances. The `all_relations()` factory returns five instantiated relations ready for immediate use. The `__init__.py` usage example is end-to-end:

```python
mr = ParaphraseConsistency()
transformed_prompt = mr.transform(original_prompt)
original_scores = run_agent(original_prompt, n=30)
transformed_scores = run_agent(transformed_prompt, n=30)
result: MRResult = mr.evaluate(original_scores, transformed_scores)
```

MR-003's seeded RNG (`random.Random(self._seed)`) ensures deterministic context selection. MR-004's dispatch table provides four distinct transformation variants. MR-005's injectable `translator` callable provides a clean extension point for real translation services.

**Gaps:**

1. **scipy fallback masks violations silently:** When `scipy` is not installed, `evaluate()` always returns PASS. This is functionally unusable for the primary purpose of these classes (detecting violations). No user-visible warning is produced. The fallback should at minimum set `p_value = float('nan')` or `evidence` should note "Statistical test skipped: scipy not available."

2. **FR-011 calibration is not actionable from these files:** The tolerance values are hardcoded; there is no path for engineers to recalibrate them against real output pairs without modifying the source. This limits the operational utility for the contracts' requirement that "tolerances should be calibrated against baseline data."

**Improvement Path:**

- Emit a `warnings.warn()` when scipy is unavailable so users are not silently misled.
- Add tolerance as a constructor parameter in each MR class (alongside the hardcoded class constant default) so calibrated values can be injected without subclassing.

---

### Traceability (0.87/1.00)

**Evidence:**

The `__init__.py` "Requirement traceability" section explicitly maps FR identifiers. Every class docstring references the governing contracts section. Every module header includes H-07 and H-10 compliance statements. Class names in the implementation (`ParaphraseConsistency`, `NegationHandling`, `IrrelevantContextAppendation`, `FormattingPerturbation`, `LanguageRoundTrip`) match the system-design.md module decomposition table exactly (lines 301-305 of system-design.md). Public API aliases (`ContextWindowStability = IrrelevantContextAppendation`, `FormatInvariance = FormattingPerturbation`, `PromptRoundTrip = LanguageRoundTrip`) provide traceability back to the canonical names in the task specification and FR text.

**Gaps:**

1. The FR traceability comment in `__init__.py` maps requirement IDs incorrectly (sequential FR-011=MR-002 rather than FR-011=calibration utility). This creates a traceability error: a reader following the FR-011 trace would land at NegationHandling, not the calibration utility. This is a factual traceability defect, not merely a style issue.

2. FR-010 AC requirement for `BaseMetric` inheritance is not traced anywhere in the delivered files to the architectural decision that justified the deviation. There is no comment, ADR reference, or note linking the domain ABC choice to the H-07 rationale or to a specific section of system-design.md.

**Improvement Path:**

- Correct the FR traceability mapping in `__init__.py`.
- Add a comment in `base.py` or `__init__.py` citing the system-design.md section (1.4 Module Decomposition, H-07 Enforcement Rules) that explicitly justifies why `MetamorphicRelation` is a domain ABC rather than a `DeepEval.BaseMetric` subclass.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Completeness | 0.82 | 0.90 | Add formal architectural deviation note for FR-010 AC (BaseMetric not inherited); add calibration stub module interface for FR-011 |
| 2 | Internal Consistency | 0.83 | 0.92 | Resolve Cohen's r vs. Cohen's d for MR-002: either update contracts C.2 to say "d" with rationale, or switch implementation to Cohen's r to match contracts and the other four MRs |
| 3 | Traceability | 0.87 | 0.93 | Correct the FR traceability mapping in `__init__.py` (FR-011 is calibration utility, not MR-002); add system-design.md cross-reference for the domain-ABC architectural decision |
| 4 | Methodological Rigor | 0.87 | 0.93 | Move `FormattingVariant` and `TranslationLanguage` enums to a shared `enums.py` to satisfy H-10; add scipy unavailability warning; move module-level `import re` to top of `mr_005_roundtrip.py` |
| 5 | Actionability | 0.88 | 0.93 | Emit `warnings.warn()` when scipy fallback activates; add tolerance as constructor parameter for calibration injection |
| 6 | Evidence Quality | 0.89 | 0.93 | Correct FR traceability comment; add citation to contracts C.6 (Fisher's method aggregation) as a note for downstream implementers |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score with specific file and line references
- [x] Uncertain scores resolved downward (Internal Consistency scored 0.83 not 0.85 due to Cohen's r/d discrepancy)
- [x] First-draft calibration applied (implementation is high quality for a first iteration; scores reflect genuine gaps not overly penalized)
- [x] No dimension scored above 0.95 without exceptional evidence
- [x] Composite computed arithmetically: 0.82(0.20) + 0.83(0.20) + 0.87(0.20) + 0.89(0.15) + 0.88(0.15) + 0.87(0.10) = 0.164 + 0.166 + 0.174 + 0.1335 + 0.132 + 0.087 = 0.857

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.857
threshold: 0.94
weakest_dimension: Completeness
weakest_score: 0.82
critical_findings_count: 0
iteration: 1
improvement_recommendations:
  - "Add formal FR-010 deviation note citing system-design.md H-07 justification, or add BaseMetric adapter"
  - "Resolve MR-002 Cohen's r vs. Cohen's d discrepancy with contracts C.2"
  - "Correct FR traceability mapping in __init__.py (FR-011 is calibration utility, not MR-002)"
  - "Move FormattingVariant and TranslationLanguage enums to shared enums.py (H-10)"
  - "Add warnings.warn() when scipy fallback activates to prevent silent masking"
  - "Add tolerance as constructor parameter for calibration injection (FR-011 support)"
```
