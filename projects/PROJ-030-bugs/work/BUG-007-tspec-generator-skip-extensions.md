# BUG-007: tspec-generator silently skips unrecognized extension outcomes (#195)

> **Type:** bug
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Severity:** major
> **Created:** 2026-03-31
> **Completed:** 2026-03-31
> **Parent:** PROJ-030-bugs
> **GitHub Issue:** [#195](https://github.com/geekatron/jerry/issues/195)
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

Clark transformation rules define only 3 outcome types (RULE-OT-01 success, RULE-OT-02 failure, RULE-OT-03 rejoin). Extensions with unrecognized outcomes silently produce no scenario — a P-022 violation (misrepresenting coverage completeness).

## Steps to Reproduce

1. Create a use case with an extension that has a non-standard outcome (e.g., "deferred" or "escalated")
2. Run `/test-spec` tspec-generator against the use case
3. Observe that the extension produces no BDD scenario -- no error, no warning
4. Check coverage report: it reports 100% even though the extension was silently skipped

## Fix

Add RULE-OT-04 fallback to `skills/test-spec/rules/clark-transformation-rules.md` that flags unrecognized outcomes and invokes H-31 clarification. Update tspec-generator failure modes table.

## Files

- `skills/test-spec/rules/clark-transformation-rules.md` (lines 121-147)
- `skills/test-spec/agents/tspec-generator.md` (lines 149-156, 255-261)

## Acceptance Criteria

- [ ] RULE-OT-04 exists for unrecognized outcome values
- [ ] Unrecognized outcomes trigger H-31 clarification, not silent skip
- [ ] Failure modes table updated with explicit handling
