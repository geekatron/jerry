# STORY-009: Add Frontmatter Schema Validation to CI Pipeline

<!--
TEMPLATE: Story
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
PURPOSE: Ensure every PR validates all agent and skill definitions against frontmatter schemas
-->

> **Type:** story
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Created:** 2026-03-27T08:00:00Z
> **Due:**
> **Completed:** 2026-03-27T06:00:00Z
> **Parent:** FEAT-001
> **Owner:** adam.nowak
> **Effort:** 3

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [User Story](#user-story) | As a / I want / So that |
| [Summary](#summary) | What needs to happen |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Children (Tasks)](#children-tasks) | Task breakdown |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Status changes |

---

## User Story

**As a** Jerry framework contributor submitting a PR

**I want** CI to automatically validate all agent and skill frontmatter against the Anthropic schemas

**So that** invalid definitions (wrong field names, multiline descriptions, missing required fields) are caught before merge, not discovered at runtime

---

## Summary

The `jerry agents validate-frontmatter` CLI command exists (STORY-008) and validates all 119 definitions. But it's not wired into the CI pipeline (`.github/workflows/ci.yml`). A contributor could introduce a broken agent definition (e.g., `tools:` instead of `allowed-tools:` in a SKILL.md) and CI would pass.

The existing CI already has a `plugin-validation` job and a `cli-integration` job -- the new job follows the same pattern.

**Scope:**
- Add a `frontmatter-validation` job to `.github/workflows/ci.yml`
- Job runs `uv run jerry agents validate-frontmatter`
- Exit code 1 = CI failure (invalid definitions found)
- Add to the `ci-success` final gate check
- JSON output mode for potential future PR comment integration

**Not in scope:**
- PR comment with validation results (future enhancement)
- Pre-commit hook (separate concern)

---

## Acceptance Criteria

- [ ] `.github/workflows/ci.yml` contains a `frontmatter-validation` job
- [ ] Job installs dependencies via `uv sync --frozen`
- [ ] Job runs `uv run jerry agents validate-frontmatter` and fails on non-zero exit
- [ ] `ci-success` job includes `frontmatter-validation` in its `needs` list
- [ ] `ci-success` job checks `frontmatter-validation.result` in the final gate
- [ ] A PR introducing `tools:` in a SKILL.md (instead of `allowed-tools:`) would fail CI
- [ ] A PR introducing a multiline `description: >` in an agent .md would fail CI

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Owner |
|----|-------|--------|-------|
| TASK-001 | Add frontmatter-validation job to ci.yml | pending | -- |
| TASK-002 | Add to ci-success needs list and gate check | pending | -- |
| TASK-003 | Verify CI would catch known-bad definitions | pending | -- |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-001: Claude Code Schema Validation](../FEAT-001-claude-code-schema-validation.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | STORY-008 | CLI command must exist |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-27 | adam.nowak | pending | Story created -- CI has no frontmatter validation today |
