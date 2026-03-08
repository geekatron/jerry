# Quality Score Report: Stream 1A — Requirements Specification (harness-requirements.md)

## L0 Executive Summary

**Score:** 0.875/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Internal Consistency (0.84)
**One-line assessment:** A well-structured, evidence-rich requirements document that misses the threshold primarily due to a real module naming inconsistency, an NFR-to-FR priority mismatch in the CI gate, missing FR-012 in the reverse traceability table, and no phasing map connecting requirements to the ADR-001 implementation roadmap.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-036-prompt-regression-harness/requirements/harness-requirements.md`
- **Deliverable Type:** Requirements Specification (NASA-SE, NPR 7123.1D)
- **Criticality Level:** C4 (architecture/governance deliverable — all tiers applied)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-03-07T00:00:00Z
- **Iteration:** 1 of adversarial scoring cycle (Stream 1A)
- **ADR Source Verified:** PROJ-035/decisions/ADR-001-test-harness-architecture.md (ACCEPTED 2026-03-06)

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.875 |
| **Threshold** | 0.94 (C4 adversarial gate per scoring task brief) |
| **Pass Threshold (H-13)** | 0.92 |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No (iteration 1; no prior adv-executor reports) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.90 | 0.180 | All 4 layers, 10 FMEAs, 10 STK-Ns covered; minor gap on phasing map and test corpus requirement |
| Internal Consistency | 0.20 | 0.84 | 0.168 | layer4_stats.py vs stats.py naming conflict; NFR-002 "Should" priority for a "Must" CI gate; self-referential IF-005 ADR source |
| Methodological Rigor | 0.20 | 0.88 | 0.176 | NASA-SE format applied rigorously to FRs; NFRs lack G/W/T structure; no phasing cross-reference |
| Evidence Quality | 0.15 | 0.88 | 0.132 | All 22 ADR evidence entries traced; specific citations; minor dependency on ADR-001 for evidence descriptions |
| Actionability | 0.15 | 0.88 | 0.132 | Concrete file paths, function names, schemas; missing phase-to-requirement delivery map |
| Traceability | 0.10 | 0.87 | 0.087 | Four bidirectional matrices present; FR-012 absent from FMEA reverse trace table |
| **TOTAL** | **1.00** | | **0.875** | |

---

## Detailed Dimension Analysis

### Completeness (0.90/1.00)

**Evidence:**
The document covers all required content areas: 30 FRs (FR-001 through FR-030) spanning all 4 ADR-001 architectural layers, 15 NFRs (NFR-001 through NFR-015), 7 interface specifications (IF-001 through IF-007), 10 stakeholder needs (STK-N-001 through STK-N-010), and the complete FMEA coverage table for FM-001 through FM-010. The layer allocation in the traceability matrix correctly maps FR-001 through FR-007 to Layer 1 (promptfoo), Layer 2 (DeepEval), Layer 3 (metamorphic), Layer 4 (statistical), and cross-cutting concerns. Cross-cutting requirements (FR-021 through FR-030) address governance, process, and observability concerns not tied to a single layer.

The L1 Requirements Quality Checklist (lines 1317-1332) passes every criterion with documented evidence, and the self-review (S-010) at lines 1476-1514 confirms completeness across all dimensions.

**Gaps:**
1. No requirement for the initial test case corpus. FR-027 requires test case authorship on PRs going forward, but there is no requirement specifying the minimum initial set of test cases that must exist before the harness is considered production-ready. An engineer reading these requirements cannot determine what "done" looks like for Phase A from a test case inventory standpoint.
2. NFR-015 specifies "macOS, Linux" for local development without Docker (line 1116), but does not address Windows. ADR-001 has no Windows constraint, so this may be an appropriate exclusion, but it is not documented as a conscious decision with rationale.
3. No requirement for the behavioral property registry that FR-013 (MR coverage tracking) depends on. FR-013 acceptance criterion reads "a list of documented behavioral properties for an agent" but no requirement specifies how or where these behavioral properties are defined, maintained, or structured.

**Improvement Path:**
Add FR-031 specifying the minimum initial test case corpus (e.g., "at least 3 test cases per agent type covered in Phase B"). Add NFR-016 or a gap note for the behavioral property registry format. Document Windows exclusion with explicit rationale in NFR-015.

---

### Internal Consistency (0.84/1.00)

**Evidence:**
The document correctly reconciles the potential conflict between FR-005 (Smoke mode N=1) and FR-014 (N >= 20 enforcement) by explicitly excluding Smoke mode from statistical analysis. FR-016 aligns QUALITY_PASS_THRESHOLD=0.92 with H-13. FR-023 (UV-only) is correctly aligned with H-05. The FMEA table correctly maps all 10 failure modes with RPN values matching ADR-001.

**Gaps — Specific Inconsistencies:**

1. **Module naming conflict (lines 1356-1360 vs. line 1359):** The allocation table (lines 1355-1360) maps FR-018 to `jerry/testing/layer4_stats.py`, but FR-019 (line 555) specifies the shared statistical module at `jerry/testing/stats.py`. These appear to be different files — `layer4_stats.py` as the pipeline orchestration layer and `stats.py` as the shared statistical function library — but FR-030 (line 837) only lists `jerry/testing/layer4_stats.py` (not `stats.py`) in the module path specification for the layer architecture. FR-019 is explicit that the shared module is `jerry/testing/stats.py` and it is imported via `from jerry.testing.stats import compare_versions`. This creates an unresolved question: does `jerry/testing/layer4_stats.py` import from `jerry/testing/stats.py`, or are they the same file? The allocation table and FR-030 module list are inconsistent on this point.

2. **NFR-002 priority mismatch (lines 880-892):** NFR-002 (Standard mode latency <= 15 minutes) is marked "Should" priority. However, FR-002 (lines 103-124) is marked "Must" and requires that the GitHub Actions workflow execute the promptfoo regression evaluation for PRs modifying agent definitions. If the regression evaluation has only a "Should" latency bound, then the "Must" CI gate may routinely time out in GitHub Actions (default 6-hour job timeout, but PR workflows typically enforce shorter feedback loop norms). The NFR-002 priority should be "Must" to match the PR-blocking function of the CI gate it governs.

3. **IF-005 self-referential ADR source (line 1260):** The ADR Source field for IF-005 reads: "ADR-001 Architecture Diagram 'CI/CD Gate Decision'; ADR-001 FR-018 (from this document)." Referencing "FR-018 (from this document)" as an ADR Source is internally circular — ADR sources should be external documents, not other requirements in the same specification. This should reference the architectural intent in ADR-001 directly, not a requirement that is itself derived from ADR-001.

4. **FR-028 run count vs. FR-005 Full mode (lines 787-788 vs. 187):** FR-028 specifies N=30 for model migration mode, which matches Full mode. However, FR-028 is marked "Should" priority while FR-005 (Full mode N=30) is "Must." If Full mode is "Must" but model migration mode is "Should," the N=30 run count cannot be derived from FR-005 alone for migration use cases — this is an implicit dependency that should be made explicit.

**Improvement Path:**
Resolve the `layer4_stats.py` vs `stats.py` naming by adding an explicit statement in FR-030 or FR-019 that `jerry/testing/stats.py` is imported by `jerry/testing/layer4_stats.py`. Escalate NFR-002 to "Must" priority. Remove the self-referential ADR source in IF-005 and replace with the ADR-001 section that establishes the CI/CD gate pattern.

---

### Methodological Rigor (0.88/1.00)

**Evidence:**
The document applies NASA-SE NPR 7123.1D methodology explicitly, citing Process 1 (Stakeholder Expectations), Process 2 (Technical Requirements), and Process 11 (Requirements Management). All 30 Must-priority FRs use Given/When/Then acceptance criteria format. Verification methods are assigned to every requirement using the A/D/I/T taxonomy (Analysis, Demonstration, Inspection, Test). Rationale is present for every requirement. The FMEA-derived requirements table explicitly maps mitigation requirements to each failure mode. The self-review checklist (S-010) is structurally complete.

**Gaps:**
1. **NFRs lack Given/When/Then structure.** All Must-priority FRs use the structured Given/When/Then format (e.g., FR-001 lines 84-88, FR-002 lines 109-112). NFRs use descriptive acceptance criteria paragraphs rather than this format. NFR-001 (line 870-873) reads "measure wall-clock time for Smoke evaluation on a representative agent; verify < 60 seconds for P95 across 10 runs" — this is a verification method description embedded in what should be an acceptance criterion. NFR-003, NFR-004, and NFR-007 have similar structure. Consistent methodology requires either G/W/T format for all Must-priority requirements or explicit documentation of why NFRs deviate.

2. **No phasing cross-reference table.** ADR-001 defines a six-phase implementation roadmap (Phases A through F). The requirements document mentions phases in individual requirement rationale fields (e.g., FR-004 cites "Phase A," FR-012 cites "Phase D," FR-013 cites "Phase D") but provides no table mapping each FR and NFR to its delivery phase. An engineer picking up Phase B implementation cannot identify which requirements are in scope without reading every FR's rationale section. This is a methodological completeness gap for an operationally useful requirements specification.

3. **Priority cardinality not analyzed.** The document lists 22 "Must" FRs, 8 "Should" FRs, and 0 "May" FRs, with 11 "Must" NFRs and 4 "Should" NFRs, but does not analyze whether the Must set is achievable within Phase A-B scope. NASA-SE methodology recommends feasibility analysis of priority assignments. No such analysis is present.

**Improvement Path:**
Rewrite NFR acceptance criteria in Given/When/Then format for all Must-priority NFRs. Add an Appendix A: Phase-to-Requirements Map table cross-referencing each FR/NFR to its ADR-001 implementation phase. Add a one-paragraph feasibility note on Must priority count vs. Phase A-B scope.

---

### Evidence Quality (0.88/1.00)

**Evidence:**
Every FR and NFR rationale field contains at least one specific citation to an ADR-001 section, E-XXX evidence entry, or Jerry governance rule. The traceability matrix at lines 1408-1431 maps all 22 evidence entries (E-001 through E-022) to the requirements they derive. Citations are specific: ADR-001 section names, evidence entry descriptions, and external research citations (LLMORPH ASE 2025 for NFR-006 line 956, ICML 2025 for NFR-007 line 974). FR-015 rationale cites the Wilcoxon selection rationale from specific ADR sections. FR-007 cites specific pattern numbers (PAT-002) from Phase 3 synthesis.

**Gaps:**
1. **Evidence descriptions absent for indirect citations.** Twelve requirements cite only E-XXX identifiers without describing what that evidence contains (e.g., FR-010 rationale at line 326 cites "E-010; E-002" but only describes the LLMORPH study and notes the evidence ID — a reader without ADR-001 cannot evaluate the strength of E-002). The document is nominally traceable but not standalone-readable from an evidence standpoint. This is a documentation quality gap, not a methodology gap.

2. **E-012 deferred without requirement.** E-012 is cited in the traceability matrix (line 1421) as "(Phase E; deferred; architecture extensibility via FR-030)." This is a valid deferral acknowledgment. However, the rationale does not explain why PPI calibration is deferred to Phase E specifically rather than Phase B or C. The evidence for PPI's value (E-012) is acknowledged but its deferral rationale is not documented.

3. **NFR-008 rationale is weak.** NFR-008 (test case file naming convention, line 990-1000) rationale reads: "Consistent naming enables automated test case discovery, CI tooling to associate YAML files with agent definition files for coverage tracking (FR-013)..." This is a functional benefit statement but does not cite any ADR-001 evidence entry. It is the only requirement without an E-XXX or ADR section citation.

**Improvement Path:**
Add a brief description of each E-XXX evidence entry's content in the traceability matrix (one sentence per entry). Add an ADR-001 citation or explicit governance rule citation to NFR-008 rationale. Document PPI deferral rationale in the E-012 traceability row.

---

### Actionability (0.88/1.00)

**Evidence:**
Requirements specify concrete implementation artifacts: `jerry/testing/stats.py` (FR-019), `jerry/testing/layer2_deepeval.py` (FR-008, FR-009), `jerry/testing/layer3_metamorphic.py` (FR-010, FR-011), `jerry/testing/stats.py` (FR-014, FR-015), `tests/prompt-regression/criteria/` (FR-007), `tests/prompt-regression/mr-config.yaml` (FR-011). Function signatures are specified: `compare_versions()`, `wilson_score_intervals()`, `InsufficientSamplesError`, `RegressionResult`. JSON schemas are fully defined in the interface specifications (IF-003, IF-005). CLI commands are specified to the argument level (NFR-013). GitHub Actions workflow YAML snippets are provided in IF-006.

**Gaps:**
1. **No phase delivery map.** As noted in Methodological Rigor, requirements cite phases in individual rationale fields but do not provide a consolidated phase-to-requirement map. An engineer responsible for Phase B implementation must scan all 30+ requirements to identify Phase B scope. This reduces practical actionability.

2. **FR-013 behavioral property registry undefined.** FR-013 acceptance criterion (line 398) specifies "a list of documented behavioral properties for an agent" but does not specify where this list lives, who owns it, or its format. Without knowing the structure of the behavioral property registry, an engineer cannot implement the coverage metric.

3. **FR-012 verification method is weak.** FR-012 (agent-specific MRs) verification method reads: "Inspection (verify at least two agent-specific MRs defined per agent class after Phase D); Demonstration (show an agent-specific MR executing only for its target agent type)." The word "after Phase D" in an inspection criterion makes the verification time-dependent and not runnable at requirements validation time. This is structurally deferred verification, which is acceptable but should be explicitly labeled as a Phase D acceptance criterion rather than a requirement-time inspection.

**Improvement Path:**
Add Appendix A: Phase-to-Requirements Map. Add FR-031 or an appendix section specifying the behavioral property registry format and ownership (to enable FR-013 implementation). Revise FR-012 verification method to label the Phase D dependency explicitly.

---

### Traceability (0.87/1.00)

**Evidence:**
Four bidirectional traceability tables are present and structurally complete:
1. ADR-001 Evidence to Requirements (lines 1408-1431): 22 evidence entries mapped.
2. Stakeholder Needs to Requirements (lines 1433-1446): 10 STK-N needs mapped.
3. ADR-001 Architectural Layers to Requirements (lines 1448-1456): 5 layer categories mapped.
4. FMEA Failure Modes to Requirements — Reverse Trace (lines 1458-1472): 11 requirements mapped.

The traceability strategy section (lines 1383-1401) describes the full chain from stakeholder needs through evidence through requirements through verification.

**Gaps:**
1. **FR-012 absent from FMEA reverse trace table.** The FMEA-derived requirements table (lines 1302-1313) shows FM-003 (Incomplete MR coverage, RPN=240) is mitigated by "FR-012 (agent-specific MRs), FR-013 (MR coverage metric), FR-011 (calibration)." However, the reverse trace table (lines 1460-1472) does not include a row for FR-012. FR-011, FR-013, and other FM-003 mitigations appear in the table, but FR-012 is omitted. This is a genuine traceability gap — FR-012 cannot be traced backward to its FMEA failure mode without cross-referencing the forward table.

2. **STK-N-001 coverage is overloaded.** The Stakeholder Needs to Requirements table (line 1437) maps STK-N-001 to 21 requirements. This is not inherently wrong — STK-N-001 is the most general need ("Know whether a prompt change caused a regression") — but it means the mapping is informationally weak for that row: it provides no signal about which requirements primarily address STK-N-001 vs. which address it incidentally.

3. **No forward trace from requirements to verification artifacts.** The traceability matrix does not include a verification trace showing which requirements correspond to which planned test artifacts (e.g., unit tests in `jerry/testing/tests/`, integration tests, CI pipeline steps). This is a forward traceability gap that becomes relevant during V&V.

**Improvement Path:**
Add FR-012 row to the FMEA reverse trace table mapping it to FM-003. Add a "Primary / Secondary" column to the STK-N mapping for STK-N-001 to distinguish primary requirements from incidental coverage. Add an Appendix B: Verification Artifact Map as a forward trace from each requirement to its planned verification test location.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Internal Consistency | 0.84 | 0.90+ | Resolve `layer4_stats.py` vs `stats.py` naming conflict with explicit statement in FR-030 or FR-019; escalate NFR-002 to "Must" priority; remove self-referential ADR source from IF-005 |
| 2 | Traceability | 0.87 | 0.92+ | Add FR-012 to FMEA reverse trace table (maps to FM-003); add Appendix B verification artifact map |
| 3 | Methodological Rigor | 0.88 | 0.92+ | Rewrite NFR Must-priority acceptance criteria in Given/When/Then format; add Appendix A phase-to-requirements map |
| 4 | Actionability | 0.88 | 0.92+ | Define behavioral property registry format (required by FR-013); add phase delivery map; revise FR-012 verification to label Phase D dependency explicitly |
| 5 | Completeness | 0.90 | 0.93+ | Add requirement for initial test case corpus minimum; add behavioral property registry requirement (FR-031); document Windows exclusion in NFR-015 |
| 6 | Evidence Quality | 0.88 | 0.92+ | Add one-sentence evidence descriptions to E-XXX entries in traceability matrix; add ADR-001 citation to NFR-008 rationale |

---

## Specific Findings Requiring Resolution Before PASS

The following findings represent concrete defects (not style preferences) that must be addressed:

### FINDING-1: Module Naming Conflict (Internal Consistency — High Priority)

**Location:** FR-030 line 837, FR-019 line 555, Allocation table line 1359
**Finding:** FR-030 module path list specifies `jerry/testing/layer4_stats.py` but FR-019 specifies the shared statistical module at `jerry/testing/stats.py` imported via `from jerry.testing.stats import compare_versions`. The allocation table (line 1359) maps FR-018 to "`jerry/testing/layer4_stats.py` + GHA integration" which conflates the report orchestration layer (layer4_stats.py) with the statistical functions module (stats.py). It is unclear whether these are two separate files with a dependency relationship, or a naming inconsistency that could cause implementation confusion.
**Required Resolution:** Add one sentence to FR-019 or FR-030 explicitly stating: "The `jerry/testing/layer4_stats.py` module is the pipeline orchestration layer that imports and coordinates functions from `jerry/testing/stats.py`; they are distinct modules." Alternatively, if they are the same module, rename one reference to eliminate the discrepancy.

### FINDING-2: NFR-002 Priority Mismatch with FR-002 (Internal Consistency — High Priority)

**Location:** NFR-002 line 882, FR-002 lines 103-124
**Finding:** FR-002 (PR-triggered GitHub Actions regression gate) is "Must" priority. NFR-002 (Standard mode latency <= 15 minutes) is "Should" priority. A "Must" CI gate governed by a "Should" latency bound is internally inconsistent: if the latency "Should" be 15 minutes but is not required to be, then the "Must" CI gate may be practically unusable for PRs. Engineers cannot block merge on a gate that may take arbitrarily long.
**Required Resolution:** Escalate NFR-002 to "Must" priority with rationale: "A Must-priority CI gate (FR-002) requires a Must-priority latency bound to be operationally viable."

### FINDING-3: FR-012 Missing from FMEA Reverse Trace (Traceability — Medium Priority)

**Location:** FMEA Reverse Trace table lines 1460-1472
**Finding:** The FMEA-derived requirements table (line 1306) shows FM-003 is mitigated by FR-012, FR-013, and FR-011. The reverse trace table includes rows for FR-011 and FR-013 but omits FR-012. This means FR-012 cannot be traced backward to its FMEA origin without consulting the forward table.
**Required Resolution:** Add row `| FR-012 | FM-003 (incomplete MR coverage) |` to the FMEA reverse trace table.

### FINDING-4: Behavioral Property Registry Undefined (Completeness — Medium Priority)

**Location:** FR-013 lines 393-412
**Finding:** FR-013 acceptance criterion references "a list of documented behavioral properties for an agent" as the denominator for MR coverage percentage. No requirement defines the format, location, ownership, or initial content of this behavioral property registry. FR-013 is unimplementable without this definition.
**Required Resolution:** Add a requirement (FR-031 or as an acceptance criterion sub-item in FR-013) specifying: the file format for behavioral property registry (e.g., YAML per agent at `tests/prompt-regression/contracts/{agent-id}.yaml`), what constitutes a "documented behavioral property," and who is responsible for maintaining it.

### FINDING-5: Self-Referential IF-005 ADR Source (Internal Consistency — Low Priority)

**Location:** IF-005 line 1260
**Finding:** ADR Source field reads "ADR-001 FR-018 (from this document)" — citing a requirement from this document as an ADR source is circular and meaningless for traceability purposes.
**Required Resolution:** Replace with a direct reference to the ADR-001 section that establishes the CI/CD gate pattern, e.g., "ADR-001 Architecture Diagram 'CI/CD Gate Decision'; ADR-001 L1 Constraints M-003."

---

## Strengths

The following aspects of the deliverable are genuinely strong and should be preserved in revision:

1. **Depth of FMEA coverage.** All 10 failure modes are addressed with explicit requirement mappings, RPN values, and acknowledged residual gaps. FM-007 (highest RPN=432) is correctly identified as structurally irreducible — this is intellectual honesty, not a deficiency.

2. **Acceptance criteria specificity.** Must-priority FRs use concrete, measurable Given/When/Then criteria with named constants (MIN_STATISTICAL_SAMPLE_SIZE, QUALITY_PASS_THRESHOLD), specific file paths, and measurable thresholds. These are among the most implementable requirement acceptance criteria the framework has produced.

3. **Interface specification depth.** Seven interface contracts are defined with data schemas (IF-003, IF-005 include full JSON structures), protocol descriptions, ADR sources, and constraints. IF-002 includes actual Python class signatures. This level of interface specification eliminates implementation ambiguity at layer boundaries.

4. **Evidence chain completeness.** The 22-entry evidence-to-requirements traceability matrix is comprehensive and specific. Every evidence entry traces to the requirements it derives, including appropriate "deferred" notations for Phase E (E-012) work.

5. **Cross-cutting governance requirements.** FR-022 (OSI license verification), FR-023 (UV-only), FR-027 (test case authorship process) translate framework governance rules into harness-specific requirements. This is correct requirements engineering — governance constraints become testable requirements.

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score with specific line references
- [x] Uncertain scores resolved downward (Internal Consistency scored 0.84 not 0.87 due to confirmed naming conflict)
- [x] First-draft calibration considered (0.875 is within the 0.85-0.90 expected range for a first-draft C4 requirements specification of this scope)
- [x] No dimension scored above 0.90 without explicit evidence for that claim
- [x] Completeness scored 0.90 (not higher) despite self-declared PASS checklist — independent verification identified the behavioral property registry gap and test corpus gap not caught by self-review

---

## Session Handoff Schema

```yaml
verdict: REVISE
composite_score: 0.875
threshold: 0.94
weakest_dimension: Internal Consistency
weakest_score: 0.84
critical_findings_count: 2
iteration: 1
improvement_recommendations:
  - "Resolve layer4_stats.py vs stats.py naming conflict in FR-019/FR-030/allocation table"
  - "Escalate NFR-002 priority from Should to Must"
  - "Add FR-012 to FMEA reverse trace table (FM-003 mapping)"
  - "Define behavioral property registry format and location (required by FR-013)"
  - "Remove self-referential IF-005 ADR source; replace with direct ADR-001 citation"
  - "Add NFR Must-priority acceptance criteria in Given/When/Then format"
  - "Add Appendix A: Phase-to-Requirements Map (FR phase delivery alignment)"
  - "Add ADR-001 citation to NFR-008 rationale"
```
