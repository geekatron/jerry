# PROJ-001: OSS Release - Work Tracker

> Work tracking for preparing Jerry for open-source release.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Project overview and status |
| [Epics](#epics) | Strategic work items |
| [Features](#features) | Feature breakdown under EPIC-001 |
| [Enablers (FEAT-001)](#enablers-feat-001) | CI fix enablers (done) |
| [Enablers (FEAT-002)](#enablers-feat-002) | Research phase enablers |
| [Enablers (FEAT-003)](#enablers-feat-003) | CLAUDE.md optimization enablers |
| [Tasks (FEAT-002)](#tasks-feat-002) | Research phase tasks |
| [Tasks (FEAT-003)](#tasks-feat-003---by-enabler) | Implementation phase tasks by enabler |
| [Discoveries](#discoveries) | Documented findings during work |
| [Decisions](#decisions) | Key decisions and their rationale |
| [Bugs (FEAT-001)](#bugs-feat-001) | CI build defects (all resolved) |
| [Bugs (FEAT-003)](#bugs-feat-003) | CLAUDE.md optimization defects |
| [Orchestration](#orchestration) | Workflow coordination artifacts |
| [Completed](#completed) | Finished items |
| [Progress Summary](#progress-summary) | Overall project completion status |
| [History](#history) | Change log |

---

## Summary

| Field | Value |
|-------|-------|
| Project | PROJ-001-oss-release |
| Status | IN_PROGRESS |
| Created | 2026-02-10 |
| PR (FEAT-001) | [#6](https://github.com/geekatron/jerry/pull/6) (merged) |

---

## Epics

| ID | Title | Status | Priority | Features | Progress |
|----|-------|--------|----------|----------|----------|
| [EPIC-001](./work/EPIC-001-oss-release/EPIC-001-oss-release.md) | OSS Release Preparation | in_progress | high | 3 | 45% |

---

## Features

| ID | Title | Status | Parent | Progress |
|----|-------|--------|--------|----------|
| [FEAT-001](./work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/FEAT-001-fix-ci-build-failures.md) | Fix CI Build Failures | done | EPIC-001 | 100% |
| [FEAT-002](./work/EPIC-001-oss-release/FEAT-002-research-and-preparation/FEAT-002-research-and-preparation.md) | Research and Preparation | in_progress | EPIC-001 | 10% |
| [FEAT-003](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/FEAT-003-claude-md-optimization.md) | CLAUDE.md Optimization | pending | EPIC-001 | 0% |

---

## Enablers (FEAT-001)

> All FEAT-001 enablers are **done**. 9/9 bugs resolved, 4/4 enablers complete.

| ID | Title | Status | Priority | Parent | Children |
|----|-------|--------|----------|--------|----------|
| [EN-001](./work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/EN-001-fix-plugin-validation/EN-001-fix-plugin-validation.md) | Fix Plugin Validation | done | high | FEAT-001 | BUG-001, TASK-001, TASK-002, TASK-003, DEC-001 |
| [EN-002](./work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/EN-002-fix-test-infrastructure/EN-002-fix-test-infrastructure.md) | Fix Test Infrastructure | done | medium | FEAT-001 | BUG-004 (TASK-001), BUG-005 (TASK-001, TASK-002) |
| [EN-003](./work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/EN-003-fix-validation-test-regressions/EN-003-fix-validation-test-regressions.md) | Fix Validation Test Regressions | done | high | FEAT-001 | BUG-006, TASK-001, TASK-002 |
| [EN-004](./work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/EN-004-fix-precommit-hook-coverage/EN-004-fix-precommit-hook-coverage.md) | Fix Pre-commit Hook Coverage | done | high | FEAT-001 | BUG-010 (done), BUG-011 (done), DEC-001, DEC-002 |

---

## Enablers (FEAT-002)

> Research phase enablers (1xx block).

| ID | Title | Status | Priority | Parent | Progress |
|----|-------|--------|----------|--------|----------|
| [EN-101](./work/EPIC-001-oss-release/FEAT-002-research-and-preparation/EN-101-oss-best-practices-research/EN-101-oss-best-practices-research.md) | OSS Release Best Practices Research | partial | high | FEAT-002 | 100% |
| [EN-102](./work/EPIC-001-oss-release/FEAT-002-research-and-preparation/EN-102-claude-code-best-practices/EN-102-claude-code-best-practices.md) | Claude Code Best Practices Research | pending | high | FEAT-002 | 0% |
| [EN-103](./work/EPIC-001-oss-release/FEAT-002-research-and-preparation/EN-103-claude-md-optimization/EN-103-claude-md-optimization.md) | CLAUDE.md Optimization Research | pending | high | FEAT-002 | 0% |
| [EN-104](./work/EPIC-001-oss-release/FEAT-002-research-and-preparation/EN-104-plugins-research/EN-104-plugins-research.md) | Claude Code Plugins Research | pending | medium | FEAT-002 | 0% |
| [EN-105](./work/EPIC-001-oss-release/FEAT-002-research-and-preparation/EN-105-skills-research/EN-105-skills-research.md) | Claude Code Skills Research | pending | medium | FEAT-002 | 0% |
| [EN-106](./work/EPIC-001-oss-release/FEAT-002-research-and-preparation/EN-106-decomposition-research/EN-106-decomposition-research.md) | Decomposition with Imports Research | pending | medium | FEAT-002 | 0% |
| [EN-107](./work/EPIC-001-oss-release/FEAT-002-research-and-preparation/EN-107-current-state-analysis/EN-107-current-state-analysis.md) | Current State Analysis | complete | high | FEAT-002 | 100% |

---

## Enablers (FEAT-003)

> CLAUDE.md optimization enablers (2xx block).

| ID | Title | Status | Priority | Parent | Progress | Tasks |
|----|-------|--------|----------|--------|----------|-------|
| [EN-201](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-201-worktracker-skill-extraction/EN-201-worktracker-skill-extraction.md) | Worktracker Skill Extraction | pending | high | FEAT-003 | 0% | 7 |
| [EN-202](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-202-claude-md-rewrite/EN-202-claude-md-rewrite.md) | CLAUDE.md Rewrite | pending | high | FEAT-003 | 0% | 7 |
| [EN-203](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-203-todo-section-migration/EN-203-todo-section-migration.md) | TODO Section Migration | pending | medium | FEAT-003 | 0% | 4 |
| [EN-204](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-204-validation-testing/EN-204-validation-testing.md) | Validation & Testing | pending | medium | FEAT-003 | 0% | 6 |
| [EN-205](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-205-documentation-update/EN-205-documentation-update.md) | Documentation Update | pending | medium | FEAT-003 | 0% | 4 |
| [EN-206](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-206-context-distribution-strategy/EN-206-context-distribution-strategy.md) | Context Distribution Strategy | pending | high | FEAT-003 | 0% | 6 |
| [EN-207](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-207-worktracker-agent-implementation/EN-207-worktracker-agent-implementation.md) | Worktracker Agent Implementation | pending | high | FEAT-003 | 0% | 10 |

**FEAT-003 Enabler Summary:** 7 Enablers, 44 Tasks

---

## Tasks (FEAT-002)

| ID | Title | Status | Parent | Effort |
|----|-------|--------|--------|--------|
| [TASK-001](./work/EPIC-001-oss-release/FEAT-002-research-and-preparation/TASK-001-orchestration-plan-design.md) | Orchestration Plan Design | complete | FEAT-002 | 8 |
| TASK-002 | Move artifacts to correct location | complete | FEAT-002 | 2 |
| TASK-003 | Create worktracker documents | complete | FEAT-002 | 4 |
| TASK-004 | Execute expanded research agents | pending | FEAT-002 | 8 |

### Tasks per Enabler (FEAT-002)

**EN-101: OSS Best Practices Research** (3 tasks)

| ID | Title | Status | Effort |
|----|-------|--------|--------|
| TASK-001 | License research | complete | 2 |
| TASK-002 | Essential files research | complete | 2 |
| TASK-003 | Security practices research | complete | 2 |

**EN-102: Claude Code Best Practices** (3 tasks)

| ID | Title | Status | Effort |
|----|-------|--------|--------|
| TASK-001 | Hook system research | pending | 2 |
| TASK-002 | Session management research | pending | 2 |
| TASK-003 | CLI patterns research | pending | 2 |

**EN-103: CLAUDE.md Optimization Research** (3 tasks)

| ID | Title | Status | Effort |
|----|-------|--------|--------|
| TASK-001 | Context loading research | pending | 2 |
| TASK-002 | Decomposition strategies | pending | 2 |
| TASK-003 | Token optimization | pending | 2 |

**EN-104: Plugins Research** (3 tasks)

| ID | Title | Status | Effort |
|----|-------|--------|--------|
| TASK-001 | Manifest research | pending | 2 |
| TASK-002 | Discovery mechanisms | pending | 2 |
| TASK-003 | Distribution patterns | pending | 2 |

**EN-105: Skills Research** (3 tasks)

| ID | Title | Status | Effort |
|----|-------|--------|--------|
| TASK-001 | Skill structure research | pending | 2 |
| TASK-002 | Agent patterns research | pending | 2 |
| TASK-003 | Invocation mechanisms | pending | 2 |

**EN-106: Decomposition Research** (3 tasks)

| ID | Title | Status | Effort |
|----|-------|--------|--------|
| TASK-001 | Import syntax research | pending | 2 |
| TASK-002 | Loading strategies | pending | 2 |
| TASK-003 | Tiered architecture | pending | 2 |

**EN-107: Current State Analysis** (4 tasks)

| ID | Title | Status | Effort |
|----|-------|--------|--------|
| TASK-001 | Codebase analysis | complete | 3 |
| TASK-002 | CLAUDE.md inventory | complete | 2 |
| TASK-003 | Skills inventory | complete | 2 |
| TASK-004 | Documentation gaps | complete | 2 |

---

## Tasks (FEAT-003 - by Enabler)

**EN-201: Worktracker Skill Extraction** (8 pts)

| ID | Title | Status | Effort |
|----|-------|--------|--------|
| [TASK-001](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-201-worktracker-skill-extraction/TASK-001-fix-skill-md-description.md) | Fix SKILL.md description bug | pending | 1 |
| [TASK-002](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-201-worktracker-skill-extraction/TASK-002-create-entity-hierarchy-rules.md) | Create worktracker-entity-hierarchy.md | pending | 1 |
| [TASK-003](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-201-worktracker-skill-extraction/TASK-003-create-system-mappings-rules.md) | Create worktracker-system-mappings.md | pending | 2 |
| [TASK-004](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-201-worktracker-skill-extraction/TASK-004-create-behavior-rules.md) | Create worktracker-behavior-rules.md | pending | 1 |
| [TASK-005](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-201-worktracker-skill-extraction/TASK-005-create-directory-structure-rules.md) | Create worktracker-directory-structure.md | pending | 1 |
| [TASK-006](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-201-worktracker-skill-extraction/TASK-006-update-skill-navigation.md) | Update SKILL.md with navigation pointers | pending | 1 |
| [TASK-007](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-201-worktracker-skill-extraction/TASK-007-validate-skill-loading.md) | Validate skill loads correctly | pending | 1 |

**EN-202: CLAUDE.md Rewrite** (8 pts)

| ID | Title | Status | Effort |
|----|-------|--------|--------|
| [TASK-001](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-202-claude-md-rewrite/TASK-001-create-identity-section.md) | Create Identity section | pending | 1 |
| [TASK-002](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-202-claude-md-rewrite/TASK-002-create-navigation-section.md) | Create Navigation pointers section | pending | 2 |
| [TASK-003](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-202-claude-md-rewrite/TASK-003-create-active-project-section.md) | Create Active project section | pending | 1 |
| [TASK-004](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-202-claude-md-rewrite/TASK-004-create-critical-constraints-section.md) | Create Critical constraints section | pending | 1 |
| [TASK-005](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-202-claude-md-rewrite/TASK-005-create-quick-reference-section.md) | Create Quick reference section | pending | 1 |
| [TASK-006](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-202-claude-md-rewrite/TASK-006-validate-pointers.md) | Validate all pointers resolve correctly | pending | 1 |
| [TASK-007](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-202-claude-md-rewrite/TASK-007-verify-line-count.md) | Verify line count target (60-80 lines) | pending | 1 |

**EN-203: TODO Section Migration** (3 pts)

| ID | Title | Status | Effort |
|----|-------|--------|--------|
| [TASK-001](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-203-todo-section-migration/TASK-001-create-todo-integration-rules.md) | Create todo-integration.md rule file | pending | 1 |
| [TASK-002](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-203-todo-section-migration/TASK-002-move-meta-todo-requirements.md) | Move META TODO requirements | pending | 1 |
| [TASK-003](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-203-todo-section-migration/TASK-003-add-brief-todo-mention.md) | Add brief TODO mention in CLAUDE.md | pending | 0.5 |
| [TASK-004](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-203-todo-section-migration/TASK-004-update-skill-todo-loading.md) | Update skill to load TODO rules | pending | 0.5 |

**EN-204: Validation & Testing** (5 pts)

| ID | Title | Status | Effort |
|----|-------|--------|--------|
| [TASK-001](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-204-validation-testing/TASK-001-fresh-session-baseline.md) | Start fresh Claude Code session for baseline | pending | 0.5 |
| [TASK-002](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-204-validation-testing/TASK-002-verify-token-count.md) | Verify context token count at session start | pending | 1 |
| [TASK-003](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-204-validation-testing/TASK-003-test-worktracker-skill.md) | Test /worktracker skill invocation | pending | 1 |
| [TASK-004](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-204-validation-testing/TASK-004-test-navigation-pointers.md) | Test navigation pointers resolve | pending | 1 |
| [TASK-005](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-204-validation-testing/TASK-005-test-typical-workflows.md) | Test typical workflows | pending | 1 |
| [TASK-006](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-204-validation-testing/TASK-006-document-issues.md) | Document issues found | pending | 0.5 |

**EN-205: Documentation Update** (3 pts)

| ID | Title | Status | Effort |
|----|-------|--------|--------|
| [TASK-001](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-205-documentation-update/TASK-001-update-installation-md.md) | Update INSTALLATION.md | pending | 1 |
| [TASK-002](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-205-documentation-update/TASK-002-create-claude-md-guide.md) | Create CLAUDE-MD-GUIDE.md | pending | 1 |
| [TASK-003](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-205-documentation-update/TASK-003-update-adrs.md) | Update relevant ADRs | pending | 0.5 |
| [TASK-004](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-205-documentation-update/TASK-004-add-context-optimization-rationale.md) | Add context optimization rationale | pending | 0.5 |

**EN-206: Context Distribution Strategy** (6 tasks)

| ID | Title | Status | Effort |
|----|-------|--------|--------|
| [TASK-001](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-206-context-distribution-strategy/TASK-001-restructure-to-context.md) | Restructure to .context/ | pending | 3 |
| [TASK-002](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-206-context-distribution-strategy/TASK-002-implement-sync-mechanism.md) | Implement sync mechanism | pending | 3 |
| [TASK-003](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-206-context-distribution-strategy/TASK-003-create-bootstrap-skill.md) | Create bootstrap skill | pending | 2 |
| [TASK-004](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-206-context-distribution-strategy/TASK-004-user-documentation.md) | User documentation | pending | 1 |
| [TASK-005](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-206-context-distribution-strategy/TASK-005-integration-testing.md) | Integration testing | pending | 2 |
| [TASK-006](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-206-context-distribution-strategy/TASK-006-rollback-documentation.md) | Rollback documentation | pending | 1 |

**EN-207: Worktracker Agent Implementation** (10 tasks)

| ID | Title | Status | Effort |
|----|-------|--------|--------|
| [TASK-001](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-207-worktracker-agent-implementation/TASK-001-create-wt-agent-template.md) | Create wt-agent template | pending | 1 |
| [TASK-002](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-207-worktracker-agent-implementation/TASK-002-create-wti-rules.md) | Create WTI rules | pending | 2 |
| [TASK-003](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-207-worktracker-agent-implementation/TASK-003-create-verification-report-template.md) | Create verification report template | pending | 1 |
| [TASK-004](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-207-worktracker-agent-implementation/TASK-004-create-audit-report-template.md) | Create audit report template | pending | 1 |
| [TASK-005](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-207-worktracker-agent-implementation/TASK-005-implement-wt-verifier.md) | Implement wt-verifier | pending | 3 |
| [TASK-006](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-207-worktracker-agent-implementation/TASK-006-implement-wt-visualizer.md) | Implement wt-visualizer | pending | 2 |
| [TASK-007](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-207-worktracker-agent-implementation/TASK-007-implement-wt-auditor.md) | Implement wt-auditor | pending | 3 |
| [TASK-008](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-207-worktracker-agent-implementation/TASK-008-update-skill-md.md) | Update SKILL.md | pending | 1 |
| [TASK-009](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-207-worktracker-agent-implementation/TASK-009-adversarial-review.md) | Adversarial review | pending | 2 |
| [TASK-010](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-207-worktracker-agent-implementation/TASK-010-integration-testing.md) | Integration testing | pending | 2 |

---

## Discoveries

| ID | Title | Status | Impact | Path |
|----|-------|--------|--------|------|
| [DISC-001](./work/EPIC-001-oss-release/FEAT-002-research-and-preparation/FEAT-002--DISC-001-missed-research-scope.md) | Missed Research Scope - Claude Code Best Practices | validated | critical | FEAT-002 |
| [DISC-001](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/FEAT-003--DISC-001-navigation-tables-for-llm-comprehension.md) | Navigation Tables for LLM Comprehension | validated | high | FEAT-003 |

---

## Decisions

| ID | Title | Status | Impact | Path |
|----|-------|--------|--------|------|
| [DEC-001](./work/EPIC-001-oss-release/FEAT-002-research-and-preparation/FEAT-002--DEC-001-transcript-decisions.md) | Transcript Decisions (MIT License, Dual Repo, Orchestration, Decomposition) | accepted | strategic | FEAT-002 |
| [DEC-002](./work/EPIC-001-oss-release/FEAT-002-research-and-preparation/FEAT-002--DEC-002-orchestration-execution-decisions.md) | Orchestration Execution Decisions (Tiered, QG>=0.92, Checkpoints, Auto-retry) | accepted | tactical | FEAT-002 |
| [DEC-003](./work/EPIC-001-oss-release/FEAT-002-research-and-preparation/FEAT-002--DEC-003-phase-2-execution-strategy.md) | Phase 2 Execution Strategy (Enabler ID Block Numbering) | accepted | tactical | FEAT-002 |
| [DEC-001](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/FEAT-003--DEC-001-navigation-table-standard.md) | Navigation Table Standard | accepted | tactical | FEAT-003 |
| [DEC-001](./work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/EN-004-fix-precommit-hook-coverage/DEC-001-precommit-installation-strategy.md) | Pre-commit Installation Strategy (make setup exists, improve warning) | accepted | tactical | EN-004 |
| [DEC-002](./work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/EN-004-fix-precommit-hook-coverage/DEC-002-pytest-hook-file-type-coverage.md) | Pytest Hook File Type Coverage (types_or: python, markdown) | accepted | tactical | EN-004 |

### Decision Summary

| Code | Decision | Source |
|------|----------|--------|
| FEAT-002:DEC-001:D-001 | MIT License for OSS release | Transcript |
| FEAT-002:DEC-001:D-002 | Orchestration approach for workflow coordination | Transcript |
| FEAT-002:DEC-001:D-003 | Dual repository strategy (internal / jerry) | Transcript |
| FEAT-002:DEC-001:D-004 | Decomposition with imports for CLAUDE.md optimization | Transcript |
| FEAT-002:DEC-002:D-001 | Tiered execution within phases | Conversation |
| FEAT-002:DEC-002:D-002 | Quality gate threshold >=0.92 | Conversation |
| FEAT-002:DEC-002:D-003 | User checkpoints after each gate | Conversation |
| FEAT-002:DEC-002:D-004 | Auto-retry 2x before user escalation | Conversation |
| FEAT-002:DEC-003:D-001 | Enabler IDs use Feature-scoped blocks (FEAT-002 = 1xx, FEAT-003 = 2xx) | Conversation |
| FEAT-003:DEC-001 | Navigation tables with anchor links for LLM comprehension | Research |
| EN-004:DEC-001:D-001 | Close BUG-010: `make setup` already exists for pre-commit installation | Research (ps-investigator) |
| EN-004:DEC-001:D-002 | Improve session hook warning to reference `make setup` | Research (ps-investigator) |
| EN-004:DEC-002:D-001 | Use `types_or: [python, markdown]` on pytest hook | Research (ps-researcher) |

---

## Bugs (FEAT-001)

> FEAT-001 bugs: All 9 resolved.

| ID | Title | Status | Priority | Severity | Parent |
|----|-------|--------|----------|----------|--------|
| [BUG-001](./work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/EN-001-fix-plugin-validation/BUG-001-marketplace-manifest-schema-error.md) | Marketplace manifest schema error: `keywords` not allowed | done | high | major | EN-001 |
| [BUG-004](./work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/EN-002-fix-test-infrastructure/BUG-004-transcript-pipeline-no-datasets.md) | Transcript pipeline test finds no datasets | done | medium | major | EN-002 |
| [BUG-005](./work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/EN-002-fix-test-infrastructure/BUG-005-project-validation-missing-artifacts.md) | Project validation tests reference non-existent PROJ-001-plugin-cleanup | done | medium | major | EN-002 |
| [BUG-006](./work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/EN-003-fix-validation-test-regressions/BUG-006-validation-test-ci-regressions.md) | Validation test CI regressions (lint + pip compatibility) | done | high | major | EN-003 |
| [BUG-007](./work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/FEAT-001--BUG-007-synthesis-content-test-overly-prescriptive.md) | Synthesis content validation test overly prescriptive | done | high | major | FEAT-001 |
| [BUG-010](./work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/EN-004-fix-precommit-hook-coverage/BUG-010-session-hook-no-auto-install.md) | ~~Session hook no auto-install~~ Warning doesn't reference `make setup` | done | low | minor | EN-004 |
| [BUG-011](./work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/EN-004-fix-precommit-hook-coverage/BUG-011-precommit-pytest-python-only.md) | Pre-commit pytest hook only triggers on Python file changes | done | high | major | EN-004 |

## Bugs (FEAT-003)

> Bugs from CLAUDE.md optimization work.

| ID | Title | Status | Priority | Parent |
|----|-------|--------|----------|--------|
| [BUG-001](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-202-claude-md-rewrite/BUG-001-relationships-typo.md) | Relationships typo | pending | low | EN-202 |
| [BUG-002](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-202-claude-md-rewrite/BUG-002-story-folder-id-mismatch.md) | Story folder ID mismatch | pending | low | EN-202 |
| [BUG-003](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-202-claude-md-rewrite/BUG-003-template-path-inconsistency.md) | Template path inconsistency | pending | medium | EN-202 |
| [BUG-004](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-202-claude-md-rewrite/BUG-004-todo-section-not-migrated.md) | TODO section not migrated | pending | medium | EN-202 |
| [BUG-005](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-202-claude-md-rewrite/BUG-005-mandatory-skill-usage-lost.md) | Mandatory skill usage lost | pending | high | EN-202 |
| [BUG-006](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-202-claude-md-rewrite/BUG-006-working-with-jerry-lost.md) | Working with Jerry section lost | pending | high | EN-202 |
| [BUG-007](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-202-claude-md-rewrite/BUG-007-problem-solving-templates-lost.md) | Problem solving templates lost | pending | medium | EN-202 |
| [BUG-008](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-202-claude-md-rewrite/BUG-008-askuserquestion-flow-lost.md) | AskUserQuestion flow lost | pending | medium | EN-202 |

---

## Orchestration

### FEAT-002 Research Orchestration

**Workflow ID:** oss-release-20260131-001
**Orchestration Path:** [./work/EPIC-001-oss-release/FEAT-002-research-and-preparation/orchestration/](./work/EPIC-001-oss-release/FEAT-002-research-and-preparation/orchestration/)

| Artifact | Path |
|----------|------|
| Plan | [ORCHESTRATION_PLAN.md](./work/EPIC-001-oss-release/FEAT-002-research-and-preparation/orchestration/ORCHESTRATION_PLAN.md) |
| State | [ORCHESTRATION.yaml](./work/EPIC-001-oss-release/FEAT-002-research-and-preparation/orchestration/ORCHESTRATION.yaml) |
| Worktracker | [ORCHESTRATION_WORKTRACKER.md](./work/EPIC-001-oss-release/FEAT-002-research-and-preparation/orchestration/ORCHESTRATION_WORKTRACKER.md) |
| Diagram | [ORCHESTRATION_DIAGRAM_ASCII.md](./work/EPIC-001-oss-release/FEAT-002-research-and-preparation/orchestration/ORCHESTRATION_DIAGRAM_ASCII.md) |

**Phase Status:**

| Phase | Status | Agents | QG Score |
|-------|--------|--------|----------|
| Phase 0: Research | in_progress (requires expansion) | 4/9 complete | QG-0 FAILED (0.876) |
| Phase 1: Requirements | blocked | 0/4 | - |
| Phase 2: Architecture | blocked | 0/4 | - |
| Phase 3: Implementation | blocked | 0/4 | - |
| Phase 4: Validation | blocked | 0/3 | - |

---

## Completed

| ID | Title | Completed | Resolution |
|----|-------|-----------|------------|
| BUG-001 (FEAT-001) | Marketplace manifest schema error | 2026-02-11 | Added keywords to marketplace schema, validation tests, Draft202012Validator |
| BUG-002 (FEAT-001) | CLI `projects list` crashes | 2026-02-10 | Resolved by committing `projects/` directory to git |
| BUG-003 (FEAT-001) | Bootstrap test assumes `projects/` dir | 2026-02-10 | Resolved by committing `projects/` directory to git |
| BUG-004 (FEAT-001) | Transcript pipeline test finds no datasets | 2026-02-11 | Restored 33 test data files from prior repository migration |
| BUG-005 (FEAT-001) | Project validation tests reference non-existent project | 2026-02-11 | Dynamic project discovery + category directories |
| BUG-006 (FEAT-001) | Validation test CI regressions | 2026-02-11 | Removed f-prefix, added uv skipif |
| BUG-007 (FEAT-001) | Synthesis content test overly prescriptive | 2026-02-11 | Raised content check threshold to >= 3 files |
| BUG-010 (FEAT-001) | Session hook warning improved to reference `make setup` | 2026-02-11 | DEC-001: auto-install rejected, warning text updated |
| BUG-011 (FEAT-001) | Pre-commit pytest hook Python-only trigger | 2026-02-11 | `types_or: [python, markdown]` applied per DEC-002 |
| FEAT-001 | Fix CI Build Failures | 2026-02-11 | All 9 bugs resolved, 4 enablers done, PR #6 merged, CI green |

---

## Progress Summary

```
+------------------------------------------------------------------+
|                   PROJECT PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Epics:     [#########...........] 45% (0/1 completed)            |
| Features:  [#######.............] 33% (1/3 completed)            |
| Enablers:  [########............] 39% (7/18 complete/partial)    |
| Tasks:     [#####...............] 18% (12/~75 completed)         |
| Decisions: [####################] 100% (6/6 documented)          |
| Discovery: [####################] 100% (2/2 documented)          |
+------------------------------------------------------------------+
| Overall:   [########............] 38%                             |
+------------------------------------------------------------------+
```

### FEAT-003 Breakdown

```
+------------------------------------------------------------------+
|              FEAT-003: CLAUDE.md Optimization                     |
+------------------------------------------------------------------+
| EN-201:    [....................] 0% (0/7 tasks)                 |
| EN-202:    [....................] 0% (0/7 tasks)                 |
| EN-203:    [....................] 0% (0/4 tasks)                 |
| EN-204:    [....................] 0% (0/6 tasks)                 |
| EN-205:    [....................] 0% (0/4 tasks)                 |
| EN-206:    [....................] 0% (0/6 tasks)                 |
| EN-207:    [....................] 0% (0/10 tasks)                |
+------------------------------------------------------------------+
| Total:     [....................] 0% (0/44 tasks)                |
+------------------------------------------------------------------+
```

---

## History

| Date | Author | Event |
|------|--------|-------|
| 2026-02-10 | Claude | Project created. EPIC-001, FEAT-001 with 5 bugs from PR #6 CI failures |
| 2026-02-10 | Claude | BUG-002, BUG-003 resolved. FEAT-001 restructured with EN-001, EN-002 Enablers |
| 2026-02-11 | Claude | EN-001 completed (BUG-001 + 3 tasks). EN-003 created and completed (BUG-006 regression + 2 tasks) |
| 2026-02-11 | Claude | EN-002 completed (BUG-004 + BUG-005). FEAT-001 100%. All 7 bugs resolved, CI green on PR #6 |
| 2026-02-11 | Claude | BUG-007 filed and resolved. Synthesis content check threshold raised to >= 3 files |
| 2026-02-11 | Claude | PII sanitization: replaced real names with generic names across 27 transcript files |
| 2026-02-11 | Claude | Partial cleanup: removed orphaned expected output file. Unnecessary test data directories with PII NOT addressed (premature closure) |
| 2026-02-11 | Claude | Reopened BUG-004 and EN-002: unnecessary test data directories with PII still on disk. Removed directories and cleaned references |
| 2026-02-11 | Claude | Git history sanitized: removed PII from commit messages, removed internal references |
| 2026-02-11 | Claude | PR #6 merged to main. Project reopened for continued OSS launch work |
| 2026-02-11 | Claude | Added FEAT-002 (Research, 7 enablers EN-101-107), FEAT-003 (CLAUDE.md Optimization, 7 enablers EN-201-207, 44 tasks). |
| 2026-02-11 | Claude | FEAT-001 reopened: EN-004 (Fix Pre-commit Hook Coverage) created with BUG-010 (session hook no auto-install) and BUG-011 (pytest hook python-only). Each bug has 1 task. Root cause of repeated CI failures on markdown-only commits identified. |
| 2026-02-11 | Claude | EN-004: DEC-001 and DEC-002 created via /problem-solving research. BUG-010 revised (make setup exists, auto-install rejected, warning improved). BUG-010 done. Code: session_start_hook.py warning updated, .pre-commit-config.yaml types_or + header fixed. 8/9 FEAT-001 bugs done. |
| 2026-02-11 | Claude | FEAT-001 closed: BUG-011 resolved, EN-004 done, all 9/9 bugs and 4/4 enablers complete. Entity files synchronized (EN-001 AC/progress, EN-002 status, EN-004 progress, FEAT-001 status). 100% complete. |

---

*Last Updated: 2026-02-11*
