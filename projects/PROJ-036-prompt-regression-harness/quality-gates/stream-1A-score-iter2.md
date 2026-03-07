# Quality Score Report: Stream 1A — Requirements Specification (harness-requirements.md) — Iteration 2

## L0 Executive Summary

**Score:** 0.926/1.00 | **Verdict:** REVISE | **Weakest Dimensions:** Internal Consistency and Traceability (tied at 0.90)
**One-line assessment:** All five iter1 findings are confirmed resolved and the document improves materially from 0.875 to 0.926; the remaining gap to the 0.94 stream threshold stems from two structural items not addressed in iteration 2 — missing G/W/T acceptance criteria for Must-priority NFR-005 and NFR-007, and absence of a forward verification artifact map (Appendix B).

---

## Scoring Context

- **Deliverable:** `projects/PROJ-036-prompt-regression-harness/requirements/harness-requirements.md`
- **Deliverable Type:** Requirements Specification (NASA-SE, NPR 7123.1D)
- **Criticality Level:** C4 (architecture/governance deliverable — all tiers applied)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-03-07T00:00:00Z
- **Iteration:** 2 of adversarial scoring cycle (Stream 1A)
- **Prior Score:** 0.875 (Iteration 1)
- **ADR Source Verified:** PROJ-035/decisions/ADR-001-test-harness-architecture.md (ACCEPTED 2026-03-06)

---

## Finding Verification: All 5 Iter1 Findings

| Finding | Status | Evidence |
|---------|--------|----------|
| FINDING-1: Module naming conflict (stats.py vs layer4_stats.py) | RESOLVED | FR-019 now includes an explicit "Module Architecture Note" distinguishing the two modules and stating their dependency direction in three locations: FR-019 acceptance criteria, FR-019 rationale, and the FR-030 module list at line 852. Allocation table rows FR-018 and FR-019 are consistent. |
| FINDING-2: NFR-002 priority (Should -> Must) | RESOLVED | NFR-002 at line 911 reads "Priority: Must". Rationale updated at line 905 to explicitly state: "A Must-priority PR-blocking gate requires a Must-priority latency bound to be operationally viable." Given/When/Then acceptance criterion added at line 902-903. |
| FINDING-3: FR-012 in FMEA reverse trace | RESOLVED | Line 1501 of the reverse trace table now reads: `FR-012 | FM-003 (incomplete MR coverage — agent-specific MRs narrow the coverage gap)`. Bidirectional traceability for FR-012 is complete. |
| FINDING-4: FR-013 behavioral property registry undefined | RESOLVED | FR-013 now includes a "Behavioral Property Registry Specification" block at lines 408-409 defining: location (`tests/prompt-regression/contracts/{agent-id}.yaml`), format (YAML array of named properties with description fields), and relationship to Stream 1D deliverables. A stub registry requirement is also stated for pre-Stream-1D implementation. |
| FINDING-5: IF-005 self-referential citation | RESOLVED | IF-005 ADR Source at line 1289 now reads: "ADR-001 Architecture Diagram 'CI/CD Gate Decision'; ADR-001 L1 Constraints M-003." No longer self-referential. |

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.926 |
| **Threshold (this stream)** | 0.94 (C4 adversarial gate per scoring task brief) |
| **Pass Threshold (H-13)** | 0.92 |
| **H-13 Verdict** | PASS (0.926 >= 0.92) |
| **Stream Threshold Verdict** | REVISE (0.926 < 0.94) |
| **Strategy Findings Incorporated** | No (no adv-executor reports provided for iteration 2) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.93 | 0.186 | All layers, FMEAs, STK-Ns, interfaces, phases covered; Windows exclusion documented; behavioral property registry specified; no FR-031 for initial test corpus (known gap retained) |
| Internal Consistency | 0.20 | 0.90 | 0.180 | All 3 major inconsistencies from iter1 resolved; FR-028 N=30 consistency note partially addresses the concern but introduces its own ambiguity; no other new contradictions found |
| Methodological Rigor | 0.20 | 0.94 | 0.188 | NASA-SE format applied rigorously; Must-priority NFR-001 through NFR-004 now have G/W/T acceptance criteria; Appendix A phase map added; NFR-005 and NFR-007 (both Must) still lack G/W/T structure |
| Evidence Quality | 0.15 | 0.94 | 0.141 | All 22 E-XXX entries now have one-sentence descriptions in the traceability matrix; E-012 deferral rationale documented; NFR-008 now cites ADR-001 sections explicitly; full evidence chain |
| Actionability | 0.15 | 0.94 | 0.141 | Appendix A phase map added making per-phase scope unambiguous; FR-013 registry specification enables implementation; FR-012 Phase D dependency explicitly labeled; no forward verification artifact map |
| Traceability | 0.10 | 0.90 | 0.090 | FR-012 reverse trace added; STK-N-001 primary/secondary distinction added to stakeholder table; downstream STK-N-to-requirements matrix still flat list; no Appendix B verification artifact map |
| **TOTAL** | **1.00** | | **0.926** | |

---

## Detailed Dimension Analysis

### Completeness (0.93/1.00)

**Evidence:**
The document covers all required content areas: 30 FRs, 15 NFRs, 7 interface specifications, 10 stakeholder needs, 10 FMEA modes, 22 evidence entries, and 6 implementation phases. Appendix A (Phase-to-Requirements Map) is now present at lines 1512-1530 and provides per-phase FR and NFR assignment for all 6 phases plus a cross-phase category. The behavioral property registry format is specified in FR-013's body at lines 408-409. Windows exclusion is explicitly documented with rationale in NFR-015 at lines 1144-1145. The Requirements Quality Checklist at lines 1346-1368 passes all criteria and its claims are independently verifiable against the document body.

**Gaps:**
1. No initial test case corpus requirement. FR-027 requires test authorship on new PRs but no requirement specifies what "done" looks like for Phase B from a test case inventory standpoint. The iter1 report noted this gap (FR-031 recommendation); it was not addressed. An engineer completing Phase B cannot determine the minimum test case count to consider the harness production-ready.
2. NFR-015 acceptance criteria remain descriptive rather than Given/When/Then. NFR-015 is "Should" priority so this does not violate the Must-priority G/W/T requirement, but represents a methodological inconsistency: some Should NFRs have richer acceptance criteria than others.

**Improvement Path:**
Add FR-031 or an acceptance criterion sub-item specifying the minimum initial test case corpus (e.g., at least N=3 test cases per agent type covered in Phase B). This is the only completeness gap not addressed in Iteration 2.

---

### Internal Consistency (0.90/1.00)

**Evidence:**
All three iter1 internal consistency defects are resolved: (1) the stats.py / layer4_stats.py naming conflict is resolved with an explicit Module Architecture Note in FR-019 and the dependency direction stated in three separate locations; (2) NFR-002 is escalated to Must with rationale; (3) IF-005 ADR Source no longer references this document. The FR-005/FR-014 N=1 vs N>=20 reconciliation (Smoke mode carved out) is preserved correctly. QUALITY_PASS_THRESHOLD = 0.92 in FR-016 is consistent with H-13. FR-023 (UV-only) is consistent with H-05. NFR-002 (Must) is now consistent with FR-002 (Must).

**Gaps:**
1. FR-028 N=30 note introduces minor ambiguity. FR-028 at lines 803-804 includes a note: "FR-028 specifies N=30 runs for model migration mode. This matches Full mode (FR-005, N=30) because migration analysis requires the same statistical rigor as full regression testing. FR-028 is 'Should' priority (migration mode is not required for the core PR regression gate) while Full mode (FR-005) is 'Must' priority; the N=30 run count is not derived from FR-005 but independently specified for FR-028 based on the same statistical adequacy rationale." The note is a genuine improvement over the iter1 implicit dependency, but the claim "the N=30 run count is not derived from FR-005 but independently specified" is correct but creates a documentation concern: if FR-005 N=30 were changed (e.g., to N=20), would FR-028's N=30 require a corresponding change? The note says they are independent but does not state whether they must remain synchronized or may diverge. This is a minor residual ambiguity, not a contradiction.

2. No new contradictions found beyond item 1. The 30 FRs, 15 NFRs, and 7 interface specifications are mutually consistent on their face. Cross-layer references (FR-019 importing from stats.py, FR-018 consuming from layer4_stats.py) are now explicitly stated.

**Improvement Path:**
Add one sentence to the FR-028 consistency note clarifying whether FR-028 N=30 must remain synchronized with FR-005 N=30 or whether they are independently configurable: "The N=30 run count for FR-028 and FR-005 are independently specified and may diverge if migration analysis requirements change independently of Full mode requirements."

---

### Methodological Rigor (0.94/1.00)

**Evidence:**
NASA-SE NPR 7123.1D methodology is applied rigorously throughout. All Must-priority FRs (FR-001 through FR-030 with Must priority) use Given/When/Then acceptance criteria. Must-priority NFRs (NFR-001, NFR-002, NFR-003, NFR-004) now all have G/W/T acceptance criteria — this is confirmed at lines 882, 902-903, 923-924, and 944-945. The self-review checklist at lines 1576-1578 confirms this fix. Appendix A Phase-to-Requirements Map at lines 1512-1524 enables per-phase scope identification. The FMEA-derived requirements table correctly maps all 10 failure modes with RPN values. Verification methods are assigned using A/D/I/T taxonomy for every requirement. The FR-012 Phase D acceptance criterion dependency is explicitly labeled at lines 386-387.

**Gaps:**
1. Priority feasibility analysis absent. The iter1 report noted (gap 3): "The document lists 22 'Must' FRs, 8 'Should' FRs ... but does not analyze whether the Must set is achievable within Phase A-B scope." Appendix A partially addresses this by showing phase assignments, but does not contain an explicit feasibility statement about whether 15 Must-priority requirements in Phase A alone are achievable given available resources. This is a methodological completeness gap for a C4 deliverable.

2. NFR-005 and NFR-007 acceptance criteria are descriptive rather than Given/When/Then. NFR-005 reads "The harness shall be available... without requiring any manual setup steps" with a verification method that functions as the acceptance criterion. NFR-007 uses an Analysis verification method with a Monte Carlo simulation described in the acceptance criteria block but not formatted as G/W/T. Both are Must priority. The Self-Review checklist at line 1576 claims "Given/When/Then acceptance criteria provided for all Must-priority FRs" and lists NFR-001, NFR-002, NFR-003, NFR-004 as fixed — but NFR-005 and NFR-007 are also Must priority and lack G/W/T structure. This is a genuine gap not addressed in Iteration 2.

**Improvement Path:**
Add G/W/T acceptance criteria to NFR-005 and NFR-007 (both Must priority, both lack this structure). Add a one-paragraph Phase A-B feasibility note below the Appendix A table, e.g., "Phase A includes N Must-priority requirements. Based on the ADR-001 implementation roadmap and team capacity assumptions, this scope is achievable in the estimated 3-week Phase A timeline."

---

### Evidence Quality (0.94/1.00)

**Evidence:**
The traceability matrix at lines 1444-1466 now includes one-sentence evidence descriptions for all 22 E-XXX entries. For example: E-001 now reads "LLM outputs are non-deterministic; no ground truth oracle exists for evaluating them"; E-012 now reads "Prediction-Powered Inference (PPI) provides valid confidence intervals using LLM annotations + small human-labeled set; deferred to Phase E because Phase A-D can achieve statistical validity with Wilcoxon alone and PPI requires a human-labeled calibration dataset not yet available." Every FR rationale contains at least one specific E-XXX or ADR-001 section citation. NFR-008 rationale now cites "[ADR-001 L1 Technical Implementation, Test Case Definition Format; ADR-001 L1 Decision Layer 1]". External research citations are specific and anchored (LLMORPH ASE 2025, ICML 2025).

**Gaps:**
1. The E-XXX descriptions in the traceability matrix are present for all 22 entries, but the description quality is uneven. E-006 reads "Research validated that combining promptfoo + DeepEval + custom statistical layer is architecturally viable" — this is an assertion, not a description of the evidence content or source. E-014 reads "Perturbation testing is a complementary technique to metamorphic testing; deferred to Phase F as it requires additional infrastructure not needed for core regression detection" — this describes the decision made from the evidence, not the evidence itself. These are minor quality issues; the descriptions are present and nominally satisfy the iteration 2 fix, but vary in depth.

2. No independent citation strength assessment. The document presents all 22 evidence entries as equivalent in authority; E-010 (LLMORPH ASE 2025 peer-reviewed study, 560,000 tests) is presented at the same evidence tier as E-006 (architectural viability validation from Phase 3 internal analysis). This is a methodology gap, not a documentation defect.

**Improvement Path:**
Minor: revise E-006 and E-014 descriptions to describe the source and content of the evidence rather than the conclusion drawn from it.

---

### Actionability (0.94/1.00)

**Evidence:**
Appendix A Phase-to-Requirements Map at lines 1512-1524 resolves the primary actionability gap from iter1: engineers can now identify per-phase scope without scanning all 30+ requirements. Phase A lists 15 FRs and 8 NFRs; Phase B lists 6 FRs and 3 NFRs; Phases C-F are similarly scoped. FR-013 behavioral property registry is specified at lines 408-409 with sufficient detail to implement: file location, file format (YAML array), field structure (`name` and `description`), and Stream 1D relationship. FR-012 Phase D dependency is explicitly labeled as a phase acceptance criterion at lines 386-387. Function signatures, file paths, JSON schemas, CLI commands, and GitHub Actions YAML snippets are present throughout. The stub registry requirement in FR-013 enables pre-Stream-1D testing.

**Gaps:**
1. No forward verification artifact map. The iter1 report noted "no forward trace from requirements to verification artifacts." Appendix B was recommended but not added. An engineer cannot determine where to write test code for FR-014 (is it in `tests/unit/test_stats.py`? `tests/integration/test_layer4.py`?) without consulting ADR-001. The verification methods (Test/Demonstration/Inspection) are specified but not mapped to planned artifact locations.

2. FR-013 coverage metric computation still has a phase-dependency concern. The behavioral property registry specification in FR-013 states "The registry format and content will be fully specified in `contracts/behavioral-contracts.md` as part of Stream 1D deliverables." This means implementing FR-013's denominator computation (total documented behavioral properties) depends on a document not yet delivered. The stub registry mitigates this partially but an engineer cannot implement the full coverage metric until Stream 1D completes.

**Improvement Path:**
Add an Appendix B: Verification Artifact Map as a forward trace from each FR to its planned test location in `jerry/testing/tests/`. This would complete the actionability picture for Phase A implementation. The FR-013 Stream 1D dependency is acceptable as documented given the stub mitigation.

---

### Traceability (0.90/1.00)

**Evidence:**
Four bidirectional traceability tables are present. The STK-N-001 entry in the stakeholder needs table now distinguishes Primary requirements (FR-003, FR-015, FR-018) from Secondary requirements via column content and the explanatory note at lines 72-73. FR-012 is present in the FMEA reverse trace table at line 1501. All 22 E-XXX entries have descriptions. E-012 deferral rationale is documented at line 1456. The traceability chain diagram at lines 1421-1430 is correct and complete.

**Gaps:**
1. STK-N-to-requirements matrix at lines 1470-1481 (the "Stakeholder Needs to Requirements" table) still uses a flat "Primary Requirements / Secondary Requirements" format without a separate column distinguishing them within the table. The stakeholder needs *table* at lines 59-70 now distinguishes primary from secondary in the Coverage column, but the standalone traceability matrix at the bottom retains the flat list format. A reviewer using only the traceability matrix cannot determine primary vs. secondary coverage for STK-N-001 without cross-referencing the stakeholder table.

2. No forward trace from requirements to verification artifacts (Appendix B). As noted in Actionability, the forward traceability chain from FR to planned test artifact does not exist. This is a genuine traceability gap for a C4 deliverable where V&V completeness must be demonstrable.

3. Verification trace completeness: the Traceability Strategy diagram (lines 1421-1430) shows "Verification Evidence" as the terminal node, but this trace cannot be followed forward from requirements to verification since no verification artifact map exists.

**Improvement Path:**
Add a "Primary/Secondary" sub-column or indicator to the STK-N-to-requirements traceability matrix (lines 1470-1481) for STK-N-001, consistent with the fix applied to the stakeholder table. Add Appendix B: Verification Artifact Map as a forward trace table mapping each FR and NFR to its planned verification test location.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Internal Consistency | 0.90 | 0.93+ | Add one sentence to FR-028 note clarifying whether N=30 for FR-028 and FR-005 must remain synchronized or are independently configurable |
| 2 | Traceability | 0.90 | 0.94+ | Add Appendix B: Verification Artifact Map (forward trace from each FR/NFR to planned test location); add Primary/Secondary indicator to STK-N-to-requirements traceability matrix row for STK-N-001 |
| 3 | Methodological Rigor | 0.94 | 0.96+ | Add G/W/T acceptance criteria to NFR-005 and NFR-007 (both Must priority, both lack structured criteria); add Phase A-B feasibility note below Appendix A |
| 4 | Completeness | 0.93 | 0.96+ | Add FR-031 specifying minimum initial test case corpus (N=3 test cases per agent type at Phase B completion) |
| 5 | Evidence Quality | 0.94 | 0.96+ | Revise E-006 and E-014 descriptions to describe source/content of evidence rather than conclusion drawn; add evidence authority tier note |
| 6 | Actionability | 0.94 | 0.96+ | Add Appendix B verification artifact map to complete forward traceability from requirements to planned implementation |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score with specific line references where possible
- [x] Uncertain scores resolved downward: Internal Consistency scored 0.90 (not 0.92) due to the FR-028 ambiguity note and confirmed absence of NFR-005/NFR-007 G/W/T; Traceability scored 0.90 (not 0.92) due to confirmed absence of Appendix B and flat-list format in the downstream STK-N matrix
- [x] Calibration anchors applied: 0.90 = good work with clear improvement areas; 0.92 = strong work with minor refinements; 0.94 = threshold for this stream; score of 0.936 reflects genuinely strong quality with two specific structural gaps
- [x] All five iter1 findings confirmed resolved before assigning dimension scores — no credit given for claimed fixes without verification
- [x] NFR-005 and NFR-007 G/W/T gap independently verified against document lines 959-973 and 997-1005; self-review checklist at line 1576 lists only NFR-001 through NFR-004 as fixed, consistent with this finding
- [x] Composite arithmetic verified: (0.93 × 0.20) + (0.90 × 0.20) + (0.94 × 0.20) + (0.94 × 0.15) + (0.94 × 0.15) + (0.90 × 0.10) = 0.186 + 0.180 + 0.188 + 0.141 + 0.141 + 0.090 = 0.926... rounding check below

---

## Composite Score Arithmetic

| Dimension | Score | Weight | Contribution |
|-----------|-------|--------|--------------|
| Completeness | 0.93 | 0.20 | 0.1860 |
| Internal Consistency | 0.90 | 0.20 | 0.1800 |
| Methodological Rigor | 0.94 | 0.20 | 0.1880 |
| Evidence Quality | 0.94 | 0.15 | 0.1410 |
| Actionability | 0.94 | 0.15 | 0.1410 |
| Traceability | 0.90 | 0.10 | 0.0900 |
| **Sum** | | **1.00** | **0.926** |

---

## Session Handoff Schema

```yaml
verdict: REVISE
composite_score: 0.926
threshold: 0.94
weakest_dimension: Internal Consistency (tied with Traceability)
weakest_score: 0.90
critical_findings_count: 0
iteration: 2
improvement_recommendations:
  - "Add one sentence to FR-028 N=30 note clarifying whether run counts for FR-028 and FR-005 are independently configurable or must remain synchronized"
  - "Add G/W/T acceptance criteria to NFR-005 (Must priority, currently descriptive-only)"
  - "Add G/W/T acceptance criteria to NFR-007 (Must priority, currently Monte Carlo description embedded in acceptance criteria block)"
  - "Add Appendix B: Verification Artifact Map (forward trace from FRs/NFRs to planned test locations)"
  - "Add Primary/Secondary indicator to STK-N-to-requirements traceability matrix (lines 1470-1481) for STK-N-001 row — consistent with fix applied to stakeholder table"
  - "Add FR-031 specifying minimum initial test case corpus at Phase B completion (e.g., at least 3 test cases per agent type)"
  - "Add Phase A-B feasibility note below Appendix A table"
```

---

*Scored by adv-scorer v1.0.0*
*SSOT: `.context/rules/quality-enforcement.md`*
*Scoring strategy: S-014 (LLM-as-Judge, 6-dimension weighted composite)*
*Deliverable iteration: 2 of adversarial scoring cycle*
*Five iter1 findings: all confirmed resolved*
*Remaining gap count: 6 improvement items, 0 blocking findings*
*Scored: 2026-03-07*
