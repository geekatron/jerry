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
| — | — | — | — |

---

## History

| Date | Author | Change |
|------|--------|--------|
| 2026-02-19 | Claude | PROJ-004 created. Context resilience initiative to address session exhaustion during multi-orchestration runs. |
| 2026-02-19 | Claude | SPIKE-001 orchestration started. Workflow ID: spike001-ctxres-20260219-001. Phase 1 (Inventory Existing Mechanisms) dispatched. |
| 2026-02-19 | Claude | SPIKE-001 complete. 7 phases executed, 2 quality gates passed (QG-1: 0.93, QG-2: 0.92). Synthesis produced with 14 follow-up work items. SPIKE-001 status: done. Recommend proceeding with FEAT-001 implementation. |
| 2026-02-19 | Claude | SPIKE-002 created and started. Supplementary spike to address SPIKE-001 gap: Jerry CLI infrastructure (TokenCounter, session lifecycle, config system, enforcement engines) was not factored into context resilience design. SPIKE-002 will revise follow-up work items with CLI-integrated approach. Workflow ID: spike002-cli-integration-20260219-001. |
| 2026-02-19 | Claude | SPIKE-002 complete. 4 phases + 1 quality gate executed (QG-1: 0.94 PASS). 14 SPIKE-001 items consolidated to 10 revised CWIs (CWI-00 through CWI-09). Key addition: CWI-00 FileSystemSessionRepository (P0 enabler) per user feedback. ADR-SPIKE002-001 proposes two-phase CLI-integrated architecture. Estimated effort: 19.5-28.5 hours (22-23% reduction). SPIKE-002 status: done. |
