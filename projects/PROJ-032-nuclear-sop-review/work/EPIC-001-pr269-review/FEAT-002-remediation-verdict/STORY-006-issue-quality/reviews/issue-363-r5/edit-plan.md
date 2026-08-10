# Issue #363 — R5 Reconciled Edit Plan (plateau root-cause + final edits)

> Quality-gap analysis after 4 scoring rounds (0.72 → 0.91 → 0.90 → 0.91 vs 0.92 gate, zero Critical since R2).
> Target text: `STORY-006-issue-quality/revised/issue-363.md` (22 lines; identical to `snapshots/published/issue-363.md` except title-line format). No HTML rejection comments exist in any text variant; the sole reviser rejection is implicit (R3 optional edit #5 skipped).

## Document Sections

| Section | Purpose |
|---------|---------|
| [Verdict](#verdict) | Why it plateaus, in one paragraph |
| [Persistent Dimension Deficits](#persistent-dimension-deficits) | Score trajectories and the rotating-nit pattern |
| [Inter-Round Contradictions](#inter-round-contradictions) | C1–C5 |
| [Rejected-Demand Verdicts](#rejected-demand-verdicts) | RJ-1/RJ-2 vs ground truth, with git evidence |
| [Final Edit List](#final-edit-list) | E0–E2, exact strings |
| [Word-Budget Ruling](#word-budget-ruling) | 450-word clause not triggered |
| [R5 Scoring Context](#r5-scoring-context) | What the next judge must treat as settled |

## Verdict

The text is factually clean; the plateau is judge-side. R4's sole residual finding (MR-01, line counts 250/76/559 "each 1 short") is **refuted by authoritative git evidence** («PR worktree» is a checkout at exactly `c07033ce`): `git show c07033ce^:<file> | wc -l` = **250 / 76 / 559**, all three pre- and post-fix blobs end with a trailing newline (killing R4's `wc -l`-undercount hypothesis), and numstat (+16/0, +9/0, +19/−2) reconciles those pre-fix counts with wc-verified post-fix totals **266/85/576**. R4's "direct read" post-fix totals (267/86/577) were each a +1 phantom-line miscount, so its reconstructed 251/77/560 are all wrong. R4 states IC and EQ (both 0.91, zero named defects) "are expected to clear 0.92 once Priority 1 removes the deliverable's last confirmed factual imprecision" — and that imprecision does not exist. With MR-01 struck, **no confirmed defect remains**; two micro-hardening edits below close the only residual attack surfaces.

## Persistent Dimension Deficits

| Dimension | R1 | R2 | R3 | R4 | Persistent driver |
|---|---|---|---|---|---|
| Methodological Rigor | 0.60 | 0.94 | 0.89 | 0.91 | Only dimension with a NEW finding each round: every-run claim (real, fixed R2) → #358 range (real, fixed R4) → line counts (R4, **invalid**). Rotating single-nit pattern = the plateau engine. |
| Internal Consistency | 0.73 | 0.93 | 0.91 | 0.91 | R3/R4 hold 0.91 with **no named defect**; R4 pins it to MR-01. |
| Evidence Quality | 0.68 | 0.89 | 0.90 | 0.91 | Residual diff noise in 4/6 shared files (property of the commit, not editable) + "23/25" not independently re-derived (R4: ambiguity, not contradiction). |
| Completeness | 0.78 | 0.91 | 0.90 | **0.92** | Cleared; no outstanding deficit. |
| Actionability | 0.75 | 0.91 | 0.91 | **0.92** | Cleared. |
| Traceability | 0.80 | 0.83 | 0.90 | **0.92** | Cleared (gloss + hyperlink edits, R3). |

All 15 required edits across R1–R3 were verifiably applied (R2 and R4 confirm). Post-R3 the text had exactly one real defect (#358 range), fixed in R4; R4 then manufactured MR-01 via its own measurement error.

## Inter-Round Contradictions

| ID | Contradiction |
|---|---|
| C1 | R2 credited MR 0.94 **because** 250/76/559 match the register verbatim ("3 exact line-count matches" cited as pro-score evidence); R4 docked MR **because** the same numbers allegedly mismatch its reconstruction. R4's side is factually wrong (see RJ-2). |
| C2 | H-23 churn: R1 required replacing "agents consume at runtime" with "every markdown file over 30 lines"; R3 then billed the missing "Claude-consumed" qualifier — an imprecision R1's own replacement text introduced — as a new deficit. |
| C3 | R1 offered exact-6-path pathspec **or** a disclosure note as alternatives; the reviser did both; R2 still docked EQ for residual noise in 4/6 shared files — un-editable commit property retained as a standing deduction thereafter. |
| C4 | R4 holds IC/EQ at 0.91 while stating no gap was found in either — dimensions pinned to another dimension's (invalid) finding, contradicting independent-dimension scoring. |
| C5 | R3 classed the 559 re-check as Optional; R4 re-classed the identical item as Priority-1 required (MR-01) — then got the facts wrong. |

## Rejected-Demand Verdicts

| ID | Demand | Reviser action | Verdict vs ground truth |
|---|---|---|---|
| RJ-1 | R3 edit #5 (Optional): re-verify `c3-adr-workflow-definition.md` pre-fix count; correct 559→560 if changed | Skipped (kept 559) | **Rejection RIGHT.** `git show c07033ce^:skills/nuclear-sop/examples/c3-adr-workflow-definition.md \| wc -l` = 559. |
| RJ-2 | R4 Priority-1 (MR-01): change 250→251, 76→77, 559→560, or soften all three to "~" | Not yet acted on — ruled here | **REJECTED — factually wrong on all three.** Pre-fix blobs at `c07033ce^` = 250/76/559 exactly; every blob ends `\n` (undercount hypothesis refuted); numstat +16/0, +9/0, +19/−2 gives post-fix 266/85/576, matching direct `wc -l` of the «PR worktree» files. Register REM-14 G1 and issue text are both exact. No correction, no hedging. |

No other rejections exist: R1's 5, R2's 5, and R3's 4 required edits are all present in the current text (independently re-confirmed during this analysis).

## Final Edit List

Minimal set. E0 is a ruled no-change; E1–E2 are the only text changes.

| ID | Action | Rationale |
|---|---|---|
| E0 | **NO CHANGE** to "250 lines", "76 lines", "559 lines" | RJ-2. Numbers verified exact against `c07033ce^` blobs and register REM-14 G1. |
| E1 | Line 7: replace "over 30 lines to open with a navigation table" with "over 30 lines to include a navigation table" | H-23 verbatim is "MUST **include** a navigation table"; placement is NAV-002 (MEDIUM, SHOULD). "requires…to open with" overstates a MEDIUM as HARD — same deficit family as the confirmed R1/R3 paraphrase findings; last remaining rule-paraphrase imprecision. Net −1 word. |
| E2 | Line 16: delete "and 3 of the skill's own 5 templates" (sentence becomes "…matching 23 of the repo's 25 canonical templates (the `.context/templates/` corpus); the missing rows…") | Robustness trim of the one remaining independently-falsifiable figure: direct pre-fix measurement finds **2** format-bearing skill templates (`PRE_JOB_BRIEF`, `POST_JOB_BRIEF`); "3 of 5" holds only under a compliant-includes-YAML-exempt reading. Register-internal figure stays in the register; the issue simply stops repeating it. The 23/25 clause is retained — numerator 23 independently confirmed (23 nav-table-bearing files under `.context/templates/`); denominator is register-definitional (R4: ambiguity, not contradiction). Net −8 words. |

Everything else stays: title, bullets, Step-0 phrasing, "flagship example" (unchallenged ×4 rounds), sibling-issue note (#357, #359–#362; #358 exclusion re-confirmed against remediation-log FIX-NOW trace), CI/commit links, Tracking footer.

## Word-Budget Ruling

Completeness scored **0.92 in R4 with no outstanding deficit → completeness is NOT the binding dimension → the 450-word growth clause is NOT triggered.** Binding dimensions (MR/IC/EQ) are precision-type and favor zero growth. Current body = **282 words** (title and 67-word Tracking footer excluded). Ruled cap: **282** (hold at current). Post-edit projection: **273** (E1 −1, E2 −8).

## R5 Scoring Context

The next judge MUST treat as settled (do not re-litigate): (1) pre-fix line counts 250/76/559 — verified against `c07033ce^` git blobs, this document; (2) #358 exclusion and #357/#359–#362 attribution — remediation-log FIX-NOW trace; (3) Step-0-only template loading — sop-brief diff; (4) REM-01..07 = #350–#356 merge blockers. Dimensions must be scored independently (C4): a dimension with zero named defects cannot be held below 0.92 by reference to another dimension's finding.
