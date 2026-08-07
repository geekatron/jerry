# Quality Score Report: GitHub Issue #360 — nuclear-sop OE artifact contract (REVISED DRAFT round 4)

## L0 Executive Summary
**Score:** 0.92/1.00 | **Verdict:** PASS (marginal — 0.0025 above threshold before rounding) | **Weakest Dimension:** Actionability (0.91)
**One-line assessment:** All 3 round-3 required edits are verbatim-satisfied and independently re-verified against ground truth (including a brand-new, unrequested `#361` cross-reference that checked out correct); no new defects found; two residual precision nits remain but are optional polish, not blockers.

## Scoring Context
- **Deliverable:** `.../STORY-006-issue-quality/revised/issue-360.md` (round 4) | **Type:** Review-issue text | **Criticality:** C4
- **Ground truth used:** `remediation-register.md` REM-11 (+ REM-12 for the cross-reference check), `evidence-c07033ce.md` (full commit diff + CI), sibling snapshots `final/issue-357.md` through `final/issue-363.md` (BUG/REM/issue-number mapping), worktracker `BUG-011-oe-artifact-contract` (existence confirmed)
- **SSOT:** quality-enforcement.md (weights, H-13), s-014-llm-as-judge.md (rubric) | **Scored:** 2026-08-07 | **Iteration:** 4
- **Prior Score:** 0.90 (REVISE, R3) | **Improvement Delta:** +0.02

## Score Summary
| Metric | Value |
|---|---|
| Weighted Composite | **0.92** (precise: 0.9225) |
| Threshold (H-13) | 0.92 |
| Verdict | **PASS** (marginal) |
| Strategy Findings Incorporated | Yes (9 strategies across R1-R3, ~28 findings) — all now Stale or Addressed; zero new findings from independent re-verification |
| Critical Findings Valid Against This Draft? | No (same as R3 — the flawed self-verifying grep was removed in R3 and remains removed) |
| Unresolved Critical Findings? | None → no override to REVISE |

## Dimension Scores
| Dimension | Weight | Score | Weighted | Evidence Summary |
|---|---|---|---|---|
| Completeness | 0.20 | 0.92 | 0.184 | Both R3 gaps closed: "confirm three things" now names all 3 fix claims; sibling cross-link `(the other six: #357-#359, #361-#363)` added and independently verified exact. |
| Internal Consistency | 0.20 | 0.93 | 0.186 | Unchanged from R3 (not a target of this revision); "seven"/"six" arithmetic now additionally self-verifying via the explicit issue-number list; zero contradictions found. |
| Methodological Rigor | 0.20 | 0.93 | 0.186 | Every claim re-verified true against diff/register, including composition-twin mirrors (`sop-brief.prompt.md`, `sop-capture.prompt.md`/`.governance.yaml`) I explicitly located; the new `#361` claim is independently confirmed correct (BUG-012/REM-12). |
| Evidence Quality | 0.15 | 0.92 | 0.138 | R3's sole flagged gap ("no corroboration for seven fixes") now closed with a specific, verified-accurate citation (6 issue numbers). |
| Actionability | 0.15 | 0.91 | 0.1365 | Both R3 gaps closed (retrieval-protocol now in the confirm list; mis-attribution risk now caveated with `#361`); residual: "mirror copies" claim isn't independently checkable via the literal diff command given. |
| Traceability | 0.10 | 0.92 | 0.092 | Unchanged from R3 — commit hash, CI URL, register section, 5 named files all still trace cleanly; kept flat rather than double-crediting the `#361` fix already counted under Rigor/Actionability. |
| **TOTAL** | **1.00** | | **0.9225 -> 0.92** | |

## Verification of Round-3 Required Edits (independent re-check against round 4 text)

1. **"Confirm two things" -> "confirm three things," third clause names the `sop-brief.md` Step 4 retrieval-protocol check.** SATISFIED — current text reads: *"confirm three things: (1) the template, baseline, and worked example now use only `docs/experience/{entry_id}.yaml`; (2) `agents/sop-capture.md` adds a step appending the OE entry reference to the workflow definition's Attachments section; and (3) `agents/sop-brief.md` Step 4 now searches by `workflow_id` first (Glob, then filter), applying `workflow_type` only as a post-read filter, never the initial search key."* Clause (3) matches the diff verbatim in substance (`evidence-c07033ce.md` lines ~507-515: exact-match primary / keyword secondary / `workflow_type` post-read-filter-only).
2. **Extend the parenthetical to caveat the `sop-capture.md` mixed hunk.** SATISFIED AND EXCEEDED — current text: *"even this scoped diff's `sop-capture.md` hunk includes unrelated `execution_log_final` lines, tracked separately as #361."* R3 asked only for a generic caveat ("tracked separately"); the revision adds a specific issue number. I independently re-derived the BUG/REM/issue mapping across `snapshots/final/issue-357.md` through `issue-363.md`: BUG-008..014 = REM-08..14 = issues #357..#363 sequentially, confirming BUG-012/REM-12 (state machine/completion contract, which owns the `execution_log_final` semantics per the register's REM-12 fix spec item 2) = issue **#361**. The claim is factually correct, not just present.
3. **"one of seven mechanical fixes" -> add "(the other six: #357-#359, #361-#363)".** SATISFIED AND VERIFIED — cross-checked against all 7 FIX-NOW sibling snapshots (`final/issue-357.md` .. `final/issue-363.md`): all 7 are labeled "fixed on your branch" (REM-08..14), while the 7 DEFER-REWORK siblings (`final/issue-350.md` .. `issue-356.md`, REM-01..07) are labeled "Blocks merge" / "not maintainer-fixable" — confirming the "seven mechanical fixes" set is exactly {#357,#358,#359,#360,#361,#362,#363} and "the other six" enumeration is complete and correctly excludes the DEFER-REWORK issues.

**All 3 required edits: SATISFIED, with edit 2 exceeding the literal ask (added a specific, independently-verified-correct issue number rather than a bare caveat).**

## New-Defect Sweep (independent, not limited to the R3 required-edit list)
Full sentence-by-sentence re-verification of the round-4 text against `remediation-register.md` REM-11 and `evidence-c07033ce.md` found **no new factual errors**. Two non-blocking precision observations (neither rises to Minor-severity given low materiality):
- The "`.yaml` ... everywhere (template, baseline, example, both agents, **mirror copies**)" claim is accurate (composition-twin fixes independently confirmed in `sop-brief.prompt.md`, `sop-capture.prompt.md`, `sop-capture.governance.yaml`), but the literal `git diff` command given for verification does not include the composition files, so a reader cannot check that specific sub-claim from the instructions as written. Low materiality: composition files are documented elsewhere in this same commit as non-normative derived artifacts (`agents/` pair wins on conflict).
- "as three documents promised" (Attachments step) compresses the register's slightly different 3-document set (template/example/tutorial-Step-4) versus the 5-file list named earlier in the same paragraph (template/baseline/example/both agents) — not a factual error, just a minor cross-sentence referent ambiguity for a highly attentive reader.

Neither observation is a required edit; both are optional future polish.

## Improvement Recommendations (optional — not required for PASS)
| Priority | Dimension | Current | Optional Target | Suggestion |
|---|---|---|---|---|
| 1 | Actionability | 0.91 | 0.93+ | If ever revised again, extend the verify command or add a sixth confirm clause covering the composition-twin mirror files, so "mirror copies" is independently checkable rather than asserted. |
| 2 | Completeness | 0.92 | 0.93+ | Optionally disambiguate "as three documents promised" to name which three (template/example/tutorial), avoiding the referent overlap with the 5-file list two sentences earlier. |

**Implementation guidance:** Both items are cosmetic; do not hold the merge or re-open the revision cycle for these. They are recorded for completeness of the audit trail only.

## Leniency Bias Check
- [x] Each dimension scored independently before composite computed
- [x] Evidence cited per dimension from register/diff/sibling-snapshot cross-reference, not impression
- [x] Uncertain scores resolved downward at every dimension-level judgment call (e.g., Actionability held at 0.91 rather than 0.92-0.93; Traceability held flat at 0.92 rather than double-crediting the `#361` fix already counted under Rigor/Actionability; Completeness held at 0.92 rather than 0.93)
- [x] Composite (0.9225 -> 0.92) is a marginal pass, reported transparently as such rather than rounded-up narrative confidence
- [x] No dimension scored above 0.93; three specific evidence points documented per dimension above 0.90 (see Dimension Scores + Verification sections)
- [x] All 3 round-3 required edits independently re-verified against primary evidence (diff + 9-file sibling cross-reference), not rubber-stamped from the prior report's say-so
- [x] Consistency-with-prior-round instruction honored: dimensions not targeted by required edits (Internal Consistency, Traceability) were not re-litigated downward or upward without new evidence
