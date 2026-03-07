# Quality Score Report: Engineering Review — FEAT-036-001 Four-Layer Composite Test Harness

## L0 Executive Summary

**Score:** 0.918/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Completeness (0.84)

**One-line assessment:** The engineering review is rigorous for the domains it covers (architecture, code quality, security, CI/CD) but has a material evidence gap: the compliance matrix substantiates only 16 of the claimed 27 verified FRs, and FR-006 through FR-009, FR-011, FR-022–024, FR-027, FR-029–030 receive no independent evidence within the deliverable, lowering Completeness below threshold. Targeted expansion of the compliance matrix to cover all 30 FRs would close the primary gap.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-036-prompt-regression-harness/reviews/engineering-review.md`
- **Deliverable Type:** Analysis (Engineering Review)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Quality Threshold:** 0.94 (user-specified, exceeds H-13 minimum of 0.92)
- **Iteration:** 1
- **Prior Score:** N/A (first independent scoring)
- **Reviewer Self-Score:** 0.948
- **Scored:** 2026-03-07T00:00:00Z

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.918 |
| **Threshold** | 0.94 |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No — deliverable scored directly from content and cross-referenced documents |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.84 | 0.168 | Compliance matrix covers 16/30 FRs with evidence; 11 FRs absent; FR-026 PARTIAL but FR is Must-priority |
| Internal Consistency | 0.20 | 0.94 | 0.188 | Very minor inconsistencies (CQ-02 duplication, CQ-03 formula divergence); exit-code mapping discrepancy CICD-03 unexplained |
| Methodological Rigor | 0.20 | 0.95 | 0.190 | Systematic per-area review with tabular evidence; NIST SSDF methodology cited; spot-check sampling explicit |
| Evidence Quality | 0.15 | 0.93 | 0.1395 | Strong file:line citations where present; Traceability row's "FR-001 through FR-027 in VCRM" is an external document reference, not within-deliverable evidence |
| Actionability | 0.15 | 0.94 | 0.141 | All 11 findings have severity, owner, remediation; 3 recommendations lack target dates or acceptance criteria |
| Traceability | 0.10 | 0.91 | 0.091 | H-rules traceable; FR-028 verified in narrative but absent from compliance matrix; 11 FRs have no compliance row at all |
| **TOTAL** | **1.00** | | **0.9175** | |

**Rounded composite: 0.918**

---

## Detailed Dimension Analysis

### Completeness (0.84/1.00)

**Evidence for score:**

The deliverable covers 7 review areas (L1.1–L1.7) and claims "24/27 FRs verified PASS" in the S-014 Completeness row. Cross-referencing the compliance matrix against the requirements specification reveals:

FRs explicitly verified with evidence in the compliance matrix:
FR-001, FR-002, FR-003, FR-004, FR-005, FR-010, FR-014, FR-015, FR-016, FR-017, FR-018, FR-019, FR-020, FR-021, FR-025 (15 FRs via compliance table).
FR-028 verified via CI/CD section narrative (1 additional FR).
Total with within-deliverable evidence: **16 FRs**.

FRs absent from the compliance matrix with no independent within-deliverable evidence:
- FR-006, FR-007, FR-008, FR-009 (Layer 2: DeepEval evaluation backend — 4 MUST-priority FRs)
- FR-011 (MR calibration — SHOULD priority)
- FR-022, FR-023, FR-024 (observability, baseline CLI, history persistence — SHOULD/MUST)
- FR-027 (test case authorship PR checklist — MUST priority)
- FR-029, FR-030 (trend persistence, layer extensibility — SHOULD/MUST)

Total absent from compliance matrix: **11 FRs** (including at least 3 Must-priority ones: FR-027, FR-030, and potentially FR-022/FR-023).

The "24/27" claim in the Completeness row is not substantiated by evidence within the deliverable. The VCRM citation ("FR-001 through FR-027 traced to implementation files in VCRM") defers verification to an external document, which does not count as within-review evidence under the S-014 rubric.

FR-026 is Must-priority per the requirements specification. Its PARTIAL status (deepeval absent from pyproject.toml) means a Must-priority acceptance criterion (pinned version in uv.lock) is unmet. The review correctly identifies this but the compliance matrix rows for FR-006–FR-009 (the Layer 2 DeepEval backend FRs) are entirely absent — a significant gap given that Layer 2 covers FR-006 through FR-009 and FR-021 (only FR-021 appears).

H-20 is correctly scored CONDITIONAL. All 7 H-rules checked are present with evidence (H-05, H-07, H-10, H-11, H-13, H-20, H-23). NFRs are entirely absent from the compliance matrix — none of NFR-001 through NFR-015 appear, which is a gap given this is a C4 review.

**Gaps:**
- 11 FRs have no compliance matrix row and no within-deliverable verification evidence
- The "24/27 FRs verified PASS" claim is overstated relative to the within-deliverable evidence
- NFRs entirely absent from compliance matrix (NFR-001 through NFR-015)
- FR-027 (MUST-priority, test case authorship enforcement) has no compliance row

**Improvement path:**
Expand compliance matrix to cover all 30 FRs and at least the Must-priority NFRs. For each absent FR, either add a compliance row with evidence or explicitly note "not yet implemented" with the implementation phase. The self-claimed 0.92 score for completeness is generous given the 11 absent FRs — 0.84 reflects the gap more accurately.

---

### Internal Consistency (0.94/1.00)

**Evidence:**

The review is largely internally consistent. Architecture findings in L1.1 align with the compliance matrix H-07/H-10 rows. Code quality findings in L1.2 align with CQ-01/CQ-02/CQ-03 tracker entries. Test coverage findings in L1.4 align with COV-01 through COV-04. Security findings in L1.3 align with SEC-01 through SEC-04.

Minor inconsistencies identified:

1. **CICD-03 and exit code mapping:** The CI/CD section narrative states "Exit code mapping (FR-018): PASS" citing `REGRESSION -> exit 1`, `MARGINAL -> exit 0`. But CICD-03 (LOW finding) notes that the standard workflow maps MARGINAL to exit 0 while `layer4_stats.py._exit_code()` maps MARGINAL to exit 2. This is an inconsistency in the FR-018 PASS verdict — the compliance matrix says PASS but the finding acknowledges that the workflow does not match the module's mapping. The review hedges ("verify this is intentional") but still marks FR-018 PASS without resolving whether the discrepancy is a defect or a documented design decision.

2. **CQ-02 constant duplication acknowledged but Internal Consistency scored 0.96:** The review itself scores Internal Consistency at 0.96, docking 0.04 for CQ-02 and CQ-03. The CICD-03 exit code discrepancy is an additional inconsistency not factored into that score. The review's self-score slightly overestimates this dimension.

3. **Coverage claim:** L0 executive summary lists "four adapter modules" with low coverage (deepeval_adapter.py, reports/generator.py, mr_003_context.py, mr_004_formatting.py, mr_005_roundtrip.py) — that is 5 modules, not four. The text says "Four adapter modules (`deepeval_adapter.py` at 0%, `reports/generator.py` at 14%, `mr_003_context.py` at 36%, `mr_004_formatting.py` at 20%, `mr_005_roundtrip.py` at 38%)" listing five distinct modules. This is a minor internal inconsistency in the executive summary.

**Gaps:**
- FR-018 PASS verdict is in mild tension with CICD-03 finding
- "Four adapter modules" counting error (five are listed)
- CICD-03 left open without a definitive resolution of design intent

**Improvement path:**
Either mark FR-018 as CONDITIONAL in the compliance matrix (matching the actual state) or resolve CICD-03 explicitly as a documented design decision before marking PASS. Fix the adapter count in L0.

---

### Methodological Rigor (0.95/1.00)

**Evidence:**

The review follows a systematic per-area structure with defined review scope for each of the 7 areas. The methodology is explicitly stated: NIST SSDF (RV.1, RV.2, RV.3), S-014 LLM-as-Judge with 6-dimension rubric. Each area includes a status determination (PASS/CONDITIONAL/FAIL), a tabular finding list, and severity-classified findings.

Strengths:
- Architecture compliance section verifies all 11 domain modules and all 6 forbidden dependency patterns
- Security section uses a structured threat model approach (STRIDE, CWE, OWASP) with explicit control mapping
- Test coverage section tabulates per-module coverage numbers with H-20 compliance status
- CI/CD section uses a structured table for workflow correctness across 10 aspects
- Spot-check methodology in Code Quality section is explicit (8 modules, 100% annotation and docstring compliance)
- FR-019 dependency guard is independently verified (AST-based static analysis test cited)

Minor methodological gap:
- The review claims to verify "all source modules" for H-11 but the spot-check table covers 8 of the approximately 16 source modules. The claim "All public function signatures across the reviewed modules include..." implicitly limits the scope to reviewed modules — honest but not a complete audit.
- Property-based testing coverage (Hypothesis) is noted correctly but the reviewer does not independently verify max_examples values match the cited 30-50 range.

**Gaps:**
- Spot-check for H-11 covers 8/~16 modules; the word "All" in the finding header is qualified by "reviewed modules" in the body but the header creates an impression of completeness
- No methodology stated for selection of which 8 modules were spot-checked (risk of cherry-picking high-performers)

**Improvement path:**
State explicitly which modules were selected for spot-check and why (e.g., "one from each architectural layer, plus the two adapter modules with highest public API surface"). This would raise the dimension to 0.97+.

---

### Evidence Quality (0.93/1.00)

**Evidence:**

The deliverable makes extensive use of file:line citations where it has direct knowledge:
- `types.py:245` for CQ-01 (datetime.utcnow)
- `store.py:40` for CQ-02 (constant duplication)
- `stats.py:154` vs `mr_001_paraphrase.py:150` for CQ-03 (Cohen's r)
- `layer4_stats.py:102` for ARCH-01 (lazy import)
- `prompt-regression-full.yml:303`, `prompt-regression-full.yml:437` for CICD findings
- `mr_001_paraphrase.py:150` for INTEG-01

Security control verification is structured with explicit implementation descriptions (e.g., `_validate_score_array()` for CWE-20, `VersionKey` for CWE-22). Prior QG scores (0.956, 0.955, 0.957) are cited as convergence history.

Evidence gap:
- The Traceability dimension row states "FR-001 through FR-027 traced to implementation files in VCRM" but the VCRM is an external document not reproduced within the review. This is a citation to external evidence rather than within-deliverable evidence, which reduces the evidence quality for that claim.
- The "350 tests PASS, 0 failures" claim is asserted without a test run artifact path or timestamp cited. A C4 review should cite a test execution artifact (e.g., `pytest results: 2026-03-07 run at path/to/junit.xml`).
- The "5 agent YAML files confirmed" for FR-001 PASS does not specify which agent YAML files or their paths.

**Gaps:**
- Test execution results cited without an artifact path (just "350 tests PASS")
- FR-001 PASS evidence is vague ("5 agent YAML files confirmed" without naming them)
- 11 FRs have no within-deliverable evidence at all (propagates from Completeness)

**Improvement path:**
Cite the test run output file or CI job URL for the 350-test PASS claim. Name the 5 YAML files for FR-001. The per-finding citations are strong where present and should be maintained.

---

### Actionability (0.94/1.00)

**Evidence:**

All 11 open findings in the tracker have: severity classification, area assignment, finding description, status, owner assignment, and remediation guidance.

Remediation guidance quality:
- COV-01: "Add unit tests for MR-003/004/005 transforms; integration tests for ReportGenerator; resolve deepeval dep" — specific and sequenced
- SEC-01: Specific docker inspect command provided to get the SHA digest — highly actionable
- DEP-01: "Declare deepeval as a pinned optional dependency in test dependency group" — specific
- CQ-01: Exact replacement code provided (`datetime.now(datetime.UTC).isoformat() + "Z"`) — excellent
- CQ-02: "Import QUALITY_PASS_THRESHOLD from stats.py instead of duplicating" — specific

Minor actionability gap:
- No target dates or sprint assignments for any finding — makes prioritization of the 3 MEDIUM findings against each other unclear in practice
- CICD-03 remediation says "Verify this is intentional... If so, document the design decision" — this is a conditional action that defers the decision to the implementer without defining what "documented" means (a code comment? a WORKTRACKER entry? a design doc?)
- The "Conditions for unconditional GO" in L0 does not specify a timeline or success definition for when GO becomes unconditional

**Gaps:**
- No target completion timeline for MEDIUM findings
- CICD-03 remediation is vague ("verify... document")
- GO conditions do not specify definition of done or verification method

**Improvement path:**
Add "Expected resolution: 1 sprint" or equivalent to the 3 MEDIUM findings. Replace the CICD-03 "verify and document" with a specific acceptance criterion (e.g., "Add a comment in `prompt-regression-standard.yml` before the MARGINAL case: `# Design decision: MARGINAL mapped to exit 0 per [decision reference]` ").

---

### Traceability (0.91/1.00)

**Evidence:**

H-rule traceability:
- H-05, H-07, H-10, H-11, H-13, H-20, H-23 all have compliance matrix entries with status and evidence. This is strong H-rule coverage.

FR traceability (as noted in Completeness and Evidence Quality):
- 16 of 30 FRs have compliance matrix rows
- 11 FRs have no compliance row
- The traceability summary claims "FR-001 through FR-027 traced to implementation files in VCRM" — this relies on an external document without reproducing the key traceability facts in the review itself

Security control traceability:
- MC-01 through MC-14 cited: "12/14 IMPLEMENTED, 2 PARTIAL" — but no per-MC breakdown is given in this review; a table would strengthen this
- MC-31, MC-32, MC-33 verified individually in the CI/CD section — good

Behavioral contract traceability:
- 119 testable constraints cited with section-level PASS counts (C: 36/36, D: 24/24, E: 12/12, F: 3/6 universal, 41/41 agent-specific). This matches the constraint-verification.md L0 Executive Summary exactly — confirmed.

Finding-to-H-rule traceability:
- COV-01 is traced to H-20 in the compliance matrix
- SEC-01 traced to MC-08 in the security section
- DEP-01 traced to FR-026 in the dependency section
- CQ-01, CQ-02 are not explicitly traced to an H-rule (H-11 docstrings/type hints doesn't directly cover deprecated APIs or constant duplication — these are coding practice findings, which is appropriate, but a note that "CQ-01 is below HARD-rule level" would be cleaner)

**Gaps:**
- 11 FRs have no compliance row — traceability chain broken for those FRs
- MC-01 through MC-14 cited as 12/14 implemented with no per-MC table in this review
- FR-028 verified in CI/CD narrative but not in the compliance matrix (inconsistent treatment)
- No NFR traceability anywhere in the compliance matrix

**Improvement path:**
Add compliance rows for the 11 absent FRs (even a brief "FR-006: Layer 2 DeepEval metrics — PARTIAL (deepeval dependency absent)"). Add a summary column to the MC table. Move FR-028 into the compliance matrix.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Completeness | 0.84 | 0.92+ | Expand compliance matrix to cover all 30 FRs and at minimum the 6 MUST-priority NFRs. For FR-006–FR-009 (Layer 2 DeepEval), add rows noting PARTIAL status due to deepeval dependency gap. For FR-027 (test case authorship), add evidence of PR template existence. For FR-022, FR-023, add compliance rows. This single change closes the largest scoring gap. |
| 2 | Traceability | 0.91 | 0.95+ | Add compliance rows for the 11 absent FRs. Move FR-028 from CI/CD narrative into the compliance matrix. Add at minimum a summary reference to the MC-01–MC-14 per-control status within this review (not just citing the security-assessment.md). |
| 3 | Internal Consistency | 0.94 | 0.96+ | Resolve CICD-03 explicitly — either mark FR-018 CONDITIONAL in the compliance matrix or add a documented design-decision annotation in the workflow file and reference it here. Fix "four adapter modules" count (five are listed) in the L0 executive summary. |
| 4 | Evidence Quality | 0.93 | 0.96+ | Cite a specific test execution artifact path or CI run URL for the "350 tests PASS" claim. Name the 5 YAML files for FR-001 PASS evidence. For the H-11 spot-check, state selection rationale. |
| 5 | Actionability | 0.94 | 0.96+ | Add expected resolution timeline for the 3 MEDIUM findings. Sharpen CICD-03 remediation from "verify and document" to a specific acceptance criterion. Add definition-of-done to the L0 "Conditions for unconditional GO" items. |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing weighted composite
- [x] Evidence documented for each score (specific sections and cross-references cited)
- [x] Uncertain scores resolved downward (Completeness held at 0.84, not rounded up to 0.87)
- [x] First-draft calibration considered (this is a first independent scoring; reviewer self-score of 0.948 was not adopted)
- [x] No dimension scored above 0.95 without exceptional evidence (Methodological Rigor at 0.95 is the ceiling; justified by explicit NIST SSDF methodology and systematic per-area structure)
- [x] The 0.94 threshold (user-specified, above H-13 minimum of 0.92) was used as the pass bar; the composite of 0.918 does not meet it
- [x] Weighted composite verified: (0.84 × 0.20) + (0.94 × 0.20) + (0.95 × 0.20) + (0.93 × 0.15) + (0.94 × 0.15) + (0.91 × 0.10) = 0.168 + 0.188 + 0.190 + 0.1395 + 0.141 + 0.091 = 0.9175 ≈ **0.918**

---

## Score Delta vs. Self-Score

The reviewer self-assessed 0.948 (PASS). This scoring finds 0.918 (REVISE). The primary driver of the delta is Completeness: the reviewer scored 0.92 while this scoring finds 0.84.

**Reason for delta:** The reviewer treated the VCRM external document as completing the FR verification ("FR-001 through FR-027 traced to implementation files in VCRM"). Under the S-014 rubric, evidence must be within the deliverable for it to count toward the score — citing an external document is traceability, not verification. The 11 FRs absent from the compliance matrix have no independent verification evidence within this review, which is a material gap for a C4 deliverable.

The reviewer's other dimension scores (Internal Consistency 0.96, Methodological Rigor 0.97, Traceability 0.95) were also moderately optimistic. This scoring finds 0.94, 0.95, and 0.91 respectively — consistent with the leniency counteraction directive.

---

## Session Context (Handoff Schema)

```yaml
verdict: REVISE
composite_score: 0.918
threshold: 0.94
weakest_dimension: Completeness
weakest_score: 0.84
critical_findings_count: 0
iteration: 1
improvement_recommendations:
  - "Expand compliance matrix to cover all 30 FRs (11 currently absent); add at minimum FR-006–FR-009, FR-011, FR-022–024, FR-027, FR-029–030"
  - "Move FR-028 from CI/CD narrative into compliance matrix for consistent treatment"
  - "Add compliance rows for NFRs (at minimum the 4 MUST-priority NFRs)"
  - "Resolve CICD-03 / FR-018 PASS tension — mark FR-018 CONDITIONAL or add documented design decision"
  - "Fix 'four adapter modules' count error in L0 executive summary (five are listed)"
  - "Cite specific test execution artifact for 350-test PASS claim"
  - "Add target resolution timelines to the 3 MEDIUM findings in the tracker"
```

---

*Scored by adv-scorer*
*Strategy: S-014 LLM-as-Judge, 6-dimension weighted composite*
*SSOT: `.context/rules/quality-enforcement.md`*
*Cross-referenced against: harness-requirements.md (FR-001 through FR-030), constraint-verification.md*
*Date: 2026-03-07*
