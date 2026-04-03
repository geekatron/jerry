# STORY-025: Add jerry schema validate CLI Command (GH #193)

> **Type:** story
> **Status:** completed
> **Priority:** medium
> **Impact:** high
> **Created:** 2026-03-30T00:00:00Z
> **Due:**
> **Completed:** 2026-03-30T12:00:00Z
> **Parent:** FEAT-001
> **Owner:**
> **Effort:** 2
> **GitHub Issue:** [#193](https://github.com/geekatron/jerry/issues/193)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What and why |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Dependencies](#dependencies) | Relationship to other work |
| [History](#history) | Change log |

---

## Summary

`scripts/validate-agent-frontmatter.py` runs as a separate CI step alongside `jerry agents validate-frontmatter`. This creates two parallel code paths that can drift. Port ALL validation logic (including the STORY-022 P-003 check) into the CLI command handler. Delete the standalone script. One code path, one entry point.

---

## Architectural Constraints

| Constraint | Rationale |
|------------|-----------|
| **MUST NOT keep standalone validation scripts** | `scripts/validate-agent-frontmatter.py` is a parallel implementation of what the CLI does. Maintaining two is a regression risk. |
| **All validation MUST go through `jerry agents validate-frontmatter`** | CLI is the single entry point. CI invokes the CLI. Developers invoke the CLI. Tests invoke the CLI handler. |
| **MUST follow Clean Architecture** | Validation logic in `src/agents/application/commands/validate_frontmatter_command.py` (application layer). Schema loading from `docs/schemas/` (infrastructure adapter). |
| **H-10 resolution required** | The handler file has a pre-existing H-10 violation (3 classes in one file). Must be resolved to allow edits -- split `FrontmatterFileResult`, `ValidateFrontmatterResult`, and `ValidateFrontmatterCommandHandler` into separate files. |
| **Tests MUST live in `tests/`** | `scripts/tests/test_validate_agent_frontmatter.py` must be moved to `tests/` and rewritten to test the CLI handler, not the deleted script. |
| **MUST follow TDD Red/Green/Refactor (H-20)** | Write failing test for P-003 check via CLI handler BEFORE porting. Red: test calls handler, no P-003 check, fails. Green: port check from script, test passes. Refactor: delete script + script tests. |

---

## Acceptance Criteria

- [x] `jerry agents validate-frontmatter` includes P-003 Agent tool check (string normalization, type-hardened T5, fail-closed governance lookup)
- [x] `scripts/validate-agent-frontmatter.py` deleted
- [x] `scripts/tests/test_validate_agent_frontmatter.py` moved to `tests/` and tests CLI handler
- [x] CI workflow uses single `uv run jerry agents validate-frontmatter` (remove separate script step from ci.yml)
- [x] 89/89 agents pass via CLI command
- [x] H-10 violation in `validate_frontmatter_command.py` resolved (3 classes split into separate files)
- [x] Zero validation scripts remain in `scripts/`
- [x] Full test suite passes

---

## Dependencies

| Type | Item | Description |
|------|------|-------------|
| Blocked By | BUG-004 | Clean test baseline |
| Blocked By | BUG-005 | All hook tests passing |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-30 | adam.nowak | pending | Created from PROJ-024 session. Linked to GH #193. |
| 2026-03-30 | adam.nowak | completed | Commit `4600c0ae`. Split H-10 (4 files), ported P-003 check, deleted script + script tests, updated CI. 8 P-003 tests + 41 schema tests green. GH #193 closed. |
