# Plugin Development Playbook

> **Version:** 1.0.0
> **Created:** 2026-01-12
> **Source:** Claude Code official documentation via Context7

---

## Overview

This playbook documents how to develop a Claude Code plugin without duplicating code, including local development workflows, permanent installation options, and gotchas specific to Jerry's project structure.

---

## Table of Contents

1. [Plugin Structure Requirements](#plugin-structure-requirements)
2. [Development Workflow Options](#development-workflow-options)
3. [Jerry Project Structure Analysis](#jerry-project-structure-analysis)
4. [Gotchas and Conflicts](#gotchas-and-conflicts)
5. [Recommended Actions](#recommended-actions)
6. [Quick Reference](#quick-reference)

---

## Plugin Structure Requirements

### Standard Claude Code Plugin Layout

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Required: Plugin manifest
├── commands/                 # Slash commands (.md files) - AUTO-DISCOVERED
├── agents/                   # Subagent definitions (.md files) - AUTO-DISCOVERED
├── skills/                   # Agent skills (subdirectories) - AUTO-DISCOVERED
│   └── skill-name/
│       └── SKILL.md         # Required for each skill
├── hooks/
│   └── hooks.json           # Event handler configuration
├── .mcp.json                # MCP server definitions (optional)
└── scripts/                 # Helper scripts and utilities
```

### Auto-Discovery Mechanism

Claude Code **automatically discovers** components at plugin load time:

| Directory | Discovery Pattern | Registration |
|-----------|-------------------|--------------|
| `commands/` | `*.md` files | `/command-name` |
| `agents/` | `*.md` files | Available as subagents |
| `skills/` | `*/SKILL.md` | Loaded on trigger phrases |
| `hooks/` | `hooks.json` | Event handlers |

**Key Insight**: No manual registration required. Components appear automatically.

### Manifest File

The manifest file **MUST** be named `plugin.json` (not `manifest.json`):

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Brief explanation of plugin purpose",
  "author": {
    "name": "Author Name",
    "email": "author@example.com"
  }
}
```

**Minimal manifest** (only `name` is required):

```json
{
  "name": "jerry"
}
```

---

## Development Workflow Options

### Option 1: `--plugin-dir` Flag (Development)

**Best for**: Active development, quick iteration

```bash
# Load plugin from local directory
claude --plugin-dir ./path/to/plugin

# Load multiple plugins
claude --plugin-dir ./plugin-one --plugin-dir ./plugin-two

# With Jerry specifically
claude --plugin-dir /path/to/jerry
```

**Limitation**: Must specify every time you launch Claude Code.

**Workaround - Shell Alias**:

```bash
# Add to ~/.zshrc or ~/.bashrc
alias cc='claude --plugin-dir /path/to/jerry'
```

---

### Option 2: Local Marketplace (Permanent Installation)

**Best for**: Permanent local installation without publishing

#### Step 1: Create Marketplace Directory

```bash
mkdir -p ~/.claude-marketplaces/jerry-local/.claude-plugin
```

#### Step 2: Create `marketplace.json`

```json
{
  "name": "jerry-local",
  "owner": {
    "name": "Your Name",
    "email": "your@email.com"
  },
  "plugins": [
    {
      "name": "jerry",
      "source": "/absolute/path/to/jerry",
      "description": "Framework for behavior and workflow guardrails"
    }
  ]
}
```

#### Step 3: Add Marketplace via CLI

```bash
/plugin marketplace add ~/.claude-marketplaces/jerry-local
```

#### Step 4: Install Plugin

```bash
/plugin install jerry@jerry-local
```

#### Alternative: Configure in settings.json

Add to `~/.claude/settings.json` (global) or `.claude/settings.json` (project):

```json
{
  "extraKnownMarketplaces": {
    "jerry-local": {
      "source": {
        "source": "directory",
        "path": "/absolute/path/to/marketplace-dir"
      }
    }
  },
  "enabledPlugins": {
    "jerry@jerry-local": true
  }
}
```

---

### Option 3: Project-Scoped Installation

**Best for**: Team projects where plugin lives in repo

```bash
# Install to project scope (creates .claude/plugins/)
/plugin install jerry@jerry-local --scope project

# Install to local scope (gitignored)
/plugin install jerry@jerry-local --scope local
```

---

## Jerry Project Structure Analysis

### Current Structure

```
jerry/
├── .claude/                    # Claude Code PROJECT configuration
│   ├── agents/                 # Agent definitions
│   ├── commands/               # Slash commands
│   ├── hooks/                  # Hook scripts
│   ├── rules/                  # Coding standards
│   ├── patterns/               # Design patterns
│   ├── settings.json           # Project settings
│   └── settings.local.json     # Local overrides
│
├── .claude-plugin/             # Plugin manifest directory
│   └── manifest.json           # ⚠️ Should be plugin.json
│
├── skills/                     # Skills at project root (CORRECT)
│   ├── worktracker/
│   ├── orchestration/
│   ├── problem-solving/
│   └── architecture/
│
├── hooks/                      # Root-level hooks
│   └── hooks.json
│
├── CLAUDE.md                   # Project context
└── AGENTS.md                   # Agent registry
```

### Structure Assessment

| Component | Location | Status | Notes |
|-----------|----------|--------|-------|
| Plugin manifest | `.claude-plugin/manifest.json` | **ISSUE** | Should be `plugin.json` |
| Skills | `skills/` | CORRECT | At plugin root |
| Agents | `.claude/agents/` | **CONFLICT** | Should be at `agents/` |
| Commands | `.claude/commands/` | **CONFLICT** | Should be at `commands/` |
| Hooks | `.claude/hooks/` + `hooks/` | **CONFLICT** | Duplicate directories |
| Settings | `.claude/settings.json` | CORRECT | Project config |

---

## Gotchas and Conflicts

### Gotcha 1: `manifest.json` vs `plugin.json`

**Problem**: Jerry uses `manifest.json` but Claude Code expects `plugin.json`.

**Impact**: Plugin may not be recognized when loaded via `--plugin-dir`.

**Fix**:
```bash
# Rename or create symlink
mv .claude-plugin/manifest.json .claude-plugin/plugin.json
# OR
ln -s manifest.json .claude-plugin/plugin.json
```

---

### Gotcha 2: `.claude/` Serves Dual Purpose

**Problem**: `.claude/` is both:
1. **Project configuration** (settings.json, rules/) - recognized by Claude Code
2. **Plugin components** (agents/, commands/) - expected at plugin root

**Impact**:
- When running in the Jerry repo, `.claude/` works as project config
- When distributing as a plugin, agents/commands in `.claude/` won't auto-discover

**Current Behavior**:
- Your `manifest.json` explicitly lists paths like `.claude/agents/orchestrator.md`
- This works but bypasses auto-discovery (manual registration)

**Auto-Discovery Expectation**:
```
jerry/
├── agents/           # Claude Code expects here for auto-discovery
├── commands/         # Claude Code expects here for auto-discovery
└── .claude/          # Only project settings
```

---

### Gotcha 3: Two Hooks Directories

**Problem**: Hooks exist in two places:
- `hooks/hooks.json` - Plugin-level hooks (at root)
- `.claude/hooks/*.py` - Project-level hook scripts

**Current `manifest.json` references**:
```json
"hooks": {
  "pre_tool_use": ".claude/hooks/pre_tool_use.py",
  "subagent_stop": ".claude/hooks/subagent_stop.py"
}
```

**Impact**: Confusion about which hooks are loaded when.

---

### Gotcha 4: Explicit vs Auto-Discovery

**Problem**: `manifest.json` explicitly registers components:
```json
"skills": [
  {
    "name": "worktracker",
    "entry": "skills/worktracker/SKILL.md"
  }
]
```

But Claude Code's **standard plugin format** auto-discovers from directories.

**Impact**:
- Explicit registration may not be supported (depends on Claude Code version)
- May need to rely solely on auto-discovery

---

### Gotcha 5: Running Claude Code IN the Plugin Directory

**Problem**: When you run `claude` inside the Jerry directory:
1. `.claude/settings.json` is loaded as **project** config
2. If loaded via `--plugin-dir .`, it's ALSO a **plugin**

**Impact**: Double-loading of some configurations.

**Workaround**: Use `--plugin-dir` only when running OUTSIDE the plugin directory.

---

## Recommended Actions

### Immediate (No Breaking Changes)

1. **Create `plugin.json` symlink**:
   ```bash
   cd .claude-plugin
   ln -s manifest.json plugin.json
   ```

2. **Add shell alias for development**:
   ```bash
   # ~/.zshrc
   alias jerry-dev='claude --plugin-dir /path/to/jerry'
   ```

### Short-Term (Minor Restructure)

3. **Create root-level `agents/` and `commands/`** (symlinks):
   ```bash
   # From project root
   ln -s .claude/agents agents
   ln -s .claude/commands commands
   ```

   This enables auto-discovery while maintaining current structure.

### Long-Term (Clean Architecture)

4. **Separate concerns**:
   ```
   jerry/
   ├── .claude/                  # Project config ONLY
   │   ├── settings.json
   │   ├── settings.local.json
   │   └── rules/
   │
   ├── .claude-plugin/
   │   └── plugin.json
   │
   ├── agents/                   # Plugin agents (moved from .claude/)
   ├── commands/                 # Plugin commands (moved from .claude/)
   ├── skills/                   # Already correct
   ├── hooks/
   │   └── hooks.json
   │
   └── scripts/                  # Hook implementations
       ├── pre_tool_use.py
       └── subagent_stop.py
   ```

---

## Quick Reference

### Development Commands

```bash
# Test plugin locally
claude --plugin-dir .

# Multiple plugins
claude --plugin-dir ./jerry --plugin-dir ./other-plugin

# Add local marketplace
/plugin marketplace add ./path/to/marketplace

# Install from local marketplace
/plugin install jerry@jerry-local

# List installed plugins
/plugin list

# Check plugin status
/plugin info jerry@jerry-local
```

### Settings Locations

| Scope | Location | Purpose |
|-------|----------|---------|
| Global | `~/.claude/settings.json` | User-wide settings |
| Project | `.claude/settings.json` | Repo-specific config |
| Local | `.claude/settings.local.json` | Gitignored overrides |
| Plugin | `.claude/plugin-name.local.md` | Plugin state |

### Plugin Component Discovery

| Component | Auto-Discovery Path | Manual Registration |
|-----------|---------------------|---------------------|
| Commands | `commands/*.md` | `plugin.json` commands array |
| Agents | `agents/*.md` | `plugin.json` agents array |
| Skills | `skills/*/SKILL.md` | `plugin.json` skills array |
| Hooks | `hooks/hooks.json` | `plugin.json` hooks object |

---

## References

- [Claude Code Plugins Documentation](https://code.claude.com/docs/en/plugins)
- [Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- [Settings Reference](https://code.claude.com/docs/en/settings)
- [Plugin Development Kit](https://github.com/anthropics/claude-code/tree/main/plugins/plugin-dev)

---

*Playbook Version: 1.0.0*
*Last Updated: 2026-01-12*
*Source: Context7 + Official Claude Code Documentation*
