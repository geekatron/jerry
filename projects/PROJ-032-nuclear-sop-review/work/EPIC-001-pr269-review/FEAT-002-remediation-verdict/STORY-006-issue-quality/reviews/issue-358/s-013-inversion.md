# Inversion Report: GitHub issue #358 (BUG-009 registration enforcement surfaces)

**Strategy:** S-013 Inversion Technique
**Deliverable:** `snapshots/final/issue-358.md`
**Criticality:** C4 (tournament)
**Date:** 2026-08-07
**Reviewer:** adv-executor (S-013)
**H-16 Compliance:** N/A for this blind single-strategy execution (no S-003 output supplied to this agent)
**Goals Analyzed:** 3 | **Assumptions Mapped:** 6 | **Vulnerable Assumptions:** 2 (Major), 3 (Minor)

## Summary

The issue text's factual claims (commit SHA, branch name, CI run, the 89→93 count, the H-22/L2-REINJECT gap, the "nuclear workflow" misroute mechanics) all verified exactly against the remediation register, remediation log, verdict, and commit diff — no Critical fabrication or misdirection found. Inverting the text's implicit goals ("reader can locate every cited artifact" and "reader knows what to do if they disagree") surfaces two vulnerable assumptions worth tightening before this is treated as a finished external-facing artifact. **Recommendation: ACCEPT with minor mitigations.**

## Goal Inventory

1. Reader (human or agent) understands the defect and the fix with zero repo-governance context (explicit).
2. Reader can independently verify the fix is real (explicit — "How to verify").
3. Reader knows what to do next: nothing, unless they object (explicit).

## Findings Table

| ID | Assumption / Anti-Goal | Type | Confidence | Severity | Evidence | Affected Dimension |
|----|------------------------|------|------------|----------|----------|--------------------|
| S-013-01 | The `Tracking:` path (`projects/PROJ-032-nuclear-sop-review/work/BUG-009-...` on branch `feat/proj-032-nuclear-sop-review`) is reachable by the external reader | Assumption | Low | Major | Line 14 gives a bare repo-relative path on a non-default branch, no URL, no fetch/clone instruction; nothing in the ground truth confirms this branch is pushed/visible to PR #269's contributor | Actionability |
| S-013-02 | If the reader disagrees with the fix, they know where to say so | Anti-Goal | N/A | Minor | Line 5: "Nothing for you to do unless you disagree with the fix" — no venue named (comment here? reply on PR #269?) | Actionability |
| S-013-03 | The dense (1)/(2)/(3) run-on sentence in "What was wrong" remains scannable at first read | Assumption | Medium | Minor | Line 7 packs three distinct defects into one paragraph with inline numbering, no line breaks | Actionability |
| S-013-04 | "PROJ-032/BUG-009" and "REM-09" need no gloss for a zero-context reader | Assumption | Medium | Minor | Title and line 14 use bare locator codes; harmless as IDs but unexplained | Completeness |
| S-013-05 | The one verify command captures the full remediation scope for this cluster | Assumption | High | Minor | Line 11 diffs only 2 files; register's REM-09 "Affected files" also lists the phase-6 collision-analysis artifact (annotated, not diffed) — omission doesn't mislead, just narrows the audit trail | Traceability |

## Finding Details

### S-013-01: Tracking path may be unresolvable to the external reader [MAJOR]

**Type:** Assumption
**Original Assumption:** Naming a worktracker path on `feat/proj-032-nuclear-sop-review` is sufficient for the PR author (or their agent) to locate the underlying register entry if they want more detail.
**Inversion:** If that branch is not pushed to (or visible in) the public `geekatron/jerry` remote the contributor has access to, the path is dead — the reader cannot `git show` or browse it, and has no way to know that.
**Plausibility:** Plausible — no ground-truth artifact confirms the branch is public, and the path is given without a hyperlink or fetch command (contrast with the "How to verify" section, which does give a runnable command).
**Consequence:** Low real-world impact (the Tracking line is provenance, not action-required), but violates the "resolvable references" bar the mission sets, and an agent blindly following the path will burn a tool call on a 404/not-found.
**Evidence:** `snapshots/final/issue-358.md` line 14.
**Dimension:** Actionability
**Mitigation:** Either (a) drop the repo-path form entirely and just say "tracked internally as BUG-009 / REM-09; no action needed from you," or (b) if the branch is confirmed public, give a `github.com/geekatron/jerry/blob/feat/proj-032-nuclear-sop-review/...` URL instead of a bare path.
**Acceptance Criteria:** Tracking line either contains a working URL or explicitly states the reference is internal-only and non-actionable.

### S-013-02: No stated venue for disagreement [MINOR]

**Original Assumption:** "unless you disagree with the fix" is self-explanatory.
**Inversion:** A careful reader (or an agent optimizing for minimal ambiguity) pauses to ask where a disagreement should be posted — this issue thread, or PR #269 itself.
**Consequence:** Minor friction only; GitHub convention (comment on the open issue) is a reasonable default guess.
**Mitigation:** Append "(comment on this issue if so)."

## Recommendations

- **Major:** S-013-01 — make the Tracking reference either a working link or explicitly non-actionable/internal-only.
- **Minor (MAY fix):** S-013-02 — add a one-clause pointer for the disagreement path. S-013-03 — split the numbered defects into a short list for scannability. S-013-04 — no fix required; codes are locator-only and don't block action. S-013-05 — optional: note the fix also touched the phase-6 collision-analysis artifact (annotation only) for completeness.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | Core defect/fix/verify content is complete; S-013-04 is cosmetic |
| Internal Consistency | 0.20 | Positive | Every fact cross-checks cleanly against register, log, verdict, and diff |
| Methodological Rigor | 0.20 | Neutral | N/A to this artifact type |
| Evidence Quality | 0.15 | Positive | Commit SHA, branch, CI run, and counts all verified correct |
| Actionability | 0.15 | Negative | S-013-01 (unresolvable path) and S-013-02 (no disagreement venue) both add reader friction |
| Traceability | 0.10 | Negative (minor) | S-013-05: verify command narrower than the full affected-files set |

**Result:** No Critical or fabricated claims found. 1 Major (unresolvable Tracking reference) and 4 Minor findings on actionability/polish. Text is fact-accurate and largely self-contained; tightening the Tracking section closes the main gap.
