# Quality Score Report: Stream 5B — V&V Execution (PROJ-036)

## L0 Executive Summary

**Score:** 0.84/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Internal Consistency (0.77)

**One-line assessment:** The V&V set delivers rigorous, evidence-backed verification for the statistical and MR subsystems, but is blocked from PASS by a cross-document scoping inconsistency (FR-026/FR-027 appear in the FMEA document but not in the requirements coverage matrix), an arithmetic error in the RPN total, and incomplete Section F agent-specific assertion verification — all of which must be resolved before the SAR gate.

---

## Scoring Context

- **Deliverable:** Four documents scored as a unified set:
  - `projects/PROJ-036-prompt-regression-harness/verification/requirements-coverage-matrix.md`
  - `projects/PROJ-036-prompt-regression-harness/verification/interface-verification.md`
  - `projects/PROJ-036-prompt-regression-harness/verification/constraint-verification.md`
  - `projects/PROJ-036-prompt-regression-harness/verification/fmea-mitigation-verification.md`
- **Deliverable Type:** Analysis (V&V Execution)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Custom Threshold:** 0.94 (C4 requirement per scoring brief)
- **Scored:** 2026-03-07

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.84 |
| **Threshold** | 0.94 (C4 — custom) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.83 | 0.1660 | 25/25 FRs addressed; Section F agent-specific YAMLs unverified; 3 of 6 universal invariants PARTIAL |
| Internal Consistency | 0.20 | 0.77 | 0.1540 | FR-026/FR-027 scoping inconsistency; RPN arithmetic error (stated 1,833, actual 1,823) |
| Methodological Rigor | 0.20 | 0.88 | 0.1760 | NPR 7123.1D applied; I/A/T categorization consistent; Analysis (A) usage thin for FR-003 |
| Evidence Quality | 0.15 | 0.84 | 0.1260 | Specific file:line citations throughout; pyproject.toml and per-agent YAMLs explicitly unread |
| Actionability | 0.15 | 0.90 | 0.1350 | Specific remediation paths for each gap; SAR/TRR readiness clearly differentiated |
| Traceability | 0.10 | 0.83 | 0.0830 | Forward/reverse traces present; FR-026/FR-027 breaks traceability chain in FMEA-to-VCRM |
| **TOTAL** | **1.00** | | **0.8400** | |

---

## Detailed Dimension Analysis

### Completeness (0.83/1.00)

**Evidence:**
The coverage matrix addresses all 25 FRs (FR-001 through FR-025) with explicit status for each. Layer 1, Layer 3/4, and Security/Infrastructure clusters are 100% verified. The FMEA document covers all 10 failure modes (FM-001 through FM-010). The constraint verification document covers all specified constraints in Sections C, D, and E with 100% pass rates. Four inter-layer interfaces are addressed in the interface verification document.

**Gaps:**
- Section F (Cross-Agent Consistency): 3 of 6 universal structural invariants are PARTIAL (SI-UNIV-002, SI-UNIV-005, SI-UNIV-006 not enforced in CI). Per-agent YAML files for all 5 agents (ps-researcher, ps-analyst, ps-architect, ps-critic, adv-scorer) explicitly acknowledged as "NOT VERIFIED (file not read)" — this is a substantial scope gap covering SI-RSRCH-001 through SI-SCOR-011 (approximately 41 invariants unverified).
- FR-009 remains PARTIAL: the per-agent/version/metric JSON path is not fully traced to implementation; `conftest.py` was not read.
- DeepEval version pinning in `pyproject.toml` acknowledged as a follow-on action item (FM-008 mitigation partially unverified).
- FR-012 and FR-013 are NOT STARTED, though both are SHOULD priority with documented deferral rationale.

**Improvement Path:**
Read the 5 per-agent YAML test case files and verify SI assertion implementation. Read `conftest.py` to confirm FR-009 disk write path. Read `pyproject.toml` to confirm DeepEval version pinning. This would raise Completeness to approximately 0.90+.

---

### Internal Consistency (0.77/1.00)

**Evidence:**
PASS/PARTIAL/NOT STARTED statuses are consistently applied across all four documents for shared requirements (FR-012, FR-013 consistently NOT STARTED in both requirements-coverage-matrix.md and fmea-mitigation-verification.md). The constraint verification document cross-references the interface verification document for Section C evidence. Debiasing enforcement (mandatory at adapter construction) is consistently described across requirements-coverage-matrix.md and fmea-mitigation-verification.md.

**Gaps:**
1. **FR-026/FR-027 scoping discontinuity:** The FMEA document references FR-026 (version pinning + re-baseline runbook) and FR-027 (test case authorship PR checklist) as verified mitigating requirements, including them in the FMEA-to-requirement forward trace table and marking both PASS. Neither FR-026 nor FR-027 appears anywhere in requirements-coverage-matrix.md, which covers only FR-001 through FR-025. This creates an internal inconsistency: the FMEA document implies requirements beyond the 25 covered in the VCRM, but the VCRM provides no accounting for them. Either the VCRM scope is incomplete (should cover FR-026 and FR-027) or the FMEA document is referencing requirement IDs outside the agreed scope.

2. **RPN arithmetic error:** The FMEA document states "Total Original RPN: 1,833" in the residual risk table. Independent sum: 432+280+240+168+144+144+140+125+90+60 = 1,823. The stated total is 10 points higher than the actual sum. This is a factual error in a quantitative verification artifact.

3. **MR-002 minimum_sample_size contradiction:** requirements-coverage-matrix.md (FR-011) describes MR-002 `minimum_sample_size=15` and notes "15 (not 20)." The constraint-verification.md (C.2) states "minimum_sample_size: int = 15 (reduced from 20 — derivation: N=15 sufficient for Wilcoxon on directional tests per contracts C.2)." This is consistent with the contracts, but the description in fmea-mitigation-verification.md (FM-002 evidence table) states N enforcement applies as `minimum_sample_size` without noting the MR-002 exception — creating a minor ambiguity about whether FM-002 is fully mitigated or whether the exception represents residual risk.

**Improvement Path:**
Reconcile FR-026/FR-027: either add them to the requirements-coverage-matrix.md with explicit status rows, or clarify in the FMEA document that they are FMEA-derived requirements outside the FR-001 through FR-025 scope with an explicit scope note. Fix the RPN arithmetic. Clarify the FM-002/MR-002 N=15 exception explicitly in the FMEA document.

---

### Methodological Rigor (0.88/1.00)

**Evidence:**
NPR 7123.1D Process 7 is the stated governing standard, consistently cited across all four documents. The V-method classification (I=Inspection, A=Analysis, T=Test) is applied to each FR in the coverage matrix with a legend. The FMEA document provides a structured failure mode mitigation matrix with RPN decomposition (S×O×D), residual RPN estimates, and explicit "Mitigation Category" classifications. Review readiness assessment (PDR/CDR/TRR/SAR) with percentage thresholds provides decision-quality information for gate owners. Forward and reverse trace tables in the FMEA document are correctly structured. The constraint verification document uses a tabular constraint-by-constraint verification pattern that is systematic and complete for Sections C-E.

**Gaps:**
- The Analysis (A) method is applied to only 1 requirement (FR-003). The evidence for FR-003 is: "Architecture note; promptfoo two-provider setup is placeholder per design note." This is an architectural observation, not a formal analysis. An analysis-method verification should demonstrate logical sufficiency of the design for meeting the requirement — this evidence doesn't fully establish that the before/after comparison mechanism (as implemented in Layer 4 Wilcoxon rather than promptfoo two-provider) satisfies FR-003's acceptance criteria AC-1 through AC-3.
- The residual RPN reduction percentages lack derivation. The 79.3% reduction claim follows from the stated (incorrect) 1,833 total and the residual total of 380. Using the correct total (1,823), the actual reduction is 79.2% — immaterial, but the underlying arithmetic error should still be corrected.

**Improvement Path:**
Strengthen the FR-003 Analysis evidence to demonstrate that the Layer 4 Wilcoxon implementation satisfies each AC point. Fix the RPN arithmetic.

---

### Evidence Quality (0.84/1.00)

**Evidence:**
The documents exhibit strong evidence quality where files were read. Specific module-level constants are quoted: `MIN_STATISTICAL_SAMPLE_SIZE = 20`, `BONFERRONI_K_FULL_SUITE = 13`, `BONFERRONI_ALPHA_FULL = 0.004`, `_BASELINE_QUALITY_GATE = 0.92`, per-MR TOLERANCE values. Specific method names, exception class names, and import statements are cited. The H-07 compliance check is particularly strong: a table lists each domain file, its external imports, and explicitly states "None" for adapter imports. The forbidden dependency verification enumerates 6 specific forbidden patterns and checks each against implementation.

**Gaps:**
- FR-009 PARTIAL: the evidence establishes the top-level `promptfoo-config.yaml` output path but cannot trace the per-agent/version/metric subdirectory path. This is honestly acknowledged rather than asserted without evidence — but it limits verifiability.
- Per-agent YAML files (ps-researcher.yaml through adv-scorer.yaml) were not read, so all agent-specific SI assertions are unverified. The document is honest about this but it leaves the Section F evidence base thin.
- `pyproject.toml` not read, so DeepEval version pinning (FM-008 primary mitigation) is unverified against the actual package management configuration. The model version pinning in `promptfoo-config.yaml` is verified, but this is only half of FR-026's scope.
- The module docstring content is used as evidence for FR-019 (cross-project sharing). Docstring claims are weaker evidence than import analysis — the docstring asserts cross-project sharing intent but does not prove PROJ-017 actually imports from the module.

**Improvement Path:**
Read the 5 per-agent YAML test case files, `conftest.py`, and `pyproject.toml`. Add import-level evidence for FR-019 PROJ-017 usage (look for `from jerry.testing.stats import` in PROJ-017 code). This would raise Evidence Quality to approximately 0.90.

---

### Actionability (0.90/1.00)

**Evidence:**
Every gap is accompanied by a specific remediation action. FR-009: "recommend reading `conftest.py` to confirm fixture-driven path construction." SI-UNIV-002: "Add `not-contains` assertion with first line of system prompt to `defaultTest`." SI-UNIV-005: "Add `not-regex` for JSON tool call patterns `{\"tool_use\": ...}`." The `_wilcoxon_p_and_effect` shared dependency: "this module should have unit tests validating the helper directly." SAR readiness: explicitly marked No with two specific conditions (FR-009 disk write path confirmation; FR-012/FR-013 formal deferral). The FMEA residual risk quantification gives gate owners a clear accept/reject framework.

**Gaps:**
- The FR-026/FR-027 scoping inconsistency identified in Internal Consistency has no explicit action item in any of the four documents — the inconsistency is invisible to the authors because it spans document boundaries.
- The RPN arithmetic error has no self-referential detection mechanism; it would benefit from a verification arithmetic check.

**Improvement Path:**
Add an explicit action item for the FR-026/FR-027 scope reconciliation. Minor: add a computational verification note to the residual risk table.

---

### Traceability (0.83/1.00)

**Evidence:**
The requirements-coverage-matrix.md Cross-Reference Validation table explicitly validates all 25 FR IDs against the requirements baseline, confirming zero orphan and zero stale references. The FMEA document provides both a FMEA-to-requirement forward trace and a requirements-to-FMEA reverse trace. Each FR in the VCRM links to a verification procedure (IP-NNN or TP-NNN), a V-level, and evidence sources. All four documents reference NPR 7123.1D Process 7 as the governing standard. The References section of each document enumerates sources with specific content used.

**Gaps:**
- The FR-026/FR-027 scope gap breaks the traceability chain. The FMEA document traces FM-007 and FM-008 through FR-027 and FR-026 respectively, but these requirements have no corresponding entry in the VCRM. A reviewer following the requirement chain from VCRM → FMEA document would find requirements referenced that do not appear in the primary coverage matrix. The VCRM cross-reference validation section would have caught this if its scope included FMEA-derived requirements.
- Agent-specific SI invariants (SI-RSRCH-001 through SI-SCOR-011) are traceable at the requirement level (behavioral-contracts.md) but have no implementation-level traceability since the per-agent YAML files were not verified.

**Improvement Path:**
Expand the VCRM cross-reference validation to include FMEA-derived requirements (FR-026, FR-027) or add a scope boundary note explaining that FR-026/FR-027 are out of scope with a forward reference to where they are verified. Complete agent-specific YAML verification to close the SI traceability gap.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Internal Consistency | 0.77 | 0.88 | Resolve FR-026/FR-027 scoping discontinuity: either add FR-026 and FR-027 rows to requirements-coverage-matrix.md, or add an explicit scope note in fmea-mitigation-verification.md clarifying they are FMEA-derived requirements outside the FR-001 through FR-025 scope. |
| 2 | Internal Consistency | 0.77 | 0.88 | Fix RPN arithmetic: the stated total "1,833" should be "1,823." Recompute the risk reduction percentage: 79.2% (not 79.3%). |
| 3 | Completeness | 0.83 | 0.90 | Read all 5 per-agent YAML test case files (ps-researcher.yaml, ps-analyst.yaml, ps-architect.yaml, ps-critic.yaml, adv-scorer.yaml) and verify SI assertion implementation. Update Section F constraint-verification.md with findings. |
| 4 | Completeness + Evidence | 0.83/0.84 | 0.90 | Read `conftest.py` to confirm FR-009 disk write path construction; read `pyproject.toml` to confirm DeepEval version pinning for FR-026/FM-008. |
| 5 | Traceability | 0.83 | 0.90 | Expand VCRM cross-reference validation scope to include FMEA-derived requirements FR-026 and FR-027, or add explicit scope boundary documentation. |
| 6 | Evidence Quality | 0.84 | 0.90 | Add import-level evidence for FR-019 PROJ-017 cross-project usage (locate `from jerry.testing.stats import` in PROJ-017 codebase rather than relying on docstring assertion). |
| 7 | Methodological Rigor | 0.88 | 0.92 | Strengthen FR-003 Analysis evidence: demonstrate that Layer 4 Wilcoxon satisfies each of FR-003's acceptance criteria (AC-1: before/after comparison; AC-2: version key integrity; AC-3: paired comparison) as a formal logical sufficiency argument, not just an architectural observation. |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score — specific quotes, file names, and gap characterizations
- [x] Uncertain scores resolved downward (Internal Consistency set to 0.77 not 0.80 due to FR-026/FR-027 + arithmetic error combination; Traceability set to 0.83 not 0.85 due to same FR-026/FR-027 issue)
- [x] First-draft calibration considered — this is iteration 1; calibration anchors applied (0.85 = strong with minor refinements; this set sits at 0.84 overall consistent with "significant gaps requiring focused revision")
- [x] No dimension scored above 0.95; highest is Actionability at 0.90, which is justified by the specific, implementable remediation paths documented throughout
- [x] RPN arithmetic independently verified: 432+280+240+168+144+144+140+125+90+60 = 1,823 (document states 1,833 — error confirmed)
- [x] Composite arithmetic verified: 0.1660+0.1540+0.1760+0.1260+0.1350+0.0830 = 0.8400

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.84
threshold: 0.94
weakest_dimension: internal_consistency
weakest_score: 0.77
critical_findings_count: 0
iteration: 1
improvement_recommendations:
  - "Resolve FR-026/FR-027 scoping discontinuity (add to VCRM or add scope note in FMEA document)"
  - "Fix RPN arithmetic: stated 1,833 should be 1,823; update risk reduction percentage to 79.2%"
  - "Read 5 per-agent YAML test case files and verify SI assertion implementation for Section F"
  - "Read conftest.py (FR-009 disk write path) and pyproject.toml (DeepEval version pinning)"
  - "Expand VCRM cross-reference validation to include FR-026 and FR-027"
  - "Add import-level evidence for FR-019 PROJ-017 cross-project usage"
  - "Strengthen FR-003 Analysis evidence with formal AC-by-AC sufficiency argument"
```

---

*Score Report generated by adv-scorer v1.0.0*
*S-014 LLM-as-Judge | SSOT: `.context/rules/quality-enforcement.md`*
*C4 Criticality | Custom Threshold: 0.94 | Gap to threshold: 0.10*
*2026-03-07*
