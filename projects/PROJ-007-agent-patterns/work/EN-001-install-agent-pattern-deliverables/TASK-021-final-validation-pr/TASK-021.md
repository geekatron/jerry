# TASK-021: Final validation + commit + PR

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Criticality:** C3
> **Created:** 2026-02-21T23:59:00Z
> **Parent:** EN-001
> **Owner:** --
> **Effort:** 2
> **Activity:** deployment

---

## Summary

Run final end-to-end validation, commit all EN-001 installation changes, and create the pull request.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Description](#description) | What this task requires |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Implementation Notes](#implementation-notes) | Technical approach and constraints |
| [Related Items](#related-items) | Parent and related work |
| [History](#history) | Status changes |

---

## Description

Run full end-to-end validation of all EN-001 installation work: pre-commit hooks, pytest suite, and constitutional compliance check (S-007). After all checks pass, commit all installation changes with a semantic commit message and create a pull request to merge `feat/proj-007-agent-patterns` into `main`.

This task is the terminal task for EN-001. All prior tasks (TASK-012 through TASK-020) must be complete before this task begins.

### Steps

1. Verify all prior tasks (TASK-012..TASK-020) are marked done
2. Run pre-commit hooks: `uv run pre-commit run --all-files`
3. Run test suite: `uv run pytest tests/`
4. Run constitutional compliance check (S-007) against all installed files
5. Verify HARD rule budget (H-32..H-35 added, total <= 35)
6. Verify no orphan H-rule references in quality-enforcement.md
7. Stage all installation changes with `git add` (specific files, not `-A`)
8. Commit with semantic message referencing EN-001 and PROJ-007
9. Push branch and create PR via `gh pr create`

---

## Acceptance Criteria

- [ ] AC-1: All pre-commit hooks pass (`uv run pre-commit run --all-files`)
- [ ] AC-2: All tests pass (`uv run pytest tests/`)
- [ ] AC-3: Constitutional compliance check (S-007) passes for all installed files
- [ ] AC-4: HARD rule budget verified: H-01..H-35, total <= 35
- [ ] AC-5: No orphan H-rule references (every rule in quality-enforcement.md HARD index has a source file)
- [ ] AC-6: Commit created with semantic message referencing PROJ-007 / EN-001
- [ ] AC-7: PR created targeting `main` branch and ready for review

---

## Implementation Notes

### Validation Sequence

Run in this order (stop on first failure):

1. `uv run pre-commit run --all-files`
2. `uv run pytest tests/`
3. Manual S-007 constitutional compliance sweep of installed files
4. Orphan reference audit of quality-enforcement.md HARD index

### Commit Message Pattern

```
feat(proj-007): install agent pattern deliverables into framework

Install PROJ-007 orchestration output (agent-patterns-20260221-001):
- agent-development-standards.md → .context/rules/
- agent-routing-standards.md → .context/rules/
- ADR-PROJ007-001 and ADR-PROJ007-002 → docs/design/
- H-32..H-35 → quality-enforcement.md HARD rule index
- agent-pattern-taxonomy.md → docs/knowledge/
- agent-definition-v1.schema.json → docs/schemas/
- CLAUDE.md and mandatory-skill-usage.md updated

Closes EN-001. All quality gates pass (avg 0.957 orchestration + C4 tournament 0.952).
```

### PR Body

Include:
- Summary of what was installed
- Link to PROJ-007 orchestration run
- Checklist of AC items from EN-001
- Test plan (hooks, pytest, S-007)

### UV Enforcement

All Python execution MUST use `uv run`. NEVER use `python` or `pytest` directly (H-05).

### Dependency

All of TASK-012 through TASK-020 must be complete before this task starts.

---

## Related Items

- **Parent:** [EN-001](../EN-001.md)
- **Depends on:** TASK-012, TASK-013, TASK-014, TASK-015, TASK-016, TASK-017, TASK-018, TASK-019, TASK-020 (all must be done)
- **Target branch:** `main`
- **Orchestration run:** `agent-patterns-20260221-001`

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-21 | pending | Created — terminal task for EN-001; all other tasks must complete first |
