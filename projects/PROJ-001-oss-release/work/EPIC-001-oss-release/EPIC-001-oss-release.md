# EPIC-001: OSS Release Preparation

> **Type:** epic
> **Status:** in_progress
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-10
> **Due:** ---
> **Completed:** ---
> **Parent:** —
> **Owner:** Adam Nowak
> **Target Quarter:** FY26-Q1

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and key objectives |
| [Business Outcome Hypothesis](#business-outcome-hypothesis) | Expected business outcomes |
| [Children (Features/Capabilities)](#children-featurescapabilities) | Feature inventory and tracking |
| [Progress Summary](#progress-summary) | Overall epic progress |
| [Related Items](#related-items) | Hierarchy and dependencies |
| [History](#history) | Status changes and key events |

---

## Summary

Prepare the Jerry framework for public open-source release on GitHub. This epic covers all work needed to ensure the codebase is clean, CI is passing, documentation is complete, and the project is welcoming to contributors.

**Key Objectives:**
- Fix all CI build failures blocking PR merge (FEAT-001 - done)
- Conduct deep research on Claude Code best practices (FEAT-002)
- Optimize CLAUDE.md and all skills using decomposition/imports patterns (FEAT-003)
- Migrate license from MIT to Apache 2.0 (FEAT-015 - done)
- Update README with platform support notice and documentation disclaimers (FEAT-016)
- Modernize installation instructions for repository-based access (FEAT-017)
- Create user-facing runbooks and playbooks (FEAT-018)

---

## Business Outcome Hypothesis

**We believe that** fixing all CI failures, conducting thorough research, and optimizing the framework

**Will result in** a stable, well-tested, well-documented framework that can be publicly shared and attract contributors

**We will know we have succeeded when** all CI checks pass green, documentation is complete for L0/L1/L2 personas, and the repository is ready for public access

---

## Children (Features/Capabilities)

### Feature Inventory

| ID | Title | Status | Priority | Progress |
|----|-------|--------|----------|----------|
| FEAT-001 | Fix CI Build Failures | done | high | 100% |
| FEAT-002 | Research and Preparation | done | high | 100% |
| FEAT-003 | CLAUDE.md Optimization | done | critical | 100% |
| FEAT-015 | License Migration (MIT to Apache 2.0) | done | high | 100% |
| FEAT-016 | Post-Release README & Documentation Updates | done | high | 100% |
| FEAT-017 | Installation Instructions Modernization | done | high | 100% |
| FEAT-018 | User Documentation — Runbooks & Playbooks | done | medium | 100% |

### Feature Links

- [FEAT-001: Fix CI Build Failures](./FEAT-001-fix-ci-build-failures/FEAT-001-fix-ci-build-failures.md)
- [FEAT-002: Research and Preparation](./FEAT-002-research-and-preparation/FEAT-002-research-and-preparation.md)
- [FEAT-003: CLAUDE.md Optimization](./FEAT-003-claude-md-optimization/FEAT-003-claude-md-optimization.md)
- [FEAT-015: License Migration (MIT to Apache 2.0)](./FEAT-015-license-migration/FEAT-015-license-migration.md)
- [FEAT-016: Post-Release README & Documentation Updates](./FEAT-016-post-release-documentation/FEAT-016-post-release-documentation.md)
- [FEAT-017: Installation Instructions Modernization](./FEAT-017-installation-instructions/FEAT-017-installation-instructions.md)
- [FEAT-018: User Documentation — Runbooks & Playbooks](./FEAT-018-user-documentation/FEAT-018-user-documentation.md)

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                     EPIC PROGRESS TRACKER                         |
+------------------------------------------------------------------+
| Features:  [####################] 100% (7/7 completed)            |
| Enablers:  [####################] 100% (37/37 completed)          |
| Bugs:      [################### ] 94% (15/16 completed)           |
| Tasks:     [####################] 100% (all completed)            |
+------------------------------------------------------------------+
| Overall:   [################### ] 98%                             |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Features** | 7 |
| **Completed Features** | 7 (FEAT-001, FEAT-002, FEAT-003, FEAT-015, FEAT-016, FEAT-017, FEAT-018) |
| **Pending Features** | 0 |
| **Feature Completion %** | 100% |
| **Total Enablers** | 37 (4 FEAT-001 + 8 FEAT-002 + 7 FEAT-003 + 6 FEAT-015 + 6 FEAT-016 + 3 FEAT-017 + 3 FEAT-018) |
| **Completed Enablers** | 37 |
| **Total Effort (new features)** | 24 (9 FEAT-016 + 7 FEAT-017 + 10 FEAT-018) |
| **Total Bugs (FEAT-001)** | 7 (all resolved) |
| **Total Bugs (FEAT-003)** | 8 (all resolved) |
| **Total Bugs (EPIC-001 direct)** | 1 (BUG-004, pending) |

---

## Related Items

### PR Reference

- **PR #6:** [fix: Windows CRLF line ending support in VTT validator](https://github.com/geekatron/jerry/pull/6) — Merged

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-10 | Claude | pending | Epic created |
| 2026-02-10 | Claude | in_progress | FEAT-001 created with 5 bugs from PR #6 CI failures |
| 2026-02-10 | Claude | in_progress | Progress sync: 2/5 bugs completed (BUG-002, BUG-003). FEAT-001 restructured with EN-001, EN-002 Enablers. |
| 2026-02-11 | Claude | in_progress | EN-001 completed (BUG-001 + 3 tasks). EN-003 created and completed (BUG-006 regression from EN-001/TASK-002 + 2 tasks). Progress: 67% (4/6 bugs, 2/3 enablers). |
| 2026-02-11 | Claude | done | EN-002 completed (BUG-004 + BUG-005, 3 tasks). FEAT-001 100%. All 6 bugs resolved, all 3 enablers done. Full test suite 2510 passed locally. Pending CI verification on PR #6. |
| 2026-02-11 | Claude | in_progress | Reopened: BUG-007 filed for `test_synthesis_contains_canon_doc` failure. Content check threshold too low. |
| 2026-02-11 | Claude | done | BUG-007 resolved. Raised content check threshold to >= 3 files. 7/7 bugs completed. CI verified green. |
| 2026-02-11 | Claude | in_progress | Reopened: OSS launch not yet complete. FEAT-001 (CI fixes) done, but additional features needed. |
| 2026-02-11 | Claude | in_progress | Added FEAT-002 (Research, 7 enablers EN-101-107) and FEAT-003 (CLAUDE.md Optimization, 7 enablers EN-201-207, 44 tasks). |
| 2026-02-12 | Claude | in_progress | FEAT-002 closed (all 8 enablers done including EN-108 version bumping). PR #12 merged. 8 EN-202 bugs closed. EN-207 confirmed complete. FEAT-003 at 57%. |
| 2026-02-12 | Claude | done | EN-206 complete (context distribution: .context/ restructure, bootstrap script, 22 integration tests). EN-204 complete (validation: 80 lines, 13/13 pointers, 2540 tests pass). EN-205 complete (docs: BOOTSTRAP.md, CLAUDE-MD-GUIDE.md, INSTALLATION.md updated). FEAT-003 100%. All 3 features, 20 enablers, 15 bugs complete. EPIC-001 closed. |
| 2026-02-12 | Claude | in_progress | **REOPENED**: Premature closure. All EPIC-001 deliverables bypassed quality framework: no adversarial feedback loops, no quality scoring (>=0.92 target), no creator→critic→revision cycles, no multi-platform testing (Windows/Linux). Closure was invalid per Jerry quality standards. All deliverables require retroactive quality review under EPIC-002. |
| 2026-02-16 | Claude | done | EPIC-001 re-closed. All 3 features validated by FEAT-006 retroactive quality review (EN-501: 0.949, EN-502: 0.951). Verification report: PROJ-001-epic001-verification-2026-02-16.md |
| 2026-02-17 | Claude | in_progress | **Reopened.** FEAT-015 created: License Migration (MIT to Apache 2.0). 6 enablers (EN-930–935), 14 effort points. Licensing is in PLAN.md scope with unchecked criterion. EPIC-001 now 4 features (3 done, 1 pending). |
| 2026-02-17 | Claude | in_progress | FEAT-015 completed (license migration). 3 new features created from post-release transcript packet: FEAT-016 (README & docs, 3 EN, 5 pts), FEAT-017 (installation instructions, 3 EN, 7 pts), FEAT-018 (runbooks/playbooks, 3 EN, 10 pts). DEC-004 recorded (3 decisions: OSX-primary, optimization deferred, installation model shift). EPIC-001 now 7 features (4 done, 3 pending), 34 enablers (25 done, 9 pending). |
| 2026-02-18 | Claude | in_progress | FEAT-016 completed. EN-936/937/938 done (README platform notice, Windows issue template, optimization disclaimer). EN-945 done (macOS + Linux issue templates, README links all 3 platforms). EPIC-001 now 5/7 features done, 29/35 enablers, ~75%. |
| 2026-02-18 | Claude | in_progress | EN-946 complete (feature-request.yml worktracker-aligned, config.yml, CONTRIBUTING.md updated). FEAT-016 re-closed at 5/5 enablers, 9/9 points. EPIC-001 now 5/7 features (71%), 31/36 enablers (86%), ~75%. |
| 2026-02-18 | Claude | done | FEAT-017 and FEAT-018 completed via orchestration workflow epic001-docs-20260218-001 (5 phases, 38 agents, 3 QGs). QG-1: 0.9220, QG-2: 0.926, QG-3: 0.937 — all PASS. Deliverables: docs/INSTALLATION.md (rewritten), docs/runbooks/getting-started.md, docs/playbooks/problem-solving.md, docs/playbooks/orchestration.md, docs/playbooks/transcript.md. All 7 features, 37 enablers, 15 bugs complete. **EPIC-001 CLOSED.** |
| 2026-02-18 | Claude | in_progress | **Reopened.** BUG-004 created: Plugin Uninstall Fails — Name/Scope Mismatch. Plugin UI shows `jerry @ jerry` but plugin.json declares `jerry-framework`. Uninstall fails with scope error. Also found: plugin.json license still says MIT (should be Apache-2.0). |
