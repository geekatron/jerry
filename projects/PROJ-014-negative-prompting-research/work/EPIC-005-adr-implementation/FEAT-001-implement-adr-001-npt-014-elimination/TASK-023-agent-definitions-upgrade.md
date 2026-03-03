# TASK-023: Phase 3: Agent definitions — upgrade forbidden_actions in skills/*/agents/

> **Type:** task
> **Status:** completed
> **Priority:** high
> **Created:** 2026-02-28
> **Completed:** 2026-02-28
> **Parent:** FEAT-001
> **Owner:** Claude
> **Activity:** DEVELOPMENT

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description |
| [Content](#content) | Description and acceptance criteria |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Status changes |

---

## Summary

Upgrade forbidden_actions sections in 28 agent definition files (Phase 3A batch) plus 3 individual NPT-014 instances (Phase 3B) to structured negation with agent-specific consequence and alternative text.

---

## Content

### Description

Upgrade forbidden_actions sections in 28 agent definition files (Phase 3A batch) plus 3 individual NPT-014 instances outside forbidden_actions blocks (Phase 3B). Each agent's P-003, P-020, and P-022 lines upgraded from bare prohibitions to structured negation with agent-specific consequence and alternative text using the Template B lookup tables.

### Acceptance Criteria

- [x] Phase 3A: 28 agent files upgraded via 5 parallel background agents
- [x] Phase 3B: 3 individual instances upgraded (ps-critic, ts-extractor, orch-planner)
- [x] Each agent has customized P-022 consequence text per lookup table
- [x] Each agent has customized P-002 output type per lookup table
- [x] Domain-specific forbidden action lines added per lookup table

### Implementation Notes

Phase 3A executed via 5 parallel background agents grouped by skill prefix: ps-* (9 files), orch-* (3 files), nse-* (8 files), wt-* (3 files), ts-* (5 files). Each agent received the full Template B specification with lookup tables for per-agent customization. Phase 3B had 3 instances, but orch-planner.md was already handled by the orch-* background agent, so only 2 manual edits were needed.

### Related Items

- Parent: [FEAT-001: Implement ADR-001](./FEAT-001-implement-adr-001-npt-014-elimination.md)
- Depends On: [TASK-021: Baseline capture](./TASK-021-baseline-capture.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| ps-* agents (9 files) | Agent definition edits | `skills/problem-solving/agents/ps-*.md` |
| orch-* agents (3 files) | Agent definition edits | `skills/orchestration/agents/orch-*.md` |
| nse-* agents (8 files) | Agent definition edits | `skills/nasa-se/agents/nse-*.md` |
| wt-* agents (3 files) | Agent definition edits | `skills/worktracker/agents/wt-*.md` |
| ts-* agents (5 files) | Agent definition edits | `skills/transcript/agents/ts-*.md` |

### Verification

- [x] Acceptance criteria verified
- [x] 28 agent files upgraded (Phase 3A) + 2 individual edits (Phase 3B)
- [x] Committed in 47451ef6

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-28 | Created | Initial creation |
| 2026-02-28 | completed | 28 agent files + 2 individual instances upgraded |
