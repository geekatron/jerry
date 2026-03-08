# Quality Score Report: Stream 1D — Behavioral Contracts (PROJ-036)

## L0 Executive Summary

**Score:** 0.921/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Traceability (0.86)
**One-line assessment:** All three iter1 blocking findings are resolved cleanly and the deliverable has crossed the H-13 standard threshold (0.92), but sits 0.019 below the C4-specific threshold (0.94) due to three residual gaps: a missing power analysis derivation for N=30, the Jerry Constitution version discrepancy (v1.1 in master vs. v1.0 in CLAUDE.md), and a missing requirement-to-contract traceability matrix.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-036-prompt-regression-harness/contracts/` (10-file set)
- **Deliverable Type:** Requirements / Specifications (behavioral contract set)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Threshold Applied:** 0.94 (C4 threshold specified in scoring brief)
- **Standard H-13 Threshold:** 0.92
- **Scored:** 2026-03-07T12:00:00Z
- **Iteration:** 2 (independent scoring of revised deliverable)
- **Prior Score:** 0.881 (iter1) — read for context only; not used as anchor; scored independently
- **Creator Self-Assessment:** 0.947 — NOT adopted; scored independently per adv-scorer role

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.921 |
| **Threshold (C4)** | 0.94 |
| **Threshold (H-13 standard)** | 0.92 |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No (no adv-executor reports provided) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.93 | 0.186 | All 5 agents, 5 MRs, 4 categories present; SI-SCOR-010/011, SI-CRIT-007 back-propagated to master per creator's claim but SI-ARCH-010 still listed as WARNING-only and absent from master A.4 table body |
| Internal Consistency | 0.20 | 0.95 | 0.190 | Bonferroni k=13 now authoritative and consistent across all 10 files; QUALITY_FLOOR_BREACH correctly scoped to Full mode in schema, master prose, and all per-agent merge_decisions |
| Methodological Rigor | 0.20 | 0.92 | 0.184 | Wilcoxon, effect size, Fisher's method all well-justified; N=30 power claim stated but derivation still asserted not shown; Fisher's method not encoded in per-agent contracts |
| Evidence Quality | 0.15 | 0.90 | 0.135 | LLMORPH, ICML 2025, Cohen (1988) cited; full bibliographic citations (authors, DOI) still absent; LLM non-determinism baseline uncited |
| Actionability | 0.15 | 0.93 | 0.140 | Machine-readable schemas, pseudocode violation conditions, Python code examples; test artifact directories unspecified |
| Traceability | 0.10 | 0.86 | 0.086 | All 25 related_failure_modes now populated; Jerry Constitution v1.1 reference unresolved vs. v1.0 in CLAUDE.md; requirement-to-contract traceability matrix absent |
| **TOTAL** | **1.00** | | **0.921** | |

**Arithmetic check:** (0.93×0.20) + (0.95×0.20) + (0.92×0.20) + (0.90×0.15) + (0.93×0.15) + (0.86×0.10) = 0.186 + 0.190 + 0.184 + 0.135 + 0.1395 + 0.086 = **0.9205 ≈ 0.921**

---

## Fix Verification

### Fix 1: Bonferroni k=13 consistent across master and all per-agent files

**Status: FULLY RESOLVED**

Master Section D.3 now opens with an explicit paragraph: "Authoritative comparison-set count (k=13): The full evaluation set comprises exactly 13 simultaneous comparisons: 6 S-014 dimensions + 1 composite score + 5 MRs + 1 pass rate = 13." The regression-threshold schema `comparison_sets` example now contains a `full_evaluation` entry with `k_comparisons: 13` and a description referencing `corrected_alpha_full_k13`. All 5 per-agent contracts use the field `corrected_alpha_full_k13: 0.004` with consistent inline comment. No residual k=12 or k=14 ambiguity exists. The previous implementer-facing contradiction is eliminated.

### Fix 2: QUALITY_FLOOR_BREACH scoped to Full mode only

**Status: FULLY RESOLVED**

The regression-threshold schema's Standard mode `regression_classifications_available` const array remains `["QUALITY_CHECK_PASS", "QUALITY_CHECK_FAIL", "MR_WARNING", "MR_REGRESSION"]` — QUALITY_FLOOR_BREACH is absent. The schema now adds a `description` field explicitly explaining this omission. Master Section D.5 includes a "QUALITY_FLOOR_BREACH scope" paragraph. All 5 per-agent contracts annotate the QUALITY_FLOOR_BREACH line in `merge_decisions` with "Full mode only" and the agent-specific `minimum_acceptable` threshold value. The QUALITY_FLOOR_BREACH value in each per-agent `classification` block is consistent with `quality_bounds.minimum_acceptable` in the same file (verified: ps-researcher 0.78, ps-analyst 0.81, ps-architect 0.84, ps-critic 0.79, adv-scorer 0.87 — all match).

### Fix 3: related_failure_modes populated in all 25 MR entries

**Status: FULLY RESOLVED**

Verified by reading all 5 per-agent contracts. Every MR entry in every agent now contains a populated `related_failure_modes` array with 2-3 FM IDs each, plus inline comments explaining the FM-to-MR relationship. The FM pattern is consistent across agents for equivalent MRs (MR-001 maps to FM-003 + FM-009 in all agents; MR-002 maps to FM-001 + FM-004 + FM-009 in all agents; etc.). The machine-readable traceability gap from iter1 is closed.

---

## Detailed Dimension Analysis

### Completeness (0.93/1.00)

**Evidence:**

The deliverable remains structurally comprehensive. All 5 agents have individual contract files. All 5 MRs are specified in both master and per-agent files. All 4 contract categories (structural invariants, quality bounds, MR tolerances, regression thresholds) are present. All 4 schemas are production-grade JSON Schema Draft 2020-12 with `additionalProperties: false`.

Improvements since iter1:
- Master Section D.3 now contains the k=13 derivation paragraph (previously absent)
- Master Section D.5 now contains the QUALITY_FLOOR_BREACH scope explanation (previously absent)
- Per-agent contracts now contain mode-scoped comments in `merge_decisions` (previously absent)
- All 25 MR entries now contain `related_failure_modes` (previously empty)

The creator's self-assessment claims SI-CRIT-007, SI-SCOR-010, and SI-SCOR-011 were back-propagated to master tables A.5/A.6. Independent verification: SI-SCOR-010 and SI-SCOR-011 are present in the master A.6 table (verified in read of behavioral-contracts.md). SI-CRIT-007 is present in master A.5. These are confirmed back-propagated.

**Gaps:**

1. **SI-ARCH-010 not in master A.4 table.** Master table A.4 (ps-architect structural invariants) contains SI-ARCH-001 through SI-ARCH-009. SI-ARCH-010 (navigation table check) is in the ps-architect per-agent contract but not listed in master A.4. The creator's claim notes "back-propagated" but this item was not confirmed present in master A.4 during reading — SI-ARCH-010 is a WARNING-only invariant and may have been excluded from the master intentionally, but no explanation exists.

2. **Fisher's method aggregation not encoded in machine-readable form.** Section C.6 specifies Fisher's method for multi-MR assessment, but no per-agent contract field or schema block encodes the aggregation method. An implementer reading per-agent contracts cannot find the Fisher's method specification without cross-referencing master prose.

3. **Cross-agent MR interaction effects unspecified.** Section F does not specify what happens when ps-researcher MR-001 passes but ps-analyst MR-001 fails on the same pipeline run. The interaction logic is incomplete.

**Improvement Path:**

Verify whether SI-ARCH-010 should be in master A.4 (it was back-propagated to the per-agent file in iter1 as a WARNING-only item). Add a `fisher_aggregation_method` field to the regression-threshold schema.

---

### Internal Consistency (0.95/1.00)

**Evidence:**

The three internal consistency defects from iter1 are completely eliminated. No new contradictions were found in the revised files.

Key consistency verifications performed:
- k=13 is consistent across master D.3 prose, regression-threshold schema `comparison_sets` example, and all 5 per-agent `bonferroni.corrected_alpha_full_k13` fields
- QUALITY_FLOOR_BREACH is absent from Standard mode `regression_classifications_available` const array in schema AND from Standard mode merge_decisions in all per-agent contracts
- Per-agent `classification.QUALITY_FLOOR_BREACH` threshold values match `quality_bounds.minimum_acceptable` in all 5 agents
- `related_failure_modes` FM patterns are consistent across agents for equivalent MRs
- Quality band thresholds (PASS >= 0.92, REVISE 0.85-0.91, REJECTED < 0.85) unchanged and consistent across all files
- Wilson confidence level (0.95) and minimum_n_for_floor_check (20) unchanged and consistent

**Minor residual gaps:**

1. **Master B.3 table does not document adv-scorer gap asymmetry.** The adv-scorer uses a 0.03 gap (overall_floor - minimum_acceptable) rather than the standard 0.04. This is now documented in the per-agent contract comment ("overall_floor - 0.03 (tighter gap than other agents)") but the master B.3 table has no corresponding footnote. Readers of the master alone would not know to expect this asymmetry.

2. **`rejected_maximum: 0.85` field name in per-agent contracts is semantically ambiguous.** The prose in B.2 uses "< 0.85" (exclusive) but the field name `rejected_maximum: 0.85` implies the boundary is at or below 0.85. Both are consistent with quality-enforcement.md but the field name is potentially confusing for implementers.

**Improvement Path:**

Add a footnote to master B.3 documenting the adv-scorer 0.03 gap. Consider renaming `rejected_maximum` to `rejected_upper_bound_exclusive` or adding an inline comment clarifying boundary semantics.

---

### Methodological Rigor (0.92/1.00)

**Evidence:**

The statistical methodology remains sound and well-justified. Specific methodological strengths verified:

1. **Wilcoxon selection:** Three independent rationales (distribution-free, paired, outlier-robust), plus ICML 2025 citation for preferring Wilcoxon over t-test.
2. **Effect size threshold:** The negligible-effect override (r < 0.10 = NO_REGRESSION even if p < 0.05) is explicitly justified: "At N=30, a Wilcoxon test can detect differences as small as r = 0.05." Correct reasoning.
3. **Two-condition violation logic:** Both Wilcoxon p < threshold AND mean_delta > tolerance must hold simultaneously. Prevents false alarms from significance without practical effect. Preserved and well-documented.
4. **Fisher's method:** Correctly specified in C.6 with the chi2 formula and degrees of freedom (2k). Appropriate for combining independent MR p-values.
5. **Graduated evaluation modes:** N=10 < 20 minimum prevents Wilcoxon in Standard mode; the fallback to mean-based floor check is methodologically correct.
6. **QUALITY_FLOOR_BREACH resolution methodology:** Correctly identified that Wilson intervals require N >= 20, making QUALITY_FLOOR_BREACH impossible in Standard mode. The QUALITY_CHECK_FAIL alternative is appropriate.

**Gaps:**

1. **Power analysis for N=30 is asserted, not derived.** Master D.1 states: "Recommended N per version: 30 (provides 80% power to detect an effect size of Cohen's r = 0.30 at alpha = 0.05)." This is a correct assertion — the claim can be verified with `scipy.stats` — but the derivation is absent. This was specifically called out in iter1 as needing "a one-paragraph power analysis narrative" and remains unaddressed. For a C4 deliverable specifying test sample sizes, this is a verifiability gap.

2. **MR-002 minimum_n=15 not numerically justified.** The claim that N=15 is sufficient for large effects (r >= 0.40) is directionally correct but not computed. The iter1 report asked for this explicitly.

3. **Fisher's method aggregation not in per-agent contracts or schema.** Section C.6 specifies the method but no per-agent YAML field or schema property encodes `combined_p_value_threshold` or `multi_mr_aggregation_method`. An implementer reading per-agent contracts alone cannot determine how to aggregate multi-MR results.

**Improvement Path:**

Add a Python one-liner to D.1: `scipy.stats.wilcoxon` power calculation at N=30, r=0.30, alpha=0.05. Add analogous calculation for N=15 at r=0.40 in C.2. Add a `fisher_aggregation_method: "fishers_combined_p"` field to the regression-threshold schema.

---

### Evidence Quality (0.90/1.00)

**Evidence:**

The external evidence base supports the design choices:

1. **LLMORPH citation:** The 8.6% FPR claim from ASE 2025 appears consistently in master C.0, C.1, B.5, and the mr-tolerance schema `max_delta_rationale` field description. Used as the calibration anchor for MR-001 tolerance (0.05).
2. **ICML 2025 position paper:** Cited in D.1 for Wilcoxon preference. Consistent with ADR-001 Force F-2 reference.
3. **Cohen (1988):** Cited in regression-threshold schema `rationale` field. Effect size conventions (r=0.10 small, r=0.30 medium, r=0.50 large) are consistently applied.
4. **Calibration honesty:** All per-agent contracts declare `calibration_status: "analytically_derived"` with the FM-009 mitigation note. The document does not overstate confidence in its tolerances.
5. **FM-to-MR justifications:** Inline comments in all 25 MR entries briefly explain each FM assignment. The explanations are brief but accurate.

**Gaps:**

1. **LLMORPH and ICML 2025 citations remain bibliographically underspecified.** The References section lists "LLMORPH (ASE 2025)" and "ICML 2025 position paper" without authors, title, DOI, or URL. This was specifically called out in iter1 and has not been addressed. For a C4 requirements document, a reviewer cannot locate these papers to verify the cited claims. The 8.6% FPR is a specific empirical claim that should be traceable to a locatable source.

2. **LLM non-determinism baseline (0.02-0.04 std dev) is still uncited.** The claim appears throughout the document as a design anchor but no specific study or measurement is cited. Master B.5 says "derived from LLMORPH's 8.6% false positive rate baseline" — but LLMORPH's FPR is not the same metric as temperature=0 std dev. The derivation from FPR to std dev range is not shown.

3. **FM inline comments are brief and untraceable to specific ADR-001 sections.** The comments explain the FM-to-MR relationship in one sentence but do not cite ADR-001 section numbers. An auditor wanting to verify the FM description must read all of ADR-001 to find the referenced FM.

**Improvement Path:**

Add full bibliographic citations for LLMORPH (ASE 2025) and ICML 2025 (authors, title, URL/DOI). Clarify the derivation of the 0.02-0.04 non-determinism baseline or acknowledge it as a community convention. Add ADR-001 section references to FM inline comments.

---

### Actionability (0.93/1.00)

**Evidence:**

The deliverable is highly actionable for an implementer:

1. **JSON Schema Draft 2020-12** schemas for all 4 contract types with `additionalProperties: false` and worked examples.
2. **Pseudocode violation conditions** in all 25 per-agent MR entries: `"wilcoxon_p < 0.05 AND mean_abs_delta > 0.05"` — directly translatable to test assertion code.
3. **Python code examples** in master D.1, D.2, D.3 using scipy.stats, statsmodels.
4. **Regression report JSON schema** (D.6) specifies exact output format.
5. **Mode-specific classifications** as const arrays in regression-threshold schema.
6. **Special considerations sections** in ps-critic and adv-scorer provide concrete implementation guidance.
7. **RATE_REGRESSION and MR_MULTI_REGRESSION entries** now present in all per-agent merge_decisions tables (not in iter1) — closes a gap that would have caused "unknown classification" handling errors.

**Gaps:**

1. **Test artifact directories do not exist.** ps-critic specifies `implementation_path: "contracts/test-artifacts/ps-critic/"` and adv-scorer specifies `contracts/test-artifacts/adv-scorer/"`. These paths do not exist in the repository. The specifications are accurate descriptions of future work, not actionable now.

2. **Fisher's method aggregation not encoded.** C.6 specifies the method in prose but no schema field or per-agent YAML field makes this machine-readable. An automated implementation pipeline cannot discover the aggregation method from the per-agent contracts alone.

3. **No per-agent concrete MR-001 paraphrase examples.** The master gives one example for MR-001. Per-agent contracts provide negation examples for MR-002 but not paraphrase examples for MR-001. A paraphrase generator implementation would benefit from agent-specific examples.

**Improvement Path:**

Stub test artifact directories with placeholder README files. Add `fisher_aggregation_method` field to regression-threshold schema. Add one per-agent MR-001 paraphrase example or reference the master example explicitly.

---

### Traceability (0.86/1.00)

**Evidence:**

Material improvement from iter1 (0.82 → 0.86):

1. **FMEA failure-mode cross-referencing:** All 25 MR entries now have populated `related_failure_modes` arrays (verified). This was the primary traceability gap in iter1.
2. **ADR-001 traceability:** All 5 per-agent contracts cite `source_adr` with full path. Master Overview maps each category to ADR-001 layers and FM IDs.
3. **Constitutional principle attribution:** Per-agent G-eval criteria reference P-003, P-020, P-022 by ID.
4. **Schema source fields:** All four schemas include `source` fields with pattern `^behavioral-contracts\.md#.+$`.
5. **Field-name traceability:** `corrected_alpha_full_k13` is now traceable from per-agent YAML → master D.3 → schema comparison_sets example.

**Residual gaps:**

1. **Jerry Constitution version discrepancy still unresolved.** Master Section A.7 references "Jerry Constitution v1.1." The project-level CLAUDE.md references "Jerry Constitution v1.0." This was called out in iter1 and remains unaddressed. If v1.1 does not exist in the repository, the behavioral contracts cite a phantom governance document. If v1.1 exists but differs from v1.0, the binding constitutional principles may differ from what the project operates under. Either interpretation is a traceability failure.

2. **Requirement-to-contract traceability matrix absent.** The `harness-requirements.md` exists in the project directory. No traceability matrix maps each contract clause to a specific harness-requirements.md requirement ID. For C4 requirements, this bidirectional traceability is expected and cannot be waived without documented justification.

3. **LLMORPH citation not locatable** (traceability impact). The 8.6% FPR claim drives multiple design choices (MR-001 tolerance, B.5 stability bounds rationale) but the source is not traceable to a locatable document. This affects both Evidence Quality and Traceability.

4. **Master B.3 does not document adv-scorer gap asymmetry.** Readers of the master table cannot trace adv-scorer minimum_acceptable to its derivation without consulting the per-agent contract.

**Improvement Path:**

Resolve the Jerry Constitution version reference: check whether v1.1 exists; if not, change A.7 to v1.0. Add a requirement-to-contract traceability table. Add full bibliographic citations for LLMORPH. Add a footnote to master B.3 for the adv-scorer gap.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Traceability | 0.86 | 0.91 | Resolve Jerry Constitution version reference: verify whether v1.1 exists in the repository. If it does not, change A.7 reference to v1.0. Phantom governance citations block auditability. |
| 2 | Methodological Rigor | 0.92 | 0.95 | Add a Python one-liner to D.1 showing `scipy.stats` power calculation at N=30, r=0.30, alpha=0.05. Add analogous calculation for N=15 at r=0.40 in C.2. Both are single-line additions. |
| 3 | Evidence Quality | 0.90 | 0.93 | Add full bibliographic citations for LLMORPH (ASE 2025) and ICML 2025 position paper (authors, title, URL or DOI). Without these, the two primary external citations cannot be independently verified. |
| 4 | Traceability | 0.86 | 0.91 | Add a requirement-to-contract traceability cross-reference table mapping each major contract section to the corresponding harness-requirements.md requirement ID. |
| 5 | Completeness | 0.93 | 0.95 | Verify SI-ARCH-010 status in master A.4. Back-propagate if missing. Add Fisher's method aggregation as a machine-readable field in the regression-threshold schema. |
| 6 | Actionability | 0.93 | 0.95 | Stub test artifact directories with placeholder README files. Add per-agent Fisher aggregation field. |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score with specific file paths, field names, and section references cited
- [x] Uncertain scores resolved downward: Traceability scored 0.86 (not 0.90) because both the Jerry Constitution phantom reference and the missing requirement-to-contract matrix are material for C4 requirements; Methodological Rigor scored 0.92 (not 0.94) because the power analysis derivation gap was explicitly requested in iter1 and not addressed
- [x] Calibration check: 0.921 composite for a strong revised draft is appropriate; two dimensions remain below 0.92 with documented justification
- [x] No dimension scored above 0.95 without exceptional evidence: Internal Consistency (0.95) is justified by three specific inter-file consistency defects being completely eliminated with zero new contradictions found
- [x] Anchor avoidance: Creator's self-assessment of 0.947 was not adopted. Independently computed from evidence. Composite 0.921 differs from self-assessment by 0.026.
- [x] Rubric applied literally: "0.90+" for Internal Consistency requires "No contradictions, all claims aligned" — the three iter1 contradictions are resolved; only minor asymmetries remain that do not constitute contradictions

---

## Verdict Rationale

**Composite: 0.921 | Verdict: REVISE (C4 threshold: 0.94)**

The three iter1 blocking findings are fully resolved:
- Bonferroni k=13 is now authoritative and consistent across all 10 files
- QUALITY_FLOOR_BREACH is correctly scoped to Full mode only in schema, master prose, and all per-agent contracts
- All 25 MR `related_failure_modes` entries are populated with machine-traceable FM IDs

The deliverable passes the H-13 standard quality threshold (0.92) by 0.001. It does not pass the C4-specific threshold (0.94), falling short by 0.019.

The remaining gaps are targeted and addressable:
- The Jerry Constitution v1.1 reference requires a one-line check and correction
- The power analysis derivation requires a one-line Python snippet
- The full bibliographic citations require identifying the paper URLs/DOIs
- The requirement-to-contract matrix requires mapping work but not architectural changes

No fundamental rethinking is required. The deliverable is substantively correct and production-near for the statistical framework it specifies.

---

## Score Composite Arithmetic (Verified)

```
Completeness:         0.93 × 0.20 = 0.1860
Internal Consistency: 0.95 × 0.20 = 0.1900
Methodological Rigor: 0.92 × 0.20 = 0.1840
Evidence Quality:     0.90 × 0.15 = 0.1350
Actionability:        0.93 × 0.15 = 0.1395
Traceability:         0.86 × 0.10 = 0.0860
                                    ------
SUM (unrounded):                    0.9205
REPORTED COMPOSITE:                 0.921
```

---

## Session Context Schema (for orchestrator)

```yaml
verdict: REVISE
composite_score: 0.921
threshold: 0.94
weakest_dimension: traceability
weakest_score: 0.86
critical_findings_count: 0
iteration: 2
delta_from_iter1: +0.040
improvement_recommendations:
  - "Resolve Jerry Constitution version discrepancy: A.7 references v1.1; CLAUDE.md references v1.0. Verify and align."
  - "Add power analysis derivation for N=30 (r=0.30, alpha=0.05) and N=15 (MR-002, r=0.40) — one Python snippet each in D.1 and C.2."
  - "Add full bibliographic citations for LLMORPH (ASE 2025) and ICML 2025 position paper (authors, title, DOI/URL)."
  - "Add requirement-to-contract traceability cross-reference to harness-requirements.md."
  - "Verify SI-ARCH-010 presence in master A.4; back-propagate if absent."
  - "Add master B.3 footnote documenting adv-scorer 0.03 gap asymmetry vs. standard 0.04."
  - "Add fisher_aggregation_method field to regression-threshold schema; stub test-artifact directories."
note: >
  All three iter1 blocking findings (Bonferroni k inconsistency, QUALITY_FLOOR_BREACH scope,
  related_failure_modes population) are fully resolved. Remaining gaps are targeted documentation
  and traceability completeness items. Gap to C4 threshold: 0.019. Achievable in one targeted
  revision pass.
```
