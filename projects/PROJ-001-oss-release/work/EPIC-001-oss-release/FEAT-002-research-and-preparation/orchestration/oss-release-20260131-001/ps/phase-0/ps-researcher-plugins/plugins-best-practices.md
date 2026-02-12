# Claude Code Plugins Best Practices Research

> **PS ID:** PROJ-001-oss-release
> **Entry ID:** EN-104
> **Topic:** Claude Code Plugins Research
> **Workflow:** oss-release-20260131-001
> **Phase:** 0 (Divergent Exploration)
> **Agent:** ps-researcher
> **Date:** 2026-01-31

---

## Executive Summary (L0 - ELI5)

Think of Claude Code plugins like **Lego blocks for your AI assistant**. Just as you can add special Lego pieces to give your creation new abilities (wheels to make it roll, wings to pretend it flies), plugins let you add new superpowers to Claude Code.

**Key Takeaways for Non-Technical Stakeholders:**

1. **Plugins are safe by design** - Claude Code asks permission before doing anything important, like a well-trained assistant who checks before touching your files.

2. **Three ways to share plugins:**
   - Personal use (just for you)
   - Team use (shared with your project collaborators)
   - Community use (published for everyone)

3. **Plugins can do four main things:**
   - Add new commands (like `/format-code`)
   - Provide specialized AI helpers (agents)
   - Add knowledge and skills (domain expertise)
   - React to events (like automatically checking code before saving)

4. **Quality matters** - Well-made plugins have clear documentation, proper versioning, and security considerations.

---

## Technical Implementation Details (L1 - Engineer)

### 1. Plugin Architecture

#### 1.1 Directory Structure

The standard Claude Code plugin structure follows a well-defined layout:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Required: Plugin manifest
├── commands/                 # Slash commands (.md files)
├── agents/                   # Subagent definitions (.md files)
├── skills/                   # Agent skills (subdirectories)
│   └── skill-name/
│       └── SKILL.md         # Required for each skill
├── hooks/
│   └── hooks.json           # Event handler configuration
├── .mcp.json                # MCP server definitions
├── .lsp.json                # LSP server configurations (optional)
├── scripts/                 # Helper scripts and utilities
└── README.md                # Plugin documentation
```

**Critical Rule:** Components MUST be at plugin root level, not nested inside `.claude-plugin/`. Only `plugin.json` belongs in `.claude-plugin/`.

**Source:** [Claude Code Plugins Reference](https://code.claude.com/docs/en/plugins-reference)

#### 1.2 plugin.json Schema

The manifest file is the only required file. Complete schema:

```json
{
  "name": "plugin-name",
  "version": "1.2.0",
  "description": "Brief plugin description",
  "author": {
    "name": "Author Name",
    "email": "author@example.com",
    "url": "https://github.com/author"
  },
  "homepage": "https://docs.example.com/plugin",
  "repository": "https://github.com/author/plugin",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "commands": ["./custom/commands/special.md"],
  "agents": "./custom/agents/",
  "skills": "./custom/skills/",
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json",
  "outputStyles": "./styles/",
  "lspServers": "./.lsp.json"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | **Yes** | Unique identifier (kebab-case, no spaces) |
| `version` | string | No | Semantic version (e.g., "2.1.0") |
| `description` | string | No | Brief explanation of plugin purpose |
| `author` | object | No | Author information (name, email, url) |
| `keywords` | array | No | Discovery tags for marketplace |
| `commands` | string\|array | No | Additional command files/directories |
| `agents` | string\|array | No | Additional agent files |
| `skills` | string\|array | No | Additional skill directories |
| `hooks` | string\|object | No | Hook config path or inline config |
| `mcpServers` | string\|object | No | MCP config path or inline config |
| `lspServers` | string\|object | No | LSP server configurations |

**Source:** [Plugins Reference - Schema](https://code.claude.com/docs/en/plugins-reference)

#### 1.3 Plugin Discovery Mechanisms

Claude Code discovers plugins through multiple mechanisms:

1. **Marketplace Installation:**
   ```bash
   /plugin install plugin-name@marketplace-name
   ```

2. **Local Development:**
   ```bash
   cc --plugin-dir /path/to/plugin
   ```

3. **Scope-Based Settings Files:**
   - `~/.claude/settings.json` (user scope - default)
   - `.claude/settings.json` (project scope - shared via VCS)
   - `.claude/settings.local.json` (local scope - gitignored)
   - `managed-settings.json` (managed scope - read-only)

**Source:** [Claude Code Documentation](https://code.claude.com/docs/en/plugins-reference)

### 2. Hook System

#### 2.1 Available Hook Events

| Event | Trigger Point | Use Case |
|-------|--------------|----------|
| `PreToolUse` | Before Claude uses any tool | Validate tool calls, security checks |
| `PostToolUse` | After successful tool execution | React to results, logging |
| `PostToolUseFailure` | After tool execution fails | Error handling, retry logic |
| `PermissionRequest` | When permission dialog shown | Custom permission handling |
| `UserPromptSubmit` | When user submits prompt | Prompt enhancement, context loading |
| `Notification` | When Claude sends notifications | Custom notification handling |
| `Stop` | When Claude attempts to stop | Completion verification |
| `SubagentStart` | When subagent starts | Subagent orchestration |
| `SubagentStop` | When subagent stops | Subagent cleanup |
| `SessionStart` | At session beginning | Context initialization |
| `SessionEnd` | At session end | Cleanup, summary generation |
| `PreCompact` | Before history compaction | State preservation |

#### 2.2 Hook Configuration Format

**hooks.json structure:**

```json
{
  "description": "Security validation hooks",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/validate.py",
            "timeout": 10
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
            "prompt": "Verify task completion: tests run, build succeeded. Return 'approve' to stop or 'block' with reason.",
            "timeout": 30
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
            "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/load-context.sh"
          }
        ]
      }
    ]
  }
}
```

#### 2.3 Hook Types

| Type | Use Case | Example |
|------|----------|---------|
| `command` | Deterministic checks, file operations | `bash ${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh` |
| `prompt` | LLM-driven decision making | `"Evaluate if this bash command is safe..."` |
| `agent` | Complex verification with tools | Agentic verifier with tool access |

**Best Practice:** Use prompt-based hooks for context-aware validation; command hooks for fast, deterministic checks.

**Source:** [Claude Code GitHub - Plugin Dev Skill](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/hook-development/SKILL.md)

### 3. Skills Development

#### 3.1 SKILL.md Frontmatter

Skills require YAML frontmatter with specific trigger phrases:

```yaml
---
name: Hook Management Skill
description: This skill should be used when the user asks to "create a hook", "add a PreToolUse hook", "validate tool use", "implement prompt-based hooks", or mentions hook events (PreToolUse, PostToolUse, Stop).
version: 0.1.0
---

# Skill Title

## Overview
Detailed skill instructions...
```

**Critical:** The description must include **specific trigger phrases** in third-person format. Vague descriptions like "Use this skill when working with hooks" will NOT trigger properly.

**Source:** [Claude Code GitHub - Skill Development](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/skill-development/SKILL.md)

#### 3.2 Skill Structure

```
skills/
├── pdf-processor/
│   ├── SKILL.md          # Required: Main skill definition
│   ├── reference.md      # Optional: Additional documentation
│   └── scripts/          # Optional: Supporting scripts
└── code-reviewer/
    └── SKILL.md
```

### 4. Agent Definitions

#### 4.1 Agent Markdown Format

```markdown
---
description: What this agent specializes in
capabilities: ["task1", "task2", "task3"]
---

# Agent Name

Detailed description of the agent's role, expertise, and when Claude should invoke it.

## Capabilities
- Specific task the agent excels at
- Another specialized capability
- When to use this agent vs others

## Context and examples
Provide examples of when this agent should be used.
```

**Source:** [Claude Code Plugins Reference](https://code.claude.com/docs/en/plugins-reference)

### 5. Development Workflow

#### 5.1 Local Testing

```bash
# Start Claude Code with local plugin
cc --plugin-dir /path/to/plugin

# Trigger skill/command and verify behavior
# Restart Claude Code after changes
```

#### 5.2 Development Tips

1. **Test with plugin installed** - Navigate to plugin directory and run `claude /command-name args`
2. **Verify `${CLAUDE_PLUGIN_ROOT}`** - Add debug output to confirm path expansion
3. **Test across directories** - Ensure consistent behavior from different working directories
4. **Validate resources** - Confirm all required scripts/configs exist

**Source:** [Claude Code GitHub - Command Development](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/command-development/examples/plugin-commands.md)

#### 5.3 Debugging

```bash
# Enable debug mode
claude --debug
```

Debug output shows:
- Plugin loading details
- Manifest validation errors
- Command, agent, hook registration
- MCP server initialization

### 6. Distribution Strategies

#### 6.1 Installation Scopes

| Scope | Settings File | Use Case |
|-------|---------------|----------|
| `user` | `~/.claude/settings.json` | Personal plugins (default) |
| `project` | `.claude/settings.json` | Team plugins (via VCS) |
| `local` | `.claude/settings.local.json` | Project-specific, gitignored |
| `managed` | `managed-settings.json` | Enterprise-managed (read-only) |

#### 6.2 CLI Commands

```bash
# Install with scope
claude plugin install formatter@marketplace --scope project

# Uninstall
claude plugin uninstall formatter@marketplace --scope user

# Enable/Disable without uninstalling
claude plugin enable formatter@marketplace
claude plugin disable formatter@marketplace

# Update
claude plugin update formatter@marketplace
```

#### 6.3 Marketplace Distribution

To create a marketplace:

1. Create a git repository with `.claude-plugin/marketplace.json`
2. Define plugin entries with source paths
3. Users add marketplace: `/plugin marketplace add user-or-org/repo-name`

**marketplace.json Example:**

```json
{
  "name": "company-marketplace",
  "version": "1.0.0",
  "description": "Internal plugin marketplace",
  "owner": {
    "name": "company-name",
    "email": "dev@company.com"
  },
  "plugins": [
    {
      "name": "enterprise-devops",
      "description": "CI/CD automation plugin",
      "source": "./plugins/devops",
      "version": "2.3.1",
      "category": "devops"
    }
  ]
}
```

**Source:** [Anthropic Claude Plugins Official Repository](https://github.com/anthropics/claude-plugins-official)

### 7. Versioning Practices

Follow semantic versioning:

- **MAJOR** - Breaking changes (incompatible API changes)
- **MINOR** - New features (backward-compatible additions)
- **PATCH** - Bug fixes (backward-compatible fixes)

```json
{
  "version": "2.1.0"
}
```

**Best Practices:**
- Start at `1.0.0` for first stable release
- Update version before distributing changes
- Document changes in `CHANGELOG.md`
- Use pre-release versions for testing: `2.0.0-beta.1`

---

## Strategic Implications (L2 - Architect)

### 1. Architecture Trade-offs

#### 1.1 Plugin Caching Strategy

**Design Decision:** Claude Code copies plugins to a cache directory rather than using them in-place.

**Trade-offs:**

| Benefit | Cost |
|---------|------|
| Security isolation | No dynamic file access outside plugin root |
| Reproducible behavior | Path traversal limitations |
| Verification capability | Symlinks required for external dependencies |

**Mitigation Strategies:**
1. Use symlinks for external resources (honored during copy)
2. Restructure marketplace to include all required files
3. Keep plugins self-contained

**Source:** [Plugins Reference - Caching](https://code.claude.com/docs/en/plugins-reference)

#### 1.2 Hook Execution Model

**Design Decision:** Plugin hooks merge with user hooks and execute in parallel.

**Implications:**
- Multiple hooks can react to same event
- No guaranteed ordering between plugin hooks
- Potential for conflicting modifications

**Recommendation:** Design hooks to be idempotent and non-conflicting.

### 2. Performance Implications

#### 2.1 Context Window Impact

**Finding:** Plugins consume system prompt space.

**Recommendation from Anthropic:**
> "Plugins are designed to toggle on and off as needed. Enable them when you need specific capabilities and disable them when you don't to reduce system prompt context and complexity."

**Best Practice:**
- Keep MCP servers under 10 per project
- Disable unused plugins
- Use skill trigger phrases that are specific enough to avoid false positives

**Source:** [Everything Claude Code Best Practices](https://github.com/affaan-m/everything-claude-code)

#### 2.2 Hook Timeout Considerations

| Hook Type | Default Timeout | Recommendation |
|-----------|-----------------|----------------|
| Command | 60 seconds | Set explicit timeout based on expected execution time |
| Prompt | 30 seconds | Keep prompts focused for faster LLM evaluation |
| Agent | Variable | Use iteration limits (`--max-iterations`) |

### 3. Security Analysis (FMEA)

#### 3.1 Risk Assessment

| Failure Mode | Effect | Severity | Probability | Detection | RPN | Mitigation |
|--------------|--------|----------|-------------|-----------|-----|------------|
| Malicious plugin code | Data exfiltration, system compromise | 10 | 3 | 2 | 60 | Trust verification, code review |
| Command injection in hooks | Arbitrary code execution | 9 | 4 | 3 | 108 | Use `${CLAUDE_PLUGIN_ROOT}`, validate inputs |
| Prompt injection in skills | Behavior manipulation | 7 | 5 | 4 | 140 | Sanitize skill content, review trigger phrases |
| MCP server misconfiguration | Tool access escalation | 8 | 4 | 3 | 96 | Only enable trusted servers |
| Stale plugin version | Unpatched vulnerabilities | 6 | 6 | 5 | 180 | Regular updates, version pinning |

**Source:** Derived from [Claude Code Security](https://code.claude.com/docs/en/security)

#### 3.2 Security Best Practices

1. **Trust Verification:**
   - Verify plugin source before installation
   - Review hook scripts and MCP configurations
   - Use project scope for team-reviewed plugins

2. **Sandboxing:**
   - Run Claude Code in containerized environments for sensitive work
   - Use deny lists for risky commands
   - Limit file system access via MCP configuration

3. **Credential Protection:**
   - Never store secrets in plugin files
   - Use environment variables for sensitive configuration
   - Leverage Claude Code's encrypted credential storage

**Source:** [Claude Code Security Documentation](https://code.claude.com/docs/en/security), [MintMCP Blog](https://www.mintmcp.com/blog/claude-code-security)

### 4. One-Way Door Decisions

#### 4.1 Plugin Name

**Permanence:** Plugin names cannot change without breaking existing installations.

**Recommendation:** Choose descriptive, future-proof names following kebab-case convention.

#### 4.2 Component Organization

**Permanence:** Directory structure establishes the plugin's component architecture.

**Recommendation:**
- Plan for extensibility (separate skills vs monolithic commands)
- Consider multi-skill plugins for related capabilities
- Keep agents focused on single responsibility

#### 4.3 Marketplace Structure

**Permanence:** Once published, marketplace structure affects all consumers.

**Recommendation:**
- Use strict mode for controlled updates
- Version marketplace schema
- Plan for backward compatibility

### 5. Integration Patterns

#### 5.1 Plugin Interaction with Core

```
┌─────────────────────────────────────────────────────────────┐
│                      Claude Code Core                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Session   │  │    Tool     │  │     Permission      │  │
│  │   Manager   │  │   Executor  │  │      Manager        │  │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘  │
│         │                │                     │             │
├─────────┼────────────────┼─────────────────────┼─────────────┤
│         │   Hook Events  │                     │             │
│         ▼                ▼                     ▼             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                  Plugin Hook System                      ││
│  │  ┌───────────────┐ ┌────────────────┐ ┌───────────────┐ ││
│  │  │ SessionStart  │ │  PreToolUse    │ │ PostToolUse   │ ││
│  │  │ SessionEnd    │ │ PostToolFailure│ │    Stop       │ ││
│  │  └───────────────┘ └────────────────┘ └───────────────┘ ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
                              │
           ┌──────────────────┼──────────────────┐
           ▼                  ▼                  ▼
    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
    │  Plugin A   │    │  Plugin B   │    │  Plugin C   │
    │ ┌─────────┐ │    │ ┌─────────┐ │    │ ┌─────────┐ │
    │ │ Skills  │ │    │ │ Agents  │ │    │ │  Hooks  │ │
    │ │ Hooks   │ │    │ │  MCP    │ │    │ │Commands │ │
    │ │Commands │ │    │ │ Skills  │ │    │ │ Agents  │ │
    │ └─────────┘ │    │ └─────────┘ │    │ └─────────┘ │
    └─────────────┘    └─────────────┘    └─────────────┘
```

#### 5.2 Capability Extension Patterns

**Pattern 1: Vertical Extension (Domain Expertise)**
- Add skills with domain knowledge
- Provide specialized agents for specific tasks
- Example: Security review plugin with security-reviewer agent

**Pattern 2: Horizontal Extension (Workflow Enhancement)**
- Add hooks for workflow automation
- Provide commands for common operations
- Example: CI/CD plugin with pre-commit hooks

**Pattern 3: Integration Extension (External Systems)**
- Add MCP servers for external tool access
- Provide LSP servers for code intelligence
- Example: Database plugin with query execution MCP

### 6. Documentation Requirements

#### 6.1 Minimum Documentation

| Document | Purpose | Location |
|----------|---------|----------|
| README.md | Plugin overview, installation, usage | Plugin root |
| CHANGELOG.md | Version history, breaking changes | Plugin root |
| plugin.json | Structured metadata | `.claude-plugin/` |

#### 6.2 Recommended Documentation

| Document | Purpose | Location |
|----------|---------|----------|
| SECURITY.md | Security considerations | Plugin root |
| CONTRIBUTING.md | Contribution guidelines | Plugin root |
| LICENSE | Legal terms | Plugin root |
| docs/ | Detailed documentation | Plugin root |

**Source:** [Anthropic Claude Plugins Official](https://github.com/anthropics/claude-plugins-official)

---

## 5W2H Analysis

### What
- Claude Code plugins are modular extensions providing skills, agents, hooks, commands, MCP servers, and LSP servers
- Plugins follow a standardized directory structure with `.claude-plugin/plugin.json` manifest

### Why
- Enable customization without modifying core Claude Code
- Share best practices across teams and organizations
- Automate repetitive workflows and enforce standards

### Who
- Individual developers (personal plugins)
- Engineering teams (project-scoped plugins)
- Organizations (marketplace maintainers)
- Community (open-source plugin authors)

### When
- Use during development for workflow automation
- Install at session start for capability enhancement
- Toggle as needed to optimize context usage

### Where
- Installed at user, project, or local scope
- Distributed via marketplaces or direct installation
- Cached in Claude Code's plugin cache directory

### How
- Create plugin directory with required structure
- Define manifest in `plugin.json`
- Add components (skills, hooks, agents, etc.)
- Test with `--plugin-dir` flag
- Distribute via marketplace or direct path

### How Much
- Minimal overhead for simple plugins
- Context window impact proportional to enabled features
- Hook execution time varies by type (command: fast, prompt: slower)

---

## References and Citations

### Primary Sources (Anthropic Official)

1. [Claude Code Plugins Reference](https://code.claude.com/docs/en/plugins-reference) - Complete technical specification
2. [Claude Code GitHub - Plugins README](https://github.com/anthropics/claude-code/blob/main/plugins/README.md) - Plugin structure documentation
3. [Anthropic Claude Plugins Official](https://github.com/anthropics/claude-plugins-official) - Official plugin marketplace
4. [Claude Code Security](https://code.claude.com/docs/en/security) - Security documentation
5. [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices) - Agentic coding guidance

### Secondary Sources (Community)

6. [Everything Claude Code](https://github.com/affaan-m/everything-claude-code) - Battle-tested configurations (High reputation, Context7)
7. [Claude Code Tools](https://github.com/pchalasani/claude-code-tools) - Hooks and utilities (High reputation, Context7)
8. [Awesome Claude Code](https://github.com/hesreallyhim/awesome-claude-code) - Curated plugin list
9. [Composio Blog - Claude Code Plugin](https://composio.dev/blog/claude-code-plugin) - Workflow improvement guide
10. [MintMCP Blog - Security](https://www.mintmcp.com/blog/claude-code-security) - Enterprise security considerations

### Context7 Library Sources

- `/anthropics/claude-code` - High reputation, 781 code snippets, Benchmark Score: 68.5
- `/affaan-m/everything-claude-code` - High reputation, 649 code snippets, Benchmark Score: 68.5
- `/pchalasani/claude-code-tools` - High reputation, 541 code snippets, Benchmark Score: 55.5

---

## Appendix: Quick Reference

### A. Common Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Plugin not loading | Invalid plugin.json | Validate JSON syntax with `/plugin validate` |
| Commands not appearing | Wrong directory structure | Move to plugin root, not in `.claude-plugin/` |
| Hooks not firing | Script not executable | Run `chmod +x script.sh` |
| MCP server fails | Missing `${CLAUDE_PLUGIN_ROOT}` | Use variable for all plugin paths |
| Path errors | Absolute paths used | All paths must be relative (`./`) |
| LSP executable not found | Binary not installed | Install language server separately |

### B. Environment Variables

| Variable | Purpose |
|----------|---------|
| `${CLAUDE_PLUGIN_ROOT}` | Absolute path to plugin directory |
| `$ARGUMENTS` | Context passed to prompt-based hooks |

### C. Exit Codes (Hook Commands)

| Code | Meaning |
|------|---------|
| 0 | Success - stdout shown in transcript |
| 2 | Error - stderr fed back to Claude |

---

*Document generated by ps-researcher agent as part of PROJ-001-oss-release orchestration workflow.*
