# Research: Claude Code Plugin .claude Folder Loading Behavior

> **PS ID:** PROJ-009-oss-release
> **Entry ID:** EN-202-research-001
> **Topic:** Does `.claude/rules/` in a Plugin Get Loaded for End Users?
> **Workflow:** en202-rewrite-20260201-001
> **Agent:** ps-researcher
> **Date:** 2026-02-02
> **Requested By:** User (gap analysis follow-up)

---

## Executive Summary (L0 - ELI5)

**Question:** If we put `.claude/rules/` in our Jerry plugin, will users get those rules automatically?

**Answer: NO.** When a user installs a plugin, only the plugin components (skills, hooks, agents, commands) are loaded. The `.claude/` folder is **project-level memory** for the developer/maintainer of the repository, NOT a distributable component of plugins.

**Analogy:** Think of it like a house blueprint (`.claude-plugin/`) vs. the architect's personal notes (`.claude/`). When you buy the blueprint, you get the house design, not the architect's sticky notes about their preferences.

---

## Technical Implementation Details (L1 - Engineer)

### 1. Plugin vs Project Structure

**Plugin Directory Structure** (what gets distributed):

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
└── README.md                # Plugin documentation
```

**Project Memory Structure** (developer-only, NOT distributed):

```
project-root/
├── .claude/
│   ├── settings.json        # Project-scope settings
│   ├── settings.local.json  # Local settings (gitignored)
│   └── rules/               # Project-level memory (rules)
│       ├── coding-standards.md
│       └── custom-rules.md
└── ...
```

### 2. What Gets Loaded When a User Installs a Plugin

| Component | Location | Loaded for Users? | Notes |
|-----------|----------|-------------------|-------|
| `plugin.json` | `.claude-plugin/` | ✅ Yes | Required manifest |
| `commands/` | Plugin root | ✅ Yes | Slash commands |
| `agents/` | Plugin root | ✅ Yes | Agent definitions |
| `skills/` | Plugin root | ✅ Yes | Skills auto-loaded |
| `hooks/` | Plugin root | ✅ Yes | Event handlers |
| `.mcp.json` | Plugin root | ✅ Yes | MCP server configs |
| `.lsp.json` | Plugin root | ✅ Yes | LSP configs |
| **`.claude/`** | Project root | ❌ **NO** | Developer memory only |
| **`.claude/rules/`** | Project root | ❌ **NO** | Developer memory only |
| **`.claude/patterns/`** | N/A | ❌ **NO** | Not a standard path |

### 3. Settings Scope Hierarchy

Claude Code uses a tiered settings system, but this is for **settings.json**, NOT rules:

| Scope | Settings File | Purpose |
|-------|---------------|---------|
| `user` | `~/.claude/settings.json` | Personal settings (default) |
| `project` | `.claude/settings.json` | Team settings (via VCS) |
| `local` | `.claude/settings.local.json` | Project-specific, gitignored |
| `managed` | `managed-settings.json` | Enterprise-managed (read-only) |

**Key Insight:** The `.claude/` folder at project scope is intended for **repository-specific configuration**, not plugin distribution.

### 4. Plugin Caching Behavior

From the research:

> "Claude Code copies plugins to a cache directory rather than using them in-place."

**Implications:**
1. Plugin contents are copied to `~/.claude/plugin-cache/` (or similar)
2. Only files within the plugin directory structure are copied
3. Project-level `.claude/` folder is NOT part of the plugin directory
4. No mechanism exists to "inject" rules into user's `.claude/rules/`

### 5. Evidence from Context7 Research

**Finding 1:** Plugin structure explicitly excludes `.claude/`:
> "Components MUST be at plugin root level, not nested inside `.claude-plugin/`. Only `plugin.json` belongs in `.claude-plugin/`."

**Finding 2:** Rules are for project memory:
> "`.claude/rules/` directory can contain .md files with additional context... Symlinks can be used to share rules across projects."

**Finding 3:** No mention of plugin-to-user rule distribution:
The plugin documentation contains NO mechanism for distributing `.claude/rules/` to end users.

---

## Strategic Implications (L2 - Architect)

### 1. Architectural Constraint

**One-Way Door Decision:** The `.claude/rules/` system was designed for project-level memory, not cross-project distribution. This is an intentional design choice by Anthropic.

**Trade-offs:**

| Benefit | Cost |
|---------|------|
| Project isolation | Cannot auto-distribute rules to users |
| Security (no rule injection) | Users must manually configure rules |
| Explicit control | More setup friction for OSS adopters |

### 2. Options for Jerry Framework Distribution

Given this constraint, we have three options for distributing Jerry's behavioral rules:

#### Option A: Skills as Rule Carriers (Recommended)

Put behavioral guidance **inside SKILL.md files** instead of `.claude/rules/`:

```
skills/
└── worktracker/
    ├── SKILL.md              # Includes behavioral instructions
    └── rules/                # Reference documentation (loaded on-demand)
        └── entity-rules.md
```

**Pros:**
- Skills ARE distributed via plugins
- Skills are auto-loaded when invoked
- Natural place for behavioral guidance

**Cons:**
- Larger SKILL.md files
- Instructions only apply when skill is active

#### Option B: CLAUDE.md as Instruction Carrier

Keep critical instructions in CLAUDE.md, which users copy/customize:

```
CLAUDE.md (in repo root)
- Identity section
- Navigation pointers
- Critical constraints (inline)
- Quick reference
```

**Pros:**
- Single file to copy
- User has full control
- Works with current design

**Cons:**
- Requires manual user action
- Not "install and go"

#### Option C: Bootstrap Script/Command

Create a `/bootstrap` command that sets up `.claude/rules/`:

```bash
/bootstrap --rules --patterns
# Creates:
#   .claude/rules/source-repository.md (symlink or copy)
#   .claude/patterns/ (symlink or copy)
```

**Pros:**
- Explicit user action (security)
- Configurable
- One-time setup

**Cons:**
- Requires implementation
- Additional step for users

### 3. Recommendation

**Hybrid Approach:**

1. **Skills carry behavioral instructions** (Option A) - Primary distribution
2. **CLAUDE.md provides quick reference** (Option B) - For projects using Jerry
3. **Documentation guides rule setup** (EN-205) - For advanced users

This aligns with the current EN-202 CLAUDE.md rewrite strategy:
- CLAUDE.md is lean (80 lines)
- Skills contain detailed behavioral rules
- `.claude/rules/` is for project maintainers (us), not end users

---

## 5W2H Analysis

### What
- `.claude/rules/` in a plugin does **NOT** get loaded for end users
- Plugin components (skills, agents, hooks, commands) ARE loaded

### Why
- Security: Prevents unauthorized rule injection
- Project isolation: Each project controls its own rules
- Explicit design: Rules are project memory, not plugin components

### Who
- Plugin developers: Use `.claude/` for their development workflow
- Plugin consumers: Only receive plugin manifest components
- Jerry users: Must set up `.claude/rules/` manually or via skills

### When
- Plugin install: Only `.claude-plugin/` contents are copied
- Session start: Project `.claude/rules/` loaded (if exists)
- Skill invocation: Skill-specific guidance becomes active

### Where
- Plugins cached: `~/.claude/plugin-cache/` or similar
- Project rules: `project-root/.claude/rules/`
- User rules: `~/.claude/rules/` (user scope, not implemented)

### How
- Skills: Include behavioral guidance in SKILL.md
- Documentation: Guide users to set up rules if needed
- Bootstrap: Consider `/bootstrap` command for advanced setup

### How Much
- Zero automatic rule distribution from plugins
- All rules require explicit user/project setup

---

## Existing Work Items

Based on worktracker search, the following items relate to this research:

| Work Item | Status | Relevance |
|-----------|--------|-----------|
| **EN-004: Claude Code Plugins Research** | COMPLETE | Contains plugin architecture findings |
| **EN-202: CLAUDE.md Rewrite** | COMPLETE | Implemented lean CLAUDE.md strategy |
| **EN-205: Documentation Update** | PENDING | Should include user bootstrap guidance |
| **FEAT-002: CLAUDE.md Optimization** | IN_PROGRESS | Overall optimization feature |

### Gap Identified

**No work item exists for:**
- User `.claude/rules/` bootstrap/onboarding
- `/bootstrap` command implementation
- Rules distribution strategy documentation

**Recommendation:** Create new enabler or spike under EN-205 to address bootstrap guidance.

---

## Conclusion

**Answer to User's Questions:**

1. **Do we have units of work to bootstrap a user's `.claude/rules/` and `.claude/patterns/`?**

   **Partially.** EN-205 includes TASK-002 "Create CLAUDE-MD-GUIDE.md (user onboarding guide)" which could cover this, but there's no dedicated work item for bootstrap tooling or rules distribution strategy.

2. **Does `.claude/` in a plugin get loaded for end users?**

   **No.** Plugin structure explicitly uses `.claude-plugin/` for distribution. The `.claude/` folder is project-level memory that stays with the developer repository and is NOT copied during plugin installation.

---

## References

### Primary Sources

1. [Claude Code Plugins Reference](https://code.claude.com/docs/en/plugins-reference) - Official documentation
2. Context7: `/anthropics/claude-code` - High reputation, 781 code snippets
3. `plugins-best-practices.md` - EN-004 research artifact

### Internal Sources

4. EN-004: Claude Code Plugins Research (COMPLETE)
5. EN-202: CLAUDE.md Rewrite orchestration artifacts
6. FEAT-002: CLAUDE.md Optimization feature documentation

---

*Research artifact generated by ps-researcher agent as part of EN-202 workflow.*
*Date: 2026-02-02*
