# Quality Score Report: Anthropic Agent Skills Best Practices Research

## L0 Executive Summary

**Score:** 0.926/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Traceability (0.89)

**One-line assessment:** A strong research deliverable that resolved three of four iter-3 gaps (within-search selection rationale, Step 6 success criterion, evidence date standardization) but fell short on traceability because UC-004, UC-017, and UC-025 (the domain scoring criteria) are absent from the Requirements Coverage Matrix and the UC-017 compliance gap was only partially resolved; three surgical additions will close the remaining 0.024 gap.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-021-use-case/orchestration/use-case-skills-20260308-001/research/anthropic-skill-best-practices.md`
- **Deliverable Type:** Research
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Quality Threshold:** 0.95 (user override C-008; standard H-13 threshold is 0.92)
- **Iteration:** 4 of max 6
- **Prior Scores:** iter-1 = 0.837, iter-2 = 0.909, iter-3 = 0.9235
- **Scored:** 2026-03-08

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.926 |
| **Threshold** | 0.95 (C-008 user override) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No (no adv-executor reports provided) |
| **Score Delta from Prior Iteration** | +0.0025 (iter-3: 0.9235 -> iter-4: 0.926) |
| **Gap to Threshold** | -0.024 |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.93 | 0.186 | L0/L1/L2 complete; 4 matrix UCs covered "Full"; Step 6 success criterion added; UC-004/UC-017/UC-025 absent from coverage matrix |
| Internal Consistency | 0.20 | 0.94 | 0.188 | L0 findings trace to L1 with explicit cross-refs; L2 Derives From column present; no contradictions; confidence scale defined in iter-4 |
| Methodological Rigor | 0.20 | 0.92 | 0.184 | 13-step audit trail with query strings; within-search selection criteria added (iter-3 gap resolved); per-result discard rationale not documented |
| Evidence Quality | 0.15 | 0.93 | 0.1395 | 8 primary official-domain sources; full URLs with access dates present; 7 key findings each 3+ sources; one finding uses framework doc as 3rd source |
| Actionability | 0.15 | 0.93 | 0.1395 | 7-step sequence with specific actions; Step 6 success criterion added (iter-3 gap resolved); Step 6 uses 0.85 threshold without explanation of relationship to H-13 0.92 gate |
| Traceability | 0.10 | 0.89 | 0.089 | UC-002/026/027/028 covered with Status column; UC-004/UC-017/UC-025 (domain scoring criteria) absent from matrix; iter-3 UC-017 gap partially resolved only |
| **TOTAL** | **1.00** | | **0.926** | |

---

## Detailed Dimension Analysis

### Completeness (0.93/1.00)

**Evidence:**

The document delivers all six major research areas: skill architecture (Section 1), tool selection (Section 2), prompt engineering (Section 3), multi-agent coordination (Section 4), quality assurance (Section 5), and context management (Section 6). The L0/L1/L2 structure is fully populated. The Implementation Sequence covers 7 ordered steps with rationale and derivation columns. Per-skill recommendation tables are detailed and specific for /use-case, /test-spec, and /contract-design. The Requirements Coverage Matrix marks all four listed requirements (UC-002, UC-026, UC-027, UC-028) as "Full" with specific section references and a Status column added in iter-4.

The iter-3 gap for Step 6 is resolved in iter-4: "Success criterion: all three skills produce coherent artifacts from a single representative use case as input, with no handoff failures and output quality >= 0.85 on S-014 dimensions" now appears in Step 6.

Section 5.5 was expanded in iter-4 to address background subagent failure handling and the `background: true` vs. synchronous invocation decision, resolving the prior UC-026 completeness gap.

**Gaps:**

The domain scoring criteria for this evaluation specify UC-004 (Anthropic skill authoring best practices documented), UC-017 (3+ independent sources per key finding), and UC-025 (evidence-based recommendations with source traceability). None of these three IDs appear in the Requirements Coverage Matrix. Their substantive content is addressed in the document — UC-004 through Sections 1-6 broadly; UC-017 through the Cross-Reference Validation table in Methodology; UC-025 through inline source citations and L2 recommendation tables. However, without explicit matrix entries, completeness for those criteria cannot be verified from the matrix alone.

**Improvement Path:**

Add UC-004, UC-017, and UC-025 as rows in the Requirements Coverage Matrix with Status="Full" and section references. This is three table rows with no content changes — all underlying research is already present in the document. Once added, the matrix provides full traceability for all domain scoring criteria.

---

### Internal Consistency (0.94/1.00)

**Evidence:**

L0 executive summary findings include explicit cross-references: "[Source 1, Source 2; see Section 1.2]", "[Source 3; see Section 1.1]", "[Source 4, Source 5; see Section 4.1]", "[Source 3, Source 6; see Section 5.1]", "[Source 3, Source 5; see Section 5.5]". Every L0 finding traces to a named L1 section. L2 recommendation tables include a "Derives From" column pointing to specific L1 sections and source numbers, forming a closed derivation chain.

The iter-3 gap about the confidence scale is resolved: the frontmatter now reads "(0.92) -- 8 unique primary sources cross-referenced, all from authoritative publishers (0.0-1.0 handoff confidence scale per Jerry handoff-v2.schema.json)."

The Section 3.2 header gap from iter-3 ("Agent Definition Format (Claude Code and Jerry H-34)") is addressed in the opening paragraph of that section, which clarifies that "Jerry extends Anthropic's base single-file agent definition format... with a mandatory dual-file architecture (H-34). H-34 is a Jerry-specific governance requirement, not part of Anthropic's Claude Code specification."

Spot-checks on the cross-reference validation table: progressive disclosure cites Sources 1, 2, 7 (confirmed in sections 1.2, 6.2, 6.4); creator-critic patterns cites Sources 3, 4, 6 (confirmed in sections 5.1, 5.2); tool design quality cites Sources 2, 3, 4 (confirmed in sections 2.2, 2.3). All spot-checks pass.

The "start with 1 agent" principle appears consistently in the /use-case recommendation, /contract-design recommendation, Step 7 of the implementation sequence, and the cross-cutting agent count row without contradiction.

**Gaps:**

No material contradictions were found. The Revision 4 header in the frontmatter states "Revision: 4" and the footer states "Research Version: 4.0.0" — consistent. The source count "8 unique primary sources" is stated in the frontmatter, the References section header, and corresponds to exactly 8 numbered references.

**Improvement Path:**

No changes required for this dimension. The score of 0.94 reflects the strong alignment across the document. It is not 0.95+ because there is no visible cross-validation of the confidence score of 0.92 against an explicit calibration scale beyond the parenthetical reference — a minor gap that does not warrant further revision at this stage.

---

### Methodological Rigor (0.92/1.00)

**Evidence:**

The Methodology section documents 13 steps with query strings, result counts, and sources identified per step. Steps 10-13 are revision-phase steps specifically targeting error handling gaps, demonstrating iterative research depth. Source selection criteria provide a 3-tier classification (Primary/Secondary/Discarded) with named discarded sources and explicit rationale.

The iter-3 gap — within-search selection rationale absent — is resolved in iter-4. The Source Selection Criteria section now states: "Within each search result set, selection prioritized: official documentation domain names (anthropic.com, claude.com, code.claude.com, platform.claude.com, learn.microsoft.com), publication dates post-2024, and titles indicating technical depth over vendor marketing summaries." This is a clear, verifiable criterion set.

The Gaps and Limitations table documents 4 gaps with Impact, Mitigation, and Basis columns. Each Basis column cites specific search evidence (e.g., "Confirmed via WebFetch of Source 3 (Building Effective Agents): 'remarkably little explicit guidance on error handling...'" for the error handling gap). This is methodological evidence of due diligence.

All 8 source access dates are present (2026-03-08 for all). References include full URLs (resolved in iter-4). Publication dates follow a standardized format in iter-4: YYYY-MM for Sources 1-4, "current" for official documentation pages (Sources 5, 7, 8) where no specific publication date applies. This is appropriate and consistent.

**Gaps:**

The within-search selection criteria are stated at the general level but not applied per-result. Step 1 states "10 results; 3 primary sources identified" — it is clear that 3 of 10 were selected, but the document does not identify which 7 were examined and discarded, nor does the Source Validation table enumerate the discarded results beyond the two named examples (PubNub, SkyWork) and the generic statement "approximately 40 other search results."

For a C4 deliverable at a 0.95 threshold, the absence of per-result or per-search-batch discard documentation is a genuine methodological transparency gap. A reviewer cannot independently audit source selection decisions without knowing what was considered and rejected, even if they trust the general criteria.

**Improvement Path:**

Add a "Representative Discarded Sources" mini-table in the Methodology section listing 3-5 examples from the major searches (Steps 1-3) with source title, domain, and discard reason per the classification criteria. This demonstrates that the within-search selection criteria were applied to specific results, not just stated abstractly. Exhaustive per-URL documentation is not required — a representative sample suffices.

---

### Evidence Quality (0.93/1.00)

**Evidence:**

All 8 sources are from official Anthropic or Microsoft domains. A domain note in the References section clarifies: "claude.com/blog and anthropic.com/engineering are both official Anthropic properties. Sources 1, 2, 4 originate from these domains and carry equivalent credibility to anthropic.com/research (Source 3)." This was an iter-3 gap and is now resolved.

Every reference includes: full URL, domain/publisher, publication date (ISO-8601 format in iter-4), access date (2026-03-08), and a Key Insight summary. The iter-3 gap regarding WebFetch URL documentation is resolved — the References section now includes full URLs and the Methodology table Step 7 lists abbreviated forms with the note that full URLs are in References, which is an acceptable cross-reference given the length of some URLs.

Publication dates are standardized in iter-4: Sources 1-4 use YYYY-MM format; Sources 5, 7, 8 use "current" with access dates, appropriate for living documentation pages.

Direct quotations are used for key claims throughout. Seven key findings each cite 3+ independent sources per the Cross-Reference Validation table.

**Gaps:**

The "Guardrails and forbidden actions" key finding in the Cross-Reference Validation table cites "Source 5, Source 8, Jerry H-34" and notes "3 (2 external + 1 framework)." While transparent, a framework document (agent-development-standards.md) serving as the third source for a best-practices finding is weaker evidence than three independent external sources. The underlying claim it supports — "Jerry operationalizes this guidance through the `.governance.yaml` `capabilities.forbidden_actions` array" — is a characterization of Jerry's design choices, not an external best practice finding. The two external sources (Sources 5, 8) are sufficient for the external best-practice claim; the Jerry H-34 reference is more accurately described as "framework alignment" than "independent cross-validation."

Methodology Step 7 in the audit trail shows partial URL truncation ("claude.com/blog/equipping-agents-...") while the References section has full URLs. This is a presentational inconsistency but not a substantive gap.

**Improvement Path:**

In the Cross-Reference Validation table, rename the "Guardrails and forbidden actions" row to distinguish between the external best-practice finding (Sources 5, 8) and the Jerry framework alignment (H-34). Alternatively, identify an independent external source (e.g., NIST SSDF, OWASP ASVS) that corroborates the guardrails principle to replace Jerry H-34 as the third source. The transparent footnote "(2 external + 1 framework)" partially addresses this but does not resolve the underlying evidence quality question.

---

### Actionability (0.93/1.00)

**Evidence:**

The 7-step Implementation Sequence is actionable with imperative-verb Actions, Rationale, and Derives From columns. Per-skill recommendation tables provide specific tool tiers (T2 for /use-case, T1/T2 for /test-spec, T2/T3 for /contract-design), specific `maxTurns` values (25 for /test-spec), specific cognitive modes (divergent/convergent/systematic), and specific governance YAML field values.

The iter-3 gap — Step 6 success criterion absent — is resolved. Step 6 now reads: "Success criterion: all three skills produce coherent artifacts from a single representative use case as input, with no handoff failures and output quality >= 0.85 on S-014 dimensions." This is specific and testable.

The /contract-design recommendation includes three measurable criteria for when to adopt the orchestrator-worker topology: "3+ distinct workflow stages each requiring different tool sets," "2+ cognitive modes," or "single agent's `<methodology>` exceeds 1,500 tokens." Agent count expansion criteria in the cross-cutting table similarly provide three measurable triggers. The iter-3 recommendation to add "C3=7, C4=10" to the maker-checker note is implemented.

**Gaps:**

The Step 6 success criterion uses a 0.85 threshold. The project operates at C4 criticality with a user-override threshold of 0.95 (the threshold in this scoring call) and the standard H-13 threshold is 0.92. The document does not explain the relationship between the 0.85 pipeline-validation floor, the 0.92 H-13 production gate, and the 0.95 project-specific threshold. An implementer following Step 6 would achieve 0.85 quality and reasonably believe the pipeline is validated, without knowing that production artifacts must then reach 0.92 or higher. This creates a potential implementation gap.

**Improvement Path:**

Add one sentence after the Step 6 success criterion: "Note: 0.85 serves as the minimum smoke-test bar for pipeline correctness. Production artifact quality must meet H-13 (>= 0.92) or the project-specific threshold when submitting for quality gate passage." This takes five words of context and closes the ambiguity without restructuring the step.

---

### Traceability (0.89/1.00)

**Evidence:**

The Requirements Coverage Matrix covers UC-002, UC-026, UC-027, and UC-028 with a Status column (all "Full") and specific section references. The iter-4 revision added the Status column as noted in the frontmatter: "iter-4 adversary revisions: traceability matrix status."

Inline source citations are dense and consistent: every substantive claim in L1 and L2 carries a [Source N] reference or a Jerry framework rule ID citation. The L0 summary includes inline citations linking findings to both source numbers and sections. The L2 recommendation tables include a "Source" column and an "L1 Section" column, creating a forward traceability chain from recommendation back to research finding.

The constitutional compliance footer cites P-001 (all claims cited; 8 unique sources verified), P-002 (file persisted), P-004 (full provenance with access dates, methodology, and fetched URLs; requirements coverage matrix with status column), P-022 (gaps documented with basis statements). The reference to "requirements coverage matrix with status column" in the P-004 evidence directly reflects the iter-4 addition.

**Gaps:**

The domain scoring criteria for this evaluation specify UC-004, UC-017, and UC-025. None of these IDs appear in the Requirements Coverage Matrix. The iter-3 score identified "UC-017 ambiguity in compliance matrix" as the traceability gap. The iter-4 revision added the Status column to existing rows but did not add UC-017, UC-025, or UC-004 as new matrix entries.

The substantive content for these requirements is present in the document: UC-017 compliance is demonstrated by the Cross-Reference Validation table; UC-025 compliance is demonstrated by the inline citations and L2 "Source" columns; UC-004 compliance is demonstrated by the entire L1 technical analysis. However, a reviewer using the Requirements Coverage Matrix to assess compliance with the domain scoring criteria will find no entries for UC-004, UC-017, or UC-025, creating a traceability failure for those criteria specifically.

The Cross-Reference Validation table in the Methodology section is labeled "Cross-Reference Validation" without linking the label to "UC-017" by ID (the "(UC-017)" parenthetical from iter-3 was removed). This is appropriate cleanup but means there is now no reference to UC-017 anywhere in the document.

**Improvement Path:**

Add three rows to the Requirements Coverage Matrix:
- UC-004 | "Anthropic skill authoring best practices documented" | Full | "L1 Sections 1-6 (all major topic areas); L2 Implementation Sequence; L2 per-skill recommendations"
- UC-017 | "3+ independent sources per key finding" | Full | "Methodology: Cross-Reference Validation table (7 key findings, each 3+ unique sources documented)"
- UC-025 | "Evidence-based recommendations with source traceability" | Full | "L2 recommendation tables (Source column per row); References section (8 citations with URLs); L2 Recommendations 'L1 Section' column"

This is a three-row table addition requiring no content changes elsewhere. The underlying evidence already exists.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Traceability | 0.89 | 0.93 | Add UC-004, UC-017, UC-025 rows to Requirements Coverage Matrix with Status="Full" and section references. Three table rows; no content changes. Highest ROI: closes traceability gap and also resolves the Completeness gap for the same criteria. |
| 2 | Actionability | 0.93 | 0.95 | Add one sentence after the Step 6 success criterion explaining that 0.85 is the pipeline smoke-test floor and that production artifacts must meet H-13 (>= 0.92) or project threshold. |
| 3 | Methodological Rigor | 0.92 | 0.94 | Add a "Representative Discarded Sources" mini-table listing 3-5 specific discarded sources from Steps 1-3 with discard reason. Demonstrates that the within-search selection criteria were applied to actual results, not stated abstractly. |
| 4 | Evidence Quality | 0.93 | 0.95 | Reclassify the "Guardrails and forbidden actions" Cross-Reference Validation row to distinguish external best-practice sources (Sources 5, 8) from Jerry framework alignment (H-34), or replace H-34 with an independent external source. |
| 5 | Completeness | 0.93 | 0.95 | Resolved by Priority 1 (matrix row additions cover UC-004/UC-017/UC-025 which are the remaining completeness gaps). No separate action needed. |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing the weighted composite
- [x] Evidence documented for each score with specific section references to the deliverable
- [x] Uncertain scores resolved downward: Traceability held at 0.89 (not 0.91) because UC-017 was the stated iter-3 gap and the iter-4 resolution did not add UC-017 to the matrix; Methodological Rigor held at 0.92 (not 0.93) because the per-result discard documentation gap is real and unresolved
- [x] C4 user-override threshold (0.95) applied strictly — composite of 0.926 is below threshold, verdict is REVISE
- [x] No dimension scored above 0.95 — the highest score (Internal Consistency 0.94) reflects genuinely strong but non-perfect execution
- [x] Iter-4 calibration considered: delta of +0.0025 from iter-3 is consistent with partial gap resolution (3 of 4 iter-3 gaps resolved; 1 partially resolved); not inflated for iteration count or effort
- [x] Weighted composite verified: (0.93×0.20) + (0.94×0.20) + (0.92×0.20) + (0.93×0.15) + (0.93×0.15) + (0.89×0.10) = 0.186 + 0.188 + 0.184 + 0.1395 + 0.1395 + 0.089 = 0.926
- [x] Score inflation check: iter-3 Traceability was 0.90; iter-4 dropped to 0.89 because the UC-017 matrix entry gap from iter-3 was not fully resolved (Status column added but UC-017 not added as a row) — anti-leniency principle applied

**Leniency check narrative:** The deliverable is genuinely high-quality research. Three of four iter-3 gaps were resolved, representing real improvement. However, the traceability score drops from 0.90 to 0.89 because the iter-3 report specifically identified "UC-017 ambiguity in the Requirements Coverage Matrix" as a gap, and the iter-4 deliverable added a Status column to existing rows without adding UC-017 as a new row. Applying the anti-leniency rule (uncertain scores resolved downward), Traceability is scored at 0.89. The composite of 0.926 is honest: this is a strong deliverable with a clear, bounded, three-addition path to the 0.95 threshold.

---

## Progress Trajectory

| Iteration | Score | Delta | Status |
|-----------|-------|-------|--------|
| iter-1 | 0.837 | -- | Baseline |
| iter-2 | 0.909 | +0.072 | Large gains: measurable criteria, matrix, source fix, H-34 coverage |
| iter-3 | 0.9235 | +0.0145 | Targeted gains; convergence developing |
| iter-4 | 0.926 | +0.0025 | Partial resolution; 1 of 4 gaps unresolved |
| Remaining gap | -0.024 | | Achievable in 1 targeted iteration |

The plateau detection criterion (delta < 0.01 for 3 consecutive iterations) has not triggered: deltas are 0.072, 0.0145, 0.0025 — the third delta is below 0.01, but the criterion requires 3 consecutive sub-0.01 deltas. One more iteration is warranted. If iter-5 also shows delta < 0.01, plateau detection should activate regardless of remaining gap.

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.926
threshold: 0.95
weakest_dimension: traceability
weakest_score: 0.89
critical_findings_count: 0
iteration: 4
prior_scores:
  iter_1: 0.837
  iter_2: 0.909
  iter_3: 0.9235
  iter_4: 0.926
delta_from_prior: +0.0025
gap_to_threshold: -0.024
improvement_recommendations:
  - "Add UC-004, UC-017, UC-025 rows to Requirements Coverage Matrix (Status=Full; 3 table rows; no content changes needed)"
  - "Add Step 6 threshold explanation: 0.85 is pipeline smoke-test floor; production gate is H-13 >= 0.92"
  - "Add representative discarded sources mini-table to Methodology (3-5 examples from Steps 1-3 with discard reason)"
  - "Reclassify or replace Jerry H-34 as 3rd source in Guardrails key finding in Cross-Reference Validation table"
plateau_risk: MEDIUM
  # iter-4 delta (+0.0025) is below 0.01 threshold
  # plateau criterion is 3 consecutive sub-0.01 deltas -- not yet triggered
  # if iter-5 also shows delta < 0.01, circuit breaker should activate
  # gap closure path is clear and surgical: estimated iter-5 composite if all 4 recommendations implemented: 0.950-0.955
```

---

*Score Report Version: 4.0 (iter-4 scoring)*
*Scoring Agent: adv-scorer*
*Strategy: S-014 (LLM-as-Judge)*
*SSOT: `.context/rules/quality-enforcement.md`*
*Produced: 2026-03-08*
