# Quality Score Report: Stream 1D — Behavioral Contracts (PROJ-036)

## L0 Executive Summary

**Score:** 0.939/1.00 | **Verdict:** REVISE (C4 threshold: 0.94) | **Weakest Dimension:** Evidence Quality (0.92)
**One-line assessment:** Both iter4 fixes are confirmed present (Section G traceability matrix and N_min bridge paragraph), but two specific contradictions were introduced or carried forward — the G.1 vs G.3 FR-022/FR-023 inconsistency (new in iter4) and the ASE 2025 body-text citation error that was claimed resolved in iter3 but remains uncorrected at C.0 line 300 — holding the composite at 0.939, 0.001 below the C4 threshold.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-036-prompt-regression-harness/contracts/` (10-file set: 1 master, 5 per-agent, 4 schemas)
- **Deliverable Type:** Requirements / Specifications (behavioral contract set)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Threshold Applied:** 0.94 (C4 stream threshold specified in scoring brief)
- **Standard H-13 Threshold:** 0.92
- **Scored:** 2026-03-07T20:00:00Z
- **Iteration:** 4 (independent scoring of revised deliverable)
- **Prior Score:** 0.938 (iter3, exact composite per verified arithmetic) — read for context only; not used as anchor; scored independently
- **Strategy Findings Incorporated:** No (no adv-executor reports provided)

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.939 |
| **Threshold (C4)** | 0.94 |
| **Threshold (H-13 standard)** | 0.92 |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.94 | 0.1880 | Section G adds full traceability matrix; Fisher machine-readability gap and test artifact directory stubs still absent |
| Internal Consistency | 0.20 | 0.94 | 0.1880 | G.1 row for A.7 claims FR-022/FR-023 enforced by behavioral contracts; G.3 explicitly lists FR-022/FR-023 as not covered — direct contradiction within Section G; C.0 body text still reads "ASE 2025" while References and citation index correctly say "ASE 2024" |
| Methodological Rigor | 0.20 | 0.96 | 0.1920 | N_min bridge paragraph present and effective (iter4 Fix 2); explains unpaired Z-test gives N_min≈154 while paired Wilcoxon operates on N pairs; scipy simulation is the authoritative verification |
| Evidence Quality | 0.15 | 0.92 | 0.1380 | C.0 body text citation says "ASE 2025" (incorrect); References correctly say "ASE 2024" — inconsistency claimed resolved in iter3 report but verifiably uncorrected in body text; B.5 std dev derivation still asserted not computed |
| Actionability | 0.15 | 0.93 | 0.1395 | All iter3 strengths retained; test artifact directories still unspecified; Fisher not machine-readable in per-agent schemas; power simulation delta approximation still present |
| Traceability | 0.10 | 0.93 | 0.0930 | Section G fully present with 20-row forward trace (G.1), 22-requirement reverse trace (G.2), 4-section coverage assessment (G.3); all FR/NFR IDs verified to exist in harness-requirements.md; G.1 A.7 row contains factual error on FR-022/FR-023 scope; FM inline comments still lack ADR-001 section numbers |
| **TOTAL** | **1.00** | | **0.939** | |

**Arithmetic verification:**
```
Completeness:         0.94 × 0.20 = 0.18800
Internal Consistency: 0.94 × 0.20 = 0.18800
Methodological Rigor: 0.96 × 0.20 = 0.19200
Evidence Quality:     0.92 × 0.15 = 0.13800
Actionability:        0.93 × 0.15 = 0.13950
Traceability:         0.93 × 0.10 = 0.09300
                                    -------
SUM (unrounded):                    0.93850
REPORTED COMPOSITE:                 0.939
C4 THRESHOLD:                       0.940
GAP:                                -0.001
```

**VERDICT: REVISE — 0.001 below exact C4 threshold**

---

## Fix Verification (Iter4 Fixes)

### Fix 1: Requirement-to-Contract Traceability Matrix (Section G)

**Status: PRESENT AND LARGELY EFFECTIVE — with one internal consistency defect**

Section G is fully present at line 792 of behavioral-contracts.md. The section appears in the document navigation table and contains:

**G.1 Forward Trace (lines 797–826):** A 20-row table mapping each contract section (A.1 through D.6) to specific FR/NFR IDs with traceability rationale. All requirement IDs in G.1 were independently verified against harness-requirements.md:
- FR-007, FR-008, FR-010, FR-011, FR-012, FR-013, FR-014, FR-015, FR-016, FR-017, FR-018, FR-019, FR-020, FR-021, FR-022, FR-023, FR-028 — all exist
- NFR-002, NFR-006 — both exist
- Rationale column explains why each contract section implements each requirement ID

**G.2 Reverse Trace (lines 828–855):** A 22-row table mapping requirement IDs back to contract sections. Includes explicit coverage of FR-001, FR-004 as infrastructure-only (no behavioral contract coverage) with rationale.

**G.3 Coverage Assessment (lines 856–865):** A 4-section summary with "None" orphan risk for all four major contract sections. An explicit "not covered" list identifies 15 infrastructure requirements (FR-001, FR-002 partial, FR-003, FR-004, FR-006, FR-009 partial, FR-019, FR-022, FR-023, FR-024, FR-025, FR-026, FR-027, FR-029, FR-030, NFR-001, NFR-003, NFR-004, NFR-005) with rationale.

**Defect found in G.1:** The A.7 row (Constitutional Compliance Invariants) lists `FR-008, FR-022, FR-023` as the "Requirement IDs Enforced." FR-022 (OSI-Approved License Verification) and FR-023 (UV-Only Python Execution) are infrastructure requirements about dependency licensing and execution environment — they are not behavioral oracle contracts. G.3 correctly identifies FR-022 and FR-023 as "not covered by behavioral contracts." This means G.1 and G.3 directly contradict each other on the coverage status of FR-022 and FR-023. A reader relying on G.1 would believe the behavioral contracts govern license compliance and UV enforcement; G.3 correctly says they do not. This is a factual error in G.1 that needs correction: FR-022/FR-023 should be removed from the A.7 row in G.1 (the correct mappings for SI-CONST-001 through SI-CONST-004 are to the constitutional triplet H-01/H-02/H-03 encoded in quality-enforcement.md, not to FR-022/FR-023 which govern implementation infrastructure).

**Net assessment:** Section G is a substantial addition that addresses the primary traceability gap identified in iter3. The G.1/G.3 FR-022/FR-023 contradiction is a precision defect, not a fundamental structural failure. Removing FR-022/FR-023 from G.1 A.7 and either leaving the row blank or mapping to the correct constitutional traceability sources would close this defect in one line edit.

**Expected Traceability score impact (iter3 → iter4):** +0.04 (from 0.89 to 0.93). Section G resolves the primary traceability gap. The G.1 defect prevents full 0.96+ achievement.

### Fix 2: N_min Formula Bridge

**Status: FULLY RESOLVED AND EFFECTIVE**

Lines 500–501 of behavioral-contracts.md (within Section D.1 power analysis):

> "The N_min ≈ 154 result applies to the unpaired Z-test approximation of the Wilcoxon test. For the paired Wilcoxon signed-rank test (which operates on N paired differences rather than 2N independent samples), the effective sample size is the number of pairs. The scipy simulation below provides the authoritative power verification at N=30 paired observations."

This exactly addresses the iter3 gap: the formula path from N_min=153.76 to "therefore N=30 is sufficient" is now bridged by explaining that the formula applies to the unpaired approximation while the paired test operates on N differences. The scipy simulation is correctly positioned as the authoritative verification. The bridge paragraph is concise, accurate, and appears immediately after the N_min computation, before the simulation code block — exactly where a reader needs it.

**Evidence of effectiveness:** The derivation is now a complete chain: H0/H1 → parameters → Z_alpha/2 and Z_beta → N_min formula → 153.76 → bridge paragraph explaining paired vs unpaired distinction → scipy simulation → empirical power 0.83 (uncorrected) and 0.71 (corrected). No gaps remain in the methodological chain.

---

## Detailed Dimension Analysis

### Completeness (0.94/1.00)

**Evidence:**

All iter3 completeness coverage is retained:
- 5 agents × 5 MRs = 25 MR entries, all present with `related_failure_modes` populated
- 4 contract categories fully specified (structural invariants, quality bounds, MR tolerances, regression thresholds)
- 4 JSON Schema files with `additionalProperties: false`
- SI-SCOR-010, SI-SCOR-011 in A.6; SI-CRIT-007 in A.5; SI-ARCH-010 in A.4

Iter4 adds Section G (traceability matrix), which adds a new required domain. The forward trace covers all major contract sections. The coverage assessment explicitly accounts for requirements outside behavioral contract scope.

**Gaps:**

1. **Fisher's method not machine-readable.** No per-agent YAML field encodes `fisher_aggregation_method` or `combined_p_value_threshold`. An automated pipeline reading only per-agent contracts cannot discover the C.6 aggregation method. Present since iter2, not addressed.

2. **Test artifact directories not stubbed.** `implementation_path: "contracts/test-artifacts/adv-scorer/"` references a non-existent path. Present since iter2, not addressed.

**Improvement Path:**

Add `fisher_aggregation_method: "fishers_combined_p"` field to the regression-threshold schema. Create stub `contracts/test-artifacts/{agent}/README.md` files noting calibration artifact requirements.

---

### Internal Consistency (0.94/1.00)

**Evidence:**

All iter3 consistency strengths are retained:
- k=13 consistent across master D.3, schema `comparison_sets` example, and all 5 per-agent `corrected_alpha_full_k13: 0.004`
- QUALITY_FLOOR_BREACH absent from Standard mode `regression_classifications_available` in schema; D.5 scope paragraph present
- Per-agent `classification.QUALITY_FLOOR_BREACH` threshold values match `quality_bounds.minimum_acceptable` in all 5 agents

**New contradictions introduced or carried forward in iter4:**

1. **G.1 vs G.3 contradiction on FR-022/FR-023 coverage (new in iter4):**
   - G.1, A.7 row: "Requirement IDs Enforced: FR-008, FR-022, FR-023"
   - G.3, unambiguously states: FR-022, FR-023 are in the "not covered by behavioral contracts" list
   - These cannot both be correct. FR-022 governs OSI license verification; FR-023 governs UV-only execution. Neither is an agent behavioral oracle. The constitutional invariants (SI-CONST-001 through SI-CONST-004) govern P-003/P-020/P-022 compliance in agent outputs, not dependency licensing.
   - This is a factual contradiction within Section G, the new content added in iter4.

2. **C.0 body text citation year inconsistency (carried from pre-iter3, not corrected):**
   - Line 300: `Per ADR-001 Layer 3 and LLMORPH (ASE 2025, 560K tests, 8.6% false positive rate):`
   - References section [5]: `Proceedings of the 39th IEEE/ACM International Conference on Automated Software Engineering (ASE 2024)`
   - Inline citation index: `[5] | Deng et al. / LLMORPH (ASE 2024) | C.0 (8.6% FPR baseline)...`
   - The iter3 score report stated this was "resolved." It was not: the body text at C.0 was not corrected, only the References section. The body citation remains ASE 2025.

**Residual minor gaps (unchanged from iter3):**

- Master B.3 adv-scorer gap asymmetry footnote absent (floor - 0.03 not documented in master table)
- `rejected_maximum: 0.85` semantic naming ambiguity

**Improvement Path:**

Correct G.1 A.7 row: remove FR-022/FR-023 from "Requirement IDs Enforced" (correct mapping for SI-CONST-001 through SI-CONST-004 is to the constitutional triplet in quality-enforcement.md, which is cited in body text but not encoded as an FR). Correct C.0 body text: change "ASE 2025" to "ASE 2024" to match the reference [5] entry.

---

### Methodological Rigor (0.96/1.00)

**Evidence:**

Fix 2 (N_min bridge) resolves the last major methodological gap from iter3. The complete methodological chain is now present:

1. **Formal N=30 power analysis:** H0/H1 explicitly stated, Z_alpha/2=2.88 and Z_beta=0.84 computed with qnorm calls, N_min formula derived, computation shown (153.76), bridge paragraph explains paired vs unpaired distinction, scipy simulation provides authoritative verification, empirical powers 0.83 (uncorrected) and 0.71 (corrected) stated with tradeoff acknowledgment.

2. **MR-002 N=15 derivation:** Z_required = r × sqrt(N) formula applied at N=15 and N=20, power approximately 0.66 and 0.61, practical justification present.

3. **Wilcoxon selection:** Three rationales (distribution-free, paired, outlier-robust) plus NeurIPS 2023 citation [6].

4. **Wilson interval:** N=20 minimum derived from interval width > 0.30 below N=20.

5. **Fisher's method:** chi2 formula and df=2k stated, severity table present.

6. **Effect size rationale:** Negligible-effect override for r < 0.10 justified by detection sensitivity at N=30.

**Remaining minor gap:**

The power analysis simulation uses `delta = 0.30 * baseline.std()` to model a Cohen's r=0.30 effect. Cohen's r for the Wilcoxon test is Z/sqrt(N), not a direct score delta. The code is a reasonable approximation but the comment does not note the approximation, meaning an implementer who runs it verbatim will get approximately (not rigorously) the stated power. This was identified in iter3 and remains.

**Improvement Path:**

Add a code comment noting that the `delta = 0.30 * baseline.std()` formulation is an approximation of a Cohen's r=0.30 effect and that the simulation result should be interpreted accordingly.

---

### Evidence Quality (0.92/1.00)

**Evidence:**

All 8 external references are present with DOIs/ISBNs/URLs. The inline citation index maps all 8 references to the sections that cite them. Cohen (1988) and scipy (2024) are properly cited within the D.1 power analysis. The LLMORPH citation in the References section is correctly identified as ASE 2024.

**Remaining gaps:**

1. **ASE 2025 body text citation remains uncorrected.** Line 300 introduces LLMORPH with "LLMORPH (ASE 2025, 560K tests, 8.6% false positive rate)." The References section correctly cites ASE 2024 (Deng et al., DOI: 10.1145/3691620.3695058). The iter3 score report stated this was resolved, but the C.0 body text was not corrected. A reader encountering this document without consulting the References section will see an incorrect conference year for the primary supporting evidence cited at C.0. This is a verifiable factual error in an evidence citation.

2. **B.5 std dev derivation not shown.** The 0.02-0.04 std dev range in B.5 is "derived from LLMORPH's 8.6% false positive rate baseline" — the mathematical connection from FPR to std dev range is asserted but not computed. This has been present since iter1.

3. **ICML 2025 position paper substituted.** The NeurIPS 2023 MT-Bench paper (Zheng et al.) is a reasonable foundational substitute, but it is acknowledged as not equivalent to the ADR-001 Force F-2 citation.

**Improvement Path:**

Correct C.0 body text: change "ASE 2025" to "ASE 2024" with citation [5]. Add a one-sentence derivation linking LLMORPH's 8.6% FPR to the 0.02-0.04 std dev range, or label it explicitly as a community convention.

---

### Actionability (0.93/1.00)

**Evidence:**

All iter3 actionability strengths are retained:
- JSON Schema Draft 2020-12 for all 4 contract types with `additionalProperties: false`
- Pseudocode violation conditions in all 25 MR entries
- Python code examples in D.1, D.2, D.3, D.6
- Regression report JSON schema with field names and sample values
- Mode-specific const arrays in schema enforcing classification compatibility
- adv-scorer special considerations with calibration artifact specification

Section G (iter4 addition) is a traceability matrix — it does not add or subtract from actionability.

**Remaining gaps:**

1. **Test artifact directories not stubbed.** `implementation_path: "contracts/test-artifacts/adv-scorer/"` references a non-existent path.

2. **Fisher's method not machine-readable.** No per-agent YAML field encodes the C.6 aggregation logic.

3. **Power simulation delta approximation uncaveated.** The `delta = 0.30 * baseline.std()` formulation in the simulation code is an approximation of Cohen's r=0.30 without a clarifying comment.

**Improvement Path:**

Stub test artifact directories with placeholder README files. Add `fisher_aggregation_method` field to the regression-threshold schema. Add code comment to power simulation noting the delta approximation.

---

### Traceability (0.93/1.00)

**Evidence:**

Section G substantially resolves the primary traceability gap identified in iter3:

1. **G.1 Forward trace:** 20 contract-section rows, each mapping to requirement IDs with rationale. Coverage spans all major sections A through D. All cited FR/NFR IDs verified as existing in harness-requirements.md.

2. **G.2 Reverse trace:** 22 requirement IDs mapped back to contract sections. Infrastructure requirements (FR-001, FR-004) are explicitly acknowledged as not covered by behavioral contracts with explanation.

3. **G.3 Coverage assessment:** 4-section table with orphan risk assessment. Explicit enumeration of 15 requirements not covered by behavioral contracts (FR-001, FR-002 partial, FR-003, FR-004, FR-006, FR-009 partial, FR-019, FR-022, FR-023, FR-024, FR-025, FR-026, FR-027, FR-029, FR-030, NFR-001, NFR-003, NFR-004, NFR-005) with rationale that these are harness infrastructure requirements.

4. **All 25 MR `related_failure_modes` populated** (retained from iter2).

5. **k=13 traceability chain** intact: per-agent YAML → master D.3 → schema.

6. **Jerry Constitution references** resolved (retained from iter3).

**Remaining gaps:**

1. **G.1 A.7 row contains a factual error.** FR-022/FR-023 are listed as "Requirement IDs Enforced" by constitutional invariants, contradicting G.3's correct identification of them as not covered. This reduces traceability accuracy in the section most meant to document coverage.

2. **FM inline comments lack ADR-001 section numbers.** References to FM-003, FM-009 etc. do not cite the ADR-001 section where each FM is defined.

3. **Master B.3 adv-scorer gap asymmetry not traced.** The adv-scorer's floor - 0.03 deviation from the standard floor - 0.04 is not documented in the master B.3 table.

**Improvement Path:**

Correct G.1 A.7 row: remove FR-022/FR-023 from "Requirement IDs Enforced." Add ADR-001 section references to FM inline comments. Add B.3 footnote for adv-scorer floor gap.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Internal Consistency | 0.94 | 0.96 | Correct G.1 A.7 row: remove FR-022/FR-023 from "Requirement IDs Enforced" — these are infrastructure requirements explicitly listed as not covered by G.3. Correct C.0 body text line 300: change "ASE 2025" to "ASE 2024" with citation [5] to match the References section. Both are single-line corrections. (+0.002 composite if IC reaches 0.96) |
| 2 | Evidence Quality | 0.92 | 0.94 | Fix C.0 "ASE 2025" body text (same edit as Priority 1). Add B.5 std dev derivation sentence linking LLMORPH 8.6% FPR to 0.02-0.04 std dev range, or explicitly label as community convention. (+0.003 composite if EQ reaches 0.94) |
| 3 | Traceability | 0.93 | 0.95 | Fix G.1 A.7 FR-022/FR-023 error (same as Priority 1). Add ADR-001 section references to FM inline comments (e.g., "FM-003 (ADR-001 §5.2)"). Add B.3 footnote documenting adv-scorer floor - 0.03 deviation. |
| 4 | Completeness | 0.94 | 0.95 | Add `fisher_aggregation_method: "fishers_combined_p"` field to regression-threshold schema. Stub test artifact directories with placeholder README files. |
| 5 | Actionability | 0.93 | 0.95 | Add clarifying comment to power simulation `delta = 0.30 * baseline.std()` noting the approximation. Implement Priority 4 items. |

**Minimum fix to reach C4 threshold of 0.94:**

Priority 1 edits alone (two single-line corrections) would raise Internal Consistency from 0.94 to 0.96 and Evidence Quality from 0.92 to 0.93:
- New IC: 0.96 × 0.20 = 0.1920 (was 0.1880, +0.004)
- New EQ: 0.93 × 0.15 = 0.1395 (was 0.1380, +0.0015)
- New composite: 0.9385 + 0.004 + 0.0015 = 0.9440 → PASS

The entire gap (0.001 below C4 threshold) can be closed by correcting the G.1 A.7 FR-022/FR-023 error and the C.0 "ASE 2025" body text — two single-line edits.

---

## Iter3 Fix Retention Check

All three iter3 fixes remain intact:
- Jerry Constitution phantom reference eliminated: A.7 correctly references `docs/governance/JERRY_CONSTITUTION.md` and `.context/rules/quality-enforcement.md`
- Formal N=30 power analysis derivation: Section D.1 block fully present with H0/H1, Z values, formula, scipy simulation
- Full bibliographic references: 8 references with DOI/ISBN/URL, inline citation index present

All three iter2 fixes remain intact:
- k=13 consistent across master, schema, and all 5 per-agent contracts
- QUALITY_FLOOR_BREACH scope: absent from Standard mode const array in schema, D.5 scope paragraph present
- All 25 MR `related_failure_modes` entries populated

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite; Methodological Rigor raised from 0.95 to 0.96 independent of other dimensions based on Fix 2 evidence
- [x] Evidence documented for each score with specific section references, line numbers, and exact quotes cited
- [x] Uncertain scores resolved downward: Internal Consistency scored 0.94 (not 0.96) because two specific contradictions were identified; Evidence Quality scored 0.92 (not 0.93) because the ASE year correction was claimed in iter3 as resolved but is verifiably uncorrected
- [x] Calibration check: 0.939 composite for a fourth-iteration C4 deliverable that has resolved 7 of 9 previously-identified gaps is appropriate; two residual gaps are precisely documented
- [x] No dimension scored above 0.96 without exceptional evidence: Methodological Rigor (0.96) is justified by a complete, independently verifiable power analysis chain with no remaining derivation gaps
- [x] Anchor avoidance: Prior score of 0.938 (iter3 verified arithmetic) was read for context only. Internal Consistency was scored lower (0.94) than iter3 (0.96) based on independent evidence of two contradictions — not anchored to prior score
- [x] Rubric applied literally: 0.9+ for Internal Consistency requires "No contradictions, all claims aligned" — two specific contradictions disqualify 0.95+; 0.94 reflects near-excellent execution with two identified contradictions that are minor in context but real
- [x] First-draft calibration: This is iteration 4 of a C4 deliverable; 0.939 is appropriate for a document this close to the threshold
- [x] ASE 2025 body text: Independently verified at line 300 of behavioral-contracts.md — the claim in iter3 that this was resolved is factually incorrect; the correction was applied only in the References section, not in the body text

---

## Score Composite Arithmetic (Verified)

```
Completeness:         0.94 × 0.20 = 0.18800
Internal Consistency: 0.94 × 0.20 = 0.18800
Methodological Rigor: 0.96 × 0.20 = 0.19200
Evidence Quality:     0.92 × 0.15 = 0.13800
Actionability:        0.93 × 0.15 = 0.13950
Traceability:         0.93 × 0.10 = 0.09300
                                    -------
SUM (unrounded):                    0.93850
REPORTED COMPOSITE:                 0.939
C4 THRESHOLD:                       0.940
GAP:                                -0.001
```

**VERDICT: REVISE** | **Composite: 0.939** | **Gap to C4 threshold: 0.001**

The deliverable passes the standard H-13 threshold (0.92) by 0.019 points. It is 0.001 below the C4-specific threshold (0.94). Two single-line corrections close the gap entirely: (1) correct G.1 A.7 to remove FR-022/FR-023 from "Requirement IDs Enforced," and (2) correct C.0 body text from "ASE 2025" to "ASE 2024" with citation [5].

---

## Session Context Schema (for orchestrator)

```yaml
verdict: REVISE
composite_score: 0.939
threshold: 0.94
weakest_dimension: evidence_quality
weakest_score: 0.92
critical_findings_count: 0
iteration: 4
delta_from_iter3: +0.001
improvement_recommendations:
  - "Correct G.1 A.7 row: remove FR-022/FR-023 from Requirement IDs Enforced — these are infrastructure requirements contradicted by G.3 coverage assessment (Internal Consistency: 0.94 -> 0.96, +0.004 composite)"
  - "Correct C.0 body text line 300: change 'ASE 2025' to 'ASE 2024 [5]' — correction was claimed in iter3 but body text was not updated (Evidence Quality: 0.92 -> 0.93, +0.0015 composite)"
  - "Together these two single-line edits close the 0.001 gap to the C4 threshold of 0.940"
  - "Add B.5 std dev derivation linking LLMORPH 8.6% FPR to 0.02-0.04 std dev range or label as community convention (Evidence Quality further improvement)"
  - "Add ADR-001 section references to FM inline comments; add B.3 footnote for adv-scorer floor gap deviation (Traceability further improvement)"
note: >
  All four iter3 and iter4 fixes are present: Jerry Constitution resolved, power analysis with N_min
  bridge, full bibliography, and Section G traceability matrix. Two precision defects prevent crossing
  the C4 threshold: (1) G.1 A.7 lists FR-022/FR-023 as enforced by behavioral contracts while G.3
  correctly lists them as not covered — a direct contradiction introduced in iter4; (2) C.0 body
  text still reads ASE 2025 despite the iter3 report claiming this was resolved. Both are single-line
  corrections with no architectural impact. The substantive content is complete and rigorous.
```
