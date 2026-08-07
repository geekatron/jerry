# Pre-Mortem Report: GitHub Issue #355 (BUG-006 / REM-06 — OE feedback-loop design)

**Strategy:** S-004 Pre-Mortem Analysis
**Deliverable:** `projects/PROJ-032-nuclear-sop-review/work/EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-006-issue-quality/snapshots/final/issue-355.md`
**Criticality:** C4 (tournament)
**Date:** 2026-08-07
**Reviewer:** adv-executor (S-004)
**Failure Scenario:** It is six months from now. The contributor (or their AI agent) read issue #355, tried to act on it, and either (a) burned an extra round-trip chasing a broken/ambiguous reference, or (b) committed the redesign to the wrong branch, or (c) mis-scoped the fix because the affected files were never named — and the issue had to be re-explained in a PR comment.

## Summary

The issue text is factually accurate against ground truth (verified against `remediation-register.md` REM-06, `remediation-log.md`, and the live GitHub issue #355 via WebFetch — title, body substance, and assignees all match). No Critical (factually-wrong) findings were found. Three Major gaps reduce actionability by forcing extra lookups or navigation risk, and two Minor polish items remain. Recommendation: **ACCEPT with targeted mitigations** — the content is sound; the friction is in reference resolvability and missing scope detail.

## Findings Table

| ID | Failure Cause | Category | Likelihood | Severity | Priority | Affected Dimension |
|----|---------------|----------|------------|----------|----------|--------------------|
| PM-001-s004 | Bare file path + separate branch note for the analysis doc, not a clickable link; reader may resolve on default `main` branch and get a 404/stale file | Technical | Medium | Major | P1 | Actionability |
| PM-002-s004 | Worktracker path given without filename or repeated branch qualifier | Technical | Medium | Major | P1 | Actionability |
| PM-003-s004 | No "Affected files" list — agent must open the register just to learn scope before any work can start | Process | High | Major | P1 | Actionability |
| PM-004-s004 | "candidate designs" overstates REM-06's content (open either/or options, not enumerated architectures like REM-01's a/b/c) | Assumption | Low | Minor | P2 | Evidence Quality |
| PM-005-s004 | No pointer to where the fix belongs (contributor's own PR branch) vs. the review branch cited for reference | Process | Low | Minor | P2 | Actionability |

## Finding Details

### PM-001: Non-resolvable analysis reference [MAJOR]

**Failure Cause:** The issue cites the file as `` `remediation-register.md` in `projects/.../STORY-004-remediation/` on branch `feat/proj-032-nuclear-sop-review` `` — three separate tokens (filename, directory, branch) the reader must assemble into a URL themselves. GitHub does not auto-link bare paths. If the reader (or their agent) builds a URL against `main` (the repo's default branch — confirmed non-default via WebFetch) instead of the named branch, they get a 404 or, worse, silently land on an unrelated/missing path.
**Evidence:** Line 10 of the issue text: "`remediation-register.md` in `projects/.../STORY-004-remediation/` on branch `feat/proj-032-nuclear-sop-review`".
**Mitigation:** Replace with a single clickable blob URL: `https://github.com/geekatron/jerry/blob/feat/proj-032-nuclear-sop-review/projects/PROJ-032-nuclear-sop-review/work/EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/remediation-register.md#rem-06-oe-feedback-loop-design`.
**Acceptance Criteria:** Issue contains one clickable link that resolves directly to the REM-06 section without manual branch/path assembly.

### PM-002: Worktracker path incomplete [MAJOR]

**Failure Cause:** `projects/PROJ-032-nuclear-sop-review/work/BUG-006-oe-feedback-loop-design` is a directory reference, not the file (`BUG-006-oe-feedback-loop-design.md`), and does not restate that it lives on the same non-default branch as the analysis doc. Confirmed via repo Glob that the file exists at that directory with the `.md` suffix.
**Evidence:** Line 10: "Worktracker: `projects/PROJ-032-nuclear-sop-review/work/BUG-006-oe-feedback-loop-design`".
**Mitigation:** Append the filename and fold it into the same branch-qualified link as PM-001, e.g. link text `BUG-006-oe-feedback-loop-design.md` pointing to the blob URL on `feat/proj-032-nuclear-sop-review`.
**Acceptance Criteria:** Reference resolves to the actual worktracker file, not just its containing directory.

### PM-003: No affected-files list [MAJOR]

**Failure Cause:** REM-06 in the register names five concrete affected files (`sop-brief.md`, `sop-capture.md`, `nuclear-sop-behavior-rules.md`, `PLAYBOOK.md`, `bb-003-oe-feedback-loop-integrity.md`). The issue names none of them, so an agent cannot even start scoping a fix without first opening and reading the register — a full extra lookup hop the ~300-word budget had room to avoid.
**Evidence:** Issue body (paragraph 1) describes the defect but never names a file; compare register REM-06 "Affected files" row.
**Mitigation:** Add one line: "Affected files: `skills/nuclear-sop/agents/sop-brief.md`, `sop-capture.md`, `rules/nuclear-sop-behavior-rules.md`, `PLAYBOOK.md`, `behavioral-baselines/bb-003-oe-feedback-loop-integrity.md`."
**Acceptance Criteria:** Issue lists the affected files inline; no register lookup required to identify scope.

## Recommendations

- **P1 (Major, should-fix):** PM-001, PM-002, PM-003 — convert bare path+branch citations to direct clickable links, add the worktracker filename, and add an inline affected-files list. All three are additive (do not remove any existing accurate content) and fit within the ~300-word budget with room to spare (current text is well under budget).
- **P2 (Minor, monitor):** PM-004 — soften "candidate designs" to "design options" to match REM-06's actual either/or framing rather than REM-01's enumerated architectures. PM-005 — add a one-clause pointer that the redesign should land on the contributor's own PR branch, not the cited review branch.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | PM-003: missing affected-files list is a real completeness gap for an actionable issue |
| Internal Consistency | 0.20 | Neutral | No contradictions found against ground truth |
| Methodological Rigor | 0.20 | Neutral | Content faithfully compresses REM-06 without distortion |
| Evidence Quality | 0.15 | Negative | PM-004: mild overstatement of register content ("candidate designs") |
| Actionability | 0.15 | Negative | PM-001, PM-002, PM-003: reader must manually resolve/assemble references or open the register before acting |
| Traceability | 0.10 | Negative | PM-001, PM-002: references are not directly resolvable links |

**Result:** Zero Critical findings (no factual errors against ground truth); 3 Major, 2 Minor. All are reference-resolvability and scope-completeness gaps, not misinformation. Live GitHub issue #355 (fetched independently) matches the snapshot's title, body substance, and assignees.
