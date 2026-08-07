# FMEA Report: GitHub Issue #360 (PROJ-032/BUG-011 — nuclear-sop OE artifact contract)

**Strategy:** S-012 FMEA (Failure Mode and Effects Analysis)
**Deliverable:** `projects/PROJ-032-nuclear-sop-review/work/EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-006-issue-quality/snapshots/final/issue-360.md`
**Criticality:** C4 (tournament)
**Date:** 2026-08-07
**Reviewer:** adv-executor (S-012)
**Elements Analyzed:** 6 | **Failure Modes Identified:** 4 | **Total RPN:** 423

## Summary

Decomposed the ~320-word issue into 6 elements (title, attribution, defect narrative, fix narrative, verification steps, tracking footer) and fact-checked every claim against the remediation register (REM-11), the commit diff, and the live PR worktree. All substantive factual claims (extension mismatch, three-way retrieval-protocol drift, unsatisfiable AC-7, unwritten Attachments contract, CI run link, commit hash, branch name) verified accurate — zero Critical findings. Four Minor/Major findings concern internal-code self-containedness and one verification-command completeness gap. **Recommendation: ACCEPT** — no factual corrections required; one Major polish item on the tracking footer recommended before close.

## Findings Table

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Corrective Action | Affected Dimension |
|----|---------|-------------|---|---|---|-----|----------|-------------------|--------------------|
| S-012-01 | Tracking footer | Insufficient: internal-branch file path offered as the only "how to trace this" pointer, with no accessibility caveat | 6 | 6 | 5 | 180 | Major | Add one caveat sentence if the register isn't yet on `main` | Actionability |
| S-012-02 | Title + Tracking footer | Ambiguous: unglossed internal ID conventions (PROJ-032/BUG-011, REM-11) | 2 | 5 | 6 | 60 | Minor | Add a 4-word gloss on first use | Completeness |
| S-012-03 | How-to-verify | Insufficient: verification grep narrower than the register's own validation command | 3 | 4 | 6 | 72 | Minor | Widen the grep pattern | Methodological Rigor |
| S-012-04 | "What was wrong" paragraph | Insufficient: 3 distinct defects (extension mismatch, protocol drift, unwritten Attachments step) narrated as one dense clause-chain | 3 | 5 | 5 | 75 | Minor | Split into a 3-item list | Actionability |

## Finding Details

### S-012-01: Tracking footer points to a maintainer-only artifact with no accessibility note

**Element:** Tracking footer ("worktracker `.../BUG-011-oe-artifact-contract` ... register section REM-11 ... on branch `feat/proj-032-nuclear-sop-review`").

**Effect:** The path is accurate (verified: `projects/PROJ-032-nuclear-sop-review/work/BUG-011-oe-artifact-contract/BUG-011-oe-artifact-contract.md` exists) but lives on the maintainer's internal review branch, not the contributor's `proj-0039-nuclear-engineer` branch or `main`. An external contributor or their agent following this pointer to "trace the full review" has no signal whether that branch is public/pushed, and no fallback if it 404s.

**S/O/D rationale:** S=6 (could send the reader down a dead-end lookup, though the actionable content is fully self-contained above the `---` separator so nothing is blocked); O=6 (this exact footer pattern recurs across the tournament's issue set, per the shared template); D=5 (only detectable by attempting the link/path, not obvious from reading alone).

**Corrective Action:** Append one sentence: *"This tracking detail is for the maintainer's internal record; everything you need to act is in the sections above."* Optionally add: *"If `feat/proj-032-nuclear-sop-review` isn't visible to you, the register will be merged to `main` before final disposition."*

**Acceptance Criteria:** Footer includes an explicit "no action needed here" or accessibility caveat.

**Post-Correction RPN estimate:** ~40 (Minor).

### S-012-02: Unglossed internal ID conventions

**Element:** Title (`PROJ-032/BUG-011`) and footer (`REM-11`, `STORY-004-remediation`).

**Effect:** A zero-context reader can act on the issue without understanding these codes (they are identifiers, not instructions), so this does not block actionability — but it is exactly the "unexplained internal code" pattern the mission calls out.

**S/O/D rationale:** S=2 (cosmetic; body text is self-contained), O=5 (recurs across every issue in this batch), D=6 (only noticeable on close read).

**Corrective Action:** No structural change needed; if editing anyway, add a 4-word parenthetical on first use, e.g. "`BUG-011` (internal tracking ID)".

**Post-Correction RPN estimate:** ~30 (Minor).

## Recommendations

**Major:**
- S-012-01: Add an accessibility/no-action-needed caveat to the tracking footer's internal-branch reference. Estimated RPN reduction: 180 -> 40.

**Minor (optional polish):**
- S-012-03: Widen the verification grep to `grep -rn "experience/.*\.md\|oe-entry-.*\.md" skills/nuclear-sop/` to match the register's own validation command (currently both patterns return 0 hits against the live worktree, so this is a robustness improvement, not a live defect).
- S-012-04: Split the "What was wrong" paragraph into a 3-item list (extension mismatch; 3-way retrieval-protocol drift; unwritten Attachments step) to make the bundled-defect count explicit for both human and agent readers.
- S-012-02: Optional ID glossing; low value given body self-containedness.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | All three sub-defects, fix scope, and verification steps present |
| Internal Consistency | 0.20 | Neutral | No contradictions found between title, body, and footer |
| Methodological Rigor | 0.15 | Slightly Negative | S-012-03: verification command weaker than the register's own gate |
| Evidence Quality | 0.15 | Positive | Commit hash, CI run link, and file/line-level claims all verified exact against ground truth |
| Actionability | 0.15 | Slightly Negative | S-012-01, S-012-04: footer lookup friction and dense narrative reduce one-pass actionability |
| Traceability | 0.10 | Positive | Register section, worktracker ID, and commit hash all resolve correctly |

## Fact-Check Ledger (verified against ground truth)

| Claim in issue | Verified against | Result |
|---|---|---|
| "one of seven mechanical fixes ... in commit c07033ce" | remediation-register.md Cluster Index (7 FIX-NOW clusters, REM-08..14) | Accurate |
| Extension mismatch: rules/write path `.yaml`, template/baseline/example said `.md` | evidence-c07033ce.md diffs (POST_JOB_BRIEF.template.md, bb-003, c3-adr-workflow-definition.md) | Accurate |
| "one of the worked example's acceptance criteria was literally unsatisfiable" (AC-7) | evidence diff line ~1732 (`*.md` -> `*.yaml` glob vs. capture write path) | Accurate |
| Retrieval protocol "specified three different ways" | register REM-11 G2 (rules vs. sop-brief Step 4 vs. bb-003 B-24) | Accurate |
| Attachments section "documented ... never actually writes it" | register REM-11 G3; evidence diff adds Section 11 write step to sop-capture.md | Accurate |
| Fix applies convention "everywhere ... both agents, and their mirror copies" | evidence commit stat touches sop-brief/sop-capture .md + .governance.yaml + composition/*.agent.yaml + *.prompt.md | Accurate |
| CI link "15/15 green" | evidence-c07033ce.md header, exact URL match | Accurate |
| Worktracker path `work/BUG-011-oe-artifact-contract` | confirmed exists via glob in scratchpad worktree | Accurate |

---
*Execution ID: FM-20260807-issue360*
