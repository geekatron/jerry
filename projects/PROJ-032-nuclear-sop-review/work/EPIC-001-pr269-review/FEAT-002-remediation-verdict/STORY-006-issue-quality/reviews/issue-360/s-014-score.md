# Quality Score Report: GitHub Issue #360 (PROJ-032/BUG-011 — nuclear-sop OE artifact contract)

## L0 Executive Summary
**Score:** 0.75/1.00 | **Verdict:** REJECTED | **Weakest Dimension:** Methodological Rigor (0.62)
**One-line assessment:** The narrative (what was wrong / what changed) is precise and verified accurate against the remediation register and commit diff, but the issue's sole self-verification command (`grep -rn "experience/.*\.md" skills/nuclear-sop/`) is a Critical, three-way-corroborated factual defect — it does not return "nothing" against the real post-fix worktree — and the paired `git diff` command is materially over-broad (Major, three-way-corroborated). An autonomous agent reader following "How to verify" literally gets misled.

## Scoring Context
- **Deliverable:** `projects/PROJ-032-nuclear-sop-review/work/EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-006-issue-quality/snapshots/final/issue-360.md`
- **Type:** Other (GitHub issue text) | **Criticality:** C4 (tournament) | **Strategy:** S-014
- **Ground truth used:** remediation-register.md REM-11 (G1/G2/G3, fix spec items 1-7), evidence-c07033ce.md (full commit diff + CI header)
- **Strategy findings incorporated:** 9 blind strategies, 27 findings (3 Critical — same defect; 4 Major; 20 Minor)

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|---|---|---|---|---|
| Completeness | 0.20 | 0.83 | 0.166 | All 5 narrative elements present, map 1:1 to REM-11 G1/G2/G3; verify-grep checks only a subset of REM-11's own validation pattern |
| Internal Consistency | 0.20 | 0.88 | 0.176 | No hard contradictions; "both agents" phrasing overstates sop-capture's role in the retrieval-protocol fix |
| Methodological Rigor | 0.20 | 0.62 | 0.124 | ~9/11 factual claims verified accurate (several near-verbatim vs. diff); the one claim built for literal execution fails on execution (3x corroborated Critical) |
| Evidence Quality | 0.15 | 0.75 | 0.1125 | Commit hash + CI URL exact-match verified; descriptive claims precisely cite files; offered verification evidence itself unreliable |
| Actionability | 0.15 | 0.65 | 0.0975 | "Nothing to do" default remains clear; the offered confirmation action misleads if executed literally |
| Traceability | 0.10 | 0.75 | 0.075 | Register section/commit/CI all resolve; diff scoped to 29 files vs. ~5 relevant; internal shorthand unglossed for a zero-context reader |
| **TOTAL** | **1.00** | | **0.75** | |

## Per-Dimension Justification

**Completeness (0.83):** What/why/what-changed/verify/tracking all present. "What was wrong" accurately bundles all three REM-11 defect groups (extension mismatch, 3-way retrieval-protocol drift, unwritten Attachments promise). Gap: the verify-grep (`experience/.*\.md`) is a proper subset of the register's own validation command (`experience/.*\.md\|oe-entry-.*\.md`, REM-11 fix item 7) — independently flagged by 6 findings (S-010-01, PM-001-20260807, S-001-02, S-007-02, S-011-01, S-012-03). No cross-link to the other 6 sibling issues (S-013-03, Minor).

**Internal Consistency (0.88):** No direct contradictions between sections. One precision slip (S-001-05): "the workflow-ID-primary search protocol are now the single convention everywhere ... both agents" implies sop-capture carried the retrieval-protocol defect; per the register's fix item 5, only sop-brief performs OE retrieval and needed that specific fix (sop-capture already used `.yaml` pre-fix).

**Methodological Rigor (0.62, factual accuracy vs. ground truth):** Verified accurate against the register/diff: "seven mechanical fixes" (REM-08..14, all FIX-NOW, confirmed), extension mismatch + literally-unsatisfiable AC-7 (G1, confirmed via diff line for AC-7), three-way retrieval-protocol drift (G2, confirmed), unimplemented Attachments promise plus the new sop-capture "Section 11 attachment" step (G3, confirmed near-verbatim against the diff hunk), "CI 15/15 green" and run URL (exact match to the evidence pack header). Critical defect: three independent blind strategies (S-003-01, S-002-01, S-013-01) each report reproducing the issue's exact verify-grep against the real post-fix worktree and getting 2 non-empty hits (`examples/c3-adr-workflow-definition.md`, `agents/sop-capture.md`) rather than the claimed "nothing," attributing it to the same mechanism (unanchored `.*` crossing to an unrelated `.md` filename later on the same line). Judged VALID: three independently-run strategies converging on identical file:line pairs and an identical causal mechanism is not a plausible coincidence of hallucination. Major, independently corroborated 3x (S-001-01, S-007-01, S-011-02): the paired `git diff c07033ce^ c07033ce -- skills/nuclear-sop/` command reproduces all 7 bundled FIX-NOW clusters across 29 files (confirmed by the evidence-pack commit stat), not just the ~5 files this issue describes.

**Evidence Quality (0.75):** Commit hash and CI evidence are precise and verified exact against the evidence pack. Descriptive claims name specific files (post-job template, one behavioral baseline, the worked example, sop-capture.md) rather than vague references. However, the concrete evidence-gathering mechanism offered to the reader (the verify section) is unreliable for the reasons above, which undercuts confidence in the overall evidentiary chain.

**Actionability (0.65):** "Nothing for you to do unless you disagree with the fix" is clear and, per the register, correct. But the one action the issue explicitly invites ("How to verify") produces a false-negative signal (grep) and an unnecessarily noisy result requiring manual filtering (diff), which could cause an autonomous agent to wrongly conclude the fix is incomplete or fail to self-verify at all.

**Traceability (0.75):** Register section (REM-11), worktracker path, and commit hash all resolve to real artifacts (independently confirmed by multiple strategies). Weaknesses: diff-scope imprecision (above); unglossed internal shorthand ("BUG-011", "worktracker") for a reader with zero repo-governance context (S-001-03, S-007-03, S-011-03, S-012-02); the Tracking footer's only pointer is a path on the maintainer's internal review branch with no note on external accessibility (S-012-01, Major).

## Critical Findings Assessed
| ID(s) | Verdict | Rationale |
|---|---|---|
| S-003-01, S-002-01, S-013-01 (same defect) | VALID — blocks PASS regardless of composite | 3 independently-run blind strategies report identical file:line reproductions and an identical causal mechanism against the real worktree; convergence at this specificity is not plausible hallucination |

## Required Edits to Reach PASS
1. Replace the verify-grep with a check immune to cross-line/cross-cell false positives and covering both OE path forms — e.g., state the criterion in plain language: "confirm `docs/experience/{entry_id}.yaml` is the only extension used for OE entries across the template, baseline, and worked example" — rather than a fragile single-line regex.
2. Scope the verify-diff to the files this fix actually touched (`templates/POST_JOB_BRIEF.template.md`, `behavioral-baselines/bb-003-oe-feedback-loop-integrity.md`, `examples/c3-adr-workflow-definition.md`, `agents/sop-brief.md`, `agents/sop-capture.md`), or add one sentence noting the commit bundles six other unrelated fixes.
3. Reword "the workflow-ID-primary search protocol are now the single convention everywhere ... both agents" to attribute the retrieval-protocol fix specifically to sop-brief (the only agent that performs OE retrieval).
4. Drop the redundant trailing ", on your branch" from the "What was wrong" sentence (already established two sentences earlier).
5. Add a brief (3-5 word) gloss at first use of "BUG-011" and "worktracker" for a reader with zero repo-governance context.
6. Add one caveat sentence to the Tracking footer noting the linked branch is the maintainer's internal record and is not required reading in order to act.

## Leniency Bias Check
- [x] Each dimension scored independently against SSOT criteria before composite computed
- [x] Evidence cited per dimension (register sections, diff hunks, named convergent strategy findings)
- [x] Uncertain scores resolved downward (Methodological Rigor set to 0.62 not 0.65-0.70; Actionability set to 0.65 not 0.70)
- [x] Deliverable is a "final" tournament snapshot, not a first draft — full rigor applied, no first-draft leniency
- [x] No dimension scored above 0.90; no exceptional-evidence claim required
- [x] 3 lowest dimensions (Methodological Rigor, Actionability, Evidence Quality) each backed by specific, named, multiply-corroborated evidence, not impression
