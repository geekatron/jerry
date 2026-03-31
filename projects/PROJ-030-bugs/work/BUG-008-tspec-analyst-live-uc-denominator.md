# BUG-008: tspec-analyst uses live UC as coverage denominator (#197)

> **Type:** bug
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Severity:** major
> **Created:** 2026-03-31
> **Parent:** PROJ-030-bugs
> **GitHub Issue:** [#197](https://github.com/geekatron/jerry/issues/197)
> **Coordinating Epic:** EPIC-002 (PROJ-024)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description of the defect |
| [Steps to Reproduce](#steps-to-reproduce) | How to observe the defect |
| [Fix](#fix) | Proposed resolution |
| [Files](#files) | Affected source files |
| [Acceptance Criteria](#acceptance-criteria) | Conditions for resolution |

---

## Summary

tspec-analyst computes coverage by counting flows from the current (live) use case file, ignoring the `coverage.total_flows` snapshot recorded in Feature file frontmatter at generation time. If the UC is modified after test generation, coverage metrics are wrong.

## Steps to Reproduce

1. Generate a Feature file from a use case with `/test-spec` tspec-generator
2. Modify the source use case to add a new extension or alternative flow
3. Run `/test-spec` tspec-analyst coverage analysis on the Feature file
4. Observe that coverage is computed against the modified UC flow count, not the `coverage.total_flows` snapshot from generation time

## Fix

Cross-reference Feature file frontmatter `coverage.total_flows` against live UC computation. Flag divergence as a staleness warning. Recommend re-generation when counts differ.

## Files

- `skills/test-spec/agents/tspec-analyst.md` (lines 82-107, Step 2 methodology)
- `skills/test-spec/rules/clark-transformation-rules.md` (RULE-SL-02, lines 162-166)

## Acceptance Criteria

- [ ] tspec-analyst cross-references Feature file `coverage.total_flows` with live UC count
- [ ] Divergence produces a staleness warning in the coverage report
- [ ] Coverage report shows both generation-time and current flow counts when they differ
