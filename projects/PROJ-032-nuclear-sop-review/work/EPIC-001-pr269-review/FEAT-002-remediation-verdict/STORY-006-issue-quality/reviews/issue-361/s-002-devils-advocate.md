# Devil's Advocate Report: GitHub Issue #361 (BUG-012 state-machine/completion contract)

**Strategy:** S-002 Devil's Advocate
**Deliverable:** `snapshots/final/issue-361.md` (live text of geekatron/jerry issue #361)
**Criticality:** C4 (tournament execution)
**Date:** 2026-08-07
**Reviewer:** adv-executor (S-002)
**H-16 Note:** No S-003 Steelman output was provided to this execution instance (blind, single-strategy invocation). Per this tournament's documented group ordering (steelman group precedes challenge group), H-16 compliance is assumed satisfied at the orchestration level; this instance could not independently confirm it. Findings below stand regardless of Steelman status — they are text-level critiques verifiable against ground truth.

## Summary

Fact-checked every substantive claim in issue #361 against the remediation register (REM-12), the fix commit evidence pack, and the live PR-branch worktree — **all claims verified accurate** (state-machine divergence, completion-contract type break, verifier fail-open gap, and the "fixed on your branch" status all match ground truth exactly, including the branch name, commit SHA, and CI run link). No Critical findings. 3 counter-arguments identified (0 Critical, 1 Major, 2 Minor), all targeting actionability/self-containedness rather than factual accuracy. Recommend ACCEPT with one targeted revision (S-002-01).

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| S-002-01 | "How to verify" diff command is unscoped to this defect | Major | Line 11: `git diff c07033ce^ c07033ce -- skills/nuclear-sop/` | Actionability |
| S-002-02 | Unexplained internal shorthand adds no information | Minor | Title "PROJ-032/BUG-012:"; body "(its SEC-008 item)" | Concision / Self-Containedness |
| S-002-03 | Cross-branch doc reference will go stale after merge | Minor | Line 14: "on branch `feat/proj-032-nuclear-sop-review`" | Resolvable References |

## Finding Details

### S-002-01: Verification command doesn't isolate the described defect [MAJOR]

**Claim Challenged:** "How to verify: on `proj-0039-nuclear-engineer`, run `git diff c07033ce^ c07033ce -- skills/nuclear-sop/`."

**Counter-Argument:** Commit `c07033ce` is a single squashed commit implementing **all seven** FIX-NOW clusters (REM-08..14), touching 29 files (confirmed via `evidence-c07033ce.md` commit stat: 498 insertions / 197 deletions across registration text, schema fixes, composition drift, nav tables, and the state-machine/completion fix this issue describes). The path filter `-- skills/nuclear-sop/` still leaves ~20+ files from REM-08, REM-10, REM-11, REM-13, and REM-14 in the diff output. A reader who runs the given command to verify *this specific* fix must manually hunt through unrelated schema, registration, and composition-drift hunks to find the ~5 files that actually implement REM-12.

**Impact:** Forces an extra lookup/filtering step on every reader who wants to verify the claim as stated — directly weakens the "resolvable references / actionable verification" quality this line exists to provide.

**Dimension:** Actionability

**Response Required:** Narrow the path filter to the files REM-12 actually touches.

**Acceptance Criteria:** Replace the command with:
`git diff c07033ce^ c07033ce -- skills/nuclear-sop/templates/PROCEDURE_STATE.template.yaml skills/nuclear-sop/agents/sop-executor.md skills/nuclear-sop/agents/sop-capture.md skills/nuclear-sop/agents/sop-verifier.md skills/nuclear-sop/composition/sop-verifier.prompt.md`

### S-002-02: Internal shorthand carries no marginal information [MINOR]

**Claim Challenged:** Title prefix `"PROJ-032/BUG-012:"`; body clause `"(its SEC-008 item)"`.

**Counter-Argument:** The title tag is a maintainer-internal worktracker cross-reference meaningless to an external reader (it doesn't block understanding, since the substantive explanation follows in plain language, but it's dead weight at the one place — the title — that must convey the most with the fewest words). Similarly, `"(its SEC-008 item)"` restates, in an unexplained internal code, a defect already fully described one clause earlier ("the exact fail-open gap the PR's own compliance gate had flagged as remediation-required"). Removing it loses zero information for this audience.

**Response Required:** Drop `"(its SEC-008 item)"` entirely; consider moving `PROJ-032/BUG-012` to a trailing parenthetical or omitting it (GitHub's own issue number already serves as the unique identifier).

**Acceptance Criteria:** Body reads identically without the parenthetical; title's plain-language portion is unchanged.

### S-002-03: Tracking reference points to a branch that will not outlive this review [MINOR]

**Claim Challenged:** "register section REM-12 in `remediation-register.md` ... on branch `feat/proj-032-nuclear-sop-review`."

**Counter-Argument:** Verified via GitHub API that `feat/proj-032-nuclear-sop-review` currently exists and is resolvable (latest commit `b2cf2966`, 2026-08-07) — the reference is accurate **today**. But this is the maintainer's internal review branch, not the reader's PR branch (`proj-0039-nuclear-engineer`); once it merges to `main` (the normal lifecycle for a review branch) it will typically be deleted, silently breaking this specific citation for anyone who follows it later.

**Response Required:** Add a one-line fallback so the reference survives the branch's eventual deletion.

**Acceptance Criteria:** Append "(or under the same path on `main` once this review branch merges)" to the tracking sentence.

## Recommendations

- **P1 (Major — should resolve):** S-002-01 — rescope the verify command to REM-12's actual files.
- **P2 (Minor — acknowledgment sufficient):** S-002-02 — drop the two internal-code fragments that add no information for this audience.
- **P2 (Minor — acknowledgment sufficient):** S-002-03 — add a post-merge fallback to the cross-branch tracking reference.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | All three defects and their fixes are fully and correctly described |
| Internal Consistency | 0.20 | Neutral | No contradictions between "what was wrong" and "what the fix changed" |
| Methodological Rigor | 0.20 | Neutral | N/A to this artifact type |
| Evidence Quality | 0.15 | Positive | Every factual claim independently verified against register, diff evidence, and live worktree — zero discrepancies found |
| Actionability | 0.15 | Negative | S-002-01: verify command requires manual filtering to reach the relevant 5 files |
| Traceability | 0.10 | Negative | S-002-03: one tracking reference is branch-pinned and will go stale post-merge |

**Result:** No Critical findings; this is among the more factually solid issues in the batch. The single Major finding (S-002-01) is a low-cost, high-value fix (one command edit) that would materially improve reader verification experience.
