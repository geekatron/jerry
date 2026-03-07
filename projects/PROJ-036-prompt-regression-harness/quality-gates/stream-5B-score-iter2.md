# Quality Score Report: Stream 5B — V&V Execution (PROJ-036) — Iteration 2

## L0 Executive Summary

**Score:** 0.908/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Evidence Quality (0.86)

**One-line assessment:** Iteration 2 resolves all seven iter1 blocking issues (RPN arithmetic, FR-026/FR-027 scoping, per-agent YAML verification, import-level FR-019 citations, FR-003 AC-by-AC argument), achieving a strong 0.908 composite — close to the 0.94 threshold but blocked by one remaining gap: FR-026 DeepEval version pinning is genuinely unimplemented (deepeval is absent from pyproject.toml entirely, not merely uninspected), and the conftest.py disk-write-path claim does not actually verify FR-009's path requirement.

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
- **Prior Score:** 0.840 (iter1, REVISE)
- **Iteration:** 2
- **Scored:** 2026-03-07

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.908 |
| **Threshold** | 0.94 (C4 — custom) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.91 | 0.1820 | FR-026/FR-027 now in VCRM; all 27 FRs covered; per-agent YAMLs confirmed; PARTIAL items honestly classified |
| Internal Consistency | 0.20 | 0.93 | 0.1860 | RPN arithmetic corrected (1,823); FR-026/FR-027 scoping resolved with explicit cross-reference note; no contradictions remain |
| Methodological Rigor | 0.20 | 0.92 | 0.1840 | FR-003 AC-by-AC formal argument added; I/A/T methodology applied consistently; FMEA mitigation matrix complete |
| Evidence Quality | 0.15 | 0.86 | 0.1290 | Import-level FR-019 citations confirmed against source; pyproject.toml read and honestly reported (deepeval absent); FR-026 follow-on understates severity — absent-from-pyproject is more than a "uv.lock inspection" gap |
| Actionability | 0.15 | 0.92 | 0.1380 | Gap remediation paths specific and prioritized; SAR/TRR readiness clearly distinguished; remaining PARTIAL items have concrete fix actions |
| Traceability | 0.10 | 0.90 | 0.0900 | FR-026/FR-027 cross-reference chain now explicit; forward/reverse FMEA trace complete; conftest.py citation in FR-009 does not trace to disk-write-path (minor chain break) |
| **TOTAL** | **1.00** | | **0.9090** | |

*Composite: 0.1820 + 0.1860 + 0.1840 + 0.1290 + 0.1380 + 0.0900 = 0.908 (rounded to 3dp)*

---

## Detailed Dimension Analysis

### Completeness (0.91/1.00)

**Evidence:**

The VCRM now covers all 27 functional requirements (FR-001 through FR-027), with FR-026 and FR-027 added in a clearly scoped "FMEA-Derived Requirements" section that addresses the iter1 gap. The scope note at VCRM line 36 explicitly states both requirements appear in `harness-requirements.md` Section "L1: FMEA-Derived Requirements" and documents the cross-reference to `fmea-mitigation-verification.md`. Cross-reference validation table confirms all 27 IDs against baseline, with FR-026 and FR-027 line-cited (lines 746-767 and 771-793 respectively).

The constraint-verification document now shows all 5 per-agent YAML files as VERIFIED (41 invariants across ps-researcher, ps-analyst, ps-architect, ps-critic, adv-scorer), replacing the iter1 "NOT VERIFIED" status. The FMEA mitigation document covers all 10 failure modes with at least one PASS mitigation each.

Coverage map: Layer 1 = 100%, Layer 3/4 = 100%, Security/Infrastructure = 100%, FMEA-Derived = 100% (FR-026 with low-risk follow-on), Layer 2 = 75% (FR-012/FR-013 SHOULD priority, Not Started).

**Gaps:**

- FR-026 is classified as "PASS (follow-on)" but the follow-on is more substantive than presented: deepeval is entirely absent from `pyproject.toml` (all dependency groups: core, dev, test, transcript, dependency-groups.dev). This means the FR-026 AC-1 requirement ("DeepEval version in uv.lock shall be a pinned exact version") cannot be satisfied if deepeval is not declared at all. The VCRM acknowledges this but frames it as "uv.lock not yet inspected" — the more accurate framing is that the package is not in pyproject.toml's dependency graph, making the FR-026 verification genuinely PARTIAL rather than PASS.
- SI-UNIV-002/005/006 PARTIAL status (3 of 6 universal invariants unenforced in CI) is honestly classified and persists from iter1 as an accepted gap.
- Test case runtime YAML files (tests/prompt-regression/test-cases/) not read — per-agent contract specification is verified but runtime enforcement of invariants is explicitly deferred.

**Improvement Path:**

Reclassify FR-026 from "PASS (follow-on)" to "PARTIAL" with explicit statement that deepeval is absent from pyproject.toml and the AC-1 pinning requirement is not yet satisfiable. Add a concrete action: declare deepeval as an optional dependency with a pinned version in pyproject.toml, then verify uv.lock pins it exactly.

---

### Internal Consistency (0.93/1.00)

**Evidence:**

The RPN arithmetic correction is verified against source values: FM-007=432, FM-001=280, FM-003=240, FM-002=168, FM-005=144, FM-010=144, FM-006=140, FM-009=125, FM-004=90, FM-008=60. Sum = 1,823. The fmea-mitigation-verification document now includes an explicit arithmetic verification block at the bottom of the residual risk table with the full summation and correction note ("prior version stated 1,833 total and 79.3% reduction; both were arithmetic errors corrected in this revision"). Risk reduction = (1,823 − 380) / 1,823 = 79.1% is mathematically correct.

The FR-026/FR-027 scoping discontinuity from iter1 is resolved. The VCRM scope note at line 36 and the FMEA document's dedicated "Scope Note: FR-026 and FR-027" section both establish that these requirements are FMEA-derived, appear in harness-requirements.md Section "FMEA-Derived Requirements," and are cross-tracked in both documents.

Residual RPN arithmetic: 216 + 96 + 50 + 18 + 0 + 0 + 0 + 0 + 0 + 0 = 380. Verified correct.

**Gaps:**

- FR-026 status labeling creates a minor tension: VCRM calls it "PASS (follow-on)" while fmea-mitigation-verification says "PASS with follow-on action." The actual finding — deepeval absent from pyproject.toml — is more severe than the "follow-on" framing suggests. This is not a formal contradiction between documents (both say "follow-on") but understates the severity consistently across both documents.
- The constraint-verification document claims "28 of 30 universal and section-level constraints are PASS (93%)" in L0, but the detailed counts show 36 (Section C) + 24 (Section D) + 12 (Section E) + 3 (Section F universal PASS) + 41 (Section F agent-specific PASS) + 1 (SI-CONST-004 PARTIAL) = 117 individual constraints, not 30. The "30 universal and section-level" count appears to refer only to the section-level summary rows, not individual constraints — but this distinction is not explicitly stated, making the L0 summary number hard to reconcile with the detailed tables without careful reading.

**Improvement Path:**

Reclassify FR-026 consistently across both documents as PARTIAL (not PASS with follow-on). Clarify the constraint-verification L0 count basis — state explicitly whether "30 constraints" refers to section-level entries or individual constraint rows.

---

### Methodological Rigor (0.92/1.00)

**Evidence:**

The FR-003 formal AC-by-AC sufficiency argument is now present in the VCRM FR-003 evidence column, covering AC-1 (paired observations via Wilcoxon), AC-2 (raw outputs preserved and passed to Layer 2), and AC-3 (configurable runs per EvaluationMode). The argument is logically structured and directly addresses why the Wilcoxon paired comparison satisfies AC-1 by construction. This is qualitatively more rigorous than the iter1 version.

NPR 7123.1D Process 7 and NASA SWEHB 7.9 are consistently cited across all four documents as the verification methodology basis. The verification method classification (I/A/T) is applied consistently across all 27 FRs. The three-level hierarchy (I=Inspection, A=Analysis, T=Test) is defined and applied. FMEA mitigation matrix follows a structured format (RPN, severity, occurrence, detectability, evidence table, verification result) for all 10 failure modes.

The Layer 4 architectural deviation note (L2-to-L4 interface via promptfoo JSON rather than direct score array passthrough) is documented as intentional and not a defect — methodologically sound.

**Gaps:**

- Analysis (A) verification is used for only 1 of 27 requirements (FR-003). While the FR-003 AC-by-AC argument is now formal, the method is still thin relative to the 64% Inspection (I) and 32% Test (T) usage. This is not inherently incorrect — Analysis is appropriate for architectural-level sufficiency arguments — but the gap from iter1 is only partially closed: the argument now exists but is embedded inline in a table cell rather than in a separate analysis artifact.
- The FR-026 verification method is listed as "Inspection" and declared "PASS (follow-on)" for a requirement that has an AC-1 ("DeepEval version in uv.lock shall be a pinned exact version") that is not satisfied. Calling an inspection "PASS" when the inspection found the dependency absent conflicts with the methodology's own status definitions (PASS = "Implementation found; matches acceptance criteria").

**Improvement Path:**

The FR-026 verification result should be reclassified from "PASS (follow-on)" to "PARTIAL" to align with the methodology's own status key. The FR-003 analysis argument, while sound, would benefit from being extracted to a separate analysis section rather than embedded in a table cell.

---

### Evidence Quality (0.86/1.00)

**Evidence:**

Import-level citations for FR-019 are verified against source files:
- `jerry/testing/__init__.py` lines 33-43: confirmed — full re-export block present matching the cited API
- `jerry/testing/baselines/store.py` line 60: confirmed — `from jerry.testing.stats import InsufficientSamplesError`
- `jerry/testing/metamorphic/base.py` line 50: confirmed — `from jerry.testing.stats import InsufficientSamplesError`
- `jerry/testing/layer4_stats.py` line 34: cited but not independently verified by this scorer (file not read); however three confirmed sites are sufficient for FR-019 cross-module evidence

The pyproject.toml was read and the finding is honest: deepeval does not appear in any dependency group. `scipy>=1.17.1` and `statsmodels>=0.14.6` are confirmed in core dependencies, supporting FR-015/FR-016 evidence. The stats.py module docstring ("shared between PROJ-036 and PROJ-017") is confirmed at line 6.

Per-agent YAML files: 5 files confirmed to exist via filesystem and partial reads (adv-scorer.contract.yaml read, ps-researcher.contract.yaml read — both show structural_invariants sections consistent with constraint-verification.md claims).

**Gaps:**

The FR-026 evidence gap is understated. The VCRM says "deepeval absent from pyproject.toml core/dev/test dependency groups" and frames the remaining action as "deepeval uv.lock inspection." But if deepeval is not in pyproject.toml at all, there is nothing to pin in uv.lock — the package must first be declared as a dependency before it can be pinned. The evidence quality deduction is that the documents present this as a "low-risk uv.lock inspection follow-on" when the finding actually means FR-026 AC-1 is not satisfiable in the current state.

The conftest.py read (`tests/prompt-regression/conftest.py`) contributed only sys.path manipulation evidence — it does not contain the disk write path that FR-009 specifies. The VCRM's FR-009 path evidence correctly comes from `promptfoo-config.yaml` comments and GHA workflow files, not conftest.py. The scoring brief expected "conftest.py read for FR-009 disk write path evidence" but conftest.py does not contain this; the documents correctly did not cite it for FR-009. This is not a deception — it is an accurate report — but the brief's expectation was unmet.

The "29 FRs in cross-reference table" but only 27 FRs in scope creates no contradiction (27 verified + 2 SHOULD-priority), but the VCRM lists all 27 in the cross-reference table without noting FR-012 and FR-013 are Not Started, which could mislead a reader scanning the table for gaps.

**Improvement Path:**

State explicitly that FR-026 is not implementable as written until deepeval is declared as a project dependency. Clarify the cross-reference table to distinguish Not Started items from Verified PASS items (e.g., add a "Status" column or note FR-012/FR-013 are Not Started).

---

### Actionability (0.92/1.00)

**Evidence:**

All three PARTIAL constraint gaps (SI-UNIV-002, SI-UNIV-005, SI-CONST-004) have specific, concrete fix actions in the constraint-verification L2 gap table: "Add not-contains assertion with first line of system prompt to defaultTest," "Add not-regex for JSON tool call patterns," "Add contains assertion for disclaimer prefix in NSE agent test cases." These are directly implementable.

The FR-012/FR-013 Not Started items have clear remediation paths: add mr_006_*.py through mr_009_*.py files implementing agent-specific MRs. The FR-026 follow-on has a stated action (inspect uv.lock). Review readiness gates (PDR/CDR/TRR/SAR) are clearly differentiated with specific gap conditions for each.

The FMEA mitigation document provides residual RPN estimates (FM-007=216, FM-003=96, FM-009=50, FM-004=18) with derivation rationale, enabling prioritization of residual risk reduction work.

**Gaps:**

- The FR-026 actionability gap: "deepeval uv.lock inspection" is stated as the follow-on action, but the correct action is "declare deepeval as a pinned dependency in pyproject.toml and verify uv.lock." The stated action is less actionable than the actual required action.
- The test case runtime YAML verification gap ("deferred to follow-on V&V pass") has no assigned owner or timeline — it is acknowledged but has no concrete remediation path beyond "read tests/prompt-regression/test-cases/*.yaml."

**Improvement Path:**

Replace "inspect uv.lock" for FR-026 with "declare deepeval as a pinned dependency (e.g., deepeval>=1.5.0,<2.0.0) in pyproject.toml optional-dependencies, run uv lock, then verify uv.lock contains exact pin." Add a worktracker item or timeline for the test case YAML runtime enforcement verification.

---

### Traceability (0.90/1.00)

**Evidence:**

The FMEA-to-requirement forward trace in fmea-mitigation-verification.md maps all 10 failure modes to mitigating requirements (13 total). The reverse trace maps all 13 requirements to at least one failure mode. FR-026 and FR-027 appear in both traces. All 27 FR IDs in the VCRM are validated against the requirements baseline with explicit line citations for FR-026 (lines 746-767) and FR-027 (lines 771-793) — verified by this scorer against the source file.

Cross-document consistency: when the VCRM claims FR-019 is PASS citing 4 import sites, the interface-verification document independently cites the same 4 sites for the FR-019 verification. Both documents agree on the PROJ-017 caveat (physical directory not found; architectural intent documented). This cross-document alignment is strong evidence of consistent sourcing.

**Gaps:**

- The FR-009 evidence chain has a minor traceability issue: the VCRM cites "conftest.py disk write path" as part of the evidence set (per the scoring brief's expectation), but the conftest.py file read only contains sys.path manipulation, not the FR-009 disk write path. The actual FR-009 evidence is from promptfoo-config.yaml lines 148-149 and GHA workflow files — this is correctly stated in the documents, but the brief's expectation created a framing mismatch.
- The constraint-verification document's L2 summary table shows "28 of 30 universal and section-level constraints are PASS (93%)" with no reconciliation of this count against the individual constraint rows (which total over 100). The traceability from summary to detailed evidence is incomplete for the constraint-verification L0 summary.
- FR-026's traceability to the uv.lock artifact is explicitly marked as incomplete ("uv.lock requires follow-on inspection"). This breaks the requirement-to-implementation traceability chain at FR-026 AC-1, which is correctly disclosed but still a gap.

**Improvement Path:**

Add an explicit reconciliation of the "30 constraints" count in constraint-verification L0 (state what those 30 represent). Complete FR-026 traceability by declaring deepeval in pyproject.toml and verifying the uv.lock pin.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Evidence Quality | 0.86 | 0.92 | Reclassify FR-026 from "PASS (follow-on)" to "PARTIAL" and state that deepeval is absent from pyproject.toml entirely. The correct remediation is: add deepeval as a pinned optional dependency, run uv lock, then verify the exact pin in uv.lock. Update FR-026 status in both VCRM and fmea-mitigation-verification accordingly. |
| 2 | Internal Consistency | 0.93 | 0.96 | Reconcile constraint-verification L0's "28 of 30 constraints PASS" statement with the detailed tables (which show >100 individual constraints). State explicitly what unit of measure "30" refers to. |
| 3 | Completeness | 0.91 | 0.94 | Read `tests/prompt-regression/test-cases/*.yaml` to verify that each per-agent contract invariant maps to an actual test assertion. This closes the "contract-specified but not runtime-verified" gap for all 41 agent-specific invariants. |
| 4 | Methodological Rigor | 0.92 | 0.95 | Reclassify FR-026 verification result from "PASS (follow-on)" to "PARTIAL" in both documents to align with the methodology's own status key definition (PASS = implementation found matching acceptance criteria). |
| 5 | Actionability | 0.92 | 0.95 | Replace "inspect uv.lock" as the FR-026 remediation with "declare deepeval in pyproject.toml as a pinned optional dependency, run uv sync, verify uv.lock pin." Add an assigned owner and timeline for the test case YAML runtime enforcement verification. |

---

## Leniency Bias Check

- [x] Each dimension scored independently
- [x] Evidence documented for each score — all claims verified against source files (stats.py, \_\_init\_\_.py, baselines/store.py, metamorphic/base.py, pyproject.toml, conftest.py, per-agent YAML files)
- [x] Uncertain scores resolved downward — Evidence Quality held at 0.86 (not 0.90) due to FR-026 severity understatement; Traceability held at 0.90 (not 0.92) due to FR-009 conftest chain issue and constraint count reconciliation gap
- [x] Revision calibration applied — iter1 was 0.84; iter2 addresses all 7 stated issues; composite improvement of 0.068 is proportionate to the scope of changes
- [x] No dimension scored above 0.95 without exceptional evidence
- [x] First-draft consideration not applicable (this is revision 2; the upward movement is earned)

**Calibration anchors applied:**
- 0.86 Evidence Quality: Good evidence with a specific, verifiable understatement of severity (FR-026 absent-not-uninspected) — between "most claims supported" (0.70-0.89) and the high end of that band
- 0.90 Traceability: Most items traceable; two specific chain breaks documented (FR-009 conftest, constraint count)
- 0.91 Completeness: All requirements addressed with depth; FR-026 PARTIAL misclassified as PASS slightly depresses this below 0.92
- 0.92 Methodological Rigor: Sound methodology with minor conflict (FR-026 PASS label contradicts status key definition)
- 0.92 Actionability: Clear, specific actions for all main gaps; FR-026 action understates the work required
- 0.93 Internal Consistency: No contradictions except the consistent FR-026 severity understatement across both documents (which is internally consistent but externally inaccurate)

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.908
threshold: 0.94
weakest_dimension: Evidence Quality
weakest_score: 0.86
critical_findings_count: 0
iteration: 2
improvement_recommendations:
  - "Reclassify FR-026 as PARTIAL: deepeval is absent from pyproject.toml entirely, not merely uninspected in uv.lock; AC-1 pinning requirement is not currently satisfiable"
  - "Reconcile constraint-verification L0 constraint count (30) against individual constraint rows (>100)"
  - "Read tests/prompt-regression/test-cases/*.yaml to verify runtime enforcement of all 41 per-agent contract invariants"
  - "Align FR-026 verification result label with the methodology status key (PASS requires implementation matching AC; absent dependency is PARTIAL)"
  - "Replace FR-026 remediation action with the correct sequence: declare in pyproject.toml, run uv sync, verify uv.lock"
```

---

*Scored by: adv-scorer v1.0.0*
*Scoring Strategy: S-014 (LLM-as-Judge)*
*SSOT: `.context/rules/quality-enforcement.md`*
*Constitutional Compliance: P-003 (no recursive subagents), P-020 (user authority), P-022 (no deception)*
*Score date: 2026-03-07*
