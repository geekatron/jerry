# TASK-164: Regression test: bracket-canonical golden renders cleanly via mmdc

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** BUG-006
> **Owner:** eng-qa

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Actual render check, not text inspection. Uses test_data/golden/bracket-canonical/.

---

## Acceptance Criteria

- [ ] mmdc renders mindmap.mmd to SVG without parse error
- [ ] Output SVG file exists and is non-empty (>1KB)
- [ ] Test integrated into CI
