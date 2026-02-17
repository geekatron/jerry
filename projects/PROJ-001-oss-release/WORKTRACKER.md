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
| [EPIC-001](./work/EPIC-001-oss-release/EPIC-001-oss-release.md) | OSS Release Preparation | done | high |
| [EPIC-002](./work/EPIC-002-quality-enforcement/EPIC-002-quality-enforcement.md) | Quality Framework Enforcement & Course Correction | done | critical |
| [EPIC-003](./work/EPIC-003-quality-implementation/EPIC-003-quality-implementation.md) | Quality Framework Implementation | in_progress | critical |
| [EPIC-004](./work/EPIC-004-advanced-adversarial/EPIC-004-advanced-adversarial.md) | Advanced Adversarial Capabilities | pending | medium |

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
| [BUG-001](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-202-claude-md-rewrite/BUG-001-relationships-typo.md) | Relationships typo | done | low | EN-202 |
| [BUG-002](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-202-claude-md-rewrite/BUG-002-story-folder-id-mismatch.md) | Story folder ID mismatch | done | low | EN-202 |
| [BUG-003](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-202-claude-md-rewrite/BUG-003-template-path-inconsistency.md) | Template path inconsistency | done | medium | EN-202 |
| [BUG-004](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-202-claude-md-rewrite/BUG-004-todo-section-not-migrated.md) | TODO section not migrated | done | medium | EN-202 |
| [BUG-005](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-202-claude-md-rewrite/BUG-005-mandatory-skill-usage-lost.md) | Mandatory skill usage lost | done | high | EN-202 |
| [BUG-006](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-202-claude-md-rewrite/BUG-006-working-with-jerry-lost.md) | Working with Jerry section lost | done | high | EN-202 |
| [BUG-007](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-202-claude-md-rewrite/BUG-007-problem-solving-templates-lost.md) | Problem solving templates lost | done | medium | EN-202 |
| [BUG-008](./work/EPIC-001-oss-release/FEAT-003-claude-md-optimization/EN-202-claude-md-rewrite/BUG-008-askuserquestion-flow-lost.md) | AskUserQuestion flow lost | done | medium | EN-202 |
| [BUG-001](./work/EPIC-003-quality-implementation/BUG-001-pr13-ci-pipeline-failures/BUG-001-pr13-ci-pipeline-failures.md) | PR #13 CI Pipeline Failures | in_progress | critical | EPIC-003 |

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
| FEAT-002 | Research and Preparation | 2026-02-12 | All 8 enablers complete (EN-101 through EN-108). EN-108 version bumping merged via PR #12. |
| BUG-001 (EN-202) | Relationships typo | 2026-02-02 | NOT_APPLICABLE — content extracted to /worktracker skill |
| BUG-002 (EN-202) | Story folder ID mismatch | 2026-02-02 | NOT_APPLICABLE — content extracted to /worktracker skill |
| BUG-003 (EN-202) | Template path inconsistency | 2026-02-02 | FIXED — paths corrected in new CLAUDE.md |
| BUG-004 (EN-202) | TODO section not migrated | 2026-02-02 | FIXED — EN-203 executed, todo-integration-rules.md created |
| BUG-005 (EN-202) | Mandatory skill usage lost | 2026-02-02 | FIXED — mandatory-skill-usage.md created in .claude/rules/ |
| BUG-006 (EN-202) | Working with Jerry section lost | 2026-02-02 | FIXED — project-workflow.md created in .claude/rules/ |
| BUG-007 (EN-202) | Problem solving templates lost | 2026-02-02 | FIXED — templates added to problem-solving SKILL.md |
| BUG-008 (EN-202) | AskUserQuestion flow lost | 2026-02-02 | FIXED — added to project-workflow.md |
| EN-206 | Context Distribution Strategy | 2026-02-12 | .context/ restructure, bootstrap script, 22 integration tests |
| EN-204 | Validation & Testing | 2026-02-12 | 80 lines, 13/13 pointers, 2540 tests pass |
| EN-205 | Documentation Update | 2026-02-12 | BOOTSTRAP.md, CLAUDE-MD-GUIDE.md, INSTALLATION.md updated |
| FEAT-003 | CLAUDE.md Optimization | 2026-02-12 | All 7 enablers complete. 80 lines, tiered loading, context distribution |
| EPIC-001 | OSS Release Preparation | 2026-02-16 | Re-closed after retroactive validation (FEAT-006). All 3 features, 20 enablers, 15 bugs. EN-501: 0.949, EN-502: 0.951. |
| FEAT-010 | FEAT-009 Tournament Remediation | 2026-02-15 | All 7 enablers PASS (avg 0.933). FEAT-009 re-scored 0.93. 260 E2E tests pass. |
| EPIC-003 | Quality Framework Implementation | — | IN PROGRESS: 4/6 features done (FEAT-008/009/010/011), FEAT-012 + FEAT-014 pending. 73% complete. |
| EN-501 | FEAT-003 Retroactive Quality Review | 2026-02-16 | Score 0.949 (3 iterations). 16 fixed, 4 accepted, 3 N/A, 2 info. |
| EN-502 | Bootstrap Cross-Platform Validation | 2026-02-16 | Score 0.951 (4 iterations). 47 tests passing. All HIGH resolved. |
| FEAT-006 | EPIC-001 Retroactive Quality Review | 2026-02-16 | All 5 enablers complete (EN-501: 0.949, EN-502: 0.951, EN-503/504/505 closed). |
| EPIC-002 | Quality Framework Enforcement | 2026-02-16 | All 4 features (FEAT-004/005/006/013), 24 enablers, 163 effort points, 100% complete. |

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
| 2026-02-12 | Claude | EN-108 complete. FEAT-002 closed (all 8 enablers done). PR #12 merged. |
| 2026-02-12 | Claude | All 8 EN-202 bugs closed (resolved in earlier sessions). EN-207 confirmed complete. |
| 2026-02-12 | Claude | Feature branch feature/PROJ-001-oss-release-feat003 created for remaining FEAT-003 work. |
| 2026-02-12 | Claude | EN-206 complete: .context/ restructure with symlinks, bootstrap_context.py, /bootstrap skill, 22 integration tests, docs/BOOTSTRAP.md |
| 2026-02-12 | Claude | EN-204 complete: Validation passed (80 lines, 13/13 pointers, 2540 tests, no worktracker content in CLAUDE.md) |
| 2026-02-12 | Claude | EN-205 complete: docs/CLAUDE-MD-GUIDE.md, docs/BOOTSTRAP.md, INSTALLATION.md updated |
| 2026-02-12 | Claude | FEAT-003 closed: All 7 enablers complete (100%). EPIC-001 closed: All 3 features complete (100%). |

| 2026-02-12 | Claude | EPIC-001 REOPENED: Premature closure without quality gates. All EPIC-001 deliverables bypassed adversarial feedback loops, quality scoring (>=0.92), creator→critic→revision cycles, and multi-platform testing. |
| 2026-02-12 | Claude | Project status reverted from COMPLETE to IN_PROGRESS. |
| 2026-02-12 | Claude | EPIC-002 created: Quality Framework Enforcement & Course Correction. Addresses enforcement mechanisms, adversarial strategy research, retroactive quality review, and skill enhancement. |
| 2026-02-12 | Claude | EPIC-002 expanded: FEAT-004 updated (18 FC + 8 NFC, EN-307 added for /orchestration), FEAT-005 updated (19 FC + 8 NFC). 13 enabler entity files created (EN-301–307, EN-401–406). FEAT-007 created (Advanced Adversarial Capabilities, 5 enablers EN-601–605). Total: 4 features, 23 enablers, 199 points. |
| 2026-02-12 | Claude | EN-301 TASK-001/002/003 complete: 36 adversarial strategies cataloged across academic (12), industry/LLM (14), emerging (10). ~117 citations, ~4,500 lines of research. 5 background agents used (ps-researcher ×3, nse-explorer ×1). |
| 2026-02-12 | Claude | EN-401 TASK-001/002 complete: Claude Code hooks (729 lines, 24 refs) and guardrail frameworks (1,724 lines, 30 refs). |
| 2026-02-13 | Claude | EN-301 TASK-004 (synthesis) launched: ps-synthesizer consolidating 36 candidates into 15-strategy catalog. EN-401 TASK-003/004/005 launched in parallel: .claude/rules/ patterns, prompt engineering enforcement, alternative approaches. |
| 2026-02-13 | Claude | EN-301 TASK-004 (synthesis) complete. EN-401 TASK-003/004/005 all complete. All task entity files being rewritten to use official /worktracker TASK template (NFC-6 compliance). |
| 2026-02-14 | Claude | EPIC-003 created: Quality Framework Implementation. Implements EPIC-002 designs into code. FEAT-008 with 11 enablers (EN-701–EN-711) across 5 phases: Foundation, Deterministic, Probabilistic, Skills, Integration. |
| 2026-02-14 | Claude | FEAT-009 created under EPIC-003: Adversarial Strategy Templates & /adversary Skill. 12 enablers (EN-801–EN-812) across 7 phases. 10 strategy templates, 3 skill agents, agent extensions, E2E tests. |
| 2026-02-15 | Claude | FEAT-009 all 12 enablers PASS (>= 0.92). C4 Tournament Review applied all 10 strategies — composite score 0.85 (REVISE). 7 Critical, 18 Major, 20 Minor findings. |
| 2026-02-15 | Claude | FEAT-009 orchestration artifacts moved from wrong folder (FEAT-009-adversarial-templates/) to correct folder (FEAT-009-adversarial-strategy-templates/). Old folder deleted. |
| 2026-02-15 | Claude | FEAT-010 created under EPIC-003: FEAT-009 Tournament Remediation. 7 enablers (EN-813–EN-819), 29 tasks, 26 effort points. Addresses all P0 Critical and P1 Major findings. |
| 2026-02-15 | Claude | FEAT-010 completed: All 7 enablers PASS (avg 0.933, lowest 0.922). FEAT-009 re-scored from 0.85 to 0.93. 260 E2E tests pass. All Critical and Major findings resolved. |
| 2026-02-15 | Claude | EPIC-003 completed: All 4 features (FEAT-008, FEAT-009, FEAT-010, FEAT-011), 34 enablers, 100% complete. Quality framework fully implemented with working enforcement. |
| 2026-02-16 | Claude | FEAT-012 created under EPIC-002: Progressive Disclosure Rules Architecture. 6 enablers (EN-901–906), 32 tasks. Restructures .context/rules/ into tiered progressive disclosure: enforcement rules (auto-loaded) + companion guides (on-demand) + code patterns (on-demand). Remediates naive EN-702 token optimization that deleted educational content. |
| 2026-02-16 | Claude | EPIC-002 full audit: wt-auditor (27 issues), wt-verifier (4 enablers verified), wt-visualizer (hierarchy diagrams). Progress metrics corrected. |
| 2026-02-16 | Claude | FEAT-013 created under EPIC-002: Worktracker Integrity Remediation. 6 enablers (EN-907–912), 29 tasks, 15 effort points. Fixes all audit findings. |

| 2026-02-16 | Claude | EN-501 closed (0.949, 3 iterations). EN-502 closed (0.951, 4 iterations). FEAT-006 closed (5/5 enablers). EPIC-002 closed (4/4 features, 24/24 enablers, 163/163 points). Quality framework enforcement complete and all EPIC-001 deliverables retroactively validated. |
| 2026-02-16 | Claude | PROJ-001 full audit (wt-auditor/wt-verifier/wt-visualizer): 14 errors, 11 warnings, 5 info. Corrective actions: EPIC-001 re-closed (done), EPIC-003 reverted to in_progress (FEAT-012 pending, FEAT-007 deferred), FEAT-004/005 ACs checked + Evidence added, FEAT-013 DoD verified + Evidence added, FEAT-002 enabler count fixed (7→8), FEAT-003 broken link fixed. All entity files now have delivery evidence per WTI-006. |
| 2026-02-16 | Claude | EPIC-004 created (Advanced Adversarial Capabilities, pending, medium priority). FEAT-007 moved from EPIC-003 to EPIC-004 — deferred strategies requiring cross-model LLM infrastructure, not needed for OSS release. |
| 2026-02-17 | Claude | FEAT-014 created under EPIC-003: Framework Synchronization. 5 enablers (EN-925–929), 21 tasks, 18 effort points. Codebase audit found 15 gaps: incomplete AGENTS.md, missing /adversary rule triggers, truncated skill docs, no adversarial template tests. EPIC-003 now 6 features (4 done, 2 pending). |
| 2026-02-17 | Claude | BUG-001 created under EPIC-003: PR #13 CI Pipeline Failures. 8 tasks across 3 root causes: (A) 11 uv-dependent tests missing subprocess marker, (B) Windows PowerShell syntax errors in ci.yml, (C) cascading gate/coverage failures. Priority: critical. |

---

*Last Updated: 2026-02-17*
