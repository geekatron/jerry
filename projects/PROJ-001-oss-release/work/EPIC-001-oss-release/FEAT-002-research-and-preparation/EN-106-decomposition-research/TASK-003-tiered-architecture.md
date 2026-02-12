# TASK-003: Tiered Architecture Design

<!--
TEMPLATE: Task
VERSION: 0.1.0
-->

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Frontmatter](#frontmatter) | Task metadata |
| [Description](#description) | Tiered architecture and token distribution |
| [History](#history) | Change log |

---

## Frontmatter

```yaml
id: "TASK-003"
work_type: TASK
title: "Tiered Architecture Design"
status: DONE
priority: CRITICAL
assignee: "ps-researcher-decomposition"
parent_id: "EN-106"
effort: 1
activity: RESEARCH
```

---

## Description

Design tiered loading architecture for Jerry context optimization.

### Tiered Architecture (Jerry-Specific)

| Tier | Location | Loading | Content | Lines |
|------|----------|---------|---------|-------|
| Tier 1 | CLAUDE.md | Always | Identity, navigation, constraints | ~75 |
| Tier 2 | .claude/rules/ | Auto-loaded | Standards, architecture | ~500 |
| Tier 3 | skills/ | On-demand | Worktracker, PS, NASA-SE | ~1500+ |
| Tier 4 | docs/ | Explicit | Reference, governance | Unlimited |

### Token Distribution

| Tier | Current | After Optimization |
|------|---------|-------------------|
| Tier 1 | ~10,000 | ~3,500 |
| Tier 2 | ~3,000 | ~3,000 (no change) |
| Tier 3 | 0 (inline) | 0 (on demand) |
| **Total at Start** | ~13,000 | ~6,500 |

### Acceptance Criteria

- [x] Tiered architecture designed
- [x] Content allocation defined
- [x] Token reduction calculated

### Related Items

- Parent: [EN-106](./EN-106-decomposition-research.md)
- Output: [decomposition-best-practices.md](../orchestration/oss-release-20260131-001/ps/phase-0/ps-researcher-decomposition/decomposition-best-practices.md)
- Plan: [PLAN-CLAUDE-MD-OPTIMIZATION.md](../orchestration/oss-release-20260131-001/plans/PLAN-CLAUDE-MD-OPTIMIZATION.md)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-01 | DONE | Design complete |
