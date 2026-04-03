# Heuristic Evaluation: Claude Code Frontmatter Schema DX

> Nielsen Heuristic Evaluation of `claude-code-frontmatter-v1.schema.json` and
> `claude-code-skill-frontmatter-v1.schema.json` against developer experience
> criteria for JSON Schema field documentation.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Scope and Method](#scope-and-method) | What was evaluated and how |
| [Steelman: Strengths](#steelman-strengths) | What both schemas do well |
| [Findings: Agent Schema](#findings-agent-schema) | Per-finding analysis for frontmatter-v1 |
| [Findings: Skill Schema](#findings-skill-schema) | Per-finding analysis for skill-frontmatter-v1 |
| [Cross-Schema Findings](#cross-schema-findings) | Issues affecting both schemas |
| [Common Mistake Analysis](#common-mistake-analysis) | 10 common mistakes with error message assessment |
| [Technical Criteria Assessment](#technical-criteria-assessment) | EN-002 TC-1 through TC-4 verdict |
| [Metrics Summary](#metrics-summary) | Finding counts by severity |
| [Recommendations by Priority](#recommendations-by-priority) | Ordered remediation list |

---

## Scope and Method

**Schemas evaluated:**
- Agent schema: `docs/schemas/claude-code-frontmatter-v1.schema.json` (16 fields)
- Skill schema: `docs/schemas/claude-code-skill-frontmatter-v1.schema.json` (18 fields)

**Heuristics applied:**
- H5: Error Prevention
- H9: Help users recognize, diagnose, and recover from errors
- H10: Help and Documentation

**Severity scale:**
- 0 = Cosmetic
- 1 = Minor: Users can easily work around
- 2 = Major: Users will struggle but can recover
- 3 = Severe: Users may fail to complete their task
- 4 = Catastrophic: Users cannot complete their task

**Evaluation date:** 2026-03-26
**Evaluator:** ps-reviewer (convergent, evidence-based)

---

## Steelman: Strengths

Before identifying issues, the strongest aspects of both schemas deserve acknowledgment:

1. **Model field is comprehensive.** Both schemas document full model IDs, aliases, extended context variants, and environment variable override order in a single description. This is exemplary field documentation -- most developers will not need to look elsewhere.

2. **`mcpServers` dual-format handling is well-documented.** The agent schema correctly documents that both the official array format and legacy object format are accepted, preventing developers from breaking existing files when they discover the official docs only describe the array form.

3. **`permissionMode` uses an enum.** Enumerating all five valid values eliminates one entire class of typo errors for a field that has critical security implications.

4. **`effort: max` warning is present.** Both schemas call out that `max` is Opus 4.6 only, which prevents a subtle misconfiguration with no obvious runtime error.

5. **`disable-model-invocation` vs `user-invocable` distinction is documented.** The skill schema explicitly explains that `user-invocable` controls menu visibility only, and that disabling programmatic invocation requires the other field. This prevents a significant developer confusion.

6. **`background` subagent behavior is documented.** The behavior around auto-denied permissions and failing `AskUserQuestion` calls is non-obvious and would cause hard-to-debug issues without documentation.

7. **Schema-level `description` sources are cited.** The root schema descriptions reference the Anthropic docs and the research artifact, giving developers a path to the authoritative source.

---

## Findings: Agent Schema

### [AG-001] `disallowedTools` has no description examples or valid tool names

| Attribute | Value |
|-----------|-------|
| **Heuristic** | H10 (Help and Documentation) |
| **Severity** | 2 (Major) |
| **Location** | `properties.disallowedTools.description` |
| **Field** | `disallowedTools` |

**Current description:**
> "Denylist of tools to remove from inherited or specified set. Applied before tools allowlist."

**Problem:** The description explains the semantics correctly but gives no example values. A developer who has not memorized tool name casing (is it `Bash` or `bash`? `WebSearch` or `web_search`?) will not know what string values to put here. The `tools` field provides an example in its `oneOf` sub-schema (`'Read, Write, Glob, Bash'`), but `disallowedTools` provides nothing. A developer cannot tell from this field alone whether the values should be PascalCase, snake_case, or kebab-case.

**Recommended improvement:**
```
"Denylist of tools to remove from inherited or specified set. Applied before tools allowlist. Example: ['Bash', 'Write', 'mcp__context7__query-docs']. Tool names are PascalCase for built-in tools and 'mcp__{server}__{tool}' for MCP tools."
```

---

### [AG-002] `maxTurns` has no guidance on choosing a value

| Attribute | Value |
|-----------|-------|
| **Heuristic** | H10 (Help and Documentation) |
| **Severity** | 1 (Minor) |
| **Location** | `properties.maxTurns.description` |
| **Field** | `maxTurns` |

**Current description:**
> "Maximum agentic turns before agent stops."

**Problem:** The description is technically accurate but offers no practical guidance. What happens when the limit is reached -- does the agent error, or does it stop gracefully with whatever it has? What is the default? What values are typical for different agent types? A developer trying to cap a potentially expensive agent has no reference point.

**Recommended improvement:**
```
"Maximum agentic turns before agent stops. Agent halts gracefully -- partial results may be returned. No default; omit to allow unlimited turns. Typical values: 5-10 for focused tasks, 20-50 for research, unlimited for orchestration. Example: 10"
```

---

### [AG-003] `skills` field gives no example skill names or path format

| Attribute | Value |
|-----------|-------|
| **Heuristic** | H10 (Help and Documentation) |
| **Severity** | 2 (Major) |
| **Location** | `properties.skills.description` |
| **Field** | `skills` |

**Current description:**
> "Skill names to preload. Full skill content injected into agent context at startup. Subagents do NOT inherit skills from parent conversation."

**Problem:** The description correctly explains what preloading does and the inheritance behavior. However, it does not say what a "skill name" looks like. Are these directory names (e.g., `worktracker`), slash-command names (e.g., `problem-solving`), or full paths? Without an example, a developer who wants to preload the `/worktracker` skill has to discover by trial and error whether to write `worktracker`, `problem-solving`, or `skills/worktracker`.

**Recommended improvement:**
```
"Skill names to preload into agent context at startup. Use the skill directory name (e.g., 'worktracker', 'problem-solving'). Full skill content injected before any user turn. Subagents do NOT inherit skills from parent conversation. Example: ['worktracker', 'problem-solving']"
```

---

### [AG-004] `hooks` description lists 24+ events inline but gives no structure example

| Attribute | Value |
|-----------|-------|
| **Heuristic** | H5 (Error Prevention) + H10 (Help and Documentation) |
| **Severity** | 2 (Major) |
| **Location** | `properties.hooks.description` |
| **Field** | `hooks` |

**Current description:**
> "Lifecycle hooks scoped to this agent. Supports 24+ hook events: SessionStart, UserPromptSubmit, PreToolUse, PermissionRequest, PostToolUse, PostToolUseFailure, Notification, SubagentStart, SubagentStop, TaskCreated, TaskCompleted, Stop, StopFailure, TeammateIdle, InstructionsLoaded, ConfigChange, CwdChanged, FileChanged, WorktreeCreate, WorktreeRemove, PreCompact, PostCompact, Elicitation, ElicitationResult, SessionEnd. Stop in frontmatter auto-converts to SubagentStop at runtime."

**Problem:** The list of 24+ event names is useful, but the description never shows what the object value should look like. A developer writing hooks for the first time has no template. The `Stop`-to-`SubagentStop` auto-conversion is buried at the end of a long sentence and is the kind of non-obvious behavior that causes runtime surprises. Additionally, without showing the structure (event name -> command or shell expression), the entire field is opaque. This problem is amplified because `additionalProperties: true` means no sub-schema validation will catch structural errors.

**Recommended improvement:**
```
"Lifecycle hooks scoped to this agent. Object keyed by event name. Example: {\"PreToolUse\": [{\"matcher\": \"Bash\", \"hooks\": [{\"type\": \"command\", \"command\": \"echo before-bash\"}]}]}. Supported events: SessionStart, PreToolUse, PostToolUse, PostToolUseFailure, Stop (auto-converted to SubagentStop). See hooks docs for full structure. WARNING: 'Stop' in frontmatter is silently converted to 'SubagentStop' at runtime."
```

---

### [AG-005] `name` description does not state that consecutive hyphens are forbidden

| Attribute | Value |
|-----------|-------|
| **Heuristic** | H5 (Error Prevention) |
| **Severity** | 1 (Minor) |
| **Location** | `properties.name.description` |
| **Field** | `name` |

**Current description:**
> "Agent identifier. Kebab-case, lowercase letters, numbers, and hyphens. Must be unique within scope (project > user > plugin). Must not contain consecutive hyphens or reserved words 'claude'/'anthropic'."

**Problem:** The description mentions "must not contain consecutive hyphens" but the `pattern` (`^[a-z][a-z0-9]*(-[a-z0-9]+)*$`) actually enforces this. The description is consistent with the pattern, so this is not an error. However, the description does not mention that the name must begin with a lowercase letter (not a digit), which the pattern enforces. A developer naming an agent `3d-renderer` will get a pattern mismatch error with no explanation. Severity is Minor because the pattern violation message itself is visible, but the reason is not.

**Recommended improvement:**
```
"Agent identifier. Kebab-case only: must start with a lowercase letter, then lowercase letters, numbers, or hyphens. No consecutive hyphens. Must not contain reserved words 'claude' or 'anthropic'. Must be unique within scope (project > user > plugin). Example: 'ps-researcher', 'wt-auditor'"
```

---

### [AG-006] `color` field documents only "Known values" as a hint, not an enum

| Attribute | Value |
|-----------|-------|
| **Heuristic** | H5 (Error Prevention) |
| **Severity** | 1 (Minor) |
| **Location** | `properties.color.description` |
| **Field** | `color` |

**Current description:**
> "Background color for subagent UI identification. Used by /agents interactive command. Not in official frontmatter table. Known values: blue, purple, yellow, green, red. See github.com/anthropics/claude-code/issues/8501."

**Problem:** The field type is `string` with no enum, which is appropriate given the field is undocumented and the value set may change. The description correctly flags it as unofficial. The issue is minor: "Known values" reads ambiguously -- does this mean other values silently fail, or are other values accepted? The GitHub issue reference is helpful for provenance but may break when the issue is closed or the URL changes.

**Recommended improvement:**
```
"Background color for subagent UI identification in /agents command. Not in official frontmatter table (undocumented field). Observed values: 'blue', 'purple', 'yellow', 'green', 'red'. Other values may be silently ignored. Omit if UI color is not needed."
```

---

### [AG-007] `isolation` has only one valid enum value with no explanation of when NOT to use it

| Attribute | Value |
|-----------|-------|
| **Heuristic** | H5 (Error Prevention) |
| **Severity** | 1 (Minor) |
| **Location** | `properties.isolation.description` |
| **Field** | `isolation` |

**Current description:**
> "Run in temporary git worktree. Gives isolated copy of repository. Auto-cleaned if subagent makes no changes."

**Problem:** The description explains what `worktree` does but does not warn about the performance cost (worktree creation takes time) or when isolation is counterproductive (e.g., agents that need to read files written by the parent during the same session). The `auto-cleaned if subagent makes no changes` behavior is important: if a developer uses isolation expecting an audit trail, the absence of changes silently removes that trail.

**Recommended improvement:**
```
"Run in an isolated temporary git worktree copy of the repository. Use when you want file-system isolation from the parent session. Auto-cleaned if the subagent makes no changes (no audit trail). Adds ~1-2s startup latency. Only valid value: 'worktree'. Example: isolation: worktree"
```

---

### [AG-008] `initialPrompt` field omits what happens when agent is invoked as a subagent

| Attribute | Value |
|-----------|-------|
| **Heuristic** | H5 (Error Prevention) |
| **Severity** | 2 (Major) |
| **Location** | `properties.initialPrompt.description` |
| **Field** | `initialPrompt` |

**Current description:**
> "Auto-submitted as first user turn when agent runs as main session agent (--agent flag or agent setting). Commands (/skill-name) and skills are processed. Prepended to user-provided prompt. Only meaningful for --agent mode, not subagent invocations."

**Problem:** The last sentence warns that `initialPrompt` is "only meaningful for --agent mode." However, it does not say what happens when this field is set and the agent IS invoked as a subagent (via Task tool) -- is the field silently ignored, or does it behave unexpectedly? Many Jerry agents are subagents, not main session agents. A developer who sets `initialPrompt` on a subagent agent definition expecting it to customize the startup behavior will get silent failure with no diagnostic.

**Recommended improvement:**
```
"Auto-submitted as first user turn when agent runs in --agent mode (main session). Commands and skill invocations are processed. Prepended to any user-provided prompt. When this agent is invoked as a subagent (via Task tool), this field is silently IGNORED. To customize a subagent's starting instructions, pass them in the Task tool's prompt parameter instead."
```

---

## Findings: Skill Schema

### [SK-001] `allowed-tools` description contradicts the field name's intuitive semantics

| Attribute | Value |
|-----------|-------|
| **Heuristic** | H5 (Error Prevention) + H9 (Diagnose and Recover) |
| **Severity** | 3 (Severe) |
| **Location** | `properties.allowed-tools.description` |
| **Field** | `allowed-tools` |

**Current description:**
> "Tools Claude can use without asking permission when this skill is active. Does NOT restrict tools -- grants blanket approval for listed tools on top of global settings."

**Problem:** The current description includes the critical "Does NOT restrict tools" warning, but it is placed at the end and the field name `allowed-tools` strongly implies restriction semantics (an allowlist). A developer looking to restrict an agent to read-only tools using SKILL.md will write `allowed-tools: [Read, Glob]` and believe they have sandboxed the skill. They have not -- the skill still has all tools; they have simply granted blanket approval for Read and Glob. This misconception has security implications and is exacerbated by the agent schema's `tools` field, which DOES restrict. The warning must be the first thing a developer reads, not the last.

**Recommended improvement:**
```
"IMPORTANT: This field grants automatic approval for listed tools -- it does NOT restrict which tools Claude can use. Unlisted tools can still be used but may prompt for permission. To actually restrict tool access, use the 'tools' field in an agent .md file (not a SKILL.md). Example: 'Read, Write, Glob, Bash(git:*)'. Supports permission syntax for fine-grained control."
```

---

### [SK-002] `context` field does not warn that it requires `agent` to be set meaningfully

| Attribute | Value |
|-----------|-------|
| **Heuristic** | H5 (Error Prevention) |
| **Severity** | 2 (Major) |
| **Location** | `properties.context.description` |
| **Field** | `context` |

**Current description:**
> "Set to 'fork' to run in a forked subagent context. Skill content becomes the subagent task prompt. Subagent does NOT have access to conversation history. CLAUDE.md is still loaded. GitHub Issue #17283 (context: fork bug) resolved Jan 2026."

**Problem:** When `context: fork` is set, the `agent` field becomes meaningful for specifying the subagent type. The description explains what `fork` does but does not mention the `agent` field or explain what default behavior to expect if `agent` is omitted. A developer who sets `context: fork` may not realize they should also set `agent` to control which model and tools the forked subagent uses. The three built-in agent types (`Explore`, `Plan`, `general-purpose`) with their different capabilities are only documented in the `agent` field -- there is no cross-reference here.

**Recommended improvement:**
```
"Set to 'fork' to run this skill in a forked subagent context. Skill content becomes the task prompt; subagent has no conversation history access. Use with the 'agent' field to specify subagent type (default: general-purpose with all tools). CLAUDE.md is still loaded. Example: context: fork / agent: Explore (Haiku, read-only)."
```

---

### [SK-003] `agent` field describes three built-in types but gives no example of using a custom agent

| Attribute | Value |
|-----------|-------|
| **Heuristic** | H10 (Help and Documentation) |
| **Severity** | 2 (Major) |
| **Location** | `properties.agent.description` |
| **Field** | `agent` |

**Current description:**
> "Subagent type when context: fork is set. Built-in: Explore (Haiku, read-only tools), Plan (inherits model, read-only tools), general-purpose (inherits model, all tools). Custom: any name matching .claude/agents/*.md. Default: general-purpose."

**Problem:** The description correctly documents built-in values and custom agent support. However, "any name matching .claude/agents/*.md" is ambiguous -- does the value need to include the `.md` extension, or is it just the base filename? A developer writing `agent: ps-researcher` vs `agent: ps-researcher.md` has no guidance on which is correct. The path `.claude/agents/*.md` also suggests agents must be in `.claude/agents/`, but Jerry stores agents in `skills/*/agents/` -- a developer using the custom agent feature with Jerry agents will not find documentation for their specific layout.

**Recommended improvement:**
```
"Subagent type when context: fork is set. Built-in: 'Explore' (Haiku, read-only), 'Plan' (inherits model, read-only), 'general-purpose' (inherits model, all tools). Custom: the base filename without .md extension of a file in .claude/agents/ (e.g., agent: ps-researcher). Only meaningful when context: fork is set. Default: general-purpose."
```

---

### [SK-004] `paths` field gives no pattern syntax examples

| Attribute | Value |
|-----------|-------|
| **Heuristic** | H10 (Help and Documentation) |
| **Severity** | 2 (Major) |
| **Location** | `properties.paths.description` |
| **Field** | `paths` |

**Current description:**
> "Glob patterns limiting when this skill auto-activates. When set, Claude loads the skill only when working with files matching the patterns. Same format as path-specific rules."

**Problem:** "Same format as path-specific rules" is a reference without a target for most developers. A developer adding file-scoped activation has no example to follow. Common questions include: Are these relative to repo root? Does `src/**/*.py` work? Can you mix file extensions? The absence of examples means developers will trial-and-error their way through glob syntax. The description also says "working with files matching" -- does that mean files open in the editor, files touched by the last command, or files in the current working directory?

**Recommended improvement:**
```
"Glob patterns (relative to repo root) that limit when this skill auto-activates. Claude loads the skill only when the active file matches a pattern. Example: ['src/**/*.py', 'tests/**/*.py'] or '**/*.ts'. Standard minimatch glob syntax. Useful for language-specific skills. When omitted, skill activates based on description keywords."
```

---

### [SK-005] `shell` field does not warn about the env var dependency for powershell

| Attribute | Value |
|-----------|-------|
| **Heuristic** | H5 (Error Prevention) + H9 (Diagnose and Recover) |
| **Severity** | 2 (Major) |
| **Location** | `properties.shell.description` |
| **Field** | `shell` |

**Current description:**
> "Shell for !`command` inline blocks in skill content. 'powershell' requires CLAUDE_CODE_USE_POWERSHELL_TOOL=1 env var. Default: bash."

**Problem:** The description mentions the env var requirement but does not explain what happens if the env var is absent and `shell: powershell` is set. Does validation fail at load time, or does Claude silently fall back to bash, or does the inline command block fail at runtime? The failure mode is undocumented, meaning a developer who sets `shell: powershell` without the env var may spend significant time debugging why their inline blocks are not running correctly.

**Recommended improvement:**
```
"Shell for !`command` inline blocks in skill content. 'bash' (default) works without configuration. 'powershell' requires the CLAUDE_CODE_USE_POWERSHELL_TOOL=1 environment variable to be set -- without it, powershell inline blocks will fail silently or error at runtime. Only affects !`command` blocks, not Bash tool calls. Values: 'bash' | 'powershell'."
```

---

### [SK-006] `mode` field has no guidance on when to set it or what UI change to expect

| Attribute | Value |
|-----------|-------|
| **Heuristic** | H10 (Help and Documentation) |
| **Severity** | 1 (Minor) |
| **Location** | `properties.mode.description` |
| **Field** | `mode` |

**Current description:**
> "UNCONFIRMED (secondary source only). When true, categorizes skill as a 'mode command' shown in a separate UI section. Default: false. Not confirmed in primary Anthropic documentation as of March 2026."

**Problem:** The UNCONFIRMED label is appropriate and transparent (this is a DX strength). The issue is that even accepting the uncertainty, the description gives no guidance on what developers should observe when they set `mode: true` to verify it worked. Without a "how to tell it worked" signal, developers cannot distinguish between "it worked silently" and "it did nothing." This is a minor issue given the field is already flagged as unconfirmed.

**Recommended improvement:**
```
"UNCONFIRMED (secondary source only -- not in primary Anthropic docs as of March 2026). When true, may categorize the skill as a 'mode command' in a separate UI section of the /slash menu. To verify: invoke /skills or / and look for a distinct 'modes' grouping. Set to false (default) unless you have confirmed this feature in your Claude Code version."
```

---

### [SK-007] `metadata` field's recommended keys are listed but not explained

| Attribute | Value |
|-----------|-------|
| **Heuristic** | H10 (Help and Documentation) |
| **Severity** | 0 (Cosmetic) |
| **Location** | `properties.metadata.description` |
| **Field** | `metadata` |

**Current description:**
> "Agent Skills Standard field. Arbitrary key-value pairs (string-to-string map). Recommended keys: author, version, mcp-server, category, tags."

**Problem:** The recommended keys are listed but not explained. A developer unfamiliar with the Agent Skills open standard will not know what `mcp-server` means in this context (does it reference a server name, a server URL, a capability declaration?) or what format `version` should take (semver? date?). These are cosmetic issues because the field accepts arbitrary strings; no validation will fail.

**Recommended improvement:**
```
"Agent Skills Standard field (agentskills.io). Arbitrary string key-value pairs for skill distribution metadata. Recommended keys: author (your name/email), version (semver e.g. '1.0.0'), mcp-server (MCP server this skill requires), category (skill domain), tags (comma-separated topics). Example: {author: 'team@company.com', version: '1.2.0'}"
```

---

### [SK-008] `compatibility` field gives no example of what an environment requirement looks like

| Attribute | Value |
|-----------|-------|
| **Heuristic** | H10 (Help and Documentation) |
| **Severity** | 1 (Minor) |
| **Location** | `properties.compatibility.description` |
| **Field** | `compatibility` |

**Current description:**
> "Agent Skills Standard field. Environment requirements (max 500 chars)."

**Problem:** "Environment requirements" is entirely vague. There is no example of what this looks like for real requirements (operating system? Claude Code version? minimum model tier? required MCP servers?). The 500-character limit is documented, which is good. The lack of any example means this field will either be left empty or filled with inconsistent ad-hoc content across different skills.

**Recommended improvement:**
```
"Agent Skills Standard field (agentskills.io). Human-readable environment requirements for this skill (max 500 chars). Example: 'Requires Claude Code >= 1.2.0. Requires context7 MCP server. Only tested on macOS/Linux. Minimum model: sonnet.' Omit if skill has no special requirements."
```

---

## Cross-Schema Findings

### [CS-001] Both schemas use `additionalProperties: true` with no discoverability aid for unknown fields

| Attribute | Value |
|-----------|-------|
| **Heuristic** | H9 (Recognize, Diagnose, and Recover) |
| **Severity** | 2 (Major) |
| **Location** | Root `additionalProperties` in both schemas |
| **Field** | Schema root |

**Problem:** Both schemas set `additionalProperties: true`, which is correct -- Claude Code silently ignores unknown fields and breaking on them would be counterproductive. However, this means a developer who accidentally uses an agent-only field in a SKILL.md (e.g., writing `tools:` instead of `allowed-tools:`) will receive no validation error. The field will be silently accepted and have no effect. This is precisely the failure mode from the "Common Mistakes" list item 4: tools vs allowed-tools confusion.

There is no way to add a schema-level warning for this without breaking the `additionalProperties: true` contract. However, the `allowed-tools` description in the skill schema should proactively mention this by name as the field to use instead of `tools`.

**Recommended improvement:** Update `allowed-tools` description in the skill schema to include:
```
"NOTE: Use 'allowed-tools' (hyphenated) in SKILL.md, NOT 'tools'. Writing 'tools:' in a SKILL.md file will be silently ignored."
```

---

### [CS-002] `effort: max` constraint is documented but not schema-enforced

| Attribute | Value |
|-----------|-------|
| **Heuristic** | H5 (Error Prevention) |
| **Severity** | 2 (Major) |
| **Location** | `properties.effort` in both schemas |
| **Field** | `effort` |

**Problem:** Both schemas document that `effort: max` is Opus 4.6 only. This is a cross-field constraint: `effort: max` is only valid when `model: opus` (or a model alias resolving to Opus 4.6). JSON Schema Draft 2020-12 can express this as an `if/then` conditional: if `effort == max` then `model` must be in `["opus", "claude-opus-4-6", "claude-opus-4-6[1m]"]`. Currently this constraint exists only in the description text.

Schema enforcement would turn a silent misconfiguration (effort: max with a haiku model silently doing less) into a validation error. This is a significant DX improvement given that the failure mode is not an error but a silent capability degradation that is hard to notice.

**Recommended improvement:** Add a schema-level `if/then` conditional to both schemas:
```json
"if": {
  "properties": { "effort": { "const": "max" } },
  "required": ["effort"]
},
"then": {
  "properties": {
    "model": {
      "enum": ["opus", "claude-opus-4-6", "claude-opus-4-6[1m]"]
    }
  }
}
```
If the model is not set to Opus, the validator surfaces: "effort: max requires model to be one of: opus, claude-opus-4-6, claude-opus-4-6[1m]"

---

### [CS-003] `description` field omits the required minimum content for routing quality

| Attribute | Value |
|-----------|-------|
| **Heuristic** | H5 (Error Prevention) |
| **Severity** | 2 (Major) |
| **Location** | `properties.description` in both schemas |
| **Field** | `description` |

**Problem:** Both schemas enforce `minLength: 10`, which prevents empty strings. However, both also explain that `description` is the "primary routing signal" (agent) or that "Claude uses this to decide when to load automatically" (skill). A description of ten characters is technically valid but effectively useless for routing. A developer writing `description: "Does stuff"` passes schema validation but gets a non-functional routing signal.

There is no reasonable schema-level fix short of raising `minLength` (which is arbitrary) or adding a pattern (which is too prescriptive). The DX fix is to make the description field's own description more prescriptive about what constitutes a useful value.

**Agent schema - recommended improvement:**
```
"When Claude should delegate to this agent. MUST include: (1) what the agent does, (2) when to invoke it, (3) at least one trigger keyword. Include 'use proactively' to encourage automatic invocation. No XML angle brackets (<>). Bad example: 'Does research'. Good example: 'Research agent for literature surveys and landscape analysis. Use proactively when asked to research, survey, or investigate a topic.'"
```

**Skill schema - recommended improvement:**
```
"What this skill does and when to use it. Claude uses this for automatic invocation decisions. MUST include: WHAT the skill does, WHEN to use it, and trigger phrases that would cause Claude to load it. Third person, single-line string only (multiline YAML indicators >, |, >-, |- may be misparsed). Min 10 chars, max 1024 chars. No XML angle brackets. Example: 'Problem-solving skill for research, analysis, and root cause investigation. Use when asked to investigate, research, debug, or analyze.'"
```

---

### [CS-004] `model` field has inconsistent alias sets between agent and skill schemas

| Attribute | Value |
|-----------|-------|
| **Heuristic** | H5 (Error Prevention) |
| **Severity** | 2 (Major) |
| **Location** | `properties.model.description` in both schemas |
| **Field** | `model` |

**Problem:** The agent schema lists model aliases as: `sonnet, opus, haiku, inherit`. The skill schema lists them as: `sonnet, opus, haiku, default, inherit`. The skill schema includes `default` as a valid alias; the agent schema does not. If `default` is a valid alias, omitting it from the agent schema will cause a developer to get a confused error message ("default is not a valid enum") if they try to use it for an agent. If `default` is not valid for agents, the description in the agent schema should explicitly say so.

Additionally, the agent schema description does not mention the full ID `claude-haiku-4-5` while the skill schema does -- these should be identical lists.

**Recommended improvement:** Audit whether `default` is a valid agent model alias at runtime. If yes, add it to the agent schema model description. If no, add a note to the skill schema: "Note: 'default' is only valid in SKILL.md files, not agent definitions." Ensure the full model ID lists match exactly between both schemas.

---

## Common Mistake Analysis

Ten common developer mistakes evaluated against what error message or schema behavior they would encounter:

| # | Mistake | Schema Response | DX Quality | Finding |
|---|---------|-----------------|------------|---------|
| 1 | Wrong model value (e.g., "claude-3") | `model` is a free-form string with no enum. Validation passes silently. | POOR: No error. Developer gets runtime failure or silent degradation. | [CS-004] model aliases undocumented |
| 2 | Missing required field `name` or `description` | `required: ["name", "description"]` triggers a standard JSON Schema error: "Missing required property 'name'". | GOOD: Error is clear and field is named. |  |
| 3 | Wrong `mcpServers` format (pure object with wrong value types) | Agent schema accepts both array and object formats via `oneOf`. Very permissive. | ADEQUATE: Unlikely to fail unless the value type is wrong. |  |
| 4 | Using `tools:` in SKILL.md instead of `allowed-tools:` | `additionalProperties: true` means `tools:` in a skill file is silently accepted. | POOR: Silent failure. Developer loses tool configuration silently. | [CS-001] |
| 5 | `name` with uppercase or underscores (e.g., "PS_Researcher") | Pattern `^[a-z][a-z0-9]*(-[a-z0-9]+)*$` fails. Error: "String does not match pattern." Pattern is shown but not decoded. | ADEQUATE: Error fires, but the pattern is cryptic to interpret. | [AG-005] |
| 6 | `effort: max` with non-Opus model | No schema enforcement. Both pass validation. Silent runtime degradation. | POOR: No error. Developer has no feedback. | [CS-002] |
| 7 | Invalid `permissionMode` value (e.g., "always-allow") | Enum validation fires: "Value is not one of the allowed values: default, acceptEdits, dontAsk, bypassPermissions, plan". | GOOD: All valid options listed in error. |  |
| 8 | `context: fork` without `agent` field | `context` validates fine (enum with one value). `agent` is optional. No error, but subagent defaults to general-purpose silently. | ADEQUATE: Works by design, but developer may not get expected behavior. | [SK-002] |
| 9 | Empty `description` string ("") | `minLength: 10` fails: "String is too short (0 < 10)". | GOOD: Error fires. But threshold is too low to prevent useless descriptions. | [CS-003] |
| 10 | `disallowedTools:` in a SKILL.md file | `additionalProperties: true` accepts it silently. Has no effect in a skill file. | POOR: Silent failure. Developer's tool restriction is ignored. | [CS-001] |

**Summary of common mistake outcomes:**
- 3 mistakes fail silently with no diagnostic (items 1, 6, 10)
- 1 mistake partially fails with silent wrong behavior (item 4)
- 4 mistakes surface errors that range from adequate to good (items 2, 3, 5, 7, 9)
- 2 mistakes work but may not produce the expected behavior (items 8, 9 edge case)

---

## Technical Criteria Assessment

| Criterion | Status | Evidence |
|-----------|--------|---------|
| TC-1: Missing required field error identifies the field name and its purpose | PASS | `required: ["name", "description"]` produces standard JSON Schema error naming the field. Description text explains each field's purpose. |
| TC-2: Invalid enum value error lists all valid options | PASS (partial) | `permissionMode`, `effort`, `memory`, `isolation`, `context`, `shell` all use enum and will show all valid values. `model` is NOT an enum -- wrong model values pass silently. |
| TC-3: Pattern mismatch error shows the expected pattern with an example | FAIL | `name` uses `pattern` which produces "String does not match pattern ^[a-z][a-z0-9]*(-[a-z0-9]+)*$" -- the pattern is shown but no example value is provided in the error or the description to help decode it. |
| TC-4: Schema descriptions are under 200 chars and include one example value | FAIL | Multiple descriptions exceed 200 characters. The `hooks` description is approximately 430 characters. The `model` description in the agent schema is approximately 225 characters. Several fields have no example value: `maxTurns`, `disallowedTools`, `skills`. |

---

## Metrics Summary

| Metric | Value |
|--------|-------|
| Schemas Reviewed | 2 |
| Fields Reviewed | 34 (16 agent + 18 skill) |
| Critical Issues (Severity 4) | 0 |
| Severe Issues (Severity 3) | 1 (SK-001: allowed-tools semantics) |
| Major Issues (Severity 2) | 10 (AG-004, AG-008, SK-002, SK-003, SK-004, SK-005, CS-001, CS-002, CS-003, CS-004) |
| Minor Issues (Severity 1) | 6 (AG-001 reclassified, AG-002, AG-003, AG-005, AG-006, AG-007, SK-006, SK-008) |
| Cosmetic Issues (Severity 0) | 1 (SK-007) |
| Positive Observations | 7 (in Steelman section) |
| TC-1 | PASS |
| TC-2 | PASS (partial -- model field is not enum-validated) |
| TC-3 | FAIL |
| TC-4 | FAIL |
| **Overall DX Assessment** | **NEEDS_WORK** |

---

## Recommendations by Priority

Ordered by severity, then impact on common developer mistakes:

### Priority 1: Fix the silent failure cases (Severity 3-4)

1. **[SK-001]** Rewrite `allowed-tools` description to lead with the warning that it does NOT restrict tools. Move the security-relevant caveat to the first sentence.

2. **[CS-001]** Add an explicit note to `allowed-tools` (skill schema): "Use 'allowed-tools' in SKILL.md, NOT 'tools'. Writing 'tools:' in a SKILL.md file is silently ignored."

3. **[CS-002]** Add an `if/then` conditional to both schemas to enforce that `effort: max` requires an Opus model. This converts a silent degradation into a schema validation error.

### Priority 2: Fix major description gaps (Severity 2)

4. **[CS-004]** Audit the `default` model alias discrepancy and align both schemas to the same alias list.

5. **[CS-003]** Strengthen both `description` field descriptions to include a concrete good/bad example, making it clear what constitutes a useful routing description.

6. **[AG-004]** Rewrite `hooks` description with a minimal structural example showing the event-name to command object pattern.

7. **[AG-008]** Add an explicit warning to `initialPrompt` that it is silently ignored for subagent invocations, and redirect developers to use the Task tool prompt parameter.

8. **[SK-002]** Add a cross-reference from `context: fork` description to the `agent` field.

9. **[SK-003]** Clarify the custom agent naming convention (base filename without `.md`).

10. **[SK-004]** Add glob pattern examples to `paths` field with a note about what "working with files" means.

11. **[SK-005]** Document what happens when `shell: powershell` is set without the env var (silent fallback vs runtime error).

### Priority 3: Improve discoverability (Severity 1)

12. **[AG-001]** Add tool name examples and casing guidance to `disallowedTools`.

13. **[AG-002]** Add practical guidance on maxTurns values and what happens at the limit.

14. **[AG-003]** Add a skill name format example to `skills` (directory name, not slash-command).

15. **[AG-005]** Clarify that `name` must start with a lowercase letter, not a digit.

16. **[SK-008]** Add a concrete example of environment requirements to `compatibility`.

### Priority 4: Cosmetic improvements (Severity 0)

17. **[SK-007]** Explain the `metadata` recommended key semantics briefly.

18. **[AG-006]** Clarify whether undocumented `color` values are silently ignored or cause errors.

19. **[SK-006]** Add a "how to verify it worked" note to the `mode` field description.

---

*Evaluation: ps-reviewer*
*Schemas: docs/schemas/claude-code-frontmatter-v1.schema.json, docs/schemas/claude-code-skill-frontmatter-v1.schema.json*
*Date: 2026-03-26*
*EN-002: Developer Experience Review*
