# Quality Score Report: Three-Style Rewrites — PROJ-014 A/B Testing Experiment

## L0 Executive Summary

**Score:** 0.937/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Traceability (0.88)
**One-line assessment:** The artifact has resolved all prior confirmed defects and is internally rigorous, but misses the 0.95 PASS threshold primarily because the iteration 6 gate report is absent from the document header, and H-13 C2 contains a borderline conditional scope marker; addressing the header gap and confirming or resolving the H-13 C2 observation will bring the artifact within striking distance of PASS.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-014-negative-prompting-research/orchestration/ab-testing-20260301-001/phase-0-design/three-style-rewrites.md`
- **Deliverable Type:** Design (Phase 0 experimental material — A/B testing condition stimuli)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scoring Threshold:** 0.95 (user-specified C4 gate, iteration 7)
- **Prior Score:** 0.948 (iteration 6)
- **Iteration:** 7 (user-approved exception; configured max was 5)
- **Scored:** 2026-03-01T00:00:00Z

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.937 |
| **Threshold** | 0.95 (user-specified) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No — standalone scoring |
| **D-012 Resolution Status** | CONFIRMED RESOLVED — "without asking" removed from H-31 C1; clause fully establishes positive scope |
| **New Defects Found** | 2 (D-013, D-014) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.95 | 0.1900 | All 40 entries present; all sections and checklist complete; no missing items detectable |
| Internal Consistency | 0.20 | 0.93 | 0.1860 | All C1/C2/C3 pass structural checks; H-13 C2 borderline conditional marker warrants D-013 |
| Methodological Rigor | 0.20 | 0.93 | 0.1860 | Strong three-category sweep and sub-requirement method; no explicit C3 `<instead>` over-specification check |
| Evidence Quality | 0.15 | 0.95 | 0.1425 | All constraints traced to named source files with sections; iteration audit trail complete |
| Actionability | 0.15 | 0.96 | 0.1440 | All 40 entries immediately usable; verify tags provide scorable criteria; format reference clear |
| Traceability | 0.10 | 0.88 | 0.0880 | Per-constraint source traceability strong; iteration 6 gate report missing from document header (D-014) |
| **TOTAL** | **1.00** | | **0.937** | |

---

## Detailed Dimension Analysis

### Completeness (0.95/1.00)

**Evidence:**
All 30 rewrites are present (10 constraints × 3 conditions), verified by direct inspection of each constraint section. All 10 neutral descriptions are present in both the inline positions and the consolidated Neutral Descriptions table. Required document sections are all present: Summary, Condition Format Reference, Constraint Rewrites (10 subsections), Neutral Descriptions, Validation Checklist (with all 7 sub-checks), and S-010 Self-Review Notes (4 iterations documented). The navigation table includes anchor links for all major sections per H-23.

The validation checklist covers all required quality dimensions:
- Count verification (30 rewrites + 10 neutrals)
- C1 negation sweep (all three categories)
- C2 format check
- C3 four-tag check
- Neutral description quality check
- Condition label absence check
- Semantic equivalence check
- Source verification check

**Gaps:**
No functional completeness gap is found. The document is fully populated. The 0.95 rather than 0.97+ reflects the absence of a Revision History summary table that would make the 7-iteration change log navigable without reading all S-010 notes sequentially. This is a minor structural convenience gap, not a content gap.

**Improvement Path:**
Adding a compact revision history table (Version | Change | Defect Fixed) at the top of the S-010 section would raise this to 0.97. Not required for PASS.

---

### Internal Consistency (0.93/1.00)

**Evidence:**
A fresh word-by-word sweep of all 10 C1 entries was performed independently of the checklist, testing against the full Category 1/2/3 vocabulary. All 10 C1 entries pass. Specific confirmations:

- H-01 C1: "Omit the Task tool" — positive imperative. Clean.
- H-02 C1: "takes precedence over" — comparative, not negation. Clean.
- H-07 C1: "import only from" — positive scoping. Clean.
- H-13 C1: "falls below the threshold" — conditional descriptor within a positive instruction. Clean.
- H-31 C1: D-012 confirmed resolved. "When requirements are clear or the answer is in the codebase, proceed directly" — conditional positive, no negation. Clean.
- H-22 C1: "before the work begins" — plain temporal. Clean.
- H-15 C1: "only...after the self-review is complete" — sequencing qualifier. Clean.

All 10 C2 entries confirmed as pure "NEVER X" structure with no embedded alternatives or conditional consequence clauses.

All 10 C3 entries confirmed with all four required tags present and in correct order.

Cross-condition semantic scope: All 10 constraints verified as co-extensive across C1/C2/C3/neutral. H-01 (3 sub-requirements), H-07 (3 sub-requirements), H-15 (2 sub-requirements), H-31 (4 sub-requirements) — all confirmed consistent.

**Gaps (D-013):**
H-13 C2 reads: "NEVER deliver a C2+ deliverable with a quality score below 0.92. NEVER skip the revision cycle **when a score falls below the threshold**."

The second sentence contains "when a score falls below the threshold" as a scope qualifier attached to the prohibition. This is a borderline case: "when Y" defines the condition under which the prohibited action (skipping the revision cycle) applies. Compare to D-003 pattern: "NEVER X **without Y**" (which was corrected as encoding an implicit alternative). The "when Y" construction is not encoding an alternative — it is scoping the applicability of the prohibition. However, it is structurally different from all other C2 entries, which use either bare "NEVER X" (most common) or "NEVER X than Y" (comparative, H-07 C2), and creates a marginal framing difference from the C2 purity standard.

Per the scoring instruction: "When uncertain between adjacent scores, choose the lower one." The existence of this structural anomaly in C2, even if defensible, introduces a small but real inconsistency signal. This is documented as D-013 (Minor — H-13 C2 conditional scope qualifier).

**Improvement Path:**
Rewrite the H-13 C2 second sentence as: "NEVER skip the revision cycle for a below-threshold score." This converts the conditional scope qualifier into a modifier of the prohibited object, matching the structural purity of all other C2 entries.

---

### Methodological Rigor (0.93/1.00)

**Evidence:**
The scoring methodology is explicitly documented and consistently applied across all 7 iterations. The three-category negation taxonomy (Category 1: direct prohibition language; Category 2: embedded negative constructions; Category 3: temporal/modal/adverbial negation) is comprehensive and systematically applied. The sub-requirement enumeration method (derive from C2, verify in C1/C3/neutral) is sound and addresses the core cross-condition scope parity requirement. Source verification traces each constraint to named files and sections. The iterative correction history shows disciplined defect detection and targeted fixes without scope creep.

**Gaps:**
One methodological gap is present: there is no explicit check for **C3 `<instead>` over-specification relative to C1**. The `<instead>` tag provides a positive alternative instruction. If any `<instead>` tag introduces specificity that is narrower or broader than the corresponding C1 entry, a quiet asymmetry exists that would affect experimental validity. A spot-check of H-07 shows the `<instead>` tag ("inject the concrete adapter at src/bootstrap.py using dependency injection") is slightly more prescriptive than the H-07 C1 entry. While not a clear defect, the absence of an explicit `<instead>`-vs-C1 scope check means this dimension of cross-condition equivalence is unverified by the document's own methodology.

This is a methodology gap, not a confirmed defect in the content. It represents the limit of the current verification framework rather than an error in the rewrites.

**Improvement Path:**
Add a `<instead>` vs. C1 scope check to the Semantic Equivalence Check section, verifying that each `<instead>` tag and its corresponding C1 entry cover the same behavioral instruction set. This would raise Methodological Rigor to 0.96.

---

### Evidence Quality (0.95/1.00)

**Evidence:**
All 10 constraints are traced to specific source files with section and line references:

- H-01: `.context/rules/quality-enforcement.md` (HARD Rule Index, L2-REINJECT rank=1) + `agent-development-standards.md` (Structural Patterns)
- H-02: `.context/rules/quality-enforcement.md` (HARD Rule Index) + `CLAUDE.md` (Critical Constraints table)
- H-05: `.context/rules/python-environment.md` (HARD Rules table and Command Reference)
- H-07: `.context/rules/architecture-standards.md` (HARD Rules table, line 34) + L2-REINJECT rank=4
- H-10: `.context/rules/architecture-standards.md` (HARD Rules table, line 35)
- H-13: `.context/rules/quality-enforcement.md` (Quality Gate Rule Definitions, line 125) + L2-REINJECT rank=2
- H-31: `.context/rules/quality-enforcement.md` (Quality Gate Rule Definitions, line 132) + L2-REINJECT rank=2
- H-22: `.context/rules/mandatory-skill-usage.md` (HARD Rules table, line 23) — with documented scope narrowing rationale
- T1-T5: `.context/rules/agent-development-standards.md` (Tool Security Tiers section, lines 221-237)
- H-15: `.context/rules/quality-enforcement.md` (HARD Rule Index line 61 + Quality Gate Rule Definitions line 128)

The S-010 Self-Review Notes explicitly state that C3 consequence fields were derived from documented consequences in source files rather than invented. The companion constraint-selection artifact (PROJ-014-AB-PHASE0-01) is cited as the prior verification record.

**Gaps:**
The evidence is strong. The 0.95 rather than 0.97 reflects that the companion artifact (PROJ-014-AB-PHASE0-01) is cited but its content is not directly verifiable from this document — readers must locate and read a separate file to verify the initial constraint justification. This is a minor accessibility gap rather than an evidence quality defect.

**Improvement Path:**
None required for PASS at 0.95 threshold once other dimensions are addressed.

---

### Actionability (0.96/1.00)

**Evidence:**
All 40 entries (30 rewrites + 10 neutral descriptions) are self-contained and immediately usable as experimental stimuli. The condition format reference table provides clear mappings (C1 = NPT-007, C2 = NPT-014, C3 = NPT-013, Neutral = Factual passive). The C3 `<verify>` tags provide operationalized, scorable behavioral criteria that are directly usable by evaluators. The neutral descriptions are appropriate for blind scorer orientation: they describe the constraint factually without biasing the evaluator toward compliance or violation framing.

The document structure supports Phase 2 use directly — a scorer can navigate to any constraint by section, find all four framings, and use them without further transformation.

**Gaps:**
The 0.96 rather than 0.98 reflects the absence of explicit usage instructions for Phase 2 scorers (e.g., randomization protocol, scoring rubric reference). However, the document's scope is the Phase 0 stimulus design, not the Phase 2 scoring protocol — this is a scope boundary, not a defect. No revision needed for this dimension.

**Improvement Path:**
None required for PASS.

---

### Traceability (0.88/1.00)

**Evidence:**
Traceability is strong in most dimensions:
- Document ID (PROJ-014-AB-PHASE0-02) → TASK-025 → workflow (ab-testing-20260301-001) → phase (Phase 0 / Step 0.2)
- Each constraint linked to specific rule file and section
- Each defect fix linked to iteration number and corresponding gate report
- Version history in footer covers all 7 iterations with agent identifiers
- Source verification section at bottom of document lists file paths for all 10 constraints

**Gaps (D-014):**
The document header lists gate reports for iterations 1 through 5 only:
```
Gate Reports: three-style-rewrites-gate.md (i1) | ...-i2.md (i2) | ...-i3.md (i3) | ...-i4.md (i4) | ...-i5.md (i5)
```
The iteration 6 gate report (`three-style-rewrites-gate-i6.md`) exists in the adversary-gates directory (confirmed present) but is not linked in the header. A reader following the traceability chain from header references would find a gap between iteration 5 and the current iteration 7 gate report. The footer text references iteration 6 ("D-011 fixed in i6") but without a header link, the gate report is not immediately discoverable through the document's own navigation.

This is the most impactful defect in iteration 7 because Traceability is already a comparatively lower-weight dimension, and this gap pulls an otherwise-clean dimension down. The fix is trivial.

**Improvement Path:**
Add `| adversary-gates/three-style-rewrites-gate-i6.md (iteration 6)` to the Gate Reports header line. This will raise Traceability to 0.95+ and bring the composite score meaningfully closer to threshold.

---

## New Defects Found

### D-013 (Minor) — H-13 C2 Conditional Scope Qualifier

**Location:** Constraint 5 (H-13), C2 (Blunt Prohibition), second sentence.

**Current text:** "NEVER skip the revision cycle when a score falls below the threshold."

**Issue:** The "when a score falls below the threshold" clause is a conditional scope qualifier attached to the prohibition. All other C2 entries use bare "NEVER X" or "NEVER X than Y" (comparative) constructions. This entry introduces a "NEVER X when Y" pattern that is structurally distinct from C2 purity, even if the semantic intent is acceptable. Per the D-003 correction standard, C2 encodes what NOT to do; conditional qualifiers belong in C3's `<instead>` and `<verify>` tags.

**Severity:** Minor — the prohibition is semantically correct and the "when Y" does not encode an alternative; it scopes the applicability. However, the structural anomaly creates a detectable framing difference within the C2 condition that could affect experimental validity.

**Recommended fix:** Rewrite as: "NEVER skip the revision cycle for a below-threshold score." or "NEVER deliver a C2+ deliverable with a composite quality score below 0.92. NEVER bypass the mandatory revision cycle."

**Impact on score:** Contributes to Internal Consistency scoring at 0.93 rather than 0.95.

---

### D-014 (Minor) — Iteration 6 Gate Report Missing from Document Header

**Location:** Document header, Gate Reports line (line 10).

**Current text:** Lists gate reports for iterations 1-5 only. The iteration 6 gate report (`three-style-rewrites-gate-i6.md`) is absent.

**Issue:** The gate report for iteration 6 exists in the adversary-gates directory but is not linked in the document header. A reader following the traceability chain would discover a gap between iteration 5 header entry and the current iteration 7 gate being created. The iteration 6 report is referenced in the footer ("D-011 fixed in i6") but not navigably linked in the header.

**Severity:** Minor — the iteration 6 report is discoverable by directory inspection, and the footer reference provides a semantic link. However, the traceability chain in the document header is incomplete, reducing the header's utility as a navigation entry point.

**Recommended fix:** Add `| \`adversary-gates/three-style-rewrites-gate-i6.md\` (iteration 6)` to the Gate Reports header line, and also add the iteration 7 gate report link once it exists.

**Impact on score:** Primary driver of Traceability scoring at 0.88 rather than 0.94.

---

## Defect Resolution Status

| Defect | Status | Evidence |
|--------|--------|---------|
| D-001 (H-07 C3 missing sub-rule b) | Confirmed Resolved | H-07 C3 `<prohibition>` contains three NEVER clauses covering all sub-rules (a), (b), (c) |
| D-002 (H-22 scope asymmetry) | Confirmed Resolved | All H-22 framings reference only `/problem-solving`; both inline and table neutral match |
| D-003 (C2 "NEVER X without Y" constructions) | Confirmed Resolved | All 10 C2 entries are bare "NEVER X" — no "without Y" conditional clauses |
| D-004 (H-07 neutral passive negation) | Confirmed Resolved | Neutral reads "imports only from domain" — positive construction |
| D-005 (H-22 table neutral scope mismatch) | Confirmed Resolved | Table row 8 matches inline neutral exactly |
| D-006 (H-31 C2/C3 missing "or irreversible") | Confirmed Resolved | All four H-31 framings contain "destructive or irreversible" |
| D-007 (H-01 C3 missing Task tool prohibition) | Confirmed Resolved | H-01 C3 `<prohibition>` and `<verify>` both cover Task tool restriction |
| D-008 (H-01 C1/neutral missing Task tool restriction) | Confirmed Resolved | H-01 C1 uses "Omit the Task tool"; H-01 neutral uses "restricted from worker agent tool configurations" |
| D-009 (H-15 C1/C3/neutral missing critic-passthrough) | Confirmed Resolved | All four H-15 framings cover both sub-requirements (present-to-user AND pass-to-critic) |
| D-010 (H-01 C1 embedded negative "is not included") | Confirmed Resolved | Changed to "Omit" — clean positive imperative |
| D-011 (H-22 C1 temporal negation "not after") | Confirmed Resolved | Changed to "before the work begins" — plain temporal preposition |
| D-012 (H-31 C1 adverbial negation "without asking") | **Confirmed Resolved** | "without asking" removed; "When requirements are clear or the answer is in the codebase, proceed directly" fully establishes scope positively |
| D-013 (H-13 C2 conditional scope qualifier) | **New — Open** | See new defects section above |
| D-014 (Iteration 6 gate report missing from header) | **New — Open** | See new defects section above |

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Traceability | 0.88 | 0.95 | Fix D-014: Add iteration 6 and 7 gate report links to document header. Trivial single-line change. Highest composite impact given Traceability gap. |
| 2 | Internal Consistency | 0.93 | 0.96 | Fix D-013: Rewrite H-13 C2 second sentence to remove "when a score falls below the threshold" conditional qualifier. Replace with bare prohibition: "NEVER bypass the mandatory revision cycle." |
| 3 | Methodological Rigor | 0.93 | 0.96 | Add `<instead>` vs. C1 scope check to the Semantic Equivalence Check methodology. For each constraint, verify `<instead>` tag and C1 entry cover equivalent behavioral instruction sets. Document findings (likely all pass, closing the methodological gap). |

**Estimated composite after Priority 1 + 2 fixes:**
- Traceability: 0.88 → 0.95, weighted contribution: 0.0880 → 0.0950 (+0.0070)
- Internal Consistency: 0.93 → 0.96, weighted contribution: 0.1860 → 0.1920 (+0.0060)
- New composite estimate: 0.937 + 0.007 + 0.006 = **0.950** (meets threshold exactly)

Priority 3 fix would bring the composite to approximately 0.953-0.955, providing a safety margin above the 0.95 threshold.

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing weighted composite
- [x] Evidence documented for each score — specific text quotes and structural observations cited
- [x] Uncertain scores resolved downward (H-13 C2 observation documented as D-013 and reflected in Internal Consistency score rather than dismissed)
- [x] High-iteration calibration considered — iteration 7 is a near-complete document; 0.93x range is appropriate for remaining minor defects
- [x] No dimension scored above 0.95 without clear evidence (Actionability at 0.96 is the highest; evidence: all 40 entries are self-contained and immediately deployable with operationalized verify tags)
- [x] Score does not exceed prior iteration's 0.948 — this scoring is consistent with the incremental improvement trajectory; 0.937 reflects that D-013 and D-014 were not present in the prior evaluation scope

**Anti-leniency confirmation:** The score of 0.937 is lower than the prior iteration's 0.948. This is directionally correct: iteration 7's specific improvements (D-012 fix + comprehensive sweep) did close D-012, but the scoring evaluation independently identified two new minor defects (D-013, D-014) that were previously either undiscored or not surfaced. The strict scoring standard applied here finds that these defects, while minor, measurably reduce the composite below the prior score when evaluated freshly. The user specified >= 0.95 as the threshold; the current artifact does not meet it.

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.937
threshold: 0.95
weakest_dimension: Traceability
weakest_score: 0.88
critical_findings_count: 0
iteration: 7
new_defects:
  - id: D-013
    severity: Minor
    location: "Constraint 5 (H-13), C2, second sentence"
    description: "NEVER X when Y conditional scope qualifier — structurally inconsistent with C2 purity standard"
    fix: "Rewrite as bare prohibition: 'NEVER bypass the mandatory revision cycle.'"
    composite_impact: "-0.006 (Internal Consistency 0.93 vs expected 0.96)"
  - id: D-014
    severity: Minor
    location: "Document header, Gate Reports line"
    description: "Iteration 6 gate report (three-style-rewrites-gate-i6.md) absent from header despite existing in directory"
    fix: "Add i6 and i7 links to Gate Reports header line"
    composite_impact: "-0.007 (Traceability 0.88 vs expected 0.95)"
resolved_defects:
  - D-012: confirmed resolved — "without asking" removed from H-31 C1; positive scope established
prior_defects_all_resolved: true  # D-001 through D-011 all confirmed resolved
estimated_composite_after_fixes: 0.950
fixes_required_for_pass: 2  # D-013 + D-014 (Priority 1 and 2 only)
improvement_recommendations:
  - "Fix D-014: Add three-style-rewrites-gate-i6.md and three-style-rewrites-gate-i7.md links to document header"
  - "Fix D-013: Rewrite H-13 C2 second sentence — remove 'when a score falls below the threshold' conditional qualifier"
  - "Optional: Add <instead>-vs-C1 scope check to Semantic Equivalence Check methodology (Priority 3)"
score_trajectory:
  - iteration: 1
    score: 0.856
  - iteration: 2
    score: 0.882
  - iteration: 3
    score: 0.897
  - iteration: 4
    score: 0.928
  - iteration: 5
    score: 0.943
  - iteration: 6
    score: 0.948
  - iteration: 7
    score: 0.937
trajectory_note: "Iteration 7 score is lower than iteration 6. This reflects fresh independent identification of D-013 and D-014 which were not surfaced in prior evaluations. Both defects are minor and fixable in iteration 8. The comprehensive D-012 fix is confirmed; no regression in content quality."
```

---

*Report Version: 1.0*
*Scoring Agent: adv-scorer*
*Strategy: S-014 (LLM-as-Judge)*
*SSOT: `.context/rules/quality-enforcement.md`*
*Artifact: PROJ-014-AB-PHASE0-02 v7.0.0*
*Gate: C4 Adversary Gate, Iteration 7*
*Scored: 2026-03-01*
