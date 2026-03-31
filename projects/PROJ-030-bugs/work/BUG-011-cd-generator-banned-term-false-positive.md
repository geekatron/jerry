# BUG-011: cd-generator banned-term false positives under 60 chars (#198)

> **Type:** bug
> **Status:** pending
> **Priority:** medium
> **Impact:** high
> **Severity:** major
> **Created:** 2026-03-31
> **Parent:** PROJ-030-bugs
> **GitHub Issue:** [#198](https://github.com/geekatron/jerry/issues/198)
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

SUBSTRING_TERMS list includes bare `pending` with underspecified word-boundary matching. Combined with <60 char length gate, legitimate domain terms like "impending return item" get incorrectly rejected.

## Steps to Reproduce

1. Invoke `/contract-design` cd-generator with a use case containing the operation description "impending return item"
2. Observe that Layer 2a banned-term check rejects the description because "pending" substring-matches within "impending"
3. Note the description is under 60 characters, so the length gate does not bypass the check

## Fix

Specify explicit word-boundary regex pattern (`\bpending\b`). Add domain vocabulary allowlist. Add test examples documenting expected behavior for edge cases.

## Files

- `skills/contract-design/agents/cd-generator.md` (lines 120-143, Layer 2a banned-term check)

## Acceptance Criteria

- [ ] Word-boundary matching uses explicit `\b` pattern or equivalent
- [ ] "impending" does not match when searching for "pending"
- [ ] Domain vocabulary terms under 60 chars are not false-positived
