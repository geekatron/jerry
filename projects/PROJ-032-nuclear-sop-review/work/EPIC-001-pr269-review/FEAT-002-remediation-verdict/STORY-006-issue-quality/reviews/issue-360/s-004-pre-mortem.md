# Pre-Mortem Report: GitHub Issue #360 (BUG-011 / REM-11 OE artifact contract)

**Strategy:** S-004 Pre-Mortem Analysis
**Deliverable:** `issue-360.md` snapshot of GitHub issue #360, geekatron/jerry
**Criticality:** C4 (tournament)
**Failure Scenario:** It is six months from now. PR #269's author read this issue, misjudged it as a routine no-action notice, and either (a) never re-verified the fix against their own branch state, or (b) tried the verify command and got confused output, losing trust in the maintainer's remediation claims generally.

## Summary

The text is well-grounded: every factual claim (branch name, commit SHA, cluster ID, worktracker path, CI run link, fix substance) was checked against the remediation register, log, verdict, and the actual diff/worktree, and all verified true. Failure risk is concentrated in one spot — the "How to verify" grep command is narrower than the register's own validation command and could give a false sense of completeness if reused as a template for other issues. One secondary risk: the OE-invisibility consequence, while accurate, is stated without a plain-language definition of "feedback loop," which could cost a non-Jerry-fluent agent a beat to parse. Recommendation: ACCEPT with one Minor polish; no Critical or Major failure causes identified.

## Findings Table

| ID | Failure Cause | Category | Likelihood | Severity | Priority | Affected Dimension |
|----|---------------|----------|------------|----------|----------|--------------------|
| PM-001-20260807 | "How to verify" grep omits the `oe-entry-.*\.md` alternation the register's own validation step uses, silently narrowing what the reader actually checks | Technical | Low | Minor | P2 | Evidence Quality |
| PM-002-20260807 | "feedback loop" and "operating experience" used without a one-clause plain definition, costing an unfamiliar reader a small parse cost | Process | Low | Minor | P2 | Actionability |

## Finding Details

### PM-001: Verify command is narrower than the fix's own validation criterion [MINOR]

**Failure Cause:** The issue instructs `grep -rn "experience/.*\.md" skills/nuclear-sop/` to confirm the fix. The remediation register's REM-11 validation step is `grep -rn "experience/.*\.md|oe-entry-.*\.md" skills/nuclear-sop/`. The second alternation exists specifically because one fixed location — `capture/oe-entry-{entry_id}.md` in `POST_JOB_BRIEF.template.md` (pre-fix) — does not contain the string "experience/" on its own line. Both commands currently return 0 hits (verified against the PR worktree), so the instruction is not factually wrong today, but it checks a proper subset of what was actually fixed.
**Likelihood:** Low — the practical outcome (0 hits) is identical today either way.
**Severity:** Minor — does not mislead about the current state, only under-specifies the check.
**Evidence:** Issue line: `grep -rn "experience/.*\.md" skills/nuclear-sop/`; register fix-spec validation line 291 of `remediation-register.md`: `grep -rn "experience/.*\.md\|oe-entry-.*\.md" skills/nuclear-sop/`.
**Dimension:** Evidence Quality
**Mitigation:** Extend the grep in the issue to match the register's own criterion: `grep -rn "experience/.*\.md\|oe-entry-.*\.md" skills/nuclear-sop/`.
**Acceptance Criteria:** Issue text's verify command matches the fix specification's validation command exactly (or a documented superset).

### PM-002: "Feedback loop" left undefined for a reader with zero repo context [MINOR]

**Failure Cause:** The issue calls the capture/retrieve mechanism "the skill's 'operating experience' loop" and later "the feedback loop the skill names as its key capability" — accurate paraphrase of REM-11, but a reader unfamiliar with the skill (the stated audience) must infer that "loop" = "write lessons after a run, read them before the next one" purely from context clues scattered across two sentences.
**Likelihood:** Low — the surrounding sentence does explain the mechanism ("capture lessons learned after each run, retrieve them before the next").
**Severity:** Minor — the explanation is present, just distributed rather than upfront.
**Evidence:** Issue lines 5-6: "the skill's 'operating experience' loop — capture lessons learned after each run, retrieve them before the next — was internally inconsistent..."
**Dimension:** Actionability
**Mitigation:** No text change required; the parenthetical already carries the definition. Retain as-is or move the em-dash clause earlier in the sentence for a marginal readability gain.
**Acceptance Criteria:** N/A — optional polish only.

## Recommendations

**P0:** None.
**P1:** None.
**P2:** PM-001-20260807 — align the verify grep with the register's own two-pattern check. PM-002-20260807 — optional wording tightening, no action required.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | All claims present and traceable; no missing context identified beyond PM-002 (negligible). |
| Internal Consistency | 0.20 | Neutral | No contradictions found across issue text, register, log, verdict, and diff. |
| Methodological Rigor | 0.20 | Neutral | All 5 failure-category lenses applied (Technical: PM-001; Process: PM-002; Assumption/External/Resource: none surfaced). |
| Evidence Quality | 0.15 | Slightly Negative | PM-001: verify instruction is a true-but-incomplete subset of the actual fix scope. |
| Actionability | 0.15 | Neutral | Reader (human or agent) can act from the text alone; PM-002 is cosmetic. |
| Traceability | 0.10 | Positive | Branch, commit, CI run, register section, and worktracker path all independently verified against ground truth and the live worktree. |

**Overall assessment:** ACCEPT. This is the strongest-verified issue text reviewed under this protocol — zero factual errors found against ground truth (remediation register, log, verdict, evidence diff, and live PR worktree all cross-checked). Only two Minor, non-blocking findings.
