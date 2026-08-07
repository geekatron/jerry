# Pre-Mortem Report: GitHub issue #363 (BUG-014, navigation tables)

**Strategy:** S-004 Pre-Mortem Analysis
**Deliverable:** `projects/PROJ-032-nuclear-sop-review/work/EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-006-issue-quality/snapshots/final/issue-363.md`
**Criticality:** C4 (tournament)
**Date:** 2026-08-07
**Reviewer:** adv-executor (S-004)
**Note on H-16:** This is a blind, independent strategy execution within a tournament (no S-003 Steelman handoff is provided to this agent); proceeding per tournament orchestration design, not a standalone H-16 gate.
**Failure Scenario:** Six months from now, PR #269's external contributor (or their agent) reads issue #363, misjudges the fix's scope and process, and either (a) trusts a false "read on every run" criticality claim, (b) runs the suggested verification command and gets confused by unrelated diff noise, or (c) wants to object to the fix but finds no channel to do so — wasting a review cycle on an issue that was supposed to require zero contributor action.

## Summary

Two Major failure causes (a factual overstatement and an imprecise verification command) and three Minor gaps were found via prospective hindsight. The issue is well-sourced and its core claims (branch, commit, CI run, file list, "23/25 templates" ratio) all verify against ground truth and are live/resolvable on GitHub. **Recommendation: REVISE** — targeted text fixes only, no re-investigation needed.

## Findings Table

| ID | Failure Cause | Category | Likelihood | Severity | Priority |
|----|---------------|----------|------------|----------|----------|
| S-004-01 | "read by the brief agent on every run" overstates WORKFLOW_DEFINITION.template.md's actual consumption | Assumption | Medium | Major | P1 |
| S-004-02 | Verify command's `templates/` directory glob pulls in unrelated REM-11/REM-12 diffs | Technical | High | Major | P1 |
| S-004-03 | "unless you disagree with the fix" names no channel for disagreement | Process | Medium | Minor | P2 |
| S-004-04 | Verify command assumes contributor's local clone already has `c07033ce` | Process | Medium | Minor | P2 |
| S-004-05 | Tracking footer cites "register section REM-14" / "worktracker" with no gloss | Assumption | Low | Minor | P2 |

## Finding Details

### S-004-01: Overstated read frequency [MAJOR]

**Failure Cause:** Line 7 states `WORKFLOW_DEFINITION.template.md` is "read by the brief agent on every run." Ground truth (`skills/nuclear-sop/agents/sop-brief.md`, confirmed in both the PR worktree and the `c07033ce` diff) shows this file is loaded only inside **STEP 0 (Optional): Workflow Definition Generation from Natural Language** — invoked solely when no workflow definition exists and the user opts into natural-language generation. STEP 1 (Mandatory) validates an already-supplied workflow definition; it does not load this template.
**Category:** Assumption | **Likelihood:** Medium — a reader with no repo context has no way to catch this, and it inflates the file's perceived runtime criticality.
**Evidence:** `sop-brief.md` line 129: "STEP 0 (Optional): Workflow Definition Generation from Natural Language" -> line 141: "a. Load `skills/nuclear-sop/templates/WORKFLOW_DEFINITION.template.md`".
**Dimension:** Evidence Quality / Actionability
**Mitigation:** Change to "(250 lines, loaded by the brief agent's optional Step 0 when generating a workflow definition from natural language)" or drop the parenthetical entirely and keep just the line count.
**Acceptance Criteria:** Text no longer claims unconditional per-run consumption of a template that is only loaded on an optional path.

### S-004-02: Verification command mixes in unrelated diffs [MAJOR]

**Failure Cause:** Line 11's command diffs the whole `skills/nuclear-sop/templates/` directory. That directory also contains `POST_JOB_BRIEF.template.md` (`.yaml`-extension fix, REM-11) and `PROCEDURE_STATE.template.yaml` (state-machine rewrite, REM-12) — both changed by the same commit for unrelated clusters. Anyone running the command as written sees three unrelated diff hunks alongside the two nav-table additions, with nothing in the issue to explain the extra noise.
**Category:** Technical | **Likelihood:** High — this is deterministic; every run of the given command reproduces the noise.
**Evidence:** Commit `c07033ce` diffstat: `templates/HOLD_POINT_LOG.template.md`, `templates/POST_JOB_BRIEF.template.md`, `templates/PROCEDURE_STATE.template.yaml`, `templates/WORKFLOW_DEFINITION.template.md` all appear under `templates/`; only the first and last belong to BUG-014.
**Dimension:** Actionability / Traceability
**Mitigation:** Replace the directory globs with the exact six file paths:
`git diff c07033ce^ c07033ce -- skills/nuclear-sop/templates/WORKFLOW_DEFINITION.template.md skills/nuclear-sop/templates/HOLD_POINT_LOG.template.md skills/nuclear-sop/examples/c3-adr-workflow-definition.md skills/nuclear-sop/SKILL.md skills/nuclear-sop/PLAYBOOK.md skills/nuclear-sop/docs/reference.md`
**Acceptance Criteria:** Running the copy-pasted command shows only nav-table-related hunks.

## Recommendations

- **P1 (S-004-01):** Correct the read-frequency claim for `WORKFLOW_DEFINITION.template.md` (Step 0, optional, not every run).
- **P1 (S-004-02):** Scope the verify command to the six exact files, not directory globs.
- **P2 (S-004-03):** Add one clause naming where to raise disagreement (comment on issue #363 or reply on PR #269).
- **P2 (S-004-04):** Prepend a fetch/pull reminder before the `git diff` command for contributors on a stale local clone.
- **P2 (S-004-05):** Gloss "register section REM-14" / "worktracker" as internal-only traceability, or drop from the reader-facing footer.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Evidence Quality | 0.15 | Negative | S-004-01: one factual claim does not match the cited agent's actual behavior |
| Actionability | 0.15 | Negative | S-004-02, S-004-03, S-004-04: verify/disagree/fetch gaps force lookups or guesswork |
| Completeness | 0.20 | Neutral | Core facts (branch, commit, CI, files, ratio) all verified against ground truth |
| Traceability | 0.10 | Negative | S-004-05: unexplained internal register/worktracker terms in reader-facing text |
| Internal Consistency | 0.20 | Positive | No contradictions found between paragraphs |
| Methodological Rigor | 0.20 | Neutral | N/A for a communication artifact |

**Result:** 0 Critical, 2 Major, 3 Minor. All P1/P2 mitigations are single-sentence or single-line text edits; no re-investigation required.
