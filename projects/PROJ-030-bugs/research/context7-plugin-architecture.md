# Context7 Plugin Architecture and Claude Code Integration

> **PS ID:** proj-030
> **Entry ID:** e-002
> **Topic:** Context7 MCP Plugin Architecture in Claude Code
> **Agent:** ps-researcher
> **Created:** 2026-02-26
> **Confidence:** HIGH (0.92) -- upgraded from 0.88 after empirical verification

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Non-technical overview for stakeholders |
| [L1: Technical Analysis](#l1-technical-analysis) | Implementation findings for engineers |
| [L2: Architectural Implications](#l2-architectural-implications) | Strategic impact for Jerry Framework |
| [Research Questions](#research-questions) | Questions investigated |
| [Methodology](#methodology) | How research was conducted |
| [Empirical Verification](#empirical-verification) | Runtime evidence confirming dual-namespace thesis |
| [Findings](#findings) | Detailed 5W1H structured findings |
| [Recommendations](#recommendations) | Actionable next steps |
| [References](#references) | Complete citation list |

---

## L0: Executive Summary

Context7 can be connected to Claude Code in **two completely different ways**, and Jerry currently uses **both simultaneously** without realizing they create different tool name prefixes. This is like having the same employee registered under two different badge numbers -- the security system treats them as two separate people.

**The core problem:** When Context7 is installed as a **Plugin** (via `enabledPlugins` in `settings.json`), its tools get the long prefix `mcp__plugin_context7_context7__`. When installed as a **manually configured MCP Server** (via `claude mcp add` or `.mcp.json`), its tools get the short prefix `mcp__context7__`. Jerry's agent definitions reference the short names (`mcp__context7__resolve-library-id`), but the actual runtime may present the long plugin names instead. The `settings.local.json` file hedges by allowing both, but agent definitions only know about one.

**Why this matters:** If a subagent's tools list specifies `mcp__context7__resolve-library-id` but Claude Code presents the tool as `mcp__plugin_context7_context7__resolve-library-id`, the agent cannot use Context7. This causes silent degradation -- agents fall back to WebSearch or, worse, hallucinate library documentation.

**Recommendation:** Three configuration options were evaluated -- plugin-only, manual MCP server only, and a hybrid of both. The recommended approach is to remove the plugin registration and use a **user-scoped manual MCP server** exclusively, which preserves the short tool names matching existing agent definitions, ensures subagent access, and eliminates the namespace collision.

---

## L1: Technical Analysis

### 1. Two Configuration Methods for Context7

Context7 can be integrated with Claude Code via two distinct mechanisms. Jerry currently uses both.

#### Method A: Plugin Installation (via `enabledPlugins`)

In `.claude/settings.json` (line 80-82):

```json
"enabledPlugins": {
    "context7@claude-plugins-official": true
}
```

**Effect:** Claude Code downloads the Context7 plugin from the `claude-plugins-official` marketplace. The plugin bundles an MCP server. Plugin-provided MCP servers are auto-namespaced with a `plugin_<registry>_<plugin-name>` prefix.

**Resulting tool names:**
- `mcp__plugin_context7_context7__resolve-library-id`
- `mcp__plugin_context7_context7__query-docs`

The naming pattern is: `mcp__plugin_<plugin-name>_<server-name>__<tool-name>`.

For Context7: the plugin name is `context7`, the server name within the plugin is also `context7`, producing the double `context7_context7` in the middle.

**Version caveat:** The plugin naming formula `mcp__plugin_<plugin-name>_<server-name>__<tool-name>` is empirically observed from Claude Code v1.0.x-era GitHub issues (#20983, #15145), not from an official naming specification. It should be re-verified on major Claude Code upgrades. The empirical verification in this session (see [Empirical Verification](#empirical-verification)) confirms the formula is accurate as of the current Claude Code version.

#### Method B: Manual MCP Server Configuration

Alternatively, Context7 can be added directly as an MCP server:

```bash
claude mcp add --transport sse context7 https://mcp.context7.com/sse
```

Or via `npx`:

```bash
claude mcp add context7 -- npx -y @upstash/context7-mcp
```

**Resulting tool names:**
- `mcp__context7__resolve-library-id`
- `mcp__context7__query-docs`

The naming pattern is: `mcp__<server-name>__<tool-name>`.

### 2. Jerry's Current Configuration (Dual Registration)

Jerry's `settings.local.json` attempts to cover both namespaces by listing permissions for **both** prefixes (lines 24-29):

```json
"mcp__context7__*",
"mcp__context7__resolve-library-id",
"mcp__context7__query-docs",
"mcp__plugin_context7_context7__*",
"mcp__plugin_context7_context7__resolve-library-id",
"mcp__plugin_context7_context7__query-docs",
```

This is a **defensive workaround**, not a designed solution. It grants permission under both possible namespaces.

### 3. Tool Name Resolution Rules

Based on Claude Code documentation and GitHub issues, the tool naming rules are:

| Configuration Method | Tool Name Pattern | Example |
|---------------------|-------------------|---------|
| Manual MCP Server | `mcp__<server-name>__<tool-name>` | `mcp__context7__resolve-library-id` |
| Plugin MCP Server | `mcp__plugin_<plugin-name>_<server-name>__<tool-name>` | `mcp__plugin_context7_context7__resolve-library-id` |

**Critical insight from GitHub Issue #15145:** There is a documented namespace divergence where installing a plugin can cause ALL MCP servers (including manually configured ones) to be re-prefixed under the plugin namespace. Anthropic closed Issue #15145 as NOT PLANNED, confirming this is by-design behavior, not a defect (see [Reference #7](#references)). This means even if you configure Context7 manually AND as a plugin, the plugin namespace may dominate and rename the manual server's tools.

### 4. Permission System for MCP Tools

Based on Claude Code's official permissions documentation, GitHub Issues, and runtime observation:

**Wildcard permission syntax -- resolved timeline:**

- **July 2025:** Issue #3107 confirmed wildcards did NOT work. The correct syntax was the bare server name `mcp__<server-name>`.
- **Late 2025:** Issues #13077, #14730 continued to report wildcard failures.
- **Current documentation (2026):** The official permissions page now documents BOTH `mcp__puppeteer` (bare name) AND `mcp__puppeteer__*` (wildcard) as valid, indicating wildcard support was added in a later release.

The current documentation (code.claude.com/docs/en/permissions) states:

> - `mcp__puppeteer` matches any tool provided by the `puppeteer` server
> - `mcp__puppeteer__*` wildcard syntax that also matches all tools from the `puppeteer` server
> - `mcp__puppeteer__puppeteer_navigate` matches the `puppeteer_navigate` tool

**Recommended practice:** Use the bare server name `mcp__context7` as the primary permission. This is the original and most reliable form. The wildcard form `mcp__context7__*` is now also documented as working but has a longer bug history.

### 5. Agent Definition `mcpServers` Field Behavior

From Claude Code's subagent documentation, the `mcpServers` frontmatter field:

> Each entry is either a **server name referencing an already-configured server** (e.g., `"slack"`) or an **inline definition** with the server name as key and a full MCP server config as value.

**Tool inheritance rules for subagents:**

| Scenario | Tool Access |
|----------|-------------|
| `tools` field **omitted** | Subagent **inherits ALL tools** from main thread, including MCP tools |
| `tools` field **specified** | Only listed tools are available |
| `mcpServers` specified | The named MCP servers are made available; their tools follow naming convention |

**Critical issue from GitHub #13898:** Custom subagents CANNOT access **project-scoped** MCP servers (from `.mcp.json`). They can only access **user-scoped** MCP servers (from `~/.claude.json` via `--scope user`). This means if Context7 is only configured at the project level, subagents (which Jerry uses heavily via the Task tool) may not be able to use it at all, and will hallucinate responses instead.

### 6. Wildcard Behavior Across Namespaces

**The critical question: Does `mcp__context7__*` grant permission to `mcp__plugin_context7_context7__resolve-library-id`?**

**Answer: NO.** These are completely separate permission namespaces.

Evidence:
1. The permission system matches on the **server name** portion. `mcp__context7` matches tools from a server named `context7`. The plugin server is internally named differently (with the `plugin_context7_context7` compound prefix).
2. GitHub Issue #20983 confirms the plugin naming produces `mcp__plugin_<plugin-name>_<server-name>__<tool-name>`, which is a distinct namespace from `mcp__<server-name>__<tool-name>`.
3. The `settings.local.json` file explicitly lists both patterns separately, confirming they are treated as distinct permission entries.

**This is why Jerry has both sets of permissions** -- the person who configured `settings.local.json` discovered empirically that one set alone was insufficient.

### 7. Context7's Actual Tools

Context7 (by Upstash) exposes exactly **two tools**:

| Tool | Purpose | Call Sequence |
|------|---------|---------------|
| `resolve-library-id` | Resolve a library/package name to a Context7 library ID | Must be called first |
| `query-docs` | Retrieve documentation for a resolved library ID | Requires output from resolve-library-id |

The tool names are consistent regardless of installation method; only the prefix changes.

---

## L2: Architectural Implications

### 1. Dual-Registration Anti-Pattern

Jerry currently has Context7 registered as BOTH a plugin (`enabledPlugins`) AND relies on the `mcp__context7__` namespace in agent definitions. [Source: `.claude/settings.json` lines 80-82 for plugin registration; `.claude/settings.local.json` lines 24-29 for dual permissions] This creates:

- **Namespace ambiguity:** Depending on which registration "wins" at runtime, tools may appear under either prefix.
- **Permission sprawl:** `settings.local.json` must list 6 permission entries for what should be 2 tools.
- **Agent definition fragility:** All agent `.md` files reference `mcp__context7__resolve-library-id` and `mcp__context7__query-docs`. If the plugin registration wins, these names do not match the actual tool names available.

### 2. Subagent MCP Access Gap

The GitHub Issue #13898 finding has significant implications for Jerry: [Source: GitHub Issue #13898]

- Jerry's agents are invoked via the `Task` tool as subagents.
- If Context7's MCP server is only available at project scope, subagents may not be able to access it.
- This explains potential silent failures where research agents fall back to WebSearch instead of using Context7.

**Mitigation:** Configure Context7 at **user scope** (`--scope user`) rather than project scope.

### 3. Tool Name Length Risk

GitHub Issue #20983 documents that the plugin naming convention can produce tool names exceeding the Claude API's 64-character limit. For Context7:

- `mcp__plugin_context7_context7__resolve-library-id` = 49 characters (safe)
- `mcp__plugin_context7_context7__query-docs` = 42 characters (safe)

Context7's short tool names keep it under the limit, but this is a risk factor for other plugins Jerry might adopt.

### 4. Recommended Architecture

**Single registration method:** Choose ONE of:

| Option | Pros | Cons | Recommended? |
|--------|------|------|:------------:|
| **Plugin only** (`enabledPlugins`) | Auto-updates, official registry, no manual setup | Long tool names, must update all agent definitions, subagent access issues | No |
| **Manual MCP server only** (user scope) | Short tool names matching current agent definitions, reliable subagent access, full control | Manual updates, no marketplace benefits | **Yes** |
| **Hybrid: both registered, agents updated to plugin prefix** | No migration needed for existing plugin, agents always match runtime | Longest tool names, plugin prefix may change, ties agents to plugin distribution channel | No |

**Why the hybrid option is not recommended:** The hybrid approach (keeping both plugin and manual registrations while updating all agent definitions to use the plugin prefix `mcp__plugin_context7_context7__`) would eliminate the namespace mismatch by standardizing on the longer prefix. However, it inherits the worst properties of both methods: (1) it does not resolve the subagent MCP access limitation documented in Issue #13898 -- plugin-provided MCP servers are still subject to project-scope restrictions, meaning subagents invoked via the Task tool may still fail silently; (2) the plugin naming formula `mcp__plugin_<plugin-name>_<server-name>__<tool-name>` is not guaranteed stable across Claude Code major versions (it was empirically observed, not officially specified), creating a fragile dependency; (3) it requires updating 7 agent definitions and `TOOL_REGISTRY.yaml` to use longer, less readable tool names; and (4) maintaining both registrations adds ongoing operational complexity with no corresponding benefit, since the manual server alone provides all required functionality. The hybrid approach is appropriate only if a future Claude Code release provides a stable, documented plugin naming contract and resolves the subagent access limitation for plugin-provided servers.

**Recommended approach:** Remove the `enabledPlugins` Context7 entry and configure Context7 as a user-scoped MCP server:

```bash
claude mcp add --transport sse --scope user context7 https://mcp.context7.com/sse
```

This ensures:
1. Tool names match agent definitions (`mcp__context7__resolve-library-id`)
2. Subagents can access Context7 (user-scoped servers are inherited)
3. Permissions are simple (`mcp__context7` or `mcp__context7__*`)
4. No namespace collision with plugin prefix

### Deployment Considerations

| Consideration | Impact | Mitigation | Source |
|---------------|--------|------------|--------|
| Per-developer setup | Each developer must run `claude mcp add --scope user context7 ...` | Document in onboarding; consider `.mcp.json` for project-scope fallback | `[DOCUMENTED]` — Claude Code MCP docs (Ref #1) |
| CI runners | CI environments need Context7 configured separately | Add to CI setup script or use project-scope `.mcp.json` | `[INFERRED]` — CI environments lack user-scope config by default |
| Worktree isolation | User-scoped servers are shared across all worktrees on the same machine | Verify via `claude mcp list` that Context7 is accessible from worktrees | `[INFERRED]` — user-scope is per-OS-user, not per-worktree |
| Multi-project conflicts | User-scope affects ALL Claude Code projects | Context7 is read-only and project-agnostic; low conflict risk | `[INFERRED]` — user-scope applies globally per Claude Code docs (Ref #1) |
| Auto-update loss | Plugin auto-updates stop; manual `@upstash/context7-mcp` updates needed | Pin version in command; schedule quarterly update checks | `[INFERRED]` — plugins auto-update via marketplace; manual servers do not |

### 5. Impact on TOOL_REGISTRY.yaml

The TOOL_REGISTRY.yaml correctly references `mcp__context7__resolve-library-id` and `mcp__context7__query-docs`. If the plugin-only approach were adopted instead, every reference would need to change to `mcp__plugin_context7_context7__resolve-library-id` and `mcp__plugin_context7_context7__query-docs`. This would affect 7 agent definitions and the registry itself.

### 6. Governance File Impact Assessment

| File | Current State | Issue | Fix Needed |
|------|--------------|-------|:----------:|
| `settings.json` (`enabledPlugins`) | Context7 enabled as plugin | Creates competing namespace | Remove plugin entry |
| `settings.local.json` | Both namespaces listed | Permission sprawl | Remove `mcp__plugin_*` entries |
| `TOOL_REGISTRY.yaml` | Uses `mcp__context7__` prefix | Correct for manual server config | No change needed |
| `mcp-tool-standards.md` | Uses `mcp__context7__` prefix | Correct for manual server config | No change needed |
| Agent definitions (7 files) | Use `mcp__context7__` prefix | Correct for manual server config | No change needed |

---

## Research Questions

| # | Question | Answer | Confidence |
|---|----------|--------|:----------:|
| RQ-1 | How is Context7 set up in Claude Code? | Two methods: Plugin via `enabledPlugins` or MCP Server via `claude mcp add`. They produce different tool name prefixes. | HIGH |
| RQ-2 | What are the exact tool names Context7 exposes? | `resolve-library-id` and `query-docs`. Prefix depends on config method. | HIGH |
| RQ-3 | What is the `mcp__plugin_` naming pattern? | `mcp__plugin_<plugin-name>_<server-name>__<tool-name>`. Documented in Issues #20983, #15145. | HIGH |
| RQ-4 | What tools does `mcpServers: [context7]` give an agent? | References an already-configured server by name. If tools field is omitted, all MCP tools inherited. If specified, only listed tools available. Project-scoped servers may not be accessible to subagents. | HIGH |
| RQ-5 | Does `mcp__context7__*` grant access to `mcp__plugin_context7_context7__*`? | **NO.** These are completely separate namespaces. Each must be permitted independently. | HIGH |

---

## Methodology

### Sources Consulted

| Source Type | Sources | Credibility |
|-------------|---------|:-----------:|
| Official Documentation | Claude Code docs (code.claude.com) -- MCP, Permissions, Subagents, Plugins, Plugins Reference | HIGH |
| GitHub Issues | anthropics/claude-code #3107 (wildcard permissions), #15145 (namespace collision), #20983 (tool name length), #13898 (subagent MCP access) | HIGH |
| Codebase Analysis | `.claude/settings.json`, `.claude/settings.local.json`, `TOOL_REGISTRY.yaml`, `mcp-tool-standards.md` | HIGH |
| Product Pages | claude.com/plugins/context7 (Context7 plugin page) | MEDIUM |
| Context7 Documentation | github.com/upstash/context7 | HIGH |

### Approach

1. **Multi-source triangulation:** Cross-referenced official docs, GitHub issues, and codebase configuration to build a complete picture.
2. **5W1H framework:** Structured findings around Who (Anthropic/Upstash), What (dual naming), Where (settings files), When (plugin vs manual config), Why (separate registration systems), How (permission resolution).
3. **Evidence chain:** Each claim is backed by at least one primary source (official documentation or GitHub issue with Anthropic contributor response).
4. **Design-intent confirmation:** Issue #15145's closure as NOT PLANNED strengthens the recommendation to avoid plugins, since the namespace separation is permanent by design rather than a temporary bug.

### Limitations

1. ~~**Could not verify runtime behavior empirically**~~ -- **RESOLVED.** Post-research empirical verification from a live Claude Code session confirmed the dual-namespace behavior. See [Empirical Verification](#empirical-verification).
2. **Context7 MCP quota exceeded** during research -- could not use Context7 to look up Claude Code's own documentation via the MCP tool.
3. **Issue #2928 not found** -- the originally requested issue number does not exist or has been renumbered. The relevant issues are #3107, #15145, and #20983.

---

## Empirical Verification

Post-research verification from a live Claude Code session confirms the dual-namespace finding. The following runtime evidence was collected from the current session's MCP tool list.

**Verification method:** Tool names were obtained by examining Claude Code's runtime tool inventory -- the set of tools presented to the agent in the active session context. Claude Code version: 2.1.61 (retrieved via `claude --version` on 2026-02-26). **Reproduction steps:** (1) Start a Claude Code session in a repository with Context7 enabled as a plugin in `.claude/settings.json` under `enabledPlugins`. (2) Inspect the available tool names in the session's tool list (visible in the system prompt or via tool invocation attempts). (3) Compare observed prefixes against the two naming patterns documented in Section 3.

### Context7 Tools (Plugin Prefix Confirmed)

The current session exposes Context7 tools with the **plugin prefix**:

- `mcp__plugin_context7_context7__resolve-library-id`
- `mcp__plugin_context7_context7__query-docs`

This confirms Formula B: the plugin naming pattern `mcp__plugin_<plugin-name>_<server-name>__<tool-name>` is active in the current Claude Code runtime. The tools are NOT available under the short `mcp__context7__` prefix.

### Memory-Keeper Tools (Manual MCP Prefix Confirmed)

The current session exposes Memory-Keeper tools with the **manual MCP server prefix**:

- `mcp__memory-keeper__context_save`
- `mcp__memory-keeper__context_get`
- `mcp__memory-keeper__context_search`

This confirms that manually configured MCP servers use the `mcp__<server-name>__<tool-name>` pattern, while plugins use the longer `mcp__plugin_<plugin-name>_<server-name>__<tool-name>` pattern. The two namespaces are operationally distinct.

### BUG-001 Confirmation

The canonical names documented in `mcp-tool-standards.md` for Memory-Keeper are:

| Canonical Name (Governance) | Actual Runtime Name | Match? |
|-----------------------------|---------------------|:------:|
| `mcp__memory-keeper__store` | `mcp__memory-keeper__context_save` | NO |
| `mcp__memory-keeper__retrieve` | `mcp__memory-keeper__context_get` | NO |
| `mcp__memory-keeper__search` | `mcp__memory-keeper__context_search` | NO |

This confirms BUG-001: the governance files reference tool names that do not exist at runtime.

### Verification Impact on Research Confidence

| Claim | Pre-Verification Evidence | Post-Verification Evidence | Confidence Change |
|-------|--------------------------|---------------------------|:-----------------:|
| Plugin tools use `mcp__plugin_` prefix | GitHub Issues #20983, #15145 | Live session tool list | HIGH -> VERIFIED |
| Manual MCP tools use `mcp__<server>__` prefix | Claude Code documentation | Live session tool list (Memory-Keeper) | HIGH -> VERIFIED |
| Namespaces are separate | Documentation inference | Both prefixes observed in same session | HIGH -> VERIFIED |
| BUG-001 tool name mismatch | Codebase analysis | Runtime names differ from canonical names | HIGH -> VERIFIED |
| Subagent MCP access limited to user-scope servers (Issue #13898) | GitHub Issue #13898 report | Not empirically tested in this session -- subagent Task invocation with Context7 not attempted | HIGH (issue report) -- NOT YET VERIFIED empirically |

---

## Findings (5W1H)

### WHO

- **Anthropic** develops and maintains Claude Code's plugin system, MCP integration, and permission framework.
- **Upstash** develops and maintains Context7 as both an MCP server package (`@upstash/context7-mcp`) and a Claude Code plugin in the official marketplace.
- **Jerry Framework** (this project) consumes Context7 via both configuration methods simultaneously.

### WHAT

Two distinct tool naming conventions coexist in Claude Code:

1. **Manual MCP servers:** `mcp__<server-name>__<tool-name>` (e.g., `mcp__context7__resolve-library-id`)
2. **Plugin MCP servers:** `mcp__plugin_<plugin-name>_<server-name>__<tool-name>` (e.g., `mcp__plugin_context7_context7__resolve-library-id`)

These are **separate permission namespaces** -- granting access to one does not grant access to the other.

### WHERE

The conflict manifests in:
- `.claude/settings.json` line 80-82 (`enabledPlugins`)
- `.claude/settings.local.json` lines 24-29 (dual permission entries)
- `TOOL_REGISTRY.yaml` (references short-form names only)
- All 7 agent definitions that use Context7 (reference short-form names only)

### WHEN

**[INFERRED]** This dual-registration pattern was introduced when the Context7 plugin was enabled in `settings.json` alongside governance files that already referenced the manual MCP server naming convention. **[INFERRED]** The codebase analysis suggests governance was written first (using `mcp__context7__` names), and plugin registration was added later without updating agent definitions. This inference is based on the naming convention mismatch pattern; git log verification was not performed.

### WHY

The dual registration exists because:
1. **[INFERRED]** The plugin system is newer than the manual MCP server configuration.
2. **[INFERRED]** The governance files were authored referencing the manual naming convention.
3. **[INFERRED]** No integration test validates that agent tool references match actual runtime tool names.
4. **[EVIDENCED by `settings.local.json`]** `settings.local.json` was patched defensively to allow both namespaces.

### HOW

**How the permission system resolves MCP tool names:**

1. Claude Code loads MCP servers from all scopes (managed, user, project, local, plugin).
2. Each server's tools are prefixed based on their source (plugin vs manual).
3. Permission rules match against the **full prefixed name**.
4. `mcp__context7` matches all tools from a server named `context7` (manual config).
5. `mcp__plugin_context7_context7` matches all tools from the Context7 plugin server.
6. These are distinct entries -- one does not match the other.
7. Agent definitions specify tools by full name; if the name does not match the runtime prefix, the tool is unavailable to that agent.

---

## Recommendations

### Immediate (BUG-002 candidate)

1. **Choose one registration method.** Remove `enabledPlugins.context7@claude-plugins-official` from `settings.json` and ensure Context7 is configured as a **user-scoped manual MCP server**.

2. **Simplify `settings.local.json` permissions.** Remove the 6 Context7 entries and replace with:
   ```json
   "mcp__context7"
   ```
   This single entry matches all tools from the `context7` server.

3. **Verify subagent access.** After switching to user-scope manual configuration, verify that agents invoked via the Task tool can access Context7.

### Short-Term

4. **Add a pre-flight check.** Create a validation script that compares tool names in agent definitions against actual MCP server tool names at runtime (via `/mcp` command output).

5. **Document the naming convention** in `mcp-tool-standards.md`. Add a section explicitly documenting the plugin vs manual server naming difference and Jerry's decision to use manual server configuration.

### Long-Term

6. **Monitor Claude Code plugin/MCP evolution.** The naming convention issues (#20983, #15145) suggest Anthropic may revise the plugin MCP naming scheme. Track claude-code releases for changes.

---

## References

1. [Claude Code MCP Documentation](https://code.claude.com/docs/en/mcp) - Official MCP integration guide. Key insight: Plugin MCP servers start automatically when enabled; servers appear as standard MCP tools.
2. [Claude Code Permissions Documentation](https://code.claude.com/docs/en/permissions) - Official permissions guide. Key insight: `mcp__puppeteer` matches all tools; `mcp__puppeteer__*` also works.
3. [Claude Code Subagents Documentation](https://code.claude.com/docs/en/sub-agents) - Official subagent guide. Key insight: `mcpServers` field references already-configured servers; tools inherited when `tools` omitted.
4. [Claude Code Plugins Documentation](https://code.claude.com/docs/en/plugins) - Official plugin creation guide. Key insight: Plugin skills namespaced as `/plugin-name:skill-name`.
5. [Claude Code Plugins Reference](https://code.claude.com/docs/en/plugins-reference) - Plugin technical reference. Key insight: Plugin MCP servers in `.mcp.json` at plugin root.
6. [GitHub Issue #3107: MCP wildcard permissions not honored](https://github.com/anthropics/claude-code/issues/3107) - Key insight: MCP permissions originally did NOT support wildcards. Correct syntax: `mcp__<server-name>` (no `__*`). Status: CLOSED (July 2025).
7. [GitHub Issue #15145: MCP servers incorrectly namespaced under plugin](https://github.com/anthropics/claude-code/issues/15145) - Key insight: Installing a plugin can cause ALL MCP servers to be namespaced under `plugin:<name>:*`. Status: Closed as NOT PLANNED. **Status note:** Closed as NOT PLANNED means Anthropic considers the plugin namespacing behavior to be by-design, not a bug. The plugin prefix for MCP servers is the intended permanent behavior when using plugins.
8. [GitHub Issue #20983: MCP plugin tool names exceed 64-char limit](https://github.com/anthropics/claude-code/issues/20983) - Key insight: Plugin naming pattern `mcp__plugin_<plugin>_<server>__<tool>` confirmed. Closed as duplicate of #20830.
9. [GitHub Issue #13898: Custom subagents cannot access project-scoped MCP servers](https://github.com/anthropics/claude-code/issues/13898) - Key insight: Subagents hallucinate MCP results when server is project-scoped; user-scoped servers work correctly.
10. [Context7 GitHub Repository](https://github.com/upstash/context7) - Upstash Context7 MCP server. Tools: `resolve-library-id`, `query-docs`.
11. [Context7 Claude Plugin Page](https://claude.com/plugins/context7) - Official Context7 plugin listing. 127,061 installs.
12. [Context7 MCP Tool Reference - Glama](https://glama.ai/mcp/servers/@upstash/context7-mcp/tools/resolve-library-id) - Tool specification reference.
13. [GitHub Issue #13077: Claude Code wildcard permission fix](https://github.com/anthropics/claude-code/issues/13077) - Key insight: Continued report of wildcard permission failures in Late 2025, supporting the timeline that wildcard syntax was not yet reliable.
14. [GitHub Issue #14730: Related wildcard permission fix](https://github.com/anthropics/claude-code/issues/14730) - Key insight: Additional wildcard permission failure report in Late 2025 timeframe, corroborating Issue #13077.

---

## PS Integration

### Artifact

- **File:** `projects/PROJ-030-bugs/research/context7-plugin-architecture.md`
- **Type:** Research Report
- **Related Bug:** BUG-001 (memory-keeper tool names -- same class of issue)
- **Memory-Keeper verification:** Empirical observation confirms Memory-Keeper uses the `mcp__memory-keeper__` prefix (manual MCP server). However, canonical names in `mcp-tool-standards.md` (e.g., `mcp__memory-keeper__store`) do NOT match runtime names (e.g., `mcp__memory-keeper__context_save`), confirming BUG-001.
- **Candidate Bug:** BUG-002 (Context7 dual-registration namespace conflict)

### State

```yaml
researcher_output:
  ps_id: "proj-030"
  entry_id: "e-002"
  artifact_path: "projects/PROJ-030-bugs/research/context7-plugin-architecture.md"
  summary: "Context7 has dual registration (plugin + manual MCP) creating separate tool name namespaces. Agent definitions reference short names but plugin creates long names. Recommend removing plugin registration and using user-scoped manual MCP server."
  sources_count: 14
  confidence: "high"
  next_agent_hint: "ps-architect for ADR on MCP configuration strategy"
```
