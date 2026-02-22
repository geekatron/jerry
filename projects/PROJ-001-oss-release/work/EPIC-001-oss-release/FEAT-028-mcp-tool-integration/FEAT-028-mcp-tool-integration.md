# FEAT-028: MCP Tool Integration (Context7 + Memory-Keeper)

> **Type:** feature
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-20
> **Due:** --
> **Completed:** 2026-02-20
> **Parent:** EPIC-001-oss-release
> **Owner:** Claude

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this feature delivers |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Children Stories/Enablers](#children-storiesenablers) | Child work items |
| [Enablers](#enablers) | Implementation work items |
| [Progress Summary](#progress-summary) | Tracking |
| [History](#history) | Change log |

---

## Summary

Add governance rules and agent definitions for proactive MCP tool usage across the Jerry Framework. Context7 (documentation lookup) was partially integrated in 5 PS agents but not governed by rules. Memory-Keeper (cross-session persistence) was installed but zero agents referenced it.

**Key Deliverables:**
- `.context/rules/mcp-tool-standards.md` — MCP governance rule (SSOT)
- Context7 tools added to 2 NASA-SE agents (nse-explorer, nse-architecture)
- Memory-Keeper tools added to 7 agents across orchestration, problem-solving, nasa-se, and transcript skills
- SKILL.md, AGENTS.md, TOOL_REGISTRY.yaml updated with MCP tool references

**Criticality:** C3 (touches `.context/rules/` per AE-002)

---

## Acceptance Criteria

| ID | Criterion | Status |
|----|-----------|--------|
| AC-1 | `.context/rules/mcp-tool-standards.md` exists with Context7 + Memory-Keeper governance | PASS |
| AC-2 | Rule file accessible via `.claude/rules/` symlink (same inode) | PASS |
| AC-3 | 7 agents have `mcp__context7__` tools (5 PS + 2 NSE) | PASS |
| AC-4 | 7 agents have `mcp__memory-keeper__` tools (3 orch + ps-architect + nse-requirements + 2 transcript) | PASS |
| AC-5 | 4 SKILL.md files include MCP tools in `allowed-tools` frontmatter | PASS |
| AC-6 | AGENTS.md has MCP Tool Access section with agent-to-tool matrix | PASS |
| AC-7 | TOOL_REGISTRY.yaml has correct Memory-Keeper tool names and updated agent_permissions | PASS |

---

## Children Stories/Enablers

See [Enablers](#enablers) below for the full decomposition.

---

## Enablers

| ID | Title | Status | Priority | Effort |
|----|-------|--------|----------|--------|
| EN-001 | MCP Governance Rule File | done | high | 2 |
| EN-002 | Context7 Agent Updates | done | high | 2 |
| EN-003 | Memory-Keeper Agent Updates | done | high | 3 |
| EN-004 | Skill Registry Updates | done | high | 2 |
| EN-005 | Verification + Quality Gate | done | high | 2 |

### Enabler Links

- [EN-001: MCP Governance Rule File](./EN-001-mcp-governance-rule.md)
- [EN-002: Context7 Agent Updates](./EN-002-context7-agent-updates.md)
- [EN-003: Memory-Keeper Agent Updates](./EN-003-memory-keeper-agent-updates.md)
- [EN-004: Skill Registry Updates](./EN-004-skill-registry-updates.md)
- [EN-005: Verification + Quality Gate](./EN-005-verification-quality-gate.md)

### Execution Order

```
EN-001 (Rule file)           <- Foundation
    |
EN-002 (Context7) + EN-003 (Memory-Keeper)  <- Parallel agent updates
    |
EN-004 (Registry updates)   <- Consolidation
    |
EN-005 (Verification + QG)  <- Quality gate
```

---

## Progress Summary

```
[##########] 100% (5/5 enablers, 11/11 effort points)
```

---

## History

| Date | Author | Event |
|------|--------|-------|
| 2026-02-20 | Claude | FEAT-028 created. 5 enablers (EN-001 through EN-005), 11 effort points. |
| 2026-02-20 | Claude | EN-001 DONE: `.context/rules/mcp-tool-standards.md` created (~90 lines). Context7 triggers, Memory-Keeper triggers, canonical tool names, agent integration matrix. Symlink auto-propagates to `.claude/rules/`. |
| 2026-02-20 | Claude | EN-002 DONE: Context7 tools added to nse-explorer and nse-architecture. YAML frontmatter + `<context7_integration>` sections following ps-researcher SOP-CB.6 pattern. |
| 2026-02-20 | Claude | EN-003 DONE: Memory-Keeper tools added to 7 agents (orch-planner, orch-tracker, orch-synthesizer, ps-architect, nse-requirements, ts-parser, ts-extractor). YAML frontmatter + `<memory_keeper_integration>` sections with key patterns. |
| 2026-02-20 | Claude | EN-004 DONE: 4 SKILL.md files updated (problem-solving, nasa-se, orchestration, transcript). AGENTS.md: MCP Tool Access section with Context7 + Memory-Keeper matrices. TOOL_REGISTRY.yaml: Memory-Keeper tools expanded from wildcard to 5 individual tools, agent_permissions updated for all 9 agents, metrics updated. |
| 2026-02-20 | Claude | EN-005 DONE: Grep verification (7 Context7, 7 Memory-Keeper — both match expected). Inode verification (same inode for .context/rules/ and .claude/rules/). Test suite: 3299 passed, 0 failed. |
