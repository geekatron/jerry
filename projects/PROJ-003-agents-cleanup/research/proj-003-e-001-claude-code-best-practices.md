# Research: Claude Code Plugin Structure Best Practices

| Metadata | Value |
|----------|-------|
| **Document ID** | proj-003-e-001 |
| **PS ID** | proj-003 |
| **Entry Type** | Research |
| **Topic** | Claude Code Plugin Structure Best Practices |
| **Date** | 2026-01-12 |
| **Author** | ps-researcher (v2.0.0) |
| **Status** | Complete |

---

## L0: Executive Summary

Claude Code plugins provide a structured approach to extending Claude's capabilities through **Skills**, **Agents** (Subagents), **Commands**, and **Hooks**. Based on Anthropic's official documentation and community best practices from 2024-2026:

**Key Findings:**

1. **Plugin Directory Structure**: All plugins MUST follow a standardized structure with `.claude-plugin/plugin.json` as the manifest and component directories (commands/, agents/, skills/, hooks/) at the **plugin root level**, NOT inside `.claude-plugin/`.

2. **Skills vs Commands vs Agents**:
   - **Skills**: Auto-invoked by Claude based on task context; use for portable expertise
   - **Commands**: User-initiated via `/command` syntax; use for explicit, repeatable workflows
   - **Agents**: Autonomous subprocesses for complex multi-step tasks; can invoke skills and commands

3. **Migration Path**: Anthropic recommends migrating from standalone `.claude/` configurations to plugin-based structures for team sharing and versioning.

4. **Deprecation Note**: Skills and slash commands were **merged** in v2.1.3 (simplified mental model, no behavioral change). Output styles were deprecated then restored based on community feedback.

---

## L1: Technical Summary

### 1. Plugin Directory Structure (Official)

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # REQUIRED: Plugin manifest (ONLY this inside .claude-plugin/)
├── commands/                # Slash commands (optional) - .md files
├── agents/                  # Subagent definitions (optional) - .md files
├── skills/                  # Agent skills (optional) - subdirectories with SKILL.md
│   └── skill-name/
│       ├── SKILL.md         # Required for each skill
│       ├── scripts/         # Python/Bash automation
│       ├── references/      # Documentation loaded into context
│       └── assets/          # Templates, binary files
├── hooks/
│   └── hooks.json           # Event handler configuration
├── .mcp.json                # MCP server definitions (optional)
├── scripts/                 # Helper scripts and utilities
└── README.md                # Plugin documentation
```

**Critical Rule**: Component directories (commands/, agents/, skills/, hooks/) **MUST be at plugin root**, NOT nested inside `.claude-plugin/`. Only `plugin.json` belongs in `.claude-plugin/`.

### 2. Plugin Manifest Schema (plugin.json)

```json
{
  "$schema": "https://anthropic.com/claude-code/plugin.schema.json",
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Brief explanation of plugin purpose",
  "author": {
    "name": "Author Name",
    "email": "author@example.com",
    "url": "https://example.com"
  },
  "homepage": "https://docs.example.com",
  "repository": {
    "type": "git",
    "url": "https://github.com/user/plugin-name.git"
  },
  "license": "MIT",
  "keywords": ["automation", "workflow"],
  "commands": "./commands",
  "agents": ["./agents", "./specialized-agents"],
  "hooks": "./hooks/hooks.json",
  "mcpServers": "./.mcp.json"
}
```

**Required Fields**: `name`, `version`, `description`

**Optional Fields**: `author`, `homepage`, `repository`, `license`, `keywords`, `commands`, `agents`, `hooks`, `mcpServers`

### 3. Component Comparison Matrix

| Aspect | Skills | Commands | Agents (Subagents) |
|--------|--------|----------|-------------------|
| **Invocation** | Automatic (Claude decides) | Manual (`/command`) | Automatic (Claude delegates) |
| **Location** | `skills/{name}/SKILL.md` | `commands/*.md` | `agents/*.md` |
| **Context** | Injected into conversation | Parameterized templates | Separate context window |
| **Persistence** | Scoped to skill execution | Single command | Task completion |
| **Concurrency** | Sequential | Sequential | Parallel possible |
| **Can Use** | N/A | N/A | Skills AND Commands |
| **Best For** | Portable expertise | Explicit workflows | Complex multi-step tasks |

### 4. SKILL.md Format

```yaml
---
name: Skill Name
description: This skill should be used when the user asks to "specific phrase 1",
  "specific phrase 2". Include exact trigger phrases.
version: 1.0.0
allowed-tools: Read, Grep, Write
context: fork  # Optional: run in forked sub-agent context
agent: specialist  # Optional: specify agent type
---

## Overview
Skill instructions and guidance content...

## Workflow
1. Step one
2. Step two

## Examples
Example usage scenarios...
```

**Description Best Practice**: Use third-person format with **specific trigger phrases**. Avoid vague descriptions like "Use for hook management" - instead use "This skill should be used when the user asks to 'create a hook', 'add a PreToolUse hook', or mentions hook events."

### 5. Agent Definition Format (agents/*.md)

```yaml
---
name: agent-name
description: Use this agent when the user asks to "perform X", "analyze Y".
  <example>User: "Review this code for security issues"</example>
  <example>User: "Help me architect this feature"</example>
model: inherit  # or specific model
color: blue  # Visual distinction
tools:
  - Read
  - Grep
  - Write
---

You are a specialized agent for [domain]. Your responsibilities include:
1. [Specific task]
2. [Specific task]

## Methodology
...

## Output Format
...
```

**Best Practices**:
- Include 2-4 concrete `<example>` blocks
- Use `model: inherit` unless specific model needed
- Apply principle of least privilege for tools
- Use different colors for multiple agents

### 6. Hook Configuration (hooks/hooks.json)

```json
{
  "PreToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Validate file write safety"
        },
        {
          "type": "command",
          "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh",
          "timeout": 30
        }
      ]
    }
  ],
  "PostToolUse": [
    {
      "matcher": "Edit",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Analyze edit result for potential issues"
        }
      ]
    }
  ],
  "Stop": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Verify task completion: tests run, build succeeded"
        }
      ]
    }
  ],
  "SessionStart": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "command",
          "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/init.sh",
          "timeout": 10
        }
      ]
    }
  ]
}
```

**Hook Events**: `PreToolUse`, `PostToolUse`, `Stop`, `SessionStart`

**Hook Types**: `prompt` (LLM evaluation) or `command` (script execution)

### 7. Migration from Standalone to Plugin

```bash
# 1. Create plugin structure
mkdir -p my-plugin/.claude-plugin
mkdir -p my-plugin/{skills,commands,agents,hooks}

# 2. Copy existing configurations
cp -r .claude/commands/* my-plugin/commands/
cp -r .claude/agents/* my-plugin/agents/
cp -r .claude/skills/* my-plugin/skills/

# 3. Create plugin.json
cat > my-plugin/.claude-plugin/plugin.json << 'EOF'
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "Migrated from standalone configuration"
}
EOF

# 4. Migrate hooks from settings.json to hooks.json
# Copy hooks object from .claude/settings.json to my-plugin/hooks/hooks.json

# 5. Remove original files to avoid duplicates
# Plugin version takes precedence when loaded
```

---

## L2: Architectural Analysis

### 2.1 Skills Architecture (Deep Dive)

Skills operate through a **prompt expansion and context modification** pattern rather than direct execution. Key architectural insights:

**Skill Tool Meta-Architecture:**
- Claude receives a formatted list of all available skills in the Skill tool's description
- Selection is **pure LLM-based reasoning**, not algorithmic pattern matching
- No classification models involved - Claude's language model determines skill match

**Message Injection Pattern:**
When invoked, skills inject two user messages:
1. **Metadata message** (visible): Status indicators for user
2. **Hidden skill prompt** (`isMeta: true`): Detailed instructions for Claude

This dual-message approach prevents UI clutter while providing comprehensive workflow guidance.

**Execution Context Modification:**
- **Conversation Context**: Injected `isMeta: true` messages guide reasoning
- **Execution Context**: Pre-approved tools and optional model switching
- Tool permissions are **scoped to skill execution** - restrictions lift after completion

**Token Budget**: Default 15,000 characters for skill descriptions to prevent context overflow.

### 2.2 When to Use Each Component

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Decision Tree: Skills vs Commands vs Agents       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   Need explicit, manual trigger?                                    │
│     YES → Use COMMAND (/command syntax)                             │
│     NO  ↓                                                           │
│                                                                     │
│   Need autonomous multi-step work with separate context?            │
│     YES → Use AGENT (subagent)                                      │
│     NO  ↓                                                           │
│                                                                     │
│   Need portable expertise auto-invoked by Claude?                   │
│     YES → Use SKILL                                                 │
│     NO  → Consider CLAUDE.md for simpler context                    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Performance Consideration**: Tool-based mechanisms (skills, subagents) have **2-3x latency overhead** vs. direct injection (slash commands, CLAUDE.md). Choose based on whether autonomous invocation justifies cost.

**Context Isolation**: Subagent context isolation is **absolute**. No automatic sharing of main conversation context. Be explicit in delegation prompts.

### 2.3 Hierarchy and Composition

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Architecture Hierarchy                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   AGENTS (Standalone entities)                                      │
│      │                                                              │
│      ├─── CAN EXECUTE → SKILLS                                      │
│      │                    │                                         │
│      │                    └─── CONTAIN → COMMANDS (in workflows/)   │
│      │                                                              │
│      └─── CAN EXECUTE → COMMANDS (directly)                         │
│                                                                     │
│   Key: Agents execute both; Skills contain commands; Commands are   │
│        leaf nodes in the execution tree.                            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.4 Plugin Discovery Mechanism

Skills and plugins load from multiple sources with priority:

1. **Plugin-provided** (highest priority when enabled)
2. **Project settings** (`.claude/skills/`)
3. **User configuration** (`~/.claude/skills/`)
4. **Built-in skills** (lowest priority)

**Auto Hot-Reload (v2.1.0+)**: Skills in `~/.claude/skills` or `.claude/skills` are immediately available without restart.

### 2.5 Security and Trust Model

**Plugin Trust**: Anthropic does not verify third-party plugins. Users must trust plugins before installation.

**Tool Permissions**: Apply principle of least privilege:
```yaml
# Good: Minimal tools
tools:
  - Read
  - Grep

# Bad: Overly permissive
tools:
  - "*"
```

**Hook Security Patterns**:
- PreToolUse hooks for validation before writes
- Security scans via command hooks
- Permission validation at SessionStart

### 2.6 Deprecation Timeline (2025-2026)

| Version | Change | Impact |
|---------|--------|--------|
| v2.1.3 | Skills and slash commands merged | Simplified mental model |
| v2.0.82 | Tool renaming (View → Read, LSTool → LS) | Update tool references |
| v2.0.49 | MCP scope terminology changed | "project" → "local", "global" → "user" |
| v2.0.30 | Custom ripgrep config removed | Use default search behavior |
| v2.0.64+ | Rules system introduced | New `.claude/rules/` directory |

**SDK Migration**: Legacy SDK entrypoint removed. Use `@anthropic-ai/claude-agent-sdk`.

---

## 5W1H Analysis

### WHO
- **Creator**: Anthropic (official Claude Code team)
- **Authoritative Sources**:
  - Anthropic documentation (docs.anthropic.com, code.claude.com)
  - GitHub repository (github.com/anthropics/claude-code)
  - Anthropic engineering blog

### WHAT
- **Plugin**: A bundled collection of Skills, Commands, Agents, Hooks, and MCP servers
- **Skill**: Auto-invoked knowledge module with SKILL.md definition
- **Command**: User-initiated workflow via `/command` syntax
- **Agent**: Autonomous subprocess with separate context window
- **Hook**: Event handler for lifecycle events (PreToolUse, PostToolUse, Stop, SessionStart)

### WHERE
- **User-level**: `~/.claude/` directory
- **Project-level**: `.claude/` directory in repository root
- **Plugin-level**: Custom plugin directory with `.claude-plugin/plugin.json`

### WHEN
- **Skills (Oct 2025)**: Introduced with auto-invocation pattern
- **Plugins (Late 2025)**: Full plugin system with marketplace
- **Hot-Reload (v2.1.0)**: Immediate skill availability
- **Merger (v2.1.3)**: Skills and commands unified

### WHY
- **Separation of Concerns**: Different invocation patterns for different use cases
- **Portability**: Skills as shareable expertise packages
- **Team Consistency**: Plugins ensure same tools for all team members
- **Explicit Control**: Commands for predictable, manual workflows
- **Autonomy**: Agents for complex, multi-step independent work

### HOW
- **Discovery**: Claude scans plugin directories, loads manifests
- **Registration**: Components auto-discovered by directory convention
- **Invocation**:
  - Skills: LLM reasoning matches description to user intent
  - Commands: Explicit `/command` syntax
  - Agents: Claude delegates based on description + examples

---

## Recommendations for Jerry Framework

Based on this research, the following recommendations apply to the Jerry agents cleanup project:

1. **Migrate to Plugin Structure**: Convert current `.claude/agents/` to a proper plugin with manifest
2. **Use Skills for Portable Expertise**: Convert agent capabilities that should auto-invoke to skills
3. **Use Commands for Explicit Workflows**: Keep `/command` pattern for deliberate user-initiated actions
4. **Apply Hook Security**: Add PreToolUse validation hooks for Write/Edit operations
5. **Follow Naming Conventions**: kebab-case for directories/files, specific trigger phrases in descriptions
6. **Version Control**: Use semantic versioning in plugin.json, treat plugins as first-class dependencies

---

## Sources

### Primary (Anthropic Official)

1. [Create Plugins - Claude Code Docs](https://code.claude.com/docs/en/plugins) - Official plugin creation guide
2. [Plugins Reference - Claude Code Docs](https://code.claude.com/docs/en/plugins-reference) - Technical reference
3. [Claude Code Plugins README - GitHub](https://github.com/anthropics/claude-code/blob/main/plugins/README.md) - Official repository documentation
4. [Claude Code Best Practices - Anthropic Engineering](https://www.anthropic.com/engineering/claude-code-best-practices) - Anthropic engineering blog
5. [Claude Code CHANGELOG - GitHub](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md) - Version history and deprecations
6. [Agent Skills - Claude Code Docs](https://code.claude.com/docs/en/skills) - Skills documentation
7. [Create Custom Subagents - Claude Code Docs](https://docs.anthropic.com/en/docs/claude-code/sub-agents) - Subagent guide
8. [Hooks Reference - Claude Code Docs](https://docs.anthropic.com/en/docs/claude-code/hooks) - Hooks documentation

### Secondary (Community Analysis)

9. [Claude Agent Skills: A First Principles Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/) - Technical architecture analysis
10. [Understanding Claude Code: Skills vs Commands vs Subagents vs Plugins](https://www.youngleaders.tech/p/claude-skills-commands-subagents-plugins) - Component comparison
11. [When to Use Skills vs Commands vs Agents - Daniel Miessler](https://danielmiessler.com/blog/when-to-use-skills-vs-commands-vs-agents) - Decision framework
12. [Claude Code Customization Guide - alexop.dev](https://alexop.dev/posts/claude-code-customization-guide-claudemd-skills-subagents/) - Practical guide
13. [Reverse Engineering Claude Code - Level Up Coding](https://levelup.gitconnected.com/reverse-engineering-claude-code-how-skills-different-from-agents-commands-and-styles-b94f8c8f9245) - Architecture analysis

### Context7 Documentation Sources

14. [Claude Code Context7 Library](https://context7.com/anthropics/claude-code) - Aggregated documentation with 800+ code snippets

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-01-12 | ps-researcher | Initial research document |
