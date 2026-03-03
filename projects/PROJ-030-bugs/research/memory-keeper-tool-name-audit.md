# Memory-Keeper Tool Name Audit

> Research report: actual MCP tool names vs. Jerry Framework references.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Root cause and impact |
| [Actual Tool Inventory](#actual-tool-inventory) | Complete tool list from mcp-memory-keeper |
| [Tool Name Mapping](#tool-name-mapping) | Wrong names vs. correct names |
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

---

## Actual Tool Inventory

The mcp-memory-keeper server exposes **38 tools** across three profiles. When used as a Claude Code MCP server, tool names are prefixed with `mcp__memory-keeper__` (the server name from the MCP config).

### Minimal Profile (8 tools)

| Tool Name | Description |
|-----------|-------------|
| `context_session_start` | Initialize new session with name, description, project dir |
| `context_save` | Store context items with key, value, category, priority, channel |
| `context_get` | Retrieve saved context by key, category, or session with filtering |
| `context_search` | Full-text search across saved context |
| `context_status` | Check current session status and statistics |
| `context_checkpoint` | Create named context snapshots |
| `context_restore_checkpoint` | Restore from saved snapshots |
| `context_prepare_compaction` | Auto-save critical context before compaction |

### Standard Profile (adds 14 tools = 22 total)

| Tool Name | Description |
|-----------|-------------|
| `context_set_project_dir` | Configure project directory for git tracking |
| `context_session_list` | List recent sessions |
| `context_cache_file` | Cache file content with hash for change detection |
| `context_file_changed` | Check if a file has changed since cached |
| `context_batch_save` | Save multiple context items atomically |
| `context_batch_update` | Update multiple items with partial updates atomically |
| `context_batch_delete` | Delete multiple items by keys or pattern atomically |
| `context_reassign_channel` | Move context items between channels |
| `context_link` | Create relationships between context items |
| `context_get_related` | Get items related to a given context item |
| `context_export` | Export session data for backup or sharing |
| `context_import` | Import previously exported session data |
| `context_git_commit` | Create git commit with automatic context save |
| `context_summarize` | Get AI-friendly summary of session context |

### Full Profile (adds 16 tools = 38 total)

| Tool Name | Description |
|-----------|-------------|
| `context_watch` | Create and manage watchers for real-time monitoring |
| `context_semantic_search` | Search using natural language queries |
| `context_delegate` | Delegate analysis tasks to specialized agents |
| `context_branch_session` | Create branch from current session for alternatives |
| `context_merge_sessions` | Merge another session into the current one |
| `context_journal_entry` | Add timestamped journal entry with tags and mood |
| `context_timeline` | Get timeline of activities with grouping |
| `context_compress` | Intelligently compress old context to save space |
| `context_integrate_tool` | Track events from other MCP tools |
| `context_diff` | Get changes since a specific point in time |
| `context_list_channels` | List all channels with metadata |
| `context_channel_stats` | Get statistics for channels |
| `context_analyze` | Analyze context to extract entities and relationships |
| `context_find_related` | Find entities related to a key or entity |
| `context_visualize` | Generate visualization data for knowledge graph |
| `context_search_all` | Search across multiple or all sessions |

---

## Tool Name Mapping

The Jerry Framework references 5 tools. None of them exist.

| Jerry References (WRONG) | Actual Tool Name | Parameter Differences |
|---|---|---|
| `mcp__memory-keeper__store` | `mcp__memory-keeper__context_save` | Uses `key`+`value` (same concept), but adds `category`, `priority`, `channel`, `private` params |
| `mcp__memory-keeper__retrieve` | `mcp__memory-keeper__context_get` | Uses `key` param (same), but adds `category`, `channel`, `keyPattern`, filtering, pagination |
| `mcp__memory-keeper__search` | `mcp__memory-keeper__context_search` | Uses `query` param (same concept), adds `searchIn`, `category`, `channel`, filtering |
| `mcp__memory-keeper__list` | `mcp__memory-keeper__context_session_list` | Different concept: lists sessions, not individual items. For item listing, use `context_get` without key filter |
| `mcp__memory-keeper__delete` | `mcp__memory-keeper__context_batch_delete` | Uses `keys` array or `keyPattern` (glob syntax) |

### Additional High-Value Tools Not Referenced by Jerry

These tools exist in the actual server but are completely absent from Jerry's governance:

| Tool | Value for Jerry |
|------|----------------|
| `context_session_start` | Should be called at session start per MCP-002 |
| `context_checkpoint` | Maps directly to AE-006 checkpoint requirements |
| `context_restore_checkpoint` | Session resume / handoff recovery |
| `context_prepare_compaction` | Maps directly to AE-006e compaction event handling |
| `context_summarize` | Phase boundary summaries for handoffs |
| `context_diff` | Change tracking between phases |
| `context_search_all` | Cross-session search (multi-session research per MCP-M-001) |
| `context_link` | Relationship tracking between context items |
| `context_batch_save` | Efficient multi-item persistence at phase boundaries |

---

## Tool Profiles

The server supports three profiles to control context overhead:

| Profile | Tool Count | Recommended For |
|---------|------------|----------------|
| **minimal** | 8 | Basic session persistence, checkpointing |
| **standard** | 22 | Multi-session workflows, batch operations, git integration |
| **full** | 38 | Knowledge graph, semantic search, real-time monitoring |

**Recommendation for Jerry:** The **standard** profile (22 tools) covers all MCP-002 requirements plus batch operations and git integration. The full profile adds semantic search and knowledge graph features that could enhance cross-session research (MCP-M-001) but adds 16 tools to agent context.

---

## Affected Files

### Governance Rules (3 files)

| File | References | Impact |
|------|-----------|--------|
| `.context/rules/mcp-tool-standards.md` | Canonical Tool Names table, Memory-Keeper Integration section, Agent Integration Matrix, Error Handling | SSOT for tool names; all other files derive from this |
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

| File | References |
|------|-----------|
| `.claude/settings.local.json` | Permission allowlist: `mcp__memory-keeper__store`, `retrieve`, `list`, `delete`, `search` |

### Prompt Files (3+ files)

| File | References |
|------|-----------|
| `skills/orchestration/composition/orch-planner.prompt.md` | Tool usage examples |
| `skills/orchestration/composition/orch-tracker.prompt.md` | Tool usage examples |
| `skills/orchestration/composition/orch-synthesizer.prompt.md` | Tool usage examples |

---

## Remediation Plan

### Phase 1: Fix Tool Names (Critical)

1. Update `.context/rules/mcp-tool-standards.md` canonical tool names table
2. Update `.claude/settings.local.json` permission allowlist
3. Update `TOOL_REGISTRY.yaml` tool definitions and agent permissions
4. Update L2-REINJECT markers in `mcp-tool-standards.md`

### Phase 2: Fix Agent Definitions

5. Update 7 agent `.md` files (frontmatter `tools` field + methodology references)
6. Update 7 agent `.governance.yaml` / `.agent.yaml` files
7. Update 3+ prompt `.prompt.md` files

### Phase 3: Fix Skill Files

8. Update 4 SKILL.md files

### Phase 4: Enhance Integration

9. Add `context_session_start` to session-start workflow
10. Map `context_checkpoint` to AE-006 checkpoint requirements
11. Map `context_prepare_compaction` to AE-006e compaction handling
12. Consider adding `context_summarize` for phase boundary handoffs
13. Decide on tool profile (recommend: standard/22 tools)

---

## Sources

- [mkreyman/mcp-memory-keeper GitHub](https://github.com/mkreyman/mcp-memory-keeper)
- [mcp-memory-keeper npm](https://www.npmjs.com/package/mcp-memory-keeper)
- [MCP Memory Keeper - Awesome MCP Servers](https://mcpservers.org/servers/mkreyman/mcp-memory-keeper)
- [MCP Memory Keeper - Glama](https://glama.ai/mcp/servers/@mkreyman/mcp-memory-keeper)
- [MCP Memory Keeper - LobeHub](https://lobehub.com/mcp/mkreyman-mcp-memory-keeper)

---

*Research Date: 2026-02-26*
*Agent: Main context (manual research)*
*Data Sources: WebSearch, WebFetch (Context7 quota exceeded — fallback per MCP error handling)*
