# Red Team Report: GitHub Issue #351 (BUG-002 / REM-02)

**Strategy:** S-001 Red Team Analysis (adapted, communication-artifact scope)
**Deliverable:** `snapshots/final/issue-351.md` (~190-word issue body + tracking line)
**Criticality:** C4
**Date:** 2026-08-07
**Threat Actor:** An external contributor (or their coding agent) with zero Jerry-governance context, acting on this issue text alone, under time pressure, who will follow the first path/link that looks authoritative rather than cross-checking every reference.

## Summary

The issue's factual claims check out against the remediation register and BUG-002 worktracker entity — no fabrication found. The attack surface is entirely in **reference resolvability**: the tracking line mixes a bare, branch-less path with a branch-qualified path in the same sentence, omits full GitHub URLs the source artifacts already provide, never states that the cited paths live outside the PR's own branch, and compresses an 8-sub-defect design question down to 3 without flagging the compression. Recommendation: **REVISE** (targeted, not structural).

## Findings Table

| ID | Attack Vector | Category | Exploitability | Severity |
|----|---------------|----------|-----------------|----------|
| S-001-01 | Worktracker path has no branch tag; the register path in the same sentence does | Ambiguity | High | Critical |
| S-001-02 | Raw relative paths, no full GitHub URLs, despite source docs (BUG-002 itself) using them | Dependency | Medium | Major |
| S-001-03 | Never states the cited artifacts live outside the PR's own branch (`proj-0039-nuclear-engineer`) | Boundary | Medium | Major |
| S-001-04 | Design question shows 3 of 8 REM-02 sub-defects with no "partial list" signal | Rule circumvention | Medium | Major |
| S-001-05 | Assignee line: two usernames space-separated, trailing whitespace | Degradation | Low | Minor |

## Finding Details

### S-001-01: Branch-less worktracker path next to a branch-qualified path [CRITICAL]

**Evidence:** Line 10: `Worktracker: \`projects/PROJ-032-nuclear-sop-review/work/BUG-002-user-hold-runtime-model\` (register section REM-02). Full analysis ... : \`remediation-register.md\` in \`.../STORY-004-remediation/\` on branch \`feat/proj-032-nuclear-sop-review\`.` The `on branch ...` clause grammatically attaches only to the second path.
**Attack:** A reader (human or agent) checks `main` for the worktracker path first (no branch stated = default assumption), gets a 404, and concludes the tracking reference is broken or the work doesn't exist — verified: this file only exists on `feat/proj-032-nuclear-sop-review` (confirmed via repo search).
**Countermeasure:** State the branch once, scoped to both paths, e.g.: "Both paths below are on branch `feat/proj-032-nuclear-sop-review` of `geekatron/jerry`: Worktracker: `.../BUG-002-user-hold-runtime-model/` ... Register: `.../STORY-004-remediation/remediation-register.md`."
**Acceptance Criteria:** Every path in the tracking line resolves without the reader guessing a branch.

### S-001-02: No resolvable URLs despite the source artifact using them [MAJOR]

**Evidence:** Tracking line uses bare paths (`projects/PROJ-032-.../BUG-002-user-hold-runtime-model`, `remediation-register.md` in `.../STORY-004-remediation/`). Compare `BUG-002-user-hold-runtime-model.md` itself, which links `GitHub Issue: [#351](https://github.com/geekatron/jerry/issues/351)` — a full URL.
**Attack:** An agent with no local checkout (the stated audience) cannot dereference a bare path; it must infer the repo (`geekatron/jerry`), infer it should use `blob/{branch}/{path}`, and infer that GitHub — not some other host — is where it lives. Any one guess wrong = dead end.
**Countermeasure:** Replace both with full blob URLs, e.g. `https://github.com/geekatron/jerry/blob/feat/proj-032-nuclear-sop-review/projects/PROJ-032-nuclear-sop-review/work/BUG-002-user-hold-runtime-model/BUG-002-user-hold-runtime-model.md`.
**Acceptance Criteria:** Both references are clickable, host-qualified URLs.

### S-001-03: Silent about the paths being outside the PR's own branch [MAJOR]

**Evidence:** No sentence states these artifacts sit on the maintainer's review branch, not on PR #269's branch (`proj-0039-nuclear-engineer`).
**Attack:** The PR author checks out their own branch, searches for `remediation-register.md` (absent there), and reasonably concludes the tracking reference is a maintainer-side error rather than a different-branch pointer.
**Countermeasure:** Add one clause: "(maintainer review artifact, not on your PR branch)."
**Acceptance Criteria:** Text explicitly disambiguates "your branch" vs. "reviewer's branch."

### S-001-04: Design question shows 3 of 8 sub-defects with no "partial" signal [MAJOR]

**Evidence:** Issue's design question: "what is the pinned runtime execution model, how do USER-HOLD and the briefing agent's six interactive gates actually reach a human under that model, and what is the terminating scope of the self-check rule?" BUG-002's own acceptance criteria (ground truth) add: a timeout/unattended-mode policy for USER-HOLD, whether SR-02 escalates to STOP at C3+, and a context-budget/checkpoint model justifying step limits — none mentioned.
**Attack:** An agent treats the visible question as the full spec, ships a fix for runtime-model + gate-reachability + NS-H-01 only, and re-review fails against acceptance criteria the issue never surfaced.
**Countermeasure:** Append: "...and: a timeout/unattended policy for USER-HOLD, whether SR-02 escalates to STOP at C3+, and a context-budget model justifying the skill's step/token limits (see full acceptance criteria in the linked register)."
**Acceptance Criteria:** All 8 REM-02 sub-defects are either stated or explicitly flagged as "see full list."

## Recommendations

- **P0:** S-001-01 — unify branch attribution for both tracking paths.
- **P1:** S-001-02 — convert both paths to full GitHub blob URLs. S-001-03 — one clause disambiguating branch ownership. S-001-04 — extend the design question or flag it as partial.
- **P2:** S-001-05 — trim trailing whitespace, add a comma between assignee names.

## Scoring Impact

| Dimension | Impact | Rationale |
|-----------|--------|-----------|
| Actionability | Negative | S-001-01/02/03 make the "full analysis" pointer unreliable for the stated zero-context audience |
| Traceability | Negative | S-001-01 breaks path resolution; S-001-04 hides scope |
| Evidence Quality | Neutral | Core factual claims (tool gap, runtime-model ambiguity, NS-H-01 non-termination) verified accurate against register/verdict |
| Completeness | Negative | S-001-04 undercounts the redesign scope |

**Overall assessment:** Targeted remediation — 4 concrete text edits close all Major/Critical findings; no factual retraction needed.
