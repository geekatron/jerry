# BUG-011: tspec-analyst uses live UC as coverage denominator instead of generation-time snapshot (#197)

> **Type:** bug
> **Status:** pending
> **Priority:** medium
> **Impact:** medium
> **Severity:** major
> **Created:** 2026-03-14
> **Parent:** PROJ-030-bugs
> **Owner:** unassigned

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and key details |
| [Steps to Reproduce](#steps-to-reproduce) | Steps to reproduce the issue |
| [Acceptance Criteria](#acceptance-criteria) | Conditions for bug to be fixed |
| [Related Items](#related-items) | Hierarchy and related work items |
| [History](#history) | Status changes and key events |

---

## Summary

The tspec-analyst agent computes coverage against the live use case artifact at analysis time. If extensions are added to the use case after BDD feature files were generated, the coverage percentage drops without any actual test gap -- the tests still cover what was originally specified. The denominator should be a generation-time snapshot, not the live document. This was identified as RT-004 during C4 tournament S-001 Red Team analysis.

**Key Details:**
- **Files:** `skills/test-spec/agents/tspec-analyst.md`, `tspec-analyst.governance.yaml`
- **Symptom:** Coverage percentage decreases when use case is updated post-generation, even without real test gaps
- **Frequency:** When use cases are modified after BDD feature file generation
- **Fix Complexity:** Medium
- **Source:** C4 tournament S-001 Red Team (RT-004)

---

## Steps to Reproduce

1. Create a use case and generate BDD feature files using tspec-generator
2. Run tspec-analyst -- observe coverage percentage (expected: high/100%)
3. Add new extensions to the use case artifact
4. Re-run tspec-analyst without regenerating feature files
5. Observe coverage percentage has dropped despite no actual test gap in the originally-specified scope

---

## Acceptance Criteria

- [ ] tspec-analyst uses a generation-time snapshot of the use case as the coverage denominator
- [ ] Coverage analysis distinguishes between "untested original scope" and "new extensions added post-generation"
- [ ] Coverage report flags post-generation use case changes separately from genuine test gaps
- [ ] Generation-time snapshot mechanism documented in agent methodology

---

## Related Items

### Hierarchy

- **Parent:** PROJ-030-bugs

### Related Items

- **GitHub Issue:** [#197](https://github.com/geekatron/jerry/issues/197)
- **Parent Issue:** [#194](https://github.com/geekatron/jerry/issues/194)
- **Labels:** bug

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-03-14 | pending | Triaged from GitHub Issue #197 |
