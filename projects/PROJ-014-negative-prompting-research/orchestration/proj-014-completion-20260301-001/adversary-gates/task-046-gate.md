# Quality Score Report: Negative Prompting Research Page (TASK-046)

## L0 Executive Summary

**Score:** 0.805/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Actionability (0.72)
**One-line assessment:** The page accurately presents all key statistics and the full taxonomy but is missing the entire "Practical Application" section from the source article -- the section that operationalizes the findings -- leaving the reader knowing the format without being able to systematically apply it. Does not meet the C4 threshold of 0.95.

---

## Scoring Context

- **Deliverable:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/docs/research/negative-prompting.md`
- **Deliverable Type:** MkDocs research page (public-facing documentation)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Threshold:** 0.95 (C4, per user specification)
- **Scored:** 2026-03-01

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.805 |
| **Threshold** | 0.95 (C4) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No |
| **Gap to Threshold** | -0.145 |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.77 | 0.154 | Key findings, taxonomy, methodology, cross-links present; entire Practical Application section absent |
| Internal Consistency | 0.20 | 0.88 | 0.176 | All statistics verified against source; two ADR status simplifications (not contradictions) |
| Methodological Rigor | 0.20 | 0.85 | 0.170 | Statistical qualifications correct; 60% null finding passingly noted; no limitations section |
| Evidence Quality | 0.15 | 0.76 | 0.114 | 3 academic citations (thin for 75-source study); 5 GitHub links all on feature branch |
| Actionability | 0.15 | 0.72 | 0.108 | NPT-013 template present; NPT-009 decision table, upgrade workflow, pe-skill usage absent |
| Traceability | 0.10 | 0.83 | 0.083 | 5 GitHub links, 4 ADRs linked; NPT reference file and SKILL.md not linked |
| **TOTAL** | **1.00** | | **0.805** | |

---

## Detailed Dimension Analysis

### Completeness (0.77/1.00)

**Evidence:**

Present and confirmed against source:
- All 5 Key Findings bullets (100% vs 92.2%, CONDITIONAL GO, blunt prohibition anti-pattern, concentration at behavioral timing, 14-pattern taxonomy)
- Full NPT taxonomy: all 14 patterns with Type, Evidence tier, and Recommendation columns match source exactly
- All 7 technique types (A1-A7) with descriptions
- A/B test methodology: study design and results summary in admonition blocks
- 6-phase pipeline quality gate table with all gate scores
- ADR table (4 ADRs) and features table (5 features)
- Implementation section
- 5 GitHub cross-links to source artifacts
- 3 academic citations

**Gaps:**

The following content from the source article (`jerry-docs-negative-prompting.md`) is absent from the deliverable:

1. **"Practical Application" section** (source lines 196-251): The entire section covering `/prompt-engineering` skill usage guide (pe-builder, pe-constraint-gen, pe-scorer with usage examples), the NPT-009 vs NPT-013 decision table (5-row table by context type), and the step-by-step upgrade workflow (NPT-014 to NPT-009 to NPT-013 with the three binary-testability criteria). This is a substantial content gap on a practitioner-facing page.

2. **"The Two Patterns That Matter Most" subsection** (source lines 162-192): The dedicated NPT-009 explanation with worked YAML example, NPT-013 example with worked behavioral constraint, and the explicit decision rule distinguishing the two patterns.

3. **"What the Research Did Not Change" subsection** (source lines 287-293): Convention-alignment rationale, reversibility commitment, and open research question statement.

4. **Explicit 60% claim null finding treatment**: The source devotes an explicit subsection to "The 60% Claim: Untested, Not Disproven" with the methodological nuance that the claim is unestablished rather than disproven. The deliverable mentions "null finding" only in the phase quality gate table, without explanation.

5. **NPT-014 quantification**: Source provides the baseline statistics (61%, 22 of 36 instances in Jerry at research start) establishing scope. Deliverable omits.

**Improvement Path:** Add the Practical Application section from the source article. Add NPT-009 worked example alongside NPT-013. Add explicit 60% null finding explanation. This is the largest single gap.

---

### Internal Consistency (0.88/1.00)

**Evidence:**

All statistics verified against the source article with exact agreement:
- Violation rates: 0/90 (C3), 2/90 (C2), 7/90 (C1) -- match
- McNemar p = 0.016 -- match
- Bonferroni adjusted alpha = 0.0167 -- match
- Effect size pi_d = 0.078, 95% CI [0.023, 0.133] -- match
- Haiku improvement: 10 percentage points -- match
- H-22 violation concentration: 67%, 6/9 violations -- match (source line 115 says "6 of 9", deliverable says "6/9")
- Phase gate scores: all six phases match (0.950/0.933/0.935 Phase 1, etc.)
- 270 trials, 3 models, 3 conditions: match
- 75 sources in Phase 1: match
- 130 upgrade recommendations in Phase 4: match
- 23 C4 quality gates: match

**Gaps:**

Two minor simplifications (not contradictions) found in the ADR status column:
- ADR-001: Source says "Unconditional -- evidence is T1+T3"; deliverable says "Accepted -- evidence is T1+T3". Not a contradiction, but loses the "unconditional" characterization that distinguishes it from the conditional ADR-002.
- ADR-002: Source says "Phase 5A implemented; Phase 5B completed via PG-003"; deliverable says "Implemented". This loses the PG-003 contingency pathway information.
- ADR-003: Source says "Component A implemented; Component B completed via PG-003"; deliverable says "Implemented". Same loss.

One terminology drift: NPT-007 described as "untested baseline" in deliverable taxonomy table (line 64) versus "untreated baseline" in source (line 160). Not a contradiction; the terms are nearly synonymous in experimental design context.

**Improvement Path:** Expand ADR status column to preserve the conditional/unconditional distinction. The simplifications are minor but reduce precision in a C4 deliverable.

---

### Methodological Rigor (0.85/1.00)

**Evidence:**

Strong methodological documentation present:
- McNemar exact test correctly named and applied (matched-pair design)
- Bonferroni correction properly stated with adjusted alpha (0.0167, correct for 3 pairwise comparisons)
- Effect size with confidence interval disclosed (pi_d = 0.078, 95% CI [0.023, 0.133])
- Pre-registered minimum effect size threshold stated (0.10) -- the honest treatment of the CONDITIONAL GO verdict
- Evidence tier vocabulary (T1, T3, T4) applied consistently in taxonomy
- Pressure scenarios defined (3 conditions: normal, mild, strong pressure)
- Independent blind scoring with inter-rater agreement stated
- Phase gate scores disclosed with the relevant rubric (S-014, 6-dimension weighted composite)
- Study design (10 constraints, 3 models, 3 framing conditions, 3 pressure conditions per constraint) disclosed

**Gaps:**

1. **No limitations section**: The source explicitly states "the causal comparison of structured negative versus structurally equivalent positive framing remains the open research question for future work" (source line 293). This is an important methodological limitation (the study cannot distinguish NPT-013's benefit from effect of consequence+alternative as separate factors). Absent from deliverable.

2. **60% null finding treatment**: The source devotes an explicit subsection with the methodological nuance "It is not disproven; it is simply unestablished." The deliverable mentions it only in passing in the phase table ("Research question bifurcation; null finding on 60% hallucination claim"). For methodological rigor on a C4 public page, this distinction matters.

3. **Constraint selection rationale**: The source notes the constraints tested "span behavioral timing (H-22), tool restrictions (H-05), architectural boundaries (H-07), and constitutional principles (P-003, P-020, P-022)" -- the deliverable reproduces this but does not explain why this set represents generalizability of the finding.

**Improvement Path:** Add a brief limitations section or subsection noting the open causal question. Expand the 60% null finding discussion to match the source's nuance. Both can be done in fewer than 100 words each.

---

### Evidence Quality (0.76/1.00)

**Evidence:**

Present:
- 3 named academic citations (Liu et al. AAAI 2026, Wen et al. EMNLP 2024, Barreto & Jana EMNLP 2025) with venue, year, and relevance
- 5 GitHub octicons links to source artifacts: A/B test go-no-go, all 4 ADRs, Final Synthesis, NPT Pattern Catalog, WORKTRACKER
- MkDocs Material octicons link format correctly applied
- "Related Reading" link to full blog post

**Gaps:**

1. **3 citations for a 75-source study**: The research drew on 75 unique sources across academic, industry, and vendor documentation. A public research page citing only 3 of those sources provides thin evidential coverage. The single-vs-multi-agent format reference (the comparison doc) cites 20 sources with venue-level attribution and cluster membership. The deliverable falls well short of that standard.

2. **No DOI or URL for academic citations**: Citations are author/year/venue only. A reader who wants to verify "Liu et al., AAAI 2026" has no direct link. The source article also does not provide DOIs, so this is a shared limitation, but on a public page it is a meaningful gap.

3. **All GitHub links point to feature branch**: Every octicons link uses `feat/proj-014-negative-prompting-research` branch. When the branch is merged or deleted, all links will break. A stable public documentation page should link to `main` or to specific commit hashes. This is a structural concern for link longevity.

4. **"Related Reading" link unverified**: The link `../blog/posts/structured-negation-constraint-enforcement.md` points to a blog post that may not yet exist. The source article does not list this path. If the blog post does not exist, this is a broken link on a public page.

5. **NPT pattern reference and SKILL.md unlinked**: The source article lists `skills/prompt-engineering/rules/npt-pattern-reference.md` and `skills/prompt-engineering/SKILL.md` as primary references. Neither is linked from the deliverable. These are the operational artifacts readers would most want to access.

**Improvement Path:** Add at minimum 5-8 additional academic citations from the Phase 1 literature (the source identifies Wen et al. EMNLP 2024 as +7.3-8% improvement, which is a second claim not fully cited). Convert branch links to main or commit-pinned URLs. Add link to NPT pattern reference file. Verify the blog post link.

---

### Actionability (0.72/1.00)

**Evidence:**

Present:
- NPT-013 format template with example (the handoff object example)
- Taxonomy with Recommendation column -- reader can identify which pattern to use for which context
- NPT-014 labeled as anti-pattern with "Upgrade all instances"
- CONDITIONAL GO verdict explanation -- reader understands adoption framing

**Gaps:**

The entire "Practical Application" section from the source article is absent. This is the largest actionability gap:

1. **No NPT-009 vs NPT-013 decision table**: The source provides a 5-row table (by context: forbidden_actions YAML, SKILL.md routing disambiguation, rule file behavioral constraints, agent markdown body guardrails, constitutional compliance tables) with recommended pattern and rationale. Without this, a reader who understands both patterns cannot determine which to apply in their specific context without reading the source article.

2. **No NPT-009 example**: The deliverable shows NPT-013 format and example. NPT-009 format ("P-003 VIOLATION: NEVER {action} -- Consequence: {impact}") is not demonstrated. A reader trying to write agent governance YAML `forbidden_actions` entries has no template.

3. **No upgrade workflow**: The source provides a 3-step workflow for upgrading an NPT-014 constraint to NPT-009 to NPT-013, with a concrete example and three binary-testability criteria. Absent from deliverable. This is the most directly useful operational content on the page.

4. **No /prompt-engineering skill usage guide**: The source explains `pe-constraint-gen` usage ("Generate NPT-013 constraints for a research agent that must not hallucinate sources"), `pe-builder` purpose, and `pe-scorer` role. Absent from deliverable. FEAT-005 is mentioned in the features table but without guidance on how to use it.

**Improvement Path:** Add the Practical Application section from the source article. This is not summarization -- it is restoration of missing content that the source considers essential for the page's stated goal. Minimum: NPT-009 example, NPT-009 vs NPT-013 decision table, upgrade workflow.

---

### Traceability (0.83/1.00)

**Evidence:**

Present:
- 5 GitHub octicons links covering the primary research artifacts:
  - A/B test go-no-go determination (TASK-025)
  - ADR-001, ADR-002, ADR-003, ADR-004 (all four)
  - Final Synthesis (Phase 6)
  - NPT Pattern Catalog (Phase 3)
  - WORKTRACKER.md
- Phase quality gate scores disclosed with attribution to S-014 rubric
- Academic citations with venue-level attribution

**Gaps:**

1. **NPT pattern reference file unlinked**: `skills/prompt-engineering/rules/npt-pattern-reference.md` is the operational artifact implementing the taxonomy. It is listed in the source's References section but absent from the deliverable's links.

2. **Prompt Engineering SKILL.md unlinked**: The primary deliverable of FEAT-005 is `skills/prompt-engineering/SKILL.md`. Not linked.

3. **Phase 1-5 artifacts not linked**: Only Phase 6 (Final Synthesis) and Phase 3 (NPT Pattern Catalog) have links. No links to Phase 1 literature survey, Phase 2 claim validation, Phase 4 application analysis, or Phase 5 individual ADRs (the ADR table itself links to the ADRs, but the barrier synthesis artifacts are not linked).

4. **Feature branch link stability**: All GitHub links use branch `feat/proj-014-negative-prompting-research`. When the branch is merged to main and eventually deleted, links break. A public documentation page requires stable URLs.

5. **Academic citation verification**: Citations are author/year/venue without DOI. Full traceability would include a means to locate the source directly.

**Improvement Path:** Add links to NPT pattern reference and SKILL.md. Convert feature branch links to main branch links after merge. Add DOIs or arXiv links for the three cited papers.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Actionability | 0.72 | 0.88 | Add the complete "Practical Application" section from the source article: NPT-009 example with YAML, NPT-009 vs NPT-013 decision table (5 rows by context type), and upgrade workflow with 3 binary-testability criteria |
| 2 | Completeness | 0.77 | 0.90 | Add "The Two Patterns That Matter Most" subsection (NPT-009 vs NPT-013 with worked examples and decision rule), explicit 60% null finding treatment, and "What the Research Did Not Change" section |
| 3 | Evidence Quality | 0.76 | 0.88 | Add 5+ additional academic citations from the Phase 1 literature; add link to NPT pattern reference file; verify and add blog post link or remove it; convert GitHub links from feature branch to main after merge |
| 4 | Methodological Rigor | 0.85 | 0.92 | Add explicit limitations subsection noting the open causal question (structured negative vs structurally equivalent positive); expand 60% null finding treatment to match source's "unestablished, not disproven" nuance |
| 5 | Internal Consistency | 0.88 | 0.92 | Restore conditional/unconditional distinction in ADR-001 status; restore PG-003 contingency notation in ADR-002 and ADR-003 status fields |
| 6 | Traceability | 0.83 | 0.90 | Add links to SKILL.md and NPT pattern reference; convert all feature branch links to stable main/commit URLs post-merge |

---

## Leniency Bias Check

- [x] Each dimension scored independently before composite computed
- [x] Evidence documented for each score with specific line-number references
- [x] Uncertain scores resolved downward (Completeness held at 0.77 not 0.82 due to Practical Application gap; Evidence Quality held at 0.76 not 0.80 due to branch link instability and thin citation count)
- [x] First-draft calibration considered (this is a first deliverable against a source article with substantially more content)
- [x] No dimension scored above 0.95 (highest is Internal Consistency at 0.88, justified by complete statistical accuracy)
- [x] C4 threshold (0.95) applied per user specification -- composite of 0.805 is well below threshold

---

## Session Context (Handoff Schema)

```yaml
verdict: REVISE
composite_score: 0.805
threshold: 0.95
weakest_dimension: Actionability
weakest_score: 0.72
critical_findings_count: 0
iteration: 1
improvement_recommendations:
  - "Add complete Practical Application section: NPT-009 example, NPT-009 vs NPT-013 decision table, upgrade workflow"
  - "Add The Two Patterns That Matter Most subsection and 60% null finding treatment"
  - "Add 5+ academic citations, link NPT pattern reference file, fix GitHub branch links"
  - "Add limitations section on open causal question"
  - "Restore conditional/unconditional ADR status distinctions"
  - "Link SKILL.md and convert feature branch links to stable URLs post-merge"
```
