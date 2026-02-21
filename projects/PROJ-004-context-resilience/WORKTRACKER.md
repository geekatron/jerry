# PROJ-004: Context Resilience - Work Tracker

> Global Manifest for PROJ-004. Detect context exhaustion and enable graceful session handoff with automated resumption.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Project overview and status |
| [Epics](#epics) | Strategic work items |
| [Decisions](#decisions) | Key decisions |
| [History](#history) | Change log |

---

## Summary

| Field | Value |
|-------|-------|
| Project | PROJ-004-context-resilience |
| Status | IN_PROGRESS |
| Created | 2026-02-19 |

---

## Epics

| ID | Title | Status | Priority |
|----|-------|--------|----------|
| [EPIC-001](./work/EPIC-001-context-resilience/EPIC-001-context-resilience.md) | Context Resilience | in_progress | high |

> Features, Enablers, Spikes, and Tasks are tracked within the Epic and its children.

---

## Decisions

| ID | Title | Status | Impact |
|----|-------|--------|--------|
| [DEC-001](./work/EPIC-001-context-resilience/FEAT-001-context-detection/DEC-001-cli-first-architecture.md) | CLI-First Hook Architecture & Context Monitoring Bounded Context | accepted | critical |

---

## History

| Date | Author | Change |
|------|--------|--------|
| 2026-02-19 | Claude | PROJ-004 created. Context resilience initiative to address session exhaustion during multi-orchestration runs. |
| 2026-02-19 | Claude | SPIKE-001 orchestration started. Workflow ID: spike001-ctxres-20260219-001. Phase 1 (Inventory Existing Mechanisms) dispatched. |
| 2026-02-19 | Claude | SPIKE-001 complete. 7 phases executed, 2 quality gates passed (QG-1: 0.93, QG-2: 0.92). Synthesis produced with 14 follow-up work items. SPIKE-001 status: done. Recommend proceeding with FEAT-001 implementation. |
| 2026-02-19 | Claude | SPIKE-002 created and started. Supplementary spike to address SPIKE-001 gap: Jerry CLI infrastructure (TokenCounter, session lifecycle, config system, enforcement engines) was not factored into context resilience design. SPIKE-002 will revise follow-up work items with CLI-integrated approach. Workflow ID: spike002-cli-integration-20260219-001. |
| 2026-02-19 | Claude | SPIKE-002 complete. 4 phases + 1 quality gate executed (QG-1: 0.94 PASS). 14 SPIKE-001 items consolidated to 10 revised CWIs (CWI-00 through CWI-09). Key addition: CWI-00 FileSystemSessionRepository (P0 enabler) per user feedback. ADR-SPIKE002-001 proposes two-phase CLI-integrated architecture. Estimated effort: 19.5-28.5 hours (22-23% reduction). SPIKE-002 status: done. |
| 2026-02-19 | Claude | SPIKE-002 Phase 5 (architecture revision): User identified ADR-SPIKE002-001 chose wrong alternative. DISC-001 documented hook-CLI violations. DEC-001 captured 4 corrective decisions. ADR-SPIKE002-002 produced (QG-2 PASS 0.92). 12 revised CWIs (CWI-00 through CWI-11). |
| 2026-02-19 | User | DEC-001 accepted: 4 architectural decisions approved (D-001 CLI-first hooks, D-002 proper bounded context, D-003 jerry hooks namespace, D-004 enforcement debt tracked separately). |
| 2026-02-19 | Claude | 11 worktracker entity files created under FEAT-001: EN-001 through EN-007 (enablers), ST-001 through ST-003 (stories), SPIKE-003 (spike). All with BDD Gherkin acceptance criteria. Implementation ready. |
| 2026-02-20 | Claude | FEAT-001 implementation workflow complete (feat001-impl-20260220-001). 6 phases, 11 agents, 3 quality gates all PASSED (0.927, 0.922, 0.922). ST-003 validation: 20 PASS, 5 PARTIAL, 1 DEFERRED. |
| 2026-02-20 | Claude | EN-008 (Context Resilience Hardening) created with 5 child tasks (TASK-001 through TASK-005) to address the 5 PARTIAL acceptance criteria items from ST-003 validation report. |
| 2026-02-20 | Claude | TASK-006 added to EN-008: context window size hardcoded to 200K, config key disconnected. Different subscriptions + models have different windows. Configuration-first approach required since subscription tier cannot be auto-detected. |
