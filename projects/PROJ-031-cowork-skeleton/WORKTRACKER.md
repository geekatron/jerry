# PROJ-031-cowork-skeleton -- Work Tracker

> Global manifest for the Jerry CoWork Skeleton Distribution project. Tracks all Epics, Features, Enablers, Stories, and Tasks with relationships.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Work Items](#work-items) | All active work items with status and parent |
| [Hierarchy](#hierarchy) | Decomposition tree |
| [Notes](#notes) | GitHub parity and structural notes |

---

## Work Items

| ID | Type | Title | Status | Parent |
|----|------|-------|--------|--------|
| EPIC-001 | Epic | Jerry CoWork Skeleton Distribution | pending | PROJ-031 |
| FEAT-001 | Feature | Skeleton Generation | pending | EPIC-001 |
| STORY-001 | Story | Skeleton Regeneration Script | pending | FEAT-001 |
| TASK-006 | Task | Strip-Set Correction and No-Duplicate-Skill-Names Gate (c-007) | pending | STORY-001 |
| STORY-002 | Story | Minimal projects/ Stub and README | pending | FEAT-001 |
| STORY-003 | Story | Skeleton Validation and Acceptance | pending | FEAT-001 |
| EN-001 | Enabler | CI Sync Automation | pending | EPIC-001 |
| TASK-001 | Task | Workflow Triggers and Permissions | pending | EN-001 |
| TASK-002 | Task | Regenerate-and-Push Job | pending | EN-001 |
| TASK-003 | Task | Token and Branch-Protection Strategy | pending | EN-001 |
| FEAT-002 | Feature | Security and Threat Model | pending | EPIC-001 |
| STORY-004 | Story | STRIDE Threat Model of Derived-Branch CI | pending | FEAT-002 |
| STORY-005 | Story | Threat Remediations and Branch-Protection Strategy | pending | FEAT-002 |
| FEAT-003 | Feature | User Documentation (Diataxis) and MkDocs | pending | EPIC-001 |
| STORY-006 | Story | Tutorial: Install Jerry in Claude CoWork | pending | FEAT-003 |
| STORY-007 | Story | How-To: Sync/Update Skeleton and Troubleshoot File-Limit | pending | FEAT-003 |
| STORY-008 | Story | Reference: Skeleton Branch and CI Workflow | pending | FEAT-003 |
| TASK-004 | Task | MkDocs and docs.yml Wiring | pending | STORY-008 |
| STORY-009 | Story | Explanation: Why the Skeleton Exists | pending | FEAT-003 |
| EN-002 | Enabler | Adversarial Quality Gate | pending | EPIC-001 |
| TASK-005 | Task | Quality Gate Definition and Per-Phase Application | pending | EN-002 |

---

## Hierarchy

```
EPIC-001: Jerry CoWork Skeleton Distribution
|
+-- FEAT-001: Skeleton Generation
|   +-- STORY-001: Skeleton Regeneration Script
|   |   +-- TASK-006: Strip-Set Correction and No-Duplicate-Skill-Names Gate (c-007)
|   +-- STORY-002: Minimal projects/ Stub and README
|   +-- STORY-003: Skeleton Validation and Acceptance
|
+-- EN-001: CI Sync Automation (Epic-level Enabler, INV-EN03)
|   +-- TASK-001: Workflow Triggers and Permissions
|   +-- TASK-002: Regenerate-and-Push Job
|   +-- TASK-003: Token and Branch-Protection Strategy
|
+-- FEAT-002: Security and Threat Model
|   +-- STORY-004: STRIDE Threat Model of Derived-Branch CI
|   +-- STORY-005: Threat Remediations and Branch-Protection Strategy
|
+-- FEAT-003: User Documentation (Diataxis) and MkDocs
|   +-- STORY-006: Tutorial: Install Jerry in Claude CoWork
|   +-- STORY-007: How-To: Sync/Update Skeleton and Troubleshoot File-Limit
|   +-- STORY-008: Reference: Skeleton Branch and CI Workflow
|   |   +-- TASK-004: MkDocs and docs.yml Wiring
|   +-- STORY-009: Explanation: Why the Skeleton Exists
|
+-- EN-002: Adversarial Quality Gate (Epic-level Enabler, INV-EN03)
    +-- TASK-005: Quality Gate Definition and Per-Phase Application
```

---

## Notes

- **GitHub Issue parity (H-32):** This is the `geekatron/jerry` repository, so every Epic, Feature, Enabler, Story, Task, and Bug MUST have a corresponding GitHub Issue. The initiative Epic **EPIC-001 ↔ [#305](https://github.com/geekatron/jerry/issues/305)** is created and linked (drafted at [work/EPIC-001-github-issue-draft.md](./work/EPIC-001-github-issue-draft.md)). Child issues (Features, Enablers, Stories, Tasks) are pending — to be created after the approval gate and tracked under parent Epic [#305](https://github.com/geekatron/jerry/issues/305); the maintainer creates and links them via `gh`.
- **Epic-level Enablers (INV-EN03):** EN-001 and EN-002 are parented directly under EPIC-001 as cross-cutting infrastructure and process work, permitted by the Enabler invariant `Enabler.allowed_parents = [Feature, Epic]`.
- **Task placement (containment):** TASK-004 (MkDocs wiring) is nested under STORY-008 rather than directly under FEAT-003, because a Feature's allowed children are Story and Enabler only — a Task cannot be a direct child of a Feature.
- **Status vocabulary:** All entities start at `pending` (the strategic/delivery initial state), keeping a single status vocabulary across the manifest.
- **TASK-006 (Strip-Set Correction + c-007 gate):** Added 2026-07-02 to capture the skeleton-generation strip-set correction surfaced by the 2026-07-02 live install test (dedicated repo `geekatron/jerry-claude-plugin`, installed on Claude Web). Parented under STORY-001 (regeneration script owns the strip logic; the c-007 gate is a generation step between strip and force-push). Design is already folded into ADR-PROJ031-001 (c-003/c-007/c-008). GitHub parity (H-32) is **live**: TASK-006 ↔ [#314](https://github.com/geekatron/jerry/issues/314), tracked under Epic [#305](https://github.com/geekatron/jerry/issues/305).
