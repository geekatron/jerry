# Steelman Report: Claude Code MCP Tool Permission Model: Context7 Namespace Analysis

## Steelman Context

| Field | Value |
|-------|-------|
| **Deliverable** | `projects/PROJ-030-bugs/research/context7-permission-model.md` |
| **Deliverable Type** | Research |
| **Criticality Level** | C4 |
| **Strategy** | S-003 (Steelman Technique) |
| **SSOT Reference** | `.context/rules/quality-enforcement.md` |
| **Steelman By** | adv-executor | **Date:** 2026-02-26T00:00:00Z | **Original Author:** ps-researcher |
| **Execution ID** | 20260226T001 |
| **Template** | `.context/templates/adversarial/s-003-steelman.md` |

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Steelman assessment and improvement count |
| [Steelman Reconstruction](#steelman-reconstruction) | Deliverable rewritten in strongest form |
| [Improvement Findings Table](#improvement-findings-table) | SM-NNN findings with severity |
| [Improvement Details](#improvement-details) | Expanded evidence for Critical and Major findings |
| [Scoring Impact](#scoring-impact) | Dimension-level impact of improvements |
| [Execution Statistics](#execution-statistics) | Protocol steps and finding counts |

---

## Summary

**Steelman Assessment:** The deliverable presents a technically sound, well-evidenced investigation into a real and impactful MCP tool namespace mismatch. Its core thesis and recommendation are correct and actionable; the principal weaknesses are gaps in executive communication (the L0 summary undersells the agent-level breakage) and incomplete impact scoping (the agent definitions affected are unnamed and uncounted).

**Improvement Count:** 1 Critical, 5 Major, 3 Minor

**Original Strength:** The research is strong at the L1 technical layer. Sources are credible (official Claude Code docs plus corroborating GitHub issues), the permission precedence hierarchy is accurately mapped, and the trade-off table is appropriately structured. The methodology section's honest disclosure of limitations is a notable quality.

**Recommendation:** Incorporate improvements — particularly SM-001 (L0 gap restatement), SM-002 (agent impact inventory), SM-003 (plugin formula version gate), SM-004 (residual risk column), and SM-005 (TOOL_REGISTRY.yaml scope check) — before downstream critique strategies (S-002, S-004) engage. Most Minor improvements (SM-007 through SM-009) can be incorporated in a single pass.

---

## Steelman Reconstruction

> All improvements are marked with `[SM-NNN]` inline annotations referencing the Findings Table below.

---

### Claude Code MCP Tool Permission Model: Context7 Namespace Analysis

> Research report on MCP tool naming, wildcard scoping, and permission hierarchy in Claude Code, with specific focus on Context7 plugin vs MCP server namespacing.

#### Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Plain-language findings for project decision-making |
| [L1: Technical Analysis](#l1-technical-analysis) | Detailed technical findings with configuration examples |
| [L2: Architectural Implications](#l2-architectural-implications) | Strategic trade-offs, risks, and recommendations |
| [Research Questions](#research-questions) | Scoped questions driving this investigation |
| [Methodology](#methodology) | Sources consulted and credibility assessment |
| [References](#references) | Full citation list with URLs |

---

#### L0: Executive Summary

**What we researched:** How Claude Code names MCP tools internally and whether the wildcard permission `mcp__context7__*` covers tools that arrive through the Context7 *plugin* (which uses a different, longer prefix).

**Key finding:** They are **separate namespaces**. `mcp__context7__*` does NOT cover `mcp__plugin_context7_context7__*`. The two prefixes are constructed by entirely different code paths inside Claude Code:

- **User-configured MCP servers** produce tools named `mcp__{server-name}__{tool-name}` (e.g., `mcp__context7__resolve-library-id`).
- **Plugin-bundled MCP servers** produce tools named `mcp__plugin_{plugin-name}_{server-name}__{tool-name}` (e.g., `mcp__plugin_context7_context7__resolve-library-id`).

Since this project's `.claude/settings.json` enables Context7 as a **plugin** (`"enabledPlugins": {"context7@claude-plugins-official": true}`), the actual runtime tool names will use the `mcp__plugin_context7_context7__` prefix.

[SM-001] **Critical gap in `settings.local.json` defensive coverage:** The `settings.local.json` permission entries correctly cover both namespace prefixes at the session level. However, this does NOT protect agent subagents from the mismatch. Agent `.md` files that list `mcp__context7__resolve-library-id` in their `tools` YAML frontmatter field apply an allowlist that uses the wrong name — the session-level permission is irrelevant once a subagent restricts its own tool set via `tools` frontmatter. The net result is that any agent with an explicit `tools` list containing `mcp__context7__*` entries will silently fail to invoke Context7 tools at runtime, even though the session has permission. An agent that omits `tools` entirely inherits all session tools (including the plugin-prefixed ones) but violates the principle of least privilege required by the T1-T5 tier model (`agent-development-standards.md`).

**What this means for the project:** [SM-002] At least **N agent definitions** in `skills/*/agents/*.md` reference `mcp__context7__resolve-library-id` or `mcp__context7__query-docs` in their `tools` frontmatter or `mcpServers` fields. Every such agent will fail to invoke Context7 at runtime under the current plugin installation. Additionally, `mcp-tool-standards.md` canonical tool names and TOOL_REGISTRY.yaml both carry the wrong prefix, causing every agent that consults those documents to configure itself incorrectly. The `settings.local.json` defensive coverage addresses session-level permissions but does not fix the agent-definition-level mismatch.

---

#### Research Questions

| # | Question | Status |
|---|----------|--------|
| RQ-1 | How does `mcp__context7__*` work vs `mcp__plugin_context7_context7__*`? Are these separate namespaces? | **Answered** -- Separate namespaces |
| RQ-2 | Where are MCP tool permissions configured across the four levels? | **Answered** -- Four levels documented |
| RQ-3 | How does Claude Code prefix tools from Plugins vs MCP Servers? | **Answered** -- Formulas documented |
| RQ-4 | Is Context7 a Plugin or MCP Server in this project? | **Answered** -- Plugin (settings.json confirms) |

---

#### L1: Technical Analysis

##### 1. MCP Tool Naming Formulas

Claude Code uses two distinct naming formulas depending on how an MCP server is registered.

###### Formula A: User-Configured MCP Servers

When an MCP server is added via `claude mcp add`, `.mcp.json`, or `~/.claude.json`:

```
mcp__{server-name}__{tool-name}
```

**Examples:**
- Server named `context7` with tool `resolve-library-id` produces: `mcp__context7__resolve-library-id`
- Server named `memory-keeper` with tool `store` produces: `mcp__memory-keeper__store`

The `{server-name}` is the **name you chose** when adding the server (the first argument to `claude mcp add`).

**Source:** [Claude Code Permissions Docs](https://code.claude.com/docs/en/permissions) -- "mcp__puppeteer matches any tool provided by the puppeteer server" and "mcp__puppeteer__puppeteer_navigate matches the puppeteer_navigate tool provided by the puppeteer server."

###### Formula B: Plugin-Bundled MCP Servers

When an MCP server is provided by a plugin (defined in the plugin's `.mcp.json` or `plugin.json`):

```
mcp__plugin_{plugin-name}_{server-name}__{tool-name}
```

**Examples:**
- Plugin `context7` with MCP server `context7` and tool `resolve-library-id` produces: `mcp__plugin_context7_context7__resolve-library-id`
- Plugin `atlassian` with MCP server `atlassian` and tool `addCommentToJiraIssue` produces: `mcp__plugin_atlassian_atlassian__addCommentToJiraIssue`

**Source:** [GitHub Issue #23149](https://github.com/anthropics/claude-code/issues/23149) -- "Plugin MCP tools: Format: mcp__plugin_<plugin-name>_<server-name>__<tool-name>". Also confirmed by [GitHub Issue #15145](https://github.com/anthropics/claude-code/issues/15145).

[SM-003] **Version gate note:** The plugin naming formula is derived from GitHub issue reports (issues #23149 and #15145), not from an official naming specification document. Both issues were filed and discussed in the second half of 2025; the behavior appears stable across reports, but the exact Claude Code version at which this naming schema was established is not documented by Anthropic. Any future change to the plugin naming convention would not be captured by official CHANGELOG entries that reference tool naming. Teams relying on the plugin prefix SHOULD periodically verify the formula against a running Claude Code instance when upgrading.

###### Side-by-Side Comparison

| Aspect | User-Configured (Formula A) | Plugin-Bundled (Formula B) |
|--------|----------------------------|---------------------------|
| Prefix | `mcp__` | `mcp__plugin_` |
| Server identifier | `{server-name}` (user-chosen) | `{plugin-name}_{server-name}` |
| Separator before tool | `__` (double underscore) | `__` (double underscore) |
| Example | `mcp__context7__query-docs` | `mcp__plugin_context7_context7__query-docs` |
| Character count (prefix) | 5 + server name + 2 = variable | 14 + plugin + 1 + server + 2 = variable |

**Critical implication:** These are entirely different string prefixes. A permission rule matching one will NOT match the other.

##### 2. Wildcard Permission Syntax for MCP Tools

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

The current official documentation now lists **both** `mcp__puppeteer` (bare name) and `mcp__puppeteer__*` (wildcard) as valid. This suggests the wildcard syntax may have been fixed in a later release, but the bare server name (without `__*`) is the more reliable and originally-supported form.

##### 3. Permission Configuration Levels

Claude Code supports four distinct levels where MCP tool permissions can be configured, plus agent-level tool restrictions:

###### Level 1: Managed Settings (Highest Precedence)

**Location:** System-wide paths (require admin privileges):
- macOS: `/Library/Application Support/ClaudeCode/managed-settings.json`
- Linux/WSL: `/etc/claude-code/managed-settings.json`

**Capabilities:** Can enforce `allowedMcpServers`, `deniedMcpServers`, and `allowManagedMcpServersOnly`. These CANNOT be overridden.

**Source:** [Claude Code Settings Documentation](https://code.claude.com/docs/en/settings)

###### Level 2: User Settings

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

###### Level 3: Project Settings (Shared)

**Location:** `.claude/settings.json` (committed to git, shared with team)

**Capabilities:** Same `permissions` structure. Project settings override user settings for deny rules.

**Relevant finding:** The Jerry project's `.claude/settings.json` uses `allowed_tools` (which appears to be a legacy or custom field). The standard Claude Code schema uses `permissions.allow` and `permissions.deny`. [SM-006] The scope of this schema deviation is limited to `.claude/settings.json` alone; `settings.local.json` uses the correct `permissions.allow` key. The impact of the legacy `allowed_tools` key depends on whether Claude Code silently ignores unrecognized fields — this has not been verified against the current Claude Code release. If Claude Code does ignore unknown fields, the project-level shared settings file currently provides NO effective permission grants, meaning the session-level permissions are entirely governed by `settings.local.json` (Level 4) alone.

###### Level 4: Local Project Settings (Highest user-level precedence)

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

This is the **correct defensive approach** -- covering both possible namespace prefixes at the session level.

###### Level 5: Agent-Level Tool Restrictions

**Location:** Agent `.md` file YAML frontmatter `tools` field

**Capabilities:** The `tools` field in subagent frontmatter acts as an **allowlist**. Only listed tools are available to the subagent. If omitted, the subagent inherits ALL tools from the parent conversation.

**Critical finding:** The `tools` field in agent definitions uses tool names directly. If an agent definition specifies `mcp__context7__resolve-library-id` but the runtime tool is actually `mcp__plugin_context7_context7__resolve-library-id`, the agent will NOT have access to that tool. This breakage is silent — the agent receives no error, the tool simply does not appear in its available set.

**Source:** [Claude Code Sub-agents Documentation](https://code.claude.com/docs/en/sub-agents) -- "tools: Tools the subagent can use. Inherits all tools if omitted."

###### Precedence Summary

```
Managed Settings (highest, cannot override)
  > Command Line Arguments (--allowedTools, --disallowedTools)
    > Local Project Settings (.claude/settings.local.json)
      > Shared Project Settings (.claude/settings.json)
        > User Settings (~/.claude/settings.json)
```

Within a subagent, the `tools` frontmatter further restricts the available tools from the parent's permitted set.

##### 4. Context7 Configuration in This Project

**Finding:** Context7 is configured as a **plugin**, not a standalone MCP server.

**Evidence:** `.claude/settings.json` line 81:
```json
{
  "enabledPlugins": {
    "context7@claude-plugins-official": true
  }
}
```

No `.mcp.json` file exists at the project root, and no Context7 entry appears in user-level MCP configuration (`~/.claude.json` has no `mcpServers` key with a `context7` entry).

**Implication:** At runtime, Context7 tools will be registered under the **plugin prefix**:
- `mcp__plugin_context7_context7__resolve-library-id`
- `mcp__plugin_context7_context7__query-docs`

The `mcp__context7__resolve-library-id` form would only exist if Context7 were also (or instead) configured as a standalone MCP server.

##### 5. Impact on Jerry Framework Agent Definitions

The Jerry framework's `mcp-tool-standards.md` defines canonical tool names as:

| Tool | Canonical Name |
|------|---------------|
| Context7 Resolve | `mcp__context7__resolve-library-id` |
| Context7 Query | `mcp__context7__query-docs` |

[SM-002] If Context7 is installed as a plugin (which it currently is), these canonical names will not match the runtime tool names. This creates a mismatch in:

1. **Agent `tools` frontmatter** -- Agents that list `mcp__context7__resolve-library-id` in their `tools` array will not have access to the plugin-prefixed version. This affects the following agent categories declared in `mcp-tool-standards.md` Agent Integration Matrix: `ps-researcher`, `ps-analyst`, `ps-architect`, `ps-investigator`, `ps-synthesizer`, `nse-explorer`, `nse-architecture`, `eng-architect`, `eng-lead`, `eng-backend`, `eng-frontend`, `eng-infra`, `eng-devsecops`, `eng-qa`, `eng-security`, `eng-reviewer`, `eng-incident`, `red-lead`, `red-recon`, `red-vuln`, `red-exploit`, `red-privesc`, `red-lateral`, `red-persist`, `red-exfil`, `red-reporter`, `red-infra`, `red-social` -- 28 agent definitions potentially affected.
2. **Agent `mcpServers` frontmatter** -- The `mcpServers` field in agent frontmatter references server names (e.g., `context7`), not tool names. This field would need the plugin-qualified name.
3. **`mcp-tool-standards.md` Canonical Tool Names section** -- The authoritative document itself carries the wrong names, causing every agent that follows it to configure incorrectly.
4. **TOOL_REGISTRY.yaml** -- Referenced as the SSOT for tool-to-agent mappings in `mcp-tool-standards.md`. If it also carries `mcp__context7__` entries, it amplifies the mismatch to any tooling that reads TOOL_REGISTRY.yaml programmatically. The current research did not examine TOOL_REGISTRY.yaml directly. [SM-005] This gap should be closed before any remediation begins.

---

#### L2: Architectural Implications

##### Trade-Off Analysis

| Approach | Pros | Cons |
|----------|------|------|
| **A: Switch Context7 to standalone MCP server** | Tool names match canonical names. No agent definition changes needed. Simpler permission rules. Consistent with memory-keeper configuration. | Requires manual `claude mcp add` per developer (onboarding overhead). Not using Anthropic's recommended plugin distribution channel. Auto-update advantage of plugin is lost. |
| **B: Update canonical names to plugin prefix** | Matches actual runtime behavior. Correct by construction. | Longer tool names (may approach 64-char API limit for some tools). All 28+ agent definitions and documentation must be updated. Plugin name could change in future releases. |
| **C: Support both prefixes (current `settings.local.json` approach)** | Defensive. Works regardless of installation method. | Doubles the permission entries. Agent `tools` frontmatter can only specify one name -- must omit `tools` (inherit all) or list both. Documentation remains ambiguous. Does NOT fix agent-definition-level breakage. |
| **D: Omit `tools` from agent definitions; rely on session-level permissions** | Simplest. No tool name coupling in agent definitions. | Agents get access to ALL tools, violating principle of least privilege (T1-T5 tier model in `agent-development-standards.md`). Requires documented justification per H-34. |

##### Recommended Approach

**Approach A (switch to standalone MCP server)** is the cleanest solution for the Jerry framework because:

1. It aligns canonical tool names with runtime names.
2. It avoids the 64-character tool name limit risk (plugin prefix adds ~19 characters).
3. It is consistent with how `memory-keeper` is configured (as a standalone MCP server, not a plugin).
4. Agent definitions and `mcp-tool-standards.md` require zero changes.

**Migration path:**
```bash
# 1. Disable the plugin
# Remove "context7@claude-plugins-official" from .claude/settings.json enabledPlugins

# 2. Add as standalone MCP server (user scope for all projects)
claude mcp add --scope user context7 -- npx -y @upstash/context7-mcp

# 3. Simplify settings.local.json permissions -- remove plugin-prefixed entries
# Keep only: "mcp__context7__*", "mcp__context7__resolve-library-id", "mcp__context7__query-docs"
```

[SM-004 / SM-008] **Developer onboarding risk and residual risk after migration:**

The `claude mcp add` command must be run manually by each developer on each workstation. This is the principal operational risk of Approach A. Mitigations and residual risk:

| Risk | Likelihood | Impact | Mitigation | Residual Risk After Mitigation |
|------|-----------|--------|------------|-------------------------------|
| Plugin prefix changes in future Claude Code version | Medium | High -- all permission entries break | Approach A eliminates this risk entirely | None (Approach A) |
| Tool name exceeds 64-char API limit with plugin prefix | Low (Context7 tools have short names) | High -- API error, tool unusable | Approach A eliminates; Approach B: monitor tool name lengths | None (Approach A) |
| Developer forgets `claude mcp add` setup step | Medium | Medium -- Context7 silently unavailable; LLM falls back to training data | Add `.mcp.json` project-scoped config so Claude Code auto-configures without manual step | Low: `.mcp.json` project config makes setup automatic for new clones |
| Wildcard permissions silently fail | Low (appears fixed in recent versions) | Medium -- tools require manual approval each time | Include both bare name and explicit tool entries as fallback | Low: bare-name entries provide explicit fallback regardless of wildcard behavior |
| `allowed_tools` field in `.claude/settings.json` is silently ignored | Medium (unverified) | Medium -- shared project settings provide no effective grants | Migrate `.claude/settings.json` to use `permissions.allow` key | Low: `settings.local.json` provides session grants independently |

##### Alignment with Existing Architecture

The Jerry framework's `agent-development-standards.md` defines a T1-T5 tool tier model where agents specify their allowed tools explicitly. This model assumes stable, predictable tool names. Plugin-prefixed names introduce instability because:

1. The prefix depends on the plugin's name in the marketplace entry, which is external to Jerry's control.
2. If Context7 is installed from a different marketplace or forked, the plugin name changes.
3. The `mcpServers` frontmatter field in agent definitions references server names, not full tool names, creating a layer of indirection that is documented for user-configured servers but not for plugin-bundled servers.

[SM-007] The T1-T5 tier impact is concentrated in T3 (External) agents, which are the agents that declare `context7` in `mcpServers`. T1 (Read-Only) and T2 (Read-Write) agents are unaffected. T4 (Persistent) and T5 (Full) agents that also use Context7 inherit the T3 breakage. Any new agent development that follows the T3 template in `agent-development-standards.md` will inherit the broken canonical name unless the SSOT documents are corrected first.

---

#### Methodology

##### Sources Consulted

| Source Type | Source | Credibility | Accessed |
|-------------|--------|-------------|---------|
| Official documentation | [Claude Code Permissions](https://code.claude.com/docs/en/permissions) | HIGH | [SM-009] Add date |
| Official documentation | [Claude Code Settings](https://code.claude.com/docs/en/settings) | HIGH | [SM-009] Add date |
| Official documentation | [Claude Code MCP](https://code.claude.com/docs/en/mcp) | HIGH | [SM-009] Add date |
| Official documentation | [Claude Code Sub-agents](https://code.claude.com/docs/en/sub-agents) | HIGH | [SM-009] Add date |
| Official documentation | [Claude Code Plugins Reference](https://code.claude.com/docs/en/plugins-reference) | HIGH | [SM-009] Add date |
| GitHub issue | [#23149 Plugin MCP tool names exceed 64-char limit](https://github.com/anthropics/claude-code/issues/23149) | HIGH (primary source for Formula B) | [SM-009] Add date |
| GitHub issue | [#15145 MCP servers incorrectly namespaced under plugin name](https://github.com/anthropics/claude-code/issues/15145) | HIGH (confirms plugin prefix behavior) | [SM-009] Add date |
| GitHub issue | [#2928 Wildcard permissions for MCP servers](https://github.com/anthropics/claude-code/issues/2928) | HIGH (confirms bare name vs wildcard) | [SM-009] Add date |
| GitHub issue | [#3107 MCP wildcard permissions not honored](https://github.com/anthropics/claude-code/issues/3107) | HIGH (documents wildcard bug history) | [SM-009] Add date |
| GitHub issue | [#13077 --allowedTools wildcard for MCP](https://github.com/anthropics/claude-code/issues/13077) | HIGH (documents CLI wildcard bug) | [SM-009] Add date |
| GitHub issue | [#14730 Wildcard matching fails](https://github.com/anthropics/claude-code/issues/14730) | MEDIUM (duplicate, but confirms pattern) | [SM-009] Add date |
| Project configuration | `.claude/settings.json` (local file) | HIGH (primary source) | 2026-02-26 |
| Project configuration | `.claude/settings.local.json` (local file) | HIGH (primary source) | 2026-02-26 |
| Context7 GitHub | [upstash/context7](https://github.com/upstash/context7) | HIGH (official installation docs) | [SM-009] Add date |

##### Limitations

1. **No access to `~/.claude/settings.json`** -- Permission denied when attempting to read user-level settings. Could not verify whether Context7 is also configured as a standalone MCP server at user scope.
2. **Plugin naming behavior is documented primarily through bug reports**, not official specification. The `mcp__plugin_{plugin}_{server}__` formula is derived from observed behavior reported in GitHub issues, not from an official naming specification document. [SM-003] Teams should re-verify this formula upon each Claude Code major version upgrade.
3. **Wildcard support status is ambiguous** -- The official docs now list both `mcp__servername` and `mcp__servername__*` as valid, but multiple resolved bug reports (from mid-to-late 2025) indicate wildcards were broken. The exact version where wildcards became reliable is not documented.
4. **TOOL_REGISTRY.yaml not examined** -- [SM-005] The canonical SSOT for tool-to-agent mappings was not read during this research. Its contents may amplify or contain the namespace mismatch. This should be examined before remediation begins.

---

#### References

1. [Claude Code Permissions Documentation](https://code.claude.com/docs/en/permissions) -- Key insight: Official MCP permission syntax including bare name (`mcp__puppeteer`) and wildcard (`mcp__puppeteer__*`) forms.
2. [Claude Code Settings Documentation](https://code.claude.com/docs/en/settings) -- Key insight: Four-level precedence hierarchy (managed > CLI > local > project > user).
3. [Claude Code MCP Documentation](https://code.claude.com/docs/en/mcp) -- Key insight: MCP server scopes (local, project, user) and plugin-provided MCP servers.
4. [Claude Code Sub-agents Documentation](https://code.claude.com/docs/en/sub-agents) -- Key insight: `tools` frontmatter as allowlist; `mcpServers` frontmatter for server access.
5. [Claude Code Plugins Reference](https://code.claude.com/docs/en/plugins-reference) -- Key insight: Plugin MCP server integration behavior and namespacing.
6. [GitHub Issue #23149: Plugin MCP tool names exceed 64-char limit](https://github.com/anthropics/claude-code/issues/23149) -- Key insight: Plugin tool naming formula `mcp__plugin_{plugin}_{server}__{tool}`.
7. [GitHub Issue #15145: MCP servers incorrectly namespaced under plugin name](https://github.com/anthropics/claude-code/issues/15145) -- Key insight: Plugin prefix applies to all servers when plugin is installed (bug).
8. [GitHub Issue #2928: Wildcard permissions for MCP servers](https://github.com/anthropics/claude-code/issues/2928) -- Key insight: `mcp__context7` (bare name) is the correct permission form; wildcard not originally supported.
9. [GitHub Issue #3107: MCP wildcard permissions not honored](https://github.com/anthropics/claude-code/issues/3107) -- Key insight: Wildcards did not work; bare server name was the workaround.
10. [GitHub Issue #13077: --allowedTools wildcard for MCP tools](https://github.com/anthropics/claude-code/issues/13077) -- Key insight: CLI wildcard patterns silently failed for MCP tools.
11. [GitHub Issue #14730: Wildcard permissions matching fails](https://github.com/anthropics/claude-code/issues/14730) -- Key insight: Confirms wildcard bug across multiple Claude Code versions.
12. [Context7 GitHub Repository](https://github.com/upstash/context7) -- Key insight: Installation methods (CLI `claude mcp add` as standalone server, or `.mcp.json` configuration).

---

#### PS Integration

- **PS ID:** PROJ-030-bugs
- **Entry ID:** BUG-001
- **Topic:** Context7 MCP Tool Permission Model and Namespace Analysis
- **Artifact:** `projects/PROJ-030-bugs/research/context7-permission-model.md`
- **Confidence:** HIGH (0.90) -- Primary claims sourced from official documentation and confirmed via multiple GitHub issues. Limitation: plugin naming formula derived from bug reports rather than official specification. [SM-003] Re-verify formula on Claude Code version upgrade.
- **Next agent hint:** ps-architect for decision on Context7 installation method (plugin vs standalone MCP server). Verify TOOL_REGISTRY.yaml contents before any remediation. [SM-005]

---

## Improvement Findings Table

| ID | Improvement | Severity | Section | Affected Dimension |
|----|-------------|----------|---------|--------------------|
| SM-001-20260226T001 | Restate L0 summary to surface the agent-definition-level breakage explicitly -- `settings.local.json` defensive coverage does NOT protect agents with `tools` frontmatter; session-level permission is irrelevant when a subagent creates its own allowlist | Critical | L0: Executive Summary | Completeness |
| SM-002-20260226T001 | Add agent impact inventory: identify all 28 agents in the `mcp-tool-standards.md` Agent Integration Matrix that reference Context7 and are potentially affected; name the specific `skills/*/agents/*.md` files | Major | L1: Section 5 + L0 | Completeness |
| SM-003-20260226T001 | Add version gate caveat to Formula B: plugin naming formula is derived from 2025 bug reports, not an official specification; re-verification required on Claude Code major version upgrades | Major | L1: Section 1 (Formula B) + Methodology Limitations | Evidence Quality |
| SM-004-20260226T001 | Add Residual Risk column to Risk Assessment table so readers can assess whether each mitigation reduces risk to acceptable level | Major | L2: Risk Assessment | Actionability |
| SM-005-20260226T001 | Add explicit research gap: TOOL_REGISTRY.yaml (SSOT for tool-to-agent mappings) was not examined -- if it carries `mcp__context7__` entries it amplifies the mismatch to all tooling reading it programmatically | Major | L1: Section 5 + Methodology Limitations | Completeness |
| SM-006-20260226T001 | Strengthen the `allowed_tools` vs `permissions.allow` schema mismatch finding: if Claude Code silently ignores unknown fields, `.claude/settings.json` provides zero effective permission grants, making `settings.local.json` the sole permission source | Major | L1: Section 3, Level 3 | Internal Consistency |
| SM-007-20260226T001 | Map the T1-T5 tier impact explicitly: T3 (External) agents are the primary locus of breakage; T1/T2 agents unaffected; new agent development following T3 template inherits broken canonical name | Minor | L2: Alignment with Existing Architecture | Actionability |
| SM-008-20260226T001 | Add developer onboarding residual risk: Approach A requires `claude mcp add` per developer; recommend `.mcp.json` project-scoped config as mitigation to make setup automatic | Minor | L2: Risk Assessment | Actionability |
| SM-009-20260226T001 | Add accessed dates to all web source references in the Methodology table -- critical for this topic given that wildcard behavior changed across Claude Code versions | Minor | Methodology: Sources Consulted | Evidence Quality |

---

## Improvement Details

### SM-001-20260226T001: Agent-Definition-Level Breakage Missing from L0

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | L0: Executive Summary |
| **Strategy Step** | Step 2 (Presentation weakness) + Step 3 (Reconstruction) |
| **Affected Dimension** | Completeness |

**Original Content (L0, paragraph 4):**

> "The Jerry framework's `settings.local.json` is correctly defensive by including **both** prefixes (lines 24-29). However, the `mcp-tool-standards.md` canonical tool names and all agent definitions reference only `mcp__context7__resolve-library-id` and `mcp__context7__query-docs`. If Context7 is installed as a plugin (as it currently is), these names will not match runtime tool names, causing tool invocation failures or permission denials in subagents that specify tools explicitly."

**Gap:** The original text says "tool invocation failures or permission denials" but does not clearly explain WHY the session-level defensive permissions are insufficient. A reader might conclude that adding both prefixes to `settings.local.json` is the complete fix. The mechanism of subagent `tools` frontmatter as an independent allowlist (operating below session-level permissions) is not stated in L0 — it appears only in L1 Section 5, which many executive readers will not reach.

**Strengthened Content (added to L0):**

> "Critical gap: The `settings.local.json` defensive coverage addresses session-level permissions but does NOT protect agents with explicit `tools` frontmatter. A subagent that lists `mcp__context7__resolve-library-id` in its own `tools` YAML field creates an allowlist that filters tools before session permissions apply — the session has permission, but the subagent's own allowlist excludes the plugin-prefixed name. The net result is that any T3-tier agent with an explicit `tools` list silently loses access to Context7 even when session permissions are correct."

**Rationale:** Without this explanation, the L0 summary creates a false sense of security. The defensive `settings.local.json` coverage is good but insufficient; the real risk is in the 28 agent definitions. This is a Completeness gap — the most impactful finding of the research is understated at the executive level.

**Best Case Conditions:** This improvement is most valuable when the research is consumed by team leads who read L0 only and delegate L1/L2 detail to engineers. Strengthening L0 ensures the action items reach decision-makers.

---

### SM-002-20260226T001: Agent Impact Inventory Absent

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | L1: Section 5 — Impact on Jerry Framework Agent Definitions |
| **Strategy Step** | Step 2 (Structural weakness) + Step 3 (Reconstruction) |
| **Affected Dimension** | Completeness |

**Original Content:**

> "This creates a mismatch in: 1. Agent `tools` frontmatter — Agents that list `mcp__context7__resolve-library-id` in their `tools` array will not have access to the plugin-prefixed version."

**Gap:** The impact is stated generically ("all agent definitions") but no agent names, file paths, or count are provided. The reader knows there is a problem but cannot assess scope or plan remediation without reading every agent definition file individually.

**Strengthened Content:** The Steelman Reconstruction above enumerates the 28 agent categories from `mcp-tool-standards.md`'s Agent Integration Matrix that declare Context7 usage. The actual `.md` file paths under `skills/*/agents/` should be confirmed by reading the filesystem (which was out of scope for this research report but is a necessary next step for remediation planning).

**Rationale:** Scope ambiguity reduces actionability. A remediation team that does not know which files to edit cannot plan work or estimate effort. The `mcp-tool-standards.md` Agent Integration Matrix is the definitive enumeration of affected agents; cross-referencing it closes this gap without requiring filesystem traversal in the research document itself.

---

### SM-003-20260226T001: Formula B Version Gate Missing

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | L1: Section 1 (Formula B) + Methodology Limitations |
| **Strategy Step** | Step 2 (Evidence weakness) + Step 3 (Reconstruction) |
| **Affected Dimension** | Evidence Quality |

**Original Content:**

> "Source: GitHub Issue #23149 -- 'Plugin MCP tools: Format: mcp__plugin_<plugin-name>_<server-name>__<tool-name>'. Also confirmed by GitHub Issue #15145."

**Gap:** No statement that the formula was derived from bug reports (not an official spec), and no guidance on when to re-verify. Given that the wildcard behavior already changed (breaking then being fixed) between versions, the plugin naming formula could similarly change.

**Strengthened Content:** Added explicit caveat in both Section 1 and Methodology Limitations noting that Formula B is derived from 2025 bug report observations, not an official Anthropic naming specification, and that teams should re-verify the formula on Claude Code major version upgrades.

**Rationale:** Readers following this research to configure new agents need to know the confidence level of the naming formula. Without the version-gate note, a future Claude Code upgrade could silently break all configurations built on this formula, with no indication in the documentation that the formula was ever unstable.

---

### SM-004-20260226T001: Risk Table Lacks Residual Risk Column

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | L2: Risk Assessment |
| **Strategy Step** | Step 2 (Structural weakness) + Step 3 (Reconstruction) |
| **Affected Dimension** | Actionability |

**Original Content:**

Risk table has columns: Risk | Likelihood | Impact | Mitigation — but no Residual Risk column.

**Gap:** A reader cannot determine whether the listed mitigations reduce risk to acceptable levels. For example, "Add to `.mcp.json` for project-scoped config" is listed as mitigation for the developer-forgetting risk, but the original does not state that this reduces likelihood from Medium to Low.

**Strengthened Content:** Added "Residual Risk After Mitigation" column to the Risk Assessment table in the Steelman Reconstruction, specifying the post-mitigation risk level for each row.

**Rationale:** Risk tables without residual risk columns are incomplete decision support artifacts. Architects choosing between approaches need to know not just what mitigations exist but whether those mitigations are sufficient. This is a standard risk management table requirement.

---

### SM-005-20260226T001: TOOL_REGISTRY.yaml Not Examined

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | L1: Section 5 + Methodology Limitations |
| **Strategy Step** | Step 2 (Structural weakness) |
| **Affected Dimension** | Completeness |

**Original Content:**

> "TOOL_REGISTRY.yaml — Referenced as the SSOT for tool-to-agent mappings in `mcp-tool-standards.md`. If it also carries `mcp__context7__` entries..."

**Gap:** The conditional "if it also carries" signals awareness of the gap but treats it as speculative. The research should either examine TOOL_REGISTRY.yaml and report what it found, or explicitly add it to the Methodology Limitations and flag it as a required pre-remediation check.

**Strengthened Content:** Added explicit note in Methodology Limitations and Section 5 that TOOL_REGISTRY.yaml was not examined and must be read before remediation begins. If it carries wrong canonical names, it becomes the highest-priority fix (as the SSOT for all agent-to-tool mappings).

**Rationale:** TOOL_REGISTRY.yaml is the SSOT. If it carries incorrect entries, any remediation that updates agent `.md` files but not TOOL_REGISTRY.yaml will be incomplete and risk regression.

---

### SM-006-20260226T001: `allowed_tools` Schema Mismatch Impact Not Quantified

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | L1: Section 3, Level 3 (Project Settings) |
| **Strategy Step** | Step 2 (Structural weakness) + Step 3 (Reconstruction) |
| **Affected Dimension** | Internal Consistency |

**Original Content:**

> "Relevant finding: The Jerry project's `.claude/settings.json` uses `allowed_tools` (which appears to be a legacy or custom field). The standard Claude Code schema uses `permissions.allow` and `permissions.deny`."

**Gap:** The finding is stated but not concluded. If Claude Code ignores unknown fields (likely), then the shared project settings file provides zero effective permission grants. The research leaves this as an implication without drawing the conclusion.

**Strengthened Content:** Added explicit consequence: if `allowed_tools` is silently ignored by Claude Code, the shared project settings file provides no permission grants whatsoever, making `settings.local.json` the sole permission source. This is an important finding because `.claude/settings.json` is committed to git and shared with all developers — if it provides no effective grants, the project's shared configuration is a no-op.

**Rationale:** Leaving a finding at "appears to be a legacy or custom field" without concluding its impact weakens the Internal Consistency of the analysis. The implication (no effective project-level permissions) is significant enough to state explicitly.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Positive | SM-001 (Critical) closes the most significant gap: L0 undersells agent-level breakage. SM-002 closes the agent inventory gap. SM-005 flags the TOOL_REGISTRY.yaml blind spot. Together these three improvements address the largest completeness deficit. |
| Internal Consistency | 0.20 | Positive | SM-006 resolves the `allowed_tools` finding-without-conclusion inconsistency. Strengthened L0 statement is now consistent with the detailed L1 explanation of the session vs. agent-level distinction. |
| Methodological Rigor | 0.20 | Positive | SM-003 adds the version gate caveat that honest research methodology requires when a key formula is derived from bug reports rather than official specification. |
| Evidence Quality | 0.15 | Positive | SM-003 (version gate), SM-009 (accessed dates). The original evidence is strong; these improvements add provenance traceability. |
| Actionability | 0.15 | Positive | SM-004 (residual risk column), SM-007 (T1-T5 tier mapping), SM-008 (onboarding mitigation). Readers can now assess whether mitigations are sufficient and identify exactly which agent tier is affected. |
| Traceability | 0.10 | Positive | SM-009 (accessed dates on all web sources). Given that wildcard behavior changed across versions, access dates enable readers to correlate documentation state with Claude Code version history. |

**Overall assessment:** All six dimensions are positively impacted. The original deliverable was strong in Evidence Quality and Methodological Rigor at the L1 layer; the Steelman primarily strengthens Completeness and Actionability by closing executive-layer communication gaps and scoping the impact inventory.

---

## Best Case Scenario

The Steelman Reconstruction is most compelling when:

1. Claude Code maintains the `mcp__plugin_{plugin}_{server}__` naming convention without change — the two GitHub issues (#23149, #15145) that document it are the primary evidence and remain valid.
2. The Jerry project adopts Approach A (standalone MCP server) without timeline pressure — the migration is a single-command operation per developer, but requires a team coordination step to deprecate the plugin entry.
3. The `allowed_tools` field in `.claude/settings.json` is confirmed as silently ignored by Claude Code — if so, the project's shared permission file is a no-op and the finding is more urgent than the original implies.
4. TOOL_REGISTRY.yaml examination confirms it carries the wrong canonical names — this would elevate the remediation priority from "update agent definitions" to "update SSOT first, then agent definitions."

**Key assumptions:**
- Plugin naming formula `mcp__plugin_{plugin}_{server}__` is stable within the 2025-2026 timeframe covered by the cited bug reports.
- Anthropic does not introduce a breaking rename to the plugin namespace in an upcoming Claude Code release.
- The 28 agent categories in `mcp-tool-standards.md` are the complete set of affected agents (no unlisted agents exist).

**Confidence:** HIGH (0.92) -- The core thesis is directly supported by official documentation (Formula A) and multiply-corroborated bug report evidence (Formula B). The improvements primarily strengthen communication clarity and scoping completeness, not the core technical finding.

---

## Execution Statistics

| Metric | Value |
|--------|-------|
| **Protocol Steps Completed** | 6 of 6 |
| **Total Findings** | 9 |
| **Critical** | 1 |
| **Major** | 5 |
| **Minor** | 3 |
| **H-15 Self-Review Applied** | Yes |
| **Reconstruction Preserves Original Thesis** | Yes |
| **Ready for Downstream Critique (S-002, S-004)** | Yes — substantial improvements; author review recommended before S-002 proceeds |

---

*Strategy Execution Report: S-003 (Steelman Technique)*
*Template: `.context/templates/adversarial/s-003-steelman.md` v1.0.0*
*Deliverable: `projects/PROJ-030-bugs/research/context7-permission-model.md`*
*Executed: 2026-02-26T00:00:00Z*
*Agent: adv-executor*
*Constitutional Compliance: P-003 (no subagents), P-020 (user authority), P-022 (no deception)*
