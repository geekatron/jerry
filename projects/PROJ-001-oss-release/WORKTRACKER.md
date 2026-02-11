# PROJ-001: OSS Release - Work Tracker

> Work tracking for preparing Jerry for open-source release.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Project overview and status |
| [Epics](#epics) | Strategic work items |
| [Enablers](#enablers) | Technical enabler work items |
| [Bugs](#bugs) | Tracked defects |
| [Completed](#completed) | Finished items |

---

## Summary

| Field | Value |
|-------|-------|
| Project | PROJ-001-oss-release |
| Status | ACTIVE |
| Created | 2026-02-10 |
| PR | [#6](https://github.com/geekatron/jerry/pull/6) |

---

## Epics

| ID | Title | Status | Priority | Features | Progress |
|----|-------|--------|----------|----------|----------|
| [EPIC-001](./work/EPIC-001-oss-release/EPIC-001-oss-release.md) | OSS Release Preparation | in_progress | high | 1 | 40% |

---

## Enablers

| ID | Title | Status | Priority | Parent | Children |
|----|-------|--------|----------|--------|----------|
| [EN-001](./work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/EN-001-fix-plugin-validation/EN-001-fix-plugin-validation.md) | Fix Plugin Validation | in_progress | high | FEAT-001 | BUG-001, TASK-001/002/003, DEC-001 |
| [EN-002](./work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/EN-002-fix-test-infrastructure/EN-002-fix-test-infrastructure.md) | Fix Test Infrastructure | pending | medium | FEAT-001 | BUG-004, BUG-005 |

---

## Bugs

| ID | Title | Status | Priority | Severity | Parent |
|----|-------|--------|----------|----------|--------|
| [BUG-001](./work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/EN-001-fix-plugin-validation/BUG-001-marketplace-manifest-schema-error.md) | Marketplace manifest schema error: `keywords` not allowed | in_progress | high | major | EN-001 |
| [BUG-004](./work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/EN-002-fix-test-infrastructure/BUG-004-transcript-pipeline-no-datasets.md) | Transcript pipeline test finds no datasets | pending | medium | major | EN-002 |
| [BUG-005](./work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/EN-002-fix-test-infrastructure/BUG-005-project-validation-missing-artifacts.md) | Project validation tests reference non-existent PROJ-001-plugin-cleanup | pending | medium | major | EN-002 |

---

## Completed

| ID | Title | Completed | Resolution |
|----|-------|-----------|------------|
| [BUG-002](./work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/FEAT-001--BUG-002-cli-projects-list-crash.md) | CLI `projects list` crashes with unhandled exception | 2026-02-10 | Resolved by committing `projects/` directory to git |
| [BUG-003](./work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/FEAT-001--BUG-003-bootstrap-test-missing-projects-dir.md) | Bootstrap test assumes `projects/` directory exists | 2026-02-10 | Resolved by committing `projects/` directory to git |
