# STORY-036-005: CI/CD Wiring for Automated Regression

<!--
TEMPLATE: Story
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
-->

> **Type:** story
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-03-07T00:00:00Z
> **Due:** —
> **Completed:** —
> **Parent:** FEAT-036-004
> **Owner:** —
> **Effort:** 5

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [User Story](#user-story) | As a/I want/So that |
| [Summary](#summary) | Scope and context |
| [Acceptance Criteria](#acceptance-criteria) | Observable outcomes |
| [Progress Summary](#progress-summary) | Completion metrics |
| [Related Items](#related-items) | Dependencies |
| [History](#history) | Status changes |

---

## User Story

**As a** framework maintainer

**I want** the CI/CD pipeline to automatically run regression checks when agent definitions or test harness code changes

**So that** prompt quality regressions are caught before merging to main

---

## Summary

Wire the existing GitHub Actions workflows (`.github/workflows/prompt-regression-standard.yml` and `prompt-regression-full.yml`) to execute real regression checks using the populated baselines. The standard workflow runs on PR for affected paths (agent definitions, `jerry/testing/`), using Layer 2 G-Eval scoring against stored baselines. The full workflow runs on schedule or manual trigger, including Layer 3 MR tests and Layer 4 statistical comparison.

**Scope:**
- Update `prompt-regression-standard.yml` to load real baselines and run Layer 2 scoring
- Update `prompt-regression-full.yml` to include Layer 3 MR and Layer 4 comparison
- Configure Docker image with baseline data or baseline store path
- Set up `ANTHROPIC_API_KEY` as GitHub Actions secret
- Define PR check gate: BLOCK verdict = required check failure, WARNING = annotation

---

## Acceptance Criteria

- [ ] Standard workflow runs Layer 2 G-Eval regression check on PR when agent definitions change
- [ ] Full workflow runs Layer 2 + Layer 3 + Layer 4 on schedule or manual trigger
- [ ] BLOCK verdict from Layer 4 causes the GitHub check to fail (blocks merge)
- [ ] WARNING verdict from Layer 4 posts an annotation but does not block merge
- [ ] `ANTHROPIC_API_KEY` configured as repository secret for CI runs

---

## Progress Summary

| Metric | Value |
|--------|-------|
| **Total Tasks** | 0 |
| **Completed Tasks** | 0 |
| **Completion %** | 0% |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-036-004: Baseline Collection and Validation Execution](./FEAT-036-004-baseline-execution.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | STORY-036-003 | Requires populated baselines for comparison |
| Depends On | STORY-036-004 | Validates Layer 4 works with real baselines |
| Uses | `.github/workflows/prompt-regression-standard.yml` | Standard CI workflow |
| Uses | `.github/workflows/prompt-regression-full.yml` | Full CI workflow |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-07 | Claude | pending | Story created; wires real baselines into CI/CD pipeline for automated regression gating |
