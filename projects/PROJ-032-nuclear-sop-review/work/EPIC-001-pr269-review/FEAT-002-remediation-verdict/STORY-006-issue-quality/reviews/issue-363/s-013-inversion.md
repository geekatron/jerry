# Inversion Report: GitHub Issue #363 (PROJ-032/BUG-014 nav tables)

**Strategy:** S-013 Inversion Technique
**Deliverable:** `projects/PROJ-032-nuclear-sop-review/.../STORY-006-issue-quality/snapshots/final/issue-363.md`
**Criticality:** C4 (tournament)
**Date:** 2026-08-07
**Reviewer:** adv-executor (S-013)
**Goals Analyzed:** 5 | **Assumptions Mapped:** 6 | **Vulnerable Assumptions:** 2

## Summary

Goals inverted: (1) reader acts correctly with zero repo knowledge, (2) reader can independently
verify the fix, (3) claims are factually precise. Two of six mapped assumptions failed stress-testing:
the verification command's assumed precision (it pulls in unrelated diffs from the same commit) and
two supporting line-count claims (off by one line each against the actual pre-fix file lengths,
confirmed from the diff hunks and current worktree file lengths). Recommendation: **ACCEPT with
targeted mitigation** on the verify-command scope (Major); line-count corrections are cosmetic (Minor).

## Findings Table

| ID | Assumption / Anti-Goal | Type | Confidence | Severity | Evidence | Affected Dimension |
|----|------------------------|------|------------|----------|----------|--------------------|
| S-013-01 | "git diff ... -- .../templates/ .../examples/ SKILL.md PLAYBOOK.md docs/reference.md" isolates only the REM-14 nav-table fix | Assumption | Medium | Major | evidence-c07033ce.md diffstat: `templates/` dir in c07033ce also touches `PROCEDURE_STATE.template.yaml` (REM-12 state-machine rewrite) and `POST_JOB_BRIEF.template.md` (REM-11 `.yaml`-extension change) — neither is a REM-14 change | Evidence Quality |
| S-013-02 | "76 lines" (HOLD_POINT_LOG.template.md, pre-fix) | Assumption | High | Minor | Current file = 86 lines (read in full); diffstat shows `+9` net insertions for this file → pre-fix = 77 lines, not 76 | Evidence Quality |
| S-013-03 | "559 lines" (c3-adr-workflow-definition.md, pre-fix) | Assumption | High | Minor | Current file = 577 lines; diff hunks show net +17 lines (17 ins in hunk 1, 0 net in the two 1-for-1 line edits) → pre-fix = 560 lines, not 559 | Evidence Quality |
| S-013-04 | Reader has a local clone with `c07033ce` already fetched to run the diff command | Assumption | Medium | Minor | No browser-based fallback given (e.g., a direct commit URL); only the CI Actions link is provided as a no-clone alternative, and it shows CI status, not the diff content | Actionability |

**Verified accurate (not vulnerable):** "250 lines" (WORKFLOW_DEFINITION.template.md pre-fix) matches exactly (current 266 − 16 net insertions = 250); branch name `proj-0039-nuclear-engineer`; commit `c07033ce`; CI run URL; the six affected file paths; "23 of 25 canonical templates / 3 of 5 skill templates" phrasing (matches register verbatim); "one of seven mechanical fixes" (7 FIX-NOW clusters, REM-08..14 confirmed in register); worktracker path `.../work/BUG-014-navigation-tables` (directory confirmed to exist) and the cross-branch register path (confirmed to exist on `feat/proj-032-nuclear-sop-review`).

## Finding Details

### S-013-01: Verify command scope is wider than the claimed fix [MAJOR]

**Type:** Assumption
**Original Assumption:** Scoping `git diff c07033ce^ c07033ce` to the five listed path prefixes (`templates/`, `examples/`, `SKILL.md`, `PLAYBOOK.md`, `docs/reference.md`) shows exactly this issue's fix.
**Inversion:** The same commit `c07033ce` bundles all seven FIX-NOW clusters (REM-08..14). Because `templates/` is a directory prefix (not the two specific filenames), the command also surfaces `templates/PROCEDURE_STATE.template.yaml` (REM-12: state-machine transition rewrite) and `templates/POST_JOB_BRIEF.template.md` (REM-11: `.yaml` extension standardization) — both unrelated to navigation tables.
**Plausibility:** Certain — confirmed directly from the diffstat and full diff in `evidence-c07033ce.md`.
**Consequence:** A contributor or their agent running the exact command as written will see unrelated diff hunks and may reasonably (but incorrectly) conclude they are also part of "this" fix, or lose confidence in the issue's precision when the diff doesn't match the two-file description.
**Evidence:** `evidence-c07033ce.md` diffstat lines for `templates/PROCEDURE_STATE.template.yaml` (28 changed lines) and `templates/POST_JOB_BRIEF.template.md` (4 changed lines), both under the `skills/nuclear-sop/templates/` prefix used in the issue's verify command.
**Dimension:** Evidence Quality
**Mitigation:** Replace the directory-prefix paths with the exact six file paths already enumerated in `remediation-register.md` REM-14 "Affected files": `git diff c07033ce^ c07033ce -- skills/nuclear-sop/templates/WORKFLOW_DEFINITION.template.md skills/nuclear-sop/templates/HOLD_POINT_LOG.template.md skills/nuclear-sop/examples/c3-adr-workflow-definition.md skills/nuclear-sop/SKILL.md skills/nuclear-sop/PLAYBOOK.md skills/nuclear-sop/docs/reference.md`.
**Acceptance Criteria:** Running the corrected command shows only nav-table additions/row insertions — no state-machine or file-extension changes.

### S-013-02 / S-013-03: Two line-count claims are off by one [MINOR]

**Type:** Assumption
**Original Assumption:** "76 lines" and "559 lines" report the exact pre-fix line counts of `HOLD_POINT_LOG.template.md` and `c3-adr-workflow-definition.md`.
**Inversion:** Recomputing from the current worktree file length minus the diff's net insertions gives 77 and 560 respectively, not 76 and 559. (By contrast, the third claim — "250 lines" for `WORKFLOW_DEFINITION.template.md` — checks out exactly.)
**Plausibility:** Certain — arithmetic from Read-tool line counts and diffstat insertions.
**Consequence:** Low — the qualitative claim ("long file") is unaffected and no action depends on the exact count, but a precision-checking reader/agent that recomputes will flag a discrepancy and may (wrongly) distrust the rest of the issue's factual claims.
**Evidence:** `HOLD_POINT_LOG.template.md` = 86 lines now, diffstat `+9` → 77 pre-fix. `c3-adr-workflow-definition.md` = 577 lines now, diff hunks net `+17` → 560 pre-fix.
**Dimension:** Evidence Quality
**Mitigation:** Correct to "77 lines" and "560 lines," or drop the exact counts and keep only the qualitative "long" framing plus the (already-accurate) purpose clause.
**Acceptance Criteria:** Stated counts match `wc -l` on the pre-fix blobs (`git show c07033ce^:<path> | wc -l`).

### S-013-04: No no-clone verification path [MINOR]

**Type:** Anti-Goal (verification anti-goal: "how would we guarantee a reader without git access can't verify?")
**Inversion:** Omit any browser link to the diff itself. The issue provides a CI-status link (proves tests passed, not what changed) but no link to the commit/diff view.
**Consequence:** A reader/agent without a local clone of `proj-0039-nuclear-engineer` at `c07033ce` cannot execute the suggested command and has no equivalent read-only path to inspect the actual change.
**Evidence:** Issue text §"How to verify" contains only the `git diff` command and the Actions run URL; no `github.com/geekatron/jerry/commit/c07033ce` link.
**Dimension:** Actionability
**Mitigation:** Add `https://github.com/geekatron/jerry/commit/c07033ce` (optionally scoped with `?diff=split&filepath=...` per file) alongside the `git diff` command.
**Acceptance Criteria:** A reader with browser-only access can view the exact diff without cloning.

## Recommendations

- **Major:** S-013-01 — MUST fix the verify command to the six exact file paths before this issue is treated as a template for the remaining REM-08..13 issues (same bundling risk applies to all of them).
- **Minor:** S-013-02, S-013-03 — SHOULD correct to 77/560 or remove exact counts.
- **Minor:** S-013-04 — MAY add a direct commit link for no-clone verification.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | All required sections (what/why/fix/verify/tracking) present |
| Internal Consistency | 0.20 | Neutral | No contradictions found |
| Methodological Rigor | 0.20 | Neutral | N/A to this artifact type |
| Evidence Quality | 0.15 | Negative | S-013-01 (verify command scope), S-013-02/03 (line-count precision) |
| Actionability | 0.15 | Negative | S-013-01 (misleading verify output), S-013-04 (no-clone gap) |
| Traceability | 0.10 | Positive | Register/commit/CI references all independently confirmed accurate |
