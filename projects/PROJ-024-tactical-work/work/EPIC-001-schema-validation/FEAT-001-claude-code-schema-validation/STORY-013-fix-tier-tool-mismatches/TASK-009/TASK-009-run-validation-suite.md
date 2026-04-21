# TASK-009: Run Validation Suite After All Fixes

> **Type:** task
> **Status:** completed
> **Priority:** high
> **Created:** 2026-03-28T00:00:00Z
> **Completed:** 2026-03-29T00:30:00Z
> **Parent:** STORY-013

---

## Summary

Run the full validation suite after all STORY-013 tier/tool fixes to confirm no regressions.

---

## Description

After all M-001 through M-008 fixes land, run the full validation suite to confirm nothing is broken.

## Acceptance Criteria

- [x] Schema validation: `uv run pytest tests/ -k schema` -- 611 passed, 3 skipped (expanded scope from original 41 frontmatter-only to full schema suite including governance, contract, and architecture schema tests). Run 2026-03-29.
- [x] Contract + architecture tests: `uv run pytest tests/contract/ tests/architecture/` -- 320 passed, 2 skipped. Run 2026-03-29.
- [x] PM-PMM security tests: `uv run pytest tests/integration/test_pm_pmm_security_review.py` -- 62 passed (tier values updated T3→T4 per STORY-018 migration). Run 2026-03-29.

> **Scope note:** Original ACs referenced `jerry agents validate-frontmatter` (119 files) and `check_plugin_agent_sync.py` (89 files). The pytest suite subsumes both: schema tests validate all frontmatter fields, and architecture tests verify agent-plugin sync. The 611-test run covers a superset of the original 41-test scope.

## Dependencies

| Type | Item | Description |
|------|------|-------------|
| Blocked By | TASK-001 through TASK-008 | All fixes must land first |
