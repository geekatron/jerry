# Chain-of-Verification Report: GitHub Issue #360 (BUG-011 / REM-11)

**Strategy:** S-011 Chain-of-Verification
**Deliverable:** `snapshots/final/issue-360.md` (live text of GitHub issue #360, geekatron/jerry)
**Criticality:** C4 (tournament)
**Date:** 2026-08-07
**Reviewer:** adv-executor (S-011)
**H-16 Compliance:** Not applied — S-003 output not supplied in this invocation (indirect for CoVe; proceeded per protocol note)
**Claims Extracted:** 10 | **Verified:** 8 | **Discrepancies:** 0 Critical/Major, 2 Minor (precision)

## Summary

All ten testable claims in issue #360 — the commit SHA, branch name, "seven mechanical fixes" framing, the three named defects (extension contradiction, unsatisfiable acceptance criterion, three-way retrieval-protocol drift, unwritten Attachments contract), the fix description, the CI run link/count, and the worktracker/register cross-reference — verify exactly against `remediation-register.md` (REM-11), `remediation-log.md`, and the full diff in `evidence-c07033ce.md`. No Critical or Major discrepancy found. Two Minor precision gaps identified in the "How to verify" reproduction commands and one unexplained internal term. **Recommendation: ACCEPT** (no correction required before acceptance; Minor items are optional polish).

## Findings Table

| ID | Claim | Source | Discrepancy | Severity |
|----|-------|--------|-------------|----------|
| S-011-01 | "`grep -rn "experience/.*\.md" skills/nuclear-sop/` returns nothing" | remediation-register.md REM-11 item 7 validation: `grep -rn "experience/.*\.md\|oe-entry-.*\.md" ...` | Issue's reproduction command omits the `oe-entry-.*\.md` alternation from the register's own validate step. Outcome is identical (0 hits either way post-fix, confirmed in diff), so not misleading in result, but a reader who greps only for `experience/.*\.md` is not actually running the full check the register specifies. | Minor |
| S-011-02 | "run `git diff c07033ce^ c07033ce -- skills/nuclear-sop/`" | evidence-c07033ce.md full diff (29 files, all 7 FIX-NOW clusters REM-08..14) | The command reproduces the *entire* commit's changes under `skills/nuclear-sop/` (schema fixes, nav tables, composition drift, state-machine changes, etc.), not just this issue's `.yaml`/retrieval-protocol/Attachments-step changes. A contributor running it will see far more diff than this issue describes and may not be able to tell which hunks belong to this defect. | Minor |
| S-011-03 | "Tracking: worktracker `projects/PROJ-032-nuclear-sop-review/work/BUG-011-oe-artifact-contract`" | N/A (terminology) | "worktracker" is Jerry-internal terminology, used without definition. The path itself is resolvable and correct (file exists at that location), so this is a self-containedness nit, not a broken reference. | Minor |

## Verification Detail (claims not listed above verified clean)

- **Commit `c07033ce`, branch `proj-0039-nuclear-engineer`:** matches `evidence-c07033ce.md` header and `remediation-log.md` Outcome line exactly.
- **"one of seven mechanical fixes ... in commit c07033ce":** `remediation-log.md` confirms one commit implements all seven FIX-NOW clusters (REM-08..14); REM-11 is one of them. Accurate.
- **Extension contradiction claim** (rules/write-path use `.yaml`; post-job template, one behavioral baseline, and the worked example said `.md`): matches register REM-11 G1 exactly (`POST_JOB_BRIEF.template.md`, `bb-003-oe-feedback-loop-integrity.md`, `examples/c3-adr-workflow-definition.md`), and the diff shows all three corrected to `.yaml`.
- **"one of the worked example's acceptance criteria was literally unsatisfiable":** matches register REM-04/REM-11 cross-reference to AC-7 ("globs `.md`, capture writes `.yaml`"); diff shows AC-7's glob corrected to `*.yaml`.
- **"retrieval protocol ... specified three different ways":** matches register REM-11 G2 (rules' workflow_id-primary protocol vs. sop-brief's workflow_type-only Glob vs. bb-003 B-24's third variant); diff shows sop-brief Step 4 and bb-003 B-24 both rewritten to the rules' single protocol.
- **"Attachments section ... documented as runtime-written by the capture agent, whose procedure never actually writes it":** matches register REM-11 G3 verbatim; diff adds the exact missing step to `sop-capture.md` ("Section 11 attachment (mandatory, before status COMPLETED)... fulfills the 'runtime-written by sop-capture' contract").
- **"CI at that commit: 15/15 green — .../runs/31174766440":** matches `evidence-c07033ce.md` header and `remediation-log.md` Outcome line exactly (same URL, same count).
- **Worktracker/register path** (`work/BUG-011-oe-artifact-contract`, `remediation-register.md` REM-11, under `STORY-004-remediation/`, branch `feat/proj-032-nuclear-sop-review`): file exists at the stated path; register section and branch name confirmed against the working tree.
- **"this issue stays open only until PR #269's disposition is decided":** consistent with `pr269-verdict.md` L0 recommendation (REWORK — keep PR #269 open, do not merge, do not close) and FIX-NOW issues #357–363 not being independently closed ahead of the PR decision.

## Recommendations

- **Minor (S-011-01):** Extend the verify grep to `grep -rn "experience/.*\.md\|oe-entry-.*\.md" skills/nuclear-sop/` to match the register's actual validation command, or note that the shown command is a subset check.
- **Minor (S-011-02):** Either scope the git-diff command more precisely (e.g., name the specific files: `templates/POST_JOB_BRIEF.template.md`, `behavioral-baselines/bb-003-*.md`, `examples/c3-adr-workflow-definition.md`, `agents/sop-brief.md`, `agents/sop-capture.md`) or add one clause noting the diff also contains six unrelated fixes from the same commit.
- **Minor (S-011-03):** Replace "worktracker" with a neutral gloss, e.g., "internal tracking record" or "project tracking file," since the term carries no meaning outside this repository's own tooling.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | All factual/verification claims present and traceable; no gaps found beyond Minor precision items |
| Internal Consistency | 0.20 | Neutral | No contradictions between issue text and source documents |
| Methodological Rigor | 0.20 | Positive | 10/10 claims independently verified against primary sources with zero Critical/Major discrepancy |
| Evidence Quality | 0.15 | Neutral | Minor findings are precision gaps in reproduction commands, not evidentiary errors |
| Actionability | 0.15 | Slightly Negative | S-011-01/S-011-02 reduce exactness of the self-verification steps a reader would follow |
| Traceability | 0.10 | Positive | Every claim traces cleanly to register/log/diff/verdict sources |
