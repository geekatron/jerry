# STORY-012: CI workflow runs validators against golden packets

> **Type:** story
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-04-28T00:00:00Z
> **Parent:** FEAT-003
> **Owner:** adam.nowak
> **Effort:** 3

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [User Story](#user-story) | As a / I want / So that |
| [CI Gate Design](#ci-gate-design) | Where and how it runs |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Children Tasks](#children-tasks) | Task breakdown |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Status changes |

---

## User Story

**As a** Jerry maintainer reviewing a PR that touches `/transcript`,
**I want** CI to run all 17 validators against the golden packet set on every PR,
**So that** validator regressions are caught at PR time, not at next adversary review.

---

## CI Gate Design

| Aspect | Decision |
|--------|----------|
| Workflow file | `.github/workflows/transcript-validators.yml` |
| Trigger | `pull_request` paths: `src/jerry/transcript/validation/**`, `skills/transcript/**`, `test_data/golden/**`, `docs/adrs/ADR-007-*.md`, `schemas/**` |
| Job | Run `uv run pytest tests/transcript/validation/golden/` |
| Coverage gate | ≥90% on `src/jerry/transcript/validation/` (≥95% for `infrastructure/subprocess_sandbox.py`) |
| Required check | Yes — branch protection requires this check passing |
| Caching | uv cache + golden packet content hash |

---

## Acceptance Criteria

- [ ] Workflow file `.github/workflows/transcript-validators.yml` exists and runs on relevant PRs.
- [ ] Workflow runs `uv run pytest tests/transcript/validation/golden/` (per H-05 UV-only).
- [ ] Workflow enforces ≥90% coverage on validation module; ≥95% on subprocess sandbox.
- [ ] Workflow blocks merge when validators fail or coverage drops.
- [ ] Workflow runtime under 5 minutes on standard CI runner.
- [ ] PR comment posts validator summary on failure (which rules + which goldens failed).
- [ ] Branch protection updated to require this check.
- [ ] `/eng-team` `eng-devsecops` review on workflow security (no secrets leak, hash-pinned actions).
- [ ] `/adversary` C4 ≥0.95 phase gate.

---

## Children Tasks

| ID | Title | Status |
|----|-------|--------|
| TASK-001 | Author .github/workflows/transcript-validators.yml | pending |
| TASK-002 | Hash-pin action versions per supply-chain hardening | pending |
| TASK-003 | Configure coverage gates | pending |
| TASK-004 | Configure PR comment on failure | pending |
| TASK-005 | Update branch protection (manual settings or repo-config-as-code) | pending |
| TASK-006 | Run /eng-team eng-devsecops review | pending |
| TASK-007 | Run /adversary C4 review | pending |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-003](../FEAT-003-deterministic-validation.md)

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| Blocked By | STORY-003..STORY-006, EN-002 | Validators + golden packets must exist |
| Blocked By | STORY-007 | CLI must exist (workflow may invoke CLI directly) |
| Blocks | EN-008 | Final tournament expects CI gate in place |

### Source

- [#273 §C5](https://github.com/geekatron/jerry/issues/273) — acceptance criteria mention CI workflow

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-04-28 | adam.nowak (via Claude scaffold) | pending | Story created. |
