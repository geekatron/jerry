# Constitutional Compliance Report: GitHub Issue #363 (BUG-014 / REM-14 — navigation tables)

**Strategy:** S-007 Constitutional AI Critique (adapted for a communication artifact)
**Deliverable:** `snapshots/final/issue-363.md` — live text of `geekatron/jerry` issue #363
**Criticality:** C4 (tournament)
**Reviewer:** adv-executor
**Constitutional lens (adapted):** factual accuracy, self-containedness, actionability, resolvable references, honest severity/status framing, concision — in place of code-oriented HARD/MEDIUM/SOFT rules, since the deliverable is prose, not code or governance text.

## Summary

PARTIAL compliance: 0 Critical, 2 Major (one factual overstatement, one under-scoped verify command), 2 Minor (unexplained internal labels). Core claims (commit, CI run, worktracker path, cluster count, file list, line counts, C1-C2 status framing) all check out against the remediation register, remediation log, evidence pack, and the PR worktree. Score: 0.86 (REVISE). Recommend targeted revision; no re-review of the whole issue needed.

## Findings Table

| ID | Principle (adapted) | Tier | Severity | Evidence | Affected Dimension |
|----|---------------------|------|----------|----------|--------------------|
| S-007-01 | Factual accuracy | HARD-equiv | Major | "read by the brief agent on every run" (line 7) | Evidence Quality |
| S-007-02 | Actionability / resolvable references | MEDIUM-equiv | Major | "How to verify" git diff command (line 11) | Actionability |
| S-007-03 | Self-containedness | SOFT-equiv | Minor | Title: "PROJ-032/BUG-014" prefix | Completeness |
| S-007-04 | Self-containedness | SOFT-equiv | Minor | "23 of the repo's 25 canonical templates" (line 9) | Completeness |

## Finding Details

### S-007-01: WORKFLOW_DEFINITION.template.md is not read "on every run" [MAJOR]

**Location:** Line 7, parenthetical after `templates/WORKFLOW_DEFINITION.template.md (250 lines, read by the brief agent on every run)`.
**Evidence:** `sop-brief.md` documents this file's load under **"STEP 0 (Optional): Workflow Definition Generation from Natural Language"** with an explicit trigger: *"No workflow definition file is provided. User supplies a natural language description of the procedure."* The internal worktracker record for this same defect (BUG-014) says only "consumed by sop-brief Step 0" — it does not claim "every run." Most invocations supply an existing workflow definition and never touch this template.
**Impact:** Overstates the template's runtime centrality. An external agent auditing sop-brief's behavior against this issue would expect an unconditional load and could misjudge the blast radius of any future change to this file.
**Recommendation:** Replace with: `templates/WORKFLOW_DEFINITION.template.md (250 lines, loaded by sop-brief's optional Step 0 when generating a workflow definition from a natural-language description)`.

### S-007-02: "How to verify" command is not scoped to this issue's fix [MAJOR]

**Location:** Line 11, `git diff c07033ce^ c07033ce -- skills/nuclear-sop/templates/ skills/nuclear-sop/examples/ skills/nuclear-sop/SKILL.md skills/nuclear-sop/PLAYBOOK.md skills/nuclear-sop/docs/reference.md`.
**Evidence:** Commit `c07033ce` implements all seven FIX-NOW clusters (REM-08..14) in one commit, per the remediation log's own trace table. The paths named in this command are also touched by unrelated clusters filed as separate issues: `templates/POST_JOB_BRIEF.template.md` and `templates/PROCEDURE_STATE.template.yaml` (under `templates/`) carry the `.yaml`-extension fix from issue #360 (REM-11) and the state-machine fix from issue #361 (REM-12); `SKILL.md` and `PLAYBOOK.md` also carry the registration/C3+-status rewrite from issue #357 (REM-08).
**Impact:** A contributor running the given command gets a diff dominated by hunks belonging to six other issues, with no way to tell from the command alone which lines are "this" fix. Forces a manual hunt through unrelated diff noise — the exact kind of extra lookup the mission asks this text to avoid.
**Recommendation:** Scope the diff to only the files this fix owns exclusively, and point at the specific added blocks for the shared files, e.g.:
`git diff c07033ce^ c07033ce -- skills/nuclear-sop/templates/WORKFLOW_DEFINITION.template.md skills/nuclear-sop/templates/HOLD_POINT_LOG.template.md skills/nuclear-sop/examples/c3-adr-workflow-definition.md`
and for the three files shared with other issues, `grep -n "^## " skills/nuclear-sop/SKILL.md skills/nuclear-sop/PLAYBOOK.md skills/nuclear-sop/docs/reference.md` against the nav tables (or `grep -n "P-003 Compliance"` / `"OE Accumulation Thresholds"` / `"## Related"` for the specific new rows) instead of diffing the whole files.

## Remediation Plan

**P1 (Major):** S-007-01: fix the "on every run" claim. S-007-02: narrow or replace the verify command per above.
**P2 (Minor):** S-007-03: title's `PROJ-032/BUG-014` prefix is unexplained to an external reader — either drop it or add a 3-word gloss (e.g., "internal tracking id"); it does not block understanding since the body already states there is nothing to do. S-007-04: "23 of the repo's 25 canonical templates" references an undefined corpus (`.context/templates/`); harmless to the ask (informational justification only) but could gloss with "(the framework's own reference doc templates)".

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | All required facts (commit, CI, files, tracking) present |
| Internal Consistency | 0.20 | Neutral | No internal contradictions found |
| Methodological Rigor | 0.20 | Negative | S-007-01: unverified frequency claim inserted beyond source data |
| Evidence Quality | 0.15 | Negative | S-007-01 not supported by (in fact contradicted by) sop-brief.md |
| Actionability | 0.15 | Negative | S-007-02: verify command not isolated to this defect |
| Traceability | 0.10 | Positive | Commit, CI run, worktracker path, and register section all independently confirmed accurate |

**Constitutional Compliance Score:** 1.00 − (2 × 0.05 Major + 2 × 0.02 Minor) = **0.86 (REVISE)**

**Verified accurate (no findings):** commit `c07033ce` on `proj-0039-nuclear-engineer`; CI run `31174766440` (15/15 green); all six affected file paths and line counts (250/76/559); "7 mechanical fixes" (REM-08..14) count; "3 of the skill's own 5 templates" pre-existing nav-table baseline (confirmed `PRE_JOB_BRIEF.template.md` already compliant); worktracker path `work/BUG-014-navigation-tables/`; BUG-014 status `completed` with all three ACs verified 2026-08-07 — consistent with the issue's "nothing to do" framing.
