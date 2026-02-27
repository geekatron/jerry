# Context7 Research Extraction Summary

> Key entities, relationships, and decisions extracted from Context7 namespace research.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Extracted Entities](#extracted-entities) | Named items discovered during research |
| [Relationships](#relationships) | How entities connect |
| [Decision Points](#decision-points) | Choices requiring resolution |
| [Bug Candidates](#bug-candidates) | Potential new bug filings |

---

## Extracted Entities

### Configuration Entities

| Entity | Type | Location | Status |
|--------|------|----------|--------|
| Context7 Plugin Registration | Config | `.claude/settings.json` `enabledPlugins` | Active (dual-registered) |
| Context7 MCP Server Permissions | Config | `.claude/settings.local.json` lines 24-29 | Active (defensive dual-prefix) |
| Memory-Keeper MCP Server | Config | `.claude/settings.local.json` lines 19-23 | Active (wrong tool names per BUG-001) |
| TOOL_REGISTRY.yaml | Governance | `TOOL_REGISTRY.yaml` | References wrong `mcp__context7__` prefix |

### Namespace Entities

| Entity | Formula | Example |
|--------|---------|---------|
| Plugin prefix (Formula B) | `mcp__plugin_{plugin}_{server}__{tool}` | `mcp__plugin_context7_context7__resolve-library-id` |
| Manual MCP prefix (Formula A) | `mcp__{server}__{tool}` | `mcp__context7__resolve-library-id` |
| Memory-Keeper prefix | `mcp__{server}__{tool}` | `mcp__memory-keeper__context_save` |

### Affected File Categories

| Category | Count | Pattern |
|----------|-------|---------|
| Agent definitions with Context7 `tools` | 28 categories (from Integration Matrix) | `skills/*/agents/*.md` |
| Governance files (mcp-tool-standards.md) | 1 | `.context/rules/mcp-tool-standards.md` |
| Permission settings | 2 | `.claude/settings.json`, `.claude/settings.local.json` |
| Tool registry | 1 | `TOOL_REGISTRY.yaml` |

---

## Relationships

```
Plugin Registration (.claude/settings.json)
  └── Produces: mcp__plugin_context7_context7__* namespace
       └── NOT matched by: mcp__context7__* permissions

Manual MCP Server (~/.claude/settings.json or `claude mcp add`)
  └── Produces: mcp__context7__* namespace
       └── Matched by: mcp__context7__* permissions
       └── Referenced by: Agent definitions, TOOL_REGISTRY.yaml, mcp-tool-standards.md

settings.local.json (defensive dual-listing)
  └── Grants: Both mcp__context7__* AND mcp__plugin_context7_context7__*
  └── Purpose: Session-level workaround, does not fix agent-level tools frontmatter
```

---

## Decision Points

| ID | Decision | Options | Status |
|----|----------|---------|--------|
| DP-01 | Context7 registration method | (A) Manual user-scoped MCP, (B) Update agents to plugin prefix, (C) Keep dual | Recommended: A |
| DP-02 | Permission wildcard syntax | Functional in current Claude Code version? | Unverified |
| DP-03 | Memory-Keeper tool name alignment | Fix via BUG-001 or combined fix | Pending BUG-001 |
| DP-04 | `allowed_tools` field in settings.json | Legacy/functional/ignored? | Unresolved |

---

## Bug Candidates

| ID | Title | Source | Filed? |
|----|-------|--------|--------|
| BUG-001 | Memory-Keeper tool name mismatch | Prior audit | Yes (GitHub #111) |
| BUG-002 (candidate) | Context7 dual-namespace tool resolution failure | This research | Not yet filed |

---

*Extracted from: context7-permission-model.md, context7-plugin-architecture.md*
*Extraction date: 2026-02-26*
*C4 adversarial tournament: 0.823 / 0.837 baseline scores (REVISE)*
