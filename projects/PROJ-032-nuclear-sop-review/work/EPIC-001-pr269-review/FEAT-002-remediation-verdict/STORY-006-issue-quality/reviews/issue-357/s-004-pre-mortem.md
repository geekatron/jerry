# Pre-Mortem Report: GitHub Issue #357 (BUG-008 — registration/status truth)

**Strategy:** S-004 Pre-Mortem Analysis (adapted for a communication artifact)
**Deliverable:** `projects/PROJ-032-nuclear-sop-review/.../STORY-006-issue-quality/snapshots/final/issue-357.md`
**Criticality:** C4 tournament
**H-16 note:** No prior S-003 output was provided to this agent for this issue; findings below are produced directly against the artifact per the executor's task scope.

**Failure scenario:** It is one week later. PR #269's author's AI agent read issue #357, tried to follow "How to verify" literally, and either (a) failed with `fatal: bad revision 'c07033ce^'` because its clone never fetched the maintainer's push, or (b) ran the exact diff command shown, saw only 2 files change, and told the author "verified" — missing that the issue's own "what changed" claim spans 4 files. The author now has partial, unverifiable confidence in a Critical-severity governance claim (C3+ approval status).

## Findings

| ID | Cause | Category | Likelihood | Severity | Priority |
|----|-------|----------|------------|----------|----------|
| S-004-01 | Verify step is git-CLI-only; no clickable commit/compare link for agents without local clone access | Technical | Medium | Major | P1 |
| S-004-02 | Verify command's file list (2 files) is narrower than the fix's claimed scope (4 files) | Assumption | High | Major | P0 |
| S-004-03 | Verify command assumes local branch already fetched; no fetch/pull instruction given | Process | Medium | Minor | P2 |
| S-004-04 | Title says "risk levels", body says "criticality levels" for the same concept | Assumption | Low | Minor | P2 |
| S-004-05 | "Unless you disagree with the fix" gives no channel for disagreement | Process | Low | Minor | P2 |
| S-004-06 | "Two entry-point documents" undercounts where the false claim actually lived | Evidence | Low | Minor | P2 |

### S-004-02 [MAJOR, P0] — Verify command doesn't cover the fix's full claimed scope

**Failure cause:** "What the fix changed" asserts the C1-C2 restriction is now "stated identically in SKILL.md, PLAYBOOK.md, the rules file, and the reference docs" (4 files) — confirmed true against ground truth (`skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md` NS-H-08 and `skills/nuclear-sop/docs/reference.md` NS-H-08 row were both also corrected in `c07033ce`). But "How to verify" only diffs `SKILL.md` and `PLAYBOOK.md`. A reader following the instructions literally sees 2 of the 4 corrected files and cannot confirm the "stated identically" claim.
**Likelihood:** High — this is the literal, only verification path given.
**Mitigation:** Extend the command: `git diff c07033ce^ c07033ce -- skills/nuclear-sop/SKILL.md skills/nuclear-sop/PLAYBOOK.md skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md skills/nuclear-sop/docs/reference.md`.
**Acceptance criteria:** Verify command's path list matches the file list named in "What the fix changed."

### S-004-01 [MAJOR, P1] — No link-based verification path

**Failure cause:** The sole verification method is a local `git diff`. An AI agent operating purely via GitHub's web/API surface (no repo clone, e.g. WebFetch-only tooling) cannot execute it and has no fallback.
**Mitigation:** Add a direct link alongside the command, e.g. `https://github.com/geekatron/jerry/commit/c07033ce` (or a compare view scoped to the two/four paths above), so both CLI-capable and web-only agents can verify.
**Acceptance criteria:** Issue contains at least one clickable, resolvable URL for verifying the diff, not only a shell command.

### S-004-03 [MINOR, P2] — Fetch precondition unstated

**Failure cause:** `c07033ce^` resolution fails with `fatal: bad revision` on a clone that hasn't fetched the maintainer's push to `proj-0039-nuclear-engineer`.
**Mitigation:** Prefix with `git fetch origin proj-0039-nuclear-engineer && ` or note "after fetching your branch."

### S-004-04 [MINOR, P2] — Title/body term mismatch

**Failure cause:** Title: "approved for all risk levels"; body: "approved for all criticality levels" (with the framework's-risk-tiers gloss attached only to the body term). Same concept, two labels.
**Mitigation:** Use "criticality levels" in both, or gloss the title term too.

### S-004-05 [MINOR, P2] — No disagreement channel named

**Failure cause:** "Nothing for you to do unless you disagree with the fix" doesn't say where/how to disagree.
**Mitigation:** Add ", by commenting on this issue" (or the PR review thread) after "disagree with the fix."

### S-004-06 [MINOR, P2] — "Two entry-point documents" undercounts affected files

**Failure cause:** "What was wrong" frames the contradiction as living in "two entry-point documents" (SKILL.md, PLAYBOOK.md), but ground truth shows the same false "approved for all criticality levels" line also existed verbatim in the rules file (`nuclear-sop-behavior-rules.md` NS-H-08) and the reference docs (`docs/reference.md` NS-H-08 row) — i.e., 3 files carried the false claim, 1 (PLAYBOOK.md) carried the contradicting-but-correct claim.
**Mitigation:** "the skill's entry-point documents and their supporting rules/reference files" or state the count explicitly.

## What Held Up (no finding needed)

Verified accurate against ground truth: the "five files" registration list (CLAUDE.md:78, AGENTS.md, mandatory-skill-usage.md, `.claude-plugin/plugin.json`, CHANGELOG.md — all confirmed present in the PR worktree); the verbatim "NOT registered and NOT live-routable" quote; the PLAYBOOK.md-vs-SKILL.md contradiction; the CI link and 15/15 result; the `c07033ce` short-SHA; the worktracker tracking path; the cross-reference to issue #353 (QG-E4 invalidation, confirmed consistent with the #353 snapshot).

## Scoring Impact

| Dimension | Impact | Rationale |
|-----------|--------|-----------|
| Evidence Quality | Negative | S-004-02, S-004-06: verification scope narrower than claimed scope |
| Actionability | Negative | S-004-01, S-004-03, S-004-05: agent/human cannot fully self-serve verification or next steps |
| Internal Consistency | Negative | S-004-04, S-004-06: title/body term drift; document-count drift |
| Completeness | Neutral | Core narrative (what/why/fix/tracking) is present |
| Methodological Rigor | Neutral | n/a for this artifact type |
| Traceability | Positive | Commit SHA, CI run, worktracker path, and issue cross-reference all resolve |

## Execution Statistics
- **Total Findings:** 6
- **Critical:** 0
- **Major:** 2
- **Minor:** 4
