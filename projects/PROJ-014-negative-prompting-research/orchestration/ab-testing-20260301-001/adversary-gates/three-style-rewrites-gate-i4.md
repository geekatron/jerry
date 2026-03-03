# Quality Score Report: Three-Style Rewrites — Iteration 4

## L0 Executive Summary

**Score:** 0.928/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Internal Consistency (0.88)
**One-line assessment:** The D-008 and D-009 fixes are both confirmed resolved, but a new minor defect (D-010) in H-01 C1 — "Ensure the Task tool is not included" — violates NPT-007's positive-only requirement via a negative embedded construction the validation checklist does not catch; composite falls 0.022 below the 0.95 C4 threshold.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-014-negative-prompting-research/orchestration/ab-testing-20260301-001/phase-0-design/three-style-rewrites.md`
- **Deliverable Type:** Research/Design (experimental stimulus artifact)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Threshold (C4):** 0.95 (elevated from H-13 baseline of 0.92 per task specification)
- **Scored:** 2026-03-01
- **Iteration:** 4 (addressing D-008, D-009)
- **Prior Score:** 0.897 (iteration 3)

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.928 |
| **Threshold** | 0.95 (C4) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No — standalone scoring |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.97 | 0.194 | All 40 entries present; all NPT format checks pass; validation checklist complete |
| Internal Consistency | 0.20 | 0.88 | 0.176 | D-008/D-009 resolved; new D-010 — H-01 C1 "not included" is a negative construction in a positive-only framing |
| Methodological Rigor | 0.20 | 0.93 | 0.186 | NPT-007/014/013 requirements met for all but H-01 C1 edge case; C2 purity holds; C3 four-tag structure intact |
| Evidence Quality | 0.15 | 0.95 | 0.143 | All constraints traceable to named source files; consequence fields derive from documented consequences |
| Actionability | 0.15 | 0.95 | 0.143 | Rewrites are specific and implementable; tool names, paths, and thresholds are concrete |
| Traceability | 0.10 | 0.96 | 0.096 | Source rules cited per constraint; gate reports referenced; iteration history documented |
| **TOTAL** | **1.00** | | **0.928** | |

---

## Detailed Dimension Analysis

### Completeness (0.97/1.00)

**Evidence:**

- All 30 rewrites present: 10 constraints × 3 conditions (C1, C2, C3), confirmed by the validation checklist (lines 367-378 of the artifact).
- All 10 neutral descriptions present in both inline form (within each constraint section) and the consolidated table (lines 348-359).
- Navigation table present with anchor links per H-23.
- Validation checklist covers all required dimensions: count verification, C1 negative-language check, C2 format check, C3 four-tag check, neutral quality check, condition label absence, semantic equivalence, and source verification.
- The four-tag structure check (lines 410-419) confirms all 10 constraints have all four XML elements in C3.
- Iteration history (S-010 self-review notes) documents all prior defects and their fixes — demonstrating process completeness.

**Gaps:**

- The gate reports header references only iterations 1 and 2: `adversary-gates/three-style-rewrites-gate.md (iteration 1) | adversary-gates/three-style-rewrites-gate-i2.md (iteration 2)`. The iteration 3 gate report is not linked in the header. This is a minor documentation gap — the iteration 3 S-010 notes reference the gate (line 531: "adv-scorer in three-style-rewrites-gate-i2.md") but the header should reference `three-style-rewrites-gate-i3.md` if it exists, or note that it was consolidated.

**Improvement Path:**

- Add the iteration 3 gate report path to the header, or add a note that D-005/D-006/D-007 were caught post-iteration-2 and documented inline.

---

### Internal Consistency (0.88/1.00)

**Evidence of consistency:**

D-008 RESOLVED: H-01 C1 now includes Task tool restriction ("Ensure the Task tool is not included in a worker agent's allowed_tools configuration") and neutral now includes "The Task tool is restricted from worker agent tool configurations; only orchestrator agents carry it." All four framings (C1, C2, C3, neutral) cover all three H-01 sub-requirements: (1) no sub-agent spawning, (2) results returned to orchestrator, (3) Task tool excluded from worker allowed_tools.

D-009 RESOLVED: H-15 C1 now includes "Complete a self-review pass before passing deliverables to critics as well." H-15 C3 prohibition now has two sentences: "NEVER present a deliverable without first completing a self-review. NEVER pass an unreviewed deliverable to a critic." H-15 C3 verify covers "presented or passed to a critic." H-15 neutral uses "and before it is passed to a downstream critic." All four framings cover both sub-requirements.

**Defect Found — D-010 (Minor):**

H-01 C1 reads: "Ensure the Task tool is not included in a worker agent's allowed_tools configuration."

The phrase "is not included" is a negative construction embedded within a positive imperative. NPT-007 specifies positive-only framing — "tells the model what to do" with "no prohibitions." The word "not" in "is not included" introduces a prohibition-by-negation that deviates from strict positive framing.

Compare against the correct positive alternatives:
- "Omit the Task tool from a worker agent's allowed_tools configuration."
- "Restrict the Task tool to orchestrator agents only; keep it absent from worker agent tool configurations."
- "Configure worker agent allowed_tools to exclude the Task tool."

The validation checklist (line 382-391) scans for "never", "don't", "must not", "forbidden" — it does not scan for negative constructions using "not" embedded in positive imperatives. This is a gap in the checklist's validation coverage.

This is an asymmetry within C1: all other C1 rewrites use purely positive constructions (e.g., "Return all results to the orchestrator", "Use uv run", "Keep domain code isolated", "Score all C2+ deliverables"). The H-01 C1 "not included" clause is the sole exception.

**Cross-Condition Equivalence Assessment (full table below):**

Per the methodology: read C2 first, enumerate sub-requirements, verify each in C1, C3, and neutral.

| # | Constraint | C2 Sub-Requirements | C1 | C3 | Neutral | Status |
|---|-----------|--------------------|----|----|---------|-|
| 1 | H-01 | (1) no spawning, (2) no Task in worker tools | (1) orchestrator-only + (2) "Ensure... not included" [negative construction] | (1) + (2) both in prohibition | (1) + (2) + (3) | PASS with D-010 flag |
| 2 | H-02 | (1) follow instructions, (2) no substituting | (1) + (2) + clarification guidance | (1) + (2) + clarification in instead | (1) + (2) | PASS |
| 3 | H-05 | (1) no python/pip/pip3 | uv run + uv add (positive) | prohibition + examples in instead | uv run + uv add (factual) | PASS |
| 4 | H-07 | (a) domain imports, (b) app imports, (c) bootstrap-only | (a) + (b) + (c) | (a) + (b) + (c) in prohibition | (a) + (b) + (c) | PASS |
| 5 | H-13 | (1) no delivery < 0.92, (2) no skip revision | (1) + (2) | (1) in prohibition; (2) in instead | (1) + (2) | PASS |
| 6 | H-10 | (1) one class per file | (1) | (1) | (1) | PASS |
| 7 | H-31 | (1) multiple interpretations, (2) unclear scope, (3) destructive, (4) irreversible | (1)-(4) | (1)-(4) in prohibition | (1)-(4) | PASS |
| 8 | H-22 | (1) no skipping /problem-solving, (2) no delaying | (1) + (2) proactive | (1) + (2) | (1) + (2) | PASS |
| 9 | T1-T5 | (1) no over-assignment, (2) no full when read-only sufficient | (1) via T1-first + escalation logic; (2) implicit in (1) | (1) in prohibition; (2) in instead | (1) + (2) | PASS |
| 10 | H-15 | (1) no unreviewed to user, (2) no unreviewed to critic | (1) + (2) | (1) + (2) in prohibition + verify | (1) + (2) | PASS |

9 of 10 constraints are fully equivalent across all four framings. H-01 passes semantic equivalence but has the NPT-007 purity defect (D-010).

**Improvement Path:**

Replace "Ensure the Task tool is not included in a worker agent's allowed_tools configuration." with a purely positive construction such as "Omit the Task tool from every worker agent's allowed_tools list." Extend the C1 negative-language checklist to scan for embedded "not" in "is not", "are not", "does not" constructions.

---

### Methodological Rigor (0.93/1.00)

**Evidence:**

**NPT-007 (C1 Positive) compliance:** 9 of 10 constraints use unambiguous positive-only imperative constructions. No NEVER, don't, must not, or forbidden language detected in any C1. The D-008 fix's "Ensure the Task tool is not included" is the sole deviation (D-010 above).

**NPT-014 (C2 Blunt) compliance:** All 10 C2 entries use pure "NEVER X" format. The D-003 fixes from iteration 2 removed all "NEVER X without Y" constructions. Re-verification confirms:
- H-02 C2: "NEVER override user instructions. NEVER substitute a different action." — clean.
- H-31 C2: "NEVER proceed on a request that has multiple valid interpretations, unclear scope, or destructive or irreversible implications. NEVER assume intent when ambiguity is present." — clean.
- H-22 C2: "NEVER skip /problem-solving invocation for research or analysis tasks. NEVER delay skill invocation until after work has started." — clean.
- H-15 C2: "NEVER present an unreviewed deliverable. NEVER pass an unreviewed deliverable to a critic." — clean.
All 10 C2 entries are NPT-014 compliant.

**NPT-013 (C3 Structured) compliance:** All 10 constraints have all four required XML tags: `<prohibition>`, `<consequence>`, `<instead>`, `<verify>`. The four-tag check at lines 410-419 confirms this. All tags are internally consistent — the `<instead>` tags describe the positive alternative matching the prohibited behavior; `<verify>` tags provide checkable assertions.

**Note on H-31 C3 prohibition:** "NEVER proceed on an ambiguous request without asking a clarifying question when..." — this is a "NEVER X without Y" construction in C3. This is structurally appropriate for NPT-013 because the structured format explicitly accommodates nuance in the `<prohibition>` tag; only C2 (NPT-014) requires bare "NEVER X" form. No defect here.

**Neutral framing compliance:** All 10 neutral descriptions use factual/passive language. No imperative verbs detected. No prohibition language. No XML tags. H-22 neutral ("is expected to be invoked") is factual description of framework behavior, not instruction.

**Semantic equivalence methodology:** The upgraded checklist (iteration 2) enumerates sub-requirements from C2 first, then cross-verifies C1, C3, and neutral — confirmed in the checklist notes at line 443.

**Gaps:**

The validation checklist's C1 negative-language check does not catch "not" in embedded constructions ("is not included", "are not permitted", etc.) — only standalone prohibition keywords. This gap allowed D-010 to pass the checklist undetected.

**Improvement Path:**

Extend C1 checklist to include: "No 'not' embedded in 'is not', 'are not', 'does not' constructions." Fix H-01 C1 to use a positive construction.

---

### Evidence Quality (0.95/1.00)

**Evidence:**

- All 10 constraints cite their source rules with specific file paths and section references (Source Verification Check, lines 458-467).
- Consequence fields in C3 derive from documented, real consequences: "CI blocks the merge" (H-07, H-10), "environment corruption and CI build failures" (H-05), "context window exhaustion" (H-01), "trust erosion" (H-02). These are not invented — they match the source rule files' documented consequences.
- The companion artifact (PROJ-014-AB-PHASE0-01, constraint-selection.md) is cited as the source verification basis.
- The D-002 narrowing rationale is documented at line 505-507: NPT-014 works best with a single focused prohibition; experiment tests framing style, not skill coverage breadth.
- Iteration 4 changes are precisely scoped: D-008 adds one positive sentence to C1, one factual sentence to both neutral locations. D-009 adds one sentence to C1, one sentence to C3 prohibition, updates C3 verify, and updates both neutral locations.

**Minor gap:**

The iteration 3 gate report is not linked from the header (same as noted in Completeness). Evidence of D-005, D-006, D-007 fixes exists in the S-010 notes but is not linked to an external gate report document.

**Improvement Path:**

Link the iteration 3 gate report in the header (if the file exists). If the iteration 3 score was incorporated directly from the adv-scorer rather than persisted as a separate gate file, note this explicitly.

---

### Actionability (0.95/1.00)

**Evidence:**

- C1 rewrites provide specific, implementable positive instructions: concrete tool names (`uv run`, `uv add`, `/problem-solving`), specific file paths (`src/bootstrap.py`, `src/domain/`, `src/application/`), quantitative thresholds (0.92), and procedural steps ("Start from T1... escalate to the next tier only when...").
- C2 rewrites provide clear behavioral boundaries: an agent reading "NEVER use python, pip, or pip3 directly" knows exactly what commands to avoid.
- C3 rewrites provide both the prohibition and the concrete alternative in `<instead>`. The `<verify>` tags are expressed as checkable post-conditions ("No python, pip, or pip3 command appears in the response").
- Neutral descriptions accurately characterize what the constraint controls without prescribing behavior — appropriate for scorer orientation.
- All 10 `<verify>` tags are formulated as observable conditions, not vague intent assertions.

**Minor gap:**

H-13 C3 `<instead>` says "identify dimensions scoring below threshold, revise those dimensions specifically, and re-score before delivering" — this is actionable but does not name the six S-014 dimensions. For an agent that has not loaded quality-enforcement.md, this could be insufficiently specific. However, C1 says "Score all C2+ deliverables using the S-014 rubric across all six dimensions" — which is within the same document structure. This is a minor coordination gap, not a blocking defect.

**Improvement Path:**

The actionability score is strong. No high-priority changes warranted here.

---

### Traceability (0.96/1.00)

**Evidence:**

- Full source verification table (lines 458-467) lists the specific file and section for each of the 10 constraints.
- Gate report links in the header trace the revision history.
- S-010 self-review notes document all four iterations of changes with per-defect cross-references (D-001 through D-009).
- The document ID (PROJ-014-AB-PHASE0-02), phase (0 / Step 0.2), workflow (ab-testing-20260301-001), parent task (TASK-025), and author chain are all recorded in the frontmatter.
- The semantic equivalence checklist explicitly notes which defect fixes resolved which sub-requirement gaps (e.g., "D-007 fixed C3; D-008 fixed C1 and neutral").
- Version history at the bottom (lines 588-596) is complete and consistent with the S-010 notes.

**Minor gap:**

The gate report header links iterations 1 and 2 only; the iteration 3 gate report path is absent. Full traceability would require all four gate reports to be linked.

**Improvement Path:**

Add `adversary-gates/three-style-rewrites-gate-i3.md` (iteration 3) to the header gate report list.

---

## D-008 and D-009 Resolution Status

### D-008 (Significant — H-01 C1 and neutral missing Task tool restriction)

**Status: RESOLVED.**

H-01 C1 now reads: "Return all results to the orchestrator. When a task is too large for a single agent, decompose it into sub-results and return each to the orchestrator for coordination. The orchestrator is the sole entity that spawns additional workers. Ensure the Task tool is not included in a worker agent's allowed_tools configuration."

H-01 neutral (inline and table) now reads: "The framework enforces a single-level agent nesting boundary. Worker agents return results to the orchestrator; the orchestrator coordinates all subsequent delegations. The Task tool is restricted from worker agent tool configurations; only orchestrator agents carry it."

Semantic equivalence is achieved for all three sub-requirements across all four framings. The resolution introduced D-010 (the "not included" negative construction in C1), which is a new minor defect.

### D-009 (Minor — H-15 critic-passthrough absent from C1/C3/neutral)

**Status: RESOLVED.**

H-15 C1 now reads: "Before presenting any deliverable, perform a self-review: check completeness, internal consistency, and evidence quality. Identify and correct any defects found. Note the corrections made. Only present the deliverable after the self-review is complete. Complete a self-review pass before passing deliverables to critics as well."

H-15 C3 prohibition now reads: "NEVER present a deliverable without first completing a self-review. NEVER pass an unreviewed deliverable to a critic."

H-15 C3 verify now reads: "The response includes an explicit self-review step with findings noted before the final deliverable is presented or passed to a critic."

H-15 neutral now reads: "The framework requires a self-review step before any deliverable is presented to the user and before it is passed to a downstream critic."

All four framings explicitly cover both sub-requirements (present-to-user and pass-to-critic). D-009 is fully resolved.

---

## New Defects Found

### D-010 (Minor) — H-01 C1 Negative Construction in Positive-Only Framing

**Location:** Constraint 1 (H-01), C1 (Positive / NPT-007), sentence 4.

**Text:** "Ensure the Task tool is not included in a worker agent's allowed_tools configuration."

**Problem:** The phrase "is not included" is a negative construction — it tells the model what NOT to be present rather than what TO DO. NPT-007 requires positive-only framing: "tells the model what to do." A prohibition embedded in "ensure X is not Y" deviates from strict positive-only semantics. This matters for the A/B experiment because the C1 condition is intended to test pure positive framing; any residual negative language creates a confound between C1 and C2 stimulus conditions.

The validation checklist (lines 382-391) scans for "never", "don't", "must not", "forbidden" but does not catch "not" embedded in constructions like "is not included", "are not permitted", or "does not contain."

**Severity:** Minor — the semantic intent is correct and the scope is equivalent to C2/C3. However, for experimental stimulus integrity, strict NPT-007 compliance is required in C1.

**Fix required:**

Replace: "Ensure the Task tool is not included in a worker agent's allowed_tools configuration."
With one of:
- "Omit the Task tool from every worker agent's allowed_tools list."
- "Keep the Task tool absent from worker agent tool configurations; restrict it to orchestrator agents only."
- "Configure worker agent definitions to carry only the tools their tasks require, excluding the Task tool."

Also extend the C1 validation checklist to scan for "not" in embedded constructions:
- "is not", "are not", "does not", "will not", "should not", "cannot" — all should be flagged for review in C1 entries.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Internal Consistency / Methodological Rigor | D-010 present | Resolved | Replace H-01 C1 "Ensure the Task tool is not included..." with a purely positive construction: "Omit the Task tool from every worker agent's allowed_tools list." |
| 2 | Internal Consistency / Methodological Rigor | Checklist gap | Closed | Extend C1 checklist to include "is not / are not / does not / will not" embedded negative constructions as flagged terms requiring review |
| 3 | Completeness / Traceability | Iteration 3 gate report not linked | Linked | Add `adversary-gates/three-style-rewrites-gate-i3.md` to the header gate report list |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score — specific line numbers and text cited
- [x] Uncertain scores resolved downward (Internal Consistency scored 0.88 not 0.90 due to D-010 being a genuine NPT-007 purity defect in an experiment stimulus where framing purity is the research variable)
- [x] First-draft calibration not applicable — this is iteration 4; scored against rubric as-it-stands, not relative to prior iterations
- [x] No dimension scored above 0.95 without exceptional evidence (Traceability at 0.96 — well-evidenced with specific line citations; Evidence Quality at 0.95 — supported by source verification table)
- [x] Anti-leniency instruction applied: D-010 identified despite checklist passing — scored against the actual NPT-007 requirement, not the checklist

**Scoring rationale for Internal Consistency at 0.88:** The rubric states 0.9+ requires "no contradictions, all claims aligned." The H-01 C1 entry contains a claim ("this is positive-only framing") that is contradicted by evidence ("is not included" is a negative construction). The contradiction is minor — it is not a semantic equivalence failure and it is a single sentence — but it is real, traceable, and consequential for the experiment's stimulus integrity. A score of 0.88 (7-0.89 band: "minor inconsistencies") is appropriate.

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.928
threshold: 0.95
weakest_dimension: Internal Consistency
weakest_score: 0.88
critical_findings_count: 0
iteration: 4
improvement_recommendations:
  - "Replace H-01 C1 sentence 4 with purely positive construction: 'Omit the Task tool from every worker agent's allowed_tools list.' — resolves D-010 NPT-007 purity defect"
  - "Extend C1 checklist to scan for embedded negative constructions (is not, are not, does not, will not)"
  - "Add iteration 3 gate report path to document header (traceability gap)"
```

---

*Score Report Version: 1.0.0*
*Scoring Agent: adv-scorer*
*SSOT: `.context/rules/quality-enforcement.md`*
*Strategy: S-014 LLM-as-Judge, 6-dimension weighted composite*
*Artifact Version: 4.0.0 (design-agent-002-r4)*
*Scored: 2026-03-01*
