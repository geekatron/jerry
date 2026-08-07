# Quality Score Report: GitHub Issue #362 (BUG-013 composition drift)

## L0 Executive Summary
**Score:** 0.68/1.00 | **Verdict:** REJECTED | **Weakest Dimension:** Methodological Rigor (0.50, Critical)
**One-line assessment:** The issue's headline "what was wrong" claim misattributes a fix to the wrong file, and its own "How to verify" command cannot surface the evidence for that claim — a zero-context reader following the text literally cannot confirm it.

## Scoring Context
- **Deliverable:** `.../STORY-006-issue-quality/snapshots/final/issue-362.md`
- **Deliverable Type:** Other (GitHub issue text, C4 tournament artifact)
- **Criticality Level:** C4 | **Strategy:** S-014 | **SSOT:** quality-enforcement.md
- **Scored:** 2026-08-07 | **Iteration:** 1 | **Strategy findings incorporated:** Yes (9 reports, re-verified against primary sources)

## Score Summary
| Metric | Value |
|---|---|
| Weighted Composite | **0.68** |
| Threshold | PASS >= 0.92 / REVISE 0.85-0.91 / REJECTED < 0.85 |
| Verdict | **REJECTED** |
| Critical findings (validated) | 1 (misattribution of PLAYBOOK.md fix to SKILL.md) |

## Dimension Scores
| Dimension | Weight | Score | Weighted | Severity | Evidence Summary |
|---|---|---|---|---|---|
| Completeness | 0.20 | 0.78 | 0.156 | Major | 5 expected sections present; named safety mechanisms undefined for zero-context reader; no sibling-issue pointer |
| Internal Consistency | 0.20 | 0.84 | 0.168 | Major | Line 5 self-tension: "nothing to do" immediately paired with an embedded open decision |
| Methodological Rigor | 0.20 | 0.50 | 0.100 | **Critical** | Line 7 "SKILL.md labeled...canonical" contradicted by primary commit diff (fix is in PLAYBOOK.md only) |
| Evidence Quality | 0.15 | 0.62 | 0.093 | Major | Good anchors (hash/CI/register) but flagship claim's own verify path can't substantiate it |
| Actionability | 0.15 | 0.60 | 0.090 | Major | Verify command omits PLAYBOOK.md, omits fetch step, and (per bundled commit) is noisy |
| Traceability | 0.10 | 0.68 | 0.068 | Major | Worktracker path resolves to a directory not a file; verify path broken for the core claim |
| **TOTAL** | **1.00** | | **0.675 -> 0.68** | | |

## Critical Finding — Independently Verified
I read `evidence-c07033ce.md` directly rather than trusting strategy reports alone. Confirmed:
- The `"(canonical format)"` -> `"(derived artifacts)"` edit and the four `Canonical agent definition` -> `Derived composition artifact` table-row edits occur **only** inside the `skills/nuclear-sop/PLAYBOOK.md` diff hunk (evidence pack lines 167, 207-210).
- `skills/nuclear-sop/SKILL.md`'s diff in this commit is **purely additive** (a new "DERIVED ARTIFACTS" `File Structure` block, evidence line ~265-266) — it contains no `-` line removing a prior "canonical" claim.
- Therefore issue line 7, "Meanwhile SKILL.md labeled the never-loaded `composition/` copy 'canonical,'" is not supported by the commit that the issue itself cites as proof, and the issue's own verify command (line 11, scoped to `composition/`, `agents/`, `SKILL.md`) omits `PLAYBOOK.md` — the one file that would show it.
- Independently raised as Critical by 6 of 9 blind strategies (S-010-01, S-003-01, S-002-01/02, S-001-01, S-007-01, S-013-01/02) — I judge this **valid**. Per instructions, this BLOCKS PASS regardless of composite.
- Secondary confirmed inaccuracy (Major, 6 strategies): line 7's "full stop-work in the agent file" implies `agents/sop-executor.md` was already clean pre-fix. Evidence pack lines 1478-1479 show its SEC-001 text ended "...and proceed with full STAR unchanged" (a self-contradicting tail) that this same commit removed — confirmed by register REM-13 fix spec item 2 ("`agents/sop-executor.md` line ~142 -> delete the tail").

## Detailed Dimension Notes
**Completeness (0.78):** All five expected sections present and on-topic. Gaps: "context-isolation contract" and "runtime self-delegation check" (line 7) are named but never glossed; no pointer to the other 6 sibling FIX-NOW issues (#357-361, #363) or the register's Cluster Index.
**Internal Consistency (0.84):** Narrative flows logically end-to-end. Gap: line 5's "Nothing for you to do unless you disagree" is immediately followed by an embedded open decision ("yours to decide during rework"), an unresolved tension about whether action is invited now.
**Methodological Rigor (0.50):** See Critical Finding above — the two confirmed factual defects sit at the center of the security narrative this issue exists to communicate.
**Evidence Quality (0.62):** Commit hash, CI run link (verified: evidence pack header confirms 15/15 green), branch name, and register section are credible anchors. Undermined because the one mechanism offered for independent verification (the diff command) cannot support the flagship claim, and (per S-011-01/S-012-01) the same commit bundles 29 files across all 7 FIX-NOW clusters with no disambiguation of which hunks belong to this defect.
**Actionability (0.60):** Clear top-line instruction, but the sole concrete action (run the verify diff) is broken as written: missing `PLAYBOOK.md`, missing a `git fetch` step before diffing a commit pushed directly to the contributor's branch (S-004-02), and the line-5 decision has no stated trigger or forum.
**Traceability (0.68):** Worktracker reference (line 14) resolves to a directory, not `BUG-013-composition-drift.md`. The verify command is the document's actual trace-to-source mechanism, and it is incomplete for the one claim most likely to be checked.

## Required Edits to Reach PASS
1. Line 7: `Meanwhile SKILL.md labeled the never-loaded \`composition/\` copy "canonical."` -> `Meanwhile PLAYBOOK.md labeled the never-loaded \`composition/\` copy "(canonical format)."`
2. Line 11: append `skills/nuclear-sop/PLAYBOOK.md` to the git diff path list.
3. Line 11: add one clause noting commit `c07033ce` bundles all 7 FIX-NOW clusters (REM-08..14), so unrelated hunks will appear; this defect's own hunks are limited to `composition/`, `agents/sop-executor.md`, `agents/sop-brief.governance.yaml`, `SKILL.md`, `PLAYBOOK.md`.
4. Line 11: prepend a fetch step, e.g. "After `git fetch origin proj-0039-nuclear-engineer`, run: ...".
5. Line 7: `full stop-work in the agent file` -> `stop-work in the agent file (undercut by a contradictory "proceed unchanged" tail that this same fix also deleted)`.
6. Line 5: split into "No action needed on this issue right now." and "Later, if you take up rework, you may choose to delete `composition/` entirely instead of keeping it synced — that decision is deferred, not part of this fix."
7. Line 7: gloss "the entire context-isolation contract" and "the runtime self-delegation check" with a short parenthetical each (what they restrict/protect).
8. Line 14: `work/BUG-013-composition-drift` -> `work/BUG-013-composition-drift/BUG-013-composition-drift.md`.
9. Add one sentence/link to the sibling FIX-NOW issues or the register's Cluster Index for readers wanting the full remediation picture.

## Leniency Bias Check
- [x] Each dimension scored independently before composite computed
- [x] Evidence cited with file/line references for every score, not impression
- [x] Critical finding re-verified against primary commit diff myself, not taken on strategy-report trust alone
- [x] Uncertain scores resolved downward (Methodological Rigor held at 0.50 boundary; Internal Consistency capped at 0.84, not lifted to Minor band)
- [x] No dimension scored above 0.95; max assigned is 0.84
- [x] Composite (0.675->0.68) verified by direct summation of weighted terms
