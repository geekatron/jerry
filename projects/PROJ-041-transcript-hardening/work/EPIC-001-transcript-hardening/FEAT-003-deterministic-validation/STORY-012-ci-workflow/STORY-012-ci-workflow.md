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
| [Summary](#summary) | What this story delivers |
| [CI Gate Design](#ci-gate-design) | Where and how it runs |
| [Agent Assignment](#agent-assignment) | Specific skill+agent mappings |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Children Tasks](#children-tasks) | Task breakdown |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Status changes |

---

## Summary

Add a CI workflow that runs the validators against golden packets on every PR, blocking merge on validator failures or coverage drops. Branch protection requires this check. Hash-pinned action versions per supply-chain hardening; runtime environment validated for parity with developer-local execution.

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

## Agent Assignment

| Step | Skill | Agent | Purpose |
|------|-------|-------|---------|
| 1 | `/eng-team` | `eng-devsecops` | Author `.github/workflows/transcript-validators.yml`; hash-pin action versions per supply-chain hardening; configure coverage gates (≥90% module / ≥95% subprocess sandbox) |
| 2 | `/eng-team` | `eng-devsecops` | PR comment posting on failure (validator summary); branch protection update (require this check) |
| 3 | `/eng-team` | `eng-security` | Workflow security review: no secrets leak, principle of least privilege on workflow permissions |
| 4 | `/eng-team` | `eng-qa` | End-to-end test: workflow runs against test_data/golden/ on PR; blocks merge on validator failure |
| 5 | `/eng-team` | `eng-infra` | Validate CI runtime environment matches developer-local execution (no env-drift between CI and local SubprocessSandbox behavior); per ps-architect D-4.5 |
| 6 | `/adversary` | `adv-executor` + `adv-scorer` | C4 ≥0.95 review on workflow + supply chain hardening |
| 6 | `/worktracker` | `wt-verifier` | Validate AC; close |

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

| ID | Title | Owner | Status |
|----|-------|-------|--------|
| [TASK-132](./TASK-132-author-transcript-validators-workflow.md) | Author .github/workflows/transcript-validators.yml; hash-pin actions; coverage gates | `eng-devsecops` | pending |
| [TASK-133](./TASK-133-configure-pr-comment-and-branch-protection.md) | PR comment posting on failure (validator summary); branch protection update | `eng-devsecops` | pending |
| [TASK-134](./TASK-134-workflow-security-review.md) | Workflow security review: no secrets leak, principle of least privilege | `eng-security` | pending |
| [TASK-135](./TASK-135-e2e-test-against-golden-packets.md) | End-to-end test: workflow runs against test_data/golden/ on PR; blocks merge on validator failure | `eng-qa` | pending |
| [TASK-136](./TASK-136-validate-runtime-env-parity.md) | Validate CI runtime environment matches developer-local execution (per ps-architect D-4.5) | `eng-infra` | pending |
| [TASK-137](./TASK-137-run-adversary-c4-review.md) | Run /adversary C4 review on workflow + supply chain hardening | `adv-executor` | pending |

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
