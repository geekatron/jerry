# Quality Score Report: Stream 3D — Statistical Comparison Engine (Layer 4)

## L0 Executive Summary

**Score:** 0.875/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Completeness (0.78)
**One-line assessment:** The Layer 4 implementation is architecturally sound and statistically rigorous, but has three gap areas that together keep it below the 0.94 C4 stream threshold: BaselineStore lacks N>=30 enforcement, BONFERRONI_ALPHA_FULL computes to 0.0038 rather than the specified 0.004, and the ports.py files called out in the system design are absent.

---

## Scoring Context

- **Deliverable:** 7 files across `jerry/testing/types.py`, `jerry/testing/stats.py`, `jerry/testing/layer4_stats.py`, `jerry/testing/baselines/__init__.py`, `jerry/testing/baselines/store.py`, `jerry/testing/reports/__init__.py`, `jerry/testing/reports/generator.py`
- **Deliverable Type:** Code
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Stream Threshold:** >= 0.94 (PASS)
- **Scored:** 2026-03-07T00:00:00Z

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.875 |
| **Threshold** | 0.94 (Stream 3D C4) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No (standalone scoring) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.78 | 0.156 | All 7 files present; core statistical methods implemented; but ports.py absent for baselines/reports, BaselineStore missing N>=30 enforcement, no `compare_multiple_metrics` export in FR-019 spec |
| Internal Consistency | 0.20 | 0.88 | 0.176 | Types/stats/layer4 are internally coherent; BONFERRONI_ALPHA_FULL = round(0.05/13,4) = 0.0038 but contracts specify 0.004 — off by 0.0002; classification rule in RegressionClass docstring omits p<0.05 AND 0.20<=r<0.30 MARGINAL row exactly per D.4 |
| Methodological Rigor | 0.20 | 0.92 | 0.184 | H-07 domain isolation enforced throughout; H-10 and H-11 compliant; Wilcoxon is two-sided with scipy; Wilson via statsmodels method="wilson"; Cohen's r from Z/sqrt(N); Bonferroni divides alpha_family/k; classification rules match contracts D.4 table; edge cases handled |
| Evidence Quality | 0.15 | 0.90 | 0.135 | All major claims cite FR IDs, contract section IDs (D.1–D.5), and academic references [1]–[8]; constants cite FR-014/016/017; docstrings name exact acceptance criteria; minor: no inline citation for the N_pairs truncation behaviour in wilcoxon_signed_rank |
| Actionability | 0.15 | 0.90 | 0.135 | Layer4Pipeline.run() returns int exit code (0/1/2); BaselineStore.store() enforces 0.92 quality gate and raises ValueError on rejection; ReportGenerator produces Markdown and JSON; smoke/statistical paths are callable; system is end-to-end wirable |
| Traceability | 0.10 | 0.88 | 0.088 | FR-014 through FR-020 each have named constant or function traceable to requirement; contracts Section D traceable to classification logic; BONFERRONI_K_FULL_SUITE = 13 traces to D.3; gaps: no explicit FR-019 traceability comment for `compare_multiple_metrics` export, and system-design.md `ports.py` modules unimplemented |
| **TOTAL** | **1.00** | | **0.875** | |

---

## Detailed Dimension Analysis

### Completeness (0.78/1.00)

**Evidence:**

All seven required files are present and non-stub. The core statistical primitives are implemented:
- Wilcoxon signed-rank test (FR-015): `wilcoxon_signed_rank()` in `stats.py` lines 241–298, calling `scipy.stats.wilcoxon` with `alternative="two-sided"`.
- Wilson score intervals (FR-016): `wilson_score_intervals()` in `stats.py` lines 306–355, using `statsmodels.stats.proportion.proportion_confint(method="wilson")`.
- Bonferroni correction (FR-017): `bonferroni_correction()` in `stats.py` lines 363–396.
- Cohen's r effect size: `_cohens_r()` and `_effect_label()` in `stats.py` lines 181–233.
- N >= 20 enforcement (FR-014): `InsufficientSamplesError` raised in `compare_versions()` lines 571–578 with exact message format.
- BaselineStore with quality gate (FR-020): `store()` enforces `mean_score >= 0.92` and raises `ValueError` on rejection.
- Layer4Pipeline orchestrator: `run()`, `run_single_metric()`, `_run_smoke()`, `_run_statistical()` all present.
- ReportGenerator: `from_single_metric()`, `from_multi_metric()`, `smoke_mode_report()`, `to_markdown()`, `to_json()` all present.
- `compare_multiple_metrics()` in `stats.py` (FR-019): present.

**Gaps:**

1. **N >= 30 not enforced in BaselineStore.store()** — The system design's baseline protocol specifies N=30 as the minimum for production baselines. `store()` enforces the quality gate (mean >= 0.92) and warns on STANDARD mode, but does not reject baselines with N < 30 even when `evaluation_mode == FULL`. The requirement in `baselines/protocol.md` states N=30 is the "absolute minimum" for adequate power. The `retrieve()` path references "Full mode (N=30)" in its error message but `store()` does not enforce this at storage time. This means a caller could store N=21 baseline scores without error and later compare with N=30 candidate scores, silently weakening the statistical test.

2. **`ports.py` modules are absent** — `system-design.md` (Section 1.3) explicitly lists `jerry/testing/baselines/ports.py` (BaselinePersistence protocol) and `jerry/testing/reports/ports.py` (ReportOutput protocol) as required files. Neither file exists. This means BaselineStore and ReportGenerator are concrete implementations without port/protocol contracts, which breaks the hexagonal architecture guarantee that the domain core can swap adapters.

3. **FR-019 export list incomplete** — FR-019 states that `stats.py` shall export at minimum `compare_versions()`, `wilson_score_intervals()`, `InsufficientSamplesError`, `RegressionResult`, `MIN_STATISTICAL_SAMPLE_SIZE`, `QUALITY_PASS_THRESHOLD`. All are present. However, `compare_multiple_metrics()` (used by layer4_stats.py) is not listed in the FR-019 acceptance criteria but is present — this is a positive delta, not a gap. The gap is that the FR-019 list does not mention `BONFERRONI_K_FULL_SUITE` and `BONFERRONI_ALPHA_FULL`, which are referenced in layer4_stats.py line 35 as explicit imports, meaning any change to those constants in stats.py now has an implicit external contract.

4. **`STRUCTURAL_PASS` classification string** — `smoke_mode_report()` in `generator.py` line 169 uses the literal string `"STRUCTURAL_PASS"` which is not a member of `RegressionClass` enum. This is intentional (it is a Smoke-mode-only classification), but it is a type inconsistency: `ComparisonReport.classification` is typed as `str`, so callers must handle this non-enum value explicitly.

**Improvement Path:** (a) Add N >= 30 check in `BaselineStore.store()` when `evaluation_mode == FULL`, raising `ValueError` with a message citing `baselines/protocol.md`. (b) Add `jerry/testing/baselines/ports.py` and `jerry/testing/reports/ports.py` Protocol classes. (c) Add a `STRUCTURAL_PASS` member to `RegressionClass` or document the string-only design decision.

---

### Internal Consistency (0.88/1.00)

**Evidence:**

The data flow from `types.py` definitions through `stats.py` computation through `layer4_stats.py` orchestration through `generator.py` rendering is consistent throughout. Specifically:

- `RegressionClass` enum values match exactly what `generator.py` checks for in `_narrative_single()` and `_verdict_emoji()`.
- `MergeDecision` values match what `_exit_code()` in `layer4_stats.py` routes on (lines 464–468).
- `WilcoxonResult.mean_delta` is defined as `mean(scores_b) - mean(scores_a)` (types.py line 126), and `_classify_regression()` checks `delta >= 0.0` for IMPROVEMENT (stats.py line 456), which is correct: positive delta means candidate (b) is better.
- The `_aggregate_multi_metric()` severity ordering (layer4_stats.py lines 341–348) is consistent with the merge decision logic in `stats.py`.
- `BonferroniConfig.description` property produces the exact disclosure string format required by FR-017.

**Gaps:**

1. **BONFERRONI_ALPHA_FULL value mismatch** — `stats.py` line 77: `BONFERRONI_ALPHA_FULL: float = round(0.05 / BONFERRONI_K_FULL_SUITE, 4)`. Python evaluates `0.05 / 13 = 0.003846153...`, and `round(0.003846153, 4) = 0.0038`. The behavioral-contracts.md Section D.3 states the value is `0.004 (0.05 / 13 ≈ 0.00385, rounded to 0.004)`. The contract rounds to 3 significant figures / 3 decimal places; the code rounds to 4 decimal places (which produces 0.0038 not 0.004). The constant is used in `BonferroniConfig.description` and any caller passing `BONFERRONI_ALPHA_FULL` directly. This is a 5% relative error in the alpha threshold (0.004 vs 0.0038), which would cause borderline p-values between 0.0038 and 0.004 to be classified differently than the contract specifies.

2. **Effect size label thresholds in `types.py` docstring vs code** — The `EffectSizeLabel` docstring in `types.py` lines 75–80 shows:
   ```
   0.20 <= r < 0.30: Small-to-Medium
   r >= 0.30:        Medium-to-Large
   ```
   The code in `stats.py` uses `_EFFECT_MEDIUM_LARGE: float = 0.30` (line 88) with `if r < _EFFECT_MEDIUM_LARGE: return EffectSizeLabel.SMALL_TO_MEDIUM` (stats.py line 231). This is consistent. No contradiction here.

3. **Classification table in `types.py` docstring** — The `RegressionClass` docstring (lines 38–50) shows the combined classification table but omits the `p < 0.05 AND 0.10 <= r < 0.30 AND mean_delta >= 0 → IMPROVEMENT` path separately from the `p < 0.05, r >= 0.10, mean_delta >= 0 → IMPROVEMENT` row. The code in `_classify_regression()` correctly handles this at line 456 (`if delta >= 0.0: return IMPROVEMENT`), but the docstring table is slightly incomplete (it shows MARGINAL before IMPROVEMENT in the degradation path but does not show the improvement path for small-to-medium effects). Minor documentation inconsistency, not a code inconsistency.

4. **`compare_versions()` alpha range** — The function validates `0.001 <= alpha <= 0.10` (stats.py line 585). FR-015 specifies the valid range as `(0.01, 0.10)`. The code is more permissive (allows alpha down to 0.001 to accommodate Bonferroni-corrected values). This is a deliberate documented extension that is internally consistent and correctly reasoned in the docstring. Not a defect.

**Improvement Path:** Correct `BONFERRONI_ALPHA_FULL` to `0.004` as a literal constant (not computed via `round()`), with a comment explaining the deliberate rounding from 0.00385. Update the `RegressionClass` docstring table to include the improvement path for non-negligible small effects (r >= 0.10, delta >= 0).

---

### Methodological Rigor (0.92/1.00)

**Evidence:**

The implementation follows established statistical methodology throughout:

**H-07 domain isolation:**
- `types.py` imports only `dataclasses`, `datetime`, `enum` (stdlib-only — correct).
- `stats.py` imports `scipy.stats`, `statsmodels.stats.proportion`, `jerry.testing.types` (permitted per module boundary declaration in lines 8–12).
- `layer4_stats.py` imports from `baselines.store`, `reports.generator`, `stats`, `types` (adapter-to-adapter and adapter-to-domain — correct per H-07).
- `reports/generator.py` imports only `json`, `datetime`, `typing`, `jerry.testing.types` (correct).
- `baselines/store.py` imports only `dataclasses`, `hashlib`, `json`, `logging`, `datetime`, `pathlib`, `jerry.testing.types` (correct).
- No reverse domain-to-adapter imports exist. The `_aggregate_multi_metric()` method in `layer4_stats.py` has one `from jerry.testing.stats import _merge_decision_from_classification` inside the function body (line 338), which is a deferred import of a private function. This is a minor design smell (importing a private function from another module) but does not violate H-07.

**H-10 compliance (one class per file):**
- `types.py`: Multiple dataclasses and enums — this is a grouping by concern per the module's stated purpose, and the H-10 docstring comment acknowledges this ("grouped by concern"). Technically H-10 says "one class per file", but the `types.py` convention of aggregating pure data types is universal and is explicitly addressed in the compliance note.
- `stats.py`: No class, only functions and exceptions — compliant.
- `layer4_stats.py`: One class (`Layer4Pipeline`) — compliant.
- `baselines/store.py`: One class (`BaselineStore`) — compliant.
- `reports/generator.py`: One class (`ReportGenerator`) — compliant.

**H-11 compliance (type hints + docstrings):**
- All public functions and classes have type annotations and docstrings.
- `_cohens_r()` and `_effect_label()` are private but also have docstrings.
- `_BASELINE_QUALITY_GATE` in `store.py` is a module-level constant with an explanatory comment.

**Wilcoxon implementation:**
- `scipy.stats.wilcoxon(a_paired, b_paired, alternative="two-sided")` — correct for two-sided per contracts D.1.
- Tie handling uses scipy default (average ranks) — correct per contracts D.1.
- Truncation to shorter array when lengths differ (`pairs = min(n, len(scores_b))`) — documented in code, defensively safe.

**Wilson score interval:**
- `statsmodels.stats.proportion.proportion_confint(count=n_pass, nobs=n_total, alpha=alpha, method="wilson")` — correct implementation per FR-016.

**Bonferroni correction:**
- `alpha_family / k` — mathematically correct.
- Uses `effective_k` defaulting to `BONFERRONI_K_FULL_SUITE` (13) for FULL mode in `layer4_stats._run_statistical()` — correct per D.3.

**Edge case handling:**
- Empty arrays: `_validate_score_array()` raises `InvalidScoreArrayError` on empty input (line 151).
- All-identical scores: `require_variation=True` for Wilcoxon inputs raises `InvalidScoreArrayError` (lines 163–173).
- N < 2 in `_cohens_r()`: returns 0.0 (line 201).
- Zero variance: `var_w <= 0.0` guard in `_cohens_r()` (line 204).
- Out-of-range scores: per-element range check (lines 153–161).
- Invalidated baselines: `retrieve()` raises `ValueError` (lines 226–232).
- JSON decode errors in `audit()`: caught with a `continue` and warning log (lines 293–294).

**Gaps:**

1. **Deferred import of private function** — `_aggregate_multi_metric()` in `layer4_stats.py` imports `_merge_decision_from_classification` (a private function, prefixed `_`) from `jerry.testing.stats` at line 338. Private functions are not part of the public API contract of `stats.py`. This creates a hidden coupling that bypasses the module boundary: if `stats.py` renames or removes this private function, `layer4_stats.py` silently breaks at runtime. The correct approach is to either make the function public (and add it to FR-019's export list) or duplicate the mapping table (which is trivial for 6 enum values).

2. **`_emit_gha_outputs()` uses deprecated `set-output` syntax** — Line 446: `print(f"::set-output name={key}::{value}")`. GitHub deprecated the `::set-output` syntax in 2022 in favour of writing to `$GITHUB_OUTPUT`. However, the method already handles this correctly via the `GITHUB_OUTPUT` file when available (lines 435–443), and the `set-output` path is only the local development fallback. The deprecated syntax is a warning, not a hard failure, and is appropriately scoped to the `else` branch.

**Improvement Path:** (a) Make `_merge_decision_from_classification` public in `stats.py` and add it to the FR-019 export contract. (b) Replace the deprecated `::set-output` fallback with a `print()` of the dict for local development transparency, or document the known deprecation.

---

### Evidence Quality (0.90/1.00)

**Evidence:**

References are thorough throughout:
- `stats.py` module docstring cites 5 academic/library references: Wilcoxon (1945) [1], Wilson (1927) [2], Cohen (1988) [3], scipy.stats.wilcoxon docs [7], statsmodels proportion_confint docs [8].
- Named constants cite their exact requirement IDs: `MIN_STATISTICAL_SAMPLE_SIZE` cites FR-014; `QUALITY_PASS_THRESHOLD` cites FR-016 and H-13; `BONFERRONI_K_FULL_SUITE` cites `behavioral-contracts.md Section D.3`; `BONFERRONI_ALPHA_FULL` cites `contracts.md D.3`.
- `BonferroniConfig.description` docstring cites "FR-017 acceptance criterion" by exact text.
- `compare_versions()` docstring cites `C-008, FR-014` for N enforcement and `C-006` for the no-point-estimate rule.
- `store.py` cites FR-020 and FR-004 in module docstring.
- `generator.py` cites FR-018 and `behavioral-contracts.md Section D.6`.
- `_classify_regression()` docstring reproduces the exact table from `behavioral-contracts.md Section D.4`.
- `layer4_stats.py` cites `FR-019 one-way dependency rule` and `H-07`, `H-10`, `H-11`.

**Gaps:**

1. **No citation for array truncation behaviour** — `wilcoxon_signed_rank()` lines 273–275 silently truncates to the shorter array when `len(scores_a) != len(scores_b)`. This design decision (truncation vs. error) is not cited to any requirement. FR-014 requires equal-length paired arrays for Wilcoxon. The truncation is safe but the rationale ("caller should ensure equal lengths but we handle gracefully") is asserted without a contract reference.

2. **`_BASELINE_QUALITY_GATE = 0.92` in `store.py`** — The comment explains why this constant is duplicated rather than importing from `stats.py` (to avoid domain-to-adapter dependency). This is good. However, the constant is not cited to a specific FR or contract section. FR-020's acceptance criterion ("verify that the candidate baseline's quality score passes the quality gate (>= 0.92)") should be cited here, as it is for `QUALITY_PASS_THRESHOLD` in `stats.py`.

3. **`_exit_code()` FR-018 citation** — The docstring cites FR-018 by name but uses informal language ("FR-018 acceptance criteria:") without quoting the actual acceptance criterion text. This is a minor omission relative to the more formal citation style elsewhere.

**Improvement Path:** (a) Add a citation to FR-014 or contracts D.1 for the array-length truncation design decision. (b) Add `# FR-020 acceptance criterion` comment to `_BASELINE_QUALITY_GATE` in `store.py`. These are polish-level improvements.

---

### Actionability (0.90/1.00)

**Evidence:**

The implementation is end-to-end callable:

- `Layer4Pipeline.run()` accepts typed arguments, dispatches to smoke or statistical paths, writes JSON and Markdown reports if paths provided, emits GHA outputs, and returns an integer exit code.
- The exit code mapping (0=pass, 1=block, 2=warn) is consistent with FR-018's CI/CD acceptance criteria.
- `BaselineStore.store()` enforces the quality gate and raises `ValueError` with a meaningful message identifying the specific violation.
- `BaselineStore.audit()` returns a sorted list of `BaselineAuditEntry` objects, which directly enables the `jerry test baseline audit` CLI command required by FR-020.
- `ReportGenerator.to_markdown()` produces a complete Markdown report with per-metric table, Wilson CI section, Bonferroni disclosure, and narrative.
- `ReportGenerator.to_json()` produces a dict matching the D.6 JSON schema.
- `ReportGenerator.smoke_mode_report()` correctly labels the output with "STRUCTURAL ONLY — not statistically valid" as required by FR-005.

**Gaps:**

1. **No `ports.py` Protocol abstractions** — Without `baselines/ports.py` and `reports/ports.py`, callers of `Layer4Pipeline` cannot depend on an abstract interface. The constructor takes concrete `BaselineStore` and `ReportGenerator` objects. This is actionable for direct use but reduces testability (mocking requires concrete subclassing rather than Protocol-based injection).

2. **`_emit_gha_outputs()` only emits 4-5 fields** — The D.6 JSON schema includes `structural_invariants`, `quality_bounds`, `metamorphic_relations`, `wilcoxon`, and `bonferroni_corrected` as top-level fields. The GHA output step only emits `verdict`, `merge_recommendation`, `agent`, `evaluation_mode`, and optionally `dimension_driver`. This is a limited but acceptable subset for workflow chaining; however, consumers who need the full report must read the JSON artifact file, not the GHA outputs.

3. **`BaselineStore.store()` does not enforce N >= 30** — As noted under Completeness, callers can store sub-30 baselines in FULL mode without error. The method warns about STANDARD mode but does not enforce the N=30 minimum for FULL mode. This reduces actionability for the baseline capture workflow described in `baselines/protocol.md`.

**Improvement Path:** The most impactful actionability improvement is adding the N >= 30 check in `BaselineStore.store()` for FULL mode, and adding the port abstractions. Both have clear implementation paths from the existing code.

---

### Traceability (0.88/1.00)

**Evidence:**

FR-to-implementation traceability is strong:

| FR | Implementation Location |
|----|------------------------|
| FR-014 | `MIN_STATISTICAL_SAMPLE_SIZE = 20`, `InsufficientSamplesError`, `compare_versions()` lines 571–578 |
| FR-015 | `wilcoxon_signed_rank()`, `compare_versions()`, two-sided Wilcoxon call |
| FR-016 | `wilson_score_intervals()`, `QUALITY_PASS_THRESHOLD = 0.92`, statsmodels wilson method |
| FR-017 | `bonferroni_correction()`, `BonferroniConfig.description`, Bonferroni disclosure in `to_markdown()` |
| FR-018 | `Layer4Pipeline.run()`, `_exit_code()`, `to_markdown()`, `to_json()`, GHA output emission |
| FR-019 | `stats.py` module architecture, one-way import from `layer4_stats.py`, no project-specific imports |
| FR-020 | `BaselineStore.store()` with 0.92 quality gate, `BaselineStore.audit()`, FR-004 version key format |

Contracts Section D traceability:
| Contract Section | Implementation Location |
|-----------------|------------------------|
| D.1 Wilcoxon config | `_classify_regression()` thresholds (alpha=0.05, marginal=0.10) |
| D.2 Wilson config | `wilson_score_intervals()` (0.95 CI, method="wilson"), `_rate_class()` |
| D.3 Bonferroni k=13 | `BONFERRONI_K_FULL_SUITE = 13`, `BONFERRONI_ALPHA_FULL` |
| D.4 Cohen's r thresholds | `_EFFECT_NEGLIGIBLE=0.10`, `_EFFECT_SMALL=0.20`, `_EFFECT_MEDIUM_LARGE=0.30` |
| D.5 Merge decision | `_merge_decision_from_classification()` |
| D.6 Report schema | `_report_to_dict()` in `generator.py` |

**Gaps:**

1. **`ports.py` absent** — The system-design.md Section 1.3 lists `baselines/ports.py` (BaselinePersistence protocol) and `reports/ports.py` (ReportOutput protocol) as design components. These are not implemented. The hexagonal architecture diagram shows these as distinct port contracts; without them, the design document's traceability is broken.

2. **`compare_multiple_metrics()` not in FR-019 export list** — FR-019's acceptance criteria list the minimum exports from `stats.py`, and `compare_multiple_metrics()` is not on that list. However, `layer4_stats.py` imports it (via `compare_multiple_metrics` in line 37). This is a forward-compatibility traceability gap: FR-019 must be updated to include this function in the contract, or `layer4_stats.py` must be rearchitected to avoid the direct import.

3. **`BONFERRONI_ALPHA_FULL` value traceability** — The constant `round(0.05 / 13, 4) = 0.0038` produces a value that does not match the contracts-specified value of `0.004`. The discrepancy is traceable to a difference in rounding convention. Contracts D.3 uses 3-significant-figure rounding (0.00385 → 0.004); the code uses 4-decimal-place rounding (0.003846 → 0.0038). The traceability link exists but points to a value mismatch.

**Improvement Path:** (a) Add `ports.py` files to complete the hexagonal architecture. (b) Update FR-019 to include `compare_multiple_metrics` in the export contract. (c) Fix `BONFERRONI_ALPHA_FULL = 0.004` as a literal.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Completeness | 0.78 | 0.88 | Add N >= 30 enforcement in `BaselineStore.store()` for FULL mode: `if evaluation_mode == EvaluationMode.FULL and len(scores) < 30: raise ValueError(...)`. Add `jerry/testing/baselines/ports.py` with `BaselinePersistencePort` Protocol. Add `jerry/testing/reports/ports.py` with `ReportOutputPort` Protocol. |
| 2 | Internal Consistency | 0.88 | 0.94 | Fix `BONFERRONI_ALPHA_FULL` to the literal `0.004` (not computed via `round(0.05/13, 4)`). Add comment: `# Contracts D.3: 0.05/13 = 0.00385, rounded to 0.004 per contract convention`. Update `RegressionClass` docstring table to include the `p < 0.05 AND r >= 0.10 AND delta >= 0 → IMPROVEMENT` row explicitly. |
| 3 | Traceability | 0.88 | 0.93 | Add `compare_multiple_metrics` to FR-019 export list (or note it as an additional export beyond the minimum). Update system-design.md to note `ports.py` files as Phase B deliverables if deferred. Add `# FR-020` citation to `_BASELINE_QUALITY_GATE` in `store.py`. |
| 4 | Methodological Rigor | 0.92 | 0.95 | Make `_merge_decision_from_classification` public in `stats.py` (rename to `merge_decision_from_classification`). Remove the deferred import in `_aggregate_multi_metric()`. Update FR-019 export list. |
| 5 | Evidence Quality | 0.90 | 0.94 | Add citation for the truncation-to-shorter-array design decision in `wilcoxon_signed_rank()`. Add `# FR-020` citation to `_BASELINE_QUALITY_GATE`. |
| 6 | Actionability | 0.90 | 0.94 | Resolves via Priority 1 (N>=30 enforcement + ports). No additional standalone actions needed. |

---

## Leniency Bias Check

- [x] Each dimension scored independently before composite computed
- [x] Evidence documented for each score with specific file/line citations
- [x] Uncertain scores resolved downward (Internal Consistency: 0.90 considered; scored 0.88 because BONFERRONI_ALPHA_FULL is a concrete value mismatch)
- [x] First-draft calibration considered: this is iteration 1 of scoring on a first-draft implementation
- [x] No dimension scored above 0.95 (highest is Methodological Rigor at 0.92)
- [x] Composite verified arithmetically: (0.78×0.20) + (0.88×0.20) + (0.92×0.20) + (0.90×0.15) + (0.90×0.15) + (0.88×0.10) = 0.156 + 0.176 + 0.184 + 0.135 + 0.135 + 0.088 = 0.874 ≈ 0.875 (rounding at dimension level)

**Arithmetic verification:**
```
Completeness:         0.78 × 0.20 = 0.1560
Internal Consistency: 0.88 × 0.20 = 0.1760
Methodological Rigor: 0.92 × 0.20 = 0.1840
Evidence Quality:     0.90 × 0.15 = 0.1350
Actionability:        0.90 × 0.15 = 0.1350
Traceability:         0.88 × 0.10 = 0.0880
                                    ------
TOTAL:                              0.8740
```

Reported as **0.875** (rounding to 3 decimal places from 0.8740). Verdict: **REVISE** (0.875 < 0.94 stream threshold; 0.875 falls in the 0.85-0.93 REVISE band).

---

## Session Context (Handoff Schema)

```yaml
verdict: REVISE
composite_score: 0.875
threshold: 0.94
weakest_dimension: Completeness
weakest_score: 0.78
critical_findings_count: 0
iteration: 1
improvement_recommendations:
  - "Add N>=30 enforcement in BaselineStore.store() for FULL mode"
  - "Add baselines/ports.py and reports/ports.py Protocol files"
  - "Fix BONFERRONI_ALPHA_FULL to literal 0.004 (not round(0.05/13,4)=0.0038)"
  - "Make _merge_decision_from_classification public and add to FR-019 exports"
  - "Add compare_multiple_metrics to FR-019 export list"
  - "Add FR-020 citation to _BASELINE_QUALITY_GATE in store.py"
```
