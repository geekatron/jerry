# GitHub Issue Scan: Claude Code Frontmatter Issues

> Systematic scan of anthropics/claude-code GitHub issues affecting agent and skill YAML frontmatter parsing, field behavior, and schema validation.

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Business/project impact overview |
| [L1: Detailed Findings](#l1-detailed-findings) | Per-issue technical analysis with schema impact |
| [L2: Strategic Implications](#l2-strategic-implications) | Architectural risk assessment and schema strategy |
| [Methodology](#methodology) | Search queries and source classification |
| [References](#references) | All cited GitHub issues with URLs |

---

## L0: Executive Summary

We scanned 40+ GitHub issues in the anthropics/claude-code repository covering frontmatter parsing bugs, undocumented fields, breaking changes, tool restrictions, and schema validation gaps. The scan reveals that Claude Code's frontmatter system is actively evolving and has significant undocumented behavior that directly affects Jerry's agent definition schema (H-34).

**Key takeaways for the project:**

1. **Claude Code has no proper YAML parser** -- it uses a simplified regex-based parser that fails on valid YAML multiline strings, flow sequences, and block scalars. This means our agents must use single-line values only in official frontmatter fields, or risk silent discovery failures.

2. **The `Task` tool was renamed to `Agent` in v2.1.63** -- this is a confirmed breaking change affecting hook payloads. Our schema and any hook-based validation must account for both names.

3. **Tool restriction (`disallowedTools`) is not a security boundary** -- agents can bypass it trivially via Bash. Our T1-T5 tier model provides governance value but should not be treated as enforcement against a determined agent.

4. **Several fields are undocumented but functional** -- `color` (8 named values), `isolation: "worktree"` (now documented), and `background: true` exist but were not in the official field table until recently.

5. **Custom frontmatter fields are stripped** -- any field beyond the recognized set is silently removed before being shown to the model. Our `.governance.yaml` separation pattern (H-34) is architecturally correct -- putting governance metadata in frontmatter would cause it to be silently lost.

---

## L1: Detailed Findings

### Category 1: Frontmatter Parsing Bugs

#### F-001: Multi-line YAML Descriptions Silently Break Discovery

| Attribute | Value |
|-----------|-------|
| **Issue** | [#4700](https://github.com/anthropics/claude-code/issues/4700), [#9817](https://github.com/anthropics/claude-code/issues/9817), [#11322](https://github.com/anthropics/claude-code/issues/11322) |
| **Status** | Closed (NOT_PLANNED) |
| **Summary** | Claude Code lacks a proper YAML parser. Multi-line `description` values (folded, literal, or Prettier-wrapped) cause the agent/skill file to be silently ignored. No error message is produced. |
| **Impact on our schemas** | CRITICAL. If any Jerry agent definition uses multi-line YAML in official frontmatter fields, the agent will silently fail to load. Our current agent definitions must be audited for multiline values in the `.md` frontmatter. |
| **Recommended schema action** | Add a CI validation rule (L5): all `.md` frontmatter fields must be single-line or quoted. Add to agent-development-standards.md as a MEDIUM standard. |

**Affected YAML patterns (all valid YAML, all broken in Claude Code):**
```yaml
# BROKEN - folded scalar
description: >
  Multi-line description that
  will be joined with spaces.

# BROKEN - literal scalar
description: |
  Multi-line description preserving
  newlines.

# BROKEN - implicit multiline (Prettier-formatted)
description:
  Expert code review specialist. Proactively reviews code
  for quality, security, and maintainability.

# WORKS - single line
description: Expert code review specialist. Reviews code for quality.

# WORKS - quoted (if content fits)
description: "Expert code review specialist. Reviews code for quality."
```

#### F-002: Flow Sequence Syntax Causes React Crash

| Attribute | Value |
|-----------|-------|
| **Issue** | [#22161](https://github.com/anthropics/claude-code/issues/22161), [#25826](https://github.com/anthropics/claude-code/issues/25826) |
| **Status** | Open |
| **Summary** | YAML flow sequences with colons in `argument-hint` (e.g., `[optional: path]`) are parsed as arrays of objects instead of strings, causing a React error #31 and unrecoverable TUI hang. |
| **Impact on our schemas** | LOW for Jerry (we do not use `argument-hint` in agent definitions). However, if skill definitions use bracket syntax in any field, they would crash. |
| **Recommended schema action** | Add a validation warning for YAML values containing unquoted brackets in any frontmatter field. |

#### F-003: Missing `name` Field Causes API 500 Errors

| Attribute | Value |
|-----------|-------|
| **Issue** | [#6377](https://github.com/anthropics/claude-code/issues/6377), [#22843](https://github.com/anthropics/claude-code/issues/22843) |
| **Status** | Closed (NOT_PLANNED) |
| **Summary** | Agent files missing the `name` field in frontmatter cause the entire Claude Code session to return API 500 errors on all subsequent requests. The parse error is logged at DEBUG level but not surfaced to the user. Files without any frontmatter at all are even worse -- completely blocking. |
| **Impact on our schemas** | MEDIUM. Our H-34 schema already requires `name` as a required field in `.md` frontmatter. This confirms that omitting it is not just a schema violation but a runtime crasher. |
| **Recommended schema action** | No schema change needed -- `name` is already required. Add a pre-flight check (L3) that validates all agent `.md` files have valid frontmatter with `name` before session start. |

#### F-004: Invalid Glob Patterns in `paths` Property

| Attribute | Value |
|-----------|-------|
| **Issue** | [#13905](https://github.com/anthropics/claude-code/issues/13905) |
| **Status** | Open |
| **Summary** | Glob patterns starting with `{` or `*` are reserved YAML indicators and cannot be used unquoted in `paths` frontmatter. Patterns like `{src,lib}/**/*.ts` and `**/*.ts` fail parsing. |
| **Impact on our schemas** | LOW. Jerry rules files use `paths` in `.claude/rules/` but do not use glob patterns in agent/skill frontmatter. |
| **Recommended schema action** | Document that glob patterns in `paths` must be quoted. |

---

### Category 2: Undocumented Fields

#### F-005: `color` Field -- Undocumented but Functional

| Attribute | Value |
|-----------|-------|
| **Issue** | [#8501](https://github.com/anthropics/claude-code/issues/8501), [#21501](https://github.com/anthropics/claude-code/issues/21501), [#23691](https://github.com/anthropics/claude-code/issues/23691) |
| **Status** | #8501 Closed (NOT_PLANNED), #21501 Open |
| **Summary** | Agent definitions accept a `color` frontmatter field with 8 hardcoded named values (blue, purple, yellow, green, magenta, cyan, red, white). The `/agents` slash command uses it, and it is parsed from frontmatter, but it is not in the official documentation table. |
| **Impact on our schemas** | LOW. Jerry does not use `color` in agent definitions. However, this confirms that Claude Code's field set is broader than documented. |
| **Recommended schema action** | Add `color` as an optional field to the recognized-fields list in agent-development-standards.md with a note that it is undocumented. Do NOT add to our `.md` frontmatter since it is cosmetic only. |

#### F-006: `isolation: "worktree"` -- Was Undocumented, Now Fixed

| Attribute | Value |
|-----------|-------|
| **Issue** | [#27023](https://github.com/anthropics/claude-code/issues/27023) |
| **Status** | Closed (COMPLETED) |
| **Summary** | The `isolation` field accepting `"worktree"` was missing from subagent docs. Now documented as of v2.1.49+. |
| **Impact on our schemas** | Our H-34 field table already lists `isolation` as `enum: worktree`. Confirmed correct. |
| **Recommended schema action** | No change needed. Confirmed our schema is aligned. |

#### F-007: `background: true` -- Added for Background Agents

| Attribute | Value |
|-----------|-------|
| **Issue** | [#22034](https://github.com/anthropics/claude-code/issues/22034) |
| **Status** | Feature request |
| **Summary** | Agent definitions support `background: true` to always run as a background task. |
| **Impact on our schemas** | Our H-34 field table already lists `background` as `boolean`. Confirmed correct. |
| **Recommended schema action** | No change needed. |

#### F-008: Custom Frontmatter Fields Are Silently Stripped

| Attribute | Value |
|-----------|-------|
| **Issue** | [#13005](https://github.com/anthropics/claude-code/issues/13005) |
| **Status** | Closed (duplicate of #13003) |
| **Summary** | Any frontmatter field beyond the recognized set (`name`, `description`, and the extended fields) is silently stripped before being shown to the model. The field is parsed but discarded. |
| **Impact on our schemas** | CRITICAL VALIDATION. This confirms that Jerry's dual-file architecture (H-34) is architecturally correct. If we put governance metadata (version, tool_tier, identity, etc.) in the `.md` frontmatter, it would be silently stripped by Claude Code and never reach the agent. The `.governance.yaml` companion file approach avoids this entirely. |
| **Recommended schema action** | Document this finding as a design rationale note in agent-development-standards.md. This is strong evidence supporting the H-34 dual-file architecture decision. |

---

### Category 3: Breaking Changes

#### F-009: Task Tool Renamed to Agent (v2.1.63)

| Attribute | Value |
|-----------|-------|
| **Issue** | [#29677](https://github.com/anthropics/claude-code/issues/29677) |
| **Status** | Open (stale) |
| **Summary** | Claude Code v2.1.63 renamed the `Task` tool to `Agent`. The `tools` filter in settings.json is backward-compatible (still accepts `"Task"`), but the `tool_name` field in hook payloads changed from `"Task"` to `"Agent"`. Hook scripts checking for `"Task"` silently pass through without executing validation logic. |
| **Impact on our schemas** | HIGH. Jerry's agent-development-standards.md references the `Task` tool extensively. Our H-35 rule says "Worker agents MUST NOT include `Task` in the official `tools` frontmatter field." If Claude Code no longer recognizes `Task` as a tool name, our constraint language must be updated. Our settings.json permission patterns may also need updating. |
| **Recommended schema action** | (1) Audit all references to "Task tool" in Jerry rule files and agent definitions. (2) Update H-35 to reference both `Task` and `Agent` or use a version-conditional reference. (3) Update hook scripts to match both tool names. (4) Verify settings.json `allow`/`deny` patterns work with both names. |

#### F-010: Custom Agents Stopped Working in VS Code Extension

| Attribute | Value |
|-----------|-------|
| **Issue** | [#9139](https://github.com/anthropics/claude-code/issues/9139) |
| **Status** | Closed |
| **Summary** | Custom agents with proper YAML frontmatter that worked in previous versions no longer worked in the VS Code extension. Breaking change with no migration path. |
| **Impact on our schemas** | MEDIUM. Jerry primarily uses CLI, but VS Code extension users may encounter this. |
| **Recommended schema action** | No schema change. Document as a known environment-specific issue. |

---

### Category 4: Field Interaction Bugs

#### F-011: `context: fork` + `agent:` Fields Ignored by Skill Tool

| Attribute | Value |
|-----------|-------|
| **Issue** | [#17283](https://github.com/anthropics/claude-code/issues/17283), [#18394](https://github.com/anthropics/claude-code/issues/18394) |
| **Status** | Closed (COMPLETED, marked duplicate of #16803) |
| **Summary** | When a skill is invoked via the Skill tool, the `context: fork` and `agent:` frontmatter fields are ignored 95%+ of the time. The skill runs in the main conversation context instead of spawning the specified subagent. |
| **Impact on our schemas** | LOW for current Jerry usage (Jerry skills do not use `context: fork`). However, if Jerry were to adopt forked skill contexts for isolation, this would be a blocker. |
| **Recommended schema action** | No immediate schema change. Add to a "known limitations" section for future reference. |

#### F-012: `context: fork` Breaks `AskUserQuestion`

| Attribute | Value |
|-----------|-------|
| **Issue** | [#19751](https://github.com/anthropics/claude-code/issues/19751), [#34592](https://github.com/anthropics/claude-code/issues/34592) |
| **Status** | Open |
| **Summary** | Using `context: fork` in skill frontmatter breaks the `AskUserQuestion` tool -- foreground sub-agents that should have access to user interaction cannot prompt the user. |
| **Impact on our schemas** | MEDIUM. If Jerry agents rely on `AskUserQuestion` (which they do for H-31 clarification), forked contexts would break this capability. |
| **Recommended schema action** | Document incompatibility between `context: fork` and `AskUserQuestion`. |

#### F-013: Agent Body Content Not Injected via Task Tool

| Attribute | Value |
|-----------|-------|
| **Issue** | [#13627](https://github.com/anthropics/claude-code/issues/13627) |
| **Status** | Closed (NOT_PLANNED, duplicate of #4554) |
| **Summary** | The markdown body content (instructions after `---` frontmatter) of custom agents defined in `.claude/agents/*.md` is completely ignored when spawned as a subagent via the Task tool. Only the YAML frontmatter metadata (name, description, color) is used. The system prompt function exists but its output is never passed to the spawn function. |
| **Impact on our schemas** | CRITICAL. This means agent instruction content in the `.md` body may not reach the spawned agent. Jerry's entire agent definition architecture relies on the markdown body containing the agent's identity, methodology, guardrails, and output specifications. If this bug is active in our Claude Code version, our agents may be running without their instructions. |
| **Recommended schema action** | IMMEDIATE: Verify whether this bug affects Jerry's current Claude Code version. Test by adding a canary phrase to an agent's markdown body and confirming it appears in the agent's output. If confirmed, investigate the plugin-based workaround (SubagentStart hook injection per PR #20654). |

#### F-014: `skills:` Field Not Preloaded for Team Teammates

| Attribute | Value |
|-----------|-------|
| **Issue** | [#29441](https://github.com/anthropics/claude-code/issues/29441), [#27736](https://github.com/anthropics/claude-code/issues/27736) |
| **Status** | Closed (duplicate of #24780) |
| **Summary** | When team orchestration spawns an agent as a separate process (not via Task tool), skills declared in frontmatter `skills:` field are silently ignored. In-process subagents (Task tool) work correctly. Additionally, the `skills` field value is not rendered in the Task tool's agent description, so the orchestrator cannot see what skills an agent has. |
| **Impact on our schemas** | MEDIUM. Jerry uses the Task tool (in-process path) which reportedly works. But the visibility gap means orchestrators cannot see agent skill lists during routing. |
| **Recommended schema action** | No schema change needed. Note that `skills` field works for Task tool but not for team teammates. |

#### F-015: Worktree Isolation + Context Compaction Creates Nested Worktrees

| Attribute | Value |
|-----------|-------|
| **Issue** | [#27881](https://github.com/anthropics/claude-code/issues/27881), [#29110](https://github.com/anthropics/claude-code/issues/29110) |
| **Status** | Closed (NOT_PLANNED) |
| **Summary** | When context compaction triggers during worktree-isolated agent execution, the CWD drifts into the worktree path. Subsequent worktree creations nest inside the previous one. When nesting fails silently, the agent falls back to the main branch and commits directly, bypassing branch isolation. |
| **Impact on our schemas** | MEDIUM. Jerry does not currently use `isolation: worktree`, but this is a documented field. If adopted, context compaction could cause security violations. |
| **Recommended schema action** | Add a warning note to agent-development-standards.md about the `isolation: worktree` + context compaction interaction. |

---

### Category 5: Tool Restriction Issues

#### F-016: `disallowedTools` Trivially Bypassed via Bash

| Attribute | Value |
|-----------|-------|
| **Issue** | [#31292](https://github.com/anthropics/claude-code/issues/31292) |
| **Status** | Open |
| **Summary** | `disallowedTools: [Write, Edit]` is trivially bypassed via Bash commands (sed, awk, echo, tee, etc.). The restriction is name-based, not capability-based. An agent with Bash access can perform any file operation regardless of `disallowedTools`. |
| **Impact on our schemas** | HIGH. Jerry's T1-T5 tool tier model uses `tools` and `disallowedTools` in frontmatter to enforce principle of least privilege. This finding means tool restrictions are governance-level (advisory) not enforcement-level (deterministic). Any agent with Bash access effectively has T2+ write capability regardless of tier assignment. |
| **Recommended schema action** | (1) Add a note to agent-development-standards.md Tool Security Tiers section that `disallowedTools` is not a security boundary when Bash is available. (2) T1 (Read-Only) agents MUST NOT have Bash in their `tools` list if read-only enforcement is required. (3) Consider adding this to the Known Limitations section. |

#### F-017: `allowed-tools` in SKILL.md Not Enforced

| Attribute | Value |
|-----------|-------|
| **Issue** | [#18837](https://github.com/anthropics/claude-code/issues/18837), [#18737](https://github.com/anthropics/claude-code/issues/18737) |
| **Status** | Open / Closed (various) |
| **Summary** | The `allowed-tools` field in skill frontmatter does not appear to be enforced by the CLI -- Claude can freely use tools not listed. Additionally, the Agent SDK ignores `allowed-tools` entirely, requiring manual replication in SDK options. |
| **Impact on our schemas** | MEDIUM. Jerry skills define `allowed-tools` but if the CLI does not enforce them, the restriction is aspirational only. |
| **Recommended schema action** | Document that `allowed-tools` enforcement depends on Claude Code version and may not be reliable. |

#### F-018: Custom Agents Cannot Use MCP Tools Despite Frontmatter

| Attribute | Value |
|-----------|-------|
| **Issue** | [#25200](https://github.com/anthropics/claude-code/issues/25200), [#13605](https://github.com/anthropics/claude-code/issues/13605) |
| **Status** | Open |
| **Summary** | Custom agents defined in `.claude/agents/` cannot access MCP tools at runtime, even when the MCP server is declared via `mcpServers` in frontmatter and tool names are listed in `tools`. The MCP tools are not injected into the subagent's tool inventory. |
| **Impact on our schemas** | HIGH. Jerry agents like ps-researcher declare `mcpServers: context7` in frontmatter with the expectation that Context7 tools will be available. If this bug is active, MCP tools would be silently unavailable to subagents. |
| **Recommended schema action** | IMMEDIATE: Verify whether MCP tools declared in agent frontmatter actually reach subagents in Jerry's current deployment. If not, document the workaround (MCP tools must be configured at the session level, not per-agent). |

---

### Category 6: Hooks Gotchas

#### F-019: Hooks in Agent Frontmatter Not Executed for Subagents

| Attribute | Value |
|-----------|-------|
| **Issue** | [#18392](https://github.com/anthropics/claude-code/issues/18392), [#17688](https://github.com/anthropics/claude-code/issues/17688) |
| **Status** | Closed (duplicate of #17688) |
| **Summary** | All three hook types (PreToolUse, PostToolUse, Stop) defined in agent frontmatter are completely ignored when the agent runs as a subagent via the Task tool. No log files are generated, no commands are executed. |
| **Impact on our schemas** | HIGH. If Jerry defines hooks in agent frontmatter for validation or enforcement (L3/L4 enforcement layers), they will not fire for subagents. This means agent-level hooks cannot be used for tool-call gating in the orchestrator-worker topology. |
| **Recommended schema action** | (1) Document that hooks in agent `.md` frontmatter are NOT executed for subagents. (2) All hook-based enforcement must be defined at the session level (`.claude/hooks.json` or project-level hooks), not in individual agent definitions. (3) Review our enforcement architecture (L3/L4) for reliance on agent-level hooks. |

#### F-020: `once: true` Not Supported for Agent Hooks

| Attribute | Value |
|-----------|-------|
| **Issue** | [#19410](https://github.com/anthropics/claude-code/issues/19410) |
| **Status** | Closed (COMPLETED -- docs fixed) |
| **Summary** | The `once: true` hook option is only supported for skills, not for agents. The sub-agents documentation had an incorrect example showing `once: true` in an agent hook. The docs were corrected to remove the misleading example. |
| **Impact on our schemas** | LOW. Jerry does not currently use `once: true` in agent hooks. |
| **Recommended schema action** | Add a constraint note: `hooks.*.once` is only valid for SKILL.md, not for agent definitions. |

#### F-021: Skill-Scoped Hooks Not Triggered in Plugins

| Attribute | Value |
|-----------|-------|
| **Issue** | [#17688](https://github.com/anthropics/claude-code/issues/17688) |
| **Status** | Open |
| **Summary** | Hooks defined in SKILL.md frontmatter using the `hooks` YAML property are not triggered when the skill is loaded within a plugin context. |
| **Impact on our schemas** | LOW for current Jerry (not plugin-based). Relevant if Jerry is ever packaged as a Claude Code plugin. |
| **Recommended schema action** | No immediate action. Note for future plugin packaging work. |

---

### Category 7: Schema/Validation Requests

#### F-022: VS Code Extension Schema Outdated for SKILL.md

| Attribute | Value |
|-----------|-------|
| **Issue** | [#23330](https://github.com/anthropics/claude-code/issues/23330), [#25380](https://github.com/anthropics/claude-code/issues/25380), [#24975](https://github.com/anthropics/claude-code/issues/24975), [#26795](https://github.com/anthropics/claude-code/issues/26795) |
| **Status** | Closed (duplicate chain) |
| **Summary** | The VS Code extension's YAML schema validator only recognizes 5 base Agent Skills standard fields (compatibility, description, license, metadata, name) but rejects 9 Claude Code extended fields (allowed-tools, argument-hint, context, agent, model, hooks, disable-model-invocation, user-invocable, version). |
| **Impact on our schemas** | MEDIUM. This confirms that there are TWO field sets: (1) the Agent Skills open standard (5 fields) and (2) Claude Code extensions (9+ fields). Our schema should distinguish between these. |
| **Recommended schema action** | (1) Document the two-tier field set (Agent Skills standard vs. Claude Code extensions) in our schema. (2) Note that the VS Code extension may show false-positive validation errors for extended fields. |

#### F-023: Plugin Validate Tool Improved

| Attribute | Value |
|-----------|-------|
| **Issue** | Changelog reference |
| **Status** | Implemented |
| **Summary** | The `claude plugin validate` command now checks skill, agent, and command frontmatter plus hooks/hooks.json, catching YAML parse errors and schema violations. |
| **Impact on our schemas** | POSITIVE. We can use `claude plugin validate` as a supplementary validation step alongside our own JSON Schema validation. |
| **Recommended schema action** | Consider integrating `claude plugin validate` into our L5 CI checks if Jerry is structured as a plugin. |

---

### Category 8: Permission Mode Issues

#### F-024: `bypassPermissions` Inherited by All Subagents

| Attribute | Value |
|-----------|-------|
| **Issue** | [#20264](https://github.com/anthropics/claude-code/issues/20264), [#29610](https://github.com/anthropics/claude-code/issues/29610) |
| **Status** | Open |
| **Summary** | When a parent agent uses `permissionMode: bypassPermissions`, all subagents unconditionally inherit this mode -- it cannot be overridden to a more restrictive mode. Additionally, `bypassPermissions` does not bypass Read/Bash for paths outside the project root in background subagents. |
| **Impact on our schemas** | HIGH for security model. If Jerry's main context uses `bypassPermissions`, all worker agents inherit it regardless of their individual `permissionMode` frontmatter settings. The per-agent permission mode in frontmatter is advisory only when the parent is permissive. |
| **Recommended schema action** | (1) Document that `permissionMode` in agent frontmatter is overridden by the parent's mode when more permissive. (2) If session-level permissions are `bypassPermissions`, agent-level restrictions are ineffective. |

#### F-025: Sandbox + `bypassPermissions` Interaction Gap

| Attribute | Value |
|-----------|-------|
| **Issue** | [#29048](https://github.com/anthropics/claude-code/issues/29048), [#17838](https://github.com/anthropics/claude-code/issues/17838) |
| **Status** | Open |
| **Summary** | When using `bypassPermissions` with sandbox enabled, `sandbox.filesystem.allowWrite` restrictions are only enforced for the Bash tool. Write/Edit tools run in-process via `fs.writeFileSync` and are not subject to bwrap filesystem isolation. |
| **Impact on our schemas** | LOW for Jerry (does not use sandbox mode). |
| **Recommended schema action** | No immediate action. |

---

### Category 9: Field Naming Inconsistencies

#### F-026: Kebab-case vs. camelCase Field Name Inconsistency

| Attribute | Value |
|-----------|-------|
| **Issue** | Multiple issues, observed across documentation |
| **Status** | Active inconsistency |
| **Summary** | SKILL.md uses kebab-case fields (`allowed-tools`, `argument-hint`, `disable-model-invocation`, `user-invocable`). Agent `.md` files use camelCase fields (`disallowedTools`, `mcpServers`, `maxTurns`, `permissionMode`). This is a confirmed naming convention split between skill and agent contexts. |
| **Impact on our schemas** | MEDIUM. Our H-34 documentation lists agent fields in camelCase but our skills would need kebab-case. Using the wrong casing for a context would cause silent field stripping. |
| **Recommended schema action** | (1) Explicitly document the naming convention split: skills use kebab-case, agents use camelCase. (2) Add validation that checks field casing matches the file type. |

---

## Consolidated Field Registry

Based on all findings, the complete known field set for each context:

### Agent Definition Fields (`.claude/agents/*.md`)

| Field | Type | Status | Notes |
|-------|------|--------|-------|
| `name` | string | **Required** | Missing causes API 500 errors (F-003) |
| `description` | string | Recommended | MUST be single-line (F-001) |
| `tools` | string/array | Optional | Allowlist; inherits ALL if omitted |
| `disallowedTools` | string/array | Optional | Name-based, bypassable via Bash (F-016) |
| `model` | enum | Optional | sonnet, opus, haiku, inherit |
| `permissionMode` | enum | Optional | Overridden by parent if parent is more permissive (F-024) |
| `maxTurns` | number | Optional | Max agentic turns |
| `skills` | array | Optional | Works for Task tool, not for team teammates (F-014) |
| `mcpServers` | object/string | Optional | May not work for custom agents (F-018) |
| `hooks` | object | Optional | NOT executed for subagents (F-019) |
| `memory` | enum | Optional | user, project, local |
| `background` | boolean | Optional | Run as background task |
| `isolation` | enum | Optional | "worktree"; has compaction bug (F-015) |
| `color` | string | Undocumented | 8 named values: blue, purple, yellow, green, magenta, cyan, red, white |

### Skill Definition Fields (`SKILL.md`)

| Field | Type | Status | Notes |
|-------|------|--------|-------|
| `name` | string | Optional | Lowercase + hyphens, max 64 chars; derived from directory if omitted |
| `description` | string | Recommended | MUST be single-line (F-001) |
| `allowed-tools` | string | Optional | May not be enforced (F-017) |
| `argument-hint` | string | Optional | Avoid unquoted brackets (F-002) |
| `context` | enum | Optional | "fork"; unreliable 95%+ of the time (F-011) |
| `agent` | string | Optional | Subagent type; ignored when context:fork fails |
| `model` | enum | Optional | Model override when skill is active |
| `hooks` | object | Optional | Not triggered in plugin contexts (F-021) |
| `disable-model-invocation` | boolean | Optional | Require manual /name invocation |
| `user-invocable` | boolean | Optional | Hide from / menu if false |
| `version` | string | Optional | Rejected by VS Code validator (F-022) |

### Agent Skills Open Standard Fields (recognized by VS Code validator)

| Field | Status |
|-------|--------|
| `compatibility` | Standard |
| `description` | Standard |
| `license` | Standard |
| `metadata` | Standard |
| `name` | Standard |

---

## L2: Strategic Implications

### Risk Assessment

| Risk | Severity | Likelihood | Mitigation |
|------|----------|-----------|------------|
| Agent instructions not reaching subagents (F-013) | Critical | Unknown (version-dependent) | Verify immediately; prepare SubagentStart hook workaround |
| MCP tools unavailable in subagents (F-018) | High | Likely for `.claude/agents/` | Verify; ensure MCP is session-level not per-agent |
| Tool restrictions bypassable (F-016) | High | Certain if Bash is available | Document as advisory; T1 agents must exclude Bash |
| Hooks not firing in subagents (F-019) | High | Confirmed | Move enforcement to session-level hooks |
| Task-to-Agent rename breaking hooks (F-009) | High | Confirmed in v2.1.63+ | Dual-name matching in all hook scripts |
| Silent parsing failures (F-001) | Medium | High for Prettier users | CI lint rule for single-line frontmatter |
| Permission mode inheritance (F-024) | Medium | Confirmed | Document hierarchy; test in isolation |

### Schema Strategy Recommendations

1. **H-34 dual-file architecture is strongly validated** by F-008 (custom fields stripped) and F-013 (body content may not be injected). The separation into `.md` (official fields only) + `.governance.yaml` (machine-readable governance) is the correct design given Claude Code's behavior.

2. **Add a "Claude Code Known Limitations" section** to agent-development-standards.md documenting: (a) single-line frontmatter requirement, (b) disallowedTools bypass via Bash, (c) hooks not firing for subagents, (d) MCP tool injection uncertainty for custom agents.

3. **Audit the Task-to-Agent rename impact** across all Jerry rule files, agent definitions, and settings files. This is the most immediate action item.

4. **Verify F-013 (body content injection) in Jerry's current version** -- if agent instructions are not reaching subagents, this is a critical runtime failure that needs workaround before any further agent development.

5. **Reclassify tool tier enforcement** -- given F-016, the T1-T5 model provides governance structure and routing guidance but should be explicitly labeled as "advisory" rather than "enforced" in documentation. True enforcement requires excluding Bash from the `tools` list for agents that must be read-only.

---

## Methodology

### Search Queries Executed

| # | Query | Results |
|---|-------|---------|
| 1 | `site:github.com/anthropics/claude-code frontmatter yaml issue` | 10 issues |
| 2 | `site:github.com/anthropics/claude-code "SKILL.md" yaml frontmatter` | 10 issues |
| 3 | `site:github.com/anthropics/claude-code subagent schema agent definition` | 10 issues |
| 4 | `site:github.com/anthropics/claude-code mcpServers frontmatter` | 10 issues |
| 5 | `site:github.com/anthropics/claude-code hooks frontmatter agent skill bug` | 10 issues |
| 6 | `site:github.com/anthropics/claude-code "context: fork" agent bug` | 7 issues |
| 7 | `site:github.com/anthropics/claude-code Task Agent rename tool "v2.1"` | 10 issues |
| 8 | `site:github.com/anthropics/claude-code "allowed-tools" OR "disallowedTools"` | 10 issues |
| 9 | `site:github.com/anthropics/claude-code deprecated field agent "breaking change"` | 6 issues |
| 10 | `site:github.com/anthropics/claude-code "isolation" OR "worktree" OR "background"` | 10 issues |
| 11 | `site:github.com/anthropics/claude-code official schema validation request` | 10 issues |
| 12 | `site:github.com/anthropics/claude-code "color" field agent frontmatter` | 10 issues |
| 13 | `site:github.com/anthropics/claude-code "memory" field agent frontmatter` | 10 issues |
| 14 | `site:github.com/anthropics/claude-code "permissionMode" agent frontmatter` | 10 issues |

### Source Credibility

| Source Type | Credibility | Count |
|-------------|------------|-------|
| GitHub Issues (anthropics/claude-code) | HIGH -- primary source, bug reports with reproduction steps | 40+ issues |
| Claude Code Documentation (code.claude.com) | HIGH -- official documentation | Referenced |
| Claude Code Changelog | HIGH -- official release notes | Referenced |

### Limitations

1. **Version currency** -- Some issues may have been fixed in versions newer than those referenced. Status was checked at scan time (2026-03-26) but may have changed.
2. **Search coverage** -- GitHub search is limited to indexed content and may miss issues with unusual phrasing or those in closed/locked state.
3. **Reproduction not performed** -- Findings are based on issue reports, not local reproduction. F-013 and F-018 should be verified in Jerry's current environment before taking action.

---

## References

### Category 1: Frontmatter Parsing Bugs
1. [#4700 - Agent YAML Parsing Fails with Valid Line Breaks in Frontmatter](https://github.com/anthropics/claude-code/issues/4700) -- Key insight: Claude Code has no proper YAML parser; multiline values silently break discovery
2. [#9817 - Skill discovery is very sensitive to frontmatter formatting](https://github.com/anthropics/claude-code/issues/9817) -- Key insight: Silent failure with no error message
3. [#11322 - Skill frontmatter parser fails on Prettier-formatted multi-line descriptions](https://github.com/anthropics/claude-code/issues/11322) -- Key insight: Prettier auto-wrapping triggers the bug
4. [#22161 - argument-hint YAML frontmatter with brackets causes React error #31](https://github.com/anthropics/claude-code/issues/22161) -- Key insight: Flow sequences with colons cause TUI crash
5. [#6377 - Frontmatter Parsing Error: Missing 'name' Field Despite Valid YAML](https://github.com/anthropics/claude-code/issues/6377) -- Key insight: Platform-specific parsing failures
6. [#22843 - Malformed agent files cause API 500 errors](https://github.com/anthropics/claude-code/issues/22843) -- Key insight: Missing frontmatter causes cascading API failures
7. [#13905 - Invalid YAML syntax in claude/rules frontmatter paths property](https://github.com/anthropics/claude-code/issues/13905) -- Key insight: Glob patterns must be quoted in YAML

### Category 2: Undocumented Fields
8. [#8501 - Claude Code subagent YAML Frontmatter authoritative documentation](https://github.com/anthropics/claude-code/issues/8501) -- Key insight: `color` field is undocumented but functional
9. [#21501 - Feature: Add color/icon support in agent front matter](https://github.com/anthropics/claude-code/issues/21501) -- Key insight: 8 hardcoded color values
10. [#27023 - Subagents documentation missing isolation: "worktree" configuration](https://github.com/anthropics/claude-code/issues/27023) -- Key insight: Now documented as of Feb 2026
11. [#13005 - SKILL.md custom frontmatter fields are stripped before showing to model](https://github.com/anthropics/claude-code/issues/13005) -- Key insight: Custom fields silently discarded

### Category 3: Breaking Changes
12. [#29677 - Task to Agent tool rename in v2.1.63 breaks hook payloads](https://github.com/anthropics/claude-code/issues/29677) -- Key insight: Undocumented breaking change; hook scripts silently bypassed
13. [#9139 - Custom agents no longer work in VSCode extension](https://github.com/anthropics/claude-code/issues/9139) -- Key insight: Breaking change with no migration path

### Category 4: Field Interaction Bugs
14. [#17283 - Skill tool should honor context: fork and agent: frontmatter fields](https://github.com/anthropics/claude-code/issues/17283) -- Key insight: Fields ignored 95%+ of the time
15. [#18394 - Skill frontmatter fork parameter fails inconsistently](https://github.com/anthropics/claude-code/issues/18394) -- Key insight: context:fork unreliable
16. [#19751 - context: fork in a skill breaks AskUserQuestion](https://github.com/anthropics/claude-code/issues/19751) -- Key insight: Forked contexts lose user interaction
17. [#13627 - Custom agent body content not injected when subagent is spawned via Task tool](https://github.com/anthropics/claude-code/issues/13627) -- Key insight: Agent instructions may be completely ignored
18. [#29441 - Agent skills: frontmatter not preloaded for team-spawned teammates](https://github.com/anthropics/claude-code/issues/29441) -- Key insight: skills field only works for Task tool path
19. [#27736 - Agent skills field from frontmatter not rendered in Task tool agent description](https://github.com/anthropics/claude-code/issues/27736) -- Key insight: Orchestrators cannot see agent skill lists
20. [#27881 - EnterWorktree creates nested worktrees when CWD drifts after context compaction](https://github.com/anthropics/claude-code/issues/27881) -- Key insight: Worktree isolation bypassed on compaction
21. [#29110 - Spawned agents: bypassPermissions ineffective, worktree data loss, plan mode loop](https://github.com/anthropics/claude-code/issues/29110) -- Key insight: Multiple agent spawning issues

### Category 5: Tool Restriction Issues
22. [#31292 - disallowedTools trivially bypassed via Bash tool](https://github.com/anthropics/claude-code/issues/31292) -- Key insight: Tool restrictions are name-based not capability-based
23. [#18837 - allowed-tools in skill frontmatter not enforced](https://github.com/anthropics/claude-code/issues/18837) -- Key insight: Skill tool restrictions may be unenforced
24. [#18737 - Major Inconsistency in SKILL.md allowed-tools support between CLI and Agent SDK](https://github.com/anthropics/claude-code/issues/18737) -- Key insight: SDK ignores allowed-tools entirely
25. [#25200 - Custom agents cannot use deferred MCP tools even when declared in mcpServers/tools](https://github.com/anthropics/claude-code/issues/25200) -- Key insight: MCP tools not injected into subagent inventory
26. [#13605 - Custom plugin subagents cannot access MCP tools](https://github.com/anthropics/claude-code/issues/13605) -- Key insight: Built-in agents can, custom cannot

### Category 6: Hooks Gotchas
27. [#18392 - Hooks in agent frontmatter are not executed for subagents](https://github.com/anthropics/claude-code/issues/18392) -- Key insight: All hook types ignored for subagents
28. [#17688 - Skill-scoped hooks defined in SKILL.md frontmatter are not triggered within plugins](https://github.com/anthropics/claude-code/issues/17688) -- Key insight: Plugin context breaks hook execution
29. [#19410 - Inconsistent documentation regarding once: true support for Agent hooks](https://github.com/anthropics/claude-code/issues/19410) -- Key insight: once:true only for skills, not agents

### Category 7: Schema/Validation
30. [#23330 - VS Code Extension: YAML Frontmatter Validation Schema Outdated for SKILL.md](https://github.com/anthropics/claude-code/issues/23330) -- Key insight: 5 standard fields vs. 14+ extended fields
31. [#25380 - SKILL.md validator only recognizes Agent Skills standard fields](https://github.com/anthropics/claude-code/issues/25380) -- Key insight: Two-tier field set confirmed
32. [#24975 - IDE validator does not recognize allowed-tools in skill frontmatter](https://github.com/anthropics/claude-code/issues/24975) -- Key insight: Extended fields rejected
33. [#26795 - Skill frontmatter validator reports allowed-tools as unsupported despite being valid](https://github.com/anthropics/claude-code/issues/26795) -- Key insight: Validator schema not updated

### Category 8: Permission Mode
34. [#20264 - Allow restrictive permission modes for subagents even when parent uses bypassPermissions](https://github.com/anthropics/claude-code/issues/20264) -- Key insight: Permission mode inheritance cannot be restricted
35. [#29610 - bypassPermissions does not bypass Read/Bash for paths outside project root](https://github.com/anthropics/claude-code/issues/29610) -- Key insight: bypassPermissions has its own limitations
36. [#29048 - sandbox.filesystem.allowWrite not enforced for Write/Edit in bypassPermissions](https://github.com/anthropics/claude-code/issues/29048) -- Key insight: Sandbox enforcement gap

---

*Research conducted: 2026-03-26*
*Agent: ps-researcher*
*PS Context: PROJ-024-tactical-work / GitHub Issue Scan*
*Sources: 36 GitHub issues from anthropics/claude-code repository*
*Confidence: HIGH (primary source analysis of official repository issues)*
