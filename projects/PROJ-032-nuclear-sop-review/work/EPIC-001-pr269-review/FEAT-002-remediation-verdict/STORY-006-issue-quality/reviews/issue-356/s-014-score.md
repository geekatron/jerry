# Quality Score Report: GitHub Issue #356 (PROJ-032/BUG-007 — nuclear-sop command gating)

## L0 Executive Summary
**Score:** 0.64/1.00 | **Verdict:** REJECTED | **Critical Block:** YES | **Weakest Dimensions:** Internal Consistency & Methodological Rigor (0.52 each)
**One-line assessment:** The opening paragraph misstates the defect's scope as spanning four artifact types, directly contradicting the issue's own design question two sentences later and conflating two separately-filed issues' scope into this one — fix that sentence first; everything else is a secondary tightening pass.

## Scoring Context
- **Deliverable:** `.../STORY-006-issue-quality/snapshots/final/issue-356.md` (GitHub issue #356 text)
- **Type:** Other (adversarial-tournament GitHub issue text) | **Criticality:** C4
- **Ground truth used:** remediation-register.md REM-07 (G1/G2/G3, redesign question), REM-03/REM-06 headers (scope disambiguation), `src/infrastructure/internal/enforcement/security_enforcement_engine.py` (verified exists), BUG-007 worktracker entity (verified exists), STORY-006's self-containedness mandate, evidence-c07033ce.md (branch name)
- **Strategy findings incorporated:** Yes — 9 blind strategies (~29 findings), used as corroborating evidence after independent verification
- **Scored:** 2026-08-07

## Score Summary

| Metric | Value |
|---|---|
| Weighted Composite | **0.64** |
| Bands | PASS >= 0.92 · REVISE 0.85-0.91 · REJECTED < 0.85 |
| Verdict | **REJECTED** |
| Validated Critical findings | 1 (blocks PASS regardless of composite) |

## Dimension Scores

| Dimension | Wt | Score | Weighted | Evidence |
|---|---|---|---|---|
| Completeness | .20 | 0.72 | 0.144 | Design question inline covers 2 of REM-07's 6 redesign elements (gating model, screening scope). Omits: neutralizing verbatim payload echo, surfacing H-05, narrowing sop-brief/sop-capture Bash grants, correcting PLAYBOOK's mitigation-hierarchy claim, and the available interim mitigation — all present in the linked register but not inline, against STORY-006's own "carry design question ... inline" acceptance criterion. |
| Internal Consistency | .20 | 0.52 | 0.104 | Opening paragraph: screening "covers only one of the several attacker-influenceable inputs (workflow definitions, state files, lessons-learned entries, hold-point logs)." Design question two sentences later: "all *definition-sourced* fields." These describe different, non-overlapping problem scopes in the same short document — a direct, scope-defining self-contradiction, not a stylistic nuance. |
| Methodological Rigor | .20 | 0.52 | 0.104 | Verified against REM-07 ground truth: the gap is unscreened fields *within* the workflow-definition file (Action, Target, Expected Result, Sign-off Criterion, Hold Reason, Sections 2/3/9 prose). State-file tamper protection is REM-03 (issue #352); OE/lessons-learned injection is REM-06 (issue #355) — confirmed via register headers; neither is a REM-07 member. The opening paragraph's 4-artifact framing is factually wrong vs. this ground truth. All other checkable facts are accurate: bypass examples (nc, `python -m http.server`, base64) match G1; verbatim log-echo claim matches G2; engine-duplication claim matches G3; severity "major" and DEFER-REWORK match the register header exactly. |
| Evidence Quality | .15 | 0.70 | 0.105 | Concrete, independently-checkable examples for the block-list weakness. But "a deterministic security enforcement engine this duplicates" names no engine — verified it resolves to `src/infrastructure/internal/enforcement/security_enforcement_engine.py`, which a reader cannot confirm or evaluate (the design question's 3rd option) without an out-of-band repo search. |
| Actionability | .15 | 0.72 | 0.108 | Design question names 3 concrete gating options (allow-list, category-based pause points, engine delegation) and is genuinely actionable at the structural level. But a contributor acting only on the visible text satisfies 2 of REM-07's 6 acceptance-criteria elements, risking a second review round-trip against criteria never shown in the issue body. |
| Traceability | .10 | 0.70 | 0.070 | Worktracker path (verified: `work/BUG-007-executor-command-gating/BUG-007-executor-command-gating.md` exists) carries no branch qualifier of its own; the "on branch `feat/proj-032-nuclear-sop-review`" clause grammatically attaches to the adjacent register-path sentence. Confirmed this path does not exist on the PR's own branch (evidence-c07033ce.md: PR branch is a different, separately-numbered project tree). Issue also cites the Worktracker directory, not the entity file. |
| **TOTAL** | **1.00** | | **0.635 → 0.64** | |

## Critical Finding (independently verified — blocks PASS)

**Scope-conflation in the opening paragraph.** "...covers only one of the several attacker-influenceable inputs (workflow definitions, state files, lessons-learned entries, hold-point logs) that end up driving tool calls" conflates REM-07's actual scope (fields *within* one workflow-definition document) with two separately-filed defects: state-file tamper protection (REM-03 / issue #352) and OE/lessons-learned corpus injection (REM-06 / issue #355). Directly contradicts the issue's own design question ("all definition-sourced fields"). Independently caught by 6 of 9 blind strategies (S-010-01, S-003-01, S-002-DA-001, S-004-01, S-007-02, S-011-01) and confirmed here against remediation-register.md REM-03/REM-06/REM-07. Risk: a contributor builds cross-document screening (wrong target) and/or duplicates #352/#355 with no cross-reference to disambiguate. Per scoring rules, a valid Critical finding blocks PASS regardless of composite.

## Required Edits (minimal set to reach PASS)

1. **[Critical]** Replace: "...likewise covers only one of the several attacker-influenceable inputs (workflow definitions, state files, lessons-learned entries, hold-point logs) that end up driving tool calls" → "...covers only WARNING/CAUTION-annotated text inside the workflow definition — other fields in that same document that equally drive tool calls (Action, Target, Expected Result, Sign-off Criterion, Hold Reason, and free-form prose in Sections 2/3/9) are unscreened. (State-file tampering and lessons-learned/OE injection are tracked separately as issues #352 and #355.)"
2. **[Major]** After "a deterministic security enforcement engine this duplicates" insert: "(`src/infrastructure/internal/enforcement/security_enforcement_engine.py`)".
3. **[Major]** Extend the design question: after "...drive tool calls?" add "Also required: neutralize verbatim payload echo into logs (hash/excerpt, not verbatim), surface H-05 (uv-only Python) in executor constraints, narrow sop-brief's and sop-capture's Bash grants to their actual read-only needs, and correct PLAYBOOK.md's claim that SEC-001/002 are 'the primary mitigations' (SR-06 human review is the actual primary control)."
4. **[Major]** In the Tracking line, cover both paths with one branch qualifier: "...(register section REM-07) — both this Worktracker path and the register below are on branch `feat/proj-032-nuclear-sop-review`, not this PR's branch."
5. **[Minor]** Point to the entity file, not the directory: append `/BUG-007-executor-command-gating.md` to the Worktracker path.
6. **[Minor]** Add: "(Available now, independent of the redesign: narrowing sop-brief's and sop-capture's Bash grants, since their declared needs are already covered by other tools.)"

## Leniency Bias Check
- [x] Each dimension scored independently against SSOT rubric text before composite computed
- [x] Every score traced to specific evidence (register text, file-existence checks, STORY-006 AC text) — none asserted on impression alone
- [x] Uncertain scores (Internal Consistency, Methodological Rigor) resolved to 0.52, the lower edge of the plausible band, not the midpoint
- [x] No dimension scored above 0.80; none approached 0.90+ territory requiring exceptional-evidence justification
- [x] The Critical finding was independently re-derived from remediation-register.md before being allowed to block PASS, rather than accepted solely on strategy-report say-so
