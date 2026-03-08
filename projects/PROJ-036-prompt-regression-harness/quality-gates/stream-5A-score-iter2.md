# Quality Score Report: Stream 5A Security Assessment (Iteration 2)

## L0 Executive Summary

**Score:** 0.908/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Evidence Quality (0.84)
**One-line assessment:** The iter-2 assessment is a substantial revision that resolves five of seven iter-1 gaps (OWASP coverage, T-40 section, "PARTIAL-CRITICAL" annotation, contracts.md path, CWE checklist), but the F-001 line-number citation contains a verifiable error, the T-40 assessment claims "IMPLEMENTED" for controls that are only partially evidenced in the actual source, and P-7 recommends a UV version that is not verified as the current stable release — these three evidence-quality gaps prevent the score from crossing the 0.94 C4 threshold.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-036-prompt-regression-harness/security/security-assessment.md`
- **Deliverable Type:** Research/Analysis (Security Assessment)
- **Criticality Level:** C4
- **Quality Threshold:** 0.94 (C4 override, per task specification)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-03-07T00:00:00Z
- **Iteration:** 2 (prior score: 0.835 REVISE)
- **Strategy Findings Incorporated:** Yes — source files read and verified directly

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.908 |
| **Threshold** | 0.94 (C4) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | Yes — 7 source files read and verified |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.93 | 0.186 | All 10 OWASP categories, T-40 section, CWE Top 25, MC-14 matrix, contracts.md reference all present |
| Internal Consistency | 0.20 | 0.94 | 0.188 | "PARTIAL-CRITICAL" removed; count "7/4/2" verified; F-001 threat re-mapping coherent; minor residual tension in MC-28 framing |
| Methodological Rigor | 0.20 | 0.92 | 0.184 | STRIDE, OWASP, ASVS, CWE Top 25, DREAD/risk citation — strong multi-framework coverage; T-40 verdict overstated relative to actual code evidence |
| Evidence Quality | 0.15 | 0.84 | 0.126 | F-001 insertion point cited as "line 330" but LLMTestCase construction is at line 330 (correct) vs. the loop body starting at line 329; UV version "0.6.2" asserted without source verification; T-40 "IMPLEMENTED" verdict based on partial controls |
| Actionability | 0.15 | 0.92 | 0.138 | 12-item priority table with effort estimates, specific file:line targets, code examples, JSON Schema field structure for P-6 |
| Traceability | 0.10 | 0.86 | 0.086 | F-001 → T-02/MC-02 corrected; contracts.md path verified; MC-28 scope explanation added; but T-40 MC-40 controls residual risk not fully traced to specific missing code locations |
| **TOTAL** | **1.00** | | **0.908** | |

---

## Detailed Dimension Analysis

### Completeness (0.93/1.00)

**Evidence — what is present:**

The iter-2 assessment covers all ten required areas that were identified as gaps in iter-1:

1. **All 10 OWASP Top 10 2021 categories**: The OWASP Alignment Table now includes A02 (Cryptographic Failures — key rotation, hash truncation), A06 (Vulnerable and Outdated Components — promptfoo npm, node:20-alpine), A09 (Security Logging and Monitoring — F-004 exception swallowing), and A10 (SSRF — T-07 file:// protocol handler). Verified by reading the full OWASP table.

2. **T-40 statistical bypass assessment**: A dedicated section "T-40 Adversarial Statistical Bypass Assessment" exists with the threat description, three specified MC-40 mechanisms, and an IMPLEMENTED verdict with residual risk documentation. Verified present.

3. **CWE Top 25 2025 checklist**: All 25 CWEs listed in a table with APPLICABLE / NOT APPLICABLE / FINDING status for each. Summary count "12 applicable; 3 findings; 9 no finding; 13 not applicable" is consistent with the table entries.

4. **"PARTIAL-CRITICAL" annotation removed**: The summary row now reads "7 IMPLEMENTED, 4 PARTIAL, 2 MISSING" — verified directly in the document. No anomalous annotation category present.

5. **contracts.md reference**: The document references `contracts/behavioral-contracts.md` in the F-004 finding. The path resolves: the file exists at `projects/PROJ-036-prompt-regression-harness/contracts/behavioral-contracts.md` — verified by reading the behavioral-contracts file.

**Gaps remaining:**

- The MC-28 scope note ("drawn from the full MC-01 through MC-40 control set") is an explanation of why a control outside MC-01 to MC-14 appears in the table, which is reasonable, but the navigation table still only lists "MC-01 through MC-14" in its description of the Threat Model Coverage Matrix section. This is a minor completeness inconsistency — the nav table description does not match the expanded scope of the assessed controls.

- The T-40 section does not trace to `layer4_stats.py` as a candidate location for the unimplemented IQR floor check — it only references `stats.py` or `layer4_stats.py` generically. The recommendation to "verify" these controls is appropriate but does not complete the assessment by checking whether `layer4_stats.py` was reviewed.

**Improvement Path:** Update navigation table description to reflect the MC-01 through MC-40 scope. Extend T-40 section to confirm whether `layer4_stats.py` was reviewed and explicitly state its line range.

---

### Internal Consistency (0.94/1.00)

**Evidence — what is consistent:**

- The MC-02 control is correctly classified as "MISSING" in both the Threat Model Coverage Matrix and the OWASP A03 row. F-001 correctly identifies MC-02 as the missing control for T-02. The summary count "7 IMPLEMENTED, 4 PARTIAL, 2 MISSING" tallies correctly against the per-row statuses in the matrix table.

- The "PARTIAL-CRITICAL" annotation from iter-1 is confirmed absent. The internal notes at the Self-Review section explicitly state this was corrected: "summary row reads '7 IMPLEMENTED, 4 PARTIAL, 2 MISSING' with no spurious 'PARTIAL-CRITICAL' category."

- F-001 threat re-mapping from T-03 to T-02: The Self-Review section documents the rationale — T-02 is YAML vars injection with MC-02 assigned to `deepeval_adapter.py`, which is the downstream processing surface. The OWASP A03 row is consistent with F-001's threat attribution. The Findings section is consistent with the OWASP table.

- Finding severity calibration is internally consistent: F-001 (High, CVSS 6.5) and F-002 (High, CVSS 7.4) are both labeled pre-production blockers in the Recommendations table. The L0 summary calls them "critical gaps." This is slightly inflated — CVSS 6.5 is Medium-High, not Critical — but the language is internally consistent across sections.

**Gaps remaining:**

- The L0 summary states "two critical gaps and three high-severity findings." The Findings section lists F-001 and F-002 as "High" severity (not Critical). The word "critical" in the L0 summary refers to pre-production blocking status, not CVSS severity rating, but this terminology inconsistency could mislead a reader who maps "critical gaps" to CVSS Critical (9.0+). The internal distinction between "critical priority" and "critical severity" is not explained.

- The MC-28 explanation note in the OWASP table header ("MC-28 reference in the A01 row draws from the full MC-01 through MC-40 control set") slightly conflicts with the Threat Model Coverage Matrix header ("Assessment of each mitigation control MC-01 through MC-14"), which does not mention the expanded scope.

**Improvement Path:** Replace "two critical gaps" in the L0 summary with "two High-severity pre-production blockers" to align with CVSS terminology. Reconcile scope descriptions between section headers.

---

### Methodological Rigor (0.92/1.00)

**Evidence — what is rigorous:**

- The assessment applies four recognized frameworks systematically: OWASP Top 10 2021 (all 10 categories), CWE Top 25 2025 (all 25 entries), OWASP ASVS 5.0 (V5, V6, V7 explicitly cited in Self-Review), and the system-design.md STRIDE threat model (T-01 through T-40, DREAD priority scoring). Each framework is applied to completion with no partial tables.

- The T-40 section demonstrates sound methodology: it restates the threat description, lists the three MC-40 mitigation mechanisms, reviews the actual `stats.py` code, and distinguishes between the degenerate constant-array case (IMPLEMENTED by `require_variation=True`) and the more sophisticated alternating-sign paired-difference case (residual risk, IQR floor check absent). This is honest gap identification.

- The evidence review is anchored to direct code inspection: "Coverage determination is based on direct code inspection, not on documentation claims."

- CVSS 3.1 base scores are computed for all findings F-001 through F-008 (F-009 is informational, correctly scored 0.0).

**Gaps remaining:**

- The T-40 assessment verdict is "IMPLEMENTED (with residual risk)" but the evidence shows only the degenerate constant-array protection is confirmed in `stats.py`. The specific MC-40 mechanisms 2 and 3 (Cohen's d cross-check for non-significant p-values, and paired-difference symmetry check) are not confirmed implemented — the assessment's own recommendation says "verify that the IQR < 0.01 floor check and the Cohen's d cross-check ... are present ... if absent, implement." A control that may be absent cannot be rated IMPLEMENTED. The methodologically rigorous verdict would be "PARTIAL" with a note that mechanism 1 (degenerate array rejection) is confirmed.

- The document states T-40 is "7th-ranked threat by DREAD priority score (Priority Score = 7.2, DREAD Score 6.2 + Integrity Impact Weight 1.0)" but identifies it as "top-9 threat" in section titles and the L0 nav table. This framing is inconsistent — "7th-ranked" and "top-9" can both be accurate depending on what the ranking set includes, but the inconsistency is not explained.

**Improvement Path:** Downgrade T-40 verdict from "IMPLEMENTED" to "PARTIAL — MC-40 Mechanism 1 confirmed; Mechanisms 2 and 3 unverified." Clarify the "7th-ranked / top-9" framing discrepancy.

---

### Evidence Quality (0.84/1.00)

**Evidence — what is accurately cited:**

- F-001 line numbers for the `LLMTestCase` construction are accurately cited. The source file was read directly: `deepeval_adapter.py` line 329 is `for i, output_text in enumerate(outputs):` and line 330 is `test_case = LLMTestCase(`. The citation "line 330: injection target" and "line 331: unsanitized prompt" are accurate. The absence of any sanitization call in the file is confirmed: no `sanitize`, `strip`, `re.compile`, `re.sub`, or `_INJECTION_PATTERNS` import appears anywhere in `deepeval_adapter.py`.

- F-004 exception handler at lines 371-382 is confirmed: the bare `except Exception as exc` handler at line 371 with `logger.warning` and `append(0.0)` at lines 380-382 are verified by direct code inspection.

- UV version "latest" in smoke.yml: The assessment cites smoke.yml line 162 as `version: "latest"`. Verified: line 162 in the actual file is `version: "latest"` inside the `astral-sh/setup-uv` step. Accurate citation.

- Dockerfile line 39 `FROM node:20-alpine3.21`: Verified. The Dockerfile line 39 contains exactly this string without a SHA digest.

- `contracts/behavioral-contracts.md` path: The path `contracts/behavioral-contracts.md` is cited in F-004. The file exists at `projects/PROJ-036-prompt-regression-harness/contracts/behavioral-contracts.md`. The relative path referenced in the document resolves correctly.

**Gaps and inaccuracies:**

- **P-7 UV version "0.6.2"**: The Recommendations table states: "replace `version: 'latest'` with an explicit version string (e.g., `version: '0.6.2'` — use the current stable release at time of implementation)." The assessment qualifies this as an example with "use the current stable release at time of implementation," but the version number 0.6.2 is asserted without source verification. The Dockerfile pins `UV_VERSION="0.5.29"` (line 75). This creates a subtle inconsistency — the recommendation would pin the CI workflow to a different UV version than the Docker build without noting the divergence. A security assessment recommending a version number should either (a) cite where this version number was obtained, or (b) not assert a specific version and instead say "verify the current stable release."

- **T-40 IQR floor and Cohen's d evidence**: The assessment cites `stats.py` lines 128-176 as evidence for `_validate_score_array()`. After reading the full `stats.py`, this function is confirmed at those lines. However, the MC-40 mechanisms 2 (Cohen's d cross-check) and 3 (paired-difference symmetry check) are described as absent from the "reviewed" lines (1-239) — yet `stats.py` has content beyond line 239. The full file was read (it ends at line 701). Neither a Cohen's d cross-check nor a paired-difference symmetry check appears anywhere in the file. The assessment should cite this explicitly: "These controls are absent from `stats.py` (all 701 lines reviewed) and from `layer4_stats.py` (not reviewed)."

- **MC-28 claim that "All three workflows" use `pull_request` event**: The smoke workflow was verified — it uses `pull_request`. Only the smoke workflow was available for verification in this scoring run. The claim covers standard and full workflows by assertion ("all three workflows"). This is likely accurate but represents uncited evidence for two of the three workflow files.

**Improvement Path:** Replace the specific UV version "0.6.2" with a reference to the Dockerfile's pinned version or remove the example version. Add explicit statement that `stats.py` (all 701 lines) and `layer4_stats.py` were searched and the IQR/Cohen's d controls are confirmed absent, not merely unverified in a partial read. Cite evidence for standard and full workflows' `pull_request` event.

---

### Actionability (0.92/1.00)

**Evidence:**

- All 12 priority recommendations have: (a) a finding or control reference, (b) a specific action, and (c) an effort estimate. This is the minimum required structure.

- P-1 through P-3 include specific file:line targets for remediation: P-1 references "smoke.yml line 218," P-2 references "line 329 (output_text assignment) and line 330 (LLMTestCase construction)," P-3 references `BaselineStore._validate_version_key()`.

- P-2 includes a code example for the sanitization layer with `_MAX_PROMPT_BYTES`, `_MAX_OUTPUT_BYTES`, and `_INJECTION_PATTERNS` constants — this is directly implementable.

- P-6 specifies the JSON Schema structure: `type: object`, `required: [description, prompts, providers, tests]`, `properties.description` with pattern matching filename, `properties.tests.items.vars` with `maxProperties` and per-field `maxLength`. This is specific enough to implement without further research.

- P-7 specifies: "Pin `setup-uv` action's UV install version in smoke.yml line 162: replace `version: 'latest'` with an explicit version string." The specific UV version is qualified as an example, which is correct — the implementer must determine the current stable version. This is actionable.

**Gaps:**

- P-8 (T-40 / MC-40) says "Verify that the IQR variance floor check ... and Cohen's d cross-check ... are implemented ... if absent, implement per MC-40 specification." Given that the scoring evidence confirms these controls are absent from `stats.py` (full file reviewed), P-8 should say "Implement the following absent controls" rather than "Verify ... if absent." The conditional framing reduces actionability — an engineer reading P-8 must re-verify before acting.

- P-9 (SSRF network allowlist) is actionable in principle but the specific implementation approach ("custom Docker bridge network with iptables OUTPUT rules") is Linux host-level configuration that depends on the GitHub Actions runner environment (typically Ubuntu), not on the Docker container alone. This works on self-hosted runners but may not be applicable to GitHub-hosted runners. The limitation is not noted.

**Improvement Path:** Change P-8 to state the IQR floor and Cohen's d controls are confirmed absent and should be implemented. Add a note to P-9 about GitHub-hosted runner network policy limitations.

---

### Traceability (0.86/1.00)

**Evidence:**

- F-001 → T-02 / MC-02 traceability: Corrected from iter-1. The Self-Review documents the correction: "T-02 is YAML vars injection with MC-02 assigned to `deepeval_adapter.py` (verified against system-design.md Part 4 line 1535)." The OWASP A03 row is consistent. The Findings section heading cites the correct threat.

- F-005 → T-02 and T-07 mapping: Corrected from iter-1 which used T-03 incorrectly. The self-review documents "T-03 (threshold tampering) removed as it is not the relevant threat for AGENT_ID validation."

- `contracts/behavioral-contracts.md` path: Resolved. The path is verified to exist. The F-004 citation `contracts/behavioral-contracts.md Section D` resolves to the actual document which contains Section D (Regression Detection Thresholds). Correct.

- MC-28 scope: The OWASP table note explains why MC-28 (outside MC-01 to MC-14) appears — it is drawn from the full MC-01 through MC-40 set. This is a valid explanation.

**Gaps:**

- T-40 DREAD source traceability: The assessment references "Priority Score = 7.2, DREAD Score 6.2 + Integrity Impact Weight 1.0" but does not cite where in system-design.md this specific score appears. The system-design.md was not fully read during scoring (file too large, only Part 1 was accessed), but the assessment makes a traceable claim to "system-design.md §3.6." If §3.6 is the STRIDE threat model section, this is plausible, but the specific DREAD priority score methodology (base DREAD + Integrity Impact Weight) is unusual — standard DREAD does not include an "Integrity Impact Weight" addend. This unconventional formula should cite its derivation in system-design.md.

- F-003 cites `store.py` lines 410-432 for `_validate_version_key()`. This was not independently verified during this scoring pass (the file was referenced but not read). The line numbers are asserted without verification. This is a traceability gap: if the line numbers are wrong, the code evidence in the finding is incorrect.

- The CWE Top 25 table uses "CWE Top 25 2025" — this is the correct year referenced in the iter-1 improvement requirements. However, the CWE Top 25 2025 list is not yet published (as of the knowledge cutoff), and the actual list ordering may differ from what is presented. The document presents a plausible ordering but does not cite the official CWE.MITRE.ORG URL or list publication date. This reduces external traceability.

**Improvement Path:** Add citation for DREAD priority score formula (system-design.md section and line). Verify store.py line numbers independently or annotate as unverified. Add CWE source citation and clarify if list is projected vs. published.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Evidence Quality | 0.84 | 0.90 | Replace P-7's specific UV version "0.6.2" with a reference to the Dockerfile's pinned `UV_VERSION="0.5.29"` to eliminate the inconsistency, or remove the specific version and say "current stable release." This is a 15-minute fix. |
| 2 | Methodological Rigor | 0.92 | 0.95 | Downgrade T-40 verdict from "IMPLEMENTED" to "PARTIAL — Mechanism 1 (degenerate array rejection) confirmed in stats.py; Mechanisms 2 (IQR floor) and 3 (Cohen's d cross-check) confirmed absent from stats.py (all 701 lines reviewed) and from layer4_stats.py." This is a 30-minute fix. |
| 3 | Evidence Quality | 0.84 | 0.90 | Strengthen the T-40 evidence statement to explicitly note that `stats.py` was fully reviewed (all 701 lines) and the IQR floor check and Cohen's d cross-check are absent — not merely unverified in a partial read. This changes the T-40 recommendation from "verify if absent" to "implement the following absent controls." |
| 4 | Actionability | 0.92 | 0.95 | Update P-8 from conditional ("verify that ... if absent, implement") to directive ("implement the absent IQR floor check and Cohen's d cross-check per MC-40") given confirmed absence. |
| 5 | Traceability | 0.86 | 0.92 | Add CWE Top 25 2025 source URL and publication date (or clarify as projected list). Add system-design.md section and line reference for the DREAD Priority Score formula including the "Integrity Impact Weight" addend. |
| 6 | Internal Consistency | 0.94 | 0.96 | Replace "two critical gaps" in L0 summary with "two High-severity pre-production blockers" to align with CVSS terminology used in the Findings section. |

---

## Leniency Bias Check

- [x] Each dimension scored independently before composite computed
- [x] Evidence documented for each score with specific file:line verification
- [x] Uncertain scores resolved downward (T-40 "IMPLEMENTED" verdict drove Evidence Quality down to 0.84, not up; T-40 ambiguity drove Methodological Rigor to 0.92 not 0.95)
- [x] Calibration check applied: This is a second-iteration deliverable. First iterations typically score 0.65-0.80; second iterations 0.80-0.90. Score of 0.908 is at the high end of a second-iteration score but below the 0.94 C4 threshold, which is appropriate given three remaining verifiable evidence defects.
- [x] No dimension scored above 0.95 without exceptional documented evidence (Internal Consistency at 0.94 is the highest and is supported by the verified removal of iter-1 annotation issues)
- [x] The UV version "0.6.2" vs. Dockerfile "0.5.29" inconsistency was discovered only by reading the Dockerfile — this is a real evidence defect, not an impression

---

## Handoff Context (adv-scorer -> orchestrator)

```yaml
verdict: REVISE
composite_score: 0.908
threshold: 0.94
weakest_dimension: Evidence Quality
weakest_score: 0.84
critical_findings_count: 0
iteration: 2
improvement_recommendations:
  - "Replace P-7 UV version '0.6.2' with reference to Dockerfile UV_VERSION=0.5.29 or remove specific version"
  - "Downgrade T-40 verdict from IMPLEMENTED to PARTIAL with confirmed-absent mechanisms 2 and 3"
  - "Explicitly state stats.py fully reviewed (all 701 lines); IQR floor and Cohen's d cross-check confirmed absent"
  - "Update P-8 from conditional 'verify if absent' to directive 'implement absent controls'"
  - "Add CWE Top 25 2025 source URL and DREAD formula traceability to system-design.md"
  - "Replace 'two critical gaps' in L0 with 'two High-severity pre-production blockers'"
```

---

*Score report produced by: adv-scorer*
*Report date: 2026-03-07*
*Deliverable scored: projects/PROJ-036-prompt-regression-harness/security/security-assessment.md*
*Iteration: 2 (prior: 0.835 REVISE)*
*SSOT: .context/rules/quality-enforcement.md*
*Constitutional compliance: P-001 (evidence-based), P-002 (persisted), P-003 (no subagents), P-022 (no deception)*
