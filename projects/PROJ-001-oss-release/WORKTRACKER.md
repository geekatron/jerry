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
| Status | COMPLETED |
| Created | 2026-02-10 |
| PR | [#6](https://github.com/geekatron/jerry/pull/6) |

---

## Epics

| ID | Title | Status | Priority | Features | Progress |
|----|-------|--------|----------|----------|----------|
| [EPIC-001](./work/EPIC-001-oss-release/EPIC-001-oss-release.md) | OSS Release Preparation | done | high | 1 | 100% |

---

## Enablers

| ID | Title | Status | Priority | Parent | Children |
|----|-------|--------|----------|--------|----------|
| [EN-001](./work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/EN-001-fix-plugin-validation/EN-001-fix-plugin-validation.md) | Fix Plugin Validation | done | high | FEAT-001 | BUG-001, TASK-001, TASK-002, TASK-003, DEC-001 |
| [EN-002](./work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/EN-002-fix-test-infrastructure/EN-002-fix-test-infrastructure.md) | Fix Test Infrastructure | done | medium | FEAT-001 | BUG-004 (TASK-001), BUG-005 (TASK-001, TASK-002) |
| [EN-003](./work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/EN-003-fix-validation-test-regressions/EN-003-fix-validation-test-regressions.md) | Fix Validation Test Regressions | done | high | FEAT-001 | BUG-006, TASK-001, TASK-002 |

---

## Bugs

| ID | Title | Status | Priority | Severity | Parent |
|----|-------|--------|----------|----------|--------|
| [BUG-001](./work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/EN-001-fix-plugin-validation/BUG-001-marketplace-manifest-schema-error.md) | Marketplace manifest schema error: `keywords` not allowed | done | high | major | EN-001 |
| [BUG-004](./work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/EN-002-fix-test-infrastructure/BUG-004-transcript-pipeline-no-datasets.md) | Transcript pipeline test finds no datasets | done | medium | major | EN-002 |
| [BUG-005](./work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/EN-002-fix-test-infrastructure/BUG-005-project-validation-missing-artifacts.md) | Project validation tests reference non-existent PROJ-001-plugin-cleanup | done | medium | major | EN-002 |
| [BUG-006](./work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/EN-003-fix-validation-test-regressions/BUG-006-validation-test-ci-regressions.md) | Validation test CI regressions (lint + pip compatibility) | done | high | major | EN-003 |
| [BUG-007](./work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/FEAT-001--BUG-007-synthesis-content-test-overly-prescriptive.md) | Synthesis content validation test overly prescriptive | done | high | major | FEAT-001 |

---

## Completed

| ID | Title | Completed | Resolution |
|----|-------|-----------|------------|
| [BUG-001](./work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/EN-001-fix-plugin-validation/BUG-001-marketplace-manifest-schema-error.md) | Marketplace manifest schema error: `keywords` not allowed | 2026-02-11 | Added keywords to marketplace schema, validation tests, Draft202012Validator |
| [BUG-002](./work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/FEAT-001--BUG-002-cli-projects-list-crash.md) | CLI `projects list` crashes with unhandled exception | 2026-02-10 | Resolved by committing `projects/` directory to git |
| [BUG-003](./work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/FEAT-001--BUG-003-bootstrap-test-missing-projects-dir.md) | Bootstrap test assumes `projects/` directory exists | 2026-02-10 | Resolved by committing `projects/` directory to git |
| [BUG-004](./work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/EN-002-fix-test-infrastructure/BUG-004-transcript-pipeline-no-datasets.md) | Transcript pipeline test finds no datasets | 2026-02-11 | Added 33 missing test data files |
| [BUG-005](./work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/EN-002-fix-test-infrastructure/BUG-005-project-validation-missing-artifacts.md) | Project validation tests reference non-existent PROJ-001-plugin-cleanup | 2026-02-11 | Dynamic project discovery + category directories + orchestration valid_category |
| [BUG-006](./work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/EN-003-fix-validation-test-regressions/BUG-006-validation-test-ci-regressions.md) | Validation test CI regressions (lint + pip) | 2026-02-11 | Removed f-prefix, added uv skipif |
| [BUG-007](./work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/FEAT-001--BUG-007-synthesis-content-test-overly-prescriptive.md) | Synthesis content validation test overly prescriptive | 2026-02-11 | Raised content check threshold to >= 3 files |
