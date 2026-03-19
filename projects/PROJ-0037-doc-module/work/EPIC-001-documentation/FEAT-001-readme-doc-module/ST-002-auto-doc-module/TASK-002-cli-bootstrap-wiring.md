# TASK-002: Wire CLI docs namespace to DocsGenerator via bootstrap.py

> **Type:** task
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Created:** 2026-03-10T00:00:00Z
> **Due:**
> **Completed:** 2026-03-10T00:00:00Z
> **Parent:** ST-002
> **Owner:** eng-backend-3
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

Phase 2 of the implementation pipeline. Wire the docs bounded context into the CLI:
- Add `create_docs_generator()` factory function to `src/bootstrap.py`
- Add `_handle_docs()` dispatch function to `src/interface/cli/main.py`
- Do NOT modify `parser.py` — `_add_docs_namespace()` already exists

---

## Acceptance Criteria

- [ ] `uv run jerry docs generate` runs without error and prints generated sections to stdout
- [ ] `uv run jerry docs generate --check` exits 0 when README is current, exits 1 when drift detected
- [ ] `uv run jerry docs generate --write` updates README.md between marker comments
- [ ] `create_docs_generator()` follows existing factory function patterns in bootstrap.py
- [ ] No circular imports between `src/docs/` and `src/bootstrap.py`

---

## Related Items

### Hierarchy

- **Parent Story:** [ST-002](../ST-002-auto-doc-module.md)
- **Orchestration Phase:** impl-20260310-001 / phase-2 / eng-backend-3
- **Depends On:** TASK-001 (Barrier 1 PASS required)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-10 | Claude | pending | Task created; awaiting Barrier 1 |
| 2026-03-10 | Claude | in_progress | Barrier 1 PASSED; Phase 2 started |
| 2026-03-10 | Claude | completed | Barrier 2 PASSED (0.9435 >= 0.94, 5 iterations). Mode mapping bug found+fixed. Template path guard added. 18 tests passing. |
