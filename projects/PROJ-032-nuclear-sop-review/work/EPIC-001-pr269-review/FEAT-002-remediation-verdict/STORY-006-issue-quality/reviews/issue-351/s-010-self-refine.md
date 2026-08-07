# S-010 Self-Refine — Issue #351 (BUG-002: USER-HOLD runtime model)

| Field | Value |
|-------|-------|
| Strategy | S-010 Self-Refine |
| Deliverable | GitHub issue #351 text (snapshots/final/issue-351.md) |
| Criticality | C4 (tournament) |
| Date | 2026-08-07 |
| Iteration | 1 of 1 |

## Summary

The issue text is factually accurate against ground truth (REM-02, BUG-002, verdict) on every substantive claim checked: the AskUserQuestion tool-grant gap, the unpinned runtime model, the non-terminating self-check rule, the DEFER-REWORK/critical disposition, and both cited paths resolve live on GitHub. One paraphrase (the self-check rule's scope) understates the underlying rule and could misdirect a fix; two minor polish items remain. Ready for external posting with the Major item addressed.

## Findings Table

| ID | Finding | Severity | Evidence | Dimension |
|----|---------|----------|----------|-----------|
| S-010-01 | Self-check rule scope understated: "before every file write" omits Edit/Bash | Major | Ground truth: "NS-H-01: STAR mandatory before every Write, Edit, Bash" (gap-analysis.md); issue says only "file write" | Evidence Quality / Actionability |
| S-010-02 | Worktracker reference names a directory, not the entity file | Minor | Issue: "Worktracker: `projects/PROJ-032-nuclear-sop-review/work/BUG-002-user-hold-runtime-model`" — actual file is `.../BUG-002-user-hold-runtime-model.md` | Actionability |
| S-010-03 | Title carries unglossed internal ID prefix "PROJ-032/BUG-002" | Minor | Title: "PROJ-032/BUG-002: nuclear-sop — how does the user-approval pause..." — no reader outside this repo's maintainers can place these tokens | Self-containedness |

## Finding Details

### S-010-01: Self-check rule scope understated

- **Severity:** Major
- **Affected Dimension:** Evidence Quality / Actionability
- **Evidence:** Issue text: "the rule 'run a self-check before every file write' is non-terminating as written, because recording the self-check is itself a file write." Ground truth (PR worktree `validation/gap-analysis.md` line 190): "NS-01 | NS-H-01: STAR mandatory before every Write, Edit, Bash." Bash tool calls (e.g., running a command) are not "file writes" at all.
- **Impact:** A reader (human or agent) who takes the issue text as the full scope of the design question would assume the non-termination problem — and any fix — only concerns steps that write files, and could ship a fix that leaves Bash-triggered steps unchecked, reproducing the same defect the issue is meant to close.
- **Recommendation:** Replace "before every file write" with "before every Write, Edit, or command-execution step" (or equivalent plain-language phrasing covering all three trigger actions).

## Recommendations

1. **Widen the self-check rule paraphrase to cover Write/Edit/Bash, not just file writes** (resolves S-010-01).
2. **Append the filename to the worktracker path** — `.../BUG-002-user-hold-runtime-model/BUG-002-user-hold-runtime-model.md` — so the reference is a direct file link rather than a directory browse (resolves S-010-02).
3. **Either drop or gloss the "PROJ-032/BUG-002" title prefix** (e.g., trailing "(internal tracking ref)") since GitHub issue #351 is already the durable external identifier and the prefix adds no information a non-maintainer can use (resolves S-010-03).

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Positive | All named claims (tool grant, runtime model, non-termination, disposition) present and verified |
| Internal Consistency | 0.20 | Positive | No contradictions found between issue text and REM-02/BUG-002/verdict |
| Methodological Rigor | 0.20 | Neutral | N/A to a communication artifact |
| Evidence Quality | 0.15 | Negative | S-010-01: one claim narrower/less accurate than its source rule |
| Actionability | 0.15 | Negative | S-010-01 (scope), S-010-02 (path not a direct file link) |
| Traceability | 0.10 | Positive | Worktracker path and register section both resolve on GitHub (verified live) |

## Decision

**Outcome:** Ready for external review; one Major polish item (S-010-01) recommended before or alongside next issue edit — does not warrant re-blocking the already-posted issue.

**Rationale:** Zero Critical findings; all factual claims verified true against ground truth and confirmed live on GitHub (issue #351, both cited paths). The Major finding is a precision gap in a paraphrase, not a factual error or broken reference.

**Next Action:** Apply the S-010-01 wording fix in a follow-up issue edit; S-010-02/S-010-03 are optional polish.
