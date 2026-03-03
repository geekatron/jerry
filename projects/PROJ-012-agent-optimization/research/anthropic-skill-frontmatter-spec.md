# Anthropic Claude Code Skill Frontmatter Specification -- Complete Research

<!-- VERSION: 1.0.0 | DATE: 2026-03-02 | SOURCE: PROJ-012 Agent Optimization | AGENT: ps-researcher -->

> Comprehensive specification of YAML frontmatter fields for Claude Code SKILL.md files and subagent definitions. Covers the Agent Skills open standard, Claude Code extensions, and comparison with Jerry Framework agent definitions.

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Quick Reference](#l0-quick-reference) | Complete field table for all three specifications |
| [L1: Field-by-Field Specification](#l1-field-by-field-specification) | Detailed per-field spec with constraints and defaults |
| [L2: Behavioral Analysis](#l2-behavioral-analysis) | Context loading, strict mode, comparison with Jerry agent schema |
| [Sources](#sources) | Provenance for all extracted data |

---

## L0: Quick Reference

### Skill Frontmatter Fields (Claude Code -- 10 fields)

Source: `https://code.claude.com/docs/en/skills` (Anthropic official documentation, March 2026)

| # | Field | Type | Required | Default | Constraints | Brief Description |
|---|-------|------|----------|---------|-------------|-------------------|
| 1 | `name` | string | No | Directory name | Max 64 chars; lowercase letters, numbers, hyphens only | Display name; becomes `/slash-command` |
| 2 | `description` | string | Recommended | First paragraph of markdown body | Free text | What skill does and when to use it |
| 3 | `argument-hint` | string | No | None | Free text | Autocomplete hint for expected arguments |
| 4 | `disable-model-invocation` | boolean | No | `false` | `true` or `false` | Prevents Claude from auto-loading this skill |
| 5 | `user-invocable` | boolean | No | `true` | `true` or `false` | Controls visibility in `/` menu |
| 6 | `allowed-tools` | string | No | Inherit all | Comma-separated tool names | Tools allowed without permission prompts |
| 7 | `model` | string | No | Inherit | Model identifier | Model to use when skill is active |
| 8 | `context` | string | No | None | Only `fork` is documented | Run in forked subagent context |
| 9 | `agent` | string | No | `general-purpose` | Built-in or custom agent name | Subagent type for `context: fork` |
| 10 | `hooks` | object | No | None | Same format as settings.json hooks | Lifecycle hooks scoped to skill |

### Agent Skills Open Standard Fields (agentskills.io -- 6 fields)

Source: `https://agentskills.io/specification` (Agent Skills open standard specification)

| # | Field | Type | Required | Default | Constraints | Brief Description |
|---|-------|------|----------|---------|-------------|-------------------|
| 1 | `name` | string | Yes | N/A | 1-64 chars; lowercase alphanum + hyphens; no leading/trailing/consecutive hyphens; must match directory name | Skill identifier |
| 2 | `description` | string | Yes | N/A | 1-1024 chars; non-empty | What skill does and when to use it |
| 3 | `license` | string | No | None | Free text (recommend short) | License name or reference |
| 4 | `compatibility` | string | No | None | 1-500 chars | Environment requirements |
| 5 | `metadata` | object | No | None | String keys to string values | Arbitrary key-value pairs |
| 6 | `allowed-tools` | string | No | None | Space-delimited tool list (experimental) | Pre-approved tools |

### Subagent/Agent Frontmatter Fields (Claude Code -- 12 fields)

Source: `https://code.claude.com/docs/en/sub-agents` (Anthropic official documentation, March 2026)

| # | Field | Type | Required | Default | Constraints | Brief Description |
|---|-------|------|----------|---------|-------------|-------------------|
| 1 | `name` | string | Yes | N/A | Lowercase letters and hyphens | Unique agent identifier |
| 2 | `description` | string | Yes | N/A | Free text | When Claude should delegate to this agent |
| 3 | `tools` | string/array | No | Inherit all | Tool names | Allowed tools (allowlist) |
| 4 | `disallowedTools` | string/array | No | None | Tool names | Tools to deny (denylist) |
| 5 | `model` | string | No | `inherit` | `sonnet`, `opus`, `haiku`, `inherit` | Model selection |
| 6 | `permissionMode` | string | No | None | `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan` | Permission handling |
| 7 | `maxTurns` | number | No | None | Positive integer | Max agentic turns |
| 8 | `skills` | array | No | None | Skill name strings | Skills preloaded into context |
| 9 | `mcpServers` | object/array | No | None | Server names or inline definitions | MCP servers available |
| 10 | `hooks` | object | No | None | Same format as settings.json hooks | Lifecycle hooks |
| 11 | `memory` | string | No | None | `user`, `project`, `local` | Persistent memory scope |
| 12 | `background` | boolean | No | `false` | `true` or `false` | Always run as background task |
| 13 | `isolation` | string | No | None | `worktree` | Git worktree isolation |

### Unified Field Comparison Matrix

| Field | Agent Skills Std | CC Skill | CC Subagent | Jerry Canonical | Notes |
|-------|:---:|:---:|:---:|:---:|-------|
| `name` | REQ | opt | REQ | REQ | Skills fall back to directory name |
| `description` | REQ | rec | REQ | REQ | Skills fall back to first paragraph |
| `argument-hint` | -- | opt | -- | -- | Skill-only (autocomplete) |
| `disable-model-invocation` | -- | opt | -- | -- | Skill-only (auto-load control) |
| `user-invocable` | -- | opt | -- | -- | Skill-only (menu visibility) |
| `allowed-tools` | exp | opt | -- | -- | Standard uses space-delimited; CC uses comma-separated |
| `tools` | -- | -- | opt | REQ | Agent-only (allowlist); Jerry uses abstract names |
| `disallowedTools` | -- | -- | opt | -- | Agent-only (denylist) |
| `model` | -- | opt | opt | REQ | Agents default to `inherit`; Jerry uses abstract tiers |
| `permissionMode` | -- | -- | opt | -- | Agent-only |
| `maxTurns` | -- | -- | opt | -- | Agent-only |
| `skills` | -- | -- | opt | -- | Agent-only (preloaded skills) |
| `mcpServers` | -- | -- | opt | -- | Agent-only |
| `hooks` | -- | opt | opt | -- | Both skills and agents |
| `memory` | -- | -- | opt | -- | Agent-only (persistent memory) |
| `background` | -- | -- | opt | -- | Agent-only |
| `isolation` | -- | -- | opt | -- | Agent-only |
| `context` | -- | opt | -- | -- | Skill-only (`fork`) |
| `agent` | -- | opt | -- | -- | Skill-only (subagent type for fork) |
| `license` | opt | -- | -- | -- | Standard-only |
| `compatibility` | opt | -- | -- | -- | Standard-only |
| `metadata` | opt | -- | -- | -- | Standard-only (arbitrary k-v) |
| `version` | -- | -- | -- | REQ | Jerry-only (semver) |
| `identity` | -- | -- | -- | REQ | Jerry-only (role, expertise, cognitive_mode) |
| `tool_tier` | -- | -- | -- | REQ | Jerry-only (T1-T5) |
| `guardrails` | -- | -- | -- | REQ | Jerry-only (input/output/fallback) |
| `constitution` | -- | -- | -- | REQ | Jerry-only (principles, forbidden actions) |
| `persona` | -- | -- | -- | opt | Jerry-only (tone, style, audience) |
| `output` | -- | -- | -- | opt | Jerry-only (levels, location, format) |
| `portability` | -- | -- | -- | opt | Jerry-only (cross-vendor) |
| `session_context` | -- | -- | -- | opt | Jerry-only (handoff protocol) |
| `enforcement` | -- | -- | -- | opt | Jerry-only (quality tier) |
| `prior_art` | -- | -- | -- | opt | Jerry-only (citations) |
| `validation` | -- | -- | -- | opt | Jerry-only (post-completion checks) |

Legend: REQ = required, opt = optional, rec = recommended, exp = experimental, -- = not present in this spec.

---

## L1: Field-by-Field Specification

### 1. Skill Frontmatter Fields (Claude Code)

Source: `https://code.claude.com/docs/en/skills` -- "Frontmatter reference" section.

Claude Code skills follow the Agent Skills open standard (`agentskills.io`) and extend it with additional fields. All fields are optional. Only `description` is recommended.

#### 1.1 `name`

| Attribute | Value |
|-----------|-------|
| **Type** | `string` |
| **Required** | No |
| **Default** | If omitted, Claude Code uses the parent directory name |
| **Constraints** | Lowercase letters, numbers, and hyphens only. Max 64 characters. |
| **Validation Pattern** | `^[a-z0-9][a-z0-9-]*$` (inferred from Agent Skills spec: must not start or end with hyphen, no consecutive hyphens) |
| **Agent Skills Additional** | Must match the parent directory name. Must not contain consecutive hyphens (`--`). |
| **Behavioral Notes** | Becomes the `/slash-command` for user invocation. Used as display name in skill listings. The Agent Skills standard requires this field; Claude Code makes it optional with fallback to directory name. |
| **Reserved Words** | Per Jerry `skill-standards.md`: names must not contain `claude` or `anthropic` (security restriction to prevent impersonation). This is a Jerry extension, not an Anthropic constraint. |

#### 1.2 `description`

| Attribute | Value |
|-----------|-------|
| **Type** | `string` |
| **Required** | Recommended (Claude Code); Required (Agent Skills standard) |
| **Default** | If omitted in Claude Code, uses the first paragraph of the markdown body content |
| **Constraints** | Agent Skills: 1-1024 characters, non-empty |
| **Behavioral Notes** | Claude uses this field to decide when to apply the skill automatically. Descriptions are loaded into context at session start so Claude knows what skills are available. The full skill content only loads when invoked. Descriptions should include specific keywords that help agents identify relevant tasks. Poor descriptions lead to missed activations. |
| **Context Budget** | Skill descriptions are loaded into context with a budget of 2% of the context window, with a fallback of 16,000 characters. Run `/context` to check for warnings about excluded skills. Override with `SLASH_COMMAND_TOOL_CHAR_BUDGET` environment variable. |

#### 1.3 `argument-hint`

| Attribute | Value |
|-----------|-------|
| **Type** | `string` |
| **Required** | No |
| **Default** | None |
| **Constraints** | Free text |
| **Behavioral Notes** | Shown during autocomplete to indicate expected arguments. Examples: `[issue-number]`, `[filename] [format]`. Claude Code specific; not in the Agent Skills standard. |

#### 1.4 `disable-model-invocation`

| Attribute | Value |
|-----------|-------|
| **Type** | `boolean` |
| **Required** | No |
| **Default** | `false` |
| **Behavioral Notes** | When `true`: (1) Only the user can invoke this skill via `/name`. (2) Claude cannot load it automatically. (3) The skill description is NOT loaded into Claude's context. (4) The Skill tool cannot programmatically invoke it. Use for workflows with side effects (deploy, commit, send-slack-message) where you want to control timing. |
| **Interaction with `user-invocable`** | See the invocation matrix in L2. |

#### 1.5 `user-invocable`

| Attribute | Value |
|-----------|-------|
| **Type** | `boolean` |
| **Required** | No |
| **Default** | `true` |
| **Behavioral Notes** | When `false`: (1) Hidden from the `/` autocomplete menu. (2) Claude can still invoke it automatically if description matches. (3) The skill description IS still loaded into context. Use for background knowledge that isn't actionable as a command. Note: this only controls menu visibility, NOT Skill tool access. To block programmatic invocation, use `disable-model-invocation: true`. |

#### 1.6 `allowed-tools`

| Attribute | Value |
|-----------|-------|
| **Type** | `string` (comma-separated in Claude Code; space-delimited in Agent Skills standard) |
| **Required** | No |
| **Default** | Inherits all tools available in the session |
| **Constraints** | Claude Code tool names: `Read`, `Grep`, `Glob`, `Write`, `Edit`, `Bash`, `WebFetch`, `WebSearch`, `Agent`, `NotebookEdit`, plus MCP tool names (`mcp__<server>__<tool>`) |
| **Behavioral Notes** | Tools listed here can be used by Claude without asking permission when this skill is active. Your permission settings still govern baseline approval behavior for all other tools. Supports glob-like patterns for Bash: `Bash(git *)`, `Bash(npm *)`. |
| **Agent Skills Standard** | Field is marked "Experimental. Support for this field may vary between agent implementations." Uses space-delimited format. |

#### 1.7 `model`

| Attribute | Value |
|-----------|-------|
| **Type** | `string` |
| **Required** | No |
| **Default** | Inherits from current session |
| **Constraints** | Model alias (e.g., `sonnet`, `opus`, `haiku`) or full model identifier |
| **Behavioral Notes** | Sets the model used when this skill is active. Applies to the skill's execution context. |

#### 1.8 `context`

| Attribute | Value |
|-----------|-------|
| **Type** | `string` |
| **Required** | No |
| **Default** | None (skill runs inline in main conversation) |
| **Allowed Values** | `fork` (only documented value) |
| **Behavioral Notes** | When set to `fork`: (1) The skill runs in an isolated subagent context. (2) The skill content becomes the prompt that drives the subagent. (3) The subagent does NOT have access to conversation history. (4) Results are summarized and returned to the main conversation. (5) CLAUDE.md files are loaded into the forked context. **Warning**: `context: fork` only makes sense for skills with explicit task instructions. If your skill contains guidelines without a task, the subagent receives guidelines but no actionable prompt and returns without meaningful output. |

#### 1.9 `agent`

| Attribute | Value |
|-----------|-------|
| **Type** | `string` |
| **Required** | No |
| **Default** | `general-purpose` |
| **Constraints** | Must be a valid built-in agent name or custom agent from `.claude/agents/` |
| **Built-in Options** | `Explore` (Haiku, read-only), `Plan` (inherits, read-only), `general-purpose` (inherits, all tools) |
| **Behavioral Notes** | Only relevant when `context: fork` is set. Determines the execution environment (model, tools, and permissions) for the forked subagent. |

#### 1.10 `hooks`

| Attribute | Value |
|-----------|-------|
| **Type** | `object` |
| **Required** | No |
| **Default** | None |
| **Behavioral Notes** | Hooks scoped to this skill's lifecycle. Only active while the skill is running. Cleaned up when the skill finishes. All hook events are supported. Uses the same configuration format as `settings.json` hooks. The `once` field (boolean) is available for skill hooks -- if `true`, the hook runs only once per session and is then removed. |
| **Supported Events** | `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `Notification`, `SubagentStart`, `SubagentStop`, `Stop`, `UserPromptSubmit`, `SessionStart`, `SessionEnd`, `PreCompact`, `ConfigChange`, `WorktreeCreate`, `WorktreeRemove`, `TeammateIdle`, `TaskCompleted` |
| **Format** | Same nested structure as settings.json: `{ "EventName": [{ "matcher": "...", "hooks": [{ "type": "command", "command": "..." }] }] }` |

### 2. Agent Skills Open Standard Fields

Source: `https://agentskills.io/specification`

The open standard defines the portable, cross-tool baseline that all implementations should support.

#### 2.1 `name` (Standard)

| Attribute | Value |
|-----------|-------|
| **Type** | `string` |
| **Required** | Yes |
| **Constraints** | 1-64 characters. Unicode lowercase alphanumeric characters and hyphens (`a-z` and `-`). Must not start or end with `-`. Must not contain consecutive hyphens (`--`). Must match the parent directory name. |
| **Validation Pattern** | `^[a-z0-9]([a-z0-9-]*[a-z0-9])?$` with additional check for no `--` |

#### 2.2 `description` (Standard)

| Attribute | Value |
|-----------|-------|
| **Type** | `string` |
| **Required** | Yes |
| **Constraints** | 1-1024 characters. Non-empty. Should describe both what the skill does and when to use it. Should include specific keywords that help agents identify relevant tasks. |

#### 2.3 `license` (Standard)

| Attribute | Value |
|-----------|-------|
| **Type** | `string` |
| **Required** | No |
| **Constraints** | Free text. Recommended to keep short (license name or bundled file reference). |
| **Examples** | `Apache-2.0`, `Proprietary. LICENSE.txt has complete terms` |

#### 2.4 `compatibility` (Standard)

| Attribute | Value |
|-----------|-------|
| **Type** | `string` |
| **Required** | No |
| **Constraints** | 1-500 characters if provided |
| **Behavioral Notes** | Most skills do not need this field. Include only if the skill has specific environment requirements. |
| **Examples** | `Designed for Claude Code (or similar products)`, `Requires git, docker, jq, and access to the internet` |

#### 2.5 `metadata` (Standard)

| Attribute | Value |
|-----------|-------|
| **Type** | `object` |
| **Required** | No |
| **Constraints** | Map from string keys to string values. Recommend making key names reasonably unique to avoid conflicts. |
| **Behavioral Notes** | Clients can use this to store additional properties not defined by the spec. |
| **Examples** | `{ "author": "example-org", "version": "1.0" }` |

#### 2.6 `allowed-tools` (Standard)

| Attribute | Value |
|-----------|-------|
| **Type** | `string` |
| **Required** | No |
| **Constraints** | Space-delimited list of tool names. Experimental. |
| **Behavioral Notes** | Support varies between agent implementations. |
| **Examples** | `Bash(git:*) Bash(jq:*) Read` |

### 3. Subagent/Agent Frontmatter Fields (Claude Code)

Source: `https://code.claude.com/docs/en/sub-agents` -- "Supported frontmatter fields" section.

Only `name` and `description` are required. The markdown body becomes the system prompt.

#### 3.1 `name` (Agent)

| Attribute | Value |
|-----------|-------|
| **Type** | `string` |
| **Required** | Yes |
| **Constraints** | Unique identifier using lowercase letters and hyphens |
| **Behavioral Notes** | Used for delegation routing. Claude uses this name to reference the subagent. Must be unique within its scope. |

#### 3.2 `description` (Agent)

| Attribute | Value |
|-----------|-------|
| **Type** | `string` |
| **Required** | Yes |
| **Behavioral Notes** | Claude uses this to decide when to delegate tasks. Write a clear description so Claude knows when to use it. Include "use proactively" to encourage proactive delegation. |

#### 3.3 `tools` (Agent)

| Attribute | Value |
|-----------|-------|
| **Type** | `string` or `array` |
| **Required** | No |
| **Default** | Inherits ALL tools from the main conversation (including MCP tools) |
| **Behavioral Notes** | Allowlist of tools the subagent can use. Supports `Agent(agent_type)` syntax to restrict which subagent types can be spawned. If `Agent` is omitted entirely, the agent cannot spawn subagents. **Subagents cannot spawn other subagents** -- `Agent(agent_type)` only applies to agents running as main thread with `claude --agent`. |
| **Available Tools** | `Read`, `Grep`, `Glob`, `Write`, `Edit`, `Bash`, `WebFetch`, `WebSearch`, `Agent`, `NotebookEdit`, plus MCP tools |

#### 3.4 `disallowedTools` (Agent)

| Attribute | Value |
|-----------|-------|
| **Type** | `string` or `array` |
| **Required** | No |
| **Behavioral Notes** | Denylist of tools removed from the inherited or specified tool list. Takes precedence: a tool listed in both `tools` and `disallowedTools` is denied. |

#### 3.5 `model` (Agent)

| Attribute | Value |
|-----------|-------|
| **Type** | `string` |
| **Required** | No |
| **Default** | `inherit` (uses the same model as the main conversation) |
| **Allowed Values** | `sonnet`, `opus`, `haiku`, `inherit` |
| **Behavioral Notes** | Determines which AI model the subagent uses. Use `haiku` for fast, cheap tasks. Use `opus` for complex reasoning. |

#### 3.6 `permissionMode` (Agent)

| Attribute | Value |
|-----------|-------|
| **Type** | `string` |
| **Required** | No |
| **Allowed Values** | `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan` |
| **Behavioral Notes** | Subagents inherit the permission context from the main conversation but can override the mode. If the parent uses `bypassPermissions`, this takes precedence and cannot be overridden. `dontAsk` auto-denies permission prompts (explicitly allowed tools still work). `plan` enables read-only exploration mode. |

#### 3.7 `maxTurns` (Agent)

| Attribute | Value |
|-----------|-------|
| **Type** | `number` |
| **Required** | No |
| **Constraints** | Positive integer |
| **Behavioral Notes** | Maximum number of agentic turns before the subagent stops. Prevents runaway execution. |

#### 3.8 `skills` (Agent)

| Attribute | Value |
|-----------|-------|
| **Type** | `array` of strings |
| **Required** | No |
| **Behavioral Notes** | The FULL content of each listed skill is injected into the subagent's context at startup, not just made available for invocation. Subagents do NOT inherit skills from the parent conversation -- you must list them explicitly. This is the inverse of `context: fork` in skills. |

#### 3.9 `mcpServers` (Agent)

| Attribute | Value |
|-----------|-------|
| **Type** | `object` or `array` |
| **Required** | No |
| **Behavioral Notes** | Each entry is either: (1) a server name referencing an already-configured server (e.g., `"slack"`), or (2) an inline definition with the server name as key and a full MCP server config as value. |

#### 3.10 `hooks` (Agent)

| Attribute | Value |
|-----------|-------|
| **Type** | `object` |
| **Required** | No |
| **Behavioral Notes** | Hooks scoped to this subagent's lifecycle. Only run while that specific subagent is active. Cleaned up when it finishes. All hook events are supported. `Stop` hooks in agent frontmatter are automatically converted to `SubagentStop` events. Uses the same configuration format as settings.json hooks. |

#### 3.11 `memory` (Agent)

| Attribute | Value |
|-----------|-------|
| **Type** | `string` |
| **Required** | No |
| **Allowed Values** | `user`, `project`, `local` |
| **Behavioral Notes** | Gives the subagent a persistent directory that survives across sessions. Scopes: `user` = `~/.claude/agent-memory/<name>/` (all projects), `project` = `.claude/agent-memory/<name>/` (project-specific, can commit to VCS), `local` = `.claude/agent-memory-local/<name>/` (project-specific, gitignored). When enabled: (1) system prompt includes instructions for reading/writing memory directory, (2) includes first 200 lines of `MEMORY.md` in the directory, (3) Read/Write/Edit tools are automatically enabled. |

#### 3.12 `background` (Agent)

| Attribute | Value |
|-----------|-------|
| **Type** | `boolean` |
| **Required** | No |
| **Default** | `false` |
| **Behavioral Notes** | When `true`, always runs this subagent as a background task. Background subagents run concurrently while you continue working. Before launching, Claude Code prompts for any tool permissions the subagent will need upfront. `AskUserQuestion` tool calls fail in background but the subagent continues. |

#### 3.13 `isolation` (Agent)

| Attribute | Value |
|-----------|-------|
| **Type** | `string` |
| **Required** | No |
| **Allowed Values** | `worktree` |
| **Behavioral Notes** | When set to `worktree`, the subagent runs in a temporary git worktree, giving it an isolated copy of the repository. The worktree is automatically cleaned up if the subagent makes no changes. Requires a git repository. |

### 4. String Substitutions (Claude Code Skills)

Skills support dynamic string substitution in the markdown body content (not frontmatter):

| Variable | Type | Description |
|----------|------|-------------|
| `$ARGUMENTS` | string | All arguments passed when invoking the skill. If not present in content, arguments are appended as `ARGUMENTS: <value>`. |
| `$ARGUMENTS[N]` | string | Access a specific argument by 0-based index (e.g., `$ARGUMENTS[0]`). |
| `$N` | string | Shorthand for `$ARGUMENTS[N]` (e.g., `$0`, `$1`). |
| `${CLAUDE_SESSION_ID}` | string | Current session ID. |
| `` !`command` `` | string | Shell command preprocessing. Command runs before content is sent to Claude; output replaces the placeholder. |

### 5. CLI-Defined Agents (`--agents` flag)

Agents can be passed as JSON when launching Claude Code via `claude --agents '{...}'`. These exist only for that session and aren't saved to disk. The JSON format uses the same frontmatter fields as file-based subagents, with one addition:

| Field | Notes |
|-------|-------|
| `prompt` | Replaces the markdown body. Equivalent to the system prompt in file-based agents. |
| All other fields | Same as file-based: `description`, `tools`, `disallowedTools`, `model`, `permissionMode`, `maxTurns`, `skills`, `mcpServers`, `hooks`, `memory`. |

---

## L2: Behavioral Analysis

### Invocation Control Matrix (Skills)

The interaction between `disable-model-invocation` and `user-invocable` creates four behavioral modes:

| `disable-model-invocation` | `user-invocable` | User Can Invoke | Claude Can Invoke | Description Loaded | Full Content Loads When |
|:---:|:---:|:---:|:---:|:---:|:---|
| `false` (default) | `true` (default) | Yes | Yes | Yes (always) | User invokes via `/name` OR Claude auto-loads |
| `true` | `true` (default) | Yes | No | No | User invokes via `/name` only |
| `false` (default) | `false` | No | Yes | Yes (always) | Claude auto-loads when relevant |
| `true` | `false` | No | No | No | **Never loads** -- effectively disabled |

Key insight: `disable-model-invocation: true` removes the skill description from Claude's context entirely, making the skill invisible to Claude. `user-invocable: false` only hides from the `/` menu but keeps the description in context.

### Context Loading Behavior (Progressive Disclosure)

| Phase | What Loads | Size Budget | Mechanism |
|-------|-----------|-------------|-----------|
| **Session Start** | All skill `name` + `description` fields (for skills where `disable-model-invocation != true`) | 2% of context window; fallback: 16,000 chars. Override: `SLASH_COMMAND_TOOL_CHAR_BUDGET` env var | Injected into system prompt as available skills |
| **Skill Activation** | Full SKILL.md markdown body | No explicit limit; recommendation: keep under 500 lines | Loaded when Claude decides to use the skill or user invokes `/name` |
| **Execution** | Supporting files (references, scripts, assets) | No explicit limit; governed by context window | Loaded on-demand via Read tool during execution |

For subagents with preloaded skills (`skills` field), the FULL skill content is injected at startup -- not just made available for invocation. This is a different loading path than the progressive disclosure model.

### Skill-Agent Relationship (context: fork)

Two directions of interaction between skills and agents:

| Approach | System Prompt | Task | Also Loads |
|----------|---------------|------|------------|
| Skill with `context: fork` | From agent type (`Explore`, `Plan`, etc.) | SKILL.md content | CLAUDE.md |
| Subagent with `skills` field | Subagent's markdown body | Claude's delegation message | Preloaded skills + CLAUDE.md |

With `context: fork`, the skill author writes the task and picks an agent type to execute it.
With `skills` in a subagent, the subagent author controls the system prompt and loads skill content as reference material.

### Skill Discovery and Location Priority

Skills are discovered from multiple locations. Higher-priority locations win when names conflict:

| Priority | Location | Path Pattern | Scope |
|----------|----------|-------------|-------|
| 1 (highest) | Enterprise | Managed settings | All users in organization |
| 2 | Personal | `~/.claude/skills/<name>/SKILL.md` | All user's projects |
| 3 | Project | `.claude/skills/<name>/SKILL.md` | Current project only |
| 4 (lowest) | Plugin | `<plugin>/skills/<name>/SKILL.md` | Where plugin is enabled |

Plugin skills use a `plugin-name:skill-name` namespace and cannot conflict with other levels.

Auto-discovery: Claude Code automatically discovers skills from nested `.claude/skills/` directories when working with files in subdirectories (supports monorepo setups).

Legacy: `.claude/commands/` files still work and support the same frontmatter. If a skill and a command share the same name, the skill takes precedence.

### Agent Scope and Priority

| Priority | Location | How to Create |
|----------|----------|---------------|
| 1 (highest) | `--agents` CLI flag | JSON when launching Claude Code |
| 2 | `.claude/agents/` | Interactive or manual (project) |
| 3 | `~/.claude/agents/` | Interactive or manual (user) |
| 4 (lowest) | Plugin `agents/` dir | Installed with plugins |

### Permission Control for Skills

Three mechanisms control which skills Claude can invoke:

1. **Disable all skills**: Add `Skill` to `permissions.deny` in settings.
2. **Allow/deny specific skills**: Use `Skill(name)` for exact match, `Skill(name *)` for prefix match with any arguments in permission rules.
3. **Per-skill opt-out**: Add `disable-model-invocation: true` to frontmatter.

### Field Differences Between Agent Skills Standard and Claude Code

Claude Code extends the Agent Skills standard with 4 additional fields and modifies 2 fields:

| Change Type | Field | Agent Skills Standard | Claude Code Extension |
|-------------|-------|----------------------|----------------------|
| **Relaxed** | `name` | Required | Optional (falls back to directory name) |
| **Relaxed** | `description` | Required | Recommended (falls back to first paragraph) |
| **Added** | `argument-hint` | N/A | Autocomplete hint |
| **Added** | `disable-model-invocation` | N/A | Controls auto-loading |
| **Added** | `user-invocable` | N/A | Controls menu visibility |
| **Added** | `model` | N/A | Model selection |
| **Added** | `context` | N/A | Fork execution |
| **Added** | `agent` | N/A | Subagent type for fork |
| **Added** | `hooks` | N/A | Lifecycle hooks |
| **Not adopted** | `license` | Optional | Not in CC frontmatter ref |
| **Not adopted** | `compatibility` | Optional | Not in CC frontmatter ref |
| **Not adopted** | `metadata` | Optional | Not in CC frontmatter ref |
| **Modified** | `allowed-tools` | Space-delimited (exp.) | Comma-separated; supports patterns |

The standard fields `license`, `compatibility`, and `metadata` are not listed in Claude Code's frontmatter reference table but may be silently ignored rather than rejected. The open standard permits additional properties.

### Comparison: Skill Frontmatter vs Jerry Agent Schema

Jerry's agent definition schema (`jerry-claude-agent-definition-v1.schema.json`) serves a different purpose than Claude Code's native skill/agent frontmatter. Jerry adds governance, quality enforcement, and multi-agent coordination layers.

#### Shared Fields (Direct Mapping)

| CC Native Field | Jerry Schema Field | Mapping Notes |
|-----------------|-------------------|---------------|
| `name` | `name` | Same constraints. Jerry adds kebab-case pattern `^[a-z]+-[a-z]+(-[a-z]+)*$` |
| `description` | `description` | Same purpose. Jerry adds maxLength 1024 and no-XML-tags constraint |
| `model` | `model` | CC uses `sonnet/opus/haiku/inherit`; Jerry canonical uses abstract tiers `reasoning_high/reasoning_standard/fast` mapped at build time |
| `tools` | `capabilities.allowed_tools` (Jerry schema) / `tools.native` (canonical) | CC uses vendor tool names; Jerry canonical uses abstract names mapped at build time |
| `disallowedTools` | `tools.forbidden` (canonical) | Same concept; Jerry uses abstract tool names |
| `permissionMode` | Not in Jerry schema | Jerry uses enforcement tiers (hard/medium/soft) instead |
| `maxTurns` | `maxTurns` | Same field in both |
| `skills` | `skills` | Same field |
| `mcpServers` | `mcpServers` / `tools.mcp` (canonical) | Jerry canonical uses MCP server names; CC uses object format |
| `hooks` | `hooks` | Same field |
| `memory` | `memory` | Same field |
| `background` | `background` | Same field |
| `isolation` | `isolation` | Same field |

#### Jerry-Only Fields (No CC Equivalent)

| Jerry Field | Purpose | Why No CC Equivalent |
|-------------|---------|---------------------|
| `version` | Semantic versioning for agent definitions | CC does not version agent definitions |
| `identity` (role, expertise, cognitive_mode) | Agent identity for routing and capability description | CC uses `description` field only |
| `tool_tier` | T1-T5 security classification | CC has no tiered tool governance |
| `persona` (tone, style, audience) | Output voice configuration | CC relies on system prompt body |
| `guardrails` (input/output/fallback) | Declarative safety constraints | CC relies on system prompt body |
| `constitution` (principles, forbidden_actions) | Constitutional compliance | CC has no governance framework |
| `output` (location, levels, format) | Structured output specification | CC relies on system prompt body |
| `session_context` | Handoff protocol for multi-agent coordination | CC subagents don't have structured handoff |
| `enforcement` | Quality gate tier (hard/medium/soft) | CC has no quality enforcement tiers |
| `portability` | Cross-vendor compatibility | CC is vendor-specific |
| `validation` | Post-completion verification | CC has no declarative validation |
| `prior_art` | Source citations | CC has no citation framework |

#### Skill-Only Fields (No Jerry Agent Equivalent)

| CC Skill Field | Purpose | Why Not in Jerry Agents |
|----------------|---------|------------------------|
| `argument-hint` | Autocomplete hint | Agents don't have user-invokable arguments |
| `disable-model-invocation` | Auto-load control | Agents are always invoked via Task tool, not auto-loaded |
| `user-invocable` | Menu visibility | Agents are not user-invocable commands |
| `context` | Fork execution | Jerry uses Task tool for agent delegation |
| `agent` | Subagent type for fork | Jerry agents don't fork into other agent types |

### Implications for Jerry Compose Pipeline

The compose pipeline generates `.md` files in `skills/*/agents/` that Claude Code parses as subagent definitions. The official frontmatter fields it should emit are:

**Must use (recognized by Claude Code runtime)**:
1. `name` -- agent identifier
2. `description` -- delegation routing
3. `model` -- model selection
4. `tools` -- tool allowlist (if specified; omit to inherit all)
5. `disallowedTools` -- tool denylist (if needed)
6. `permissionMode` -- permission behavior
7. `maxTurns` -- execution bound
8. `skills` -- preloaded skills
9. `mcpServers` -- MCP server access
10. `hooks` -- lifecycle hooks
11. `memory` -- persistent memory
12. `background` -- background execution
13. `isolation` -- worktree isolation

**Jerry governance fields** (`version`, `tool_tier`, `identity`, `persona`, `guardrails`, `constitution`, `output`, `session_context`, `enforcement`, `portability`, `prior_art`, `validation`) should be injected into the markdown body as XML sections per the current architecture (H-34). Claude Code silently ignores unrecognized frontmatter fields, so including them in frontmatter would not cause errors but would not provide runtime enforcement either.

### Unknown Field Handling

The Agent Skills standard specification does not explicitly define strict vs. permissive parsing behavior. Based on the standard's `metadata` field (which accepts arbitrary key-value pairs) and the `agentskills.io/integrate-skills` guidance (which focuses on reading only `name` and `description` at startup), implementations are expected to:

1. Parse only known fields from frontmatter.
2. Silently ignore unknown fields (permissive parsing).
3. Store the full frontmatter for potential use by other consumers.

Claude Code follows this pattern: unrecognized frontmatter fields are silently ignored. Jerry's existing schema uses `"additionalProperties": true` on the canonical schema and `"additionalProperties": false` on the skill frontmatter schema, reflecting this expectation.

---

## Sources

| Source | URL | Access Date | Content Extracted |
|--------|-----|-------------|-------------------|
| Claude Code Skills Documentation | `https://code.claude.com/docs/en/skills` | 2026-03-02 | Skill frontmatter reference (10 fields), context loading, invocation control, discovery, progressive disclosure |
| Agent Skills Open Standard | `https://agentskills.io/specification` | 2026-03-02 | SKILL.md format specification (6 fields), directory structure, naming constraints, progressive disclosure |
| Agent Skills Overview | `https://agentskills.io/what-are-skills` | 2026-03-02 | Discovery flow, activation behavior, progressive disclosure phases |
| Agent Skills Integration Guide | `https://agentskills.io/integrate-skills` | 2026-03-02 | Metadata parsing, context injection format, security considerations |
| Claude Code Sub-agents Documentation | `https://code.claude.com/docs/en/sub-agents` | 2026-03-02 | Subagent frontmatter reference (13 fields), built-in agents, scoping, memory, isolation |
| Claude Code Hooks Reference | `https://code.claude.com/docs/en/hooks` | 2026-03-02 | Hook configuration format, skill/agent hook integration, lifecycle events |
| Jerry Agent Canonical Schema | `docs/schemas/agent-canonical-v1.schema.json` | 2026-03-02 | Jerry canonical agent definition fields |
| Jerry Agent Definition Schema | `docs/schemas/jerry-claude-agent-definition-v1.schema.json` | 2026-03-02 | Jerry Claude Code agent definition fields (dual-layer) |
| Jerry Skill Frontmatter Schema | `docs/schemas/jerry-skill-frontmatter-v1.schema.json` | 2026-03-02 | Jerry skill frontmatter validation schema |

---

<!-- VERSION: 1.0.0 | DATE: 2026-03-02 | SOURCE: PROJ-012 | AGENT: ps-researcher -->
*Research Version: 1.0.0*
*Project: PROJ-012 Agent Optimization*
*Agent: ps-researcher (divergent mode)*
*Quality: Pre-critique; L0/L1/L2 complete*
