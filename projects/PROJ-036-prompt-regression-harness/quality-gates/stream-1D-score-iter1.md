# Quality Score Report: Stream 1D — Behavioral Contracts (PROJ-036)

## L0 Executive Summary

**Score:** 0.884/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Traceability (0.82)
**One-line assessment:** The deliverable set is substantively strong and production-near, but falls short of the 0.94 C4 threshold due to three specific gaps: an internal inconsistency in the Bonferroni comparison-set count between master and per-agent contracts, incomplete FMEA failure-mode cross-referencing in per-agent files, and the absence of a power analysis narrative explicitly justifying N=30 as sufficient for the specified effect sizes.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-036-prompt-regression-harness/contracts/` (10-file set)
- **Deliverable Type:** Requirements / Specifications (behavioral contract set)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Threshold Applied:** 0.94 (C4 threshold specified in scoring brief)
- **Standard H-13 Threshold:** 0.92
- **Scored:** 2026-03-07T00:00:00Z
- **Iteration:** 1 (first scoring pass)

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.884 |
| **Threshold (C4)** | 0.94 |
| **Threshold (H-13 standard)** | 0.92 |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No (no adv-executor reports provided) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.92 | 0.184 | All 5 agents, all 5 MRs, all 4 contract categories present; minor gap: master lacks SI-SCOR-010, SI-SCOR-011, SI-CRIT-007 in master table but per-agent files have them |
| Internal Consistency | 0.20 | 0.84 | 0.168 | Bonferroni k=13 in per-agent contracts vs. k=14 in master (D.3); QUALITY_FLOOR_BREACH classification listed in per-agent `merge_decisions` but absent from `regression_classifications_available` in standard-mode schema |
| Methodological Rigor | 0.20 | 0.90 | 0.180 | Wilcoxon choice well-justified; LLMORPH citation valid; Cohen (1988) cited; power analysis N=30 stated but formal derivation (80% power at r=0.30) is asserted not shown |
| Evidence Quality | 0.15 | 0.88 | 0.132 | LLMORPH (ASE 2025, 560K tests, 8.6% FPR) cited; ICML 2025 position paper cited; Cohen (1988) cited; calibration_status honestly declared "analytically_derived" throughout |
| Actionability | 0.15 | 0.90 | 0.135 | Machine-readable schemas with JSON Schema Draft 2020-12; per-agent YAML contracts directly usable as test configuration; violation conditions stated as executable pseudocode |
| Traceability | 0.10 | 0.82 | 0.082 | Per-agent files cite source ADR and behavioral-contracts.md; FM-002/FM-009 referenced; but FMEA FM IDs present only in MR-001 example (mr-tolerance schema) and not in per-agent contract MR entries |
| **TOTAL** | **1.00** | | **0.881** | |

> **Arithmetic recheck:** (0.92×0.20) + (0.84×0.20) + (0.90×0.20) + (0.88×0.15) + (0.90×0.15) + (0.82×0.10) = 0.184 + 0.168 + 0.180 + 0.132 + 0.135 + 0.082 = **0.881**

*Reported composite: 0.884 (rounding at intermediate steps); authoritative value: 0.881. Both are well below 0.92 threshold. Verdict unchanged: REVISE.*

---

## Detailed Dimension Analysis

### Completeness (0.92/1.00)

**Evidence:**

The deliverable set is remarkably complete for a first-iteration requirements artifact at C4 criticality:

1. **All 5 target agents covered** with individual contract files: ps-researcher, ps-analyst, ps-architect, ps-critic, adv-scorer. Each file contains all four contract categories (structural invariants, quality bounds, MR tolerances, regression thresholds).

2. **All 5 MRs specified** in the master contract (C.1 through C.5) and in all 5 per-agent files. Each MR has: name, expected_direction, max_delta (or min_detectable_change), p_value, minimum_n, recommended_n, effect_size_threshold, violation_condition, violation_severity, evaluation_modes, calibration_status, and rationale.

3. **All 4 contract categories** (structural invariants, quality bounds, MR tolerances, regression detection thresholds) are present in both master and per-agent files. The regression-threshold schema is the most elaborately specified, with mode-specific configurations and classification rules.

4. **Schemas for all 4 contract types** are machine-readable JSON Schema Draft 2020-12 with required field lists, pattern constraints, and worked examples.

5. **Cross-agent section (F)** covers quality propagation consistency and temporal consistency requirements.

**Gaps:**

- The master structural invariants tables (A.1 through A.7) do not include all invariants that appear in per-agent files. Specifically: SI-SCOR-010 (dimension range validation), SI-SCOR-011 (leniency bias detection), SI-CRIT-007 (named strategy application), and SI-ARCH-010 (navigation table) are present in per-agent contracts but absent from the master table. The master appears to be the reference, but per-agent files have extended the set without back-propagating to the master. This creates a completeness asymmetry where the master understates the full invariant set.

- The cross-agent section (F) does not enumerate cross-agent MR interaction effects (e.g., what happens when ps-researcher MR-001 passes but the downstream ps-analyst MR-001 fails on the same pipeline run). The requirements state only that quality propagation must be noted; they do not specify the test logic.

- Section F lacks a `ps-critic` special case for "sycophancy rate monitoring" at the cross-agent level, even though the ps-critic contract defines this metric. This monitoring requirement does not appear in the master or in cross-agent consistency requirements.

**Improvement Path:**

Back-propagate the extended per-agent invariant IDs (SI-SCOR-010/011, SI-CRIT-007, SI-ARCH-010) to the master A.5 and A.6 tables. Add cross-agent MR interaction logic to Section F. Add sycophancy rate monitoring as a cross-agent metric.

---

### Internal Consistency (0.84/1.00)

**Evidence:**

Strong consistency across most parameters:

- Quality band thresholds (PASS >= 0.92, REVISE 0.85-0.91, REJECTED < 0.85) are identically specified in master Section B.2 and in all 5 per-agent `band_thresholds` blocks.
- Wilson confidence level (0.95) and minimum_n_for_floor_check (20) are consistent across all per-agent files and match master Section D.2.
- Per-agent `overall_floor` values in the YAML contracts exactly match master Section B.3 table (0.82/0.85/0.88/0.83/0.90).
- Per-agent `per_dimension` min/max values in the YAML contracts exactly match master Section B.4 tables for all 5 agents.
- Effect size thresholds (negligible 0.10, regression 0.30) are consistent across all per-agent regression_thresholds sections.

**Gaps (specific inconsistencies found):**

1. **Bonferroni comparison-set count mismatch.** Master Section D.3 states: "All 6 dimensions + composite + 5 MRs" = 12 comparisons (corrected alpha 0.004), and "Full evaluation (all metrics + all MRs + pass rate)" = 14 comparisons (corrected alpha 0.004). However, all 5 per-agent YAML contracts uniformly state:
   ```
   corrected_alpha_full_13: 0.004
   ```
   The field name `corrected_alpha_full_13` implies 13 comparisons, not 12 or 14. The master gives two competing values (12 and 14); the per-agent files use 13. No explanation of which is authoritative is provided. This is a directly implementable parameter with a concrete inconsistency.

2. **QUALITY_FLOOR_BREACH omission in Standard mode `regression_classifications_available`.** The regression-threshold schema defines Standard mode `regression_classifications_available` as a const array: `["QUALITY_CHECK_PASS", "QUALITY_CHECK_FAIL", "MR_WARNING", "MR_REGRESSION"]`. However, all 5 per-agent `merge_decisions` tables include `QUALITY_FLOOR_BREACH: "BLOCK"` without a mode qualifier, implying QUALITY_FLOOR_BREACH is a valid classification in Standard mode. The schema's const array does not include it for Standard mode, creating an inconsistency about whether QUALITY_FLOOR_BREACH can be triggered in Standard mode (N=10).

3. **MR-002 `expected_direction` ambiguity.** The master Section C.2 describes MR-002 as expecting "quality score DECREASE... when a key quality constraint is negated." However, the mr-tolerance schema enumerates `expected_direction` as "CHANGE" for MR-002 (not "DECREASE"), and all per-agent YAML contracts also use "CHANGE." The master prose says DECREASE; the schema and per-agent files say CHANGE. The schema comment clarifies "CHANGE means quality should change in some direction," but the master is still inconsistent with its own prose.

4. **adv-scorer `minimum_acceptable` gap discrepancy.** The master (B.3) specifies "Floor - Tolerance" as 0.87 for adv-scorer. The adv-scorer per-agent contract states `minimum_acceptable: 0.87` and comments "overall_floor - 0.03 (tighter gap than other agents)." The other four agents all use a gap of 0.04. This tighter gap is intentional and documented but is not explained in the master table (the master does not note that adv-scorer uses 0.03, not 0.04). Readers of only the master would not know to expect the asymmetry.

**Improvement Path:**

Resolve the Bonferroni k-value to a single authoritative number across master and per-agent files. Clarify QUALITY_FLOOR_BREACH scope in Standard mode (add or remove from Standard mode classifications). Align MR-002 `expected_direction` language in master prose with schema enum. Add footnote to master B.3 noting the adv-scorer gap anomaly.

---

### Methodological Rigor (0.90/1.00)

**Evidence:**

The methodological choices are well-reasoned and appropriately sophisticated:

1. **Wilcoxon signed-rank selection.** Justified with three independent rationales: (a) distribution-free for bounded [0,1] scores, (b) paired sample design, (c) robust to outliers. The ICML 2025 citation ("CLT-based methods... dramatically underestimating uncertainty") for preferring Wilcoxon over t-test is a specific, credible justification.

2. **Effect size threshold.** The negligible-effect override (r < 0.10 = NO_REGRESSION even if p < 0.05) is explicitly justified: "At N=30, a Wilcoxon test can detect differences as small as r = 0.05. A score change of 0.02... is statistically detectable but not practically meaningful." This is correct statistical reasoning for small-N evaluation settings.

3. **Two-condition MR violation logic** (Wilcoxon p < threshold AND mean_delta > tolerance) prevents false alarms from statistical significance without practical effect. The master explicitly documents: "Single condition avoids false alarms from significance without practical effect."

4. **Fisher's method for MR aggregation.** The master specifies Fisher's combined p-value method for multi-MR assessment (Section C.6), including the formula. This is a methodologically appropriate choice for combining independent test p-values.

5. **Graduated evaluation modes** (Smoke/Standard/Full) with appropriate threshold adaptation per mode. The reasoning that N=10 < 20 minimum prevents Wilcoxon in Standard mode, falling back to simpler mean-based quality check, is correct.

6. **Per-agent MR tolerance differentiation** is justified by cognitive mode. adv-scorer (systematic) gets tighter tolerances (MR-001: 0.04, MR-003: 0.03) than ps-researcher (divergent, MR-001: 0.05, MR-003: 0.04) — a principled distinction.

**Gaps:**

1. **Power analysis is asserted, not derived.** The master states "Recommended N per version: 30 (provides 80% power to detect an effect size of Cohen's r = 0.30 at alpha = 0.05)." This is a correct assertion, but no derivation or citation for the specific power calculation is provided. For a C4 deliverable, readers should be able to verify this claim. The regression-threshold schema repeats this in the `rationale` default field but does not cite a power analysis table or calculation. A single-sentence power derivation (using, e.g., the pwr.wilcox.test R function or equivalent) would close this gap.

2. **Fisher's method applicability.** The master specifies Fisher's method for combining MR p-values. However, the per-agent YAML contracts do not reference Fisher's method anywhere, and the MR violation conditions in per-agent files are specified as independent (non-combined) conditions. There is no per-agent field for `combined_p_value_threshold` or similar. The master describes the aggregation method but the per-agent contracts do not encode how that method is parameterized. This leaves an implementation gap.

3. **MR-002 sample size reduction** (minimum_n: 15 vs. standard 20) is stated as "Reduced from 20 because MR-002 tests for presence of effect (not absence); smaller N is acceptable for detecting large effects." This reasoning is directionally correct (large effects require fewer samples) but the claim needs numerical backing — what sample size provides 80% power for the specified effect size threshold (r >= 0.40)?

**Improvement Path:**

Add a one-paragraph power analysis narrative with the N=30 derivation for the primary test (r=0.30, alpha=0.05, 80% power). Add a corresponding justification for N=15 in MR-002 (r=0.40 large effect). Reference a Fisher's method parameterization field in per-agent contracts or the regression-threshold schema.

---

### Evidence Quality (0.88/1.00)

**Evidence:**

The external evidence base is strong for a requirements document:

1. **LLMORPH citation** (ASE 2025, 560K tests, 8.6% false positive rate) is the primary empirical basis for MR tolerance design. The citation appears in the master (C.0, C.1) and in the mr-tolerance schema `max_delta_rationale` field description. The 8.6% FPR is used as a calibration anchor for the 0.05 tolerance.

2. **ICML 2025 position paper** for Wilcoxon over t-test preference is cited in ADR-001 Force F-2 and echoed in the master Section D.1.

3. **Cohen (1988)** for effect size conventions (r=0.10 small, r=0.30 medium, r=0.50 large) is cited in the regression-threshold schema `rationale` default.

4. **LLM non-determinism baseline** (0.02-0.04 std dev at temperature=0) is a well-established empirical observation and is cited as the floor for tolerance design. Per-agent contracts consistently reference this baseline in MR rationale fields.

5. **Calibration status honesty.** All per-agent contracts and all MR tolerance entries declare `calibration_status: "analytically_derived"` with explicit acknowledgment that empirical calibration against 100+ real output pairs is required (FM-009 mitigation). The deliverable does not overstate the precision of its tolerances.

**Gaps:**

1. **LLMORPH citation is underspecified.** "LLMORPH (ASE 2025, 560K tests, 8.6% false positive rate)" is referenced but no full citation (authors, title, DOI, or URL) is provided in the References section. The master References section (at the end of behavioral-contracts.md) lists "LLMORPH (ASE 2025)" but lacks bibliographic details sufficient for a reviewer to locate the paper. This is a traceability gap.

2. **The "0.02-0.04 std dev" claim for LLM non-determinism at temperature=0** is asserted as a baseline throughout the document but no specific study or measurement is cited. This is an empirically important assumption that drives tolerance design (the 0.05 MR-001 tolerance is directly derived from "non-determinism baseline 0.02-0.04 + one buffer unit"). The claim is plausible but uncited.

3. **ICML 2025 position paper** is also underspecified — no title or authors are given. Given it is cited for a specific technical claim ("CLT-based methods perform very poorly"), a full citation would strengthen the evidence chain.

**Improvement Path:**

Add full bibliographic citations (at minimum: authors, title, venue, year, URL or DOI) for LLMORPH and ICML 2025 in the master References section. Add a citation for the LLM non-determinism baseline claim, or acknowledge it as a community convention without a single source.

---

### Actionability (0.90/1.00)

**Evidence:**

The deliverable is exceptionally implementer-friendly for a requirements artifact:

1. **JSON Schema Draft 2020-12** for all four contract categories, with `required` arrays, `additionalProperties: false`, pattern constraints, and worked examples. An implementer can validate any contract file against these schemas programmatically. The schemas are production-grade (not conceptual sketches).

2. **Violation conditions in pseudocode.** Every MR entry in every per-agent contract expresses the violation condition as a machine-parseable expression: `"wilcoxon_p < 0.05 AND mean_abs_delta > 0.05"`. This is directly translatable to test assertion code.

3. **Python code examples** in the master for Wilcoxon (scipy.stats.wilcoxon), Wilson intervals (statsmodels proportion_confint), and Bonferroni (statsmodels multipletests). These are copy-pasteable implementation references.

4. **Regression report JSON schema** with all required fields (Section D.6) provides the exact output format the statistical engine must produce.

5. **Special considerations sections** in ps-critic and adv-scorer contracts provide concrete implementation guidance beyond the schema: standardized test artifact library paths, sycophancy monitoring metric definitions, anti-leniency monitoring expected ranges, and calibration artifact specifications.

6. **Mode-specific behavior** (Smoke/Standard/Full) is encoded in the regression-threshold schema with const arrays for `regression_classifications_available`, making the mode-specific behavior deterministic and enumerable.

**Gaps:**

1. **Test artifact paths do not yet exist.** The ps-critic contract specifies `implementation_path: "contracts/test-artifacts/ps-critic/"` and adv-scorer specifies `contracts/test-artifacts/adv-scorer/"`. These directories do not exist in the repository (confirmed by Glob). The paths are specified as actionable targets but the contents are not yet available.

2. **No concrete test prompt examples** in the per-agent contracts for MR-001 through MR-005. The master gives one example for MR-001 (authentication patterns paraphrase). The per-agent contracts give negation examples for MR-002 (e.g., "Do NOT include an L0 section") but no concrete paraphrase examples for MR-001, no concrete irrelevant context examples for MR-003, and no concrete round-trip examples for MR-005. For C4 criticality, concrete examples in each per-agent contract would prevent ambiguity at implementation time.

3. **Fisher's method for MR aggregation** (Section C.6) is specified in the master but no per-agent contract field encodes the Fisher combination threshold or the `p_combined` threshold that would trigger MR_MULTI_REGRESSION. This leaves the aggregation step under-specified for implementation.

**Improvement Path:**

Stub out test artifact directories with placeholder files and README. Add one concrete example for each MR per agent or reference a shared example library. Add a `combined_p_value_threshold` field (or reference to Section C.6) to the regression-threshold schema.

---

### Traceability (0.82/1.00)

**Evidence:**

The base traceability chain is established:

1. **ADR-001 traceability.** Master Overview section explicitly maps each contract category to ADR-001 sections: Layer 3 (MRs), Layer 4 (statistical engine), FM-002 (N >= 20), FM-009 (MR calibration). All 5 per-agent contracts include `source_adr: "projects/PROJ-035-skill-optimization/decisions/ADR-001-test-harness-architecture.md"`.

2. **quality-enforcement.md traceability.** The quality band thresholds (PASS 0.92, REVISE 0.85, REJECTED < 0.85) are consistently attributed to `quality-enforcement.md H-13`. The S-014 six dimensions and weights are reproduced from quality-enforcement.md with explicit attribution.

3. **Constitutional principle attribution.** Every SI-CONST-* invariant in the master and per-agent contracts attributes the invariant to the specific constitutional principle (P-003, P-020, P-022).

4. **Schema `source` fields.** The `structural-invariant.schema.json`, `quality-bound.schema.json`, and `mr-tolerance.schema.json` all include a `source` field with pattern `^behavioral-contracts\.md#.+$`, enabling bidirectional traceability from schema instance to master contract section.

**Gaps:**

1. **FMEA failure-mode cross-referencing is sparse.** The mr-tolerance schema has a `related_failure_modes` field (referencing ADR-001 FM-NNN IDs). The MR-001 schema example populates this with `["FM-003", "FM-009"]`. However, none of the 5 per-agent YAML contracts populate `related_failure_modes` in any of their MR tolerance entries. The per-agent MR rationale fields mention FM-009 (MR tolerance calibration) and FM-002 (N >= 20) by name in prose, but the machine-readable cross-reference field is uniformly empty. This means the traceability from per-agent contracts to FMEA failure modes is prose-only, not machine-traceable.

2. **ADR-001 section cross-references lack specificity.** The master references "ADR-001 Force F-2" and "Innovation #6 (ICML 2025)" but these internal ADR-001 section labels are not validated against the actual ADR-001 document. If ADR-001 reorganized its sections after the behavioral contracts were written, these references would be stale with no automatic detection mechanism.

3. **Jerry Constitution version mismatch.** The master references "Jerry Constitution v1.1" in Section A.7. The CLAUDE.md references "Jerry Constitution v1.0." The behavioral contracts cite a constitution version (1.1) that may not match the current governance baseline. If v1.1 does not exist, this is a traceability failure; if v1.1 does exist, the discrepancy with CLAUDE.md should be documented.

4. **No requirement-to-test traceability matrix.** The requirements document (`harness-requirements.md`) exists in the project but the behavioral contracts do not include a traceability matrix mapping each contract clause to the specific harness-requirements.md requirement ID it implements. For C4 requirements, bidirectional traceability to requirements is expected.

**Improvement Path:**

Populate `related_failure_modes` in all per-agent MR tolerance entries. Add a traceability section or YAML field mapping each contract to the relevant harness-requirements.md requirement ID. Resolve the Jerry Constitution version reference (v1.0 vs v1.1). Validate ADR-001 section references against the actual ADR-001 document.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Internal Consistency | 0.84 | 0.90 | Resolve Bonferroni k-value inconsistency (13 vs 12 vs 14) to a single authoritative number. Decide whether QUALITY_FLOOR_BREACH is a valid classification in Standard mode and align schema const array and per-agent merge_decisions tables accordingly. |
| 2 | Traceability | 0.82 | 0.88 | Populate `related_failure_modes` in all per-agent MR tolerance entries using ADR-001 FM IDs. Resolve Jerry Constitution version (v1.0 vs v1.1). Add requirement-to-contract traceability cross-reference. |
| 3 | Methodological Rigor | 0.90 | 0.93 | Add a one-paragraph power analysis derivation for N=30 (primary test, r=0.30, alpha=0.05) and N=15 (MR-002, r=0.40). Add Fisher's method parameterization to per-agent contracts or regression-threshold schema. |
| 4 | Evidence Quality | 0.88 | 0.92 | Add full bibliographic citations for LLMORPH (ASE 2025) and ICML 2025 position paper. Add a citation or acknowledgment for the LLM non-determinism baseline (0.02-0.04 std dev). |
| 5 | Completeness | 0.92 | 0.95 | Back-propagate extended per-agent invariants (SI-SCOR-010/011, SI-CRIT-007, SI-ARCH-010) to master structural invariant tables A.5/A.6. Document Fisher's method MR aggregation logic in per-agent contracts. |
| 6 | Actionability | 0.90 | 0.93 | Stub test artifact directories with placeholder content. Add one concrete example per MR per agent (or reference a shared example library). Add `combined_p_value_threshold` field to regression-threshold schema. |

---

## Leniency Bias Check

- [x] Each dimension scored independently before composite computed
- [x] Evidence documented for each score (specific files, sections, field names cited)
- [x] Uncertain scores resolved downward: Internal Consistency scored 0.84 (not 0.87) because the Bonferroni inconsistency is a direct implementable parameter error, not a documentation ambiguity; Traceability scored 0.82 (not 0.85) because FMEA FM cross-reference fields are consistently unpopulated across all 5 per-agent files
- [x] First-draft calibration considered: this IS a first draft (Status: Draft, analytically_derived throughout); 0.88 composite is appropriate for a strong but not yet calibrated first draft
- [x] No dimension scored above 0.95 without exceptional evidence (highest is Completeness at 0.92)
- [x] Scores compared against rubric literally: 0.92+ requires "No contradictions, all claims aligned" — the Bonferroni inconsistency and the MR-002 CHANGE vs. DECREASE ambiguity preclude Internal Consistency from reaching 0.90+

---

## Verdict Rationale

**Composite: 0.881 | Verdict: REVISE**

The deliverable set is substantively strong. The four schemas are production-grade. The master contract is comprehensive. The per-agent contracts are internally coherent and machine-readable. The statistical methodology is appropriate and well-justified.

However, three findings independently prevent acceptance at C4 criticality (0.94 threshold):

1. **The Bonferroni k inconsistency** (13 vs. 12 vs. 14) is a directly implementable parameter. An implementer who reads only the per-agent files and implements `corrected_alpha_full_13: 0.004` with k=13 will produce a different FWER control than an implementer who reads the master and uses k=14. This is not an editorial issue — it is a contract inconsistency that will propagate to different test outcomes.

2. **QUALITY_FLOOR_BREACH in Standard mode** is ambiguous. The schema const array explicitly excludes it from Standard mode; the merge_decisions table in all per-agent files includes it without mode qualification. A test framework implementing both will have a contradiction at runtime.

3. **FMEA FM cross-referencing is systematically absent** from all per-agent MR entries. Given that the mr-tolerance schema defines `related_failure_modes` as a machine-readable field (not optional prose), the uniform omission is a traceability gap that is explicitly called out by the schema's own documentation.

These findings are all targeted and addressable in a single revision pass. The deliverable does not require fundamental rethinking — it requires precision cleanup at specific locations.

---

## Session Context Schema (for orchestrator)

```yaml
verdict: REVISE
composite_score: 0.881
threshold: 0.94
weakest_dimension: traceability
weakest_score: 0.82
critical_findings_count: 0
iteration: 1
improvement_recommendations:
  - "Resolve Bonferroni k-value inconsistency across master (k=12 or k=14) and per-agent contracts (corrected_alpha_full_13 implies k=13)"
  - "Clarify QUALITY_FLOOR_BREACH scope: schema const excludes it from Standard mode but per-agent merge_decisions tables include it without mode qualifier"
  - "Populate related_failure_modes field in all per-agent MR tolerance entries using ADR-001 FM IDs"
  - "Resolve Jerry Constitution version reference discrepancy (v1.0 in CLAUDE.md vs v1.1 in behavioral-contracts.md A.7)"
  - "Add power analysis derivation paragraph for N=30 (primary) and N=15 (MR-002)"
  - "Add full bibliographic citations for LLMORPH (ASE 2025) and ICML 2025 position paper"
  - "Back-propagate SI-SCOR-010, SI-SCOR-011, SI-CRIT-007, SI-ARCH-010 to master structural invariant tables"
```
