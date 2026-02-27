# Claude Code MCP Tool Permission Model: Context7 Namespace Analysis

> Research report on MCP tool naming, wildcard scoping, and permission hierarchy in Claude Code, with specific focus on Context7 plugin vs MCP server namespacing.

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Plain-language findings for project decision-making |
| [L1: Technical Analysis](#l1-technical-analysis) | Detailed technical findings with configuration examples |
| [L2: Architectural Implications](#l2-architectural-implications) | Strategic trade-offs, risks, and recommendations |
| [Research Questions](#research-questions) | Scoped questions driving this investigation |
| [Methodology](#methodology) | Sources consulted and credibility assessment |
| [Empirical Verification](#empirical-verification) | Runtime evidence from current session |
| [References](#references) | Full citation list with URLs |
| [PS Integration](#ps-integration) | Project state and artifact metadata |

---

## L0: Executive Summary

**What we researched:** How Claude Code names MCP tools internally and whether the wildcard permission `mcp__context7__*` covers tools that arrive through the Context7 *plugin* (which uses a different, longer prefix).

**Key finding:** They are **separate namespaces**. `mcp__context7__*` does NOT cover `mcp__plugin_context7_context7__*`. The two prefixes are constructed by entirely different code paths inside Claude Code:

- **User-configured MCP servers** produce tools named `mcp__{server-name}__{tool-name}` (e.g., `mcp__context7__resolve-library-id`).
- **Plugin-bundled MCP servers** produce tools named `mcp__plugin_{plugin-name}_{server-name}__{tool-name}` (e.g., `mcp__plugin_context7_context7__resolve-library-id`).

Since this project's `.claude/settings.json` enables Context7 as a **plugin** (`"enabledPlugins": {"context7@claude-plugins-official": true}`), the actual runtime tool names will use the `mcp__plugin_context7_context7__` prefix. The `mcp__context7__*` permission entries in `settings.local.json` would only take effect if Context7 were configured as a standalone MCP server (via `claude mcp add` or `.mcp.json`), not as a plugin.

**What this means for the project:** The Jerry framework's `settings.local.json` is correctly defensive by including **both** prefixes (lines 24-29). However, the `.context/rules/mcp-tool-standards.md` canonical tool names and all agent definitions reference only `mcp__context7__resolve-library-id` and `mcp__context7__query-docs`. If Context7 is installed as a plugin (as it currently is), these names will not match runtime tool names, causing tool invocation failures or permission denials in subagents that specify tools explicitly.

---

## Research Questions

| # | Question | Status |
|---|----------|--------|
| RQ-1 | How does `mcp__context7__*` work vs `mcp__plugin_context7_context7__*`? Are these separate namespaces? | **Answered** -- Separate namespaces |
| RQ-2 | Where are MCP tool permissions configured across the permission levels? | **Answered** -- Five levels documented |
| RQ-3 | How does Claude Code prefix tools from Plugins vs MCP Servers? | **Answered** -- Formulas documented |
| RQ-4 | Is Context7 a Plugin or MCP Server in this project? | **Answered** -- Plugin (settings.json confirms) |

---

## L1: Technical Analysis

### 1. MCP Tool Naming Formulas

Claude Code uses two distinct naming formulas depending on how an MCP server is registered.

#### Formula A: User-Configured MCP Servers

When an MCP server is added via `claude mcp add`, `.mcp.json`, or `~/.claude.json`:

```
mcp__{server-name}__{tool-name}
```

**Examples:**
- Server named `context7` with tool `resolve-library-id` produces: `mcp__context7__resolve-library-id`
- Server named `memory-keeper` with tool `store` produces: `mcp__memory-keeper__store`

The `{server-name}` is the **name you chose** when adding the server (the first argument to `claude mcp add`).

**Source:** [Claude Code Permissions Docs](https://code.claude.com/docs/en/permissions) -- "mcp__puppeteer matches any tool provided by the puppeteer server" and "mcp__puppeteer__puppeteer_navigate matches the puppeteer_navigate tool provided by the puppeteer server."

#### Formula B: Plugin-Bundled MCP Servers

When an MCP server is provided by a plugin (defined in the plugin's `.mcp.json` or `plugin.json`):

```
mcp__plugin_{plugin-name}_{server-name}__{tool-name}
```

**Examples:**
- Plugin `context7` with MCP server `context7` and tool `resolve-library-id` produces: `mcp__plugin_context7_context7__resolve-library-id`
- Plugin `atlassian` with MCP server `atlassian` and tool `addCommentToJiraIssue` produces: `mcp__plugin_atlassian_atlassian__addCommentToJiraIssue`

**Source:** [GitHub Issue #23149](https://github.com/anthropics/claude-code/issues/23149) -- "Plugin MCP tools: Format: mcp__plugin_<plugin-name>_<server-name>__<tool-name>". Also confirmed by [GitHub Issue #15145](https://github.com/anthropics/claude-code/issues/15145).

**Version caveat:** This formula is empirically observed from Claude Code v1.0.x-era GitHub issues (#23149, #15145), not from an official naming specification. It should be re-verified on major Claude Code upgrades.

#### Side-by-Side Comparison

| Aspect | User-Configured (Formula A) | Plugin-Bundled (Formula B) |
|--------|----------------------------|---------------------------|
| Prefix | `mcp__` | `mcp__plugin_` |
| Server identifier | `{server-name}` (user-chosen) | `{plugin-name}_{server-name}` |
| Separator before tool | `__` (double underscore) | `__` (double underscore) |
| Example | `mcp__context7__query-docs` | `mcp__plugin_context7_context7__query-docs` |
| Character count (prefix) | 5 + server name + 2 = variable | 14 + plugin + 1 + server + 2 = variable |

**Critical implication:** These are entirely different string prefixes. A permission rule matching one will NOT match the other.

### 2. Wildcard Permission Syntax for MCP Tools

The official Claude Code documentation (as of the current permissions page) states:

| Syntax | Effect |
|--------|--------|
| `mcp__puppeteer` | Matches **any tool** provided by the `puppeteer` server |
| `mcp__puppeteer__*` | Wildcard syntax that **also** matches all tools from the `puppeteer` server |
| `mcp__puppeteer__puppeteer_navigate` | Matches a **specific** tool |

**Source:** [Claude Code Permissions Documentation](https://code.claude.com/docs/en/permissions) -- MCP section under "Tool-specific permission rules."

**Historical context on wildcard reliability:**

There is a documented history of wildcard bugs in Claude Code. Multiple GitHub issues reported that `mcp__servername__*` wildcards silently failed to match:

- [Issue #3107](https://github.com/anthropics/claude-code/issues/3107): `mcp__atlassian__*` did not prevent permission prompts. Resolution: the correct syntax at that time was `mcp__atlassian` (without wildcard). Closed July 2025.
- [Issue #13077](https://github.com/anthropics/claude-code/issues/13077): `--allowedTools "mcp__myserver__*"` silently denied tools. Closed December 2025.
- [Issue #14730](https://github.com/anthropics/claude-code/issues/14730): Wildcard patterns in `.claude/settings.json` did not work. Closed December 2025 as duplicate.
- [Issue #2928](https://github.com/anthropics/claude-code/issues/2928): Feature request for `mcp__context7__*`. Resolution: use `mcp__context7` (bare server name). Closed July 2025.

The current official documentation now lists **both** `mcp__puppeteer` (bare name) and `mcp__puppeteer__*` (wildcard) as valid. This suggests the wildcard syntax was fixed in a late-2025 release: Issues #3107 and #2928 were closed in July 2025 (wildcards still broken), while #13077 and #14730 were closed in December 2025 (likely when the fix shipped). The bare server name (without `__*`) is the more reliable and originally-supported form.

### 3. Permission Configuration Levels

Claude Code supports five distinct levels where MCP tool permissions can be configured, including agent-level tool restrictions:

#### Level 1: Managed Settings (Highest Precedence)

**Location:** System-wide paths (require admin privileges):
- macOS: `/Library/Application Support/ClaudeCode/managed-settings.json`
- Linux/WSL: `/etc/claude-code/managed-settings.json`

**Capabilities:** Can enforce `allowedMcpServers`, `deniedMcpServers`, and `allowManagedMcpServersOnly`. These CANNOT be overridden.

**Source:** [Claude Code Settings Documentation](https://code.claude.com/docs/en/settings)

#### Level 2: User Settings

**Location:** `~/.claude/settings.json`

**Capabilities:** `permissions.allow`, `permissions.deny`, `permissions.ask` arrays. Applies across all projects for this user.

**Example:**
```json
{
  "permissions": {
    "allow": ["mcp__context7"]
  }
}
```

#### Level 3: Project Settings (Shared)

**Location:** `.claude/settings.json` (committed to git, shared with team)

**Capabilities:** Same `permissions` structure. Project settings override user settings for deny rules.

**Note:** `.claude/settings.json` is a HIGH-credibility primary source for fields the Claude Code runtime actually consumes (e.g., `enabledPlugins`, `permissions`). Other fields present in the same file (such as `allowed_tools`) are documentation-only constructs used by the Jerry framework's governance layer and are not parsed by the Claude Code runtime.

**Relevant finding:** The Jerry project's `.claude/settings.json` uses `allowed_tools`, which is NOT a standard Claude Code permission field [inferred from runtime behavior -- this field does not appear in the Claude Code official settings schema at [Settings Documentation](https://code.claude.com/docs/en/settings), which documents only `permissions.allow`, `permissions.deny`, and `permissions.ask` arrays]. The `allowed_tools` field is likely ignored by Claude Code's permission system and has no effect on tool access. This is a separate cleanup item.

#### Level 4: Local Project Settings (Highest user-level precedence)

**Location:** `.claude/settings.local.json` (gitignored, personal to developer)

**Capabilities:** Same `permissions` structure. Local settings override project settings.

**Current Jerry configuration (lines 18-29):**
```json
{
  "permissions": {
    "allow": [
      "mcp__memory-keeper__*",
      "mcp__memory-keeper__store",
      "mcp__memory-keeper__retrieve",
      "mcp__memory-keeper__list",
      "mcp__memory-keeper__delete",
      "mcp__memory-keeper__search",
      "mcp__context7__*",
      "mcp__context7__resolve-library-id",
      "mcp__context7__query-docs",
      "mcp__plugin_context7_context7__*",
      "mcp__plugin_context7_context7__resolve-library-id",
      "mcp__plugin_context7_context7__query-docs"
    ]
  }
}
```

This is the **correct defensive approach** -- covering both possible namespace prefixes.

#### Level 5: Agent-Level Tool Restrictions

**Location:** Agent `.md` file YAML frontmatter `tools` field

**Capabilities:** The `tools` field in subagent frontmatter acts as an **allowlist**. Only listed tools are available to the subagent. If omitted, the subagent inherits ALL tools from the parent conversation.

**Critical finding:** The `tools` field in agent definitions uses tool names directly. If an agent definition specifies `mcp__context7__resolve-library-id` but the runtime tool is actually `mcp__plugin_context7_context7__resolve-library-id`, the agent will NOT have access to that tool.

**Source:** [Claude Code Sub-agents Documentation](https://code.claude.com/docs/en/sub-agents) -- "tools: Tools the subagent can use. Inherits all tools if omitted."

#### Precedence Summary

```
Managed Settings (highest, cannot override)
  > Command Line Arguments (--allowedTools, --disallowedTools)
    > Local Project Settings (.claude/settings.local.json)
      > Shared Project Settings (.claude/settings.json)
        > User Settings (~/.claude/settings.json)
```

Within a subagent, the `tools` frontmatter further restricts the available tools from the parent's permitted set.

### 4. Context7 Configuration in This Project

**Finding:** Context7 is configured as a **plugin**, not a standalone MCP server.

**Evidence:** `.claude/settings.json` line 81:
```json
{
  "enabledPlugins": {
    "context7@claude-plugins-official": true
  }
}
```

No `.mcp.json` file exists at the project root (confirmed via Glob search). User-level MCP configuration (`~/.claude/settings.json`) could not be verified (permission denied); it is unknown whether Context7 is also configured as a standalone MCP server at user scope.

**Implication:** At runtime, Context7 tools will be registered under the **plugin prefix**:
- `mcp__plugin_context7_context7__resolve-library-id`
- `mcp__plugin_context7_context7__query-docs`

The `mcp__context7__resolve-library-id` form would only exist if Context7 were also (or instead) configured as a standalone MCP server.

### 5. Impact on Jerry Framework Agent Definitions

The Jerry framework's `.context/rules/mcp-tool-standards.md` defines canonical tool names as:

| Tool | Canonical Name |
|------|---------------|
| Context7 Resolve | `mcp__context7__resolve-library-id` |
| Context7 Query | `mcp__context7__query-docs` |

If Context7 is installed as a plugin (which it currently is), these canonical names will not match the runtime tool names. This creates a mismatch in:

1. **Agent `tools` frontmatter** -- Agents that list `mcp__context7__resolve-library-id` in their `tools` array will not have access to the plugin-prefixed version.
2. **Agent `mcpServers` frontmatter** -- The `mcpServers` field in agent frontmatter references server names (e.g., `context7`), not tool names. This field would need the plugin-qualified name.
3. **Documentation and SOPs** -- All references to `mcp__context7__` in Jerry documentation assume the non-plugin prefix.

**Memory-Keeper status:** Memory-Keeper is configured as a standalone MCP server and uses the `mcp__memory-keeper__` prefix as expected. However, the canonical tool names in `.context/rules/mcp-tool-standards.md` (e.g., `mcp__memory-keeper__store`) do NOT match actual runtime tool names (e.g., `mcp__memory-keeper__context_save`). This confirms BUG-001 is a real, verified tool name mismatch -- the same class of issue as the Context7 namespace problem.

### Affected Files Inventory

The following files reference `mcp__context7__` and would be affected by namespace changes. Gathered via `Grep` search across the codebase on 2026-02-26.

**Agent definition files (frontmatter `tools` or `mcpServers` fields):**

| File | Reference Type |
|------|---------------|
| `skills/problem-solving/agents/ps-researcher.md` | `mcpServers: context7: true` + prose `mcp__context7__resolve-library-id`, `mcp__context7__query-docs` |
| `skills/problem-solving/agents/ps-analyst.md` | `mcpServers: context7: true` + prose `mcp__context7__*` |
| `skills/problem-solving/agents/ps-architect.md` | `mcpServers: context7: true` + prose `mcp__context7__*` |
| `skills/problem-solving/agents/ps-synthesizer.md` | `mcpServers: context7: true` + prose `mcp__context7__*` |
| `skills/problem-solving/agents/ps-investigator.md` | `mcpServers: context7: true` + prose `mcp__context7__*` |
| `skills/nasa-se/agents/nse-explorer.md` | `mcpServers: context7: true` + prose `mcp__context7__resolve-library-id`, `mcp__context7__query-docs` |
| `skills/nasa-se/agents/nse-architecture.md` | `mcpServers: context7: true` + prose `mcp__context7__resolve-library-id`, `mcp__context7__query-docs` |
| `skills/eng-team/agents/eng-lead.md` | `mcpServers: context7: true` |
| `skills/eng-team/agents/eng-architect.md` | `mcpServers: context7: true` |
| `skills/eng-team/agents/eng-backend.md` | `mcpServers: context7: true` |
| `skills/eng-team/agents/eng-frontend.md` | `mcpServers: context7: true` |
| `skills/eng-team/agents/eng-infra.md` | `mcpServers: context7: true` |
| `skills/eng-team/agents/eng-devsecops.md` | `mcpServers: context7: true` |
| `skills/eng-team/agents/eng-qa.md` | `mcpServers: context7: true` |
| `skills/eng-team/agents/eng-security.md` | `mcpServers: context7: true` |
| `skills/eng-team/agents/eng-reviewer.md` | `mcpServers: context7: true` |
| `skills/eng-team/agents/eng-incident.md` | `mcpServers: context7: true` |
| `skills/red-team/agents/red-lead.md` | `mcpServers: context7: true` |
| `skills/red-team/agents/red-recon.md` | `mcpServers: context7: true` |
| `skills/red-team/agents/red-vuln.md` | `mcpServers: context7: true` |
| `skills/red-team/agents/red-exploit.md` | `mcpServers: context7: true` |
| `skills/red-team/agents/red-privesc.md` | `mcpServers: context7: true` |
| `skills/red-team/agents/red-lateral.md` | `mcpServers: context7: true` |
| `skills/red-team/agents/red-persist.md` | `mcpServers: context7: true` |
| `skills/red-team/agents/red-exfil.md` | `mcpServers: context7: true` |
| `skills/red-team/agents/red-social.md` | `mcpServers: context7: true` |
| `skills/red-team/agents/red-infra.md` | `mcpServers: context7: true` |
| `skills/red-team/agents/red-reporter.md` | `mcpServers: context7: true` |

**Skill-level files (`allowed-tools` in SKILL.md):**

| File | Reference Type |
|------|---------------|
| `skills/problem-solving/SKILL.md` | `allowed-tools` includes `mcp__context7__resolve-library-id`, `mcp__context7__query-docs` |
| `skills/nasa-se/SKILL.md` | `allowed-tools` includes `mcp__context7__resolve-library-id`, `mcp__context7__query-docs` |
| `skills/eng-team/SKILL.md` | `allowed-tools` includes `mcp__context7__resolve-library-id`, `mcp__context7__query-docs` |
| `skills/red-team/SKILL.md` | `allowed-tools` includes `mcp__context7__resolve-library-id`, `mcp__context7__query-docs` |

**Rules and configuration files:**

| File | Reference Type |
|------|---------------|
| `.context/rules/mcp-tool-standards.md` | Canonical tool name definitions and integration protocol |
| `.claude/settings.local.json` | `permissions.allow` entries (both prefixes) |
| `TOOL_REGISTRY.yaml` | Tool-to-agent mapping SSOT |

**Total: 28 agent definition files, 4 SKILL.md files, 3 rules/config files = 35 files affected.**

---

## L2: Architectural Implications

### Trade-Off Analysis

Evaluated using multi-criteria decision analysis across four dimensions: tool name stability, operational overhead, compliance with principle of least privilege (T1-T5 tier model), and team onboarding burden.

| Approach | Pros | Cons |
|----------|------|------|
| **A: Switch Context7 to standalone MCP server** | Tool names match canonical names. No agent definition changes needed. Simpler permission rules. | Loses plugin auto-update. Requires manual `claude mcp add` per developer. Not using Anthropic's recommended distribution channel. |
| **B: Update canonical names to plugin prefix** | Matches actual runtime behavior. Correct by construction. | Longer tool names (may approach 64-char API limit for some tools). All agent definitions and documentation must be updated. Plugin name could change in future releases. |
| **C: Support both prefixes (current `settings.local.json` approach)** | Defensive. Works regardless of installation method. | Doubles the permission entries. Agent `tools` frontmatter can only specify one name -- must omit `tools` (inherit all) or list both. Documentation remains ambiguous. |
| **D: Omit `tools` from agent definitions; rely on session-level permissions** | Simplest. No tool name coupling in agent definitions. | Agents get access to ALL tools, violating principle of least privilege (T1-T5 tier model in `.context/rules/agent-development-standards.md`). |

### Recommended Approach

**Approach A (switch to standalone MCP server)** is the cleanest solution for the Jerry framework because:

1. It aligns canonical tool names with runtime names.
2. It avoids the 64-character tool name limit risk (plugin prefix adds ~19 characters).
3. It is consistent with how `memory-keeper` is configured (as a standalone MCP server, not a plugin).
4. Agent definitions and `.context/rules/mcp-tool-standards.md` require zero changes.

**Migration path:**

**Scope selection:** User scope (`--scope user`) is recommended as the primary installation method because it is consistent with how Memory-Keeper is configured (standalone MCP server) and applies across all projects without per-project setup. Alternatively, project scope via `.mcp.json` provides automatic configuration for all developers who clone the repository but requires each project to maintain its own Context7 entry.

```bash
# 1. Disable the plugin
# Remove "context7@claude-plugins-official" from .claude/settings.json enabledPlugins

# 2. Add as standalone MCP server (user scope -- recommended for consistency with memory-keeper)
claude mcp add --scope user context7 -- npx -y @upstash/context7-mcp@latest
# Alternative: project scope via .mcp.json (auto-configures for all developers on this project)

# 3. Update agent tools frontmatter
# All agent .md files referencing mcp__context7__ in their `tools` field -- no changes needed
# (the manual MCP prefix already matches the canonical names)

# 4. Update settings.local.json permissions
# Remove plugin-prefixed entries; keep only: "mcp__context7" (bare server name)

# 5. Update TOOL_REGISTRY.yaml
# Verify Context7 entries reference mcp__context7__ prefix (already correct)

# 6. Verify
# In a new Claude Code session, confirm:
# Run `claude mcp list` to verify the MCP server appears in the active configuration.
# - `mcp__context7__resolve-library-id` appears in available tools (not mcp__plugin_*)
# - A subagent invoked via Task can access Context7 tools
```

**Acceptance criteria:** Migration is complete when: (a) only `mcp__context7__` prefix tools appear at runtime, (b) no `mcp__plugin_context7_context7__` tools are visible, (c) a Task-invoked subagent can successfully call Context7.

**Rollback procedure:** If migration fails: (a) re-enable `enabledPlugins` in `.claude/settings.json`, (b) restore dual-prefix `settings.local.json` entries, (c) verify tools work under the plugin prefix.

### Risk Assessment

| Risk | Likelihood | Impact | Mitigation | Residual Risk |
|------|-----------|--------|------------|---------------|
| Plugin prefix changes in future Claude Code version | Medium (Claude Code release cadence is rapid; plugin manifest formats are lightly documented and subject to change without deprecation notice) | High -- all permission entries break | Approach A eliminates this risk entirely | None (eliminated) |
| Tool name exceeds 64-char API limit with plugin prefix | Low (Context7 tools have short names; the longest observed is ~55 chars) | High -- API error, tool unusable | Approach A eliminates; Approach B: monitor tool name lengths | None (eliminated by Approach A) |
| Developer forgets `claude mcp add` setup step | Medium (one-time manual step per developer; no CI enforcement currently exists) | Low -- documented in onboarding | Add to project-scoped `.mcp.json` for automatic configuration | Low -- `.mcp.json` fallback catches most cases |
| Wildcard permissions silently fail | Low (appears fixed in late-2025 releases based on issue closure timeline; see Section 2 above) | Medium -- tools require manual approval each time | Include both bare name and explicit tool entries as fallback | Low -- explicit entries provide redundant coverage |

### Alignment with Existing Architecture

The Jerry framework's `.context/rules/agent-development-standards.md` defines a T1-T5 tool tier model where agents specify their allowed tools explicitly. This model assumes stable, predictable tool names. Plugin-prefixed names introduce instability because:

1. The prefix depends on the plugin's name in the marketplace entry, which is external to Jerry's control.
2. If Context7 is installed from a different marketplace or forked, the plugin name changes.
3. The `mcpServers` frontmatter field in agent definitions references server names, not full tool names, creating a layer of indirection that is documented for user-configured servers but not for plugin-bundled servers. However, empirical verification confirms that `mcpServers: { context7: true }` does resolve correctly for plugin-installed servers at runtime [see [Empirical Verification](#empirical-verification), point 3].

---

## Methodology

### Sources Consulted

| Source Type | Source | Credibility |
|-------------|--------|-------------|
| Official documentation | [Claude Code Permissions](https://code.claude.com/docs/en/permissions) | HIGH |
| Official documentation | [Claude Code Settings](https://code.claude.com/docs/en/settings) | HIGH |
| Official documentation | [Claude Code MCP](https://code.claude.com/docs/en/mcp) | HIGH |
| Official documentation | [Claude Code Sub-agents](https://code.claude.com/docs/en/sub-agents) | HIGH |
| Official documentation | [Claude Code Plugins Reference](https://code.claude.com/docs/en/plugins-reference) | HIGH |
| GitHub issue | [#23149 Plugin MCP tool names exceed 64-char limit](https://github.com/anthropics/claude-code/issues/23149) | HIGH (primary source for Formula B) |
| GitHub issue | [#15145 MCP servers incorrectly namespaced under plugin name](https://github.com/anthropics/claude-code/issues/15145) | HIGH (confirms plugin prefix behavior) |
| GitHub issue | [#2928 Wildcard permissions for MCP servers](https://github.com/anthropics/claude-code/issues/2928) | HIGH (confirms bare name vs wildcard) |
| GitHub issue | [#3107 MCP wildcard permissions not honored](https://github.com/anthropics/claude-code/issues/3107) | HIGH (documents wildcard bug history) |
| GitHub issue | [#13077 --allowedTools wildcard for MCP](https://github.com/anthropics/claude-code/issues/13077) | HIGH (documents CLI wildcard bug) |
| GitHub issue | [#14730 Wildcard matching fails](https://github.com/anthropics/claude-code/issues/14730) | MEDIUM (duplicate, but confirms pattern) |
| Project configuration | `.claude/settings.json` (local file) | HIGH (primary source) |
| Project configuration | `.claude/settings.local.json` (local file) | HIGH (primary source) |
| Context7 GitHub | [upstash/context7](https://github.com/upstash/context7) | HIGH (official installation docs) |

### Limitations

1. **No access to `~/.claude/settings.json`** -- Permission denied when attempting to read user-level settings. Could not verify whether Context7 is also configured as a standalone MCP server at user scope.
2. **Plugin naming behavior is documented primarily through bug reports**, not official specification. The `mcp__plugin_{plugin}_{server}__` formula is derived from observed behavior reported in GitHub issues, not from an official naming specification document.
3. **Wildcard support status is ambiguous** -- The official docs now list both `mcp__servername` and `mcp__servername__*` as valid, but multiple resolved bug reports (from mid-to-late 2025) indicate wildcards were broken. The exact version where wildcards became reliable is not documented.

---

## Empirical Verification

The following runtime evidence was gathered from the current Claude Code session (2026-02-26) to empirically verify the dual-namespace thesis.

### Observed Runtime Tool Names

**Context7 tools (plugin-installed):**

| Expected (canonical) | Actual (runtime) | Match? |
|---------------------|-----------------|--------|
| `mcp__context7__resolve-library-id` | `mcp__plugin_context7_context7__resolve-library-id` | NO -- plugin prefix present |
| `mcp__context7__query-docs` | `mcp__plugin_context7_context7__query-docs` | NO -- plugin prefix present |

**Memory-Keeper tools (standalone MCP server):**

| Expected (canonical in .context/rules/mcp-tool-standards.md) | Actual (runtime) | Match? |
|----------------------------------------------|-----------------|--------|
| `mcp__memory-keeper__store` | `mcp__memory-keeper__context_save` | NO -- different tool name |
| `mcp__memory-keeper__retrieve` | `mcp__memory-keeper__context_get` | NO -- different tool name |
| `mcp__memory-keeper__search` | `mcp__memory-keeper__context_search` | NO -- different tool name |
| (not documented) | `mcp__memory-keeper__context_list` | N/A -- undocumented tool |
| (not documented) | `mcp__memory-keeper__context_delete` | N/A -- undocumented tool |

### Verification Conclusions

1. **Dual-namespace thesis CONFIRMED.** Context7 tools at runtime use the `mcp__plugin_context7_context7__` prefix, exactly as predicted by Formula B. The canonical `mcp__context7__` prefix does NOT appear in the available tools list. This is direct empirical evidence that the plugin installation method produces a different namespace than the standalone MCP server method.

2. **BUG-001 tool name mismatch CONFIRMED for both MCP integrations.** Memory-Keeper uses the correct `mcp__memory-keeper__` prefix (standalone server), but the *tool names themselves* differ from what `.context/rules/mcp-tool-standards.md` documents. The canonical name `store` maps to runtime name `context_save`; `retrieve` maps to `context_get`; `search` maps to `context_search`. This is a tool-name-level mismatch (the MCP server exposes different operation names than what Jerry's documentation assumes), distinct from but compounding the namespace-prefix-level mismatch affecting Context7.

3. **Agent `mcpServers` field works for plugin-installed servers.** Despite Context7 being installed as a plugin rather than a standalone server, agents with `mcpServers: { context7: true }` in their frontmatter DO receive Context7 tools at runtime. The tools arrive under the plugin prefix, but the `mcpServers` server-name reference resolves correctly. This means agent definitions using `mcpServers` are functional; the mismatch only affects agents that reference specific tool names in `tools` frontmatter or in prose instructions.

4. **Methodology upgrade.** This empirical verification elevates the evidence basis from documentation-and-bug-reports (secondary sources) to direct runtime observation (primary source). The Formula B plugin naming pattern is confirmed operational in the current Claude Code version running this session. **Generalizability scope:** This runtime observation confirms Formula B for the specific case of the `context7` plugin with its `context7` MCP server. The general formula `mcp__plugin_{plugin-name}_{server-name}__{tool-name}` is inferred from GitHub issue patterns (#23149, #15145) covering additional plugins (e.g., `atlassian`); full generalizability across all plugins has not been independently verified at runtime.

---

## References

1. [Claude Code Permissions Documentation](https://code.claude.com/docs/en/permissions) -- Key insight: Official MCP permission syntax including bare name (`mcp__puppeteer`) and wildcard (`mcp__puppeteer__*`) forms.
2. [Claude Code Settings Documentation](https://code.claude.com/docs/en/settings) -- Key insight: Five-level precedence hierarchy (managed > CLI > local > project > user).
3. [Claude Code MCP Documentation](https://code.claude.com/docs/en/mcp) -- Key insight: MCP server scopes (local, project, user) and plugin-provided MCP servers.
4. [Claude Code Sub-agents Documentation](https://code.claude.com/docs/en/sub-agents) -- Key insight: `tools` frontmatter as allowlist; `mcpServers` frontmatter for server access.
5. [Claude Code Plugins Reference](https://code.claude.com/docs/en/plugins-reference) -- Key insight: Plugin MCP server integration behavior and namespacing.
6. [GitHub Issue #23149: Plugin MCP tool names exceed 64-char limit](https://github.com/anthropics/claude-code/issues/23149) -- Key insight: Plugin tool naming formula `mcp__plugin_{plugin}_{server}__{tool}`.
7. [GitHub Issue #15145: MCP servers incorrectly namespaced under plugin name](https://github.com/anthropics/claude-code/issues/15145) -- Key insight: Plugin prefix applies to all servers when plugin is installed (bug).
8. [GitHub Issue #2928: Wildcard permissions for MCP servers](https://github.com/anthropics/claude-code/issues/2928) -- Key insight: `mcp__context7` (bare name) is the correct permission form; wildcard not originally supported.
9. [GitHub Issue #3107: MCP wildcard permissions not honored](https://github.com/anthropics/claude-code/issues/3107) -- Key insight: Wildcards did not work; bare server name was the workaround.
10. [GitHub Issue #13077: --allowedTools wildcard for MCP tools](https://github.com/anthropics/claude-code/issues/13077) -- Key insight: CLI wildcard patterns silently failed for MCP tools.
11. [GitHub Issue #14730: Wildcard permissions matching fails](https://github.com/anthropics/claude-code/issues/14730) -- Key insight: Confirms wildcard bug across multiple Claude Code versions.
12. [Context7 GitHub Repository](https://github.com/upstash/context7) -- Key insight: Installation methods (CLI `claude mcp add` as standalone server, or `.mcp.json` configuration). See README.md "Getting Started" section for the `npx -y @upstash/context7-mcp@latest` installation command and MCP configuration examples.

---

## PS Integration

- **PS ID:** PROJ-030-bugs
- **Entry ID:** BUG-001
- **Entity File:** `projects/PROJ-030-bugs/work/bugs/BUG-001-memory-keeper-tool-name-mismatch/BUG-001-memory-keeper-tool-name-mismatch.md`
- **Topic:** Context7 MCP Tool Permission Model and Namespace Analysis
- **Artifact:** `projects/PROJ-030-bugs/research/context7-permission-model.md`
- **Confidence:** HIGH (0.85) -- Primary claims sourced from official documentation and confirmed via multiple GitHub issues. Limitations: (1) plugin naming formula derived from bug reports rather than official specification, (2) user-level settings (`~/.claude/settings.json`) were unreadable due to permission denial, preventing verification of whether Context7 is also configured as a standalone MCP server at user scope.
### Action Items

1. File BUG-002 for Context7 dual-namespace tool resolution failure (plugin prefix vs canonical name mismatch)
2. ps-architect: Evaluate migration options (user-scope standalone MCP server via `claude mcp add --scope user` vs project-scope `.mcp.json` configuration)
3. Update agent definitions and `TOOL_REGISTRY.yaml` per selected migration path
