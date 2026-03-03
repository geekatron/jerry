# Quality Score Report: Three-Style Rewrites — PROJ-014 A/B Testing

## L0 Executive Summary

**Score:** 0.856/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Internal Consistency (0.82)
**One-line assessment:** The deliverable is structurally sound with 30 rewrites and 10 neutral descriptions all present, but three confirmed defects — H-07 C3 missing sub-rule (b) from its prohibition tag, H-22 semantic narrowing in C2, and passive negation in H-07 neutral — block acceptance at the C4 threshold of 0.95 and require targeted revision before experiment assembly.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-014-negative-prompting-research/orchestration/ab-testing-20260301-001/phase-0-design/three-style-rewrites.md`
- **Document ID:** PROJ-014-AB-PHASE0-02
- **Deliverable Type:** Experimental design artifact (three-style rewrites + neutral descriptions for A/B testing)
- **Criticality Level:** C4
- **Quality Threshold:** 0.95 (C4 elevated threshold per scoring request)
- **Standard Threshold:** 0.92 (H-13)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Iteration:** 1 (first scoring)
- **Scored:** 2026-03-01

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.856 |
| **Threshold (C4 elevated)** | 0.95 |
| **Standard Threshold (H-13)** | 0.92 |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No — standalone S-014 scoring |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.87 | 0.174 | All 30 rewrites and 10 neutrals present; H-07 C3 prohibition omits sub-rule (b) |
| Internal Consistency | 0.20 | 0.82 | 0.164 | C1 purity confirmed; H-07 C3 vs C2 completeness inconsistency; H-22 C2 semantic narrowing |
| Methodological Rigor | 0.20 | 0.85 | 0.170 | Source-verified; framing purity documented; "NEVER X without Y" pattern borderline in C2 |
| Evidence Quality | 0.15 | 0.87 | 0.131 | C3 consequences trace to source; H-07 C3 missing sub-rule b is an accuracy gap |
| Actionability | 0.15 | 0.83 | 0.125 | Mostly prompt-ready; H-07 C3 and H-22 C2 require targeted revision before assembly |
| Traceability | 0.10 | 0.92 | 0.092 | Full document ID, workflow, parent task, constraint IDs, source citations present |
| **TOTAL** | **1.00** | | **0.856** | |

---

## Detailed Dimension Analysis

### Completeness (0.87/1.00)

**Evidence:**
All structural requirements are met at the macro level. The document contains exactly 30 rewrites (10 constraints × 3 conditions) organized by constraint section. All 10 neutral descriptions are present in both inline form (within each constraint section) and in the consolidated table. The navigation table lists four sections with anchor links (H-23 compliant). The validation checklist is present and covers all six required verification categories. The S-010 self-review is documented with corrections noted.

**Gaps:**
1. **H-07 C3 prohibition tag incomplete.** Source rule H-07 has three sub-rules: (a) `src/domain/` MUST NOT import from application/infrastructure/interface/, (b) `src/application/` MUST NOT import from infrastructure/interface/, (c) only bootstrap.py instantiates infrastructure adapters. The C3 `<prohibition>` tag covers sub-rules (a) and (c) but omits sub-rule (b): "NEVER import from infrastructure/ or interface/ inside src/application/." The C2 rewrite correctly includes all three sub-rules as three explicit NEVER clauses. This omission means the C3 version of H-07 is substantively incomplete compared to the source rule and compared to the C2 version of the same constraint.
2. Self-review notes acknowledge the H-07 C3 composition but do not flag the sub-rule (b) omission — indicating the self-review did not catch this gap.

**Improvement Path:**
Add "NEVER import from infrastructure/ or interface/ within src/application/." to the H-07 C3 `<prohibition>` tag. This is a targeted, localized fix requiring one sentence addition.

---

### Internal Consistency (0.82/1.00)

**Evidence of Passing Checks:**
- C1 purity confirmed: Full grep across all C1 rewrite blocks for "NEVER", "never", "don't", "must not", "forbidden", "shall not", "do not", "prohibit" found zero matches in any C1 text block. All 10 C1 rewrites are prohibition-free.
- C3 completeness confirmed: All 10 C3 rewrites contain all four XML tags (`<prohibition>`, `<consequence>`, `<instead>`, `<verify>`). Tags are properly formed and closed.
- No condition labels ("C1:", "C2:", "C3:", "positive:", "blunt:") found in any rewrite text body.
- Neutral descriptions confirmed free of XML tags and imperative commands directed at the reader.

**Gaps / Inconsistencies:**

**Defect 1 — H-07 C2/C3 semantic completeness asymmetry (Significant):**
The C2 rewrite for H-07 contains three explicit NEVER clauses covering all three source sub-rules. The C3 prohibition tag covers only two of the three sub-rules. This creates an experimentally problematic inconsistency: C2 and C3 are supposed to encode the same behavioral requirement in different framing styles, but they actually encode different subsets of the rule. If a participant rates the C2 and C3 versions of H-07, they are evaluating prompts with different semantic coverage, not different framing of the same content.

**Defect 2 — H-22 C2 semantic narrowing (Moderate):**
H-22 in source covers a broad set of skills: `/problem-solving`, `/nasa-se`, `/orchestration`, `/transcript`, `/adversary`, `/ast`, `/eng-team`, `/red-team`. The C1 rewrite covers four skills explicitly (problem-solving, orchestration, nasa-se) and correctly captures the proactive invocation principle. The neutral description similarly covers four skills. However, the C2 rewrite narrows to prohibit only: "NEVER begin a research or analysis task without first invoking `/problem-solving`." This covers only one of the eight skill mappings. The C3 `<prohibition>` also narrows to `/problem-solving` and delay prohibition only. While narrowing may be intentional for experimental tractability, it creates semantic asymmetry: C1/neutral are broader than C2/C3. A rater comparing C1 (covering four skills) with C2 (covering one skill) is not evaluating the same constraint in different framings.

**Borderline — C2 "NEVER X without Y" construction (Minor):**
Four C2 rewrites use the grammatical form "NEVER do X without Y":
- H-02 C2: "NEVER substitute a different action... without obtaining explicit user approval first"
- H-31 C2: "NEVER proceed on a request... without first asking a clarifying question"
- H-22 C2: "NEVER begin a research or analysis task without first invoking /problem-solving"
- H-15 C2: "NEVER present a deliverable... without first completing a self-review pass"

The NPT-014 format is defined as "ONLY 'NEVER X' bare prohibition, NO consequences, NO alternatives." The "without Y" clause could be argued to implicitly encode an alternative ("do Y instead"). However, these clauses are grammatically part of the prohibition statement itself (they complete the scope of what is prohibited), not separate elaboration. The document's self-review notes explicitly evaluated this for H-07 C2 (three clauses) but not for the "without Y" pattern across other C2s. This is a borderline finding — not a clear defect but a purity concern that should be evaluated against the NPT-014 definition used in the experiment design.

**Improvement Path:**
Fix Defect 1 (H-07 C3 prohibition). Evaluate Defect 2 (H-22 scope): either narrow C1 and neutral to match C2/C3's `/problem-solving`-only focus, or broaden C2 and C3 to cover the same skills as C1/neutral. Evaluate the "without Y" pattern against the NPT-014 definition to determine whether it constitutes implicit alternative encoding.

---

### Methodological Rigor (0.85/1.00)

**Evidence:**
The methodology is sound and well-documented. Each constraint was composed after direct source-file verification, and source citations are specific (file + section + line references). The self-review notes document three corrections made during composition, demonstrating genuine iterative quality improvement. The constraint selection follows the specification: one constraint per HARD rule, spanning architectural, quality, workflow, and environment domains. The framing purity requirements were correctly understood and applied in 9 of 10 constraints for C1, in 10 of 10 for C3 tag completeness, and approximately 10 of 10 for C2 (with the "without Y" borderline concern noted).

**Gaps:**
1. The self-review explicitly evaluated H-07 C2 (three NEVER clauses) as conforming to NPT-014 format, but did not identify the H-07 C3 omission of sub-rule (b). The self-review methodology was not applied rigorously enough to catch cross-condition asymmetries.
2. The semantic equivalence check in the validation checklist (lines 440-449) performed a high-level pass ("all three encode [summary]") rather than a systematic cross-condition comparison verifying that the behavioral requirement is identically scoped across C1, C2, C3, and neutral. The H-22 narrowing and H-07 asymmetry would have been caught by a rigorous cross-condition scope comparison.
3. The "NEVER X without Y" pattern was not explicitly flagged against the NPT-014 definition for four C2 rewrites.

**Improvement Path:**
Add a cross-condition semantic scope check to the self-review methodology: for each constraint, verify that the behavioral requirement covered in C2 (expressed as prohibitions) is exactly co-extensive with what is expressed in C1 (expressed as positive instructions) and the neutral description. Any narrowing or broadening in one condition relative to another should be a flagged defect.

---

### Evidence Quality (0.87/1.00)

**Evidence:**
C3 consequence fields are directly sourced from documented rule consequences rather than invented. Verified spot-checks:
- H-05 C3 consequence: "environment corruption and CI build failures" — matches source `python-environment.md`: "Command fails. Environment corruption." and "NEVER use system Python -- doing so causes environment corruption and CI build failures." Accurate.
- H-07 C3 consequence: "Architecture tests fail and CI blocks the merge" — matches source `architecture-standards.md` H-07 consequence: "Architecture test fails. CI blocks merge." Accurate.
- H-01 C3 consequence: "Unbounded recursion exhausts the context window, violates P-003, and breaks the orchestrator's coordination authority" — matches `agent-development-standards.md` Pattern 2: "unbounded recursion exhausts the context window, violates P-003, and breaks the orchestrator's coordination authority." Accurately quoted.
- T1-T5 C3: Consequence "increases the attack surface, violates the principle of least privilege" — consistent with `agent-development-standards.md` Tier Constraints section. Accurate.

Source verification references in the checklist are specific and correctly attributed.

**Gaps:**
1. H-07 C3 `<prohibition>` tag omits sub-rule (b), making the C3 version evidentially incomplete relative to the source rule. The evidence used is accurate as far as it goes, but it is selective in a way that creates an accuracy gap.
2. H-22 C3 `<consequence>` ("Skill context is not loaded, the agent operates without the framework's methodology, work quality degrades, and rework is required") — accurately traces to `mandatory-skill-usage.md` H-22 consequence: "Work quality degradation. Rework required." The C3 expands this accurately. No evidence accuracy gap here.

**Improvement Path:**
Ensure the H-07 C3 prohibition accurately represents all three sub-rules as documented in the source. The consequence and instead/verify tags are already accurate; only the prohibition element requires correction.

---

### Actionability (0.83/1.00)

**Evidence:**
The document is well-structured for downstream prompt assembly. Rewrites are clearly delineated by constraint with horizontal rules. The three conditions per constraint are labeled with their condition name (C1, C2, C3) for assembly-time identification. The neutral descriptions table provides a consolidated view for scorer orientation. The XML formatting in C3 rewrites is syntactically consistent and machine-parseable. Self-review corrections are documented, demonstrating that the artifact was refined before delivery.

**Gaps:**
1. **H-07 C3 gap blocks direct use.** Any assembler using H-07 C3 as-is would be injecting an incomplete version of the rule into the experimental prompt. This requires a revision before the constraint can be used. The artifact is not safely drop-in ready.
2. **H-22 scope asymmetry requires design decision.** Before the H-22 constraint can be assembled into experiments, the team must decide whether to use the narrow (one-skill) or broad (four-skill) interpretation and align all four framings accordingly. This is a design decision the artifact leaves open.
3. The "NEVER X without Y" C2 pattern may be acceptable or may require revision depending on the NPT-014 operational definition. Until this is resolved, four C2 rewrites are conditionally non-actionable.

**Improvement Path:**
Fix the H-07 C3 gap and resolve the H-22 scope decision. These are targeted fixes that can be completed in one revision pass. Once fixed, the artifact is fully ready for prompt assembly.

---

### Traceability (0.92/1.00)

**Evidence:**
The document provides comprehensive traceability at all levels:
- **Document level:** Document ID (PROJ-014-AB-PHASE0-02), phase (0 / Step 0.2), workflow (ab-testing-20260301-001), parent task (TASK-025), date (2026-03-01), author (ps-analyst / design-agent-002).
- **Constraint level:** Each constraint is labeled with its rule ID (H-01, H-02, H-05, H-07, H-13, H-10, H-31, H-22, T1-T5/AD-T1, H-15).
- **Source level:** Validation checklist provides source file + section + approximate line references for all 10 constraints.
- **Companion artifact:** Reference to PROJ-014-AB-PHASE0-01 (constraint-selection) for companion source documentation.
- **Workflow integration:** Footer specifies next step (C4 Adversary Gate 1) and source verification methodology.

**Gaps:**
The source verification for H-07 cites "architecture-standards.md (HARD Rules table, line 34)" which is accurate. However, the H-07 C3 omission of sub-rule (b) is not traceable to a documented decision — it appears to be an accidental omission rather than a deliberate design choice. There is no note in the self-review or validation checklist explaining why C3 covers only two of the three H-07 sub-rules. This traceability gap makes the omission harder to evaluate as intentional vs. accidental.

**Improvement Path:**
Either fix the H-07 C3 omission (making it a non-issue) or document explicitly why sub-rule (b) is excluded from C3 if exclusion is intentional.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Issue | Target | Recommendation |
|----------|-----------|-------|--------|----------------|
| 1 | Internal Consistency | H-07 C3 prohibition omits sub-rule (b) | 0.92 | Add "NEVER import from infrastructure/ or interface/ within src/application/." to the H-07 C3 `<prohibition>` tag. Direct localized fix, one sentence. |
| 2 | Internal Consistency | H-22 scope asymmetry (C1/neutral cover 4 skills; C2/C3 cover 1) | 0.90 | Design decision required: either (a) narrow C1 and neutral to match C2/C3's `/problem-solving`-only focus, or (b) broaden C2 and C3 to enumerate the same skills as C1/neutral. Option (a) is more consistent with NPT-014's simplicity preference. |
| 3 | Methodological Rigor | "NEVER X without Y" pattern in 4 C2 rewrites — implicit alternative encoding concern | 0.88 | Define operationally whether "without Y" clauses violate NPT-014 purity. If they do: revise H-02, H-31, H-22, H-15 C2 rewrites to bare "NEVER X" form, moving the "Y" condition into the C3 `<instead>` tag where it belongs. |
| 4 | Internal Consistency | H-07 neutral: "application code does not import from infrastructure" contains passive negation | 0.86 | Rephrase to purely factual: "Application code is restricted to imports from the domain layer; infrastructure adapters are wired exclusively at bootstrap.py." Removes "does not" passive negation. |
| 5 | Methodological Rigor | Cross-condition semantic scope check missing from self-review | 0.85 | Add a cross-condition check to future self-reviews: for each constraint, verify that the behavioral scope encoded in C2 (prohibitions) is exactly co-extensive with C1 (positive framing) and neutral (factual description). |

---

## Detailed Defect Register

| Defect ID | Severity | Location | Description | Experiment Impact |
|-----------|----------|----------|-------------|-------------------|
| D-001 | Critical | H-07 C3 `<prohibition>` | Sub-rule (b) — "src/application/ MUST NOT import from infrastructure/interface/" — absent. C2 covers it; C3 does not. | Semantic asymmetry between C2 and C3 invalidates H-07 as a between-condition comparison pair. |
| D-002 | Significant | H-22 C2 and C3 | Scope narrowed to `/problem-solving` only; C1 and neutral cover 4 skills. | H-22 between-condition comparisons evaluate different semantic coverage, not just different framing styles. |
| D-003 | Borderline | H-02, H-31, H-22, H-15 C2 | "NEVER X without Y" construction may encode implicit alternative (Y = the correct behavior). | If NPT-014 definition excludes implicit alternatives, four C2 rewrites are contaminated. Requires NPT-014 operational definition ruling. |
| D-004 | Minor | H-07 neutral description | "does not import from infrastructure" contains passive negation language. | May introduce subtle framing bias in scorer orientation; low experiment impact given passive voice. |

---

## Leniency Bias Check

- [x] Each dimension scored independently
- [x] Evidence documented for each score with specific line/section references
- [x] Uncertain scores resolved downward (Internal Consistency uncertain at 0.82 vs 0.85 — resolved to 0.82; Actionability uncertain at 0.83 vs 0.87 — resolved to 0.83)
- [x] C4 calibration considered: at C4 with threshold 0.95, defects carry higher weight; D-001 (semantic asymmetry) is experiment-invalidating for H-07 cross-condition comparisons
- [x] No dimension scored above 0.92 without exceptional evidence (Traceability at 0.92: justified by specific document-level, constraint-level, source-level, and workflow-level traceability evidence)
- [x] First-scoring calibration: score of 0.856 is consistent with a first-draft artifact with genuine structural integrity but real defects requiring revision — appropriate for this artifact quality level

---

## Handoff Schema

```yaml
verdict: REVISE
composite_score: 0.856
threshold: 0.95
weakest_dimension: internal_consistency
weakest_score: 0.82
critical_findings_count: 2
iteration: 1
improvement_recommendations:
  - "Fix H-07 C3 prohibition: add sub-rule (b) — NEVER import from infrastructure/ or interface/ within src/application/"
  - "Resolve H-22 scope decision: align all four framings to same skill coverage (narrow or broad)"
  - "Rule on NPT-014 'without Y' pattern: if implicit alternative, revise 4 C2 rewrites to bare NEVER form"
  - "Fix H-07 neutral passive negation: rephrase 'does not import' to factual restriction statement"
```

---

*Scored by: adv-scorer*
*Strategy: S-014 LLM-as-Judge with 6-dimension weighted composite*
*Workflow: ab-testing-20260301-001 / Adversary Gate 2 (three-style-rewrites)*
*Deliverable iteration: 1*
*Date: 2026-03-01*
