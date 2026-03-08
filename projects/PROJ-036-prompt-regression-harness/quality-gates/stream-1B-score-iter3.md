# Quality Score Report: Stream 1B - System Design with Threat Model (Iteration 3)

## L0 Executive Summary

**Score:** 0.944/1.00 | **Verdict:** PASS | **Weakest Dimension:** Evidence Quality (0.93)
**One-line assessment:** Both iter2 improvement targets are fully resolved -- all ~20 Medium-likelihood threats now have inline justifications, DREAD dimension rationale covers all 9 High-risk threats, and four authoritative external security references (ET-15 through ET-18) are cited with specific section references -- pushing Evidence Quality from 0.90 to 0.93 and clearing both the H-13 threshold (0.92) and the C4 aspirational target (0.94).

---

## Scoring Context

- **Deliverable:** `projects/PROJ-036-prompt-regression-harness/design/system-design.md`
- **Deliverable Type:** Design
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-03-07T02:30:00Z
- **Iteration:** 3 (revised from iter 2 composite 0.937)
- **Prior Score:** 0.937 (iteration 2)

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.944 |
| **Threshold** | 0.92 (H-13); C4 aspirational target 0.94 |
| **Verdict** | PASS |
| **Strategy Findings Incorporated** | No (no adv-executor reports available) |

> **C4 threshold note:** The orchestration plan set a 0.94 aspirational target for C4 work. The composite is 0.9445 (rounded to 0.944), clearing both the SSOT H-13 threshold (0.92) and the C4 aspirational target. Verdict is PASS.

---

## Fix Verification: Iter2 Improvement Targets

| Finding from Iter2 | Status | Evidence |
|--------------------|--------|---------|
| Medium-likelihood threats lack inline justification (~20 threats) | **RESOLVED** | All Medium-likelihood threats now have parenthetical inline justifications in the STRIDE table Likelihood column. Verified: T-05, T-06, T-09, T-12, T-13, T-17, T-18, T-23, T-27, T-31, T-32, T-33, T-36, T-37, T-39 all have rationale text. Low-likelihood threats (T-08, T-10, T-14, T-15, T-16, T-21, T-26) do not require justification at this level. |
| DREAD dimension rationale covers only top 3 of 9 High-risk threats | **RESOLVED** | Lines 1589-1637 provide per-dimension score rationale for all 9 High-risk threats: T-19, T-20, T-02, T-35, T-29, T-28, T-40, T-07, T-22. Each threat has 5 rows (Damage, Reproducibility, Exploitability, Affected Users, Discoverability) with specific rationale text. |
| No external security reference citations | **RESOLVED** | ET-15 through ET-18 added (lines 1742-1745): ET-15 (CIS Docker Benchmark v1.6, sections 4 and 5 with 6 specific sub-sections cited), ET-16 (NIST SP 800-190, sections 3-5.4), ET-17 (OWASP CI/CD Top 10 2023, CICD-SEC-1/-2/-4/-7 cited), ET-18 (GitHub Actions Security Hardening, specific practices). All four map to specific mitigation controls. |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.94 | 0.188 | All 4 layers, 40 threats across 6 surfaces; 6 concrete fixtures; 5 MR tolerances; three secondary gaps persist (YAML sample, MR port, Observability port) |
| Internal Consistency | 0.20 | 0.95 | 0.190 | DREAD ordering mechanically derivable; module boundaries consistent; no new inconsistencies in iter3 additions |
| Methodological Rigor | 0.20 | 0.95 | 0.190 | DREAD dimension rationale now complete for all 9 High-risk threats; external security references add methodological grounding; no sequence diagram remains the one residual gap |
| Evidence Quality | 0.15 | 0.93 | 0.1395 | All three iter2 evidence gaps resolved: Medium-likelihood justifications, full DREAD rationale, four authoritative external references with specific section citations |
| Actionability | 0.15 | 0.94 | 0.141 | No change from iter2; promptfoo YAML sample still absent; all other actionability elements remain fully implemented |
| Traceability | 0.10 | 0.96 | 0.096 | ET-15 through ET-18 add external standard traceability for container and CI/CD controls; 18 evidence entries; 40/40 threat-to-control; minor gap: Observability port |
| **TOTAL** | **1.00** | | **0.9445** | |

**Weighted composite:** 0.188 + 0.190 + 0.190 + 0.1395 + 0.141 + 0.096 = **0.9445**

---

## Detailed Dimension Analysis

### Completeness (0.94/1.00)

**Evidence:**

The iter3 additions (Medium-likelihood justifications, extended DREAD rationale, ET-15 through ET-18) do not address the three secondary completeness gaps identified in iter2. The primary completeness content — four layers, 40 threats across 6 attack surfaces with all 6 STRIDE categories, 6 concrete pytest fixtures, 5 MR tolerances with calibration methodology — remains complete and unchanged.

**Gaps (unchanged from iter2):**

1. **No sample promptfoo YAML test case.** The `ps_researcher.yaml` format remains unspecified. An engineer implementing Layer 1 still cannot determine the exact promptfoo YAML format for provider block, `vars.user_query`, or `type: python` assertion invocation from this design.

2. **No MetamorphicRelationPort protocol.** No formal port interface (analogous to `EvaluationPort`) exists for the MR layer. MR invocation is described via pattern prose only.

3. **Observability port unspecified.** The Langfuse adapter appears in the hexagonal diagram without a protocol definition. Marked optional but architecturally incomplete.

**Assessment:** Score unchanged at 0.94. Iter3 improvements did not close completeness gaps. Three secondary items remain.

**Improvement Path:**

Add a 15-25 line `ps_researcher.yaml` sample under section 2.3. Define `MetamorphicRelationPort` protocol.

---

### Internal Consistency (0.95/1.00)

**Evidence:**

Iter3 additions are internally consistent with the existing framework:

1. The extended DREAD dimension rationale table (T-35 through T-22) uses the same format and scoring conventions as the original top-3 table. Scores are internally consistent with the DREAD summary table: T-35 (Damage=9, R=8, E=5, A=8, D=4 averages to 6.8, confirmed). T-29 (D=9, R=6, E=5, A=9, D=5 averages to 6.8, confirmed). T-28 (D=8, R=5, E=5, A=8, D=6 averages to 6.4, confirmed). T-40 (D=8, R=6, E=5, A=8, D=4 averages to 6.2, confirmed). T-07 (D=8, R=5, E=6, A=7, D=5 averages to 6.2, confirmed). T-22 (D=8, R=6, E=5, A=8, D=4 averages to 6.2, confirmed). All averages are consistent with the DREAD summary table values.

2. Medium-likelihood justifications are consistent with the existing risk rating methodology. All justifications explain why a threat is rated M (not H, not L), aligning with the impact/likelihood/risk table structure.

3. ET-15 through ET-18 reference controls that are already in the Controls Index (MC-07 through MC-14, MC-28, MC-29, MC-31, MC-33). No new controls claimed without prior definition.

**Remaining gap (unchanged):** The `EvaluationReport` dataclass is mutable (`@dataclass` not `@dataclass(frozen=True)`) while all peer types are frozen. This is documented as intentional in the iter2 report but unexplained in the design document itself.

**Assessment:** Score unchanged at 0.95. No new inconsistencies; no new consistency gains beyond confirming iter3 additions are coherent.

---

### Methodological Rigor (0.95/1.00)

**Evidence:**

Two genuine rigor improvements in iter3:

1. **DREAD dimension rationale now complete for all 9 High-risk threats.** Lines 1591-1637 provide a 45-row table (9 threats x 5 dimensions) with specific rationale for each dimension score. This addresses the primary remaining rigor gap from iter2 (which noted: "DREAD dimension rationale only for top 3 threats"). The rationale is specific and defensible: T-35 Reproducibility=8 "Crafting constant or zero-difference arrays is deterministic once the attacker understands the Wilcoxon test"; T-07 Exploitability=6 "Requires knowledge of promptfoo's YAML processing and `file://` handler; documented in promptfoo docs." This level of specificity satisfies the methodological standard for DREAD risk scoring.

2. **External security references add methodological grounding.** ET-15 through ET-18 ground the container hardening choices (MC-07 through MC-14) in CIS Docker Benchmark v1.6 and NIST SP 800-190, and the CI/CD controls (MC-28, MC-29, MC-31, MC-33) in OWASP CI/CD Top 10 and GitHub Actions Security Hardening. This transforms the security control selection from design judgment into methodology traceable to established standards.

**Remaining gap:** No formal sequence diagram. This was iter2's primary remaining rigor gap and persists. The ASCII flow diagrams in section 1.5 approximate a sequence diagram but lack actor lifelines, message labels with data types, and return arrows. For a C4 design, this remains a methodological gap.

**Assessment:** Score improves from 0.94 to 0.95. The DREAD completion is a genuine rigor achievement. The sequence diagram gap is the remaining limiter.

---

### Evidence Quality (0.93/1.00)

**Evidence:**

All three iter2 evidence quality gaps are now resolved:

1. **Medium-likelihood threats now have inline justification.** Every threat with Likelihood=M carries a parenthetical explanation immediately in the Likelihood cell. Examples: T-06 "no structural limit exists until MC-06 is implemented; a single PR can add arbitrary YAML files"; T-12 "environment variables are visible to all processes in the container namespace; a compromised npm dependency could read process environment"; T-33 "GitHub Actions workflows default to broad permissions unless explicitly restricted; developers frequently copy workflow templates without narrowing the permissions block." The justifications are specific, not generic, and tied to implementation details of this specific system. Total Medium-likelihood threats with justification: approximately 14 (T-05, T-06, T-09, T-12, T-13, T-17, T-18, T-23, T-27, T-31, T-32, T-33, T-36, T-37, T-39) plus the High-rated threats that have "Likelihood rationale:" inline text (T-19, T-20, T-22, T-25, T-28, T-29, T-34, T-35, T-40).

2. **DREAD dimension rationale covers all 9 High-risk threats.** Each of the 6 previously-unrated threats (T-35, T-29, T-28, T-40, T-07, T-22) now has 5-dimension justification. The rationale is specific and appropriately calibrated: T-28 Reproducibility=5 "Depends on misconfiguration (using `pull_request_target` instead of `pull_request`); not always reproducible" correctly distinguishes this from T-29 Reproducibility=6 (workflow modification is more reliably exploitable).

3. **Four external security references added (ET-15 through ET-18).** Each entry follows the established format (Evidence ID, Source, Specific Location, Design Element Supported) and maps to specific controls. ET-15 cites CIS Docker Benchmark v1.6 sections 4 and 5 with six sub-sections named and mapped to MC-07 through MC-14. ET-16 cites NIST SP 800-190 sections 3-5.4 mapped to the AS-2 threat model rationale. ET-17 cites four OWASP CI/CD Top 10 items mapped to four specific GHA controls. ET-18 cites GitHub's official hardening documentation mapped to event type selection, CODEOWNERS enforcement, secret masking, and permissions. All four are authoritative sources used precisely.

**Remaining gaps:**

1. **Observability port (Langfuse) has no evidence entry.** The optional Langfuse adapter appears in the hexagonal diagram and outbound ports section without traceability to a requirement or architectural decision.

2. **Statistical methodology external references.** The Wilcoxon signed-rank test and Wilson score interval selections are referenced to ADR-001 but not to external statistical literature (e.g., Hollander & Wolfe nonparametric statistics; Wilson 1927 original paper; or standard references). This is a minor gap given that these are well-established methods.

**Assessment:** Evidence Quality improves from 0.90 to 0.93. The three primary gaps are closed. Remaining gaps are minor (optional port, statistical citations). The 0.93 score reflects "most claims with credible citations" -- the large improvement from three specific gaps being closed, with two smaller residual items preventing 0.95+.

---

### Actionability (0.94/1.00)

**Evidence:**

No iter3 changes address actionability. The deliverable's actionability remains as assessed in iter2:

- All 6 pytest fixtures are fully implemented with concrete bodies, environment variable resolution, and documented exception paths.
- MR tolerance values (0.05, >=0.40 Cohen's d, 0.03, 0.05, 0.06) are specified with derivation rationale.
- DREAD priority ordering is mechanically derivable from the documented formula.
- Docker invocation contract (volume mounts, flags) is fully specified.
- GHA workflow inputs/outputs are documented.

**Remaining gap (unchanged):**

The `ps_researcher.yaml` promptfoo test case sample remains absent. An engineer implementing Layer 1 cannot determine from this design the format for the `providers:` block (which Anthropic model, which SDK version), the `tests:` block structure, the `vars` field conventions, or the `assert: - type: python` assertion provider invocation syntax. This is a real gap for Layer 1 implementation.

**Assessment:** Score unchanged at 0.94. The YAML sample gap persists as the sole actionability limiter.

---

### Traceability (0.96/1.00)

**Evidence:**

ET-15 through ET-18 are a genuine traceability addition:

1. **Container hardening controls now trace to external standards.** Previously MC-07 through MC-14 traced to ADR-001 Consequences (ET-05, ET-14) but lacked external standard authority. ET-15 (CIS Docker Benchmark v1.6) and ET-16 (NIST SP 800-190) close this gap, providing the authoritative source for why `--cap-drop=ALL`, `--security-opt=no-new-privileges:true`, read-only filesystem, and single-process container patterns were selected.

2. **CI/CD workflow security controls now trace to external standards.** MC-28, MC-29, MC-31, MC-33 previously had no external citation. ET-17 (OWASP CI/CD Top 10) maps each control to a specific risk category; ET-18 (GitHub Actions Security Hardening) provides official source documentation for the implementation choices.

3. **Total evidence entries: 18.** Coverage spans: design decisions (ET-01 through ET-11), framework rules (ET-12), metamorphic relations (ET-13), Docker threat model (ET-14), and external security standards (ET-15 through ET-18). All primary design elements have at least one traceable evidence entry.

4. **Threat-to-control mapping remains 40/40 complete.** No change from iter2.

**Remaining gap:** The Observability port (Langfuse, optional) still lacks a traceability entry. This is the single remaining gap in otherwise comprehensive coverage.

**Assessment:** Score improves from 0.95 to 0.96. The addition of four external reference entries with specific section citations is a genuine traceability gain. The remaining gap (Observability port) is minor given the optional nature of that component.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Actionability | 0.94 | 0.97 | Add a 15-25 line sample `ps_researcher.yaml` promptfoo test case under section 2.3 showing: `providers:` block (Anthropic Claude model, SDK version), `tests:` block with one test case, `vars.user_query` field, and `assert:` block with `type: python` assertion invoking the custom assertion provider |
| 2 | Completeness | 0.94 | 0.96 | Define `MetamorphicRelationPort` protocol analogous to `EvaluationPort` (formal typed port contract for MR layer invocation) |
| 3 | Methodological Rigor | 0.95 | 0.97 | Add formal sequence diagram for end-to-end evaluation flow (GHA trigger -> Layer 4 verdict -> PR comment) with actor lifelines and message labels |
| 4 | Internal Consistency | 0.95 | 0.96 | Add explanatory comment in `EvaluationReport` documenting why it is not frozen (timestamp and smoke_label fields are set post-construction), clarifying the intentional asymmetry with all other types in types.py |
| 5 | Evidence Quality | 0.93 | 0.95 | Add ET-19 tracing Wilcoxon signed-rank test selection to a standard statistical reference (e.g., Hollander & Wolfe, Nonparametric Statistical Methods, or the scipy.stats.wilcoxon documentation with citation to its theoretical basis) |
| 6 | Completeness | 0.94 | 0.95 | Add `ObservabilityPort` protocol definition for the Langfuse adapter, even if brief; or mark it explicitly as "deferred to implementation phase" with a note |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing weighted composite
- [x] Evidence documented for each score with specific line references
- [x] Uncertain scores resolved downward (Evidence Quality scored at 0.93, not 0.95, because Observability port and statistical method citations remain absent)
- [x] Iteration-3 status considered: this is a third-iteration revised deliverable; scores reflect actual current state, not effort
- [x] No dimension scored above 0.96 without documented evidence
- [x] All three iter3 fixes independently verified against the document rather than assumed from revision claim
- [x] DREAD dimension scores independently cross-checked: all 9 threat averages confirmed against the DREAD summary table
- [x] Composite computed mechanically (0.9445), not anchored to prior score (0.937)
- [x] Completeness held at 0.94 (unchanged) because iter3 additions did not close the YAML/MR-port/Observability completeness gaps
- [x] Actionability held at 0.94 (unchanged) because the promptfoo YAML sample gap persists
- [x] Evidence Quality scored at 0.93 (not 0.95) because two minor gaps remain despite three primary gaps closing

---

## Session Context (Orchestrator Handoff)

```yaml
verdict: PASS
composite_score: 0.9445
threshold: 0.92
weakest_dimension: Evidence Quality
weakest_score: 0.93
critical_findings_count: 0
iteration: 3
improvement_recommendations:
  - "Add sample ps_researcher.yaml promptfoo test case (15-25 lines) in section 2.3"
  - "Define MetamorphicRelationPort protocol analogous to EvaluationPort"
  - "Add formal sequence diagram for end-to-end evaluation flow (GHA trigger -> Layer 4 verdict)"
  - "Add explanatory comment in EvaluationReport explaining why it is not frozen"
  - "Add ET-19 tracing Wilcoxon test selection to standard statistical reference"
  - "Add ObservabilityPort protocol definition or explicitly defer to implementation phase"
```
