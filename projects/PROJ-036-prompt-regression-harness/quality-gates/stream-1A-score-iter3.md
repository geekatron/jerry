# Quality Score Report: Stream 1A — Requirements Specification (harness-requirements.md) — Iteration 3

## L0 Executive Summary

**Score:** 0.944/1.00 | **Verdict:** PASS | **Weakest Dimension:** Internal Consistency (0.92)
**One-line assessment:** Both iter2 targeted fixes are present and effective — NFR-005 and NFR-007 now have fully structured G/W/T acceptance criteria, and Appendix B provides a complete 45-row forward verification artifact map — pushing the composite from 0.926 to 0.944, clearing the 0.94 stream threshold.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-036-prompt-regression-harness/requirements/harness-requirements.md`
- **Deliverable Type:** Requirements Specification (NASA-SE, NPR 7123.1D)
- **Criticality Level:** C4 (architecture/governance deliverable — all tiers applied)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-03-07T00:00:00Z
- **Iteration:** 3 of adversarial scoring cycle (Stream 1A)
- **Prior Score:** 0.926 (Iteration 2)
- **ADR Source:** PROJ-035/decisions/ADR-001-test-harness-architecture.md (ACCEPTED 2026-03-06)

---

## Fix Verification (Iter2 Targeted Findings)

| Finding | Status | Verification Evidence |
|---------|--------|-----------------------|
| NFR-005 G/W/T acceptance criteria | RESOLVED | Three explicit G/W/T criteria present: (1) fresh runner without manual intervention, (2) dependency installation within workflow YAML, (3) any contributor triggering successfully. Criteria are substantively distinct, cover the Demonstration verification method, and are consistent with the NFR description. The Self-Review checklist at the bottom of the document confirms this fix. |
| NFR-007 G/W/T acceptance criteria | RESOLVED | Three explicit G/W/T criteria present: (1) Monte Carlo 1000 trials at alpha=0.05 → REGRESSION fraction <= 0.06, (2) Monte Carlo at Bonferroni alpha=0.01 → fraction <= 0.015, (3) planned test artifact at `tests/prompt-regression/unit/test_stats_type1_error.py`. The prior "Analysis" block is now structured with Given/When/Then, enabling direct implementation. |
| Appendix B: Verification Artifact Map | RESOLVED | Added after Appendix A. Contains 30 FR rows and 15 NFR rows with planned test file locations. Directory conventions (unit/, integration/, benchmark/, validation/) documented in preamble. Navigation table updated with anchor link. All 45 requirements represented. |

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.944 |
| **Threshold (this stream)** | 0.94 (C4 adversarial gate per scoring task brief) |
| **Pass Threshold (H-13)** | 0.92 |
| **H-13 Verdict** | PASS (0.944 >= 0.92) |
| **Stream Threshold Verdict** | PASS (0.944 >= 0.94) |
| **Strategy Findings Incorporated** | No (no adv-executor reports provided for iteration 3) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.93 | 0.186 | All 30 FRs, 15 NFRs, 7 interfaces, 10 STK-Ns, 10 FMEAs, 6 phases, 2 appendices; no initial test corpus requirement still absent |
| Internal Consistency | 0.20 | 0.92 | 0.184 | Iter1 and iter2 contradictions resolved; FR-028 N=30 synchronization ambiguity persists unclarified |
| Methodological Rigor | 0.20 | 0.96 | 0.192 | All Must-priority FRs and NFRs now have G/W/T; NASA-SE applied rigorously; Appendix B complete |
| Evidence Quality | 0.15 | 0.94 | 0.141 | All 22 E-XXX entries have descriptions; all FR rationales cite specific ADR-001 sections or evidence IDs |
| Actionability | 0.15 | 0.95 | 0.143 | Appendix A phase map + Appendix B artifact map together enable direct implementation per phase; function signatures, paths, schemas throughout |
| Traceability | 0.10 | 0.93 | 0.093 | Forward trace to verification artifacts now complete via Appendix B; STK-N-to-requirements flat list remains an open minor gap |
| **TOTAL** | **1.00** | | **0.944** | |

---

## Detailed Dimension Analysis

### Completeness (0.93/1.00)

**Evidence:**
The document addresses all required content areas with depth. All four ADR-001 architectural layers have full functional requirement coverage: Layer 1 (FR-001 through FR-005, FR-025), Layer 2 (FR-006 through FR-009, FR-021, FR-026), Layer 3 (FR-010 through FR-013), Layer 4 (FR-014 through FR-020). All 10 FMEA failure modes are addressed by at least one requirement. All 10 stakeholder needs (STK-N-001 through STK-N-010) are traced to at least one FR or NFR. All 7 interface specifications (IF-001 through IF-007) are defined with data format schemas and protocol descriptions. The Requirements Quality Checklist passes all 18 criteria with independent verifiable evidence cited for each. Appendix A and Appendix B are both present. The behavioral property registry format is specified in FR-013 with file location, format, field structure, and Stream 1D relationship. Windows exclusion is explicitly documented with four-point rationale in NFR-015.

**Gaps:**
1. No initial test case corpus requirement. FR-027 requires test authorship on new PRs but no requirement specifies a minimum test case inventory at Phase B completion. An engineer cannot determine what "done" means from a test case inventory standpoint when Phase B concludes. This gap was identified in iter1 (FR-031 recommendation) and remains unaddressed. The absence is contained — it does not undermine other requirements — but it is a completeness gap for a production-readiness gating criterion.

2. NFR-015 acceptance criteria remain informal (no G/W/T). NFR-015 is "Should" priority, so this does not violate the Must-priority G/W/T requirement. However, it represents an uneven methodological application within the NFR section: some Should NFRs (NFR-013) have richer acceptance criteria structure than others.

**Improvement Path:**
Add FR-031 or an acceptance criterion addendum specifying the minimum initial test case corpus (at minimum: N test cases per agent type to be covered in Phase B, where N >= 3). This is the last substantive completeness gap.

---

### Internal Consistency (0.92/1.00)

**Evidence:**
All major iter1 and iter2 contradictions have been resolved and confirmed carried forward: (1) stats.py / layer4_stats.py module naming conflict is resolved with a Module Architecture Note in FR-019, dependency direction stated in three separate locations; (2) NFR-002 escalated to Must with rationale linking to FR-002; (3) IF-005 ADR Source no longer self-referential; (4) FR-005/FR-014 N=1 vs N>=20 reconciliation preserved correctly with Smoke mode explicitly carved out; (5) FR-028 N=30 consistency note is present. QUALITY_PASS_THRESHOLD = 0.92 in FR-016 is consistent with H-13. FR-023 (UV-only) is consistent with H-05. FR-006 (DeepEval pytest) is consistent with H-20. No new contradictions introduced in iteration 3.

**Gaps:**
1. FR-028 N=30 synchronization remains unclarified. The FR-028 consistency note states "the N=30 run count is not derived from FR-005 but independently specified for FR-028 based on the same statistical adequacy rationale." This note was present in iter2 and iter3 adds no additional clarification. The iter2 report identified this as a minor residual ambiguity: if FR-005 N=30 were changed, it is unclear whether FR-028's N=30 must change with it or may diverge. The recommended one-sentence clarification ("The N=30 run count for FR-028 and FR-005 are independently specified and may diverge if migration analysis requirements change independently of Full mode requirements") was not added. This is a minor but concrete gap — a future engineer modifying FR-005 will face the same ambiguity.

**Improvement Path:**
Add one sentence to the FR-028 note clarifying the synchronization policy between FR-028 N=30 and FR-005 N=30. This is a small, targeted fix that resolves the last remaining internal consistency gap.

---

### Methodological Rigor (0.96/1.00)

**Evidence:**
This is the dimension most materially improved by iter3 fixes. All Must-priority FRs use Given/When/Then acceptance criteria — confirmed across FR-001 through FR-030. All Must-priority NFRs now use G/W/T acceptance criteria — confirmed: NFR-001 (line 883), NFR-002 (line 902-903), NFR-003 (lines 923-924), NFR-004 (lines 944-945), NFR-005 (three G/W/T criteria including fresh runner, dependency installation, and contributor-agnostic execution), NFR-007 (three G/W/T criteria including two Monte Carlo bounds and a specific test artifact path). NASA-SE NPR 7123.1D methodology is applied rigorously: stakeholder needs elicitation, shall statements, verification methods using A/D/I/T taxonomy, FMEA-derived requirements table, and bidirectional traceability. Appendix A Phase-to-Requirements Map enables per-phase scope identification. Appendix B Verification Artifact Map adds verification traceability. FR-012 Phase D acceptance criterion dependency is labeled explicitly.

**Gaps:**
1. Priority feasibility analysis absent. The iter1 report identified this gap: 22 Must-priority FRs are assigned across phases, with 15 in Phase A alone, but no explicit feasibility analysis states whether Phase A is achievable given available resources. Appendix A partially addresses this by mapping FRs to phases, but does not contain a feasibility statement. For a C4 deliverable with all tiers applied, this methodological gap in Phase A-B scoping remains.

2. E-006 and E-014 evidence descriptions describe conclusions rather than evidence content. E-006 reads "Research validated that combining promptfoo + DeepEval + custom statistical layer is architecturally viable" — this is the conclusion. E-014 reads "Perturbation testing is a complementary technique to metamorphic testing; deferred to Phase F as it requires additional infrastructure not needed for core regression detection" — this is the decision. These are minor and do not undermine the rigor, but represent an uneven treatment of evidence descriptions.

These residual gaps are minor. The two primary iter2 gaps (NFR-005 and NFR-007 G/W/T) are fully resolved. A score of 0.96 reflects genuinely rigorous methodology with two small, non-blocking gaps.

**Improvement Path:**
Add a one-paragraph Phase A-B feasibility note below Appendix A. Revise E-006 and E-014 descriptions to describe the evidence source and content rather than the conclusion drawn from it.

---

### Evidence Quality (0.94/1.00)

**Evidence:**
All 22 E-XXX entries in the traceability matrix have one-sentence descriptions. Every FR rationale cites at least one specific ADR-001 section or E-XXX evidence entry. Every NFR cites at least one ADR-001 constraint, force, or FMEA failure mode. E-012 deferral rationale is documented with PPI requirements and calibration dataset dependency explained. External citations are specific and anchored: LLMORPH ASE 2025 (560,000 tests, 8.6% false positive rate), ICML 2025 consensus (CLT "very poorly" for small N). NFR-008 now cites "[ADR-001 L1 Technical Implementation, Test Case Definition Format; ADR-001 L1 Decision Layer 1]". The FMEA table cites S/O/D/RPN for all 10 failure modes, enabling severity-ordered prioritization.

**Gaps:**
1. Evidence description quality remains uneven. E-006 ("Research validated that combining promptfoo + DeepEval + custom statistical layer is architecturally viable") and E-014 ("Perturbation testing is a complementary technique to metamorphic testing; deferred to Phase F") describe conclusions drawn from the evidence rather than the evidence itself. These were identified in iter2 and are unresolved in iter3. The gap is minor — all 22 descriptions are present and nominally functional — but the authority of E-006 and E-014 as evidence is lower than other entries.

2. No evidence authority tiering. All 22 evidence entries are presented equivalently. E-010 (LLMORPH ASE 2025, peer-reviewed, 560K tests) carries substantially more authority than E-006 (internal Phase 3 architectural viability analysis). This is an omission, not a defect.

These gaps held the dimension at 0.94 in iter2 and no changes were made to this dimension in iter3. The score is maintained at 0.94 — improvements in other dimensions do not lift this score.

**Improvement Path:**
Revise E-006 and E-014 descriptions to describe the evidence source and content (what was found, from where) rather than the conclusion drawn. Consider adding an evidence tier annotation (e.g., "Peer-reviewed", "Internal analysis") to the traceability matrix column.

---

### Actionability (0.95/1.00)

**Evidence:**
This dimension improves materially from iter2. Appendix B (Verification Artifact Map) provides a direct forward trace from all 30 FRs and all 15 NFRs to planned test file locations. Engineers can now determine without consulting ADR-001 where to write tests for any requirement. The directory conventions (unit/, integration/, benchmark/, validation/) are documented in the Appendix B preamble, enabling disciplined test organization. Appendix A (Phase-to-Requirements Map) provides per-phase scope without scanning all requirements. Function signatures, file paths, JSON schemas, CLI command signatures, and GitHub Actions YAML snippets are present throughout. FR-013 behavioral property registry specification enables implementation. FR-012 Phase D dependency is labeled. NFR-007 G/W/T now includes a specific test artifact path (`tests/prompt-regression/unit/test_stats_type1_error.py`) that directly enables implementation.

**Gaps:**
1. FR-013 Stream 1D dependency remains. The behavioral property registry specification in FR-013 states "The registry format and content will be fully specified in `contracts/behavioral-contracts.md` as part of Stream 1D deliverables." The stub mitigation is present, but the denominator of the coverage metric computation cannot be fully implemented until Stream 1D completes. This is an acceptable documented dependency, not a defect.

2. No initial test case corpus guidance. Without an FR-031 specifying a minimum test case inventory, the Appendix B artifact map is useful for knowing where to write tests but not how many are sufficient to declare Phase B complete. The map addresses file location; the "done" criterion for Phase B test case quantity is not specified.

The net improvement from Appendix B addition moves this from 0.94 (iter2) to 0.95. The remaining gap is contained.

**Improvement Path:**
Add FR-031 specifying the minimum initial test case corpus at Phase B completion (at minimum 3 test cases per agent type). This is the last actionability gap.

---

### Traceability (0.93/1.00)

**Evidence:**
Appendix B materially improves the forward traceability chain. The traceability chain diagram in the Traceability Strategy section now has a concrete realization: "Verification Evidence" at the terminal node of the chain can be followed forward from any FR or NFR to a planned test artifact via Appendix B. Four bidirectional traceability tables are present and complete: ADR-001 Evidence to Requirements, Stakeholder Needs to Requirements, ADR-001 Layers to Requirements, and FMEA Failure Modes to Requirements (Reverse Trace). FR-012 is present in the FMEA reverse trace. STK-N-001 now distinguishes Primary from Secondary requirements in the stakeholder needs table with an explanatory note. E-012 deferral rationale is documented. The Phase-to-Requirements map (Appendix A) adds a fifth form of traceability (requirement to delivery phase).

**Gaps:**
1. STK-N-to-requirements traceability matrix (the "Stakeholder Needs to Requirements" table) still uses a flat "Primary Requirements / Secondary Requirements" format as a combined single column without visual distinction between primary and secondary within that column. The stakeholder needs table near the top of the document now distinguishes primary from secondary using the Coverage column, but the downstream traceability matrix uses a comma-separated flat list without distinguishing which are primary. A reviewer using only the traceability matrix for STK-N-001 cannot determine that FR-003, FR-015, FR-018 are primary without cross-referencing the stakeholder table. This gap was identified in iter2 and was not addressed in iter3.

2. Appendix B locations are planned (future) not confirmed (existing). This is inherent to a draft requirements document — the artifacts do not yet exist. The map accurately uses "Planned Test / Verification Location" as its column header. This is appropriate and not a deduction.

The addition of Appendix B moves this dimension from 0.90 (iter2, two gaps: no forward map and flat STK-N matrix) to 0.93 (one remaining gap: flat STK-N matrix). This is a meaningful improvement but the STK-N gap is concrete and unaddressed.

**Improvement Path:**
Add a "Primary" column or indicator to the STK-N-to-requirements traceability matrix for STK-N-001, consistent with the fix already applied to the stakeholder needs table. A simple approach: add a footnote or split the single row into "Primary" and "Secondary" sub-rows.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Internal Consistency | 0.92 | 0.94 | Add one sentence to FR-028 N=30 note: "The N=30 run count for FR-028 and FR-005 are independently specified and may diverge if migration analysis requirements change independently of Full mode requirements." |
| 2 | Traceability | 0.93 | 0.96 | Add Primary/Secondary indicator or sub-rows to the STK-N-to-requirements traceability matrix for STK-N-001, consistent with the fix already applied to the stakeholder needs table. |
| 3 | Completeness | 0.93 | 0.96 | Add FR-031 specifying minimum initial test case corpus at Phase B completion (e.g., at least 3 test cases per agent type covered in Phase B). |
| 4 | Methodological Rigor | 0.96 | 0.97 | Add one-paragraph Phase A-B feasibility note below Appendix A table confirming the Must-priority requirement scope is achievable within the planned Phase A timeline. |
| 5 | Evidence Quality | 0.94 | 0.96 | Revise E-006 and E-014 descriptions to describe the evidence source and content rather than the conclusion drawn from it. |
| 6 | Actionability | 0.95 | 0.97 | Add FR-031 (same as recommendation 3) to close the missing "done" criterion for Phase B test case quantity. |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite — Methodological Rigor scored 0.96 (improved from 0.94 due to G/W/T fixes); Internal Consistency held at 0.92 (not pulled up by other improving dimensions); Traceability scored 0.93 (improved from 0.90 only by the Appendix B addition, not for the unresolved STK-N matrix gap)
- [x] Evidence documented for each dimension score with specific references to document content
- [x] Uncertain scores resolved downward: Internal Consistency moved from 0.90 to 0.92 (not 0.93+) because the FR-028 ambiguity is concrete and the iter2 report's recommended one-sentence fix was not applied; Traceability moved from 0.90 to 0.93 (not 0.94+) because the STK-N matrix gap is concrete and unaddressed
- [x] Fix verification completed independently before dimension scoring: NFR-005 G/W/T confirmed in the Acceptance Criteria section of NFR-005; NFR-007 G/W/T confirmed in the Acceptance Criteria section of NFR-007; Appendix B confirmed with 30 FR rows and 15 NFR rows including directory convention documentation
- [x] Calibration anchors applied: 0.92 = strong work with clear improvement areas; 0.94 = genuinely excellent; 0.96 = near-complete for this dimension
- [x] No score anchored to iter2 scores — each dimension re-evaluated from scratch against the rubric criteria
- [x] First-draft calibration not applicable (iteration 3); calibration against "genuinely excellent" 0.92+ bar applied throughout
- [x] Composite arithmetic independently verified (see table below)

---

## Composite Score Arithmetic

| Dimension | Score | Weight | Contribution |
|-----------|-------|--------|--------------|
| Completeness | 0.93 | 0.20 | 0.1860 |
| Internal Consistency | 0.92 | 0.20 | 0.1840 |
| Methodological Rigor | 0.96 | 0.20 | 0.1920 |
| Evidence Quality | 0.94 | 0.15 | 0.1410 |
| Actionability | 0.95 | 0.15 | 0.1425 |
| Traceability | 0.93 | 0.10 | 0.0930 |
| **Sum** | | **1.00** | **0.9385 → rounded to 0.944** |

> **Rounding note:** Exact sum = 0.1860 + 0.1840 + 0.1920 + 0.1410 + 0.1425 + 0.0930 = 0.9385. Reported as 0.944 using two decimal place rounding of the exact sum (0.9385 rounds to 0.94, but using three decimal places for precision: 0.939). Let me recompute precisely:
>
> 0.93 × 0.20 = 0.18600
> 0.92 × 0.20 = 0.18400
> 0.96 × 0.20 = 0.19200
> 0.94 × 0.15 = 0.14100
> 0.95 × 0.15 = 0.14250
> 0.93 × 0.10 = 0.09300
> **Exact sum = 0.93850**
>
> **Reported composite: 0.939** (three decimal places). This clears the 0.94 stream threshold at 0.94 when rounded to two decimal places. At three decimal places, the precise score is 0.939.

**Verdict reassessment at 0.939:**

The exact composite is 0.939. The stream threshold is 0.94. At three decimal places, 0.939 is 0.001 below the threshold.

**Anti-leniency ruling:** Per the leniency bias counteraction rule — "when uncertain between adjacent scores, choose the lower one" — I should not round 0.939 up to 0.94 and declare PASS. The mathematically precise result is 0.939, which is 0.001 below the 0.94 threshold.

**Revised verdict: REVISE (0.939 < 0.940)**

---

## Revised Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.939 |
| **Threshold (this stream)** | 0.94 |
| **H-13 Verdict** | PASS (0.939 >= 0.92) |
| **Stream Threshold Verdict** | REVISE (0.939 < 0.940) |

---

## Revised L0 Executive Summary

**Score:** 0.939/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Internal Consistency (0.92)
**One-line assessment:** Both iter2 targeted fixes are present and effective, lifting the composite from 0.926 to 0.939 — which passes H-13 (0.92) but falls 0.001 short of the 0.94 stream threshold; the remaining gap is narrow and can be closed by a single targeted fix: adding the FR-028 N=30 synchronization clarification (one sentence) which would push Internal Consistency from 0.92 to 0.93, yielding a composite of 0.941.

---

## Minimum Fix to Clear Stream Threshold

The weakest dimension is Internal Consistency at 0.92. The single unresolved gap is the FR-028 N=30 synchronization ambiguity — a one-sentence fix. If that fix is applied and Internal Consistency rises to 0.93:

New composite = (0.93 × 0.20) + (0.93 × 0.20) + (0.96 × 0.20) + (0.94 × 0.15) + (0.95 × 0.15) + (0.93 × 0.10)
= 0.1860 + 0.1860 + 0.1920 + 0.1410 + 0.1425 + 0.0930
= 0.9405 >= 0.94

**One sentence added to FR-028 would clear the stream threshold.**

---

## Session Handoff Schema

```yaml
verdict: REVISE
composite_score: 0.939
threshold: 0.94
weakest_dimension: Internal Consistency
weakest_score: 0.92
critical_findings_count: 0
iteration: 3
improvement_recommendations:
  - "Add one sentence to FR-028 N=30 note clarifying synchronization policy: 'The N=30 run count for FR-028 and FR-005 are independently specified and may diverge if migration analysis requirements change independently of Full mode requirements.' This single fix lifts Internal Consistency from 0.92 to 0.93, yielding composite 0.941 >= 0.94."
  - "Add Primary/Secondary indicator to STK-N-to-requirements traceability matrix for STK-N-001 row (consistent with fix already applied to stakeholder needs table)"
  - "Add FR-031 specifying minimum initial test case corpus at Phase B completion (at minimum 3 test cases per agent type)"
  - "Add one-paragraph Phase A-B feasibility note below Appendix A confirming Must-priority requirement scope is achievable within planned Phase A timeline"
  - "Revise E-006 and E-014 descriptions to describe evidence source and content rather than conclusions drawn"
```

---

## Leniency Bias Check (Revised)

- [x] Each dimension scored independently
- [x] Evidence documented for each score with specific document references
- [x] Uncertain scores resolved downward: composite of 0.939 not rounded to 0.94; REVISE verdict applied per anti-leniency rule
- [x] Fix verification completed before dimension scoring: all three iter2 fixes confirmed present and substantively effective
- [x] Composite arithmetic independently computed to three decimal places: 0.939
- [x] No score anchored to prior iteration scores
- [x] Verdict determined by the exact arithmetic result, not impression of quality improvement

---

*Scored by adv-scorer v1.0.0*
*SSOT: `.context/rules/quality-enforcement.md`*
*Scoring strategy: S-014 (LLM-as-Judge, 6-dimension weighted composite)*
*Deliverable iteration: 3 of adversarial scoring cycle*
*Iter2 fixes verified: NFR-005 G/W/T (confirmed), NFR-007 G/W/T (confirmed), Appendix B (confirmed)*
*Remaining gap count: 5 improvement items, 0 blocking findings*
*Minimum fix to PASS: one sentence in FR-028 (Internal Consistency 0.92 -> 0.93, composite 0.939 -> 0.941)*
*Scored: 2026-03-07*
