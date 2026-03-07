# Quality Score Report: Stream 5A Security Assessment (Iteration 4)

## L0 Executive Summary

**Score:** 0.944/1.00 | **Verdict:** PASS | **Weakest Dimension:** Evidence Quality (0.91)
**One-line assessment:** All six iter3→iter4 prescribed fixes verified present and factually correct — the S-010 T-40 row now reads PARTIAL, the header is correctly stamped "Iteration: 4," label alignment is exact, the MC-40 header names all three mechanisms, the CWE source URL is present and correct, and the Cohen's r vs Cohen's d distinction is explained with enough specificity to satisfy Evidence Quality at 0.91; the composite clears the 0.94 C4 threshold.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-036-prompt-regression-harness/security/security-assessment.md`
- **Deliverable Type:** Analysis (Security Assessment)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-03-07T00:00:00Z
- **Iteration:** 4 (iter1: 0.835, iter2: 0.908, iter3: 0.932)
- **Prior Verdict:** REVISE (iter3, score 0.932)

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.944 |
| **Threshold** | 0.94 (C4, custom) |
| **Verdict** | PASS |
| **Strategy Findings Incorporated** | No — code verified directly against source files |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.97 | 0.194 | All 14 MC controls, all 10 OWASP categories, all 25 CWE Top 25 2025 entries, dedicated T-40 section, 9 findings, 12 recommendations; header and S-010 T-40 row now fully accurate. |
| Internal Consistency | 0.20 | 0.95 | 0.190 | Iteration header (iter4 with full score history), S-010 T-40 row (PARTIAL verdict), summary count (7/4/2), MC-40 absent-controls section header (Mechanisms 1, 2, and 3) — all internally consistent; no surviving contradictions from iter3. |
| Methodological Rigor | 0.20 | 0.96 | 0.192 | Cohen's r vs Cohen's d distinction now explicit with "rank-biserial correlation" vs "standardized mean difference" phrasing; 701-line stats.py review cited; DREAD/CVSS/ASVS/OWASP methodologies present; no methodological gaps remain from iter3 list. |
| Evidence Quality | 0.15 | 0.91 | 0.137 | All previously verified claims still accurate; CWE source URL added and points to correct MITRE archive; Cohen's distinction supported by stats.py code read confirming _cohens_r() as Z-based r, not d; minor residual: F-009 NIST SP 800-57 citation still lacks section/table reference. |
| Actionability | 0.15 | 0.96 | 0.144 | P-1 through P-12 with effort estimates; P-8 imperative with three numbered sub-items; P-7 exact version and file:line; code examples for F-001, F-003–F-008; P-9 weakest (recommendation-to-add-recommendation) but unchanged from iter3 where it was accepted at 0.96. |
| Traceability | 0.10 | 0.87 | 0.087 | CWE source URL now present; each finding traces to CWE+CVSS+threat+requirement+file:line; F-004 T-35 "indirectly" qualifier persists as minor gap; F-009 NIST SP 800-57 still lacks section reference. |
| **TOTAL** | **1.00** | | **0.944** | |

---

## Detailed Dimension Analysis

### Completeness (0.97/1.00)

**Evidence:**

The iter4 document resolves both completeness gaps identified in iter3:

1. **Iteration header (fix 2):** Line 8 reads `Iteration: 4 (iter1: 0.835, iter2: 0.908, iter3: 0.932)` — full four-iteration history present. Footer at line 653 confirms: `Iteration: 4 (iter1: 0.835, iter2: 0.908, iter3: 0.932 — threshold 0.94)`. No reader consulting the header in isolation would undercount revision history.

2. **S-010 T-40 row (fix 1):** Line 639 reads `PASS — dedicated T-40 section with PARTIAL verdict; three absent MC-40 mechanisms explicitly documented after full 701-line stats.py review.` The S-010 self-review now correctly reports the T-40 verdict as PARTIAL, eliminating the completeness gap in the self-review's own accuracy.

3. **Structural coverage:** All 14 MC controls assessed; all 10 OWASP Top 10 2021 categories addressed; all 25 CWE Top 25 2025 entries systematically checked (12 applicable, 13 not applicable); dedicated T-40 section with explicit mechanism-by-mechanism evidence; 9 findings F-001 through F-009; 12 prioritized recommendations P-1 through P-12; Supply Chain, Container Security, and Runtime Hardening sections all present.

**Gaps:**

None with material consequence. One cosmetic observation: the S-010 completeness row for "All specified implementation files reviewed" continues to list 10 files (including `base.py` and `layer4_stats.py`), and the T-40 assessment's text is explicit that stats.py received a 701-line full review; however, the assessment does not include a one-line statement confirming that layer4_stats.py was reviewed and contained no additional MC-40 mechanism implementations — a marginal gap that has no impact on correctness since the scope note at line 655 confirms all 10 files reviewed.

**Improvement Path:**

A single sentence in the T-40 section confirming that layer4_stats.py was reviewed and found clean of IQR/Cohen's d/symmetry implementations would raise this to 0.98, but the current 0.97 is well-earned.

---

### Internal Consistency (0.95/1.00)

**Evidence:**

All four internal consistency issues from iter3 are resolved:

1. **Header vs. content (fix 2):** Header "Iteration: 4" is consistent with content reflecting four rounds of revision. The score history in the header (0.835, 0.908, 0.932) matches the externally known iteration scores.

2. **S-010 T-40 row vs. T-40 body verdict (fix 1):** S-010 row now reads "PARTIAL verdict" (line 639). T-40 body section reads "Assessment: PARTIAL" (line 548). These are consistent.

3. **MC-40 mechanisms header vs. body enumeration (fix 4):** Section heading "Confirmed absent controls (MC-40 Mechanisms 1, 2, and 3)" (line 557) is consistent with the numbered list below it enumerating all three mechanisms.

4. **Label alignment (fix 3):** The threat description list at line 544 now reads "IQR variance floor check: reject score arrays where IQR < 0.01" — matching the absent-controls enumeration label at line 561 "IQR variance floor check (MC-40 Mechanism 1)." The label reconciliation burden is eliminated.

5. **Summary row consistency:** "7 IMPLEMENTED, 4 PARTIAL, 2 MISSING" (line 56) correctly matches the count of individual MC rows — unchanged and verified from iter2.

6. **CVSS–severity alignment:** F-001 (6.5, High), F-002 (7.4, High), F-003 (5.3, Medium), F-004 (4.3, Medium), F-005 (4.6, Medium), F-006 (3.1, Low), F-007 (2.5, Low), F-008 (3.7, Low), F-009 (0.0, Info) — all consistent with respective severity labels.

**Gaps:**

One minor residual: F-004's threat citation reads "T-35 (Adversarial score sequences, indirectly)" in the finding header and the F-004 description refers to `stats.py` `_validate_score_array()` as providing "some protection" — the connection between F-004 (silent exception swallowing) and T-35 (adversarial score sequences) is accurate but the "indirectly" qualifier means the threat chain requires one inferential step that is not explicitly bridged in the text. This does not rise to a contradiction — it is a traceability precision gap more than a consistency gap — and its impact on Internal Consistency is minor. No new consistency issues introduced in iter4.

**Improvement Path:**

Adding one bridging sentence in F-004 ("Silent exception injection provides an adversarial path to T-35 because...") would resolve the residual and push this to 0.96.

---

### Methodological Rigor (0.96/1.00)

**Evidence:**

The primary methodological gap from iter3 — the Cohen's r vs. Cohen's d distinction — is resolved by fix 6:

Line 562: "Cohen's r (a Wilcoxon-derived rank-biserial correlation) is computed via `_cohens_r()`, but MC-40 specifies Cohen's d (the standardized mean difference). These are distinct metrics: Cohen's r measures rank-order effect size while Cohen's d measures mean-difference effect size normalized by pooled standard deviation."

This explanation is technically accurate and confirmed against the stats.py implementation: `_cohens_r()` at lines 184-212 derives r from the normal approximation of the Wilcoxon W statistic using `r = |Z| / sqrt(N)`, which is indeed rank-biserial, not a pooled-standard-deviation-normalized mean difference. A reviewer now understands why the presence of Cohen's r does not satisfy MC-40 Mechanism 2. The distinction is correctly placed inline with the evidence for MC-40 Mechanism 2 absence, which is the highest-value location.

Additional methodological strengths unchanged from iter3:
- 701-line full-file review of stats.py explicitly cited with line-number evidence for all assertions
- DREAD scoring for T-40 prioritization (Priority Score = 7.2)
- CWE Top 25 2025 systematically applied — no CWE skipped or treated inconsistently
- OWASP ASVS V5/V6/V7 addressed in S-010 self-review
- Threat-to-control correlation uses system-design.md Part 4 line 1535 as primary source
- CVSS 3.1 base scores with vector strings for all findings

**Gaps:**

One marginal residual: The assessment does not include a statement confirming that layer4_stats.py (which orchestrates stats.py) was reviewed and found not to add any MC-40 mechanism implementations independent of stats.py. The scope note at line 655 confirms 10 files reviewed, but the T-40 section focuses exclusively on stats.py. Since layer4_stats.py is the caller of stats.py's `compare_versions()`, any IQR/Cohen's d/symmetry logic added in layer4_stats.py as a wrapper would partially satisfy MC-40 without appearing in stats.py. The assessment does not address this possibility explicitly. This is a minor rigor gap, not an error.

**Improvement Path:**

One sentence: "layer4_stats.py was reviewed and does not implement IQR variance floor, Cohen's d cross-check, or paired-difference symmetry logic; all three mechanisms remain absent across the full Layer 4 code surface."

---

### Evidence Quality (0.91/1.00)

**Evidence:**

Fix 5 (CWE source URL) and fix 6 (Cohen's r vs Cohen's d) directly address the two evidence quality gaps from iter3:

1. **CWE Top 25 2025 URL (fix 5):** Line 576 now contains a hyperlinked citation: `[CWE Top 25 2025](https://cwe.mitre.org/top25/archive/2025/2025_cwe_top25.html)`. The URL is the correct MITRE archive path for the 2025 edition, making the rank ordering (CWE-79 as rank 1, CWE-787 as rank 2, etc.) verifiable against the primary source. The traceability gap identified in iter3 is resolved.

2. **Cohen's r vs Cohen's d distinction (fix 6):** The explanation added to line 562 provides the necessary technical grounding — a reader can verify the claim by reading `_cohens_r()` in stats.py (which I verified: the formula `r = |Z| / sqrt(N)` is exactly the rank-biserial correlation, not Cohen's d) and by confirming no `statistics.stdev()` or pooled-standard-deviation calculation exists in stats.py (confirmed absent in my full read). The evidence for MC-40 Mechanism 2 absence is now independently verifiable.

3. **All previously verified claims remain accurate:** F-001 insertion point at deepeval_adapter.py line 330 (verified: raw strings pass to LLMTestCase with no sanitization); F-002 Dockerfile line 39 tag-only, smoke.yml line 218 `:latest` (verified in Dockerfile read); T-40 all-identical check at lines 128-176 (verified in stats.py read); `_cohens_r()` at lines 184-212 (verified in stats.py read).

**Gaps:**

Two residual evidence quality items persist:

1. **F-009 NIST SP 800-57 citation precision:** Line 451 states "below the NIST SP 800-57 128-bit minimum for collision-resistant identifiers" without a section number or table reference. NIST SP 800-57 Part 1 Table 3 (Comparable algorithm strengths) is the correct locus for this claim. The claim is correct but imprecise — a reader would need to search the 170-page document to verify it. This reduces evidence quality for F-009 specifically.

2. **store.py F-003 evidence (unverified in this scoring session):** The assessment cites `store.py` lines 410-432 for `_validate_version_key()`. `store.py` was not among the context files provided to this scoring session for direct verification. The pattern of accuracy in all other verified claims provides high confidence that this citation is correct, but it remains a low-confidence unverified claim rather than a confirmed-verified one. This is the same gap identified in iter3; it has not been resolved because resolving it would require updating context file access rather than the deliverable itself.

These two residual gaps are why Evidence Quality is 0.91 rather than 0.95+. Neither is a factual error; both are precision/verifiability gaps. The first is fixable with a section citation; the second is a scoring process limitation.

**Improvement Path:**

Add "NIST SP 800-57 Part 1 Rev. 5, Table 3" to the F-009 citation. This alone would raise Evidence Quality to approximately 0.93.

---

### Actionability (0.96/1.00)

**Evidence:**

Unchanged from iter3 where Actionability was rated 0.96. No regression or improvement observed in iter4 for this dimension — the iter4 fixes were targeted at Internal Consistency, Completeness, Evidence Quality, Methodological Rigor, and Traceability rather than Actionability.

Actionability strengths confirmed:
- P-1 and P-2 labeled "pre-production blockers" — decision makers can act immediately
- P-7 specifies exact action: replace `version: "latest"` with `version: "0.5.29"` at smoke.yml line 162
- P-8 imperative ("Implement the following absent controls") with three numbered sub-items specifying exact thresholds: IQR < 0.01, |Cohen's d| > 0.50 when p > alpha, mean |diff| > 0.05 when signed rank sum ≈ 0
- Code examples present for F-001, F-003, F-004, F-005, F-007, F-008, F-009
- P-1 specifies priority order (Smoke workflow `:latest` first, then Standard/Full, then Dockerfile)

**Gaps:**

- P-9 ("Add a network policy recommendation") remains the weakest actionability point. The recommendation is to add a network policy, rather than itself providing the network policy implementation. A developer picking up P-9 must design the iptables configuration from the description provided. This is an acceptable limitation for a security assessment (P-9 is Medium priority, correctly placed below the High blockers).
- P-6 (JSON Schema implementation) does not name a responsible team or reference an existing promptfoo schema template. A developer picking up P-6 would need to research promptfoo's expected output schema format independently.

**Improvement Path:**

P-9: Include a concrete `docker network create` command with example iptables OUTPUT rules, or explicitly state "This requires platform-level network policy outside the container; contact infrastructure team." Either would raise Actionability to 0.97.

---

### Traceability (0.87/1.00)

**Evidence:**

Fix 5 (CWE source URL) resolves the most significant traceability gap from iter3:

Line 576: `[CWE Top 25 2025](https://cwe.mitre.org/top25/archive/2025/2025_cwe_top25.html)` — the rank ordering in the checklist table (CWE-79 rank 1, CWE-787 rank 2) is now traceable to a primary source without ambiguity about which edition or year is being referenced.

Additional traceability strengths unchanged from iter3:
- Each finding (F-001 through F-009) provides: CWE ID, CVSS 3.1 base score with vector, threat ID, requirement (FR-xx or MC-xx), affected file with line numbers
- F-001 traces to system-design.md Part 4 line 1535 with exact field values quoted
- F-005 threat mapping corrected from T-03 to T-02/T-07 with rationale
- MC-28 OWASP table citation explained as drawn from full MC-01–MC-40 set
- S-010 self-review provides a second traceability layer

**Gaps:**

Two residual traceability gaps persist:

1. **F-004 T-35 "indirectly" qualifier:** The threat citation "T-35 (Adversarial score sequences, indirectly)" in the F-004 header is accurate but requires the reader to infer the causal chain: silent exception swallowing → corrupted score arrays → adversarial bypass of significance testing → T-35 effect. The chain is inferential rather than explicitly stated. This is the primary reason Traceability scores 0.87 rather than 0.92+.

2. **F-009 NIST SP 800-57 section missing:** As noted in Evidence Quality, the cryptographic standard citation lacks a specific section and table reference. For traceability purposes, this means a reviewer cannot directly verify the 128-bit minimum claim without searching the full standard document.

These two gaps were present in iter3 (Traceability was 0.94) and were listed as improvement paths. They were not addressed in iter4. The iter3 Traceability score of 0.94 may have been generous — on re-evaluation applying stricter leniency-bias counteraction, the F-004 indirect linkage is a more significant traceability gap than a 0.94 score implies. A traceability score of 0.87 reflects that the F-004 gap requires an inferential step not present in the text, and the F-009 gap means one cryptographic standards claim lacks a specific locator. Two unresolved traceability gaps in a C4 deliverable warrant a downward adjustment from the iter3 score.

**Calibration note:** The iter3 Traceability score of 0.94 was set before the Cohen's r vs. Cohen's d explanation was added. The Cohen's explanation in iter4 does not materially affect Traceability (it is an Evidence Quality item). The F-004 and F-009 gaps have existed since iter2 and were not resolved by any iter4 fix. Applying the calibration anchor (0.85 = strong work with minor refinements needed) and recognizing two specific, identifiable gaps, 0.87 is the appropriate score.

**Improvement Path:**

- F-004: Add one sentence in the finding description: "Silent exception swallowing creates an adversarial path to T-35 because an attacker who can reliably trigger exceptions in the DeepEval pipeline produces a controlled all-zeros (or near-zero) score array, which suppresses Wilcoxon significance even when the prompt has regressed." This resolves the inferential gap and is the single highest-value improvement available for Traceability.
- F-009: Add "NIST SP 800-57 Part 1 Rev. 5, Table 3" to the citation.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Traceability | 0.87 | 0.93 | F-004: Add one sentence bridging the T-35 adversarial path — explain explicitly how exception swallowing produces controlled score arrays that suppress Wilcoxon significance. |
| 2 | Evidence Quality | 0.91 | 0.94 | F-009: Add "NIST SP 800-57 Part 1 Rev. 5, Table 3" to the cryptographic standard citation, making the 128-bit minimum claim directly verifiable. |
| 3 | Methodological Rigor | 0.96 | 0.97 | Add one sentence confirming layer4_stats.py review found no IQR/Cohen's d/symmetry implementation, closing the MC-40 surface coverage gap. |
| 4 | Actionability | 0.96 | 0.97 | P-9: Add a concrete `docker network create` command or explicitly state this requires platform-level infrastructure team action. |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score with specific line citations
- [x] Uncertain scores resolved downward (Traceability re-evaluated from iter3's 0.94 to 0.87 on stricter application of rubric — F-004 indirect linkage is more than a minor gap at C4)
- [x] Calibration anchors applied: 0.92 = genuinely excellent; 0.87 = strong work with identifiable refinements needed
- [x] No dimension scored above 0.97
- [x] Weighted composite verified arithmetically: (0.97 × 0.20) + (0.95 × 0.20) + (0.96 × 0.20) + (0.91 × 0.15) + (0.96 × 0.15) + (0.87 × 0.10) = 0.194 + 0.190 + 0.192 + 0.137 + 0.144 + 0.087 = 0.944
- [x] Verdict matches score range table: 0.944 >= 0.92 → PASS

---

## Session Context

```yaml
verdict: PASS
composite_score: 0.944
threshold: 0.94
weakest_dimension: Traceability
weakest_score: 0.87
critical_findings_count: 0
iteration: 4
improvement_recommendations:
  - "F-004: Add one sentence bridging T-35 adversarial path from exception swallowing to score array corruption"
  - "F-009: Add NIST SP 800-57 Part 1 Rev. 5 Table 3 section citation"
  - "T-40: Confirm layer4_stats.py reviewed and found clean of MC-40 mechanism implementations"
  - "P-9: Provide concrete docker network create command or explicit infrastructure team referral"
```

---

*Score report produced by: adv-scorer (Quality Scorer Agent)*
*Scoring date: 2026-03-07T00:00:00Z*
*Deliverable: `projects/PROJ-036-prompt-regression-harness/security/security-assessment.md`*
*Strategy: S-014 (LLM-as-Judge), 6-dimension SSOT weighted composite*
*SSOT: `.context/rules/quality-enforcement.md`*
