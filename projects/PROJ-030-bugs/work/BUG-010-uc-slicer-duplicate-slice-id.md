# BUG-010: uc-slicer lacks duplicate slice_id conflict detection (#199)

> **Type:** bug
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Severity:** major
> **Created:** 2026-03-31
> **Completed:** 2026-03-31
> **Parent:** PROJ-030-bugs
> **GitHub Issue:** [#199](https://github.com/geekatron/jerry/issues/199)
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

uc-slicer documents append-only re-invocation but has no validation comparing new slice_ids against existing ones. Schema doesn't enforce `uniqueItems` on slices array. Duplicate slice_ids corrupt downstream artifacts.

## Steps to Reproduce

1. Run `/use-case` uc-slicer on a use case to produce initial slices
2. Re-invoke uc-slicer on the same use case (append-only mode)
3. Observe that new slices can have slice_ids identical to existing ones
4. Run downstream `/test-spec` or `/contract-design` -- duplicate slice_ids cause artifact corruption or overwrites

## Fix

Add duplicate detection step to 8-step slicing methodology. Update JSON schema with uniqueItems constraint. Invoke H-31 clarification on conflict.

## Files

- `skills/use-case/agents/uc-slicer.md` (lines 81-165 methodology, line 227-228 re-invocation guardrail)
- `docs/schemas/use-case-realization-v1.schema.json` (lines 354-358, slice_id definition)

## Acceptance Criteria

- [ ] uc-slicer collects existing slice_ids before appending
- [ ] Duplicate slice_id triggers H-31 clarification
- [ ] JSON schema enforces uniqueness on slices array
