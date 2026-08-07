# Quality Score Report: GitHub Issue #358 (PROJ-032/BUG-009 — nuclear-sop registration gaps)

## L0 Executive Summary
**Score:** 0.79/1.00 | **Verdict:** REJECTED | **Weakest Dimension:** Completeness (0.72)
**One-line assessment:** Every explicit factual claim checked against ground truth is true, but the verify command and "what changed" prose are materially incomplete versus the register's own scope, several tracking references don't resolve cleanly, and ungloosed internal codenames survive despite the project's own documented "spell out or drop" policy for this exact audience.

## Scoring Context
- Deliverable: `.../STORY-006-issue-quality/snapshots/final/issue-358.md` | Type: review-issue text, zero-context external audience | Criticality: C4
- Ground truth used: remediation-register.md REM-09 (lines 216-235), evidence-c07033ce.md (full diff), pr269-verdict.md (disposition)
- Strategy findings incorporated: Yes — 9 blind strategies, ~42 raw findings, cross-checked against ground truth directly (not taken on faith)
- Critical-block check: No single Critical-severity (<=0.50) defect found; the REJECTED verdict is cumulative across dimensions

## Score Summary
| Metric | Value |
|---|---|
| Weighted Composite | 0.79 |
| Bands | PASS >=0.92 / REVISE 0.85-0.91 / REJECTED <0.85 |
| Verdict | **REJECTED** |
| Critical finding block | No |

## Dimension Scores
| Dimension | Wt | Score | Wtd | Evidence |
|---|---|---|---|---|
| Completeness | .20 | 0.72 | .144 | "What the fix changed" states only 3 of 5 confirmed REM-09/G3 AGENTS.md sub-edits (omits the refreshed "Last verified" date and the new sop-* MCP-exclusion sentence, both present in the diff); no link from "PR #269's disposition" to the already-decided REWORK verdict or its 7 open blockers (#350-#356, per pr269-verdict.md); title/body keep "PROJ-032/BUG-009", "REM-09", "compound trigger" ungloosed although pr269-verdict.md states this issue batch's own policy is to spell out or drop internal codenames for this audience |
| Internal Consistency | .20 | 0.88 | .176 | No contradictions found; one sentence supports two readings — "on branch feat/proj-032-nuclear-sop-review" in the Tracking line is ambiguous between qualifying only the register path or both the worktracker and register paths |
| Methodological Rigor (factual accuracy vs ground truth) | .20 | 0.80 | .160 | Every specific claim checked is TRUE: SHA, CI link, "seven fixes"=REM-08..14, 89->93 count, the "nuclear workflow" misroute mechanism, no-compound-trigger claim, phrase-beats-priority resolution. Confirmed gap: the prescribed verify diff covers 2 of the 3 files REM-09 actually touched — register's own "Affected files" line lists a third (the phase-6 collision-analysis artifact, `registration-trigger-map-row.md`, under the PR's own `PROJ-0039-nuclear-engineer` tree), which carries the "CORRECTED/SUPERSEDED" annotation directly refuting the collision-analysis claim this issue itself criticizes |
| Evidence Quality | .15 | 0.82 | .123 | Commit SHA, CI run, and register section are all cited with specificity and are verifiably accurate; CI link is clickable, but the SHA and the register path are bare identifiers requiring manual reconstruction, and the AGENTS.md evidence is partial (see Completeness) |
| Actionability | .15 | 0.76 | .114 | The "nothing to do" instruction is unambiguous and correct. The one optional action (verify) has real friction for the stated audience (an AI agent acting from text alone): incomplete file scope, `^` caret syntax not portable off bash/zsh, and no fetch/shallow-clone guidance. No channel is given for the "if you disagree" branch |
| Traceability | .10 | 0.74 | .074 | CI run link resolves cleanly. The worktracker Tracking reference is a directory, not the entity file — confirmed the actual file is `BUG-009-registration-enforcement-surfaces.md` inside it, so literal resolution fails before a human/agent finds the right artifact |
| **TOTAL** | **1.00** | | **0.79** | |

## Verdict Rationale
0.79 < 0.85 -> **REJECTED** per the task's 3-band scale. Five of six dimensions land in the Major band (0.51-0.84); only Internal Consistency reaches Minor (0.85-0.91). No dimension collapses to Critical (<=0.50), so `critical_block = No` — this is a cumulative-gap rejection, not a single fatal defect. Convergent validity is strong: 9 independent blind strategies produced overlapping evidence for the same ~6 defect clusters, each confirmed here against remediation-register.md / evidence-c07033ce.md directly: directory-not-file path (S-010-04, S-004-01, S-007-01); incomplete verify scope (S-011-01, S-012-01); incomplete AGENTS.md description (S-003-01, S-002-03, S-011-04, S-001-06); unlinked SHA/register (S-003-02, S-001-03); unresolved PR-disposition reference (S-002-01, S-001-02); ungloosed internal codes (S-001-01, S-011-02, S-012-04, S-013-04).

## Required Edits to Reach PASS (>=0.92)
1. Verify command: add the third REM-09 file — `registration-trigger-map-row.md` (phase-6 collision-analysis artifact, `PROJ-0039-nuclear-engineer/orchestration/nuclear-sop-build-20260325-001/eng/phase-6/eng-reviewer-001/`) — to `git diff c07033ce^ c07033ce -- ...`.
2. "What the fix changed": extend the AGENTS.md sentence to also name the refreshed "Last verified" date and the new sop-* sentence in the MCP "Not included (by design)" note.
3. Tracking line: append the filename — `.../BUG-009-registration-enforcement-surfaces/BUG-009-registration-enforcement-surfaces.md`.
4. Tracking line: rewrite so "on branch feat/proj-032-nuclear-sop-review" unambiguously covers both the worktracker path and the register path.
5. Hyperlink the commit at first mention: `[c07033ce](https://github.com/geekatron/jerry/commit/c07033ce159d9852744486aed0a54e9528b4668d)`.
6. Hyperlink `remediation-register.md` to a direct GitHub blob URL on `feat/proj-032-nuclear-sop-review` instead of a bare path+branch pair.
7. Add one sentence resolving "PR #269's disposition": already REWORK, gated on seven open design-decision issues (#350-#356), not on this issue.
8. Add a disagreement channel: "(comment here or on PR #269)".
9. Title: drop or parenthesize the bare "PROJ-032/BUG-009:" prefix per the verdict doc's own stated codename policy for this audience.
10. Gloss "compound trigger" and "REM-09" on first use with a short parenthetical each.
11. Note the six sibling FIX-NOW issues from the same commit (#357, #359-#363).
12. Verify command: add a portability note (shallow clone -> `git fetch --unshallow`; `^` is not portable to cmd/PowerShell — use `~1` or link to the GitHub commit view).

## Leniency Bias Check
- [x] Each dimension scored independently against primary-source evidence, not impression
- [x] Every score cross-checked directly against remediation-register.md / evidence-c07033ce.md / pr269-verdict.md, not taken solely from strategy claims
- [x] Uncertain scores (Methodological Rigor 0.80 vs 0.85, Completeness 0.72 vs 0.75) resolved to the lower value
- [x] No dimension scored >=0.90; none required the >0.90 three-evidence-point justification
- [x] Findings judged invalid or mitigated, excluded from scoring: S-013-01's "dead reference" risk (S-001-03 confirms the branch/file are live-fetched public); severity-omission cluster (S-002-04, S-007-03, S-012-03, S-012-05) weighted lightly since the register's own Rationale text also calls REM-09 "mechanical"
