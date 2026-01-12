# Research: Claude Code Plugins Prior Art

| Metadata | Value |
|----------|-------|
| **Document ID** | proj-003-e-002 |
| **PS ID** | proj-003 |
| **Entry Type** | Research |
| **Topic** | Claude Code Plugins Prior Art |
| **Date** | 2026-01-12 |
| **Author** | ps-researcher (v2.0.0) |
| **Status** | Complete |

---

## L0: Executive Summary

This research documents the evolution and current state of Claude Code plugin ecosystem through analysis of official Anthropic sources, community repositories, and marketplace patterns. The plugin system has matured significantly since October 2025, establishing clear standards that Jerry's agent organization should align with.

**Key Findings:**

1. **Standardized Plugin Structure**: The plugin ecosystem has converged on a canonical directory structure with `.claude-plugin/plugin.json` manifest and component directories (commands/, agents/, skills/, hooks/) at plugin root level.

2. **Skills as the Primary Pattern**: Agent Skills (launched October 16, 2025) have emerged as the dominant pattern for packaging domain expertise. Skills use progressive disclosure, loading metadata at startup and full content on-demand.

3. **Multi-Agent Orchestration**: The orchestrator-worker pattern (Opus 4 coordinating Sonnet 4 subagents) has proven highly effective, with Anthropic's research showing 90.2% improvement over single-agent approaches.

4. **Deprecation Trends**: Legacy patterns include `.claude.json` configuration, `allowedTools`/`ignorePatterns` settings, and Windows `C:\ProgramData\ClaudeCode\` paths. The SDK migrated from `@anthropic-ai/claude-code` to `@anthropic-ai/claude-agent-sdk`.

5. **Marketplace Adoption**: Official marketplace launched December 16, 2025 with 36 curated plugins. Community marketplaces support 130+ agents and 739+ skills across categories.

---

## L1: Technical Summary

### 1. Plugin Ecosystem Evolution Timeline

| Date | Milestone |
|------|-----------|
| **Oct 9, 2025** | Plugin system released |
| **Oct 16, 2025** | Agent Skills specification launched |
| **Oct 2025** | Skills/commands merger in v2.1.3 |
| **Dec 16, 2025** | Official plugin marketplace (36 plugins) |
| **Dec 2025** | Agent Skills spec released as open standard |
| **Dec 2025** | OpenAI adopted same Skills format for Codex CLI |

### 2. Canonical Plugin Directory Structure

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Required: Plugin manifest (ONLY file here)
├── commands/                 # Slash commands (.md files)
│   └── my-command.md        # Filename becomes /my-command
├── agents/                   # Subagent definitions (.md files)
│   └── specialist.md        # Agent with YAML frontmatter
├── skills/                   # Agent skills (subdirectories)
│   └── skill-name/
│       ├── SKILL.md         # Required core file
│       ├── scripts/         # Executable Python/Bash
│       ├── references/      # Context documentation
│       └── assets/          # Templates, static files
├── hooks/
│   └── hooks.json           # Event handlers
├── .mcp.json                # MCP server definitions
├── scripts/                 # Helper utilities
└── README.md
```

**Critical Rules:**
- Component directories MUST be at plugin root, NOT inside `.claude-plugin/`
- Use `${CLAUDE_PLUGIN_ROOT}` for portable path references
- All naming uses kebab-case
- Custom paths supplement defaults, don't replace them

### 3. SKILL.md Specification

```yaml
---
name: my-skill-name
description: Clear description of functionality and when to use
allowed-tools:              # Optional: restrict Claude's tools
  - Read
  - Write
  - Bash
context: fork              # Optional v2.1.0+: run in forked subagent
agent: analyzer            # Optional v2.1.0+: specify agent type
hooks:                     # Optional v2.1.0+: skill-level hooks
  pre-tool-use: hook-name
  post-tool-use: hook-name
---

# Skill Instructions

[Main content Claude follows when skill is active]

## Examples
- Example usage

## Guidelines
- Best practice
```

**Best Practices:**
- Keep SKILL.md under 5,000 words to prevent context overflow
- Use progressive disclosure: metadata -> full skill -> bundled files
- Bundle scripts for deterministic operations
- Reference files loaded via Read tool

### 4. Hook System Patterns

**Event Types:**
- `PreToolUse` - Before tool execution (can block/modify)
- `PostToolUse` - After tool completion
- `UserPromptSubmit` - User submits prompt
- `PermissionRequest` - Permission requested (v2.0.45+)
- `SessionStart` - Session begins/resumes
- `Stop` - Agent finishes responding
- `SubagentStop` - Subagent completes (v1.0.41+)
- `SessionEnd` - Session terminates

**hooks.json Pattern:**
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/scripts/pre-edit.sh",
        "timeout": 5000
      }]
    }],
    "PostToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/scripts/post-bash.py"
      }]
    }]
  }
}
```

**Decision Control (PreToolUse):**
- Exit code 0: Allow operation
- Exit code 2: Deny with error message
- JSON output: `{"decision": "allow|deny|ask", "message": "..."}`

### 5. Subagent Orchestration Patterns

**Built-in Subagents:**
- **Explore**: Read-only codebase search/analysis
- **Plan**: Research for planning (prevents infinite nesting)
- **General-purpose**: Complex multi-step tasks

**Custom Subagent Pattern (agents/*.md):**
```yaml
---
name: code-reviewer
description: Specialized code review agent
model: claude-sonnet-4
allowedTools:
  - Read
  - Grep
  - Glob
disallowedTools:
  - Write
  - Edit
permissionMode: auto
---

# Code Review Agent

You are a specialized code review agent...
```

**Multi-Agent Architecture:**
- Orchestrator (Opus 4) coordinates workers (Sonnet 4)
- 80% of performance variance explained by token usage
- Each subagent operates with isolated context (no pollution)
- Subagents cannot spawn subagents (one level max)

### 6. Popular Community Plugin Patterns

**Categories from Official Marketplace (36 plugins):**
- LSP integrations
- Internal workflow tools
- External service connections

**Community Plugin Categories:**
- DevOps: CI/CD, deployment, monitoring
- Security: Code auditing, vulnerability scanning
- Data: Analysis, visualization, reporting
- Frontend: UI/UX, responsive design, accessibility
- Testing: Automated test generation, coverage
- Documentation: Auto-docs, API specs, tutorials

**Notable Plugins:**
- **ClaudeForge** (117 stars): CLAUDE.md generator aligned with Anthropic practices
- **software-architecture**: Clean Architecture, SOLID patterns
- **aws-skills**: CDK, cost optimization, serverless patterns
- **claude-code-safety-net**: Blocks destructive git/filesystem commands

### 7. Deprecated Patterns to Avoid

| Deprecated | Replacement | Version |
|------------|-------------|---------|
| `.claude.json` | `.claude/settings.json` | v2.0.8+ |
| `allowedTools` setting | Permission rules in settings | v2.0.8+ |
| `ignorePatterns` setting | Deny permissions | v2.0.8+ |
| `@anthropic-ai/claude-code` SDK | `@anthropic-ai/claude-agent-sdk` | v2.0+ |
| `appendSystemPrompt` | `systemPrompt` | v2.1+ |
| Windows `C:\ProgramData\ClaudeCode\` | `C:\Program Files\ClaudeCode\` | v2.1.2 |
| `.claude/skills/` (legacy) | `.github/skills/` (recommended) | v2.1+ |
| Output styles | `--system-prompt-file` or plugins | v2.0.30 (un-deprecated) |

### 8. Configuration File Locations

**settings.json Hierarchy (highest to lowest precedence):**
1. Managed: `/Library/Application Support/ClaudeCode/managed-settings.json` (macOS)
2. Local: `.claude/settings.local.json` (gitignored)
3. Project: `.claude/settings.json` (committed)
4. User: `~/.claude/settings.json` (global)

**CLAUDE.md Locations:**
1. Project root: `./CLAUDE.md`
2. Parent directories (monorepo support)
3. User global: `~/.claude/CLAUDE.md`

**Skills Locations (recommended -> legacy):**
1. `.github/skills/` (project, recommended)
2. `~/.github/skills/` (user, recommended)
3. `.claude/skills/` (project, legacy)
4. `~/.claude/skills/` (user, legacy)

---

## L2: Architectural Analysis

### 1. Plugin System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Claude Code Runtime                          │
├─────────────────────────────────────────────────────────────────┤
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐       │
│  │  System Prompt │  │  Skill Meta  │  │   User Prompt │       │
│  │    (base)      │  │ (name+desc)  │  │               │       │
│  └───────────────┘  └───────────────┘  └───────────────┘       │
│         │                  │                   │                │
│         └──────────────────┼───────────────────┘                │
│                            ▼                                    │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              Skill Selection (LLM Reasoning)                 ││
│  │   - No algorithmic routing                                   ││
│  │   - Pure transformer forward-pass                            ││
│  │   - Selects based on task-skill match                        ││
│  └─────────────────────────────────────────────────────────────┘│
│                            │                                    │
│              ┌─────────────┼─────────────┐                      │
│              ▼             ▼             ▼                      │
│  ┌───────────────┐ ┌───────────────┐ ┌───────────────┐         │
│  │   SKILL.md    │ │   scripts/    │ │  references/  │         │
│  │  (injected)   │ │  (executed)   │ │   (loaded)    │         │
│  └───────────────┘ └───────────────┘ └───────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

**Progressive Disclosure Flow:**
1. **Startup**: Load skill `name` + `description` into system prompt
2. **Selection**: LLM decides relevance (pure reasoning, no routing code)
3. **Activation**: Full SKILL.md loaded via Read tool
4. **Expansion**: Referenced files loaded on-demand
5. **Execution**: Scripts run via Bash, output only returned

### 2. Dual Message Injection Pattern

When a skill activates, Claude injects two messages:

```
User Message 1 (Visible, isMeta: false):
"The 'pdf' skill is loading"

User Message 2 (Hidden, isMeta: true):
[Full 500-5,000 word skill prompt]
```

This separates user transparency from AI context, preventing UI clutter while maintaining comprehensive instructions.

### 3. Multi-Agent Orchestration Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Orchestrator (Opus 4)                        │
│                                                                 │
│  - Maintains overall task context                               │
│  - Decomposes work into subtasks                                │
│  - Coordinates parallel execution                               │
│  - Synthesizes subagent results                                 │
└───────────────────────────┬─────────────────────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            │               │               │
            ▼               ▼               ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│ Subagent A    │ │ Subagent B    │ │ Subagent C    │
│ (Sonnet 4)    │ │ (Sonnet 4)    │ │ (Sonnet 4)    │
│               │ │               │ │               │
│ - Isolated    │ │ - Isolated    │ │ - Isolated    │
│   context     │ │   context     │ │   context     │
│ - Cannot spawn│ │ - Cannot spawn│ │ - Cannot spawn│
│   subagents   │ │   subagents   │ │   subagents   │
└───────────────┘ └───────────────┘ └───────────────┘
```

**Performance Factors (95% of variance):**
- Token usage: 80%
- Tool calls: 10%
- Model choice: 5%

### 4. Hook Lifecycle

```
┌──────────────────────────────────────────────────────────────┐
│                      Session Lifecycle                        │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  SessionStart ─────────────────────────────────────┐         │
│       │                                            │         │
│       ▼                                            │         │
│  UserPromptSubmit                                  │         │
│       │                                            │         │
│       ▼                                            │         │
│  ┌─────────────────────────────────────────┐       │         │
│  │ Tool Loop                               │       │         │
│  │                                         │       │         │
│  │  PermissionRequest ──► allow/deny/ask   │       │         │
│  │       │                                 │       │         │
│  │       ▼                                 │       │         │
│  │  PreToolUse ──► allow/deny/modify       │       │         │
│  │       │                                 │       │         │
│  │       ▼                                 │       │         │
│  │  [Tool Execution]                       │       │         │
│  │       │                                 │       │         │
│  │       ▼                                 │       │         │
│  │  PostToolUse ──► log/analyze/act        │       │         │
│  │       │                                 │       │         │
│  └───────┼─────────────────────────────────┘       │         │
│          │                                         │         │
│          ▼                                         │         │
│  Stop/SubagentStop                                 │         │
│       │                                            │         │
│       ▼                                            │         │
│  SessionEnd ◄──────────────────────────────────────┘         │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### 5. Jerry Alignment Recommendations

Based on prior art analysis, Jerry's agent organization should:

| Current Jerry Pattern | Recommended Alignment |
|----------------------|----------------------|
| `.claude/agents/` | Keep (matches plugin standard) |
| `skills/` at project root | Consider `.github/skills/` for cross-platform |
| Orchestrator agent | Aligns with orchestrator-worker pattern |
| `SKILL.md` format | Adopt official frontmatter schema |
| Single `AGENTS.md` registry | Consider individual `.md` files per agent |
| Hook implementation | Implement `hooks.json` pattern |

**Migration Priority:**
1. **High**: Ensure skills use official SKILL.md frontmatter
2. **High**: Adopt `${CLAUDE_PLUGIN_ROOT}` for portable paths
3. **Medium**: Consider `.github/skills/` location
4. **Medium**: Implement hooks.json for lifecycle events
5. **Low**: Create plugin.json manifest for distribution

---

## Sources

### Official Anthropic Sources
- [Claude Code Plugins README](https://github.com/anthropics/claude-code/blob/main/plugins/README.md)
- [Agent Skills Overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Equipping Agents for the Real World](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [How We Built Our Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [Claude Code CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)

### Community & Documentation
- [Plugin Structure - Claude Plugins Dev](https://claude-plugins.dev/skills/@anthropics/claude-plugins-official/plugin-structure)
- [Claude Agent Skills Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)
- [awesome-claude-code Repository](https://github.com/hesreallyhim/awesome-claude-code)
- [awesome-claude-code-plugins](https://github.com/ccplugins/awesome-claude-code-plugins)
- [Claude Code Plugins Plus Skills](https://github.com/jeremylongshore/claude-code-plugins-plus-skills)
- [Claude Code Workflows](https://github.com/shinpr/claude-code-workflows)
- [Hooks Reference - Claude Code Docs](https://code.claude.com/docs/en/hooks)
- [Settings Configuration Guide](https://www.eesel.ai/blog/settings-json-claude-code)
- [Claude Code Customization Guide](https://alexop.dev/posts/claude-code-customization-guide-claudemd-skills-subagents/)

### Marketplace & Tools
- [Official Plugin Marketplace](https://github.com/anthropics/claude-plugins-official)
- [Claude Code Marketplace](https://claudecodemarketplace.com/)
- [Claude Marketplaces](https://claudemarketplaces.com/)
- [@anthropic-ai/claude-code npm](https://www.npmjs.com/package/@anthropic-ai/claude-code)
- [@anthropic-ai/claude-agent-sdk npm](https://www.npmjs.com/package/@anthropic-ai/claude-agent-sdk)

### Multi-Agent Architecture
- [wshobson/agents - Multi-Agent Orchestration](https://github.com/wshobson/agents)
- [Claude Subagents Complete Guide](https://www.cursor-ide.com/blog/claude-subagents)
- [Multi-Agent Orchestration with Claude Code](https://sjramblings.io/multi-agent-orchestration-claude-code-when-ai-teams-beat-solo-acts/)
- [Claude Flow Agent Orchestration](https://github.com/ruvnet/claude-flow)
