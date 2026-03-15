# BUG-009: tspec-generator silently skips extensions with unrecognized outcome values (#195)

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

When a use case extension has an outcome value that does not match the expected pattern (`success|failure|rejoin:\d+`), the tspec-generator agent silently skips the extension. The resulting feature file contains missing scenarios with no warning or diagnostic output. This was identified as FM-004 (RPN 320) during C4 tournament S-012 FMEA analysis.

**Key Details:**
- **File:** `skills/test-spec/agents/tspec-generator.md`
- **Symptom:** Feature file missing scenarios for extensions with non-standard outcome values
- **Frequency:** When use case extensions use non-standard outcome formats
- **Fix Complexity:** Low
- **Source:** C4 tournament S-012 FMEA (FM-004, RPN 320)

---

## Steps to Reproduce

1. Create a use case with an extension that has an outcome value not matching `success|failure|rejoin:\d+`
2. Invoke tspec-generator to produce a BDD feature file from the use case
3. Observe that the extension is silently skipped -- no scenario generated and no warning emitted

---

## Acceptance Criteria

- [ ] tspec-generator emits a warning when an extension outcome value does not match the recognized pattern
- [ ] Non-standard outcome values produce a diagnostic message identifying the skipped extension
- [ ] Feature file output includes a comment or marker indicating skipped extensions
- [ ] No silent data loss for unrecognized extension outcomes

---

## Related Items

### Hierarchy

- **Parent:** PROJ-030-bugs

### Related Items

- **GitHub Issue:** [#195](https://github.com/geekatron/jerry/issues/195)
- **Parent Issue:** [#194](https://github.com/geekatron/jerry/issues/194)
- **Labels:** bug

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-03-14 | pending | Triaged from GitHub Issue #195 |
