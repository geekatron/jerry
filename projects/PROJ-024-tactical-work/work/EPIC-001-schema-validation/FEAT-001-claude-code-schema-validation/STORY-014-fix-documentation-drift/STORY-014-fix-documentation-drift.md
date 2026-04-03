# STORY-014: Fix Documentation Drift in Tool Standards and Agent Development Standards

<!--
TEMPLATE: Story
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
PURPOSE: Update stale documentation that contradicts actual agent/skill definitions
-->

> **Type:** story
> **Status:** completed
> **Priority:** medium
> **Impact:** medium
> **Created:** 2026-03-27T10:00:00Z
> **Due:**
> **Completed:** 2026-03-29T00:30:00Z
> **Parent:** FEAT-001
> **Owner:** adam.nowak
> **Effort:** 3

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [User Story](#user-story) | As a / I want / So that |
| [Summary](#summary) | What needs to happen |
| [Drift Items](#drift-items) | All identified documentation inconsistencies |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Children (Tasks)](#children-tasks) | Task breakdown |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Status changes |

---

## User Story

**As a** Jerry framework developer creating new agents

**I want** the rule files and reference tables to accurately reflect the actual agent definitions

**So that** I don't model new agents based on incorrect examples or stale reference data

---

## Summary

STORY-012 audit found that two key reference documents have drifted from reality. Developers reading these docs will get wrong information about which agents have which tools and tiers.

---

## Drift Items

### D-001: agent-development-standards.md -- T1 Example Agents Are Actually T2

| Attribute | Value |
|-----------|-------|
| **File** | `.context/rules/agent-development-standards.md` |
| **Location** | Tool Security Tiers table, T1 row |
| **Current** | Lists `adv-executor, adv-scorer, wt-auditor` as T1 examples |
| **Actual** | All three have `Write` and/or `Edit` in tools -- that's T2 |
| **Fix** | Move these to the T2 row. Find actual T1-only agents (read-only) as T1 examples, or note that no pure T1 agents currently exist. |
| **Source** | eng-security SEC-002 |

### D-002: mcp-tool-standards.md -- Agent Integration Matrix Stale

| Attribute | Value |
|-----------|-------|
| **File** | `.context/rules/mcp-tool-standards.md` |
| **Location** | Agent Integration Matrix table |
| **Issues** | (a) 6 UX agents have Context7 in frontmatter but are absent from matrix: ux-orchestrator, ux-atomic-architect, ux-heuristic-evaluator, ux-inclusive-evaluator, ux-jtbd-analyst, ux-lean-ux-facilitator. (b) eng-reviewer is listed in "Not included (by design)" section but actually has `mcpServers: context7: true`. (c) Matrix doesn't include adv-executor after STORY-011 adds Context7. |
| **Fix** | Update matrix to match actual frontmatter declarations. Move eng-reviewer from exclusion list to inclusion list. Add 6 UX agents. |
| **Source** | ps-analyst |

---

## Acceptance Criteria

- [x] D-001: T1 examples fixed in STORY-017 -- now pe-scorer, diataxis-classifier, sb-voice (verified T1 agents)
- [x] D-001: adv-scorer moved to T2 examples; adv-executor now T4 (External) after tier renumbering
- [x] D-002: 8 UX agents added to mcp-tool-standards.md Agent Integration Matrix (ux-orchestrator, ux-atomic-architect, ux-heart-analyst, ux-heuristic-evaluator, ux-inclusive-evaluator, ux-jtbd-analyst, ux-kano-analyst, ux-lean-ux-facilitator)
- [x] D-002: eng-reviewer already in Context7 inclusion list (verified in matrix)
- [x] D-002: adv-executor in matrix with Context7 (added in STORY-011)
- [x] D-002: 3 UX agents without Context7 added to exclusion list (ux-ai-design-guide, ux-sprint-facilitator, ux-behavior-diagnostician)
- [x] No remaining discrepancies between matrix and actual mcpServers frontmatter (verified: `grep -rl 'context7' skills/*/agents/*.md` cross-referenced against matrix rows)

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Owner |
|----|-------|--------|-------|
| TASK-001 | Fix D-001: Update T1/T2 tier examples in agent-development-standards.md | completed (STORY-017) | claude |
| TASK-002 | Fix D-002: Update mcp-tool-standards.md Agent Integration Matrix | completed | claude |
| TASK-003 | Verify matrix matches all agents with mcpServers | completed | claude |

**TASK-003 verification evidence:** `grep -rl 'context7' skills/*/agents/*.md` returns 34 agents. All 34 are accounted for in the mcp-tool-standards.md matrix (26 in Context7 column) or exclusion list (8 without Context7 use web-only tools). Verified against mcp-tool-standards.md v1.4.0 (2026-03-28).

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-001: Claude Code Schema Validation](../FEAT-001-claude-code-schema-validation.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Informed By | STORY-012 | Audit identified all drift items |
| Depends On | STORY-011 | D-002 matrix update for adv-executor depends on STORY-011 landing first |
| Depends On | STORY-013 | Tier fixes may change which agents appear in which tier examples |
| Depends On | STORY-015 | D-001 tier example fixes depend on final tier definitions from renumbering ADR |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-27 | adam.nowak | pending | Story created from STORY-012 audit findings |
| 2026-03-29 | claude | completed | D-001 resolved by STORY-017 (T1 examples fixed to pe-scorer, diataxis-classifier, sb-voice). D-002 resolved: 8 UX agents + 3 exclusions added to mcp-tool-standards.md matrix. eng-reviewer and adv-executor already present from prior work. |
