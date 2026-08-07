# FMEA Report: GitHub Issue #362 (BUG-013 composition drift)

**Strategy:** S-012 FMEA (Failure Mode and Effects Analysis)
**Deliverable:** `snapshots/final/issue-362.md` (live text of GH issue #362, geekatron/jerry)
**Criticality:** C4 (tournament)
**Date:** 2026-08-07
**Reviewer:** adv-executor (S-012)
**H-16 Compliance:** N/A for this blind single-strategy execution (steelman not chained here)
**Elements Analyzed:** 6 (Title, What-this-is, What-was-wrong, What-the-fix-changed, How-to-verify, Tracking) | **Failure Modes Identified:** 4 | **Total RPN:** 468

## Summary

Fact-checked every quantitative and structural claim in the issue text (line counts, file lists, commit hash, branch, CI link, SEC-001 behavior deltas, "canonical"→"derived artifact" relabel) against the remediation register, remediation log, and the full `c07033ce` diff — all check out; **no factual or misleading claims found (zero Critical findings)**. The gaps found are all missing-context/actionability friction (Major/Minor per the task's severity rubric): the "How to verify" command is scoped too broadly for the single-issue claim it supports, and a few internal terms/paths lack the last mile of self-containedness. **Recommendation: ACCEPT with one targeted revision** (S-012-01).

## Findings Table

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Corrective Action | Affected Dimension |
|----|---------|-------------|---|---|---|-----|----------|--------------------|--------------------|
| S-012-01 | How to verify | Suggested `git diff` scope (`composition/`, `agents/`, `SKILL.md`) is shared by 4 other FIX-NOW clusters (REM-08/09/10/12) in the *same* commit `c07033ce`; running it surfaces unrelated hunks (reasoning_effort additions, state-machine rewrites, registration text) with no note distinguishing them from this bug's fix | 5 | 10 | 6 | 300 | Major | Add one sentence noting the commit is shared across 6 sibling issues (#357-361, #363) and point to the specific tells for *this* bug: the `DERIVED ARTIFACT` header comments in `composition/*`, the SEC-001 `STOP-WORK` restoration, and the PLAYBOOK.md/SKILL.md "(canonical format)"→"(derived artifacts)" relabel | Actionability |
| S-012-02 | Tracking | Worktracker reference given as a directory (`.../work/BUG-013-composition-drift`) rather than the actual file (`.../BUG-013-composition-drift/BUG-013-composition-drift.md`) — a zero-context reader following the path literally gets a directory, not a document | 3 | 8 | 4 | 96 | Major | Append the filename: `.../BUG-013-composition-drift/BUG-013-composition-drift.md` | Traceability |
| S-012-03 | What was wrong | "the caller-responsibility notice," "the entire context-isolation contract," and "the runtime self-delegation check" are named as dropped content but never glossed — a reader with zero repo context can't judge why any of the three matter | 3 | 7 | 5 | 105 | Minor | Add a 4-8 word parenthetical per term, e.g. "the context-isolation contract (what the orchestrator must withhold from the verifier's prompt)" | Completeness |
| S-012-04 | What this is | "yours to decide during rework" uses "rework" as if self-evident; it is actually this review's internal DEFER-REWORK disposition label, applied to a *different* set of 7 sibling issues (#350-356), not to this one | 2 | 6 | 6 | 72 | Minor | Replace with plain language, e.g. "yours to decide if you redesign the agent-packaging pipeline later" | Completeness |

**Severity note:** bands above follow the task-specific rubric (Critical = factually wrong/misleading/wrong-path; Major = missing context forcing a lookup; Minor = polish), not the template's generic RPN≥200 cutoff — S-012-01's RPN is high on paper but does not mislead, so it is scored Major.

## Finding Details

### S-012-01: Verify command scope bleeds across sibling issues

**Element:** How to verify (final paragraph before Tracking).
**Failure Mode:** The command `git diff c07033ce^ c07033ce -- skills/nuclear-sop/composition/ skills/nuclear-sop/agents/ skills/nuclear-sop/SKILL.md` is accurate and will run — but per `evidence-c07033ce.md`'s commit stat, all 29 changed files across REM-08 through REM-14 landed in this one commit, and `agents/*.governance.yaml` (REM-10 reasoning_effort), `agents/sop-executor.md`/`sop-capture.md`/`sop-verifier.md` (REM-12 state-machine/`execution_log_final` contract), and `SKILL.md` (REM-08 registration text) all fall inside the requested paths. A verifier following only this issue's instructions will see a diff several times larger than the composition-drift fix and has no textual cue for which hunks answer *this* bug.
**Effect:** Forces a manual lookup (cross-referencing the register or the other 6 issues) to isolate the relevant evidence; risks the external agent concluding the fix is broader or narrower than it is.
**S/O/D rationale:** S=5 (confusion, not a wrong conclusion, since all shown content is true); O=10 (guaranteed on every run, by construction of the shared commit); D=6 (not obvious without diffing against the register).
**Corrective Action:** One added sentence naming the shared-commit fact and 2-3 concrete greppable tells for this bug specifically (e.g., `grep -rn "DERIVED ARTIFACT" skills/nuclear-sop/composition/`).
**Acceptance Criteria:** Revised text lets a reader distinguish REM-13-scoped hunks from sibling-cluster hunks without leaving the issue.
**Post-Correction RPN estimate:** ~60 (D drops to 2 once the disambiguating pointer is present).

## Recommendations

1. **[Major, S-012-01]** Add the shared-commit disclosure + greppable tells to "How to verify." Highest RPN; directly reduces verifier lookup cost.
2. **[Minor, S-012-02]** Append the `.md` filename to the worktracker path.
3. **[Minor, S-012-03]** Gloss the three dropped-content nouns in "What was wrong" with short parentheticals.
4. **[Minor, S-012-04]** Replace bare "rework" with plain language disambiguating it from the DEFER-REWORK issue set.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative (minor) | S-012-03/04: three technical nouns and one disposition term left unglossed |
| Internal Consistency | 0.20 | Neutral | No contradictions found between issue text and ground truth |
| Methodological Rigor | 0.20 | Neutral | N/A to this artifact type |
| Evidence Quality | 0.15 | Positive | All quantitative claims (line counts, commit hash, CI link, file lists) verified exact-match against evidence pack |
| Actionability | 0.15 | Negative | S-012-01: verify step requires external disambiguation to execute cleanly |
| Traceability | 0.10 | Negative (minor) | S-012-02: worktracker reference resolves to a directory, not a document |

---
*Total findings: 4 (0 Critical, 1 Major, 3 Minor — using task-specific severity rubric)*
