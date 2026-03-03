# Quality Score Report: Tweet + Cross-Post — PROJ-014 Negative Prompting Research

## L0 Executive Summary

**Score:** 0.918/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Traceability (0.82)
**One-line assessment:** All statistics are accurate and the thread is genre-appropriate, but label inconsistency between the tweet and Post 1 (NPT-013 vs C3) and missing links in published form lower traceability; one targeted revision to align labels and note the [MEDIUM_URL]/[JERRY_DOCS_URL] placeholders as required items will close the gap.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-014-negative-prompting-research/orchestration/proj-014-completion-20260301-001/articles/tweet-crosspost.md`
- **Deliverable Type:** Social Media Artifact (tweet + cross-post thread)
- **Criticality Level:** C4 (publication artifact; threshold raised to >= 0.95 per scoring request)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Source Data Verified:** `orchestration/ab-testing-20260301-001/phase-3-analysis/mcnemar-tables.md`, `work/EPIC-006-validation-and-publication/TASK-025-ab-testing.md`, `articles/medium-negative-prompting.md`
- **Scored:** 2026-03-01

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.918 |
| **Threshold** | 0.95 (C4 per scoring request) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No — scored directly from source data cross-check |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.92 | 0.184 | All core findings present; 270 tests, 90 pairs, 3 models, 100%/92.2%, McNemar p, 56% timing, Haiku 10pp; 14-pattern taxonomy referenced in CTA; minor: no blunt-negation C2 result surfaced in thread |
| Internal Consistency | 0.20 | 0.94 | 0.188 | Statistics are internally consistent across tweet and all posts; one label discrepancy: tweet uses "NPT-013" while Post 1 uses "C3 (structured negation)" — same thing, but reader must infer equivalence |
| Methodological Rigor | 0.20 | 0.93 | 0.186 | Correct stats cited (p=0.016 exact McNemar, not asymptotic); correct framing of matched-pair rationale in CTA post; per-model non-significance omitted but acceptable at genre scale |
| Evidence Quality | 0.15 | 0.93 | 0.140 | All quantitative claims verified against source data: 270 invocations confirmed, 90 matched pairs confirmed, 7/90=7.8% violation rate confirmed, 56% timing violation rate confirmed (5/9 instances), Haiku 10pp confirmed; character counts self-reported and plausible |
| Actionability | 0.15 | 0.94 | 0.141 | Post 5 explicitly drives to Medium article + Jerry docs; NPT-013 three-component structure is stated verbatim in Post 3 for immediate use; "5 things you can apply today" teased in Post 5 |
| Traceability | 0.10 | 0.82 | 0.082 | [MEDIUM_URL] and [JERRY_DOCS_URL] are placeholders — not yet resolved to real links; NPT-013 label introduced in tweet without definition, C3 used in Post 1 without naming NPT-013, label unification is deferred to reader; no mention of 75-source literature base in thread |
| **TOTAL** | **1.00** | | **0.921** | |

> **Composite recalculation:** 0.184 + 0.188 + 0.186 + 0.140 + 0.141 + 0.082 = **0.921**

---

## Detailed Dimension Analysis

### Completeness (0.92/1.00)

**Evidence:**
The thread covers every major finding the genre requires:
- Core statistic: 100% vs 92.2%, 7.8pp gap (tweet, Post 1)
- Sample: 270 tests, 90 matched pairs, 3 models (Posts 1-2)
- Statistical significance: McNemar exact p=0.016 (Post 1)
- Mechanism: NPT-013 three-component structure (Post 3)
- Key insight: structure not polarity (tweet, Post 4a)
- Subgroup finding: 56% timing violation rate, Haiku 10pp (Post 4b)
- Taxonomy reference: "14-pattern NPT taxonomy" in CTA (Post 5)
- X format: 6-post thread (4a/4b split confirmed) with correct budget management

**Gaps:**
- C2 (blunt negation) result — 97.8% compliance — is not surfaced in any post. Omitting C2 is defensible for brevity, but it means readers cannot see the full three-way comparison that defines the CONDITIONAL GO decision. The finding that bare NEVER is better than positive-only but worse than structured negation is a meaningful nuance.
- The "75 academic/industry sources" literature base is not mentioned anywhere in the thread, making the research feel purely empirical without the foundational literature context.

**Improvement Path:**
Either add a brief mention of C2 result ("a bare NEVER hits 97.8% — better, but not sufficient") in Post 4b, or ensure it's captured in the CTA reference to the full article. The literature omission is acceptable for genre.

---

### Internal Consistency (0.94/1.00)

**Evidence:**
All statistics are consistent across tweet and all posts:
- 270 / 90 matched pairs / 3 models cited consistently in tweet and Posts 1-2
- 100% compliance and 92.2% cited identically in tweet and Post 1
- McNemar p=0.016 cited once (Post 1) — does not contradict anything elsewhere
- 56% timing violation rate and Haiku 10pp cited once (Post 4b) — consistent with Medium article source

**Gaps:**
One label inconsistency: the tweet uses "NPT-013 (structured negation)" while Post 1 uses "C3 (structured negation)". These are the same construct. The parenthetical "(structured negation)" connects them, but a reader encountering the tweet independently and then Post 1 must infer that NPT-013 = C3. The Medium article defines C3 as the NPT-013 format, but the thread does not explicitly bridge this.

Post 3 refers to "NPT-013" again without ever saying C3 = NPT-013. The thread uses both labels without unification.

**Improvement Path:**
In Post 1, change "C3 (structured negation)" to "NPT-013/C3 (structured negation)" or add a bridge phrase. Alternatively, pick one label and use it consistently across all posts.

---

### Methodological Rigor (0.93/1.00)

**Evidence:**
- Exact McNemar p-value used throughout (p=0.016, which is the exact two-sided value 0.0156 rounded correctly)
- Post 5 CTA explicitly distinguishes McNemar from chi-square for matched-pair designs: "why McNemar over chi-square for matched-pair designs" — this is methodologically correct and the right level of rigor for a CTA teaser
- "blind-scored by a separate model instance" in Post 2 correctly describes the scoring independence used in the A/B test
- "No cherry-picking" in Post 2 is accurate: C3 never lost a single matchup in the source data
- The three framing conditions (positive, blunt, structured) are correctly described in the Medium article but the thread only implies them

**Gaps:**
Per-model results are individually not significant (Haiku p=0.250, Sonnet p=0.500, Opus p=0.500 per `mcnemar-tables.md`). The thread does not mention this. In a research paper this would be a critical omission. For social media, it is within genre norms — the pooled result is significant and is what is reported. However, the claim "The 7.8pp gap held across every constraint and model" (tweet) is accurate as a directional statement (C3 never lost any matchup at any model) but could be misread as "each model individually hit significance." This is a borderline rigor issue.

The 56% violation rate for timing constraints is accurately sourced: the Medium article states "it failed in 5 out of 9 instances (56% violation rate)" which matches the tweet thread.

**Improvement Path:**
The per-model significance gap is acceptable at this genre. The "held across every constraint and model" phrasing is directionally correct (no counter-examples in any model). No mandatory change needed, but a careful reader could flag it. Verified as acceptable.

---

### Evidence Quality (0.93/1.00)

**Evidence — all claims verified against source data:**

| Claim in Artifact | Source | Verified |
|---|---|---|
| 270 tests | TASK-025: "C1/C2/C3 across 3 models, 270 total invocations" | Confirmed |
| 3 Claude models | mcnemar-tables.md: haiku, sonnet, opus | Confirmed |
| 90 matched pairs | mcnemar-tables.md: n=90 pooled | Confirmed |
| NPT-013 100% compliance | mcnemar-tables.md: C3 VIOLATE column = 0 across all 90 pairs | Confirmed |
| Positive-only 92.2% | TASK-025: "C1: 92.2%"; 7/90 violations = 7.8% violation rate | Confirmed |
| 7.8pp gap | 100% - 92.2% = 7.8pp | Confirmed |
| McNemar exact p=0.016 | mcnemar-tables.md: "Exact McNemar p-value = 0.0156" rounded to 0.016 | Confirmed |
| C3 never lost a matchup | mcnemar-tables.md: c=0 in all strata | Confirmed |
| 56% timing violation rate | medium-negative-prompting.md: "failed in 5 out of 9 instances (56% violation rate)" | Confirmed |
| Haiku 10pp improvement | mcnemar-tables.md: haiku C1=3 violations / 30 pairs = 10% violation rate, C3=0; delta=10pp | Confirmed |
| 14-pattern NPT taxonomy | TASK-025 context, medium article | Confirmed |

**Character counts:** Self-reported in the document. The stated ~216 chars for the tweet body was manually verified as approximately correct (manual count yields ~219-220; within normal counting variation). All posts claimed to be under 280 chars; no post appeared to exceed the budget based on visual inspection.

**Gaps:**
The character counts are self-asserted and not independently verified by a tool. The document's own count table shows all items under 280. Minor gap: Post 3 is listed as 271 chars; manual inspection confirms it is likely within budget but cannot be verified to the character without tooling.

**Improvement Path:**
Character counts should ideally be verified with a tool before publication, not self-reported. This is a pre-publication check, not a scoring blocker.

---

### Actionability (0.94/1.00)

**Evidence:**
- Post 3 delivers the NPT-013 three-component template verbatim: `NEVER {action} — Consequence: {what breaks downstream}. Instead: {compliant alternative}.` A reader can apply this immediately.
- Post 5 CTA is specific: directs to Medium article for methodology and "5 things you can apply today," and to Jerry docs for the full 14-pattern taxonomy.
- Two distinct URLs (MEDIUM_URL, JERRY_DOCS_URL) serve two audiences: practitioners who want the article, and framework users who want the taxonomy.
- The thread builds sequentially: hook (Post 1) → methodology credibility (Post 2) → actionable format (Post 3) → insight + subgroup finding (Posts 4a/4b) → CTA (Post 5). This is sound thread architecture.

**Gaps:**
Both URLs are placeholders ([MEDIUM_URL], [JERRY_DOCS_URL]) and not yet resolved. This is expected at the pre-publication stage, but the artifact cannot drive actual traffic until these are replaced. This is noted as a pre-publication requirement, not scored as a defect.

**Improvement Path:**
Replace placeholders with real URLs before publishing. No content changes needed.

---

### Traceability (0.82/1.00)

**Evidence:**
- Post 5 references both MEDIUM_URL and JERRY_DOCS_URL — these are the primary traceability links to source documentation.
- The 14-pattern NPT taxonomy is named in Post 5, traceable to the Jerry docs artifact.
- McNemar test methodology is correctly attributed ("why McNemar over chi-square for matched-pair designs") in Post 5, pointing readers to the full methodology in the article.

**Gaps:**
1. **Placeholder URLs:** [MEDIUM_URL] and [JERRY_DOCS_URL] are not resolved. The traceability chain from thread to source is incomplete until publication.
2. **Label bridge missing:** NPT-013 (tweet, Post 3) and C3 (Post 1, Post 2) are the same construct but never explicitly equated within the thread. A reader encountering the thread standalone cannot trace "C3" to "NPT-013" without reading the Medium article.
3. **No mention of 75-source literature base:** The research is grounded in 75 academic/industry sources; this is the foundation of the taxonomy. The thread presents it as purely empirical without acknowledging the literature review component.
4. **Bonferroni caveat:** The McNemar result passes Bonferroni correction marginally (p=0.016 vs. adjusted alpha=0.0167 per the Medium article). The tweet/thread presents "statistically significant" without noting the marginality. This is acceptable for social media but a traceability gap for rigorous readers.

**Improvement Path:**
- Priority 1: Resolve placeholder URLs before publication.
- Priority 2: Add one phrase unifying NPT-013 = C3 labels (e.g., change "C3 (structured negation)" in Post 1 to "NPT-013 — structured negation").
- Priority 3 (optional): Add a brief mention of the literature foundation ("75 sources across AAAI, NeurIPS, EMNLP") somewhere in the thread to establish research pedigree.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Traceability | 0.82 | 0.90 | Resolve [MEDIUM_URL] and [JERRY_DOCS_URL] placeholders before publication — these are required for any traceability chain |
| 2 | Internal Consistency | 0.94 | 0.97 | Unify NPT-013/C3 labels: change "C3 (structured negation)" in Post 1 to "NPT-013 (structured negation)" to match tweet and Post 3; removes inferential burden on reader |
| 3 | Completeness | 0.92 | 0.95 | Optional: add one sentence in Post 4b noting the C2 (blunt negation) result — "a bare NEVER improves on positive-only (97.8%) but falls short of structured negation" — to show the full three-way comparison |
| 4 | Traceability | 0.82 | 0.88 | Optional: add "grounded in 75 academic/industry sources" in Post 2 to anchor empirical findings in literature review |

---

## Verdict Assessment

**Composite score: 0.921 against C4 threshold of 0.95.**

This artifact scores below the C4 threshold. The gap (0.029) is meaningful and driven primarily by the traceability dimension (0.82), which reflects real gaps: unresolved URL placeholders and a label inconsistency that creates inferential burden for standalone readers.

**Critical path to PASS:**
- Priority 1 (URL resolution) is a pre-publication operational requirement, not a content defect. Resolving it would raise Traceability from 0.82 to approximately 0.90.
- Priority 2 (label unification) is a one-phrase edit. Resolving it would raise Internal Consistency from 0.94 to approximately 0.97.
- With both changes applied, estimated composite: (0.95 * 0.92) + (0.97 * 0.90) + (other dimensions unchanged) = approximately 0.934–0.938. Still below 0.95.

**Honest assessment of the 0.95 C4 threshold for this artifact type:**
The 0.95 threshold for C4 is calibrated for architecture decisions and governance artifacts. Social media artifacts have an inherent constraint: character limits prevent the degree of nuance, caveat documentation, and traceability that would normally satisfy C4 rigor. The tweet/thread is accurate, well-constructed, and ready for publication pending URL resolution and the label fix. The score gap reflects the genre constraint as much as any content deficiency.

**Recommended path forward:** Apply Priority 1 and Priority 2 changes (URL resolution + label unification). Re-score after URL resolution; expected composite 0.934–0.938, which may warrant threshold recalibration for social media artifacts.

---

## Leniency Bias Check

- [x] Each dimension scored independently before composite computed
- [x] Evidence documented for each score (source data cross-referenced against mcnemar-tables.md, TASK-025, medium-negative-prompting.md)
- [x] Uncertain scores resolved downward (Traceability: placeholder URLs and label gap both penalized)
- [x] Genre-appropriate calibration applied (social media artifacts cannot achieve C4 documentation depth by design; gaps that are genre-unavoidable noted but still scored)
- [x] No dimension scored above 0.95 without exceptional justification
- [x] Statistics verified independently against source data — no dimension score was elevated due to trust in self-reported numbers; all key statistics confirmed

---

## Session Context (Handoff Schema)

```yaml
verdict: REVISE
composite_score: 0.921
threshold: 0.95
weakest_dimension: traceability
weakest_score: 0.82
critical_findings_count: 0
iteration: 1
improvement_recommendations:
  - "Resolve [MEDIUM_URL] and [JERRY_DOCS_URL] placeholders — required before publication"
  - "Unify NPT-013/C3 labels: change 'C3 (structured negation)' in Post 1 to 'NPT-013 (structured negation)'"
  - "Optional: add C2 (97.8%) result in Post 4b for three-way comparison completeness"
  - "Optional: reference 75-source literature base in Post 2"
```

*Score Report Version: 1.0*
*Agent: adv-scorer*
*SSOT: `.context/rules/quality-enforcement.md`*
*Scored: 2026-03-01*
