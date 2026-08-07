# Steelman Report: GitHub Issue #358 (BUG-009 / REM-09 — registration enforcement surfaces)

## Steelman Context
- **Deliverable:** `.../STORY-006-issue-quality/snapshots/final/issue-358.md`
- **Deliverable Type:** Communication/specification artifact (GitHub issue text)
- **Criticality Level:** C4 (tournament review)
- **Strategy:** S-003 (Steelman Technique)
- **Steelman By:** adv-executor | **Date:** 2026-08-07

## Summary

**Steelman Assessment:** Every factual claim in the issue (commit SHA, CI run, diff contents, worktracker path, 89→93 count, priority-collision mechanics) checks out against the remediation register, remediation log, and the actual commit diff. The text is already honest about severity ("Nothing for you to do") and translates internal enforcement jargon (L2-REINJECT) into plain language without naming it. No Critical (factually-wrong or misleading) findings.

**Improvement Count:** 0 Critical, 2 Major, 4 Minor
**Original Strength:** High — accurate, appropriately scoped, honestly framed as low-priority/informational.
**Recommendation:** Incorporate the two Major improvements (both close small actionability/completeness gaps); Minor items are polish.

## Improvement Findings Table

| ID | Description | Severity | Dimension |
|----|-------------|----------|-----------|
| S-003-01 | "What the fix changed" undercounts the actual AGENTS.md diff | Major | Completeness |
| S-003-02 | No clickable commit link; only a bare short SHA | Major | Actionability |
| S-003-03 | "compound trigger" / "trigger-mapped skill" used without a gloss | Minor | Self-containedness |
| S-003-04 | Verify command assumes a non-shallow local clone | Minor | Actionability |
| S-003-05 | "REM-09" internal ID unexplained | Minor | Self-containedness |
| S-003-06 | Body (~340 words) runs longer than needed for a "nothing to do" issue | Minor | Concision |

## Improvement Details

### S-003-01 (Major) — Completeness

**Original:** "`AGENTS.md` gets the missing section link, a summary row, and the corrected total of 93."

**Ground truth (commit `c07033ce` diff):** the AGENTS.md hunk also (a) bumps "Last verified: 2026-03-09" → "2026-08-07" and (b) appends a new sentence to the MCP "Not included (by design)" note: "sop-\* agents do not use MCP tools; their persistence model uses file-based output per P-002 ... not cross-session MCP storage." Both are real, in-scope parts of REM-09 (per the register's own G3 defect list) but are absent from the issue's description of the fix.

**Strengthened:** "`AGENTS.md` gets the missing section link, a summary row, the corrected total of 93, an updated 'Last verified' date, and a new sentence noting `sop-*` agents don't use MCP tools (file-based persistence, matching the existing `eng-*`/`red-*` pattern)."

**Rationale:** The issue explicitly invites a `git diff` verification. A reader (human or agent) who runs that diff and finds two hunks not mentioned in the prose has reasonable grounds to wonder whether the fix scope crept beyond what was described — an avoidable trust gap, not a real problem.

---

### S-003-02 (Major) — Actionability / Resolvable References

**Original:** references the fix only as backticked text — `` `c07033ce` `` — with no link.

**Verified:** full SHA is `c07033ce159d9852744486aed0a54e9528b4668d` (evidence pack, matches commit-log header); GitHub does not reliably autolink SHAs inside inline code spans.

**Strengthened:** `[c07033ce](https://github.com/geekatron/jerry/commit/c07033ce159d9852744486aed0a54e9528b4668d)` at first mention and in "How to verify," alongside the existing CI link.

**Rationale:** The CI link is already one click; the commit reference should match — lets a reviewer (or an AI agent without local git access) inspect the actual diff in-browser instead of needing to clone and run `git diff` to see what changed.

---

## Minor Findings (brief)

- **S-003-03:** Add a short parenthetical on first use, e.g. "compound trigger (a multi-word phrase match that outranks the numeric priority ranking)" — the surrounding sentence already conveys the effect, so this is polish, not a comprehension blocker.
- **S-003-04:** `git diff c07033ce^ c07033ce -- ...` fails on a shallow clone (common in CI checkouts). Append: "(shallow clone? `git fetch --unshallow` first)".
- **S-003-05:** "register section REM-09" — one clause identifying REM-09 as "the maintainer's internal remediation-cluster ID for this defect" would remove the last unglossed internal code in the issue.
- **S-003-06:** The Tracking paragraph's nested internal path (`.../STORY-004-remediation/` on the internal review branch) is not actionable for the external reader — it's an internal artifact, not something they can open. Trimming it to "worktracker `BUG-009-registration-enforcement-surfaces`, issue #358" would shorten the issue without losing anything the PR author can act on.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Positive | S-003-01 closes the AGENTS.md diff-description gap |
| Internal Consistency | 0.20 | Neutral | Already consistent with ground truth |
| Methodological Rigor | 0.20 | Neutral | No methodology claims to strengthen |
| Evidence Quality | 0.15 | Neutral | All cited facts (SHA, CI run, counts) already verified accurate |
| Actionability | 0.15 | Positive | S-003-02, S-003-04 remove lookup friction |
| Traceability | 0.10 | Positive | S-003-02 (direct commit link), S-003-05 (ID gloss) |

**Best Case Scenario:** This issue is strongest when read by a technically literate contributor (or their agent) with GitHub browser access and a full local clone of `proj-0039-nuclear-engineer`; under those conditions every claim resolves and every command executes as written. Confidence: HIGH.
