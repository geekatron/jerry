# Claude Code CLI Best Practices Research

> **PS ID:** PROJ-009-oss-release
> **Entry ID:** EN-002
> **Topic:** Claude Code CLI Best Practices Research
> **Workflow:** oss-release-20260131-001
> **Phase:** 0 (Divergent Exploration)
> **Agent:** ps-researcher
> **Created:** 2026-01-31

---

## L0: Executive Summary (ELI5)

Claude Code is Anthropic's AI-powered coding assistant that lives in your terminal. Think of it like having a brilliant developer sitting next to you who can:
- **Read your entire codebase** and understand how everything connects
- **Execute commands** like running tests, building projects, and managing git
- **Remember your preferences** through configuration files called CLAUDE.md
- **Automate workflows** through "hooks" that trigger actions at specific moments

**Key Takeaways for OSS Release:**
1. **Configuration is layered** - Settings flow from user-level to project-level, allowing teams to share standards
2. **Memory is modular** - Rules can be split into focused files for maintainability
3. **Hooks enable automation** - Pre/post actions on tool usage, session events, and more
4. **Context management is critical** - Performance degrades as context fills; use `/compact` and `/clear`
5. **Integration is extensive** - Works with VS Code, JetBrains, GitHub Actions, and MCP servers

---

## L1: Technical Implementation Details

### 1. Claude Code Architecture

#### 1.1 CLI Patterns and Design

Claude Code follows an **agentic architecture** where the CLI acts as an orchestration layer for AI-powered development workflows.

```
Terminal/IDE
     │
     ▼
┌─────────────────────────────────────────────┐
│            Claude Code CLI                   │
├─────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────────┐ │
│  │ Commands│  │ Agents  │  │   Skills    │ │
│  └────┬────┘  └────┬────┘  └──────┬──────┘ │
│       │            │              │         │
│       └────────────┼──────────────┘         │
│                    ▼                        │
│  ┌─────────────────────────────────────┐   │
│  │         Hooks Layer                  │   │
│  │  (PreToolUse, PostToolUse, etc.)    │   │
│  └─────────────────────────────────────┘   │
│                    ▼                        │
│  ┌─────────────────────────────────────┐   │
│  │           Tool Execution             │   │
│  │  (Read, Write, Edit, Bash, Glob...)  │   │
│  └─────────────────────────────────────┘   │
│                    ▼                        │
│  ┌─────────────────────────────────────┐   │
│  │          MCP Servers                 │   │
│  │  (External tool integrations)        │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

**Source:** [Claude Code Overview](https://code.claude.com/docs/en/overview), [Anthropic Claude Code GitHub](https://github.com/anthropics/claude-code)

#### 1.2 Session Management Best Practices

Sessions in Claude Code maintain conversation history and context. Key considerations:

| Aspect | Best Practice | Rationale |
|--------|--------------|-----------|
| Session Start | Use `SessionStart` hook to load context | Provides consistent initialization |
| Session End | Use `SessionEnd` hook to persist state | Enables session continuity |
| Context Clearing | Use `/clear` between unrelated tasks | Prevents context pollution |
| Context Compaction | Use `/compact` with focus instructions | Preserves important context |

**SessionStart Hook Example:**

```json
{
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
```

**Source:** [Claude Code Hooks Reference](https://code.claude.com/docs/en/hooks), [GitButler - Claude Code Hooks](https://blog.gitbutler.com/automate-your-ai-workflows-with-claude-code-hooks)

#### 1.3 Hook System

Claude Code supports multiple hook events that enable deterministic control:

| Hook Event | Trigger Point | Common Use Cases |
|------------|---------------|------------------|
| `SessionStart` | Session begins/resumes | Load context, check prerequisites |
| `SessionEnd` | Session terminates | Persist state, cleanup |
| `UserPromptSubmit` | User submits prompt | Validation, logging, context injection |
| `PreToolUse` | Before tool execution | Safety checks, approvals |
| `PostToolUse` | After tool execution | Formatting, validation, notifications |
| `PostToolUseFailure` | Tool execution fails | Error handling, retries |
| `Stop` | Agent stops | Final verification, cleanup |
| `PreCompact` | Before context compaction | Save critical state |
| `SubagentStart/Stop` | Subagent lifecycle | Resource management |

**Hook Configuration Pattern:**

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "tool == \"Bash\" && tool_input.command matches \"git push\"",
        "hooks": [
          {
            "type": "command",
            "command": "#!/bin/bash\necho '[Hook] Review changes before push...' >&2\nread -r"
          }
        ],
        "description": "Pause before git push to review changes"
      }
    ],
    "PostToolUse": [
      {
        "matcher": "tool == \"Edit\" && tool_input.file_path matches \"\\.(ts|tsx|js|jsx)$\"",
        "hooks": [
          {
            "type": "command",
            "command": "#!/bin/bash\nfile_path=$(echo \"$input\" | jq -r '.tool_input.file_path')\nprettier --write \"$file_path\" 2>&1"
          }
        ],
        "description": "Auto-format JS/TS files with Prettier after edits"
      }
    ]
  }
}
```

**Security Note:** Direct edits to hooks in settings files don't take effect immediately. Claude Code requires review in the `/hooks` menu for changes to apply - this prevents malicious hook modifications.

**Source:** [Hooks Reference - Claude Code Docs](https://code.claude.com/docs/en/hooks), [Everything Claude Code](https://github.com/affaan-m/everything-claude-code)

#### 1.4 Tool Execution Patterns

Claude Code provides built-in tools for code manipulation:

| Tool | Purpose | Safety Level |
|------|---------|--------------|
| `Read` | Read file contents | Safe (no modification) |
| `Write` | Create/overwrite files | Requires permission |
| `Edit` | Modify existing files | Requires permission |
| `Bash` | Execute shell commands | Requires permission |
| `Glob` | Find files by pattern | Safe (no modification) |
| `Grep` | Search file contents | Safe (no modification) |
| `WebFetch` | Fetch web content | May require permission |

**Tool Permission Configuration:**

```bash
# Use /permissions command to manage allowlist
/permissions

# Add specific tools to always allow
Edit                     # Allow file edits
Bash(git commit:*)       # Allow git commits
mcp__puppeteer__*        # Allow all Puppeteer MCP tools
```

**Source:** [Claude Code Best Practices - Anthropic](https://www.anthropic.com/engineering/claude-code-best-practices)

---

### 2. Configuration Best Practices

#### 2.1 settings.json Patterns

Claude Code uses a hierarchical settings system with clear precedence:

```
┌─────────────────────────────────────────────┐
│  Managed Settings (Highest Priority)         │
│  ~/.claude/managed-settings.json             │
│  (Cannot be overridden - org policies)       │
├─────────────────────────────────────────────┤
│  Command Line Arguments                      │
│  --model, --output-format, etc.              │
├─────────────────────────────────────────────┤
│  Local Project Settings                      │
│  .claude/settings.local.json                 │
│  (Personal, git-ignored)                     │
├─────────────────────────────────────────────┤
│  Shared Project Settings                     │
│  .claude/settings.json                       │
│  (Team-shared, checked into git)             │
├─────────────────────────────────────────────┤
│  User Settings (Lowest Priority)             │
│  ~/.claude/settings.json                     │
│  (Global user preferences)                   │
└─────────────────────────────────────────────┘
```

**Project Settings Example (.claude/settings.json):**

```json
{
  "model": "claude-opus-4-5-20251101",
  "allowedTools": ["Edit", "Bash(git:*)"],
  "ignorePatterns": ["node_modules/", "*.lock", "dist/"],
  "hooks": {
    "PreToolUse": [...],
    "PostToolUse": [...]
  },
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

**Source:** [Settings Precedence - Claude Code Docs](https://code.claude.com/docs/en/iam)

#### 2.2 .claude Directory Structure

Standard Claude Code project structure:

```
project-root/
├── .claude/
│   ├── settings.json          # Team settings (git-tracked)
│   ├── settings.local.json    # Personal settings (git-ignored)
│   └── rules/                 # Modular rule files
│       ├── frontend/
│       │   ├── react.md
│       │   └── styles.md
│       ├── backend/
│       │   ├── api.md
│       │   └── database.md
│       └── general.md
├── CLAUDE.md                   # Main project memory (recommended)
└── CLAUDE.local.md             # Personal overrides (git-ignored)
```

**Source:** [Modular Rules in Claude Code](https://claude-blog.setec.rs/blog/claude-code-rules-directory), [Manage Claude's Memory](https://code.claude.com/docs/en/memory)

#### 2.3 Rule Files Organization

Rules can be conditionally applied using YAML frontmatter with glob patterns:

**Path-Specific Rule Example (.claude/rules/frontend/react.md):**

```markdown
---
paths:
  - "src/components/**/*.tsx"
  - "src/pages/**/*.tsx"
---

# React Component Standards

## Component Structure
- Use functional components with hooks
- Props interface above component definition
- Export named components (not default)

## State Management
- Use React Query for server state
- Use Zustand for client state
- Avoid prop drilling > 2 levels

## Testing
- Co-locate tests with components
- Use React Testing Library
- Test behavior, not implementation
```

**Source:** [Modular Rules - Claude Code Docs](https://code.claude.com/docs/en/memory)

#### 2.4 Pattern Catalogs

For complex projects, maintain a pattern catalog that skills and commands can reference:

```
.claude/
└── patterns/
    ├── PATTERN-CATALOG.md       # Index of all patterns
    ├── architecture/
    │   ├── hexagonal.md
    │   └── cqrs.md
    ├── testing/
    │   ├── unit-test.md
    │   └── integration-test.md
    └── security/
        └── authentication.md
```

**Source:** [Claude Code Handbook](https://github.com/nikiforovall/claude-code-rules)

---

### 3. Integration Patterns

#### 3.1 IDE Integration

**VS Code Extension:**

The VS Code extension provides a native graphical interface with features:
- Review and edit Claude's plans before accepting
- Auto-accept edits as they're made
- @-mention files with specific line ranges
- Access conversation history
- Open multiple conversations in tabs

**Permission Modes:**
- **Normal mode:** Claude asks permission for each action
- **Plan mode:** Claude describes actions, waits for approval
- **Auto-accept mode:** Claude makes edits without asking

**JetBrains Integration:**

Supported in: IntelliJ, PyCharm, Android Studio, WebStorm, PhpStorm, GoLand

```bash
# Install JetBrains plugin
claude integrations install jetbrains
```

**Source:** [VS Code Integration - Claude Code Docs](https://code.claude.com/docs/en/vs-code)

#### 3.2 Git Hook Integration

**Pre-commit Hook Example:**

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Run Claude for code review
claude -p "Review staged changes for issues" --output-format json \
  | jq -e '.issues | length == 0' \
  || { echo "Issues found. Aborting commit."; exit 1; }
```

**Headless Mode for Automation:**

```bash
# One-off queries
claude -p "Explain what this project does"

# Structured output for scripts
claude -p "List all API endpoints" --output-format json

# Stream output for real-time processing
claude -p "Analyze this log file" --output-format stream-json
```

**Source:** [Best Practices - Claude Code Docs](https://code.claude.com/docs/en/best-practices)

#### 3.3 CI/CD Integration (GitHub Actions)

**Claude Code Action Setup:**

```yaml
# .github/workflows/claude-review.yml
name: Claude Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write

    steps:
      - uses: actions/checkout@v4

      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          mode: review

      - name: Post Review Comments
        uses: actions/github-script@v7
        with:
          script: |
            // Post Claude's review as PR comments
```

**Easy Setup via CLI:**

```bash
# Interactive setup wizard
/install-github-app
```

**Security Best Practices:**
- Always use GitHub Secrets for API keys
- Limit action permissions to minimum required
- Create CLAUDE.md for CI/CD context

**Source:** [Claude Code Action GitHub](https://github.com/anthropics/claude-code-action), [Integrating with GitHub Actions](https://stevekinney.com/courses/ai-development/integrating-with-github-actions)

#### 3.4 MCP Server Integration

MCP (Model Context Protocol) enables Claude Code to connect with external services.

**Configuration Scopes:**
- **Local:** `~/.claude.json` (personal, project-specific)
- **Global:** Shared across all projects

**MCP Server Configuration Example:**

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "kubernetes": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/servers/kubernetes-mcp/index.js"],
      "env": {
        "KUBECONFIG": "${KUBECONFIG}",
        "K8S_NAMESPACE": "${K8S_NAMESPACE:-default}"
      }
    },
    "api-service": {
      "type": "http",
      "url": "https://api.example.com/mcp",
      "headers": {
        "Authorization": "Bearer ${API_TOKEN}"
      }
    }
  }
}
```

**Debugging MCP:**

```bash
# Debug MCP configuration issues
claude --mcp-debug
```

**Source:** [MCP Integration - Claude Code Docs](https://code.claude.com/docs/en/mcp), [Top 10 MCP Servers](https://apidog.com/blog/top-10-mcp-servers-for-claude-code/)

---

### 4. Performance Optimization

#### 4.1 Context Management

**The Problem:** As context windows fill, LLM performance degrades. Models become less precise and prone to errors near token limits.

**Key Insight:** LLMs have an "attention budget" - every token attends to every other token (n^2 relationships).

**Context Management Commands:**

```bash
# Check current context usage
/context

# Reset context between unrelated tasks
/clear

# Compact context with focus instructions
/compact Focus on the API changes

# Check per-server MCP costs
/mcp

# Check token usage
/cost
```

**CLAUDE.md Compaction Instructions:**

```markdown
# Compact Instructions

When compacting, please:
- Preserve the full list of modified files
- Keep all test commands and their results
- Maintain key architectural decisions
- Focus on code samples and API usage
```

**Source:** [Context Management - Claude Code Handbook](https://github.com/nikiforovall/claude-code-rules), [Best Practices - Claude Code Docs](https://code.claude.com/docs/en/best-practices)

#### 4.2 Token Optimization Strategies

| Strategy | Token Savings | Implementation |
|----------|---------------|----------------|
| Use `/clear` between tasks | 50-70% | Simple habit change |
| Modular CLAUDE.md | Up to 60% | Split into rules/ files |
| Skills for specialized tasks | Up to 97% | Load-on-demand patterns |
| Tool Search (new feature) | ~47% | Automatic in latest versions |
| Tiered context loading | ~60% | 3-tier architecture |

**Tiered Context Pattern:**

```
Tier 1: Core Rules (always loaded)
├── Project overview
├── Critical conventions
└── Essential commands

Tier 2: Domain Rules (conditionally loaded via paths:)
├── Frontend patterns
├── Backend patterns
└── Testing patterns

Tier 3: Skills (loaded on-demand via /skill)
├── Code review skill
├── Deployment skill
└── Migration skill
```

**Source:** [Token Management 2026](https://richardporter.dev/blog/claude-code-token-management), [Optimize Claude Code Context by 60%](https://medium.com/@jpranav97/stop-wasting-tokens-how-to-optimize-claude-code-context-by-60-bfad6fd477e5)

#### 4.3 Session Efficiency

**Pattern: Clear and Catch Up**

```bash
# 1. Clear the state
/clear

# 2. Run catchup command to reload context
/catchup  # Custom command that reads git diff and relevant files

# 3. Continue work with fresh context
```

**Pattern: Progress Persistence**

```markdown
<!-- .claude/progress.md -->
# Current Task Progress

## Status: IN_PROGRESS
## Last Updated: 2026-01-31

### Completed
- [x] Database schema design
- [x] API endpoints implementation

### In Progress
- [ ] Frontend integration

### Decisions Made
- Using REST over GraphQL for simplicity
- PostgreSQL for primary database
```

Then use SessionStart hook to load this file.

**Source:** [How I Use Every Claude Code Feature](https://blog.sshh.io/p/how-i-use-every-claude-code-feature)

---

### 5. Plugin Architecture

#### 5.1 Plugin Directory Structure

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Required: Plugin manifest
├── commands/                 # Slash commands (.md files)
├── agents/                   # Subagent definitions (.md files)
├── skills/                   # Agent skills (subdirectories)
│   └── skill-name/
│       ├── SKILL.md         # Required for each skill
│       ├── references/      # Reference documentation
│       ├── examples/        # Example code/configs
│       └── scripts/         # Helper scripts
├── hooks/
│   └── hooks.json           # Event handler configuration
├── .mcp.json                 # MCP server definitions
└── scripts/                  # Helper scripts and utilities
```

**Source:** [Plugin Structure - Claude Code](https://github.com/anthropics/claude-code)

#### 5.2 Skills System

Skills provide specialized, load-on-demand capabilities:

**SKILL.md Template:**

```markdown
---
name: code-review
description: Expert code review with security focus
tools: Read, Grep, Glob
model: opus
---

# Code Review Skill

## Purpose
Perform comprehensive code reviews focusing on:
- Security vulnerabilities
- Performance issues
- Code style violations
- Test coverage gaps

## Workflow
1. Identify changed files
2. Analyze each file for issues
3. Generate review report

## Reference
@references/security-checklist.md
@references/style-guide.md
```

**Source:** [Skill Development - Claude Code](https://github.com/anthropics/claude-code)

#### 5.3 Plugin Installation

```bash
# Add official marketplace
claude plugin marketplace add https://github.com/anthropics/claude-plugins-official

# Open plugins browser
/plugins

# Install specific plugins
claude plugin install typescript-lsp@claude-plugins-official
claude plugin install mgrep@mixedbread-ai

# Recommended plugins for development:
# - typescript-lsp: TypeScript intelligence
# - pyright-lsp: Python type checking
# - mgrep: Enhanced search
# - context7: Live documentation lookup
```

**Source:** [Everything Claude Code](https://github.com/affaan-m/everything-claude-code)

---

## L2: Architect-Level Strategic Implications

### 1. Trade-off Analysis

#### 1.1 CLAUDE.md Size vs. Context Efficiency

| Approach | Pros | Cons | Recommendation |
|----------|------|------|----------------|
| Large CLAUDE.md (500+ lines) | Complete context always available | Token waste, context pollution | Avoid |
| Minimal CLAUDE.md (<100 lines) | Token efficient | May miss important context | Use with skills |
| Modular rules/ | Best of both worlds | More files to maintain | **Recommended** |

**Decision Rationale:** The modular approach using `.claude/rules/` directory provides the optimal balance. Rules are:
- Conditionally loaded based on file paths
- Easier to maintain by different team members
- Prevent merge conflicts in team settings

#### 1.2 Hook Complexity vs. Maintainability

| Approach | Use Case | Risk Level |
|----------|----------|------------|
| Simple hooks (logging only) | Audit trails | Low |
| Validation hooks | Safety checks | Medium |
| Complex orchestration hooks | Workflow automation | High |

**Decision Rationale:** Start with simple hooks and evolve. Complex hooks become technical debt quickly.

#### 1.3 MCP Server Count vs. Context Overhead

Each MCP server adds tool definitions to every request. Empirical measurements:

```
0 MCP servers: ~0 tokens overhead
3 MCP servers: ~5-10K tokens overhead
10 MCP servers: ~20-50K tokens overhead
```

**Decision Rationale:** Use `/mcp` to monitor costs. Prefer essential servers only.

### 2. One-Way Door Decisions

These decisions are difficult to reverse once implemented:

| Decision | Impact | Reversibility |
|----------|--------|---------------|
| CLAUDE.md structure | Team adoption, muscle memory | Moderate - requires team retraining |
| Hook architecture | Automation dependencies | Low - breaking changes cascade |
| Plugin dependencies | Workflow integrations | Low - version lock-in risk |
| MCP server choices | Integration complexity | Moderate - can swap servers |

### 3. Performance Implications

#### 3.1 Context Window Utilization

```
┌────────────────────────────────────────────────────────────┐
│                    Context Window (~200K tokens)            │
├────────────────────────────────────────────────────────────┤
│ ████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
│ └─ System Prompt + CLAUDE.md (~5-15K)                      │
│                                                             │
│ ░░░░████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
│      └─ MCP Tool Definitions (~5-20K)                      │
│                                                             │
│ ░░░░░░░░░░░░░░░░██████████████████████░░░░░░░░░░░░░░░░░░░ │
│                  └─ Conversation History (growing)          │
│                                                             │
│ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░████████████████░░░ │
│                                        └─ Working Files     │
│                                                             │
│ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██████ │
│                                                    └─ Free  │
└────────────────────────────────────────────────────────────┘

DANGER ZONE: Avoid using last 20% for memory-intensive tasks
- Performance degrades significantly
- Model accuracy decreases
- Error rates increase
```

**Recommendation:** Monitor with `/context` and proactively `/compact` at 60-70% utilization.

### 4. Design Rationale for OSS Release

#### 4.1 Configuration Hierarchy for OSS

For an OSS project release, structure configuration as:

```
Repository Root
├── CLAUDE.md                      # OSS project overview, contribution guidelines
├── .claude/
│   ├── settings.json              # Team-recommended settings
│   └── rules/
│       ├── contribution.md        # Contribution standards
│       ├── architecture.md        # Architecture patterns
│       └── testing.md             # Testing requirements
└── CLAUDE.local.md.example        # Template for local customization
```

**Rationale:**
1. `settings.json` checked in with safe defaults
2. `settings.local.json` gitignored for personal preferences
3. `CLAUDE.local.md.example` provides template for contributors

#### 4.2 Hook Patterns for OSS

**Recommended Hooks for OSS:**

```json
{
  "PreToolUse": [
    {
      "matcher": "Write && file_path matches \"\\.env\"",
      "hooks": [
        {
          "type": "command",
          "command": "echo 'BLOCKED: Cannot write to .env files' >&2; exit 1"
        }
      ],
      "description": "Prevent secret file modifications"
    }
  ],
  "PostToolUse": [
    {
      "matcher": "Edit && file_path matches \"\\.(py|ts|js)$\"",
      "hooks": [
        {
          "type": "command",
          "command": "# Run linter on changed file\n# Exit 0 to not block, just warn"
        }
      ],
      "description": "Lint after code changes"
    }
  ]
}
```

#### 4.3 Security Considerations

| Risk | Mitigation | Implementation |
|------|------------|----------------|
| Secret exposure | Hook blocking .env writes | PreToolUse hook |
| Malicious hook injection | Review requirement | Built-in `/hooks` review |
| Unsafe bash commands | Command allowlist | `allowedTools` in settings |
| Context pollution | Path-specific rules | YAML frontmatter paths |

---

## Summary Recommendations for OSS Release

### Immediate Actions

1. **Create modular .claude/rules/ structure**
   - Split CLAUDE.md into focused rule files
   - Use path-specific loading for context efficiency

2. **Implement core hooks**
   - SessionStart for context loading
   - PreToolUse for safety checks
   - PostToolUse for formatting/linting

3. **Configure settings.json for team sharing**
   - Safe defaults
   - Recommended allowedTools
   - Essential MCP servers only

### Best Practices Checklist

- [ ] CLAUDE.md under 300 lines
- [ ] Rules organized in .claude/rules/
- [ ] Path-specific rules using YAML frontmatter
- [ ] settings.json with minimal allowedTools
- [ ] Hooks reviewed and approved
- [ ] MCP servers limited to essentials
- [ ] Context management documented
- [ ] Security patterns implemented

---

## Sources and Citations

### Primary Sources (Anthropic Official)

- [Claude Code Overview](https://code.claude.com/docs/en/overview)
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Hooks Reference](https://code.claude.com/docs/en/hooks)
- [Memory Management](https://code.claude.com/docs/en/memory)
- [Settings and IAM](https://code.claude.com/docs/en/iam)
- [MCP Integration](https://code.claude.com/docs/en/mcp)
- [VS Code Integration](https://code.claude.com/docs/en/vs-code)
- [Claude Code GitHub Repository](https://github.com/anthropics/claude-code)
- [Claude Code Action](https://github.com/anthropics/claude-code-action)

### Community Resources (High Reputation)

- [Everything Claude Code](https://github.com/affaan-m/everything-claude-code) - Battle-tested configurations from Anthropic hackathon winner
- [Claude Code Handbook](https://github.com/nikiforovall/claude-code-rules) - Comprehensive recommendations collection
- [GitButler - Claude Code Hooks](https://blog.gitbutler.com/automate-your-ai-workflows-with-claude-code-hooks)
- [Shipyard - Claude Code Cheatsheet](https://shipyard.build/blog/claude-code-cheat-sheet/)
- [Modular Rules Guide](https://claude-blog.setec.rs/blog/claude-code-rules-directory)

### Technical Deep-Dives

- [Token Optimization Strategies](https://medium.com/@jpranav97/stop-wasting-tokens-how-to-optimize-claude-code-context-by-60-bfad6fd477e5)
- [MCP Context Optimization](https://medium.com/@joe.njenga/claude-code-just-cut-mcp-context-bloat-by-46-9-51k-tokens-down-to-8-5k-with-new-tool-search-ddf9e905f734)
- [GitHub Actions Integration](https://stevekinney.com/courses/ai-development/integrating-with-github-actions)
- [Complete Claude Code Guide](https://www.siddharthbharath.com/claude-code-the-complete-guide/)

---

*Research completed: 2026-01-31*
*Agent: ps-researcher*
*Frameworks Applied: 5W2H (What, Why, Who, When, Where, How, How Much), Ishikawa (Root Cause Analysis for Context Degradation)*
