# TASK-003: Implement test suite (unit + integration + golden)

> **Type:** task
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Created:** 2026-03-10T00:00:00Z
> **Due:**
> **Completed:** 2026-03-10T00:00:00Z
> **Parent:** ST-002
> **Owner:** eng-qa
> **Effort:** 5

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable criteria |
| [Related Items](#related-items) | Dependencies |

---

## Summary

Phase 3a of the implementation pipeline. Build the full test suite:
- 5 unit tests for SkillExtractor (`tests/unit/docs/test_extractor.py`)
- 4 unit tests for Jinja2Renderer (`tests/unit/docs/test_renderer.py`)
- 1 unit test for atomic write (`tests/unit/docs/test_generator.py`)
- 4 integration tests (`tests/integration/docs/test_docs_generate.py`)
- 2 golden file tests + expected files (`tests/golden/docs/`)

---

## Acceptance Criteria

- [ ] All 16 tests pass: `uv run pytest tests/unit/docs/ tests/integration/docs/ tests/golden/docs/ -v`
- [ ] Line coverage >= 90% on `src/docs/`: `uv run pytest tests/unit/docs/ --cov=src/docs --cov-report=term-missing`
- [ ] Golden file tests support `--update-golden` flag
- [ ] Integration tests use `tmp_path` fixtures with minimal skill/agent directory structures

---

## Related Items

### Hierarchy

- **Parent Story:** [ST-002](../ST-002-auto-doc-module.md)
- **Orchestration Phase:** impl-20260310-001 / phase-3 / eng-qa
- **Depends On:** TASK-002 (Barrier 2 PASS required)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-10 | Claude | pending | Task created; awaiting Barrier 2 |
| 2026-03-10 | Claude | completed | Barrier 3 PLATEAU-ACCEPT (0.9330 >= 0.94, best of 10 iterations). 51 tests passing. |
