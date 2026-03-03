# Quality Score Report: Negative Prompting Research Article (i4)

## L0 Executive Summary

**Score:** 0.936/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Evidence Quality (0.87)
**One-line assessment:** A strong, nearly publication-ready research article held back by one factual naming error (NPT-007 labeled "Positive-Only Framing" in the Pattern Catalog contradicts source taxonomy definition), one residual "untested" that survived the i4 fix, and a minor technique-type omission for NPT-007 — targeted fixes in under 30 minutes would push this to PASS.

---

## Scoring Context

- **Deliverable:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/docs/research/negative-prompting.md`
- **Deliverable Type:** Research (public-facing MkDocs documentation page)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Threshold:** 0.95 (C4 override — user-specified for this gate series)
- **Prior Iteration:** i3 scored 0.926 REVISE
- **Scored:** 2026-03-01T00:00:00Z

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.936 |
| **Threshold** | 0.95 (C4 user-specified) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No — standalone scoring pass |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.96 | 0.192 | All 12 success criteria addressed; "What Research Did Not Change" subsection present; all 4 ADRs + 5 FEATs listed with status |
| Internal Consistency | 0.20 | 0.93 | 0.186 | One residual "untested" at line 92 contradicts "untreated" fix applied to table at line 83; all statistical figures internally consistent |
| Methodological Rigor | 0.20 | 0.95 | 0.190 | Six-phase pipeline + A/B test described with study design, matched-pair structure, pressure scenarios, statistical tests, and inter-rater agreement |
| Evidence Quality | 0.15 | 0.87 | 0.131 | NPT-007 labeled "Positive-Only Framing" in Pattern Catalog contradicts source taxonomy (NPT-007 = Blunt-Prohibition Baseline); technique type "--" should be A1/A2 per source |
| Actionability | 0.15 | 0.96 | 0.144 | Decision table, upgrade workflow (3-step), pe-constraint-gen invocation, agent table all present and specific |
| Traceability | 0.10 | 0.93 | 0.093 | ADR links, Phase 1 survey link, go-no-go link, SKILL.md link, NPT reference link all present; blog post link verified as existing |
| **TOTAL** | **1.00** | | **0.936** | |

---

## Detailed Dimension Analysis

### Completeness (0.96/1.00)

**Evidence:**

All twelve success criteria from the gate brief are satisfied in the i4 deliverable:

1. Key findings are accurate and complete: line 9 states "100% compliance (0/90 violations) versus 92.2% for positive-only framing (7/90 violations), McNemar exact p=0.016, n=270 matched pairs." The 14-pattern taxonomy and CONDITIONAL GO are both stated.
2. NPT-013 and NPT-009 formats explained with examples: dedicated sections at lines 17-53, each with template format and a concrete example.
3. 14-pattern taxonomy table: complete at lines 75-90, NPT-001 through NPT-014, with technique type, evidence tier, and recommendation per pattern.
4. Practical application section: present at lines 96-152 including the `/prompt-engineering` skill agent table, NPT-009/NPT-013 decision table, and 3-step upgrade workflow.
5. A/B test methodology: documented at lines 155-198 in MkDocs `??? note` and `??? abstract` blocks with study design, results table, statistical tests.
6. CONDITIONAL GO honesty about effect size gap: present at lines 203-214, explicitly naming pi_d=0.078 vs pre-registered minimum 0.10.
7. Limitations section: present at lines 218-225, addressing open causal question and 60% hallucination claim.
8. "What the Research Did Not Change" subsection: present at lines 209-215 with 4 bullets (positive framing default, quality gate unchanged, C1 tasks unaffected, reversibility).
9. Implementation section: present at lines 229-247, listing all 4 ADRs with status and all 5 FEATs.
10. Cross-links: blog post link at line 287 resolves (file exists at `docs/blog/posts/structured-negation-constraint-enforcement.md`), SKILL.md link at line 289, NPT reference link at line 289, GitHub ADR links at line 247, go-no-go determination link at line 197.
11. Voice: direct, technically precise, warm without being effusive — characteristic McConkey/Saucer Boy register throughout.
12. Factual accuracy: substantially correct; one NPT-007 naming issue found (see Evidence Quality).

**Gaps:**

- None at the completeness level. The one naming issue in NPT-007 affects evidence quality but does not constitute a missing section.

**Improvement Path:**

Completeness is already at 0.96. The score would reach 0.97+ if the NPT-007 naming error were corrected (which would also ensure the pattern catalog is consistent with the source taxonomy — a completeness sub-requirement when source fidelity is part of the brief).

---

### Internal Consistency (0.93/1.00)

**Evidence:**

The i4 fixes resolved the most significant i3 issue: "Untested" was changed to "Untreated" in the Pattern Catalog table for NPT-007 (line 83: "Untreated baseline"). Statistical figures are internally consistent throughout: 0/90, 7/90, 2/90 violation counts; p=0.016; pi_d=0.078; 95% CI [0.023, 0.133]; Bonferroni alpha=0.0167; model-level breakdown (Haiku 10pp, Sonnet 2 violations, Opus 1 violation) all cross-check cleanly.

The CONDITIONAL GO verdict logic is internally consistent: lines 203-207 explain why conditional rather than unconditional (pi_d < 0.10 pre-registered minimum) without contradicting the statistical significance claim.

**Gaps:**

One residual inconsistency survives the i4 fix:

- Line 92: "NPT-007 (positive-only) **serves as the untested baseline** for comparison." The word "untested" was the i3 finding. The i4 fix applied "Untreated" to the table at line 83 but missed this prose instance at line 92. "Untested" and "Untreated" have distinct meanings in the research context: "untreated" is the correct A/B test terminology (NPT-007 = control/untreated condition); "untested" implies absence of investigation. The prose at line 92 still reads "untested."

Also at line 92: "NPT-007 (positive-only) serves as the untested baseline" — this conflates the A/B test condition label (positive-only = C1) with the taxonomy pattern name (NPT-007 = Blunt-Prohibition Baseline per source taxonomy, not positive-only framing). The article uses "positive-only" and "NPT-007" interchangeably throughout, which is consistent with the A/B test's condition coding but creates an internal tension with the Pattern Catalog table's name for NPT-007.

**Improvement Path:**

Fix line 92: change "untested" to "untreated." Optionally add a parenthetical clarifying that NPT-007 serves as the control condition label in the A/B test (C1), distinct from its taxonomy identity as "Blunt-Prohibition Baseline Acknowledgment." The internal consistency score would rise to approximately 0.96 with the single-word fix.

---

### Methodological Rigor (0.95/1.00)

**Evidence:**

The A/B test methodology section (lines 155-198) documents all substantive elements required for a rigorous empirical presentation:

- Scale: 270 blind invocations confirmed.
- Design: matched-pair, three conditions (C1 positive-only, C2 blunt prohibition, C3 structured negation), with concrete examples per condition.
- Constraints tested: 10 representative constraints spanning four constraint categories (behavioral timing H-22, tool restrictions H-05, architectural boundaries H-07, constitutional principles P-003/P-020/P-022).
- Pressure scenarios: three conditions (normal, mild, strong pressure) described.
- Scoring: binary compliance, no partial credit, blind independent scoring with inter-rater agreement verification.
- Statistical tests: McNemar exact test, Bonferroni correction, effect size pi_d with 95% CI.
- Limitation transparency: open causal question and 60% claim are addressed in the Limitations section.
- Pre-registration of PG-003: line 205 explicitly states the contingency was pre-specified.

The six-phase research pipeline table (lines 255-263) is complete with quality gate scores per phase.

**Gaps:**

- The methodology does not state the inter-rater agreement score (92.6% raw, AC1=0.920) in the article body — the go-no-go determination document contains this but the public article omits it. This is a minor gap for a public-facing article rather than a research paper proper; inter-rater agreement is implied by the "independent blind scoring with inter-rater agreement verification" language. Not penalized heavily for a documentation article.
- The statistical power analysis context (the study was designed to detect pi_d >= 0.10 at 80% power; observed pi_d=0.078 falls below the minimum detectable effect) is not surfaced in the article. The article correctly explains the effect size gap but does not note that the study was underpowered for the observed effect. This is a significant methodological nuance for intellectual honesty. The Limitations section could address this.

**Improvement Path:**

Adding a brief note that pi_d=0.078 falls below the minimum detectable effect (0.10) for which the study was powered would strengthen methodological transparency. This does not require a full power analysis section — one sentence in Limitations suffices.

---

### Evidence Quality (0.87/1.00)

**Evidence:**

The three anchor citations (Liu et al. AAAI 2026, Wen et al. EMNLP 2024, Barreto & Jana EMNLP 2025) are correctly cited with findings and relevance at lines 277-283. The distinction between negation comprehension and behavioral compliance is correctly drawn in the Barreto & Jana annotation.

The A/B test data is internally consistent with the go-no-go determination source document (verified: p=0.016, pi_d=0.078, CI [0.023, 0.133], C3=0/90, C1=7/90, C2=2/90, H22 share=6/9=67%).

**Gaps:**

One factual naming error with source data:

**NPT-007 name discrepancy.** The Pattern Catalog table (lines 75-90) labels NPT-007 as "Positive-Only Framing" with technique type "--". The authoritative source taxonomy (taxonomy-pattern-catalog.md v3.0.0, TASK-008, 2026-02-28) defines NPT-007 as "Blunt-Prohibition Baseline Acknowledgment," technique types A1 and A2, evidence tier T1. The NPT pattern reference file (npt-pattern-reference.md) confirms: NPT-007 is assigned to A2 (alongside NPT-006, NPT-009, NPT-010).

The confusion arises from the A/B test's condition coding: the A/B test uses "C1: Positive-only (NPT-007)" as a label. However, this is the condition code, not the taxonomy pattern name. NPT-007 in the taxonomy is the blunt prohibition baseline (worst-performing), not positive-only framing. The article's Pattern Catalog has absorbed the A/B condition label into the taxonomy table, overwriting the taxonomy's actual pattern name. This is a source-data fidelity error.

Additionally, the technique type "--" for NPT-007 in the article's table is incorrect — the source taxonomy assigns NPT-007 to A1/A2 (Prohibition-only / Structured prohibition). The article's table should show "A1/A2" or at minimum not leave it blank when all other patterns have technique type assignments.

Also at line 92, the prose correctly calls NPT-007 "positive-only" in the context of the A/B test but the footnote at line 83 says "untreated baseline" — this dual usage is not explained to the reader, creating potential for misunderstanding what NPT-007 actually represents.

**Improvement Path:**

1. Rename NPT-007 in the Pattern Catalog table from "Positive-Only Framing" to "Positive-Only Framing (C1 control condition)" or, more accurately, "Blunt-Prohibition Baseline (C1 condition = positive-only)" with a note explaining that NPT-007 labels the control condition in the A/B test.
2. Add the correct technique type for NPT-007: "A1/A2" per source taxonomy.
3. Consider a brief parenthetical in the table explaining the dual role of NPT-007 (taxonomy anti-pattern label AND A/B test C1 control condition label).

---

### Actionability (0.96/1.00)

**Evidence:**

The Practical Application section (lines 96-152) provides concrete, implementable guidance:

- Agent table with purpose and "when to use" for all three `/prompt-engineering` agents (pe-builder, pe-constraint-gen, pe-scorer) — lines 103-106.
- Natural-language invocation example for pe-constraint-gen — lines 108-114.
- NPT-009 vs NPT-013 decision table with five rows covering all major deployment contexts — lines 119-126.
- Three-step upgrade workflow with before/after examples and three quality criteria to check — lines 129-151.
- Three-criteria self-review checklist for finished constraints (binary-testable, specific consequence, achievable alternative) — line 151.

The Implementation section (lines 229-247) provides ADR status and feature status that tells a reader exactly what has been changed and what remains.

**Gaps:**

- The article does not explicitly tell the reader where to find the `/prompt-engineering` skill or how to invoke it (e.g., that it requires `/prompt-engineering` invocation keyword or that `pe-constraint-gen` is the agent for automated constraint generation). The SKILL.md link is present in References but not surfaced earlier in the Practical Application section. Minor gap.

**Improvement Path:**

Adding a one-line invocation example ("Use `/prompt-engineering` or invoke pe-constraint-gen directly") in the Practical Application opening paragraph would make the skill discoverable without requiring the reader to navigate to SKILL.md first.

---

### Traceability (0.93/1.00)

**Evidence:**

All primary sources link correctly:

- Go-no-go determination: line 197 links to correct path under `ab-testing-20260301-001/phase-3-analysis/go-no-go-determination.md` (file exists, verified).
- ADR links: lines 234-247 link to all four ADRs via GitHub branch paths.
- Phase 1 survey link: line 283 links to `phase-1/` directory.
- Final Synthesis (Phase 6): line 269.
- NPT Pattern Catalog: line 269.
- WORKTRACKER.md: line 269.
- Prompt Engineering SKILL.md: line 289.
- NPT Pattern Reference: line 289.
- Blog post: line 287 — file `docs/blog/posts/structured-negation-constraint-enforcement.md` exists (verified).
- Related Research cross-links: lines 295-298 — four internal research pages listed.

**Gaps:**

- The article's three academic citations use venue-level URLs (AAAI proceedings archive, ACL Anthology venue page) rather than direct paper DOIs. For a public documentation site, venue-level links are acceptable, but they require readers to search for the paper themselves. Traceability is adequate but not excellent.
- The "How This Research Was Conducted" section mentions "23 C4 quality gates across the entire project" (line 253) but does not link to or describe what those gates are. The phase table shows per-phase gate scores but the reader cannot trace back to the gate reports. Minor gap for a documentation article.

**Improvement Path:**

Adding DOI or direct links to the three anchor papers would raise this to 0.96. The "23 C4 quality gates" claim could be supported by a link to WORKTRACKER.md or the orchestration plan.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Evidence Quality | 0.87 | 0.93 | Fix NPT-007 name in Pattern Catalog table from "Positive-Only Framing" to reflect dual role: rename to "Positive-Only Framing (C1 control)" or "Blunt-Prohibition Baseline (C1=positive-only)" and add technique type "A1/A2" (currently "--") per source taxonomy |
| 2 | Internal Consistency | 0.93 | 0.96 | Fix line 92: change "serves as the **untested** baseline" to "serves as the **untreated** baseline" — the i4 fix applied this to the table but missed the prose instance |
| 3 | Methodological Rigor | 0.95 | 0.97 | Add one sentence in Limitations noting that the study was powered to detect pi_d >= 0.10 at 80% power, and the observed pi_d=0.078 falls below the minimum detectable effect — meaning the near-miss is not informative about whether the true effect exceeds 0.10 |
| 4 | Traceability | 0.93 | 0.96 | Replace venue-level citation URLs with direct DOI or ACL Anthology paper links for the three anchor citations |
| 5 | Actionability | 0.96 | 0.98 | Add one-line invocation example for `/prompt-engineering` skill in the Practical Application section opening |

---

## Leniency Bias Check

- [x] Each dimension scored independently before composite computed
- [x] Evidence documented for each score with specific line references
- [x] Uncertain scores resolved downward (Evidence Quality held at 0.87 despite strong overall quality; Internal Consistency held at 0.93 for single-word residual error)
- [x] Calibration anchors applied: 0.87 Evidence Quality = "most claims supported, one factual naming error against source data"; 0.93 Internal Consistency = "minor inconsistency (single word) after targeted fix"; 0.95 Methodological Rigor = "strong methodology with minor transparency gap on power analysis"
- [x] No dimension scored above 0.97 — all scores have documented ceiling rationale
- [x] Composite verified: (0.96 x 0.20) + (0.93 x 0.20) + (0.95 x 0.20) + (0.87 x 0.15) + (0.96 x 0.15) + (0.93 x 0.10) = 0.192 + 0.186 + 0.190 + 0.1305 + 0.144 + 0.093 = 0.9355 ≈ 0.936

---

## Composite Verification

| Dimension | Score | Weight | Weighted |
|-----------|-------|--------|---------|
| Completeness | 0.96 | 0.20 | 0.192 |
| Internal Consistency | 0.93 | 0.20 | 0.186 |
| Methodological Rigor | 0.95 | 0.20 | 0.190 |
| Evidence Quality | 0.87 | 0.15 | 0.1305 |
| Actionability | 0.96 | 0.15 | 0.144 |
| Traceability | 0.93 | 0.10 | 0.093 |
| **TOTAL** | | **1.00** | **0.9355** |

Rounded to three decimal places: **0.936**.

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.936
threshold: 0.95
weakest_dimension: evidence_quality
weakest_score: 0.87
critical_findings_count: 0
blocking_findings_count: 1
iteration: 4
improvement_recommendations:
  - "Fix NPT-007 name in Pattern Catalog: change 'Positive-Only Framing' to 'Blunt-Prohibition Baseline (C1 control = positive-only)' and add technique type 'A1/A2' per taxonomy-pattern-catalog.md v3.0.0"
  - "Fix line 92 prose: 'untested baseline' -> 'untreated baseline'"
  - "Add one sentence to Limitations: study powered for pi_d >= 0.10 at 80% power; pi_d=0.078 is below MDE, so near-miss is uninformative"
  - "Replace venue-level citation URLs with direct DOI/ACL Anthology paper links"
  - "Add /prompt-engineering invocation hint in Practical Application section"
gap_to_threshold: 0.014
estimated_i5_score: 0.952
```

---

## Appendix: i4 Fixes Verified

The four i4 fixes listed in the gate brief were verified:

| Fix | Verified | Notes |
|-----|----------|-------|
| "Untested" -> "Untreated" for NPT-007 in table | PARTIAL | Table at line 83: "Untreated baseline" PASS. Prose at line 92: "untested baseline" FAIL — fix was incomplete |
| "What the Research Did Not Change" subsection added | PASS | Lines 209-215, 4 bullets present |
| Blog post link verified as existing | PASS | `docs/blog/posts/structured-negation-constraint-enforcement.md` exists |
| URL conversion deferred to post-merge | ACKNOWLEDGED | Scope limitation noted; no score impact |
