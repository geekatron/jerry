# Memory-Keeper Tool Name Audit

> Research report: actual MCP tool names vs. Jerry Framework references, with three-layer naming architecture.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Root cause and impact |
| [Three-Layer Tool Naming Architecture](#three-layer-tool-naming-architecture) | MCP Server vs. Claude Code Runtime vs. Jerry Source Code |
| [What to Reference Where](#what-to-reference-where) | Quick-reference guide for each file type |
| [Memory-Keeper: Complete Name Resolution](#memory-keeper-complete-name-resolution) | All 38 tools across all three layers |
| [Context7: Complete Name Resolution](#context7-complete-name-resolution) | Both tools across all three layers |
| [Tool Name Mapping (Wrong vs. Correct)](#tool-name-mapping-wrong-vs-correct) | Current wrong names and their corrections |
| [Tool Profiles](#tool-profiles) | Minimal, standard, full tool sets |
| [Affected Files](#affected-files) | Every file referencing wrong names |
| [Remediation Plan](#remediation-plan) | Fix steps |
| [Sources](#sources) | Research sources |

---

## Summary

**Root Cause:** The Jerry Framework governance files, agent definitions, TOOL_REGISTRY.yaml, and permission settings all reference memory-keeper tool names that do not exist. The framework was built against assumed tool names (`store`, `retrieve`, `search`, `list`, `delete`) that never matched the actual MCP server API.

**Actual server:** [mkreyman/mcp-memory-keeper](https://github.com/mkreyman/mcp-memory-keeper) (npm: `mcp-memory-keeper`)

**Impact:** MCP-002 (HARD rule) mandates memory-keeper usage at phase boundaries, but the behavioral instructions reference nonexistent tool names. This causes:
1. Agents cannot follow the instructions because tool names don't resolve
2. L2 reinject markers reference dead tool names
3. Permission allowlist in `settings.local.json` grants access to nonexistent tools
4. No memory-keeper usage occurs despite rules mandating it

**Secondary finding:** Context7 tool name references also have inconsistencies between MCP server naming (`mcp__context7__`) and Plugin naming (`mcp__plugin_context7_context7__`), though the permission allowlist wildcards cover both.

---

## Three-Layer Tool Naming Architecture

Tool names exist in three distinct layers. Each layer has a different naming convention, and Jerry governance files MUST reference the correct layer.

```
Layer 1: MCP Server Package            Layer 2: Claude Code Runtime            Layer 3: Jerry Source Code
(npm source code)                      (what the LLM sees at runtime)          (governance files reference)

context_save                    -->    mcp__memory-keeper__context_save   -->  mcp__memory-keeper__context_save
                                       ^                                      ^
                                       |                                      |
                                       Prefix added by Claude Code            MUST match Layer 2 exactly
```

### Layer 1: MCP Server Package (Raw Tool Names)

These are the tool names defined in the npm package source code. You will see these in the mcp-memory-keeper GitHub repo and npm documentation.

**Naming convention:** `context_{action}` (e.g., `context_save`, `context_get`, `context_search`)

**Where you see Layer 1 names:**
- npm package documentation
- GitHub README
- MCP server source code
- MCP protocol messages (internal)

**You do NOT reference Layer 1 names in Jerry governance files.**

### Layer 2: Claude Code Runtime (Prefixed Tool Names)

Claude Code adds a prefix to every MCP tool based on how the tool provider is configured. The prefix formula differs between MCP Servers and Plugins.

**MCP Server prefix formula:** `mcp__<server-name>__<tool-name>`

- `<server-name>` comes from the key in the `mcpServers` config object (e.g., `memory-keeper` from `~/.claude/.claude.json`)
- `<tool-name>` is the Layer 1 raw tool name

**Plugin prefix formula:** `mcp__plugin_<registry>_<plugin-name>__<tool-name>`

- `<registry>` is the plugin marketplace (e.g., `context7`)
- `<plugin-name>` is the plugin identifier (e.g., `context7`)

**Current configuration:**

| Tool Provider | Type | Config Location | Prefix |
|---------------|------|-----------------|--------|
| memory-keeper | **MCP Server** | `~/.claude/.claude.json` → `mcpServers.memory-keeper` | `mcp__memory-keeper__` |
| Context7 | **Plugin** | `~/.claude/settings.json` → `enabledPlugins["context7@claude-plugins-official"]` | `mcp__plugin_context7_context7__` |

**Permission wildcard behavior** ([Claude Code Permissions Docs](https://code.claude.com/docs/en/permissions)):
- `mcp__memory-keeper` (bare server name) — allows ALL tools from the `memory-keeper` MCP server
- `mcp__memory-keeper__*` (wildcard) — equivalent, also allows all tools from `memory-keeper`
- `mcp__memory-keeper__context_save` (specific) — allows only that one tool
- **Wildcards are prefix-scoped:** `mcp__context7__*` only covers the `mcp__context7__` prefix. It does NOT cover `mcp__plugin_context7_context7__*`. These are separate namespaces. Both entries are needed in the permission allowlist if Context7 might be configured as either an MCP server or a Plugin. ([GitHub #2928](https://github.com/anthropics/claude-code/issues/2928), [GitHub #3107](https://github.com/anthropics/claude-code/issues/3107))
- **Plugin naming convention:** `mcp__plugin_<plugin-name>_<server-name>__<tool-name>` ([GitHub #20983](https://github.com/anthropics/claude-code/issues/20983))

**Where you see Layer 2 names:**
- Claude Code's tool list shown to the LLM at runtime
- Tool call invocations in conversation logs
- Permission allowlists in `settings.local.json`

### Layer 3: Jerry Source Code (Governance References)

These are the names that appear in Jerry's governance files, agent definitions, TOOL_REGISTRY.yaml, and MCP standards. **Layer 3 names MUST exactly match Layer 2 names** because the LLM uses Layer 2 names to invoke tools.

**Where you write Layer 3 names:**
- `.context/rules/mcp-tool-standards.md` (Canonical Tool Names table)
- `TOOL_REGISTRY.yaml` (tool definitions and agent permissions)
- Agent `.md` files (frontmatter `tools`/`mcpServers` fields, methodology references)
- Agent `.governance.yaml` files (`capabilities.allowed_tools`)
- Skill `SKILL.md` files (MCP integration sections)
- `.claude/settings.local.json` (permission allowlist)
- L2-REINJECT markers (behavioral reinforcement)

---

## What to Reference Where

### Quick Reference Table

| File Type | Layer to Use | Example Name (Memory-Keeper) | Example Name (Context7) |
|-----------|-------------|------------------------------|-------------------------|
| `mcp-tool-standards.md` Canonical Tool Names | **Layer 2** | `mcp__memory-keeper__context_save` | `mcp__plugin_context7_context7__resolve-library-id` |
| `TOOL_REGISTRY.yaml` tool definitions | **Layer 2** | `mcp__memory-keeper__context_save` | `mcp__plugin_context7_context7__resolve-library-id` |
| Agent `.md` frontmatter (`mcpServers`) | **Server name only** | `memory-keeper` | `plugin:context7:context7` |
| Agent `.md` methodology body | **Layer 2** | `mcp__memory-keeper__context_save` | `mcp__plugin_context7_context7__resolve-library-id` |
| Agent `.governance.yaml` `allowed_tools` | **Layer 2** | `mcp__memory-keeper__context_save` | `mcp__plugin_context7_context7__resolve-library-id` |
| `settings.local.json` permission allowlist | **Layer 2** (wildcards OK) | `mcp__memory-keeper__*` | `mcp__plugin_context7_context7__*` |
| L2-REINJECT markers | **Layer 2** (short names OK for token budget) | `context_save` with context | `resolve-library-id` with context |
| Skill `SKILL.md` files | **Layer 2** | `mcp__memory-keeper__context_save` | `mcp__plugin_context7_context7__resolve-library-id` |
| npm/GitHub documentation references | **Layer 1** | `context_save` | `resolve-library-id` |

### Settings.local.json Allowlist Guidance

The permission allowlist in `settings.local.json` uses Layer 2 names. **Wildcards are supported and recommended:**

```json
{
  "permissions": {
    "allow": [
      "mcp__memory-keeper__*",
      "mcp__plugin_context7_context7__*"
    ]
  }
}
```

**Current problem:** `settings.local.json` has both the wildcard `mcp__memory-keeper__*` (correct, catches all tools) AND specific wrong tool names (`mcp__memory-keeper__store`, `retrieve`, `list`, `delete`, `search`). The specific wrong entries are redundant (the wildcard covers everything) but add noise and suggest incorrect tool names to anyone reading the file.

**Context7 note:** `settings.local.json` has both `mcp__context7__*` (MCP server prefix) and `mcp__plugin_context7_context7__*` (Plugin prefix). These are **separate namespaces** per Claude Code's prefix-scoped wildcard matching ([source](https://code.claude.com/docs/en/permissions)). Both entries are a **defensive belt-and-suspenders** approach: if Context7 is configured as a Plugin (current), the plugin-prefix wildcard is active; if it were reconfigured as an MCP server, the server-prefix wildcard would be active. Both can be kept. The individual tool entries (`resolve-library-id`, `query-docs`) under each wildcard are redundant and can be removed.

---

## Memory-Keeper: Complete Name Resolution

### Minimal Profile (8 tools)

| Layer 1 (Package) | Layer 2 (Runtime) | Description |
|--------------------|-------------------|-------------|
| `context_session_start` | `mcp__memory-keeper__context_session_start` | Initialize new session |
| `context_save` | `mcp__memory-keeper__context_save` | Store context items |
| `context_get` | `mcp__memory-keeper__context_get` | Retrieve by key/category/session |
| `context_search` | `mcp__memory-keeper__context_search` | Full-text search |
| `context_status` | `mcp__memory-keeper__context_status` | Session status and stats |
| `context_checkpoint` | `mcp__memory-keeper__context_checkpoint` | Create named snapshots |
| `context_restore_checkpoint` | `mcp__memory-keeper__context_restore_checkpoint` | Restore snapshots |
| `context_prepare_compaction` | `mcp__memory-keeper__context_prepare_compaction` | Auto-save before compaction |

### Standard Profile (adds 14 tools = 22 total)

| Layer 1 (Package) | Layer 2 (Runtime) | Description |
|--------------------|-------------------|-------------|
| `context_set_project_dir` | `mcp__memory-keeper__context_set_project_dir` | Configure git tracking |
| `context_session_list` | `mcp__memory-keeper__context_session_list` | List recent sessions |
| `context_cache_file` | `mcp__memory-keeper__context_cache_file` | Cache file with hash |
| `context_file_changed` | `mcp__memory-keeper__context_file_changed` | Check file changes |
| `context_batch_save` | `mcp__memory-keeper__context_batch_save` | Atomic multi-save |
| `context_batch_update` | `mcp__memory-keeper__context_batch_update` | Atomic multi-update |
| `context_batch_delete` | `mcp__memory-keeper__context_batch_delete` | Atomic multi-delete |
| `context_reassign_channel` | `mcp__memory-keeper__context_reassign_channel` | Move items between channels |
| `context_link` | `mcp__memory-keeper__context_link` | Create relationships |
| `context_get_related` | `mcp__memory-keeper__context_get_related` | Get related items |
| `context_export` | `mcp__memory-keeper__context_export` | Export session data |
| `context_import` | `mcp__memory-keeper__context_import` | Import session data |
| `context_git_commit` | `mcp__memory-keeper__context_git_commit` | Commit with context save |
| `context_summarize` | `mcp__memory-keeper__context_summarize` | AI-friendly summary |

### Full Profile (adds 16 tools = 38 total)

| Layer 1 (Package) | Layer 2 (Runtime) | Description |
|--------------------|-------------------|-------------|
| `context_watch` | `mcp__memory-keeper__context_watch` | Real-time monitoring |
| `context_semantic_search` | `mcp__memory-keeper__context_semantic_search` | Natural language search |
| `context_delegate` | `mcp__memory-keeper__context_delegate` | Delegate analysis tasks |
| `context_branch_session` | `mcp__memory-keeper__context_branch_session` | Branch for alternatives |
| `context_merge_sessions` | `mcp__memory-keeper__context_merge_sessions` | Merge sessions |
| `context_journal_entry` | `mcp__memory-keeper__context_journal_entry` | Timestamped journal |
| `context_timeline` | `mcp__memory-keeper__context_timeline` | Activity timeline |
| `context_compress` | `mcp__memory-keeper__context_compress` | Compress old context |
| `context_integrate_tool` | `mcp__memory-keeper__context_integrate_tool` | Track MCP events |
| `context_diff` | `mcp__memory-keeper__context_diff` | Changes since timestamp |
| `context_list_channels` | `mcp__memory-keeper__context_list_channels` | List channels |
| `context_channel_stats` | `mcp__memory-keeper__context_channel_stats` | Channel statistics |
| `context_analyze` | `mcp__memory-keeper__context_analyze` | Extract entities |
| `context_find_related` | `mcp__memory-keeper__context_find_related` | Find related entities |
| `context_visualize` | `mcp__memory-keeper__context_visualize` | Knowledge graph viz |
| `context_search_all` | `mcp__memory-keeper__context_search_all` | Cross-session search |

---

## Context7: Complete Name Resolution

| Layer 1 (Package) | Layer 2 (Runtime) | Description |
|--------------------|-------------------|-------------|
| `resolve-library-id` | `mcp__plugin_context7_context7__resolve-library-id` | Resolve package to library ID |
| `query-docs` | `mcp__plugin_context7_context7__query-docs` | Query library documentation |

**Note:** Jerry governance currently references `mcp__context7__resolve-library-id` and `mcp__context7__query-docs` (MCP server prefix). Since Context7 is configured as a **Plugin** (not an MCP server), the actual runtime names use the plugin prefix `mcp__plugin_context7_context7__`. However, the `settings.local.json` wildcard covers both prefixes, so Context7 tools function correctly despite the naming mismatch in governance files.

---

## Tool Name Mapping (Wrong vs. Correct)

### Memory-Keeper (5 wrong references)

| Jerry References (WRONG) | Correct Layer 2 Name | Parameter Differences |
|---|---|---|
| `mcp__memory-keeper__store` | `mcp__memory-keeper__context_save` | Uses `key`+`value` (same concept), adds `category`, `priority`, `channel`, `private` |
| `mcp__memory-keeper__retrieve` | `mcp__memory-keeper__context_get` | Uses `key` (same), adds `category`, `channel`, `keyPattern`, filtering, pagination |
| `mcp__memory-keeper__search` | `mcp__memory-keeper__context_search` | Uses `query` (same concept), adds `searchIn`, `category`, `channel`, filtering |
| `mcp__memory-keeper__list` | `mcp__memory-keeper__context_session_list` | Different concept: lists sessions, not items. For item listing, use `context_get` without key filter |
| `mcp__memory-keeper__delete` | `mcp__memory-keeper__context_batch_delete` | Uses `keys` array or `keyPattern` (glob syntax) |

### Context7 (2 inconsistent references)

| Jerry References (Inconsistent) | Correct Layer 2 Name | Status |
|---|---|---|
| `mcp__context7__resolve-library-id` | `mcp__plugin_context7_context7__resolve-library-id` | Works via wildcard, but governance name is wrong prefix |
| `mcp__context7__query-docs` | `mcp__plugin_context7_context7__query-docs` | Works via wildcard, but governance name is wrong prefix |

### Additional High-Value Tools Not Referenced by Jerry

These exist in the actual server but are completely absent from Jerry's governance:

| Layer 2 Name | Value for Jerry |
|------|----------------|
| `mcp__memory-keeper__context_session_start` | Should be called at session start per MCP-002 |
| `mcp__memory-keeper__context_checkpoint` | Maps directly to AE-006 checkpoint requirements |
| `mcp__memory-keeper__context_restore_checkpoint` | Session resume / handoff recovery |
| `mcp__memory-keeper__context_prepare_compaction` | Maps directly to AE-006e compaction event handling |
| `mcp__memory-keeper__context_summarize` | Phase boundary summaries for handoffs |
| `mcp__memory-keeper__context_diff` | Change tracking between phases |
| `mcp__memory-keeper__context_search_all` | Cross-session search (multi-session research per MCP-M-001) |
| `mcp__memory-keeper__context_link` | Relationship tracking between context items |
| `mcp__memory-keeper__context_batch_save` | Efficient multi-item persistence at phase boundaries |

---

## Tool Profiles

The server supports three profiles to control context overhead:

| Profile | Tool Count | Recommended For |
|---------|------------|----------------|
| **minimal** | 8 | Basic session persistence, checkpointing |
| **standard** | 22 | Multi-session workflows, batch operations, git integration |
| **full** | 38 | Knowledge graph, semantic search, real-time monitoring |

**Recommendation for Jerry:** The **standard** profile (22 tools) covers all MCP-002 requirements plus batch operations and git integration. The full profile adds semantic search and knowledge graph features that could enhance cross-session research (MCP-M-001) but adds 16 tools to agent context.

**Current configuration:** Memory-keeper appears to be running in **full** profile (all 38 tools visible in Claude Code runtime).

---

## Affected Files

### Governance Rules (3 files)

| File | References | Impact |
|------|-----------|--------|
| `.context/rules/mcp-tool-standards.md` | Canonical Tool Names table (5 wrong memory-keeper names, 2 inconsistent Context7 names), Memory-Keeper Integration section, Agent Integration Matrix, Error Handling, L2-REINJECT markers | SSOT for tool names; all other files derive from this |
| `.context/rules/quality-enforcement.md` | L2-REINJECT marker referencing store/retrieve | L2 behavioral reinforcement points at dead tools |
| `TOOL_REGISTRY.yaml` | Tool definitions (`mcp__memory-keeper__store/retrieve/search/list/delete`), agent_permissions for 7 agents | Agent permission declarations reference nonexistent tools |

### Agent Definitions (7 agents across 14 files: .md + .governance.yaml)

| Agent | Files |
|-------|-------|
| `orch-planner` | `skills/orchestration/agents/orch-planner.md`, `composition/orch-planner.agent.yaml` |
| `orch-tracker` | `skills/orchestration/agents/orch-tracker.md`, `composition/orch-tracker.agent.yaml` |
| `orch-synthesizer` | `skills/orchestration/agents/orch-synthesizer.md`, `composition/orch-synthesizer.agent.yaml` |
| `ps-architect` | `skills/problem-solving/agents/ps-architect.md`, `composition/ps-architect.agent.yaml` |
| `nse-requirements` | `skills/nasa-se/agents/nse-requirements.md`, `composition/nse-requirements.agent.yaml` |
| `ts-parser` | `skills/transcript/agents/ts-parser.md`, `composition/ts-parser.agent.yaml` |
| `ts-extractor` | `skills/transcript/agents/ts-extractor.md`, `composition/ts-extractor.agent.yaml` |

### Skill Files (4 files)

| File | References |
|------|-----------|
| `skills/orchestration/SKILL.md` | Tool name references in MCP integration section |
| `skills/problem-solving/SKILL.md` | Tool name references |
| `skills/nasa-se/SKILL.md` | Tool name references |
| `skills/transcript/SKILL.md` | Tool name references |

### Settings (1 file)

| File | References | Status |
|------|-----------|--------|
| `.claude/settings.local.json` | Wildcard `mcp__memory-keeper__*` (correct, catches all), specific wrong entries `store/retrieve/list/delete/search` (redundant noise), both `mcp__context7__*` and `mcp__plugin_context7_context7__*` (belt-and-suspenders, both valid per separate namespaces) | Functional via wildcards; remove redundant specific entries |

### Prompt Files (3+ files)

| File | References |
|------|-----------|
| `skills/orchestration/composition/orch-planner.prompt.md` | Tool usage examples |
| `skills/orchestration/composition/orch-tracker.prompt.md` | Tool usage examples |
| `skills/orchestration/composition/orch-synthesizer.prompt.md` | Tool usage examples |

---

## Remediation Plan

### Phase 1: Fix SSOT Tool Names (Critical)

1. Update `.context/rules/mcp-tool-standards.md`:
   - Canonical Tool Names table: replace 5 wrong memory-keeper names with correct Layer 2 names
   - Canonical Tool Names table: replace 2 Context7 entries with correct Plugin prefix names
   - Memory-Keeper Integration section: update trigger table tool references
   - L2-REINJECT marker: update `store`/`retrieve` to `context_save`/`context_get`
2. Update `.claude/settings.local.json`:
   - Remove specific wrong entries (lines 19-23: `store`, `retrieve`, `list`, `delete`, `search`)
   - Keep wildcard `mcp__memory-keeper__*` (sufficient per [Claude Code docs](https://code.claude.com/docs/en/permissions))
   - Keep both Context7 wildcards (`mcp__context7__*` and `mcp__plugin_context7_context7__*`) as defensive belt-and-suspenders
   - Remove redundant specific Context7 entries (wildcards cover them)
3. Update `TOOL_REGISTRY.yaml`:
   - Tool definitions: replace all 5 wrong memory-keeper tool entries
   - Agent permissions: update all 7 agents with correct tool names
   - Add Context7 plugin-prefix corrections

### Phase 2: Fix Agent Definitions

4. Update 7 agent `.md` files (frontmatter `tools`/`mcpServers` fields + methodology references)
5. Update 7 agent `.governance.yaml` / `.agent.yaml` files (`capabilities.allowed_tools`)
6. Update 3+ prompt `.prompt.md` files

### Phase 3: Fix Skill Files

7. Update 4 SKILL.md files (MCP integration sections)

### Phase 4: Enhance Integration

8. Add `context_session_start` to session-start workflow
9. Map `context_checkpoint` to AE-006 checkpoint requirements
10. Map `context_prepare_compaction` to AE-006e compaction handling
11. Consider adding `context_summarize` for phase boundary handoffs
12. Decide on tool profile (recommend: standard/22 tools)

---

## Sources

- [mkreyman/mcp-memory-keeper GitHub](https://github.com/mkreyman/mcp-memory-keeper)
- [mcp-memory-keeper npm](https://www.npmjs.com/package/mcp-memory-keeper)
- [MCP Memory Keeper - Awesome MCP Servers](https://mcpservers.org/servers/mkreyman/mcp-memory-keeper)
- [MCP Memory Keeper - Glama](https://glama.ai/mcp/servers/@mkreyman/mcp-memory-keeper)
- [MCP Memory Keeper - LobeHub](https://lobehub.com/mcp/mkreyman-mcp-memory-keeper)
- `~/.claude/.claude.json` — MCP server configuration (memory-keeper as global MCP server)
- `~/.claude/settings.json` — Plugin configuration (Context7 as Plugin)
- `.claude/settings.local.json` — Permission allowlist (both wildcards and specific entries)

---

*Research Date: 2026-02-26*
*Agent: Main context (manual research)*
*Data Sources: WebSearch, WebFetch, local config file inspection*
