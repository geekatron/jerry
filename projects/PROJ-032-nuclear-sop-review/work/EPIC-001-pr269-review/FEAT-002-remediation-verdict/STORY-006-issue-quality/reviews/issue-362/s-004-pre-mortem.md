# Pre-Mortem Report: GitHub Issue #362 (BUG-013 composition drift)

**Strategy:** S-004 Pre-Mortem Analysis (adapted for a ~300-word communication artifact)
**Deliverable:** `issue-362.md` (live text of geekatron/jerry issue #362)
**Criticality:** C4 tournament member
**Failure Scenario:** Six months from now, PR #269's external contributor (or their agent) read issue #362, acted on its literal text, and something went wrong: either they wasted a cycle on a decision that wasn't theirs to make yet, or a copy-pasted command failed on their machine, or they closed the loop believing more of PR #269 was settled than actually was.

## Summary

Fact-checking against the remediation register (REM-13), the evidence pack diff, and the live PR worktree confirms the issue's substantive claims (branch, commit, cluster count, guard-strength drift, line counts, CI link, tracking path) are all accurate. No Critical (factually-wrong) findings. Two Major actionability gaps and three Minor polish gaps were found via prospective hindsight. **Recommendation: ACCEPT with minor mitigations** — the text is honest and well-evidenced; the failure modes below are about a reader's next action, not about truth.

## Findings Table

| ID | Failure Cause | Category | Likelihood | Severity | Priority | Affected Dimension |
|----|---------------|----------|------------|----------|----------|--------------------|
| S-004-01 | "Nothing to do" contradicted by "yours to decide during rework" in the same sentence | Process | Medium | Major | P1 | Actionability |
| S-004-02 | Verify command assumes the commit is already fetched locally | Technical | Medium | Major | P1 | Actionability |
| S-004-03 | "which is what plugin.json actually loads" omits that Claude Code also loads the same pair | Assumption | Low | Minor | P2 | Completeness |
| S-004-04 | Only SKILL.md named as mislabeling composition/ "canonical"; PLAYBOOK.md had the identical label | Assumption | Low | Minor | P2 | Completeness |
| S-004-05 | "runtime self-delegation check" under-names the restored block, which also re-asserts read-only (no Write/Edit/Bash) | Technical | Low | Minor | P2 | Evidence Quality |

## Finding Details

### S-004-01: "Nothing to do" vs. "yours to decide" [MAJOR]

**Failure Cause:** Line 5 reads: "Nothing for you to do unless you disagree — though whether the `composition/` copies should exist at all is yours to decide during rework." The first clause tells the reader (or their agent triaging a backlog of issues) to take no action; the second clause immediately hands them an open decision. An agent parsing this for a task list will either drop the decision point entirely (never revisits whether to delete `composition/`) or treat it as an immediate action item and start deleting files unprompted mid-review — neither matches the register's actual intent ("the contributor's call in rework," i.e., later, during the DEFER-REWORK redesign pass, not now).
**Category:** Process
**Likelihood:** Medium — this is exactly the kind of soft, deferred instruction that gets lost or over-executed by an agent working from issue text alone.
**Severity:** Major — degrades actionability without being factually wrong.
**Evidence:** Issue line 5; confirmed against remediation-register.md REM-13 ("If the contributor prefers to delete `composition/` instead, that is their call in rework; the default maintainer action is sync + relabel").
**Mitigation:** Split into two sentences with an explicit trigger: "No action needed on this issue right now. Later, when you take up the DEFER-REWORK items (issues #350-#356), you may choose to delete `composition/` entirely instead of keeping it synced — that decision is deferred to that pass, not this one."
**Acceptance Criteria:** Text no longer places a live decision inside a "nothing to do" sentence; the decision has a named trigger (which future issue/pass revisits it).

### S-004-02: Verify command has an unstated fetch prerequisite [MAJOR]

**Failure Cause:** "How to verify" tells the reader to run `git diff c07033ce^ c07033ce -- ...` "on `proj-0039-nuclear-engineer`" directly. The commit was pushed by the maintainer, not the contributor — if the contributor's local clone hasn't fetched since, this fails with `unknown revision or path not in the working tree`, and neither a human skimming nor an agent executing verbatim is told to fetch first.
**Category:** Technical
**Likelihood:** Medium — first thing many contributors would try after reading this issue.
**Severity:** Major — a copy-pasted command that fails on a fresh checkout is exactly the "commands work" failure mode the mission calls out.
**Evidence:** Issue line 11; no `git fetch`/`git pull` step precedes the `git diff` instruction anywhere in the issue.
**Mitigation:** Prepend: "After fetching the branch (`git fetch origin proj-0039-nuclear-engineer`), run: ..."
**Acceptance Criteria:** The verify command sequence succeeds on a clone that has not yet seen `c07033ce`.

## Recommendations

- **P1 (S-004-01):** Rewrite the "nothing to do" sentence to separate "no action now" from the deferred `composition/`-deletion decision, naming when that decision resurfaces.
- **P1 (S-004-02):** Add a `git fetch` step before the `git diff` verification command.
- **P2 (S-004-03, S-004-04):** Optional polish — add "and Claude Code" after "plugin.json," and "and PLAYBOOK.md" after "SKILL.md," to match the fuller record in the register without materially lengthening the issue.
- **P2 (S-004-05):** Optional — rename "runtime self-delegation check" to "runtime self-check (delegation + read-only enforcement)" for closer traceability to the restored block.

## Scoring Impact

| Dimension | Impact | Rationale |
|-----------|--------|-----------|
| Completeness | Neutral | Core claims (7 clusters, 3-strength guard drift, dropped verifier content, line counts) are all present and accurate; only cross-file completeness (PLAYBOOK.md, Claude Code) is missing. |
| Internal Consistency | Negative | S-004-01: "nothing to do" directly abuts an open decision in the same sentence. |
| Methodological Rigor | Neutral | N/A at this artifact size. |
| Evidence Quality | Positive | Every checked claim (branch, commit, line counts 324/214→261, CI run, worktracker path) verified true against the register, evidence pack, and live PR worktree. |
| Actionability | Negative | S-004-01, S-004-02 both degrade the reader's ability to act correctly without guessing. |
| Traceability | Positive | Tracking footer correctly cites the register section and worktracker path; both resolve. |

## Execution Statistics
- **Total Findings:** 5
- **Critical:** 0
- **Major:** 2
- **Minor:** 3
- **Protocol Steps Completed:** 6 of 6
