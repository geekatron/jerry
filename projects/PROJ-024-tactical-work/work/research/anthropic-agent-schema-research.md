# Anthropic Claude Code Agent Definition Schema -- Research Findings

> **PS ID:** PROJ-024 | **Date:** 2026-03-26 | **Researcher:** ps-researcher | **Criticality:** C4
> **Confidence:** HIGH (0.90) -- Primary source is Anthropic's official documentation at code.claude.com

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Non-technical overview of findings |
| [L1: Complete Field Reference](#l1-complete-field-reference) | Detailed per-field analysis with types and constraints |
| [L2: Strategic Implications](#l2-strategic-implications) | Impact on Jerry's schema governance |
| [Gap Analysis](#gap-analysis) | Delta between our schema and Anthropic's specification |
| [Agent Discovery and Spawning](#agent-discovery-and-spawning) | How Claude Code finds and invokes agents |
| [Tool Reference](#tool-reference) | Complete list of valid tool names for tools/disallowedTools fields |
| [Hook Events Reference](#hook-events-reference) | All lifecycle hook events supported in agent frontmatter |
| [Skill Frontmatter Reference](#skill-frontmatter-reference) | Skill-specific fields that differ from agent frontmatter |
| [Methodology](#methodology) | How research was conducted |
| [References](#references) | All sources with URLs |

---

## L0: Executive Summary

We investigated what Anthropic officially documents as the YAML frontmatter schema for Claude Code agent definition files (.md files). This matters because Jerry's agent governance relies on validating these files, and any mismatch between our schema and Anthropic's actual runtime behavior creates either false rejections (blocking valid agents) or false acceptances (allowing invalid configurations).

**Key findings:**

1. **Our existing schema is mostly accurate but missing two fields.** Anthropic documents 15 frontmatter fields for agents. Our schema at `docs/schemas/claude-code-frontmatter-v1.schema.json` covers 13 of them (including the undocumented `color`). We are missing `effort` and `initialPrompt`, both added in recent Claude Code releases.

2. **Our `mcpServers` type is wrong.** The official documentation defines `mcpServers` as an **array** (list) of either string references or inline object definitions. Our schema defines it as an **object** (dictionary). This is a structural mismatch that would fail validation on correctly-formatted agent files.

3. **Our `model` enum is incomplete.** Anthropic now accepts full model IDs (e.g., `claude-opus-4-6`, `claude-sonnet-4-6`) in addition to the aliases (`sonnet`, `opus`, `haiku`, `inherit`). Our enum restricts to only the four aliases.

4. **No official JSON schema exists from Anthropic.** The Python Agent SDK has a `types.py` with `AgentDefinition` dataclass, but no published JSON Schema. Our schema fills a real gap.

5. **The Task tool was renamed to Agent in v2.1.63.** Existing `Task(...)` references in settings and agent definitions still work as aliases.

---

## L1: Complete Field Reference

### Official Supported Frontmatter Fields (15 fields)

The following table represents the **authoritative** set of frontmatter fields documented by Anthropic at [code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents) as of March 2026.

| # | Field | Required | Type | Default | Constraints | Description |
|---|-------|----------|------|---------|-------------|-------------|
| 1 | `name` | **Yes** | string | -- | Lowercase letters, numbers, hyphens. Kebab-case. Must be unique within scope. | Agent identifier. Becomes the reference name for `Agent(name)` syntax. |
| 2 | `description` | **Yes** | string | -- | No documented max length. Multiline supported via YAML literal block (`\|`). | When Claude should delegate to this agent. Primary routing signal for automatic delegation. Include "use proactively" to encourage automatic invocation. |
| 3 | `tools` | No | string or array | Inherits ALL tools from parent | Comma-separated string or YAML array. Special syntax: `Agent(name)` restricts spawnable subagents. | Allowlist of tools. If omitted, inherits all tools from the main conversation including MCP tools. |
| 4 | `disallowedTools` | No | string or array | none | Same format as `tools`. Applied first when both are set. | Denylist of tools to remove from inherited or specified set. |
| 5 | `model` | No | string | `inherit` | Accepts aliases (`sonnet`, `opus`, `haiku`, `inherit`) **or** full model IDs (e.g., `claude-opus-4-6`, `claude-sonnet-4-6`). Same values as `--model` CLI flag. | Model selection. Resolution order: (1) `CLAUDE_CODE_SUBAGENT_MODEL` env var, (2) per-invocation model parameter, (3) frontmatter model, (4) main conversation model. |
| 6 | `permissionMode` | No | string (enum) | inherits from parent | `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan` | Permission prompt behavior. If parent uses `bypassPermissions`, it takes precedence. If parent uses auto mode, subagent inherits auto mode and frontmatter is ignored. |
| 7 | `maxTurns` | No | integer | no limit | Minimum 1 (implicit). | Maximum agentic turns before the subagent stops. |
| 8 | `skills` | No | array of strings | none (does NOT inherit from parent) | Skill names matching existing skills. | Skills to preload. Full skill content is injected into agent context at startup. Subagents do NOT inherit skills from parent conversation. |
| 9 | `mcpServers` | No | **array** | inherits from parent | Each entry is either a string (server name reference) or an inline definition `{name: {type, command, args}}`. | MCP servers available to this subagent. String references share parent session connection. Inline definitions are connected at subagent start, disconnected at finish. |
| 10 | `hooks` | No | object | none | Keys are hook event names. Values are arrays of hook configurations. All hook events are supported. | Lifecycle hooks scoped to this subagent. `Stop` in frontmatter is auto-converted to `SubagentStop` at runtime. Most common: `PreToolUse`, `PostToolUse`, `Stop`. |
| 11 | `memory` | No | string (enum) | none | `user`, `project`, `local` | Persistent memory scope. Enables cross-session learning. Creates memory directory: `user` at `~/.claude/agent-memory/<name>/`, `project` at `.claude/agent-memory/<name>/`, `local` at `.claude/agent-memory-local/<name>/`. When enabled, Read/Write/Edit tools auto-enabled. First 200 lines or 25KB of MEMORY.md injected into system prompt. |
| 12 | `background` | No | boolean | `false` | -- | Always run this subagent as a background task. Background subagents auto-deny permissions not pre-approved. AskUserQuestion tool calls fail (but subagent continues). |
| 13 | `effort` | No | string (enum) | inherits from session | `low`, `medium`, `high`, `max` (Opus 4.6 only) | Effort level when this subagent is active. Overrides the session effort level. Controls reasoning depth. |
| 14 | `isolation` | No | string (enum) | none | `worktree` | Run in a temporary git worktree. Gives isolated copy of repository. Worktree auto-cleaned if subagent makes no changes. |
| 15 | `initialPrompt` | No | string | none | Commands (`/skill-name`) and skills are processed. | Auto-submitted as the first user turn when this agent runs as the main session agent (via `--agent` flag or `agent` setting). Prepended to any user-provided prompt. Only meaningful for `--agent` mode, not for subagent invocations. |

### Undocumented But Observed Fields

| Field | Status | Evidence | Behavior |
|-------|--------|----------|----------|
| `color` | **Used by `/agents` command** but not in official frontmatter table | GitHub Issue [#8501](https://github.com/anthropics/claude-code/issues/8501); `/agents` interactive UI generates it | Background color for subagent UI identification. Values observed: `blue`, `purple`, `yellow`, `green`, `red`, and possibly others. Selected during `/agents` creation flow ("Choose a color" step). |

### Fields in `--agents` CLI JSON vs File-Based Frontmatter

The `--agents` CLI flag accepts JSON with one additional field not in file-based frontmatter:

| Field | In `.md` frontmatter | In `--agents` JSON | Notes |
|-------|---------------------|---------------------|-------|
| `prompt` | No (markdown body serves this purpose) | **Yes** | Equivalent to the markdown body in file-based agents. |

All 15 frontmatter fields are also supported in the `--agents` JSON format.

### Agent SDK Python `AgentDefinition` Dataclass

The Python Agent SDK (`claude-agent-sdk-python`) defines a subset:

```python
@dataclass
class AgentDefinition:
    description: str
    prompt: str
    tools: list[str] | None = None
    model: Literal["sonnet", "opus", "haiku", "inherit"] | None = None
    skills: list[str] | None = None
    memory: Literal["user", "project", "local"] | None = None
    mcpServers: list[str | dict[str, Any]] | None = None
```

**Source:** [github.com/anthropics/claude-agent-sdk-python/blob/main/src/claude_agent_sdk/types.py](https://github.com/anthropics/claude-agent-sdk-python/blob/main/src/claude_agent_sdk/types.py)

This SDK type is a **subset** of the full Claude Code frontmatter -- it omits `hooks`, `permissionMode`, `maxTurns`, `background`, `isolation`, `effort`, `initialPrompt`, `disallowedTools`, and `color`. The SDK is for programmatic agent orchestration; Claude Code's file-based agents support the full set.

---

## L2: Strategic Implications

### 1. Schema Update Required (Critical)

Our existing schema at `docs/schemas/claude-code-frontmatter-v1.schema.json` requires the following corrections:

| Issue | Current State | Required State | Impact |
|-------|--------------|----------------|--------|
| **Missing `effort`** | Not present | Add as enum: `low`, `medium`, `high`, `max` | Jerry agents using effort frontmatter would fail validation |
| **Missing `initialPrompt`** | Not present | Add as string | Agents designed for `--agent` mode would fail validation |
| **Wrong `mcpServers` type** | `type: "object"` with `additionalProperties` | `type: "array"` with items being string or object | Currently accepts invalid format, rejects valid format |
| **Incomplete `model` enum** | `enum: ["sonnet", "opus", "haiku", "inherit"]` | Either remove enum constraint or add pattern for full model IDs | Agents using full model IDs (e.g., `claude-opus-4-6`) would fail validation |

### 2. Governance Architecture Implications

**Separation of concerns is validated.** Anthropic's frontmatter is strictly for Claude Code runtime behavior (tool access, model selection, hooks, permissions). Jerry's governance metadata (version, tool_tier, identity, persona, capabilities, guardrails, constitution) correctly lives in the separate `.governance.yaml` file per H-34. There is zero overlap -- Anthropic does not define or consume any governance fields.

**`additionalProperties: true` in our schema is correct.** Claude Code silently ignores unrecognized frontmatter fields. Our schema flags them for governance awareness but does not reject them. This is the right behavior.

### 3. Tool Naming Convention

The `tools` and `disallowedTools` fields use exact tool names from Claude Code's internal tool registry. The `Agent(name)` syntax for restricting spawnable subagents is a special extension. Our schema currently handles this as a string, which is correct -- no structural change needed, but documentation should note the `Agent(name)` pattern.

### 4. Hook Events Scope

All 24+ hook events are supported in agent frontmatter (not just the 4 we document). Our schema uses `additionalProperties: true` for hooks, which correctly accommodates this. However, our documentation in `agent-development-standards.md` only mentions `PreToolUse`, `PostToolUse`, `SubagentStart`, and `SubagentStop` -- the full set is much larger (see [Hook Events Reference](#hook-events-reference)).

### 5. Skill Frontmatter vs Agent Frontmatter

Skills and agents have **different** frontmatter schemas. Skills support fields not in agent frontmatter (`disable-model-invocation`, `user-invocable`, `allowed-tools`, `context`, `agent`, `paths`, `shell`, `argument-hint`). Agent frontmatter supports fields not in skill frontmatter (`tools`, `disallowedTools`, `mcpServers`, `permissionMode`, `maxTurns`, `background`, `isolation`, `initialPrompt`, `memory`). The `name`, `description`, `model`, `effort`, `hooks`, and `skills` fields appear in both. Jerry's skill definitions (SKILL.md files) use the skill frontmatter schema, not the agent schema.

### 6. Risk: No Upstream JSON Schema

Anthropic does not publish a JSON Schema for agent frontmatter. Our schema is Jerry's independent interpretation of the documentation. This means:
- **Positive:** We fill a real gap. No one else has a formal schema.
- **Risk:** Upstream changes (new fields, changed types) require manual tracking via changelog monitoring.
- **Mitigation:** Pin schema version to Claude Code version. Add changelog monitoring to maintenance process.

---

## Gap Analysis

### Our Schema vs Anthropic's Official Specification

| Field | Our Schema | Anthropic Official | Status |
|-------|-----------|-------------------|--------|
| `name` | string, pattern `^[a-z][a-z0-9]*(-[a-z0-9]+)*$` | string, "lowercase letters and hyphens" | **MATCH** (our pattern is stricter but compatible) |
| `description` | string, minLength 10 | string, required | **MATCH** (our minLength is stricter) |
| `model` | enum: `sonnet, opus, haiku, inherit` | enum aliases + full model IDs + `inherit` | **NEEDS UPDATE** -- add full model ID support |
| `tools` | oneOf string/array | string or array, comma-separated | **MATCH** |
| `disallowedTools` | oneOf string/array | string or array | **MATCH** |
| `mcpServers` | **object** with additionalProperties | **array** of string or inline-object | **NEEDS FIX** -- wrong type |
| `permissionMode` | enum: 5 values | enum: 5 values | **MATCH** |
| `maxTurns` | integer, minimum 1 | integer | **MATCH** |
| `skills` | array of strings | array of strings | **MATCH** |
| `hooks` | object, additionalProperties true | object with event name keys | **MATCH** (permissive, correct) |
| `memory` | enum: `user, project, local` | enum: `user, project, local` | **MATCH** |
| `background` | boolean | boolean, default false | **MATCH** |
| `isolation` | enum: `worktree` | enum: `worktree` | **MATCH** |
| `color` | string (documented as undocumented) | Not in official table; used by /agents UI | **ACCEPTABLE** |
| `effort` | **MISSING** | enum: `low, medium, high, max` | **NEEDS ADDITION** |
| `initialPrompt` | **MISSING** | string | **NEEDS ADDITION** |

### Summary

- **11 fields match** correctly
- **2 fields missing** (`effort`, `initialPrompt`)
- **1 field wrong type** (`mcpServers`: object should be array)
- **1 field incomplete** (`model`: needs full model ID support)
- **1 field acceptable** (`color`: correctly documented as undocumented)

---

## Agent Discovery and Spawning

### How Claude Code Finds Agents

Claude Code discovers agents from four sources, in priority order (highest wins when names collide):

| Priority | Source | Location | Scope |
|----------|--------|----------|-------|
| 1 (highest) | CLI flag | `--agents '{JSON}'` | Current session only |
| 2 | Project | `.claude/agents/*.md` | Current project |
| 3 | User | `~/.claude/agents/*.md` | All projects for this user |
| 4 (lowest) | Plugin | `<plugin>/agents/*.md` | Where plugin is enabled |

**Loading timing:** Agents are loaded at session start. Adding a file manually during a session requires restarting the session or using `/agents` to reload.

**Name uniqueness:** When multiple agents share the same `name`, the higher-priority source wins. The `/agents` command shows which agents are active and which are overridden.

### How Subagents Are Spawned

1. **Claude decides** to delegate based on the task and the agent's `description` field.
2. **Claude invokes the `Agent` tool** (renamed from `Task` in v2.1.63) with parameters:
   - `prompt`: The task description for the subagent (only channel from parent to subagent)
   - `subagent_type`: Which agent definition to use (matches `name`)
   - `model`: Optional per-invocation model override
   - `run_in_background`: Optional boolean
   - Additional parameters: `resume`, `max_turns`, `name`, `team_name`, `mode`, `isolation`
3. **Subagent receives** only: its system prompt (from markdown body), basic environment details (working directory), and the task prompt. It does NOT receive the main conversation history.
4. **Subagent executes** in its own context window with its own tool set.
5. **Subagent returns** its final message to the parent. Intermediate tool calls and results stay inside the subagent context.
6. **Subagents cannot spawn other subagents.** The `Agent` tool in a subagent's context is not available for further nesting.

### Context Isolation Model

| Aspect | Behavior |
|--------|----------|
| Conversation history | NOT passed to subagent |
| System prompt | Agent's markdown body + basic environment details |
| CLAUDE.md | Loaded through normal message flow |
| Skills | Only those listed in `skills` frontmatter (NOT inherited from parent) |
| Tools | Inherited from parent unless `tools` or `disallowedTools` restrict them |
| Permissions | Inherited from parent; `permissionMode` can override |
| MCP servers | Inherited from parent + any declared in `mcpServers` |
| Memory | Separate memory directory per agent name and scope |

### Resuming Subagents

- Claude uses `SendMessage` tool with the agent's ID to resume a stopped subagent.
- Resumed subagents retain full conversation history.
- If a stopped subagent receives `SendMessage`, it auto-resumes in the background.
- Subagent transcripts persist at `~/.claude/projects/{project}/{sessionId}/subagents/agent-{agentId}.jsonl`.

---

## Tool Reference

The following are the exact tool names valid for `tools` and `disallowedTools` frontmatter fields. These are Claude Code's internal tools as documented at [code.claude.com/docs/en/tools-reference](https://code.claude.com/docs/en/tools-reference).

| Tool Name | Permission Required | Description |
|-----------|-------------------|-------------|
| `Agent` | No | Spawns a subagent with its own context window |
| `AskUserQuestion` | No | Asks multiple-choice questions to gather requirements |
| `Bash` | Yes | Executes shell commands |
| `CronCreate` | No | Schedules recurring or one-shot prompts |
| `CronDelete` | No | Cancels a scheduled task by ID |
| `CronList` | No | Lists all scheduled tasks |
| `Edit` | Yes | Makes targeted edits to files |
| `EnterPlanMode` | No | Switches to plan mode |
| `EnterWorktree` | No | Creates isolated git worktree |
| `ExitPlanMode` | Yes | Presents plan and exits plan mode |
| `ExitWorktree` | No | Exits worktree session |
| `Glob` | No | Finds files by pattern matching |
| `Grep` | No | Searches patterns in file contents |
| `ListMcpResourcesTool` | No | Lists MCP server resources |
| `LSP` | No | Code intelligence via language servers |
| `NotebookEdit` | Yes | Modifies Jupyter notebook cells |
| `PowerShell` | Yes | Executes PowerShell commands (Windows, opt-in) |
| `Read` | No | Reads file contents |
| `ReadMcpResourceTool` | No | Reads specific MCP resource by URI |
| `Skill` | Yes | Executes a skill in the main conversation |
| `TaskCreate` | No | Creates a task in the task list |
| `TaskGet` | No | Retrieves task details |
| `TaskList` | No | Lists all tasks with status |
| `TaskOutput` | No | (Deprecated) Retrieves background task output |
| `TaskStop` | No | Kills a running background task |
| `TaskUpdate` | No | Updates task status/dependencies |
| `TodoWrite` | No | Manages session task checklist (non-interactive/SDK) |
| `ToolSearch` | No | Searches for deferred MCP tools |
| `WebFetch` | Yes | Fetches content from a URL |
| `WebSearch` | Yes | Performs web searches |
| `Write` | Yes | Creates or overwrites files |

**Special syntax:** `Agent(name1, name2)` restricts which subagents can be spawned. This is an allowlist -- only named agents can be invoked.

**MCP tools:** MCP server tools follow the pattern `mcp__<server-name>__<tool-name>` and are also valid in `tools`/`disallowedTools` fields.

---

## Hook Events Reference

All hook events supported in agent frontmatter. The `Stop` event in frontmatter is auto-converted to `SubagentStop` at runtime for subagents.

| Event | When It Fires | Can Block? | Hook Types |
|-------|--------------|------------|------------|
| `SessionStart` | Session begins or resumes | No | command only |
| `InstructionsLoaded` | CLAUDE.md or rules loaded | No | command, http, prompt, agent |
| `UserPromptSubmit` | User submits a prompt | Yes | command, http, prompt, agent |
| `PreToolUse` | Before tool execution | Yes | command, http, prompt, agent |
| `PermissionRequest` | Permission dialog shown | Yes | command, http, prompt, agent |
| `PostToolUse` | After tool succeeds | Yes | command, http, prompt, agent |
| `PostToolUseFailure` | After tool fails | No | command, http, prompt, agent |
| `Notification` | Notification sent | No | command, http, prompt, agent |
| `SubagentStart` | Subagent spawned | No | command, http, prompt, agent |
| `SubagentStop` | Subagent finishes | Yes | command, http, prompt, agent |
| `TaskCreated` | Task created | Yes | command, http, prompt, agent |
| `TaskCompleted` | Task marked complete | Yes | command, http, prompt, agent |
| `Stop` | Claude finishes responding | Yes | command, http, prompt, agent |
| `StopFailure` | Turn ends due to API error | No | command, http, prompt, agent |
| `TeammateIdle` | Agent team teammate about to idle | Yes | command, http, prompt, agent |
| `ConfigChange` | Config file changes | Yes | command, http, prompt, agent |
| `CwdChanged` | Working directory changes | No | command only |
| `FileChanged` | Watched file changes | No | command only |
| `PreCompact` | Before context compaction | No | command, http, prompt, agent |
| `PostCompact` | After compaction completes | No | command, http, prompt, agent |
| `WorktreeCreate` | Worktree creation | Yes | command, http, prompt, agent |
| `WorktreeRemove` | Worktree removal | No | command, http, prompt, agent |
| `Elicitation` | MCP server requests input | Yes | command, http, prompt, agent |
| `ElicitationResult` | User responds to elicitation | Yes | command, http, prompt, agent |
| `SessionEnd` | Session terminates | No | command, http, prompt, agent |

---

## Skill Frontmatter Reference

Skills use a **different** frontmatter schema than agents. Both are .md files with YAML frontmatter, but the field sets differ.

### Skill-Only Fields (NOT in Agent Frontmatter)

| Field | Type | Description |
|-------|------|-------------|
| `disable-model-invocation` | boolean | Prevent Claude from auto-loading this skill. Default: false |
| `user-invocable` | boolean | Hide from `/` menu. Default: true |
| `allowed-tools` | string (comma-separated) | Tools allowed without permission when skill is active |
| `context` | string | Set to `fork` to run in a forked subagent context |
| `agent` | string | Which subagent type to use when `context: fork` |
| `paths` | string or array | Glob patterns limiting when skill is auto-activated |
| `shell` | string | Shell for inline commands: `bash` (default) or `powershell` |
| `argument-hint` | string | Hint shown during autocomplete (e.g., `[issue-number]`) |

### Shared Fields (In Both Agent and Skill Frontmatter)

| Field | Notes |
|-------|-------|
| `name` | Optional in skills (defaults to directory name); required in agents |
| `description` | Recommended in skills; required in agents |
| `model` | Same behavior in both |
| `effort` | Same behavior in both |
| `hooks` | Same behavior in both |
| `skills` | Not documented for skill frontmatter, but available in agent frontmatter |

### Agent-Only Fields (NOT in Skill Frontmatter)

| Field | Notes |
|-------|-------|
| `tools` | Skills use `allowed-tools` instead |
| `disallowedTools` | Not applicable to skills |
| `mcpServers` | Skills do not scope MCP servers |
| `permissionMode` | Skills inherit permission context |
| `maxTurns` | Skills do not have turn limits |
| `memory` | Skills do not have persistent memory |
| `background` | Skills do not run in background |
| `isolation` | Skills do not support worktree isolation |
| `initialPrompt` | Skills do not support auto-prompts |

---

## Methodology

### Sources Consulted

| Source | Type | Credibility | What Was Extracted |
|--------|------|------------|-------------------|
| [code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents) | Official documentation | HIGH | Complete frontmatter field table, examples, behavior descriptions |
| [code.claude.com/docs/en/tools-reference](https://code.claude.com/docs/en/tools-reference) | Official documentation | HIGH | Complete tool name list for tools/disallowedTools fields |
| [code.claude.com/docs/en/hooks](https://code.claude.com/docs/en/hooks) | Official documentation | HIGH | Complete hook events, input/output schemas |
| [code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills) | Official documentation | HIGH | Skill frontmatter reference, distinction from agent frontmatter |
| [github.com/anthropics/claude-code/issues/8501](https://github.com/anthropics/claude-code/issues/8501) | GitHub issue | MEDIUM | Undocumented `color` field, schema documentation gaps |
| [github.com/anthropics/claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python) | Official SDK source | HIGH | AgentDefinition dataclass, type constraints |
| [code.claude.com/docs/en/changelog](https://code.claude.com/docs/en/changelog) | Official changelog | HIGH | Timeline of field additions (effort, memory, initialPrompt) |
| [releasebot.io/updates/anthropic/claude-code](https://releasebot.io/updates/anthropic/claude-code) | Aggregator | MEDIUM | Cross-reference for changelog entries |

### Research Approach

1. **Primary source:** Fetched and analyzed the complete official subagent documentation page.
2. **Cross-validation:** Compared against the Python Agent SDK types.py for type constraints.
3. **Gap identification:** Compared each field against our existing schema.
4. **Changelog review:** Searched for recent additions to identify fields we might be missing.
5. **Community validation:** Checked GitHub issues for known documentation gaps.

### What Was NOT Found

- **No official JSON Schema from Anthropic.** The Python SDK has typed dataclasses; the TypeScript SDK has TypeScript interfaces. Neither publishes a JSON Schema.
- **No exhaustive `color` field enum.** The `/agents` UI presents color options but no documentation enumerates all valid values.
- **No formal `name` pattern specification.** The docs say "lowercase letters and hyphens" but do not specify regex. Numbers appear to be allowed based on observation.
- **No `maxTurns` upper bound.** Documentation says "Maximum number of agentic turns" with no stated maximum value.
- **No `description` length limit.** No maximum length documented for agent descriptions.

---

## References

1. [Create custom subagents - Claude Code Docs](https://code.claude.com/docs/en/sub-agents) -- Key insight: Complete frontmatter field table with 15 official fields, priority-based agent discovery, context isolation model, and `Agent(name)` tool restriction syntax.
2. [Tools reference - Claude Code Docs](https://code.claude.com/docs/en/tools-reference) -- Key insight: 31 internal tools with exact names for `tools`/`disallowedTools` fields, including recently added Task* tools and LSP.
3. [Hooks reference - Claude Code Docs](https://code.claude.com/docs/en/hooks) -- Key insight: 24+ hook events all supported in agent frontmatter, with full input/output JSON schemas for PreToolUse and PostToolUse.
4. [Extend Claude with skills - Claude Code Docs](https://code.claude.com/docs/en/skills) -- Key insight: Skills have a different frontmatter schema from agents; shared fields are name, description, model, effort, hooks.
5. [GitHub Issue #8501 - Claude Code subagent YAML Frontmatter authoritative documentation](https://github.com/anthropics/claude-code/issues/8501) -- Key insight: `color` field generated by `/agents` command but not in official docs; documentation gap acknowledged.
6. [Claude Agent SDK Python - types.py](https://github.com/anthropics/claude-agent-sdk-python/blob/main/src/claude_agent_sdk/types.py) -- Key insight: AgentDefinition dataclass confirms field types; `mcpServers` is `list[str | dict[str, Any]]` (array, not object).
7. [Changelog - Claude Code Docs](https://code.claude.com/docs/en/changelog) -- Key insight: `effort` frontmatter added for skills/commands; `memory` frontmatter added for agents; `initialPrompt` added; Task renamed to Agent in v2.1.63.
8. [Skill authoring best practices - Claude API Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) -- Key insight: effort field values `low`, `medium`, `high`, `max` (Opus 4.6 only).
9. [Claude Code by Anthropic - Release Notes](https://releasebot.io/updates/anthropic/claude-code) -- Key insight: Cross-reference confirming effort, maxTurns, disallowedTools additions for plugin-shipped agents.
10. [GitHub Issue #6005 - Feature Request: Add disallowed-tools to sub-agent frontmatter](https://github.com/anthropics/claude-code/issues/6005) -- Key insight: `disallowedTools` was initially a feature request, now implemented.

---

*Research completed: 2026-03-26*
*Agent: ps-researcher*
*Confidence: HIGH (0.90)*
*Sources: 10 (8 HIGH credibility, 2 MEDIUM)*
