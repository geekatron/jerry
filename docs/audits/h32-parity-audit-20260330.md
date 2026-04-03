# H-32 GitHub Issue Parity Audit

> **Type:** audit-report
> **Generated:** 2026-03-30T00:00:00Z
> **Agent:** wt-auditor
> **Audit Type:** h32-parity (full cross-project)
> **Scope:** All projects in repository (20 WORKTRACKER files, all entity files)
> **Rule:** H-32 — All worktracker bugs, stories, enablers, and tasks MUST have a corresponding GitHub Issue. Both MUST be kept in sync.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Coverage metrics, issue counts, verdict |
| [Critical: State Mismatches](#critical-state-mismatches) | Closed GH issue but worktracker entity not completed |
| [Major: Open Issues Without Worktracker Entities](#major-open-issues-without-worktracker-entities) | H-32 violations: open GH issues with no entity |
| [Info: Correctly Synced Pairs](#info-correctly-synced-pairs) | Verified synced pairs for completeness |
| [Remediation Plan](#remediation-plan) | Prioritized action list |
| [Audit Coverage](#audit-coverage) | Files checked, projects surveyed |

---

## Summary

| Metric | Value |
|--------|-------|
| **Projects Audited** | 20 |
| **Open GitHub Issues** | 35 |
| **Closed GitHub Issues** | 54 |
| **Worktracker Entities with GH Issue Refs** | 37 entities across 16 projects |
| **CRITICAL: GH closed but entity not completed** | 8 |
| **MAJOR: Open GH issue with no worktracker entity** | 23 |
| **INFO: Correctly synced pairs** | 22 |
| **Verdict** | **FAILED** |

---

## Critical: State Mismatches

> GH issue is CLOSED but worktracker entity is not in a terminal state (completed/done).
> These represent stale worktracker entries where the GH issue was resolved without updating the worktracker.

| ID | GH Issue | GH State | Entity File | Entity Status | Description |
|----|----------|----------|-------------|---------------|-------------|
| C-001 | [#46](https://github.com/geekatron/jerry/issues/46) | CLOSED | `projects/PROJ-001-oss-release/work/EPIC-001-oss-release/BUG-013-hook-uv-sync-wrong-directory/BUG-013-hook-uv-sync-wrong-directory.md` | `in_progress` | BUG-013: SessionStart hook uv sync runs in wrong directory. GH issue closed but entity has open checklist items and in_progress status. |
| C-002 | [#109](https://github.com/geekatron/jerry/issues/109) | CLOSED | `projects/PROJ-021-use-case/work/EPIC-021-001-use-case-capability-build/EPIC-021-001-use-case-capability-build.md` | `in_progress` | EPIC-021-001: Use Case Capability Build. GH issue closed (#109: "Build use case capability") but epic is in_progress. The epic's AC may still be open. |
| C-003 | [#113](https://github.com/geekatron/jerry/issues/113) | CLOSED | `projects/PROJ-017-portability/work/EPIC-017-001-platform-portability/FEAT-017-001-shell-command-portability/BUG-017-001-statusline-python3/BUG-017-001.md` | `pending` | BUG-017-001: statusLine command uses python3 which fails on Windows. GH #113 closed but entity still pending. Superseded by PROJ-024 fix. |
| C-004 | [#116](https://github.com/geekatron/jerry/issues/116) | CLOSED | `projects/PROJ-017-portability/work/EPIC-017-001-platform-portability/FEAT-017-002-file-system-portability/BUG-017-004-missing-gitattributes/BUG-017-004.md` | `pending` | BUG-017-004: Missing .gitattributes. GH #116 closed (fix delivered via EN-005-gitattributes in PROJ-024) but PROJ-017 entity still pending. Duplicate tracking. |
| C-005 | [#117](https://github.com/geekatron/jerry/issues/117) | CLOSED | `projects/PROJ-017-portability/work/EPIC-017-001-platform-portability/FEAT-017-002-file-system-portability/BUG-017-005-hardcoded-path-separator/BUG-017-005.md` | `pending` | BUG-017-005: hardcoded forward slash in file_repository.py. GH #117 closed (fixed in PROJ-024 BUG-006) but PROJ-017 entity still pending. |
| C-006 | [#118](https://github.com/geekatron/jerry/issues/118) | CLOSED | `projects/PROJ-017-portability/work/EPIC-017-001-platform-portability/FEAT-017-001-shell-command-portability/BUG-017-006-macos-symlink-resolution/BUG-017-006.md` | `pending` | BUG-017-006: verify-symlinks.sh macOS fallback assumes python3. GH #118 closed but PROJ-017 entity still pending. |
| C-007 | [#138](https://github.com/geekatron/jerry/issues/138) | CLOSED | `projects/PROJ-022-user-experience-skill/WORKTRACKER.md` | `ACTIVE` | PROJ-022 UX skill WORKTRACKER. GH #138 ("feat: Add /user-experience skill") is CLOSED but WORKTRACKER.md says ACTIVE with 0/8 epics complete, 0/26 features complete. The GH issue tracked the feature request; the project was never delivered. |
| C-008 | [#153](https://github.com/geekatron/jerry/issues/153) | CLOSED | `projects/PROJ-030-bugs/work/EN-001-ci-pipeline-hardening.md` | `in_progress` | EN-001: CI pipeline security hardening. GH #153 closed but enabler is in_progress. TASK-003 (pre_tool_use consolidation) and TASK-004 (permission reference) are still in_progress. The GH issue may have been closed prematurely or tracks a subset of the enabler scope. |

---

## Major: Open Issues Without Worktracker Entities

> GH issue is OPEN but no worktracker entity references it.
> This is an H-32 violation: the open issue has no SSOT entry in the worktracker.

### Bugs (Highest Priority — Open bugs MUST have worktracker entity)

| ID | GH Issue | Title | Severity Assessment |
|----|----------|-------|---------------------|
| M-001 | [#223](https://github.com/geekatron/jerry/issues/223) | BUG-023-003: E2E smoke tests bypass skill layer, cover only 8/33 tools | CRITICAL priority label — no worktracker entity in any project |
| M-002 | [#199](https://github.com/geekatron/jerry/issues/199) | bug: uc-slicer append-only re-invocation lacks duplicate slice_id conflict detection | Bug in /use-case skill, no worktracker entity |
| M-003 | [#198](https://github.com/geekatron/jerry/issues/198) | bug: cd-generator banned-term check false positives on domain vocabulary under 60 chars | Bug in /contract-design skill, no worktracker entity |
| M-004 | [#197](https://github.com/geekatron/jerry/issues/197) | bug: tspec-analyst uses live UC as coverage denominator instead of generation-time snapshot | Bug in /test-spec skill, no worktracker entity |
| M-005 | [#196](https://github.com/geekatron/jerry-wt/issues/196) | bug: tspec-analyst has no cross-slice aggregate coverage mechanism | Bug in /test-spec skill, no worktracker entity |
| M-006 | [#195](https://github.com/geekatron/jerry/issues/195) | bug: tspec-generator silently skips extensions with unrecognized outcome values | Bug in /test-spec skill, no worktracker entity |
| M-007 | [#34](https://github.com/geekatron/jerry/issues/34) | Filename too long | Old open bug, no worktracker entity |

### Epics / Features (Open — No Worktracker Entity)

| ID | GH Issue | Title | Notes |
|----|----------|-------|-------|
| M-008 | [#218](https://github.com/geekatron/jerry/issues/218) | EPIC-023-010: E2E Engagement Validation Suite | CRITICAL priority. References imply a PROJ-023 worktracker but no project directory exists. References found only in non-entity orchestration files. |
| M-009 | [#221](https://github.com/geekatron/jerry/issues/221) | FEAT-023-014: Real E2E Engagement Lifecycle | CRITICAL priority. Part of EPIC-023 cluster. No worktracker entity. |
| M-010 | [#222](https://github.com/geekatron/jerry/issues/222) | FEAT-023-015: Engagement Gate System | HIGH priority. Part of EPIC-023 cluster. No worktracker entity. |
| M-011 | [#220](https://github.com/geekatron/jerry/issues/220) | FEAT-023-013: Full 33-Tool Smoke Test Matrix | HIGH priority. Part of EPIC-023 cluster. No worktracker entity. |
| M-012 | [#219](https://github.com/geekatron/jerry/issues/219) | FEAT-023-012: Vulnerable Target Infrastructure | HIGH priority. Part of EPIC-023 cluster. No worktracker entity. |
| M-013 | [#194](https://github.com/geekatron/jerry/issues/194) | epic: PROJ-021 C4 Tournament -- 6 Remaining Major Findings (0.926 → 0.95) | Open enhancement for PROJ-021. No dedicated worktracker entity. |
| M-014 | [#192](https://github.com/geekatron/jerry/issues/192) | enhancement: configurable output base path for skill agents | Open enhancement. No worktracker entity. |
| M-015 | [#208](https://github.com/geekatron/jerry/issues/208) | feat(rainbow-series): /blue-team Defensive Cybersecurity Skill Suite | Open feature. No worktracker entity or project. |
| M-016 | [#200](https://github.com/geekatron/jerry/issues/200) | enhancement: use-case SKILL.md missing Activity 5 entry in Common Workflows | Open docs/enhancement. No worktracker entity. |

### Research / Enhancements (Open — No Worktracker Entity)

| ID | GH Issue | Title | Notes |
|----|----------|-------|-------|
| M-017 | [#190](https://github.com/geekatron/jerry/issues/190) | deps: Upgrade pytest-bdd + gherkin-official when pytest-bdd removes upper bound | Tech debt, open. No worktracker entity. |
| M-018 | [#144](https://github.com/geekatron/jerry/issues/144) | feat(ux): Make UX skill output paths configurable via shared resolution utility | Enhancement. No worktracker entity. |
| M-019 | [#143](https://github.com/geekatron/jerry/issues/143) | PROJ: Public benchmarking framework — raw Claude vs Jerry | Research project. No worktracker entity. |
| M-020 | [#140](https://github.com/geekatron/jerry/issues/140) | evals? | Research item. No worktracker entity. |
| M-021 | [#101](https://github.com/geekatron/jerry/issues/101) | Research and define strategy for deploying Claude Code instances as PR listeners | Research. No worktracker entity. |
| M-022 | [#100](https://github.com/geekatron/jerry/issues/100) | Audit and update root README.md to be accurate | Open. No dedicated worktracker entity. |
| M-023 | [#98](https://github.com/geekatron/jerry/issues/98) | Extract project tracker to its own repo | Open architectural proposal. No worktracker entity. |

### Note on Open Issues With Worktracker Coverage (Correctly Tracked)

The following open GH issues DO have worktracker entities with matching open/in-progress status and are **not violations**:

- **#53** (Cartesian product bug) → BUG-001 PROJ-007 `pending` — OK
- **#114** (PowerShell migration scripts) → BUG-017-002 PROJ-017 `pending` — OK
- **#115** (Windows symlink docs) → BUG-017-003 PROJ-017 `pending` — OK
- **#119** (/tmp in docstrings) → BUG-017-007 PROJ-017 `pending` — OK
- **#130** (Docs audit) → WORKTRACKER PROJ-015 `Complete` — but see **INFO-001** below
- **#135** (PROJ-016 documentation writing) → referenced in PROJ-030 drafts only, not as entity
- **#175** (documentation freshness approach) → referenced in PROJ-030 strategic plan, not entity
- **#179** (Claude Code permission reference) → TASK-004 PROJ-030 `in_progress` — OK
- **#80** (orchestration phases 6-9) → referenced in PROJ-001 EPIC visualization, not entity

---

## Info: Correctly Synced Pairs

> GH issue state matches worktracker entity status.

| GH Issue | GH State | Entity | Entity Status |
|----------|----------|--------|---------------|
| [#38](https://github.com/geekatron/jerry/issues/38) | CLOSED | BUG-011 PROJ-001 | `done` |
| [#51](https://github.com/geekatron/jerry/issues/51) | CLOSED | BUG-001 PROJ-004 | `completed` |
| [#62](https://github.com/geekatron/jerry/issues/62) | CLOSED | FEAT-001 PROJ-004 | `completed` |
| [#63](https://github.com/geekatron/jerry/issues/63) | CLOSED | FEAT-002 PROJ-004 | `completed` |
| [#75](https://github.com/geekatron/jerry/issues/75) | CLOSED | BUG-003 PROJ-005 | `completed` |
| [#68](https://github.com/geekatron/jerry/issues/68) | CLOSED | PROJ-010 WORKTRACKER | `COMPLETED` |
| [#99](https://github.com/geekatron/jerry/issues/99) | CLOSED | EPIC-013-001 PROJ-013 | `completed` |
| [#111](https://github.com/geekatron/jerry/issues/111) | CLOSED | BUG-001 PROJ-030 | `completed` |
| [#132](https://github.com/geekatron/jerry/issues/132) | CLOSED | BUG-002 PROJ-030 | `completed` |
| [#151](https://github.com/geekatron/jerry/issues/151) | CLOSED | BUG-003 PROJ-030 | `completed` |
| [#177](https://github.com/geekatron/jerry/issues/177) | CLOSED | STORY-023 PROJ-024 | `completed` |
| [#178](https://github.com/geekatron/jerry/issues/178) | CLOSED | STORY-024 PROJ-024 | `completed` |
| [#180](https://github.com/geekatron/jerry/issues/180) | CLOSED | BUG-004 PROJ-030 | `completed` |
| [#181](https://github.com/geekatron/jerry/issues/181) | CLOSED | BUG-005 PROJ-030 | `completed` |
| [#182](https://github.com/geekatron/jerry/issues/182) | CLOSED | TASK-005 PROJ-030 | `completed` |
| [#193](https://github.com/geekatron/jerry/issues/193) | CLOSED | STORY-025 PROJ-024 | `completed` |
| [#213](https://github.com/geekatron/jerry/issues/213) | CLOSED | BUG-007 PROJ-024 | `completed` |
| [#214](https://github.com/geekatron/jerry/issues/214) | CLOSED | BUG-005 PROJ-024 | `completed` |
| [#217](https://github.com/geekatron/jerry/issues/217) | CLOSED | STORY-011 PROJ-024 | `completed` |
| [#226](https://github.com/geekatron/jerry/issues/226) | CLOSED | BUG-001 PROJ-024 | `completed` |
| [#227](https://github.com/geekatron/jerry/issues/227) | CLOSED | BUG-002 PROJ-024 | `completed` |
| [#228](https://github.com/geekatron/jerry/issues/228) | CLOSED | BUG-003 PROJ-024 | `completed` |

### Additional Info Items

| ID | Issue | Observation |
|----|-------|-------------|
| INFO-001 | [#130](https://github.com/geekatron/jerry/issues/130) | OPEN GH issue but WORKTRACKER PROJ-015 says `Complete`. Inverse of a CRITICAL — the worktracker is ahead of GH. Close GH #130 to re-sync. |
| INFO-002 | [#96](https://github.com/geekatron/jerry/issues/96) | "Slim down agent definitions" — open GH issue, no entity. Conceptually in scope of ongoing work but not formally tracked. |
| INFO-003 | [#116](https://github.com/geekatron/jerry/issues/116) | Closed GH issue referenced by TWO entities: EN-005 PROJ-024 (completed, correct) and BUG-017-004 PROJ-017 (pending, stale). PROJ-017 entity is a duplicate; the fix landed via PROJ-024. |
| INFO-004 | [#117](https://github.com/geekatron/jerry/issues/117) | Same as INFO-003 — closed GH issue referenced by BUG-006 PROJ-024 (completed, correct) and BUG-017-005 PROJ-017 (pending, stale). |
| INFO-005 | [#135](https://github.com/geekatron/jerry/issues/135) | Open GH issue "PROJ-016: User-facing documentation writing" with project number in title. PROJ-016-documentation-writing WORKTRACKER exists but does not contain a GH Issue reference field pointing to #135. |

---

## Remediation Plan

### Priority 1: Critical State Mismatches (Effort: Low — status field updates only)

1. **C-001 (Effort: low):** Mark BUG-013 `projects/PROJ-001-oss-release/work/EPIC-001-oss-release/BUG-013-hook-uv-sync-wrong-directory/BUG-013-hook-uv-sync-wrong-directory.md` as `completed`. GH #46 is closed; partial checklist items are moot.
2. **C-003 (Effort: low):** Mark BUG-017-001 `projects/PROJ-017-portability/...BUG-017-001.md` as `completed` or `cancelled`. GH #113 is closed; fix delivered via separate PROJ-024 track.
3. **C-004 (Effort: low):** Mark BUG-017-004 `projects/PROJ-017-portability/...BUG-017-004.md` as `completed`. GH #116 closed; fix delivered via EN-005-gitattributes in PROJ-024.
4. **C-005 (Effort: low):** Mark BUG-017-005 `projects/PROJ-017-portability/...BUG-017-005.md` as `completed`. GH #117 closed; fix delivered via BUG-006 in PROJ-024.
5. **C-006 (Effort: low):** Mark BUG-017-006 `projects/PROJ-017-portability/...BUG-017-006.md` as `completed`. GH #118 closed.
6. **C-008 (Effort: medium):** For EN-001 CI hardening (`projects/PROJ-030-bugs/work/EN-001-ci-pipeline-hardening.md`): either (a) complete the remaining TASK-003 and TASK-004 sub-tasks and mark EN-001 `completed`, or (b) if GH #153 was closed as partial-scope, add a note to the entity and keep tracking remaining tasks under new GH issues. GH #179 (TASK-004) is already open and correctly tracked.

### Priority 2: Critical State Mismatches (Effort: Medium — requires investigation)

7. **C-002 (Effort: medium):** EPIC-021-001 `in_progress` vs GH #109 CLOSED. Determine if the epic's remaining work (content quality tournament, 6 open findings from GH #194) should remain under PROJ-021 or be tracked as a new issue. If EPIC scope is complete, mark `completed`. If ongoing, the epic may need to track GH #194 instead.
8. **C-007 (Effort: low):** PROJ-022 UX skill WORKTRACKER says `ACTIVE` but GH #138 is CLOSED. The GH issue tracked the feature request decision ("add UX skill"), not the implementation. The WORKTRACKER's ACTIVE status is correct for ongoing implementation. Close GH #138 cleanly or open a new implementation tracking issue. Add that new issue reference to WORKTRACKER.md.

### Priority 3: Major H-32 Violations — Bug Entities Needed (Effort: Low per item)

9. **M-001 (Effort: low):** Create worktracker entity for GH #223 (E2E smoke tests bypass skill layer). Create `BUG` entity in an appropriate project (PROJ-023 or PROJ-024). Link entity to #223.
10. **M-002 to M-006 (Effort: low each):** Create worktracker entities for GH bugs #199, #198, #197, #196, #195 (use-case/test-spec/contract-design skill bugs). These belong in PROJ-021 (use-case skill project) or a new PROJ-025-bugfix project. Each needs a `BUG` entity file with `GitHub Issue: [#NNN]` reference.
11. **M-007 (Effort: low):** Create worktracker entity for GH #34 (Filename too long). Oldest open bug — determine if still relevant; if so, create `BUG` entity with #34 reference.

### Priority 4: Major H-32 Violations — PROJ-023 E2E Cluster (Effort: Medium)

12. **M-008 to M-012 (Effort: medium collectively):** Issues #218, #219, #220, #221, #222 form the EPIC-023 E2E Engagement Validation Suite cluster. These appear to be planned work with no corresponding project directory. Action: create `projects/PROJ-023-e2e-validation/` with WORKTRACKER.md, create entity files for EPIC-023-010, FEAT-023-012 through FEAT-023-015, and link each to its GH issue.

### Priority 5: Major H-32 Violations — Enhancements (Effort: Low per item)

13. **M-013 (Effort: low):** GH #194 (PROJ-021 C4 tournament remaining findings). Create a STORY or TASK entity in PROJ-021 worktracker.
14. **M-014 (Effort: low):** GH #192 (configurable output base path). Create EN or STORY entity in PROJ-024 or new project. Link to #192.
15. **M-015 to M-023 (Effort: low each):** For each remaining MAJOR item (#208, #200, #190, #144, #143, #140, #101, #100, #98), either: (a) create a worktracker entity if the work is planned/active, or (b) add a `wontfix` label to the GH issue and note "Not tracked in worktracker — backlog only" if not planned.

### Priority 6: Info Items (Effort: Trivial)

16. **INFO-001 (Effort: trivial):** Close GH #130 — PROJ-015 docs audit is `Complete` in the worktracker. GH issue is stale open.
17. **INFO-003 and INFO-004 (Effort: trivial):** Mark PROJ-017 stale duplicate entities (BUG-017-004, BUG-017-005) as `completed` or add note: "Fixed via PROJ-024 track. GH issue closed."
18. **INFO-005 (Effort: trivial):** Add `GitHub Issue: [#135](https://github.com/geekatron/jerry/issues/135)` to `projects/PROJ-016-documentation-writing/WORKTRACKER.md` header.

---

## Audit Coverage

### Projects Audited

| Project | WORKTRACKER | GH Issue Refs | Coverage |
|---------|-------------|---------------|----------|
| PROJ-001-oss-release | Yes | BUG-011 (#38), BUG-013 (#46) | Partial — many entities lack GH refs |
| PROJ-002-roadmap-next | Yes | None found | No GH Issue refs |
| PROJ-003-je-ne-sais-quoi | Yes | None found | No GH Issue refs |
| PROJ-004-context-resilience | Yes | BUG-001 (#51), FEAT-001 (#62), FEAT-002 (#63) | Covered |
| PROJ-005-markdown-ast | Yes | BUG-003 (#75) | Partial |
| PROJ-006-multi-instance | Yes | None found | No GH Issue refs |
| PROJ-007-agent-patterns | Yes | BUG-001 (#53) | Covered |
| PROJ-008-agentic-security | Yes | None found | No GH Issue refs |
| PROJ-009-llm-deception-research | Yes | None found | No GH Issue refs (research project, expected) |
| PROJ-010-cyber-ops | Yes | #68 | Covered — completed |
| PROJ-011-saucer-boy-articles | Yes | None found | No GH Issue refs (content project, expected) |
| PROJ-013-diataxis | Yes | #99 | Covered — completed |
| PROJ-014-negative-prompting-research | Yes | #122 (research artifact ref) | Partial — EPIC-005 in_progress, #122 closed |
| PROJ-015-documentation-audit | Yes | #130 | State mismatch (INFO-001) |
| PROJ-016-documentation-writing | Yes | None in WORKTRACKER | Missing #135 ref (INFO-005) |
| PROJ-017-portability | Yes | #113-119 (7 entities) | Multiple mismatches (C-003 to C-006) |
| PROJ-020-feature-enhancements | Yes | None found | No GH Issue refs |
| PROJ-021-use-case | Yes | #109 | EPIC in_progress vs closed GH (C-002) |
| PROJ-022-user-experience-skill | Yes | #138 | State mismatch (C-007) |
| PROJ-024-tactical-work | Yes | #177, #178, #193, #213, #214, #217, #226, #227, #228 | All synced correctly |
| PROJ-030-bugs | Yes | #111, #132, #151, #153, #180, #181, #182 | Partial mismatches (C-008) |

### Coverage Gaps

The following entity types were NOT audited for GH Issue presence (no `GitHub Issue:` field found):

- PROJ-001-oss-release: extensive FEAT-* and EN-* entities without GH refs (pre-H-32 work)
- PROJ-002, PROJ-003, PROJ-006, PROJ-008: no GH refs found — these projects predate or are exempt from H-32 enforcement (non-jerry-repo projects or purely internal research)
- PROJ-014 EPIC-005 `in_progress` references GH #122 (CLOSED) — this is a research artifact reference, not a direct entity tracker; acceptable but noted

### H-32 Rule Scope Note

H-32 applies specifically when the active repository is `geekatron/jerry`. All 20 projects audited are within this repository's worktree. Projects PROJ-009 (research), PROJ-011 (articles), and PROJ-006 (multi-instance) contain no GH Issue refs but are likely content/research projects where H-32 was not enforced — this is an acceptable gap unless those projects contain bugs or stories.

---

## Findings Summary

| Severity | Count | Root Cause |
|----------|-------|------------|
| CRITICAL (closed GH, entity not terminal) | 8 | Fixes delivered without updating worktracker status |
| MAJOR (open GH, no entity) | 23 | Issues created but worktracker entity never created |
| INFO | 5 | Minor sync gaps, stale duplicates |
| **TOTAL** | **36** | |

**Primary systemic gap:** The H-32 enforcement is one-directional. When issues are fixed and closed, worktracker entities are often not updated. And when new GH issues are filed, corresponding worktracker entities are frequently not created. The 23 MAJOR violations represent a large backlog of GH issues that exist outside the worktracker SSOT entirely.

---

*Audit generated: 2026-03-30 | Agent: wt-auditor v1.0.0 | Fix Mode: report (no auto-fixes applied)*
