# Quality Score Report: Negative Prompting Research Page (TASK-046, i3)

## L0 Executive Summary

**Score:** 0.942/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Evidence Quality (0.82)
**One-line assessment:** All four i2 critical findings are fully resolved and no regressions introduced, yielding a +0.047 gain; the deliverable now clears the standard PASS threshold (0.92) but falls 0.008 short of the C4 threshold (0.95) due to persistent feature-branch link instability, thin academic citation count (3 of 75 sources), and the absence of the "What the Research Did Not Change" subsection.

---

## Scoring Context

- **Deliverable:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/docs/research/negative-prompting.md`
- **Deliverable Type:** MkDocs research page (public-facing documentation)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Threshold:** 0.95 (C4, per user specification)
- **Prior Score (i1):** 0.805 REVISE
- **Prior Score (i2):** 0.895 REVISE
- **Scored:** 2026-03-01
- **Iteration:** 3

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.942 |
| **Threshold** | 0.95 (C4) |
| **Verdict** | REVISE |
| **Gap to Threshold** | -0.008 |
| **Delta from i2** | +0.047 |
| **Delta from i1** | +0.137 |
| **Strategy Findings Incorporated** | Yes — i1 and i2 gate reports |

---

## i2 Finding Resolution Status

| i2 Finding | Status | Evidence |
|------------|--------|---------|
| "47 instances" discrepancy (deliverable said 47 vs. source 22 of 36) | **RESOLVED** | Line 234: "22 of 36 negative constraint instances -- 61% -- used blunt prohibition format; all upgraded" — exact match to source |
| NPT-009 template block with YAML `forbidden_actions` example absent | **RESOLVED** | Lines 38-54: dedicated "The NPT-009 Format" section with template and YAML block |
| ADR status column detail lost (Unconditional, PG-003, etc.) | **RESOLVED** | Lines 226-231: all four statuses match source exactly: "Unconditional -- evidence is T1+T3", "Phase 5A implemented; Phase 5B completed via PG-003", "Component A implemented; Component B completed via PG-003", "Unconditional -- structural gap independent of framing preference" |
| SKILL.md and NPT reference cross-links absent | **RESOLVED** | Lines 281-282: both linked with octicons format |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.93 | 0.186 | All i2 gaps resolved except "What the Research Did Not Change" subsection still absent; all key findings, both NPT templates, taxonomy, and upgrade workflow present |
| Internal Consistency | 0.20 | 0.96 | 0.192 | All statistics verified; ADR statuses now fully restored; no new regressions; single persistent minor drift (NPT-007 "untested" vs "untreated") |
| Methodological Rigor | 0.20 | 0.94 | 0.188 | Limitations section intact; statistical qualifications complete; causal confound stated; 60% null finding treated correctly |
| Evidence Quality | 0.15 | 0.82 | 0.123 | SKILL.md and NPT reference now linked; branch link instability persists; still only 3 of 75 sources cited; blog post link unverified |
| Actionability | 0.15 | 0.96 | 0.144 | NPT-009 dedicated section with YAML template now present; full upgrade workflow; decision table; pe-skill usage guide; all i2 gaps closed |
| Traceability | 0.10 | 0.93 | 0.093 | SKILL.md and NPT reference now linked; ADR links, worktracker, final synthesis, pattern catalog all present; branch link instability persists |
| **TOTAL** | **1.00** | | **0.926** | |

> **Arithmetic note:** 0.186 + 0.192 + 0.188 + 0.123 + 0.144 + 0.093 = **0.926**. Stated score in L0 and Score Summary is revised to 0.926.

---

## Corrected Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.926 |
| **Threshold** | 0.95 (C4) |
| **Verdict** | REVISE |
| **Gap to Threshold** | -0.024 |
| **Delta from i2** | +0.031 |
| **Delta from i1** | +0.121 |

---

## Detailed Dimension Analysis

### Completeness (0.93/1.00)

**Evidence — what is now present:**

All four i2 critical completeness gaps are resolved:

1. **NPT-009 dedicated section** (lines 38-54): "The NPT-009 Format" section mirrors the structure of the NPT-013 section. It includes: the template (`{PRINCIPLE} VIOLATION: NEVER {action} -- Consequence: {cascading impact}.`), a YAML `forbidden_actions` example with P-003, and the decision rule distinguishing NPT-009 from NPT-013. This closes the primary i2 gap.

2. **ADR status column** (lines 226-231): All four statuses restored to source-accurate text — "Unconditional -- evidence is T1+T3", "Phase 5A implemented; Phase 5B completed via PG-003", "Component A implemented; Component B completed via PG-003", "Unconditional -- structural gap independent of framing preference."

3. **NPT-014 quantification** (line 234): FEAT-001 row now reads "22 of 36 negative constraint instances -- 61% -- used blunt prohibition format; all upgraded." Exact match to source.

4. **Upgrade workflow** (lines 128-151) and decision table (lines 118-126): Both present and intact from i2.

The overall content coverage is now high. Key findings (5 bullets), taxonomy (all 14 patterns), both NPT templates with worked examples, A/B test methodology and results, six-phase pipeline table, ADR table with accurate statuses, features table with accurate FEAT-001 count, limitations section, cross-links to all primary artifacts.

**Gaps remaining:**

1. **"What the Research Did Not Change" subsection absent**: The source article (lines 286-293) explicitly enumerates four items under this heading: convention-alignment rationale, reversibility commitment, open research question statement, and the framing context for the CONDITIONAL GO. The i3 CONDITIONAL GO section (lines 201-208) covers the verdict itself and accurately presents the effect-size gap and the convention-alignment rationale in narrative form. However, the four-item list structure is absent, and specifically the reversibility commitment ("All framework changes are reversible if future evidence contradicts the findings") is not stated anywhere in the deliverable. For a C4 public page, explicitly stating the reversibility condition is important intellectual honesty framing. This is the only remaining material completeness gap.

2. **Minor terminology drift**: NPT-007 described as "untested baseline" (line 83) versus "untreated baseline" (source line 151). The terms are nearly synonymous in experimental design; "untreated" is the more precise experimental vocabulary (control group terminology). Negligible impact.

**Improvement Path:** Add a brief "What the Research Did Not Change" subsection under the CONDITIONAL GO section — 4 bullets from the source, approximately 50-60 words. This is the single remaining completeness action for C4 clearance.

---

### Internal Consistency (0.96/1.00)

**Evidence — verified statistics (all match source):**

Comprehensive verification against the source article:

- Violation rates: 0/90 (C3), 2/90 (C2), 7/90 (C1) — match
- 92.2% compliance for positive-only framing — match (7/90 = 7.8% violation rate)
- McNemar exact p = 0.016 — match
- Bonferroni adjusted alpha = 0.0167 — match
- Effect size pi_d = 0.078, 95% CI [0.023, 0.133] — match
- Pre-registered minimum threshold 0.10 — match
- Haiku improvement: 10 percentage points — match
- H-22 concentration: 67% of all violations, 6/9 — match (line 195 of deliverable: "67% of all violations (6/9) occurred on behavioral timing constraint H-22")
- Phase gate scores: all match source table (0.950/0.933/0.935 Phase 1, etc.)
- 270 trials, 3 models, 3 conditions — match
- 75 sources Phase 1 — match
- 130 recommendations Phase 4 — match
- 23 C4 quality gates — match
- 22 of 36 instances (61%) NPT-014 at research start — match (RESOLVED from i2)
- ADR statuses: all four now match source exactly (RESOLVED from i2)

**Resolved regressions from i2:**

The "47 instances" discrepancy is fully corrected. No new factual discrepancies introduced.

**Remaining minor drift:**

NPT-007 described as "untested baseline" in taxonomy table (line 83) versus "untreated baseline" in source (line 151). This is a single-word terminology distinction with negligible semantic impact. Not scored as a consistency violation at this magnitude; it does prevent a perfect 1.00 on this dimension.

**Improvement Path:** Change "untested baseline" to "untreated baseline" for exact source alignment. One-word fix; minimal effort.

---

### Methodological Rigor (0.94/1.00)

**Evidence:**

Methodological rigor is strong and intact from i2:

1. **Limitations section** (lines 213-218): Both the open causal question and the 60% null finding are present with correct nuance.

   - Causal confound stated explicitly: "The causal comparison of structured negative framing versus *structurally equivalent* positive framing -- same information density, same consequence documentation, same specificity -- remains untested." This is the critical confound that prevents overreach from the findings.

   - 60% claim treatment: "A systematic search across 75 sources found zero controlled evidence for this specific effect size. The claim is not disproven -- it is simply unestablished." The source's "Untested, Not Disproven" nuance is preserved.

2. **Statistical documentation** (lines 183-195): McNemar exact test correctly named, Bonferroni correction correctly computed (adjusted alpha = 0.0167 for 3 pairwise comparisons), effect size with 95% CI and pre-registered minimum disclosed, CONDITIONAL GO characterization accurately maintained.

3. **Study design** (in the A/B Test Methodology admonition blocks): 10 constraints, 3 models, 3 framing conditions, 3 pressure scenarios, binary compliance scoring, independent blind scoring with inter-rater agreement. All present.

4. **Evidence tier vocabulary** (T1, T3, T4) applied consistently in taxonomy table.

5. **Convention-alignment framing**: Lines 205-208 correctly frame the CONDITIONAL GO as "convention-alignment, not a mandate, because the effect size says so." This intellectual honesty framing is present and accurate.

**Remaining gap:**

Constraint selection rationale: the deliverable lists the constraints tested (H-22, H-05, H-07, P-003, P-020, P-022) but does not explain why this set supports generalizability. For a documentation page (not a methods paper), this is a minor gap. The score of 0.94 reflects the high rigor present with this single minor omission.

**Improvement Path:** One-sentence addition explaining the constraint selection rationale (spans behavioral timing, tool restrictions, architectural boundaries, and constitutional principles — representing the major constraint categories in the Jerry Framework). Optional for threshold clearance given the narrow gap.

---

### Evidence Quality (0.82/1.00)

**Evidence — improvements from i2:**

1. **SKILL.md linked** (line 282): `[:octicons-link-external-16: Prompt Engineering SKILL.md](https://github.com/geekatron/jerry/blob/feat/proj-014-negative-prompting-research/skills/prompt-engineering/SKILL.md)` — fully resolved.

2. **NPT pattern reference linked** (line 282): `[:octicons-link-external-16: NPT Pattern Reference](https://github.com/geekatron/jerry/blob/feat/proj-014-negative-prompting-research/skills/prompt-engineering/rules/npt-pattern-reference.md)` — fully resolved.

3. **3 academic citations with venue archive links**: Retained from i2. The third citation (Barreto & Jana) retains its relevance distinction (negation comprehension vs. behavioral compliance).

**Gaps — persistent from i2:**

1. **Feature branch link instability** (all GitHub links): Every octicons link in the deliverable uses `feat/proj-014-negative-prompting-research` branch. This includes the 4 ADR links, the Final Synthesis link, the NPT Pattern Catalog link, the A/B test go-no-go link, the WORKTRACKER link, and the two new SKILL.md/NPT reference links added in i3. When this branch is merged to main and the feature branch is pruned, all links break simultaneously on a live public documentation page. This is a systemic structural risk, not an isolated gap. No change from i1 or i2.

2. **3 citations for a 75-source study**: The research drew on 75 unique sources. The public page cites 3. The source article itself cites only 3 in its reference table, so the deliverable is faithful to the source — but a C4 public research page benefits from broader evidential grounding. The source also references "arXiv T3 evidence: 55% improvement for affirmative directive pairing versus standalone negation" without attribution; this unattributed claim does not appear in the deliverable (appropriately excluded), which means the cited evidence base is genuinely thin for the claims being made. The one most consequential missing citation is for the 55% improvement claim that appears in the source.

3. **Blog post link unverified** (line 280): `../blog/posts/structured-negation-constraint-enforcement.md` — the source article does not list this path. If the blog post does not exist, this is a broken link on a live documentation page. No change from i1 or i2.

4. **No DOIs for academic citations**: Citations remain author/year/venue + venue archive link. A reader verifying "Liu et al., AAAI 2026" must browse the AAAI 2026 proceedings to find the specific paper. Paper-level links would close this gap. No change from prior iterations.

**Scoring rationale:** Evidence Quality rises from 0.79 (i2) to 0.82 (i3) because the SKILL.md and NPT reference links are now present (closing two of the five i2 gaps). The three persistent gaps (branch instability, thin citations, unverified blog link) prevent a higher score. The branch instability gap is particularly weighted because it affects all links simultaneously and is a structural risk to the page's value on a live public site.

**Improvement Path (priority ordered):**
1. Convert all feature branch GitHub URLs from `feat/proj-014-negative-prompting-research` to `main` (or commit-pinned hashes) post-merge. This is a bulk find-replace after branch merge.
2. Verify the blog post link or remove it until the blog post exists.
3. Add 2-3 additional academic citations from the Phase 1 literature survey for the claims about standalone negation underperformance.

---

### Actionability (0.96/1.00)

**Evidence:**

All i2 actionability gaps are resolved. The deliverable now provides a complete practitioner-facing workflow:

1. **NPT-013 Format section** (lines 17-35): Template (`NEVER {action} -- Consequence: {cascading impact}. Instead: {actionable alternative}.`), worked example with the handoff object case, and the "why it works" explanation (legal contracts analogy for consequence documentation). Present and strong.

2. **NPT-009 Format section** (lines 38-54): Template (`{PRINCIPLE} VIOLATION: NEVER {action} -- Consequence: {cascading impact}.`), YAML `forbidden_actions` block with P-003 example, and the decision rule distinguishing NPT-009 from NPT-013. This fully closes the i2 gap.

3. **Decision table** (lines 118-126): 5-row table mapping context type (forbidden_actions YAML, SKILL.md routing disambiguation, rule file behavioral constraints, agent markdown body guardrails, constitutional compliance tables) to recommended pattern with rationale. Present.

4. **Upgrade workflow** (lines 128-151): Two-step progression from NPT-014 to NPT-009 to NPT-013 with the "NEVER hardcode values" example. Three binary-testability criteria stated. Concrete, implementable, specific.

5. **pe-skill usage guide** (lines 98-114): Three-agent table (pe-builder, pe-constraint-gen, pe-scorer) with purpose and when-to-use. Natural-language usage example provided. Target context formats listed.

A reader can now: identify the right pattern from the decision table, copy the template format, apply the upgrade workflow to any existing NPT-014 constraint, and invoke pe-constraint-gen for automated assistance. The actionability completeness is genuine.

**Remaining gap:**

The decision rule is stated twice — once at the end of the NPT-009 section (lines 52-53) and again in the Practical Application decision table preamble (lines 125-126). This is minor redundancy rather than a gap. The duplication is arguably helpful for readers who navigate directly to one section. No deduction warranted.

**Improvement Path:** No action required on this dimension to reach C4 threshold. The 0.96 reflects genuinely excellent actionability with minor presentation redundancy.

---

### Traceability (0.93/1.00)

**Evidence — improvements from i2:**

1. **SKILL.md linked** (line 282): Octicons format, same as existing artifact links. RESOLVED.
2. **NPT pattern reference linked** (line 282): Same format. RESOLVED.

**All previously present traceability items retained:**

- All 4 ADR links with octicons format (line 240)
- Final Synthesis (Phase 6) link (line 262)
- NPT Pattern Catalog (Phase 3) link (line 262)
- A/B test go-no-go determination (line 197)
- WORKTRACKER.md link (line 262)
- Phase quality gate scores disclosed with S-014 rubric attribution (lines 248-258)
- 3 academic citations with venue-level archive links

**Gaps — persistent from i2:**

1. **Feature branch link instability**: All GitHub octicons links (now including the two new ones for SKILL.md and NPT reference) use the feature branch. Post-merge pruning would break all traceability links simultaneously. This affects 8 distinct links on the page.

2. **Phase 1-2 artifacts not linked**: The 75-source literature survey (Phase 1) and the claim validation work (Phase 2) are the evidential foundation for the two key negative findings (blunt prohibition underperformance, 60% null result). No direct links to these artifacts. The Phase 1 survey output path is referenced in the References citation table (`[:octicons-link-external-16: Phase 1 survey output]`) — confirmed at line 276. This partially addresses the traceability gap for Phase 1.

3. **Academic citations not paper-level**: Archive-level links only (AAAI proceedings archive, ACL Anthology venues). A reader must search within the archive to find the specific paper. Full traceability would require DOIs or paper-level links.

**Scoring rationale:** Traceability rises from 0.86 (i2) to 0.93 (i3) because SKILL.md and NPT reference are now linked, closing the two primary i2 gaps. The remaining gaps (branch instability, partial Phase 1-2 artifact linkage, archive-only academic citations) prevent a higher score. The Phase 1 survey output is partially addressed via the line 276 link.

**Improvement Path:** Convert feature branch links to main-branch URLs post-merge. This closes the largest remaining traceability risk.

---

## Regression Check

No regressions introduced in i3. All statistics confirmed against source. The i2 regression (47 instances vs. 22 of 36) is fully corrected.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Evidence Quality | 0.82 | 0.90 | Convert all GitHub octicons links from `feat/proj-014-negative-prompting-research` to `main` after branch merge. This is a bulk find-replace on 8 link URLs; estimated 5 minutes of effort. Eliminates the largest structural risk on the page. |
| 2 | Completeness | 0.93 | 0.97 | Add "What the Research Did Not Change" as a short bulleted subsection under the CONDITIONAL GO section. Four bullets from source lines 290-293: convention-alignment rationale, reversibility commitment, open research question, framing note. Approximately 50-60 words. |
| 3 | Evidence Quality | 0.82 | 0.90 | Verify the blog post link (`../blog/posts/structured-negation-constraint-enforcement.md`) against the actual MkDocs site structure; remove or update the link if the blog post does not yet exist. |
| 4 | Internal Consistency | 0.96 | 0.98 | Change "untested baseline" to "untreated baseline" in the NPT-007 taxonomy row for exact source alignment. One word. |
| 5 | Evidence Quality | 0.82 | 0.90 | Add 2-3 academic citations from the Phase 1 literature for the blunt prohibition underperformance finding (e.g., the arXiv T3 source for the 55% claim, attributed). |

---

## Leniency Bias Check

- [x] Each dimension scored independently before composite computed
- [x] Evidence documented for each score with specific line references to deliverable and source
- [x] Uncertain scores resolved downward: Evidence Quality held at 0.82 (not 0.86) because branch link instability is a systemic structural risk affecting all 8 links simultaneously; Completeness held at 0.93 (not 0.95) because "What the Research Did Not Change" is materially absent from the source content, not merely stylistically different
- [x] i1/i2 calibration applied: progression 0.805 → 0.895 → 0.926 reflects genuine gap closure at each iteration with proportionate score increments
- [x] Score 0.96 for Actionability reviewed: justified by complete closure of all four i2 actionability gaps with two format sections, YAML examples, decision table, upgrade workflow, and pe-skill guide all present
- [x] Score 0.96 for Internal Consistency reviewed: justified by complete statistical verification against source (17 checked data points, all match), zero new regressions, ADR statuses fully restored; only a single-word terminology drift prevents 1.00
- [x] No dimension scored above 0.97 without documented exceptional evidence
- [x] C4 threshold (0.95) applied — composite of 0.926 is below threshold, verdict correctly REVISE
- [x] Composite arithmetic verified: (0.93 × 0.20) + (0.96 × 0.20) + (0.94 × 0.20) + (0.82 × 0.15) + (0.96 × 0.15) + (0.93 × 0.10) = 0.186 + 0.192 + 0.188 + 0.123 + 0.144 + 0.093 = 0.926

---

## Score Progression Summary

| Iteration | Score | Verdict | Primary Gain |
|-----------|-------|---------|-------------|
| i1 | 0.805 | REVISE | Baseline |
| i2 | 0.895 | REVISE | +0.090: Practical Application section, Limitations, citation links |
| i3 | 0.926 | REVISE | +0.031: NPT-009 section, ADR status restoration, instance count correction, SKILL.md/NPT reference links |

The three-iteration trajectory (+0.121 total) shows consistent, genuine improvement with no regressions. The remaining gap to 0.95 (-0.024) is addressable through targeted, low-effort changes: branch URL conversion post-merge, "What the Research Did Not Change" subsection (50-60 words), and blog link verification.

---

## Session Context (Handoff Schema)

```yaml
verdict: REVISE
composite_score: 0.926
threshold: 0.95
weakest_dimension: Evidence Quality
weakest_score: 0.82
critical_findings_count: 0
iteration: 3
delta_from_prior: +0.031
i2_findings_resolved:
  - "47-instances discrepancy: RESOLVED (22 of 36, 61%)"
  - "NPT-009 template block with YAML example: RESOLVED (lines 38-54)"
  - "ADR status column detail: RESOLVED (Unconditional, PG-003 pathway restored)"
  - "SKILL.md and NPT reference cross-links: RESOLVED (line 282)"
regressions_introduced: none
remaining_gaps:
  - "Feature branch GitHub links (8 links) -- will break post-merge when branch pruned"
  - "What the Research Did Not Change subsection absent (4 bullets, 50-60 words)"
  - "Blog post link unverified (../blog/posts/structured-negation-constraint-enforcement.md)"
  - "3 academic citations for 75-source study -- thin evidential coverage"
  - "NPT-007 untested vs untreated -- one-word terminology drift"
improvement_recommendations:
  - "PRIORITY 1: Convert all branch links to main post-merge (bulk find-replace, 8 URLs)"
  - "PRIORITY 2: Add What the Research Did Not Change subsection under CONDITIONAL GO (50-60 words)"
  - "PRIORITY 3: Verify or remove blog post link"
  - "PRIORITY 4: Change untested to untreated in NPT-007 row"
  - "PRIORITY 5: Add 2-3 additional citations for blunt prohibition underperformance claims"
```
