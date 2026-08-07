# Inversion Report: GitHub Issue #350 (PROJ-032/BUG-001)

**Strategy:** S-013 Inversion Technique
**Deliverable:** `projects/PROJ-032-nuclear-sop-review/work/EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-006-issue-quality/snapshots/final/issue-350.md`
**Criticality:** C4 (tournament) | **Date:** 2026-08-07
**Goals Analyzed:** 3 | **Assumptions Mapped:** 6 | **Vulnerable Assumptions:** 4

## Summary

The issue text accurately restates REM-01's substance (delegation-topology conflict, missing suspend/resume, hop-ceiling breach, acceptable descope) with no internal jargon leaking through, and its severity/status framing matches the register exactly. Stress-testing the text's implicit "every reference resolves" assumption found one confirmed broken reference (empirically verified against the PR #269 worktree) and one quotation-fidelity gap. Recommendation: REVISE (targeted fix to one line; rest is sound).

## Findings

| ID | Assumption / Anti-Goal | Confidence | Severity | Evidence |
|----|------------------------|------------|----------|----------|
| S-013-01 | "A reader who follows the bare `Worktracker:` path will find it" | High (confirmed false) | Critical | Path `projects/PROJ-032-nuclear-sop-review/work/BUG-001-qg-hold-delegation-topology` carries **no branch qualifier**, unlike the very next sentence which tags `remediation-register.md` with `on branch feat/proj-032-nuclear-sop-review`. Verified empirically: `projects/PROJ-032*` does not exist anywhere in the checked-out PR #269 branch worktree (glob returned zero matches); the path only exists on `feat/proj-032-nuclear-sop-review`. An external contributor/agent operating from the PR branch (the only branch they have context for) will 404 on this path with no signal to try a different branch. |
| S-013-02 | "The quoted clause is what the file actually says" | Medium | Major | Issue quotes `"cannot invoke any other agent"` as if verbatim. `skills/nuclear-sop/agents/sop-executor.md:77` actually reads: *"It cannot spawn subagents, delegate to sop-verifier, or invoke any other agent."* The quoted fragment is a trimmed paraphrase, not a contiguous substring — an agent grepping the file for the exact quoted string to verify the claim gets a false negative. |
| S-013-03 | "`PROJ-032/BUG-001` in the title needs no gloss" | High | Minor | The title embeds this code before the reader has seen the Worktracker line that maps it to a path. Not blocking (body clarifies it a few lines down) but adds a moment of unexplained-code friction on first read. |
| S-013-04 | "'Three-handoff routing ceiling' is self-evidently authoritative" | Medium | Minor | No source/rationale given for why 3 is the ceiling or what enforces it; register's underlying evidence file (skill-integration-analysis.md) is itself flagged as "not shipped or citable" (REM-01 G4), so the issue correctly avoids citing it — but the bare assertion still asks the reader to take the ceiling on faith. Acceptable at this word budget; noted for completeness. |

## Finding Detail — S-013-01 [CRITICAL]

**Type:** Anti-goal (unaddressed resolvable-reference requirement)
**Inversion:** "What would guarantee a reader can't find the tracked item?" → omit the branch tag on exactly one of two adjacent internal paths, in a text explicitly written for readers with zero repo/branch context.
**Consequence:** Broken navigation on the issue's primary "go read more" pointer; an AI agent following it programmatically fails silently or reports a false "not found."
**Mitigation:** Append the same branch qualifier used for the register path, e.g.: "Worktracker: `projects/PROJ-032-nuclear-sop-review/work/BUG-001-qg-hold-delegation-topology` (register section REM-01), on branch `feat/proj-032-nuclear-sop-review` of this repo — not part of PR #269's own branch." **Acceptance criteria:** both paths in the Tracking line carry an explicit, identical branch qualifier.

## Finding Detail — S-013-02 [MAJOR]

**Mitigation:** Replace with the full verbatim clause and matching quotation marks: `"It cannot spawn subagents, delegate to sop-verifier, or invoke any other agent."` (or drop the quote marks and paraphrase without implying a direct quote). **Acceptance criteria:** quoted text is a byte-exact substring of `sop-executor.md`.

## Scoring Impact

| Dimension | Impact | Rationale |
|-----------|--------|-----------|
| Evidence Quality | Negative | S-013-02: misquotation weakens claim verifiability |
| Traceability | Negative | S-013-01: unresolvable reference breaks the traceability chain to source artifacts |
| Actionability | Neutral | Redesign question and descope option remain clear and unaffected |
| Completeness | Neutral | Minor gaps only (S-013-03/04) |
