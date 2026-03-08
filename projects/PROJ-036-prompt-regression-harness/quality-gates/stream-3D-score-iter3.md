# Quality Score Report: Stream 3D — Layer 4 Statistical Comparison Engine (Iteration 3)

## L0 Executive Summary

**Score:** 0.892/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Internal Consistency (0.86)
**One-line assessment:** Iteration 3 successfully resolves the iter2 port-abstraction defect (Layer4Pipeline now typed to BaselinePersistencePort and ReportOutputPort), but three residual issues block the 0.94 C4 threshold: stale concrete-type references in the layer4_stats.py module docstring, an orphaned class attribute (_MIN_FULL_SAMPLES) that is defined but never used, and a "Public API" comment label applied to an underscore-prefixed attribute — all three are Internal Consistency or Completeness defects that collectively hold the composite below threshold.

---

## Scoring Context

- **Deliverable:** `jerry/testing/` (10 files: types.py, stats.py, layer4_stats.py, baselines/__init__.py, baselines/store.py, baselines/ports.py, reports/__init__.py, reports/generator.py, reports/ports.py, __init__.py)
- **Deliverable Type:** Code
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** .context/rules/quality-enforcement.md
- **Stream Threshold:** 0.94 PASS (C4 criticality, elevated above standard 0.92)
- **Prior Scores:** 0.874 (iter1), 0.934 (iter2, NOTE: iter2 score applied a different file set; iter3 is the corrected deliverable)
- **Scored:** 2026-03-07T00:00:00Z

---

## Iter2 Fix Verification (REQUIRED)

The primary iter2 defect was: Layer4Pipeline.__init__ used concrete types `BaselineStore` and `ReportGenerator | None` as parameter types, violating the hexagonal port abstraction.

| Fix | Location | Status | Evidence |
|-----|----------|--------|----------|
| `baseline_store` parameter typed to port | layer4_stats.py line 88 | CONFIRMED | `baseline_store: BaselinePersistencePort` |
| `report_generator` parameter typed to port | layer4_stats.py line 89 | CONFIRMED | `report_generator: ReportOutputPort \| None = None` |
| Import changed from store to port | layer4_stats.py line 33 | CONFIRMED | `from jerry.testing.baselines.ports import BaselinePersistencePort` |
| Import changed from generator to port | layer4_stats.py line 34 | CONFIRMED | `from jerry.testing.reports.ports import ReportOutputPort` |
| Concrete ReportGenerator retained for default factory only | layer4_stats.py line 99 | CONFIRMED | `self._gen = report_generator or ReportGenerator()` — correct hexagonal pattern (accept port, default to concrete) |

**Iter2 fix verdict: VERIFIED COMPLETE.**

---

## Key Contract Verification

| Contract | Required Value | Actual Value | Location | Status |
|----------|---------------|--------------|----------|--------|
| BONFERRONI_ALPHA_FULL | literal 0.004 (NOT computed) | `0.004` (literal) | stats.py line 80 | PASS |
| MIN_STATISTICAL_SAMPLE_SIZE | 20 | `20` | stats.py line 63 | PASS |
| QUALITY_PASS_THRESHOLD | 0.92 | `0.92` | stats.py line 68 | PASS |
| BONFERRONI_K_FULL_SUITE | 13 | `13` | stats.py line 73 | PASS |
| H-07 types.py stdlib-only | stdlib only | `dataclasses`, `datetime`, `enum` | types.py lines 19-21 | PASS |
| H-07 stats.py stated contract | stdlib + scipy + statsmodels + jerry.testing.types | Confirmed in imports | stats.py lines 38-55 | PASS |
| H-10 one class per file | Layer4Pipeline only | Only `Layer4Pipeline` class defined | layer4_stats.py | PASS |
| H-10 one class per file | BaselineStore only | Only `BaselineStore` class defined | store.py | PASS |
| H-10 one class per file | ReportGenerator only | Only `ReportGenerator` class defined | generator.py | PASS |
| @runtime_checkable on ports | Both ports | `@runtime_checkable` decorator applied | ports.py line 31, reports/ports.py line 32 | PASS |
| merge_decision_from_classification PUBLIC | No underscore prefix | `def merge_decision_from_classification(` | stats.py line 472 | PASS |
| wilcoxon_signed_rank PUBLIC | No underscore prefix | `def wilcoxon_signed_rank(` | stats.py line 244 | PASS |
| bonferroni_correction PUBLIC | No underscore prefix | `def bonferroni_correction(` | stats.py line 366 | PASS |

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.892 |
| **Stream Threshold** | 0.94 (C4 stream requirement) |
| **Standard Threshold** | 0.92 (H-13) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.90 | 0.180 | All 10 files present, all contracts verified; _MIN_FULL_SAMPLES defined but orphaned |
| Internal Consistency | 0.20 | 0.86 | 0.172 | 3 specific inconsistencies: stale docstring concrete references, orphaned attribute, mismatched naming convention |
| Methodological Rigor | 0.20 | 0.90 | 0.180 | Strong hexagonal design throughout; one orphaned constant reduces rigor |
| Evidence Quality | 0.15 | 0.90 | 0.135 | FR citations and statistical references throughout; external contracts not verifiable in-scope |
| Actionability | 0.15 | 0.88 | 0.132 | Clear usage examples and error messages; multi-metric k-override pattern not exemplified |
| Traceability | 0.10 | 0.93 | 0.093 | Near-complete FR cross-referencing with acceptance criteria quoted inline |
| **TOTAL** | **1.00** | | **0.892** | |

---

## Detailed Dimension Analysis

### Completeness (0.90/1.00)

**Evidence:**

All 10 deliverable files are implemented and contain the specified content:
- `types.py`: ScoreArray, RegressionResult, ComparisonReport, MultiMetricResult, BaselineRecord, BaselineAuditEntry, RegressionClass, RateClass, EffectSizeLabel, EvaluationMode, MergeDecision — all present.
- `stats.py`: compare_versions(), compare_multiple_metrics(), wilcoxon_signed_rank(), wilson_score_intervals(), bonferroni_correction(), all named constants — all present.
- `layer4_stats.py`: Layer4Pipeline with run(), run_single_metric(), write_report() — run() and run_single_metric() present. Note: write_report() is NOT a method on Layer4Pipeline; file persistence is handled by _persist_report() (private). The task specification listed write_report() as a method, but the implementation uses _persist_report() and exposes persistence via run() arguments. This is a minor scope deviation.
- `baselines/__init__.py`: Exports BaselineStore and BaselinePersistencePort — confirmed.
- `baselines/store.py`: BaselineStore with quality-gated store/retrieve, N>=30 enforcement, invalidation, audit — all methods present.
- `baselines/ports.py`: BaselinePersistencePort Protocol with @runtime_checkable — confirmed.
- `reports/__init__.py`: Exports ReportGenerator and ReportOutputPort — confirmed.
- `reports/generator.py`: from_single_metric(), from_multi_metric(), smoke_mode_report(), to_markdown(), to_json() — all present.
- `reports/ports.py`: ReportOutputPort Protocol with @runtime_checkable — confirmed.
- `__init__.py`: FR-019 public API exports per docstring — confirmed. Exports: compare_versions, compare_multiple_metrics, wilson_score_intervals, merge_decision_from_classification, InsufficientSamplesError, MIN_STATISTICAL_SAMPLE_SIZE, QUALITY_PASS_THRESHOLD, BONFERRONI_K_FULL_SUITE, BONFERRONI_ALPHA_FULL, RegressionResult, RegressionClass, ScoreArray.

**Gaps:**

1. `write_report()` as a named public method on Layer4Pipeline does not exist. The specification listed it, but the implementation exposes persistence through `run()` parameters `output_json_path` and `output_markdown_path`, and the private `_persist_report()`. This is a completeness gap relative to the specification, though the functionality is implemented.

2. `BaselineStore._MIN_FULL_SAMPLES: int = 30` is defined as a class attribute (line 102) but is never referenced anywhere in the class implementation. The `store()` method's `min_samples` parameter defaults to `30` directly without referencing this constant. The constant exists but is effectively dead code. This reduces completeness: the constant does not serve its stated purpose as a named, referenceable threshold.

**Improvement Path:**
- Either rename `_persist_report` to `write_report` and expose it as a public method, OR update the specification to reflect that persistence is handled through run() arguments.
- Either reference `_MIN_FULL_SAMPLES` in the `store()` method's default parameter (`min_samples: int = _MIN_FULL_SAMPLES`), OR remove the class attribute and keep only the inline default.

---

### Internal Consistency (0.86/1.00)

**Evidence:**

Most of the codebase is internally consistent. Classification logic in `_classify_regression()` matches the classification table in `RegressionClass` docstring exactly. Constants are consistently valued across modules (QUALITY_PASS_THRESHOLD = 0.92 in stats.py; _BASELINE_QUALITY_GATE = 0.92 in store.py — deliberate duplication with documented rationale). Port interfaces match concrete implementations in method signatures.

**Gaps:**

Three specific inconsistencies were identified:

1. **Stale module docstring in layer4_stats.py:** The responsibilities list in the module docstring (lines 8-14) reads:
   ```
   - Interact with the baseline store (BaselineStore).
   - Call the report generator (ReportGenerator).
   ```
   After the iter2 fix, the class interacts with `BaselinePersistencePort` and `ReportOutputPort`, not the concrete types. The docstring was not updated. This is an internal inconsistency between the stated module responsibility and the actual implementation. The dependency direction comment at line 18-22 correctly says "adapter → adapter via port" but the responsibilities list contradicts it by naming concrete types.

2. **"Public API" comment on underscore-prefixed attribute:** `BaselineStore._MIN_FULL_SAMPLES` (store.py line 102) is preceded by the comment `#: Minimum number of scores required for FULL mode baselines.` and is labeled with `# Public API` in the in-line comment structure (the section header comment directly before it says `# Public API`). However, the attribute uses the `_` prefix convention which signals private/internal access. This is a naming inconsistency: the comment signals public but the naming convention signals private.

3. **Orphaned constant creates dead code:** `BaselineStore._MIN_FULL_SAMPLES: int = 30` is defined at class scope but `store()` method uses `min_samples: int = 30` as a direct literal default without referencing `_MIN_FULL_SAMPLES`. The constant is defined but never consumed, creating dead code inconsistency between the declared interface (a named constant for the minimum) and the actual usage (a hardcoded literal in the default parameter).

**Improvement Path:**
- Update layer4_stats.py module docstring to reference `BaselinePersistencePort` and `ReportOutputPort` instead of concrete types.
- Either remove the underscore from `_MIN_FULL_SAMPLES` (making it `MIN_FULL_SAMPLES`) and reference it in `store(min_samples: int = _MIN_FULL_SAMPLES)`, or remove the "Public API" comment heading, or remove the constant entirely.

---

### Methodological Rigor (0.90/1.00)

**Evidence:**

Hexagonal architecture is properly applied across all 10 files:
- Domain layer (types.py, ports.py files): stdlib-only imports, defining data contracts and port interfaces.
- Adapter layer (store.py, generator.py): depend on domain, not on other adapters.
- Orchestration adapter (layer4_stats.py): imports from both domain and adapter layers through ports; does not re-implement statistical logic.

Statistical methodology is sound:
- Wilcoxon signed-rank uses two-sided alternative with scipy (line 280-285 in stats.py).
- Cohen's r computed via normal approximation with correct mu_W and var_W formulas (lines 205-212).
- Wilson CI uses statsmodels with method="wilson" — correct for non-Wald CI (lines 342-347).
- N>=20 enforcement is at the public API entry point (compare_versions), not in the raw Wilcoxon function — documented design choice (stats.py line 261).
- Belt-and-suspenders guard: MARGINAL + RATE_REGRESSION promoted to REGRESSION (stats.py lines 608-612).
- Worst-case aggregation for multi-metric results with severity ordering — correct approach.
- BaselineStore uses SHA-256 hash truncated to 16 hex chars for filesystem-safe filenames — sound approach.
- Version key format validation enforces ":" separator with non-empty parts.
- `bonferroni_correction()` validates k>=1 and alpha_family in (0,1).

**Gaps:**

1. **Orphaned class attribute reduces rigor:** `BaselineStore._MIN_FULL_SAMPLES: int = 30` is defined at class scope but never referenced in `store(min_samples: int = 30)`. A named constant that is defined but never used creates a maintenance hazard — if someone updates `_MIN_FULL_SAMPLES` expecting it to change the enforcement threshold, it will have no effect. The methodological rigor score is reduced because the intended "named constant" pattern is not actually implemented consistently.

2. **Alpha range lower bound is wider than FR-015 specification:** stats.py line 590 accepts alpha down to 0.001, but the comment says "FR-015 specifies (0.01, 0.10) for uncorrected single-metric use." The code correctly accommodates Bonferroni-corrected alpha (0.004), but the range `[0.001, 0.10]` is not fully documented as a deliberate design decision with a source. The comment at line 590-595 explains the rationale informally — this is acceptable but could be more precise.

**Improvement Path:**
- Reference `_MIN_FULL_SAMPLES` in the `store()` method signature: `min_samples: int = _MIN_FULL_SAMPLES`.
- Optionally, make `_MIN_FULL_SAMPLES` a public constant (remove underscore) to make it part of the BaselineStore public API.

---

### Evidence Quality (0.90/1.00)

**Evidence:**

All statistical methods cite primary sources:
- Wilcoxon (1945) cited in stats.py module docstring and `wilcoxon_signed_rank()` docstring.
- Wilson (1927) cited in module docstring and `wilson_score_intervals()` docstring.
- Cohen (1988) cited in effect size computation, `_cohens_r()` docstring, and `EffectSizeLabel` docstring.
- scipy and statsmodels doc references [7] and [8] cited.

FR acceptance criteria are quoted verbatim in docstrings:
- FR-014: "The N=20 threshold shall be a named constant" — quoted at stats.py line 62.
- FR-016: "The 0.92 pass-rate threshold shall be the named constant QUALITY_PASS_THRESHOLD" — quoted at stats.py line 66.
- FR-017: "The regression report shall disclose the Bonferroni correction" — quoted in BonferroniConfig.description docstring.
- FR-020: "verify that the candidate baseline's quality score passes the quality gate (>= 0.92)" — quoted in store.py line 120.

Mathematical derivations are documented:
- `_cohens_r()` shows mu_W and var_W formulas with variable definition (lines 203-212).
- BONFERRONI_ALPHA_FULL comment explicitly explains why 0.004 is used as a literal vs. computed: "round(0.05/13, 4) = 0.0038, which would be a 5% relative error" (stats.py lines 76-80).

Classification logic is traced to `behavioral-contracts.md Section D.4` with the exact table reproduced in both `RegressionClass` docstring and `_classify_regression()` docstring.

**Gaps:**

1. External documents (behavioral-contracts.md, baselines/protocol.md) are frequently cited but are not within the scored file set. The implementation appears consistent with the cited contracts, but this cannot be independently verified from the 10 files alone. Specifically: "baselines/protocol.md specifies N=30 as the absolute minimum" is cited three times in store.py but the protocol document is external.

2. The rate-class promotion logic ("belt-and-suspenders guard" at stats.py lines 608-612) is implemented but not traced to a specific FR or contract requirement — it appears to be an implicit design decision without a citation.

**Improvement Path:**
- Add a citation for the rate-class promotion logic (e.g., a reference to the specific behavioral contract section that motivates the belt-and-suspenders guard, or a note that it is an implementation-level defense-in-depth decision not required by a specific FR).

---

### Actionability (0.88/1.00)

**Evidence:**

Layer4Pipeline has a complete, runnable usage example in the class docstring (lines 62-83 in layer4_stats.py) showing exact method signature with realistic argument values.

BaselineStore has a usage example showing store() and retrieve() patterns with realistic inputs (lines 66-81 in store.py).

ReportGenerator has a usage example (lines 50-57 in generator.py).

Port interfaces show usage examples with explicit type annotation patterns:
- `store: BaselinePersistencePort = BaselineStore(Path("baselines/data"))` in ports.py.
- `gen: ReportOutputPort = ReportGenerator()` in reports/ports.py.

Error messages are specific and actionable:
- InsufficientSamplesError: "Wilcoxon requires N >= 20 per version (got {N_a}, {N_b}). Use Smoke mode for single-run structural checks only." — tells the user what to do.
- Invalidated baseline error: "Re-collect the baseline using Full mode (N=30)." — explicit remediation.
- Quality gate rejection in store(): includes agent_id, metric_id, and version_key in the error message.

CI/CD integration is actionable:
- Exit codes 0/1/2 documented in run() and _exit_code() docstrings.
- GHA output variable names documented (verdict, merge_recommendation, agent, evaluation_mode, dimension_driver).
- Fallback to stdout for local development.

**Gaps:**

1. **Multi-metric k-override usage pattern not exemplified.** The compare_multiple_metrics() docstring states: "For the full 13-metric suite, pass k=BONFERRONI_K_FULL_SUITE to ensure the correct correction is applied even when not all metrics are present in a given call." This is the critical usage pattern for production, but no usage example demonstrates it. The Layer4Pipeline.run() docstring shows `metric_scores` as a dict but does not show how to set `bonferroni_k=BONFERRONI_K_FULL_SUITE` when fewer than 13 metrics are present.

2. **`smoke_mode_report()` docstring notes "not statistically valid" but does not explain what structural_violations should contain** — no schema or format specification for violation strings beyond "list[str]".

**Improvement Path:**
- Add a concrete usage example in compare_multiple_metrics() showing `k=BONFERRONI_K_FULL_SUITE` override when only a subset of 13 metrics is available.
- Consider adding a note in the Layer4Pipeline.run() docstring showing when to set `bonferroni_k=BONFERRONI_K_FULL_SUITE` explicitly.

---

### Traceability (0.93/1.00)

**Evidence:**

FR requirements are cross-referenced in virtually every module and class:
- Module docstrings cite their FR sources (FR-004, FR-014, FR-015, FR-016, FR-017, FR-018, FR-019, FR-020).
- Acceptance criteria are quoted verbatim inline at the point of implementation.
- `__init__.py` docstring labels each exported symbol with its FR source: "FR-014", "FR-016", "FR-017".
- H-07, H-10, H-11 compliance is declared in every module docstring.
- SPDX-License-Identifier header present in all 10 files.

Dependency direction is documented in layer4_stats.py lines 18-22 with explicit "allowed" and "FORBIDDEN" arrows.

The `BonferroniConfig.description` property docstring states "Satisfies FR-017 acceptance criterion" — direct one-to-one traceability.

`BaselineAuditEntry` docstring traces to "FR-020 acceptance criterion" for the CLI command.

Classification logic includes the exact contracts table reference with section number (behavioral-contracts.md Section D.4).

**Gaps:**

1. The rate-class promotion (belt-and-suspenders guard at stats.py lines 606-612) is implemented without a requirement reference. It is described as a "belt-and-suspenders guard" in a comment but does not trace to a specific FR, behavioral contract section, or design decision document.

2. `BaselineStore._MIN_FULL_SAMPLES` references "baselines/protocol.md" three times but the protocol document is not within the scored file set and cannot be validated. The traceability chain terminates at an external reference.

**Improvement Path:**
- Add a traceability comment to the rate-class promotion logic: either a reference to a specific behavioral contract clause or a note that it is an unspecified design-level guard added beyond the FR requirements.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Internal Consistency | 0.86 | 0.92 | Fix layer4_stats.py module docstring: replace "BaselineStore" and "ReportGenerator" in responsibilities list with "BaselinePersistencePort" and "ReportOutputPort" to match the iter2 port-abstraction fix. |
| 2 | Internal Consistency | 0.86 | 0.92 | Fix _MIN_FULL_SAMPLES: change `store(min_samples: int = 30)` to `store(min_samples: int = _MIN_FULL_SAMPLES)` so the class attribute is actually referenced. This resolves both the orphaned constant and the "Public API comment on underscore-prefixed attribute" issues simultaneously if the attribute is renamed to `MIN_FULL_SAMPLES`. |
| 3 | Completeness | 0.90 | 0.95 | Resolve the write_report() specification gap: either add `write_report()` as a public method delegation to `_persist_report()`, or document in the module that report persistence is handled through run() arguments (update specification to match implementation). |
| 4 | Actionability | 0.88 | 0.93 | Add usage example to compare_multiple_metrics() showing explicit `k=BONFERRONI_K_FULL_SUITE` override when only a subset of metrics is present. |
| 5 | Traceability | 0.93 | 0.96 | Add citation to rate-class promotion logic at stats.py lines 608-612: reference the specific behavioral contract section or note it as an implementation-level defense-in-depth decision. |

---

## Composite Score Arithmetic

```
composite = (completeness   × 0.20) + (internal_consistency × 0.20)
          + (meth_rigor     × 0.20) + (evidence_quality     × 0.15)
          + (actionability  × 0.15) + (traceability         × 0.10)

         = (0.90 × 0.20) + (0.86 × 0.20) + (0.90 × 0.20)
         + (0.90 × 0.15) + (0.88 × 0.15) + (0.93 × 0.10)

         = 0.180 + 0.172 + 0.180 + 0.135 + 0.132 + 0.093

         = 0.892
```

**Stream threshold:** 0.94 (C4 stream requirement)
**Standard threshold:** 0.92 (H-13)
**Result:** 0.892 — REVISE (below both thresholds)

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score — specific file locations and line numbers cited
- [x] Uncertain scores resolved downward — Internal Consistency scored 0.86 not 0.88 because three distinct issues were found, not one
- [x] First-draft calibration considered — this is iteration 3, not a first draft; calibration adjusted upward from first-draft anchor
- [x] No dimension scored above 0.95 without exceptional evidence — Traceability at 0.93 is highest; justified by near-complete FR citation coverage

**Bias check note:** The primary risk in scoring this deliverable is anchoring on the successful iter2 fix and over-crediting the overall quality. The three residual inconsistencies (stale docstring, orphaned constant, mismatched naming convention) are concrete, verifiable defects — not subjective judgments. Scores reflect these defects accurately. The composite of 0.892 is 0.048 below the C4 stream threshold of 0.94, and 0.028 below the standard H-13 threshold of 0.92.

---

## Session Context Protocol (Handoff Schema)

```yaml
verdict: REVISE
composite_score: 0.892
threshold: 0.94
weakest_dimension: Internal Consistency
weakest_score: 0.86
critical_findings_count: 0
iteration: 3
improvement_recommendations:
  - "Fix layer4_stats.py module docstring: replace concrete type references (BaselineStore, ReportGenerator) with port interface names (BaselinePersistencePort, ReportOutputPort)"
  - "Fix _MIN_FULL_SAMPLES: reference the class attribute in store() default parameter instead of inline literal 30; optionally rename to MIN_FULL_SAMPLES to resolve naming convention inconsistency"
  - "Resolve write_report() specification gap: add public method or update specification"
  - "Add multi-metric k-override usage example to compare_multiple_metrics() docstring"
  - "Add traceability citation to rate-class promotion logic"
```
