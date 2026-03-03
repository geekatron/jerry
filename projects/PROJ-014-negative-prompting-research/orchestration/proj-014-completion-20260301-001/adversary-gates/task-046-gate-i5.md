# Quality Score Report: Negative Prompting Research Article (i5)

## L0 Executive Summary

**Score:** 0.953/1.00 | **Verdict:** PASS | **Weakest Dimension:** Evidence Quality (0.93) / Traceability (0.93) (tied)
**One-line assessment:** All three i5 fixes verified and effective — NPT-007 row corrected, "untreated" prose fix applied, statistical power note added — pushing the composite to 0.953 and clearing the 0.95 C4 threshold; remaining gaps (venue-level citation URLs, missing /prompt-engineering invocation hint) are cosmetic and do not block acceptance.

---

## Scoring Context

- **Deliverable:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/docs/research/negative-prompting.md`
- **Deliverable Type:** Research (public-facing MkDocs documentation page)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Threshold:** 0.95 (C4 user-specified)
- **Prior Score:** i4 = 0.936 REVISE
- **Scored:** 2026-03-01T00:00:00Z
- **Iteration:** 5

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.953 |
| **Threshold** | 0.95 (C4 user-specified) |
| **Verdict** | PASS |
| **Strategy Findings Incorporated** | No — standalone scoring pass |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.96 | 0.192 | All 13 success criteria satisfied; all sections present with depth |
| Internal Consistency | 0.20 | 0.96 | 0.192 | All three i5 fixes applied; statistical figures cross-check cleanly; NPT-007 dual role now documented |
| Methodological Rigor | 0.20 | 0.96 | 0.192 | Statistical power note added to Limitations; pre-registration, matched-pair design, blind scoring, inter-rater verification all documented |
| Evidence Quality | 0.15 | 0.93 | 0.1395 | NPT-007 name/type/evidence corrected (A1, T1 untreated control); venue-level citation URLs remain minor gap |
| Actionability | 0.15 | 0.96 | 0.144 | Decision table, 3-step upgrade workflow, pe-constraint-gen invocation example, ADR/FEAT status table all present |
| Traceability | 0.10 | 0.93 | 0.093 | All primary source links present; venue-level citation URLs and unlinked "23 quality gates" claim are minor persistent gaps |
| **TOTAL** | **1.00** | | **0.953** | |

---

## Detailed Dimension Analysis

### Completeness (0.96/1.00)

**Evidence:**

All 13 success criteria from the gate brief are satisfied in the i5 deliverable:

1. Key findings accurate and complete (line 9): "100% compliance (0/90 violations) versus 92.2% for positive-only framing (7/90 violations) across all tested conditions (McNemar exact p=0.016, n=270 matched pairs)." The 14-pattern taxonomy and CONDITIONAL GO are both stated.
2. NPT-013 and NPT-009 formats explained with examples: dedicated sections at lines 17-53 with template format and concrete examples for each.
3. 14-pattern taxonomy table: complete at lines 75-90, NPT-001 through NPT-014, with technique type, evidence tier, and recommendation per pattern.
4. NPT-007 row correct (line 83): "Positive-Only Framing (Control Baseline) | A1 | T1 (untreated control) | A/B test control condition; default when no specific constraint need exists" — i5 fix applied.
5. Practical application section: present at lines 96-152 with `/prompt-engineering` agent table, NPT-009/NPT-013 decision table, and 3-step upgrade workflow.
6. A/B test methodology: documented at lines 155-198 in MkDocs `??? note` and `??? abstract` blocks.
7. CONDITIONAL GO honesty: lines 203-207, naming pi_d=0.078 vs pre-registered minimum 0.10.
8. "What the Research Did Not Change" subsection: lines 209-215 with 4 bullets.
9. Limitations section: lines 218-227, all three required items present (statistical power note, open causal question, 60% hallucination claim).
10. Implementation section: lines 233-247, 4 ADRs with status and 5 FEATs listed.
11. Cross-links: blog post (line 289), SKILL.md (line 291), NPT reference (line 291), 4 ADR GitHub links (line 247), go-no-go determination (line 197), Final Synthesis (line 269).
12. "untested" → "untreated" at line 92: confirmed fixed.
13. Voice: direct, technically precise, warm — Saucer Boy/McConkey register consistent throughout.

The article is 301 lines and does not include a document-level navigation table (H-23). For a public-facing MkDocs article where navigation is provided by the site structure, this is not penalized as a completeness gap.

**Gaps:**

None at the completeness level. All sections and success criteria present with appropriate depth.

**Improvement Path:**

Completeness is at 0.96. A navigation table added above the Key Findings section would satisfy H-23 for internal compliance but is not required for MkDocs publication readiness.

---

### Internal Consistency (0.96/1.00)

**Evidence:**

All three i5 fixes applied and verified:

- **Fix 1 (NPT-007 row):** Line 83 — "Positive-Only Framing (Control Baseline) | A1 | T1 (untreated control) | A/B test control condition; default when no specific constraint need exists." The i4 inconsistency (NPT-007 name overwriting source taxonomy; blank technique type; missing evidence tier) is resolved. The parenthetical "(Control Baseline)" signals the dual role to readers.
- **Fix 2 ("untreated" prose):** Line 92 — "NPT-007 (positive-only) serves as the **untreated** baseline for comparison." The word "untested" from i3 is fully eliminated in both table (line 83) and prose (line 92). FULLY RESOLVED.
- **Fix 3 (statistical power note):** Lines 222-223 — "The study was powered to detect a minimum effect size of pi_d >= 0.10 (n=90 matched pairs per condition). The observed pi_d of 0.078 falls below this threshold, meaning the near-miss does not tell us whether the true population effect exceeds 0.10 -- only that this sample could not detect it at that level." FULLY RESOLVED.

Statistical figures cross-check cleanly across all occurrences:
- 0/90 violations (C3, line 179) consistent with "100% compliance" (line 9)
- 7/90 violations (C1, line 181) consistent with "92.2% compliance" (line 9)
- 2/90 violations (C2, line 179) consistent with "2.2% violation rate" (line 178)
- p=0.016 (lines 9, 185) consistent with Bonferroni-corrected alpha=0.0167 (lines 32, 186)
- pi_d=0.078 (lines 12, 187, 205, 222) consistent throughout
- CI [0.023, 0.133] consistent (lines 187)
- Haiku 10pp, Sonnet 2 violations, Opus 1 violation (lines 191-193) cross-check: total = 7 violations = consistent with C1 count

CONDITIONAL GO logic consistent: lines 12, 205, and 207 all frame the result as "significant but below pre-registered minimum" — no contradiction.

NPT-007 dual usage: "positive-only" appears in A/B condition context (lines 92, 166, 181, 211) and the table uses "Positive-Only Framing (Control Baseline)" (line 83). The "(Control Baseline)" parenthetical makes the dual role explicit. Consistent.

**Gaps:**

No material inconsistencies identified. Minor note: line 83 shows NPT-007 technique type as "A1" where the i4 report suggested "A1/A2." The i5 brief specifies the fix as "type → 'A1'" which is what was implemented. This is within stated scope. No consistency issue created.

**Improvement Path:**

Internal consistency is at 0.96. The remaining 0.04 gap reflects standard calibration headroom — no specific remediation is actionable without introducing new content.

---

### Methodological Rigor (0.96/1.00)

**Evidence:**

The A/B test methodology section (lines 155-198) documents all substantive elements:

- Scale: 270 blind invocations confirmed (line 160)
- Design: matched-pair, three conditions with concrete examples per condition (lines 163-168)
- Constraints tested: 10 representative constraints spanning four categories (line 170)
- Pressure scenarios: three levels described (line 172)
- Scoring: binary compliance, no partial credit, blind independent scoring, inter-rater agreement verification (line 174)
- Statistical tests: McNemar exact test, Bonferroni correction, effect size pi_d with 95% CI (lines 183-187)
- Pre-registration: PG-003 contingency explicitly noted as "pre-specified" (line 205)
- Open causal question: information density vs framing variable acknowledged (lines 224-225)
- 60% hallucination claim disposition: null finding documented (lines 226-227)
- **Statistical power note (i5 fix, lines 222-223):** Study was powered for pi_d >= 0.10 at n=90 matched pairs; observed pi_d=0.078 falls below MDE; explanation of what this means for interpretation of the near-miss. FULLY RESOLVED.

The six-phase research pipeline table (lines 257-265) includes quality gate scores per phase, confirming systematic execution.

**Gaps:**

- Inter-rater agreement coefficient (AC1=0.920) not stated in the article body. The article states "inter-rater agreement verification" (line 174) but does not quantify it. For a public documentation article this is acceptable; a research paper would require this explicitly.
- The number of matched pairs per condition (n=90) is stated in the power note (line 222) but not in the study design section itself (lines 159-174). This is a minor structural placement gap.

**Improvement Path:**

Adding the inter-rater agreement coefficient to the study design `??? note` block and confirming n=90 matched pairs per condition in that same block would raise this to 0.97. Both are minor additions.

---

### Evidence Quality (0.93/1.00)

**Evidence:**

The NPT-007 fix resolves the primary i4 Evidence Quality gap:

**NPT-007 row (i5 fix verified):** Line 83 now shows "Positive-Only Framing (Control Baseline) | A1 | T1 (untreated control) | A/B test control condition; default when no specific constraint need exists."

- Name: "Positive-Only Framing (Control Baseline)" — communicates the A/B control condition role; "(Control Baseline)" parenthetical prevents confusion with the source taxonomy's independent definition. RESOLVED.
- Type: "A1" — technique type now populated (i4 had "−−" blank). RESOLVED.
- Evidence: "T1 (untreated control)" — evidence tier now present and labeled with methodology context. RESOLVED.
- Recommendation: "A/B test control condition; default when no specific constraint need exists" — accurate and informative. RESOLVED.

Anchor citations (lines 277-283):
- Liu et al. AAAI 2026: finding correctly stated (instruction hierarchy failure under standalone negative constraints); relevance accurate (T1 evidence for NPT-014 underperformance).
- Wen et al. EMNLP 2024: finding correctly stated (+7.3-8% compliance for structured vs blunt). PASS.
- Barreto & Jana EMNLP 2025: finding correctly stated (+25.14% negation reasoning accuracy); distinction between comprehension and behavioral compliance correctly drawn. PASS.

A/B test data verified against stated source: p=0.016, pi_d=0.078, CI [0.023, 0.133], C3=0/90, C1=7/90, C2=2/90, H-22 share=6/9=67%. All consistent.

**Gaps:**

Persistent from i4 (not in scope of i5 fixes):

- **Venue-level citation URLs.** Lines 279-281 link to AAAI proceedings archive page and ACL Anthology venue pages — not individual paper DOIs or direct paper URLs. A reader looking up Liu et al. AAAI 2026 or Wen et al. EMNLP 2024 must search within the proceedings rather than navigate directly to the paper. This is a minor credibility navigation gap for the citations, not a claims-support gap. The citations are credible; the URLs are inconvenient.
- The note that Phase 1 covered "75 unique sources" (line 283) is supported by a link to the Phase 1 survey directory but not to a specific source inventory file. Minor.

**Improvement Path:**

Adding direct paper links (DOI or ACL Anthology individual paper page) for the three anchor citations would raise this to 0.96. This is a post-publication polish item, not a blocking gap.

---

### Actionability (0.96/1.00)

**Evidence:**

The Practical Application section (lines 96-152) provides concrete, implementable guidance:

- Agent table: pe-builder (interactive prompt assembly), pe-constraint-gen (NPT constraint formatter), pe-scorer (quality evaluation), with purpose and when-to-use per agent (lines 103-106). Specific and differentiated.
- Natural-language invocation example for pe-constraint-gen (lines 108-114): exact syntax to use.
- NPT-009 vs NPT-013 decision table: 5 rows covering all major deployment contexts (governance YAML, SKILL.md routing, rule files, agent markdown body, constitutional tables) — lines 119-126.
- Decision rule stated twice for redundancy (lines 52-53 and line 126): "if you need to reference a constitutional principle and the context is governance metadata, use NPT-009. If there is a concrete alternative action the agent should take instead, use NPT-013."
- Three-step upgrade workflow with before/after examples (lines 130-149): NPT-014 → NPT-009 → NPT-013. Concrete code blocks at each step.
- Three-criteria self-review checklist for finished constraints (line 151): binary-testable, specific consequence, achievable alternative.
- Implementation section (lines 233-247): ADR status and FEAT status tell the reader exactly what has changed and what the current state is.

**Gaps:**

Persistent from i4 (not in scope of i5 fixes):

- The article does not provide a one-line invocation hint for `/prompt-engineering` in the Practical Application section. The reader learns about pe-builder, pe-constraint-gen, and pe-scorer but not how to invoke the parent skill. The SKILL.md link is in References (line 291) but not co-located with the agent descriptions. A reader could reasonably want to know: "do I type `/prompt-engineering` to access these agents?"

**Improvement Path:**

Adding "Invoke via `/prompt-engineering`" as a one-line prefix to the agent table (line 100 or in the section introduction) would surface the invocation pattern at point-of-need.

---

### Traceability (0.93/1.00)

**Evidence:**

All primary sources are linked:

- Go-no-go determination: line 197 — GitHub branch link to `ab-testing-20260301-001/phase-3-analysis/go-no-go-determination.md`.
- 4 ADR links: line 247 — all four ADRs linked via GitHub branch paths.
- Final Synthesis Phase 6, NPT Pattern Catalog, WORKTRACKER: line 269.
- Phase 1 survey directory: line 283.
- Prompt Engineering SKILL.md: line 291.
- NPT Pattern Reference: line 291.
- Blog post: line 289 — `docs/blog/posts/structured-negation-constraint-enforcement.md`.
- Related Research cross-links: lines 297-300, four internal research pages.

The traceability chain from claim to source is intact for all major findings:
- "100% compliance (0/90)" — traceable to go-no-go determination (line 197).
- "14-pattern NPT taxonomy" — traceable to NPT Pattern Catalog (line 269).
- "23 C4 quality gates" — traceable via WORKTRACKER link (line 269).
- Academic citations — traceable to venue-level URLs (lines 279-281).

**Gaps:**

Persistent from i4 (not in scope of i5 fixes):

- Venue-level citation URLs rather than direct paper DOIs/links. The three anchor papers (Liu et al. AAAI 2026, Wen et al. EMNLP 2024, Barreto & Jana EMNLP 2025) require manual search within the linked proceedings/venue pages.
- "23 C4 quality gates across the entire project" (line 253): the WORKTRACKER link at line 269 provides path to the worktracker but does not point directly to the gate reports index. A reader specifically interested in validating the 23-gate claim would need to navigate the worktracker.

**Improvement Path:**

Direct paper links for three anchor citations would raise to 0.96. These are post-publication polish items.

---

## i5 Fix Verification

| Fix | Status | Evidence |
|-----|--------|---------|
| (1) NPT-007 row updated: name → "Positive-Only Framing (Control Baseline)", type → "A1", evidence → "T1 (untreated control)", recommendation expanded | PASS | Line 83: `\| NPT-007 \| Positive-Only Framing (Control Baseline) \| A1 \| T1 (untreated control) \| A/B test control condition; default when no specific constraint need exists \|` |
| (2) Prose "untested" → "untreated" at line 92 | PASS | Line 92: "NPT-007 (positive-only) serves as the **untreated** baseline for comparison." — confirmed via grep |
| (3) Statistical power note added to Limitations section | PASS | Lines 222-223: "The study was powered to detect a minimum effect size of pi_d >= 0.10 (n=90 matched pairs per condition). The observed pi_d of 0.078 falls below this threshold, meaning the near-miss does not tell us whether the true population effect exceeds 0.10 -- only that this sample could not detect it at that level." |

All three i5 fixes are fully and correctly applied.

---

## Improvement Recommendations (Priority Ordered)

These are post-PASS polish items — none blocks acceptance.

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Evidence Quality + Traceability | 0.93 | 0.96 | Replace venue-level citation URLs (lines 279-281) with direct DOI or ACL Anthology individual paper links for Liu et al., Wen et al., and Barreto & Jana |
| 2 | Actionability | 0.96 | 0.97 | Add one-line invocation hint "Invoke via `/prompt-engineering`" in the Practical Application section near the agent table (line 100 area) |
| 3 | Methodological Rigor | 0.96 | 0.97 | Add inter-rater agreement coefficient (AC1=0.920) to the study design `??? note` block; confirm n=90 matched pairs per condition in that block |
| 4 | Completeness | 0.96 | 0.97 | Add a document navigation table after the lede blockquote for H-23 compliance (optional for MkDocs publication but advisable for internal doc standards) |

---

## Composite Verification

| Dimension | Score | Weight | Weighted |
|-----------|-------|--------|---------|
| Completeness | 0.96 | 0.20 | 0.1920 |
| Internal Consistency | 0.96 | 0.20 | 0.1920 |
| Methodological Rigor | 0.96 | 0.20 | 0.1920 |
| Evidence Quality | 0.93 | 0.15 | 0.1395 |
| Actionability | 0.96 | 0.15 | 0.1440 |
| Traceability | 0.93 | 0.10 | 0.0930 |
| **TOTAL** | | **1.00** | **0.9525** |

Rounded to three decimal places: **0.953**

Threshold: 0.95 (C4 user-specified). Score 0.953 >= 0.95. **PASS.**

---

## Leniency Bias Check

- [x] Each dimension scored independently before composite computed
- [x] Evidence documented for each score with specific line references
- [x] Uncertain scores resolved downward — Evidence Quality and Traceability held at 0.93 (not 0.95) for persistent venue-level URL gap despite all i5 content fixes being fully effective
- [x] Calibration anchors applied: 0.93 = "most claims supported/traceable with minor navigation gap in citations"; 0.96 = "strong work with one minor refinement needed (no specific actionable fix beyond cosmetic)"
- [x] No dimension scored above 0.96 — confirmed. All scores have documented evidence ceiling.
- [x] Composite verified: 0.1920 + 0.1920 + 0.1920 + 0.1395 + 0.1440 + 0.0930 = 0.9525
- [x] First-draft calibration not applicable (this is iteration 5; scoring calibrated against convergence trajectory i1→i2→i3→i4→i5: 0.805→0.895→0.926→0.936→0.953)

**Anti-leniency note:** Evidence Quality and Traceability were independently confirmed at 0.93 rather than 0.95. The i5 fixes were substantial and effective for Internal Consistency (0.93→0.96), but the venue-level citation URL gap was explicitly identified in i4 and was not in scope for i5 fixes — holding these at 0.93 rather than rewarding the iteration for work it did not do.

---

## Session Context Handoff

```yaml
verdict: PASS
composite_score: 0.953
threshold: 0.95
weakest_dimension: evidence_quality
weakest_score: 0.93
critical_findings_count: 0
blocking_findings_count: 0
iteration: 5
improvement_recommendations:
  - "Replace venue-level citation URLs with direct DOI/ACL paper links for three anchor citations (lines 279-281) — post-PASS polish"
  - "Add /prompt-engineering invocation hint in Practical Application section near agent table — post-PASS polish"
  - "Add inter-rater agreement coefficient (AC1=0.920) to study design block — post-PASS polish"
gap_to_threshold: 0.003
score_delta_from_i4: +0.017
convergence_trajectory: "0.805 -> 0.895 -> 0.926 -> 0.936 -> 0.953"
```
