# PROJ-001: OSS Release - Work Tracker

> Global Manifest for PROJ-001. Tracks Epics, Bugs, Decisions, Discoveries, and Impediments.
> Features, Enablers, and Tasks are tracked in their respective entity files.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Project overview and status |
| [Epics](#epics) | Strategic work items (pointers) |
| [Bugs](#bugs) | All project bugs |
| [Decisions](#decisions) | Key decisions and their rationale |
| [Discoveries](#discoveries) | Documented findings during work |
| [Completed](#completed) | Resolved items ledger |
| [History](#history) | Change log |

---

## Summary

| Field | Value |
|-------|-------|
| Project | PROJ-001-oss-release |
| Status | IN_PROGRESS |
| Created | 2026-02-10 |

---

## Epics

| ID | Title | Status | Priority |
|----|-------|--------|----------|
| [EPIC-001](./work/EPIC-001-oss-release/EPIC-001-oss-release.md) | OSS Release Preparation | in_progress | high |

> Features, Enablers, and Tasks are tracked within the Epic and its children.

---

## Bugs

| ID | Title | Status | Priority | Parent |
|----|-------|--------|----------|--------|
| [BUG-001](./work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/EN-001-fix-plugin-validation/BUG-001-marketplace-manifest-schema-error.md) | Marketplace manifest schema error | done | high | EN-001 |
| [BUG-004](./work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/EN-002-fix-test-infrastructure/BUG-004-transcript-pipeline-no-datasets.md) | Transcript pipeline test finds no datasets | done | medium | EN-002 |
| [BUG-005](./work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/EN-002-fix-test-infrastructure/BUG-005-project-validation-missing-artifacts.md) | Project validation tests reference non-existent project | done | medium | EN-002 |
| [BUG-006](./work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/EN-003-fix-validation-test-regressions/BUG-006-validation-test-ci-regressions.md) | Validation test CI regressions | done | high | EN-003 |
| [BUG-007](./work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/FEAT-001--BUG-007-synthesis-content-test-overly-prescriptive.md) | Synthesis content test overly prescriptive | done | high | FEAT-001 |
| [BUG-010](./work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/EN-004-fix-precommit-hook-coverage/BUG-010-session-hook-no-auto-install.md) | Session hook warning doesn't reference `make setup` | done | low | EN-004 |
| [BUG-011](./work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/EN-004-fix-precommit-hook-coverage/BUG-011-precommit-pytest-python-only.md) | Pre-commit pytest hook Python-only trigger | done | high | EN-004 |
| [BUG-001](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-202-claude-md-rewrite/BUG-001-relationships-typo.md) | Relationships typo | pending | low | EN-202 |
| [BUG-002](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-202-claude-md-rewrite/BUG-002-story-folder-id-mismatch.md) | Story folder ID mismatch | pending | low | EN-202 |
| [BUG-003](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-202-claude-md-rewrite/BUG-003-template-path-inconsistency.md) | Template path inconsistency | pending | medium | EN-202 |
| [BUG-004](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-202-claude-md-rewrite/BUG-004-todo-section-not-migrated.md) | TODO section not migrated | pending | medium | EN-202 |
| [BUG-005](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-202-claude-md-rewrite/BUG-005-mandatory-skill-usage-lost.md) | Mandatory skill usage lost | pending | high | EN-202 |
| [BUG-006](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-202-claude-md-rewrite/BUG-006-working-with-jerry-lost.md) | Working with Jerry section lost | pending | high | EN-202 |
| [BUG-007](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-202-claude-md-rewrite/BUG-007-problem-solving-templates-lost.md) | Problem solving templates lost | pending | medium | EN-202 |
| [BUG-008](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-202-claude-md-rewrite/BUG-008-askuserquestion-flow-lost.md) | AskUserQuestion flow lost | pending | medium | EN-202 |

---

## Decisions

| ID | Title | Status | Impact | Path |
|----|-------|--------|--------|------|
| [DEC-001](./work/EPIC-001-oss-release/FEAT-002-research-and-preparation/FEAT-002--DEC-001-transcript-decisions.md) | Transcript Decisions (MIT License, Dual Repo, Orchestration, Decomposition) | accepted | strategic | FEAT-002 |
| [DEC-002](./work/EPIC-001-oss-release/FEAT-002-research-and-preparation/FEAT-002--DEC-002-orchestration-execution-decisions.md) | Orchestration Execution Decisions (Tiered, QG>=0.92, Checkpoints, Auto-retry) | accepted | tactical | FEAT-002 |
| [DEC-003](./work/EPIC-001-oss-release/FEAT-002-research-and-preparation/FEAT-002--DEC-003-phase-2-execution-strategy.md) | Phase 2 Execution Strategy (Enabler ID Block Numbering) | accepted | tactical | FEAT-002 |
| [DEC-001](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/FEAT-003--DEC-001-navigation-table-standard.md) | Navigation Table Standard | accepted | tactical | FEAT-003 |
| [DEC-001](./work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/EN-004-fix-precommit-hook-coverage/DEC-001-precommit-installation-strategy.md) | Pre-commit Installation Strategy | accepted | tactical | EN-004 |
| [DEC-002](./work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/EN-004-fix-precommit-hook-coverage/DEC-002-pytest-hook-file-type-coverage.md) | Pytest Hook File Type Coverage | accepted | tactical | EN-004 |

> Decision details (individual D-001, D-002, etc.) live in the respective decision files.

---

## Discoveries

| ID | Title | Status | Impact | Path |
|----|-------|--------|--------|------|
| [DISC-001](./work/EPIC-001-oss-release/FEAT-002-research-and-preparation/FEAT-002--DISC-001-missed-research-scope.md) | Missed Research Scope - Claude Code Best Practices | validated | critical | FEAT-002 |
| [DISC-001](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/FEAT-003--DISC-001-navigation-tables-for-llm-comprehension.md) | Navigation Tables for LLM Comprehension | validated | high | FEAT-003 |

---

## Completed

| ID | Title | Completed | Resolution |
|----|-------|-----------|------------|
| BUG-001 (EN-001) | Marketplace manifest schema error | 2026-02-11 | Added keywords to marketplace schema, validation tests, Draft202012Validator |
| BUG-002 (EN-001) | CLI `projects list` crashes | 2026-02-10 | Resolved by committing `projects/` directory to git |
| BUG-003 (EN-001) | Bootstrap test assumes `projects/` dir | 2026-02-10 | Resolved by committing `projects/` directory to git |
| BUG-004 (EN-002) | Transcript pipeline test finds no datasets | 2026-02-11 | Added 33 missing test data files |
| BUG-005 (EN-002) | Project validation tests reference non-existent project | 2026-02-11 | Dynamic project discovery + category directories |
| BUG-006 (EN-003) | Validation test CI regressions | 2026-02-11 | Removed f-prefix, added uv skipif |
| BUG-007 (FEAT-001) | Synthesis content test overly prescriptive | 2026-02-11 | Raised content check threshold to >= 3 files |
| BUG-010 (EN-004) | Session hook warning improved | 2026-02-11 | DEC-001: auto-install rejected, warning text updated |
| BUG-011 (EN-004) | Pre-commit pytest hook Python-only trigger | 2026-02-11 | `types_or: [python, markdown]` applied per DEC-002 |
| FEAT-001 | Fix CI Build Failures | 2026-02-11 | All 9 bugs resolved, 4 enablers done, PR #6 merged, CI green |

---

## History

| Date | Author | Event |
|------|--------|-------|
| 2026-02-10 | Claude | Project created. EPIC-001, FEAT-001 with 5 bugs from PR #6 CI failures |
| 2026-02-10 | Claude | BUG-002, BUG-003 resolved |
| 2026-02-11 | Claude | EN-001 completed (BUG-001 + 3 tasks). EN-003 created and completed (BUG-006) |
| 2026-02-11 | Claude | EN-002 completed (BUG-004 + BUG-005). FEAT-001 100% |
| 2026-02-11 | Claude | BUG-007 filed and resolved |
| 2026-02-11 | Claude | PII sanitization across transcript files |
| 2026-02-11 | Claude | Git history sanitized: removed PII from commit messages and blobs |
| 2026-02-11 | Claude | PR #6 merged to main. FEAT-002 and FEAT-003 created under EPIC-001 |
| 2026-02-11 | Claude | FEAT-001 reopened: EN-004 created (BUG-010, BUG-011). Both resolved. FEAT-001 closed |
| 2026-02-12 | Claude | EN-108 created under FEAT-002: Version Bumping Strategy (6 tasks) |
| 2026-02-12 | Claude | WORKTRACKER.md restructured: slim pointer per behavior rules (line 121) |

---

*Last Updated: 2026-02-12*
