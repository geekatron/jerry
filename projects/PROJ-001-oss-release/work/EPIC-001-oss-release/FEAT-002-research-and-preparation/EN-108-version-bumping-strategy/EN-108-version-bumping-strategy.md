# EN-108: Version Bumping Strategy

> **Type:** enabler
> **Status:** done
> **Priority:** high
> **Impact:** high
> **Enabler Type:** infrastructure
> **Created:** 2026-02-12
> **Due:** —
> **Completed:** 2026-02-12
> **Parent:** FEAT-002
> **Owner:** —
> **Effort:** 8

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this enabler delivers |
| [Problem Statement](#problem-statement) | Why version bumping automation is needed |
| [Business Value](#business-value) | How this supports OSS release |
| [Technical Approach](#technical-approach) | Research and implementation plan |
| [Children (Tasks)](#children-tasks) | Task breakdown |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Dependencies](#dependencies) | What this depends on and enables |
| [Related Items](#related-items) | Hierarchy and cross-references |
| [History](#history) | Change log |

---

## Summary

Research, analyze, and implement an automated version bumping process for the Jerry project. After PRs are merged, version numbers in the marketplace manifest (`marketplace.json`), plugin manifest (`plugin.json`), and `pyproject.toml` need to be bumped consistently and automatically as part of the CI/CD pipeline.

**Technical Scope:**
- Research version bumping tools and strategies (conventional commits, semantic-release, custom GitHub Actions)
- Analyze current version locations: `.claude-plugin/marketplace.json` (two version fields), `.claude-plugin/plugin.json`, `pyproject.toml`
- Design a process that fits Jerry's existing CI/CD (GitHub Actions, pre-commit hooks)
- Implement the chosen solution

---

## Problem Statement

The Jerry project has version numbers in three files across two formats (JSON and TOML). Currently, version bumping is manual and error-prone. As an OSS project with external contributors and consumers, version consistency is critical for:

1. Plugin marketplace compatibility
2. Package distribution (PyPI)
3. Release tracking and changelog generation
4. Consumer confidence in release cadence

Without automation, versions will drift out of sync or be forgotten during releases.

---

## Business Value

- Enables reliable, repeatable releases for the OSS project
- Reduces manual error during release process
- Establishes professional release cadence expected of OSS projects
- Supports future automated changelog generation

### Features Unlocked

- Automated release workflow
- Changelog generation from conventional commits
- Marketplace version synchronization

---

## Technical Approach

### Phase 1: Research (TASK-001, TASK-002)

Investigate version bumping approaches:
- Conventional Commits + semantic-release
- GitHub Actions-based bumping (on merge to main)
- Python-specific tools (bump2version, python-semantic-release)
- Custom scripts vs off-the-shelf solutions
- How to keep 3 files in sync (single source of truth strategy)

### Phase 2: Design (TASK-003)

Design the chosen approach:
- Where version lives as single source of truth
- How other files derive their version
- CI/CD pipeline integration points
- Branch protection and merge workflow compatibility

### Phase 3: Implementation (TASK-004, TASK-005)

Implement and validate:
- Create/configure the tooling
- Add GitHub Actions workflow
- Test the full flow end-to-end

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Effort | Owner | Blocked By |
|----|-------|--------|--------|-------|------------|
| [TASK-006](./TASK-006-create-orchestration-plan.md) | Create orchestration plan (/orchestration + /problem-solving + /nasa-se) | done | 2 | — | — |
| [TASK-001](./TASK-001-research-version-bumping-tools.md) | Research version bumping tools and approaches | done | 2 | — | — |
| [TASK-002](./TASK-002-analyze-current-version-locations.md) | Analyze current version locations and sync strategy | done | 1 | — | — |
| [TASK-003](./TASK-003-design-version-bumping-process.md) | Design version bumping process and CI/CD integration | done | 2 | — | TASK-001, TASK-002 |
| [TASK-004](./TASK-004-implement-version-bumping.md) | Implement version bumping automation | done | 2 | — | TASK-003 |
| [TASK-005](./TASK-005-validate-end-to-end.md) | Validate end-to-end version bumping flow | done | 1 | — | TASK-004 |

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   ENABLER PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Tasks:     [####################] 100% (6/6 completed)            |
| Effort:    [####################] 100% (10/10 points completed)   |
+------------------------------------------------------------------+
| Overall:   [####################] 100%                             |
+------------------------------------------------------------------+
```

---

## Acceptance Criteria

### Definition of Done

- [x] Research completed: tools evaluated with pros/cons (6 tools, BMV recommended)
- [x] Single source of truth for version identified (pyproject.toml)
- [x] Version sync mechanism covers all 3 files (BMV + sync script + pre-commit + CI)
- [x] CI/CD pipeline bumps version automatically on merge to main (version-bump.yml)
- [x] End-to-end flow validated (TASK-005 score 0.938, 35/35 requirements)
- [x] Documentation updated with release process (design doc + orchestration artifacts)

---

## Dependencies

### Depends On

- FEAT-001 (CI build must be stable first) - DONE

### Enables

- Automated release workflow
- Marketplace publishing
- Changelog generation

---

## Related Items

### Hierarchy

- **Parent:** [FEAT-002: Research and Preparation](../FEAT-002-research-and-preparation.md)
- **Grandparent:** [EPIC-001: OSS Release Preparation](../../EPIC-001-oss-release.md)

### Version Locations

| File | Field | Current Value |
|------|-------|---------------|
| `.claude-plugin/marketplace.json` | `version` | 1.0.0 (schema version, not synced — REV-1) |
| `.claude-plugin/marketplace.json` | `plugins[0].version` | 0.2.0 |
| `.claude-plugin/plugin.json` | `version` | 0.2.0 |
| `pyproject.toml` | `version` | 0.2.0 (SSOT) |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-12 | Claude | pending | Enabler created with 5 tasks |
| 2026-02-12 | Claude | done | All 6 tasks complete. 4-phase orchestration workflow: research (0.928/0.935), design (0.926), implementation (commit 8bab29f), validation (0.938). 35/35 requirements, all REVs compliant. CP-004 approved. |
