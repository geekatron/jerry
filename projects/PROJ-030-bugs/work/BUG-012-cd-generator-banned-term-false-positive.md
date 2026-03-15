# BUG-012: cd-generator banned-term check false positives on domain vocabulary under 60 chars (#198)

> **Type:** bug
> **Status:** pending
> **Priority:** low
> **Impact:** low
> **Severity:** minor
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

The cd-generator agent's Layer 2a banned-term substring check can produce false positives on legitimate domain descriptions containing words like "pending" when the description is under 60 characters. The substring matching is overly broad and does not account for context or word boundaries. This was identified as PM-008 during C4 tournament S-014 iteration score reports.

**Key Details:**
- **File:** `skills/contract-design/agents/cd-generator.md`
- **Symptom:** Legitimate domain vocabulary flagged as banned terms in short descriptions
- **Frequency:** When API descriptions contain common domain words that overlap with banned terms
- **Fix Complexity:** Low
- **Source:** C4 tournament S-014 iteration score reports (PM-008)

---

## Steps to Reproduce

1. Create a use case realization artifact with a description containing domain vocabulary (e.g., "pending approval status")
2. Invoke cd-generator to produce an OpenAPI contract
3. Observe Layer 2a banned-term check flags "pending" as a banned term
4. Note the description is under 60 characters, triggering the false positive

---

## Acceptance Criteria

- [ ] Banned-term check uses word-boundary matching instead of substring matching
- [ ] Domain vocabulary in legitimate descriptions is not flagged as banned terms
- [ ] Descriptions under 60 characters are not disproportionately affected
- [ ] Existing banned-term detection for genuinely problematic terms is preserved

---

## Related Items

### Hierarchy

- **Parent:** PROJ-030-bugs

### Related Items

- **GitHub Issue:** [#198](https://github.com/geekatron/jerry/issues/198)
- **Parent Issue:** [#194](https://github.com/geekatron/jerry/issues/194)
- **Labels:** bug

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-03-14 | pending | Triaged from GitHub Issue #198 |
