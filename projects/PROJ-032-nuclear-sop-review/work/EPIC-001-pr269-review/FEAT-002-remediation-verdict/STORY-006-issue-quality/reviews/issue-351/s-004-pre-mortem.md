# Pre-Mortem Report: GitHub Issue #351 (BUG-002 / REM-02, PR #269)

**Strategy:** S-004 Pre-Mortem Analysis (adapted for a ~300-word communication artifact)
**Deliverable:** `snapshots/final/issue-351.md` (live text of geekatron/jerry issue #351)
**Criticality:** C4 tournament member
**Failure Scenario:** Six months from now, the contributor's AI agent read this issue, tried to act on it, and either (a) gave up because a cited reference 404'd, or (b) shipped a narrow "fix" that left the actual blocker open and PR #269 still unmergeable.

## Summary

The issue's core factual claims (tool grant, agent count, six gates, runtime-model ambiguity, STAR write-recursion) all check out against the skill source and the register. Failure risk here is not fabrication — it is **reference resolvability and completeness-of-framing**: one path lacks the branch qualifier its sibling path has, and the "blocks merge" claim doesn't disclose that six other issues gate the same merge. Recommendation: **ACCEPT with two targeted text fixes** (S-004-01, S-004-03); the rest are polish.

## Findings

| ID | Severity | Cause | Category |
|----|----------|-------|----------|
| S-004-01 | Critical | Worktracker path has no branch qualifier | Traceability |
| S-004-02 | Major | "Contradicts other documented guarantees" is unspecified | Completeness |
| S-004-03 | Major | "Blocks merge" hides that 6 other issues also gate the same merge | Process/Honesty |
| S-004-04 | Minor | "self-check before every file write" narrows the actual rule's scope | Evidence Quality |
| S-004-05 | Minor | Worktracker path has no trailing filename | Actionability |
| S-004-06 | Minor | Paths are bare relative strings, not resolvable URLs | Actionability |

### S-004-01: Worktracker path branch ambiguity [CRITICAL]

**Evidence:** "Worktracker: `projects/PROJ-032-nuclear-sop-review/work/BUG-002-user-hold-runtime-model` (register section REM-02). Full analysis ... on branch `feat/proj-032-nuclear-sop-review`."
**Why this fails:** The branch qualifier grammatically attaches only to the second (register) path. Verified: this worktracker directory exists only on `feat/proj-032-nuclear-sop-review` (confirmed on disk), not on PR #269's own branch or on `main`. A reader (or their agent) resolving the first path on the PR's branch or `main` gets a 404 and may conclude the reference is broken or invented — precisely the trust failure this whole review project is trying to avoid causing.
**Mitigation:** State the branch once, covering both paths: "Both paths below are on branch `feat/proj-032-nuclear-sop-review` (not this PR's branch): Worktracker: ... Full analysis: ..."

### S-004-02: Unspecified "documented guarantees" [MAJOR]

**Evidence:** "...or as the main-session persona (which contradicts other documented guarantees)."
**Why this fails:** Zero of the contradicted guarantees are named (verified: the register names tool-tier enforcement and verifier isolation specifically). A reader has no way to judge scope or plausibility without opening the full register — the sentence reads as an assertion with no anchor.
**Mitigation:** Name at least one example inline: "...(which would break the tool-tier enforcement and verifier-isolation guarantees documented elsewhere)."

### S-004-03: "Blocks merge" omits concurrent blockers [MAJOR]

**Evidence:** "Blocks merge of PR #269." (final sentence, stated in isolation)
**Why this fails:** True but incomplete. Verified: this is 1 of 7 concurrently open design-decision blockers (issues #350, #352–#356) gating the same merge decision. A contributor's agent reading only this issue could reasonably conclude that resolving BUG-002 alone clears PR #269 for merge, then be surprised when it doesn't.
**Mitigation:** "Blocks merge of PR #269, alongside six sibling design-decision issues (#350, #352-356) — all seven must close before merge."

### S-004-04: "file write" under-scopes the self-check rule [MINOR]

**Evidence:** "the rule 'run a self-check before every file write' is non-terminating..."
**Why this fails:** Verified against the skill's behavior rules: the self-check is mandatory before every state-modifying tool call — Write, Edit, **and Bash** — not file writes alone. A reader who takes "file write" literally could scope a fix to Write/Edit only and leave the Bash case unaddressed, even though the issue's own closing design question ("terminating scope of the self-check rule") is appropriately general.
**Mitigation:** "...before every state-modifying action (writing, editing, or running a command)..."

### S-004-05: Worktracker path has no trailing filename [MINOR]

**Evidence:** `projects/PROJ-032-nuclear-sop-review/work/BUG-002-user-hold-runtime-model` (directory, no file)
**Why this fails:** Resolvable (verified the directory and its file exist) but requires one extra navigation step to find the actual `.md` inside. Low cost, easily removed.
**Mitigation:** Append the filename: `.../BUG-002-user-hold-runtime-model/BUG-002-user-hold-runtime-model.md`.

### S-004-06: Bare relative paths instead of resolvable links [MINOR]

**Evidence:** All three cited locations are given as repo-relative path strings, not `https://github.com/geekatron/jerry/blob/{branch}/{path}` links.
**Why this fails:** An agent with zero repo context can reconstruct the URL (owner/repo are implied by "this repository," branch is named), but a direct link removes that inference step entirely and is standard GitHub-issue practice.
**Mitigation:** Render each path as a markdown link to the resolved blob URL on the stated branch.

## Scoring Impact

| Dimension | Impact | Rationale |
|-----------|--------|-----------|
| Completeness | Negative | S-004-02, S-004-03: two consequential omissions (contradiction specifics, sibling-blocker count) |
| Internal Consistency | Negative | S-004-01: branch qualifier applies inconsistently across two adjacent, parallel-structured path references |
| Evidence Quality | Neutral | Core technical claims (tool grant, agent count, six gates, write-recursion) all verified accurate |
| Actionability | Negative | S-004-01, S-004-05, S-004-06: reference friction adds lookup steps or risks dead ends |
| Traceability | Negative | S-004-01: the one path that most needs a branch anchor (the primary worktracker pointer) is the one missing it |

## Priority

**P0:** S-004-01 (branch ambiguity — fix before posting/leaving live). **P1:** S-004-02, S-004-03 (both cheap one-clause additions with real downside if omitted). **P2:** S-004-04, S-004-05, S-004-06 (polish; do not block acceptance).
