# TASK-006: Final architecture compliance and coverage gate

> **Type:** task
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Created:** 2026-03-10T00:00:00Z
> **Due:**
> **Completed:** 2026-03-11T00:00:00Z
> **Parent:** ST-002
> **Owner:** eng-reviewer
> **Effort:** 3

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable criteria |
| [Related Items](#related-items) | Dependencies |

---

## Summary

Phase 4 of the implementation pipeline. Final gate verification:
- Hexagonal layer isolation (H-07)
- One-class-per-file (H-10)
- Type hints + docstrings (H-11)
- M-1 through M-5 controls present in final code
- Full test suite passes
- Line coverage >= 90%
- `uv run jerry docs generate --check` exits 0

---

## Acceptance Criteria

- [ ] `uv run pytest tests/ -v --tb=short` — full test suite passes
- [ ] `uv run pytest tests/unit/docs/ --cov=src/docs --cov-report=term-missing` — >= 90% coverage
- [ ] `uv run jerry docs generate --check` — exits 0 against current README
- [ ] H-07, H-10, H-11 compliance verified
- [ ] M-1 through M-5 controls verified in final code

---

## Related Items

### Hierarchy

- **Parent Story:** [ST-002](../ST-002-auto-doc-module.md)
- **Orchestration Phase:** impl-20260310-001 / phase-4 / eng-reviewer
- **Depends On:** TASK-003, TASK-004, TASK-005 (Barrier 3 PASS required)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-10 | Claude | pending | Task created; awaiting Barrier 3 |
| 2026-03-11 | Claude | completed | Barrier 4 PASS (0.9480 >= 0.94, 4 iterations). BLOCKING: AstFrontmatterReader defect — `jerry docs generate --check` exits 1, all 27 skills skipped. See BUG-001. |
