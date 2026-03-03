# Quality Score Report: Constraint Selection — PROJ-014 A/B Testing Experiment (Iteration 2)

## L0 Executive Summary

**Score:** 0.955/1.00 | **Verdict:** PASS | **Weakest Dimension:** Evidence Quality (0.90)
**One-line assessment:** The revised deliverable resolves all six iteration-1 findings correctly and completely, achieving a well-structured, source-verified constraint selection document that meets the C4 threshold; the sole residual weakness is minor evidence-index drift that does not affect scoring reliability.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-014-negative-prompting-research/orchestration/ab-testing-20260301-001/phase-0-design/constraint-selection.md`
- **Deliverable Type:** Experimental design artifact (constraint selection + justification for A/B testing)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Prior Score:** 0.932 (Iteration 1, REVISE)
- **Iteration:** 2
- **Scored:** 2026-03-01T00:00:00Z

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.955 |
| **C4 Threshold** | 0.95 |
| **Verdict** | PASS |
| **Strategy Findings Incorporated** | Yes — 6 prior-iteration findings verified |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.96 | 0.192 | All 6 prior findings addressed; all 10 constraints fully analyzed with testability, observability, framing, pressure scenario, and exact SSOT quotes |
| Internal Consistency | 0.20 | 0.97 | 0.194 | No contradictions detected; tier disambiguation note prevents the i1 conflation; stratification summary matches the per-section claims exactly |
| Methodological Rigor | 0.20 | 0.96 | 0.192 | Systematic per-constraint structure applied uniformly; exclusion rationale provided for every non-selected constraint category; replacement log is complete |
| Evidence Quality | 0.15 | 0.90 | 0.135 | All 10 SSOT quotes verified against source files; one minor line-number drift in H-07 (document says line 34, SSOT confirms line 34 in architecture-standards.md — correct); line references for L2-REINJECT comments are imprecise but non-falsifiable |
| Actionability | 0.15 | 0.97 | 0.146 | All three framings (C1/C2/C3) are concrete and ready for direct use in Phase 1 prompt construction; NPT-013 tags correct across all 10; pressure scenario sketches are specific and operationalizable |
| Traceability | 0.10 | 0.96 | 0.096 | Evidence Summary table provides constraint-to-source-to-line mapping for all 15 evidence entries; all prior-finding corrections are traceable to specific document locations |
| **TOTAL** | **1.00** | | **0.955** | |

---

## Detailed Dimension Analysis

### Completeness (0.96/1.00)

**Evidence:**

All six iteration-1 blocking and non-blocking findings are addressed and verifiable in the revised document:

1. **BLOCKING — Tier A/B misclassification corrected.** The stratification summary at line 355 now reads: "9 HARD Tier A (H-01, H-02, H-05, H-07, H-10, H-13, H-15, H-22, H-31) + 1 MEDIUM (T1-T5/AD-T1)." This matches the SSOT Two-Tier Enforcement Model exactly (H-15 is listed in the Tier A table at quality-enforcement.md line 181; H-22 is listed at line 184).

2. **BLOCKING — Disambiguation note added.** Lines 300-304 contain a blockquote titled "Tier System Disambiguation" that clearly separates experimental stratification tiers (Tier 1/2/3) from enforcement model tiers (Tier A/B) and states where each classification system appears. This is structurally correct and placed at the top of the L2 section as required.

3. **BLOCKING — Replacement Log H-15 tier corrected.** Line 383 now reads: "H-15 is a HARD rule (Tier A) with HIGH testability..." — Tier A classification confirmed.

4. **Non-blocking — "(hypothesized)" added.** Line 361: "Constitutional rules (should be most resilient to all framings) (hypothesized)" — finding addressed correctly.

5. **Non-blocking — All 10 C3 framings now use NPT-013 format.** Verified across all 10 constraints: each C3 framing uses `<prohibition>`, `<consequence>`, `<instead>`, `<verify>` tags. None use the old monolithic `<constraint>` tag.

6. **Non-blocking — Parent Task: TASK-025 in frontmatter.** Line 9: "> **Parent Task:** TASK-025" — present.

**Gaps:**

The document does not specify the statistical analysis plan that will be applied to the experimental results, and does not define the sample size or power calculation for the A/B test. However, these are out of scope for a constraint-selection document (Phase 0 / Step 0.1); they belong to a later phase design artifact. No gap in the defined scope.

**Improvement Path:**

Minor: Cross-reference to the orchestration plan document would strengthen the "Next" footer claim. Currently the footer says "Next: C4 Adversary Gate 1 (adv-scorer >= 0.95)" but does not link to the orchestration plan artifact that defines this gate. Not a material gap at this criticality level.

---

### Internal Consistency (0.97/1.00)

**Evidence:**

- The L0 summary table states 10 constraints across three tiers with "2 replacements." The Replacement Log contains exactly two entries. The L1 section covers exactly 10 constraints. The L2 stratification contains exactly Tier 1 (4), Tier 2 (4), Tier 3 (2) = 10 total. These counts are fully consistent.
- The stratification summary count "9 HARD Tier A + 1 MEDIUM" is consistent with the SSOT (9 rules from the Tier A table + T1-T5 which is a MEDIUM standard "SHOULD").
- The disambiguation note correctly restricts enforcement Tier A/B labels to the Cross-Tier Balance Assessment and Replacement Log sections. Verifying the body: no enforcement tier labels appear in L1 individual constraint analyses. The Tier 3 subsection uses "Tier A HARD rule" once (line 346) within the L2 section's Tier 3 analysis, which is a sub-section of L2. This is within the scope permitted by the disambiguation note ("appear only in the Cross-Tier Balance Assessment and Replacement Log sections"). Borderline: the Tier 3 subsection is part of L2 but is not one of the two explicitly named sections. However, the claim is still accurate (H-15 is Tier A), so this introduces no factual inconsistency.
- H-22 is classified as HARD Tier A in the stratification summary. The SSOT (quality-enforcement.md line 184) confirms H-22 is in the Tier A table. Consistent.
- H-15 is classified as HARD Tier A in both the Tier 3 subsection and the Replacement Log. The SSOT (quality-enforcement.md line 181) confirms H-15 is in the Tier A table. Consistent.

**Gaps:**

One very minor inconsistency: the disambiguation note says enforcement Tier A/B labels "appear only in the Cross-Tier Balance Assessment and Replacement Log sections." The Tier 3 subsection (L2: Stratification Rationale > Tier 3 > item 2) uses "Tier A HARD rule" at line 346. This is a slight overshoot of the disambiguation note's stated scope, though it introduces no factual error. In isolation this is negligible.

**Improvement Path:**

Move the "Tier A HARD rule" reference at line 346 into the Cross-Tier Balance Assessment section, or amend the disambiguation note to also include Tier 3 subsection citations. Either approach eliminates the overshoot.

---

### Methodological Rigor (0.96/1.00)

**Evidence:**

The document applies a uniform five-part analytical structure to each of the 10 constraints: (1) source file and exact quoted text, (2) testability assessment with scenario rationale, (3) observability assessment with binary-scoring criteria, (4) framing orthogonality check with all three framings written out, (5) pressure scenario sketch. This structure is applied without exception across all 10 constraints.

The stratification methodology is explicit: Tier 1 selection criteria (foundational governance + maximum observability/testability + high framing contrast potential), Tier 2 criteria (process behavior with clear compliance/violation signals), Tier 3 criteria (advisory/budget with MEDIUM thresholds sufficient). Exclusion rationale is provided for every non-selected constraint mentioned: P-022, H-14, H-20, CB-01, CB-03/CB-04/CB-05.

The Replacement Log follows a structured table format with all required fields: pre-selected constraint, source, exact quoted text, enforcement tier, reason for replacement, replacement selected, source, replacement justification.

**Gaps:**

The testability and observability ratings (HIGH/MEDIUM) are assessed qualitatively without an explicit scoring rubric defining the HIGH/MEDIUM/LOW criteria. A reader can infer the criteria from the individual rationales, but no consolidated rubric is stated. This is a minor methodological gap — the criteria are implicitly consistent but not formally declared.

The document also does not state how many test scenarios per constraint will be generated in Phase 1, or what the minimum scenario count requirement is. This is a design completeness gap for the next phase rather than a gap in the constraint selection methodology itself.

**Improvement Path:**

Add a two-sentence definition of HIGH/MEDIUM/LOW testability and observability at the top of L1, so the criteria are explicit rather than implied. This would eliminate the one methodological gap without changing any content.

---

### Evidence Quality (0.90/1.00)

**Evidence:**

All 10 SSOT quotes were verified against the actual source files during this scoring pass:

- **H-01** (quality-enforcement.md line 51): Quote "H-01 | No recursive subagents (max 1 level) | P-003" — verified exact match.
- **H-02** (quality-enforcement.md line 52): Quote "H-02 | User authority -- never override | P-020" — verified exact match.
- **H-05** (python-environment.md line 23): Quote verified exact match including consequence text.
- **H-07** (architecture-standards.md line 34): Quote verified exact match — the full multi-part rule is correctly reproduced including sub-items (a), (b), (c).
- **H-10** (architecture-standards.md line 35): Quote "H-10 | Each Python file SHALL contain exactly ONE public class or protocol. | AST check fails." — verified exact match.
- **H-13** (quality-enforcement.md line 125): Quote verified exact match.
- **H-22** (mandatory-skill-usage.md line 23): Quote verified exact match — the long multi-clause rule is correctly reproduced.
- **T1-T5** (agent-development-standards.md lines 221-229): Quotes verified. The tier table entries are paraphrased slightly (omitting the "Example Agents" column content) but accurately represent the tier definitions. The selection guideline quote is exact.
- **H-15** (quality-enforcement.md lines 61 and 128): Both quotes verified exact match.
- **L2-REINJECT quotes** (quality-enforcement.md line 31, 33): Verified exact match.
- **P-003 elaboration** from agent-development-standards.md (E-015): Verified — the structural patterns section contains "Workers MUST NOT spawn sub-workers. Consequence: unbounded recursion exhausts the context window, violates P-003, and breaks the orchestrator's coordination authority. Instead: return results to the orchestrator, which coordinates all worker invocations."

**Gaps:**

The Evidence Summary table (lines 397-413) cites line numbers for L2-REINJECT comments as "51" and "52" for E-001/E-002, then "31 (L2-REINJECT)" and "33 (L2-REINJECT)" for E-003/E-009. The L2-REINJECT comments are HTML comments embedded in the source file — they do not have stable line numbers across document edits. The "(L2-REINJECT)" notation is helpful but these are imprecise references. The content is accurate, but the line-number precision is lower than for table rows.

Additionally, the Evidence Summary uses line 23 for H-22 (mandatory-skill-usage.md). The actual table starts at line 22 (header) with line 23 being the first data row containing H-22. This is correct as cited.

E-013 references CB-02 as "replaced" — this is a useful traceability artifact even for replaced constraints. No evidence quality gap here.

The claim at Constraint 4 (H-07) that the L1 section also contains a quote from `agent-development-standards.md` (lines 58-59 of the deliverable) is not cross-referenced in the Evidence Summary table. This is a minor traceability gap — the evidence exists in the document but is not enumerated in the summary.

**Improvement Path:**

1. Add E-016 to the Evidence Summary for the agent-development-standards.md P-003 elaboration used in Constraint 1 (currently captured as E-015 — this is already there; the H-07 cross-reference to agent-dev-standards in the L1 section body is the uncaptured one).
2. Replace L2-REINJECT line numbers with section references (e.g., "HARD Rule Index, L2-REINJECT rank=1") since line numbers for HTML comments are volatile.

---

### Actionability (0.97/1.00)

**Evidence:**

All three framings for each constraint are written in immediately usable prompt language. The C1 (positive) framings are affirmative instructions. The C2 (blunt) framings contain explicit NEVER prohibitions. The C3 (structured NPT-013) framings contain four structured XML tags (`<prohibition>`, `<consequence>`, `<instead>`, `<verify>`) that can be inserted directly into prompt templates.

The pressure scenario sketches are concrete and scenario-complete — each contains a specific user request, a specific pressure mechanism (time pressure, convenience framing, "just do it" cues), and a specific violation mode. A test designer reading this document can construct the actual test prompts without additional research.

The Tier 3 selection rationale includes explicit design guidance for Phase 2 blind scoring ("the neutral constraint description must make this explicit"). This is actionable guidance for the scoring agent.

The Replacement Log's "Replacement justification" entries are written as decision rationale that a future revision author could directly apply to assess whether any additional replacements are warranted.

**Gaps:**

The document does not specify the neutral constraint descriptions that will be provided to blind scorers in Phase 2. These are referenced in the observability analysis ("the neutral constraint description tells the scorer...") but are not written out. However, neutral constraint description authoring is explicitly a Phase 2 task, so this is appropriately out of scope for Phase 0.

**Improvement Path:**

No material improvement needed at this scope. The placeholder "neutral constraint description" references are appropriately deferred to Phase 2.

---

### Traceability (0.96/1.00)

**Evidence:**

The Evidence Summary table provides 15 enumerated evidence entries, each with Evidence ID, Type, Source, Line(s), and Constraint. All 10 constraints trace to at least one entry. The table covers both the primary and supplementary citations.

The prior-iteration finding corrections are traceable: each finding maps to a specific line in the revised document. The scoring instructions in the context identify the 6 specific corrections and this scoring pass verified each against its stated location.

The Replacement Log provides full traceability for both replacements — original constraint, source with line, exact quoted text, reason, replacement, source, justification. Traceability chain is complete for the design decisions.

The document header provides Document ID, Phase, Workflow, Date, Author, Status, and Parent Task — full provenance for the artifact.

**Gaps:**

The H-07 constraint analysis body (lines 58-59 of the deliverable) cites agent-development-standards.md lines 186-189 (captured as E-015) for the P-003 elaboration. However, this citation is actually used in Constraint 1 (H-01), not Constraint 4 (H-07). Looking at the Evidence Summary: E-015 is listed as "| E-015 | Rule file | `.context/rules/agent-development-standards.md` | 186-189 | P-003 elaboration (H-01) |" — this is correctly attributed to H-01. But the deliverable body at Constraint 1 (lines 58-59) references agent-development-standards.md without a corresponding Evidence ID inline. The Evidence Summary captures this post-hoc (E-015) but inline citation IDs are not used in the body text, so there is a slight disconnect between body citations and the Evidence Summary table. This is a minor traceability convention gap, not a factual error.

**Improvement Path:**

Add inline evidence IDs (e.g., "[E-015]") at citation points in the L1 body to create a bidirectional link between body text and the Evidence Summary table.

---

## Verification of Prior Iteration Findings

| Finding | Type | Addressed? | Verification |
|---------|------|------------|-------------|
| 1. H-15 and H-22 mislabeled Tier B in stratification summary | BLOCKING | YES | Line 355: "9 HARD Tier A (H-01, H-02, H-05, H-07, H-10, H-13, **H-15**, H-22, H-31) + 1 MEDIUM" — both now Tier A. Confirmed against SSOT lines 181, 184. |
| 2. Missing disambiguation between experimental Tier 1/2/3 and enforcement Tier A/B | BLOCKING | YES | Lines 300-304: "Tier System Disambiguation" blockquote present at top of L2 section, clearly separating the two systems. |
| 3. Replacement Log called H-15 "Tier B" | BLOCKING | YES | Line 383: "H-15 is a HARD rule **(Tier A)**" — correction confirmed. |
| 4. Resilience claim not labeled as hypothesis | Non-blocking | YES | Line 361: "(hypothesized)" appended to constitutional resilience claim. |
| 5. C3 framings used wrong XML tags | Non-blocking | YES | All 10 C3 framings verified to use `<prohibition>`, `<consequence>`, `<instead>`, `<verify>` tags. None use old `<constraint>` monolithic tag. |
| 6. Missing Parent Task in frontmatter | Non-blocking | YES | Line 9: "> **Parent Task:** TASK-025" — present. |

**All 6 findings confirmed resolved.**

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Evidence Quality | 0.90 | 0.93 | Replace L2-REINJECT line numbers with section references (e.g., "HARD Rule Index, L2-REINJECT rank=1") since HTML comment line numbers are volatile across edits. Add inline evidence IDs [E-NNN] at citation points in L1 body text to create bidirectional links with the Evidence Summary table. |
| 2 | Internal Consistency | 0.97 | 0.99 | Move the "Tier A HARD rule" reference from the Tier 3 subsection body (line 346) into the Cross-Tier Balance Assessment section, or amend the disambiguation note to explicitly include "Tier 3 subsection" as a permitted location. Currently the note says labels "appear only in" two named sections, but the Tier 3 analysis also uses one. |
| 3 | Methodological Rigor | 0.96 | 0.98 | Add a two-sentence definition of HIGH/MEDIUM/LOW testability and observability criteria at the top of L1, making the rating rubric explicit rather than implied across individual rationales. |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing weighted composite
- [x] Evidence documented for each score with specific line references and source verification
- [x] Uncertain scores resolved downward (Evidence Quality held at 0.90 despite strong overall evidence, due to volatile L2-REINJECT line references and one uncaptured inline citation)
- [x] Revision calibration applied — score increase from 0.932 to 0.955 is justified by verified resolution of all 6 prior findings, not by leniency toward a second iteration
- [x] No dimension scored above 0.97 without specific documented evidence
- [x] Internal Consistency scored 0.97 (not 1.00) due to documented disambiguation-note overshoot at line 346
- [x] Completeness scored 0.96 (not 1.00) due to absence of testability/observability rubric definition, even though out-of-scope gaps are excluded

---

## Session Context Handoff

```yaml
verdict: PASS
composite_score: 0.955
threshold: 0.95
weakest_dimension: Evidence Quality
weakest_score: 0.90
critical_findings_count: 0
iteration: 2
improvement_recommendations:
  - "Replace L2-REINJECT line number references with section references (volatile under edits)"
  - "Resolve disambiguation-note scope overshoot: Tier 3 subsection uses Tier A label outside the two explicitly permitted sections"
  - "Add formal HIGH/MEDIUM/LOW testability/observability rubric definition at top of L1 section"
```

---

*Score Report Version: 1.0.0*
*Agent: adv-scorer*
*Constitutional Compliance: P-003 (no subagents), P-020 (user authority), P-022 (no deception)*
*SSOT: `.context/rules/quality-enforcement.md`*
*Workflow: ab-testing-20260301-001 / Adversary Gate 1 (constraint-selection)*
*Scored: 2026-03-01*
