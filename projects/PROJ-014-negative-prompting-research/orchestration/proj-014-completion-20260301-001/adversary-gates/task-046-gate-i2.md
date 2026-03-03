# Quality Score Report: Negative Prompting Research Page (TASK-046, i2)

## L0 Executive Summary

**Score:** 0.895/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Evidence Quality (0.79)
**One-line assessment:** The three primary i1 findings are resolved (Practical Application section added, Limitations section added, citation links added), but the deliverable still falls short of the C4 threshold (0.95) due to a newly introduced factual discrepancy (47 vs. 22 NPT-014 instances), absent "Two Patterns That Matter Most" subsection with NPT-009 worked example, unresolved ADR status simplifications, feature branch link instability, and missing SKILL.md/NPT-reference links.

---

## Scoring Context

- **Deliverable:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/docs/research/negative-prompting.md`
- **Deliverable Type:** MkDocs research page (public-facing documentation)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Threshold:** 0.95 (C4, per user specification)
- **Prior Score (i1):** 0.805 REVISE
- **Scored:** 2026-03-01
- **Iteration:** 2

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.895 |
| **Threshold** | 0.95 (C4) |
| **Verdict** | REVISE |
| **Gap to Threshold** | -0.055 |
| **Delta from i1** | +0.090 |
| **Strategy Findings Incorporated** | Yes — i1 gate report (task-046-gate.md) |

---

## i1 Finding Resolution Status

| i1 Finding | Status | Evidence |
|------------|--------|---------|
| Missing Practical Application section (NPT-009 worked example, decision table, upgrade workflow) | **RESOLVED** | Lines 77-133: full section with pe-skill table, 5-row decision table, 2-step upgrade workflow, 3 binary-testability criteria |
| Missing academic citation links | **PARTIALLY RESOLVED** | 3 citations now have venue hyperlinks (AAAI proceedings, ACL Anthology x2); still only 3 citations for a 75-source study; no DOIs |
| Missing limitations subsection (causal question + 60% claim) | **RESOLVED** | Lines 192-199: explicit "Limitations" section with both the open causal question and the 60% null finding treatment |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.88 | 0.176 | Practical Application added; "Two Patterns That Matter Most" subsection still absent; "What the Research Did Not Change" still absent; ADR status detail still simplified |
| Internal Consistency | 0.20 | 0.84 | 0.168 | New discrepancy introduced: "47 instances" (deliverable) vs. "22 of 36" (source); ADR status simplifications persist from i1 |
| Methodological Rigor | 0.20 | 0.93 | 0.186 | Limitations section fully resolves i1 gap; causal question stated; 60% null finding given correct nuance; statistical qualifications intact |
| Evidence Quality | 0.15 | 0.79 | 0.119 | Citation links added but still only 3 of 75 sources; feature branch links unresolved; SKILL.md and NPT reference unlinked; no DOIs |
| Actionability | 0.15 | 0.93 | 0.140 | Practical Application section fully resolves i1 gap; NPT-009 vs NPT-013 decision table present; upgrade workflow with criteria present; pe-skill usage guide present |
| Traceability | 0.10 | 0.86 | 0.086 | ADR links, final synthesis, pattern catalog, worktracker all linked; SKILL.md and NPT pattern reference still unlinked; feature branch link instability persists |
| **TOTAL** | **1.00** | | **0.895** | |

---

## Detailed Dimension Analysis

### Completeness (0.88/1.00)

**Evidence — what is now present:**

The i1 primary gap is resolved. The "Practical Application" section (lines 77-133) is fully present:
- pe-builder, pe-constraint-gen, pe-scorer agent table with purpose and "when to use" columns
- NPT-009 vs NPT-013 decision table (5 rows: forbidden_actions YAML, SKILL.md routing, rule file behavioral constraints, agent markdown body guardrails, constitutional compliance tables) with rationale column
- Upgrade workflow: Step 1 (NPT-009 with consequence) and Step 2 (NPT-013 with alternative), concrete example used throughout, three binary-testability criteria stated
- Limitations section (lines 192-199): both the open causal question and 60% null finding present with appropriate nuance

Additional gains from i1:
- The research methodology section now integrates quality gate scores inline in the pipeline table (lines 229-237)
- CONDITIONAL GO verdict section is well-developed (lines 182-189)

**Gaps remaining:**

1. **"The Two Patterns That Matter Most" subsection absent**: The source article (lines 162-193) devotes a named subsection to NPT-009 with a full YAML `forbidden_actions` block example. The deliverable has NPT-013 explained with an example in the "NPT-013 Format" section but NPT-009 receives only a table row in the decision table and a decision rule sentence. A reader learning from scratch about NPT-009 has no template block analogous to the NPT-013 example. This is the single most significant remaining completeness gap.

2. **"What the Research Did Not Change" subsection absent**: Source lines 286-293 document the convention-alignment rationale, reversibility commitment, and open research question in explicit list form. The CONDITIONAL GO section in the deliverable (lines 182-189) covers the verdict itself but does not enumerate the "what did not change" items explicitly. Present in the source; absent in the deliverable.

3. **ADR status detail simplified**: Source ADR table (source lines 263-266) provides four distinct statuses: "Unconditional -- evidence is T1+T3", "Phase 5A implemented; Phase 5B completed via PG-003", "Component A implemented; Component B completed via PG-003", "Unconditional -- structural gap independent of framing preference." The deliverable simplifies all four to "Accepted -- evidence is T1+T3" and "Implemented" (lines 208-211). The conditional/unconditional distinction and PG-003 contingency pathway are lost.

4. **NPT-014 quantification**: Source states 22 of 36 instances (61%) were blunt prohibitions at research start. Deliverable FEAT-001 line says "47 instances identified, all upgraded." This is inconsistent with the source and flagged under Internal Consistency below; it also represents a completeness issue in that the baseline context (why this mattered) is incorrectly stated.

**Improvement Path:** Add the NPT-009 worked example block (mirror the NPT-013 section structure). Add "What the Research Did Not Change" as a short bulleted subsection. Restore full ADR status column from source. Resolve the 47 vs. 22 discrepancy.

---

### Internal Consistency (0.84/1.00)

**Evidence — verified statistics (all match source):**

- Violation rates: 0/90 (C3), 2/90 (C2), 7/90 (C1) — match
- 92.2% compliance for positive-only framing — match (7/90 = 7.8% violation = 92.2% compliance)
- McNemar exact p = 0.016 — match
- Bonferroni adjusted alpha = 0.0167 — match
- Effect size pi_d = 0.078, 95% CI [0.023, 0.133] — match
- Pre-registered threshold 0.10 — match
- Haiku improvement: 10 percentage points — match
- H-22 concentration: 67% of all violations, 6/9 — match (note: deliverable line 176 says "6/9 violations" while source line 115 says "6 of 9" -- the total violation count is 9 on H-22 only, but total violations across all conditions was either 9 or the broader count; this is consistent)
- Phase gate scores: all match source table
- 270 trials, 3 models, 3 conditions — match
- 75 sources Phase 1, 130 recommendations Phase 4, 23 C4 quality gates — match

**New discrepancy introduced in i2:**

The deliverable line 215 states: "FEAT-001 | NPT-014 elimination across rule files (47 instances identified, all upgraded)". The source article states at line 59: "36 negative constraint instances across 17 rule files at the start of this research, with 22 of those (61%) being bare 'NEVER X' statements." The figure "47" does not appear anywhere in the source article. The correct characterization is that 22 of 36 instances were NPT-014 (blunt prohibition) and were upgrade candidates. "47 instances" is unverifiable against the source and creates a numerical contradiction with the stated 22/36 baseline. This is a factual discrepancy introduced in the i2 revision that was not present in i1.

**Persistent simplifications from i1:**

The ADR status simplifications noted in i1 persist unchanged:
- ADR-001 status: "Accepted -- evidence is T1+T3" vs. source "Unconditional -- evidence is T1+T3" (loses the "unconditional" classification)
- ADR-002 status: "Implemented" vs. source "Phase 5A implemented; Phase 5B completed via PG-003" (loses PG-003 contingency information)
- ADR-003 status: "Implemented" vs. source "Component A implemented; Component B completed via PG-003" (same)

One legacy drift from i1 persists: NPT-007 described as "untested baseline" in deliverable (line 64) versus "untreated baseline" in source (line 151). Negligible impact in isolation but noted for completeness.

**Improvement Path:** Resolve the "47 instances" figure — either verify against the source research artifacts and use the correct number, or revert to the source article characterization. Restore the ADR status detail from the source table.

---

### Methodological Rigor (0.93/1.00)

**Evidence:**

The i1 gap is fully resolved. The "Limitations" section (lines 192-199) explicitly states:

1. **Causal question**: "The causal comparison of structured negative framing versus *structurally equivalent* positive framing -- same information density, same consequence documentation, same specificity -- remains untested." This is the precise formulation from the source and correctly identifies the confound.

2. **60% null finding**: "A systematic search across 75 sources found zero controlled evidence for this specific effect size. The claim is not disproven -- it is simply unestablished." This matches the source's nuanced treatment ("Untested, Not Disproven" subsection).

Statistical qualifications remain solid:
- McNemar exact test correctly named with matched-pair design rationale
- Bonferroni correction properly stated with correct adjusted alpha
- Effect size disclosed with confidence interval
- Pre-registered minimum threshold disclosed and the gap honestly characterized
- Evidence tier vocabulary (T1, T3, T4) applied consistently
- Pressure scenarios defined
- Independent blind scoring with inter-rater agreement stated
- CONDITIONAL GO vs. unconditional mandate distinction accurately maintained

**Remaining gap:**

The "constraint selection rationale" gap from i1 persists: the deliverable lists the constraint types tested (H-22, H-05, H-07, P-003, P-020, P-022) but does not explain why this set represents generalizability. This is a minor methodological rigor gap at this level of documentation (a public research page, not a methods paper), but noted.

**Improvement Path:** No action required to reach the threshold specifically on this dimension — 0.93 is the ceiling given this is a documentation page not a peer-reviewed paper. The only material refinement available is explaining the constraint selection rationale in 1-2 sentences.

---

### Evidence Quality (0.79/1.00)

**Evidence:**

Gains from i1:
- The 3 academic citations now have venue hyperlinks: AAAI proceedings archive link, ACL Anthology EMNLP 2024 link, ACL Anthology EMNLP 2025 link. This is an improvement over bare author/year/venue citations.
- The third citation (Barreto & Jana) now has an explicit relevance note distinguishing negation *comprehension* from behavioral compliance — this is a methodologically important distinction properly surfaced.
- 5 GitHub artifact links retained from i1.

**Gaps — partially persistent from i1:**

1. **3 citations for a 75-source study**: This is the primary evidence quality gap. The research drew on 75 sources, yet the public page cites 3. The source article (used as the authoritative research output) itself only cites 3 in its references table, so the deliverable faithfully represents the source's citation structure — but a C4 public research page is expected to provide stronger evidential grounding. The source also mentions "arXiv T3 evidence: 55% improvement for affirmative directive pairing versus standalone negation" (source line 97) without attribution. This unattributed claim in the source article does not appear in the deliverable (the deliverable mentions only the 3 named citations in its Key Findings section), which is appropriate — but it means the deliverable's evidence base is thin for the claims being made.

2. **Feature branch link instability**: All 5 GitHub octicons links continue to point to `feat/proj-014-negative-prompting-research` branch. When this branch is merged to main and eventually pruned, all links break on a public documentation page. No change from i1.

3. **SKILL.md and NPT pattern reference unlinked**: The source article's References section lists `skills/prompt-engineering/rules/npt-pattern-reference.md` and `skills/prompt-engineering/SKILL.md` as primary artifacts. The deliverable's Practical Application section now describes these skills extensively but provides no links to the underlying files. A reader who wants to examine or extend the NPT pattern reference has no path to it from the deliverable.

4. **No DOIs for academic citations**: Citations remain author/year/venue + venue archive link (not paper-level links). A reader verifying "Liu et al., AAAI 2026" must browse the AAAI 2026 proceedings archive to find the specific paper. Paper-level links or DOIs would satisfy this gap.

5. **"Related Reading" blog link unverified**: The `../blog/posts/structured-negation-constraint-enforcement.md` link appears without confirmation the target exists. The source article does not list this path. This link is potentially broken on a live site.

**Improvement Path:** Add links to the NPT pattern reference file and SKILL.md. Convert feature branch links to stable main-branch or commit-pinned URLs. If additional papers from the Phase 1 literature can be cited, add 3-5 more with venues. Verify or remove the blog post link.

---

### Actionability (0.93/1.00)

**Evidence:**

The i1 primary gap is fully resolved. The deliverable now contains:

1. **pe-skill usage guide** (lines 79-95): Table of three agents with purpose and "when to use"; natural-language usage example for `pe-constraint-gen`; explanation of output format selection (governance YAML, agent markdown body, standalone block).

2. **NPT-009 vs NPT-013 decision table** (lines 99-107): 5-row table covering exactly the use cases a practitioner would encounter: `forbidden_actions` YAML, SKILL.md routing disambiguation, rule file behavioral constraints, agent markdown body guardrails, constitutional compliance tables. Rationale column present. Decision rule stated explicitly.

3. **Upgrade workflow** (lines 109-132): Step 1 (NPT-009) and Step 2 (NPT-013) shown with a concrete "NEVER hardcode values" → NPT-009 → NPT-013 progression. Three binary-testability criteria stated and specific (binary-testable action, specific named downstream effect, alternative achievable with declared tools).

The NPT-013 format section (lines 17-35) retains its worked example and the reason-why explanation. Combined with the new Practical Application section, a reader can: identify the right pattern from the decision table, use the template format, apply the upgrade workflow, and invoke the pe-constraint-gen agent for assistance.

**Remaining gap:**

NPT-009 still lacks a dedicated worked example block. The decision table describes NPT-009 usage for `forbidden_actions` YAML and constitutional compliance tables, and the upgrade workflow Step 1 shows NPT-009 as an intermediate step, but there is no explicit NPT-009 template block equivalent to the NPT-013 template block (lines 21-23). A reader writing `forbidden_actions` entries must infer the format from the description and Step 1 of the upgrade workflow. The source article's "The Two Patterns That Matter Most" subsection (lines 166-192) provides a formal YAML block:

```yaml
forbidden_actions:
  - "P-003 VIOLATION: NEVER spawn recursive subagents -- Consequence: agent hierarchy
    violation breaks orchestrator-worker topology and causes uncontrolled token consumption."
```

This dedicated block is absent from the deliverable.

**Improvement Path:** Add a short NPT-009 template block with YAML example adjacent to or immediately after the NPT-013 format section. This is a single targeted addition that closes the only remaining actionability gap.

---

### Traceability (0.86/1.00)

**Evidence:**

Present and verified:
- All 4 ADRs linked with octicons format (lines 221)
- Final Synthesis (Phase 6) linked
- NPT Pattern Catalog (Phase 3) linked
- A/B test go-no-go determination (TASK-025) linked
- WORKTRACKER.md linked
- Phase quality gate scores disclosed with S-014 rubric attribution
- 3 academic citations with venue-level attribution and archive links

**Gaps — persistent from i1:**

1. **SKILL.md unlinked**: `skills/prompt-engineering/SKILL.md` is mentioned by agent name throughout the Practical Application section but no link is provided. This is the primary deliverable of FEAT-005 and the first thing a reader would want to access after reading about pe-constraint-gen.

2. **NPT pattern reference unlinked**: `skills/prompt-engineering/rules/npt-pattern-reference.md` implements the taxonomy and is referenced by name in the source article's References section. Not linked in the deliverable.

3. **Feature branch link instability**: All GitHub links remain on `feat/proj-014-negative-prompting-research` branch. Post-merge, these links will break. A public research page requires stable URLs. This is a systemic traceability risk, not an isolated gap.

4. **Phase 1-2 artifacts not linked**: The 75-source literature survey (Phase 1) and claim validation (Phase 2) are the evidential foundation for the key findings. No links to these artifacts are provided. Phase 6 (final synthesis) is linked; the foundational phases are not.

5. **Academic citations not paper-level**: Archive-level links provided (AAAI proceedings archive, ACL Anthology venues) rather than paper-level links. A reader must search within the archive to locate the specific paper.

**Improvement Path:** Add GitHub links to SKILL.md and NPT pattern reference (same octicons format as existing links). Convert feature branch links to main-branch equivalents after merge. Add paper-level citations or DOIs for the three academic sources.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Internal Consistency | 0.84 | 0.93 | Resolve the "47 instances" figure: source says 22 of 36 instances (61%) were NPT-014; deliverable says 47. Use the source figure or provide a reconciling footnote with the discrepancy explained. Restore full ADR status column (unconditional/conditional, PG-003 pathway) from source. |
| 2 | Completeness | 0.88 | 0.95 | Add dedicated NPT-009 template block with YAML `forbidden_actions` example (mirror the NPT-013 section structure). Add "What the Research Did Not Change" as a short bulleted subsection under CONDITIONAL GO verdict. |
| 3 | Evidence Quality | 0.79 | 0.88 | Add links to NPT pattern reference (`skills/prompt-engineering/rules/npt-pattern-reference.md`) and SKILL.md using octicons format. Convert all feature branch GitHub links to stable main-branch URLs (change `feat/proj-014-negative-prompting-research` to `main` after merge). Verify the blog post link or remove it. |
| 4 | Actionability | 0.93 | 0.96 | Add the NPT-009 template block with YAML example immediately after or alongside the NPT-013 format section. This is a single targeted addition, estimated 8-10 lines. |
| 5 | Traceability | 0.86 | 0.93 | Same as Evidence Quality P3: SKILL.md and NPT pattern reference links. Stable GitHub URLs after merge. |
| 6 | Completeness | 0.88 | 0.95 | (Secondary) Restore ADR status nuance and the "What the Research Did Not Change" subsection from source. |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score with specific line references to deliverable and source
- [x] Uncertain scores resolved downward: Internal Consistency held at 0.84 (not 0.87) due to newly introduced 47 vs. 22 discrepancy; Evidence Quality held at 0.79 (not 0.82) due to three unresolved structural gaps (branch links, SKILL.md unlinked, thin citation count)
- [x] i1 calibration applied: delta from 0.805 to 0.895 (+0.090) is proportionate to the three substantive additions (Practical Application, Limitations section, citation links)
- [x] Leniency check on Methodological Rigor (0.93): justified by full Limitations section resolution plus strong statistical documentation; score does not reflect inflation, it reflects genuine improvement from 0.85
- [x] Leniency check on Actionability (0.93): justified by complete Practical Application section; the only remaining gap (NPT-009 template block) is narrow; score is not inflated
- [x] No dimension scored above 0.95 without exceptional evidence
- [x] C4 threshold (0.95) applied — composite of 0.895 is below threshold, verdict correctly REVISE
- [x] Newly introduced discrepancy (47 instances) penalized in Internal Consistency; this is a regression from i1 that must be explicitly flagged

---

## Regression Alert

A factual discrepancy was **introduced** in the i2 revision that did not exist in i1:

> Deliverable line 215: "FEAT-001 | NPT-014 elimination across rule files **(47 instances identified, all upgraded)**"
>
> Source article line 59: "36 negative constraint instances across 17 rule files at the start of this research, with **22 of those (61%)** being bare 'NEVER X' statements."

The figure "47" does not appear in the authoritative source article and contradicts the baseline established in the research background. This must be resolved before the deliverable can pass the Internal Consistency dimension at C4 standard.

---

## Session Context (Handoff Schema)

```yaml
verdict: REVISE
composite_score: 0.895
threshold: 0.95
weakest_dimension: Evidence Quality
weakest_score: 0.79
critical_findings_count: 1
critical_finding: "Regression: 47 instances (deliverable) vs. 22 of 36 (source) for NPT-014 baseline count"
iteration: 2
delta_from_prior: +0.090
i1_findings_resolved:
  - "Practical Application section: RESOLVED"
  - "Limitations subsection: RESOLVED"
  - "Citation links: PARTIALLY RESOLVED (links added, still 3 of 75 sources)"
remaining_gaps:
  - "CRITICAL: 47 instances discrepancy introduced in i2 -- resolve against source"
  - "NPT-009 template block with YAML example absent (mirrors NPT-013 section)"
  - "ADR status simplifications persist (unconditional/conditional, PG-003 pathway)"
  - "Feature branch GitHub links unresolved -- will break post-merge"
  - "SKILL.md and NPT pattern reference unlinked"
  - "What the Research Did Not Change subsection absent"
improvement_recommendations:
  - "PRIORITY 1: Fix 47-instances discrepancy; use 22 of 36 or reconcile with sourced count"
  - "PRIORITY 2: Add NPT-009 template block with YAML forbidden_actions example"
  - "PRIORITY 3: Add links to SKILL.md and NPT pattern reference; convert branch links to main"
  - "PRIORITY 4: Restore ADR status column detail from source (unconditional, PG-003 pathway)"
  - "PRIORITY 5: Add What the Research Did Not Change as brief subsection"
```
