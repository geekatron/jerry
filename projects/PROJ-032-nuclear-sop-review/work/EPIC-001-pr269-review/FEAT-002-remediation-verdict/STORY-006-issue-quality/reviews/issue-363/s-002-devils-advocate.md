# Devil's Advocate Report: GitHub Issue #363 (PROJ-032/BUG-014 nav tables)

**Strategy:** S-002 Devil's Advocate
**Deliverable:** `snapshots/final/issue-363.md` (live text of geekatron/jerry issue #363)
**Criticality:** C4 (tournament)
**Date:** 2026-08-07
**Reviewer:** adv-executor (blind, background agent)
**H-16 Compliance:** Not independently verifiable under blindness constraint (this agent cannot read the S-003 output directory). Per the tournament's declared 6-group sequential order (self-refine -> steelman -> challenge -> verify -> decompose -> score), S-003 is assumed to have executed in the preceding group. Flagging this as an assumption, not a confirmed fact, per P-022.

## Summary

4 counter-arguments identified (0 Critical, 3 Major, 1 Minor). Every factual claim in the issue text checked against the remediation register, remediation log, evidence-c07033ce diff, and the live PR worktree — all confirmed accurate (file names, line counts, the 23/25 and 3/5 template-conformance ratios, commit hash, CI run, and tracking paths all hold up). The counter-arguments target framing and completeness, not fact-checking failures: the title front-loads unexplained internal codes, the "how to verify" command will surface unrelated diff hunks that could confuse the reader about this issue's actual scope, and the closing line risks implying the PR is closer to merge-ready than the broader remediation record supports. Recommend targeted revision; core content is sound.

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| S-002-01 | Title front-loads unexplained internal codes | Major | Title: "PROJ-032/BUG-014: nuclear-sop — ..." | Actionability |
| S-002-02 | Verify command scope will show unrelated diffs | Major | Line 11 `git diff ... -- skills/nuclear-sop/templates/ ...` | Traceability |
| S-002-03 | Closing line implies PR is closer to done than it is | Major | Line 14: "this issue stays open only until PR #269's disposition is decided" | Evidence Quality (honest status framing) |
| S-002-04 | "Long" framing not justified for the 76-line file | Minor | Line 7: "HOLD_POINT_LOG.template.md (76 lines)" | Completeness |

## Finding Details

### S-002-01: Title leads with unexplained internal codes [MAJOR]

**Claim challenged:** The issue title is `PROJ-032/BUG-014: nuclear-sop — long markdown files missing required navigation tables (fixed on your branch)`.
**Counter-argument:** The mission requires the author/agent to act with zero knowledge of this repo's internal governance. `PROJ-032` and `BUG-014` are internal worktracker codes never defined anywhere in the issue body except implicitly, three paragraphs later, in the "Tracking" footer. GitHub issue titles are the first (and sometimes only) thing surfaced in notification emails, issue lists, and PR cross-links — a reader scanning the title alone gets two opaque codes before any plain-language content.
**Impact:** Minor friction, not a wrong-path risk (the body recovers quickly), but it fails the self-containedness bar the mission sets, and it's an easy fix.
**Dimension:** Actionability
**Response Required:** Reorder the title so plain language leads and the internal code is parenthetical/trailing.
**Acceptance Criteria:** Title conveys the defect and its "fixed for you" status without requiring the reader to already know what "PROJ-032" or "BUG-014" mean. Suggested: `nuclear-sop: 6 files with missing/incomplete navigation tables — fixed on your branch (PROJ-032/BUG-014)`.

### S-002-02: "How to verify" command is not scoped to this issue's actual diff [MAJOR]

**Claim challenged:** Line 11: `git diff c07033ce^ c07033ce -- skills/nuclear-sop/templates/ skills/nuclear-sop/examples/ skills/nuclear-sop/SKILL.md skills/nuclear-sop/PLAYBOOK.md skills/nuclear-sop/docs/reference.md`.
**Counter-argument:** `c07033ce` is a single squashed commit implementing all seven FIX-NOW clusters (REM-08..14), not just REM-14 (this issue). The `skills/nuclear-sop/templates/` pathspec used here is a directory, not the two specific files this issue is about — it also matches `POST_JOB_BRIEF.template.md` and `PROCEDURE_STATE.template.yaml`, both of which were changed in the same commit for unrelated reasons (REM-11's `.yaml`-extension standardization and REM-12's state-machine documentation, tracked separately as issues #360/#361). A contributor who runs the exact command given will see diff hunks that have nothing to do with navigation tables and no way, from this issue text alone, to tell which hunks belong to #363 versus #360/#361.
**Evidence:** Confirmed against `evidence-c07033ce.md`: `templates/POST_JOB_BRIEF.template.md | 4 +-` and `templates/PROCEDURE_STATE.template.yaml | 28 +++----` both fall under `skills/nuclear-sop/templates/` and are present in the full diff alongside the two nav-table files (`WORKFLOW_DEFINITION.template.md`, `HOLD_POINT_LOG.template.md`).
**Impact:** Undermines the precision the "How to verify" section implies; a careful contributor (or their agent) may waste time reconciling extraneous changes against this issue, or wrongly conclude the nav-table fix touched files it didn't.
**Dimension:** Traceability
**Response Required:** Narrow the pathspec to exactly the six files this issue's fix touches.
**Acceptance Criteria:** Replace the directory pathspec with explicit file paths: `git diff c07033ce^ c07033ce -- skills/nuclear-sop/templates/WORKFLOW_DEFINITION.template.md skills/nuclear-sop/templates/HOLD_POINT_LOG.template.md skills/nuclear-sop/examples/c3-adr-workflow-definition.md skills/nuclear-sop/SKILL.md skills/nuclear-sop/PLAYBOOK.md skills/nuclear-sop/docs/reference.md`.

### S-002-03: Closing status line risks overstating how close PR #269 is to merge [MAJOR]

**Claim challenged:** Line 14: "Fix is already on your branch; this issue stays open only until PR #269's disposition is decided."
**Counter-argument:** Taken alone, this reads as "this one item is the last loose end." The remediation log this issue traces back to states the opposite for the PR as a whole: seven DEFER-REWORK clusters (57% of the Critical finding mass, including the skill's core safety architecture — QG-HOLD delegation, USER-HOLD runtime model, trust-boundary/tamper protection, QG-E4 validation evidence, H-36 governance ruling) remain open as separate issues (#350-#356) and, per the remediation log, "block any merge recommendation." An external contributor reading only issue #363 has no signal that resolving this issue does nothing to move the PR toward mergeable — the sentence's literal truth ("stays open until disposition is decided") is compatible with a false inference ("we're just waiting on a decision, not more fixes").
**Evidence:** `remediation-log.md` Outcome section: "They remain open as BUG-001..007 / issues #350–#356 and block any merge recommendation."
**Impact:** Honest severity/status framing is a named judgment criterion for this artifact; the omission is a status-framing gap, not a factual error, but it's exactly the kind of gap that would mislead an agent triaging issues by "what's left to do before merge."
**Dimension:** Evidence Quality / honest status framing
**Response Required:** Add one clause noting that this issue's closure is independent of the PR's overall merge readiness, which depends on separate open issues.
**Acceptance Criteria:** Closing line becomes something like: "Fix is already on your branch; this issue stays open only until PR #269's disposition is decided. (Note: PR #269's overall merge is separately blocked by unresolved issues #350–#356, unrelated to this fix.)"

### S-002-04: "Long" is asserted, not obviously true, for the 76-line file [MINOR]

**Claim challenged:** Line 7 groups `HOLD_POINT_LOG.template.md (76 lines)` with two much longer files (250 and 559 lines) under "three long runtime-consumed files."
**Counter-argument:** 76 lines does not intuitively read as "long" to a reader unfamiliar with this repo's internal >30-line navigation-table threshold (H-23, not named in the issue). Without that threshold stated, the claim that this file needed a nav table reads as an assertion rather than an application of a stated rule.
**Evidence:** `markdown-navigation-standards.md` H-23: "All Claude-consumed markdown files over 30 lines MUST include a navigation table." The issue never states this threshold.
**Impact:** Low — doesn't change what the reader should do (nothing), just weakens the "why" for one of the three files.
**Dimension:** Completeness
**Response Required:** Optional; acknowledgment sufficient.
**Acceptance Criteria:** If revised, add the numeric threshold once, e.g., "this repo requires a navigation table on any markdown file over 30 lines that agents read at runtime."

## Recommendations

**P1 (Major — SHOULD resolve):**
- S-002-01: Reorder title to lead with plain language; move `PROJ-032/BUG-014` to a trailing parenthetical.
- S-002-02: Replace the directory-scoped `git diff` pathspec with the six explicit file paths so the verify command shows only this issue's changes.
- S-002-03: Add one clause clarifying this issue's closure is independent of PR #269's overall (separately blocked) merge readiness.

**P2 (Minor — MAY resolve):**
- S-002-04: State the >30-line navigation-table threshold explicitly rather than asserting "long."

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | S-002-04: threshold rationale for the 76-line file is asserted, not stated |
| Internal Consistency | 0.20 | Neutral | No contradictions within the issue text itself |
| Methodological Rigor | 0.20 | Neutral | Not applicable to a communication artifact |
| Evidence Quality | 0.15 | Negative | S-002-03: closing status line is technically true but incomplete relative to the broader PR record |
| Actionability | 0.15 | Negative | S-002-01, S-002-02: title jargon and an unscoped verify command both add friction to acting on the text alone |
| Traceability | 0.10 | Negative | S-002-02: verify command will surface hunks not attributable to this issue from the text alone |

**Overall assessment:** Targeted revision. No claim in the issue text is factually wrong; all three Major findings are framing/precision gaps that a small, mechanical edit resolves without touching the (accurate) substantive content.
