# Anthropic Claude Code SKILL.md Schema Research

> **PS ID:** PROJ-024
> **Entry ID:** e-001
> **Topic:** Anthropic SKILL.md YAML Frontmatter Definition Schema
> **Researcher:** ps-researcher
> **Date:** 2026-03-26
> **Confidence:** HIGH (0.92) -- Primary sources are Anthropic's own documentation

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Non-technical overview of findings |
| [L1: Technical Analysis](#l1-technical-analysis) | Detailed field-by-field reference |
| [L2: Architectural Implications](#l2-architectural-implications) | Strategic impact on Jerry schema |
| [Research Questions](#research-questions) | Numbered answers to all 12 questions |
| [Methodology](#methodology) | Sources consulted and credibility assessment |
| [References](#references) | Complete citation list |

---

## L0: Executive Summary

There are **two distinct schemas** at play: the open **Agent Skills standard** (agentskills.io) and **Claude Code's proprietary extensions**. The Agent Skills standard defines only 6 fields (name, description, license, compatibility, metadata, allowed-tools). Claude Code extends this with 7 additional proprietary fields that control execution context, model selection, invocation behavior, and lifecycle hooks.

Our existing Jerry schema at `docs/schemas/claude-code-skill-frontmatter-v1.schema.json` covers 9 fields. This research discovered **4 fields we are missing** from the official Claude Code documentation: `effort`, `paths`, `shell`, and `mode`. Additionally, several fields we already track have **constraint details we had not captured** (such as the `name` field prohibiting consecutive hyphens and reserved words "claude"/"anthropic").

The practical impact: our schema needs updating to match the March 2026 official documentation. The fields we were missing are all optional, so existing SKILL.md files remain valid. However, `effort` and `paths` are particularly valuable -- `effort` controls reasoning depth, and `paths` enables file-pattern-scoped skill activation.

No official JSON Schema is published by Anthropic. The closest is the `skills-ref` validation library at github.com/agentskills/agentskills, which validates against the Agent Skills standard (not Claude Code extensions).

---

## L1: Technical Analysis

### Two-Layer Schema Architecture

Claude Code skills follow the Agent Skills open standard (agentskills.io) but extend it with proprietary fields. Understanding which fields belong to which layer matters for portability.

| Layer | Fields | Portability |
|-------|--------|-------------|
| **Agent Skills Standard** | `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools` | Cross-tool (VS Code Copilot, OpenCode, Spring AI, etc.) |
| **Claude Code Extensions** | `disable-model-invocation`, `user-invocable`, `model`, `effort`, `context`, `agent`, `hooks`, `paths`, `shell`, `mode` | Claude Code only |
| **Jerry Extensions** | `version`, `activation-keywords` | Jerry framework only |

### Complete Field Reference (Official as of March 2026)

#### 1. `name` (Agent Skills Standard + Claude Code)

| Property | Value |
|----------|-------|
| **Type** | string |
| **Required** | No (recommended; uses directory name if omitted) |
| **Max Length** | 64 characters |
| **Pattern** | `^[a-z0-9]([a-z0-9-]*[a-z0-9])?$` with additional constraints |
| **Constraints** | Lowercase letters, numbers, hyphens only. Must not start or end with hyphen. Must not contain consecutive hyphens (`--`). Must match parent directory name. Must not contain reserved words "claude" or "anthropic". No XML tags (`<>`). |
| **Default** | Directory name |

**Source:** [Extend Claude with skills](https://code.claude.com/docs/en/skills), [agentskills.io specification](https://agentskills.io/specification), [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

**Delta from our schema:** Our schema has `"pattern": "^[a-z0-9]([a-z0-9-]*[a-z0-9])?$"` which correctly enforces most constraints but does not enforce: (a) no consecutive hyphens, (b) reserved word prohibition. These require either a more complex regex or custom validation.

#### 2. `description` (Agent Skills Standard + Claude Code)

| Property | Value |
|----------|-------|
| **Type** | string |
| **Required** | Recommended (not strictly required; falls back to first paragraph of markdown) |
| **Min Length** | 1 (non-empty) |
| **Max Length** | 1024 characters |
| **Constraints** | Non-empty. No XML tags (`<>`). Should describe WHAT the skill does AND WHEN to use it. Should be written in third person. |
| **Default** | First paragraph of markdown content |

**Source:** [Extend Claude with skills](https://code.claude.com/docs/en/skills), [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

**Delta from our schema:** Our schema has `minLength: 10` which is stricter than the official minimum of 1. The official docs say "non-empty" but recommend substantive descriptions. Our 10-character minimum is a reasonable Jerry-specific tightening.

#### 3. `argument-hint` (Claude Code Extension)

| Property | Value |
|----------|-------|
| **Type** | string |
| **Required** | No |
| **Constraints** | Free-form string. Shown during autocomplete. |
| **Default** | None |

**Source:** [Extend Claude with skills](https://code.claude.com/docs/en/skills)

**Delta from our schema:** Correctly captured. No changes needed.

#### 4. `disable-model-invocation` (Claude Code Extension)

| Property | Value |
|----------|-------|
| **Type** | boolean |
| **Required** | No |
| **Default** | `false` |
| **Behavior** | When `true`: (a) skill description is NOT loaded into context, (b) Claude cannot invoke it automatically, (c) only user can invoke via `/name`. When `false`: description is always in context and Claude can invoke it. |

**Source:** [Extend Claude with skills](https://code.claude.com/docs/en/skills)

**Delta from our schema:** Correctly captured. No changes needed.

#### 5. `user-invocable` (Claude Code Extension)

| Property | Value |
|----------|-------|
| **Type** | boolean |
| **Required** | No |
| **Default** | `true` |
| **Behavior** | When `false`: (a) hidden from `/` menu, (b) only Claude can invoke it automatically. Note: this only controls menu visibility, NOT Skill tool access. To block programmatic invocation, use `disable-model-invocation: true`. |

**Source:** [Extend Claude with skills](https://code.claude.com/docs/en/skills)

**Delta from our schema:** Correctly captured. No changes needed.

#### 6. `allowed-tools` (Agent Skills Standard + Claude Code)

| Property | Value |
|----------|-------|
| **Type** | string (space-delimited per Agent Skills, comma-separated per Claude Code) OR array of strings |
| **Required** | No |
| **Default** | All tools available |
| **Constraints** | Tool names. Supports permission syntax patterns (e.g., `Bash(git:*)`, `Read`). Agent Skills standard says "space-delimited" and marks as experimental. Claude Code documentation shows comma-separated. |
| **Behavior** | Tools Claude can use without asking permission when this skill is active. Does NOT restrict tools -- it grants blanket approval for listed tools. |

**Source:** [Extend Claude with skills](https://code.claude.com/docs/en/skills), [agentskills.io specification](https://agentskills.io/specification)

**Delta from our schema:** Our schema correctly accepts both string and array. The Agent Skills standard uses space-delimited; Claude Code shows comma-separated. Both appear to work. The permission syntax pattern support (`Bash(git:*)`) is not documented in our schema.

#### 7. `model` (Claude Code Extension)

| Property | Value |
|----------|-------|
| **Type** | string |
| **Required** | No |
| **Default** | Inherits from session |
| **Accepted values** | Model aliases: `sonnet`, `opus`, `haiku`, `default`, `inherit`. Full model IDs: `claude-opus-4-6`, `claude-sonnet-4`, `claude-haiku-4-5`, etc. Extended context: `opus[1m]`, `sonnet[1m]`. Special: `opusplan`. |

**Source:** [Extend Claude with skills](https://code.claude.com/docs/en/skills), [Model configuration](https://code.claude.com/docs/en/model-config)

**Delta from our schema:** Correctly captured, but we could document the accepted aliases and full ID patterns more explicitly.

#### 8. `effort` (Claude Code Extension) -- NEW, MISSING FROM OUR SCHEMA

| Property | Value |
|----------|-------|
| **Type** | string |
| **Required** | No |
| **Enum** | `low`, `medium`, `high`, `max` |
| **Default** | Inherits from session (which defaults to `medium` for Opus 4.6 and Sonnet 4.6) |
| **Constraints** | `max` is Opus 4.6 only. Overrides session effort level when skill is active. Environment variable `CLAUDE_CODE_EFFORT_LEVEL` takes precedence over frontmatter. |
| **Behavior** | Controls adaptive reasoning depth. Lower effort is faster and cheaper. Higher effort provides deeper reasoning. Medium is recommended for most tasks. |

**Source:** [Extend Claude with skills](https://code.claude.com/docs/en/skills), [Model configuration - effort levels](https://code.claude.com/docs/en/model-config)

**Delta from our schema:** MISSING. Must be added.

#### 9. `context` (Claude Code Extension)

| Property | Value |
|----------|-------|
| **Type** | string |
| **Required** | No |
| **Enum** | `fork` (only known value) |
| **Behavior** | When set to `fork`: skill runs in a forked subagent context, isolated from the main conversation. The skill content becomes the prompt that drives the subagent. The subagent does NOT have access to conversation history. CLAUDE.md is still loaded. |

**Source:** [Extend Claude with skills](https://code.claude.com/docs/en/skills), [Create custom subagents](https://code.claude.com/docs/en/sub-agents)

**Known issue:** GitHub Issue #17283 (CLOSED/COMPLETED, Jan 2026) reported that `context: fork` and `agent:` were ignored when skills were invoked via the Skill tool. The issue is marked as resolved.

**Delta from our schema:** Correctly captured as `enum: ["fork"]`. No changes needed.

#### 10. `agent` (Claude Code Extension)

| Property | Value |
|----------|-------|
| **Type** | string |
| **Required** | No |
| **Default** | `general-purpose` (when `context: fork` is set) |
| **Accepted values** | Built-in agents: `Explore`, `Plan`, `general-purpose`. Custom agents: any name matching a `.claude/agents/*.md` file. |
| **Behavior** | Only meaningful when `context: fork` is set. Determines which subagent type executes the skill. The agent field specifies model, tools, and permissions the subagent uses. |

**Source:** [Extend Claude with skills](https://code.claude.com/docs/en/skills), [Create custom subagents](https://code.claude.com/docs/en/sub-agents)

**Delta from our schema:** Correctly captured. Could add documentation about `Explore` (Haiku model, read-only tools), `Plan` (inherits model, read-only tools), and `general-purpose` (inherits model, all tools).

#### 11. `hooks` (Claude Code Extension)

| Property | Value |
|----------|-------|
| **Type** | object |
| **Required** | No |
| **Behavior** | Hooks scoped to this skill's lifecycle. Only run when the skill is active. Automatically cleaned up when the skill finishes. Merged with global hooks. Supports ALL hook event types. |
| **Hook events** | `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PermissionRequest`, `PostToolUse`, `PostToolUseFailure`, `Notification`, `SubagentStart`, `SubagentStop`, `TaskCreated`, `TaskCompleted`, `Stop`, `StopFailure`, `TeammateIdle`, `InstructionsLoaded`, `ConfigChange`, `CwdChanged`, `FileChanged`, `WorktreeCreate`, `WorktreeRemove`, `PreCompact`, `PostCompact`, `Elicitation`, `ElicitationResult` |
| **Hook handler types** | `command`, `http`, `prompt`, `agent` |
| **Special field** | `once: true` -- runs hook only once per session then removes it. Skills-only feature, not available for agents. |

**Source:** [Extend Claude with skills](https://code.claude.com/docs/en/skills), [Hooks documentation](https://code.claude.com/docs/en/hooks)

**Delta from our schema:** Our schema has `"additionalProperties": true` which is correct but very permissive. The hooks structure is complex and deeply nested. Detailed schema for hooks would require a separate schema definition.

#### 12. `paths` (Claude Code Extension) -- NEW, MISSING FROM OUR SCHEMA

| Property | Value |
|----------|-------|
| **Type** | string (comma-separated) OR array of strings |
| **Required** | No |
| **Default** | None (skill activates regardless of file context) |
| **Constraints** | Glob patterns. Same format as path-specific rules. |
| **Behavior** | When set, Claude loads the skill automatically only when working with files matching the patterns. Limits when the skill is activated based on file paths being edited/viewed. |

**Source:** [Extend Claude with skills](https://code.claude.com/docs/en/skills)

**Delta from our schema:** MISSING. Must be added.

#### 13. `shell` (Claude Code Extension) -- NEW, MISSING FROM OUR SCHEMA

| Property | Value |
|----------|-------|
| **Type** | string |
| **Required** | No |
| **Enum** | `bash`, `powershell` |
| **Default** | `bash` |
| **Constraints** | Setting `powershell` requires `CLAUDE_CODE_USE_POWERSHELL_TOOL=1` environment variable. |
| **Behavior** | Controls the shell used for `!command` blocks (inline shell commands) in the skill content. |

**Source:** [Extend Claude with skills](https://code.claude.com/docs/en/skills)

**Delta from our schema:** MISSING. Must be added.

#### 14. `mode` (Claude Code Extension) -- NEW, MISSING FROM OUR SCHEMA

| Property | Value |
|----------|-------|
| **Type** | boolean |
| **Required** | No |
| **Default** | `false` |
| **Behavior** | When `true`, categorizes the skill as a "mode command" that modifies Claude's behavior. The skill appears in a special "Mode Commands" section at the top of the skills list, separate from regular utility skills. |

**Source:** [Claude Agent Skills: A First Principles Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/) -- secondary source. Not directly confirmed in code.claude.com primary documentation frontmatter table as of March 2026.

**Confidence:** MEDIUM. The `mode` field appears in a well-researched deep dive blog post but is NOT listed in the official [frontmatter reference table](https://code.claude.com/docs/en/skills). It may be an undocumented internal field or may have been removed. Treat as unconfirmed until verified in Claude Code source or official docs.

**Delta from our schema:** MISSING. Add with note about unconfirmed status.

#### 15. `license` (Agent Skills Standard)

| Property | Value |
|----------|-------|
| **Type** | string |
| **Required** | No |
| **Constraints** | License name or reference to bundled license file. Keep short. |

**Source:** [agentskills.io specification](https://agentskills.io/specification)

**Delta from our schema:** MISSING from our schema but part of the open standard. Not a Claude Code extension -- relevant for skill distribution.

#### 16. `compatibility` (Agent Skills Standard)

| Property | Value |
|----------|-------|
| **Type** | string |
| **Required** | No |
| **Max Length** | 500 characters |
| **Constraints** | Environment requirements. |

**Source:** [agentskills.io specification](https://agentskills.io/specification)

**Delta from our schema:** MISSING from our schema but part of the open standard.

#### 17. `metadata` (Agent Skills Standard)

| Property | Value |
|----------|-------|
| **Type** | object (string-to-string map) |
| **Required** | No |
| **Constraints** | Arbitrary key-value pairs. Recommended: author, version, mcp-server, category, tags. |

**Source:** [agentskills.io specification](https://agentskills.io/specification)

**Delta from our schema:** MISSING from our schema but part of the open standard. Note: Jerry uses `version` and `activation-keywords` as top-level frontmatter fields. The Agent Skills standard would place `version` under `metadata.version`.

### String Substitution Variables

Skills support dynamic string substitution in their markdown body content:

| Variable | Description |
|----------|-------------|
| `$ARGUMENTS` | All arguments passed when invoking the skill |
| `$ARGUMENTS[N]` | Specific argument by 0-based index |
| `$N` | Shorthand for `$ARGUMENTS[N]` |
| `${CLAUDE_SESSION_ID}` | Current session ID |
| `${CLAUDE_SKILL_DIR}` | Directory containing the SKILL.md file |

**Source:** [Extend Claude with skills](https://code.claude.com/docs/en/skills)

These are body-level features, not frontmatter fields, but are relevant to skill authoring.

### Inline Shell Commands

The `` !`<command>` `` syntax runs shell commands before skill content is sent to Claude. The command output replaces the placeholder. This is preprocessing, not something Claude executes.

**Source:** [Extend Claude with skills](https://code.claude.com/docs/en/skills)

---

## Research Questions -- Answers

### Q1: What are ALL official YAML frontmatter fields for SKILL.md files?

**Answer:** There are **13 confirmed official fields** in the Claude Code frontmatter reference table (March 2026), plus 3 Agent Skills standard fields not in that table but recognized:

**Claude Code Official Frontmatter Table (13 fields):**
1. `name` -- Display name / slash command
2. `description` -- What and when
3. `argument-hint` -- Autocomplete hint
4. `disable-model-invocation` -- Prevent auto-loading
5. `user-invocable` -- Hide from / menu
6. `allowed-tools` -- Tool permissions
7. `model` -- Model selection
8. `effort` -- Reasoning depth
9. `context` -- Fork to subagent
10. `agent` -- Subagent type
11. `hooks` -- Lifecycle hooks
12. `paths` -- File pattern activation
13. `shell` -- Shell for inline commands

**Agent Skills Standard (additional):**
14. `license` -- Skill license
15. `compatibility` -- Environment requirements
16. `metadata` -- Arbitrary key-value pairs

**Unconfirmed:**
17. `mode` -- Mode command categorization (secondary source only)

**Jerry-specific (not recognized by Claude Code):**
- `version` -- Semantic version
- `activation-keywords` -- Routing keywords

### Q2: What are the exact type constraints for each field?

**Answer:** See the [Complete Field Reference](#complete-field-reference-official-as-of-march-2026) section above. Key constraints:
- `name`: max 64 chars, `[a-z0-9-]`, no consecutive hyphens, no start/end hyphen, no "claude"/"anthropic"
- `description`: max 1024 chars, non-empty, no XML tags
- `effort`: enum `[low, medium, high, max]`
- `context`: enum `[fork]`
- `shell`: enum `[bash, powershell]`
- `compatibility`: max 500 chars
- `model`: string (aliases or full model IDs)

### Q3: Are there any NEW fields added recently (2025-2026) that we might be missing?

**Answer:** Yes. Four fields are missing from our schema:
1. **`effort`** -- Reasoning depth control (low/medium/high/max). Added with Opus 4.6 and adaptive reasoning.
2. **`paths`** -- Glob patterns for file-scoped activation.
3. **`shell`** -- Shell selection for inline commands (bash/powershell).
4. **`mode`** -- Mode command boolean (unconfirmed in primary docs).

Additionally, three Agent Skills standard fields are missing:
5. **`license`**
6. **`compatibility`**
7. **`metadata`**

### Q4: What is the official skill discovery mechanism?

**Answer:** Claude Code discovers skills through **directory scanning** at multiple locations:

1. **Enterprise** -- Managed settings path
2. **Personal** -- `~/.claude/skills/<skill-name>/SKILL.md`
3. **Project** -- `.claude/skills/<skill-name>/SKILL.md`
4. **Plugin** -- `<plugin>/skills/<skill-name>/SKILL.md`
5. **Nested** -- `.claude/skills/` directories in subdirectories (monorepo support)
6. **Additional directories** -- `--add-dir` flag directories

Priority: enterprise > personal > project. Plugin skills use `plugin-name:skill-name` namespace (no conflicts). Skills share the same name: higher-priority location wins.

**Character budget:** Skill descriptions are loaded into context with a budget of 2% of the context window, with a fallback of 16,000 characters. The `SLASH_COMMAND_TOOL_CHAR_BUDGET` env var overrides this.

**Source:** [Extend Claude with skills](https://code.claude.com/docs/en/skills)

### Q5: How does skill loading work?

**Answer:** Progressive disclosure with three tiers:

| Tier | What | When | Token Impact |
|------|------|------|-------------|
| **Metadata** | `name` + `description` (~100 tokens each) | Always at startup (unless `disable-model-invocation: true`) | Minimal |
| **SKILL.md body** | Full markdown content | When skill is invoked or deemed relevant | Moderate (keep under 500 lines) |
| **Supporting files** | `references/`, `scripts/`, `assets/` | On demand via Read tool | Variable |

When `disable-model-invocation: true`, the description is NOT loaded into context at all. When `user-invocable: false`, the description IS loaded (Claude needs it for auto-invocation decisions).

Scripts in `scripts/` can be executed via Bash without loading their contents into context -- only the script output consumes tokens.

**Source:** [Extend Claude with skills](https://code.claude.com/docs/en/skills), [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

### Q6: What is the `context: fork` behavior exactly? How does it interact with `agent`?

**Answer:**

`context: fork` creates an **isolated subagent context** to run the skill. The skill content becomes the subagent's task prompt. Key behaviors:

1. A new isolated context window is created.
2. The subagent receives the skill content as its prompt.
3. The subagent does NOT have access to the main conversation history.
4. CLAUDE.md files ARE loaded in the subagent context.
5. The `agent` field determines the subagent type (model, tools, permissions).
6. Results are summarized and returned to the main conversation.

If `agent` is omitted when `context: fork` is set, it defaults to `general-purpose`.

**Comparison table:**

| Approach | System prompt | Task | Also loads |
|----------|--------------|------|------------|
| Skill with `context: fork` | From agent type (Explore, Plan, etc.) | SKILL.md content | CLAUDE.md |
| Subagent with `skills` field | Subagent's markdown body | Claude's delegation message | Preloaded skills + CLAUDE.md |

**Warning:** `context: fork` only makes sense for skills with explicit task instructions. If the skill contains only guidelines without a task, the subagent receives guidelines but no actionable prompt.

**Historical issue:** GitHub Issue #17283 (closed Jan 2026) reported `context: fork` and `agent` being ignored when invoked via the Skill tool. This was fixed.

**Source:** [Extend Claude with skills](https://code.claude.com/docs/en/skills), [Create custom subagents](https://code.claude.com/docs/en/sub-agents), [GitHub Issue #17283](https://github.com/anthropics/claude-code/issues/17283)

### Q7: Are there any published JSON schemas from Anthropic for skill definitions?

**Answer:** **No official JSON Schema exists** for SKILL.md frontmatter.

The closest resources are:
1. **`skills-ref` validation library** at `github.com/agentskills/agentskills` -- validates against the Agent Skills standard only (6 fields), not Claude Code extensions.
2. **Discovery schema** at `https://schemas.agentskills.io/discovery/0.2.0/schema.json` -- for skill discovery/distribution, not frontmatter validation.

Our Jerry schema at `docs/schemas/claude-code-skill-frontmatter-v1.schema.json` appears to be the most comprehensive JSON Schema for Claude Code skill frontmatter that exists.

**Source:** [agentskills.io specification](https://agentskills.io/specification), [anthropics/skills repository](https://github.com/anthropics/skills)

### Q8: What is the skill directory convention?

**Answer:**

```
skill-name/
  SKILL.md           # Required -- entrypoint
  scripts/           # Optional -- executable code
  references/        # Optional -- documentation
  assets/            # Optional -- templates, resources
  examples/          # Optional -- example outputs
  evals/             # Optional -- evaluation test cases
```

Key conventions:
- Skill directory name MUST match the `name` field in frontmatter (if `name` is specified).
- `SKILL.md` is the required entrypoint (case-sensitive).
- Supporting files are referenced from SKILL.md and loaded on demand.
- Keep references one level deep from SKILL.md (avoid deeply nested references).
- For reference files over 100 lines, include a table of contents.

**Source:** [Extend Claude with skills](https://code.claude.com/docs/en/skills), [agentskills.io specification](https://agentskills.io/specification)

### Q9: How do skill permissions work?

**Answer:**

`allowed-tools` grants Claude permission to use listed tools **without asking** when the skill is active. It does NOT restrict tools -- it is an allowlist for automatic approval.

Permission hierarchy:
1. Global permission settings (`settings.json` permissions) still govern baseline behavior.
2. `allowed-tools` in the skill grants additional auto-approvals on top of global settings.
3. The `Skill(name)` and `Skill(name *)` permission patterns in settings control which skills Claude can invoke.

**Three ways to control skill access:**
1. **Deny the Skill tool entirely** -- add `Skill` to deny rules
2. **Allow/deny specific skills** -- `Skill(commit)`, `Skill(deploy *)`
3. **Hide individual skills** -- `disable-model-invocation: true`

**Source:** [Extend Claude with skills](https://code.claude.com/docs/en/skills)

### Q10: What is the interaction between skills and hooks?

**Answer:**

Skills support the **full hook system**:
- All hook event types are supported in skill frontmatter.
- Skill hooks are **scoped to the skill's lifecycle** -- they only run when the skill is active.
- Hooks are automatically cleaned up when the skill finishes.
- Skill hooks are **merged** with global hooks (from settings, plugins, etc.).
- Identical handlers are deduplicated.
- Skills support a special `once: true` field on hooks that is NOT available for subagents.

The `Stop` hook in skill frontmatter is automatically converted to `SubagentStop` at runtime.

**Source:** [Hooks documentation](https://code.claude.com/docs/en/hooks), [Create custom subagents](https://code.claude.com/docs/en/sub-agents)

### Q11: What fields does the /skills or skill listing display?

**Answer:**

The skill listing displays:
- **name** -- as the `/slash-command`
- **description** -- the purpose text
- Skills with `mode: true` appear in a separate "Mode Commands" section at the top (unconfirmed in primary docs).
- Skills with `disable-model-invocation: true` are excluded from the listing shown to Claude.
- The `/context` command shows warnings about excluded skills when the character budget is exceeded.

**Source:** [Extend Claude with skills](https://code.claude.com/docs/en/skills)

### Q12: How does `disable-model-invocation` vs `user-invocable` work in practice?

**Answer:**

| Configuration | User can invoke | Claude can invoke | Description in context |
|---|---|---|---|
| (default) | Yes | Yes | Yes -- always loaded |
| `disable-model-invocation: true` | Yes | No | No -- excluded entirely |
| `user-invocable: false` | No | Yes | Yes -- always loaded |
| Both `true`/`false` | No | No | Contradictory; likely excluded |

Key distinctions:
- `disable-model-invocation: true` is stronger -- it removes the skill from Claude's context entirely, preventing both automatic invocation and Skill tool access.
- `user-invocable: false` only hides from the `/` menu. Claude can still invoke it via the Skill tool.
- For programmatic blocking, use `disable-model-invocation: true`, NOT `user-invocable: false`.

**Source:** [Extend Claude with skills](https://code.claude.com/docs/en/skills)

---

## L2: Architectural Implications

### Schema Update Strategy

Our current schema needs the following changes:

| Change | Priority | Impact |
|--------|----------|--------|
| Add `effort` field (enum: low/medium/high/max) | HIGH | Enables reasoning depth control per skill |
| Add `paths` field (string or array of glob patterns) | HIGH | Enables file-scoped skill activation |
| Add `shell` field (enum: bash/powershell) | LOW | Windows PowerShell support |
| Add `mode` field (boolean) | LOW | Mode command categorization (unconfirmed) |
| Add `license` field (string) | LOW | Agent Skills standard compliance |
| Add `compatibility` field (string, max 500) | LOW | Agent Skills standard compliance |
| Add `metadata` field (object, string-to-string) | MEDIUM | Agent Skills standard compliance; subsumes `version` |
| Tighten `name` pattern (no consecutive hyphens, no reserved words) | MEDIUM | Prevents Claude Code rejection |
| Document `allowed-tools` permission syntax | LOW | Permission pattern support |

### Jerry-Specific Fields Decision

Our `version` and `activation-keywords` fields are Jerry extensions that Claude Code silently ignores. This is by design -- Claude Code's `additionalProperties` handling does not reject unknown fields. Two strategic options:

**Option A (Current approach):** Keep Jerry fields as top-level frontmatter. They are silently ignored by Claude Code. Jerry validates them separately.

**Option B (Standards-aligned):** Move Jerry fields under `metadata`:
```yaml
metadata:
  version: "2.2.0"
  activation-keywords: [research, analyze, investigate]
```
This aligns with the Agent Skills standard. However, it changes every existing SKILL.md file and gains no functional benefit since Claude Code ignores both approaches equally.

**Recommendation:** Keep Option A. The migration cost outweighs the standards-alignment benefit. Document the fields as "Jerry extensions" in the schema.

### Portability Considerations

The Agent Skills standard is now adopted by multiple tools (VS Code Copilot, OpenCode, Spring AI). If Jerry skills ever need to be portable:
- The 6 Agent Skills standard fields would be recognized.
- Claude Code extension fields would be ignored by other tools.
- Jerry extension fields would be ignored by all tools.

This three-layer model (standard + Claude Code + Jerry) provides clean separation.

### `effort` Field Strategic Value

The `effort` field is architecturally significant for Jerry. Currently, Jerry's `agent-development-standards.md` defines `ET-M-001` (reasoning effort by criticality: C1=default, C2=medium, C3=high, C4=max). This maps directly to the `effort` frontmatter field. Adding `effort` to skill frontmatter means Jerry can enforce reasoning depth at the skill level, not just the agent level.

### `paths` Field Strategic Value

The `paths` field enables Jerry skills to activate based on file context. This could replace or supplement `activation-keywords` for file-type-specific skills. For example, a Python-specific skill could use `paths: ["*.py", "pyproject.toml"]` to activate only when working with Python files.

### Schema Versioning

Our schema should be updated to v1.1.0 (minor version bump) since these are additive changes. No existing SKILL.md files will become invalid -- all new fields are optional.

---

## Methodology

### Sources Consulted

| Source | Type | Credibility | Key Findings |
|--------|------|-------------|-------------|
| [code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills) | Primary (official docs) | HIGH | Complete frontmatter reference table with 13 fields |
| [platform.claude.com/docs/.../best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | Primary (official docs) | HIGH | Field constraints, naming rules, progressive disclosure |
| [agentskills.io/specification](https://agentskills.io/specification) | Primary (standard spec) | HIGH | Agent Skills standard: 6 base fields |
| [code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents) | Primary (official docs) | HIGH | context: fork behavior, agent field, subagent config |
| [code.claude.com/docs/en/hooks](https://code.claude.com/docs/en/hooks) | Primary (official docs) | HIGH | Hooks in skills, once field, lifecycle |
| [code.claude.com/docs/en/model-config](https://code.claude.com/docs/en/model-config) | Primary (official docs) | HIGH | Effort levels, model aliases |
| [github.com/anthropics/skills](https://github.com/anthropics/skills) | Primary (official repo) | HIGH | Skill-creator reference implementation |
| [github.com/anthropics/claude-code/issues/17283](https://github.com/anthropics/claude-code/issues/17283) | Primary (issue tracker) | HIGH | context: fork bug status (resolved) |
| [leehanchung.github.io](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/) | Secondary (analysis blog) | MEDIUM | `mode` field documentation |
| [Anthropic Skill Development Guide PDF](docs/knowledge/anthropic-skill-development-guide.pdf) | Primary (official guide) | HIGH | Agent Skills standard fields, naming constraints |

### Search Methodology

1. Fetched the official Claude Code skills documentation page in full.
2. Fetched the Claude API best practices documentation for skills.
3. Fetched the Agent Skills specification from agentskills.io.
4. Fetched the Claude Code subagent documentation for context: fork behavior.
5. Fetched the Claude Code hooks documentation for hooks-in-skills behavior.
6. Fetched the Claude Code model configuration for effort level details.
7. Searched for each new field (effort, paths, shell, mode, initialPrompt) individually.
8. Cross-referenced our existing schema against all findings.
9. Verified GitHub issues for context: fork resolution status.
10. Checked the Anthropic skills repository for reference implementations.

### What Was Not Found

1. **No official JSON Schema** from Anthropic for SKILL.md frontmatter.
2. **`mode` field** not confirmed in primary documentation frontmatter table -- only in a secondary analysis blog.
3. **`initialPrompt`** is a subagent-only field, NOT a skill field. It was considered but does not apply.
4. No documentation on field validation error messages or behavior when invalid values are provided.
5. No documentation on the internal parsing priority when both `tools` and `disallowedTools` exist in skills (this is only documented for subagents).

---

## References

1. [Extend Claude with skills - Claude Code Docs](https://code.claude.com/docs/en/skills) -- Key insight: Complete 13-field frontmatter reference table with effort, paths, and shell fields. Primary authority for Claude Code skill schema.

2. [Skill authoring best practices - Claude API Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) -- Key insight: Name/description constraint details, progressive disclosure patterns, anti-patterns.

3. [Agent Skills Specification - agentskills.io](https://agentskills.io/specification) -- Key insight: The 6-field open standard (name, description, license, compatibility, metadata, allowed-tools). Claude Code extends this with proprietary fields.

4. [Create custom subagents - Claude Code Docs](https://code.claude.com/docs/en/sub-agents) -- Key insight: context: fork behavior, agent field options, subagent frontmatter (16 fields), skills-in-subagents vs subagents-in-skills relationship.

5. [Hooks documentation - Claude Code Docs](https://code.claude.com/docs/en/hooks) -- Key insight: All hook events supported in skills, `once: true` is skills-only feature, Stop hooks auto-converted to SubagentStop.

6. [Model configuration - Claude Code Docs](https://code.claude.com/docs/en/model-config) -- Key insight: Effort levels (low/medium/high/max), model aliases, frontmatter effort overrides session level.

7. [GitHub - anthropics/skills](https://github.com/anthropics/skills) -- Key insight: Skill-creator reference implementation, spec redirects to agentskills.io.

8. [GitHub Issue #17283 - context: fork feature request](https://github.com/anthropics/claude-code/issues/17283) -- Key insight: context: fork bug was reported Jan 2026 and marked as resolved/completed.

9. [Claude Agent Skills: A First Principles Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/) -- Key insight: `mode` field documentation (unconfirmed in primary sources).

10. [Anthropic "Complete Guide to Building Skills for Claude" PDF](docs/knowledge/anthropic-skill-development-guide.pdf) -- Key insight: January 2026 guide; covers Agent Skills standard fields. Does not cover Claude Code proprietary extensions.

11. [Complete guide to building Skills for Claude (Gist conversion)](https://gist.github.com/joyrexus/ff71917b4fc0a2cbc84974212da34a4a) -- Key insight: Confirms standard fields; no Claude Code extensions beyond standard documented here.

---

## Appendix: Schema Delta Summary

### Fields to ADD to our schema

```json
{
  "effort": {
    "type": "string",
    "enum": ["low", "medium", "high", "max"],
    "description": "Effort level when this skill is active. Overrides session effort level. 'max' is Opus 4.6 only. Default: inherits from session."
  },
  "paths": {
    "oneOf": [
      {
        "type": "string",
        "description": "Comma-separated glob patterns for file-scoped activation."
      },
      {
        "type": "array",
        "items": { "type": "string" },
        "description": "Array of glob patterns for file-scoped activation."
      }
    ],
    "description": "Glob patterns limiting when this skill is activated. When set, Claude loads the skill only when working with files matching the patterns."
  },
  "shell": {
    "type": "string",
    "enum": ["bash", "powershell"],
    "description": "Shell for !`command` blocks. 'powershell' requires CLAUDE_CODE_USE_POWERSHELL_TOOL=1. Default: bash."
  },
  "mode": {
    "type": "boolean",
    "description": "UNCONFIRMED. When true, categorizes skill as a 'mode command' shown in a separate UI section. Default: false."
  },
  "license": {
    "type": "string",
    "description": "Agent Skills Standard. License name or reference to bundled license file."
  },
  "compatibility": {
    "type": "string",
    "maxLength": 500,
    "description": "Agent Skills Standard. Environment requirements (max 500 chars)."
  },
  "metadata": {
    "type": "object",
    "additionalProperties": { "type": "string" },
    "description": "Agent Skills Standard. Arbitrary key-value pairs (string-to-string map)."
  }
}
```

### Fields to UPDATE in our schema

```json
{
  "name": {
    "description": "ADD: Must not contain consecutive hyphens (--). Must not contain reserved words 'claude' or 'anthropic'. Must match parent directory name."
  },
  "description": {
    "description": "ADD: Should be written in third person. Falls back to first paragraph of markdown if omitted."
  }
}
```

### Fields already correct (no changes needed)

- `argument-hint`
- `disable-model-invocation`
- `user-invocable`
- `allowed-tools`
- `model`
- `context`
- `agent`
- `hooks`

---

*Research Version: 1.0.0*
*Constitutional Compliance: P-001 (all claims cited), P-002 (persisted to file), P-004 (full provenance), P-022 (gaps documented)*
*Agent: ps-researcher*
*Date: 2026-03-26*
