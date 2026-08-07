# Constitutional Compliance Report: GitHub Issue #356 (BUG-007 — executor command gating)

**Strategy:** S-007 Constitutional AI Critique (adapted: communication-artifact principles substitute for code/architecture rules — factual accuracy, self-containedness, actionability, resolvable references, honest severity, concision)
**Deliverable:** `.../STORY-006-issue-quality/snapshots/final/issue-356.md` (live text of GitHub issue #356, geekatron/jerry)
**Criticality:** C4 (tournament strategy execution)
**Date:** 2026-08-07
**Reviewer:** adv-executor (S-007)
**Ground truth checked:** remediation-register.md (REM-07), BUG-007-executor-command-gating.md, pr269-verdict.md, phase-2-eng-review.md, PR #269 branch worktree

## Summary

PARTIAL compliance: the technical substance (denylist gap, injection-screening gap, log-echo second-order channel, duplication of the deterministic enforcement engine, severity=major) is accurate against the register and BUG-007 entity. **1 Critical, 2 Major, 2 Minor.** The Critical finding is a resolvable-reference failure: the cited Worktracker path does not exist on the PR's own branch. Recommend REVISE before treating this issue as reliably actionable by the contributor/agent.

## Findings Table

| ID | Principle | Severity | Evidence | Affected Dimension |
|----|-----------|----------|----------|---------------------|
| S-007-01 | Resolvable References | Critical | Worktracker path given with no branch qualifier; branch clause reads as scoped only to the register path | Actionability |
| S-007-02 | Internal Consistency / Scope Accuracy | Major | Narrative widens injection-screening scope to 4 artifact types; design question correctly narrows to workflow-definition fields | Internal Consistency |
| S-007-03 | Completeness / Actionability | Major | Omits the required PLAYBOOK "primary mitigation" correction from BUG-007's acceptance criteria | Completeness |
| S-007-04 | Actionability | Minor | "existing deterministic security enforcement engine" not named or located | Actionability |
| S-007-05 | Completeness | Minor | Available interim mitigation (narrow sop-brief/sop-capture Bash grants) omitted | Completeness |

## Finding Details

### S-007-01: Worktracker path has no attached branch, and does not exist on the PR branch [CRITICAL]

**Location:** Tracking paragraph, sentence 1: `` Worktracker: `projects/PROJ-032-nuclear-sop-review/work/BUG-007-executor-command-gating` (register section REM-07). ``
**Evidence:** Verified against the actual PR #269 worktree checkout: `projects/PROJ-032-nuclear-sop-review/` on that branch contains only `.jerry/data/events/*` — no `work/BUG-007-executor-command-gating/` directory. The path only resolves on `feat/proj-032-nuclear-sop-review` (the reviewer's branch). The issue states "on branch `feat/proj-032-nuclear-sop-review`" only once, at the end of the *next* sentence, grammatically attached to `remediation-register.md`'s location — not to the Worktracker path.
**Impact:** An external contributor or their agent checking out PR #269 (branch `proj-0039-nuclear-engineer`) and following the Worktracker path literally will find nothing there, and may reasonably conclude the reference is broken or the tracking is fabricated — undermining trust in the rest of the issue's citations.
**Remediation:** Attach the branch qualifier to both paths explicitly, e.g.: "Worktracker: `projects/PROJ-032-nuclear-sop-review/work/BUG-007-executor-command-gating` and full analysis in `remediation-register.md` under `.../STORY-004-remediation/` — both on branch `feat/proj-032-nuclear-sop-review` (not this PR's branch)."

### S-007-02: Screening-scope narrative is broader than, and inconsistent with, the actual design question [MAJOR]

**Location:** "What this is about" paragraph vs. "The design question to answer" paragraph.
**Evidence:** Narrative: "the skill's prompt-injection screening likewise covers only one of the several attacker-influenceable inputs (workflow definitions, state files, lessons-learned entries, hold-point logs) that end up driving tool calls." Design question: "what is the injection-screening scope across *all* definition-sourced fields that drive tool calls?" Ground truth (remediation-register.md REM-07 G2) scopes the actual defect to fields *within* the workflow definition (Action, Target, Expected Result, Sign-off Criterion, Hold Reason, Sections 2/3/9 prose) — not to state files, OE ("lessons-learned") entries, or hold-point logs, which are separately tracked defects (state-file tamper protection is issue #352/REM-03; the OE feedback loop is issue #355/REM-06).
**Impact:** A contributor reading only the narrative could believe BUG-007 requires building injection screening for state files, OE entries, and hold logs too — duplicating work already scoped to two other open issues, or under-scoping if they instead trust the (correct) narrower design question and wonder why the intro mentioned the other three artifact types at all.
**Remediation:** Narrow the narrative to match the design question: "...covers only WARNING/CAUTION annotations inside the workflow definition — while several other fields in that same file (the action steps, targets, expected results, sign-off text) are equally attacker-controlled and drive tool calls just the same way." Drop "state files, lessons-learned entries, hold-point logs" from this issue (they belong to #352 and #355).

### S-007-03: A required fix from the same acceptance criteria is missing from the issue [MAJOR]

**Location:** "The design question to answer" paragraph (only covers gating model + screening scope).
**Evidence:** BUG-007-executor-command-gating.md acceptance criteria also require: "PLAYBOOK's mitigation hierarchy corrected to name SR-06 human review as primary" (PLAYBOOK.md currently calls the machine-side SEC-001/SEC-002 checks "the primary mitigations," which register REM-07 G2 calls an overstatement — human review is the actual primary control).
**Impact:** A contributor who resolves only the gating-model design question and re-reads the issue for completeness will not know this correction is also required to close the bug — they would have to independently discover it in the register on a different branch.
**Remediation:** Add one sentence: "Also correct PLAYBOOK.md's claim that these machine checks are 'the primary mitigations' — human review is the primary control; the automated checks are a secondary net."

### S-007-04: Enforcement engine to delegate to is not named or located [MINOR]

**Evidence:** "the repository already has a deterministic security enforcement engine this duplicates" — no file path or component name given (actual location: `src/infrastructure/internal/enforcement/security_enforcement_engine.py`, 82 tests per register).
**Remediation:** "...duplicates the repo's `SecurityEnforcementEngine` (`src/infrastructure/internal/enforcement/`), weaker, at the prompt level."

### S-007-05: Low-risk interim mitigation omitted [MINOR]

**Evidence:** remediation-register.md REM-07 notes an interim, non-redesign mitigation available now: narrowing sop-brief/sop-capture's Bash grants, since their declared needs are already covered by other tools.
**Remediation:** Optionally add: "Independent of the redesign: sop-brief and sop-capture can have their Bash access narrowed now — their stated needs are already covered by other tools."

## Scoring Impact

Constitutional compliance score: `1.00 - (1*0.10 + 2*0.05 + 2*0.02) = 0.76` → REJECTED band (< 0.85) on this strategy's dimension, driven primarily by the branch-resolvability failure and the scope-consistency gap. Both are correctable with small, surgical text edits — no redesign of the issue is needed.

## Self-Review Note (H-15)

Every claim above was checked against a source: the PR-branch worktree checkout (S-007-01), remediation-register.md REM-07 and phase-2-eng-review.md's 5-input STRIDE list (S-007-02), BUG-007-executor-command-gating.md acceptance criteria (S-007-03), and the PR269 worktree's `security_enforcement_engine.py` path (S-007-04). No findings from other strategies' reviews were consulted (blindness preserved).
