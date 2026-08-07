# Pre-Mortem Report: GitHub Issue #353 (BUG-004 / REM-04)

**Strategy:** S-004 Pre-Mortem Analysis
**Deliverable:** `projects/PROJ-032-nuclear-sop-review/work/EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-006-issue-quality/snapshots/final/issue-353.md`
**Criticality:** C4 (tournament)
**Date:** 2026-08-07
**Reviewer:** adv-executor (S-004)
**H-16 Compliance:** N/A for this blind single-strategy tournament lane (no S-003 output supplied upstream; scope is compact communication-artifact review, not a full C3+ pipeline)
**Failure Scenario:** Six months from now, the PR #269 author reads issue #353, acts on it in good faith, and the interaction fails: they either (a) click the Worktracker path on the repo's default branch, hit a 404, and conclude the review's evidence trail is unreliable, or (b) fix only BUG-004, resubmit, and are surprised to learn four sibling Critical issues (#350–#352, #354) still block the exact "higher-risk approval" outcome this issue frames as the goal.

## Summary

Fact-checking against the remediation register, log, verdict, and commit evidence confirms the issue's substantive claims (answer-key contamination, "empirically validated" mischaracterization, withdrawal via `c07033ce`, current C1–C2 restriction, non-maintainer-fixability) are all accurate. Two failure modes surface from the temporal-hindsight lens, both about what an acting reader needs but doesn't get: one broken-reference risk (Critical) and one false-completeness risk (Major). One cosmetic self-containedness gap (Minor). Recommendation: REVISE — targeted, not structural.

## Findings Table

| ID | Failure Cause | Category | Likelihood | Severity | Priority |
|----|---------------|----------|------------|----------|----------|
| S-004-01 | Worktracker path lacks branch annotation; agent/human resolves it on default branch and 404s | Technical | High | Critical | P0 |
| S-004-02 | No mention of sibling blocking issues (#350–352, #354); reader believes fixing BUG-004 alone restores higher-risk approval | Process | Medium | Major | P1 |
| S-004-03 | "PROJ-032" in the title is an unexplained internal project code | Assumption | Low | Minor | P2 |

## Finding Details

### S-004-01: Worktracker path is not resolvable without an inferred branch [CRITICAL]

**Failure Cause:** The Tracking paragraph gives two paths back-to-back: `projects/PROJ-032-nuclear-sop-review/work/BUG-004-qg-e4-validation-evidence` (no branch stated) and `remediation-register.md` in `.../STORY-004-remediation/` "on branch `feat/proj-032-nuclear-sop-review`" (branch stated explicitly). Verified: the entire `projects/PROJ-032-nuclear-sop-review/` tree exists only on `feat/proj-032-nuclear-sop-review` — it is absent from the repo's recent main-branch commit history — so the Worktracker path 404s on GitHub's default branch view.
**Likelihood:** High — GitHub's file browser and most agents resolve unqualified repo paths against the default branch first.
**Severity:** Critical — mission's own resolvability bar ("paths carry branches") is explicitly violated for this one reference, and a 404 on the *first* linked path in the tracking section plausibly discredits the rest of the issue's citations in the reader's eyes.
**Evidence:** Issue text line: "Worktracker: `projects/PROJ-032-nuclear-sop-review/work/BUG-004-qg-e4-validation-evidence` (register section REM-04)." — no branch qualifier attached, unlike the very next path in the same paragraph.
**Mitigation:** Append the same branch qualifier to the Worktracker path: "...`work/BUG-004-qg-e4-validation-evidence` on branch `feat/proj-032-nuclear-sop-review` (register section REM-04)."
**Acceptance Criteria:** Every file-path reference in the Tracking paragraph carries an explicit branch, not just the second one.

### S-004-02: Silent omission of the other four DEFER-REWORK blockers [MAJOR]

**Failure Cause:** The issue states "Blocks any restoration of higher-risk approval" for this issue alone. Per the verdict (`pr269-verdict.md` L0) and remediation log, restoring C3+ approval also requires resolving BUG-001/002/003/005 (issues #350–#352, #354) — the register frames REM-01/02/03/05 as attacking "the skill's core safety architecture." A contributor who fixes only the validation-evidence gap could reasonably believe higher-risk approval is now unblocked.
**Likelihood:** Medium — the sentence is not literally false (it doesn't claim sufficiency), but the omission invites the inference.
**Severity:** Major — degrades actionability; the fix requires only a lookup at the register, not new evidence.
**Evidence:** Issue: "Blocks any restoration of higher-risk approval; the low-risk-only restriction otherwise stands." vs. verdict: "seven named design defects ... block merge" and remediation-log: DEFER-REWORK items "remain open ... and block any merge recommendation."
**Mitigation:** Add one clause: "...along with four sibling design-authority blockers (#350–#352, #354)."
**Acceptance Criteria:** Reader cannot conclude that resolving #353 alone is sufficient to restore higher-risk approval.

## Recommendations

- **P0:** S-004-01 — add the branch qualifier to the Worktracker path. Trivial one-clause edit; verifiable by re-reading the Tracking paragraph for a branch string attached to both paths.
- **P1:** S-004-02 — add a one-clause cross-reference to the sibling blocking issues. Verifiable by confirming the "blocks" sentence names or numerically references the other open DEFER-REWORK issues.
- **P2:** S-004-03 — optionally gloss "PROJ-032" once (e.g., "internal review tracking ID") or drop it from the title since `BUG-004` plus the Worktracker path already fully identify the item; low cost, low reader impact, acknowledge and move on.

## Scoring Impact

| Dimension | Impact | Rationale |
|-----------|--------|-----------|
| Completeness | Negative | S-004-02: omits a fact a fully-informed contributor needs |
| Internal Consistency | Negative | S-004-01: one path branch-qualified, the adjacent one is not |
| Actionability | Negative | S-004-01, S-004-02: both create wrong-path/false-completion risk for an acting agent |
| Traceability | Neutral | All substantive claims verified accurate against register/log/verdict/commit evidence |

**Result:** 1 Critical, 1 Major, 1 Minor. No factual inaccuracies found in the issue's core claims — the defects are reference-hygiene and cross-reference-completeness gaps, both cheaply fixable without touching the accurate substance.
