# Pre-Mortem Report: GitHub Issue #361 (BUG-012 / REM-12)

**Strategy:** S-004 Pre-Mortem Analysis
**Deliverable:** `snapshots/final/issue-361.md` (live text of geekatron/jerry issue #361)
**Criticality:** C4 (tournament)
**H-16 Note:** Executed as an independent blind strategy per orchestration design (not chained after a same-issue S-003 pass in this run).
**Failure Scenario:** It is 2027-02. The PR #269 author's AI agent read issue #361, tried to act on it autonomously, and either (a) reported the PR as fully mergeable, (b) stalled on the verify step, or (c) had no path to register disagreement — wasting a review cycle even though the fix itself was correct and already applied.

## Summary

Fact-checked every claim against the remediation register (REM-12), the full `c07033ce` diff, and the live PR-branch worktree: **all technical claims (three-way state-machine divergence, WAIVED-outcome gap, COMPLETED-before-capture ordering, boolean/path type mismatch, SEC-008 fail-open verifier) are accurate**, and the fix description matches the actual diff. No Critical (factually-wrong) failure causes found. Six Major/Minor causes concern **what the text omits or leaves ambiguous for an autonomous reader acting without further lookup** — chiefly, the absence of any signal that six other blockers still keep the PR unmergeable, and no defined path if the contributor disagrees with the change. Recommendation: **ACCEPT with two Major mitigations.**

## Findings Table

| ID | Failure Cause | Category | Likelihood | Severity | Priority |
|----|---------------|----------|------------|----------|----------|
| S-004-01 | No cross-reference to 6 open DEFER-REWORK blockers (#350–#356); reader may conclude PR is mergeable | Assumption | Medium-High | Major | P1 |
| S-004-02 | No defined action for "if you disagree with the fix" | Process | Medium | Major | P1 |
| S-004-03 | Verify command assumes `c07033ce`/parent already fetched locally; no fallback if absent or history rewritten | Technical | Medium | Major | P1 |
| S-004-04 | Tracking path points to a directory, not the leaf file; branch may not be casually browsable | Assumption | Low | Minor | P2 |
| S-004-05 | Stray blank `Assignees:` line reads as unfinished template artifact | Process | Low | Minor | P2 |
| S-004-06 | "What was wrong" packs 3 defects into one dense run-on paragraph, harder to parse deterministically than a list | Process | Low | Minor | P2 |

## Finding Details

### S-004-01: Missing PR-disposition context [MAJOR]

**Failure Cause:** The text states this is "one of seven mechanical fixes" but never mentions that seven *other* clusters (issues #350–#356) are open, unrelated, and — per the verdict — currently block merge ("REWORK — do not merge"). An agent reading only #361 has no signal the PR is still blocked.
**Evidence:** Issue body, "What this is" line; absent anywhere in the issue. Confirmed against `pr269-verdict.md` L0 recommendation ("REWORK... seven named design defects... block merge").
**Mitigation:** Append one sentence to "Tracking": "Six other structural blockers (issues #350–#356) are unrelated to this fix and remain open; they — not this issue — currently block merge."
**Acceptance Criteria:** Reader of #361 alone can correctly state PR #269's overall merge status.

### S-004-02: No disagreement procedure [MAJOR]

**Failure Cause:** "Nothing for you to do unless you disagree with the fix" defines a condition but not an action. An agent that disagrees has no instructed next step (comment? revert? new issue?).
**Evidence:** "What this is" closing sentence; no procedure stated anywhere in the issue.
**Mitigation:** Add: "If you disagree, comment on this issue with your concern before PR #269's disposition is decided."
**Acceptance Criteria:** Issue states a concrete action for the disagreement path.

### S-004-03: Verify step has no fallback [MAJOR]

**Failure Cause:** `git diff c07033ce^ c07033ce -- skills/nuclear-sop/` requires the commit and its parent to already be present in the reader's local clone. No `git fetch` instruction is given, and if the branch is later rebased/force-pushed the SHA could stop resolving — leaving an autonomous agent with only one, now-broken, verification path.
**Evidence:** "How to verify" section; confirmed the worktree used for this review already has the commit locally (obtained separately), so the gap is in the instruction, not the fact.
**Mitigation:** Add a fallback: link to `https://github.com/geekatron/jerry/commit/c07033ce` (works without a local clone) alongside the `git diff` command.
**Acceptance Criteria:** At least one verification method in the issue requires no local git state.

### S-004-04: Tracking path/branch reachability [MINOR]

**Failure Cause:** The worktracker path names a directory (`work/BUG-012-state-machine-contract`) rather than the file inside it, and the branch (`feat/proj-032-nuclear-sop-review`) is a maintainer-side project branch the contributor may not think to check out or browse.
**Evidence:** "Tracking" paragraph. Directory confirmed to exist with exactly one file, `BUG-012-state-machine-contract.md`, inside it.
**Mitigation:** Append `/BUG-012-state-machine-contract.md` to the path.
**Acceptance Criteria:** Path resolves directly to a file, not a listing.

### S-004-05: Stray metadata line [MINOR]

**Failure Cause:** `Assignees: ` appears blank immediately under the title, reading as an unfinished template field rather than intentional content.
**Evidence:** Line 3 of the snapshot.
**Mitigation:** Remove the empty line or assign an owner.
**Acceptance Criteria:** No empty labeled fields precede the body text.

### S-004-06: Dense run-on defect list [MINOR]

**Failure Cause:** Item (1) of "What was wrong" embeds two sub-facts (divergent transitions; missing WAIVED value) after an em-dash inside a single numbered clause, alongside items (2) and (3) written as long single sentences — harder for a parsing agent to split into discrete, independently-verifiable facts than an explicit sub-list.
**Evidence:** "What was wrong" paragraph, item (1).
**Mitigation:** Break into three top-level bullets, each with its own sub-bullets, rather than inline `(1)/(2)/(3)` prose.
**Acceptance Criteria:** Each distinct defect is its own list item.

## Recommendations

**P1 (should mitigate before/while issue stays open):** S-004-01 (add blocker cross-reference), S-004-02 (add disagreement procedure), S-004-03 (add commit-link fallback).
**P2 (polish, optional):** S-004-04 (file-level path), S-004-05 (drop blank Assignees line), S-004-06 (bulletize defect list).

## Scoring Impact

| Dimension | Impact | Rationale |
|-----------|--------|-----------|
| Completeness | Negative | S-004-01, S-004-02: PR-status and disagreement-path context missing |
| Internal Consistency | Neutral | No contradictions found; all claims verified against register/diff/worktree |
| Evidence Quality | Positive | All fact claims verified true against ground truth (state machine, WAIVED, ordering, type mismatch, SEC-008) |
| Actionability | Negative | S-004-02, S-004-03: no defined disagreement action; single verify path with no fallback |
| Traceability | Negative | S-004-04: tracking link one level too shallow |

## Execution Statistics
- **Total Findings:** 6
- **Critical:** 0
- **Major:** 3
- **Minor:** 3
