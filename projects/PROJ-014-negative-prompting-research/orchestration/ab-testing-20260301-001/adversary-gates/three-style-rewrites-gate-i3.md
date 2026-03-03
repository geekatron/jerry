# Quality Score Report: Three-Style Rewrites — PROJ-014 A/B Testing (Iteration 3)

## L0 Executive Summary

**Score:** 0.897/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Internal Consistency (0.83)
**One-line assessment:** Iteration 3 resolves all five iteration-2 fixes (D-005 through D-007 plus two minors), but introduces two new cross-condition asymmetries — D-008 (H-01 C1 and neutral do not encode the Task tool prohibition that C2 and C3 explicitly carry) and D-009 (H-15 C2 prohibits passing to a critic; C1 and C3 do not) — keeping the artifact below the 0.95 C4 threshold for the third iteration.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-014-negative-prompting-research/orchestration/ab-testing-20260301-001/phase-0-design/three-style-rewrites.md`
- **Deliverable Type:** Analysis / Experimental Design Artifact
- **Criticality Level:** C4 (Critical — irreversible architectural impact on A/B experiment validity)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Iteration:** 3 (revision addressing D-005, D-006, D-007, H-31 C3 "at least", traceability gap from iteration 2)
- **Scored:** 2026-03-01

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.897 |
| **Threshold** | 0.95 (C4 adversary gate) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No (adv-executor reports not provided; direct artifact scoring) |
| **Prior Score (Iteration 2)** | 0.882 |
| **Score Delta** | +0.015 |

---

## Iteration 2 Defect Resolution Status

| Defect | Severity | Status | Evidence |
|--------|----------|--------|----------|
| D-005 | Significant | **RESOLVED** | H-22 Neutral Descriptions table row 8 (line 357) now reads: "The framework maps research and analysis tasks to the `/problem-solving` skill. The skill is expected to be invoked at task initiation rather than partway through or after completion." This matches the inline neutral (lines 256-257) exactly. No four-skill reference remains in the table. |
| D-006 | Borderline | **RESOLVED** | H-31 C2 (line 238): "destructive or irreversible implications" — confirmed. H-31 C3 `<prohibition>` (line 246): "the action is destructive or irreversible" — confirmed. All four conditions (C1, C2, C3, neutral) now consistently encode both trigger conditions. |
| D-007 | Borderline | **RESOLVED** | H-01 C3 `<prohibition>` (lines 66-67): "NEVER spawn sub-agents from a worker agent. NEVER declare the Task tool in a worker agent's allowed_tools." H-01 C3 `<verify>` (line 69): "No Task tool call appears in the worker agent's output. The worker agent's allowed_tools does not include the Task tool." Both clauses now match C2's two-clause coverage. |
| H-31 C3 "at least" | Minor | **RESOLVED** | H-31 C3 `<prohibition>` (line 246): "without asking a clarifying question" — no "at least" qualifier present. Confirmed. |
| Traceability gap | Minor | **RESOLVED** | Document header (line 10) now contains: "Gate Reports: `adversary-gates/three-style-rewrites-gate.md` (iteration 1) \| `adversary-gates/three-style-rewrites-gate-i2.md` (iteration 2)". Both prior gate report paths are linked. |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.95 | 0.190 | All 40 elements present (30 rewrites + 10 neutrals); navigation table with anchors; validation checklist fully populated; gate report paths added; S-010 self-review for all three iterations |
| Internal Consistency | 0.20 | 0.83 | 0.166 | D-005/D-006/D-007 resolved; D-008 (new): H-01 C1 and neutral omit Task tool prohibition present in C2 and C3; D-009 (new, minor): H-15 C2 covers "pass to critic" while C1 and C3 cover only "present to user" |
| Methodological Rigor | 0.20 | 0.88 | 0.176 | All NPT-007/NPT-014/NPT-013 format requirements met; D-008 reveals the semantic equivalence checklist incorrectly certified H-01 as co-extensive when its own sub-requirement table shows the asymmetry |
| Evidence Quality | 0.15 | 0.90 | 0.135 | All constraints cite source files with specific paths; C3 consequence fields verified against documented source consequences; three-iteration revision trail documented with precise change descriptions |
| Actionability | 0.15 | 0.90 | 0.135 | All rewrites operationally clear; "at least" qualifier removed; concrete tool names, file paths, thresholds throughout; D-008 gap means C1 does not teach Task-tool-declaration prohibition to an acting agent |
| Traceability | 0.10 | 0.95 | 0.095 | Full traceability chain: source citations, parent document references, gate report links (both iterations), three-iteration revision trail with change rationale |
| **TOTAL** | **1.00** | | **0.897** | |

---

## Detailed Dimension Analysis

### Completeness (0.95/1.00)

**Evidence:**
- All 30 rewrites present, verified by heading count and validation checklist (lines 367-378). Organized in 10 constraint sections, each containing C1, C2, and C3.
- All 10 neutral descriptions present in both inline form (one per constraint section) and consolidated table form (lines 348-359).
- Navigation table with anchor links present (lines 14-21), covering all four major sections.
- Validation checklist (lines 363-467) covers: count verification, C1 negative-language check (10 items), C2 format check (10 items), C3 four-tag check (10 items), neutral quality check (11 items), condition-label absence check, semantic equivalence check (10 constraints with sub-requirement enumeration), source verification check (10 constraints).
- S-010 self-review present for all three iterations (lines 471-554), including iteration 3 post-fix cross-condition verification (lines 549-554).
- Gate report paths added to document header (line 10): iteration 1 and iteration 2 gate report paths linked — the traceability gap identified in iteration 2 scoring is closed.
- Document version 3.0.0, workflow, and agent provenance present (lines 558-565).

**Gaps:**
None substantive. The dual-presentation of neutrals (inline + table) creates redundancy but this is an intentional design choice to serve two audiences (rewrite readers and Phase 2 scorers). Both now consistent.

**Improvement Path:**
No improvement needed for Completeness. Current 0.95 is appropriate — the artifact meets the 0.9+ rubric criteria (all requirements addressed with depth).

---

### Internal Consistency (0.83/1.00)

**Evidence (resolved):**
D-005 (H-22 table neutral): RESOLVED — see defect resolution table above.
D-006 (H-31 "irreversible"): RESOLVED — all four conditions now carry both trigger terms.
D-007 (H-01 C3 missing Task tool): RESOLVED — C3 now has two prohibition clauses matching C2.
H-31 C3 "at least": RESOLVED — removed.

**D-008 (New, Significant): H-01 C1 and neutral do not encode the Task tool prohibition**

The document's own semantic equivalence checklist (line 445) enumerates three sub-requirements for H-01:
- Sub-requirement (1): workers do not spawn sub-workers
- Sub-requirement (2): results return to orchestrator
- Sub-requirement (3): Task tool not in worker allowed_tools

The checklist then maps coverage as:
- C1: covers (1) "The orchestrator is the sole entity that spawns additional workers" and (2) "return each to the orchestrator for coordination"
- C2: covers (1) and (3)
- C3: covers (1), (3), and (2)
- Neutral: covers (1) and (2)

The checklist then claims "All four co-extensive — passes." This claim is incorrect on its face: the checklist's own sub-requirement table shows that C1 and neutral cover (1) and (2) only, while C2 and C3 cover (1) and (3). Sub-requirement (3) — the explicit Task tool prohibition — is absent from C1 and neutral.

C1 (lines 52-53): "Return all results to the orchestrator. When a task is too large for a single agent, decompose it into sub-results and return each to the orchestrator for coordination. The orchestrator is the sole entity that spawns additional workers." — No mention of Task tool or allowed_tools.

Neutral (lines 47-48): "The framework enforces a single-level agent nesting boundary. Worker agents return results to the orchestrator; the orchestrator coordinates all subsequent delegations." — No mention of Task tool.

A model receiving C1 learns: orchestrator is sole spawner; return results upward. It does NOT learn: exclude Task tool from allowed_tools declaration. A model receiving C2 or C3 learns both the behavioral prohibition and the structural configuration prohibition. This is a content confound. In an experiment measuring compliance rates across framing styles, a C1 agent will fail to prohibit Task tool declarations not because of framing style but because C1 omits sub-requirement (3) entirely. This inflates the apparent performance gap between C1 and C2/C3 for any scenario testing Task tool declaration specifically.

The D-007 fix correctly addressed C3-vs-C2 scope asymmetry (Task tool added to C3). However, the same asymmetry between C1 and C2 was not addressed — possibly because C1's formulation ("The orchestrator is the sole entity that spawns additional workers") was considered semantically equivalent to sub-requirement (3). It is not equivalent: prohibiting spawning-behavior and prohibiting Task tool in the declaration field are related but distinct requirements. An agent could know the orchestrator is the sole spawner and still add Task to its allowed_tools list without invoking it.

**D-009 (New, Minor): H-15 C2 scope is broader than C1 and C3**

H-15 C2 (lines 328-329): "NEVER present an unreviewed deliverable. NEVER pass an unreviewed deliverable to a critic." — two prohibitions covering two distinct scenarios.

H-15 C1 (lines 321-323): "Before presenting any deliverable, perform a self-review... Only present the deliverable after the self-review is complete." — covers presenting only.

H-15 C3 `<prohibition>` (line 336): "NEVER present a deliverable without first completing a self-review." — covers presenting only.

H-15 C3 `<verify>` (line 339): "The response includes an explicit self-review step with findings noted before the final deliverable is presented." — covers presenting only.

C2 is the only condition that explicitly prohibits passing an unreviewed deliverable to a critic (as distinct from presenting it to the user). C1 and C3 encode only the "presenting to user" scenario. A model receiving C2 would also block critic-passthrough without self-review; models receiving C1 or C3 would not explicitly know this. This is an upward scope asymmetry in C2 — C2 carries more behavioral content than C1 or C3 for this constraint.

D-009 is minor: in practice the critic-passthrough prohibition is a natural extension of the user-presentation prohibition (if you don't present without review, you don't pass to critic without review either). The operational difference for the experiment is small. However it is a real asymmetry and should be corrected for experimental hygiene.

**Gaps:**
Two new cross-condition asymmetries found, with D-008 constituting a genuine experimental validity concern.

**Improvement Path:**
- D-008: Add explicit Task tool reference to H-01 C1. Options: (a) Add "Ensure the Task tool is not included in a worker agent's allowed_tools declaration" as a third sentence to C1. (b) Alternatively, update H-01 neutral to reference the Task tool explicitly — "The framework enforces a single-level agent nesting boundary. Worker agents return results to the orchestrator; the orchestrator coordinates all subsequent delegations. Worker agents do not include the Task tool in their declared tool configuration." Option (a) addresses the C1 content gap directly; option (b) addresses the neutral gap.
- D-009: Add "NEVER pass an unreviewed deliverable to a critic or downstream agent" to H-15 C1 (e.g., as a fourth sentence: "Do not pass the deliverable to a critic until the self-review is complete.") And add a second clause to H-15 C3 `<prohibition>`: "NEVER pass a deliverable to a critic without first completing a self-review." Update `<verify>` to include the critic-passing check.

---

### Methodological Rigor (0.88/1.00)

**Evidence:**
NPT-007 (C1) compliance: All 10 C1 rewrites are positive-only. Independent verification confirms no negative language ("never," "don't," "must not," "forbidden") in any C1. The validation checklist at lines 381-391 confirms each. D-007 fix did not introduce negative language into any C1 (the fix targeted C3 only).

NPT-014 (C2) compliance: All 10 C2 rewrites use bare NEVER X form. Post-D-003 revision, all four previously flagged C2 rewrites (H-02, H-31, H-22, H-15) now use pure NEVER X form without embedded alternatives or conditional qualifiers. H-31 C2 uses "NEVER X when [condition]" form where the condition defines WHAT is prohibited rather than offering an alternative — this is NPT-014 compliant. Validation checklist at lines 393-406 confirms each.

NPT-013 (C3) compliance: All 10 C3 rewrites contain all four required XML tags (`<prohibition>`, `<consequence>`, `<instead>`, `<verify>`). Validation checklist at lines 408-419 confirms each. D-007 fix correctly expanded H-01 C3 prohibition and verify tags without violating any structural requirement.

Neutral format compliance: All 10 neutrals are factual/passive throughout. No imperatives, no prohibition language, no XML in any neutral. Validation checklist at lines 421-433 confirms each. H-22 neutral "is expected to be invoked" is factual (describes framework behavior) not instructional — correctly retained.

**Gaps:**
The semantic equivalence checking methodology has a logical error that went uncaught in three iterations: the checklist claims all four conditions are co-extensive for H-01 despite its own sub-requirement table showing C1 and neutral cover (1) and (2) only, while C2 and C3 cover (1) and (3). The methodology's own output contradicts its conclusion. This indicates the sub-requirement enumeration approach works correctly (it correctly identifies the differential coverage) but the co-extensiveness claim is evaluated impressionistically rather than from the sub-requirement table. A strict reading of the table would have flagged D-008 before the checklist signed off.

Similarly, the D-009 gap (H-15 C2 broader than C1/C3) was not caught by the semantic equivalence check. The checklist for H-15 (line 454) states "Sub-requirements: (1) self-review before presenting. C1: (1). C2: (1). C3: (1). Neutral: (1). All four co-extensive." This treats "pass to critic" as subsumed under (1), which is debatable.

**Improvement Path:**
The semantic equivalence checklist should be upgraded to require: (a) sub-requirements are listed by reading C2 first (the most explicit condition), then verified in C1, C3, and neutral; and (b) any sub-requirement present in C2 that is absent from C1 or C3 must be flagged and either corrected or explicitly accepted with documented rationale. Reading C2 first guards against the pattern where C1's more implicit formulation is mistakenly treated as co-extensive with C2's explicit formulation.

---

### Evidence Quality (0.90/1.00)

**Evidence:**
Source citations for all 10 constraints at lines 458-467 with specific file paths and section identifiers. Examples:
- "H-01 verified against: `.context/rules/quality-enforcement.md` (HARD Rule Index, L2-REINJECT rank=1) and `.context/rules/agent-development-standards.md` (Structural Patterns section)" (line 458)
- "H-07 verified against: `.context/rules/architecture-standards.md` (HARD Rules table, line 34)" (line 461)

C3 consequence fields trace to documented source consequences, not invented ones:
- H-01: "Unbounded recursion exhausts the context window, violates P-003" — from agent-development-standards.md
- H-05: "environment corruption and CI build failures" — from python-environment.md HARD Rules table
- H-07: "Architecture tests fail and CI blocks the merge" — from architecture-standards.md
- H-10: "AST checks fail and CI blocks the merge" — traceable to source consequence documentation

Iteration 3 self-review (lines 529-554) documents each fix precisely: exact text changes, before-and-after on specific lines, cross-condition post-verification.

The parent document (constraint-selection.md / PROJ-014-AB-PHASE0-01) is referenced at lines 29 and 491, establishing the evidence chain from constraint selection through rewrite production.

**Gaps:**
The iteration 2 score report recommended adding a term-by-term comparison step to source verification (comparing each trigger condition in the source rule against each framing condition). This was not added as a formalized methodology step. The D-006 gap was corrected, but the check that would prevent the D-006 class of issue was not institutionalized. The D-008 gap (H-01 C1 missing sub-requirement 3) is another instance of the same failure mode: a sub-requirement present in the source and encoded in C2/C3 was not verified as present in C1.

**Improvement Path:**
Add a formal term-by-term comparison step to the source verification check: for each constraint, list the behavioral sub-requirements directly from the source rule text, then verify each sub-requirement is encoded (explicitly or by strong implication) in each of C1, C2, C3, and neutral. A gap in any cell of the resulting matrix should block the "co-extensive — passes" claim.

---

### Actionability (0.90/1.00)

**Evidence:**
All 30 rewrites provide sufficient operational clarity for an agent to act on them. Specific evidence of high actionability:
- H-05 C3 `<instead>`: "Use uv run for all execution (e.g., uv run pytest tests/) and uv add for all dependency management (e.g., uv add requests)" — working examples included.
- H-07 C3 `<verify>`: Fully specific import path checks enumerated for all three sub-rules across src/domain/, src/application/, and src/bootstrap.py.
- H-10 C3 `<instead>`: "e.g., money.py for class Money" — concrete instantiation.
- H-13 C1: "0.92 or above", "S-014 rubric across all six dimensions" — specific threshold and method named.
- T1-T5 C3 `<instead>`: "defaulting to T1 unless a specific higher-tier tool is genuinely needed" — default action specified.
- H-31: "at least" qualifier removed from C3 — now reads "asking a clarifying question," consistent with C1's "one targeted clarifying question."

**Gaps:**
H-01 C1 (D-008 impact): An agent operating from C1 learns to return results to the orchestrator and not spawn sub-workers. It does not learn to exclude the Task tool from its allowed_tools declaration. The actionable instruction "do not include Task in your allowed_tools" is absent from C1. This reduces C1's actionability specifically for the Task-tool-declaration scenario.

H-15 (D-009 impact): An agent operating from C1 or C3 learns to self-review before presenting. It does not learn to self-review before passing to a critic. C1 and C3 are less actionable than C2 for the critic-passthrough scenario.

H-31 C3 `<prohibition>` (line 246): The prohibition uses "without asking a clarifying question" while C1 uses "ask one targeted clarifying question." The difference between "a" and "one" is de minimis and not a meaningful actionability gap.

**Improvement Path:**
Same as D-008 and D-009 fixes described under Internal Consistency. Once H-01 C1 includes explicit Task tool guidance and H-15 C1/C3 include critic-passthrough guidance, actionability for those conditions reaches equivalence with C2.

---

### Traceability (0.95/1.00)

**Evidence:**
- Document header (lines 3-10): Document ID (PROJ-014-AB-PHASE0-02), Phase (0/Step 0.2), Workflow (ab-testing-20260301-001), Parent Task (TASK-025), Date (2026-03-01), Author (three revision agents named), Status ("REVISED — iteration 3 addressing D-005, D-006, D-007"), Gate Reports (both iterations 1 and 2 linked).
- Source verification for all 10 constraints (lines 458-467) with specific file paths and section names.
- Parent document (constraint-selection.md / PROJ-014-AB-PHASE0-01) referenced at lines 29 and 491 — establishing the constraint selection → rewrite production chain.
- S-010 self-review for all three iterations (lines 471-554) documents the revision trail with specific changes, rationale, and post-fix verification steps.
- Document version 3.0.0 at line 558.
- Workflow and step at line 559: "Workflow: ab-testing-20260301-001 / Step 0.2."
- Source verification note at line 561: "constraint-selection.md (PROJ-014-AB-PHASE0-01) + direct source file reads."

**Gaps:**
The iteration 2 score report suggested referencing the iteration 1 gate report path. This has been done: line 10 now includes both gate report paths. No remaining traceability gaps.

Minor: The iteration 3 self-review documents fixes at lines 529-554 but does not include a line reference to the changed text in each case (it describes changes in prose). Adding line references would marginally improve traceability.

**Improvement Path:**
No change required to maintain 0.95. The optional improvement (line references in revision notes) would push toward 0.97 but is not necessary for experimental integrity.

---

## New Defects Found (D-008, D-009)

| ID | Severity | Dimension Impacted | Description | Required Fix |
|----|----------|-------------------|-------------|--------------|
| D-008 | Significant | Internal Consistency, Actionability | H-01 C1 and neutral do not encode sub-requirement (3): "Task tool not in worker allowed_tools." The document's own semantic equivalence checklist (line 445) correctly maps C1 as covering only sub-requirements (1) and (2), and neutral as covering only (1) and (2), while C2 and C3 cover (1) and (3). The checklist then incorrectly concludes "All four co-extensive — passes" despite the sub-requirement table showing the asymmetry. An agent receiving C1 learns behavioral nesting discipline but not structural configuration discipline (Task tool exclusion from allowed_tools declaration). This is a content confound: C1 agents may show lower Task-tool-declaration compliance not due to framing style but due to missing content. | H-01 C1: Add a third sentence — "Ensure the Task tool is not included in a worker agent's allowed_tools configuration." H-01 neutral: Add a clause — "...and worker agents do not declare the Task tool in their tool configuration." Update validation checklist H-01 semantic equivalence entry to reflect that C1 now covers (1), (2), and (3) and neutral covers (1), (2), and a structural note. |
| D-009 | Minor | Internal Consistency | H-15 C2 contains two prohibition clauses: (1) "NEVER present an unreviewed deliverable" and (2) "NEVER pass an unreviewed deliverable to a critic." H-15 C1 covers only (1) — presenting to the user. H-15 C3 `<prohibition>` and `<verify>` cover only (1). C2 is the only condition that explicitly extends the self-review requirement to the critic-passthrough scenario. A model receiving C2 would block critic-passthrough without self-review; models receiving C1 or C3 would not have this explicitly encoded. Upward scope asymmetry: C2 carries more content than C1 or C3. | H-15 C1: Add "Do not pass the deliverable to a critic until the self-review is complete." H-15 C3 `<prohibition>`: Add second sentence "NEVER pass a deliverable to a critic without first completing a self-review." H-15 C3 `<verify>`: Add "and the deliverable was not passed to a critic before self-review." Update checklist accordingly. |

---

## Improvement Recommendations (Priority Ordered)

| Priority | Defect | Dimension | Current | Target | Recommendation |
|----------|--------|-----------|---------|--------|----------------|
| 1 | D-008 | Internal Consistency | 0.83 | 0.90+ | Add explicit Task tool prohibition to H-01 C1 (third sentence) and Task tool reference to H-01 neutral (structural note). Update checklist H-01 semantic equivalence entry. This closes the most significant experimental validity gap — without this fix, C1-vs-C2/C3 compliance differences for Task tool scenarios are confounded by content, not framing style. |
| 2 | D-009 | Internal Consistency | 0.83 | 0.90+ | Add critic-passthrough prohibition to H-15 C1 and H-15 C3 `<prohibition>` and `<verify>`. Minor change but necessary to eliminate C2's upward scope asymmetry for this constraint. |
| 3 | Checklist methodology | Methodological Rigor | 0.88 | 0.92+ | Upgrade the semantic equivalence check to read C2 first when enumerating sub-requirements, then verify each sub-requirement in C1, C3, and neutral. Any sub-requirement in C2 absent from C1 or neutral must be flagged rather than implicitly accepted. The three-iteration failure to catch D-008 traces to this methodology gap. |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite — Internal Consistency evaluated against the 10 constraints in sequence before scoring any other dimension
- [x] Evidence documented for each score with specific line references — all scores tied to artifact text
- [x] Uncertain scores resolved downward — Internal Consistency at 0.83 (considered 0.85): D-008 is a genuine experimental validity concern, not cosmetic; the checklist's own sub-requirement mapping shows the asymmetry it claims to resolve. Downward resolution applied.
- [x] C4 calibration considered: threshold is 0.95; this artifact scores 0.897 (+0.015 over iteration 2). Two new defects are real and independently identifiable. Iteration 3 progress is genuine but not sufficient.
- [x] No dimension scored above 0.95 without exceptional evidence — Completeness and Traceability at 0.95 are justified by complete element presence and full traceability chain; exceptional evidence documented above
- [x] Prior score (0.882) not anchored to current scoring — each dimension re-evaluated fresh

**Anti-leniency note on Internal Consistency:** The temptation after three iterations is to treat D-008 as a residual edge case and score Internal Consistency at 0.87+. Resisted. The reason is the nature of the artifact: it is an A/B experiment design document where cross-condition equivalence is the primary validity requirement. C1 and neutral for H-01 are currently under-specified relative to C2 and C3 by one distinct behavioral sub-requirement (Task tool declaration prohibition). This means the experiment cannot cleanly attribute C1's compliance performance on Task-tool scenarios to framing style versus content coverage. Until this is corrected, the experimental design has a confound at constraint 1. The 0.83 score reflects that two independent cross-condition asymmetries exist in a document that must have zero asymmetries to be experimentally valid.

---

## Session Context (Orchestrator Handoff)

```yaml
verdict: REVISE
composite_score: 0.897
threshold: 0.95
weakest_dimension: internal_consistency
weakest_score: 0.83
critical_findings_count: 0
iteration: 3
improvement_recommendations:
  - "D-008 (Priority 1): Add explicit Task tool prohibition to H-01 C1 — 'Ensure the Task tool is not included in a worker agent's allowed_tools configuration.' Also add Task tool reference to H-01 neutral. Update checklist H-01 semantic equivalence entry to show C1 now covers sub-requirements (1), (2), and (3)."
  - "D-009 (Priority 2): Add critic-passthrough prohibition to H-15 C1 ('Do not pass the deliverable to a critic until the self-review is complete.') and H-15 C3 <prohibition> ('NEVER pass a deliverable to a critic without first completing a self-review.'). Update H-15 C3 <verify> accordingly."
  - "Checklist methodology (Priority 3): Upgrade semantic equivalence check to read C2 first when enumerating sub-requirements, then verify each C2 sub-requirement in C1, C3, and neutral. A gap must be flagged, not implicitly accepted."
```

---

*Score Report Version: 1.0.0*
*Agent: adv-scorer*
*Strategy: S-014 (LLM-as-Judge)*
*SSOT: `.context/rules/quality-enforcement.md`*
*Workflow: ab-testing-20260301-001 / Adversary Gate Iteration 3*
*Scored: 2026-03-01*
