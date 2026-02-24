# EN-004: Skill Registry Updates

> **Type:** enabler
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Enabler Type:** infrastructure
> **Created:** 2026-02-20
> **Completed:** 2026-02-20
> **Parent:** FEAT-028-mcp-tool-integration
> **Owner:** Claude
> **Effort:** 2

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description |
| [Technical Approach](#technical-approach) | Implementation approach |
| [Changes](#changes) | Detailed change list |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [History](#history) | Change log |

---

## Summary

Update SKILL.md files, AGENTS.md, and TOOL_REGISTRY.yaml to reflect MCP tool additions across the framework.

## Technical Approach

Completed as part of parent feature. See evidence below.

---

## Changes

**SKILL.md updates (4 files):**
- `skills/problem-solving/SKILL.md` — Added Context7 + Memory-Keeper tools
- `skills/nasa-se/SKILL.md` — Added Context7 + Memory-Keeper tools
- `skills/orchestration/SKILL.md` — Added Memory-Keeper tools
- `skills/transcript/SKILL.md` — Added Memory-Keeper tools

**AGENTS.md:**
- Added "MCP Tool Access" section with Context7 and Memory-Keeper agent matrices
- Added to navigation table

**TOOL_REGISTRY.yaml:**
- Expanded `mcp__memory-keeper__context_*` wildcard to 5 individual tool definitions (store, retrieve, search, list, delete)
- Updated `agent_permissions` for 9 agents (nse-architecture, nse-explorer, nse-requirements, ps-architect, orch-planner, orch-tracker, orch-synthesizer)
- Updated `metrics` section (agents_with_context7: 7, agents_with_memory_keeper: 7)
- Updated `categories.mcp.tools` with individual tool names

## Acceptance Criteria

| ID | Criterion | Status |
|----|-----------|--------|
| AC-1 | 4 SKILL.md files have MCP tools in `allowed-tools` | PASS |
| AC-2 | AGENTS.md has MCP Tool Access section | PASS |
| AC-3 | TOOL_REGISTRY.yaml has individual Memory-Keeper tool definitions | PASS |
| AC-4 | TOOL_REGISTRY.yaml agent_permissions match agent definitions | PASS |

## History

| Date | Author | Event |
|------|--------|-------|
| 2026-02-20 | Claude | Created. All registry files updated consistently. |
