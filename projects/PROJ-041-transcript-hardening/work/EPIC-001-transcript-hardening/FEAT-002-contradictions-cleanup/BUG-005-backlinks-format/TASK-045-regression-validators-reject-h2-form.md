# TASK-045: Regression: validators reject packets using ## Backlinks H2 form

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** BUG-005
> **Owner:** eng-qa

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Test that FEAT-003 STORY-004 CONTENT-* validators reject the deprecated H2 form (covered in CONTENT-* family acceptance criteria).

---

## Acceptance Criteria

- [ ] Test packet with `## Backlinks` H2 produces validation failure
- [ ] Test packet with `<backlinks>` tag passes validation
