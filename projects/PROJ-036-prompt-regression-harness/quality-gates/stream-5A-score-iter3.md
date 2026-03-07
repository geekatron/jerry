# Quality Score Report: Stream 5A Security Assessment (Iteration 3)

## L0 Executive Summary

**Score:** 0.932/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Evidence Quality (0.88)
**One-line assessment:** The three iter3 surgical fixes are all factually verified against source files — T-40 verdict correctly changed to PARTIAL, UV version correctly stated as 0.5.29, P-8 correctly changed to imperative — but a metadata inconsistency (header still reads "Iteration: 2") and a minor unresolved Evidence Quality gap (T-40 section claims IQR check absent but does not confirm Mechanism 1 explicitly labelled as "IQR variance floor" per the T-40 body's own enumeration) prevent this from reaching the 0.94 threshold.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-036-prompt-regression-harness/security/security-assessment.md`
- **Deliverable Type:** Analysis (Security Assessment)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-03-07T00:00:00Z
- **Iteration:** 3 (iter1: 0.835, iter2: 0.908)
- **Prior Verdict:** REVISE (iter2)

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.932 |
| **Threshold** | 0.94 (C4, custom) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No — code verified directly |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.95 | 0.190 | All MC-01–MC-14 assessed; all OWASP Top 10 covered; all 25 CWE Top 25 2025 checked; T-40 dedicated section; 9 findings F-001–F-009; 12 prioritized recommendations. One structural incompleteness: iter header not updated to "Iteration: 3." |
| Internal Consistency | 0.20 | 0.91 | 0.182 | All verdict classifications consistent throughout; summary row "7 IMPLEMENTED, 4 PARTIAL, 2 MISSING" matches individual MC rows; severity labels align with CVSS scores; P-7 UV version (0.5.29) now correctly matches Dockerfile line 75. One inconsistency: document header still reads "Iteration: 2" while content reflects iter3 changes. |
| Methodological Rigor | 0.20 | 0.95 | 0.190 | Full 701-line review of stats.py confirmed and cited; explicit line-number evidence for all findings; DREAD scoring used for T-40 prioritization; CWE Top 25 2025 systematically applied; OWASP ASVS V5/V6/V7 addressed; threat-model correlation against MC-01–MC-40; CVSS 3.1 base scores present for all findings. |
| Evidence Quality | 0.15 | 0.88 | 0.132 | F-001 insertion point confirmed at deepeval_adapter.py lines 329–333 (verified by direct file read — no sanitization, no re import, raw strings passed to LLMTestCase). F-002 verified: Dockerfile line 39 tag-only, smoke.yml line 218 :latest, UV_VERSION="0.5.29" at Dockerfile line 75 correctly cited. T-40 "PARTIAL" verdict supported: IQR grep confirms zero matches across 701 lines. Minor gap: T-40 evidence paragraph at line 561 labels MC-40 Mechanism 1 as "IQR variance floor check (MC-40 Mechanism 1)" but the preceding threat description at line 544 labels it "Variance floor enforcement: reject score arrays where IQR < 0.01" — the cross-reference is clear but the numbering alignment between the threat description list and the confirmed-absent list is slightly inconsistent (absent list numbers 1/2/3 map to threat list items 1/2/3, but threat list item 1 is "Variance floor" while absent list item 1 is "IQR variance floor check" — a minor labeling gap, not an error). |
| Actionability | 0.15 | 0.96 | 0.144 | P-1 through P-12 priority-ordered with effort estimates; P-1 and P-2 explicitly marked as pre-production blockers; P-7 now correctly specifies version 0.5.29 with an exact file:line reference; P-8 now imperative ("Implement the following absent controls") with three numbered sub-items; code examples present for F-001, F-002, F-003, F-004, F-005, F-007, F-008, F-009. Remediation for F-003 correctly references VersionKey.from_string() import path. |
| Traceability | 0.10 | 0.94 | 0.094 | Each finding traces to: a CWE, CVSS base score, threat ID (T-xx), requirement (FR-xx or MC-xx), affected file with line numbers; S-010 self-review table cross-references each traceability claim. MC-28 citation in OWASP table explained as drawn from full MC-01–MC-40 set. One minor gap: F-004 threat citation is "T-35 (Adversarial score sequences, indirectly)" — the "indirectly" qualifier is accurate but leaves the traceability chain slightly loose compared to direct-threat mappings in other findings. |
| **TOTAL** | **1.00** | | **0.932** | |

---

## Detailed Dimension Analysis

### Completeness (0.95/1.00)

**Evidence:**
- All 14 threat model controls (MC-01 through MC-14) are assessed in the Threat Model Coverage Matrix with explicit IMPLEMENTED/PARTIAL/MISSING status and code-level evidence.
- All 10 OWASP Top 10 2021 categories addressed in the OWASP Alignment Table.
- All 25 CWE Top 25 2025 entries systematically checked in the CWE Checklist appendix (12 applicable, 13 not applicable).
- Dedicated T-40 section provides 7th-ranked DREAD threat assessment.
- Nine findings (F-001 through F-009) spanning Critical, High, Medium, Low, and Info severities.
- Twelve prioritized recommendations (P-1 through P-12) with effort estimates.
- Supply Chain Assessment, Container Security Assessment, and Runtime Hardening sections each present.
- S-010 self-review table cross-checks all completeness dimensions.

**Gaps:**
- Document header reads "Iteration: 2 (revised from iter 1 score 0.835 REVISE)" — this was not updated when the iter3 surgical fixes were applied. A reader consulting the header in isolation would undercount the revision history by one iteration. This is a metadata completeness gap, not a content gap.
- The Self-Review S-010 table's T-40 row still reads "PASS — dedicated T-40 section with IMPLEMENTED verdict" at line 639, which conflicts with the body verdict of "PARTIAL." This is an S-010 internal inconsistency that also creates a completeness gap in the self-review's own accuracy.

**Improvement Path:**
- Update document header to "Iteration: 3 (revised from iter 2 score 0.908 REVISE)."
- Update S-010 T-40 row to reflect the PARTIAL verdict: "PASS — dedicated T-40 section with PARTIAL verdict, 3 absent MC-40 mechanisms confirmed and documented."

---

### Internal Consistency (0.91/1.00)

**Evidence:**
- Threat Model Coverage Matrix summary row ("7 IMPLEMENTED, 4 PARTIAL, 2 MISSING") correctly matches the count of individual MC rows.
- MC-02 classified as MISSING in the matrix; F-001 severity rated High; P-2 priority rated "High — pre-production blocker." All three are consistent.
- MC-08 classified as MISSING in the matrix; F-002 severity rated High; P-1 rated "Critical — pre-production blocker." Consistent.
- P-7 UV version specification "0.5.29" matches Dockerfile line 75 `ENV UV_VERSION="0.5.29"` — a verified factual correction from iter2 (which incorrectly stated "0.6.2").
- T-40 verdict "PARTIAL" in the section header is consistent with the body description of three absent mechanisms.
- CVSS scores are consistent with severity labels: F-001 (6.5, High), F-002 (7.4, High), F-003 (5.3, Medium), F-004 (4.3, Medium), F-005 (4.6, Medium), F-006 (3.1, Low), F-007 (2.5, Low), F-008 (3.7, Low), F-009 (0.0, Info).

**Gaps:**
- Document header "Iteration: 2" conflicts with the content, which reflects three iter3 surgical fixes. A reader consulting only the header would believe this is iteration 2.
- S-010 self-review T-40 row (line 639) states "PASS — dedicated T-40 section with IMPLEMENTED verdict" — this contradicts the T-40 body section which explicitly labels the verdict "PARTIAL." This is the most significant internal consistency gap: the self-review's own verification of the T-40 section is incorrect. The S-010 table was not updated when the T-40 verdict was changed from IMPLEMENTED to PARTIAL in iter3.
- F-004 description mentions "the `stats.py` `_validate_score_array()` function rejects all-identical arrays... which provides some protection." This is accurate. However, the F-004 remediation discusses exception rate thresholds without connecting to the T-40 threat model; the connection between F-004 and T-35 is explicitly flagged as "indirectly," which is appropriate but slightly weakens the claimed traceability.

**Improvement Path:**
- Update S-010 T-40 row to remove "IMPLEMENTED" and replace with "PARTIAL."
- Update document header iteration number.
- These two fixes together would raise Internal Consistency to approximately 0.95.

---

### Methodological Rigor (0.95/1.00)

**Evidence:**
- The 701-line full-file review claim for stats.py is supported: the IQR grep returned zero matches, Cohen's d grep returned zero matches, and paired-difference symmetry grep returned zero matches — all confirming the absence assertions are based on actual code inspection.
- DREAD scoring methodology applied for T-40 prioritization (Priority Score = 7.2, DREAD Score 6.2, Integrity Impact Weight 1.0).
- CWE Top 25 2025 systematically applied with explicit APPLICABLE/NOT APPLICABLE/FINDING classification for each entry — no CWE skipped.
- Threat-to-control correlation uses system-design.md Part 4 MC mapping table as the source of truth, with line number citations (line 1535 for MC-02 assignment to deepeval_adapter.py).
- CVSS 3.1 base scores present for all findings with vector strings.
- OWASP ASVS V5 (Input Validation), V6 (Cryptography), V7 (Logging and Monitoring) explicitly checked in S-010.

**Gaps:**
- The T-40 section uses Cohen's r (not Cohen's d) for the effect size measure already present in stats.py. MC-40 Mechanism 2 specifies "Cohen's d cross-check." The assessment correctly identifies the absence of Cohen's d (a different measure from Cohen's r), but the body of the T-40 section does not explicitly explain the distinction between Cohen's r (what is present) and Cohen's d (what is specified in MC-40 but absent). A reader unfamiliar with the two measures might not understand why Cohen's r being present does not satisfy MC-40 Mechanism 2. This is a methodological clarity gap, not an error.
- The assessment does not check whether any other file in the codebase (e.g., layer4_stats.py) partially implements MC-40 mechanisms, which would affect the PARTIAL vs. MISSING classification. The scope note confirms 10 files reviewed; if layer4_stats.py was reviewed and found clean, a statement to that effect would strengthen the methodology.

**Improvement Path:**
- Add one sentence to the T-40 section distinguishing Cohen's r (present, Wilcoxon Z-to-r conversion) from Cohen's d (absent, standardized mean difference), explaining why the presence of Cohen's r does not satisfy MC-40 Mechanism 2.

---

### Evidence Quality (0.88/1.00)

**Evidence:**
- F-001: The insertion point claim (lines 329–333) verified by direct file read. No `re` module imported, no sanitization function called, no length check anywhere in deepeval_adapter.py. The `LLMTestCase` construction at line 330 receives raw `prompt` and `output_text`. Confirmed absent.
- F-002: Dockerfile line 75 `ENV UV_VERSION="0.5.29"` confirmed. Smoke workflow line 162 `version: "latest"` confirmed. Dockerfile line 39 `FROM node:20-alpine3.21` (tag-only) confirmed. All three instances match the assessment claims exactly.
- T-40 PARTIAL verdict: The IQR, Cohen's d, and paired-difference symmetry grep across all 701 lines of stats.py returned zero matches, confirming all three MC-40 mechanisms are absent. The `_validate_score_array()` all-identical check at lines 128–176 confirmed present. The `_cohens_r()` function at lines 184–212 confirmed present (Cohen's r, not Cohen's d). All code-level evidence claims verified.
- P-7: The specific version "0.5.29" is verified at Dockerfile line 75; the smoke.yml "latest" is verified at line 162. The cross-reference is accurate.

**Gaps:**
- T-40 body (lines 557–563) labels the three absent mechanisms as "IQR variance floor check (MC-40 Mechanism 1)," "Cohen's d cross-check for non-significant p-values (MC-40 Mechanism 2)," and "Paired-difference symmetry check (MC-40 Mechanism 3)." The threat description above (lines 544–546) labels them as "Variance floor enforcement," "Effect size cross-check," and "Paired-difference symmetry check." The mapping is clear on careful reading, but the label change between "Variance floor enforcement" and "IQR variance floor check" means a reader verifying the absent-controls list against the threat-model description must manually reconcile the label difference. This is a precision gap in evidence presentation.
- F-003 evidence cites `store.py` lines 410–432 for `_validate_version_key()`. However, `store.py` was not in the list of explicitly confirmed context files provided for this scoring session. The assessment claims to have reviewed store.py (listed in the S-010 completeness row). This is an unverifiable evidence claim — not necessarily false, but not independently confirmed in this scoring review. Given the pattern of accuracy in all other verified claims, this is a low-confidence gap rather than a high-confidence error.
- F-009's evidence is accurate (sha256.hexdigest()[:16] in version_keys.py) but the NIST SP 800-57 citation lacks a specific section reference, reducing traceability rigor for a cryptographic standards claim.

**Improvement Path:**
- Align the label "Variance floor enforcement" in the threat description with "IQR variance floor check" in the absent-controls list (or vice versa) for precision.
- Add NIST SP 800-57 section number to F-009 citation (e.g., "Section 5.6.1, Table 3").

---

### Actionability (0.96/1.00)

**Evidence:**
- P-1 and P-2 are explicitly marked as "pre-production blockers" with effort estimates.
- P-7 specifies exact action: replace `version: "latest"` with `version: "0.5.29"` at smoke.yml line 162 with Dockerfile line 75 as the authoritative source — this is immediately executable with zero ambiguity.
- P-8 changed from conditional ("Verify if absent, implement") to imperative ("Implement the following absent controls") with three numbered sub-items specifying the exact statistical checks to add: IQR variance floor at IQR < 0.01, Cohen's d cross-check at |d| > 0.50 when p > alpha, paired-difference symmetry at mean |diff| > 0.05 when signed rank sum ≈ 0.
- Code examples with specific line-number insertion points for F-001 (line 330), F-003 (VersionKey.from_string() import path), F-004 (exception_count threshold pattern), F-005 (bash allowlist validation), F-007 (multi-stage pip removal), F-008 (invalidation guard).
- P-9 specifies a concrete mechanism: custom Docker bridge network with iptables OUTPUT rules or host-level network policy restricting egress to api.anthropic.com:443.

**Gaps:**
- P-6 (MC-01/MC-03/MC-05/MC-06 PARTIAL) specifies JSON Schema field structure but does not identify the responsible person or team, nor does it reference an existing schema template that could be extended. A developer picking up P-6 would need to research promptfoo's expected schema format. This is acceptable for a security assessment but represents a slightly lower actionability bar than P-1/P-2/P-7/P-8.
- P-9 ("add a network policy recommendation") is the only recommendation that ends with a recommendation rather than an implementation instruction — the assessment itself recommends adding a network policy rather than specifying one. This is appropriate given the complexity of Docker network configuration, but it is the weakest actionability point in the recommendations set.

**Improvement Path:**
- P-9: Include a concrete example `docker network create` command with iptables rules, or specify that this requires a platform-level control (GitHub Actions runner network policies) outside the container itself.

---

### Traceability (0.94/1.00)

**Evidence:**
- Each finding (F-001 through F-009) provides: CWE ID, CVSS 3.1 base score with vector, threat ID (T-xx or MC-xx), requirement reference (FR-xx or MC-xx), affected file with line numbers.
- F-001 threat mapping (T-02/MC-02) traces to system-design.md Part 4 line 1535 with explicit quote: "MC-02 | Input sanitization for prompt injection | jerry/testing/evaluation/deepeval_adapter.py."
- F-005 threat mapping corrected from T-03 to T-02 and T-07, with rationale explaining the removal.
- MC-28 in the OWASP table explained as "drawn from the full MC-01 through MC-40 control set documented in system-design.md Part 4" — the out-of-range control citation is explained.
- S-010 self-review table provides a second traceability layer, cross-referencing each quality dimension against specific evidence.
- P-7 supply chain recommendation traces to both smoke.yml line 162 (the gap) and Dockerfile line 75 (the authoritative version source).

**Gaps:**
- F-004's threat citation ("T-35 (Adversarial score sequences, indirectly)") is the only finding where the threat mapping is qualified with "indirectly." The indirection is accurate (T-35 addresses adversarial score sequences; F-004's silent exception swallowing is a secondary path to that threat) but the weaker link reduces traceability confidence.
- The CWE Top 25 2025 checklist references "CWE Top 25 2025" but does not provide a URL or publication date for the specific list version. Different publications of the Top 25 use different orderings; the rank numbers in the table (CWE-79 as rank 1, CWE-787 as rank 2, etc.) should be verifiable against a cited source.

**Improvement Path:**
- Add the CWE Top 25 2025 source URL (e.g., https://cwe.mitre.org/top25/archive/2025/2025_cwe_top25.html) to the checklist section header.
- F-004: Strengthen T-35 traceability by adding one sentence explaining how silent exception swallowing creates an adversarial score manipulation path.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Internal Consistency | 0.91 | 0.95 | Update S-010 self-review T-40 row to remove "IMPLEMENTED" and replace with "PARTIAL — 3 absent MC-40 mechanisms confirmed and documented." This single fix resolves the most significant internal contradiction in the document. |
| 2 | Completeness | 0.95 | 0.97 | Update document header: change "Iteration: 2 (revised from iter 1 score 0.835 REVISE)" to "Iteration: 3 (revised from iter 2 score 0.908 REVISE)." |
| 3 | Evidence Quality | 0.88 | 0.93 | Align T-40 body labels: change "Variance floor enforcement" in the threat description list (line 544) to "IQR variance floor check" to match the absent-controls enumeration (line 561), eliminating the label reconciliation burden for readers. |
| 4 | Traceability | 0.94 | 0.96 | Add CWE Top 25 2025 source URL to the checklist section header. Strengthen F-004 T-35 traceability with one explanatory sentence. |
| 5 | Methodological Rigor | 0.95 | 0.97 | Add one sentence to the T-40 section distinguishing Cohen's r (present, Wilcoxon-derived) from Cohen's d (absent, standardized mean difference), explaining why Cohen's r does not satisfy MC-40 Mechanism 2. |

---

## Score Calculation Verification

```
Completeness:          0.95 × 0.20 = 0.190
Internal Consistency:  0.91 × 0.20 = 0.182
Methodological Rigor:  0.95 × 0.20 = 0.190
Evidence Quality:      0.88 × 0.15 = 0.132
Actionability:         0.96 × 0.15 = 0.144
Traceability:          0.94 × 0.10 = 0.094
                                    -------
Weighted Composite:                  0.932
```

---

## Critical Findings Assessment

No Critical findings from adv-executor reports are incorporated. The two High findings in the assessment itself (F-001, F-002) are findings within the deliverable, not findings about the deliverable's quality. They do not trigger automatic REVISE per H-13.

The REVISE verdict is driven solely by the composite score (0.932 < 0.94 threshold).

---

## Session Context (Handoff Schema)

```yaml
verdict: REVISE
composite_score: 0.932
threshold: 0.94
weakest_dimension: Evidence Quality
weakest_score: 0.88
critical_findings_count: 0
iteration: 3
improvement_recommendations:
  - "Update S-010 T-40 row: replace 'IMPLEMENTED' with 'PARTIAL — 3 absent MC-40 mechanisms confirmed'"
  - "Update document header from Iteration 2 to Iteration 3"
  - "Align T-40 body labels: 'Variance floor enforcement' -> 'IQR variance floor check'"
  - "Add CWE Top 25 2025 source URL; strengthen F-004 T-35 traceability"
  - "Distinguish Cohen's r (present) from Cohen's d (absent) in T-40 methodology"
```

---

## Leniency Bias Check

- [x] Each dimension scored independently
- [x] Evidence documented for each score — specific file:line citations verified against source code
- [x] Uncertain scores resolved downward (Evidence Quality at 0.88, not 0.92, because the label inconsistency in the T-40 section is a genuine gap; Internal Consistency at 0.91, not 0.94, because the S-010/T-40 contradiction is a real error)
- [x] First-draft calibration considered — this is iteration 3; scoring above 0.92 on most dimensions is appropriate for a substantially revised document
- [x] No dimension scored above 0.96 without specific evidence justification
- [x] The critical S-010 T-40 inconsistency (self-review says IMPLEMENTED, body says PARTIAL) is weighted as a genuine Internal Consistency failure, not a minor editorial issue — it would cause a reader auditing the S-010 table to reach a wrong conclusion about T-40 status

**Calibration check:** A composite of 0.932 on iteration 3 of a C4 deliverable that has improved from 0.835 → 0.908 → 0.932 reflects a document with strong foundational quality and three specific fixable gaps. The remaining gaps (S-010 T-40 contradiction, header metadata, label alignment) are real but correctable in a focused iter4 pass. The 0.008 gap to threshold is not charitable rounding — it reflects two genuine errors (S-010 T-40 row, iteration header) that require actual document changes.

---

*Score produced by: adv-scorer*
*Scoring date: 2026-03-07*
*SSOT: `.context/rules/quality-enforcement.md` (S-014, 6-dimension weighted composite)*
*Source files verified: stats.py (701 lines, IQR/Cohen's d/symmetry absent confirmed), deepeval_adapter.py (sanitization absent confirmed), Dockerfile (UV_VERSION="0.5.29" line 75 confirmed), prompt-regression-smoke.yml (version: "latest" line 162 confirmed)*
